# Synthetic panel generator

`generate.py` (numpy only) implements `generate(panel, lat, lon, seed)` from `SPEC.md`.
`check_shape.py [panel] [seed] [ncells]` prints each target beside one replicate (training
months 36..338). `SYNTH_P="b0=-11.5;phi=2"` overrides parameters for tuning.
Full grid, 10,228 cells: about 2 s, 0.7 GB.

## Design

- **World is a function of (lat, lon, seed).** All spatial fields are random Fourier features, so any
  subset of cells sees the same world. Every component has its own seeded stream. A 36-month burn-in
  (inputs and counts) precedes index 0 so lags and excitation are warm.
- **Inputs, identical in all panels for a seed (shared_null adds to `drought`).**
  `drought`: spatial exp(-d/6.5) field, each Fourier mode a fast AR(1) (0.68) plus slow AR(1) (0.97, 18% of
  variance), SD 0.94. `oni`: stochastic oscillator (period about 42 months, damping 0.93) plus 12%
  persistent noise, SD 0.85.
- **Counts.** `rate = exp(link) * (mu + min(excitation, 80))`, draw = Poisson(rate * Gamma), i.e. negative
  binomial, var = m + 2.5 m^2, rate capped at 600. `mu = exp(base + season + episodes)`.
  base = three fields (scale 4 deg, 1 deg, and a thresholded "hot spot" field) so most cells are near zero
  and a few are very active. Season: amplitude 0.5 (log), phase smooth in space. Episodes: 130 long ones
  (median 30 months, radius 2-8 deg, amplitude about 1.3) plus 500 short intense bursts (median 3 months,
  radius 0.7-2.5 deg, amplitude about 4.4). Both unrelated to any input. Excitation: decaying sums
  (fast 0.5/month, slow 0.9/month) of y^0.6 in the cell, plus the 8-neighbour mean.
  Excitation uses past counts only; nothing depends on the future.
- **Planted link (`planted_R`, same design for every R, only R changes).**
  Linked cells: where a smooth random field (scale 6 deg) exceeds 1.0, about 16% of cells in
  expectation (8% to 16% in the seeds I saw), chosen independently of the base rate, so the share of
  events in linked cells is whatever it falls out as (0.33 for seed 1). Lag weights (months 0..12):
  drought `.00 .02 .04 .14 .05 .22 .18 .04 .12 .10 .02 .07 .00`, oni
  `.00 .00 .03 .02 .10 .06 .20 .08 .24 .05 .14 .00 .08`: irregular, almost nothing at lags 0-2,
  mass at 3-10, some at 11-12. The driver is the weighted sum of dryness (minus `drought`) and `oni`,
  each standardised (pooled SD in the realisation), mixed per cell with drought share alpha in (0,1)
  from a smooth field: u = sqrt(a) Ud + sqrt(1-a) Uo. Link = ln(R) * clip(u - 1.0, 0, 3): a
  multiplier R per SD above a 1 SD threshold, capped at 3 SD (max multiplier R^3). The link also
  scales the excitation term. `rate_no_link` is the same history with the link factor removed.
- **shared_null.** Adds to the drought AND the count log-rate the same seasonal cycle (same phase field;
  drought amplitude 0.7, count amplitude 0.8) and the same slow regional trend (drought 0.8, counts 0.9,
  same spatial pattern, linear in time). No path from inputs to counts.

## Fit to the targets (pure_null, seed 1; five seeds in brackets)

Matched closely or to the right order: mean count (0.023; seeds 0.009-0.023, target 0.0097), share zero,
lag-1 autocorrelation (0.40; 0.26-0.60), top 0.1% share (0.63), top 0.01% share (0.29), max cell-month
(444; 86-701), Moran's I (0.61), drought SD, lag-1, lag-12, and oni stats.
Not matched:
- **Share of cells with any event: 0.14 (0.11-0.18) vs 0.21.** Pushing it up through base-rate spread
  raised the mean and the lag-12 autocorrelation.
- **Lag-12 autocorrelation: 0.23 (0.09-0.23) vs 0.061.** Persistent hot cells and long episodes.
- **Top 1% of cells share 0.68 (0.42-0.68) vs 0.55; variance/mean 41 (7-41) vs 24.8.** The count
  tail is so heavy that one cell-month changes these by factors across seeds; single replicates are noisy.
- **Episode lengths: median 1, p90 3, max 17 vs 1, 4, 46.** Long block-level runs above twice the
  block mean did not appear. Max of 46 months was not reached.
- **Peak/trough by calendar month: 1.5 (1.1-1.5) vs 1.99.**
- **Drought pair correlation by distance: 0.82, 0.55, 0.33, 0.16, 0.06 vs 0.91, 0.64, 0.34, 0.13,
  0.02.** The exponential kernel cannot be both this steep near and this flat far.
- shared_null drought lag-1 is 0.82 (the trend and season add persistence) and its mean count is higher
  (0.036); the shared drivers were not recalibrated.
