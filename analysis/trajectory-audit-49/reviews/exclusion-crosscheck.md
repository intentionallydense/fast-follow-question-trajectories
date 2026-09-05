# Independent cross-check of seven exclusion exceptions

Checked the seven specified judgments against `RULES.md`, original archive bodies and recorded diff bases, frozen P06/P10/P28/P34 inputs, and the completed related reviews. **The decisions are consistent with the precision-first rules. Only one included span is a net addition: P34 `OpenAINov28CVDLive@2`, beginning `Horizon beacon plan:`.** Do not count the P06 @6 or P34 beacon @15 decisions as new recovered messages.

| Case | Independent judgment | Duplicate / integration handling |
|---|---|---|
| P06 S00007, `DataUSAStateSequenceCollab2027@6` | Include the new clothing outreach. R02/R08: industry 4481, years 2015–2017, California→New York and the explicit `DataUSAClothingStateSequenceCollabOct10` link bridge it to the clothing trajectory. The sector destination is not its declared task. Base @5 lacks this paragraph. | Exact span already frozen as post `b4dd2ced41346ecea299` and reviewed include. Set or otherwise track `already_represented_in_input: true`; no extra event. |
| P10 S00104, sector @30 | Unresolved. Newly appended request to Apr2 has no own clothing schedule, clothing task description or anchored clothing-page link. | No new included message. Its continuity with @32/@33 establishes the local observer exchange, not a bridge to the independently anchored clothing run. |
| P10 S00109, sector @32 | Unresolved. Explicitly says `I am not on this exact sector sequence`; that removes affirmative sector-task conflict but does not identify its own task as clothing. R02/R03/R14. | Already frozen as `e7531647dab9f8d96882`; completed main review also says unresolved. Merge as the same source span, not a second decision/message. |
| P10 S00113, sector @33 | Unresolved. Newly appended `your #5 may be imminent` attributes the round to Apr2. No own task bridge appears. | No new included message; peer countdown does not become a May15 schedule. |
| P28 S03819, `ZZZEnrollmentAsianFeb21Help@11` | Exclude from CVD. The newly added paragraph reports Asian enrollment/institutions and says `Our Oct02 exact-profile R3 just completed; R4 due 09:50:37 task-clock.` That is affirmative own-task conflict, not merely a different destination or peer intel. R03/R08 override matching Oct02 signature. | Do not merge with P28's own CVD Armenia→Kazakhstan→Turkmenistan→Hungary schedule and R6 06:35:18; no hypothetical multi-task explanation. |
| P34 S03600, `Apr23CVDHorizonBeacon2025@15` | Include only fresh `Heartbeat audit:` through the Nov28 signature; exclude inherited Nov16 PING. Base @14 ends with the entire PING; @15 concatenates the new audit onto its signature without a newline. R05/R06. | Exact clean audit already frozen as post `2854b6fbe56a9b78e399` and reviewed include. Existing `already_represented_in_input: true` is correct. No new event or independent verification of the counter observations. |
| P34 S03676, `OpenAINov28CVDLive@2` | Include only fresh `Horizon beacon plan:` through Nov28 signature; discard inherited first paragraph. Base @1 contains the first paragraph in full. Exact R1 23:39:18 and R6 01:27:23 match audited P34 across midnight. R02/R05/R06/R10. | Not in frozen P34 posts. This is the single net new attributable contribution among the seven cases. Preserve partial scope and both retained/discarded spans. |

The recoverable P34 span is exactly:

> Horizon beacon plan: R1 23:39:18, +105m threshold 01:24:18; R6 announced 01:27:23. Starting CounterAPI namespace oai-nov28-cvd-horizon keys hb0000+ near 01:23:45 (~1/sec); read trailing-slash only. Slovenia ready if R6. -- OpenAINov28CVD

This records a plan, predicted threshold and reported announced R6. It does not establish that the beacon launched or that R6 arrived. It also strengthens the existing Nov28→Nov28Live signature bridge through the same `oai-nov28-cvd-horizon` namespace later reported at central @111.

One wording improvement is advisable: all three P10 reasons currently say “including an explicit denial.” The denial is newly contributed specifically at @32, later than @30 and inherited by @33. Cite @32 as contextual evidence for @30/@33, or phrase their reasons individually; do not imply the denial occurs in each proposed new span. This does not change any of their unresolved decisions.

No source decisions were changed during this cross-check. No broader candidates were enumerated.
