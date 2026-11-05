# Phase 1 plan: one slice, one decisive experiment

Written 2026-11-05 by the project session, before any data has been fetched or any
number computed. For audit by next-pattern and approval by the owner. Each step ends
at a gate; nothing starts without the owner's yes. Each results file copies its rule
from here and is committed before its numbers. Any later change to this rule is a
disclosed deviation. Revised the same day after next-pattern's audit, still before any
data (decision 0011).

**Nothing in this plan about a data source is a fact yet.** Coverage, licences and
access are what step 1a checks (rules 4 and 5). Sizes are rough arithmetic.

## Amendments after step 1a (decision 0013)

Made after the data check and before any outcome was computed by place or period. Where
these disagree with the text below, these win, and results files copy the amended rule.

- **H2 and M2 are dropped.** Only H1 and M1 remain, with one comparison: a two-sided 95%
  interval, its lower end at the 2.5th percentile. No food prices are used.
- **Outcome:** events with `where_prec` 1 to 3, assigned to the month of `date_start`.
- **Drought input:** SPEI-3 from SPEIbase 2.11.
- **E** is the last target month with its inputs, 2025-03: held-out 2021-04 to 2025-03,
  validation 2017-04 to 2021-03, train 1992-01 to 2017-03, the same target months at every lead.
  That is 399 months and 10,228 cells.
- **ONI:** at t-1, and its 3, 6 and 12 month means ending at t-1.
- **Circular shift:** 32 whole-year shifts, smallest p 1/33, about 0.030. Criterion 2 requires
  p <= 0.05 for a single comparison. Under year permutation the plan's p <= 0.02 stands.
- **A 1b replicate** is 2 + 19 + 32 = about 53 fits.

**Order changed after the 1b stop (decision 0015).** Fix the generator, finish 1b, add about 10
sources under a 150k cap, then stop for the owner to set the margin and pre-register a multi-input
test. 1c and 1d are deferred, and the held-out set stays unscored.

## The question, and what would answer it

Does adding lagged climate and food-price inputs improve the forecast of conflict
events in a 0.5 degree cell, three months ahead, beyond what the cell's own history,
season and neighbours already give, on a held-out period, by the margin below, with
the gain vanishing when the inputs are shuffled in time?

A "no" is an acceptable and publishable answer.

## Departures from the brief, decided under the owner's delegation

The defaults are accepted (decision 0005). The owner left design choices to this session
and next-pattern (decisions 0010 and 0011). These depart from the brief or fill its gaps:

1. **Prices are tested separately from climate (H2 below), on the cells and months
   that have them.** Why: food price monitoring plausibly starts because a crisis has
   started, so whether a price exists at all may predict conflict. Pooling them would
   let a tree model use "a price exists here" as a crisis flag and report that as a
   price effect. Cost: two comparisons instead of one, so a stricter interval.
2. **Three inputs, not four.** Fewer choices, fewer ways to get lucky.
3. **Most synthetic replicates run on a smaller panel** (see 1b), a disclosed departure
   from the brief's "same size", to keep a box shared with live apps under 24 hours.
4. **Baseline and test use the same learner.** So a gain cannot come from a better
   learner. The brief does not require this; it closes an obvious way to fool ourselves.
5. **PCMCI and convergent cross mapping are deferred until after the 1d verdict.** This
   is a deferral, not a drop. They decide nothing in Phase 1, and they are where 1b would
   most likely overrun. The owner can reverse this at any gate.

The owner accepted the **2% margin** and the **3-month lead** (decision 0012). Reasons are
below; both are judgement calls.

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
  after it starts, so that series onset is not a signal. A row needs a present price
  feature at t; otherwise it is dropped for both M2 and its baseline, decided at t from
  the past only. A price is never passed to the learner as missing, because "no price
  this month" would then be the crisis flag this design removes. Baseline B is refitted
  on that sub-panel. The exact staple list, and the coverage number that counts as too
  little, are proposed at the 1a gate from coverage counts, before any join with outcomes.
  If coverage is too little, H2 is dropped and H1 keeps a 95% interval.

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
blocks keep the temporal. Two comparisons, so a two-sided 97.5% interval (Bonferroni), its
lower end at the 1.25th percentile. About eight blocks, on a mean that a few cell-months can
dominate, may under-cover: 1b checks this on nulls built to be as hard as the real data.

**Shuffle test.** Inputs only, in train, validation and held-out alike, applied identically
to all cells in a draw and keeping calendar month, so each input's seasonality and spatial
pattern survive. A gain that is only the input acting as a seasonal clock therefore survives
too and does not count. Refits use M's frozen settings, with no retuning. Two schemes are
named now, and one is fixed at the 1b gate, before any real number:
- **Year permutation,** 99 draws. It destroys an input's year-to-year persistence, so a
  persistent input lining up with a persistent conflict episode by chance has no shuffled
  counterpart, and real can beat shuffled for a reason that is not a link.
- **Circular shift** of the whole input series by k whole years, for every k: one less than
  the years in the panel, about 29 if the panel has 30 years. It keeps persistence and breaks
  alignment. Its smallest possible p is 1/(shifts+1), about 0.033.

Prices apply either scheme to whole years within each market series' span, so far fewer shifts
may exist; the count available goes in the 1a gate report.

**Choosing the scheme, at the 1b gate.** A scheme qualifies if it meets 1b's pass marks. If
both qualify, the circular shift is used, because it answers the persistence problem. If only
one does, that one. If neither does, 1b fails.

**Verdict, for each of H1 and H2, all three required:**
1. Skill at least **0.02** (2%) and the lower end of its 97.5% interval above 0.
2. Under year permutation: observed skill above all but at most 1 of the 99 shuffled skills,
   p <= 0.02. Under circular shift: above every shift, p = 1/(shifts+1). That cannot reach the
   0.025 a Bonferroni correction would ask for, unless the series is longer than 39 years. This
   is a limit of the data, and is stated beside the result.
