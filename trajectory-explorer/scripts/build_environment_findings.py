"""Source-check curated environment claims and export compact per-task evidence."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from build_task_trajectories import ROOT

INPUT = ROOT / 'research/assembled-environment-claims.json'

def main():
    findings = json.loads(INPUT.read_text())
    index = json.loads((ROOT/'app/tasks/assembled-index.json').read_text())
    roster = {t['id']: t for t in index['trajectories']}
    original_ids = {(f['trajectory_id'], f['claim'], f['quote']): i for i,f in enumerate(findings,1)}
    findings = [f for f in findings if roster[f['trajectory_id']]['status'] != 'provisional']
    groups = {}
    seen = set()
    for n, finding in enumerate(findings, 1):
        row = roster[finding['trajectory_id']]
        dossier = json.loads((ROOT/'public'/row['file'].lstrip('/')).read_text())
        matches = [(m, s) for m in dossier['owned_messages'] if m['revision_id'] == finding['revision_id'] for s in m['spans'] if s['text'] == finding['quote']]
        assert matches, (finding['trajectory_id'], finding['claim'])
        message, span = matches[0]
        source = dossier['evidence'][finding['revision_id']]
        assert source['body'][span['start_char']:span['end_char']] == finding['quote']
        assert hashlib.sha256(finding['quote'].encode('latin1')).hexdigest() == span['text_sha256']
        identity = (finding['trajectory_id'], finding['claim'], finding['quote'])
        assert identity not in seen
        seen.add(identity)
        item = dict(finding, id=f'AE{original_ids[identity]:03}', name=row['name'], task_id=row['task_id'] or 'labor-force-followup',
            dossier_file=row['file'], trajectory_status=row['status'], source=dict(
                jsonl_line=source['jsonl_line'], body_line=source['body'][:span['start_char']].count('\n')+1,
                start_char=span['start_char'], end_char=span['end_char'], text_sha256=span['text_sha256'],
                server_time=source['server_time'], recorded_editor=source['recorded_editor'],
                observation_id=message.get('observation_id', message.get('record_id')),
                diff_base=message.get('diff_base')))
        groups.setdefault(row['task_id'] or 'labor-force-followup', []).append(item)
    dest = ROOT/'public/data/assembled-environment'
    dest.mkdir(exist_ok=True, parents=True)
    if 'labor-force-followup' not in groups:
        (dest/'labor-force-followup.json').unlink(missing_ok=True)
    for key, items in groups.items():
        (dest/f'{key}.json').write_text(json.dumps(items, ensure_ascii=False, indent=2)+'\n')
    summary = dict(claim_count=len(findings), trajectory_count=len({f['trajectory_id'] for f in findings}),
        reviewed_trajectory_count=sum(r['status'] != 'provisional' and not r['id'].startswith('FC-') and r.get('batch') != 'CVD clock audit' for r in roster.values()), task_counts={k:len(v) for k,v in groups.items()},
        dimensions=dict(Counter(f['dimension'] for f in findings)))
    (ROOT/'app/tasks/assembled-environment-index.json').write_text(json.dumps(summary, indent=2)+'\n')
    (ROOT/'public/data/assembled-environment.json').write_text(json.dumps(dict(summary=summary, claims=[i for items in groups.values() for i in items]), ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
