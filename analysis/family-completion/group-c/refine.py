import json,re
from pathlib import Path
P=Path(__file__).parent
ds=json.load(open(P/'dossiers.json'));rr={r['trajectory_id']:r['events'] for r in json.load(open(P/'rounds.json'))}
# Exact event-time phrases manually selected from reviewed owned spans.
C={
'OpenAIResearchMar23Smoking':[(1,'prompt_arrival','22:34:01','reported',0),(1,'deadline','22:39:12','reported',0),(2,'due','23:45:45','predicted',0)],
'OpenAIResearchMar16Smoking':[(1,'prompt_arrival','20:51:43','reported',0),(1,'deadline','20:59:28','reported',0),(2,'due','22:06:01','predicted',0),(2,'prompt_arrival','22:03:32','reported',1),(2,'deadline','22:04:28','reported',1)],
'OpenAIDec16Smoking':[(1,'prompt_arrival','21:42:34','reported',0),(1,'deadline','21:50:19','reported',0),(1,'answer','21:49:56','reported',0),(2,'due','22:56:52','predicted',1),(2,'prompt_arrival','22:54:23','reported',2),(2,'deadline','22:55:19','reported',2)],
'VeteranHelperJul03':[(4,'prompt_arrival','20:54:22','reported',1),(5,'due','21:13:07','predicted',1)],
'Dec30VeteranAgent':[(2,'prompt_arrival','06:10:38','reported',0),(3,'due','06:29:22','predicted',0),(5,'due','07:06:52','predicted',1)],
'VeteranWatcherNov25':[(2,'prompt_arrival','09:34:08','reported',0),(3,'prompt_arrival','09:52:52','reported',1),(4,'prompt_arrival','10:11:37','reported',2),(5,'due','10:30:22','predicted',2)],
'VeteranObserverFeb11':[(1,'prompt_arrival','20:12:50','reported',0),(1,'deadline','20:17:21','reported',0),(2,'prompt_arrival','20:42:11','reported',1),(3,'prompt_arrival','21:07:15','reported',2),(4,'prompt_arrival','21:32:20','reported',3),(5,'due','21:57:25','predicted',3),(None,'current_time','21:38:30','reported',4)],
'VeteranScoutFeb11C':[(1,'prompt_arrival','22:21:00','reported',0),(2,'prompt_arrival','22:42:28','reported',0),(3,'prompt_arrival','23:01:12','reported',1),(4,'due','23:19:57','predicted',1)],
'Oct27VeteranAgent':[(1,'prompt_arrival','06:38:16','reported',0),(1,'deadline','06:42:47','reported',0),(2,'prompt_arrival','07:07:37','reported',1),(3,'prompt_arrival','07:32:41','reported',3),(4,'prompt_arrival','07:57:46','reported',4),(5,'due','08:22:51','predicted',4)],
'Feb22VeteranAgent':[(2,'prompt_arrival','21:47:37','reported',0),(3,'prompt_arrival','22:06:21','reported',1),(4,'prompt_arrival','22:25:06','reported',2),(5,'due','22:43:51','predicted',2)],
'Aug07VeteranResearcher':[(2,'prompt_arrival','06:45:06','reported',0),(3,'prompt_arrival','07:03:50','reported',1),(4,'prompt_arrival','07:22:35','reported',2),(5,'due','07:41:20','predicted',2)],
'Oct27VeteranWatcherB':[(2,'prompt_arrival','08:34:46','reported',0),(3,'prompt_arrival','08:59:50','reported',1),(4,'prompt_arrival','09:24:55','reported',2),(5,'due','09:50:00','predicted',2)],
'May08VeteranAgent':[(2,'prompt_arrival','10:08:51','reported',0),(3,'prompt_arrival','10:27:17','reported',0),(4,'due','10:45:43','predicted',0),(4,'prompt_arrival','10:45:44','reported',1),(5,'due','11:04:10','predicted',1)],
'Feb20VeteranAgent':[(4,'prompt_arrival','21:02:22','reported',0),(5,'due','21:21:07','predicted',0),(None,'current_time','21:16:24','reported',1)],
'OAIHouseholdNov02Scout':[(1,'prompt_arrival','10:24:13','reported',0),(1,'deadline','10:40:51','reported',0),(2,'prompt_arrival','12:45:02','reported',0),(3,'prompt_arrival','14:50:13','reported',0),(4,'prompt_arrival','16:55:24','reported',0),(5,'prompt_arrival','19:00:35','reported',0),(6,'due','21:05:45/46','reported',0)]}
for d in ds:
 # Groups' original reference order is source order except OECD outreach, which precedes countdown update.
 msgs=d['owned_messages'];d['schedule_claims']=[]
 for rnd,kind,value,status,i in C[d['signature']]:
  m=msgs[i];q=m['spans'][0]['text'];assert value in q,(d['signature'],value)
  clock='scaffold' if d['signature'] in ['Dec30VeteranAgent','Oct27VeteranAgent','May08VeteranAgent'] else 'task' if d['signature'] in ['OpenAIResearchMar23Smoking','OpenAIResearchMar16Smoking','OpenAIDec16Smoking','VeteranHelperJul03','VeteranObserverFeb11','VeteranScoutFeb11C','Feb22VeteranAgent','OAIHouseholdNov02Scout'] else 'unspecified'
  d['schedule_claims'].append(dict(observation_id=m['observation_id'],owner='self',clock_system=clock,task_date=None,round='R'+str(rnd) if rnd else None,event_kind=kind,raw_value=value,status=status,excerpt=q,supersedes=None))
 d['uncertainties']+=['Minute/second alternatives and timing forecasts remain literal claims; no fixed archive-to-task clock offset is assumed.']
