"""Read-only verification of frozen assembly, independent of export validators."""
import json, hashlib, zipfile, collections, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
A=ROOT/'analysis/trajectory-assembly'
new=json.loads((A/'new-trajectories.json').read_text())
base=json.loads((A/'baseline/audited49.json').read_text())
with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as z:
    lines=z.read('revisions.jsonl').splitlines()
rev={r['rev_id']:r for r in map(json.loads,lines)}
lineids={i:r['rev_id'] for i,r in enumerate(map(json.loads,lines),1)}
errors=[]; inherited=[]; repeats=[]; overlaps=[]; claims=[]; signatures=collections.defaultdict(list); clocks=collections.defaultdict(list); spans=collections.defaultdict(list); texts=collections.defaultdict(list)
for t in base+new:
    tid=t['trajectory_id']
    signatures[t.get('signature',t.get('display_name','')).casefold()].append(tid)
    for m in t['owned_messages']:
        r=rev[m['revision_id']]
        for s in m['spans']:
            text=s['text']; start,end=s['start_char'],s['end_char']
            if r['body'][start:end]!=text or hashlib.sha256(text.encode('latin1')).hexdigest()!=s['text_sha256']: errors.append([tid,m.get('observation_id'), 'span/hash'])
            spans[r['rev_id']].append((tid,start,end))
            texts[text].append((tid,m.get('observation_id'),r['rev_id']))
            if t in new:
                previous=[x for x in rev.values() if x['page_id']==r['page_id'] and x['seq']<r['seq'] and text in x['body']]
                if previous: inherited.append(dict(trajectory_id=tid,observation_id=m['observation_id'],revision_id=r['rev_id'],previous_revisions=[x['rev_id'] for x in previous],text=text))
        if t in new and lineids.get(m['source_line'])!=r['rev_id']:errors.append([tid,m['observation_id'],'source line'])
    if t in new:
        owned={m['observation_id'] for m in t['owned_messages']}
        if len({m['revision_id'] for m in t['owned_messages']})<2:errors.append([tid,'publication threshold'])
        for c in t['schedule_claims']:
            if c['owner']=='self' and c['observation_id'] not in owned:errors.append([tid,c['observation_id'],'unowned self clock'])
            if c['owner']=='self':clocks[(c['round'],c['raw_value'])].append((tid,c['event_kind'],c['status']))
for rid,ss in spans.items():
    for i,(a,s,e) in enumerate(ss):
        for b,u,v in ss[i+1:]:
            if a!=b and max(s,u)<min(e,v):overlaps.append([rid,a,b])
for tx,locations in texts.items():
    if len(locations)>1:repeats.append(dict(text=tx,locations=locations))
result=dict(new_trajectories=len(new),baseline_trajectories=len(base),new_owned_messages=sum(len(t['owned_messages']) for t in new),batch_counts=dict(collections.Counter(t['batch'] for t in new)),errors=errors,ownership_overlaps=overlaps,exact_preexisting_owned_spans=inherited,repeated_text=repeats,signature_collisions={k:v for k,v in signatures.items() if len(v)>1},clock_collisions=[dict(round=k[0],value=k[1],claims=v) for k,v in clocks.items() if len({c[0] for c in v})>1],input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [A/'new-trajectories.json',A/'baseline/audited49.json',ROOT/'analysis/trajectory-audit-49/RULES.md',A/'research/RULES-v1.md',ROOT/'full-wiki-logs.zip']})
(OUT/'integrity-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v if k in ('errors','ownership_overlaps','signature_collisions','batch_counts') or not isinstance(v,list) else len(v) for k,v in result.items() if k!='input_hashes'},indent=2))
