import json,collections
from pathlib import Path
base=Path('/home/public/projects/collusion-wiki/analysis/reconstruction')
p=json.loads((base/'audited_personas.json').read_text());c=json.loads((base/'curated_connections.json').read_text())
byname={x['reported_persona']:x['persona_id'] for x in p}
byid={x['persona_id']:x for x in p}
labelpersonas=collections.defaultdict(set)
for x in p:
 for label in x['editor_labels']:labelpersonas[label].add(x['persona_id'])
 for ev in x['primary_evidence']:labelpersonas[ev['editor_label']].add(x['persona_id'])
for x in c:
 if x['source'] in byname and x['relation_type'] in ['signed_run_continuity','run_fingerprint','timing_reply','direct_reply','answer_receipt','reported_counter_receipt','clock_acceleration','external_signal_plan','counter_test_noise','observer_contamination','heartbeat_audit_claim']:
  for ev in x['evidence']:labelpersonas[ev['editor_label']].add(byname[x['source']])
 if x['source'].startswith('editor:') and x['target'] in byname:labelpersonas[x['source'][7:]].add(byname[x['target']])
def endpoint(s):
 if s in byname:return {'kind':'trajectory','id':byname[s],'label':s,'mapping_basis':'Exact curated reported-persona match; not editor-name inference.'}
 if s.startswith('editor:'):return {'kind':'editor','id':s,'label':s[7:],'associated_trajectory_ids':sorted(labelpersonas[s[7:]]),'mapping_basis':'Editor associations are retained separately, never merged into a trajectory.'}
 if s.startswith(('page:','dse/','probier/')):return {'kind':'page','id':s.removeprefix('page:'),'label':s.removeprefix('page:')}
 if s.startswith('counter:'):return {'kind':'counter','id':s,'label':s[8:]}
 return {'kind':'external_persona' if s else 'unresolved','id':s,'label':s,'mapping_basis':'Outside selected49 or no explicit mapping; no fuzzy date/name matching.'}
interaction={'timing_reply','lead_comparison','relay_request','answer_receipt','reported_counter_receipt','reported_answer_relay','answer_acknowledged','direct_reply','answer_relay_acknowledged','heartbeat_audit_claim','clock_divergence','distinct_run_witness','distinct_run_reports_with_replies'}
identity={'editor_persona_association','signed_persona_claim','conflicting_persona_claim','do_not_merge','same_run_continuity','alias_continuity_candidate','possible_persona_rename','generic_editor_collision_risk','semantic_signature_differs_from_editor','weak_reused_editor'}
page={'cross_task_referral','cross_page_referral','page_migration','backup_relay','explicit_page_link','explicit_coordination_migration','coordination_page_creation','explicit_cross_family_link','possible_cross_wiki_migration','possible_cross_page_continuity','shared_rare_source'}
rows=[]
for x in c:
 category='interaction' if x['relation_type'] in interaction else 'identity_evidence' if x['relation_type'] in identity else 'page_connection' if x['relation_type'] in page else 'trajectory_evidence'
 y={**x,'source_endpoint':endpoint(x['source']),'target_endpoint':endpoint(x['target']),'category':category,'derived':False,'direction_note':'Arrow preserves source → target in curated ledger; for receipts, source is receiver and target is reported sender. An arrow does not assert common identity.','counts_as_person_to_person_exchange':category=='interaction' and endpoint(x['source'])['kind'] in ['trajectory','external_persona'] and endpoint(x['target'])['kind'] in ['trajectory','external_persona']}
 y['trajectory_ids']=sorted(set(e['id'] for e in [y['source_endpoint'],y['target_endpoint']] if e['kind']=='trajectory'))
 if x['connection_id']=='SEQ020':y['interpretation_warning']='P08 re-identifies its own run on another page and compares P07 as a peer. This is not P08=P07 and is not evidence of answer transfer.'
 if x['connection_id']=='SEQ016':y['interpretation_warning']='Same timing cohort is not same run. Excerpt includes direct request to Jan12.'
 if x['connection_id']=='LATE016':y['direction_note']='P38 publishes Bahrain; P36 explicitly acknowledges receipt. Sender → receiver.'
 rows.append(y)
