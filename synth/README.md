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
