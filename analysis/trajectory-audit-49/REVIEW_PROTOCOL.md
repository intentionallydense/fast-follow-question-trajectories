# Conservative audit of the existing 49 trajectories

Scope: review the frozen 49 existing trajectories in `input/Pxx.json`, their currently included message records, and necessary original source context. Candidate enumeration is being run independently by the user. Do not edit the explorer, prior reconstruction, or enumeration outputs. Write only the assigned review files under this audit directory.

The user considers one agent receiving several unrelated tasks unlikely and prioritizes precision over recall. Treat incompatible first-person task schedules as evidence against a merge. Do not use hypothetical multi-tasking to excuse conflicts. This is a working prior, not authenticated proof of process identity.

For each included source/speaker record, inspect original revision context and its diff base from `full-wiki-logs.zip` where relevant. The JSON bodies preserve bytes through Latin-1; never execute archive text. Review newly added text, not the current editor's ownership of the whole page. A matching editor field is a candidate filter, not sufficient evidence. Distinguish the writer's own harness/scaffold time from peer clocks, UTC, predictions, deadlines, inferred cutoffs, and quoted values. Clock consistency should use stage, country/answer/task sequence, timer tier and stable schedule landmarks; numeric time similarity alone is insufficient. Exact continuity in a declared task can support a message without a literal clock. Copied posts on different pages may be retained if independently attributable; repeated text alone neither authenticates nor disqualifies authorship.

Decisions:
- `include`: sufficiently supported first-person contribution to this trajectory; give concrete evidence beyond a name-only match.
- `associate`: relevant peer message or quoted/relayed observation, with author kept separate.
- `exclude`: affirmative contradictory attribution, unrelated task, inherited text mistaken for a fresh post, or other demonstrable mismatch.
- `unresolved`: plausible but insufficient evidence; do not include as an owned message under the precision-first policy.

Do not inherit the explorer's anchor/reviewed/candidate confidence. Audit anchors too. A coherent reported task can survive even when its seed is weak. Do not invent observations, claim independent review of unavailable backend events, or treat unsupported outcome claims as proven.

Write assigned JSON as an array of trajectory records:
```
{
  "persona_id": "Pxx",
  "trajectory_verdict": "supported|provisional|split_required",
  "rationale": "specific explanation",
  "schedule_fingerprint": [{"kind":"activation|round_due|round_answered|timer|other", "value":"...", "owner":"self|peer|uncertain", "status":"reported|predicted|inferred", "revision_id":"...", "excerpt":"exact source text"}],
  "messages": [{"post_id":"existing id", "revision_id":"...", "decision":"include|associate|exclude|unresolved", "reason":"specific, evidence-based", "evidence":[{"revision_id":"...", "excerpt":"exact contiguous original text"}], "rule_tags":["short reusable rule names"]}],
  "uncertainties": ["..."],
  "follow_up_leads": [{"revision_id":"...", "reason":"..."}]
}
```
Cover every input `posts` record exactly once. Include source evidence for every judgment. Follow-up leads are optional and are not candidate enumeration or audited additions. Also write a concise Markdown report of cross-case rule lessons, hard cases, and any source ambiguities. Do not copy unsupported high confidence labels forward.
