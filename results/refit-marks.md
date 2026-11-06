# Growing refit: marks on fresh seeds

Step 1 of the order in decision 0023. Rule committed before any number, and next-pattern checks it before it runs. Seeds 3001 to 3020 have never been fitted. They are spent by this run, once, whatever it shows. Nothing here is about real data.

## The question

The refit passed a thin development test on spent seeds (`results/refit-dev.md`). On fresh seeds, is it quiet where nothing is planted, and does it detect a large planted effect, with the gain vanishing under shuffles?

## The design under test

Exactly as run in `results/refit-dev.md`, unchanged: `src/causal_atlas/refit.py`, ten spans, 195 to 434, three months' lead, skill of M against R, mean Poisson deviance, 95% moving-block interval. No setting changes after a number.

## The marks

They are those of the third design (`results/1b-known-answer.md`, "Marks, on seeds never fitted"), committed before the refit existed. Nothing is loosened. **The margin stays 0.02.** Decision 0023 runs these before the revision settles the margin, so 0.02 is what these marks test, and a lower margin chosen after this run would be a rule change that could favour a result.

**A, quiet.** pure_null, shared_null and combo_null, seeds 3001 to 3020, each with its real-shaped inputs and again with pure noise in the same input columns (four cell-level, four global). Skill within 0.005 in size on at least 18 of 20, for each panel and each kind of input. No planted panel runs until A passes. If A misses: stop, report.

**B, hears.** planted_3.50, seeds 3001 to 3020. At least 16 of 20 detected, where detected is all three of:
1. skill at least 0.02 and lower bound above 0;
2. skill above every shuffled skill;
3. median shuffled skill under 0.01 in size.

Nulls with real-shaped inputs under the same verdict: at most 1 of 20 per panel. Each scheme, circular shift (32 shifts) and year permutation (19 draws), is judged separately. A scheme qualifies if it meets both counts. The rule for choosing is unchanged: if both qualify, circular shift; if one, that one; if neither, B misses.

**If B misses:** report it and stop. Whether anything goes ahead is put to the owner. No margin, panel or schedule is changed to reach it.

## What runs, in order

1. **Quiet pass:** the 60 null replicates, each with both kinds of input, no shuffles. Stops here if A misses.
2. **Planted pass:** the 20 planted replicates, no shuffles.
3. **Shuffles,** real-shaped inputs only:
   - the first three seeds of each null, regardless;
   - the first three planted seeds, regardless;
   - any null replicate meeting criterion 1;
   - planted replicates meeting criterion 1, but only if at least 16 of them do. Below 16, B has already missed and the remaining shuffles could not change that.

A replicate that misses criterion 1 cannot be detected, so it needs no shuffles. Shuffles refit g1 alone; R is refitted, and its total is checked against the first pass.

Also reported, no mark: skill and interval on 195 to 386, for the real-window choice.

**Two departures from the third design's marks, both to save machine time:** planted_3.00, planted_2.40 and planted_combo_6, described there with no mark, do not run. The planted shuffles stop below 16, as above. The first three planted seeds are added beyond the original, because the refit's largest open caveat is that no shuffle has run, so the owner sees whether the gain vanishes even if B misses.

## A null with many input columns

**This belongs in the plan revision, not in these marks.** Decision 0021's aim needs quietness at many inputs, and these marks show it only at 8 columns. But how many, and of what shape, depends on the sources and the revision's design, and adding it here would test a configuration this design does not have. The revision has to set one before anything is run on many real inputs.

## What it costs

- **Machine:** at this run's rate of 1.61 to 1.81 hours a shuffled replicate and about 8.5 minutes unshuffled, two processes of three threads, `nice -n 19`:
  - quiet pass about 5 hours;
  - planted pass about 1.5 hours;
  - shuffles about 10 hours if B has already missed, about 24 hours if all 20 planted seeds go through.
  - **So about 17 hours if it misses at B, about 30 at most,** less if A misses. A ceiling of 36 hours stops the run and reports.
