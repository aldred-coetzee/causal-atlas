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

## Amendment to the rule (decision 0015), before any detector result

Disclosed departures from the rule above. The first table in the previous section sets nothing: the
generator is fixed first and the worth of each effect re-measured.

- **Planted panels.** After the fix, the three ratios are chosen so that the median best possible skill
  is about 0.01, 0.02 and 0.05, on the fixed generator and before any detector exists. The plan's 1.05,
  1.15 and 1.40 are reported for their best possible skill only.
- **Each panel reports** its ratio, the share of cells it affects and its best possible skill.
- **Pass mark.** Detection at least 80% on the panel worth about 0.05. The nulls' mark is unchanged.
- **The 2% margin** stays in the verdict here, and the owner sets the final margin later, with this result.

## The fixed generator, and what each effect is worth

Measured 2026-11-05 on the final generator, before any detector code exists. No real input is joined
to any real outcome.

**Fit, six seeds, median against real, training months.** Pure null: mean 0.0142 against 0.0097 (one
seed to the next: 0.0061 to 0.0278), zeros 0.9953 against 0.9953, variance over mean 17.4 against 24.8,
cells ever with an event 0.12 against 0.21, lag-1 0.29 against 0.37, lag-12 0.087 against 0.061, largest
cell-month 436 against 609. Shared-driver null: much the same (mean 0.0148, cells ever 0.14). The
multi-year persistence that was missing now mostly exists: 5 degree block-year autocorrelation at lags 1,
2, 3 and 5 is 0.55, 0.37, 0.28, 0.11 against the real 0.63, 0.43, 0.30, 0.16.

**Known misfits, kept and disclosed.** Events sit in too few cells (0.12 against 0.21) and persist a little
less than real ones, so the nulls may be somewhat easier than real data, and a false-positive rate here
may understate the real one. Calibration stopped here on cost.

**Worth of each ratio.** Best possible skill as defined above, 20 seeds (101 to 120, not used for
replicates), months 36 to 434, about 15% of cells linked. The sub-panel is the 2,000 cells nearest the
median latitude and longitude of the land cells (9.25, 20.25), generated at that size.

| Ratio | Sub-panel: 10th pct, median, 90th | Replicates at 0.02 or more, of 20 | Full panel: 10th pct, median, 90th | At 0.02 or more, of 20 | Rate lift, full |
|---|---|---|---|---|---|
| 1.05 | -0.0001, -0.0000, 0.0001 | 0 | -0.0000, -0.0000, 0.0001 | 0 | 1.000 |
| 1.15 | -0.0002, -0.0000, 0.0002 | 0 | -0.0000, 0.0001, 0.0001 | 0 | 1.001 |
| 1.40 | -0.0001, 0.0005, 0.0028 | 0 | 0.0000, 0.0002, 0.0034 | 0 | 1.005 |
| 2.00 | -0.0001, 0.0065, 0.0478 | 6 | 0.0014, 0.0082, 0.0293 | 6 | 1.033 |
| 2.40 | -0.0000, 0.0186, 0.1477 | 8 | 0.0040, 0.0375, 0.1272 | 15 | 1.082 |
| 3.00 | -0.0000, 0.0693, 0.2877 | 13 | 0.0224, 0.0746, 0.2573 | 18 | 1.184 |
| 3.50 | -0.0000, 0.1983, 0.4256 | 13 | not run | | |
| 4.00 | -0.0000, 0.0783, 0.4431 | 14 | not run | | |

**Ratios fixed for the planted panels: 2.00, 2.40, 3.00,** worth about 0.01, 0.02 and 0.05 to 0.07. The
ratio per SD past a 1 SD threshold is large because the effect only acts in some cells and some months.

**A ratio does not have one worth.** Median worth is not even monotonic in the ratio on the sub-panel.
What sets a replicate's worth is whether the linked cells happen to be busy: at ratio 3.00 the Spearman
correlation between best possible skill and the linked cells' share of the no-link rate is 0.85 on the
sub-panel and 0.82 on the full panel, and that share runs from 0 to 0.83 although always about 15% of
cells are linked. In 5 of 20 sub-panel replicates the linked cells hold under 2% of the rate. The metric
sums over events, so an effect in quiet cells scarcely counts, whatever its size.

