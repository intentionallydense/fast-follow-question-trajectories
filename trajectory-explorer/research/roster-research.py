import json,re,zipfile
ps=json.load(open('analysis/reconstruction/audited_personas.json'));cs=json.load(open('analysis/reconstruction/curated_connections.json'))
z=zipfile.ZipFile('full-wiki-logs.zip');rs={r['rev_id']:r for r in map(json.loads,z.open('revisions.jsonl'))}
primary={p['persona_id']:p['reported_persona'] for p in ps[:24]}
primary.update(dict(zip(['P'+str(i) for i in range(25,50)],['OpenAIResearchApr23','OpenAIResearchApr30','Sep24CVDScout','OpenAIResearchOct02','Aug24CVDScout','OpenAIJan18Scout','OpenAINov16CVD','May26CVDScout','Oct03CVDScout','OpenAINov28CVDLive','FPSequenceAgentMar31','OpenAIFPResearchSep05','OpenAIFPResearchNov28','OpenAINov27FP','OpenAIJul20FPScout','OpenAIFeb07FPScout','March16ScoutB','OpenAIDec04Equity','OAIResearchAug21OECD','April11OECDScout','OpenAIOECDNov27','Aug09OECDScout','RRPFeb15Scout','RRPOct30Scout','RRPFeb03Scout'])))
# Date labels only identify first-person material in a specified task family, never globally.
short={'P01':'Apr2','P02':'Jun20X','P03':'Jun15','P04':'May24','P05':'May24','P07':'Jan12','P08':'Aug08','P09':'May24','P10':'May15','P11':'Jan29','P12':'Apr27','P13':'Mar13','P14':'Aug14','P16':'Jan31','P17':'Mar08','P18':'Nov09','P19':'Jun29','P20':'Jun03','P21':'Nov08','P22':'Aug11','P23':'Dec30','P24':'Apr02'}
for p in ps[24:]:short[p['persona_id']]=p['reported_persona'].split(':')[-1]
out=[]
for p in ps:
 pid=p['persona_id'];sig=primary[pid];evid=p['primary_evidence'];proof=[{'revision_id':e['revision_id'],'excerpt':e['excerpt'],'basis':'Exact semantic signature in audited primary evidence'} for e in evid if re.search(r'(?<![A-Za-z0-9])'+re.escape(sig)+r'(?![A-Za-z0-9])',e['excerpt'])]
 if not proof and pid=='P17':proof=[{'revision_id':'dse~DataUSAConstructionSequenceMar08@1','excerpt':rs['dse~DataUSAConstructionSequenceMar08@1']['body'],'basis':'Full raw creation body signs ConstructionAgentMar08 after the exact audited Mar08 initial schedule'}]
 if not proof and pid=='P43':proof=[{'revision_id':'dse~OECDEquityPrecisionProof@1','excerpt':rs['dse~OECDEquityPrecisionProof@1']['body'],'basis':'Signed Aug21 OECD reproduction; same semantic Aug21 cohort and editor as unsigned primary. Contextual linkage only, no matching schedule in this revision.'}]
 sigs=[{'token':sig,'confidence':'contextual_medium' if pid=='P43' else 'high_conditional','evidence':proof}]
 if pid=='P34':
  ids=['dse~OpenAICVDDec08Fast2028@26','dse~OpenAICVDDec08Fast2028@32']; ss=[]
  for rid in ids:
   r=rs[rid];ls=r['body'].splitlines();add='\n'.join('\n'.join(ls[h['b0']:h['b1']]) for h in r['hunks'] if h['op'] in ['insert','replace']);ss.append({'revision_id':rid,'excerpt':add,'basis':'OpenAINov28CVD signed Nov28 CVD trajectory shares R1 23:39:18 and R6 01:27:23 with OpenAINov28CVDLive primary; consistent 22s tier.'})
  sigs.append({'token':'OpenAINov28CVD','confidence':'high_conditional','evidence':ss})
 prefix=[]
 if pid in short:
  tok=short[pid]
  for e in evid:
   txt=e['excerpt']
   if re.match(r"^[\s*']*(?:LIVE |CONFIRMED |Matching |Our |Fresh |Earlier |Independent |CORROBORATING COHORT \()?"+re.escape(tok),txt,re.I) or re.match(r'^'+re.escape(sig)+':',txt):
    prefix.append({'token':tok,'page_id':e['page_id'],'revision_id':e['revision_id'],'example':txt[:240],'restriction':'Only leading first-person status/cohort heading on this task family, and no conflicting signature. Date mention/addressee alone is not authorship.','confidence':'contextual_medium'})
 names={p['reported_persona'],p['original_persona_id'],sig,pid}
 exclusions=[{'connection_id':c['connection_id'],'relation_type':c['relation_type'],'source':c['source'],'target':c['target'],'uncertainty':c['uncertainty'],'revision_ids':[e['revision_id'] for e in c['evidence']]} for c in cs if c['relation_type'] in ['do_not_merge','distinct_runs','distinct_personas','generic_editor_collision_risk','cross_task_observer'] and (c['source'] in names or c['target'] in names)]
 if pid in ['P04','P05']:exclusions.append({'other_persona_id':'P05' if pid=='P04' else 'P04','reason':'Same May24 sector date label, distinct schedules: CT 08:01:50 10s vs 20:05:38 13s. Do not attribute unsigned May24 sector posts by date alone.'})
 if pid in ['P25','P37']:exclusions.append({'other_persona_id':'P37' if pid=='P25' else 'P25','reason':'Shared editor OpenAIResearchApr23 does not merge CVD Apr23 signature with FP Nov28 signature.'})
 if pid=='P11':exclusions.append({'reason':'Initial California time inferred; New York observed 13:27:29 contradicts prediction 14:32:19. Preserve correction, do not split run for prediction error.'})
 if pid=='P10':exclusions.append({'reason':'Sector page appearances include explicit observer statement; do not classify as sector trajectory. Task UTC mapping corrected at DataUSAClothingLive9m17@9.'})
 out.append({'persona_id':pid,'reported_persona':p['reported_persona'],'family':p['family'],'semantic_signatures':sigs,'short_reference_tokens':[short[pid]] if pid in short else [],'contextual_unsigned_prefixes':prefix,'primary_revision_ids':[e['revision_id'] for e in evid],'schedule_facts_as_reported':p['schedule'],'clustering_explanation':'Group first-person contributions carrying the proved semantic signature, then retain page/family and reported clock/timer continuity. This is a reported task trajectory, not an authenticated process. Short date tags are contextual references only; shared editor labels or matching cadence never establish identity.','exclusions':exclusions,'uncertainty':p['uncertainty']})
json.dump({'method':'Exact semantic signature roster for 49 selected audited trajectories. Signature occurrence must be a signature/first-person heading, not a quoted or addressed name. Deduplicate unchanged page inheritance before applying. Unsigned context rules are weaker. Extra signatures carry revision evidence; never merge editor labels transitively.','personas':out},open('/tmp/trajectory-persona-roster.json','w'),ensure_ascii=False,indent=2)
print('Wrote',len(out),'personas;',sum(len(p['semantic_signatures']) for p in out),'signature entries;',sum(len(p['contextual_unsigned_prefixes']) for p in out),'primary-evidence contextual prefix examples')
for p in out:
 if not p['semantic_signatures'][0]['evidence']:print('NO PROOF',p['persona_id'])
