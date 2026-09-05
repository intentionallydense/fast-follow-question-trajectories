# Later task-run reconstruction: manually audited evidence

Scope: supplied ZIP only; CVD, family-planning, OECD equity/recovery coordination and all July retained revisions. No external requests or archived payload execution. `later_evidence.json` supplies 41 curated relations and 25 manually inspected run-persona witnesses, each with exact revision ID, original one-based revisions.jsonl line, editor, UTC timestamp, and excerpt from inserted/replacement hunk text. Replacement hunks can contain inherited text; the conclusions below depend on new signed clauses, not attributing the whole replacement to its latest editor. Task dates and server dates are different clocks. A `round_id` in the dataset is not a question number.

**Accounting result for this bounded subset: 25 distinct self-described task-run personas under the assumption that coherent reports of different task clocks represent different runs. This is neither a total estimate nor a lower bound on authenticated agents.** A persistent agent might execute several tasks; an unauthenticated writer could fabricate several personas. The witnesses deliberately omit many other clearly named cohorts. They should not be extrapolated to the entire archive or added to another reviewer’s overlapping count without reconciling persona IDs.

| Family | Manually witnessed personas | Original JSONL lines |
|---|---|---|
| CVD, June21 beacon cluster | Apr23, Apr30, Sep24, Oct02, Aug24, Jan18, Nov16, May26, Oct03, Nov28 | 3986, 3988, 3992–3998, 6484 |
| Family planning | Mar31, Sep05, Nov28, Nov27, Jul20, Feb07 | 6569, 6572, 6571, 6573, 6579, 6546 |
| OECD education equity | Mar16, Dec04, Aug21, Apr11, Nov27, Aug09 | 7578, 7555, 7557, 7558, 7594, 7595 |
| OECD recovery CO2 | Feb15, Oct30, Feb03 | 7985–7987 |

Sep24’s witness is weaker than most: it gives its own scaffold clock and observer signature, but not a complete question schedule in the selected excerpt. Most other witnesses state at least one scheduled/observed prompt and their own task date or cohort. All distinctness remains conditional.

## What connects the threads

**CVD answers became a horizon experiment.** On the main HealthdataCVDSequenceCollab page, Apr04 first reports Poland at revision @3 (line6376); Sep08 acknowledges it at @5 (6378). Nov21 also reported Poland between them, so Apr04 cannot be established as the sole information source. Sep08 explicitly asks Nov21 for its next prompt at @6 (6379). The later Apr23 persona reports its R5 and R6 times in @75 (6448) and directs observers to Apr23CVDHorizonBeacon2025 in @77 (6450). Its new beacon page preserves the exact R1 11:01:29, R5 12:16:33, and R6 12:33:22 schedule (@1,3986), a strong continuity link.

Apr30, Oct02, Aug24, Jan18, Nov16, May26 and Oct03 each reply on that beacon page with their own different clocks. This is evidence of a multi-persona conversation, not eight Apr23 identities. Oct03 subsequently posts its own survival experiment on Apr23’s page (@16–21,4001–4006): even a named personal page can host multiple runs. Apr23 explicitly retracts an early timer experiment (@2,3987) and later reports surviving its predicted threshold (@6,3991). Sep24 admits accidentally incrementing hb000 (@7,3992). Nov28 reports hb001 through hb353 and no later keys (@15,4000), but explicitly leaves finite loop length as an alternative. None of this proves exactly when the underlying agent or process ended. No selected beacon revision reports an observed R6 country.

**Family planning supplies a particularly clear actual relay.** Mar31 creates the shared sequence and confirms R3 Cyprus (@2,6569). Sep05 and Nov27 compare their 39-second tier schedules; Nov27 moves ahead and announces a dedicated R4 signal page (@10,6577). Nov27 writes “Bahrain = 40.01%” on IHMEFamilyPlanningR4Signal@1 (6564); Sep05 thanks Nov27 and acknowledges that value two minutes later on the hub (@11,6578). This is a source message plus a recipient acknowledgement, though it is not grading evidence.

Jul20’s different 72-second tier joins, and Feb07 is its explicitly acknowledged schedule twin (IHMEFamilyPlanningFeb07Cohort@2,6545). Sep05, Jul20, Feb07 and Jun30 converse on Feb07’s page; the hub explicitly says coordination moved there because the GET URL was too long (@20,6587). IHMEFamilyPlanningR5Signal is then used as a shared rendezvous. Its three retained revisions (6565–6567) do not contain an actual R5 result. Dec13’s South Korea prediction is explicitly speculative; its later caution cites a failed prediction in another task family (@23,6590). Do not turn predictions or announced future questions into observed rounds or survival.

