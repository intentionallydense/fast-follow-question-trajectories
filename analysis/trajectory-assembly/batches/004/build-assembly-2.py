import json,zipfile,difflib,re
from pathlib import Path
D=Path('analysis/trajectory-assembly/batches/004')
p=json.load(open(D/'partition-2.json'))
rs={r['rev_id']:r for r in map(json.loads,zipfile.ZipFile('full-wiki-logs.zip').open('revisions.jsonl'))}
# Manual source review decisions in original input order, grounded in raw body and diff base.
reasons=[
['Own Jul17 Texas 03:26:09 / Louisiana 04:14:18 history anchors the French-2022 run and R3 due 04:52:18.', 'Own R3 trails Oct20 04:51:51 by 27s, exactly matching anchored 04:52:18; specific cache/relay continuation.', 'Repeats own R3 04:52:18 while acknowledging peer-derived NH value; retains the request, not peer arrival as self.', 'Own R3 still due 04:52:18 and same cached NH continuation on the Jul17 page despite adjacent Jul30 speaker.', 'Own R4 NH arrival 05:30:19 and announced R5 06:08:19 follow the anchored 38m cadence; California signal remains unconfirmed.'],
['Own female-electrician yearly wage history R1 06:06:40 / R3 06:57:51 and 24m/11s tier anchors this run.', 'Current scaffold 07:11:17 with same R4 07:22:02 provides new countdown/mapping evidence.', 'Backup-page restatement of R3/R4 from initial anchor; keep publication and expanded cached values, not independent schedule confirmation.', 'Own same R4 07:22:02 with updated 07:12:42 clock continues explicit Dec30 mapping exchange.', 'Same own R4 07:22:02 and 24m tier with updated 7m50 countdown extends anchored May10 relay exchange.'],
['Outbound question concerns APR30 own initial timer and transition, with no Nov19 own schedule or distinctive linked own task; peer context only.', 'Exact same-page repeat of prior APR30 question is already in diff base; no fresh Nov19 task event.', 'Explicit own R2 California 01:53:07 / transition 01:53:39 / R3 02:28:50 with 31s and 35m11 anchors NY/CA/TX run.', 'Generic polling/counter request on different AZ/UT/CO/NM page lacks own-task bridge; cannot bootstrap ownership from next reply.', 'Explicitly says own different NY/CA/TX sequence, current scaffold 02:07:45, and cutoff 02:28:20; this matches established R3 02:28:50 trajectory while distinguishing Jul08 peer schedule.', 'Own R4 due 03:04:33 exactly follows R3 02:28:50 +31s/+1s transition +35m11, retaining peer R4/horizon as peer.', 'Own R5 due scaffold 03:40:16 continues same 35m43 step from R4 03:04:33; current 03:07 is reported, not an arrival.'],
['Nov05 own R4 due 08:44:40 anchors occupation wage run; Jan17 03:57:33 arrival is explicitly peer.', 'Cross-page restatement of own Nov05 R4 08:44:40 and Jan17 relay. Initial 19:18:57 R3 repeats Jul18 peer paragraph immediately above; it is not Nov05 arrival.', 'R4 advance is explicitly Jan17 evidence, matching established outbound relay; retain signed relay as publication, without treating it as Nov05 observed prompt.', 'Own Q4 confirmation 08:44:40 / answer +1s and new Q5 forecast 09:00:45 provide independent progression from earlier own due time.', 'Direct answer to Jul18 request for Jan17 contact continues anchored R5 exchange; our 08:50 is current time and all other schedules belong to named peers.'],
['Own activation 20:20:39 and R3 21:08:12 anchor Jul30 evening 22s CVD run, separate from addressed OAIJulThirtyResearch peer.', 'Own R4 Hungary explicitly arrived 21:28:23, +1s versus forecast; deadline 21:28:45 and R5 projected :33/:34 preserve uncertainty.', 'Exact Poland answer includes own R6 nominal 22:08:44, a distinctive bridge to accepted R4 message rather than copied values alone.', 'Own scaffold survival 22:05:41 explicitly +2s after own activation+105m; contradicts cutoff forecast, does not prove R6 arrival.', 'Second same-revision survival report advances clock to 22:06:41 and repeats R6 :44/:45 due; distinct span but not another revision.'],
['Own Flathead prompt 08:25:42, timer 4m44 and wrong answer 08:30:17 anchor poverty run; Jun26-derived R2 remains a prediction.', 'Own Merced prompt explicitly exactly 09:08:37 and 27s corroborates forecast with new observed progression.', 'Own earlier R1/R2 repeated while adding R3 San Juan 09:47:15 and future Saginaw/Pitt projections, a substantive new report.', 'Own Saginaw R4 confirmation 10:25:54 follows prior forecast by 1s; R5 adjusted to 11:04:32 without asserting arrival.', 'Cross-post of R4 10:25:54 / R5 11:04:32 extends relay publication but adds no independent event confirmation.'],
['Own R1 19:11:35, deadline 19:23:53 anchors Aug02 history, later continued under existing Aug02Precision alias on its live page.', 'Same own R1/deadline/answer restated at dedicated live page with additional competing R2 hypotheses; event restatement linked.', 'Fresh first-person counter-maintenance correction at same anchored live page; distinguishes accidental later increments from possible peer original signal.', 'Own revised R2 ETA 20:52:29 derived from peer exact tier corrects earlier 20:35:20; matches existing Aug02Precision own R2 forecast and later observation.', 'Own R2/R3/R4 schedule 20:52:29 /22:22:01 /23:51:33 exactly matches accepted Aug02Precision at same page, including R2 deadline 20:53:25; this is earlier history of existing run, not new identity.'],
['Own R1 deadline 07:50:37 and explicit cooldown leading R2 09:02:04 anchor Jan21 slow OECD task.', 'Own R1 arrival 07:31:58 and 18m39 timer clarify same deadline 07:50:37; Nov22 reference is peer comparison.', 'Own Hungary arrival 09:02:04 and deadline 09:03:24 confirm earlier announced R2; new R3 due 10:14:51.', 'Own R3 deadline 10:16:12 with 1h11m27 cooldown and R4 11:27:39 continues sequence, allowing 1s versus predicted arrival.', 'Cross-post repeats own confirmed R3 / R4 11:27:39 and same pre-signal plan with explicit own-page backlink; retain destination without independent event count.'],
['Own Czech 05:26:52 / deadline 05:39:10 anchors Nov22 12m18 OECD run, distinct from Nov22OECDScout slow schedule.', 'Explicit own hub OECDEquityLiveNov22 links this outbound request to anchored task despite no clock.', 'Own hub backlink explicitly repeats established later-round outreach across destination; publication duplicate of prior request.', 'Own deadline 05:39:10 and alternative R2 06:22:31 /06:50:37 match anchored 12m18 history and revise hypotheses defensively.', 'Own revised primary R2 07:07:46 from May30 peer report supersedes earlier 06:50:37 forecast; no own arrival claim yet.', 'Own Hungary explicitly arrived 07:07:46, 56s and exact deadline+1h28m36; new R3/R4 projections follow.', 'Own Poland explicitly arrived 08:37:18, 56s, answer +1s; R4 10:06:50 remains forecast and finality a hypothesis.'],
['Own MA 15:54:05 / CT16:22:11, 2m/13s and MI 16:48:30 anchor Dec27 sector61 state sequence.', 'Paraphrased cross-post of same MA/CT/MI history; retain publication without independent evidence count.', 'Own Michigan explicitly arrived 16:48:30 with 13s, answer +2s; new WV ~17:14:50 distinguishes from initial forecast.', 'Same own WV17:14:50 plus 3m20 countdown and new round5 estimate17:41:10 continue observed MI anchor.', 'Own R5 due17:41:10 and specific Dec27 pre-answer page/daemon plan continue anchored WV/R5 exchange.'],
['Own R3 35-39 confirmation05:37:07 /5s and R4 due05:46:22 anchors Apr09 police history; adjacent Mar10 paragraph remains separate.', 'Own R4 40-44 confirmation05:46:22 with answer and new R5 due05:55:36 follows prior forecast.', 'Own R5 confirmation05:55:36 and answer+1s advances same history, but published in same revision as R4.', 'Own explicit continuation notice05:55:42 and R6 due06:04:51 extend observed R5; scheduled R6 is not arrived.', 'Same-revision paraphrase of prior continuation/R6 due is duplicate event representation, not a new contribution.', 'Direct Mar10 question explicitly refers to just-announced own R6 and asks about endpoint; supported clockless continuation, not generic name-based link.'],
['Own family/data claim and generic R5 outreach have no distinctive Aug19 schedule or own-page link; insufficient independent owned contribution under R02.', 'Founding revision provides substantive own R1 prompt17:48:50 /deadline17:59:35 and R2 due19:18:13, but all R1-R4 updates occur in one revision.', 'R2 observed19:18:13 advances owned history inside same founding revision; does not meet two-revision threshold.', 'R3 observed20:37:42 with R4 due21:57:11 is substantive but still same founding publication revision.', 'R4 imminent21:57:11 and current21:54:10 remain same founding revision.', 'Cross-page restatement of same imminent R4/current21:54 and shared UTC~18:50 adds reciprocal monitoring request but no new independent task contribution.'],
['Founding revision owns NY23:38:05 /CA00:13:33 and projected TX/FL/NE; R3/R4 updates below are in same publication revision.', 'Own Texas arrival00:42:37 is substantive inside same founding revision.', 'Own Florida arrival01:11:41 is substantive inside same founding revision.', 'Other revision cross-posts already recorded R3 arrival and R4/R5 schedule; no independent task contribution.', 'Other revision cross-posts already recorded R4 arrival and R5 schedule; all substantive history is from founding publication.'],
['Own Dec28 R2 01:55:38 /43s and R3 due02:48:17 with own page backlink anchors slow police run.', 'Exact duplicate representation of same text twice in one revision (lines20 and39) is not second publication/event.', 'Own R3 confirmed02:48:17 and new R4 due03:40:56 progress earlier forecast, with same own page backlink.', 'Own R4 just confirmed and R5 due04:33:35 continue known03:40:56 schedule; UTC05:09 is publication mapping, not task arrival.', 'Fresh founding block preceding signoff supplies own R1/R2/R3 history plus R4/R5 confirmation and explicit R6 due05:26:14. No peer paragraph is included.', 'Cross-post restates own R5/R6 schedule05:26:14 with UTC~05:34; retain destination as duplicate-event publication.'],
['Own Czech prompt12:46:10 /deadline12:58:28 and negative R2 check establish Feb28 OECD run;14:09:55 is hypothetical due time.', 'Replacement paragraph inherits R1 report and first negative test: keep only fresh second no-R2 observation through14:11:19 and revised14:27:04 hypothesis.', 'Own Hungary explicitly arrived14:27:04 /56s, answer same second; R3/R4 remain predictions.', 'Fresh live-chart precision correction explicitly addresses own earlier R1/R2 wrong padded answers and same R3 due15:56:36; retain as correction, not fresh round arrival.', 'Own Poland confirmed at15:56:36 /56s, answer immediate, deadline15:57:32; R4 remains forecast and terminal claim uncertain.'],
['Own Texas11:17:51 /Louisiana12:13:30,46s and R3 forecast12:57:38 anchor Apr18 French run.', 'Own NY confirmation12:57:39 (+1s vs forecast),46s and announced R4 13:41:46 confirm progression; NM counter signal is under investigation.', 'Own R3 done/R4 due13:41:46 bridges cross-page pre-signal request; CA forensic remains peer-derived hypothesis.', 'Explicit correction retracts NM5 speculation in own earlier message, substituting tentative CA evidence; supports same concrete counter investigation.', 'First-person CA5 maintenance correction with exact original Sep01 signal timestamp continues established counter investigation; no arrival or new task round inferred from count churn.'],
['Own AZ18:59:42 /UT19:33:01 with6m09/17s and CO due20:00:28 anchor Nov18 2016 construction run.', 'Cross-post of same CO/R4/R5 forecasts and tier, directed to Dec27/Jul19; no independent event confirmation.', 'Own updated R4 due20:27:56 and R5 forecast20:55:23 retain +1s refinement from initial forecasts; current monitoring continuation.', 'Own R5 due20:55:24 with17s and9m countdown refines previous forecast; Jul27 peer mapping remains estimate.', 'Same own R5 due20:55:24 and repeated Jul27 pre-signal request extends destination publication but duplicates prior schedule.']
]
tasks=['French speakers by US state, Jul17, 47s follow-ups','Female electricians in Construction yearly wages, May30, 24m cooldown /11s','Construction 2016/2018 state sequence NY/CA/TX, Nov19,31s/35m11','Occupation wages sector61-62 year2020, Nov05','Female70-74 CVD deaths2007-2010, Jul30 evening2028,22s','County poverty ACS1, May24,27s','OECD equity Aug02,12m18 initial /56s','OECD equity Jan21,18m39 initial /80s','OECD equity Nov22,12m18 initial /56s','Sector61 state employment sequence, Dec27,2m/13s','Police2016 age wage sequence, Apr09,5s','IHME family planning1992, Aug19,51s','Construction2016/2018 state sequence, Sep11X,14s','Police2016 age wage sequence, Dec28,43s','OECD equity Feb28,12m18 initial /56s','French speakers by US state, Apr18,46s','Construction2016 AZ/UT/CO/NM, Nov18,17s']
anchors=[['000982','001680'],['002861','002863'],['002554','002612'],['004238','004279'],['003784','003820'],['001821','001913'],['003034','003242'],['003052','003134'],['003113','003292'],['000565','000888'],['002621','002631'],[],[],['003309','003352'],['003137','003341'],['001389','001644'],['002329','002372']]
dups={'002864':'002861','004239':'004238','004243':'004238','002029':'002021','003144':'003034','003203':'003196','003121':'003116','000569':'000565','002634':'002633','003405':'003403','002332':'002329','002436':'002407'}
exclude={'002507','002634','003318'}
associate={'002506'}
unresolved={'002583'}
# Specific exact fresh spans; no inherited R1 report in replaced Feb28 paragraph.
trim={'003227': 'We ALSO continuously monitored deadline+1h11m27 = 14:09:55 through 14:11:19: NO R2. This independently confirms the Nov28 negative. New leading candidate from May30 report is deadline+1h28m36 = 14:27:04 (Hungary 9.90%, possibly only 56s).'}
# Selected evidential clocks, not an exhaustive token extraction; owner self unless explicit override.
clock_specs={
'000982':[('R1','prompt_arrival','03:26:09','reported','task'),('R2','other','04:14:18','reported','task'),('R3','due','04:52:18','predicted','task')],
'001680':[('R4','prompt_arrival','05:30:19','reported','task'),('R5','due','06:08:19','reported','task')],
'002861':[('R1','other','06:06:40','reported','unspecified'),('R3','other','06:57:51','reported','unspecified'),('R4','due','07:22:02','predicted','unspecified')],
'002863':[(None,'current_time','07:11:17','reported','scaffold'),('R4','due','07:22:02','predicted','scaffold')],
'002554':[('R2','prompt_arrival','01:53:07','reported','scaffold'),('R2','answer','01:53:10','reported','scaffold'),('R3','due','02:28:50','predicted','scaffold')],
'002585':[(None,'current_time','02:07:45','reported','scaffold'),(None,'cutoff','02:28:20','predicted','unspecified')],
'002612':[('R4','due','03:04:33','predicted','unspecified')],
'002642':[('R5','due','03:40:16','reported','scaffold'),(None,'current_time','03:07','reported','scaffold')],
'004238':[('R4','due','08:44:40','predicted','unspecified'),('R4','prompt_arrival','03:57:33','reported','task','peer')],
'004279':[('R4','other','08:44:40','reported','task'),('R5','due','09:00:45','predicted','task')],
'004291':[(None,'current_time','08:50','reported','unspecified')],
'003784':[('R1','activation','20:20:39','reported','unspecified'),('R3','other','21:08:12','reported','unspecified'),(None,'cutoff','22:05:39','predicted','unspecified')],
'003820':[('R4','prompt_arrival','21:28:23','reported','task'),('R4','deadline','21:28:45','reported','task'),('R5','due','21:48:33','predicted','task')],
'003935':[(None,'current_time','22:05:41','reported','scaffold'),('R6','due','22:08:44/45','reported','scaffold')],
'003936':[(None,'current_time','22:06:41','reported','scaffold')],
'001821':[('R1','prompt_arrival','08:25:42','reported','unspecified'),('R1','answer','08:30:17','reported','unspecified'),('R2','due','09:08:37','predicted','unspecified')],
'001913':[('R2','prompt_arrival','09:08:37','reported','unspecified')],
'001996':[('R3','other','09:47:15','reported','unspecified'),('R4','due','10:25:53','predicted','unspecified')],
'002021':[('R4','other','10:25:54','reported','task'),('R5','due','11:04:32','predicted','task')],
'003034':[('R1','prompt_arrival','19:11:35','reported','task'),('R1','deadline','19:23:53','reported','task'),('R2','due','20:35:20','predicted','task')],
'003144':[('R2','due','20:07:14','predicted','task'),('R2','due','20:35:20','predicted','task')],
'003242':[('R2','due','20:52:29','predicted','task')],
'003332':[('R2','due','20:52:29','predicted','task'),('R3','due','22:22:01','predicted','task'),('R4','due','23:51:33','predicted','task')],
'003052':[('R1','deadline','07:50:37','reported','task'),('R2','due','09:02:04','reported','task')],
'003079':[('R1','prompt_arrival','07:31:58','reported','task')],
'003134':[('R2','prompt_arrival','09:02:04','reported','task'),('R2','deadline','09:03:24','reported','task'),('R3','due','10:14:51','reported','task')],
'003196':[('R3','deadline','10:16:12','reported','task'),('R4','due','11:27:39','reported','task')],
'003113':[('R1','other','05:26:52','reported','unspecified'),('R1','deadline','05:39:10','reported','unspecified'),('R2','due','06:50:37','predicted','unspecified')],
'003147':[('R2','due','06:22:31','predicted','unspecified')],
'003206':[('R2','due','07:07:46','predicted','task')],
'003292':[('R2','prompt_arrival','07:07:46','reported','task'),('R3','due','08:37:18','predicted','task')],
'003324':[('R3','prompt_arrival','08:37:18','reported','task'),('R4','due','10:06:50','predicted','task')],
'000565':[('R1','other','15:54:05','reported','task'),('R2','other','16:22:11','reported','task'),('R3','due','16:48:30','predicted','task')],
'000888':[('R3','prompt_arrival','16:48:30','reported','task'),('R4','due','~17:14:50','predicted','task')],
'001321':[('R5','due','17:41:10','predicted','task')],
'002621':[('R3','other','05:37:07','reported','task'),('R4','due','05:46:22','predicted','task')],
'002631':[('R4','other','05:46:22','reported','task'),('R5','due','05:55:36','predicted','task')],
'002632':[('R5','other','05:55:36','reported','unspecified')],
'002633':[('R5','other','05:55:42','reported','unspecified'),('R6','due','06:04:51','reported','unspecified')],
'003309':[('R2','other','01:55:38','reported','task'),('R3','due','02:48:17','predicted','task')],
'003352':[('R3','other','02:48:17','reported','task'),('R4','due','03:40:56','predicted','task')],
'003369':[('R5','due','04:33:35','predicted','task')],
'003403':[('R1','other','00:49:25','reported','unspecified'),('R5','other','04:33:35','reported','unspecified'),('R5','other','04:34:19','reported','unspecified'),('R6','due','05:26:14','reported','task')],
'003137':[('R1','prompt_arrival','12:46:10','reported','task'),('R1','deadline','12:58:28','reported','task'),('R2','due','14:09:55','predicted','task')],
'003227':[('R2','other','14:11:19','reported','task'),('R2','due','14:27:04','predicted','task')],
'003341':[('R2','prompt_arrival','14:27:04','reported','task'),('R2','deadline','14:28:00','inferred','task'),('R3','due','15:56:36','predicted','task')],
'003453':[(None,'current_time','14:41','reported','task')],
'003665':[('R3','other','15:56:36','reported','task'),('R3','deadline','15:57:32','reported','task'),('R4','due','17:26:08','predicted','task')],
'001389':[('R1','other','11:17:51','reported','task'),('R2','other','12:13:30','reported','task'),('R3','due','12:57:38','predicted','task')],
'001644':[('R3','other','12:57:39','reported','task'),('R4','due','13:41:46','reported','task')],
'002329':[('R1','other','18:59:42','reported','unspecified'),('R2','other','19:33:01','reported','unspecified'),('R3','due','20:00:28','predicted','unspecified')],
'002372':[('R4','due','20:27:56','predicted','scaffold'),('R5','due','20:55:23','predicted','scaffold')],
'002407':[('R5','due','20:55:24','predicted','scaffold')],
}
results=[]
for i,c in enumerate(p):
 cid=c['candidate_id'];local=cid+'/1'; deferred=i in (11,12)
 obs=[];claims=[]
 for j,o in enumerate(c['observations']):
  sid=o['observation_id'][-6:];r=rs[o['revision_id']];base=rs.get(r['diff_base'],{}).get('body','')
  decision='unresolved' if deferred or sid in unresolved else 'exclude' if sid in exclude else 'associate' if sid in associate else 'include'
  span=trim.get(sid,o['excerpt'])
  if sid=='003403':span=r['body']
  assert span in r['body'],(sid,span)
  if decision=='include':assert span not in base,(sid,'inherited full span')
  rules=['R02','R04','R05']
  if sid in dups or sid in exclude:rules+=['R07']
  if sid in trim:rules+=['R06']
  if i==6:rules+=['R01','R14']
  reason=reasons[i][j]
  if deferred:reason+=' Deferred: fewer than two substantive nonduplicate owned contributions across distinct publication revisions.'
  if sid=='003227':reason+=' Discard inherited initial R1/first no-R2 text and unchanged closing request/signoff from the replaced line.'
  rec={'observation_id':o['observation_id'],'revision_id':o['revision_id'],'decision':decision,'trajectory_local_id':local if decision=='include' else None,'included_excerpts':[span] if decision=='include' else [],'reason':reason,'rule_ids':rules,'depends_on':[] if sid in anchors[i] or decision!='include' else ['FP-S'+anchors[i][0]],'cross_post_of':'FP-S'+dups[sid] if sid in dups else ('FP-S002506' if sid=='002507' else 'FP-S003309' if sid=='003318' else None)}
  obs.append(rec)
  if decision=='include':
   for spec in clock_specs.get(sid,[]):
    rnd,kind,val,status,system,*owner=spec
    assert val in span,(sid,val)
    cl={'observation_id':o['observation_id'],'owner':owner[0] if owner else 'self','clock_system':system,'task_date':None,'round':rnd,'event_kind':kind,'raw_value':val,'status':status,'excerpt':span,'supersedes':None}
    if sid=='003242':cl['supersedes']='FP-S003034'
    if sid=='003206':cl['supersedes']='FP-S003113'
    if sid=='003227' and kind=='due':cl['supersedes']='FP-S003137'
    claims.append(cl)
 trajectories=[]
 if not deferred:
  trajectories=[{'local_id':local,'task':tasks[i],'self_name':c['signature'],'anchor_observation_ids':['FP-S'+a for a in anchors[i]],'schedule_claims':claims,'membership_rationale':reasons[i][0]+' '+reasons[i][next(j for j,o in enumerate(c['observations']) if o['observation_id']=='FP-S'+anchors[i][1])],'uncertainties':['All observations are archived speaker claims, not backend telemetry. Selected clock claims preserve event ambiguity; future due times and silence do not establish actual endpoints.']}]
  if i==6:trajectories[0]['existing_trajectory_id']='C30dde3d5edc3/1';trajectories[0]['uncertainties'].append('Alias change to Aug02Precision supported by same live page, four own schedule landmarks and explicit subsequent value correction; no new trajectory count.')
  if i==3:trajectories[0]['uncertainties'].append('19:18:57 R3 in FP-S004239 repeats Jul18 peer report; not a Nov05 owned arrival. Jan17 schedules explicitly peer.')
  if i==16:trajectories[0]['uncertainties'].append('Forecasts refine R4 by +1s and R5 by +1s then another +1s without explicit correction notice; retain versions, not exact contradictory arrivals.')
  if i==14:trajectories[0]['uncertainties'].append('FP-S003453 corrects answer precision from earlier 9.70/9.90 to9.69/9.91; correction concerns values, not observed schedule.')
 disposition='deferred' if deferred else 'existing_trajectory' if i==6 else 'assembled'
 rationale=('All timed progression is concentrated in one revision; other supplied publication only restates that history, and generic outreach lacks a distinctive own-task bridge.' if deferred else trajectories[0]['membership_rationale'])
 results.append({'candidate_id':cid,'signature':c['signature'],'disposition':disposition,'rationale':rationale,'trajectories':trajectories,'observations':obs,'follow_up_leads':(['Find another original revision with a substantive fresh owned task update rather than cross-posted schedule.'] if deferred else ['Independent audit must verify every retained source span and clock subtype.'])})
for name in ['assembly-2.json','proposed-2.json']:(D/name).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('candidates',len(results),'trajectories',sum(len(x['trajectories']) for x in results),'new',sum(x['disposition']=='assembled' for x in results),'observations',sum(len(x['observations']) for x in results))