**The amended pass mark cannot be met as written.** On the sub-panel, which is 19 of each panel's 20
replicates, at most 14 of 20 replicates are worth 0.02 at any ratio tried up to 4.00, and criterion 1
needs 0.02. So 80% detection (16 of 20) is out of reach for any method. This is a design finding and not
yet a detector result.

## Second amendment (decisions 0015 and 0016), before any detector result on a planted panel

- **All 20 replicates run at full size.** One fit takes about 7 to 9 seconds at 10,228 cells, not the minutes
  assumed, so the 2,000-cell sub-panel is dropped and with it the departure from the brief's "same size". The
  pass mark is unchanged at 16 of 20, on ratio 3.00 (full panel: median worth 0.075, 18 of 20 worth at least
  0.02, one month ahead). If a timed full replicate projects past the 24 hour ceiling, this stops and reports.
- **Learner settings.** The plan's default-style settings diverge: on null panels, predictions reach 1e54,
  because a rare huge count against a tiny base rate gives an enormous Newton step. Six settings were compared
  on two pure-null seeds (2001, 2002) at both sizes, on synthetic validation months only, with no input in the
  model. Fixed: learning rate 0.05, 15 leaves, 100 rounds, L2 100, at least 200 rows per leaf; skill against a
  constant rate 0.555 to 0.568 at full size, where B0 reached 0.413 to 0.439. Skill differences among the stable
  settings were under 0.01. No per-model tuning grid runs here. `fit_predict` now stops loudly if a fit diverges.
- **Interval.** 95%, as in this file's rule, since one comparison is made per replicate.
- **B0** is reported beside B on held-out months, without the extra validation fit 1d would use.
- **A multi-input panel and its null are added** (decision 0016): reported, with no pass mark of their own
  beyond the nulls' mark for the null. Their ratio is fixed from best possible skill before they meet the detector.
- **Detection is also reported by best possible skill** in that replicate, because a ratio has no single worth.

## The rule as it runs (third amendment), committed before any detector fit on a planted panel

This replaces the panel list, ratio and mark above wherever they differ. The numbers that moved it are the
generator's own truth, never a detector's: the only detector fit so far is on a pure null, for timing, and
its result is not counted. The commit that holds this section is named under Result.

**Summary to carry everywhere.** Worth depends on the linked cells' share of the rate, not on the ratio alone. A
"no" is stated as "no effect worth 2% of deviance", beside the ratio-and-share combinations that would have been.

**Lead.** Three months, the primary lead. Worth is `lead_rates` from the generator: Monte Carlo forward simulation
with inputs known through the target month, so an upper bound (6 paths, about 4% error on one check; 24 paths gave
0.1143 against 0.1096). It exceeds one-month worth because the link's feedback through self-excitation is in the gap.

| Panel | Worth at 3 months: 10th pct, median, 90th (seeds 101 to 120) | Worth 0.02 or more | Role |
|---|---|---|---|
| planted, ratio 2.00 | 0.003, 0.012, 0.048 | 6 of 20 | reported |
| planted, ratio 2.40 | 0.007, 0.055, 0.176 | 16 of 20 | reported |
| planted, ratio 3.00 | 0.036, 0.116, 0.334 | 18 of 20 | **pass mark** |
| planted_combo, ratio 6 | 0.015, 0.143, 0.331 | 17 of 20 | reported, no mark |

**The mark moved, and this favours passing.** Decision 0015 put 80% on the panel worth about 0.05. That panel is
ratio 2.40, where only 16 of 20 can reach 0.02, so 80% would need every one detected. The mark is therefore on ratio
3.00, worth about 0.12 at most. Passing means the machinery finds effects of about that worth, not 0.05, and
the 2.40 and 2.00 rows say what happens below it. No panel sits at 0.02; detection by each replicate's own worth
covers that range.

**Pass, for each scheme.** At least 16 of 20 detected on ratio 3.00; at most 1 of 20 false positives on each of
pure_null, shared_null and combo_null, with the exact binomial bound. Schemes: circular shift, above all 32 shifts;
year permutation, above all 19 draws. Choice between schemes as in the rule. Seeds 1001 to 1020 on seven panels, 140
replicates at full size, each reporting ratio, share of cells, linked share of the rate and its own worth.

**Combination panel.** In linked cells the log rate gains ln(R) times the smaller of the drought and ONI excesses past
0.5 SD; alone, neither has any effect. combo_null has the same structure at R 3 on independent copies of the inputs.

