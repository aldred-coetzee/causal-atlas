# The monthly read counted on made-up tables: the rule

Committed 2026-11-11 before any counted number (rule 9). Decision 0066 took the monthly read into the package, off unless asked for; this is its own count. The design and every earlier number are in `docs/reading/reading-by-month.md` and are development numbers on smoke seeds. Run by `scripts/run_monthly.py`; rows kept in `results/monthly-count.jsonl`.

## What is read

`causal_atlas.months.read` as committed with this rule: each value less the mean of the same calendar month in all earlier years (at least two); the yearly finders with the month members (lines at 1 to 6 months, three windows, tails at 3 and 6 months); the steward as counted; the referee with the month settings (`MIN_PAST` 24, `WARM` 24, `SPAN` 36, `OWN` 120, `YEARS` 120, the finders' `QUIET` 12; everything else as counted), the bar drawn by whole years, labels on. The first scored month is 360 (the first January at or after 60% of 600). The referee's draws are seeded with the world's seed.

## Worlds

Made by `scripts/lab_monthly_worlds.py` (numpy only; shares nothing with the finders or the referee): 120 places by 600 months, 4 outcomes, 12 local and 4 shared series, two links, links in half the groups, season 1.0, memory "near", all else at the maker's defaults. The planted lag is `1 + seed mod 6` months.

Seven panels of 60 worlds:

| panel | what is planted | seeds from |
|---|---|---|
| plain | nothing | 62001 |
| same_month | an input's shock enters the outcome the same month, share 0.35; nothing predicts a month ahead | 62101 |
| wander | nothing; the season's size changes from year to year (0.3) | 62201 |
| steady_10 | steady links, share 0.10 | 62301 |
| steady_04 | steady links, share 0.04 | 62401 |
| burst_10 | bursts (the input above its ninth tenth), share 0.10 | 62501 |
| window_10 | links that hold in three calendar months only, share 0.10 | 62601 |

Each panel takes its seeds in order from its start until it has 60 worlds, never past the 99th of its hundred. A seed the maker refuses makes no world, is written down and passed over. No seed of 62001 to 62999 has been used for anything.

## Heard, and a false pass

As `scripts/lab_monthly.py` `relation` and `tally` have it: a planted link is **heard** when a passed row names its outcome and exactly its input series, at any lag. A pass naming the input with something else is **part**. Any other pass is **other**. In the first three panels every pass is false, a same-month pass included.

## Marks

A missed mark is reported as missed.

- **Where nothing predicts** (the first three panels together): at most **15 of 180** worlds with any pass. Given by panel as well.
- **Heard**, of the 120 links planted in a panel: at least **90%** steady at 0.10, **75%** steady at 0.04, **80%** bursts, **70%** windows.
- **Passes naming nothing planted**: in at most **12 of the 240** linked worlds.
- Each heard share is given with a 90% interval by worlds drawn again, and by lag.

## What this does not cover

- **Gaps and late starts.** The maker has neither, and the real monthly sources have both. A real monthly read needs its own placebo runs on the real table before anything, as the yearly one had.
- Many zeros; a season that shifts its timing; shares under 0.04; lags beyond six months; links in fewer than half the groups; more than 20 series.
- One family of made-up worlds, by one maker. Holding these marks says the read is ready to be tried on a placebo of the real table, not that it finds real links.
- The marks came from development runs of the same maker on other seeds, so they are not blind to it.

## Result (counted once, 2026-11-11 22:44 to 2026-11-12 00:02 UTC)

420 worlds read, each once; 19 seeds refused by the maker and passed over (same_month 62107, 62108, 62126, 62153; steady_10 62318, 62321, 62360; steady_04 62410, 62412, 62418, 62425, 62431, 62445, 62450; burst_10 62549, 62557, 62561; window_10 62630, 62634). Rows: `results/monthly-count.jsonl`. Table: `scripts/run_monthly.py table`.

**One mark is missed.**

| mark | result | |
|---|---|---|
| where nothing predicts, at most 15 of 180 worlds with any pass | **29 of 180** | **missed** |
| heard, steady at 0.10, at least 90% | 120 of 120 (interval 100% to 100%) | held |
| heard, steady at 0.04, at least 75% | 120 of 120 (100% to 100%) | held |
| heard, bursts at 0.10, at least 80% | 120 of 120 (100% to 100%) | held |
| heard, three-month windows at 0.10, at least 70% | 94 of 120, 78% (72% to 84%) | held |
| linked worlds with a pass naming nothing planted, at most 12 of 240 | 0 | held |

By panel where nothing predicts: plain 0 of 60 worlds; season changing size 0 of 60; **same-month tie 29 of 60** (35 passes). Windows by lag from one to six months: 16 of 18, 16 of 20, 16 of 18, 16 of 22, 18 of 22, 12 of 20. Every other linked panel heard every link at every lag.

**What the miss is.** All 29 worlds are in one panel: an input whose shock enters the outcome in the same month, with nothing leading. Every one of the 35 passes names that tied input, at one month before (32) or over a window of months before (3); none names a series that is not tied. The monthly read as it stands takes a same-month tie between two series that each keep their level for a lead of one month, in about half of such worlds. The yearly count had a same-year panel and held its mark there; the monthly worlds keep their level from month to month far more than the yearly ones do from year to year.

**Described after the count, not a mark and not a rescue:** each pass carries the label of decision 0061 (whether it also stands turned round or in the same month). All 35 false passes carry it. Of the 870 passes that name exactly a planted link in the four linked panels, 24 carry it. So on these worlds the label tells the two apart, but that was seen after the numbers and no mark was set for it; treating a labelled pass as no lead is a change to be counted on its own, on seeds not used here.

**What follows.** The monthly read is not to be used on the real table as it stands. It does not invent links between unrelated series (0 of 120 worlds, and no pass naming nothing planted in 240 linked worlds) and it hears planted links down to 4% of the outcome's movement. It cannot tell a one-month lead from a same-month tie. Either the label is made part of the pass and that is counted afresh, or a monthly pass is reported only as "these two move together within a month or so".

Middle time a world 35 seconds, longest 102, one thread; about 0.5 GB a process.