Calibration was by hand over five seeds, not an automated fit. The pure_null parameters were not tuned
for the planted panels.

## Revision (second pass, 6-seed medians on pure_null)

- `rate` and `rate_no_link` are now the means actually used for the draw (both capped at 300). Where the
  cap binds they are equal, so the ratio is below exp(link) there.
- Changes: base b0 -13.1, spread s_b 2.6, hot spots s_h 3.0, dispersion phi 4, rate cap 300, bursts weaker
  (500 -> 300, amplitude 3.0), long episodes stronger (amp 1.8), 20 very long "mega" episodes
  (median 70 months, amp 2.0) added, slow excitation 0.97/month. The link is unchanged.
- Result: see the final report. Not achieved: episode length max stays 10-17 months (target 46) in every
  seed and variant tried, including mega-episodes; I did not find why (likely Poisson gaps break runs,
  or the block mean absorbs the episode). Variance over mean is 8 (target 24.8): cutting the monster tail
  to stop mean swings costs variance. Any-event share about 0.14 (0.21). Seed spread of the mean is
  still 3x. shared_null was not tuned beyond the shared base parameters; its drought lag-1 is 0.755.
- Link feedback check (seed 2, linked cells, training months): the link raises the draw history, and
  `rate_no_link` is evaluated on that raised history, so it is not the counterfactual rate. At R=1.40
  linked cells had 10,369 events against 7,043 for the same cells in pure_null, a 1.47x total effect, but
  the mean per-month multiplier in active months is only 1.20 (rate/rate_no_link). At 1.05: 4,549 vs 7,043
  (different realisation of the nulls, so this pair is not comparable across R, treat with caution).
  The one-step multiplier is exact (exp(link)); the extra effect through self-excitation is not in
  `rate_no_link`.

## Revision 3 (slow regional component)

- Added `s_slow * field` to the count log-rate: a smooth spatial field (exp kernel, 6 deg) whose
  Fourier modes follow AR(1) at 0.98/month (85% of variance) and 0.99/month, independent of every input.
  b0 lowered to -14.4 to hold the mean. `generate` now accepts `planted_<R>` for any positive float R.
- `check_shape.py` prints the block annual-log autocorrelation at lags 1, 2, 3, 5 years (5-degree
  blocks with at least 12 training events, log1p of each whole-year total, block mean removed).
- Six-seed medians on pure_null: lags 0.55, 0.37, 0.28, 0.11 (real 0.63, 0.43, 0.30, 0.16; before
  0.49, 0.25, 0.17, 0.03). Mean about 0.011 (seeds 0.006-0.028). Cells with any event 0.12 (real 0.21):
  coverage did NOT improve, since lowering b0 to offset the slow field's mean removed small-rate cells.
  The planted panels and shared_null were not re-checked by the author after this change; the project
  session checked them on six seeds (see `results/1b-known-answer.md`).

## Revision 4 (combination panels, lead forecasts)

- `planted_combo_<R>`: same linked cells, base process and inputs as the single-input planted panels. In
  linked cells the log-rate gains ln(R) * clip(min(excess_drought, excess_oni), 0, 3), where each excess is
  the standardised lag-weighted input (same lags and weights as the single link; dryness for drought,
  ONI as is) minus a threshold of 0.5 SD. Either alone does nothing. Active in about 10.5% of
  cell-months of linked cells (seeds 101-106).
- `combo_null`: the outcome follows the same combination rule at R=3 but of independent drought and ONI
  drawn under new keys (110, 120); the returned `drought`/`oni` are the usual draws. `rate_no_link`
  equals `rate`, `linked` all False.
- Combination best-possible skill 1 - D(rate)/D(rate_no_link), months 36-434, seeds 101-106: R=2 median
  0.0009 (min -0.0002, max 0.0026); R=3 0.0035 (0.0008, 0.041); R=4 0.011 (0.002, 0.104); R=6 0.038
  (0.010, 0.230); R=8 0.143 (0.035, 0.359). combo_null vs pure_null (seeds 101-103, medians): mean 0.0103
  vs 0.0083, zeros 0.9959 vs 0.9967, variance/mean 9.0 vs 10.3.
- `lead_rates(panel, lat, lon, seed, lead=3, n_sim=6)`: forecast of y[tau] from y through tau-lead,
  inputs known through tau, by Monte Carlo forward simulation of the true process (months before 36 are
  NaN). no_link switches the link off from tau-lead+1. Lead 1 is exactly `rate`/`rate_no_link`. MC error:
  on planted_3.00 seed 101, skill 0.1096 at 6 paths vs 0.1143 at 24 paths (about 4% relative), forecast
  mean 0.01645 vs y mean 0.01612. About 16 s per seed at full size.
- Note: at lead>1 the link's feedback through excitation is part of the gap, so skill at lead 3 can exceed
  lead 1.