**Shuffles run only where they can matter.** A timed full replicate took 29.5 minutes, partly alongside other work,
so 140 would pass the 24 hour ceiling. The verdict needs all three criteria, so a replicate failing criterion 1 is
already a no under both schemes, and its shuffles are skipped. No verdict can change and no replicate is cut. What
is lost is the shuffled distribution on those replicates, so the first 3 seeds of each null keep their shuffles
regardless. Order: ratio 3.00, the three nulls, ratio 2.40, the combination, ratio 2.00. If the ceiling is reached, the run
stops and reports which panels are incomplete. The timed replicate on pure_null seed 1001 is not counted; it is
rerun in order, with the same seed.

## The mark is out of reach in the window that is scored: found after 7 planted replicates

The third amendment counted replicates worth 0.02 over all months (36 to 434). The detector is scored only on the
48 held-out months. Checked from the generator's truth at three months, same seeds 101 to 120:

| Panel | All months, median | Held-out: 10th pct, median, 90th | Worth 0.02 or more, held-out | 0.05 or more |
|---|---|---|---|---|
| ratio 3.00 | 0.116 | -0.0007, 0.0092, 0.361 | 9 of 20 | 6 |
| ratio 3.50 | 0.229 | -0.0003, 0.047, 0.413 | 13 of 20 | 10 |
| ratio 4.00 | 0.308 | 0.015, 0.077, 0.489 | 17 of 20 | 12 |
| combination, ratio 8 | 0.254 | -0.0001, 0.0057, 0.153 | 8 of 20 | 5 |

So 16 of 20 on ratio 3.00 cannot be met by any method, and the error is this session's: next-pattern's condition
named the lead, and the window should have been checked too. **This was not found before fitting.** It was noticed from
the first replicate's own record. When it was found, 7 replicates of ratio 3.00 had finished: 1 of 7 detected
under both schemes (seed 1006), skills -0.005 to 0.037. Any restated mark is therefore made having seen those 7, and says so.

This also bears on any real test: what a true effect is worth in 48 months depends on which cells happen to be
active in those months, and it can be nothing, even where it is large over the whole period.

## How 1b closes (agreed with next-pattern, 2026-11-05)

- **The committed mark stays and is reported as missed and unreachable** (16 of 20 on ratio 3.00; 9 of 20 can reach
  0.02 in the scored window). It is not rewritten, and no second pass mark is added: a new scoring design will need its
  own known-answer test with marks defined in its scored window, committed first.
- **The nulls and the choice of shuffle scheme are reported against their unchanged marks.** That part carries over.
- **Detection is described, with no mark:** every planted replicate's held-out worth at three months from the
  generator and whether the detector passed, and "of the n replicates worth at least 0.05, k were detected" with its
  exact binomial interval. If the machinery misses replicates clearly worth 0.05 or more, that is a stop, before the plan revision.
- **Lesson for the revision:** a 48-month score depends on which cells are active in those months. Evaluate over a longer
  or rolling window, still scored once, and carry the stabilising learner settings to baseline and test alike.

## Second run: how the window is picked, committed with four of the five candidates' numbers unread

The 48 month counts (9 at ratio 3.00, 13 at 3.50) were already in this file, and the counts over all months (18 and 20) were known.
The 96 to 240 month columns had not been read.


Decision 0017. Candidates: the last 48, 96, 144, 192 or 240 target months, as one scored block.

- **Criterion.** The shortest candidate in which at least 18 of 20 replicates of ratio 3.00 (seeds 101 to 120, from
  generator truth at three months) are worth at least 0.02, with at least 120 training target months left. If no
  candidate meets it at ratio 3.00, the same test at ratio 3.50, and the mark panel moves there. If none then, stop and talk.
- **Mark.** At least 16 of 20 detected on the mark panel, in that window. Nulls as before, at most 1 of 20. Seeds 3001 to 3020.
- **Validation block.** A longer window takes in the validation months. Settings then come from the null panels, carried
  over unchanged for baseline and test alike, so no real validation is needed for tuning. No real-data skill or baseline score
  has been computed on any month; what has been seen outside training is 1a's coverage and event counts.
