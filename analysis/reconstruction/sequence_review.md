# Hand-audited DataUSA thread reconstruction

Scope: four rich task families on June 16–17, plus the grocery result relay. This is a bounded qualitative audit, not an exhaustive census. `sequence_evidence.json` contains 57 exact source records with original JSONL line numbers, revision IDs, newly added/replaced excerpts, persona, editor label, relation type, confidence, and uncertainty. No external endpoints were contacted.

**Result: 24 selected, distinguishable run personas are documented below.** They are a reproducible witness set of self-reported task trajectories, conditional on the reports being truthful. They are **not 24 authenticated independent processes** and are not a global minimum agent count. A single process could manage several task threads, restart, or fabricate personas. This selection also excludes many additional plausible trajectories. Do not add its count to another review's count without resolving overlap.

Method: inspect revision hunks and preceding page content, focus on newly authored first-person clauses, preserve editor label separately from body signature, and use task family, initial clock, cadence, and explicit peer replies together. Replacement hunks can still contain inherited or re-encoded paragraphs; e.g. the Jan12 wording reply reappears under multiple clothing editors and must not generate identity links to those editors. Compacted active-schedule lists similarly report peers, not the compactor's identity.

## The 24 selected trajectories

References abbreviate `dse~PAGE@REV`; full page names are in the left column. Clocks below are reported task clocks, not archive UTC. When source only supplies an expected time, it is labelled due.

| Task / run persona | Distinguishing clock and cadence | Primary first-person evidence |
|---|---|---|
| Sector / ParallelSectorAgentApr2 | WV 23:22:44, 13s; #5 due 23:49:04 | DataUSAStateSequenceCollab2027@14, @29 |
| Sector / SectorAgentJun20X | WV 02:20:04, 13s; #5 due 02:46:24 | same @13, @20, @26 |
| Sector / SectorAgentJun15 | WV 18:12:11, 13s; #5 due 18:38:31 | same @15, @21 |
| Sector / AgentResearchMay24 | CT 08:01:50, 10s; MI due 08:17:44 | same @35, @54 |
| Sector / SectorAgentMay24OAI | MA 19:37:32; CT 20:05:38, 13s | same @36, @73, @95 |
| Clothing / ClothingSequenceScout | CA 10:56:58; NY 11:25:37, 15s | DataUSAClothingStateSequenceCollabOct10@1, @3 |
| Clothing / ResearchAgentOpenAIJan12 | CA 17:43:09; NY 19:43:51, 63s | same @8; DataUSAClothingLive9m17@7 |
| Clothing / OpenAIResearcherAug08 | CA 21:17:09; NY 23:17:51, 63s | same @9; DataUSAClothingLive9m17@1 |
| Clothing / DataUSAResearchHelperMay24 | CA 17:56:48; NY 19:57:30, 63s | same @10; DataUSAClothingLive9m17@4 |
| Clothing / DataResearchMay15 | CA 20:06:36; NY 22:07:18, 63s | same @13; DataUSAClothingLive9m17@8–9 |
| Clothing / ResearchAgentJan29 | CA inferred 12:31:37; NY 13:27:29, 47s | same @11; DataUSAClothingLive9m17@5 |
| Grocery / GrocerySequenceAgentApr27 | GA 05:51:18, 2m19; AR 06:28:33; NV 07:03:47, 17s | DataUSAGrocerySequenceCollab2027@1, @4 |
| Grocery / GroceryAgentMar13X | GA 02:59:23, 2m19; AR 03:36:38; KY 04:47:06, 17s | same @5, @14 |
| Grocery / GrocerySequenceHelperAug14 | GA 04:06:30, 2m19; NV 05:18:59, 17s | same @12 |
| Grocery / AgentProbeAssistantX2027 | GA 15:17:34, 9m19; AR 15:55:55; NV 16:25:29, 30s | same @2, @7, @15 |
| Grocery / GroceryWatcherJan31X | GA deadline 22:34:42; AR 23:03:44, 30s | same @9, @11 |
| Construction NY / ConstructionAgentMar08 | NY 15:39:19, 10m; CA 16:19:51, 42s; TX 16:51:06 | DataUSAConstructionSequenceMar08@1, @29, @47 |
| Construction NY / Nov09ConstructionAgent | NY 11:23:15, 10m; CA 12:03:47, 42s; TX 12:35:02 | same @2, @18, @34 |
| Construction NY / ConstructionAgentJun29 | NY 21:52:08, 10m; CA 22:32:40, 42s | same @4, @11, @39 |
| Construction NY / AgentConstructionNYCATXFL20270603 | NY 14:22:34, 5m39; CA 14:36:47; TX 14:45:33; FL 14:54:19, 11s | same @9 |
| Construction NY / Nov08ConstructionAgent | NY 12:50:17, 10m; CA 13:30:49, 42s | same @10, @42 |
| Construction NY / ChatGPTAug11 | NY 01:12:18, 10m; CA 01:52:50; TX 02:24:05; FL 02:55:20, 42s | same @13, @25, @28, @32, @35 |
| Construction NY / Dec30ConstructionAgent | NY 12:45:22, 6m40; CA 13:20:50; TX 13:49:54, 14s | same @8, @20, @48 |
| Construction NY / Apr02ConstructionAgent | NY 12:58:17, 6m40; CA 13:33:45; TX 14:02:49, 14s | same @15, @26, @53 |

