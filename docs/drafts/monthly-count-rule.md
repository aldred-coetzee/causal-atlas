# Draft: the rule for a monthly count on made-up tables

A draft for the project session to read, change and, if it chooses, commit as a rule under `results/` before any number is computed (rule 9). It is not a rule yet and nothing has been counted under it. It follows section 5 of `docs/reading/reading-by-month.md` and makes each part of that proposal exact. Every number in it from earlier work is a development number on smoke seeds, never a count.

## What is read

The monthly read in `causal_atlas.months.read`, as on this branch: each value less the mean of the same calendar month in all earlier years (at least two); the yearly finders and the month members (lines at 1 to 6 months, three windows, tails at 3 and 6); the steward as counted; the referee with the month settings (`MIN_PAST` 24, `WARM` 24, `SPAN` 36, `OWN` 120, `YEARS` 120, finders' `QUIET` 12; `RIDGE` 20 and everything else as counted), the bar drawn by whole years, labels on. The first scored month is the first January at or after 60% of the months.

## Worlds

Made by `scripts/lab_monthly_worlds.py` at the size of the real monthly table, **120 places by 600 months**, outcomes 4, local 12, shared 4, two links, links in half the groups (`frac` 0.5), season 1.0, memory "near", everything else at the maker's defaults. The planted lag is `1 + seed mod 6`, so each lag from one to six months takes a sixth of a panel.

Where nothing predicts, four panels of 60:
1. plain: kind `none`;
2. same-month tie: kind `same_month`, share 0.35 (an input's shock enters the outcome the same month; nothing predicts a month ahead);
3. season changing size: kind `none`, `wander` 0.3;
4. gaps and late starts. **The maker has neither.** Before registration either the project session adds them to the maker (a share of series starting late, a share of months missing at random, both stated), or this panel is dropped and the null mark becomes the one for 180 worlds below.

Where something predicts, four panels of 60:
5. steady, share 0.10;
6. steady, share 0.04;
7. bursts, share 0.10;
8. three-month windows, share 0.10.

The shares of panels 7 and 8 are a choice for the project session; 0.10 is proposed because the smoke numbers for bursts and windows are on that order and nothing below it was measured for either.

A seed the maker refuses ("too many links for the series free of drift") makes no world. It is listed, and the panel takes the next seed of its block until it has 60 worlds. The list of refused seeds is reported beside the result.

## What counts as heard, and as a false pass

As in the harness `scripts/lab_monthly.py` (`relation`, `tally`): a planted link is **heard** when a passed row names its outcome and exactly its input series (any lag); a pass naming the outcome and its input with something else is **part**; any other pass is **other**. In panels 1 to 4 every pass is false, a same-month pass included. In panels 5 to 8 an **other** pass is a pass naming nothing planted.

## Marks

Committed before any count; a missed mark is reported, not explained away.

- **Where nothing predicts**: at most **19 of 240** worlds with any pass (the referee's rate of 5% a world, with about two spreads of room: 12 expected, spread about 3.4). If panel 4 is dropped: at most **15 of 180**. Also reported by panel.
- **Heard**, of the links planted in each panel (two a world, so 120 a panel): at least **90%** at share 0.10 steady, **75%** at 0.04 steady, **80%** for bursts, **70%** for windows.
- **Passes naming nothing planted**: in at most **5%** of the 240 linked worlds.
- Each heard share is reported with a 90% interval by worlds drawn again, and by lag from one to six months.

## Seeds

A fresh block, **to be named by the project session**, entered in the seed ledger before the count. It must lie outside every block used in development (59001 to 61999 and anything since). One block, taken in order, panel by panel as listed above; a refused seed is passed over as said.

## Runtime and memory on this box

Measured on this branch at 120 places by 600 months, one thread, labels on, smoke seeds (development numbers):

| world | seconds | peak memory |
|---|---|---|
| nothing planted (60946) | 32 | 0.53 GB |
| steady 0.35 (60943) | 101 | 0.53 GB |
| steady 0.04 (60957) | 40 | 0.53 GB |
| bursts 0.10 (60955) | 48 | 0.53 GB |
| windows 0.10 (60956) | 38 | 0.53 GB |

The peak is the finders' stage in every world; the referee now stays below it. Before the change on this branch the same steady world peaked at 4.9 GB (5.3 GB in the earlier reading).

So 480 worlds take about 6 to 7 hours on one core, a little over an hour on six processes of one thread each, at about 0.5 GB a process. A world where a passed mode gathers many series takes longest (its label reads each series turned round).

## Settings left in years, and why

- `RIDGE` (20) is added to a slope's sum of squares over every place and scored step, which at 120 places runs to tens of thousands; it shrinks almost nothing in a monthly read, as in a yearly one. Read with 240 in place of 20 on six smoke worlds at 60 places by 480 months (60948, 60949, 60951 to 60954), every pass and every non-pass was the same and sizes moved in the third decimal place at most. It stays 20.
- The baselines' least past (`n < 3` in `baselines` and `chances`) counts earlier values a place has, not time: three values are three values whatever the step. With the season taken out first, values begin in month 24, so it removes months 24 to 26 of each series, all before any scored month. It stays as it is; on a real table with late starts it matters only in a series' first three months.

## Not covered

- Gaps, late starts, many zeros, a season that shifts its timing (unless panel 4 is built).
- Shares under 0.04, lags beyond six months, links in fewer than half the groups.
- Two smoke seeds made no world (60950 steady, 60958 same-month); how often the maker refuses at this size is not known.
- One family of made-up worlds; a real table differs in ways none of this measures.
