import json,zipfile,pathlib,hashlib,collections
D=pathlib.Path('analysis/trajectory-assembly/batches/004');proposal_bytes=(D/'proposed-2.json').read_bytes();a=json.loads(proposal_bytes);p={x['candidate_id']:x for x in json.load(open(D/'partition-2.json'))};rs={r['rev_id']:r for r in map(json.loads,zipfile.ZipFile('full-wiki-logs.zip').open('revisions.jsonl'))};by=collections.defaultdict(list)
for r in rs.values():by[r['page_id']].append(r)
changes=collections.defaultdict(list)
def change(cid,oid,reason,delta,rules):changes[cid].append(dict(observation_id=oid,reason=reason,proposed_decision='include',proposed_change=delta,rule_ids=rules))
for c in a:
 cid=c['candidate_id'];obs={o['observation_id']:o for o in c['observations']}
 if 'FP-S004239' in obs:
  o=obs['FP-S004239'];s=o['included_excerpts'][0];trim=s[s.index('ADVANCE R4'):];o['included_excerpts']=[trim];o['reason']+=' Trim the initial unattributed R3 sentence: it repeats Jul18\'s separately signed prior R3 claim and must not enter the retained Nov05 own span.';o['rule_ids']=list(dict.fromkeys(o['rule_ids']+['R06']))
  change(cid,o['observation_id'],'Initial R3 19:18:57 clause is unattributed peer material copied/paraphrased from the separately signed Jul18 report immediately above. Retain the fresh Nov05/Jan17 relay from ADVANCE onward.',{'included_excerpts':[trim],'discarded_excerpts':[s[:s.index('ADVANCE R4')]]},['R04','R06'])
 if 'FP-S001318' in obs:
  o=obs['FP-S001318'];o['cross_post_of']='FP-S001287';o['depends_on']=list(dict.fromkeys(o['depends_on']+['FP-S001287']));o['rule_ids']=list(dict.fromkeys(o['rule_ids']+['R07']));o['reason']+=' This destination publication repeats the accepted R3/NH-cache event in FP-S001287; do not count it as independent corroboration.'
  change(cid,o['observation_id'],'Own R3 04:52:18 and cached NH restate FP-S001287 on a different page. Preserve destination, add event relationship.',{'cross_post_of':'FP-S001287'},['R07'])
 for t in c['trajectories']:
  for k in t['schedule_claims']:
   if k['observation_id']=='FP-S003820' and k['round']=='R5':
    k['raw_value']='21:48:33, likely :34'
    change(cid,k['observation_id'],'The source explicitly gives nominal :33 and likely :34; raw selected clock must preserve both rather than a single precise forecast.',{'round':'R5','raw_value':k['raw_value']},['R09','R11'])
   if k['observation_id'] in ['FP-S000982','FP-S003034','FP-S003137'] and k['round']=='R1':
    date={'FP-S000982':'Jul17','FP-S003034':'Aug 02','FP-S003137':'Feb 28'}[k['observation_id']];k['task_date']=date
    if not any(x['observation_id']==k['observation_id'] and x['proposed_change'].get('schedule_claim_task_date')==date for x in changes[cid]):change(cid,k['observation_id'],'The source explicitly dates its R1 task-clock report; retain that literal month/day without inventing a year.',{'round':'R1','schedule_claim_task_date':date},['R09'])
