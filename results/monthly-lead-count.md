# The monthly read counted again: a pass is a lead only when its label does not say "together"

**The rule.** Written 2026-11-12 with `scripts/run_monthly_lead.py` and `tests/test_monthly_lead.py`, and committed before any counted seed. Decision 0068. Made-up tables only; no real series is read.

## Why

The first count of the monthly read (`results/monthly-count.md`) missed one mark: where an input moves the outcome in the same month and nothing leads, the read took the tie for a one-month lead in 29 of 60 worlds. Described after that count, and not a mark there: every one of the 35 false passes carried the label of decision 0061 (the pass also stands turned round, or is as strong read in the same month), and 24 of the 870 passes naming a planted link did. That was seen after the numbers, on seeds now spent, so it settles nothing. This count asks the question on unused seeds with the marks set first.

The real monthly series also start late and have holes, and the first count's tables had neither. Two panels here have both.

## What is changed, and what is not

- **A lead** is a pass whose label says the two series do not move together. A pass with the label, or with no label, is reported as **moving together within a month or so** and is not a lead. This is the wording decision 0061 already gave the label; what is new is that the count's marks are on leads.
- The monthly read itself (`src/causal_atlas/months.py`), the finders, the steward, the referee and the label's own thresholds are untouched. The maker is the first count's (`scripts/lab_monthly_worlds.py`), unchanged, with the same sizes: 120 places, 600 months of which the last 240 are scored, links in half the places, at one to six months by the seed.
- **Gaps** (`gaps` in the runner, applied after the maker): a third of each series' places start up to ten years late; half lose a run of one to twelve months, three times over; three in a hundred of all months are missing singly. About 8% of values in all.

## Worlds

Eight panels of 60 worlds, seeds taken in order from the first of each hundred, a seed the maker refuses passed over. Block 65001 to 65899, entered in `results/seed-ledger.md` with this rule.

| panel | what is in it | first seed |
|---|---|---|
| plain | nothing predicts | 65001 |
| same_month | an input moves the outcome in the same month, share 0.35; nothing leads | 65101 |
| same_month_gaps | the same, with gaps | 65201 |
| steady_10 | a steady link, share 0.10 | 65301 |
| steady_04 | a steady link, share 0.04 | 65401 |
| burst_10 | a link in bursts, share 0.10 | 65501 |
| window_10 | a link over a window of three months, share 0.10 | 65601 |
| steady_10_gaps | a steady link, share 0.10, with gaps | 65701 |

## Marks

1. **Where nothing predicts** (plain, same_month, same_month_gaps; 180 worlds): at most **9** worlds with any lead.
2. **Heard as a lead** (a planted link named exactly by a lead), of all links in the panel: steady_10 at least **85%**; steady_04 at least **70%**; burst_10 at least **75%**; window_10 at least **60%**; steady_10_gaps at least **70%**.
3. **Linked worlds with a lead naming nothing planted:** at most **12** of 300.

Reported beside the marks, not marks: worlds with any pass of either kind; links heard by any pass; leads by months before; time.

## What follows from each outcome

- **Every mark holds:** the monthly read may be used on the real monthly table under its own rule, a lead being a pass without the label, and a labelled pass reported only as moving together.
- **Mark 1 missed:** the label does not separate a tie from a lead; the monthly read reports every pass as "moving together within a month or so" and no monthly pass is called a lead until another way is counted.
- **A hearing mark missed:** the read may still be used with that weakness said beside any silence; if it is the panel with gaps, a real monthly read says so first.

## What this does not cover

Ties at other distances than the same month (an input that moves the outcome inside the month but is recorded a month late would be a true lead by the record). Series of counts that are mostly nought. Shared slow paths between monthly series beyond the maker's shared series. More than about 8% missing. Counted once; never run again.

## Result (counted once, 2026-11-12, 03:25 to 04:34 UTC)

480 worlds read, each once; 32 seeds refused by the maker and passed over (listed by `scripts/run_monthly_lead.py table`). Rows: `results/monthly-lead-count.jsonl`. Never to be run again.

**Every mark holds.**

| mark | result | |
|---|---|---|
| where nothing predicts, at most 9 of 180 worlds with any lead | **0 of 180** | held |
| heard as a lead, steady at 0.10, at least 85% | 117 of 120, 98% (interval 95% to 99%) | held |
| heard as a lead, steady at 0.04, at least 70% | 116 of 120, 97% (94% to 99%) | held |
| heard as a lead, bursts at 0.10, at least 75% | 120 of 120 | held |
| heard as a lead, three-month windows at 0.10, at least 60% | 98 of 120, 82% (76% to 88%) | held |
| heard as a lead, steady at 0.10 with gaps, at least 70% | 117 of 120, 98% (95% to 99%) | held |
| linked worlds with a lead naming nothing planted, at most 12 of 300 | 0 | held |

Beside the marks. The same-month tie still draws passes: 28 of 60 worlds without gaps (34 passes) and 15 of 60 with gaps (19 passes). **Every one of those 53 passes carries the label, so none is a lead.** Plain tables had no pass of either kind. Of 1,134 passes naming a planted link exactly, 52 carry the label; the label cost 3, 4 and 3 links in the three steady panels (heard by a pass, not as a lead) and none elsewhere. Leads naming part of a planted link (one of its series, or a row holding it): 50 worlds. Windows by months before, one to six: 18 of 22, 17 of 18, 14 of 18, 16 of 22, 18 of 22, 15 of 18. Middle time a world 38 seconds, longest 102, one thread.

**What follows.** The monthly read may be used on the real monthly table under its own rule, committed first: a lead is a pass without the label; a labelled pass is reported as two series moving together within a month or so. On made-up tables of this kind it then called no tie a lead in 120 worlds, invented nothing in 60 plain ones, and heard steady links down to 4% of an outcome's movement, with about 8% of values missing and late starts making no difference seen.

**Limits.** As listed under "What this does not cover". The tables are this maker's: 16 series, 120 places, fifty years of months. The real monthly table has far more series, shorter records, counts that are mostly nought, and many more than 8% missing in some sets; its own placebo and planted runs are what will say what a real monthly read can hear.

## Deviations

None.
