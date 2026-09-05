import json,zipfile,pathlib,hashlib,re
O=pathlib.Path(__file__).parent
rr=[json.loads(x) for x in zipfile.ZipFile('full-wiki-logs.zip').read('revisions.jsonl').splitlines()]
rows={r['rev_id']:r for r in rr}; nums={r['rev_id']:i for i,r in enumerate(rr,1)}
subnums={json.loads(x)['rev_id']:i for i,x in enumerate(open('coordination-subset/data/revisions.jsonl'),1)}
D=[];R=[];decisions=[]
def ref(page,n):return 'dse~'+page+'@'+str(n)
def fresh(page,n,prefix=None):
 r=rows[ref(page,n)];ls=r['body'].splitlines(True)
 s='\n'.join(''.join(ls[h['b0']:h['b1']]) for h in r['hunks'] if h['op']!='delete').strip()
 if prefix:s=s[s.index(prefix):]
 # repeated post in MCV live revision: only first copy
 if page=='HealthdataMCV2SequenceCollab' and n==2:s=s.split('\n\n')[0]
 return s

def add(key,task,name,title,bridge,spec):
 tid='FC-'+key
 messages=[]
 for page,n,prefix in spec:
  rid=ref(page,n);r=rows[rid];s=fresh(page,n,prefix)
  start=r['body'].index(s);oid=tid+':'+str(len(messages)+1)
  m=dict(observation_id=oid,revision_id=rid,decision='include',trajectory_local_id=tid,included_excerpts=[s],reason=f'Fresh owned contribution: {s[:180]} Continuity: {bridge}',rule_ids=['R02','R04','R05','R06','R08'],depends_on=[] if not messages else [messages[0]['observation_id']],cross_post_of=None,source_body_line=r['body'][:start].count('\n')+1,revisions_jsonl_line=nums[rid],diff_base=r['diff_base'],source_excerpt=s,source_line=nums[rid],body_line=r['body'][:start].count('\n')+1,page_id=r['page_id'],utc=r['time'],editor=r['label'],signature=name,spans=[dict(text=s,start_char=start,end_char=start+len(s),source_char_positions=[start],length=len(s),text_sha256=hashlib.sha256(s.encode('latin1')).hexdigest(),location_uncertainty=None)])
  messages.append(m)
  decisions.append(dict(m,archive_jsonl_line=nums[rid]))
 d=dict(local_id=tid,trajectory_id=tid,task_id=task,task=title,self_name=name,signature=name,anchor_observation_ids=[m['observation_id'] for m in messages[:2]],schedule_claims=[],membership_rationale=bridge,uncertainties=['Archive posts are self-reports, not authenticated backend telemetry.','No later arrival or termination is inferred from silence.'],batch='family-completion-b',status='independently_audited_reported_trajectory',owned_messages=messages,associated_messages=[],unassigned=[],excluded=[],candidate_follow_up_leads=[],owned_publication_count=len(messages))
 D.append(d);R.append(dict(trajectory_id=tid,events=[],timing=[]));return d
