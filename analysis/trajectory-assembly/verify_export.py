"""Check exported provenance and surface overlaps for semantic review."""
import collections
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
with zipfile.ZipFile(ROOT.parent.parent / 'full-wiki-logs.zip') as archive:
    revisions = {r['rev_id']: r for r in map(json.loads, archive.read('revisions.jsonl').splitlines())}
new = json.loads((ROOT / 'new-trajectories.json').read_text())
baseline = json.loads((ROOT / 'baseline/audited49.json').read_text())
errors, overlaps = [], []
owned = collections.defaultdict(list)
for t in baseline + new:
    tid = t['trajectory_id']
    for m in t['owned_messages']:
        body = revisions[m['revision_id']]['body']
        for s in m['spans']:
            start, end = s['start_char'], s['end_char']
            if start is None or end is None or body[start:end] != s['text']:
                errors.append([tid, m['revision_id'], 'Unresolved or incorrect source offsets'])
            if hashlib.sha256(s['text'].encode('latin1')).hexdigest() != s['text_sha256']:
                errors.append([tid, m['revision_id'], 'Incorrect source span hash'])
            owned[m['revision_id']].append((tid, start, end))
for revision, spans in owned.items():
    for i, (left, start, end) in enumerate(spans):
        for right, start2, end2 in spans[i + 1:]:
            if left != right and None not in (start, end, start2, end2) and max(start, start2) < min(end, end2):
                overlaps.append(dict(revision_id=revision, trajectories=[left, right], overlap=[max(start, start2), min(end, end2)]))
for t in new:
    ids = {m['observation_id'] for m in t['owned_messages']}
    if len({m['revision_id'] for m in t['owned_messages']}) < 2:
        errors.append([t['trajectory_id'], 'Fewer than two owned publication revisions'])
    for c in t['schedule_claims']:
        if c['owner'] == 'self' and c['observation_id'] not in ids:
            errors.append([t['trajectory_id'], c['observation_id'], 'Self clock claim is not owned'])
result = dict(checked_new_trajectories=len(new), checked_baseline_trajectories=len(baseline),
              checked_owned_spans=sum(len(v) for v in owned.values()), errors=errors,
              cross_trajectory_span_overlaps=overlaps,
              limitation='Mechanical provenance checks supplement independent semantic audits; disjoint spans do not prove distinct agents.')
(ROOT / 'export-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if errors or overlaps:
    raise SystemExit(1)
