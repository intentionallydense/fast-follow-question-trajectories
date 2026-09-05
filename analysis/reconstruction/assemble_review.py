#!/usr/bin/env python3
"""Join independently reviewed evidence, without merging identities transitively."""
import collections
import csv
import json
from pathlib import Path
import re
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent


def dump_csv(name, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (OUT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in r.items()})


def main():
    with zipfile.ZipFile(ROOT / 'full-wiki-logs.zip') as z:
        revs = [json.loads(x) for x in z.read('revisions.jsonl').splitlines()]
    by_id = {r['rev_id']: (i, r) for i, r in enumerate(revs, 1)}
    seq = json.loads((OUT / 'sequence_evidence.json').read_text())
    seq_personas = json.loads((OUT / 'sequence_personas.json').read_text())
    late = json.loads((OUT / 'later_evidence.json').read_text())
    identity = json.loads((OUT / 'identity_evidence.json').read_text())
    checked = []

    def check(e):
        rid = e.get('revision_id', e.get('rev_id'))
        lineno = e.get('revisions_jsonl_line', e.get('jsonl_line'))
        index, rev = by_id[rid]
        assert index == lineno, (rid, index, lineno)
        quote = e.get('excerpt', e.get('quote'))
        # Some reviewers join noncontiguous inserted lines. Verify every line.
        for line in quote.split('\n'):
            assert not line or line in rev['body'], (rid, line)
        checked.append((rid, lineno))
        return dict(revision_id=rid, revisions_jsonl_line=lineno, page_id=rev['page_id'],
                    time=rev['time'], editor_label=rev['label'], excerpt=quote)

    personas = []
    for i, p in enumerate(seq_personas, 1):
        ev = [check(e) for e in p['primary_evidence']]
        personas.append(dict(persona_id=f'P{i:02d}', original_persona_id=p['persona_id'],
                             family=p['family'], reported_persona=p['signature'],
                             schedule=p['distinguishing_schedule'], confidence=p['confidence'],
                             inferred_initial_clock=p['inferred_initial_clock'],
                             editor_labels=sorted({e['editor_label'] for e in ev}),
                             pages=sorted({e['page_id'] for e in ev}), primary_evidence=ev,
                             uncertainty=p['uncertainty']))
    for i, p in enumerate(late['witnesses'], len(personas) + 1):
        e = check(p['evidence'])
        quote = e['excerpt']
        if p['persona'] == 'RRP:Feb03':
            quote = quote[quote.index('RRPFeb03Scout:'):]
            e['excerpt'] = quote
        personas.append(dict(persona_id=f'P{i:02d}', original_persona_id=p['persona'],
                             family=p['persona'].split(':')[0], reported_persona=p['persona'],
                             schedule=quote,
                             confidence='medium_conditional' if p['persona'] == 'CVD:Sep24' else 'high_conditional',
                             inferred_initial_clock=False, editor_labels=[e['editor_label']], pages=[e['page_id']],
                             primary_evidence=[e],
                             uncertainty='Reported task persona, not authenticated process. ' +
                             ('Observer has own scaffold clock but selected excerpt lacks a full prompt schedule.' if p['persona'] == 'CVD:Sep24' else
                              'Different task clocks/families support different reported trajectories; one persistent agent may manage several.')))
    assert len(personas) == 49
    assert len({(p['family'], p['reported_persona']) for p in personas}) == 49
    # Root review: include the originating result, not only the recipient's ACK.
    signal_support = check(dict(revision_id='dse~IHMEFamilyPlanningR4Signal@1',
                                revisions_jsonl_line=6564,
                                excerpt='R4 SIGNAL: Bahrain = 40.01% (raw 40.00672); task time approx SIGNAL NOW. -- OpenAINov27FP'))
    nov27 = next(p for p in personas if p['reported_persona'] == 'FP:Nov27')
    nov27['primary_evidence'].append(signal_support)
    nov27['pages'] = sorted(set(nov27['pages']) | {signal_support['page_id']})
    relations = []
    for x in seq:
        ev = check(x)
        relations.append(dict(connection_id=x['evidence_id'], reviewer='sequence',
                              relation_type=x['relation_type'], source=x.get('source_alias') or x.get('source_page'),
                              target=x.get('target_alias') or x.get('target_page'),
                              source_page=x['source_page'], target_page=x.get('target_page'),
                              confidence=x['confidence'] + '_conditional_on_recorded_claim',
                              uncertainty=x['uncertainty'], evidence=[ev]))
    for i, x in enumerate(late['relations'], 1):
        ev = check(x['evidence'])
        confidence = x['confidence']
        if x['type'] == 'answer_acknowledged':
            confidence = 'medium_for_source_attribution'
        relations.append(dict(connection_id=f'LATE{i:03d}', reviewer='later',
                              relation_type=x['type'], source=x['source'], target=x['target'],
                              source_page=ev['page_id'], target_page=x['target'][5:] if x['target'].startswith('page:') else '',
                              confidence=confidence + '_conditional_on_recorded_claim',
                              uncertainty=x['rationale'] + ' No authenticated run identity or independent network telemetry.',
                              evidence=[signal_support, ev] if x['type'] == 'answer_relay_acknowledged' else [ev]))
    for x in identity['cases']:
        ev = [check(e) for e in x['evidence']]
        relations.append(dict(connection_id=x['id'], reviewer='identity', relation_type=x['relation_type'],
                              source=x['entities'][0], target='; '.join(x['entities'][1:]),
                              source_page=ev[0]['page_id'], target_page='', confidence=x['confidence'],
                              decision=x['decision'], uncertainty=x['rationale'] + ' ' + x['uncertainty'], evidence=ev))
    (OUT / 'audited_personas.json').write_text(json.dumps(personas, indent=2, ensure_ascii=False) + '\n')
    (OUT / 'curated_connections.json').write_text(json.dumps(relations, indent=2, ensure_ascii=False) + '\n')
    dump_csv('audited_personas.csv', [dict(persona_id=p['persona_id'], family=p['family'],
              reported_persona=p['reported_persona'], confidence=p['confidence'],
              schedule=p['schedule'], editor_labels=p['editor_labels'], pages=p['pages'],
              evidence_revisions=[e['revision_id'] for e in p['primary_evidence']],
              evidence_jsonl_lines=[e['revisions_jsonl_line'] for e in p['primary_evidence']],
              inferred_initial_clock=p['inferred_initial_clock'], uncertainty=p['uncertainty']) for p in personas])
    dump_csv('curated_connections.csv', [dict(connection_id=x['connection_id'], relation_type=x['relation_type'],
              source=x['source'], target=x['target'], source_page=x['source_page'], target_page=x['target_page'],
              confidence=x['confidence'], decision=x.get('decision', ''), uncertainty=x['uncertainty'],
              evidence_revisions=[e['revision_id'] for e in x['evidence']],
              evidence_jsonl_lines=[e['revisions_jsonl_line'] for e in x['evidence']]) for x in relations])
    dossier = ['# Audited run-persona dossier', '',
               'These 49 entries are a selected, non-exhaustive witness set of reported trajectories. They do not count independent agent processes. “High” rates internal trajectory evidence conditional on truthful reports. P11 and P27 have additional limitations stated below. Different families are different task trajectories, not necessarily different persistent agents.', '']
    for p in personas:
        dossier.extend([f'## {p["persona_id"]}: {p["family"]} / {p["reported_persona"]}', '',
                        f'Confidence: **{p["confidence"]}**. Editor labels in selected evidence: ' + ', '.join(f'`{a}`' for a in p['editor_labels']) + '.', '',
                        'Uncertainty: ' + p['uncertainty'], ''])
        if p['inferred_initial_clock']:
            dossier.extend(['The initial clock is inferred; the later observed NY clock is directly reported.', ''])
        for e in p['primary_evidence']:
            dossier.extend([f'`{e["revision_id"]}` — original `revisions.jsonl:{e["revisions_jsonl_line"]}`, UTC {e["time"]}.', '', '````text', e['excerpt'], '````', ''])
    (OUT / 'audited-personas.md').write_text('\n'.join(dossier) + '\n')
    evidence_doc = ['# Curated connection evidence', '',
                    '108 reviewed findings (including continuity, distinctness, fingerprints, replies, and unresolved links); these are not 108 independent exchanges. Entries retain quoted reports, not authenticated identities. Source/target semantics follow the relation type; a reply points from respondent to addressee, while an answer relay points from reported source to recipient. No transitive identity merging is applied.', '']
    for x in relations:
        evidence_doc.extend([f'## {x["connection_id"]}: {x["relation_type"]}', '',
                             f'`{x["source"]}` → `{x["target"]}`', '',
                             f'Confidence: {x["confidence"]}. ' + x['uncertainty'], ''])
        for e in x['evidence']:
            evidence_doc.extend([f'`{e["revision_id"]}` — original `revisions.jsonl:{e["revisions_jsonl_line"]}`, UTC {e["time"]}; editor `{e["editor_label"]}`.', '',
                                 '````text', e['excerpt'], '````', ''])
    (OUT / 'curated-evidence.md').write_text('\n'.join(evidence_doc) + '\n')
    counts = dict(audited_personas=len(personas), persona_confidence=dict(collections.Counter(p['confidence'] for p in personas)),
                  persona_families=dict(collections.Counter(p['family'] for p in personas)),
                  curated_findings=len(relations), validated_reference_occurrences=len(checked),
                  distinct_validated_revision_references=len(set(checked)),
                  no_transitive_identity_merges=True)
    (OUT / 'manual_review_summary.json').write_text(json.dumps(counts, indent=2) + '\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()
