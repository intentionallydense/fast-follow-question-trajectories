import json,zipfile,re,hashlib
from pathlib import Path
P=Path(__file__).parent
rs=[json.loads(x) for x in zipfile.ZipFile('full-wiki-logs.zip').read('revisions.jsonl').splitlines()];by={r['rev_id']:r for r in rs}; nums={r['rev_id']:i for i,r in enumerate(rs,1)}
tasks={t['id']:t for t in json.load(open('trajectory-explorer/app/tasks/reconstruction.json'))['tasks']}
def rev(p,n):return 'dse~'+p+'@'+str(n)
S='HealthdataSmokingSequenceCollab';V='NYCVeteransSequenceCollabJul03';B=V+'B';H='OECDHouseholdDisposableIncomeSequenceNov02'
groups=[('ihme-smoking','OpenAIResearchMar23Smoking',[(S,1),(S,5)]),('ihme-smoking','OpenAIResearchMar16Smoking',[(S,2),(S,8)]),('ihme-smoking','OpenAIDec16Smoking',[(S,4),(S,6),(S,7)]),('nyc-veterans','VeteranHelperJul03',[(V,1),(V,2),(V,5)]),('nyc-veterans','Dec30VeteranAgent',[(V,8),(B,2)]),('nyc-veterans','VeteranWatcherNov25',[(V,9),(V,20),(V,32)]),('nyc-veterans','VeteranObserverFeb11',[(V,11),(V,15),(V,29),(V,35),('Feb20VeteranAgent',2)]),('nyc-veterans','VeteranScoutFeb11C',[(V,12),(V,21)]),('nyc-veterans','Oct27VeteranAgent',[(V,13),(V,16),(V,18),(V,28),(V,30)]),('nyc-veterans','Feb22VeteranAgent',[(V,14),(V,24),(V,38)]),('nyc-veterans','Aug07VeteranResearcher',[(V,17),(V,22),(V,33)]),('nyc-veterans','Oct27VeteranWatcherB',[(V,19),(V,27),(V,31)]),('nyc-veterans','May08VeteranAgent',[(V,26),(B,1)]),('nyc-veterans','Feb20VeteranAgent',[('Feb20VeteranAgent',1),('Feb20VeteranAgent',3)]),('oecd-household-income','OAIHouseholdNov02Scout',[(H,1),(H,11),('OECDEducationEquitySequence',43)])]
def exact(p,n,sig):
 r=by[rev(p,n)]; b=by.get(r['diff_base'],{}).get('body','')
 if (p,n) in [(S,1),(H,1)]:return r['body']
 if (p,n)==(V,5):return next(l for l in r['body'].splitlines() if '--VH' in l)
 hits=[l for l in r['body'].splitlines() if sig in l and l not in b]
 return r['body'][r['body'].index(hits[0]):r['body'].index(hits[-1])+len(hits[-1])]
def message(p,n,sig,tid,decision='include',reason=None,text=None):
 r=by[rev(p,n)]; text=exact(p,n,sig) if text is None else text; start=r['body'].index(text);oid=tid+':'+r['rev_id'];anchor=tid+':'+rev(*next(g[2][0] for g in groups if g[1]==sig))
 return dict(observation_id=oid,revision_id=r['rev_id'],decision=decision,trajectory_local_id=tid,included_excerpts=[text] if decision=='include' else [],reason=reason or f'Fresh signed {sig} contribution; own cohort task and round progression continue the anchored schedule. Compared literal span with diff base and earlier page history.',rule_ids=['R02','R04','R05','R08','R10'],depends_on=[] if oid==anchor else [anchor],cross_post_of=None,source_line=nums[r['rev_id']],body_line=r['body'][:start].count('\n')+1,page_id=r['page_id'],utc=r['time'],editor=r['label'],signature=sig,diff_base=r['diff_base'],spans=[dict(text=text,start_char=start,end_char=start+len(text),source_char_positions=[start],length=len(text),text_sha256=hashlib.sha256(text.encode('latin1')).hexdigest(),location_uncertainty=None)] if decision=='include' else [],source_excerpt=text)