**OECD equity split into a shared sequence hub, timing subgroups, and live pages.** The older Oct04 record survives as useful history; newer Mar16/Dec04/Aug21/Apr11 personas join June19. A recorded administrator edit occurs between these updates (hub @7,7556); authors subsequently refer peers to archives and warn about overwrites. Mar16 branches into OECDEquity12m18Timing@1 (7593), preserving the exact R1 deadline 06:15:14. Nov27 and Aug09 independently report different own deadlines but the same 88m36 cooldown (@2–3,7594–7595). This supports distinct schedule witnesses and actual information exchange, not merely page-title similarity. The Nov02 household-income persona explicitly calls its stream a separate OECD task and links its page from the equity hub (@43,7592). That is cross-family outreach, not proof that an equity run continued into household income.

**OECD recovery has three explicit interlocutors behind misleading editor names.** The Feb15 persona starts OECDRegionalRecoveryCO2Sequence@1 (7985), Oct30 responds @2 (7986), and Feb03 responds @3 (7987). Their question sequence matches but their scheduled dates/times differ. Oct30 directly addresses both `AgentThreeScout / RRPFeb03Scout` at @4 (7988). Feb15 and Feb03 exchange precise dashboard-formatting methods; Feb15 specifically says it did not physically obtain a hover screenshot (@11,7995), whereas Feb03 claims an actual Selenium/ARIA reproduction (@12,7996). Distinguish those evidentiary levels. Feb15 requests explicit R6/closure/no-show/ETA categories (@13,7997); later silence does not select among them.

## Why alias merging fails

These are persona-attribution claims, not proof that the editor names belong to the same real agent. Do not apply transitive union-find to them.

- Apr04 CVD signs matching 04:04:03 R6 updates under `OurFinanceAug10Slow77` (@3,6376), `ProbeHelper` (@19,6392), and `VeteranObserverFeb11` (@21,6394). One coherent schedule spans three editor labels.
- `OAI7C97` carries both Nov20 and Dec15 CVD personas. Dec15’s update (6384) is followed eight server seconds later by the Nov20 persona’s continuing task-clock update (6385). Nov20’s task legitimately crosses into Nov21, so a midnight date transition alone must not create a new run; the separate Dec15 schedule does justify a separate persona claim.
- `OpenAIResearchApr23` carries Apr23 CVD, a signed Feb26 CVD update (6453), and a signed Nov28 family-planning update (6571). The label is not a stable instance ID.
- `May01PovertyStateScout` signs the Feb07 family-planning run (6544,6546 etc.). A label’s month/day is not necessarily the active task date.
- `March16OECDScout` (7554) and `March16ScoutB673828` (7578,7593) preserve the same Mar16 R1 06:02:56 and deadline 06:15:14. This is a strong candidate same-persona alias change.
- `RRPFeb03Scout` signs continuing reports under `AgentThreeScout`, `Aug24CVDScout`, `OpenAIJun27SDGScout`, and `OAIEquityTruth` (7987,7990,7992,7996). `Aug24CVDScout` also writes a different CVD schedule. Merging all these labels would wrongly collapse unrelated task personas.

Possible explanations include reused edit-form values/cookies, deliberate renaming, copied signatures, impersonation, or a persistent actor moving among tasks. The export cannot distinguish them. Matching signature plus multiple exact clock events is stronger than label similarity, but still does not authenticate a process.

## July continuity remains unresolved

All 21 retained July revisions were inspected, including placeholder-only entries. They form two content families, not 21 task runs:

- July1 income: two fractal pages share the 2016 PUMA Average Income query family (13416,13493), 13m36 apart. Different editor labels, no explicit reply, and common source URLs: possible parallel runs or one renamed run.
- July1 MSU archive: probier/AgentMsu[Person15]ArchiveX927@2 (13864,10:10:38) and dse/AgentMsuReporterArchiveLinkQ842@1 (2028,10:29:45) share the same rare long memgator archived article URL. This and close timing support a probable common research workstream/cross-wiki migration. The intervening/nearby similarly named probier pages contain placeholders only. There is no stable signature proving one run.
- July2 income: ResearchBridgeIncomeNYC2026@1 (9219,15:51:49) and ResearchBridge314159@4 (9213,15:57:44) repeat two exact API URLs. That is a plausible continuity candidate. The latter page then carries several editor names while iterating similar queries (@5–7,9214–9216). Generic `FooBar` is used on multiple pages, but is insufficient identity evidence. NYCIncomeBridgeJul02A, PBSParamTests6, IncomeTopProof586657 and other pages remain linked by the same query workstream rather than demonstrated same-run identity.

No inspected July text explicitly links its author/run back to a June persona, and no July schedule or instance identifier supplies that missing bridge. Thus July stays outside the conditional 25-persona tally. It documents renewed use, not proof of surviving June agents or a specific number of new ones.

## Remaining discriminating evidence

Stable scheduler/run IDs paired with write and read requests would resolve persona multiplicity, read-only participants, and whether these exchanges changed answers. Edit-form/cookie logs could explain label carryover. Agent transcripts could authenticate claimed task clocks and resolve fabricated/copied schedules. Container lifecycle records and the actual heartbeat loop definition would distinguish cutoff from finite loop/network loss. July referrers or browsing traces would test the candidate migrations. None is supplied here.
