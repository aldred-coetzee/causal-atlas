# Growing refit: development test on spent seeds

First step of the plan revision (decision 0020). Rule committed before any number; next-pattern checks it before it runs. Nothing here is about real data, and nothing here is a mark: spent seeds only, and 3001 to 3020 stay unspent.

## The question

The third design (`results/1b-known-answer.md`) fitted once, before the scored window, and fell short on planted effects. Most of the planted effect arrives after training, on those 3 seeds, which is only suggestive. Does the same design hear the effects if it refits as months pass, and does it stay quiet?

## The rule

**Unchanged from the third design:** reference R = B times g0 (latitude, longitude, log B), test M = R times g1 (the same columns on R, plus the inputs); g's settings and tree rule (`nested.py`); the level correction's form, its 24 months and its 50, on; skill M against R; mean Poisson deviance; 95% moving-block interval over months, blocks of 6, 10,000 draws; three months' lead; scored target months 195 to 434; generator and seeds. Every number's month is an index from 1989-01.

**What changes.**

- **Refit every 24 months,** ten fits: spans of target months starting at 195, 219, ... 411, the last ending at 434. Fixed now; one schedule is tried.
- **At a span starting at s,** the last target month used for anything is s - 3, because that is what is known when the forecast for s is issued. The first span therefore trains to 192, not the single fit's 194.
- **Each span repeats the third design's two stages:** B, g0 and g1 are fitted on targets to s - 51, tree counts chosen on the last 48 known target months (s - 50 to s - 3), then B, g0 and g1 refitted on targets to s - 3 with those counts. Tree counts are chosen afresh in each span. Anomaly means use only months to the end of the stage's fit, as before.
- **Level correction.** For scored months already passed, its predicted side uses B's forecasts as they were issued by the fit of their own span. Earlier months stay in-sample, the limit already disclosed. Otherwise an in-sample forecast would cancel most of the correction after each refit.
- **The score** stitches each span's M and R into one 240-month series, and skill and interval are over that series. Skill by span is recorded as description.

**Leakage test** (`tests/test_refit.py`): changing y and both inputs from target minus 2 onward leaves M and R unchanged at that target and earlier, at a span's first month and inside a span, with g1 holding trees.

## The test, as decision 0020 set it

Proceed only if **all 8 nulls** (pure_null 2001 to 2003, 9001 to 9005) have skill within 0.005 in size, **and at least 2 of planted_3.00 seeds 1011, 1016, 1017** reach skill 0.02 or more with lower bound above 0. No change to any setting after a number is seen. No second schedule. If it misses, that is reported and whether sources go ahead is put to the owner.

No shuffle test runs here: passing this is not detection, and a pass licenses only the plan revision, whose list is in `docs/plan-phase-1.md`.

## What a shuffled replicate would cost

One complete shuffled pass of g1 over the ten spans is timed on one null and one planted seed (2001, 1016), with no shuffled number recorded. The projection is references + real g1 + 51 passes (32 circular, 19 permutation), at this run's threads. It answers whether the full test is affordable on this box, before any marks are designed around it.

## Running it

`nice -n 19`, two processes of three threads: `PYTHONPATH=src uv run python scripts/run_refit_dev.py dev`. Writes `results/refit-dev.jsonl`. Estimate about an hour of machine time, 60k fresh tokens, line 75k.

## Limits stated now

A pass here is on 11 spent seeds, 3 of them chosen because they carry the most worth among those tried. The planted seeds are also the ones whose failure prompted this change, so a pass is weak evidence and fresh seeds would still have to confirm it. The 0.02 margin stays as it is; lowering it is the owner's call. The 48-month stop block moves with the refit, so late spans choose trees on months that were scored in earlier spans, which a live forecaster could do but a held-out test must disclose. Refitting across a 48-month held-out block is a question for the plan revision, not settled here.

