import json
from pathlib import Path
f=Path('/tmp/trajectory-interaction-map.json');d=json.loads(f.read_text());p=json.load(open('/home/public/projects/collusion-wiki/analysis/reconstruction/audited_personas.json'))
primary={e['revision_id']:x['persona_id'] for x in p for e in x['primary_evidence']}
for row in d['connections']:
 for ev in row['evidence']:
  src=row['source_endpoint'];tgt=row['target_endpoint'];author=None;basis='Unresolved in normalization; editor label alone is not author identity.'
  if ev['revision_id'] in primary:
   author={'kind':'trajectory','id':primary[ev['revision_id']]};basis='Revision is primary excerpt for selected persona dossier.'
  elif row['connection_id']=='LATE016':
   author=src if ev['revision_id'].endswith('R4Signal@1') else tgt;basis='Explicit signed publisher in first excerpt; explicit signed recipient acknowledgment in second excerpt.'
  elif row['connection_id']=='LATE001':author=tgt;basis='Acknowledgment is written by Sep08 recipient; inferred Apr04 sender is not author of this excerpt.'
  elif src['kind']=='editor' and tgt['kind'] in ['trajectory','external_persona'] and row['relation_type'] in ['signed_persona_claim','conflicting_persona_claim']:
   author=tgt;basis='Curated signed-persona claim under editor label; conditional self-identification.'
  elif src['kind'] in ['trajectory','external_persona'] and row['category'] in ['interaction','trajectory_evidence','page_connection']:
   author=src;basis='Curated source is speaker of the cited first-person report; conditional on recorded claim.'
  elif src['kind']=='trajectory' and row['relation_type'] in ['editor_persona_association','do_not_merge']:
   author=src;basis='Curated first-person source persona; editor and comparison target are separate entities.'
  ev['evidence_author_ids']=[author['id']] if author and author['kind']=='trajectory' else []
  ev['evidence_author_endpoint']=author
  ev['evidence_author_mapping_basis']=basis
 row['evidence_author_ids']=sorted({a for ev in row['evidence'] for a in ev['evidence_author_ids']})
d['mapping_rules'].append('Use each evidence.evidence_author_ids for timeline ownership, not connection source/target. LATE016 has publisher P38 then recipient P36; LATE001 is recipient-authored; SEQ033 source is recipient P15.')
f.write_text(json.dumps(d,indent=2)+'\n')
print(f, f.stat().st_size)
