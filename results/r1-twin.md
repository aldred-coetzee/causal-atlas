# R1: twin forecasts, limits and the level-free score, on spent seeds

Step R1 of `docs/plan-phase-1-revision.md`, go-ahead in decision 0031. Rule committed before any number. **Spent seeds only, so this is development: it is not a mark, and it shows nothing about real data.**

## The question

Do the changes in sections 1 and 2 of the revision stop the blow-ups and the false gains, without losing the gain on the rows where the baseline was sound?

## What runs

`src/causal_atlas/twin.py`, ten spans, 195 to 434, three months' lead, each row's own 8 input columns, tree counts 25, 50 and 100 read from one fit.

- planted_3.50, seeds 3001 to 3020. These include 3015 (crashed), 3017 (143 times observed) and the three calibrated rows.
- pure_null, shared_null, combo_null, seeds 3001 to 3005. Reported, no condition.
- pure_null 3007, with its own inputs and with noise inputs: last time's false alarm at 0.1032. Reported, no condition.
- The eight false-gain shifts: planted 3007's six and 3010's two, chosen from `results/refit-shifts.jsonl`, at or above 0.08, which takes the one just under 0.085. Same years, same world.

The main window is 195 to 434, the same ten spans as the earlier results these rows are compared with. It includes months that will be held out on real data, but these are fake worlds, so nothing real is seen. S on 291 to 386, the revision's tier 2 window, is reported beside it.

## The tree count

The smallest of 25 and 50 at which each of 3011, 3002 and 3008 keeps at least half its S at 100 trees; otherwise 100. This picks t on three planted rows, so for power. It is frozen here, and the null side is measured later on fresh seeds. `choose_trees` applies it.

## Go on to R2 only if

At that tree count, `gate` applies all of:

1. Every row above finishes.
2. R is within 0.5 to 2 times observed, over 195 to 434, on at least 18 of the 20 planted rows.
3. All eight false-gain shifts have S under 0.02.
4. The three calibrated rows have S above 0.

If not: stop and report, no setting changes. Going on still needs his go-ahead to R2.

## Also reported, no condition

Raw skill and interval beside S; S per span; M/obs and R/obs; rows and spans flagged `blown`; the share of cell-months where the factor clip and the cap act; the share of R's D from span-blocks with fewer than 5 events; the old skill on the same rows from `results/refit-marks.jsonl`.

## Departures from the plan's text

- **Noise row and null rows added** to what section 10 lists, because the false alarm in `results/refit-marks.md` is exactly what this should stop. Neither has a condition, so neither can decide anything.
- **The cap's "at or above" count** in `cap_share` is on B times the clipped factor, before g. The final forecast is bounded again after g, with the same cap.
- **The generator's true rate is not scored here.** It is a description for R3.

## Limits stated now

- All these rows have been seen, and some were chosen for what they showed. A good result here is permission to test on fresh seeds and nothing more.
- The limits (1/4 to 4, twice the block's past maximum, 5 times the trailing total) are judgement sized to the failures seen on these same seeds, so they are expected to look good on them.
- One effect size only. Eight shifts only, so this does not measure how often false gains occur; R2's calibration does that.

## Running it

`PYTHONPATH=src uv run python scripts/run_r1.py run`, as a system unit started by next-pattern, `nice -n 19`, two processes of three threads, writing `results/r1-twin.jsonl`. Restart skips finished rows. **Machine: estimate 4 hours, ceiling 5.** Tokens: estimate 200k, stop at 250k, both sessions.

## Result

**The gate passes: "go on", checked against the raw rows. Spent seeds, limits sized on these same failures, so this is permission to test on fresh seeds and shows nothing about real data.** Started 2026-11-06 11:09 CET, ended 12:36, about 1.5 hours against 4 estimated. No row failed: 37 rows, 36 jobs plus the noise row. Read with `scripts/run_r1.py summary`.

**Tree count: 25.** 3011, 3002 and 3008 keep 0.61, 0.55 and 0.61 of their S at 100 trees. Frozen by the rule, and it costs power: median planted S is 0.0234 at 25 trees and 0.0368 at 100.

| Condition | Needed | Result, 25 trees |
|---|---|---|
| Every row finishes | all | all |
| R within 0.5 to 2 times observed | at least 18 of 20 | 20 of 20, range 0.68 to 1.12 |
| False-gain shifts, S | all 8 under 0.02 | all 8, largest 0.0154 (3007, 32 years); old skill 0.085 to 0.180 |
| Calibrated rows, S | all above 0 | 3002 0.0190 (0.0039 to 0.0345), 3008 0.0280 (0.0126 to 0.0424), 3011 0.0416 (0.0248 to 0.0543) |

**The faults this was built for, no condition:** 3015 now finishes. 3017's R/obs goes from 143 to 0.99, its old skill 0.977 to S 0.0336 (0.0007 to 0.0535), raw 0.088. Pure_null 3007 with noise inputs goes from 0.1032 to -0.0091 (-0.0161 to -0.0020).

**Over 195 to 434, no condition:** planted, 16 of 20 have S at least 0.005 with the interval's lower end above 0; 3001, 3009 and 3016 show nothing clear, and 3015 has S 0.0148 with the lower end below 0. Real-input nulls, 16 rows: median -0.0014, largest 0.0002, none at 0.005. The cap acts on at most 0.22% of cell-months in a span, the factor clip on at most 12.4%. Span-blocks with few events give at most 2.3% of R's deviance.

### Two things the gate does not check

**1. The `blown` flag is measuring surges, not blow-ups.** It fires on 4 of 20 planted rows and on no null row, and at all three tree counts. Section 8 allows 1 in 20, so as written R3 would be expected to miss its Sound mark. A post hoc look, on the same seeds with nothing changed (`scripts/run_r1_blown.py`, `results/r1-blown.txt`, 25 trees):

| Seed, span | Trailing 24 months | Limit | Observed | R | M |
|---|---|---|---|---|---|
| 3010, 387 | 7,272 | 36,360 | 93,210 | 54,358 | 60,456 |
| 3015, 267 | 8,168 | 40,840 | 98,319 | 52,489 | 59,484 |
| 3017, 387 | 6,495 | 32,475 | 110,564 | 38,154 | 67,122 |
| 3018, 219 | 17,756 | 88,780 | 108,756 | 136,038 | 138,008 |

In all four the events themselves exceed the limit, and the forecast is below them in three and 1.25 to 1.27 times them in the fourth. The flag compares the forecast with the past only, so a forecast that sees a real surge coming gets marked as broken. Changing it is a rule change that could favour a result and is the owner's.

**2. R3's window looks short of power.** On 291 to 386, the window of tier 2, 9 of 20 planted rows have S at least 0.005 with the lower end above 0 and raw above 0, against 16 needed (11 of 20 at 50 and at 100 trees). Null rows: 0 of 16, largest S 0.0012. This is not a test of the tier 2 pass: M here has all 8 inputs rather than the screen's leads, and the conditions on spans and shifts are not applied. Fewer noise columns could help; those two conditions can only take rows away. The screen is untested, so this does not say R3 fails. It says expect a miss on "Hears, pipeline" unless the screen changes this.
