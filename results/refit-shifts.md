# Shifted inputs on six planted rows: an after-the-fact diagnostic

**Deviation from rule 9, before commit:** the smoke test used one of the six rows, where a spent seed should have been used, so one number exists: 3011 at a 2-year shift scored -0.0144 against its 0.0754, and R repeated the first pass. The rule below was written before it and not changed after it. That shift still runs and counts, and it is one of 16 on one row. Not a mark: `results/refit-marks.md` missed B and stays missed, whatever this shows. Chosen after seeing that run's rows.

## The question

When the inputs are moved in time, so that they cannot carry the planted link, does the gain on planted worlds vanish? The marks run stopped before any shuffle ran, so nothing yet shows the gain comes through the inputs.

## The design

- **Rows, chosen for what they separate, all planted_3.50 with real inputs, already run:**
  - baseline overshooting: 3010 (R/obs 1.95, skill 0.3003), 3014 (2.58, 0.2915), 3007 (1.73, 0.1449);
  - baseline calibrated: 3011 (1.007, 0.0754), 3002 (0.971, 0.0753), 3008 (1.078, 0.0644).
  3017 is left out: its 0.977 is a near-divergence, already understood well enough. The calibrated three are the largest skills with R/obs within 0.9 to 1.1.
- **Shifts:** circular only, the existing `circular_shift`, 16 of the rule's 32, every second one (2, 4, ... 32 years), so they span the same range. No permutation scheme. R is refitted once per row and must match the first pass's total, or the row fails. M is refitted per shift.
- **Score:** the same skill over the same scored months, against the row's first-pass skill. Each shift's total and trees are also stored.

## How it is read

For each row, with s its first-pass skill and x the median over its 16 shifted skills: **keeps** if x ≥ 0.5 s; **loses** if x ≤ 0.25 s; otherwise **between**.

| Reading | When | What it would mean |
|---|---|---|
| not hearing the link | at least 2 of the 3 calibrated rows keep | the gain does not depend on the inputs: stop this forecaster |
| baseline | at least 2 calibrated lose, at least 2 overshooting keep | the inputs matter where the baseline is sound, and overshoot gain is an artefact: fix the baseline |
| margin | at least 2 calibrated lose, at least 2 overshooting lose | the gain comes through the inputs everywhere: the mark, not the tool, is what missed |
| mixed | anything else | no reading: report it |

Evaluated first to last. `reading` in `scripts/run_refit_shifts.py` applies it, tested in `tests/test_refit_shifts.py`. Also reported per row: first-pass skill, shifted median and maximum, and whether the first-pass skill is above every shift (p = 1/17 at best).

## Limits stated now

- Six rows on a fake world, chosen after the numbers, with thresholds of 0.5 and 0.25 set by judgement. It steers the next step and shows nothing about real data or about any other effect size.
- These rows were picked for high skill, so some of that skill may be luck, which alone would make a row lean towards "loses". That favours "margin" and "baseline" over "not hearing the link". A "margin" reading therefore needs fresh seeds before anyone relies on it.
- A shifted input can still line up with slow patterns in the world, so "keeps" could have that cause rather than level repair.
- Skill here is pooled deviance, and each shift stores its total and not its deviance by span, so this does not separate a burst from a broken baseline.

## Running it

`PYTHONPATH=src uv run python scripts/run_refit_shifts.py run`, as a system unit started by next-pattern, `nice -n 19`, two processes of three threads, writing `results/refit-shifts.jsonl`. Restart skips finished rows; one failed row is reported and does not stop the others. **Machine: about 2 to 4 hours; ceiling 6.** Tokens: 60k line, this session and next-pattern together. Whatever the reading, it stops here for the owner.

## Result

Not run yet.
