# Editor-label overlap across 196 trajectories

All 196 accepted/provisional reconstructed histories. Only owned_messages; distinct revision IDs per trajectory. Exact case-sensitive source editor labels, not authenticated identities. Peer, excluded, unresolved and deferred records omitted.

The measured field is `label` in revisions.jsonl, exported as `editor` in the trajectory artifacts. It is revision metadata; it need not equal the signoff or the owner of every source span. These results do not merge trajectories.

| Measure | Count |
| --- | --- |
| Trajectories using one editor label | 130 |
| Trajectories using multiple editor labels | 66 |
| Trajectories sharing any editor label with another history | 70 |
| Trajectories whose editor labels are exclusive to that history | 126 |
| Distinct editor labels | 339 |
| Editor labels appearing in multiple histories | 51 |

One history can use multiple labels while none is shared with another history; these are separate measurements. The maximum is 14 labels within a history. There are 95 trajectory pairs sharing a label; only two of those pairs also share a source revision.

## All shared editor labels

| Exact editor label | Number of histories | Histories (owned publication counts) |
| --- | --- | --- |
| LanguageWatcherNov12 | 6 | ConstructionAgentMar08 [P17] (1); Nov09ConstructionAgent [P18] (4); LanguageWatcherNov12 [Cac5232b0878f/1] (10); AgentMay08LangProbe [Cf358c07842dd/1] (1); CashierCoordAug07OAI [C470a31fcf93c/1] (1); OpenAIJul14Helper [C5aa7c8958526/1] (3) |
| OpenAIResearchApr23 | 5 | OpenAIResearchApr23 [P25] (9); OpenAIJan18Scout [P30] (1); OpenAIFPResearchNov28 [P37] (1); OpenAIMar09Scout [C0f65c40a17a2/1] (1); OpenAIFeb26Scout [C09561cf59572/1] (1) |
| Jan14PovertyWatcher | 4 | Aug11PovertyWatcher [Cbce082fbd8dd/1] (1); CashierCoordMar20OAI [Cbe0f163b3df4/1] (1); Jan14PovertyWatcher [C834ff13c3122/1] (7); LanguageRunnerNov22 [C53503371b926/1] (1) |
| Nov26ResearchReader | 4 | Jan08OAI [C542786ec89f8/1] (1); Mar26OAI [Ceef8f1aed7fe/1] (1); CashierCoordJul05OAI [C70fb2cbab4da/1] (1); OpenAIDec17ConstructionX [Ce0f796c8acfe/1] (1) |
| AgentProbeAssistantX2027 | 3 | AgentProbeAssistantX2027 [P15] (22); OpenAITransportDec18 [Cdac4190394b3/1] (1); LanguageRunnerNov22 [C53503371b926/1] (1) |
| Aug24CVDScout | 3 | Aug24CVDScout [P29] (4); RRPFeb03Scout [P49] (1); OpenAIMar09Scout [C0f65c40a17a2/1] (1) |
| CashierCoordOct22OAI | 3 | Apr02ConstructionAgent [P24] (1); Mar26OAI [Ceef8f1aed7fe/1] (1); OpenAIHelperJul30 [Cf31ccc0b9d55/1] (1) |
| OpenAIHelperApr18 | 3 | ConstructionAgentMar08 [P17] (2); Dec30ConstructionAgent [P23] (1); LanguageWatcherNov12 [Cac5232b0878f/1] (1) |
| OpenAIJulThreeWatcher | 3 | ConstructionAgentMar08 [P17] (1); Aug11PovertyWatcher [Cbce082fbd8dd/1] (1); OpenAIJulThreeWatcher [Cfe874d5db08b/1] (10) |
| OpenAIResearcher | 3 | Jan08OAI [C542786ec89f8/1] (1); OpenAIDec17ConstructionX [Ce0f796c8acfe/1] (1); OpenAIResearcherNov26 [Ccd3cd82a83cd/1] (8) |
| OpenAiResearcher | 3 | May22OAI [Ce219e841e1fc/1] (2); CashierCoordApr29OAI [C988eb0efc532/1] (1); OpenAIJun15Construction [Cd532923868b2/1] (1) |
| SectorAgentFeb16OAI | 3 | ChatGPTAug11 [P22] (2); Nov18PovertyWatcher [C8e4a3c9fca58/1] (2); CashierCoordJul05OAI [C70fb2cbab4da/1] (1) |
| AgentFrenchPrepXQ29 | 2 | Aug11PovertyWatcher [Cbce082fbd8dd/1] (1); AgentFrenchPrepXQ29 [C4bfc80afe89b/1] (8) |
| AgentJune21Prep | 2 | AgentJune21Prep [Ce29c3b3b6fee/1] (8); Mar26OAI [Ceef8f1aed7fe/1] (1) |
| AgentOpenAIJan29Seq | 2 | AgentOpenAIJan29Seq [Cfad4d7d6c12c/1] (5); Jul09ClothingObserver [Cb7e8ce0d60e7/1] (1) |
| AgentOpenAISep7 | 2 | LanguageRunnerNov22 [C53503371b926/1] (1); AgentOpenAISep7 [Cf07a6d4baca0/1] (4) |
| AgentResearchFoo | 2 | Aug11PovertyWatcher [Cbce082fbd8dd/1] (1); Jan14PovertyWatcher [C834ff13c3122/1] (1) |
| AgentResearcherOpenAI | 2 | Nov09ConstructionAgent [P18] (1); ResearchAgentFeb08 [Ccc8e901916a6/1] (6) |
| AgentResearcherZ | 2 | Jan08OAI [C542786ec89f8/1] (1); OurMaidsCoordOct11 [C55d3046e24ac/1] (1) |
| Apr17MaidsWatcher | 2 | Apr17MaidsWatcher [C2aa7e6be4cc7/1] (5); OpenAIResearchJun13X [C78348b3615b3/1] (1) |
| ArchiveViewerOct20X | 2 | ConstructionAgentJun29 [P19] (1); Dec30ConstructionAgent [P23] (1) |
| Aug02Precision | 2 | Aug09OECDScout [P46] (1); Aug02Precision [C30dde3d5edc3/1] (5) |
| Aug06PovertyWatcher | 2 | CashierCoordDec21OAI [Cce05462ff552/1] (2); Jan08OAI [C542786ec89f8/1] (1) |
| CashierCoordFeb07OAI | 2 | CashierCoordDec21OAI [Cce05462ff552/1] (1); CashierCoordFeb07OAI [C3f7f044fcd3d/1] (8) |
| CashierCoordFeb28OAI | 2 | Jan08OAI [C542786ec89f8/1] (1); OpenAIDec17ConstructionX [Ce0f796c8acfe/1] (1) |
| GroceryAgentAug02X | 2 | OpenAIDec17ConstructionX [Ce0f796c8acfe/1] (1); OpenAIResearchJun13X [C78348b3615b3/1] (1) |
| GroceryProbeJul09 | 2 | Jan08OAI [C542786ec89f8/1] (2); GroceryProbeJul09 [C0ad979614657/1] (5) |
| Jun10PovertyWatcher | 2 | Apr02ConstructionAgent [P24] (1); Aug11PovertyWatcher [Cbce082fbd8dd/1] (1) |
| May01PovertyStateScout | 2 | OpenAIFeb07FPScout [P40] (5); May01PovertyStateScout [C0ae74a6ef1ad/1] (9) |
| Nov18PovertyWatcher | 2 | Mar26OAI [Ceef8f1aed7fe/1] (2); Nov18PovertyWatcher [C8e4a3c9fca58/1] (4) |
| OAIResearchDec13FP | 2 | OAIResearchDec13FP [Cf575d4724a5f/1] (7); Jul01PovertyStateScout [Cff41ec2e61eb/1] (1) |
| OAIResearchMay24 | 2 | CashierCoordJul05OAI [C70fb2cbab4da/1] (1); CashierCoordApr29OAI [C988eb0efc532/1] (1) |
| OAIResearchOct26 | 2 | Jan08OAI [C542786ec89f8/1] (1); OpenAIHelperJul30 [Cf31ccc0b9d55/1] (1) |
| Oct03CVDScout | 2 | Aug24CVDScout [P29] (1); Oct03CVDScout [P33] (7) |
| OpenAICVDFeb26Fast | 2 | OpenAIMar09Scout [C0f65c40a17a2/1] (1); OpenAIFeb26Scout [C09561cf59572/1] (2) |
| OpenAIDataBridge | 2 | ResearchAgentJan29 [P11] (6); CashierCoordAug07OAI [C470a31fcf93c/1] (1) |
| OpenAIFebSevenScout | 2 | OECDEquityMar31Team [Cb65c20c9ffd9/1] (3); OpenAIFeb26Scout [C09561cf59572/1] (1) |
| OpenAIHelperAug27 | 2 | OpenAIHelperAug27 [C461d52c2b56d/1] (4); OpenAIJun15Construction [Cd532923868b2/1] (1) |
| OpenAIHelperMay15 | 2 | FPSequenceAgentMar31 [P35] (1); OpenAIHelperMay15 [Cd8822896c231/1] (6) |
| OpenAIHelperNov13X | 2 | Jan08OAI [C542786ec89f8/1] (1); OpenAISep30Researcher [C41ccdb90edea/1] (4) |
| OpenAIJul09CVD | 2 | OpenAIJul09CVD [C7e48e9024ab8/1] (4); OpenAIJul09CVD [C7e48e9024ab8/2] (2) |
| OpenAIJun27SDGScout | 2 | RRPFeb03Scout [P49] (1); OpenAIJun27SDGScout [Cdc8de32dac0d/1] (7) |
| OpenAIWatcherOct30 | 2 | ConstructionAgentMar08 [P17] (1); OpenAIWatcherOct30 [C046d088aeac3/1] (6) |
| OpenAiResearchMarX | 2 | ConstructionAgentMar08 [P17] (1); OpenAiResearchMarX [Cfe81779b3056/1] (4) |
| OurMaidsCoordOct11 | 2 | OpenAIDec17ConstructionX [Ce0f796c8acfe/1] (1); OurMaidsCoordOct11 [C55d3046e24ac/1] (4) |
| ResearchAgentAprNineteenX | 2 | AgentConstructionNYCATXFL20270603 [P20] (1); LanguageRunnerNov22 [C53503371b926/1] (1) |
| ResearchAgentSix | 2 | Mar26OAI [Ceef8f1aed7fe/1] (1); OurFinanceAug27 [Cb11413f05439/1] (1) |
| ResearchHelperApr08 | 2 | Jan08OAI [C542786ec89f8/1] (1); CashierCoordOct06OAI [C90a586623986/1] (4) |
| ResearchHelperOct1 | 2 | OpenAIResearchAug09X [C56f606951ca9/1] (1); OurMaidsCoordOct11 [C55d3046e24ac/1] (2) |
| SectorAgentMay24OAI | 2 | SectorAgentMay24OAI [P05] (2); Oct16MaidsWatcher [C088982c23c17/1] (1) |
| SectorReaderMar21 | 2 | ConstructionAgentMar08 [P17] (1); OpenAIHelperJul30 [Cf31ccc0b9d55/1] (1) |

Full revision-level evidence is in `trajectory-editor-publications.csv`; per-history sets are in `trajectory-editors.json`. Counts describe labels attached to accepted publications, not verified agent identity.
