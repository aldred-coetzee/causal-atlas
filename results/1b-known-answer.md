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

**Seen before the run, on a seed outside it.** A smoke test of `scripts/run_1b_second.py` on pure_null seed 9001 gave skill -0.027
(interval -0.039 to -0.010) on the main span and -0.015 (-0.030 to -0.001) on the secondary: on 159 training months, on this one seed, the
inputs cost skill on a null. No rule changes for it.

### Check before the second run: the inputs' cost on a null (decision 0018)

Committed before any of these numbers. pure_null, seeds 9001 to 9005 (9001 was already seen, -0.027), trained on 36 to 194, main span, no
shuffles; for each seed, both inputs, drought only and ONI only. `scripts/check_null_deficit.py`, results in `results/1b-null-deficit.jsonl`.

- **Five-seed mean of both inputs above -0.01:** the second run goes as committed.
- **At or below -0.01:** the settings are re-fixed. The first fixing compared settings on the baseline only, with no inputs, so it could not
  see this; here the inputs are in. Candidates (learning rate, leaves, iterations, minimum leaf; L2 stays 100): (0.05, 15, 100, 200) as now,
  (0.05, 7, 100, 500), (0.03, 7, 100, 1000), (0.05, 3, 100, 1000), (0.03, 7, 60, 2000). On pure_null seeds 2001 to 2003, same window: among those whose
  baseline deviance is within 0.005 (as skill) of the best baseline, the highest mean skill with both inputs. Same settings for baseline and test.
  Committed, then confirmed once on seeds 9001 to 9005 by the same -0.01 line.
- **Still below after that:** stop and talk. If ONI alone carries it, that is a design finding about global series as inputs, and would apply to
  the real test.

No planted panel is touched, so this cannot favour detection, and the null marks on seeds 3001 to 3020 still judge the result.

## Third design: fix the comparison, then test it (proposal, decision 0019)

Nothing here has run. next-pattern checks it first.

**The change.** Today B and M are two separate fits, so their gap holds everything that differs between two fits. Instead M becomes **B times a correction g(inputs)**: g is a small Poisson booster fitted to y/B with weight B, the
same offset for baseline and test. Its columns are the inputs, latitude, longitude and log B. **Its number of trees is chosen on a block held back from training, and may be zero, in which case M is B exactly.** So on inputs that hold
nothing, M should stay at B. B itself keeps its settings. Shuffles refit only g, which shortens the run a lot.

- **g, fixed:** learning rate 0.05, 6 leaves, up to 100 trees, minimum leaf 2000, L2 100.
- **Training:** targets 36 to 194, scored last 240 months as the committed criterion chose; mark panel 3.50. B fitted on 36 to 146 predicts 147 to 194, g is fitted on 36 to 146, and trees chosen on 147 to 194 out of sample. Then B and g are refitted on 36 to 194 with that tree count.
- **Level.** B's rate in each 5 degree block is multiplied by (observed + 50) / (predicted + 50) over the 24 months ending at the last month known at forecast time. The form and the 50 are fixed now. **This uses later observed months as a forecaster would have them,
  so it is not "from training months only".** It applies to B before g, so to both models alike. It stays only if it lowers B's mean deviance on the spent null seeds; otherwise off.

**Development, on spent seeds only.** Nulls: pure_null 2001 to 2003 and 9001 to 9005. Planted, ratio 3.00: 1010, 1012, 1015, and 1011, 1016, 1017 (worth 0.22, 0.19, 0.29). It goes on to the marks only if all 8 null seeds have skill within 0.005 in size, and at least 2 of 1011, 1016, 1017 reach
skill 0.02 with a lower bound above 0. At most two changes to g's fixed settings are allowed, each recorded. If it still fails, **we report that this method as designed cannot detect planted effects, and why**, and stop.

**Marks, on seeds never fitted (3001 to 3020), committed before they run.**

- **A, quiet.** pure_null, shared_null, combo_null, with their real-shaped inputs and again with pure noise in the same input columns (four cell-level and four global): M against B within 0.005 in size on at least 18 of 20, for each panel and each kind of input. **No planted panel runs until A passes.** If it fails, stop and talk.
- **B, hears.** planted_3.50: at least 16 of 20 detected, last 240 months, three months' lead, as in the verdict (skill at least 0.02, lower bound above 0, above all shuffles, shuffled median under 0.01). The generator's upper bound there: 19 of 20 worth 0.02, median 0.168. Nulls under the same verdict: at most 1 of 20 per panel.
  The first three seeds of each null get shuffles regardless. Secondary span (195 to 386) is reported with no mark, for the real-window choice.
- **Described, no mark:** planted_3.00, planted_2.40, planted_combo_6, by worth.

A quiet instrument can be quiet because it is deaf, which is why A alone says nothing and B is required.

