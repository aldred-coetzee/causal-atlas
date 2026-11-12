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

## Result

Not yet run.