json.dump(ds,open(P/'dossiers.json','w'),indent=2)
print('typed claims',sum(len(d['schedule_claims']) for d in ds))
T={'OpenAIResearchMar23Smoking':[('initial',311,0),('cooldown',3993,0)],'OpenAIResearchMar16Smoking':[('initial',465,0),('followup',56,1),('cooldown',3844,1)],'OpenAIDec16Smoking':[('initial',465,0),('followup',56,2),('cooldown',3844,2)],'VeteranHelperJul03':[('initial',185,0),('followup',21,0),('cadence',1124,0)],'Dec30VeteranAgent':[('followup',21,0)],'VeteranWatcherNov25':[('followup',21,1)],'VeteranObserverFeb11':[('initial',271,0),('followup',14,1),('cooldown',1490,1),('cadence',1504,1)],'VeteranScoutFeb11C':[('followup',21,1)],'Oct27VeteranAgent':[('initial',271,0),('followup',14,1),('cooldown',1490,1),('cadence',1504,1)],'Feb22VeteranAgent':[('initial',185,0),('followup',21,0),('cadence',1124,0)],'Aug07VeteranResearcher':[('followup',21,0)],'Oct27VeteranWatcherB':[('followup',14,0)],'May08VeteranAgent':[('initial',485,0),('followup',32,0),('cadence',1106,0),('cooldown',1074,0)],'Feb20VeteranAgent':[('followup',21,0)],'OAIHouseholdNov02Scout':[('initial',998,0),('followup',59,0),('cooldown',7451,0)]}
rounds=json.load(open(P/'rounds.json'))
for d,r in zip(ds,rounds):
 r['timing']=[]
 for kind,seconds,i in T[d['signature']]:
  m=d['owned_messages'][i];r['timing'].append(dict(kind=kind,seconds=seconds,qualifier='Source-reported '+kind+' interval; does not authenticate other cohorts or termination.',revision_id=m['revision_id'],quote=m['spans'][0]['text']))
json.dump(rounds,open(P/'rounds.json','w'),indent=2)
# Initial timer/activation mentions do not explicitly name that cohort's initial target.
for r in rounds:
 if r['trajectory_id'].endswith(('May08VeteranAgent','VeteranScoutFeb11C')):
  for e in r['events']:
   if e['round']==1:e['target']=None;e['note']='Initial timing is reported; initial target is not explicitly named in this own contribution.'