- **One fit, no rolling origins.** Several refits with scored months pooled would keep training length, but at least triple
  the fits on a replicate that reaches shuffles, past the 24 hour ceiling. A single fit is drift-prone, for both models alike.
- **Limit.** The window is chosen on generator truth, so it inherits the generator's assumption about how often linked cells
  are active. Before anything is scored, the real panel's count of non-zero cell-months in the chosen window is reported against the
  synthetic count, and nothing else from the real panel. If real is far sparser, this stops: the mark would not transfer.

### The window the criterion picks

Replicates of 20 worth at least 0.02, from generator truth at three months, seeds 101 to 120 (upper bound: inputs known through
the target, about 4% error):

| Last months | 48 | 96 | 144 | 192 | 240 |
|---|---|---|---|---|---|
| Ratio 3.00 | 9 | 12 | 12 | 14 | 16 |
| Ratio 3.50 | 13 | 15 | 16 | 17 | 19 |

No window meets 18 at ratio 3.00, so as committed the mark panel moves to 3.50 and the window is the last 240 target months,
2005-04 to 2025-03, indices 195 to 434. Training targets are 36 to 194, 159 months against the floor of 120 and against 303
in the first run. The criterion measures what the effect is worth, not what a model trained on 159 months can find.

**Far sparser, as a number, fixed before the count below is run:** the real panel's non-zero cell-months in the window under half
the synthetic median (planted_3.50 and pure_null, seeds 101 to 120, each taken alone).

**The count.** Non-zero cell-months in indices 195 to 434: real 21,147. Synthetic median (min to max, seeds 101 to 120):
planted_3.50 27,990 (13,251 to 53,372), pure_null 16,050 (8,558 to 25,628). Half the medians are 13,995 and 8,025, so real is not
far sparser and the run goes ahead. Nothing else was read from the real panel.

**Second-run panels, in order:** planted_3.50, pure_null, shared_null, combo_null, planted_3.00, planted_2.40, planted_combo_6.
Each 20 replicates, seeds 3001 to 3020. The three below the mark come last, so they are what gets cut if the 1M ceiling nears.
Anomaly means use months up to 194 only. Settings are `SETTINGS` in `detector.py`, unchanged.

### Before the first fit: what next-pattern's check added

**Validation's other jobs.** The plan also used the validation block for: choosing between B and B0, the tuning grids for B, M1 and
M2, 1c's calibration report, and refitting on train plus validation. In this run there is no grid and no choice of baseline, as in the
first run: B stays the baseline, B0 is reported beside it, and the final fit is on months 36 to 194 alone. On real data, the plan revision
must state the replacement from training months only. The one proposed here is B fitted on 36 to 146 against B0 on 147 to 194, for
the same displacement rule, and the same split for calibration. No tuning grid: the settings stay fixed.

**A secondary score, with no mark.** From the same fitted models, each replicate's skill, interval and verdict are also reported on
indices 195 to 386 alone, which on the real calendar is the window without today's held-out block (2021-04 on). It is evidence for the
plan revision's choice between scoring all 240 months once or keeping the last 48 unseen. The shuffle skip changes to: shuffle when
criterion 1 is met on either span. That adds fits only where the secondary alone passes. The main verdict does not change, and those
extra fits are counted and reported.

**What the mark panel is worth.** planted_3.50, last 240 months, seeds 101 to 120: 10th percentile 0.070, median 0.168, 90th 0.437; 18 of
20 at or above 0.05. It has about 1.75 times the non-zero cell-months of the pure null (medians 27,990 and 16,050).

**This sentence travels with every summary of the second run:** the mark panel is an effect that accounts for a large part of all
activity, so a pass says the machinery finds effects that large, and a later "no" on real data rules out only effects that large.

**Limit: drift.** A model trained to 2005 is scored for twenty years. The generator's fixed hot-cell fields do not move, its slow
regional component and episodes are stationary, and its reporting does not change; on the real panel, where conflict is and how
well it is reported both moved between 2005 and 2025. So a pass here does not show robustness to drift. The nearest checks: long
episodes and the slow component, unrelated to inputs, are in every panel; shared_null adds a linear regional trend shared with the
drought. None of them moves reporting or relocates hot cells.

**A miss.** If 16 of 20 is missed, including because 159 training months are too few, that is a real result. It is reported as one
and work stops there to talk to next-pattern.

## Result

Not yet computed.
