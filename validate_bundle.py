"""Validate this snapshot using Python's standard library; run from any directory."""
from pathlib import Path
import hashlib,json,zipfile
from collections import defaultdict

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'trajectory-explorer/public'
def read(path):return json.loads(path.read_text())
def resolve(ref):
    assert ref.startswith('/data/'),ref
    path=PUBLIC/ref.lstrip('/')
    assert path.is_file(),ref
    return path

def main():
    manifest=read(ROOT/'MANIFEST.json')
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.name!='MANIFEST.json'}
    assert actual==set(manifest['files']),('File set differs from snapshot',actual ^ set(manifest['files']))
    for name,info in manifest['files'].items():
        p=ROOT/name
        assert p.stat().st_size==info['bytes'],name
        assert hashlib.sha256(p.read_bytes()).hexdigest()==info['sha256'],name
    with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as archive:
        assert archive.testzip() is None
        sources={r['rev_id']:r for line in archive.read('revisions.jsonl').splitlines() for r in [json.loads(line)]}
    index=read(PUBLIC/'data/assembled-trajectories.json')
    rows=index['trajectories'];supported={r['id'] for r in rows if r['status']!='provisional'}
    assert len(rows)==322 and len(supported)==298
    cvd=read(PUBLIC/'data/cvd-accounting/accounting.json')
    provisional={r['id'] for r in rows if r['status']=='provisional'}
    assert provisional=={'P43'}|{r['id'] for r in cvd['roster'] if r['status']=='provisional'}
    assert len(provisional)==24
    assert sum(r['status']=='supported' for r in cvd['roster'])==58
    dossiers={};owned=defaultdict(list);span_count=0
    for row in rows:
        d=read(resolve(row['file']));dossiers[row['id']]=d
        assert d['trajectory_id']==row['id']
        for rid,s in d['evidence'].items():assert s['body']==sources[rid]['body'],rid
        for group in ['owned_messages','associated_messages','unassigned','excluded']:
            for m in d[group]:
                if not m.get('revision_id'):continue
                r=sources[m['revision_id']]
                for s in m.get('spans',[]):
                    assert r['body'][s['start_char']:s['end_char']]==s['text'],(row['id'],m['revision_id'])
                    assert hashlib.sha256(s['text'].encode('latin1')).hexdigest()==s['text_sha256']
                    span_count+=1
                    if group=='owned_messages':owned[m['revision_id']].append((s['start_char'],s['end_char'],row['id']))
    for rid,spans in owned.items():
        for i,(start,end,tid) in enumerate(spans):
            for start2,end2,tid2 in spans[i+1:]:
                assert tid==tid2 or max(start,start2)>=min(end,end2),(rid,tid,tid2,'ownership overlap')
    catalog=read(PUBLIC/'data/audited-tasks.json')
    assert catalog['family_count']==41 and len(catalog['tasks'])==42
    accounts=set();sparse=0;claim_count=0
    def claim(tid,c):
        nonlocal claim_count
        d=dossiers[tid];resolve(next(r['file'] for r in rows if r['id']==tid))
        assert any(m['revision_id']==c['revision_id'] and any(s['text']==c['quote'] for s in m['spans']) for m in d['owned_messages']),(tid,c['revision_id'])
        body=sources[c['revision_id']]['body']
        assert body[c['start_char']:c['end_char']]==c['quote']
        assert hashlib.sha256(c['quote'].encode('latin1')).hexdigest()==c['text_sha256']
        claim_count+=1
    for row in catalog['tasks']:
        t=read(resolve(row['file']))
        assert t['id']==row['id'] and len(t['accounts'])==row['account_count']
        if not t['accounts']:
            sparse+=1;assert t['coverage']['status']=='insufficient_evidence' and t['coverage']['anchors']
        for anchor in (t.get('coverage') or {}).get('anchors',[]):
            body=sources[anchor['revision_id']]['body']
            assert body[anchor['start_char']:anchor['end_char']]==anchor['quote']
        for a in t['accounts']:
            assert a['id'] not in accounts;accounts.add(a['id']);resolve(a['dossier_file'])
            for c in a['events']+a['timing']:claim(a['id'],c['citation'])
    assert accounts==supported and sparse==8
    environment=read(PUBLIC/'data/assembled-environment.json')
    for c in environment['claims']:
        assert c['trajectory_id'] in supported
        resolve(c['dossier_file']);claim(c['trajectory_id'],dict(c['source'],revision_id=c['revision_id'],quote=c['quote']))
    print(f"PASS: {len(manifest['files'])} file hashes; {len(sources)} archive revisions; 298 supported + 24 provisional entries; 41 families / 42 groups; {span_count} source spans; {claim_count} owned claim citations; no cross-history ownership overlap.")

if __name__=='__main__':main()
