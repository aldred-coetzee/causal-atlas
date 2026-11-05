# 1b: known-answer test

**Rule, committed before any number, from `docs/plan-phase-1.md` as amended by decision 0013.**

**Question.** Can the 1d machinery find a planted link, and stay quiet where there is none?

**Shape.** The real outcome panel is built from UCDP GED 26.1, `where_prec` 1 to 3, by month of
`date_start`, on 10,228 cells over the 399 target months and the 36 months of warm-up before them.
These statistics come from training months (1992-01 to 2017-03) only: size, share of zeros, lag-1
and lag-12 autocorrelation, seasonal amplitude, spatial clustering, share of events in the top 1%
of cell-months, regional episode length. No validation or held-out month is used.

**Generator.** In `synth/`, imports nothing from `src/` (a test enforces this), committed before any
detector code. Written by one Sonnet subagent, about 100k fresh tokens, from a written spec holding
the shape statistics and the panel list, forbidden from opening the plan or `src/`. The mechanism is
a self-exciting negative binomial count process over a latent spatial rate, with threshold input
effects over distributed lags the author chooses, in only some cells.

**Panels,** with synthetic inputs shaped like the real ones, with multi-year persistence:
planted at rate ratios per standard deviation of input of 1.05, 1.15 and 1.40; a pure null with large
multi-year regional episodes unrelated to the inputs; and a shared-driver null, as the pure null plus
a seasonal driver and slow regional trend shared by input and outcome, with no link.

**Detector.** Exactly 1d's: baseline B and M1 as the plan defines them, with the same split, metric,
interval and verdict. M1's settings are frozen at B's during shuffles. The verdict for a replicate
needs all three: (1) skill at least 0.02 and the lower end of its 95% block-bootstrap interval above 0;
(2) under circular shift, skill above all 32 shifts; under year permutation, above all but at most 0
of 19 draws, which tests criterion 2 only coarsely, at 1 in 20; (3) the median shuffled skill under
0.01 in size. Bootstrap draws: 10,000.

Deviations already named: the 19 draws above; the sub-panel below; and the tuning grid, fixed at B's
default settings for the synthetic runs if runtime requires it, which would then be stated here.

**Replicates.** 20 per panel, each through the full pipeline with both schemes, with the oracle's
skill (the generator's own true rate) reported. One replicate per panel runs at full size, the other
19 on a contiguous sub-panel of 2,000 cells. Disclosed departure from the brief's "same size".

**Pass, or stop, for each scheme.** Detection at least 80% at ratio 1.40 (16 of 20). False positives
at most 1 of 20 on each null, with the exact binomial upper bound printed beside the count. Criterion
1's false-positive rate is reported alone, as the check on the interval. The 1.15 result is reported
and shows what 2% means. If both schemes qualify, the circular shift is used for 1d; if one, that one;
if neither, 1b fails.

**Runtime.** Ceiling 24 hours in total, `nice -n 19`, at most 6 threads. One fit of each size is
timed first; if the projection exceeds the ceiling, this stops and reports at a gate rather than
cutting replicates unasked.

**Scope.** No real input is joined to any real outcome in this step. PCMCI and CCM do not run.

## Shape statistics

From `scripts/shape_1b.py`, on the 303 training months only. Of 74,836 African events, 64,108 have
`where_prec` 1 to 3, and of those 1,852 (2.9%) fall in no cell, most plausibly on coasts, and are not
counted. This loses them for both models alike, and is a limit of the 0.5 degree land mask.

```json
{
 "cells": 10228,
 "train_months": 303,
 "mean_events_per_cell_month": 0.009703189716703387,
 "share_zero": 0.9952873171556499,
 "variance_over_mean": 24.75412242299987,
 "share_cells_ever_event": 0.2100117324990223,
 "max_cell_month": 609,
 "lag1_autocorr": 0.372282093764698,
 "lag12_autocorr": 0.06061486921204898,
 "share_events_in_top_1pct_cell_months": 1.0,
 "share_events_in_top_0.1pct_cell_months": 0.558910578298028,
 "share_events_in_top_0.01pct_cell_months": 0.21379402081739882,
 "share_events_in_top_1pct_cells": 0.5500981011605867,
 "seasonal_amplitude_peak_over_trough": 1.9856777493606137,
 "morans_i_log_cell_totals": 0.5552260008073991,
 "regional_blocks_5deg_with_events": 81,
 "episode_months_median_p90_max": [
  1.0,
  4.0,
  46
 ],
 "spei_anom_sd": 0.9361472474946902,
 "spei_lag1_autocorr": 0.7088933951384633,
 "spei_lag12_autocorr": 0.041756612122708675,
 "spei_corr_by_distance_deg": {
  "0-2": 0.9114188862354697,
  "2-5": 0.6373585145760436,
  "5-10": 0.33760215839923186,
  "10-20": 0.13439311056206057,
  "20-40": 0.023089710833414143
 },
 "oni_sd": 0.8455399105356792,
 "oni_lag1_autocorr": 0.9718425038320302,
 "oni_lag12_autocorr": -0.033338325531170734
}
```

The plan's "share of events in the top 1% of cell-months" is 1.0 here, because under 1% of cell-months
hold any event, so it says nothing. The two finer shares are added.

## Stop before the detector: the planted effects are worth less than the margin

Found on 2026-11-05 by checking the generator, before any detector code existed and with no real
input joined to any real outcome. "Best possible skill" is 1 - D(true rate) / D(true rate without
the link), the generator's own truth, over months 36 to 434, median of 6 seeds. It is measured one
month ahead on the generator's conditional rate. Skill at a 3-month lead is likely lower, not higher.

| Ratio per SD past the threshold | As written (about 15% of cells, 1 SD threshold) | All cells, 1 SD threshold | All cells, no threshold |
|---|---|---|---|
| 1.40 | 0.0006 (0.0002 to 0.0054) | 0.0055 | 0.050 |
| 2.00 | 0.014 (0.005 to 0.046) | 0.065 | 0.287 |
| 3.00 | 0.216 (0.128 to 0.385) | 0.358 | 0.522 |

So criterion 1 needs skill 0.02, and at the plan's strongest ratio even the truth reaches about 0.0006.
The pass mark of 80% detection at 1.40 cannot be met by any method on this design. At 1.40 the link
raises total events by 0.8%. These ratios and their worth depend on the generator's design, which is
one author's choice, so they illustrate the margin and do not measure it for real conflict data.

**Generator fit, six seeds, median against real, in training months.** Mean 0.0175 against 0.0097 (one
seed to the next: 0.0087 to 0.0231), zeros 0.9936 against 0.9953, variance over mean 13 against 24.8,
cells ever with an event 0.155 against 0.210, lag-1 0.39 against 0.37, lag-12 0.107 against 0.061, top 0.1%
share 0.54 against 0.56. Its author reports longest episode 17 months against 46 on one seed, so the
nulls may be easier than the real data. Returned `rate` is not capped where the draw is, which spoils
oracle skill at very high rates only.

## Result

Not yet computed. Waiting for the owner.
