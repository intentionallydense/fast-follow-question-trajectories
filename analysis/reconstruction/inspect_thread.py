#!/usr/bin/env python3
"""Print the reconstructed connections for an exact wiki/page ID or name query."""
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read_jsonl(name):
    return [json.loads(line) for line in (BASE / name).open()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', help='Exact wiki/page ID, or case-insensitive substring')
    args = parser.parse_args()
    pages = read_jsonl('threads.jsonl')
    selected = [p for p in pages if p['page_id'] == args.query]
    if not selected:
        selected = [p for p in pages if args.query.casefold() in p['page_id'].casefold()]
    if len(selected) != 1:
        print(f'{len(selected)} matching pages; pass an exact page ID:')
        for p in selected:
            print(p['page_id'])
        return
    page = selected[0]
    pid = page['page_id']
    refs = read_jsonl('thread_connections.jsonl')
    episodes = [e for e in read_jsonl('observation_episodes.jsonl') if pid in e['pages']]
    audited = [p for p in json.loads((BASE / 'audited_personas.json').read_text()) if pid in p['pages']]
    print(f'# {pid}\n')
    print(f"Publisher page family: {page['publisher_family']}; {page['revisions']} retained revisions.")
    print(f"Archive interval: {page['first_time']} to {page['last_time']}.")
    print('Editor labels: ' + ', '.join(page['editor_labels']))
    print('Extracted signature tokens: ' + ', '.join(page['observed_signatures']))
    print('\nUncertainty: ' + '; '.join(page['uncertainty_flags']))
    print('\n## Documented page references\n')
    for edge in refs:
        if pid not in (edge['source_page'], edge['target_page']):
            continue
        print(f"{edge['edge_id']}: {edge['source_page']} -> {edge['target_page']}")
        for e in edge['evidence']:
            print(f"  {e['reference_kind']}; {e['revision_id']}, revisions.jsonl:{e['revisions_jsonl_line']}, body:{e['body_line']}")
            print('  ' + e['excerpt'].replace('\n', ' '))
    print('\n## Selected manually audited personas\n')
    for p in audited:
        print(f"{p['persona_id']}: {p['reported_persona']} ({p['confidence']})")
    print('\n## Provisional textual observation blocks (not independent agents)\n')
    for e in episodes:
        print(f"{e['episode_id']}: {e['signature']}, {e['first_time']} to {e['last_time']}; context {e['publisher_page_family']}")


if __name__ == '__main__':
    main()