The strongest within-family distinct-run witnesses are reciprocal replies plus different clocks, especially Apr2 ↔ Jun20 ↔ Jun15, Apr27 ↔ Mar13, AgentProbe ↔ Jan31, and Mar08 ↔ Jun29 ↔ Nov09 ↔ Aug11. Their independence is inferential, not authenticated. The two sector May24 names must remain separate: their simultaneous reports give different initial clocks and follow-up tiers. Conversely, matching dates or timing tiers are not enough to merge.

## How the threads connect

**Sector → clothing discovery bridge.** ClothingSequenceScout creates the clothing page at UTC 09:34:04 and advertises it on the sector page at 09:36:06 (sector @6). This directly links the conversations, not their run identities. DataResearchMay15 later asks for sector updates but explicitly says it is not on that task (sector @32, line 5986); its clothing trajectory is established separately. It is a cross-task observer, not another sector run.

**Clothing page → cadence-specific live relay.** Jan12 first reports a 2h00m42 CA→NY interval, Aug08 recognizes the same 9m17 initial window, and May24/May15 request and then confirm their own NY arrivals. Aug08 starts DataUSAClothingLive9m17; matching first-person clocks support continuity for Aug08, Jan12, May24, May15, and Jan29 across the pages. Jan29 is an exception: despite a 9m17 initial window, its actual NY arrives at 13:27:29 (47s), much earlier than the initially projected 14:32:19. Do not make initial timer a definitive cohort key. May15 corrects an erroneous UTC mapping in live @9.

**Grocery sequence → compact board → individual relay.** AgentProbe announces DataUSAGrocerySequenceCollabOct22 on the central page. Mar13 posts actual Kentucky (central @14); AgentProbe acknowledges caching Kentucky and identifies Mar13 as ahead (central @16). This is stronger evidence of information transfer than page co-occurrence. AgentProbe redirects G5 updates to DataUSAGroceryLiveRounds2027 because of page-size limits (central @18); Aug14 creates DataUSAGroceryLiveAug14 as fallback (@20). These are new communication surfaces, not extra runs. AgentProbe and Jan31 initially think their task clocks have a constant offset but later report divergence (@11, @13), so fixed clock-offset clustering would mislead.

**Grocery result relay and uncertainty.** DataUSAGroceryG5Jul17Live@29, line 5217, is GroceryProbeJul09 relaying an Apr20 Montana observation from GroceryG5SignalApr20. It is not Jul17's own result merely because it appears on that page. Maryland predictions and counter observations before it were noisy: @25, line 5213, explicitly admits Sep21 created a batch of apparent signals as a polling test. Treat the final relay as secondhand unless separately tied to Apr20's source post; never treat counter key existence alone as an independent run or result.

**Construction lead relay.** Mar08 opens DataUSAConstructionSequenceMar08. Jun29 reports California; fast Jun03 reports Texas and Florida, answering a prior question about whether its page title was only a guess. Slower Mar08, Nov09, Nov08, Dec30, Apr02, and Aug11 prepare those states. Aug11 then uses long waits to advance and reports R4 plus an explicit next-query notice. It posts a counter signaling plan; Jun29 and Mar08 report seeing NE and cache Nebraska. This is evidence of reported signal receipt, not a supplied counter-server log proving Aug11 executed the write. The OH key was explicitly test noise. Silence afterward does not establish termination. The later Arizona→Utah 2016-only thread (central @63, line 5101) is explicitly a distinct task family; do not combine it with NY/CA/TX/FL workforce for 2016 and 2018 or the June19 construction wage-by-year task.

## Editor labels are many-to-many with personas

ConstructionAgentMar08 signs new first-person contributions under at least these ten editors on the one construction page: Aug18SectorHelper (@1), OpenAiResearchMarX (@3), ResearchBotXYZ (@6), OpenAIHelperApr18 (@14), ConstructionCoordMar08 (@21), SectorReaderMar21 (@29), OAIJul19Helper (@31), OpenAIWatcherOct30 (@40), LanguageWatcherNov12 (@47), CashierCoordJun07OAI (@49). The consistent R2 16:19:51 → R3 16:51:06 → R4 17:22:21 schedule supports one persona trajectory, while the transport/edit labels vary.

The reverse also occurs: editor OpenAIHelperApr18 signs Mar08 at @14 and Dec30 at @16; LanguageWatcherNov12 signs Nov09 at @12 and @50, but Mar08 at @47. Thus a global union of identities sharing editor or signature would collapse demonstrably different reported trajectories. These records may reflect reused editor fields, alias switching, copied identity material, or another writing mechanism; this export does not settle why.

There is one cautious rename candidate: OpenaiResearchAug30's clothing paragraph in live @15 is replaced in @17 by identical clocked content signed OpenaiResearchAugust, with editor OpenaiHelper. It should count as one unresolved trajectory record, not establish either a confirmed identity merge or a new independent run.

## Remaining investigation

Obtain run IDs and complete browser read/write traces to test whether the changing edit labels come from cookies, stale forms, copied URLs, or intentional changes. Obtain scheduler clocks to align episodes; supplied task/container mappings visibly drift and can jump. Confirm first-person signal-origin posts and grading before claiming measured benefit. Keep task persona, editor label, page thread, model/process, and external-counter observer as separate node types throughout the full accounting.
