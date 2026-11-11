# Stage B first read: rule check before any run

Independent reader, 2026-11-11. Read: `results/stage-b-first-read.md`, `scripts/run_stage_b.py`, decisions 0063 and 0064, `src/causal_atlas/finders.py` (the change in b1bf210), `src/causal_atlas/referee.py`. Ran: the finder tests (23 pass) and `check.py` in this directory, made-up tables only, smoke seeds 47990 to 47999. Nothing under `data/` was read except the text columns of the Bank's series file. No run of `places`, `years`, `planted`, `real` or `confirm`.

## Fix before the first placebo run

1. **`marks` counts rows, not seeds** (`scripts/run_stage_b.py` 238-245). Two processes started together each read `done` once at start (312) and can both run and keep the same seed, and a crash can leave one seed short. A step with one seed kept twice and one missing is reported as complete and holding: `check.py` part 2 gives 7 distinct of 8 years-moved seeds, and `marks` returns `(8, 0, True)`. The real read is unlocked on that value (325). Fix: count `len({r["seed"] for r in m} & set(SEEDS[step]))` and refuse when any seed appears twice.
2. **Every refusal is an `assert`** (287, 314, 324, 325, 332, 334). Run with `python -O`, the real read can be made twice, before the marks hold, and `confirm` can be run twice. Fix: replace each with `if not ...: sys.exit(msg)`.
3. **A gathered row can name a barred series, or the outcome itself** (`finders.py` 268-276). Barred series get `stand = -inf`, and `top` is the first m by a stable sort. If an allowed series' standing is NaN, it sorts after every barred one, so `m = most` reaches into barred series. `check.py` part 3 (seed 47990, six allowed series, one of them empty) gives `gathered 6` naming series 0, which is the outcome. The comment "never the outcome, which stands last" does not hold. The count rule probably makes this unreachable on the real table, but nothing checks it. Fix: drop a gathered row whose names are not all in `ok[o]`, or cap m at the number of finite allowed standings.

## The six questions

**1. Later years reaching the board, the referee or the choice of rows: holds.** The finders get `v[:, :, :LAST]` and `view` cuts it to `:FIRST` (`run_stage_b.py` 29, `run`; `finders.view`). Nothing from 2015 on reaches the steward or the referee, because `reading` and `run` cut at `:LAST`. Later years enter in four ways, none of them a value set against another value:
- **The count rule** (30, 77-82) keeps a place only if it has enough values in 1996-2014 and 2015-2024. That is selection on coverage.
- **Departures from the median** are per year (85-86).
- **Plant sizes** use spreads over 1961-2014 (165-185).
- **The placebo rolls** move 1996-2014 values into the finders' window, but only on broken tables.

Not checkable from code: a source's gap-filling, revision or calibration period can carry later information into earlier values. The registration names gap-filling as a limit, but not as a way for a lead to appear.

**2. Placebos fair, marks able to fail: holds as designed, with limits.**
- **Places moved** (146-153) keeps each series' memory, its gaps and links within a set. It loses which places sit together, missing values that fall together and, for a moved outcome, its neighbours. So it has less overlap and less power than the real read, which makes a false pass harder, not easier. World Bank outcomes are never moved.
- **Years moved** (155-161) keeps the places and neighbours. It adds a seam, one jump in one year for every series of a moved set, which widens the spread and lowers t.
- **The marks can fail.** By chance alone, with a 5% rate per run, the places mark fails 7.5% of the time and the years mark 5.7%. At a true rate of 20% the runs slip past 21% and 50% of the time. Passing both marks is compatible with a true rate near 10-15%.
- **The runs are not independent worlds.** They are rearrangements of one table, so there are fewer effective runs than the count says.
- **What neither placebo can detect:** a bar that is too narrow because one shock hits many groups in both sets in the same year. The registration names this.

**3. The finders change: holds.** With `allowed=None` and every member, the code paths are the same as before:
- `_post` is unchanged.
- `pairs_from_board` builds the same pairs in the same order as the old subset of products.
- The `components` guard and the `-{0}` in `gathered` matter only for degenerate tables.

With `allowed` set, `_post` (153) drops barred terms at every alignment alike, so lifts are not raised by terms that could never be sent. The one exception is fix 3 above.