I='DataUSAIvyTuitionSequenceCollab2027';P='AgentOurIvyProbe1781643368';LF='LFSequenceCollabMay03';F='OpenAIFuelPovertyJan01Live';MC='HealthdataMCV2SequenceCollab';MD='IhmeMcv2DataCollab2028'
specs=[
('ivy-aug12','college-state-tuition-2015','OpenAIIvyAug12Helper','Ivy tuition Aug12 2027','Own Aug12 Arkansas→Pitt sequence, 20s follow-up; Pitt 17:05:39 and R3 17:43:16 recur in the signed timing map.',[(I,1,None),(I,8,None),(I,14,None)]),
('ivy-sep30','college-state-tuition-2015','OpenAIIvySep30Helper','Ivy tuition Sep30','Arkansas 21:50:44, Pitt 22:32:34, then R3 23:10:11; shortened Sep30 signature continues the same specific clock-alignment exchange.',[(I,2,None),(I,9,None),(I,12,None),(I,17,None)]),
('ivy-nov11','college-state-tuition-2015','OpenAIIvyNov11Helper','Ivy tuition Nov11 2027','Own Nov11 Arkansas 04:49:54 and Pitt due/received 05:31:44 bridge the follow-up report and requests to Aug12.',[(I,4,None),(I,6,None),(I,13,None),(I,16,None)]),
('ivy-jun23','college-state-tuition-2015','OpenAIJun23Helper','Ivy tuition Jun23 2028','Pitt 21:16:52 and R3 due 21:54:29 match current 21:41:35 plus 12m54s; same signed mapping exchange.',[(I,10,None),(I,18,None)]),
('ivy-feb22','college-state-tuition-2015','OpenAIIvyFeb22Helper','Ivy tuition Feb22','Own Arkansas 21:07:39, Pitt 21:49:29, R3 22:27:06; probe outreach repeats exact R3 time and backlink, then own current 22:24:34.',[(I,11,None),(P,3,None),(P,5,None),(I,20,None)]),
('ivy-aug19','college-state-tuition-2015','OpenAIIvyAug19Helper','Ivy tuition Aug19','Own R1 ANC/R2 Pitt and R3 due Aug19 23:32:29 repeat across first-person countdown update in Feb22 exchange despite changed editor label.',[(P,4,None),(P,8,'Aug19 urgent ping:')]),
('slp-mar09','datausa-slp-ethnicity','OpenAISpeechMar09','SLP Puerto Rican ethnicity Mar09','Own 2020 SLP male/female 168/2840, 3m initial plus 24m cooldown, R2 due Mar09 04:59:59; explicit backlink across SLP and FooBar outreach.',[('DataUSASpeechPathEthnicityMar09',1,None),('DataUSASLPSeqMay05',2,None),('DataUSASLPSeqMay05',3,None),('FooBar579257',2,None)]),
('slp-dec05','datausa-slp-ethnicity','ResearchReaderDec05X','SLP Puerto Rican ethnicity Dec05','Own R1 09:28:28 2020 168/2840 and R2 due 09:55:28 connect the same Dec05 R2 countdown and expected 2021 values.',[('DataUSASLPSequenceDec05Live',1,None),('DataUSASLPSequenceDec05Live',2,None)]),
('fuel-may17','fuel-poverty-ni','OpenAIFuelMay17','NI fuel poverty May17','Own R1 04:04:13→R2 04:41:37→R3 05:11:42, R4 due/arrival 05:41:47; explicit R5 counter coordination ACK continues Dec28 exchange.',[(F,2,None),(F,4,None),(F,7,None)]),
('fuel-dec28','fuel-poverty-ni','OpenAIFuelDec28','NI fuel poverty Dec28','Own R1 05:40:36→R2 06:18:00→R3 06:48:05 and R4 due/arrival 07:18:10 connect signed R5 counter request and horizon correction despite changing editor labels.',[(F,3,None),(F,5,None),(F,6,None),(F,9,None)]),
('fuel-nov30','fuel-poverty-ni','FuelPovertyNov30Scout','NI fuel poverty Nov30 slow tier','Own Nov30 R1 21:25:24, R2 22:36:53, slower 46s/1h5m6 tier explicitly backlinks Jan01 page; signed Nov30 crosslink and follow-up correct horizon, report indirect signal.',[('OpenAIFuelPovertyNov30Live',1,None),(F,8,None),(F,10,None)]),
('lf-nov14','ihme-lymphatic-filariasis','LFRelayNov14','Lymphatic filariasis Nov14','Nov14 14m16s initial, first deadline 17:51:02, cooldown 1h44m45s, follow-up due and received 19:35:47; signed clock-sync and 2008 arrival survive editor changes.',[(LF,n,None) for n in [2,4,6,8,10,12,14]]),
('lf-apr15','ihme-lymphatic-filariasis','LFRelayApr15','Lymphatic filariasis Apr15','Own Apr15 follow-up due 14:42:15 repeats in current-clock/countdown exchanges; LFAlign aliases and LFHeartbeat/PromptFirst requests continue the same explicitly addressed Nov14 conversation.',[(LF,n,None) for n in [3,5,7,9,11,13]]+[('DataUSAClothing9m17Nov14Live',4,None)]),
('mcv-mar28','ihme-mcv2','MCV research agent, Mar 28','MCV2 coverage Mar28','Own Indonesia→Samoa→Algeria sequence, retired 2008 MCV2 research, exact R4 Mar28 21:07:32 and backlink bind discovery and signed 43s live update across editor labels.',[(MD,1,None),(MD,3,None),(MC,1,None),(MC,2,None)]),
('mcv-aug11','ihme-mcv2','MCVScoutAug11','MCV2 coverage Aug11 2028','Own Algeria R3 at Aug11 11:31:07, 17s deadline and R4 forecast around 11:45:54 connect two differently signed Aug11 status messages.',[(MD,4,None),(MC,9,None)])]
for args in specs:add(*args)

