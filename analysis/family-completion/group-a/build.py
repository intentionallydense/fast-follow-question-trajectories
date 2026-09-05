import json,zipfile,hashlib,re
from pathlib import Path
O=Path(__file__).parent
rs=[json.loads(x) for x in zipfile.ZipFile('full-wiki-logs.zip').read('revisions.jsonl').splitlines()]; by={r['rev_id']:r for r in rs}; ln={r['rev_id']:i for i,r in enumerate(rs,1)}
def record(rid,text,signature,reason,decision='include',depends=[]):
 r=by[rid]; start=r['body'].index(text)
 return dict(observation_id='FC-A-'+rid,revision_id=rid,decision=decision,trajectory_local_id=None,included_excerpts=[text],reason=reason,rule_ids=['R02','R04','R05','R06','R08','R10'],depends_on=depends,cross_post_of=None,source_line=ln[rid],body_line=r['body'][:start].count('\n')+1,page_id=r['page_id'],utc=r['time'],editor=r['label'],signature=signature,diff_base=r['diff_base'],source_excerpt=text,spans=[dict(text=text,start_char=start,end_char=start+len(text),source_char_positions=[start],length=len(text),text_sha256=hashlib.sha256(text.encode('latin1')).hexdigest(),location_uncertainty=None)])
def claim(m,round,event,raw,status,clock='unspecified',owner='self'):
 return dict(observation_id=m['observation_id'],owner=owner,clock_system=clock,task_date=None,round='R'+str(round),event_kind=event,raw_value=raw,status=status,excerpt=m['spans'][0]['text'],supersedes=None)
def dossier(tid,taskid,task,sig,messages,claims,uncertainties):
 for m in messages:m['trajectory_local_id']=tid
 return dict(local_id=tid,trajectory_id=tid,task_id=taskid,task=task,self_name=sig,signature=sig,batch='family-completion',status='pending_independent_review',anchor_observation_ids=[m['observation_id'] for m in messages],schedule_claims=claims,membership_rationale='Fresh signed own-task anchor and explicit same-cohort continuation with matching round schedule; all archive revisions searched for task, page, signature and schedule continuations.',uncertainties=uncertainties,owned_messages=messages,associated_messages=[],unassigned=[],excluded=[],candidate_follow_up_leads=[],owned_publication_count=len(messages))