out=[];rounds=[]
for fam,sig,refs in groups:
 tid='FC-'+fam+'-'+sig
 msgs=[message(p,n,sig,tid) for p,n in refs]
 t=dict(local_id=tid,trajectory_id=tid,task_id=fam,task=tasks[fam]['title'],self_name=sig,signature=sig,batch='family-completion',status='pending_independent_review',anchor_observation_ids=[msgs[0]['observation_id']],schedule_claims=[],membership_rationale='Explicit own-task anchor followed by substantive signed continuation with matching cohort and schedule landmarks; editor labels are not identity evidence.',uncertainties=['Posts report task observations; backend identity, grading and actual termination are not verified.'],owned_messages=sorted(msgs,key=lambda x:x['utc']),associated_messages=[],unassigned=[],excluded=[],candidate_follow_up_leads=[],owned_publication_count=len(msgs));out.append(t)
 # Carefully select source-stated round events only. Values remain absent unless stated as submitted.
 events=[]
 def ev(p,n,rnd,target,status='observed',value=None,note='Own reported round; future requests and endpoint forecasts remain predictions.'):
  quote=exact(p,n,sig);events.append(dict(round=rnd,target=target,value=value,status=status,note=note,revision_id=rev(p,n),quote=quote))
 if fam=='nyc-veterans':
  specs={
  'VeteranHelperJul03':[(V,1,1),(V,1,2),(V,1,3),(V,2,4)],'Dec30VeteranAgent':[(V,8,2),(B,2,4)],'VeteranWatcherNov25':[(V,9,2),(V,20,3),(V,32,4)],'VeteranObserverFeb11':[(V,11,1),(V,15,2),(V,29,3),(V,35,4)],'VeteranScoutFeb11C':[(V,12,1),(V,12,2),(V,21,3)],'Oct27VeteranAgent':[(V,13,1),(V,16,2),(V,28,3),(V,30,4)],'Feb22VeteranAgent':[(V,14,1),(V,14,2),(V,24,3),(V,38,4)],'Aug07VeteranResearcher':[(V,17,2),(V,22,3),(V,33,4)],'Oct27VeteranWatcherB':[(V,19,2),(V,27,3),(V,31,4)],'May08VeteranAgent':[(V,26,1),(V,26,2),(V,26,3),(B,1,4)],'Feb20VeteranAgent':[('Feb20VeteranAgent',1,4)]}[sig]
  targets={1:'World War II',2:'Korea',3:'Vietnam',4:'Gulf War (1990s)',5:'Gulf War (2001–)'}
  for p,n,rnd in specs:ev(p,n,rnd,targets[rnd])
  p,n,rnd=specs[-1]; ev(p,n,rnd+1,targets[rnd+1],'predicted')
 elif fam=='ihme-smoking':
  p,n=refs[0];ev(p,n,1,'1990')
  if sig=='OpenAIResearchMar23Smoking':ev(S,1,2,None,'predicted')
  elif sig=='OpenAIResearchMar16Smoking':ev(S,2,2,None,'predicted');ev(S,8,2,'1995','observed','25.522062%')
  else:ev(S,6,2,None,'predicted');ev(S,7,2,'1995','observed','25.52%')
 else:
  for rnd,target in enumerate(['Austria','Czechia','Mexico','Poland','Sweden'],1):ev(H,1,rnd,target,note='Normalized initial question to round 1; source R1–R4 are follow-ups 2–5.')
  ev(H,11,6,'United Kingdom / United States','predicted',note='Source R5/Q6 is scheduled, country is guessed; no arrival or termination observed.')
 rounds.append(dict(trajectory_id=tid,events=events))
 # Typed whole-span task timeline claims retain exact context without inventing a clock for individual naked timestamps.
 for m in msgs:
  for l in m['spans'][0]['text'].splitlines():
   if re.search(r'\d{1,2}:\d\d|\d+(?:m\d|h\d)',l):
    t['schedule_claims'].append(dict(observation_id=m['observation_id'],owner='self' if not ('Their R1' in l) else 'peer',clock_system='unspecified',task_date=None,round=None,event_kind='other',raw_value=l,status='reported',excerpt=l,supersedes=None))
# Explicit known freshness exclusions.
for t in out:
 sig=t['signature'];tid=t['trajectory_id']
 ex=[]
 if sig=='OpenAIResearchMar16Smoking':ex=[(S,3,'Compressed restatement of the prior Mar16 report; no independent task event.')]
 if sig=='OpenAIDec16Smoking':ex=[(S,8,'Encoding-only alteration of the Dec16 R2 report first published in revision 7; the fresh Mar16 paragraph belongs to another speaker.')]
 if sig=='VeteranHelperJul03':ex=[(V,10,'Restoration of already published July03 anchor and VH update after page deletion; not a new contribution.')]
 if sig=='OAIHouseholdNov02Scout':ex=[(H,n,'Whole-page restoration of revision 1; repeated historical report is not a fresh owned message.') for n in [3,5,8,10]]
 for p,n,reason in ex:
  r=by[rev(p,n)]; text=next((l for l in r['body'].splitlines() if sig in l),r['body']);t['excluded'].append(message(p,n,sig,tid,'exclude',reason,text))
json.dump(out,open(P/'dossiers.json','w'),indent=2);json.dump(rounds,open(P/'rounds.json','w'),indent=2)
coverage=[]
for fam,p,n in [('ihme-smoking',S,1),('nyc-veterans',V,1),('oecd-household-income',H,1),('unaids-bosnia-hiv','UNAIDSBosniaSequenceCollabNov2',1),('vermont-rent','RentVermontLamoilleSequenceSep26',1),('world-poverty-clock','WorldPovertyClockSequenceJun19',1)]:
 count=sum(t['task_id']==fam for t in out);r=by[rev(p,n)]
 reason=f'{count} supported histories traced across the complete archive, pending independent review.' if count else {'unaids-bosnia-hiv':'One substantive task anchor. Cross-family signed outreach at DataUSAStateSequenceCollab2027@22 repeats the task and asks for help; no distinct substantive task progression.','vermont-rent':'One substantive task anchor. AgentRentVermont@2 is a bare live-sequence backlink; it cannot independently establish a supported history.','world-poverty-clock':'One substantive WPC anchor. Other references relay the random-seed claim or concern different poverty tasks. Q4 is both called confirmed and described as due in this single source; this ambiguity is preserved.'}[fam]
 coverage.append(dict(family_id=fam,task_id=fam,title=tasks[fam]['title'],status='supported' if count else 'insufficient_evidence',reason=reason,anchors=[dict(revision_id=r['rev_id'],quote=r['body'])],search_notes=['Searched every archive revision without time window using task vocabulary, destination page names, body signatures, reply tags and backlinks; compared revisions to diff bases and earlier same-page bodies.','See *-search.json, fresh-review.txt and global-signed-review.txt for candidate retrieval coverage.','Existing audited 240 histories were checked for own-task/signature overlap; these missing families had no existing accounts.']))
json.dump(coverage,open(P/'coverage.json','w'),indent=2)
print('dossiers',len(out),'messages',sum(len(t['owned_messages']) for t in out),'events',sum(len(t['events']) for t in rounds))
