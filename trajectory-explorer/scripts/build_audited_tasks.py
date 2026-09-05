"""Build the task browser solely from supported audited histories and owned-span extraction."""
import hashlib
import json
from collections import Counter
from build_task_trajectories import ROOT, COMPLETION, completion_data
import zipfile

TITLES = {
 'datausa-sector61-state':'Sector 61–62 · state workforce',
 'datausa-clothing-workforce':'Clothing stores · state workforce',
 'datausa-grocery-workforce':'Grocery stores · state workforce',
 'datausa-construction-workforce-ny':'Construction · NY sequence, 2016 & 2018',
 'datausa-construction-workforce-az':'Construction · Arizona sequence, 2016',
 'ihme-cvd-deaths':'Cardiovascular deaths · country sequence',
 'ihme-family-planning':'Family planning · modern methods, 1992',
 'oecd-preprimary-private-spending':'OECD · private pre-primary spending',
 'oecd-regional-co2':'OECD · electricity-generation CO₂',
 'datausa-police-wage-age':'Police officers · wages by age',
 'datausa-language-french':'French / Cajun · state language shares',
 'datausa-poverty-county':'County poverty · ACS1, 2021',
 'datausa-construction-wage':'Construction · female electrician wages',
 'datausa-cashiers-masters':'Cashiers · master’s fields, 2014',
 'datausa-production-share':'Production occupations · city / gender shares',
 'datausa-finance-gender-gap':'Finance & insurance · occupation wage gaps',
 'datausa-maids-wage':'Maids & cleaners · gender/year wages',
 'uefa-pass-accuracy':'UEFA U21 · pass accuracy, 2021',
 'cashiers-bachelors-2015':'Cashiers · bachelor’s fields, 2015',
 'datausa-transport-production':'Transportation equipment · outbound production',
 'datausa-occupation-salary-61-62':'Sector 61–62 · occupation salaries',
 'datausa-enrollment-asian':'Universities · Asian enrollment',
 'datausa-poverty-state':'State poverty · 2013 & 2022',
 'sdg-index-score':'SDG Index · country/year scores',
 'labor-force-followup':'Labor force · year follow-up',
}

