"""Publish only batches whose independent audit/resolution gate is open, to local artifacts."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
with zipfile.ZipFile(OUT.parent.parent / 'full-wiki-logs.zip') as archive:
    revisions = {r['rev_id']: (i, r) for i, r in enumerate(map(json.loads, archive.read('revisions.jsonl').splitlines()), 1)}
result, candidate_status, audit_refs, held_candidates = [], [], [], []
for folder in sorted((OUT / 'batches').iterdir()):
    validation = folder / 'validation.json'
    if not validation.exists() or json.loads(validation.read_text())['next_batch_gate'] != 'open':
        continue
    inputs = {c['candidate_id']: c for c in json.loads((folder / 'candidates.json').read_text())}
    for path in sorted(folder.glob('assembly-*.json')):
        for candidate in json.loads(path.read_text()):
            if candidate['disposition'] != 'assembled' or candidate.get('follow_up_leads') or any(o['decision'] == 'unresolved' for o in candidate['observations']):
                held_candidates.append(dict(candidate, batch=folder.name))
            candidate_status.append(dict(candidate_id=candidate['candidate_id'], signature=candidate['signature'],
                                         batch=folder.name, disposition=candidate['disposition'], rationale=candidate['rationale'],
                                         proposed_trajectory_ids=[t['local_id'] for t in candidate['trajectories']]))
            observations = {o['observation_id']: o for o in inputs[candidate['candidate_id']]['observations']}
            for proposed in candidate['trajectories']:
                item = dict(proposed, trajectory_id=proposed['local_id'], signature=candidate['signature'],
                            batch=folder.name, status='independently_audited_reported_trajectory', owned_messages=[],
                            associated_messages=[], unassigned=[], excluded=[],
                            candidate_follow_up_leads=candidate.get('follow_up_leads', []))
                owned_ids = {o['observation_id'] for o in candidate['observations']
                             if o['decision'] == 'include' and o.get('trajectory_local_id') == proposed['local_id']}
                for relationship_key in ['correction_relations', 'correction_relationships', 'evidence_relationships']:
                    for relation in candidate.get(relationship_key, []):
                        if relation.get('observation_id') in owned_ids:
                            item.setdefault(relationship_key, []).append(relation)
                for decision in candidate['observations']:
                    if decision.get('trajectory_local_id') not in (None, proposed['local_id']):
                        continue
                    obs = observations[decision['observation_id']]
                    line, revision = revisions[obs['revision_id']]
                    spans = []
                    for text in decision.get('included_excerpts', []):
                        starts, position = [], 0
                        while (position := revision['body'].find(text, position)) != -1:
                            starts.append(position)
                            position += max(1, len(text))
                        assert starts
                        body_lines = revision['body'].split('\n')
                        source_line_start = sum(len(line) + 1 for line in body_lines[:obs['body_line'] - 1])
                        source_line_end = source_line_start + len(body_lines[obs['body_line'] - 1])
                        on_observation_line = [start for start in starts if start <= source_line_end and start + len(text) >= source_line_start]
                        selected = on_observation_line[0] if len(on_observation_line) == 1 else starts[0] if len(starts) == 1 else None
                        spans.append(dict(text=text, start_char=selected, end_char=selected + len(text) if selected is not None else None,
                                          source_char_positions=starts, length=len(text),
                                          text_sha256=hashlib.sha256(text.encode('latin1')).hexdigest(),
                                          location_uncertainty='multiple occurrences outside uniquely identified signoff line' if selected is None else None))
                    record = dict(decision, source_line=line, body_line=obs['body_line'], page_id=revision['page_id'],
                                  utc=revision['time'], editor=revision['label'], signature=obs['signature'],
                                  diff_base=revision['diff_base'], spans=spans, source_excerpt=obs['excerpt'])
                    target = {'include':'owned_messages', 'associate':'associated_messages', 'unresolved':'unassigned', 'exclude':'excluded'}[decision['decision']]
                    item[target].append(record)
                for key in ['owned_messages', 'associated_messages', 'unassigned', 'excluded']:
                    item[key].sort(key=lambda r: (r['utc'], r['revision_id'], r['body_line']))
                item['owned_publication_count'] = len({r['revision_id'] for r in item['owned_messages']})
                result.append(item)
    audit_refs.append(folder.name)
alias_path = OUT / 'trajectory-aliases.json'
if alias_path.exists():
    for bridge in json.loads(alias_path.read_text()):
        if bridge['status'] != 'independently_confirmed':
            continue
        canonical = next((t for t in result if t['trajectory_id'] == bridge['canonical']), None)
        merged = next((t for t in result if t['trajectory_id'] == bridge['merged']), None)
        assert canonical is not None and merged is not None
        canonical.setdefault('signatures', [canonical['signature']]).append(merged['signature'])
        canonical.setdefault('alias_bridges', []).append(bridge)
        canonical['anchor_observation_ids'] = list(dict.fromkeys(canonical['anchor_observation_ids'] + merged['anchor_observation_ids']))
        canonical['candidate_follow_up_leads'] += merged.get('candidate_follow_up_leads', [])
        for relationship_key in ['correction_relations', 'correction_relationships', 'evidence_relationships']:
            if merged.get(relationship_key):
                canonical.setdefault(relationship_key, []).extend(merged[relationship_key])
        canonical['membership_rationale'] += ' Alias continuity: ' + bridge['reason']
        for key in ['owned_messages', 'associated_messages', 'unassigned', 'excluded', 'schedule_claims', 'uncertainties']:
            canonical[key] += merged[key]
        for key in ['owned_messages', 'associated_messages', 'unassigned', 'excluded']:
            canonical[key].sort(key=lambda r: (r['utc'], r['revision_id'], r['body_line']))
        canonical['owned_publication_count'] = len({r['revision_id'] for r in canonical['owned_messages']})
        result.remove(merged)
result.sort(key=lambda t: (t['batch'], t['signature'], t['trajectory_id']))
canonical_ids = {t['trajectory_id']: t['trajectory_id'] for t in result}
for t in result:
    for bridge in t.get('alias_bridges', []):
        canonical_ids[bridge['merged']] = t['trajectory_id']
for c in candidate_status:
    c['canonical_trajectory_ids'] = list(dict.fromkeys(canonical_ids[tid] for tid in c['proposed_trajectory_ids']))
(OUT / 'new-trajectories.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(OUT / 'candidate-status.json').write_text(json.dumps(candidate_status, ensure_ascii=False, indent=2) + '\n')
(OUT / 'follow-up-candidates.json').write_text(json.dumps(held_candidates, ensure_ascii=False, indent=2) + '\n')
# Refresh the cross-batch comparison index whenever an audited batch is exported.
# Baseline signatures retain the previously reviewed identity interpretation.
fingerprint_path = OUT / 'accepted-fingerprints.json'
prior_baseline = {t['trajectory_id']: t for t in json.loads((OUT / 'baseline/fingerprints.json').read_text())}
fingerprints = [dict(trajectory_id=t['trajectory_id'], signatures=t.get('signatures', [t['signature']]),
                     task=t['task'], pages=sorted({m['page_id'] for m in t['owned_messages']}),
                     claims=t['schedule_claims']) for t in result]
for t in json.loads((OUT / 'baseline/audited49.json').read_text()):
    fingerprints.append(prior_baseline.get(t['trajectory_id'], dict(
        trajectory_id=t['trajectory_id'], signatures=[] if t['status'] == 'provisional' else [t['display_name']],
        task=t['task_family'], pages=sorted({m['page_id'] for m in t['owned_messages']}),
        claims=t['schedule_evidence'], status=t['status'])))
fingerprint_path.write_text(json.dumps(fingerprints, ensure_ascii=False, indent=2) + '\n')
folder = OUT / 'trajectories'
folder.mkdir(exist_ok=True)
index = ['# Audited new reported trajectories', '', 'These are reconstructed task histories, not authenticated processes. All published batches passed independent review and resolution.', '']
for i, t in enumerate(result, 1):
    slug = t['trajectory_id'].replace('/', '-')
    index.append(f"- [{t['signature']} — {t['task']}](trajectories/{slug}.md): {t['owned_publication_count']} owned publication revisions; batch {t['batch']}.")
    lines = [f"# {t['signature']}: {t['task']}", '', f"Stable trajectory ID: `{t['trajectory_id']}`. Batch {t['batch']}.", '',
             t['membership_rationale'], '', '## Uncertainties', '']
    lines += ['- ' + u for u in t['uncertainties']]
    if t.get('candidate_follow_up_leads'):
        lines += ['', 'Candidate-group follow-up leads (not accepted identity links):', '']
        lines += ['- ' + str(lead) for lead in t['candidate_follow_up_leads']]
    lines += ['', '## Selected schedule evidence', '',
              'Reported and predicted times retain their source interpretation. These are claims, not verified backend events.', '',
              '| Source observation | Owner / clock | Round / event | Literal value | Status | Supersedes |',
              '| --- | --- | --- | --- | --- | --- |']
    for c in t['schedule_claims']:
        values = [c['observation_id'], str(c['owner']) + ' / ' + str(c['clock_system']),
                  str(c['round']) + ' / ' + str(c['event_kind']), c['raw_value'], c['status'], c.get('supersedes') or '']
        lines.append('| ' + ' | '.join(str(v).replace('|', '\\|').replace('\n', ' ') for v in values) + ' |')
    for relationship_key in ['correction_relations', 'correction_relationships', 'evidence_relationships']:
        if t.get(relationship_key):
            lines += ['', 'Correction relationships:', '', '```json', json.dumps(t[relationship_key], indent=2), '```']
    lines += ['', '## Owned contributions', '']
    for m in t['owned_messages']:
        lines += [f"### {m['utc']} · {m['revision_id']}", '',
                  f"Editor `{m['editor']}`; signature `{m['signature']}`; original JSONL line {m['source_line']}; body line {m['body_line']}.", '',
                  m['reason'], '']
        for s in m['spans']:
            lines += ['    ' + s['text'].replace('\n', '\n    '), '']
        if m.get('cross_post_of'):
            lines += ['Cross-post of: `' + m['cross_post_of'] + '`; publication retained, not independent corroboration.', '']
    for key, title in [('associated_messages','Peer context'),('unassigned','Unresolved candidates'),('excluded','Excluded observations')]:
        lines += ['## ' + title, '']
        lines += [f"- `{m['revision_id']}` / `{m['observation_id']}`: {m['reason']}" for m in t[key]]
        lines += ['']
    (folder / (slug + '.md')).write_text('\n'.join(lines))
(OUT / 'INDEX.md').write_text('\n'.join(index) + '\n')
with (OUT / 'trajectories.csv').open('w', newline='') as handle:
    fields = ['trajectory_id','signature','task','batch','owned_publication_count','membership_rationale']
    writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(result)
queue = json.loads((OUT / 'candidate-queue.json').read_text())
done = {c['candidate_id'] for c in candidate_status}
summary = dict(new_audited_trajectories=len(result), audited_candidate_groups=len(done), batches=audit_refs,
               remaining_multi_post_candidates=sum(c['candidate_id'] not in done and c['retrieval_status']=='multi_post_timed' for c in queue),
               remaining_other_candidates=sum(c['candidate_id'] not in done and c['retrieval_status']!='multi_post_timed' for c in queue),
               dispositions=dict(collections.Counter(c['disposition'] for c in candidate_status)),
               original_baseline=dict(supported=48,provisional=1), live_explorer_changed=False)
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
report = ['# Assembly progress and audit record', '',
          f"{len(result)} new reported trajectories accepted from {len(done)} reviewed candidate groups. Original baseline: 48 supported histories and one provisional history.", '',
          'Counts describe reconstructed histories, not authenticated independent agents.', '',
          '| Batch | Groups | Proposed histories after corrections | Audit pass / revise / defer | Owned observation records | Gate |',
          '| --- | --- | --- | --- | --- | --- |']
for batch in audit_refs:
    v = json.loads((OUT / 'batches' / batch / 'validation.json').read_text())
    verdicts = v['audit_verdicts']
    report.append(f"| {batch} | {v['candidate_groups']} | {v['proposed_trajectories']} | {' / '.join(str(verdicts.get(k, 0)) for k in ['pass','revise','defer'])} | {v['decisions'].get('include', 0)} | {v['next_batch_gate']} |")
report += ['', 'Batch history counts precede cross-batch alias reconciliation. The canonical total above applies independently confirmed alias bridges.', '',
           '## Splits and alias reconciliation', '']
for c in candidate_status:
    if c['disposition'] == 'split':
        report.append(f"- **{c['signature']}**: {c['rationale']}")
for t in result:
    for bridge in t.get('alias_bridges', []):
        report.append(f"- **{' / '.join(t.get('signatures', [t['signature']]))}**: {bridge['reason']} Canonical history `{t['trajectory_id']}`.")
report += ['',
           '## Deferred groups', '']
for c in held_candidates:
    if c['disposition'] == 'deferred':
        report.append(f"- **{c['signature']}** (`{c['candidate_id']}`, batch {c['batch']}): {c['rationale']}")
report += ['', '## Remaining scope', '',
           f"{summary['remaining_multi_post_candidates']} screened multi-post candidate groups remain unreviewed; {summary['remaining_other_candidates']} other groups and the separate known-signature queue remain follow-up material.", '',
           'See `follow-up-candidates.json` for full decisions, unresolved observations and preserved deferred proposals; `batches/` retains the independent reviews and correction records. No changes have been made to the live explorer.']
(OUT / 'RUN-REPORT.md').write_text('\n'.join(report) + '\n')
print(json.dumps(summary, indent=2))