**Limits carried forward.** The sentence on what a pass means and the drift limit above both stand. The mark panel is a large effect. Tree counts chosen on 48 months can miss a slow or rare effect. No result here is about real data.

**Estimate.** About 100k fresh tokens, 25% line 125k, all under the 1M of this session's own spend. Machine about 1 hour development, 2 hours A, up to 10 hours B. Cut first if time or tokens run short: planted_2.40 and planted_combo_6, then planted_3.00. Never the nulls or the mark panel.

**next-pattern's check, four edits, all before development (it approved the design subject to these):**

1. **The reference is nested too.** Without this, g could beat B with no input information, by recalibrating over place or level, and that gain would read as skill. So: R = B times g0 (columns: latitude, longitude, log B), and M = R times g1 (the same columns on R, plus the inputs), with skill M against R. Each may have zero trees. Inputs alone in g was the other option, but it could not tell linked cells from others, so an effect in 17% of cells would be diluted.
2. **Level correction, conditions.** The 24 months end at target minus lead, with an assertion and a test that no later month is read; the predicted side uses B's forecasts for those months as issued at that lead (in-sample inside training, which is a disclosed limit); kept or dropped once, on the spent null seeds; the same rule goes to real data unchanged. next-pattern accepted it: outcomes up to the forecast origin are the cell's own history.
3. **Tree-count rule, one of g's fixed settings.** At each count from 0 to 100 on the stop block, the Poisson deviance. Take the smallest count within 0.1% of the zero-tree deviance of the lowest score; a tie takes the smaller. Every shuffled refit of g1 redoes this choice by the same rule, so real and shuffled are treated alike. g0 has no inputs, so it is chosen once and shared. Anomaly means use training months only, at each of the two stages.
4. **Both shuffle schemes are reported, and the rule for choosing between them is unchanged.**

Where a replicate's tree count is zero, M is R, skill is exactly 0 and the interval is recorded as 0, 0. Code: `src/causal_atlas/nested.py`, `scripts/run_1b_third.py`, `tests/test_nested.py`. `marks` runs A, exits if A fails, and only then runs B.

**Token risk.** This session is at about 828k of the 1M, and one wake after more than an hour idle rewrites its whole context, about 120k to 150k fresh (122k at 15:31 on 2026-11-05, which my earlier 760k projection did not allow for). So A runs into B automatically, stopping itself if A fails, and waits stay under an hour, or the work resumes from `STATUS.md` in a fresh context.

## Result

Rule as it ran: commit b94c22b, with the closing rule in "How 1b closes" and the early stop in decision 0018.

### First run (20 replicates of ratio 3.00, 48 scored months, 303 training months)

- **The 16 of 20 mark is missed and was out of reach.** Detected: 1 of 20 under circular shifts (interval 0.001 to 0.249), 2 of 20 under year
  permutations (0.012 to 0.317). Only 10 of these 20 replicates are worth at least 0.02 in the scored window. The scoring window, not tokens,
  stopped this design from passing.
- **Nulls and the shuffle-scheme choice: not run** (decision 0018), so their marks have no first-run result. Other planted panels were not run.
- **By worth:** of the 8 replicates worth at least 0.05, 1 was detected under circular shifts (0.003 to 0.527), 2 under permutations. Of the 12 worth
  less, none was detected under either. Worth is an upper bound.

| Seed | Worth | Skill | Interval | Shuffled median (shift, year) |
|---|---|---|---|---|
| 1017 | 0.291 | 0.069 | 0.003 to 0.105 | -0.012, -0.007 |
| 1016 | 0.188 | 0.024 | -0.019 to 0.050 | not reached |
| 1011 | 0.221 | 0.018 | -0.010 to 0.031 | not reached |
| 1015 | 0.137 | -0.163 | -0.451 to 0.043 | not reached |
| 1005 | 0.086 | 0.008 | -0.006 to 0.019 | not reached |
| 1004 | 0.063 | 0.021 | -0.009 to 0.053 | not reached |
| 1006 | 0.057 | 0.037 | 0.003 to 0.058 | 0.001, -0.002 |
| 1007 | 0.051 | 0.016 | -0.001 to 0.037 | not reached |
| 1012 | 0.019 | 0.256 | 0.143 to 0.341 | 0.098, 0.102 |
| 1008 | 0.016 | 0.186 | 0.076 to 0.251 | 0.021, 0.018 |
| 1010 | 0.003 | 0.167 | 0.053 to 0.302 | 0.140, 0.137 |

- **This triggers the committed stop: the machinery misses replicates clearly worth 0.05 or more.** Seeds 1011 and 1016 capture a tenth of their worth.
- **A second finding, not expected:** three replicates worth under 0.02 show skill of 0.17 to 0.26, more than the generator's best possible by a
  long way, and with seeds 1010 and 1012 shuffled inputs alone reach 0.10 to 0.14; seed 1015 goes to -0.16. So the gap between two fitted models here
  can be far larger than the 0.02 margin, whatever the inputs hold. The shuffle criteria caught these: none passed. The cause is not yet known.

