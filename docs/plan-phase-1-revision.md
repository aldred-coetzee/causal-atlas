# Phase 1 plan revision: discovery in two tiers

Written 2026-11-06, before any number from what it describes (decision 0030). Audited by next-pattern the same day, passed with eight text conditions, all made here. Then the owner. **Nothing here runs yet.** Each step needs its own go-ahead. Where this disagrees with `docs/plan-phase-1.md`, this wins; everything it does not touch stands, including rule 2, rule 9 and the stop at the end of 1d.

## In plain words

The old question was "does this one named input help?". The aim now (decisions 0021, 0027, 0029) is to find which of many inputs help without naming one first. So:

1. **A quick screen** tries every input at every lag and asks whether the best of them beats what luck gives when the inputs are moved in time.
2. **The slow forecaster** then tests only the few leads the screen names, on later months the screen never saw.
3. **The last four years** stay unseen until the very end and are scored once.

Before that, the forecaster's fault gets fixed. The baseline could blow up, and the test forecast could then win by repairing it, without having learned anything from the inputs.

## What this rests on, and what is still open

- **Why fix rather than stop:** on six planted rows the gain went away when the inputs were shifted, so it came through the inputs (`results/refit-shifts.md`). Those rows were chosen after the numbers, at one large effect, so this steers the design and shows nothing else.
- **Why fix at all:** with shifted inputs, 3007 still reached about 0.085 or more on 6 of 16 shifts (0.132, 0.085, 0.109, 0.104, 0.093, 0.135; the 0.085 is just under it) and 3010 on 2 of 16 (0.137, 0.180). Mark B missed, 3015 crashed, 3017's baseline reached 143 times observed (`results/refit-marks.md`).
- **The two-tier shape** comes from the independent review. It has never been run: every number the screen needs below is unmeasured.

## 1. The forecaster, changed

**R and M become twins.** Today R is B times g0, and M is R times g1, and g1 can see the place and R's own level. So M can redo a correction R lacks, and that counts as gain. In this revision:

- L = B times the level factor, as now, with the factor bounded (below).
- R = L times g(place, log L).
- M = L times g(place, log L, inputs).
- Same learner, same settings, **same number of trees t**, fitted on the same rows from the same L.

M can no longer win by doing R's job, because R has the same capacity for that job. The only thing M has and R lacks is the inputs.

**The tree count is fixed, not chosen per span.** Today's rule can jump from 0 trees to 95 on a small difference (3007's false alarm, span 8). R1 picks t once, from 25, 50 or 100, on spent seeds only: the smallest t at which the three calibrated rows (3011, 3002, 3008) keep at least half the score they have at t = 100. It is frozen before any fresh seed. This picks t on three planted rows only, so for power; the null side is then measured on fresh seeds.

**Blow-ups are stopped, and counted if they get through.**
- The level factor is clipped to between 1/4 and 4.
- Each cell's forecast is capped at twice the largest count that cell's block has seen before the span starts, and the cap is never below 1, so a block with no events yet is not capped to zero. Both limits use the past only.
- The existing floor of 0.001 per cell-month applies after the cap, so no forecast is zero when an event arrives. A test covers an event in a block with none before the span.
- A span whose forecast total is over 5 times the observed total of the previous 24 months is flagged `blown`. A blown or crashed row **counts as a miss**, never as a row skipped. This replaces today's guard, which checks single predictions and which crashed 3015.

Where these limits come from: judgement, sized so they touch only the failures seen. R1 reports how often each one acts.

## 2. The score, and why a wrong level cannot inflate it

**Level-free skill S.** Within each scored span s and each 5 degree block b, rescale each forecast so its total equals what was observed there:

