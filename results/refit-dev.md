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

## Result

Not yet run.
