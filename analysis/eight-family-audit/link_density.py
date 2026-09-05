#!/usr/bin/env python3
"""Transparent line-based link-dominance screen, pooled deduplicated histories."""
import collections,csv,html,json,random,re,zipfile
from pathlib import Path
from audit import FAMILIES
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
URL=re.compile(r'https?://[^\s<>\[\]{}"\u201c\u201d]+',re.I)
WIKI=re.compile(r'\[\[[^\]]+\]\]')
def classify(line):
 line=' '.join(html.unescape(line).split())
 if line.strip(' .') in ('','Beschreibe hier die neue Seite','Describe the new page here'):return None
 has=bool(URL.search(line) or WIKI.search(line))
 rest=URL.sub(' ',WIKI.sub(' ',line));rest=re.sub(r'<[^>]+>',' ',rest)
 # Up to 12 words of labels/annotation around source links; long prose stays prose.
 words=re.findall(r'\b\w+\b',rest)
 return line,has and len(words)<=12

def main():
 with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as z:
  pages={p['page_id']:p for p in map(json.loads,z.read('pages.jsonl').splitlines())}
  histories=collections.defaultdict(dict)
  for r in map(json.loads,z.read('revisions.jsonl').splitlines()):
   if pages[r['page_id']]['page_family'] not in FAMILIES:continue
   for line in r['body'].splitlines():
    c=classify(line)
    if c:histories[r['page_id']][c[0]]=c[1]
 rows=[]
 for pid,p in pages.items():
  if p['page_family'] not in FAMILIES:continue
  ls=histories[pid];n=len(ls);k=sum(ls.values())
  rows.append(dict(page_id=pid,family=p['page_family'],distinct_lines=n,link_lines=k,link_fraction=k/n if n else 0,mostly_links=bool(n and k/n>=.5)))
 with (OUT/'link-density.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary={'pages':len(rows),'thresholds':{str(t):sum(r['link_fraction']>=t for r in rows) for t in [.5,.6,.75,.9,1.]},'families':{f:sum(r['mostly_links'] for r in rows if r['family']==f) for f in FAMILIES},'method':'At least 50% of distinct nonempty, non-placeholder lines across retained page history consist of HTTP(S)/wiki links with at most 12 residual words (labels/short annotations). Lines deduplicated after HTML unescape and whitespace normalization. Not an exhaustive manual classification.'}
 (OUT/'link-density-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
 sample=random.Random(20260905).sample([r for r in rows if r['mostly_links']],20)
 with (OUT/'link-density-sample.txt').open('w') as f:
  for r in sample:
   f.write('\n'+json.dumps(r)+'\n')
   f.write('\n'.join(list(histories[r['page_id']])[:12])+'\n')
if __name__=='__main__':main()