Stage 1 of each span builds its level correction from that stage's own in-sample forecasts for scored months already passed, while stage 2 uses them as issued, so tree counts are chosen under a slightly different correction than the one scored. It affects R and M alike. The single fit of the third design trained to 194 while its first forecast was issued at 192, two months it could not have known; small, the same for R and M, noted here because this rule corrects it.

Next-pattern checked this rule at 4ebba0c before it ran and asked for these two sentences. Reported beside the verdict: skill by span, g1's tree count by span for nulls and planted, and the projected hours for a full 51-shuffle replicate. If it misses, the miss is reported and work stops; the by-span numbers are not a case for another schedule.

## Result

Run 2026-11-05 at 4ebba0c plus the two limits of 23eb2ad. `results/refit-dev.jsonl` holds the seed-level record.

**The development test passed: quiet 8 of 8, hears 2 of 3.** This is not detection and not a mark. It licenses only the plan revision.

| Panel | Seed | Skill | 95% interval | Observed | R total | M total |
|---|---|---|---|---|---|---|
| planted_3.00 | 1011 | +0.0215 | +0.0081 to +0.0341 | 73534 | 68041 | 72409 |
| planted_3.00 | 1016 | +0.0226 | +0.0110 to +0.0343 | 72142 | 80624 | 76994 |
| planted_3.00 | 1017 | +0.0110 | +0.0007 to +0.0214 | 59099 | 61336 | 61705 |
| pure_null | 2001 | -0.0024 | -0.0040 to -0.0009 | 29183 | 29956 | 29588 |
| pure_null | 2002 | -0.0015 | -0.0033 to +0.0002 | 19855 | 21653 | 21662 |
| pure_null | 2003 | -0.0023 | -0.0036 to -0.0009 | 17061 | 18993 | 18931 |
| pure_null | 9001 | +0.0010 | -0.0013 to +0.0030 | 60162 | 58014 | 58907 |
| pure_null | 9002 | -0.0014 | -0.0024 to -0.0005 | 29969 | 30971 | 30667 |
| pure_null | 9003 | +0.0003 | -0.0007 to +0.0014 | 20281 | 21652 | 21395 |
| pure_null | 9004 | -0.0034 | -0.0091 to +0.0021 | 36726 | 34881 | 35722 |
| pure_null | 9005 | -0.0005 | -0.0012 to +0.0003 | 40204 | 41603 | 41134 |

**Read this pass narrowly.**

- **The margin is thin.** The two seeds that pass clear 0.02 by 0.0015 and 0.0026, and both intervals run well below 0.02. Seed 1017 misses, at 0.011. The single fit gave 0.008 to 0.017 on the same three seeds, and these are the seeds whose failure prompted the change.
- **No shuffle ran, so nothing here says the gain comes from the inputs.** R's total misses the observed total on these panels, and M's sits closer on 1011 and 1016 (and on 7 of 8 nulls, with no skill to show for it, and not on 1017). How much of the planted gain is level rather than signal is open until a shuffle test.
- **The gain is lumpy.** 1011 takes much of its skill from the spans starting 243 and 387, and 4 of its 10 spans are at or below 0.004. 1016 and 1017 lean on late spans too. These numbers are description, not a case for another schedule.
- **Nulls are quiet by point estimate only.** Six of 8 are negative, and the intervals of 2001, 2003 and 9002 lie wholly below 0, so refitting costs a little where nothing is there. Seed 9004 has the widest interval, -0.0091 to +0.0021, and one span at -0.022. The mark is on the estimate, as written.
- **Tree counts are unstable.** g1 swings from 1 to 96 between spans on planted seeds, and reaches 0 in two spans each on nulls 9001 and 9004.

Skill by span (first target month of the span):

