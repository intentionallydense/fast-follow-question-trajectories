import json,zipfile,hashlib,copy
from pathlib import Path
D=Path('analysis/trajectory-assembly/batches/004');proposed=json.load(open(D/'proposed-3.json'));out=copy.deepcopy(proposed)
inputs={o['observation_id']:o for c in json.load(open(D/'partition-3.json')) for o in c['observations']}
rs={r['rev_id']:r for r in map(json.loads,zipfile.ZipFile('full-wiki-logs.zip').open('revisions.jsonl'))}
# Findings from independent manual review of every source block and its immediately preceding speakers.
fixes={
'FP-S003360':{'reason':'This later dedicated-page paragraph restates R2 08:13:08 already present in earlier outbound R3-confirmed report FP-S003299. Retain publication, encode repeated-event dependency; no second R2 event at later archive timestamp.','proposed_change':{'cross_post_of':'FP-S003299'},'rule_ids':['R07','R14']},
'FP-S001919':{'reason':'The replacement adds R4 arrival/R5 forecast but its closing R6 request and signoff are byte-identical in the diff base. Trim those inherited trailing words; attribution remains supported by signoff context in original source.','proposed_change':{'included_excerpts':['R4 New Hampshire arrived 03:52:20, answered 1.32%. R5 due about 04:36:28 task-clock; ready California 11.2%.']},'rule_ids':['R05','R06']},
'FP-S002491':{'reason':'Source explicitly identifies +1s arrival jitter relative to prior 20:58:36 forecast. Preserve correction/progression relation from observed20:58:37 to prior forecast without implying contradictory observed arrivals.','proposed_change':{'claim_id':'FP-S002491/clock1','supersedes':'FP-S002355/clock3'},'rule_ids':['R09','R11']},
'FP-S001773':{'reason':'Dedicated signal-page creation repeats owned R5 target22:11:54 and before-final state beacon plan already posted in FP-S001612. Retain this distinct destination publication with event dependency.','proposed_change':{'cross_post_of':'FP-S001612'},'rule_ids':['R07','R14']}
}
notes=[
'Jan06 own R1 07:06:55/R2 08:13:08 and R3 09:05:47 bridge to later R5 10:51:05. Own R5/history is distinct from preceding Dec28 messages. Alive11:22:02 is not R6 arrival.',
'Jan13 16:06:33 initial, observed Capella16:53:07 and Utah17:34:57 are coherent. The ready-test replaces an already specifically anchored R4 signal page, so it is operational continuation rather than an unaffiliated scratch test.',
'Jul08 exact12m differs explicitly from Jun26/Jan16 24m. Initial/R3 share one revision, but R4 actual08:00:58 occurs in a new revision and independently meets threshold.',
'Jul21 21:12:06/21:29:27 and observed R2 22:05:50/53s distinguish the Jul21 run from relayed Jan21 07:50:37/09:02:04. Founding unsigned R1 paragraph properly governed by signoff; +1s R3 correction retained.',
'Jul27 scratch remains unresolved. Clothing CA10:35:51/NY12:36:33 and fresh mapping12:49:26 establish core; Aug14 clock inquiries are specific continuations of an anchored mapping exchange, not own prompt clocks.',
'Jun30 outbound R2 forecast11:00:50 precedes detailed own global09:30:56/R1 09:31:27 and R2 observed11:00:50 in another revision; second publication adds substantive chronology, not merely a crosspost. Dec13 difference3:30:05 explicitly distinguishes peer.',
'May25 activation18:59:25, global18:58:49, R5 answer20:14:30 and R6 due20:31:18 remain separate clocks. Cap20:30:29 is inference from peer heartbeat, while self survival checks are reported current-time events, not verified teardown.',
'Nov22 unique01:21:17 history all occupies one publication revision; generic slow-cohort Jun19/Jul10 requests do not distinguish it from other Nov22 own schedules. Mixed precision/R3 line is correctly identified but cannot satisfy two-revision gate.',
'Oct22 00:23:19/deadline00:35:37 plus revised R2 02:04:13 are distinctive independent contributions; peer May30 09:22:15 is queried, not owned. Counter hygiene lacks own bridge and remains associated only.',
'Dec10 17:43:17/18:42:16 core plus receipt of Jul23 Florida relay with own C3 target19:29:38 establishes substantive continuation; mapping challenge addresses specific anchored Jul23 exchange, with all queried event times peer-owned.',
'Feb21/Feb22 task dates expressly support midnight wrap22:25:51→23:25:05→00:09:40→00:54:16. Founding dedicated page adds actual R3/R4 beyond prior outreach; Jun09 detached probe report remains peer context.',
'Mar10 R3 18:58:20 through R5 19:16:49/continuation19:16:55 are fresh distinct revision contributions, separate from Apr09 own05:37:07 history on same page. R6 19:26:04 only scheduled.',
'Mar13 R1 17:27:29 and successive actual18:33:42→19:26:21→20:19:00→21:11:39 maintain43s/+51m55 progression; Jun03/Mar31 neighboring peer reports stay outside retained spans.',
'Oct14 French/Cajun01:28:24 history is incompatible with separate Bachelors2015 cashier15:16:57/15:29:08. Cashier other-page report only repeats same R3/R4/R5 and signal plan, so remains deferred. Language revised R4 arrival is new, with inherited suffix trimmed.',
'Oct18 singleton R4 11:41:59/R5~12:26:35 cannot merge into fast R2 20:33:16/R4~21:23:57. Retained fast history has observed R3 with explicit1s jitter; identical outbound R3 crosspost already linked; horizon6400s remains inferred.',
'Sep01 own19:29:44/20:17:53→R4 21:33:54→R5 due22:11:54→California signal is coherent. Generic UI reproduction has no specific run bridge; conflicting current-task01:27:33/~74661s countdown remains unresolved rather than silently relabeled server UTC. Final01:34:22 explicitly server signal time, not task arrival.'
]
audit=[];resolution=[];coverage=[]
for c,old,note in zip(out,proposed,notes):
 issues=[]
 for o in c['observations']:
  sid=o['observation_id'];r=rs[o['revision_id']];b=rs.get(r['diff_base'],{}).get('body','')
  if sid in fixes:
   f=copy.deepcopy(fixes[sid]);issues.append({'observation_id':sid,**f});change=f['proposed_change']
   if 'cross_post_of' in change:
    o['cross_post_of']=change['cross_post_of']
    if change['cross_post_of'] not in o['depends_on']:o['depends_on'].append(change['cross_post_of'])
   if 'included_excerpts' in change:
    o['included_excerpts']=change['included_excerpts'];o['discarded_excerpts']=['If thread survives R5, please relay R6 here. -- OpenAIResearchOct14X']
    for t in c['trajectories']:
     for cl in t['schedule_claims']:
      if cl['observation_id']==sid:cl['excerpt']=change['included_excerpts'][0]
   if 'claim_id' in change:
    cl=next(cl for t in c['trajectories'] for cl in t['schedule_claims'] if cl['claim_id']==change['claim_id']);cl['supersedes']=change['supersedes']
   o['reason']+=' Independent audit: '+f['reason']
   o['rule_ids']=list(dict.fromkeys(o['rule_ids']+f['rule_ids']))
  assert all(s in r['body'] for s in o['included_excerpts'])
  assert not any(s in b for s in o['included_excerpts'])
  oldo=next(x for x in old['observations'] if x['observation_id']==sid)
  earlier=[rr['rev_id'] for rr in rs.values() if rr['page_id']==r['page_id'] and rr['seq']<r['seq'] and any(s in rr['body'] for s in o['included_excerpts'])]
  assert not earlier,(sid,earlier)
  oo=inputs[sid];lines=r['body'].splitlines();k=oo['body_line']-1
  coverage.append({'candidate_id':c['candidate_id'],'observation_id':sid,'revision_id':r['rev_id'],'revisions_jsonl_line':oo['revisions_jsonl_line'],'source_body_sha256':r['body_sha256'],'diff_base':r['diff_base'],'original_decision':oldo['decision'],'final_decision':o['decision'],'independent_source_review':'reviewed','original_source_excerpt':oo['excerpt'],'preceding_source_context':'\n'.join(lines[max(0,k-3):k+1]),'exact_retained_spans_valid':True,'full_retained_span_in_diff_base':False,'earlier_same_page_full_repeats':earlier,'source_specific_assessment':o['reason']})
 verdict='revise' if issues else 'defer' if c['disposition']=='deferred' else 'pass'
 checks={'speaker':'pass; all supplied observations and preceding signoff context reviewed, including excluded/unresolved material','freshness':'pass after listed changes; exact literal spans checked against raw body, diff base and all earlier same-page revisions','task_continuity':note,'observed_predicted_distinction':'pass; reviewed selected clock claims and original supporting clauses; raw confirmations remain other, future due times do not establish observed arrivals','duplicate_alias_collisions':'pass after listed changes; compared accepted-fingerprints including baseline and exact own schedule landmarks, plus root collision-screen; no additional supported same-history alias. Destination repetitions are retained as publication evidence only.'}
 audit.append({'candidate_id':c['candidate_id'],'signature':c['signature'],'verdict':verdict,'checks':checks,'issues':issues,'rationale':note,'observation_ids':[o['observation_id'] for o in c['observations']],'reviewer':'assemble_b (independent of assembler assemble_c)','source_review_file':'source-review-3.json'})
 resolution.append({'candidate_id':c['candidate_id'],'signature':c['signature'],'status':'resolved','audit_verdict':verdict,'corrections':issues,'final_disposition':c['disposition'],'accepted_trajectory_count':len(c['trajectories'])})
(D/'assembly-3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(D/'audit-3.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(D/'resolution-3.json').write_text(json.dumps(resolution,ensure_ascii=False,indent=2)+'\n')
(D/'source-review-3.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
print({'candidates':len(audit),'observation_reviews':len(coverage),'retained_trajectories':sum(len(c['trajectories']) for c in out),'corrections':sum(len(x['issues']) for x in audit),'verdicts':{k:sum(x['verdict']==k for x in audit) for k in ('pass','revise','defer')}})
