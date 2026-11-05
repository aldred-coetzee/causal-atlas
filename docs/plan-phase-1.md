# Phase 1 plan: one slice, one decisive experiment

Written 2026-11-05 by the project session, before any data has been fetched or any
number computed. For audit by next-pattern and approval by the owner. Each step ends
at a gate; nothing starts without the owner's yes. Each results file copies its rule
from here and is committed before its numbers. Any later change to this rule is a
disclosed deviation.

**Nothing in this plan about a data source is a fact yet.** Coverage, licences and
access are what step 1a checks (rules 4 and 5). Sizes are rough arithmetic.

## The question, and what would answer it

Does adding lagged climate and food-price inputs improve the forecast of conflict
events in a 0.5 degree cell, three months ahead, beyond what the cell's own history,
season and neighbours already give, on a held-out period, by the margin below, with
the gain vanishing when the inputs are shuffled in time?

A "no" is an acceptable and publishable answer.

## Proposed changes to the defaults, for the owner's decision

The defaults are accepted (decision 0005). The design below departs from them in
four places, and also adds a fixed lead and margin the brief left open.

1. **Prices are tested separately from climate (H2 below), on the cells and months
   that have them.** Why: food price monitoring plausibly starts because a crisis has
   started, so whether a price exists at all may predict conflict. Pooling them would
   let a tree model use "a price exists here" as a crisis flag and report that as a
   price effect. Cost: two comparisons instead of one, so a stricter interval.
2. **Three inputs, not four.** Fewer choices, fewer ways to get lucky.
3. **Full-size synthetic panels only if the box can afford them** (see 1b). Otherwise
   a smaller repeat panel, disclosed.
4. **Baseline and test use the same learner.** So a gain cannot come from a better
   learner. The brief does not require this; it closes an obvious way to fool ourselves.

Open for the owner: the **2% margin** and the **3-month lead**. Reasons are below;
both are judgement calls and he may prefer others. Recommendation: accept both. If he
changes them, he should do so now, because they cannot change after 1c.

## Fixed rule (copied into each results file)

**Panel.** Land cells of Africa on a 0.5 degree grid with edges at whole and half
degrees, by calendar month. Roughly 10,000 cells over 30 to 35 years, so about 4M
rows (rough; measured in 1a). The grid is confirmed or challenged in 1a: if fewer
than 80% of events are geocoded to the cell or finer, this goes to the owner at the
gate rather than being worked around.

**Outcome.** y = count of UCDP GED events, all violence types, in the cell-month,
using only events geocoded to the cell or finer. Actor names are dropped at ingest,
because they are never needed and rule out person-level drift. One frozen release is
used throughout; its version goes in the manifest.

**Lead.** Forecast made with information to the end of month t, for month t+3. A
three-month lead is primary because one month ahead is dominated by persistence and
leaves little room to act, and long leads have little signal to test. Leads 1 and 6
are reported as secondary, with no verdict.

**Baseline B.** Poisson gradient boosting (scikit-learn
`HistGradientBoostingRegressor`, fixed seed) on: y at t, t-1, t-2; sums over the last
3, 6, 12, 36 months; months since the last event; the cell's mean rate to date; target
calendar month; latitude and longitude; the 8 neighbours' summed y over 1, 3, 12
months. A naive comparator **B0** (the cell's same-calendar-month mean rate over the
last 3 years, blended equally with its last-12-month rate) is scored alongside. Should
B0 beat B on the validation block, B0 becomes the baseline for the test, and that is
reported.

**Test models.** Same learner and features as B, plus inputs:
- **M1, climate, all cells (H1):** the drought index (SPEI-3 if it passes 1a, otherwise
  a rainfall anomaly from CHIRPS) as the cell's anomaly from its calendar-month mean,
  over 1, 3, 6, 12 months to t; and the ONI at t and its 3, 6, 12 month means. Anomalies
  use training months only. All lags go in; none are selected.
- **M2, prices, sub-panel (H2):** M2 adds to its baseline, per cell, the median over
  staple commodities of the 12-month log price change at the nearest market within 100
  km. Sub-panel: cell-months inside a market series' span, excluding its first 12 months
  after it starts, so that series onset is not a signal. Baseline B is refitted on that
  sub-panel. The exact staple list is fixed at the 1a gate from coverage counts, with no
  look at outcomes. If 1a shows too little coverage, H2 is dropped and H1 keeps a 95%
  interval.

