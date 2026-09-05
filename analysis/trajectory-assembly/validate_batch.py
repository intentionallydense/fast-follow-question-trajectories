"""Source/coverage checks and gate status; semantic acceptance requires independent audits."""
import argparse
import collections
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('batch')
args = parser.parse_args()
folder = ROOT / 'batches' / args.batch
inputs = {c['candidate_id']: c for c in json.loads((folder / 'candidates.json').read_text())}
with zipfile.ZipFile(ROOT.parent.parent / 'full-wiki-logs.zip') as z:
    revisions = {r['rev_id']: r for r in map(json.loads, z.read('revisions.jsonl').splitlines())}
outputs = []
for path in sorted(folder.glob('assembly-*.json')):
    outputs += json.loads(path.read_text())
assert len(outputs) == len(inputs)
assert {o['candidate_id'] for o in outputs} == set(inputs)
errors, warnings = [], []
trajectory_count = 0
decisions = collections.Counter()
for group in outputs:
    cid = group['candidate_id']
    input_group = inputs[cid]
    obs = {o['observation_id']: o for o in input_group['observations']}
    chosen = {o['observation_id']: o for o in group['observations']}
    if len(chosen) != len(group['observations']) or set(chosen) != set(obs):
        errors.append([cid, 'Observation coverage does not match input'])
    trajectory_ids = {t['local_id'] for t in group['trajectories']}
    trajectory_count += len(trajectory_ids)
    for oid, decision in chosen.items():
        if oid not in obs:
            continue
        source = obs[oid]
        body = revisions[source['revision_id']]['body']
        decisions[decision['decision']] += 1
        if source['revision_id'] != decision['revision_id']:
            errors.append([cid, oid, 'Wrong source revision'])
        if decision['decision'] not in ('include', 'associate', 'exclude', 'unresolved'):
            errors.append([cid, oid, 'Invalid decision'])
        if not decision.get('reason') or not decision.get('rule_ids'):
            errors.append([cid, oid, 'Missing reason/rules'])
        if any(r not in {f'R{i:02d}' for i in range(1, 15)} for r in decision.get('rule_ids', [])):
            errors.append([cid, oid, 'Unknown rule ID'])
        if decision['decision'] == 'include':
            if decision.get('trajectory_local_id') not in trajectory_ids or not decision.get('included_excerpts'):
                errors.append([cid, oid, 'Included observation lacks trajectory/span'])
        for excerpt in decision.get('included_excerpts', []):
            if not excerpt or excerpt not in body:
                errors.append([cid, oid, 'Span not literal source', excerpt[:120]])
            elif body.count(excerpt) > 1:
                warnings.append([cid, oid, 'Repeated source substring: explicit offset needed in publication'])
        for dependency in decision.get('depends_on', []):
            if dependency not in chosen or chosen[dependency]['decision'] != 'include':
                errors.append([cid, oid, 'Dependency is not an accepted source', dependency])
    for trajectory in group['trajectories']:
        tid = trajectory['local_id']
        owned = [m for m in chosen.values() if m.get('trajectory_local_id') == tid and m['decision'] == 'include']
        if len({m['revision_id'] for m in owned}) < 2:
            errors.append([cid, tid, 'Fewer than two distinct owned publication revisions'])
        for oid in trajectory['anchor_observation_ids']:
            if oid not in chosen or chosen[oid]['decision'] != 'include' or chosen[oid].get('trajectory_local_id') != tid:
                errors.append([cid, tid, 'Anchor is not owned by this trajectory', oid])
        if not trajectory['schedule_claims']:
            errors.append([cid, tid, 'Missing selected typed schedule evidence'])
        for claim in trajectory['schedule_claims']:
            oid = claim['observation_id']
            if oid not in obs or claim['excerpt'] not in revisions[obs[oid]['revision_id']]['body']:
                errors.append([cid, tid, 'Clock claim lacks exact source', oid])
            missing = {'owner','clock_system','task_date','round','event_kind','raw_value','status','excerpt','supersedes'} - set(claim)
            if missing:
                errors.append([cid, tid, 'Clock fields missing', sorted(missing)])
            for field, allowed in {
                'owner': {'self', 'peer', 'uncertain'},
                'clock_system': {'scaffold', 'task', 'archive_utc', 'container', 'unspecified'},
                'event_kind': {'activation', 'prompt_arrival', 'answer', 'deadline', 'due', 'current_time', 'cutoff', 'other'},
                'status': {'reported', 'predicted', 'inferred'},
            }.items():
                if claim.get(field) not in allowed:
                    errors.append([cid, tid, oid, 'Invalid clock field', field, claim.get(field)])
            if claim.get('owner') == 'self' and (oid not in chosen or chosen[oid]['decision'] != 'include' or chosen[oid].get('trajectory_local_id') != tid):
                errors.append([cid, tid, oid, 'Self clock claim lacks owned observation'])
audits = []
for path in sorted(folder.glob('audit-[0-9]*.json')):
    audits += json.loads(path.read_text())
audited_ids = {a['candidate_id'] for a in audits}
audit_complete = len(audits) == len(inputs) and audited_ids == set(inputs)
result = dict(batch=args.batch, candidate_groups=len(inputs), proposed_trajectories=trajectory_count,
              decisions=dict(decisions), errors=errors, warnings=warnings,
              independent_audit_complete=audit_complete,
              audit_verdicts=dict(collections.Counter(a['verdict'] for a in audits)),
              provenance_status='passed' if not errors else 'failed',
              next_batch_gate='closed_pending_audit_and_resolution')
resolution = folder / 'audit-resolution.json'
if not errors and audit_complete and resolution.exists():
    resolved = json.loads(resolution.read_text())
    needed = {a['candidate_id'] for a in audits if a['verdict'] != 'pass'}
    if needed <= {r['candidate_id'] for r in resolved if r['status'] == 'resolved'}:
        result['next_batch_gate'] = 'open'
(folder / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if errors:
    raise SystemExit(1)