Worth depends on linked cells' share of the rate, not the ratio alone. Any "no" is stated as no effect worth 2% of deviance, beside the ratio and
share combinations that would have been worth that.

### The inputs' cost on a null (decision 0018's check)

pure_null, seeds 9001 to 9005, 159 training months, last 240 months scored. Skill with both inputs: -0.027, -0.001, -0.006, -0.021, -0.012, **mean
-0.0134, at or below the -0.01 line**. Drought alone: mean -0.0079. ONI alone: mean -0.0099. Neither input carries it alone, so the guess that ONI acts
as a clock is not shown. By the committed rule, the settings would be re-fixed next.

### Diagnostic on the first run's skill, committed before it runs

Seeds 1010, 1012, 1015, 1011 of ratio 3.00, first-run design and settings, `scripts/diagnose_1b_skill.py`. Asked for by next-pattern. No alternative score is tried.

- **Concentrated:** on at least 3 of the 4 seeds, removing the 10 cell-months with the largest absolute B-M deviance difference brings the size of skill below half
  its full value. The fix is then in the score or in capping predictions, not the window, and the second run as committed does not start.
- **Spread out:** otherwise. The cause is elsewhere, and we think again before spending.
- **Noise control:** B against B plus one column of pure noise. If its skill is above 0.02 in size on at least 2 of the 4 seeds, the instability is the learner's,
  and no input or window can be judged on this score whichever of the above holds.
- Also reported for the top 10: whether each has an extreme observed count or an extreme prediction from either model.

**Diagnostic result.** Skill, then without the top 10 cell-months, then the noise control:

| Seed | Skill | Without top 10 | Top 10's share of absolute gain | Noise column |
|---|---|---|---|---|
| 1010 | 0.167 | 0.112 | 0.28 | 0.054 |
| 1012 | 0.256 | 0.264 | 0.05 | 0.008 |
| 1015 | -0.163 | -0.010 | 0.45 | 0.003 |
| 1011 | 0.018 | 0.020 | 0.15 | -0.004 |

Under the rule above this is **spread out** (1 of 4 seeds concentrated, 3 needed), so my guess that a few huge counts carry it is not supported, except on seed 1015, where one cell predicted
near 0 by M against 195 to 640 observed carries most of the loss. The noise control is above 0.02 on 1 of 4, so the learner is not declared unstable by the rule, though 0.054 on seed 1010 is more than
twice the margin from a column of pure noise. The top cell-months are mixed: B predicting 141 to 265 against 0 to 9 observed on 1010, large observed counts on 1012 and 1011, M near 0 on 1015. **The
cause is not found.** By the rule, we think again before spending. Not measured: whether M and B differ in overall level; predictions were not kept.

**Level check, committed before it runs.** Same four seeds, first-run design, `scripts/diagnose_1b_level.py`. Agreed with next-pattern as the last step before the owner answers. Three marks:

- **M clearly worse in training:** M has every column B has, so on training months it should fit at least as well. Clearly worse is M's training deviance over 0.5% above B's (training skill below
  -0.005) on at least 2 of the 4 seeds, or the two models' training totals differing by more than 2% on at least 2. Either means the settings stop both models before they converge, and skill is
  measuring how far each got, not what the inputs hold.
- **Level in the scored months:** B's and M's scored totals differing by more than 5% of the observed total on at least 2 of the 4.
- **Level explains the skill:** held-out skill with each model rescaled to the observed total falls below half its size on at least 3 of the 4. This is a diagnostic only, not a proposed score.

**Level check result.**

| Seed | Training skill of M | Training totals obs, B, M | Scored totals obs, B, M | Skill | Skill, level matched |
|---|---|---|---|---|---|
| 1010 | 0.035 | 25,746, 25,726, 25,691 | 5,163, 11,579, 7,712 | 0.167 | 0.070 |
| 1012 | 0.064 | 107,930, 115,108, 116,305 | 18,145, 40,399, 18,749 | 0.256 | 0.133 |
| 1015 | 0.033 | 74,867, 75,458, 75,343 | 41,865, 36,625, 39,145 | -0.163 | -0.166 |
| 1011 | 0.040 | 58,520, 58,498, 58,433 | 24,937, 20,521, 19,895 | 0.018 | 0.021 |

- **M clearly worse in training: no, on any seed.** M fits training months 3% to 6% better than B, and totals differ by at most 1.1%. So stopping before convergence is not shown.
- **Level in the scored months: yes, on 3 of 4** (75%, 119%, 6% and 2.5% of the observed total). On 1010 and 1012 B predicts over twice what happened.
- **Level explains the skill: no, on 1 of 4** (3 needed). On 1010 and 1012 it takes about half; on 1015 and 1011 almost none.

