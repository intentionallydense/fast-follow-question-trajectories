"""Source integrity and ownership-collision checks for family completion research."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as z:
    sources={r['rev_id']:r for line in z.read('revisions.jsonl').splitlines() for r in [json.loads(line)]}
old=json.loads((ROOT/'analysis/trajectory-assembly/baseline/audited49.json').read_text())+json.loads((ROOT/'analysis/trajectory-assembly/new-trajectories.json').read_text())
occupied={}
for t in old:
    for m in t['owned_messages']:
        for s in m['spans']:
            occupied.setdefault(m['revision_id'],[]).append((s['start_char'],s['end_char'],t['trajectory_id']))
checks=[]; ids=set(); warnings=[]
for group in sorted(HERE.glob('group-*')):
    if not (group/'dossiers.json').exists():continue
    dossiers=json.loads((group/'dossiers.json').read_text())
    rounds=json.loads((group/'rounds.json').read_text())
    assert {r['trajectory_id'] for r in rounds}=={t['trajectory_id'] for t in dossiers}
    for t in dossiers:
        tid=t['trajectory_id'];assert tid not in ids;ids.add(tid)
        assert len({m['revision_id'] for m in t['owned_messages']})>=2,tid
        for key in ['owned_messages','associated_messages','excluded','unassigned']:
            for m in t[key]:
                r=sources[m['revision_id']]
                assert m.get('diff_base')==r['diff_base'],(tid,m['revision_id'],'diff base')
                for s in m.get('spans',[]):
                    assert r['body'][s['start_char']:s['end_char']]==s['text'],(tid,m['revision_id'],'offset')
                    assert hashlib.sha256(s['text'].encode('latin1')).hexdigest()==s['text_sha256']
                    if key=='owned_messages':
                        for a,b,other in occupied.get(m['revision_id'],[]):
                            assert not(max(a,s['start_char'])<min(b,s['end_char'])),(tid,other,m['revision_id'],'overlap')
                        occupied.setdefault(m['revision_id'],[]).append((s['start_char'],s['end_char'],tid))
                        base=sources.get(r['diff_base'],{}).get('body','')
                        if s['text'] in base:warnings.append([tid,m['revision_id'],'owned span already in diff base'])
        extraction=next(r for r in rounds if r['trajectory_id']==tid)
        for c in extraction['events']+extraction['timing']:
            assert any(m['revision_id']==c['revision_id'] and any(s['text']==c['quote'] for s in m['spans']) for m in t['owned_messages']),(tid,c)
        checks.append(dict(trajectory_id=tid,owned_messages=len(t['owned_messages'])))
    for c in json.loads((group/'coverage.json').read_text()):
        assert c['anchors'],c['task_id']
        for a in c['anchors']:assert a['quote'] in sources[a['revision_id']]['body']
report=dict(trajectory_count=len(ids),checks=checks,freshness_warnings=warnings)
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert not warnings,'Resolve source freshness warnings before export'