def msg(key,page,n):
 d=next(d for d in D if d['trajectory_id']=='FC-'+key);m=next(m for m in d['owned_messages'] if m['revision_id']==ref(page,n));return d,m,next(r for r in R if r['trajectory_id']==d['trajectory_id'])
def event(key,page,n,round,target=None,value=None,status='observed',note=None):
 d,m,r=msg(key,page,n);r['events'].append(dict(round=round,target=target,value=value,status=status,note=note or ('Own reported history; not backend verification.' if status=='observed' else 'Forecast or upcoming round; no observed arrival in this span.'),revision_id=m['revision_id'],quote=m['source_excerpt']))
def timing(key,page,n,kind,secs,qual):
 d,m,r=msg(key,page,n);r['timing'].append(dict(kind=kind,seconds=secs,qualifier=qual,revision_id=m['revision_id'],quote=m['source_excerpt']))
def clock(key,page,n,round,raw,kind='due',status='predicted',system='task',owner='self'):
 d,m,r=msg(key,page,n);assert raw in m['source_excerpt'];d['schedule_claims'].append(dict(observation_id=m['observation_id'],owner=owner,clock_system=system,task_date=None,round='R'+str(round),event_kind=kind,raw_value=raw,status=status,excerpt=m['source_excerpt'],supersedes=None))
# Extract explicit round progression and timings without upgrading expected or relayed outcomes.
for key,n in [('ivy-aug12',1),('ivy-sep30',9),('ivy-nov11',13),('ivy-jun23',10),('ivy-feb22',11)]:
 if key!='ivy-nov11':event(key,I,n,1,'Arkansas Northeastern College','2100' if key=='ivy-aug12' else None)
 else:event(key,I,4,1,'Arkansas Northeastern College')
 event(key,I,n,2,'Pitt Community College','2213' if key in ['ivy-aug12','ivy-sep30','ivy-nov11','ivy-feb22'] else None)
 event(key,I,n,3,'Cleveland Community College' if key=='ivy-aug12' else None,'2304' if key=='ivy-aug12' else None,'predicted')
 timing(key,I,n,'followup',20,'Reported Pitt answer window.')
for key,n in [('ivy-aug12',1),('ivy-nov11',4)]:
 timing(key,I,n,'initial',274,'Reported 4m34 initial window.');timing(key,I,n,'cooldown',2236,'Reported 37m16 after deadline.')
event('ivy-sep30',I,2,2,'Pitt Community College',status='predicted')
for key,n,t in [('ivy-sep30',9,'23:10:11'),('ivy-nov11',13,'06:09:21'),('ivy-jun23',10,'21:54:29'),('ivy-feb22',11,'22:27:06'),('ivy-aug12',8,'17:43:16')]:clock(key,I,n,3,t)
for key,page,n,round,t in [('ivy-sep30',I,2,1,'21:50:44'),('ivy-nov11',I,4,1,'04:49:54'),('ivy-nov11',I,13,2,'05:31:44'),('ivy-jun23',I,10,2,'21:16:52'),('ivy-feb22',I,11,2,'21:49:29'),('ivy-aug12',I,8,2,'17:05:39')]:clock(key,page,n,round,t,'prompt_arrival','reported')
for n in [1,2]:event('ivy-aug19',P,4,n,'Arkansas Northeastern College' if n==1 else 'Pitt Community College')
event('ivy-aug19',P,4,3,'Cleveland Community College','2304','predicted');clock('ivy-aug19',P,4,3,'23:32:29')
for key,page in [('slp-mar09','DataUSASpeechPathEthnicityMar09'),('slp-dec05','DataUSASLPSequenceDec05Live')]:
 event(key,page,1,1,'2020 Puerto Rican employed men/women','168;2840');event(key,page,1 if key=='slp-mar09' else 2,2,'2021 Puerto Rican employed men/women','202;3048','predicted')
 timing(key,page,1 if key=='slp-mar09' else 2,'followup',11,'Expected follow-up window, not yet received.')
 clock(key,page,1,2,'04:59:59' if key=='slp-mar09' else '09:55:28')
