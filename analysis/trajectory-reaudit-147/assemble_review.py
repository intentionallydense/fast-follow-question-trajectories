"""Consolidate independent reviews; validate coverage and literal proposed evidence."""
import collections,csv,hashlib,json,zipfile
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
A=ROOT/'analysis/trajectory-assembly'
with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as z:
    raw=z.read('revisions.jsonl').splitlines()
revs={r['rev_id']:r for r in map(json.loads,raw)}
lines={i:r['rev_id'] for i,r in enumerate(map(json.loads,raw),1)}
new=json.loads((A/'new-trajectories.json').read_text())
errors=[];findings=[];coverage=[];rows=[];quote_count=0;replacement_count=0
for batch in ['001','002','003']:
    review=json.loads((OUT/f'reviews/batch{batch}.json').read_text())
    candidates=json.loads((A/f'batches/{batch}/candidates.json').read_text())
    source_obs={o['observation_id']:o for c in candidates for o in c['observations']}
    if batch=='001':
        cs=review['candidate_coverage']; obs=[o for c in cs for o in c['decisions']]; tids=[t['trajectory_id'] for t in review['trajectory_coverage']]
    elif batch=='002':
        cs=review['reviews']; obs=[o for c in cs for o in c['observation_reviews']]; tids=[t['trajectory_id'] for t in review['trajectory_coverage']]
    else:
        cs=review['candidates']; obs=[o for c in cs for o in c['observations']]; tids=[tid for c in cs for tid in c['trajectory_ids']]
    if collections.Counter(o['observation_id'] for o in obs)!=collections.Counter(source_obs.keys()):errors.append([batch,'observation review coverage'])
    if collections.Counter(tids)!=collections.Counter(t['trajectory_id'] for t in new if t['batch']==batch):errors.append([batch,'trajectory review coverage'])
    if {c['candidate_id'] for c in cs}!={c['candidate_id'] for c in candidates}:errors.append([batch,'candidate review coverage'])
    coverage.append(dict(batch=batch,candidates=len(cs),trajectories=len(tids),observations=len(obs)))
    for o in obs:
        oid=o['observation_id']
        if o['revision_id']!=source_obs[oid]['revision_id']:errors.append([batch,oid,'review source ID mismatch'])
        rows.append(dict(batch=batch,observation_id=oid,revision_id=o['revision_id'],original_decision=o.get('original_decision',o.get('decision_reviewed')),review_verdict=o.get('review_verdict',o.get('recommended_decision')),finding_ids=';'.join(o.get('finding_ids',[]))))
    for original in review['findings']:
        f=dict(original,batch=batch)
        if f['finding_id']=='B003-M05':
            f['coordinator_resolution']='retain_supported';f['coordinator_reason']='FP-S002563 on own live page establishes the precise R4 cooldown/Q1+2h15 test; FP-S002567 anchors that exchange on Jan03ConstructionCadenceLive. FP-S002604 explicitly links that exchange and repeats the precise test. R02 permits this clockless continuation; scratch destination does not negate it.'
        elif f['confidence']=='medium':f['coordinator_resolution']='borderline_review_lead_no_required_change'
        elif f['confidence']=='conservative_metadata_review':f['coordinator_resolution']='conservative_metadata_recommendation_membership_retained'
        else:f['coordinator_resolution']='recommended_correction'
        evidence=f.get('evidence',[])+f.get('additional_evidence',[])
        for e in evidence:
            rid=e['revision_id'];text=e.get('quote',e.get('excerpt',e.get('text')))
            if not text:errors.append([f['finding_id'],'missing quote']);continue
            quote_count+=1
            if text not in revs[rid]['body']:errors.append([f['finding_id'],rid,'quote absent'])
            start=e.get('start_char')
            if start is not None and revs[rid]['body'][start:start+len(text)]!=text:errors.append([f['finding_id'],rid,'offset mismatch'])
            if e.get('revisions_jsonl_line') and lines[e['revisions_jsonl_line']]!=rid:errors.append([f['finding_id'],rid,'source line mismatch'])
        replacements=[]
        for key in ['recommended_included_excerpts','recommended_retained_excerpts','discarded_excerpts']:replacements.extend((None,s) for s in f.get(key,[]))
        for oid,ss in f.get('recommended_included_excerpts_by_observation',{}).items():replacements.extend((oid,s) for s in ss)
        for oid,text in replacements:
            replacement_count+=1
            bodies=[revs[source_obs[oid]['revision_id']]['body']] if oid else [revs[e['revision_id']]['body'] for e in evidence]
            if not any(text in b for b in bodies):errors.append([f['finding_id'],oid,'proposed span absent'])
        findings.append(f)
manifest=json.loads((OUT/'input-manifest.json').read_text())
for p,expected in manifest.items():
    if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=expected:errors.append([p,'input changed'])
result=dict(coverage=coverage,reviewed_candidate_groups=sum(c['candidates'] for c in coverage),reviewed_trajectories=sum(c['trajectories'] for c in coverage),reviewed_observations=len(rows),checked_evidence_quotes=quote_count,checked_replacement_or_discarded_spans=replacement_count,finding_groups=len(findings),confidence_counts=dict(collections.Counter(f['confidence'] for f in findings)),input_files_unchanged=len(manifest),errors=errors)
(OUT/'findings.json').write_text(json.dumps(dict(status='audit_recommendations_not_applied',findings=findings),indent=2)+'\n')
with (OUT/'observation-review.csv').open('w') as h:
    w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'review-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if errors:raise SystemExit(1)
