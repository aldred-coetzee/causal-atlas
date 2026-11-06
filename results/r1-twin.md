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

Not yet run.
