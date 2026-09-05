"""Additional read-only checks of batch004; semantic judgments remain in its audits."""
import collections
import hashlib
import json
import re
import zipfile
from pathlib import Path

BATCH = Path(__file__).resolve().parent
ROOT = BATCH.parents[1]
REPO = ROOT.parents[1]
with zipfile.ZipFile(REPO / 'full-wiki-logs.zip') as archive:
    revisions = {r['rev_id']: r for r in map(json.loads, archive.read('revisions.jsonl').splitlines())}
inputs = {c['candidate_id']: c for c in json.loads((BATCH / 'candidates.json').read_text())}
errors, freshness_flags, counts = [], [], collections.Counter()
normalize = lambda s: re.sub(r'\W+', '', s).casefold()
for path in sorted(BATCH.glob('assembly-*.json')):
    for candidate in json.loads(path.read_text()):
        cid = candidate['candidate_id']
        source = {o['observation_id']: o for o in inputs[cid]['observations']}
        decisions = {o['observation_id']: o for o in candidate['observations']}
        counts['candidates'] += 1
        for o in decisions.values():
            counts['observations'] += 1
            rev = revisions[o['revision_id']]
            base = revisions.get(rev['diff_base'], {}).get('body', '')
            if o['decision'] != 'include':
                continue
            counts['owned_observations'] += 1
            for span in o['included_excerpts']:
                counts['owned_spans'] += 1
                if span in base or (len(normalize(span)) > 50 and normalize(span) in normalize(base)):
                    freshness_flags.append([cid, o['observation_id'], 'Retained span repeats in diff base'])
            if o.get('cross_post_of'):
                target = decisions.get(o['cross_post_of'])
                if not target or target['decision'] != 'include':
                    errors.append([cid, o['observation_id'], 'Cross-post target is not retained in candidate'])
        for trajectory in candidate['trajectories']:
            counts['local_histories'] += 1
            claim_ids = {c.get('claim_id') for c in trajectory['schedule_claims']}
            for c in trajectory['schedule_claims']:
                counts['selected_clock_claims'] += 1
                o = decisions[c['observation_id']]
                if c['owner'] == 'self' and not any(c['excerpt'] in s for s in o['included_excerpts']):
                    errors.append([cid, c['observation_id'], 'Self clock excerpt extends outside owned spans'])
                if c.get('supersedes') and c['supersedes'] not in claim_ids and c['supersedes'] not in source:
                    errors.append([cid, c['observation_id'], 'Unknown correction target', c['supersedes']])
frozen = json.loads((BATCH / 'input-manifest.json').read_text())
unchanged = []
for name, digest in frozen.items():
    # The accepted exports are intentionally refreshed after the batch passes.
    if name.endswith(('accepted-fingerprints.json', 'new-trajectories.json')):
        continue
    if hashlib.sha256((REPO / name).read_bytes()).hexdigest() != digest:
        errors.append([name, 'Frozen source/prior batch changed'])
    else:
        unchanged.append(name)
result = dict(counts=counts, errors=errors, freshness_flags=freshness_flags,
              unchanged_input_files=len(unchanged),
              limitation='Full-span freshness checks do not replace clause-level source review or establish independent authorship.')
(BATCH / 'supplemental-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if errors or freshness_flags:
    raise SystemExit(1)