timing('slp-mar09','DataUSASpeechPathEthnicityMar09',1,'initial',180,'Reported initial 3m window.');timing('slp-mar09','DataUSASpeechPathEthnicityMar09',1,'cooldown',1440,'Announced 24m after initial deadline.')
# Fuel sequence values are not imported from peer Jan01 text.
for key,n,u in [('fuel-may17',2,4),('fuel-dec28',3,5)]:
 for j,target in enumerate(['Belfast','Mid Ulster','Ards and North Down'],1):event(key,F,n,j,target if key=='fuel-dec28' else None,note='Own reported matching prefix; May17 does not spell out authority names in its span.' if key=='fuel-may17' else None)
 event(key,F,n,4,status='predicted');event(key,F,u,4,'Derry City and Strabane','18,290');event(key,F,u,5,status='predicted')
 clock(key,F,u,4,'05:41:47' if key=='fuel-may17' else '07:18:10','prompt_arrival','reported');clock(key,F,u,5,'06:11:52' if key=='fuel-may17' else '07:48:15')
event('fuel-nov30','OpenAIFuelPovertyNov30Live',1,1,'Belfast');event('fuel-nov30','OpenAIFuelPovertyNov30Live',1,2,'Mid Ulster','15,880');event('fuel-nov30','OpenAIFuelPovertyNov30Live',1,3,'Ards and North Down',status='predicted');event('fuel-nov30',F,10,5,'Armagh City, Banbridge and Craigavon','19,000','indirect','Reports an ABC counter signal attributed to May17; not own R5 arrival and counter response is not independently verified.')
for kind,secs,qual in [('initial',383,'Reported 6m23 window.'),('followup',46,'Reported R2 window.'),('cooldown',3906,'Reported 1h5m6 post-deadline cooldown.')]:timing('fuel-nov30','OpenAIFuelPovertyNov30Live',1,kind,secs,qual)
clock('fuel-nov30','OpenAIFuelPovertyNov30Live',1,3,'23:42:45')
# LF: predicted due time is distinct from actual receipt.
event('lf-nov14',LF,2,1,note='Claims same initial LF task as page anchor; year/value not repeated in this owned span.')
event('lf-nov14',LF,2,2,status='scheduled');event('lf-nov14',LF,14,2,'2008',note='Own follow-up explicitly received at 19:35:47; prompt says do the same for 2008.')
timing('lf-nov14',LF,2,'initial',856,'Reported 14m16s initial timer.');timing('lf-nov14',LF,2,'cooldown',6285,'Announced 1h44m45s after deadline.');timing('lf-nov14',LF,14,'followup',79,'Reported actual 1m19s follow-up timer.')
clock('lf-nov14',LF,2,2,'19:35:47');clock('lf-nov14',LF,14,2,'19:35:47','prompt_arrival','reported','scaffold')
event('lf-apr15',LF,3,2,status='predicted');clock('lf-apr15',LF,5,2,'14:42:15',system='scaffold')
# MCV2 research bridge and own country sequence.
for j,(target,value) in enumerate([('Indonesia','75.75'),('Samoa','50.16'),('Algeria','93.96')],1):event('mcv-mar28',MC,1,j,target,value)
event('mcv-mar28',MC,1,4,status='predicted');timing('mcv-mar28',MC,1,'followup',43,'Reported follow-up tier.');timing('mcv-mar28',MC,1,'cooldown',4380,'Approximately 73m, as reported.');clock('mcv-mar28',MC,1,4,'21:07:32')
for j,t in enumerate(['Indonesia','Samoa','Algeria'],1):event('mcv-aug11',MD,4,j,t,'93.96' if j==3 else None)
event('mcv-aug11',MD,4,4,status='predicted');timing('mcv-aug11',MD,4,'followup',17,'Reported R3 17-second deadline.');clock('mcv-aug11',MD,4,3,'11:31:07','prompt_arrival','reported','scaffold');clock('mcv-aug11',MC,9,4,'11:45:54',system='scaffold')
# Source, freshness and existing-trajectory duplication assertions.
old=json.load(open('analysis/trajectory-assembly/new-trajectories.json'))
oldpairs={(m['revision_id'],s) for d in old for m in d['owned_messages'] for s in m['included_excerpts']}
for d in D:
 assert len(set(m['revision_id'] for m in d['owned_messages']))>=2
 for m in d['owned_messages']:
  r=rows[m['revision_id']];s=m['source_excerpt'];
  if (m['revision_id'],s) in oldpairs: print('EXISTING',d['trajectory_id'],m['revision_id'])
  assert r['body'][m['spans'][0]['start_char']:m['spans'][0]['end_char']]==s
  if r['diff_base']:assert s not in rows[r['diff_base']]['body'],m['revision_id']
