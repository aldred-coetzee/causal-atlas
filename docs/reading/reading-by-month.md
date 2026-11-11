# Reading by month: what the finders and the referee need first

Design notes for brief E of `docs/specs/2026-11-11-parallel-helpers-second-wave.md`. Made-up tables only; nothing real was read or set beside anything. **Every number here is a development number**: smoke seeds 60001 to 60999, never in a count. The work was stopped early at the coordinator's word (2026-11-11, 20:38 UTC); what is finished, half done and not started is said under each question, and the last section says where to pick up.

Code: `scripts/lab_monthly_worlds.py` (the world maker; numpy only, imported by the harness alone) and `scripts/lab_monthly.py` (part one the prototypes, part two the harness). `finders.py` and `referee.py` are imported and not edited; where a setting or the bar's draw is changed, it is changed in the lab's process and put back. Rows: `data/panel/monthly/asis.jsonl`, `ways.jsonl`, `base.jsonl`, `passed-over.jsonl`.

Worlds: 60 places in groups of five, 4 outcomes, 12 series that differ by place, 4 common to all; a yearly and a half-yearly cycle in every series, its size and timing a little different by group; each month carries 0.5 to 0.9 of the last month's departure (two common series 0.93 to 0.98); drifts, steps and spikes as in the yearly maker. Links: two a world, in half the places, onto the outcome's monthly shock. Early part 60% of the months, scored part the rest.

## 1. The finders and the referee as they are, where nothing predicts (finished, except the wandering season)

360 months, scored from month 216, 20 worlds a cell on the same seeds; for the first 5 of each also with the steward's floor taken away and 20 rows sent.

| Cell | Worlds with any pass | Floor away: rows passing, bar by single months | bar by whole years |
|---|---|---|---|
| season, months near each other | 7 of 20 | 68 of 100 | 66 of 100 |
| season, no memory | 3 of 20 | 70 of 100 | 76 of 100 |
| no season, months near each other | 0 of 20 | 0 of 100 | 0 of 100 |
| no season, memory as a yearly table | 0 of 20 | 0 of 100 | 0 of 100 |
| season, near, a same-month tie | 6 of 18 | 67 of 100 | 67 of 100 |

- **The false passes come from the season, not from the nearness of months and not from how the bar draws.** None of the referee's six baselines knows the calendar, so a driver's season a month before "predicts" the outcome's season; t from 5.7 to 14. Drawing whole years in place of single months changes nothing (stand-in for the referee's draw, `whole_years`).
- With the floor in place few rows are sent (0.5 a world), because a single series' other alignments carry the season as well and its lift stays under three. What gets through is the gathered rows of the modes family: all 10 rows sent in the 7 worlds passed. The floor hides the fault; it does not cure it.
- The season also deafens. Links of share 0.35 with the season in: 4 of 12 heard at one month's lag, 1 of 12 at three months, and 2 of 6 worlds had a pass naming nothing planted. The same links with no season: 12 of 12, nothing false.
- Not run: the cell with a season that changes size from year to year.

## 2. Three ways to read by month (steady links and nulls finished; bursts, windows and the floor-away check not started)

480 months, scored from month 288, lag 1 to 6 by seed. a0: season out, all else as counted. a1: season out, plain line at each of 1 to 6 months before, three windows of months, tails at 3 and 6 months. a2: a1 with the settings counted in years made months (`MIN_PAST` 24, `WARM` 24, `SPAN` 36, `OWN` 120, `QUIET` 12), bar by whole years. by: features of a calendar year against the next year's mean. bh: features of the twelve months to June against July to December. c: twelve tables, one a calendar month, one bar.

| Links heard (of planted) | a0 | a1 | a2 | by | bh | c |
|---|---|---|---|---|---|---|
| share 0.35, 3 worlds | 3 of 6 | 6 of 6 | 6 of 6 | 5 of 6 | 5 of 6 | 5 of 6 |
| share 0.10, 5 worlds | | 10 of 10 | 10 of 10 | 2 of 10 | 3 of 10 | 3 of 10 |
| share 0.04, 7 worlds | | 11 or 12 of 14 | 13 of 14 | | | |

| Worlds with any pass where nothing predicts a month ahead | a1 (either bar) | a2 | by, bh, c |
|---|---|---|---|
| nothing planted | 0 of 30 | 0 of 30 | 0 of 6 each |
| same-month tie | 0 of 6 | 0 of 6 | 0 of 6 each |
| season changing size by year (0.3) | 0 of 10 | 0 of 10 | not run |

