"""Apply the audited 49's corrections in a separate assembly, leaving all inputs intact."""
import hashlib
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
AUDIT = ROOT / 'analysis/trajectory-audit-49'


def span(body, excerpt):
    start = body.index(excerpt)
    return dict(text=excerpt, start_char=start, end_char=start + len(excerpt),
                body_line=body.count('\n', 0, start) + 1,
                text_sha256=hashlib.sha256(excerpt.encode('latin1')).hexdigest(),
                occurrence_count=body.count(excerpt))


def spans(body, excerpt):
    if excerpt in body:
        return [span(body, excerpt)]
    # The legacy explorer joins noncontiguous paragraphs with a blank line.
    # Keep the original source spans separately, never invent a contiguous span.
    parts = [x for x in excerpt.split('\n\n') if x]
    assert len(parts) > 1 and all(x in body for x in parts)
    return [span(body, x) for x in parts]


def main():
    with zipfile.ZipFile(ROOT / 'full-wiki-logs.zip') as z:
        raw = {r['rev_id']: (i, r) for i, r in enumerate(map(json.loads, z.read('revisions.jsonl').splitlines()), 1)}
    audit = json.loads((AUDIT / 'audited-trajectories.json').read_text())
    changes = json.loads((AUDIT / 'proposed-message-changes.json').read_text())['actions']
    result = []
    for t in audit:
        source = json.loads((AUDIT / 'input' / (t['persona_id'] + '.json')).read_text())
        posts = {p['id']: p for p in source['posts']}
        assembled = dict(trajectory_id=t['persona_id'], status=t['trajectory_verdict'],
                         display_name=t['name'] if t['persona_id'] != 'P43' else 'Unsigned Aug21 OECD schedule (provisional)',
                         legacy_display_name=t['name'], task_family=t['family'], owned_messages=[],
                         associated_messages=[], unassigned=[], excluded=[], schedule_evidence=t['schedule_fingerprint'],
                         uncertainties=t['uncertainties'], evidence_origin='49-trajectory audit; no new identity inference')
        for m in t['messages']:
            post = posts[m['post_id']]
            line, r = raw[m['revision_id']]
            excerpts = m['included_excerpts'] if m.get('scope') == 'partial' else post['excerpts']
            record = dict(record_id=m['post_id'], revision_id=m['revision_id'], source_line=line, page_id=r['page_id'],
                          utc=r['time'], editor=r['label'], speaker_reference=post['author_id'], decision=m['decision'],
                          spans=[s for x in excerpts for s in spans(r['body'], x)], reason=m['reason'], rule_ids=m['rule_ids'],
                          diff_base=r['diff_base'], audit_scope=m.get('scope', 'whole'))
            bucket = {'include': 'owned_messages', 'associate': 'associated_messages', 'exclude': 'excluded', 'unresolved': 'unassigned'}[m['decision']]
            assembled[bucket].append(record)
        for change in changes:
            if change['persona_id'] == t['persona_id'] and change['action'] == 'recover_new_span':
                line, r = raw[change['revision_id']]
                assembled['owned_messages'].append(dict(record_id='audit-recovery-' + t['persona_id'], revision_id=r['rev_id'],
                    source_line=line, page_id=r['page_id'], utc=r['time'], editor=r['label'], speaker_reference=t['persona_id'],
                    decision='include', spans=[span(r['body'], x) for x in change['included_excerpts']], reason=change['reason'],
                    rule_ids=['R02', 'R05', 'R06'], diff_base=r['diff_base'], audit_scope='partial_recovery'))
        assembled['owned_messages'].sort(key=lambda r: (r['utc'], r['revision_id']))
        result.append(assembled)
    folder = OUT / 'baseline'
    folder.mkdir(exist_ok=True)
    (folder / 'audited49.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    counts = {key: sum(len(t[key]) for t in result) for key in ['owned_messages', 'associated_messages', 'unassigned', 'excluded']}
    assert counts == dict(owned_messages=343, associated_messages=27, unassigned=6, excluded=1)
    (folder / 'summary.json').write_text(json.dumps(dict(trajectories=49, supported=48, provisional=1, **counts,
        corrections_applied=len(changes), source='Frozen audit input plus accepted P34 recovery; live explorer unchanged'), indent=2) + '\n')
    print(counts)


if __name__ == '__main__':
    main()
