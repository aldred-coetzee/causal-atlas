# Series that keep their level: why a planted link is not heard, and a way to hear it

Notes of helpers G and G2 (briefs: `docs/specs/2026-11-11-parallel-helpers-fourth-wave.md`, `...-fifth-wave.md`). Made-up tables only; every number is a development number on smoke seeds and none is a count. Nothing real was read or set beside anything. Code: `scripts/lab_level_worlds.py` (the maker of tables; numpy only) and `scripts/lab_levels.py` (the ways and the harness; `finders.py` and `referee.py` imported and not edited). "Heard" means a planted link passed from the board; counts are given as 35% / 20% / 10% links.

## State by question

**1. Does it happen on a made-up table? Yes, and it holds on rerun.** Tables shaped like the real yearly panel (166 places, 18 groups, 64 years: 35 seen, 19 scored; 120 series; a third missing; memory by series 0.58 to 0.97, middle 0.87). On 16 fresh tables, 144 links, as it is: **heard 0 / 0 / 0 of 48 each**; answer handed over, passed 4 / 0 / 0; answer sent alone 15 / 3 / 0. (G's six tables: 0 heard, 0 handed over, 0 alone.) The lesser t, middle 2.6 / 2.0 / 1.0 under a bar of middle 4.5.

**2. Which difference does it? The outcome's memory, with the baseline.** The baseline takes about three quarters of what was added (0.28 left; G: 0.26), because the outcome's last value already holds it; what is left goes with the input's change at 0.71 and its level at 0.43. One thing changed at a time on a clean table of 40 series, 4 tables, 12 links a size, heard as it is (and as changes):

| setting | as it is | as changes |
|---|---|---|
| all series at 0.9 | 2 / 0 / 0 | 11 / 7 / 0 |
| inputs at 0.3; at 0.97 | 6 / 1 / 0; 2 / 0 / 0 | 12 / 6 / 2; 9 / 8 / 1 |
| outcomes at 0.3; 0.6; 0.97 | 9 / 5 / 1; 8 / 4 / 0; **0 / 0 / 0** | 12 / 7 / 1; 12 / 9 / 2; 9 / 8 / 0 |
| all at 0.3 | 10 / 6 / 1 | 10 / 7 / 1 |
| 25 scored years | 1 / 0 / 0 | 11 / 6 / 1 |
| link in all places, not a quarter | 12 / 7 / 0 | 12 / 12 / 10 |
| no gaps | 2 / 2 / 0 | 12 / 12 / 7 |
| 120 series, all at 0.9 | 3 / 0 / 0 | 11 / 6 / 0 |

So: as it is, the read hears when the outcome forgets and goes deaf as the outcome keeps its level; the input's memory matters less; more years do not help; the quarter of places and the gaps cost the small links. Series count is not the cause.

**3. Ways to hear it.** Tables with any pass where nothing should pass (120 series):

| way | nothing predicts | shared slow paths, no link |
|---|---|---|
| as it is | 0 of 20 | 0 of 40 |
| (a) every series as its change | **1 of 40** (one row, t 2.9 and 3.2 over a bar of 2.56) | **1 of 40** (0 of 20 at the first path size, 1 of 20 at twice it; the path's own pair, labelled "together") |
| (b) every series less its own baseline | 0 of 20 | 1 of 20 (the path's own pair) |
| (a) or (b) for inputs only, outcomes kept | 0 of 1 | **2 of 4 each**, one pass unlabelled; stopped |

On 8 tables of the earlier made-up kind with no link: as it is 0, as changes 0. Heard on the 16 tables of question 1, of 48 a size: (a) **31 / 14 / 1** (handed over 39 / 31 / 12); (b) 31 / 13 / 0 (handed over 38 / 28 / 10); as it is 0 / 0 / 0. No pass by (a) or (b) on those tables named anything not planted. (c), more baselines: 0 heard on G's one table and it is not a panel step.

**What (a) loses.** Links put into what the outcome's history leaves, so that the input's level moves the outcome's new movement (40 series, all at 0.9): as it is 4 / 2 / 0 of 12, **as changes 0 / 0 / 0**, (b) 0 / 0 / 0. With inputs at 0.3: as it is 9 / 6 / 0, as changes 3 / 1 / 0. On the earlier made-up tables (links of that kind, short memory): steady 12 of 12 as it is, 9 as changes; threshold 5 and 2. On the table of 120 series with such links nothing was heard by any way (0 of 36 each; t near zero, a run not understood), and (b) passed one row naming nothing planted.

**4. To the table or to the referee?** (a) and (b) are steps that make a new panel and hand it to `view` and `judge` unchanged. (c) is not.

## Recommended

**Way (a): a step that writes a second panel in which every series, outcomes and inputs alike, is its value less its value the year before in the same place** (missing where either is missing; the first year is lost), read by the finders and referee exactly as counted, with the registered years. **As a second read beside the read of levels, not in its place**: the two hear different kinds of link, and (a) is deaf to the kind the level read hears best. Why (a) over (b): the same heard counts, one line of arithmetic against a baseline fitted series by series, and nothing taken from the referee. On the changed panel the bar falls from about 4.5 to about 3.0; that is where the hearing comes from and where the two false passes came from.

Dropped: the inputs-only forms (they pass shared slow paths in half the tables); the forms with copies beside (the same construction with more rows; not run); (c).

**5. What a registered count of (a) would need.** Worlds: nothing predicts; shared slow paths at two sizes; links as registered at 35 / 20 / 10%; links of the other kind, so the loss is counted and not hidden. Marks, set before: tables with any pass where nothing should pass (2 of 80 here; the referee's own rate is 0.05, and 80 tables cannot tell 2.5% from 7%, so 200 null tables or more); heard at 35% and 20% (here 65% and 29%); passes naming nothing planted. Fresh registered seeds, none of those below. About one minute a table at 120 series on one thread, so 300 tables is about five hours on one process; at the real 461 series, more. **A second real read** would need, before it: the step written and tested as its own script, its panel and manifest entry; a rule committed first that says the two reads are counted together (two reads double the chance of a false pass); the placebo runs and planted runs of the first read redone on the changed panel; the years held back still unopened.

## Not known

- Whether 2 of 80 is the rate or luck; nothing here bounds it below about 7%.
- Which kind of link the real table has more of. If the other kind, (a) adds little.
- Why no way heard the other kind on the table of 120 series; that path of the harness was run once and not checked.
- Monthly panels, late starts, the 461 series, and tied series were not tried.
- The table's settings were chosen on one seed; its memory tops at 0.97, the real at 1.00.
- A fault was found and mended in the harness (a shared path's pair was never recognised, so such a pass would have been counted as "other"); it was mended before any path table ran. The harness has had no review but its authors'.

## Seeds used

G: 61001 to 61006, 61011 to 61014. G2: 61021 to 61037 (question 1 and the ways; 61031 for the check of the copied `plant`), 61041 to 61048 (the knobs and the other kind of link), 61101 to 61140 (nothing predicts), 61201 to 61240 (shared paths), 61301 to 61304 and 61311 to 61318 (the earlier made-up tables). Outputs, one row a table, under `data/panel/levels/` (not committed): `r0, e4, e5, n1, n2, n3, p1, p2, p3, q_*, s_*, x_*` and the lane lists as started.
