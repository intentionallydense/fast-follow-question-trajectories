import json,zipfile,re,pathlib
O=pathlib.Path(__file__).parent
rows=[json.loads(x) for x in zipfile.ZipFile('full-wiki-logs.zip').read('revisions.jsonl').splitlines()]
pat=re.compile(r'Ivy|SLP|SpeechPath|Speechlanguage|Puerto Rican|FuelPoverty|fuel poverty|GapminderAge80|GAP80|age80|LFRelay|LFAlign|LFHeartbeat|LFPromptFirst|LFResearch|Lymphatic Filariasis|MCV2|MCVScout|MCV sequence|MCV research|MayTwoMCV|Feb26MCV|April19MCV|Aug11MCV',re.I)
res=[]
for i,r in enumerate(rows,1):
 lines=r['body'].splitlines(True)
 for h in r['hunks']:
  if h['op']=='delete':continue
  s=''.join(lines[h['b0']:h['b1']])
  if pat.search(s):res.append(dict(revision_id=r['rev_id'],source_line=i,page_id=r['page_id'],editor=r['label'],text=s))
(O/'search-hits.json').write_text(json.dumps(res,indent=2))
(O/'search-hits.txt').write_text('\n'.join(f"\n### {r['revision_id']} {r['editor']}\n{r['text']}" for r in res))
print('archive',len(rows),'hits',len(res))
print('\n'.join(f"{r['revision_id']} {r['text'][:120]}" for r in res if r['page_id'] not in {json.loads(x)['page_id'] for x in open('task-replicas/remaining/family-map.jsonl')}))