3. The median shuffled skill is under 0.01 in size, half the margin: the gain vanishes.

**Diagnostic, stated beside the verdict, not changing it.** The share of the gain owed to the
single largest country and to the single largest year. M is also reported at B's settings, so
a gain owed to tuning rather than to inputs can be seen.

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
| 1b | Known-answer test, including its one subagent (about 100k) | 450k | 560k |
| 1c | Baseline on validation | 300k | 375k |
| 1d | The test | 500k | 625k |
| | Independent review of 1d (rule 7) | 150k | 190k |
| | next-pattern's audit of the result | 150k | 190k |
| | **Total, leaving about 1.25M unused** | **1.75M** | cap 3M |

The unused 1.25M is not a target. The only subagents planned are the generator's author in
1b and the review. Anything else states its spec and cost first.

### 1a. Data check. Gate.

Does each source exist in a form we can use? Fetch headers and licence pages, then fetch
the data, in plain scripts. One table: fetchable without a login, licence, years covered,
resolution, size on disk, who hosts it. Sources: UCDP GED, SPEI, CHIRPS, NOAA ONI, WFP
food prices via HDX, and a land and country boundary set for the grid. Each gets a manifest
entry at `data/manifest.toml` (rule 10). `data/raw/` and `data/panel/` are git-ignored. Each
check rests on the source's own page, cited with date, not on memory.

Queries for the rule: share of events by geocoding precision, and price series coverage by
market and year, with no join between prices and outcomes. Also the first `pyproject.toml`.

Where SPEI and CHIRPS both pass, a European host breaks the tie (decision 0003). The gate report
also proposes the staple list and H2's coverage number, and states how many shifts each input allows.

*Stop if* no fetchable, licensed outcome source exists. That ends the design and goes to
the owner.

### 1b. Known-answer test. Gate.

Can the 1d machinery find a planted link, and stay quiet where there is none? Results rule
first, at `results/1b-known-answer.md`.

**Generator** in `synth/`, committed before any detector code, importing nothing from
`src/`. An import test enforces this. It is written by one Sonnet subagent, about 100k fresh,
from a written spec that holds the shape statistics and the panel list and withholds this
plan's "Test models" section, and that forbids opening this plan or `src/`. The reason: the
detector is already fixed, so the open risk runs the other way, an author who knows its lag
windows planting links that are easy for it. The spec asks for a mechanism unlike a boosted
model on lag windows: a self-exciting negative binomial count process over a latent spatial
rate, with threshold input effects over distributed lags the author chooses, in only some
cells. The spec and cost are stated at the 1b gate before spawning, and the owner can say no;
this session then writes the generator, with that limit disclosed.

The real outcome panel is built here, because the synthetic shape comes from it, from the
training block only: size, share of zeros, lag-1 and lag-12 autocorrelation, seasonal
amplitude, spatial clustering, concentration of events (share in the top 1% of cell-months),
and regional episode length. No statistic is computed on a validation or held-out month.

**Panels**, each with synthetic inputs shaped like the real ones, with real-like multi-year
persistence:
- Planted, rate ratio per standard deviation of input at 1.05, 1.15 and 1.40.
- Pure null: no links, but large multi-year regional episodes unrelated to the inputs, so the
  nulls are as hard as the real data.
- Shared-driver null: as the pure null, and input and outcome also share a seasonal driver and
  a slow regional trend, with no link. This is the realistic trap.

Each gets 20 replicates through the full pipeline, with both shuffle schemes, and the oracle's
skill (the generator's own true rate) to show what each effect is worth in deviance. Both schemes
run on the planted panels as well as the nulls, because a scheme that is quiet on nulls must also
be shown to detect. Year permutation uses 19 draws per replicate, fewer than 1d because of
runtime, so it tests criterion 2 only coarsely, at 1 in 20; disclosed.

**Pass, or stop, for each scheme:** detection at least 80% at the 1.40 ratio; false positives at
most 1 of 20 on each null, with the exact binomial bound printed beside the count, since even 0
of 20 bounds the true rate only loosely. Criterion 1's false-positive rate is also reported alone,
which is the check on the interval. The 1.15 result is reported, and tells the owner what 2% means.

**Runtime.** One replicate per panel runs at full size and the other 19 on a contiguous sub-panel
of 2,000 cells, a disclosed departure from the brief's "same size". Each replicate is 2 + 19 + about
29 = about 50 fits. At a guessed minute per full-size fit and a fifth of that on the sub-panel, this
is about 4 hours plus 16. **The ceiling is 24 hours in total.** One fit of each size is timed first;
if the projection is over the ceiling, this stops and reports at a gate rather than cutting
replicates unasked.

**Candidates, deferred.** PCMCI (tigramite) and convergent cross mapping (pyEDM) stay candidates
and do not run in 1b. The test in 1d is predictive and needs no discovery step, so they matter
only if the answer is "extend". They would then need this same known-answer test first (rule 3).

### 1c. Baseline. Gate.

Fit B0 and B on train, score on validation only, at all three leads.
`results/1c-baseline.md`, rule first. Reports skill of B over B0 and interval, calibration,
and fit time. **The held-out block is not touched**, which is how rule 9's single scoring
survives step 1c. Tuning is frozen here for B. M1 and M2 are tuned on validation in 1d by the
same grid, before the single run.

### 1d. The test. next-pattern audits. Gate, with a recommendation.

`results/1d-test.md`, rule first, with the commit hash of the code and the shuffle scheme fixed at
the 1b gate. One script scores B, M1, M2, each M at B's settings and all shuffled fits, writing only
at the end, so no partial look is possible. Run
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