def build():
    roster = json.loads((ROOT/'app/tasks/assembled-index.json').read_text())['trajectories']
    supported = {r['id']: r for r in roster if r['status'] != 'provisional'}
    extracted = json.loads((ROOT/'research/audited-rounds.json').read_text())
    extracted += completion_data('rounds.json')
    assert len(extracted) == len(supported)
    assert {r['trajectory_id'] for r in extracted} == set(supported)
    inventory = completion_data('inventory.json')
    TITLES.update({r['task_id']: r['title'] for r in inventory if r['task_id'] not in TITLES})
    tasks = {r['task_id']: dict(id=r['task_id'], title=TITLES[r['task_id']], family_id=r['family_id'], accounts=[], coverage=None) for r in inventory}
    coverage = completion_data('coverage.json')
    if coverage:
        gate = json.loads((COMPLETION/'review-gate.json').read_text())
        audit = dict(gate=gate, coverage=coverage,
            reviews=[json.loads((COMPLETION/path).read_text()) for path in gate['reviews']],
            corrections=completion_data('existing-trajectory-corrections.json'))
        (ROOT/'public/data/family-completion-review.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
        (ROOT/'public/data/trajectory-audit-rules.md').write_text((COMPLETION/'RULES-v1.md').read_text())
    with zipfile.ZipFile(ROOT.parent/'full-wiki-logs.zip') as archive:
        sources = {r['rev_id']: dict(r,jsonl_line=i) for i,line in enumerate(archive.read('revisions.jsonl').splitlines(),1) for r in [json.loads(line)]}
    for c in coverage:
        anchors=[]
        for a in c['anchors']:
            src=sources[a['revision_id']]
            start=src['body'].index(a['quote'])
            anchors.append(dict(a,jsonl_line=src['jsonl_line'],body_line=src['body'][:start].count('\n')+1,
                server_time=src['time'],recorded_editor=src['label'],start_char=start,end_char=start+len(a['quote']),
                text_sha256=hashlib.sha256(a['quote'].encode('latin1')).hexdigest(),observation_id='family-anchor',
                diff_base=src['diff_base'],body=src['body']))
        tasks[c['task_id']]['coverage']=dict(c,anchors=anchors)
    for r in extracted:
        row = supported[r['trajectory_id']]
        tid = row['task_id'] or 'labor-force-followup'
        dossier = json.loads((ROOT/'public'/row['file'].lstrip('/')).read_text())
        def citation(item):
            matches = [(m,s) for m in dossier['owned_messages'] if m['revision_id']==item['revision_id'] for s in m['spans'] if s['text']==item['quote']]
            assert matches, (r['trajectory_id'],item)
            m,s = matches[0]
            src = dossier['evidence'][item['revision_id']]
            assert src['body'][s['start_char']:s['end_char']] == item['quote']
            assert hashlib.sha256(item['quote'].encode('latin1')).hexdigest() == s['text_sha256']
            return dict(revision_id=item['revision_id'],quote=item['quote'],jsonl_line=src['jsonl_line'],
                body_line=src['body'][:s['start_char']].count('\n')+1,server_time=src['server_time'],
                recorded_editor=src['recorded_editor'],start_char=s['start_char'],end_char=s['end_char'],
                text_sha256=s['text_sha256'],observation_id=m.get('observation_id',m.get('record_id')))
        events=[]
        for i,e in enumerate(r['events']):
            assert isinstance(e['round'],int) and e['round']>0
            assert e['status'] in ['observed','predicted','scheduled','cached','indirect','inferred']
            assert e['target'] is None or isinstance(e['target'],str)
            assert e['value'] is None or isinstance(e['value'],str)
            events.append(dict(id=f"{row['id']}:E{i+1}",round=e['round'],target=e['target'],value=e['value'],status=e['status'],note=e['note'],citation=citation(e)))
        timing=[]
        for t in r['timing']:
            assert t['kind'] in ['initial','followup','cooldown','cadence'] and isinstance(t['seconds'],(int,float)) and t['seconds']>=0
            timing.append(dict(kind=t['kind'],seconds=t['seconds'],qualifier=t['qualifier'],citation=citation(t)))
        account=dict(id=row['id'],name=row['name'],description=row['title'],rationale=row['rationale'],
            dossier_file=row['file'],uncertainties=dossier['uncertainties'],events=events,timing=timing)
        tasks.setdefault(tid,dict(id=tid,title=TITLES[tid],accounts=[]))['accounts'].append(account)
    dest=ROOT/'public/data/audited-tasks'
    dest.mkdir(exist_ok=True,parents=True)
    if 'labor-force-followup' not in tasks:
        (dest/'labor-force-followup.json').unlink(missing_ok=True)
    catalog=[]
    for task in sorted(tasks.values(),key=lambda t:t['title']):
        task['rounds']=sorted({e['round'] for a in task['accounts'] for e in a['events']})
        task['accounts'].sort(key=lambda a:(a['name'].lower(),a['id']))
        (dest/(task['id']+'.json')).write_text(json.dumps(task,ensure_ascii=False,indent=2)+'\n')
        catalog.append(dict(id=task['id'],title=task['title'],account_count=len(task['accounts']),
            family_id=task.get('family_id'),coverage_status=(task.get('coverage') or {}).get('status','supported'),
            event_count=sum(len(a['events']) for a in task['accounts']),rounds=task['rounds'],
            file='/data/audited-tasks/'+task['id']+'.json'))
    index=dict(tasks=catalog,account_count=len(supported),excluded_provisional=[r['id'] for r in roster if r['status']=='provisional'],
        family_count=len({r['family_id'] for r in inventory if r['family_id']}),
        supported_task_count=sum(bool(t['account_count']) for t in catalog),
        event_count=sum(t['event_count'] for t in catalog),source_policy='Only owned spans of supported audited trajectories supply claims; no legacy rows or associated-peer messages are imported. Indirect claims within own messages remain separately labeled.')
    (ROOT/'app/tasks/audited-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'public/data/audited-tasks.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in index.items() if k!='tasks'},indent=2))
    return index

if __name__=='__main__':
    build()
