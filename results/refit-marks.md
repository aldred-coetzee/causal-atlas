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

Not yet run.
