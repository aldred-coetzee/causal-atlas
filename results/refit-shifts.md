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

Run by next-pattern as `causal-atlas-refit-shifts` from a16a9a8, 2026-11-06 02:05 to before 03:50 CET, exit 0, all six rows, 16 shifts each, about 2,000 to 2,200 seconds a row. R matched the first pass on every row. The smoke test's number repeated: 3011 at 2 years, -0.014. **The rule's reading: margin. All six rows lose. This is about planted_3.50 on a fake world, on rows chosen after the numbers; nothing here is about real data.**

| Row | R/obs | First-pass skill | Shifted median | Shifted min to max | Above every shift | M/obs, shifted median | State |
|---|---|---|---|---|---|---|---|
| 3010 overshooting | 1.953 | 0.3003 | 0.0017 | -0.0048 to 0.1803 | yes | 1.961 | loses |
| 3014 overshooting | 2.577 | 0.2915 | -0.0015 | -0.0118 to 0.0064 | yes | 2.585 | loses |
| 3007 overshooting | 1.728 | 0.1449 | -0.0019 | -0.0148 to 0.1348 | yes | 1.731 | loses |
| 3011 calibrated | 1.007 | 0.0754 | -0.0048 | -0.025 to 0.0027 | yes | 1.02 | loses |
| 3008 calibrated | 1.078 | 0.0644 | 0.0007 | -0.0029 to 0.0068 | yes | 1.081 | loses |
| 3002 calibrated | 0.971 | 0.0753 | -0.0048 | -0.0172 to 0.0027 | yes | 0.96 | loses |

Each row's skill is above all 16 of its shifts, p = 1/17 for that row at best.

**What it supports.** On these rows the gain goes away when the inputs cannot carry the link, so it came through the inputs. That includes the overshooting rows: with shifted inputs M's total stays at R's, while with the true inputs it came down (3014: 1.60 against R's 2.58). So the correction of the overshoot itself used the inputs, which goes against the "repair needing no information" suspicion for these rows.

**What the median hides, seen after the numbers.** The overshooting rows are not clean. 3007 has 6 of 16 shifts at 0.085 or more (0.132, 0.085, 0.109, 0.104, 0.093, 0.135), and 3010 has 2 (0.137, 0.180), all with inputs that carry no aligned link. The rule reads medians, so it calls these "loses", correctly by the rule, but gains that large from unlinked inputs mean a broken baseline can still hand out a large false gain. It is the same size and kind as the noise false alarm in `results/refit-marks.md`. No calibrated row shows it (largest shift 0.0068). So "margin" is the reading, and the baseline's blow-ups still need fixing.

**What it does not say.** The planted rows that missed the mark (0.0012 to 0.0145) were not tested, so nothing shows their small gains are real. Mark B stays missed. The rows were picked for high skill, so the limit above applies: fresh seeds are needed before anyone relies on this. Permutation was not run.

Tokens: about 3.9M of 7M across both sessions, my estimate from next-pattern's 3.64M at 01:41 plus the review and this step, not a fresh count.
