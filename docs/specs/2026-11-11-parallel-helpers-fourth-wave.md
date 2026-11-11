# Brief for one more helper, the fourth wave

Written by the project session before it was started (rule 7). The owner, 2026-11-11: "Please run what you can in parallel". The first wave is `docs/specs/2026-11-11-parallel-helpers.md`; **its section "What every helper is held to" binds this helper as written there**, and so does its last section on what the project session checks before using anything. Never more than three helpers at once: G starts in the place F left.

Estimated cost, fresh tokens, the helper's own estimate: about 600,000; it stops and reports at 900,000. Figures reported to the owner are counted from transcripts afterwards.

## G. Series that keep their level: why a planted link is not heard on a table like the real one, and what would hear it (design)

**The decision it serves.** The first read across the real table (`results/stage-b-first-read.md`) has its placebo runs in: with places moved round, 0 of 20 tables had any pass; with years moved round, 0 of 8. The finders and the referee do not pass noise on real series. But on the same tables with links planted, at the time of writing (four of six runs in, 36 links at 35%, 20% and 10% of the outcome's year-to-year movement), **no planted link was heard from the board, and none passed even when the answer was handed to the referee.** On made-up tables the same finders and referee heard 52 to 60 of 60 links of each of seven kinds (`results/finders-stage-a2.md`). So a quiet real read will say little, and before a second rule for a real read is written, the project needs to know what makes the difference and what reading would hear such a link without passing noise.

**What is known of the planted runs** (from the registered rows; the helper does not open them):

- The real yearly panel: 461 series, 166 places in groups, 64 years. The finders see the first 35 years, the referee scores the next 19, the last 10 are kept back. Many series have gaps or begin late.
- Each link is planted by `plant` in `scripts/run_stage_b.py` (read it): the outcome gains a multiple of the input the year before, in whole groups holding a quarter of the places (42 to 57 places), sized so that the year-to-year changes of what is added are the stated share of the outcome's year-to-year movement there.
- The inputs keep their level: each input's one year goes with the next at 0.67 to 1.00, middle 0.89. Every one of the 36 is above a half.
- Of 36 links, the board sent 1 to the referee. Handed the answer, the referee gave scores of mostly 1 to 3 (two ways of reading each) where the bar over forty rows stood at 3.9 to 5.2, and the gain over the baseline was a few per cent (middle 0.03 to 0.04 at 35% and 20%, nothing at 10%).
- The made-up tables that heard nearly everything: forty series, 60 years (35 seen, 25 scored), 120 to 480 places, links sized as a share of what the outcome's own history leaves.

**Questions, in order:**

1. **Make it happen on a made-up table.** Build made-up tables with the real panel's shape (about 166 places in groups, 64 years split 35, 19 and 10, a few hundred series or as many as time allows, series that keep their level at 0.7 to 0.99, some drifting, gaps and late starts) and plant links the way `plant` does. Do the finders and the referee as they are go deaf there too? If not, say what the made-up table still lacks.
2. **Say which difference does it.** Change one thing at a time on those tables and report what is heard: how long the input keeps its level; how long the outcome does; 19 scored years against 25; a quarter of the places against all; the number of series (rows posted, and so the bar); the way the size is stated (a share of year-to-year movement against a share of what own history leaves). Show where the link goes: taken by the baseline (the place's own history already carries a slow-moving addition), stopped by the bar, or never sent by the board.
3. **Ways to hear it, each prototyped.** At least these, and any other the helper judges worth it: (a) both series read as their change from the year before; (b) each series first reduced to what its own past does not predict, then read; (c) levels kept, the baseline given more of the place's own slow movement. For each: links heard of those planted at 35%, 20% and 10%; and, on tables where nothing predicts **with the same level-keeping series, and on tables where two series share a slow path with no link between them** (the trap a reading of drifting series falls into), how many tables have any pass. A way that hears more and passes more is not a gain; say so plainly.
4. **Whether it can be done to the table and not to the referee.** The referee is counted and is not to be changed. Can the way recommended be a step that makes a new panel from the table (changes, or what own past does not predict), leaving `finders.py` and `referee.py` exactly as counted? If not, what is the smallest thing that must change, and what would have to be counted again?
5. **What a registered count for the recommended way would need:** worlds, marks, seeds, runtime on this box.

**Rules particular to G:**

- Made-up tables only. Nothing under `data/raw/`, `data/table/` or `data/panel/stage-b/` is read, and `results/stage-b-first-read.jsonl` is not opened: what is needed from it is above. No real series is set beside another.
- `src/causal_atlas/finders.py`, `src/causal_atlas/referee.py`, `scripts/run_stage_b.py` and everything under `synth/` are read and imported, never edited. A maker of worlds the generator cannot make goes in `scripts/lab_level_worlds.py`, sharing no code with any prototype that proposes or scores; only the harness imports it (rule 3).
- Smoke seeds 61001 to 61999 only, each one used listed in the notes file. Never in a count. Every number is a development number and is called one.
- At most two processes at a time, one thread each, under 2 GB each, `nice -n 19`; outputs under `data/panel/levels/`. No job is waited on for more than about four minutes at a time: start it detached and come back to its output.

**To write:** `scripts/lab_levels.py` (prototypes and harness), `scripts/lab_level_worlds.py` if needed, `docs/reading/series-that-keep-their-level.md` (two pages at most: what was found on each question with its counts, the way recommended with its settings, what was tried and dropped, the seeds used, what is not known).