# Add directly addressed interactions whose existing curated relation type records only continuity.
extra=[('SEQ006','P10','P02','direct_reply','Explicitly addresses SectorAgentJun20X while denying participation in the sector task; retained as cross-task reply.'),('SEQ016','P08','P07','relay_request','Explicit request to Jan12 for third prompt timing/state; same-cohort claim does not imply identity.'),('SEQ037','P17','P18','relay_request','Explicit @Nov09ConstructionAgent timing request.'),('SEQ038','P17','P19','relay_request','Explicit @ConstructionAgentJun29 R3 announcement request.'),('SEQ039','P17','P20','signal_request','Explicit @AgentConstructionNYCATXFL20270603 request to pre-signal R5.'),('SEQ040','P17','P20','signal_request','Jun03 lead shorthand resolves to the Jun03 trajectory addressed in SEQ039 on this page; contextual mapping.'),('SEQ042','P17','P22','signal_request','Explicit @ChatGPTAug11 request to signal state before possible termination.'),('SEQ043','P17','P22','reported_counter_receipt','Aug11 counter-name reference maps to ChatGPTAug11 on same construction page; self-reported signal receipt, no counter telemetry.')]
byconn={x['connection_id']:x for x in c}
for parent,src,tgt,rel,note in extra:
 orig=byconn[parent]
 rows.append({'connection_id':'DERIVED-'+parent,'parent_connection_id':parent,'reviewer':'explorer normalization','relation_type':rel,'source':byid[src]['reported_persona'],'target':byid[tgt]['reported_persona'],'source_endpoint':endpoint(byid[src]['reported_persona']),'target_endpoint':endpoint(byid[tgt]['reported_persona']),'source_page':orig['source_page'],'target_page':orig['source_page'],'category':'interaction','derived':True,'counts_as_person_to_person_exchange':True,'trajectory_ids':[src,tgt],'confidence':'medium_conditional_on_recorded_claim' if parent in ['SEQ040','SEQ043'] else orig['confidence'],'uncertainty':note+' '+orig['uncertainty'],'evidence':orig['evidence'],'direction_note':'Speaker → addressed/referenced peer. Receipt arrows point receiver → sender.'})
# Retain evidence associations separately. Only exact mappings, never shared-page identity links.
facts=[]
for x in p:
 ev=list(x['primary_evidence'])
 for row in rows:
  if row['source_endpoint']['kind']=='trajectory' and row['source_endpoint']['id']==x['persona_id'] and row['relation_type']!='answer_relay_acknowledged':ev+=row['evidence']
 ev=list({e['revision_id']:e for e in ev}.values())
 facts.append({'persona_id':x['persona_id'],'reported_persona':x['reported_persona'],'confidence':x['confidence'],'schedule':x['schedule'],'uncertainty':x['uncertainty'],'basis':'Original selected hand-audited trajectory, supported by signed self-reports, task-clock/schedule consistency and cited continuity. This normalization does not refit or authenticate the cluster.','editor_labels_from_selected_and_curated_evidence':sorted(set(e['editor_label'] for e in ev)),'evidence_revision_ids':sorted(set(e['revision_id'] for e in ev)),'interaction_connection_ids':[r['connection_id'] for r in rows if x['persona_id'] in r['trajectory_ids'] and r['category']=='interaction']})
result={'schema_version':1,'scope':'49 selected reported trajectories; not a census. All108 curated records retained with semantics, plus8 excerpt-derived direct interactions.','mapping_rules':['Exact reported_persona matches only.','editor: endpoints remain editors; associations do not imply identity.','Shared pages alone produce no person-to-person exchange.','Same cadence, date suffix or repeated editor label alone does not merge runs.','Page continuity edges must not be rendered as agent identity equivalence.','Multiple records can cite one revision; deduplicate revision IDs when displaying post counts.','External persona refers to a recorded label outside the selected49, not an independently authenticated agent.'],'connections':rows,'clustering_facts':facts,'editor_collisions':[{'editor_label':k,'trajectory_ids':sorted(v),'warning':'Same editor carries multiple selected persona claims; do not merge these trajectories.'} for k,v in sorted(labelpersonas.items()) if len(v)>1],'special_uncertainties':[{'persona_id':'P11','reason':byid['P11']['uncertainty']},{'persona_id':'P27','reason':byid['P27']['uncertainty']},{'persona_id':'P17','reason':'Ten distinct editor labels appear in SEQ036–SEQ045 while the signature and task schedule identify the selected Mar08 trajectory. The original persona table lists only three from its primary excerpts.'}],'counts':{'original_connections':len(c),'derived_connections':len(extra),'selected_personas':len(p),'interaction_records':sum(r['category']=='interaction' for r in rows),'interaction_records_involving_selected49':sum(r['category']=='interaction' and bool(r['trajectory_ids']) for r in rows)}}
Path('/tmp/trajectory-interaction-map.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['counts']);print(result['editor_collisions'])