for filename,obj in [('dossiers.json',D),('rounds.json',R),('decisions.json',decisions)]: (O/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('dossiers',len(D),'messages',sum(len(d['owned_messages']) for d in D),'events',sum(len(r['events']) for r in R))
# Existing Nov14 was historically misclassified by expanding LF as labor force.
nov=next(d for d in D if d['trajectory_id']=='FC-lf-nov14')
(O/'existing-trajectory-corrections.json').write_text(json.dumps([dict(trajectory_id='C556a612bd1ee/1',task_id='ihme-lymphatic-filariasis',task='Lymphatic filariasis Nov14 · 2008 follow-up',reason='LFSequenceCollabMay03@1 explicitly defines LF as lymphatic filariasis; Nov14 @2 claims same initial task, then @14 receives 2008 follow-up. Existing owned spans exactly overlap; reclassify, never duplicate.',anchor=dict(revision_id=ref(LF,1),quote=rows[ref(LF,1)]['body']),existing_owned_messages_preserved=True)],indent=2)+'\n')
D=[d for d in D if d['trajectory_id']!='FC-lf-nov14'];R=[r for r in R if r['trajectory_id']!='FC-lf-nov14']
for filename,obj in [('dossiers.json',D),('rounds.json',R)]: (O/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
families=[('datausa-ivy-tuition','college-state-tuition-2015','College state tuition · 2015',I,1),('datausa-slp-ethnicity','datausa-slp-ethnicity','Speech-language pathologists · Puerto Rican ethnicity','DataUSASpeechPathEthnicityMar09',1),('fuel-poverty-ni','fuel-poverty-ni','Fuel poverty · Northern Ireland',F,1),('gapminder-age80','gapminder-age80','Gapminder · age 80, 2023','GapminderAge80SequenceJun20',1),('ihme-lymphatic-filariasis','ihme-lymphatic-filariasis','Lymphatic filariasis · year sequence',LF,1),('ihme-mcv2','ihme-mcv2','MCV2 coverage · country sequence',MD,1)]
sparse={I:{7:'Nov18 single substantive own-task publication.',15:'Jul08 first-person schedule anchors task, but only later generic status ping at probe @7; that does not independently substantiate a second fresh task contribution.',19:'Mar03 single substantive own-task publication.'},P:{1:'Scratch probe only.',2:'Placeholder and test line only.',6:'No new owned text.'},'DataUSASLPSeqMay05':{1:'hello2 has no own-task content.'},'DataUSASLPSequenceDec05Live':{3:'Jul01 single substantive own-task publication; its 12m cooldown differs from Mar09/Dec05.'},'GapminderAge80SequenceJun20':{1:'Only one fresh task anchor across archive. R1-R4 prefix plus predicted R5 do not supply multiple publication revisions.'},F:{1:'Jan01 has one substantive own-task anchor; later peers cite silence, not a second own report.',11:'Sep23 has one substantive own-task anchor; distinct 23s/18m44 tier.'},LF:{1:'May03 has one substantive own-task anchor; 9m55 and 44m18 differs from Nov14.',15:'New May07 API values are research assistance without an explicit own task/schedule. Nov14 prompt is inherited re-encoding.',16:'May07 later-year cache is not own received prompt history. Nov14 prompt inherited re-encoding.',17:'Sep30 has one substantive own-task anchor. Nov14 prompt inherited re-encoding.',18:'Sep03 has one substantive own-task anchor. Nov14 prompt inherited re-encoding.',19:'Dec10 has one substantive own-task anchor. Nov14 prompt inherited re-encoding.'},MC:{3:'Deletion of duplicated Mar28 text, no fresh substantive publication.',4:'June30 one substantive own-task anchor; different 26m08 cadence.',5:'May02 one substantive own-task anchor.',6:'Feb26 one substantive own-task anchor.',7:'Nov30 one substantive own-task anchor.',8:'Apr19 one substantive own-task anchor.'},MD:{2:'Jun26 explicitly owns construction wages, not MCV2 (R03/R08).'}}
notes=['Searched all 14,591 original ZIP revisions, with no ±24-hour cutoff: family terms, page backlinks, signatures, alias variants, distinctive clocks, and editor labels; inspected changed hunks against complete diff-base bodies.','Search outputs in search-hits.json and candidate-hunks.txt. Additional editor-only retrieval found unrelated construction, clothing, French language, maids, sector, and transport own-task claims; rejected under R01/R03/R08.','Retained signed cross-family outreach only when a concrete task backlink or exact schedule connects the established exchange. Probe/formatting/encoding-restoration edits and same-page repeated text are not independent evidence.','All selected spans have exact original latin1 bytes/sha256, character offsets, archive revisions.jsonl line and diff_base. Existing assembly message-pair overlap found Nov14 LF only; reclassification recorded separately.','Expanded LF scratch retrieval found AgentHealthLFData202606021332@1/@2 config/location API pages only; these are source assistance without an explicit own-task/schedule bridge.']
coverage=[]
for family,task,title,page,n in families:
 count=sum(d['task_id']==task for d in D)+(family=='ihme-lymphatic-filariasis')
 reason=f'{count} supported histories after conservative fresh-span assembly'+(' (includes corrected existing Nov14 history).' if family=='ihme-lymphatic-filariasis' else '.') if count else 'One explicit fresh own-task anchor; no second substantive own contribution across distinct revisions. Retain visible audited coverage without inventing an account.'
 coverage.append(dict(family_id=family,task_id=task,title=title,status='supported' if count else 'insufficient_evidence',reason=reason,anchors=[dict(revision_id=ref(page,n),quote=rows[ref(page,n)]['body'])],search_notes=notes,sparse_candidates=[dict(revision_id=ref(pg,k),reason=v) for pg,ns in sparse.items() for k,v in ns.items() if pg in ({I,P} if page==I else {page,'DataUSASLPSeqMay05','DataUSASLPSequenceDec05Live'} if family=='datausa-slp-ethnicity' else {F,'OpenAIFuelPovertyNov30Live'} if family=='fuel-poverty-ni' else {LF} if page==LF else {MD,MC} if page==MD else {page})]))
(O/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
# Every changed hunk on the audited family pages, plus retrieved cross-page candidates,
# receives an explicit disposition. Partial owned selections remain separate above.
sel={m['revision_id']:[x for x in d['owned_messages'] if x['revision_id']==m['revision_id']] for d in D for m in d['owned_messages']}
oldids={m['revision_id'] for m in nov['owned_messages']}
hits=json.load(open(O/'search-hits.json'));hitids={h['revision_id'] for h in hits}
family_pages={json.loads(x)['page_id'] for x in open('task-replicas/remaining/family-map.jsonl') if json.loads(x)['publisher_family'] in {f[0] for f in families}}
ledger=[]
for r in rr:
 if r['rev_id'] not in hitids and r['page_id'] not in family_pages and r['name'] not in [P,'AgentHealthLFData202606021332']:continue
 s='\n'.join(''.join(r['body'].splitlines(True)[h['b0']:h['b1']]) for h in r['hunks'] if h['op']!='delete').strip()
 if r['rev_id'] in sel: decision='include';reason='Retain only exact owned spans; any remainder of changed hunk is inherited, re-encoded, duplicated or other-speaker context.';owned=[x['source_excerpt'] for x in sel[r['rev_id']]]
 elif r['rev_id'] in oldids:decision='existing_trajectory';reason='Already owned by C556a612bd1ee/1; correct family to lymphatic filariasis, do not duplicate.';owned=[]
 elif r['seq'] in sparse.get(r['name'],{}):decision='unresolved';reason=sparse[r['name']][r['seq']];owned=[]
 elif r['name']==I and r['seq'] in [3,5]:decision='exclude';reason='Exact Sep30 paragraph already present earlier on the same page; duplicate text is not a fresh independent contribution (R05/R07).';owned=[]
 elif r['name']==P and r['seq']==7:decision='unresolved';reason='Jul08 generic R3 status ping has no new own round/timing/result; insufficient second substantive contribution.';owned=[]
 else:decision='exclude';reason='No defensible own-task bridge for these audited histories: static API/indexing text, scratch probes, inherited restoration, peer mention, or explicit unrelated own task. Page destination/editor does not authenticate ownership (R01/R03/R05/R08).';owned=[]
 ledger.append(dict(revision_id=r['rev_id'],archive_jsonl_line=nums[r['rev_id']],diff_base=r['diff_base'],decision=decision,included_excerpts=owned,candidate_excerpt=s,candidate_sha256=hashlib.sha256(s.encode('latin1')).hexdigest(),reason=reason,rule_ids=['R02','R03','R05','R06','R08','R14']))
(O/'candidate-decisions.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print('FINAL new dossiers',len(D),'owned',sum(len(d['owned_messages']) for d in D),'candidate decisions',len(ledger))
# Independent review corrections: do not promote bare confirmation to arrival;
# retain approximation and the actual clock alignment landmarks used in links.
for d in D:
 for c in d['schedule_claims']:
  if d['trajectory_id'] in ['FC-ivy-nov11','FC-ivy-feb22'] and c['round']=='R2' and c['event_kind']=='prompt_arrival':
   c['event_kind']='other';c['event_description']='Reported round confirmation timestamp; prompt-arrival versus answer time unspecified.'
  if (d['trajectory_id'],c['raw_value']) in [('FC-ivy-nov11','06:09:21'),('FC-mcv-aug11','11:45:54')]:c['raw_value']='~'+c['raw_value']
for key,page,n,raw,system in [('ivy-aug12',I,14,'17:37:06','task'),('ivy-aug12',I,14,'20:14:24','container'),('ivy-sep30',I,17,'22:53:11','task'),('ivy-sep30',I,17,'20:46:14','container'),('ivy-jun23',I,18,'21:41:35','task'),('ivy-feb22',P,5,'22:24:34','task'),('lf-apr15',LF,5,'14:06:25','scaffold'),('lf-apr15',LF,7,'14:09:10','scaffold')]:
 d,m,r=msg(key,page,n);assert raw in m['source_excerpt'];d['schedule_claims'].append(dict(observation_id=m['observation_id'],owner='self',clock_system=system,task_date=None,round=None,event_kind='current_time',raw_value=raw,status='reported',excerpt=m['source_excerpt'],supersedes=None))
(O/'dossiers.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
(O/'decisions.json').write_text(json.dumps([m for d in D for m in d['owned_messages']],ensure_ascii=False,indent=2)+'\n')
cor=json.load(open(O/'existing-trajectory-corrections.json'));cor[0]['rounds_review']='Existing audited-rounds extraction is accurate: R1 unspecified target, R2 scheduled then observed 2008; timers 856s/6285s/79s. No round or timing change needed; only task classification/descriptor correction.'
(O/'existing-trajectory-corrections.json').write_text(json.dumps(cor,ensure_ascii=False,indent=2)+'\n')
