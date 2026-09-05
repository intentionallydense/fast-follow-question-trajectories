"""Promote the independently reviewed family research into reproducible Site inputs."""
import hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
DEST=HERE.parents[1]/'trajectory-explorer/research/family-completion'
reviews=['independent-review-root.json','independent-review-a.json','independent-review-b.json']
combined={n:[] for n in ['dossiers.json','rounds.json','coverage.json']}
for group,review_name in zip('abc',reviews):
    src=HERE/f'group-{group}'
    review=json.loads((src/review_name).read_text())
    assert review['status']=='passed',(group,review)
    for name,digest in review.get('input_sha256',review.get('artifact_sha256',{})).items():
        assert hashlib.sha256((src/name).read_bytes()).hexdigest()==digest,(group,name,'changed since review')
    for n in combined:
        combined[n]+=json.loads((src/n).read_text())
    target=DEST/f'group-{group}'
    target.mkdir(parents=True,exist_ok=True)
    for p in src.glob('*.json'):
        if p.name.endswith('-search.json') or p.name in ['hits.json','search-hits.json']:continue
        shutil.copyfile(p,target/p.name)
for t in combined['dossiers.json']:t['status']='supported'
for n,data in combined.items():
    (DEST/n).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(HERE/'group-b/existing-trajectory-corrections.json',DEST/'existing-trajectory-corrections.json')
shutil.copyfile(HERE/'validation.json',DEST/'validation.json')
shutil.copyfile(HERE.parent/'trajectory-assembly/research/RULES-v1.md',DEST/'RULES-v1.md')
shutil.copyfile(HERE.parent/'trajectory-assembly/PROTOCOL.md',DEST/'PROTOCOL.md')
names=[*combined,'existing-trajectory-corrections.json','inventory.json']
gate={'status':'passed','trajectory_ids':[t['trajectory_id'] for t in combined['dossiers.json']],
      'reviews':[f'group-{g}/{r}' for g,r in zip('abc',reviews)],
      'accepted_sha256':{n:hashlib.sha256((DEST/n).read_bytes()).hexdigest() for n in names},
      'policy':'R01–R14; two substantive fresh contributions across distinct revisions; independent source/semantic review; source integrity and zero ownership overlap.'}
(DEST/'review-gate.json').write_text(json.dumps(gate,indent=2)+'\n')
print('Promoted',len(combined['dossiers.json']),'histories;',len(combined['coverage.json']),'family reviews')
