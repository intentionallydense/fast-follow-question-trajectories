#!/usr/bin/env python3
"""Offline, reproducible observation ledger; does not infer authenticated agents.

Run from any directory with Python 3. No third-party dependencies or network calls.
Only exact archived page names and conservative signature tokens are extracted.
Manual identity judgments are deliberately kept outside this script.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata
import zipfile
from datetime import datetime
from xml.etree import ElementTree as ET
from urllib.parse import unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
SIGNATURE = re.compile(r"(?<!\S)--[ \t]+([A-Za-z][A-Za-z0-9_.-]{2,79})(?=[ \t\n.,;:!?]|$)")
COORDINATION = re.compile(r"\b(?:relay|cohort|scaffold|round|R[1-9]|G[1-9]|heartbeat|ahead|cooldown|collaborat\w*|sequence)\b", re.I)
GENERIC = {'source-cache-url-list', 'relay-coordination', 'source-or-unclassified',
           'off_store_unclassified', 'loop-chain-infrastructure', 'probe-test', 'unknown'}


def normalize(s):
    return ' '.join(unicodedata.normalize('NFKC', html.unescape(s)).split())


def claim_skeleton(s):
    """Conservative duplicate flag, not evidence that two authors are identical.

    Removing non-ASCII punctuation catches repeated mojibake without modifying
    quotations. Removing signatures also catches a signature-only rewrite.
    Numeric content is retained, so changed clocks/answers remain distinguishable.
    """
    return ' '.join(re.findall(r'[A-Za-z0-9]+', SIGNATURE.sub('', s))).lower()


def write_csv(name, rows, fields):
    with (OUT / name).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(row[k], ensure_ascii=False) if isinstance(row.get(k), (list, dict)) else row.get(k, '') for k in fields})


def write_jsonl(name, rows):
    with (OUT / name).open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def main():
    with zipfile.ZipFile(ROOT / 'full-wiki-logs.zip') as z:
        checks = {name: hashlib.sha256(z.read(name)).hexdigest() == sha
                  for sha, name in (line.split() for line in z.read('SHA256SUMS').decode().splitlines())}
        assert all(checks.values()), checks
        pages = [json.loads(line) for line in z.read('pages.jsonl').splitlines()]
        revisions = [json.loads(line) for line in z.read('revisions.jsonl').splitlines()]
        labels = [json.loads(line) for line in z.read('labels.jsonl').splitlines()]
    for line, rev in enumerate(revisions, 1):
        rev['source_line'] = line
    by_id = {r['rev_id']: r for r in revisions}
    page_by_id = {p['page_id']: p for p in pages}
    label_names = {x['label'] for x in labels}
    name_to_pages = collections.defaultdict(list)
    for p in pages:
        name_to_pages[p['name']].append(p['page_id'])
    # Exact, longest-first, case-sensitive matching; boundaries prevent partial IDs.
    names = [n for n in name_to_pages if len(n) >= 5]
    page_pattern = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(re.escape(n) for n in sorted(names, key=lambda n: (-len(n), n))) + r')(?![A-Za-z0-9_])')
    signatures = []
    ref_edges = {}
    participation = {}
    sig_page = collections.defaultdict(set)
    signed_coord_pages = set()
    sig_task = collections.defaultdict(list)
    seen_page_lines = collections.defaultdict(set)
    seen_corpus_signed_lines = {}
    refs_unresolved = []
    excluded_mentions = []
    seen_claim_skeletons = collections.defaultdict(dict)
    added_line_total = 0
    fresh_line_total = 0
    no_added_revisions = 0
    for rev in sorted(revisions, key=lambda x: (x['time'], x['page_id'], x['seq'])):
        pid, editor = rev['page_id'], rev['label']
        p = page_by_id[pid]
        key = (pid, editor)
        if key not in participation:
            participation[key] = dict(page_id=pid, editor_label=editor, first_time=rev['time'],
                                      last_time=rev['time'], revision_count=0, source_revision_ids=[])
        part = participation[key]
        part['revision_count'] += 1
        part['last_time'] = rev['time']
        part['source_revision_ids'].append(rev['rev_id'])
        lines = rev['body'].split('\n')
        old = by_id.get(rev['diff_base'])
        old_lines = {normalize(s) for s in old['body'].split('\n')} if old else set()
        old_claims = {claim_skeleton(s) for s in old['body'].split('\n') if SIGNATURE.search(s)} if old else set()
        added = [(i, lines[i]) for h in rev['hunks'] if h['op'] in ('insert', 'replace')
                 for i in range(h['b0'], min(h['b1'], len(lines)))]
        if not added:
            no_added_revisions += 1
        for index, line in added:
            norm = normalize(line)
            if not norm:
                continue
            added_line_total += 1
            # Keep first appearance on a page, excluding unchanged lines in replacement hunks.
            if norm in old_lines or norm in seen_page_lines[pid]:
                continue
            seen_page_lines[pid].add(norm)
            fresh_line_total += 1
            evidence = dict(revision_id=rev['rev_id'], revisions_jsonl_line=rev['source_line'],
                            body_line=index + 1, time=rev['time'], editor_label=editor,
                            excerpt=line[:1400])
            decoded_line = unquote(html.unescape(line))
            signature_spans = [m.span(1) for m in SIGNATURE.finditer(decoded_line)]
            found_names = collections.defaultdict(list)
            for match in page_pattern.finditer(decoded_line):
                found_names[match.group(0)].append(match.span())
            for name in sorted(found_names):
                locations = found_names[name]
                locations = [(a, b) for a, b in locations if not any(sa <= a and b <= sb for sa, sb in signature_spans)]
                strict_markup = bool(re.search(r'\[\[\s*' + re.escape(name) + r'(?:\s|\||\]|$)', decoded_line))
                strict_url = bool(re.search(r'(?:[?&;](?:id|keywords)=|wiki\.cgi\?)' + re.escape(name) + r'(?:[&#;\s\]]|$)', decoded_line))
                contextual = len(name) >= 10 and any(re.search(r'\b(?:page|pages|coordination|coord|mirror|backup|see|poll|read|use|at|on|from|to|relay|hub|thread|board|signal|via|or)[\s:=>"\x27(*\[\]-]*$', decoded_line[max(0, a-75):a], re.I) for a, b in locations)
                if not locations or not (strict_markup or strict_url or contextual):
                    excluded_mentions.append(dict(source_page=pid, mentioned_name=name,
                                                   reason='signature_name_collision' if not locations else 'bare_name_mention_without_explicit_reference_context',
                                                   **evidence))
                    continue
                reference_kind = 'explicit_wiki_link' if strict_markup else 'explicit_wiki_url_reference' if strict_url else 'contextual_named_page_reference'
                options = name_to_pages[name]
                # Explicit wiki/name path wins; otherwise same-wiki reference is preferred.
                explicit = [target for target in options if target in decoded_line]
                same_wiki = [target for target in options if target.startswith(p['wiki'] + '/')]
                if len(explicit) == 1:
                    target, resolution = explicit[0], 'explicit_wiki_path'
                elif len(same_wiki) == 1:
                    target, resolution = same_wiki[0], 'same_wiki_exact_name'
                elif len(options) == 1:
                    target, resolution = options[0], 'unique_archived_name'
                else:
                    refs_unresolved.append(dict(source_page=pid, target_name=name,
                                                candidates=options, **evidence))
                    continue
                if target == pid:
                    continue
                edge_key = (pid, target)
                if edge_key not in ref_edges:
                    ref_edges[edge_key] = dict(source_page=pid, target_page=target,
                                              relation='documented_page_reference',
                                              confidence='text_reference_not_navigation_or_shared_identity',
                                              resolution=resolution, evidence=[])
                ref_edges[edge_key]['evidence'].append(dict(reference_kind=reference_kind, **evidence))
            matches = [m.group(1).rstrip('.-') for m in SIGNATURE.finditer(line)]
            matches = [s for s in matches if s in label_names or re.search(r'[0-9]|[a-z][A-Z]', s)]
            for sig in dict.fromkeys(matches):
                copied = seen_corpus_signed_lines.get((norm, sig))
                skeleton = claim_skeleton(line)
                possible_rewrite = len(skeleton) >= 50 and (skeleton in old_claims or skeleton in seen_claim_skeletons[pid])
                previous_claim = seen_claim_skeletons[pid].get(skeleton)
                sig_id = f'S{len(signatures) + 1:05d}'
                obs = dict(observation_id=sig_id, page_id=pid, signature=sig,
                           publisher_page_family=p['page_family'],
                           publisher_page_cohort=p['page_family_cohort'],
                           coordination_language=bool(COORDINATION.search(line)),
                           signature_matches_editor=(sig == editor),
                           multiple_signatures_in_line=len(set(matches)) > 1,
                           identical_signed_line_seen_before=copied,
                           possible_reencoded_or_signature_only_rewrite=possible_rewrite,
                           previous_claim_observation=previous_claim,
                           status='unverified_signature_observation', **evidence)
                signatures.append(obs)
                if copied is None:
                    seen_corpus_signed_lines[(norm, sig)] = sig_id
                if len(skeleton) >= 50 and skeleton not in seen_claim_skeletons[pid]:
                    seen_claim_skeletons[pid][skeleton] = sig_id
                sig_page[pid].add(sig)
                if obs['coordination_language']:
                    signed_coord_pages.add(pid)
                sig_task[(sig, p['page_family'])].append(obs)
    sigmap = collections.defaultdict(list)
    for obs in signatures:
        sigmap[(obs['editor_label'], obs['signature'])].append(obs)
    mapping_rows = []
    for (editor, sig), obs in sorted(sigmap.items()):
        mapping_rows.append(dict(editor_label=editor, signature=sig, exact_name_match=editor == sig,
                                 observations=len(obs), pages=sorted({o['page_id'] for o in obs}),
                                 first_time=min(o['time'] for o in obs), last_time=max(o['time'] for o in obs),
                                 observation_ids=[o['observation_id'] for o in obs],
                                 interpretation='textual_association_not_identity_merge'))
    incoming = collections.Counter(e['target_page'] for e in ref_edges.values())
    outgoing = collections.Counter(e['source_page'] for e in ref_edges.values())
    per_page_part = collections.defaultdict(list)
    for (pid, editor), part in participation.items():
        per_page_part[pid].append(part)
    thread_rows = []
    for p in pages:
        pid = p['page_id']
        parts = per_page_part[pid]
        flags = ['page_is_not_an_agent_or_run']
        if p['page_family'] in GENERIC:
            flags.append('generic_or_infrastructure_family')
        if p['page_family_cohort']:
            flags.append('page_cohort_is_publisher_metadata_not_writer_identity')
        if any(x['editor_label'] == '' for x in parts):
            flags.append('unlabelled_edits')
        if p['n_recreations']:
            flags.append('recreated_page_may_join_separate_episodes')
        if not incoming[pid] and not outgoing[pid]:
            flags.append('no_extracted_page_reference_not_proof_of_isolation')
        thread_rows.append(dict(page_id=pid, publisher_family=p['page_family'],
                                publisher_family_confidence=p['page_family_confidence'],
                                publisher_page_cohort=p['page_family_cohort'],
                                first_time=min(x['first_time'] for x in parts),
                                last_time=max(x['last_time'] for x in parts), revisions=p['n_revs'],
                                editor_labels=sorted(x['editor_label'] for x in parts),
                                observed_signatures=sorted(sig_page[pid]),
                                signed_coordination_observed=pid in signed_coord_pages,
                                incoming_reference_pages=incoming[pid], outgoing_reference_pages=outgoing[pid],
                                deleted_live=p['deleted_live'], uncertainty_flags=flags))
    # Observation episodes: a sensitivity analysis, never an agent-count estimator.
    episodes = []
    episode_counts = {}
    for gap_hours in [1, 6, 24]:
        groups = []
        for (sig, family), obs in sorted(sig_task.items()):
            clean = [o for o in obs if o['identical_signed_line_seen_before'] is None
                     and not o['possible_reencoded_or_signature_only_rewrite']
                     and not o['multiple_signatures_in_line'] and o['coordination_language']]
            clean.sort(key=lambda o: (o['time'], o['observation_id']))
            current = []
            for o in clean:
                if current and (datetime.fromisoformat(o['time'].replace('Z', '+00:00')) -
                                datetime.fromisoformat(current[-1]['time'].replace('Z', '+00:00'))).total_seconds() > gap_hours * 3600:
                    groups.append((sig, family, current))
                    current = []
                current.append(o)
            if current:
                groups.append((sig, family, current))
        episode_counts[str(gap_hours)] = len(groups)
        if gap_hours == 6:
            for i, (sig, family, obs) in enumerate(groups, 1):
                episodes.append(dict(episode_id=f'O{i:04d}', signature=sig,
                                     publisher_page_family=family, gap_hours=6,
                                     first_time=obs[0]['time'], last_time=obs[-1]['time'],
                                     editor_labels=sorted({o['editor_label'] for o in obs}),
                                     pages=sorted({o['page_id'] for o in obs}),
                                     observation_ids=[o['observation_id'] for o in obs],
                                     uncertainty='Observation block only: copying, reused signatures, page-family ambiguity and identity changes remain unresolved.'))
    edge_rows = []
    for i, (_, edge) in enumerate(sorted(ref_edges.items()), 1):
        edge['edge_id'] = f'T{i:05d}'
        edge_rows.append(edge)
    write_jsonl('signature_observations.jsonl', signatures)
    write_jsonl('thread_connections.jsonl', edge_rows)
    write_jsonl('unresolved_page_references.jsonl', refs_unresolved)
    write_jsonl('excluded_name_mentions.jsonl', excluded_mentions)
    write_jsonl('threads.jsonl', thread_rows)
    write_jsonl('observation_episodes.jsonl', episodes)
    write_csv('editor_signature_links.csv', mapping_rows,
              ['editor_label', 'signature', 'exact_name_match', 'observations', 'pages', 'first_time', 'last_time', 'observation_ids', 'interpretation'])
    write_csv('thread_participation.csv', sorted(participation.values(), key=lambda x: (x['page_id'], x['editor_label'])),
              ['page_id', 'editor_label', 'first_time', 'last_time', 'revision_count', 'source_revision_ids'])
    write_csv('threads.csv', thread_rows,
              ['page_id', 'publisher_family', 'publisher_family_confidence', 'publisher_page_cohort',
               'first_time', 'last_time', 'revisions', 'editor_labels', 'observed_signatures',
               'signed_coordination_observed', 'incoming_reference_pages', 'outgoing_reference_pages', 'deleted_live', 'uncertainty_flags'])
    write_csv('thread_connections.csv', [dict(source_page=e['source_page'], target_page=e['target_page'],
              edge_id=e['edge_id'], relation=e['relation'], confidence=e['confidence'],
              evidence_count=len(e['evidence']), first_revision=e['evidence'][0]['revision_id'],
              first_time=e['evidence'][0]['time'], revisions_jsonl_line=e['evidence'][0]['revisions_jsonl_line'],
              excerpt=e['evidence'][0]['excerpt']) for e in edge_rows],
              ['edge_id', 'source_page', 'target_page', 'relation', 'confidence', 'evidence_count',
               'first_revision', 'first_time', 'revisions_jsonl_line', 'excerpt'])
    family_summary = []
    for family in sorted({p['page_family'] for p in pages}):
        ts = [t for t in thread_rows if t['publisher_family'] == family]
        family_summary.append(dict(family=family, pages=len(ts), revisions=sum(t['revisions'] for t in ts),
                                   editor_labels=len({a for t in ts for a in t['editor_labels'] if a}),
                                   signature_tokens=len({s for t in ts for s in t['observed_signatures']}),
                                   signed_coordination_pages=sum(t['signed_coordination_observed'] for t in ts)))
    write_csv('task_families.csv', family_summary,
              ['family', 'pages', 'revisions', 'editor_labels', 'signature_tokens', 'signed_coordination_pages'])
    # Page-reference graph deliberately contains no same-agent edges.
    ns = 'http://graphml.graphdrawing.org/xmlns'
    ET.register_namespace('', ns)
    graphml = ET.Element(f'{{{ns}}}graphml')
    for attr, typ in [('page_id', 'node'), ('family', 'node'), ('relation', 'edge'), ('evidence_id', 'edge')]:
        ET.SubElement(graphml, f'{{{ns}}}key', {'id': attr, 'for': typ, 'attr.name': attr, 'attr.type': 'string'})
    graph = ET.SubElement(graphml, f'{{{ns}}}graph', {'id': 'archived_page_references', 'edgedefault': 'directed'})
    node_ids = {p['page_id']: f'p{i}' for i, p in enumerate(pages)}
    for p in pages:
        node = ET.SubElement(graph, f'{{{ns}}}node', {'id': node_ids[p['page_id']]})
        for key, value in [('page_id', p['page_id']), ('family', p['page_family'])]:
            ET.SubElement(node, f'{{{ns}}}data', {'key': key}).text = value
    for e in edge_rows:
        edge = ET.SubElement(graph, f'{{{ns}}}edge', {'id': e['edge_id'], 'source': node_ids[e['source_page']], 'target': node_ids[e['target_page']]})
        ET.SubElement(edge, f'{{{ns}}}data', {'key': 'relation'}).text = e['relation']
        ET.SubElement(edge, f'{{{ns}}}data', {'key': 'evidence_id'}).text = e['edge_id']
    ET.ElementTree(graphml).write(OUT / 'thread-map.graphml', encoding='utf-8', xml_declaration=True)
    summary = dict(source_zip_sha256=hashlib.sha256((ROOT / 'full-wiki-logs.zip').read_bytes()).hexdigest(),
                   checksums=checks, archived_pages=len(pages), archived_revisions=len(revisions),
                   editor_page_participations=len(participation),
                   first_appearance_changed_lines=fresh_line_total, changed_lines_examined=added_line_total,
                   revisions_without_insertion_or_replacement=no_added_revisions,
                   signature_observations=len(signatures), distinct_signature_tokens=len({o['signature'] for o in signatures}),
                   editor_signature_pairs=len(mapping_rows),
                   mismatch_observations=sum(not o['signature_matches_editor'] for o in signatures),
                   copied_signed_line_observations=sum(o['identical_signed_line_seen_before'] is not None for o in signatures),
                   possible_reencoded_or_signature_only_rewrite_observations=sum(o['possible_reencoded_or_signature_only_rewrite'] for o in signatures),
                   signed_coordination_pages=len(signed_coord_pages),
                   documented_directed_page_reference_pairs=len(edge_rows),
                   page_reference_evidence_kinds=dict(collections.Counter(ev['reference_kind'] for edge in edge_rows for ev in edge['evidence'])),
                   pages_in_reference_graph=len(set(incoming) | set(outgoing)),
                   unresolved_page_reference_observations=len(refs_unresolved),
                   excluded_bare_name_or_signature_mentions=len(excluded_mentions),
                   coordination_observation_episode_counts_by_gap_hours=episode_counts,
                   important='None of these counts measures independent agents. Do not sum page families or observation episodes as people/processes.')
    (OUT / 'reconstruction_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    # Check referential integrity and population accounting; these are data-audit checks.
    assert len(thread_rows) == 4579
    assert sum(x['revision_count'] for x in participation.values()) == len(revisions)
    assert all(o['revision_id'] in by_id and o['page_id'] in page_by_id for o in signatures)
    assert all(e['source_page'] in page_by_id and e['target_page'] in page_by_id for e in edge_rows)
    assert all(by_id[o['revision_id']]['body'].split('\n')[o['body_line']-1].startswith(o['excerpt']) for o in signatures)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