**Split, by rule, not by date.** E is the last month of the frozen outcome release.
- Held-out: the last 48 target months up to E. Scored once.
- Validation: the 48 target months before that. Used for tuning and for 1c.
- Train: all earlier target months, starting after a warm-up of 36 months from the
  latest start of the outcome or the climate input.

A row is used only if its target month is in its block, so nothing from a later block
enters by the features or the anomalies. Tuning is a small grid (learning rate, leaves;
at most 6 settings) on validation, separately for each model, with the same grid. The
final fit uses train plus validation.

**Metric.** Mean Poisson deviance over cell-months. Skill = 1 - D(model) / D(baseline),
so skill 0.02 means 2% lower deviance. Poisson deviance is chosen because the outcome is
a count, mostly zero, and the score must reward a correct rate.

**Interval.** Moving-block bootstrap over held-out months, whole Africa per month,
blocks of 6 months, 10,000 draws, fixed seed. Whole months keep the spatial dependence;
blocks keep the temporal. Two comparisons, so a 97.5% interval (Bonferroni). 1b checks
empirically whether this interval is honest.

**Shuffle test.** Inputs only, in train, validation and held-out alike: permute the
years, applied identically to all cells in that draw, keeping calendar month. This keeps
each input's seasonality and spatial pattern and breaks its link to any given year's
outcome, so a gain that is only the input acting as a seasonal clock survives shuffling
and does not count. Prices permute years within each market series' span. Refit, rescore,
99 draws.

**Verdict, for each of H1 and H2, all three required:**
1. Skill at least **0.02** (2%) and the lower end of its 97.5% interval above 0.
2. Observed skill above all but at most 1 of the 99 shuffled skills, p <= 0.02.
3. The median shuffled skill is under 0.01 in size, half the margin: the gain vanishes.

**Why 2%.** A gain below that would not change anyone's reading of a forecast, and a
margin set once we can see the data is worthless, so it is fixed now on judgement. 1b
shows what size of real effect produces 2%, so at the 1b gate the owner sees what this
margin can and cannot detect before any real test.

**Secondary, reported with no verdict.** Skill at leads 1 and 6. Average precision for
onset: an event in a cell-month with none in the previous 12 months. Skill by region and
by year.

**Stated limits, now, before any result.** Held-out is out of time but not unseen in any
strong sense: anyone knows roughly where conflict was in those years. One held-out window
of four years holds few ENSO cycles, so it can say little about ENSO; the interval cannot
cover a regime change. Event counts carry reporting bias, plausibly varying with access
and media, and a fatal-events dataset measures only part of conflict (to be confirmed from
the codebook). A gain would be predictive, not causal: that needs more than this design
gives. Single fit, no rolling retrain, so drift lowers both models and the comparison is
what is tested. Inputs and events are treated as known at month end; real publication delays
and later revisions of the event data are ignored, which flatters any live use of a forecast.

## Steps

Estimates are fresh tokens across both sessions. They are judgement, anchored only on an
earlier project's three experiments at about 330k each. Stop-and-say limit is estimate
plus 25%.

| Step | What | Estimate | Stop at |
|---|---|---:|---:|
| 1a | Data check | 200k | 250k |
| 1b | Known-answer test | 600k | 750k |
| 1c | Baseline on validation | 300k | 375k |
| 1d | The test | 500k | 625k |
| | Independent review of 1d (rule 7) | 150k | 190k |
| | next-pattern's audit of the result | 150k | 190k |
| | **Total, leaving about 1.1M unused** | **1.9M** | cap 3M |

The unused 1.1M is not a target. No subagents are planned except the review. If that
changes, the spec and cost come first.

### 1a. Data check. Gate.

Does each source exist in a form we can use? Fetch headers and licence pages, then fetch
the data, in plain scripts. One table: fetchable without a login, licence, years covered,
resolution, size on disk, who hosts it. Sources: UCDP GED, SPEI, CHIRPS, NOAA ONI, WFP
food prices via HDX, and a land and country boundary set for the grid. Each gets a manifest
entry at `data/manifest.toml` (rule 10). `data/raw/` and `data/panel/` are git-ignored. Each
check rests on the source's own page, cited with date, not on memory.

Queries for the rule: share of events by geocoding precision, and price series coverage by
market and year, with no join between prices and outcomes. Also the first `pyproject.toml`.

