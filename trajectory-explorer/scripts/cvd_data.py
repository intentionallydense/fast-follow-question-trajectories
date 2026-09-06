"""Load the reviewed CVD add-on without changing earlier audit decisions."""
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path

CVD = Path(__file__).resolve().parents[1] / 'research/cvd-accounting'

@lru_cache(maxsize=1)
def gate():
    if not CVD.exists():
        return None
    review=json.loads((CVD/'review-gate.json').read_text())
    assert review['status']=='passed'
    for name,sha in review['accepted_sha256'].items():
        assert hashlib.sha256((CVD/name).read_bytes()).hexdigest()==sha, name
    return review

def cvd_data(name):
    return json.loads((CVD/name).read_text()) if gate() else []

def with_cvd_extensions(dossier):
    result=copy.deepcopy(dossier)
    additions=[m for m in cvd_data('extensions.json') if m['trajectory_id']==result['trajectory_id']]
    result['owned_messages']+=additions
    return result