notes=[
'Jul17 own Texas03:26:09 and Louisiana04:14:18 lead to NY04:52:18; Oct20 is explicitly 27 seconds earlier. NH arrives05:30:19 under47s tier. Jul30 paragraph on own-named page is another signer and correctly not retained.',
'May30 R3 2016 at06:57:51 and24m/11s yield07:22:02; later own current07:11:17,07:12:42 and updated countdowns are substantive new reports in separate revisions. Expanded backup data is correctly linked as event restatement.',
'Nov19 own R2 California01:53:07, transition01:53:39 and35m11 give Texas02:28:50; own R4 03:04:33 and R5 03:40:16 continue35m43 steps. Jul08 is explicitly different AZ/UT/CO/NM task. Generic initial polling remains unresolved; later independently task-specific reply does not seed a weak link. The predicted02:28:20 cutoff is not an endpoint.',
'Nov05 R4 due08:44:40 is fulfilled at08:44:40 in a later revision, with R5 due09:00:45. Jan17 times are explicitly peer; initial Jul18 R3 clause must be trimmed. Named YOURLS contact reply responds directly to accepted request and does not claim new peer arrivals as own.',
'Jul30 evening22s own activation20:20:39 and R3 21:08:12 connect R4 arrival21:28:23 and later survival past predicted22:05:39 cutoff. Two survival reports share one revision but earlier activation/R4 revisions independently support the run. Forecast R5 uncertainty :33/:34 restored.',
'May24 Flathead08:25:42 with4m44 and Merced09:08:37 with27s match later SanJuan09:47:15/Saginaw10:25:54. Saginaw differs by1s from forecast, which is documented as forecast refinement, not an arrival conflict.',
'Independent alias confirmed: Aug02Agent earlier R1 19:11:35/deadline19:23:53 and corrected forecast20:52:29 lead on Aug02Live to Aug02Precision\'s explicit own precision correction, actual20:52:29 arrival/deadline20:53:25, R3 22:22:01/R4 23:51:33. Four exact landmarks plus first-person correction establish one reported history; counter01:59:55 is peer context.',
'Jan21 slow OECD R1 arrival07:31:58/deadline07:50:37 and18m39 tier connect Hungary09:02:04 and deadline09:03:24. R3 deadline10:16:12 gives11:27:39 R4 with a one-second progression slip. The replacement of Mar16 is newly authored Jan21 text, not an inherited same-signer message.',
'Nov22Researcher R1 05:26:52/deadline05:39:10 is12m18 tier and conflicts with existing Nov22Scout slow-run history, so no name/date-only merge. Failed candidate forecasts are explicitly replaced by07:07:46 Hungary and08:37:18 Poland arrivals.',
'Dec27 sector61 MA15:54:05/CT16:22:11 and2m/13s lead to MI16:48:30, then WV17:14:50/R5 17:41:10 forecasts and a concrete pre-answer daemon plan. Peer Jun20 noon timestamp is not assigned to self.',
'Apr09 R3 05:37:07 exists in an earlier revision than combined R4/R5/continuation reports. All later blocks in@6 have distinct own content except the second R6 continuation paraphrase, correctly excluded. Scheduled06:04:51 is never converted into arrival or verified endpoint.',
'Aug19 FP initial R1-R4 progression is one archived revision. The other timed publication repeats R4 due21:57:11/current21:54/UTC18:50, and Aug02 inquiry supplies common family answers rather than distinctive new self task evidence. Two-independent-publication threshold is not met; defer remains appropriate.',
'Sep11 construction original NY/CA plus TX00:42:37/FL01:11:41 history is all in@1. Main-hub@59 repeats those same TX/FL events with identical14s and futureNE01:40:45, so two revisions do not supply two independent substantive contributions. Deferred status upheld.',
'Dec28 first R2/R3 status occurrence at body line20 is newly inserted versus@49; second identical occurrence atline39 in@50 is excluded. Later R3 02:48:17 and R4 03:40:56/R5 04:33:35 progression occurs in distinct revisions. Full founding block before signoff is owned and fresh; R6 05:26:14 remains a scheduled future.',
'Feb28 OECD R1 12:46:10/deadline12:58:28 and failed candidate tests support fresh trimmed@2 correction. Actual Hungary14:27:04 with56s then Poland15:56:36 follow1h28m36. Inferred14:28:00 deadline is correctly inferred; live-chart value corrections are not fresh arrivals.',
'Apr18 own Texas11:17:51/Louisiana12:13:30 and46s lead to NY12:57:39 with a one-second forecast slip and announcedNH13:41:46. NM/CA counter forensic exchange explicitly continues the accepted named signal plan; later CA maintenance describes edits to a shared counter, never own R5. Apr10 shares a peer counter timestamp but has incompatible own schedule.',
'Nov18 AZ18:59:42/UT19:33:01 with6m09/17s andCO20:00:28 are consistently extended by R4/R5 forecast refinements. New~9m countdown to20:55:24 supplies substantive current status. Jul27 estimated mapped20:53 is a peer expectation, not Nov18 arrival. No exact observed-arrival conflict established.'
]
aud=[];res=[]
for c,note in zip(a,notes):
 cid=c['candidate_id'];obs={o['observation_id']:o for o in c['observations']};coverage=[]
 for src in p[cid]['observations']:
  o=obs[src['observation_id']];r=rs[o['revision_id']];b=rs.get(r['diff_base'],{}).get('body','');earlier=[]
  for s in o['included_excerpts']:
   assert s in r['body'];earlier += [v['rev_id'] for v in by[r['page_id']] if v['seq']<r['seq'] and s in v['body']]
  assert not earlier,(src['observation_id'],earlier)
  coverage.append(dict(observation_id=src['observation_id'],revision_id=r['rev_id'],revisions_jsonl_line=src['revisions_jsonl_line'],body_line=src['body_line'],diff_base=r['diff_base'],original_decision=next(x for x in json.loads(proposal_bytes) if x['candidate_id']==cid)['observations'][len(coverage)]['decision'],reviewed_decision=o['decision'],source_excerpt=src['excerpt'],source_body_sha256=r['body_sha256'],freshness_checked=True,full_owned_span_in_earlier_same_page_revisions=earlier,review_note=o['reason']))
 for t in c['trajectories']:
  for k in t['schedule_claims']:assert k['excerpt'] in rs[obs[k['observation_id']]['revision_id']]['body'];assert k['raw_value'] in k['excerpt']
 verdict='revise' if changes[cid] else 'pass'
 check=dict(speaker='Inspected all source clauses, signs, preceding signed/unsigned blocks and parent revision; peer clauses retained only as explicit relay context, with mixed Nov05 prefix trimmed.',freshness='Inspected original body and diff-base changes for every observation; also screened every final retained span against every earlier same-page revision.',task_continuity=note,observed_predicted_distinction='Reviewed every selected clock against literal source. Bare confirmations remain other, future schedules remain due, inferred deadline and speculative endpoints retain their statuses.',duplicate_alias_collisions='Compared accepted-fingerprints including original baseline and batch collision retrieval; examined owned versus peer clocks. Aug02 alias independently supported; other hits are explicit peers or unrelated families.',coverage=dict(input_observations=len(coverage),reviewed_observations=len(coverage),included_reviewed=sum(o['decision']=='include' for o in c['observations']),selected_clock_claims_reviewed=sum(len(t['schedule_claims']) for t in c['trajectories'])))
 record=dict(candidate_id=cid,signature=c['signature'],verdict=verdict,checks=check,issues=changes[cid],rationale=note,observation_reviews=coverage)
 if c['signature']=='OECDEquityAug02Agent':
  alias_spans=[]
  for rev,token in [('dse~OECDEquityAug02Live@4','UPDATE: exact-tier'),('dse~OECDEquityAug02Live@5','PRECISION CORRECTION'),('dse~OECDEquityAug02Live@6','R2 CONFIRMED')]:
   rr=rs[rev];s=next(x for x in rr['body'].splitlines() if x.startswith(token));assert s not in rs[rr['diff_base']]['body'];alias_spans.append(dict(revision_id=rev,diff_base=rr['diff_base'],excerpt=s))
  record['alias_resolution']=dict(status='independently_confirmed',canonical_trajectory_id='C30dde3d5edc3/1',alias_trajectory_id='C3099c8907b1f/1',exact_evidence=alias_spans,rationale='Four own schedule landmarks coincide, plus explicit our-R2 correction from preceding value on same page and subsequent actual R2 arrival. Not a name/page-only merge. Root may integrate alias without adding a new trajectory count.')
 aud.append(record)
 res.append(dict(candidate_id=cid,signature=c['signature'],status='resolved',audit_verdict=verdict,changes=[dict(observation_id=x['observation_id'],action=x['reason'],change=x['proposed_change'],status='applied') for x in changes[cid]],final_disposition=c['disposition'],final_owned_publication_revisions=len({o['revision_id'] for o in c['observations'] if o['decision']=='include'}),validation='All observations independently reviewed against original source and diff base; final retained/clock spans literal; no entire owned span repeats in older same-page revision. Independent threshold and peer/forecast distinctions checked.'))
(D/'assembly-2.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n');(D/'audit-2.json').write_text(json.dumps(aud,indent=2,ensure_ascii=False)+'\n');(D/'resolution-2.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
assert (D/'proposed-2.json').read_bytes()==proposal_bytes
print('Audit:',len(aud),'candidates',sum(len(x['observation_reviews']) for x in aud),'observations;',sum(map(len,changes.values())),'issues applied;',collections.Counter(x['verdict'] for x in aud))
