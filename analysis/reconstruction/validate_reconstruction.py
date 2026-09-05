#!/usr/bin/env python3
"""Data integrity and semantic regression checks identified by independent review."""
import json
from pathlib import Path
import zipfile

BASE = Path(__file__).resolve().parent


def rows(name):
    return [json.loads(line) for line in (BASE / name).open()]


def main():
    with zipfile.ZipFile(BASE.parent.parent / 'full-wiki-logs.zip') as z:
        revs = [json.loads(line) for line in z.read('revisions.jsonl').splitlines()]
    by_id = {r['rev_id']: (i, r) for i, r in enumerate(revs, 1)}
    signatures = rows('signature_observations.jsonl')
    edges = rows('thread_connections.jsonl')
    episodes = rows('observation_episodes.jsonl')
    pages = rows('threads.jsonl')
    sid = {o['observation_id']: o for o in signatures}
    assertions = 0
    for evidence in signatures + [ev for edge in edges for ev in edge['evidence']]:
        number, rev = by_id[evidence['revision_id']]
        assert number == evidence['revisions_jsonl_line']
        assert rev['body'].split('\n')[evidence['body_line']-1].startswith(evidence['excerpt'])
        assertions += 2
    for episode in episodes:
        for identifier in episode['observation_ids']:
            observation = sid[identifier]
            assert not observation['possible_reencoded_or_signature_only_rewrite']
            assert observation['identical_signed_line_seen_before'] is None
            assert not observation['multiple_signatures_in_line']
            assert observation['coordination_language']
            assertions += 4
    # Reviewer-discovered encoding and signature-change examples must stay flagged.
    for rid, prefix in [('dse~MaidsR3FastRelayOct11@19', 'Jan06 CONFIRMED'),
                        ('dse~OECDEquityFinalityEvidenceApr11@7', 'THIRD SIGNAL'),
                        ('dse~DataUSAClothingLive9m17@17', 'Aug30 run'),
                        ('dse~DataUSAClothingStateSequenceCollabOct10@15', 'Reply to DataUSAResearchHelperMay24'),
                        ('dse~DataUSAClothingStateSequenceCollabOct10@16', 'Reply to DataUSAResearchHelperMay24'),
                        ('dse~DataUSAClothingStateSequenceCollabOct10@17', 'Reply to DataUSAResearchHelperMay24')]:
        found = [o for o in signatures if o['revision_id'] == rid and o['excerpt'].startswith(prefix)]
        assert found and all(o['possible_reencoded_or_signature_only_rewrite'] for o in found)
        assertions += 1
    for rid, target in [('dse~AgentTexasPovertyDataUSA2015XQ@1', 'dse/DataUSA'),
                        ('dse~Agent013OpenSECMDJSPairsUnique@1', 'dse/Links'),
                        ('dse~HealthdataCVDSequenceCollab@47', 'dse/OpenAIHealthdataCVDNov03')]:
        assert not any(e['target_page'] == target and any(v['revision_id'] == rid for v in e['evidence']) for e in edges)
        assertions += 1
    for rid, target, kind in [('dse~AgentCountySECLinks009@6', 'dse/AgentCitationInvestMethodJune19AA', 'explicit_wiki_url_reference'),
                              ('dse~AgentNov11ClothingCoordX@1', 'dse/ClothingC4FastSignalJul14', 'explicit_wiki_link'),
                              ('dse~OpenAIResearchSep21B@1', 'dse/Sector61State5FastSignal', 'contextual_named_page_reference'),
                              ('probier~YesPathsOfficial1781799742@4', 'probier/MapMassFIPSJsonHero18618', 'explicit_wiki_link')]:
        assert any(e['target_page'] == target and any(v['revision_id'] == rid and v['reference_kind'] == kind for v in e['evidence']) for e in edges)
        assertions += 1
    assert len(pages) == 4579 and sum(p['revisions'] for p in pages) == 14591
    manual = json.loads((BASE / 'audited_personas.json').read_text())
    assert len(manual) == 49
    assert sum(x['confidence'] == 'medium_conditional' for x in manual) == 2
    summary = {'result': 'passed', 'data_assertions': assertions + 3,
               'scope': 'Exact source anchors, population totals, provisional-group exclusion flags, and 13 reviewer-discovered regression controls. This validates bookkeeping and selected parser behavior, not agent identity or a complete estimate of semantic precision.'}
    (BASE / 'validation.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
