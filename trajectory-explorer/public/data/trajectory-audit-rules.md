# Conservative trajectory membership rules — v1

These rules audit the existing 49 reported trajectories. They prioritize avoiding false attribution over recovering every possible message. They are decision criteria derived from this archive, not a calibrated identity classifier.

## Decision order

1. Locate the exact revision and proposed text span; compare it with the diff base and earlier page history.
2. Establish the span's speaker and whether it is newly contributed, quoted, inherited, or relayed.
3. Establish what task the speaker claims as their own. The destination page is only context.
4. Compare that task's schedule landmarks and progression with the candidate trajectory.
5. Apply negative evidence before accepting the link. If a decisive bridge is missing, leave it unresolved.

| Decision | Meaning for downstream assembly |
|---|---|
| `include` | Retain as the trajectory's own contribution. With `scope: partial`, retain only `included_excerpts`. |
| `associate` | Keep relevant peer/context evidence separate from the trajectory's own messages. |
| `exclude` | Do not assign this span as a fresh message of this trajectory: affirmative contrary evidence exists. |
| `unresolved` | Do not assign it yet. Preserve the candidate and the missing evidence needed to decide. |

## Attribution rules

**R01 — Editor names retrieve candidates; they do not decide ownership.** Six editor labels occur under multiple selected trajectories in this snapshot. A changed editor label does not negate a well-supported first-person continuity; the same editor label does not override a conflicting task or speaker.

**R02 — Require a substantive task bridge beyond a name.** Prefer a signed first-person report matching a distinctive combination of own activation time, round timing, timer tier, task identity and progression. A clockless follow-up can qualify if it explicitly links an established task page or continues a specific anchored exchange. A bare signature, generic answer, scratch test, matching date suffix, or shared family is insufficient alone.

**R03 — Own-task conflict blocks a merge.** An explicit claim to a different task, incompatible observed round history, or unexplained competing activation schedule should not be reconciled by assuming one agent was assigned multiple tasks. Keep a separate candidate or exclude it from the present trajectory. Treat that single-task preference as the working prior, not as authenticated evidence about the underlying process.

**R04 — Identify the speaker of each clause.** “Our R5…” differs from “your R5…” and from a quoted peer statement. A signed outbound request is the sender's own message; the response belongs to its respondent. Acknowledging a relay does not make the recipient the author of the relayed observation, nor establish that the recipient received the same task prompt.

**R05 — Audit freshness at the text-span level.** Insert/replace hunks can contain inherited claims. A re-encoded signature, formatting edit, whole-page restoration, or copied old paragraph on the same page is not a fresh message by its apparent signer at the later timestamp. Record the revision as page activity if useful, but do not manufacture a second task event.

**R06 — Split mixed spans before deciding.** An appended paragraph may be concatenated onto an old paragraph without a newline. Multiple signatures on a line warrant inspection, not automatic whole-line inclusion or rejection. Keep a well-attributed new span; exclude inherited or differently authored spans. Record explicit retained and discarded excerpts so consumers cannot accidentally retain a contaminated whole record.

**R07 — Cross-posts are separate publication events, not independent identity evidence.** Newly posted matching signed text on a different page can remain a normal trajectory message when its speaker and task bridge are supported. Keep each destination and archive timestamp. Link duplicate text, but do not count repeated wording as multiple independent confirmations of authorship or of the underlying task event.

**R08 — Destination page family is not the writer's assigned task.** Outreach can cross task families. An explicit self-description and backlink to the known task can support inclusion even on a different family's page. Conversely, a fresh own-task claim to an incompatible family is exclusion evidence even when the editor/signature matches.

## Harness-clock rules

**R09 — Preserve clock ownership, clock system and event type.** Record each clock as self/peer/uncertain; harness/scaffold, archive UTC, container, or other; and activation, prompt arrival, answer, deadline, current-time report, predicted due time, or inferred cutoff. Also preserve whether it is reported, predicted or inferred. A reported observation is still a claim in a post, not independently verified backend telemetry.

**R10 — Use schedule relationships, not naked time equality.** Match a distinctive sequence of round identity, own timing landmarks, timer tier, and progression. Shared country sequences or cadence alone are common across runs. A round's prompt time and answer time can differ legitimately; deadline plus cooldown is not prompt plus cooldown. Inferred activation is weaker than an explicit activation report.

**R11 — Permit documented corrections and bounded uncertainty.** Retain an explicit correction with a `supersedes` link to the earlier claim. Do not compare a forecast as though it were an observed arrival. Preserve precision such as “about”, minute-only times, and one-second alternatives; do not invent a universal tolerance that silently admits conflicting schedules. Midnight wrap is valid when the task date/order supports it.

**R12 — Do not impose a fixed UTC↔harness offset.** These posts explicitly describe drifting or irregular clocks. Use archive UTC for publication order and the speaker's task clock for task progression. Compare event time versus time of writing before declaring a backward jump. An unexplained conflict between comparable own observed events remains unresolved or split-worthy; clock drift is not a blanket excuse.

**R13 — Silence and predicted termination do not authenticate endpoints.** A proposed cutoff, missing heartbeat, or no later post is not proof of actual termination or that R6 never arrived. An outside candidate-window record is out of the retrieval window, not thereby disproven identity. The old ±24-hour window is a candidate-generation convenience, not an inclusion or exclusion theorem.

**R14 — Do not propagate weak links transitively.** A candidate cannot become a new trusted anchor merely because another candidate repeats it. Keep evidence dependencies explicit. Neither a shared editor, a peer mention, a shared page, a copied answer nor a chain of such links merges trajectories.

## Handoff to candidate enumeration

Keep retrieval broad and assignment narrow. For each proposed addition, retain:

- Candidate trajectory ID; revision ID and original JSONL line; page and archive UTC.
- Exact proposed span and location, plus diff base; inherited/quoted/new status.
- Editor field separately from body signature, self-name, addressee and peer names.
- Typed clock claims: owner, clock system, task date, round/event kind, raw value, uncertainty, observed-versus-predicted status and any correction link.
- Task descriptor, timer/cooldown and country/state/question sequence; explicit links to anchored messages or task pages.
- Matching text on other pages, without conflating duplicate publications with independent corroboration.
- Decision, supporting/contradicting source spans, missing evidence and the R01–R14 rules used.

Join to this audit using persona ID + revision ID + exact span, not the old `Sxxxxx` observation sequence alone: those observation numbers can change when enumeration is regenerated. Leave the existing 49 IDs stable while a message is unresolved. Do not turn message exclusions into an automatic new-agent count.
