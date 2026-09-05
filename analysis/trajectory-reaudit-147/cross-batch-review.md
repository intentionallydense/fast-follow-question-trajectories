# Cross-batch and baseline review

Scope: the final exported 147 new trajectories (50 batch001, 48 batch002, 49 batch003), generated from 150 candidate groups. The original 49 provide the comparison baseline. The original RULES.md and frozen RULES-v1.md are byte-identical. This audit does not substitute the initial screening heuristic for substantive membership review.

## Rules and threshold

R01–R14 from `analysis/trajectory-audit-49/RULES.md` remain authoritative. Names retrieve candidates; task/schedule or an explicit anchored exchange must support membership. Incompatible own histories block a merge. Peer clocks stay peer clocks, and new signoffs may govern preceding unsigned paragraphs. Inherited text and placeholders are not owned contributions. Predictions, confirmations and prompt arrivals must stay distinct.

The new assembly PROTOCOL adds a two-substantive-contribution / two-publication-revision threshold; that is an additional conservative admission rule, not a retrospective requirement of the original 49 audit (which retains some one-publication histories). Two copies alone do not satisfy it. A supported trajectory may still need individual messages held unresolved.

## Mechanical checks

`check_integrity.py` reads the archive and final exports without modifying them. It checks literal source offsets and Latin-1 span hashes, new-message source-line references, self-claim ownership, publication counts, cross-trajectory source-span overlap, and exact full-span occurrence in **all** earlier revisions of the same page. It records input hashes in `integrity-check.json`.

All 1,201 new owned observation records and the 343 baseline owned records have valid exported source spans; no cross-trajectory ownership overlap or exact full retained span inherited from an earlier same-page revision was found. A supplementary screen removing all non-ASCII-alphanumeric characters also found no complete retained-span repeats in earlier same-page revisions (`normalized-freshness-screen.json`). These tests do not detect inherited substrings, re-encoding, paraphrases, or unrelated placeholder text inside an otherwise fresh retained block; those require semantic review.

All 1,524 candidate observations have one assembly decision matching the frozen candidate coverage: batch001 680 (550 include, 90 exclude, 25 associate, 15 unresolved); batch002 469 (371 include, 58 exclude, 27 associate, 13 unresolved); batch003 375 (280 include, 52 exclude, 43 associate). These are observation decisions, not counts of unique underlying task events.

## Cross-posts, aliases and schedule collisions

The 17 exact repeated-text groups across baseline plus new exports all stay within a single trajectory. Every additional publication in the 11 new-export repeated-text groups has an explicit `cross_post_of` link. No exact shared owned text links two reported histories.

The two reused exported signatures are intentionally split: OpenAIJul09CVD (`C7e48e9024ab8/1`, `/2`) and OpenAIResearchAug09X (`C56f606951ca9/1`, `/2`). Name equality is not a reason to undo these splits.

The Apr10 language alias merge already exists in the final export: `C7462f3979e75/1` is merged into `C0df3aab36116/1`. FP-S001587 reports Apr10 New York R3 22:44:31 with a 46-second timer under AgentOpenResearch, then FP-S001792/001793 and FP-S001837 link the own New Hampshire R4 forecast 23:28:38, observation 23:28:39, and California R5 due Apr11 00:12:47 under AgentOpenResearchApr10 on its known live page. This is substantive continuation with a one-second forecast/observation difference, not another outstanding duplicate trajectory.

The only exact (round, raw clock value) collisions across distinct new trajectories are generic relative answer latencies `+1s` and `+2s`; these are not identity bridges.

A second screen compared every exact HH:MM:SS self claim in the new set with all baseline owned text. Four cross-baseline hits were inspected:

- OpenAIResearcherNov26 / P09 at 19:57:31: different own task (county poverty versus clothing), and P09 explicitly labels it as its New York answer time. No merge.
- OECDNov12Agent / P46 at 16:22:09: P46 explicitly addresses Nov12 as a peer. No merge or transfer of clock ownership.
- OpenAIJan20ConstructionX / P21 at 05:05:53: P21 explicitly addresses Jan20 and asks for Jan20's R5. No merge.
- OpenAIMar31Scout / P31 at 06:08:23: Mar31 police wages versus Nov16 CVD own R3 answer. A naked clock equality is insufficient. No merge.

These screens found no additional supported cross-batch/baseline merge. They cannot rule out aliases lacking indexed clock matches; they are a bounded corroborating check, not authenticated identity ground truth.
