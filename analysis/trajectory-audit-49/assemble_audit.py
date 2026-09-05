"""Validate and assemble conservative reviews; never modifies explorer/enumeration data."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
inputs = {p.stem: json.loads(p.read_text()) for p in sorted((ROOT / 'input').glob('P*.json'))}
manifest = json.loads((ROOT / 'input/snapshot-manifest.json').read_text())
assert all(hashlib.sha256((ROOT / 'input' / name).read_bytes()).hexdigest() == digest for name, digest in manifest.items())
with zipfile.ZipFile(PROJECT / 'full-wiki-logs.zip') as archive:
    revisions = {r['rev_id']: (i, r) for i, r in enumerate(map(json.loads, archive.read('revisions.jsonl').splitlines()), 1)}
    assert all(hashlib.sha256(archive.read(name)).hexdigest() == digest for digest, name in
               (line.split() for line in archive.read('SHA256SUMS').decode().splitlines()))
reviews = []
for path in sorted((ROOT / 'reviews').glob('*.json')):
    part = json.loads(path.read_text())
    assert isinstance(part, list), path
    reviews.extend(part)
assert len(reviews) == 49 and {r['persona_id'] for r in reviews} == set(inputs), 'Need exactly one review for each of the 49'
reviews.sort(key=lambda r: r['persona_id'])
rule_ids = {
    'fresh_delta': ['R05'], 'new_text_verified': ['R05'],
    'task_continuity': ['R02', 'R10'], 'task_stage_continuity': ['R02', 'R10'],
    'peer_author_separate': ['R04'], 'clock_owner': ['R09'],
    'insufficient_self_bridge': ['R02'], 'precision_first': ['R02'],
    'inherited_signature': ['R05'], 'formatting_not_fresh_post': ['R05'],
    'first_person_scope': ['R04'], 'clock_owner_separate': ['R04', 'R09'],
    'signature_insufficient': ['R02'], 'answer_only_no_run_landmark': ['R02'],
    'inherited_prefix_not_new_author': ['R05', 'R06'],
    'cross_post_schedule_bridge': ['R02', 'R07'], 'alias_exact_schedule_bridge': ['R02', 'R10'],
    'editor_not_owner': ['R01'], 'encoding_not_authorship': ['R05'],
    'speaker_recipient_separation': ['R04'], 'inherited_content_trim': ['R05', 'R06'],
    'unsigned_anchor': ['R02'], 'insufficient_identity_bridge': ['R02'],
    'peer_clocks_not_self': ['R09'], 'claims_not_verified_outcomes': ['R13'],
    'multiple_speakers_in_delta': ['R04', 'R06'],
    'crosspost_with_bridge': ['R02', 'R07', 'R08'], 'explicit_correction': ['R11'],
    'midnight_rollover': ['R11'], 'prediction_not_observation': ['R09', 'R11'],
    'reported_not_verified': ['R13'], 'signature_context': ['R02'],
}
flat = []
for review in reviews:
    pid = review['persona_id']
    source = inputs[pid]
    posts = {p['id']: p for p in source['posts']}
    messages = review['messages']
    assert len(messages) == len(posts) and {m['post_id'] for m in messages} == set(posts), pid
    assert review['trajectory_verdict'] in ('supported', 'provisional', 'split_required'), pid
    for fingerprint in review['schedule_fingerprint']:
        assert fingerprint['owner'] in ('self', 'peer', 'uncertain')
        assert fingerprint['status'] in ('reported', 'predicted', 'inferred')
        assert fingerprint['excerpt'] in revisions[fingerprint['revision_id']][1]['body'], (pid, fingerprint)
    for message in messages:
        post = posts[message['post_id']]
        assert message['revision_id'] == post['revision_id'], (pid, message)
        assert message['decision'] in ('include', 'associate', 'exclude', 'unresolved')
        assert message['evidence'] and message['reason'] and message['rule_tags'], (pid, message)
        assert all(tag in rule_ids for tag in message['rule_tags']), message['rule_tags']
        message['rule_ids'] = sorted({rid for tag in message['rule_tags'] for rid in rule_ids[tag]})
        for evidence in message['evidence']:
            line, revision = revisions[evidence['revision_id']]
            assert evidence['excerpt'] and evidence['excerpt'] in revision['body'], (pid, evidence)
            evidence['source_line'] = line
        if message.get('scope') == 'partial':
            assert message.get('included_excerpts') and message.get('excluded_excerpts'), (pid, message)
            for excerpt in message['included_excerpts'] + message['excluded_excerpts']:
                assert excerpt in revisions[post['revision_id']][1]['body'], (pid, excerpt)
        message.update(original_level=post['level'], original_own=post['own'], source_line=post['source_line'],
                       page_id=post['page_id'], utc=post['utc'], editor=post['editor'])
        flat.append(dict(persona_id=pid, name=source['name'], post_id=post['id'], revision_id=post['revision_id'],
                         source_line=post['source_line'], utc=post['utc'], original_level=post['level'],
                         original_own=post['own'], decision=message['decision'], scope=message.get('scope', 'whole'),
                         reason=message['reason'], rule_tags=';'.join(message['rule_tags']), rule_ids=';'.join(message['rule_ids'])))
    review['name'] = source['name']
    review['family'] = source['family']
    review['decision_counts'] = dict(collections.Counter(m['decision'] for m in messages))
counts = collections.Counter(m['decision'] for m in flat)
summary = dict(trajectories=49, input_records=len(flat), originally_owned=sum(m['original_own'] for m in flat),
               originally_peer=sum(not m['original_own'] for m in flat), decision_counts=dict(counts),
               trajectory_verdicts=dict(collections.Counter(r['trajectory_verdict'] for r in reviews)),
               partial_records=sum(m['scope'] == 'partial' for m in flat),
               owned_record_decisions=dict(collections.Counter(m['decision'] for m in flat if m['original_own'])),
               original_reviewed_decisions=dict(collections.Counter(m['decision'] for m in flat if m['original_level'] in ('anchor', 'reviewed'))),
               source_zip_sha256=hashlib.sha256((PROJECT / 'full-wiki-logs.zip').read_bytes()).hexdigest(),
               validation='Complete 49/49 coverage; one decision per snapshot record; exact-source evidence; input hashes unchanged; archive file checksums passed',
               scope='Existing snapshot only. No general candidate enumeration and no changes to the live explorer.')
excluded = json.loads((ROOT / 'excluded-observation-decisions.json').read_text())
expected = {(pid, e['observation_id']) for pid, p in inputs.items() for e in p['excluded_candidates']}
assert len(excluded) == len(expected) and {(e['persona_id'], e['observation_id']) for e in excluded} == expected
for observation in excluded:
    for evidence in observation['evidence']:
        assert evidence['excerpt'] in revisions[evidence['revision_id']][1]['body']
    if observation.get('scope') == 'partial':
        for excerpt in observation['included_excerpts'] + observation['excluded_excerpts']:
            assert excerpt in revisions[observation['revision_id']][1]['body']
summary['excluded_observations_audited'] = len(excluded)
summary['excluded_observation_decisions'] = dict(collections.Counter(e['decision'] for e in excluded))
summary['net_new_recoverable_spans'] = sum(e['decision'] == 'include' and not e.get('already_represented_in_input') for e in excluded)
for name, value in [('audited-trajectories.json', reviews), ('audit-summary.json', summary)]:
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
with (ROOT / 'message-decisions.csv').open('w', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(flat[0])); writer.writeheader(); writer.writerows(flat)
print(json.dumps(summary, indent=2))
