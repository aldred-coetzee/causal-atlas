# Series that keep their level: why a planted link is not heard, and ways to hear it

Notes of helper G (brief: `docs/specs/2026-11-11-parallel-helpers-fourth-wave.md`). **Stopped early, on the project session's word, with most of the work not done.** Made-up tables only; every number is a development number on smoke seeds and none is a count. Nothing real was read or set beside anything. Code: `scripts/lab_level_worlds.py` (the maker of tables; numpy only, imports nothing that proposes or scores) and `scripts/lab_levels.py` (the ways and the harness; `finders.py` and `referee.py` imported and not edited). Both compile.

## State by question

**1. Does it happen on a made-up table? Finished: yes.** Tables shaped like the real yearly panel: 166 places in 18 groups of 6 to 15, 64 years (35 seen, 19 scored, 10 unused), 120 series (cut from 461 to keep a run near 70 seconds), a third of values missing, one year going with the next at 0.58 to 0.95 by series, middle 0.88 (the real inputs: 0.67 to 1.00, middle 0.89). Links put in by a copy of `plant` that gives the registered one's table exactly (checked on one seed). Six tables, 54 links, the finders and referee as they are: **heard from the board 0; answer handed over, passed 0; the nine answers sent alone under a bar of their own (middle 3.3), passed 0.** The lesser of the two reads' t, middle: 2.5 at 35%, 1.4 at 20%, 1.1 at 10%, under a bar of middle 4.9; gain over the baseline, middle 0.06, 0.04, 0.01. That is the real planted runs' picture. One difference not explained: the board sent 12 of 54 answers here (10 of the 18 at 35%), against 1 of 36 on the real table, which has four times the series.

**2. Which difference does it? Half done.**
- *Where the link goes (finished for the table of question 1, 54 links):* mostly **taken by the baseline**. The middle link keeps 0.26 of what was added in the baseline's error; three quarters is gone, because the outcome's own last value already holds what the input added the year before. Places used "mean with a share of the last departure" in about 63% of scored place-years and "last value" in about 33%. What is left goes with the input's **change** the year before at 0.70 and with its **level** at 0.43; the referee and the finders read the level. The bar is not the first stop: sent alone, under the lowest bar there can be, none passed.
- *How long the input keeps its level (done; the last cell short):* a clean table of 40 series, outcomes carried at 0.9, 4 tables, 12 links a size. At 35%, heard from the board / handed over / alone: input at 0.3: **7 / 9 / 11**; at 0.6: 3 / 6 / 9; at 0.9: 3 / 2 / 6; at 0.97 (3 tables, 9 links): 2 / 1 / 2. At 20%: 1 / 2 / 4; 1 / 2 / 2; 0 / 0 / 1; 1 / 0 / 0. At 10% nothing passed anywhere. So the input's memory does much of it, steadily; it is not all of it, since at 0.3 the 20% links are still mostly missed.
- *Not run:* how long the outcome keeps its level; both short; size stated as a share of what own history leaves; 25 scored years against 19; all places against a quarter; no gaps; 120 against 40 series. The clean table of 40 hears 3 of 12 at 35% where the table of question 1 hears 0 of 18: series count, drift, wandering and gaps are not yet told apart.

