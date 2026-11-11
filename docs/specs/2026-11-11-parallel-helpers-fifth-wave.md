# Briefs for three helpers, the fifth wave: finishing what three helpers left when stopped for a restart

Written by the project session before any is started (rule 7). The owner, 2026-11-11: "Please run what you can in parallel". The first wave is `docs/specs/2026-11-11-parallel-helpers.md`; **its section "What every helper is held to" binds each helper here as written there**, and so does its last section on what the project session checks before using anything. Three at once and no more.

Each helper picks up one earlier helper's work from its notes file and its lab scripts, which are committed. The earlier brief still binds (its questions, its rules, its files, its seed range); this page says only what to do first. Estimated cost, fresh tokens, each: about 500,000; each stops and reports at 800,000. Figures reported to the owner are counted from transcripts afterwards.

## Common to all three

- Made-up tables only. Nothing under `data/raw/`, `data/table/` or `data/panel/stage-b/` is read; `results/stage-b-first-read.jsonl` is not opened. No real series is set beside another.
- `src/causal_atlas/finders.py`, `src/causal_atlas/referee.py`, `scripts/run_stage_b.py` and everything under `synth/` are read and imported, never edited.
- Smoke seeds of the earlier brief's range only, **and only seeds the notes do not list as used**; every seed used is added to the notes. Never in a count. Every number is a development number and is called one.
- At most two processes at a time for each helper, one thread each, under 2 GB each, `nice -n 19`. No job is waited on for more than about four minutes at a time: start it detached and come back to its output.
- **First, before new work: rerun the earlier helper's headline numbers on seeds it did not use**, and say plainly whether they hold. The earlier harness has had no review but its author's: read it for faults before trusting it, and say what was found.
- The notes file is brought current in place (state by question, what is recommended, what was dropped, seeds used, what is not known), two pages at most where the brief said so.

## G2. Series that keep their level (brief: `docs/specs/2026-11-11-parallel-helpers-fourth-wave.md`; notes: `docs/reading/series-that-keep-their-level.md`; seeds 61001 to 61999)

In the notes' own order. **False passes first, since they decide everything:** each way (as it is, changes, what own past does not predict, the inputs-only forms) on tables where nothing predicts and on tables where series share a slow path with no link between them: how many tables have any pass. Then heard counts on more tables, then the knobs not run, then question 5. A way that hears more and passes more is not a gain. The answer wanted: one way recommended, as a step that makes a new panel and leaves the finders and the referee as counted, with what a registered count and a second real read would need; or a plain statement that none is good enough and why.

## E2. Reading by month (brief: `docs/specs/2026-11-11-parallel-helpers-second-wave.md`, part E; notes: `docs/reading/reading-by-month.md`; seeds 60001 to 60999)

The way `a9` first (written, never run), then the rest of `data/panel/monthly/queue2.sh` from its `ways burst` line and `queue3.sh`. Then: write out exactly what would move into the package for a registered monthly count (the season step, the month settings, the referee taking its draw and settings as arguments) **as a described change and a patch file under `data/panel/monthly/`, not applied**, with a test that would show every yearly counted board and judgement unchanged; and the count's worlds, marks, seeds and runtime.

## C2. The second set of finders (brief: `docs/specs/2026-11-11-parallel-helpers.md`, part C; notes: `docs/reading/second-set-of-finders.md`; seeds 59001 to 59999, 59511 on unused)

First the reruns the notes name (the state reading on tables where nothing predicts and on slow-path tables; the common-series member on shared links at 120 places). Then what was not run: whether the additions cost hearing of the seven kinds the first set hears (`try all <kind> 120` for each, then flip_state and shared at 120 and 240), and the common-series member registered as the notes say it should be (common series taken out of the plain-line member). The change to how the referee reads a state is described and emulated only, never made. Trim the notes to two pages. Then the count's worlds, marks, seeds and runtime.