- **Tokens:** estimate 65k fresh for the code, the check, the launch and the result; line 80k, from next-pattern's count at 18:22. A step at its line stops and says so. The run is detached and writes its outcome to `results/refit-marks.jsonl` and its log, so a cold session can pick up the result from `STATUS.md`, and nothing wakes this context while it runs.

## Limits stated now

- A pass is on a synthetic world built by a generator tuned for this project, with a large effect: planted_3.50's upper bound is 19 of 20 worth 0.02, median 0.168. It says the instrument can hear an effect of that size, not smaller ones, and nothing about real effects.
- 20 seeds bound a false-positive rate only loosely: 1 of 20 is compatible with a true rate well above 5%. Nulls also get shuffles only where criterion 1 is met, so the verdict's other two criteria are seen in full only on the first three.
- With 32 shifts, "above every shift" is p = 1/33. With 19 draws, it is p = 1/20.
- The carried limits of `results/refit-dev.md` stand: late spans choose trees on months scored in earlier spans, stage 1's level correction differs slightly from stage 2's, and refitting across a 48-month held-out block is for the revision.
- `results/refit-dev.md`'s 2 of 3 on planted_3.00 had only criterion 1 to meet, so B may well miss. That would be a result.

## Running it

Smoke test before the check, spent seed only (pure_null 2001, one draw per scheme, written outside the repo): the real-input skill and interval repeat `results/refit-dev.jsonl` to the last digit, -0.002438 (-0.004011 to -0.000884), R's total too. No fresh seed has been touched.

`PYTHONPATH=src uv run python scripts/run_refit_marks.py marks`, detached. `summary` prints the outcome from the file at any time. Writes `results/refit-marks.jsonl`.

## Result

Run from 2026-11-05 19:18 as the system unit `causal-atlas-refit-marks`, started by next-pattern after its check with no edits, because the nightly restart would stop a job launched from the session. Same command, same `nice`. **It crashed at 2026-11-06 01:31:47 CET and was not restarted. Mark A passed by count. Mark B missed. The run also raises a doubt about what skill measures, below, which questions the design. Nothing here is about real data.**

### Deviations

- **The run is incomplete.** `first planted_3.50 3015` raised `FloatingPointError` in the baseline fit, from the divergence guard in `detector.py` (`src/causal_atlas/refit.py` line 37, called from line 51). `launch` treats one failed replicate as the end of the run. Not memory: peak 6.97 GB. Planted seeds 3018 to 3020 never ran, and **no shuffle ran under either scheme**, so stage 3 did not happen. The rows are the 120 null rows and 16 planted rows.
- **The guard caught one divergence and missed a sibling.** It fires only when a prediction exceeds 10 times the largest training count. Planted 3017 passed it with R's total at 143 times the observed total.
- Nothing in the method, marks or seeds was changed, and nothing was rerun.

### Mark A: passed by count, with one large false alarm

Rows within 0.005 of zero, of 20 for each, needing at least 18:

| Null panel | Real inputs | Noise inputs |
|---|---|---|
| pure_null | 19 | 18 |
| shared_null | 19 | 18 |
| combo_null | 20 | 20 |

The largest real-input null skill is 0.0127 (pure_null 3007, interval 0.0035 to 0.0205). One null row meets criterion 1, pure_null 3007 with noise inputs: **0.1032 (0.0102 to 0.222)**, with nothing planted, nearly all from span 8 (0.3661, at 95 trees). The mark allows it as a miss, and noise rows get no shuffles under this rule. 20 seeds bound a false-positive rate only loosely.

### Mark B: missed

10 of 16 finished planted seeds meet criterion 1. If 3015 and 3018 to 3020 all met it the most would be 14 of 20, below the 16 required, and that counts criterion 1 alone. The full verdict needs the shuffles, so it counts 0 under both schemes because none ran. **Shuffled medians: none exist.** So this run does not answer whether the gain vanishes when the inputs are broken from the outcome, and the median of the 16 skills, 0.044, is not evidence for a link.

R/obs and M/obs are each model's total over the observed total, where those were read for a row; blank means not read for this write-up, and the jsonl holds them all.