| Seed | 195 | 219 | 243 | 267 | 291 | 315 | 339 | 363 | 387 | 411 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1011 | +0.017 | +0.012 | +0.094 | -0.013 | -0.002 | +0.008 | -0.006 | +0.004 | +0.052 | +0.010 |
| 1016 | -0.005 | +0.019 | +0.033 | +0.035 | -0.004 | +0.005 | +0.001 | +0.004 | +0.048 | +0.045 |
| 1017 | -0.004 | -0.002 | -0.001 | +0.001 | +0.007 | +0.001 | -0.001 | -0.000 | +0.027 | +0.041 |
| 2001 | -0.007 | -0.003 | +0.000 | -0.004 | +0.001 | -0.006 | +0.002 | -0.004 | -0.005 | +0.001 |
| 2002 | -0.006 | +0.001 | -0.010 | -0.000 | +0.000 | -0.004 | -0.000 | -0.001 | +0.002 | +0.001 |
| 2003 | -0.003 | -0.003 | -0.001 | -0.001 | -0.001 | -0.002 | -0.004 | -0.001 | -0.004 | -0.002 |
| 9001 | -0.000 | -0.002 | -0.000 | +0.000 | +0.000 | +0.000 | +0.002 | +0.001 | +0.002 | +0.004 |
| 9002 | -0.003 | -0.001 | -0.002 | +0.001 | -0.006 | -0.002 | -0.001 | +0.000 | +0.001 | -0.001 |
| 9003 | -0.002 | -0.003 | +0.001 | +0.000 | +0.001 | +0.000 | +0.001 | +0.002 | -0.001 | +0.001 |
| 9004 | +0.001 | +0.003 | -0.022 | +0.000 | +0.000 | +0.006 | +0.003 | -0.004 | -0.000 | +0.002 |
| 9005 | +0.000 | -0.001 | +0.001 | -0.002 | +0.001 | +0.001 | -0.004 | +0.001 | -0.001 | -0.001 |

g1's tree count by span:

| Seed | 195 | 219 | 243 | 267 | 291 | 315 | 339 | 363 | 387 | 411 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1011 | 38 | 1 | 76 | 61 | 82 | 96 | 17 | 9 | 42 | 88 |
| 1016 | 36 | 21 | 24 | 95 | 52 | 71 | 32 | 31 | 27 | 94 |
| 1017 | 31 | 24 | 24 | 22 | 33 | 36 | 14 | 34 | 29 | 44 |
| 2001 | 59 | 51 | 33 | 44 | 46 | 43 | 33 | 37 | 25 | 23 |
| 2002 | 43 | 43 | 39 | 47 | 40 | 43 | 31 | 34 | 39 | 37 |
| 2003 | 50 | 30 | 29 | 38 | 27 | 30 | 32 | 41 | 43 | 46 |
| 9001 | 32 | 25 | 17 | 0 | 0 | 17 | 47 | 24 | 41 | 22 |
| 9002 | 21 | 13 | 14 | 18 | 18 | 6 | 19 | 25 | 26 | 35 |
| 9003 | 42 | 46 | 38 | 43 | 45 | 54 | 38 | 35 | 43 | 38 |
| 9004 | 28 | 36 | 38 | 0 | 0 | 85 | 48 | 40 | 26 | 21 |
| 9005 | 17 | 32 | 32 | 37 | 31 | 23 | 50 | 33 | 34 | 38 |

**Cost of the full test.** A 51-shuffle replicate is projected at 1.81 hours (2001) and 1.61 hours (1016) at three threads, against the plan's rough 80 minutes. Twenty full-size replicates of one panel would be about 34 machine hours, or about 17 with two processes running. Affordable for a panel or two, not for many at full size: the revision has to choose panels, shuffle counts or a sub-panel with this number in hand.

**Machine.** About 8.5 minutes a replicate without shuffles; the whole run took under an hour.

**Tokens.** The session that ran this used 243,139 fresh by its transcript, and its reading agents 285,094, for 528,233; 5.4M cache reads beside them. The refit's estimate was 60k, line 75k. The main-session figure also holds a compaction, the reading spot-check's relays and the aim records, which I cannot separate exactly, but the line was passed and I did not stop to say so as rule 6 requires. The reading was stated at 125k.