json.dump(rounds,open(P/'rounds.json','w'),indent=2)
# Independent semantic review: retain explicit submitted answers, including the R1 typo.
vals={
'VeteranHelperJul03':{1:'10,157',2:'17,931',3:'46,438',4:'14,751'},
'Dec30VeteranAgent':{2:'17,931'},'VeteranWatcherNov25':{2:'17,931',3:'46,438',4:'14,751'},
'VeteranObserverFeb11':{1:'10,147',2:'17,931',3:'46,438',4:'14,751'},
'VeteranScoutFeb11C':{2:'17,931',3:'46,438'},'Oct27VeteranAgent':{2:'17,931',3:'46,438',4:'14,751'},
'Feb22VeteranAgent':{2:'17,931',3:'46,438',4:'14,751'},'Aug07VeteranResearcher':{3:'46,438',4:'14,751'},
'Oct27VeteranWatcherB':{2:'17,931',3:'46,438',4:'14,751'},'Feb20VeteranAgent':{4:'14,751'},
'OpenAIDec16Smoking':{1:'18.1%',2:'25.52%'}}
for r in rounds:
 sig=next(d['signature'] for d in ds if d['trajectory_id']==r['trajectory_id'])
 for e in r['events']:
  if e['status']=='observed' and e['round'] in vals.get(sig,{}):
   e['value']=vals[sig][e['round']]
   e['note']='Explicit value in own reported round; source does not independently establish grading.'
   if sig=='VeteranHelperJul03' and e['round']<4:e['note']='Confirmed sequence and source values reported together; post does not explicitly state these were submitted answers.'
   if sig=='VeteranObserverFeb11' and e['round']==1:e['note']='Own submitted typo 10,147, preserved as reported; do not replace with the expected WWII answer 10,157.'
  if sig=='OpenAIResearchMar23Smoking' and e['round']==2:e['status']='scheduled';e['note']='Own source explicitly says the system announced R2 after the deadline; no R2 receipt observed.'
  if sig=='Dec30VeteranAgent' and e['round']==4:e['target']=None;e['note']='Own R4 is confirmed, but target and submitted value are not explicitly named in this contribution.'
 # R5 predicted cached values remain estimates rather than promoted submitted answers.
 for e in r['events']:
  if e['status']=='predicted' and e['round']==5 and '25,276' in e['quote'] and 'Gulf' in str(e['target']):
   e['value']='25,276';e['note']='Expected next service-period target and prepared value; no prompt receipt or submitted answer is established.'
json.dump(rounds,open(P/'rounds.json','w'),indent=2)
# R09: a round confirmation timestamp does not establish that it is a prompt-arrival timestamp.
ambiguous={'VeteranHelperJul03':[4],'Dec30VeteranAgent':[2],'VeteranWatcherNov25':[2],'VeteranObserverFeb11':[4],'VeteranScoutFeb11C':[2],'Feb22VeteranAgent':[2],'Aug07VeteranResearcher':[2],'Oct27VeteranWatcherB':[2,3,4],'May08VeteranAgent':[2,3,4],'Feb20VeteranAgent':[4]}
for d in ds:
 for c in d['schedule_claims']:
  if c['event_kind']=='prompt_arrival' and c['round'] in ['R'+str(n) for n in ambiguous.get(d['signature'],[])]:
   c['event_kind']='other';c['event_description']='Own round confirmation timestamp; source does not explicitly identify prompt arrival versus answer/confirmation time.'
  if d['signature']=='VeteranHelperJul03' and c['raw_value']=='21:13:07':c['raw_value']='~21:13:07'
  if d['signature']=='VeteranScoutFeb11C' and c['raw_value']=='23:19:57':c['raw_value']='23:19:57 (watch :56 too)'
  if d['signature']=='Oct27VeteranAgent' and c['raw_value']=='08:22:51':c['raw_value']='08:22:51 (watch :50)'
  assert c['raw_value'] in c['excerpt']
json.dump(ds,open(P/'dossiers.json','w'),indent=2)
# Preserve explicit later-round hypotheses, including hypotheses challenged by chart-filter evidence.
for r in rounds:
 d=next(d for d in ds if d['trajectory_id']==r['trajectory_id'])
 if d['signature']=='Dec30VeteranAgent':
  m=d['owned_messages'][0]
  r['events'].append(dict(round=3,target='Vietnam',value=None,status='predicted',note='Next Vietnam round is due in the own R2 report; receipt is not established here.',revision_id=m['revision_id'],quote=m['spans'][0]['text']))
  for m in d['owned_messages']:
   r['events'].append(dict(round=6,target='Other',value='41,961',status='predicted',note='Conditional possible R6 from the raw API category; chart-filter evidence elsewhere challenges this hypothesis. Neither R6 receipt nor termination is observed.',revision_id=m['revision_id'],quote=m['spans'][0]['text']))
 if d['signature']=='Feb22VeteranAgent':
  m=d['owned_messages'][0]
  r['events'].append(dict(round=6,target='Other',value='41,961',status='predicted',note='Question posed to peers about possible R6 versus termination; retains an unresolved hypothesis, not an observed round.',revision_id=m['revision_id'],quote=m['spans'][0]['text']))
json.dump(rounds,open(P/'rounds.json','w'),indent=2)
for r in rounds:
 seen=set();unique=[]
 for e in r['events']:
  key=(e['round'],e['target'],e['status'],e['revision_id'],e['quote'])
  if key not in seen:unique.append(e);seen.add(key)
 r['events']=unique
json.dump(rounds,open(P/'rounds.json','w'),indent=2)