| Planted seed | Skill | Criterion 1 | R/obs | M/obs |
|---|---|---|---|---|
| 3001 | 0.0012 | miss | | |
| 3002 | 0.0753 | met | 0.971 | |
| 3003 | 0.0501 | met | 0.681 | |
| 3004 | 0.0145 | miss | | |
| 3005 | 0.0343 | met | | |
| 3006 | 0.0379 | met | | |
| 3007 | 0.1449 | met | 1.73 | 1.36 |
| 3008 | 0.0644 | met | 1.078 | |
| 3009 | 0.0203 | met | | |
| 3010 | 0.3003 | met | 1.95 | 1.38 |
| 3011 | 0.0754 | met | 1.007 | |
| 3012 | 0.0100 | miss | 1.038 | |
| 3013 | 0.0075 | miss | 1.016 | |
| 3014 | 0.2915 | met | 2.58 | 1.60 |
| 3015 | crashed | | | |
| 3016 | 0.0087 | miss | 1.02 | |
| 3017 | 0.977 | miss, lower bound -0.0064 | 143 | 2.5 |

### What the rows suggest: skill may reward repairing the baseline

Untested, read from existing rows, and seen after the numbers, so it is a question for the revision and not a finding.

- Planted 3017 scores 0.977, span 10 at 0.992, because R's total is 143 times what happened. M gets near the truth by being less broken, which says nothing about hearing a link.
- The largest skills go with R overshooting: 3014, 3010 and 3007 above. Seed 3014 falls from 0.29 to 0.03 on the secondary window. Seeds where R's total is close to observed have ordinary skills or misses.
- The noise false alarm fits: pure_null 3007 has R/obs 1.263 and noise M/obs 0.78. M may gain by correcting R's level, which needs no information in the inputs.

If this holds, some of the 10 that met criterion 1 are inflated, and mark A's quiet counts do not guard against it, since they only show that R did not overshoot badly on most null rows. On nulls R/obs reaches about 1.31. An earlier idea that a few large bursts dominate pooled deviance is also still untested; this suspect is the sharper of the two.

### The doubt, checked on the same rows: mostly not supported

An independent review, requested by the owner, tried to falsify the paragraph above on the existing rows, and this session recomputed its numbers from the jsonl. All post hoc, with the calibration band chosen after seeing the numbers.

- **Skill tracks the baseline's miss only through three rows.** Spearman of skill against |log R/obs| on 16 planted rows is 0.57 (p = 0.02); without 3017 it is 0.48 (p = 0.07); without 3017, 3010 and 3014 it is 0.21 (p = 0.49). On the 120 null rows it is 0.06. On real-input nulls, M's total being closer to observed than R's goes with lower skill (-0.31), the opposite of what repair predicts. So the "some of the 10 are inflated" reading applies to those few rows, not to the instrument as a whole.
- **The instrument separates planted from null by size, without any shuffle.** With R/obs between 0.9 and 1.1, the 8 planted rows score 0.0075 to 0.0754 (5 meet criterion 1) and the 49 real-input nulls have median -0.0007 and maximum 0.0020; every planted row is above every null (Mann-Whitney p = 6e-10). Over all rows, 12 of 16 planted exceed the largest real-input null, 0.0127. This does not show the gain comes through the inputs, which only shuffles can test.
- **The noise false alarm has a sharper cause.** In pure_null 3007, span 8, the baseline's second stage took 0 trees, and M took 95 with noise inputs and scored 0.3661 on that span; the real-input twin took 0 and scored 0.0. M got a second go at a correction R declined (the mechanism is the review's reasoning from the code, not tested).
- **What these rows cannot say.** Only totals are stored, not deviances, so the share of skill from level alone cannot be computed. A burst and a broken baseline cannot be told apart here, and may be one mechanism.

### Tokens

The step's line was 80k, with 52.9k spent before launch. This session's transcripts rose about 376k between the reading check and this write-up, past that line, though much of it is not this step: the owner's questions, the sweeps, and full context re-cached on waking after idle (the last is my inference). The step's own share was not separated.