rid='dse~OpenAIClimateSequence729@1'; m1=record(rid,by[rid]['body'].strip(),'OpenAIClimateOct01','Own climate sequence and Oct01 schedule anchor. R3 is still described as due; R4 older-cohort forecast and R5 pattern forecast are not observations.')
m2=record('dse~OpenAIClimateSequence729@2','CONFIRMED Oct01 at 17:28:28. Q4 due 17:52:39.','OpenAIClimateOct01','Only the fresh confirmation and next due-time replace the earlier forecast. Same Oct01 R3 clock and signed paragraph establish continuation; surrounding inherited values excluded.',depends=[m1['observation_id']])
t1=dossier('FC-alaska-climate-oct01','alaska-climate','Alaska climate monthly temperature records','OpenAIClimateOct01',[m1,m2],[claim(m1,3,'due','17:28:28','predicted','task'),claim(m2,3,'prompt_arrival','17:28:28','reported','task'),claim(m2,4,'due','17:52:39','predicted','task')],['R3 first anchor says due despite introductory Confirmed; only the later explicit confirmation is treated as observed.','R4 source attributes target forecast to older cohort; R5 is conditional. No observed R4/R5 or termination evidence.'])
p='dse~DataAfricaRainfedMozambiqueCoordOAI@'; a=next(l for l in by[p+'5']['body'].splitlines() if l.startswith('Parallel cohort Jul03'));b=next(l for l in by[p+'6']['body'].splitlines() if l.startswith('Jul03 cohort update'))
n1=record(p+'5',a,'OpenAIDataAfricaJul03','Fresh Jul03 own R3 report on explicitly rainfed Mozambique page. Other cohorts and inherited setup excluded.')
n2=record(p+'6',b,'OpenAIDataAfricaJul03','Fresh explicit Jul03 update confirms R4 at previously predicted Jul04 00:41:27, with matching 69s/45m49 tier despite editor label change.',depends=[n1['observation_id']])
t2=dossier('FC-dataafrica-rainfed-jul03','dataafrica-rainfed-crops','Data Africa Mozambique rainfed crops','OpenAIDataAfricaJul03',[n1,n2],[claim(n1,3,'prompt_arrival','23:54:29','reported'),claim(n1,3,'deadline','23:55:38','reported'),claim(n1,4,'due','00:41:27 Jul04','predicted'),claim(n2,4,'prompt_arrival','00:41:27 Jul04','reported'),claim(n2,5,'due','01:28:26','predicted')],['Source calls clock real; clock system remains unspecified, not silently archive UTC.','Tete is expected, not an observed R5. No endpoint authenticated.'])
ds=[t1,t2]
def ev(m,n,target,value,status,note):return dict(round=n,target=target,value=value,status=status,note=note,revision_id=m['revision_id'],quote=m['spans'][0]['text'])
rounds=[dict(trajectory_id=t1['trajectory_id'],events=[ev(m1,1,'Yakutat, June 1965','44.3 F','observed','Reported own round.'),ev(m1,2,'Valdez, October 2002','42.6 F','observed','Reported own round.'),ev(m1,3,'Talkeetna, September 1992','37.3 F','predicted','Due in first report; later confirmed.'),ev(m1,4,'St. Paul Island, August 2016','52.9 F','predicted','Explicit older-cohort prediction, not own arrival.'),ev(m1,5,'Nome, July 1922','44.9 F','predicted','Conditional pattern forecast.'),ev(m2,3,None,None,'observed','Fresh R3 confirmation; target/value retained in previous anchor.'),ev(m2,4,None,None,'predicted','Fresh next-round due time only.')]),dict(trajectory_id=t2['trajectory_id'],events=[ev(n1,3,'Nampula',None,'observed','Own R3 confirmed.'),ev(n1,4,None,None,'predicted','R4 due.'),ev(n2,4,'Zambezia',None,'observed','Own R4 confirmed and answered.'),ev(n2,5,'Tete',None,'predicted','Strongly expected, not observed.')])]
families=[('aihw-pbs','aihw-pbs','AIHW PBS government cost','insufficient_evidence',['dse~AIHWPBSSequenceCollab@1'],'One Mar14 own-task anchor. Other AIHW archive pages contain unsigned URL/filter/proxy scratch material without a task/schedule bridge; ResearchHelperY peer mention on poverty page is not own AIHW continuation.'),('alaska-climate','alaska-climate','Alaska climate records','supported',['dse~OpenAIClimateSequence729@1','dse~OpenAIClimateSequence729@2','dse~OpenAIClimateSequence729@3'],'Oct01 supported by fresh R3 confirmation. Jun12 cohort kept separate: only one substantive publication.'),('dataafrica-health-stunting','mozambique-stunting','Mozambique moderate stunting','insufficient_evidence',['dse~DataAfricaHealthMozambiqueYearsApr15OAI@1'],'Only Apr15 own-task publication. Similar climate timer tier and link are peer context, not identity.'),('dataafrica-rainfed-crops','dataafrica-rainfed-crops','Mozambique rainfed crops','supported',[p+'1',p+'2',p+'5',p+'6',p+'7'],'Jul03 supported by R3 and R4 progression. Nov27 single anchor; Aug13 restored paragraph at @4 duplicates @2 and cannot count again; endpoint scout discloses no active own thread.'),('datausa-cashier-skills','datausa-cashier-skills','Cashiers skill RCA','insufficient_evidence',['dse~DataUSACashierSkillsRCAJan02Live@1','dse~DataUSACashierSkillsRCAJan02Live@2','dse~URGENTDataUSACashierSkillsR5Feb22@1'],'Jan02 single anchor. Feb22 anchor plus outreach repeats the same unknown R5 and due time; approximate three-minute urgency does not establish a second substantive task contribution under R07. Different cooldowns block merging Jan02 and Feb22.'),('datausa-elpaso-foreign-born','el-paso-foreign-born','El Paso foreign-born population','insufficient_evidence',['dse~DataUSAElPasoForeignBornJul23OAI@1','dse~ElPasoForeignBornSequenceDec7OAI@1'],'Jul23 and Dec7 each have one publication, different dates/cooldowns. Unsigned July10 API scratch page has no task schedule or speaker bridge.')]
coverage=[]
for fid,tid,title,status,rids,reason in families:
 coverage.append(dict(family_id=fid,task_id=tid,title=title,status=status,reason=reason,anchors=[dict(revision_id=r,quote=by[r]['body'].strip()) for r in rids],search_notes=['Searched all '+str(len(rs))+' archive revisions; broad task terms plus all anchor signatures, distinctive page names, YOURLS tags and task target sequence terms. Freshness compared with diff_base and earlier page text.','Retrieval evidence in hits.json and expanded-search.txt; detailed span decisions in decisions.json.','Existing assembly dossier signatures and all source text searched; neither accepted history duplicates existing dossiers.']))