- No pass named nothing planted in any linked world (15 worlds for a1 and a2, 8 for the others). In a1 and a2 the passing row is the plain line at the planted lag.
- Rows sent: a1 and a2 send 5 to 7 where something is planted and 0.2 to 0.4 where nothing is; by and bh send 12 to 30; c always sends its 40, so its bar is 3.2 to 3.8 against about 2.5.
- Seconds a world, one thread: a2 10 where nothing is planted and 14 to 16 where something is; a1 with both bars 11 to 23; by and bh 2 to 3; c 9 to 16. Data rows: (a) keeps every month; (b) keeps one row a year and needs three years before its first feature; (c) keeps one row a year in each of twelve tables with six columns for every driver.
- a0 fades with the lag (2 of 2 at four months, 1 of 2 at five, 0 of 2 at six, nothing sent): the members as counted look one and two steps back only, and hear a longer lag through the outcome's memory alone.
- The two bars gave the same passes in every a1 world; a1 and a2 differ by one or two links at share 0.04. One world at 360 months showed why a2 is preferred: a true link stood at t 12.0 and 10.8 on the two reads and 1.0 on the check against a recent line through 15 months, and failed.

## 3. The baseline to register (finished on four cells, 6 worlds each)

Mean squared error on the scored months, in units of each place's own early spread about its season, 4 outcomes a world.

| Way of saying next month | season + near | season, no memory | season changing size |
|---|---|---|---|
| the referee's six as they are | 0.91 | 1.54 | 0.86 |
| last month | 1.03 | 2.11 | 0.97 |
| the same month a year ago | 1.80 | 1.81 | 1.73 |
| the same month over all earlier years | 1.42 | 1.36 | 1.40 |
| that, with a share of last month's departure | 0.63 | 1.19 | 0.62 |
| **the six on months with the season out** | **0.61** | **0.96** | **0.59** |
| the six, season from the last eight years only | 0.64 | 1.03 | 0.62 |

**To register:** each value less the mean of the same calendar month in all earlier years (at least two; earlier dates alone, so it can be used at its own date: `season_out`), in the outcome and in every driver; then the referee's six baselines, chosen by place, on what is left. That holds the same month in earlier years, the months just before and the group's month before together, which is rule 2 by month. The six as they are leave half as much error again, and that gap is what a seasonal driver falsely "beats". All earlier years did better than the last eight even where the season's size wanders.

## 4. What a registered count would need (proposal; the size timing was not run)

- **Way:** a2. **Before it:** the season step, the month members, the whole-year draw and the month settings moved from the lab into the package with tests, the referee taking its draw and settings as arguments (an edit to `referee.py`, with the yearly counts shown unchanged); the monthly world maker moved beside the yearly one and read by an independent reader.
- **Worlds**, at the places and months of the real monthly table (not known to this work): where nothing predicts, four panels of 60 (plain, same-month tie, season changing size, gaps and late starts), mark at most 19 of 240 worlds with any pass (`at_most`); linked, steady at each lag of 1 to 6, bursts and three-month windows, shares 0.10 and 0.04, with a mark for passes naming nothing planted and marks for links heard set from smoke worlds of those kinds first. About 600 worlds.
- **Seeds:** a fresh block set aside in the ledger; none of 60001 to 60999.
- **Runtime:** measured only at 60 places by 480 months by 20 series: 10 to 16 seconds a world. If time grows with places times months, 120 places by 600 months is 25 to 40 seconds, so 600 worlds are about five hours on one core and under an hour on six. An estimate, not a measurement.

## Tried and dropped

- Reading months as they are: the season passes wholesale.
- The referee's own level of a series' past over hundreds of steps: too slow; the lab uses the finders' function, the same numbers to 4e-16.
- Forty rows with the floor away under two bars: over a minute a world; cut to 20 rows on the first 5 worlds of a cell.

## Seeds used

60001, 60002 (first tests); 60101 to 60120; 60141 to 60148; 60201 to 60203; 60211 to 60216; 60221 to 60228; 60301 to 60306; 60351 to 60356; 60401 to 60406; 60501 to 60524; 60541 to 60551 (60551 stopped unfinished). No world was made for 60106 and 60109 (same-month tie), 60142, 60144, 60216 and 60224 (linked): too few series free of drift for two links.

## Not known

- Whether the referee alone passes season-out months falsely when the floor is away, above all with a season changing size; whether the whole-year bar matters there. Zero false passes so far rests on the floor sending almost nothing.
- Bursts and three-month windows, where (b) and (c) should do best; shares under 0.04; lags beyond six months; ways (b) and (c) on more than 12 null worlds.
- Gaps, late starts, counts with many zeros, a season that shifts its timing: the maker has none.
- Time and memory at the real table's size.
- One family of made-up worlds; a real table differs in ways none of this measures.

## Where to pick up

Nothing is running. In order: (1) the lines of `data/panel/monthly/queue2.sh` from `ways burst` to the end (bursts, windows, the wandering-season cell of question 1, two sizes for timing); (2) all of `data/panel/monthly/queue3.sh` (way `a9`, the floor-away check on season-out months, written and not yet run; nulls for by, bh and c; share 0.015). One process at a time, each job detached. Then set question 4's marks for bursts and windows from what (1) gives.