So part of the surprise is B's level running far off on some seeds, and the cause is still only partly found: why B overshoots there, and what carries the rest, are not measured. M's 3% to 6% training gain is also larger than most of these
replicates are worth, which is consistent with overfitting the inputs, but this check does not separate the two. Four seeds, chosen because they looked odd.

The owner decided in 0019: the second run does not go ahead, and the settings re-fix falls with it.

### Second run

Not run: superseded before any fit (decision 0019).

### Third design: development result (spent seeds only; marks A and B not run)

**Outcome: the committed test to proceed was missed, so A and B did not run and seeds 3001 to 3020 are unspent.** The rule asks for this report: as designed, this method does not reach the 0.02 margin on planted effects, and the reasons are below as far as they are known. No change to g's settings was used, because the diagnostic below shows none of those tried would pass.

- **Quiet: yes.** All 8 null seeds (pure_null 2001 to 2003, 9001 to 9005) within 0.005: skill -0.0036 to -0.0001, no lower bound above 0. The first and second runs' gaps between fitted models are gone. Only pure_null, on spent seeds.
- **Hears: no.** Needed 2 of seeds 1011, 1016, 1017 at skill 0.02 or more with lower bound above 0; got 0 of 3. Skill (95% interval, worth): 1011 .0088 (.0006 to .0161, .141); 1016 .0165 (.0068 to .0275, .100); 1017 .0078 (-.0009 to .0169, .124). The others: 1015 .0152 (.0054 to .0251, .097), 1012 .0035 (-.0012 to .0101, .280), 1010 .0016 (-.0066 to .0082, .002).
- **An observation, not a result.** All 6 planted skills lie above all 8 null skills. It is 14 spent seeds, no shuffle test ran, and a lower margin chosen after seeing this would be a rule change that favours a result.
- **Level correction: kept by its rule, weakly.** It lowered mean deviance by 0.65% over the 8 nulls but was lower on only 2 of them.
- **g chose trees on nulls** (17 to 54), so "may be zero" did not happen at this tolerance; skill stayed inside the band regardless.

**Diagnostics, seeds 1011, 1016, 1017** (`scripts/diagnose_1b_third.py`, of which only the last version is kept; outputs `results/1b-third-dev-diagnostic*.jsonl`):

- Fixed tree counts 25, 50, 100, 300 and larger trees (15 leaves, minimum 500): best .0078, .0132, .0085. Handing g the generator's true linked flag: .0059, .0175, .0091. So neither tree count, capacity, nor knowing which cells are linked closes the gap.
- The reference is sound: the no-link rate beats it by only .015, .002, .002, while the full truth beats it by .154, .102, .126.
- Handing g the log of the true ratio reaches only .0117, .0177, .025. Multiplying the reference by the true ratio scores -4.7, -21.5, -13.4, because ratios reach 10^7 to 10^8 where the no-link rate is near zero. **A planted rate ratio far from 3 in these cell-months means the worth figure is not a good ruler for a multiplicative model.**
- Worth is concentrated: about 50 of 10,228 cells carry all of the net gain, and the top 12 of 240 months carry 65%, 86%, 94%.
- Most of the effect comes after training: excess events in training against scored are 391 against 20,595, 9,013 against 11,375, 2,406 against 11,737. The seed with the most in training has the best skill, on 3 seeds, so this is suggestive only.
- **Withdrawn inference.** Fitting on the scored months themselves gave .17, .11, .12, which looked as if the inputs explain the effect. Nulls score .08, .03, .15 the same way (`scripts/diagnose_1b_third_null.py`), so that fit shows nothing: the global columns can act as a month label.

**Not established:** that later episodes are the cause, that a method refitted as months pass would hear them, or that real data behaves this way. The earlier sentence about what a "no" rules out travels with this too: this says nothing yet about real effects of any size.

### How 1b closed (decision 0020)

**No result in this file is about real data.** The first design could not tell an effect from the gap between two fits. The third design is quiet (8 of 8 spent nulls within 0.005) and, with a single fit, does not reach 0.02 on effects worth 0.10 to 0.14 (0 of 3; skills 0.008 to 0.017). Marks A and B did not run, so neither its quietness nor its deafness is shown on fresh seeds.

Description only: on the 14 spent seeds all 6 planted skills lie above all 8 null skills, with no shuffle test, and a margin chosen after seeing this would favour a result.

Tokens for 1b, this session's own with its subagents: 951,058 fresh when this was written, the closing commit adding a few thousand, against the 1M ceiling; about 17.2M cache reads beside them. What the plan revision must settle is in `docs/plan-phase-1.md`.