(O/'dossiers.json').write_text(json.dumps(ds,indent=2)+'\n');(O/'rounds.json').write_text(json.dumps(rounds,indent=2)+'\n');(O/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
# Every retrieved fresh matched line gets a reviewable source-exact classification.
decisions=[]
rx=re.compile(r'aihw|pharmaceutical benefits|\bPBS\b|alaska|akclimate|climatesequence|oaiclim|stunt|rainfed|OpenAIDataAfrica|cashier.{0,40}skill|skill.{0,40}cashier|RCAResearcherJan02|el.?paso.{0,50}foreign|foreign.{0,50}el.?paso|OpenAIElPaso',re.I)
for r in rs:
 base=by.get(r['diff_base'],{}).get('body','')
 for line in r['body'].splitlines():
  if not rx.search(line) or line in base:continue
  own=[m for t in ds for m in t['owned_messages'] if m['revision_id']==r['rev_id'] and m['spans'][0]['text'] in line]
  reason='Task-family retrieval only: no independent supported continuity; scratch URLs, third-party context and singleton anchors cannot establish an owned multi-publication history.';decision='unresolved'
  if own:decision='include';reason=own[0]['reason']
  if r['rev_id']==p+'4':decision='exclude';reason='Exact Aug13 paragraph already published @2, deleted @3 and restored @4; restoration is not fresh.'
  if 'Alaska:' in line or 'S61x62-02-Alaska' in line:decision='exclude';reason='Alaska state workforce values/API, not climate own task.'
  if r['rev_id']=='dse~OpenAIClimateSequence729@2':decision='include';reason=m2['reason']
  z=record(r['rev_id'],line,r['label'],reason,decision);z['included_excerpts']=[m2['spans'][0]['text']] if r['rev_id']==m2['revision_id'] else ([line] if decision=='include' else []);decisions.append(z)
(O/'decisions.json').write_text(json.dumps(decisions,indent=2)+'\n')
print(len(ds),'dossiers',sum(len(t['owned_messages']) for t in ds),'messages',len(decisions),'retrieval decisions')
# Root independent-review corrections: preserve unspecified event subtype and peer ownership.
for t in ds:
 for c in t['schedule_claims']:
  if c['event_kind']=='prompt_arrival':
   c['event_kind']='other'; c['event_subtype']='round confirmation; arrival versus answer unspecified'
rounds[0]['events'][3]['status']='indirect'
def timing(m,kind,seconds,qualifier):return dict(kind=kind,seconds=seconds,qualifier=qualifier,revision_id=m['revision_id'],quote=m['spans'][0]['text'])
rounds[0]['timing']=[timing(m1,'initial',180,'Reported R1 timer.'),timing(m1,'followup',11,'Reported R2 and R3 timers.')]
rounds[1]['timing']=[timing(n1,'followup',69,'Reported R3 timer.'),timing(n1,'cooldown',2749,'Reported 45m49 cooldown.'),timing(n2,'followup',69,'Reported R4 timer.'),timing(n2,'cooldown',2749,'Repeated 45m49 cooldown.')]
for c in coverage:
 for a in c['anchors']:
  rid=a['revision_id']
  own=next((m for t in ds for m in t['owned_messages'] if m['revision_id']==rid),None)
  if own:a['quote']=own['spans'][0]['text'];continue
  if rid==p+'2':a['quote']=next(l for l in by[rid]['body'].splitlines() if l.startswith('Parallel cohort Aug13'))
  elif rid==p+'7':a['quote']=next(l for l in by[rid]['body'].splitlines() if l.startswith('Endpoint/value request'))
  elif rid=='dse~OpenAIClimateSequence729@3':a['quote']=next(l for l in by[rid]['body'].splitlines() if l.startswith('Jun12 cohort update'))
  elif rid=='dse~DataUSACashierSkillsRCAJan02Live@2':a['quote']=next(l for l in by[rid]['body'].splitlines() if l.startswith('MATCHING COHORT'))
for name,arr in [('dossiers',ds),('rounds',rounds),('coverage',coverage)]: (O/(name+'.json')).write_text(json.dumps(arr,indent=2)+'\n')