F* = F × (observed in s, b) / (F's total in s, b)

S = 1 − D(M*) / D(R*), with D the summed Poisson deviance over cell-months. A block with no events scores zero for both. The per-cell floor keeps F's total above zero, so the division is safe even in a block forecast near zero that has events; a test covers it. **With one or two events S is mostly noise there:** the share of D coming from span-blocks with fewer than 5 events is reported, with no mark.

**Why a wrong overall level cannot inflate it.** Multiply R by any positive constant in a span and block: the rescale divides the same constant out, so R* and D(R*) are exactly unchanged. So R could be 143 times too high across a block and span and M would earn nothing for correcting it. A test will assert this to numerical precision. The block is 5 degrees because that is the unit in which the level factor, the part that failed, acts.

**What S does not remove.** A level error varying inside a span, or inside a block, is still in R*. That is why this is one of four defences and not the whole answer: twin forecasts, the limits above, S, and a pass mark measured on no-link worlds.

**What S costs.** A link whose whole effect is to raise a block's total for a whole span is invisible to it. It sees where and when within a block and span, and that is what a lagged link should mostly move. Measured on planted worlds, not assumed.

**The rescale uses the scored months, so S is a yardstick and not a forecast.** So raw skill (the old one) is always reported beside it, and a pass also needs raw skill above zero: a forecast worse in plain terms is not a finding. The interval stays the 95% moving-block bootstrap of 6 months over whole months, with rescale factors held fixed. That interval is conditional on the rescale and will be somewhat narrow; criterion 4 in section 5 is the real guard.

**"Worth" is dropped as a ruler** (amendment 5 of decision 0020). No mark uses it. The generator's true rate is scored with S beside each planted row, as a description of the most any forecaster could get.

## 3. The months

Spans are 24 months from 195, as now, so the boundaries fall cleanly:

| Months | Dates | Spans | Used for |
|---|---|---|---|
| 36 to 194 | 1992-01 to 2005-03 | | first training only |
| 195 to 290 | 2005-04 to 2013-03 | 4 | tier 1: the screen |
| 291 to 386 | 2013-04 to 2021-03 | 4 | tier 2: leads tested |
| 387 to 434 | 2021-04 to 2025-03 | 2 | held-out, **48 months stay unseen**, scored once, last |

The months are split because leads picked and scored on the same months would look better than they are. This answers amendment 4 of decision 0020. Forecasts still train on all earlier months, refitted span by span.

**Fake worlds use exactly these windows**, so the marks test what real data will meet. This costs power against the earlier 240 scored months, and the marks will show how much. They also report what the 48-month final window could detect.

## 4. Tier 1: the screen

**Candidates.** Each input, at gaps 0, 1, 2, 3, 4, 6, 9, 12, 18 and 24 months back from the forecast origin, averaged over 1, 3, 6 and 12 months. That is 40 columns per input, each an anomaly from its calendar-month mean over months before 195. On real data each source's publication delay, from the manifest, is added to its gap. All are tried; none is picked by hand.

**Statistic, for one column.** Using R's out-of-time forecast, with residuals e = y − R*, block by block: U = Σ e·z, V = Σ R*·z², and T = the statistic over blocks of U²/V. Counts are capped at 20 in e, because one month with 609 events would otherwise decide it. Three forms of "over blocks" go to R2: the sum across all blocks, the sum of the ten largest, and a single pooled Africa-wide value. One is chosen on spent seeds, by recovery of the planted input and quietness, before any fresh seed. It is cheap and has no trees, so it has no level to repair, and R* makes it level-free.

**The search-wide gate.** Is the best of everything tried better than luck?
1. Shift **all inputs together** by k whole years, k = 1 to 32, and recompute every column. This keeps each input's calendar, persistence and relation to the others, and breaks only its alignment with the counts. The series is 36 years and 3 months, so the shift wraps inside the first 432 months, a whole-year window, as `circular_shift` already does: a month before the start comes from 432 months later, the calendar month is kept, and the last 3 months of the input are never used as a shifted value. A test asserts that every shifted value keeps its calendar month.
2. Put each column on one scale: Z = (T − mean of its T over shifts) / (SD of its T over shifts).
3. Compare the largest Z with no shift against the largest Z in each shift. The world's best column passes only if it beats all 32: search-wide p = 1/33, about 0.03, however many columns were tried. Because the whole search is rerun in each shift, correlation among columns is handled without a formula.
4. Step down: remove that column and repeat, with the remaining columns. It stops at the first failure or at **K = 5 leads**.

**Limits of the gate.** p cannot go below 1/33, because there are only 32 whole-year shifts. A source with fewer than 19 usable shifts cannot reach 0.05 and is not a candidate at this gate.

**The many-input null.** Each fake world gets its own 8 input series (4 gridded, 4 global) plus **24 decoys**: the inputs of 3 other worlds, generated by the same `synth/generate.py` with their own seeds and so unrelated to this world's counts. That is 32 inputs and **1,280 columns**, with no new generator code, so the generator's independence rule is untouched. Run on null panels this is the null. Run on planted panels it asks whether the true input stands out among decoys.

**Rule: real data may not use more columns than the marks tested.** Decoys are independent of each other and real inputs are not, which is a limit of the test. The gate itself does not assume independence.

**Target-free finders (decision 0026).** The random matrix test, multi-block shared factors and persistent homology stay candidates. None is built in these steps. Each would first have to find planted structure and stay quiet on these same many-input worlds, under this gate. Whatever it reports is then a **lead only**: it takes a place among the K and goes through tier 2. Nothing is a finding until it beats the baseline out of time (rule 2).

## 5. Tier 2: the forecaster, on leads only

M gets the leads, together, on 291 to 386. Trees can combine them. Two runs are stored for the marks: gated leads (the real pipeline), and the screen's top 5 forced through whatever the gate says (to measure the no-link mark on the hardest case).

**A lead set passes, all required:**
1. S at least the mark m, with the lower end of its interval above 0.
2. Raw skill above 0.
3. S positive in at least 3 of the 4 spans.
4. S above every circular shift of those leads, and the median shift under m/2 in size. **19 shifts on fake worlds, evenly spread over 2 to 32 years, a 1 in 20 test (p = 0.05)**; all 32 on real data (p = 1/33). The diagnostic's 16 would have been 1 in 17, about 6%; three more cost about a fifth more shift time. Measured cost: about 35 minutes per row for 16 at three threads (`results/refit-shifts.md`, answering amendment 3), so about 41 for 19.

Rejecting a world is cheap: shifts run only where 1 to 3 hold.

## 6. The no-link pass mark

**Measured on:** pure_null, shared_null and combo_null, seeds 5001 to 5020 each, 60 worlds in all, each with its 1,280 columns, forced top 5 leads through tier 2. **These worlds are used for one thing only: measuring m, after every other setting (t, the statistic's form, the limits) is frozen.** Anything tuned on them would bring m out too low.

**The formula is fixed now:** m = the larger of 0.005 and the second-largest S over those 60 worlds, so about one no-link world in 30 would reach it. The 0.005 is the quiet band already used in Mark A.

**At R2 the owner confirms the number this gives or sets a higher one, before the mark seeds are touched. A lower one needs a new decision record.** By R2 the planted rows' S on spent seeds will have been seen, so a free choice then would be made knowing roughly where planted worlds land. This is next-pattern's condition, put to him as its recommendation, and his to accept. It replaces the 2% he accepted in decision 0012. **That is a rule change made after a miss, and it could favour a result.** The protection is that it is set by a fixed formula on separate worlds and tested on fresh ones, and the marks also report what 0.02 would have given.

**Out-of-sample check of m, the only one:** on the mark seeds 5101 to 5120, the count of the 60 forced-top-5 null worlds reaching m, with its exact binomial interval. Reported beside the marks.

**On real data the mark is the larger of m and the largest real shift of that lead set.** A mark from fake worlds does not carry over alone.

## 7. Seeds

**Spent, never reused for a mark:** 1001 to 1020, 2001 to 2003, 3001 to 3020, 9001 to 9005.

**Fresh, none yet fitted:**

| Seeds | Use |
|---|---|
| 5001 to 5020 | calibration, each of the 3 null panels |
| 5101 to 5120 | marks, each of the 3 null panels |
| 5201 to 5220 | marks, planted_3.50 |
| 5301 to 5320 | description, planted_2.40 |
| 6001 to 6999 | decoys only; their counts are never used |

A test will fail if any of these appears in a committed results file before its step. Smoke tests run on spent seeds only, because that went wrong in `results/refit-shifts.md`.

## 8. The marks, on fresh seeds

No loosening of the counts in `results/refit-marks.md`.

| Mark | On | Pass |
|---|---|---|
| Quiet, screen | each null panel, 5101 to 5120 | gate names a lead in at most 2 of 20 (it runs at about 3% per world by construction) |
| Quiet, pipeline | same | whole pipeline passes in at most 1 of 20 (close to unfailable: gate at about 3% times tier 2 is near zero by construction, so section 6's forced-top-5 count is the real check) |
| Hears, screen | planted_3.50, 5201 to 5220 | gate names a column of a truly linked input in at least 16 of 20 |
| Hears, pipeline | same | whole pipeline passes in at least 16 of 20, with a true input among the leads |
| Sound | every row above | no more than 1 row in 20 blown or crashed; a blown or crashed row counts against "hears" on planted worlds and against both "quiet" marks on null worlds, never as a world that named nothing |

The exact binomial bound is printed beside each count, and the pooled count over the three null panels (60 worlds), with its interval, beside the per-panel counts, because at most 2 of 20 cannot tell 3% from 10%. Reported with no mark: planted_2.40, the share of leads that are decoys, the share of the generator's true rate reached, and S and raw skill on 387 to 434 as a description of what a final window that short can show.

**If a mark misses:** stop, report, no setting changes. It goes to the owner.

## 9. What this cannot detect

Stated now, before any result:

- **Effects smaller than the planted one.** Marks are at planted_3.50, a large effect. Below that, only the description row says anything.
- **Pure combinations.** The screen tests one column at a time. Two inputs that matter only together, with no effect alone, are missed, and tier 2 only combines what the screen names. This is short of the owner's "combinations nobody would have thought of" and is the first extension to put to him (pattern search or hierarchical testing, `docs/reading/maths-for-combinations.md`).
- **Effects on whole-block, whole-span totals,** as S removes them.
- **Links outside the grid of candidates:** gaps past 24 months, windows past 12, and any lead other than 3 months.
- **Links that come and go.** One that exists only before 2013 or only after 2021 fails by the design.
- **Effects confined to a few cells in a quiet block** when the statistic averages over blocks.
- **A shared driver a shift does not break,** such as a slow trend in both input and counts. shared_null tests one form; real ones may differ.
- **Direction and cause.** A pass says an input helps forecast. It does not say it causes anything, or that acting on it would accelerate or prevent an event. Reverse effects (conflict affecting prices, say) are possible for any input that is itself shaped by events. The owner's "contributing factors" can only be offered as candidates.
- **Anything beyond one outcome.** Conflict events only, with their reporting bias.
- **Anything about real data, from a pass on fake worlds.** The generator was tuned for this project.

## 10. Steps, limits and order

Each needs its own go-ahead. Tokens are fresh across both sessions, and each stop line is the estimate plus 25%. Earlier estimates here ran 3 to 5 times low on overheads, so these are set higher than they would otherwise be.

| Step | What | Tokens | Stop at | Machine | Ceiling |
|---|---|---:|---:|---:|---:|
| R0 | This revision and its audit | 150k–300k | 300k | 0 | 0 |
| R1 | Twin forecasts, limits, S, tests; on spent seeds, including 3015, 3017 and the eight false-gain shifts of 3007 and 3010 | 200k | 250k | 4 h | 5 h |
| R2 | Screen, gate, decoys; form chosen on spent seeds; calibration; **stop for the owner to set m** | 175k | 220k | 8 h | 10 h |
| R3 | Marks on fresh seeds, result, report | 125k | 155k | 13 h | 15 h |
| | **Fix and retest, total** | **500k** | | **25 h** | **30 h** |

**Next-pattern told the owner about 20 machine hours for this block; this is 25, ceiling 30, mainly from the screen on 140 worlds, the planted_2.40 description and 19 shifts in place of 16.** I have not trimmed it, since each is needed for a mark or for saying what the method cannot detect; dropping planted_2.40 saves about 2 hours.

**R1 goes on to R2 only if:** every spent row finishes; R is within 0.5 to 2 times observed on at least 18 of the 20 planted rows; all eight false-gain shifts have S under 0.02; and the three calibrated rows keep S above zero. If not, stop and report.

Machine figures are arithmetic from about 10 minutes a row and 35 minutes per 16 shifts, at two processes of three threads, `nice -n 19`. The screen's own time is a guess at 5 minutes a world, so it is timed first and stops if it projects past its ceiling. Runs are units started by next-pattern, below the live apps in the box's priority order.

**Afterwards, outline only, each its own go-ahead:**
- Up to five sources, 300k, named with reasons first.
- 1c and 1d on real data, with the review and next-pattern's result audit, about 550k, with a gate before real data.

The real-data order is the screen on 195 to 290, leads on 291 to 386, **stop for the owner**, then held-out for surviving leads only, once. No surviving leads: the held-out set stays unscored and a negative result is published.

**R0 overran:** since his yes, about 275k here and about 110k in next-pattern, about 385k against the 300k stop, by next-pattern's count, mostly the audit on a large context and the reload here. Next-pattern is telling him.

**Cap:** 7M working figure. By next-pattern's count from the transcripts Phase 1 stands at about 4.85M (here about 3.20M, next-pattern about 1.65M, Phase 0 taken off both). Everything above at estimate, with coordination, lands at about 6.2M to 6.5M, the rest in reserve. To be restated from a fresh count at each gate.

**Before 1c:** the pass rule for the real-data held-out score has to be written and committed. It is not in this revision.

**Stop doing, from the review:** more reading pages, reruns of the unchanged instrument, worth as a ruler, a second-stage g1 redoing R's correction, and anything on many real inputs before the many-column null has passed.
