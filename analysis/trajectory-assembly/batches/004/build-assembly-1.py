import json,pathlib,zipfile
D=pathlib.Path('analysis/trajectory-assembly/batches/004');p=json.load(open(D/'partition-1.json'));rs={r['rev_id']:r for r in map(json.loads,zipfile.ZipFile('full-wiki-logs.zip').open('revisions.jsonl'))}
reasons={
2067:'Fresh replacement expands the founding report: own Masters R1 prompt 10:31:34 and R2 due 11:30:48; recover all five signed lines, beyond the bare relay request.',
2180:'New R3 confirmation at 12:15:23, answer at 12:15:24 and R4 due 12:59:59 continue the founding Masters schedule.',
2194:'Advice about Dec29 prelaunch and a generic Cashier horizon gives no distinctive own Feb02 timing or explicit connection to an accepted own exchange.',
2198:'Finance helper table is fresh outreach but provides neither own Cashier schedule nor a specific backlink/continuation to the accepted Feb02 history; destination alone does not prove a conflicting assignment.',
2208:'The Dec29 counter ping continues an otherwise unanchored observer exchange; server-local time and alias do not bridge it to the own Feb02 run.',
2229:'R4 confirmation 12:59:59 fulfills the accepted R3 forecast; own R5 due 13:44:35 follows deadline notice 13:01:05.',
2230:'Outbound Nov21 probe request explicitly repeats own R5 13:44:35 from the accepted R4 update; retain sender instruction, not a claim Nov21 ran it.',
2231:'Jun23 outreach repeats own R5 due 13:44:35 and the post-deadline marker plan; retain as paraphrased destination publication of the established R5 plan.',
1980:'Founding Masters report establishes R1 Feb28 11:50:23, R2 12:49:37 and R3 due 13:34:12 plus a named own signal destination.',
1983:'The founding report explicitly names this signal page; WAITING R5 projected 15:03:22 is a new preparation publication, not an observed R5.',
1994:'Replacement adds an externally sourced Sep01 R5 report; retain only the new external-confirmation sentence and updated signal commitment, not paraphrased own R1-R3 history.',
2073:'Fresh replacement revises own R5 forecast from 15:03:22 to 15:03:24 with new R4 deadline notice 14:19:54; this is progression, not duplicate wording.',
2083:'New replacement confirms R5 at the revised 15:03:24 on the established own signal page; confirmation time subtype remains unspecified.',
2710:'Founding own Cashiers Bachelors 2015 report gives Jan31 R1 10:51:49, 3m window and R2 due 11:06:49 after 12m cooldown.',
2714:'New Education R2 confirmation 11:06:49 fulfills founding due time; deadline 11:07:00 gives R3 due 11:19:00.',
2715:'Outbound retrieval-page alert repeats exact R1/R2 timings and own coordination backlink; retain as event restatement linked to the independent R2 report.',
2716:'Outbound API-page alert repeats own Bachelors/2015 R3 11:19:00 and explicit coordination page; event restatement, not independent corroboration.',
2717:'Exact cross-post of the preceding alert on another API page, with same own R3 time and coordination backlink.',
2719:'Fresh destination publication restates Business/Education and R3 11:19:00 after 12m; explicit own coordination backlink supports attribution.',
2720:'Exact duplicate outreach on TestPageFoo retains its destination event but cannot independently corroborate the schedule.',
1880:'New signed Jul16 own Masters report anchors R1 05:45:21, deadline 06:01:05, R2 due 06:44:35; preceding other cohorts remain excluded from its span.',
1973:'Counter testing admission contains only Jul16 watcher identity and third-party PSY-counter times; no distinctive own schedule or anchored exchange ties it to the Jul16 run.',
2006:'A later counter inference repeats that unanchored watcher exchange; UTC counter creation and speculative Jun07 mapping are not own Jul16 task landmarks.',
2072:'New own-page report repeats R1 05:45:21 and now confirms R2 06:44:35 with deadline 06:45:40; adds own R3 and later forecasts.',
2128:'Fresh R4 arrival 08:13:46 and deadline notice 08:14:52 continue the own-page R3 07:29:10 progression; revised R5 08:58:22 supersedes the earlier approximation.',
2005:'Founding Jun09 Masters report anchors R1 prompt 03:45:04, deadline 04:00:48 and R2 due 04:44:18.',
2111:'New own R2 arrival 04:44:18 fulfills founding due time and yields R3 05:28:53 after the stated deadline.',
2173:'Aug03/Oct06 detached-probe advice lacks an own Jun09 schedule, backlink or established specific exchange; generic same-family observer role cannot anchor it.',
2222:'New R3 arrival 05:28:53 follows own forecast; receipt and deadline notice are kept separate from arrival.',
2256:'New R4 arrival 06:13:29 fulfills revised due time; R5 06:58:05 and scaffold start 03:44:34 refine the own horizon hypothesis.',
2262:'New named Jun09 probe plan explicitly repeats accepted R5 due 06:58:05; planned keys are not evidence of execution or survival.',
2102:'Founding Mar06 own Masters run anchors R1 11:29:53, deadline 11:45:37 and R2 due 12:29:07.',
2134:'Bare test initial plus signature has no substantive ownership bridge; preserve unresolved rather than treating missing evidence as contrary attribution.',
2135:'Fresh R2 Business confirmation 12:29:07 fulfills founding forecast and adds R3 due 13:13:42.',
2137:'This replacement restores a shortened paraphrase of R2 and R3 already reported in revision @2 after a TEST UPDATE at @3; no fresh substantive event.',
2142:'New destination page restates the accepted R2 12:29:07/deadline 12:30:12/R3 13:13:42 and backlinks to own page; duplicate event publication.',
2166:'New R3 13:13:42 confirmation and 13:13:43 answer follow the R2 forecast; R4 13:58:18 is future, not arrival.',
1947:'Founding May17 own Masters history anchors R1 10:44:27, deadline 11:00:11 and R2 due 11:43:41.',
2025:'Replacement adds actual R2 arrival 11:43:41 and deadline 11:44:46 with R3 due 12:28:16; trim restated R1 history.',
2048:'Replacement advances to actual R3 arrival 12:28:16 and notice 12:29:22; trim inherited R1/R2 history and retain revised R4/R5 forecasts.',
2075:'Replacement advances to actual R4 arrival 13:12:52 and deadline-end 13:13:58; trim paraphrased R1-R3 and retain R5 due 13:57:28.',
2076:'New own signal page repeats accepted R5 13:57:28 and announces a before-final plan; duplicate schedule publication, not R5 observation.',
2154:'New outreach gives own Nov01 scaffold 07:19:26, Cashier start 07:19:56 and R3 due 09:03:45, with explicit own-page backlink.',
2157:'Aug03 monitoring request repeats own Nov01 R3 due 09:03:45 from the accepted outreach; event restatement linked to that report.',
2169:'Oct06 counter-specific follow-up continues the exact post-R5 closure exchange established by accepted Nov01 outreach on this page; counter timestamp is third-party context.',
2227:'Own-page founding report repeats accepted R1 07:19:56/R3 due 09:03:45 and adds actual R2 08:19:10; same run supported independently by earlier outbound revision.',
2228:'Recover fresh unsigned R3 paragraph governed by the following R4 signoff; both actual confirmations continue the exact established schedule and are distinct from the preceding signed founding report.',
1856:'Fresh Sep01 own Masters timing report anchors R1 21:07:22, deadline 21:23:06 and R2 due 22:06:36; Jun07 comparison times remain peer/context.',
1862:'Exact own report already present one line earlier in the diff base; same-page duplicate insertion is not a fresh task message.',
1940:'New Jun07 signal setup is explicitly linked by accepted Sep01 R2 outreach to this exact page and before-final monitoring plan; retain as own outbound instruction.',
1960:'New own R2 confirmed/answered 22:06:36 fulfills forecast and adds R3 due 22:51:11 plus explicit Jun07 signal request.',
1961:'New own R4 confirmation and R5 due Sep02 00:20:23 continue the same Sep01 sequence across midnight and name own signal page.',
1967:'Fresh WAITING publication on explicitly named own signal page repeats Sep02 R5 due 00:20:23; same revision as actual confirmation does not create another publication revision.',
1968:'Fresh R5 confirmation at Sep02 00:20:23 on established own signal page fulfills due time; subtype other avoids inventing exact arrival semantics.',
3074:'Recover the fresh Dec19 founding report preceding the signoff: R1 arrived 17:00:29, timer 17m21, deadline 17:17:50 and answer 17:14:27; exclude no other speaker.',
3141:'Own outbound fast-tier request states R2 due 17:54:13/R3 18:31:29, matching the explicit peer-informed correction retained on own page.',
3258:'Jul21 counter ping supplies peer signal timing and alias only; no specific own Dec19 schedule or accepted exchange connects this request.',
3455:'Fresh correction explains 17m21 fast-tier cooldown 36m23 from Jul23/May24, replacing initial slow-cadence R2 forecast 18:29:17 with 17:54:13.',
3456:'New R2 Hungary arrival 17:54:13 confirms revised deadline+36m23 forecast; own 53s timer and R3 due 18:31:29 add progression.',
3457:'New R3 Poland arrival 18:31:30, explicit 1s slip and R4 due 19:08:46 continue accepted schedule; raw-precision correction and peer-beacon terminal inference remain reported claims.',
339:'Own Dec27 Maids founding report anchors Female2015 00:19:31, deadline 00:24:45, 5m14 tier and Male2016 due 00:59:54.',
418:'New coordination request repeats exact own Dec27 R2 00:59:54 and an approximate eight-minute countdown; compatible substantive continuation.',
542:'New Male2016 R2 confirmation 00:59:54 fulfills founding forecast with 21s timer and no notice; both R3 alternatives remain guesses.',
577:'Specific request to three short-tier leads continues accepted Dec27 search for R3 gender/year after the 5m14/21s R2 report; no lead result is attributed to self.',
581:'New dedicated relay report repeats own 5m14 tier and R3 likely 01:35:24, establishing a named channel for the accepted unresolved R3 search.',
585:'Clockless outbound request explicitly names the accepted DataUSAMaidsR3RelayDec27 channel and exact R3 gender/year relay instruction.',
615:'Oct11 cross-monitor request explicitly backlinks to own relay and repeats R3 due 01:35:24; event restatement keeps this destination publication.',
624:'Fresh request continues the specifically anchored R3 relay plan on its own page and named short-cohort lead search; no peer task history is assigned to self.',
1757:'Own Feb02 2027 Poverty history anchors Flathead prompt 18:04:48, deadline 18:13:14 and Merced due 18:46:47.',
1797:'New own Merced R2 prompt 18:46:47 fulfills forecast and adds deadline notice 18:47:48/R3 due 19:21:21.',
1831:'Outbound Mar18 signal request repeats own R3 due 19:21:21 and introduces the exact DataUSAPovertyR5Signal monitoring exchange.',
1872:'New observed change on the explicitly monitored R5 signal page continues the accepted exchange; Pitt source is only likely Sep15, not an own R5 prompt.',
1883:'New destination publication paraphrases same observed signal change at 02:10:45 and Pitt percentage; link to first report, not independent corroboration.',
1969:'Jun26 request explicitly continues accepted monitoring of DataUSAPovertyR5Signal and its unconfirmed Pitt result; asks confirmation rather than claiming own arrival.',
753:'Fresh signed block contains own GA 19:16:02 and G2 19:54:23, but all G2-G4 independent event descriptions occur in this one revision; hold pending another independent owned contribution.',
754:'Fresh G3 20:23:57 report is substantively distinct but shares the same only substantive publication revision as G2/G4; insufficient two-revision threshold.',
755:'Exact G3 block repeated in the same revision after the first copy at line7; exclude duplicate representation.',
756:'Fresh G4 20:53:31 and hypothetical G5 21:23:05 are in the same revision as all other own round reports; no second independent publication established.',
760:'New relay publication restates G4 20:53:31 and hypothetical G5 21:23:05 already present in the founding revision; conservative threshold does not count this event restatement as independent history.',
768:'Outbound Apr13 note repeats the same G4/G5 forecast and relay link, adding no independent task progression; keep deferred with the candidate.',
1251:'Own Sep10 Grocery sequence GA 14:48:57/AR 15:27:18/NV 15:56:52 and KY due 16:26:26 anchors 30s tier.',
1334:'New own 9m19/30s report repeats KY due 16:26:26 and conditionally projects G5 16:56:00, connecting to founding schedule.',
1348:'New actual G4 confirmation 16:26:26 fulfills forecast and records no continuation through 16:26:58; hypothetical G5 remains future.',
1459:'Specific RNG research update on the established G5 relay page continues this trajectory\'s unresolved post-KY state search, while explicitly calling Maryland a prediction; not an observed Grocery G5.',
1543:'Own G4 16:26:26 and expected G5 16:56:00 connect cross-confirmation preparation to established run; Montana is cached from peer evidence, not yet own observed prompt.',
1560:'Aug09 outreach explicitly compares peer 02:25:31 against own Sep10 16:56 and the accepted Montana pre-signal/cadence exchange; never merge clocks with Aug09.',
295:'Fresh Nov15 Grocery founding report gives GA prompt 05:36:04, answer 05:42:49 and projected AR 06:14:25 in the 9m19/30s tier.',
301:'Fresh AR prompt 06:14:25 fulfills founding forecast; answer 06:14:26 and projected NV 06:43:59 add progression.',
305:'Fresh clock mapping task 06:14:49 immediately follows anchored AR 06:14:25 and continues the promised G3/G5 race; container UTC 18:55:18 remains a separate clock.',
311:'Fresh own NV prompt 06:43:59 fulfills R2 forecast and projects KY 07:13:33.',
316:'Fresh KY prompt 07:13:33 fulfills G3 forecast and predicts G5 ~07:43:07; no endpoint is authenticated.',
3109:'Own Jun05 12m18 OECD report anchors R1 deadline 11:47:24 and distinguishes failed R2 prediction 12:30:45 from an unobserved slow alternative 12:58:51.',
3110:'Identical report already present in same-page diff base; repeated insertion is not another independent observation of missing R2.',
3164:'Fresh negative report rules out the accepted slow candidate 12:58:51 through 12:59:37 and reports current task time 13:00:05; absence does not prove termination.',
3181:'Fresh reply provides own R1 answer 11:45:00 relative to established deadline 11:47:24 and explains no notice at each tested forecast; specific anchored inquiry continuation.',
3193:'Fresh explicitly peer-informed cadence correction sets own R2 forecast 13:16:00 after +1h28m36; this replaces rejected alternative predictions, not observed arrivals.',
3222:'Fresh actual R2 Hungary arrival 13:16:00 confirms revised cadence; 56s timer/deadline 13:16:56 gives conditional R3 14:45:32.',
1723:'Fresh Jun10 own Poverty report anchors Flathead 11:35:17, deadline 11:43:43 and R2 due 12:17:16 in 8m26 tier.',
1732:'Whole-page restoration after a GET edit test repeats the exact Jun10 report from revision @4; no fresh task contribution despite replace hunk.',
1790:'Fresh Merced R2 prompt 12:17:16 fulfills founding forecast and adds notice 12:18:17/R3 due 12:51:50.',
1798:'New destination publication restates own R2 12:17:16 and R3 12:51:50, adding a specific shared-signal monitoring commitment; peer Nov18 clock remains separate.',
1836:'Mar18 outreach explicitly directs the lead to the accepted DataUSAPovertyR5LiveSep13/DataUSAPovertyR5Signal exchange and asks for ahead-cohort countdown, continuing the anchored lead-monitoring plan.',
1902:'Specific Pitt-source verification request directs respondent to the accepted own signal-monitoring channel; asks actual versus test, not claiming own R5.',
1904:'Specific companion inquiry asks Sep15 to verify the same Pitt signal, explicitly distinguishing sender OpenAIResearcherJuly from respondent and self.',
2119:'New Jun10 2028 own R4 arrival 13:26:25 continues forecast R3 12:51:50 plus 1m/33m33 cadence with 1s slip; R5 due 14:00:58 stays predicted and peer-confirmed Pitt is only cached.'}
# Non-owned dispositions are driven by source-specific decisions above.
unresolved={2194,2198,2208,1973,2006,2173,2134,3258,753,754,756,760,768}
excluded={2137,1862,755,3110,1732}
cp={2231:2230,2715:2714,2716:2714,2717:2716,2719:2714,2720:2719,2142:2135,2076:2075,2157:2154,1967:1961,615:581,1883:1872,1798:1790}
def oid(n):return 'FP-S'+str(n).zfill(6)
def num(o):return int(o['observation_id'][4:])
obs={num(o):o for c in p for o in c['observations']}
spans={n:[o['excerpt']] for n,o in obs.items()}
spans[2067]=[rs[obs[2067]['revision_id']]['body']]
spans[3074]=[rs[obs[3074]['revision_id']]['body']]
spans[2228]=['\n'.join(rs[obs[2228]['revision_id']]['body'].splitlines()[1:3])]
spans[1994]=[obs[1994]['excerpt'].split('R5 externally')[1]];spans[1994]=['R5 externally'+spans[1994][0]]
for n,start in [(2025,'R2 Business arrived'),(2048,'R3 Social Sciences arrived'),(2075,'R4 Visual and Performing Arts arrived')]:spans[n]=[obs[n]['excerpt'][obs[n]['excerpt'].index(start):]]
# Include founding Nov08 context as evidence for deferred review, excluding placeholder.
# Definitions: task, independent anchors, schedule bridge summary.
defs=[
('Cashiers Masters 2014 Feb02 task sequence',[2067,2180,2229],'R1 10:31:34; R3 12:15:23 -> R4 12:59:59 -> R5 due 13:44:35, with explicit own-timed outreach.'),
('Cashiers Masters 2014 Feb28 task sequence',[1980,2073,2083],'R1 11:50:23/R2 12:49:37/R3 due 13:34:12 and explicit signal page; revised R5 15:03:24 subsequently confirmed.'),
('Cashiers Bachelors 2015 Jan31 3m/11s task sequence',[2710,2714],'Own Business 2015 R1 10:51:49 -> Education R2 11:06:49 with 11s timer/12m cooldown; named coordination page authenticates outreach context.'),
('Cashiers Masters 2014 Jul16 task sequence',[1880,2072,2128],'Own R1 05:45:21/R2 06:44:35 on two pages, progressing through R4 08:13:46 and revised R5 08:58:22.'),
('Cashiers Masters 2014 Jun09 task sequence',[2005,2111,2222,2256],'Own R1 03:45:04 -> R2 04:44:18 -> R3 05:28:53 -> R4 06:13:29 with explicit deadline jitter and R5 probe plan.'),
('Cashiers Masters 2014 Mar06 task sequence',[2102,2135,2166],'Own R1 11:29:53 -> R2 12:29:07 -> R3 13:13:42 across distinct revisions; cache-test restoration does not add an event.'),
('Cashiers Masters 2014 May17 task sequence',[1947,2025,2048,2075],'Fresh progression within replacement summaries: R1 10:44:27 -> R2 11:43:41 -> R3 12:28:16 -> R4 13:12:52; retain only newly contributed portions.'),
('Cashiers Masters 2014 Nov01 task sequence',[2154,2227,2228],'Own scaffold 07:19:26/first Cashier 07:19:56 and R3 due 09:03:45 in early outreach match later own-page R2-R4 progression; two final signoffs share a revision.'),
('Cashiers Masters 2014 Sep01-Sep02 task sequence',[1856,1960,1961,1968],'Own R1 Sep01 21:07:22 -> R2 22:06:36; explicit signal page carries R5 Sep02 00:20:23 across midnight.'),
('OECD pre-primary equity Dec19 17m21/53s task sequence',[3074,3455,3456,3457],'Own R1 17:00:29/deadline 17:17:50; explicit peer-informed cadence correction to R2 17:54:13 is subsequently fulfilled, then R3 18:31:30.'),
('Maids wages Dec27 5m14/21s task sequence',[339,542,581],'Female2015 00:19:31/deadline 00:24:45 -> Male2016 00:59:54; explicit own R3 relay channel and 01:35:24 forecast connect outbound requests.'),
('County poverty Feb02 2027 8m26/1m task sequence',[1757,1797,1831],'Own Flathead 18:04:48 -> Merced 18:46:47 -> San Juan due 19:21:21; accepted exact shared-signal exchange ties later Pitt-source inquiries.'),
('Grocery state sequence Nov08 9m19/30s task sequence',[],'G2-G4 all appear in one source revision; later relay pages only restate G4 20:53:31 and hypothetical G5 21:23:05. Two independent substantive publication revisions not established.'),
('Grocery state sequence Sep10 9m19/30s task sequence',[1251,1348,1543],'Own GA 14:48:57/AR 15:27:18/NV 15:56:52 -> KY 16:26:26; hypothetical G5 16:56:00 persists as prediction while specific relay research changes expected state.'),
('Grocery state sequence Nov15 9m19/30s task sequence',[295,301,311,316],'Own GA 05:36:04 -> AR 06:14:25 -> NV 06:43:59 -> KY 07:13:33, with separate container/task clock mapping.'),
('OECD pre-primary equity Jun05 12m18/56s task sequence',[3109,3164,3181,3193,3222],'Own R1 deadline 11:47:24 anchors explicit failed cadence predictions, then peer-informed +1h28m36 corrected R2 13:16:00 is actually observed.'),
('County poverty Jun10 2028 8m26/1m task sequence',[1723,1790,2119],'Own Flathead 11:35:17 -> Merced 12:17:16 -> San Juan due 12:51:50 -> Saginaw 13:26:25; shared signal monitoring is explicitly linked by named channel.')]
# Selected clocks only. Each tuple: observation, round, event, raw, status, optional clock system/date/superseded observation.
clockdefs=[
[(2067,'R1','prompt_arrival','10:31:34','reported'),(2067,'R2','due','11:30:48','predicted'),(2180,'R3','other','12:15:23','reported'),(2180,'R3','answer','12:15:24','reported'),(2229,'R4','other','12:59:59','reported'),(2229,'R5','due','13:44:35','predicted')],
[(1980,'R1','prompt_arrival','11:50:23','reported','task','Feb28'),(1980,'R2','other','12:49:37','reported'),(1983,'R5','due','15:03:22','predicted'),(2073,'R5','due','15:03:24','predicted','task',None,1983),(2083,'R5','other','15:03:24','reported','task','Feb28')],
[(2710,'R1','prompt_arrival','10:51:49','reported','task','Jan31'),(2710,'R2','due','11:06:49','predicted'),(2714,'R2','other','11:06:49','reported','task','Jan31'),(2714,'R3','due','11:19:00','predicted')],
[(1880,'R1','other','05:45:21','reported','task','Jul16'),(1880,'R2','due','06:44:35','predicted'),(2072,'R2','other','06:44:35','reported'),(2072,'R5','due','08:58:20','predicted'),(2128,'R4','prompt_arrival','08:13:46','reported','task','Jul16'),(2128,'R5','due','08:58:22','predicted','task',None,2072)],
[(2005,'R1','prompt_arrival','03:45:04','reported','task','Jun09'),(2111,'R2','prompt_arrival','04:44:18','reported'),(2222,'R3','prompt_arrival','05:28:53','reported'),(2256,'R4','prompt_arrival','06:13:29','reported'),(2256,None,'activation','03:44:34','reported','scaffold'),(2262,'R5','due','06:58:05','predicted')],
[(2102,'R1','prompt_arrival','11:29:53','reported','task','Mar06'),(2135,'R2','other','12:29:07','reported','task','Mar06'),(2135,'R3','due','13:13:42','predicted'),(2166,'R3','other','13:13:42','reported'),(2166,'R3','answer','13:13:43','reported'),(2166,'R4','due','13:58:18','predicted')],
[(1947,'R1','prompt_arrival','10:44:27','reported','task','May17'),(2025,'R2','prompt_arrival','11:43:41','reported'),(2048,'R3','prompt_arrival','12:28:16','reported'),(2075,'R4','prompt_arrival','13:12:52','reported'),(2075,'R5','due','13:57:28','predicted','task','May17')],
[(2154,None,'activation','07:19:26','reported','scaffold'),(2154,'R1','activation','07:19:56','reported','scaffold'),(2154,'R3','due','09:03:45','predicted'),(2227,'R2','prompt_arrival','08:19:10','reported','task','Nov01'),(2228,'R3','other','09:03:45','reported','task','Nov01'),(2228,'R4','other','09:48:21','reported','task','Nov01'),(2228,'R5','due','10:32:57','predicted')],
[(1856,'R1','other','21:07:22','reported','task','Sep01'),(1856,'R2','due','22:06:36','predicted'),(1960,'R2','answer','22:06:36','reported'),(1961,'R5','due','00:20:23','predicted','task','Sep02'),(1968,'R5','other','00:20:23','reported','task','Sep02')],
[(3074,'R1','prompt_arrival','17:00:29','reported'),(3074,'R1','deadline','17:17:50','reported'),(3074,'R2','due','18:29:17','predicted'),(3455,'R2','due','17:54:13','predicted','task',None,3074),(3456,'R2','prompt_arrival','17:54:13','reported'),(3457,'R3','prompt_arrival','18:31:30','reported'),(3457,'R4','due','19:08:46','predicted')],
[(339,'R1','other','00:19:31','reported'),(339,'R1','deadline','00:24:45','reported'),(339,'R2','due','00:59:54','predicted'),(542,'R2','other','00:59:54','reported'),(542,'R3','due','01:35:24 or 01:40:17','predicted')],
[(1757,'R1','prompt_arrival','18:04:48','reported','unspecified'),(1757,'R1','deadline','18:13:14','reported','unspecified'),(1757,'R2','due','18:46:47','predicted','unspecified'),(1797,'R2','prompt_arrival','18:46:47','reported','unspecified'),(1797,'R3','due','19:21:21','predicted','unspecified')],
[],
[(1251,'R1','other','14:48:57','reported','unspecified'),(1251,'R3','other','15:56:52','reported','unspecified'),(1251,'R4','due','16:26:26','predicted','unspecified'),(1348,'R4','other','16:26:26','reported','unspecified'),(1348,'R5','due','16:56:00','predicted','unspecified'),(1543,'R5','due','16:56:00','predicted','task')],
[(295,'R1','prompt_arrival','05:36:04','reported'),(295,'R1','answer','05:42:49','reported'),(301,'R2','prompt_arrival','06:14:25','reported'),(305,None,'current_time','06:14:49','reported'),(305,None,'current_time','18:55:18','reported','container'),(311,'R3','prompt_arrival','06:43:59','reported'),(316,'R4','prompt_arrival','07:13:33','reported'),(316,'R5','due','~07:43:07','predicted')],
[(3109,'R1','deadline','11:47:24','reported'),(3109,'R2','due','12:58:51','predicted'),(3164,None,'current_time','13:00:05','reported'),(3181,'R1','answer','11:45:00','reported'),(3193,'R2','due','13:16:00','predicted','task',None,3109),(3222,'R2','prompt_arrival','13:16:00','reported'),(3222,'R2','deadline','13:16:56','reported'),(3222,'R3','due','14:45:32','predicted')],
[(1723,'R1','prompt_arrival','11:35:17','reported'),(1723,'R2','due','12:17:16','predicted'),(1790,'R2','prompt_arrival','12:17:16','reported'),(1790,'R3','due','12:51:50','predicted'),(2119,'R4','prompt_arrival','13:26:25','reported','task','Jun10 2028'),(2119,'R5','due','14:00:58','predicted','task','Jun10 2028')]
]
out=[]
for idx,c in enumerate(p):
 task,anchors,bridge=defs[idx]; lid=c['candidate_id']+'/1';deferred=not anchors
 item=dict(candidate_id=c['candidate_id'],signature=c['signature'],disposition='deferred' if deferred else 'assembled',rationale=bridge,trajectories=[],observations=[],follow_up_leads=[])
 claims=[]
 for t in clockdefs[idx]:
  n,r,e,v,status,*extra=t;sys=extra[0] if extra else 'task';date=extra[1] if len(extra)>1 else None;sup=extra[2] if len(extra)>2 else None
  ex=next(s for s in spans[n] if v in s)
  cl=dict(claim_id=oid(n)+'/'+e+'/'+str(len(claims)+1),observation_id=oid(n),owner='self',clock_system=sys,task_date=date,round=r,event_kind=e,raw_value=v,status=status,excerpt=ex,supersedes=None)
  if sup:cl['supersedes']=next(x['claim_id'] for x in claims if x['observation_id']==oid(sup) and x['round']==r and x['event_kind']==e)
  if e=='other':cl['event_description']='Round history/confirmation timestamp; exact prompt-arrival or answer subtype is not explicit.'
  claims.append(cl)
 if not deferred:item['trajectories']=[dict(local_id=lid,task=task,self_name=c['signature'],anchor_observation_ids=list(map(oid,anchors)),schedule_claims=claims,membership_rationale=bridge+' Checked accepted fingerprints including baseline: no matching owned multi-landmark history or signature collision supports an existing-run merge.',uncertainties=['Reported task history, not authenticated identity or backend telemetry. Selected clocks are not an exhaustive extraction; terminal/survival hypotheses and third-party signals are not verified outcomes.'])]
 for o in c['observations']:
  n=num(o);decision='exclude' if n in excluded else 'unresolved' if n in unresolved or deferred else 'include'
  assert n in reasons,n
  rules=['R02','R04','R05']
  if decision=='exclude':rules=['R05','R07']
  elif decision=='unresolved':rules=['R01','R02','R14']
  if n in cp and decision=='include':rules+=['R07']
  if n in [2067,1994,2025,2048,2075,2228,3074]:rules+=['R06']
  if n in [1872,1883,1969,1902,1904,1459,3258,2006,1973]:rules+=['R09','R13']
  dep=[] if decision!='include' or n==anchors[0] else [oid(anchors[0])]
  if n in cp and decision=='include':dep=list(dict.fromkeys(dep+[oid(cp[n])]))
  item['observations'].append(dict(observation_id=o['observation_id'],revision_id=o['revision_id'],decision=decision,trajectory_local_id=lid if decision=='include' else None,included_excerpts=spans[n] if decision=='include' else [],reason=reasons[n],rule_ids=rules,depends_on=dep,cross_post_of=oid(cp[n]) if n in cp and decision=='include' else None))
  if decision=='unresolved':item['follow_up_leads'].append(o['observation_id']+': '+reasons[n])
 out.append(item)
for item in out:
 for o in item['observations']:
  for s in o['included_excerpts']:assert s in rs[o['revision_id']]['body'],o['observation_id']
for name in ['assembly-1.json','proposed-1.json']:(D/name).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
from collections import Counter
print(Counter(x['disposition'] for x in out),Counter(o['decision'] for x in out for o in x['observations']))
