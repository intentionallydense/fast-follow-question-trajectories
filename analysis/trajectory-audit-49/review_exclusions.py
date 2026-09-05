"""Record source-checked root review of the snapshot's 39 excluded observations."""
from pathlib import Path
import json,zipfile,difflib,collections
ROOT=Path(__file__).resolve().parent
with zipfile.ZipFile(ROOT.parent.parent/'full-wiki-logs.zip') as z:
 rs={r['rev_id']:(i,r) for i,r in enumerate(map(json.loads,z.read('revisions.jsonl').splitlines()),1)}
result=[]
for f in sorted((ROOT/'input').glob('P*.json')):
 p=json.loads(f.read_text())
 for e in p['excluded_candidates']:
  rid=e['revision_id'];_,r=rs[rid]; old=rs.get(r['diff_base'],(None,{}))[1]
  item=dict(persona_id=p['id'],observation_id=e['observation_id'],revision_id=rid,source_line=e['source_line'],original_reasons=e['reasons'],evidence=[dict(revision_id=rid,source_line=e['source_line'],excerpt=e['excerpt'])])
  if p['id']=='P06':
   item.update(decision='include',scope='whole',reason='Fresh first-person clothing-task outreach explicitly names industry4481, years2015–17, CA→NY sequence and the trajectory coordination page. Different destination-page family is not a task-identity conflict.',rule_tags=['destination_not_task','signature_and_task_bridge'])
  elif p['id']=='P10':
   item.update(decision='unresolved',scope='whole',reason='Fresh signed sector outreach, but no clothing-task clock, unique source-page backlink or other decisive bridge to P10. The signature alone is insufficient under the precision-first policy; wrong page family alone is not affirmative exclusion evidence.',rule_tags=['destination_not_task','insufficient_task_bridge'])
  elif p['id']=='P28':
   item.update(decision='exclude',scope='whole',reason='Own Oct02 R3/R4 statement belongs to an Asian-enrollment task (University of Arizona, R4 due09:50:37), not the CVD country sequence. A matching Oct02 signature cannot override incompatible first-person task identity; do not assume multi-task assignment.',rule_tags=['conflicting_own_task','editor_not_identity'])
  elif p['id']=='P34':
   marker='Heartbeat audit:' if e['observation_id']=='S03600' else 'Horizon beacon plan:'
   before,after=e['excerpt'].split(marker,1);fresh=marker+after
   item.update(decision='include',scope='partial',included_excerpts=[fresh],excluded_excerpts=[before],reason='The revision concatenates an inherited signed paragraph and a new signed paragraph on one line. Diff-base comparison separates the fresh Nov28 contribution; preserve only that contribution, not the whole multi-signature line.',rule_tags=['split_mixed_span','signature_and_task_bridge'],already_represented_in_input=e['observation_id']=='S03600')
   if old:
    matching=max(old['body'].split('\n'),key=lambda s:difflib.SequenceMatcher(None,s,before,autojunk=False).ratio())
    item['evidence'].append(dict(revision_id=old['rev_id'],source_line=rs[old['rev_id']][0],excerpt=matching))
   if e['observation_id']=='S03600':item['reason']+=' The clean Heartbeat audit span already appears in P34’s included records; do not add it a second time.'
   else:item['reason']+=' Its R1 23:39:18 and R6 01:27:23 match P34’s established schedule across midnight.'
  else:
   item.update(decision='exclude',scope='whole',reason='Previously present signed claim reappears through encoding/formatting change or restoration on the same page. It is evidence of retained page history, not a fresh trajectory message at this revision time.',rule_tags=['inherited_not_fresh'])
   # @14 was truncated; @15 restores a previously existing Oct30 report.
   comparison=rs['dse~OECDRegionalRecoveryCO2Sequence@2'][1] if rid=='dse~OECDRegionalRecoveryCO2Sequence@15' else old
   matching=max(comparison['body'].split('\n'),key=lambda s:difflib.SequenceMatcher(None,s,e['excerpt'],autojunk=False).ratio())
   item['evidence'].append(dict(revision_id=comparison['rev_id'],source_line=rs[comparison['rev_id']][0],excerpt=matching))
  item['already_represented_in_input'] = any(post['revision_id'] == rid and any(part in quote for quote in post['excerpts']) for post in p['posts'] for part in item.get('included_excerpts', [e['excerpt']]))
  for evidence in item['evidence']:assert evidence['excerpt'] and evidence['excerpt'] in rs[evidence['revision_id']][1]['body']
  result.append(item)
assert len(result)==39
(ROOT/'excluded-observation-decisions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(collections.Counter(x['decision'] for x in result))