Where SPEI and CHIRPS both pass, a European host breaks the tie (decision 0003).

*Stop if* no fetchable, licensed outcome source exists. That ends the design and goes to
the owner.

### 1b. Known-answer test. Gate.

Can the 1d machinery find a planted link, and stay quiet where there is none? Results rule
first, at `results/1b-known-answer.md`.

**Generator** in `synth/`, committed before any detector code, importing nothing from
`src/`. An import test enforces this. Its mechanism differs from the detector's assumptions
on purpose: a self-exciting negative binomial count process over a latent spatial rate, with
threshold input effects spread over distributed lags and present in only some cells. A
limit, stated: the same session writes both, so the independence is in code and form, not
in authorship.

The real outcome panel is built here, because the synthetic shape comes from it, from the
training block only: size, share of zeros, lag-1 and lag-12 autocorrelation, seasonal
amplitude, spatial clustering. No statistic is computed on a validation or held-out month.

**Panels**, each with synthetic inputs shaped like the real ones:
- Planted, rate ratio per standard deviation of input at 1.05, 1.15 and 1.40.
- Pure null: no links.
- Shared-driver null: input and outcome share a seasonal driver and a slow regional trend
  but have no link. This is the realistic trap.

Each gets 20 replicates, full pipeline with 19 shuffles per replicate, and the oracle's skill
(the generator's own true rate) to show what each effect is worth in deviance.

**Pass, or stop:** detection at least 80% at the 1.40 ratio; false positives at most 2 of 20
on each null. The 1.15 result is reported, and tells the owner what 2% means. These are
counted with intervals (20 replicates cannot show much better than plus or minus 10 points).
Fewer shuffles than 1d because of runtime, disclosed; so 1b tests criteria 1 and 3 fully and
criterion 2 only coarsely, at 1 in 20.

**Runtime.** One fit is timed first. The brief asks for panels of the same size as the real
one. The design is 5 panels x 20 replicates x 21 fits = 2,100 fits; at about one minute per
fit (a guess) that is about 35 hours of a shared box. If the measured total exceeds 48 hours,
one replicate per panel runs at full size and the rest on a contiguous sub-panel of 2,000
cells. That is a disclosed departure from the brief.

**Candidates.** PCMCI (tigramite) and convergent cross mapping (pyEDM) run on the same panels,
on a sample of 200 cells, with link and lag recovery and false discoveries reported beside
runtime. They do not enter the verdict: the test in 1d is predictive and needs no discovery
step. A candidate that recovers planted lags with few false ones is proposed for the next
phase; one that fails, perhaps on zero-heavy counts, is dropped, and that is a result.

### 1c. Baseline. Gate.

Fit B0 and B on train, score on validation only, at all three leads.
`results/1c-baseline.md`, rule first. Reports skill of B over B0 and interval, calibration,
and fit time. **The held-out block is not touched**, which is how rule 9's single scoring
survives step 1c. Tuning is frozen here for B. M1 and M2 are tuned on validation in 1d by the
same grid, before the single run.

### 1d. The test. next-pattern audits. Gate, with a recommendation.

`results/1d-test.md`, rule first, with the commit hash of the code. One script scores B, M1,
M2 and all 198 shuffled fits, writing only at the end, so no partial look is possible. Run
once. A crash before output may be rerun, disclosed. A rerun after any output is not allowed.
A reviewer recomputes the deciding numbers from the stored predictions (rule 7).

Long runs are `nice -n 19` with at most 6 threads, since live apps share the box. Runtime is
reported.

**Recommendation, set in advance:**
- H1 or H2 passes, and survives review: **extend**, with a proposal for the owner.
- Neither passes, while 1b showed the machinery can detect an effect of that size: **stop**,
  and publish the negative result, with what the interval excludes.
- Interval spans the margin, or 1b's power was poor: **change method** only if a specific
  reason exists; otherwise stop. More data or more inputs is a new decision, not a rescue.

## Repo layout from step 1a

`pyproject.toml`, `uv.lock`, `.gitignore`, `data/manifest.toml`, `scripts/fetch_<source>.py`,
`src/causal_atlas/` (panel, features, models, score), `synth/` (generator), `tests/`,
`results/`. No framework over the sources (decision 0007).

## Reading

None is planned. If a decision needs a fact, it gets one question, one page back, and a
citation to the source (rule 5).