**4. Ties `tied` leaves, by the Bank's own descriptions: holds as coded, leaves ties.** The rule (33-34) catches FAO-sourced series and names with "current US$" or "LCU per US$". No other dollar-named series escape it. Ties left, if these series are in the panel (I could not check membership):
- **Exchange rate, by definition:**
  - PA.NUS.GDP.PLI and PA.NUS.PRVT.PLI, price level index, defined as PPP over the market rate.
  - PX.REX.REER, real effective exchange rate, which is the nominal rate deflated.
  - TX.VAL.MRCH.XD.WD and TM.VAL.MRCH.XD.WD, export and import value indexes, "converted to U.S. dollars".
  - TX.UVI.MRCH.XD.WD and TM.UVI.MRCH.XD.WD, unit value indexes, also in dollars.
  - TT.PRI.MRCH.XD.WD, terms of trade, which is less tied because the dollar may cancel.
- **Crops, through activity data:**
  - EN.GHG.CH4.AG.MT.CE.AR5, EN.GHG.N2O.AG.MT.CE.AR5 and EN.GHG.CO2.AG.MT.CE.AR5, the EDGAR agricultural emissions. The Bank says EDGAR draws on FAO, and these cover rice and crop burning.
  - The totals that contain them, EN.GHG.CH4.MT.CE.AR5 and EN.GHG.N2O.MT.CE.AR5.
- **Not ties:** agriculture value added (national accounts), agricultural employment, and food trade shares.

Fix: add these ids to `tied`, or record by id why each is left, before the first run.

**5. Marks, refusals, seeds, `confirm`, `table` against the registration: does not hold in part.**
- **What matches:**
  - The seed lists, the marks of 2 of 20 and 1 of 8, and the seeds 58900 and 58901 (35-37).
  - The confirmation rule (248-250): above the one-row bar both ways, s > 0, at least 5 groups and 5 years.
  - `confirm` reads 2015-2024 with one proposal at a time (342).
  - Its chance rate on ten scored years is low: 0 of 80 single slope proposals confirmed on null made-up tables (`check.py` part 1). The 95% upper bound is about 4%.
- **What does not match:**
  - Fixes 1 and 2 above.
  - The real read does not require the planted runs to be done (322-329), though the registration reads a silence through them. Fix: refuse `real` until all six planted seeds are kept.
  - `table` (253-279) lists rows but does not sort them into the registration's "what counts as what". That sorting is left to hand. Say so in the results file, or add it.

**6. Planted links sized and scored as stated; what a silence rules out: holds as coded, but rules out less than stated.**
- **What is coded as stated:** the link is a share of year-to-year movement in whole groups (183, registration 80). A pass counts as heard only on a row naming exactly that input (216), which is strict.
- **The sizes are not comparable with the made-up worlds.** The worlds' share is of shock variance on a z-scored input (`synth/table_panel.py` about 190). The registration compares against those worlds at 116 ("20% to 35% of what own history leaves").
- **Input memory changes the size.** The added term is the input's past level, scaled by its yearly spread. So the same share is a far larger level effect for a series with a long memory than for one without, and what the referee hears depends on which input was drawn.
- **No link is planted on a common series** (drought, ONI), the known-answer kind.
- **Planted tables are easier than the real one.** They are places-moved tables, with less competition on the board and less overlap than the real table. So a silence rules out somewhat less than the planted runs suggest.

Fix: state the share as the plant defines it, drop or qualify the comparison at 116, and report the heard count beside the input's memory.

## Not checked

- Which series are in the panel. The panel was not loaded, so the tie list in question 4 is conditional on membership.
- Decisions 0063 and 0064 beyond what the code shows.
- The referee's bar on correlated real shocks.
- A placebo run of any kind.
- Board identity against the code before b1bf210 on a full swarm, beyond reading the diff and the passing tests.

---

*Saved by the project session from the text the reader returned; the reader's own write of this file was refused by its tooling. Line numbers are those of the code as the reader read it (b1bf210, ca32035). `check.py` is the reader's and is kept as it wrote it; its second and third parts show the faults as they stood, and give different output on the code as since changed. What was done about each finding is in decision 0065.*
