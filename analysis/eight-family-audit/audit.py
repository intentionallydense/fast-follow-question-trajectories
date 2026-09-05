#!/usr/bin/env python3
"""Offline body-marker inventory, not inferred tasks or identities."""
import collections,csv,hashlib,html,json,re,zipfile
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
FAMILIES=['loop-chain-infrastructure','mixed-task','off_store_unclassified','probe-test','relay-coordination','source-cache-url-list','source-or-unclassified','unknown']
PATTERNS={
 'county_json':r'county\.json',
 'sec_regcf_context':r'regCF|raising.capital.map|us-ma-\d{3}',
 'datausa':r'datausa\.io|data ?usa',
 'oecd':r'oecd',
 'health':r'healthdata|\bIHME\b|ourworldindata|unaids',
 'usaspending':r'usaspending',
 'msu_archive':r'((?:msu|mankato).{0,50}(?:reporter|archive)|arch\.lib\.mnsu)',
 'other_public_sources':r'dataafrica|aihw|pbs\.gov|uefa|gapminder|sdgindex|worldpoverty|ninis|fuel.poverty',
}
def decoded(s):
 s=html.unescape(s)
 for _ in range(3):s=unquote(s)
 return s

def main():
 with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as z:
  assert all(hashlib.sha256(z.read(n)).hexdigest()==h for h,n in (s.split() for s in z.read('SHA256SUMS').decode().splitlines()))
  pages={p['page_id']:p for p in map(json.loads,z.read('pages.jsonl').splitlines())}
  revs=list(map(json.loads,z.read('revisions.jsonl').splitlines()))
 by=collections.defaultdict(list)
 for i,r in enumerate(revs,1):r['source_line']=i;by[r['page_id']].append(r)
 rows=[];hits=[];summary={}
 for pid,p in pages.items():
  if p['page_family'] not in FAMILIES:continue
  rr=by[pid];row={'page_id':pid,'family':p['page_family'],'method':p['page_family_method'],'revisions':len(rr),'first_time':min(r['time'] for r in rr),'last_time':max(r['time'] for r in rr)}
  for k,pat in PATTERNS.items():
   found=None
   for r in rr:
    s=decoded(r['body']);m=re.search(pat,s,re.I)
    if m:
     found={'page_id':pid,'family':p['page_family'],'marker':k,'rev_id':r['rev_id'],'source_line':r['source_line'],'decoded_context':s[max(0,m.start()-160):m.end()+300]};break
   row[k]=bool(found)
   if found:hits.append(found)
  rows.append(row)
 for f in FAMILIES:
  subset=[r for r in rows if r['family']==f]
  summary[f]={'pages':len(subset),'revisions':sum(r['revisions'] for r in subset),'methods':dict(collections.Counter(r['method'] for r in subset)),**{k:sum(r[k] for r in subset) for k in PATTERNS}}
 with (OUT/'page-inventory.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (OUT/'marker-evidence.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in hits))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