**3. Ways to hear it. Barely started: one table each, and no false-pass count at all.** On one table of 40 series (seed 61001; as it is: 0 heard, 0 handed over, 0 alone of 9), heard / handed over / alone, of 9:
- (a) every series as its change from the year before: 2 / 5 / 5
- (b) every series as what its own past did not predict (the referee's own baseline taken off): 2 / 5 / 5
- (a) for inputs only, outcomes kept as levels, rows may name only the changed copies: 3 / 6 / 7; may name either: 2 / 4 / 7
- (b) for inputs only, copies only: 2 / 5 / 7
- (c) levels kept, three more baselines for a place's own slow movement: **0 / 0 / 0**, as expected if the baseline is what takes the link
On one table of 120 series (seed 61001), way (a): 3 of 3 heard at 35% (as it is: 0 of 3), 0 of 3 at 20% (2 of 3 handed over), 0 of 3 at 10%.
**Not run: any table where nothing predicts, any table with a shared slow path.** No pass on the planted tables named a series not planted, which says nothing about noise. Until those are counted no way is a gain and **none is recommended**.

**4. To the table or to the referee? By construction only.** (a), (b) and their inputs-only forms are steps that make a new panel and hand it to `view` and `judge` unchanged (the inputs-only forms use the `allowed` mask `view` already takes). (c) changes the baselines and is not. Whether a panel step is enough depends on the false passes of question 3.

**5. A registered count. Not started.** Known for it: about 70 seconds a table a way at 120 series and 30 at 40, one thread.

## What to run next, in this order

All as `PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 .venv/bin/python scripts/lab_levels.py run <name> ...`, detached; `table <name>` prints the summary. **Never yet run, so untested code paths:** `--plant shock`, `--plant none`, `--paths`, `--synth`, `--years 70 --last 60`, the way `unpredicted_beside`.

1. False passes first, since they decide everything: `n1 --plant none --seeds 61101-61120 --ways asis,change,unpredicted,change_only,change_beside` and `p1 --plant none --paths 6 --seeds 61201-61220` with the same ways (120 series; about two hours each on one process).
2. Heard counts: `e3 --seeds 61002-61006 --ways change,unpredicted,change_only,change_beside,unpredicted_only,unpredicted_beside,baseline` (seed 61001 has only `change`).
3. The knobs left, each `--seeds 61011-61014 --series 40 --outcomes-from a --goes`: `--fixed a=0.9,b=0.97,c=0.97,d=0.97` for seed 61014 alone; `--fixed a=0.3,b=0.9,c=0.9,d=0.9`, `a=0.6,...`, `a=0.97,...`; all four sets at 0.3; `--plant shock` with all at 0.9, all at 0.3, inputs at 0.3, outcomes at 0.3; all at 0.9 with `--years 70 --last 60`, with `--frac 1.0`, with `--no-gaps`, with all three; all at 0.3 with `--frac 1.0`; all at 0.9 and all at 0.3 with `--series 120`.
4. Whether a way loses what was heard before: `--synth steady --years 60 --last 60 --places 120` with `--ways asis,change,change_beside,unpredicted` on a few seeds (links there are put into what the outcome's history leaves, from inputs of short memory; a changed input should carry less of such a link).

## Outputs under `data/panel/levels/` (not committed)

Every row in every file is a whole table. Whole files: `e1.jsonl` (6 tables, as it is), `t1.jsonl` (1 table, six ways), `k_base`, `k_in03`, `k_in06` (4 tables each). Cut short: `k_in097.jsonl` (3 of 4 tables), `e3.jsonl` (1 of 42 rows: way (a) on seed 61001). `knobs.sh` and `lane1.sh` there are the two lists of runs as they were started; both were stopped and no process of this helper is left running.

## Seeds used

61001 to 61006 (question 1; 61001 also for the check of the copied `plant`, for setting the table's memory, and for the one-table trials of the ways); 61011 to 61014 (the knobs). No other seed. Planned and not used: 61101 to 61120 (nothing predicts), 61201 to 61220 (shared paths), 61301 on (the earlier made-up tables).

## Not known

- Any false-pass figure for any way, so whether hearing more is a gain.
- Whether the outcome's memory, the quarter of places, the 19 years or the number of series matter beside the input's memory.
- Why the real board sent 1 answer of 36 and this one 12 of 54.
- The table's settings (memory, drift, wandering, reading error) were chosen on seed 61001 to bring the middle memory to 0.88; the real panel's top (1.00) is not reached (0.95 here).
- A fault found and mended in the summary printer only (rows written are unaffected). The harness has had no review but its author's.
