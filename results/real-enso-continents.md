# Real test on fields never read: the frozen search, then a forecast check with honest slope sizes, on five continental boxes

Rule first, committed before any number that joins the ONI or a decoy to these fields (rule 9). Authority to run: decision 0040. Why the forecast step changed after a miss, and why that is not rescored on Africa: decision 0041. Code: `src/causal_atlas/forecast.py`, `src/causal_atlas/links.py` (`both`, unchanged), `scripts/run_continents.py`. Seeds: `results/seed-ledger.md`.

## Why

The two-gate search passed every mark on Africa (`results/real-enso-drought-2.md`). Its one-time confirmation then missed (`results/real-enso-drought.md`, "Confirmation result"): El Niño was named and mapped correctly, but adding it to the baseline did not improve the forecast on 2000 to 2024. The diagnosis, made on that spent period, pointed at the forecast step and not at the link: slopes about three times too large because each was the best of nine lags and then selected, and a baseline that could not follow a shift in the field's level. Fixing a method on the period that failed it and scoring it there again would prove nothing. The same drought file holds every other continent, and this project had never read them. So the fix is frozen here and confirmed there.

## Seen before this rule

- **All of Africa, including its 2000 to 2024, which is spent.** Every number in the two earlier results files, the diagnosis, and the development of the forecast step below. Africa is in no mark here.
- **Development on Africa** (scratch scripts, not kept; the numbers that chose the design):
  - One multiplier for every slope, chosen inside the discovery years by five blocks of years with the claims picked again in each: 0.35 to 0.48 across baselines and scales. The multiplier that would have been best on 2000 to 2024, seen afterwards: 0.30 to 0.56. So the inner choice lands where it should.
  - Baselines against guessing zero on 2000 to 2024, region averages: each region's own last 60 months +0.35; a linear fit on own lags, the field mean and own trailing means +0.31; gradient boosting without latitude and longitude +0.18; the first rule's gradient boosting +0.06. The first rule's baseline is the weakest because it learns each place's 1951 to 1999 level and that level moved.
  - Picking claims on the field or on the baseline's residual made little difference; the field is kept, as in the first rule.
  - Region averages and single cells gave similar skill.
  - **The code below, as committed, on Africa:** the inner blocks chose the linear baseline at both scales; multiplier 0.39 (regions) and 0.36 (cells); S on 2000 to 2024 +0.033 at both scales, interval -0.030 to +0.097 (regions) and -0.022 to +0.088 (cells); larger than all 24 shifted values; below every baseline alone. **By the pass rule below that is not a pass on Africa**, and it was reached after seeing those years. Africa stays where the first results file left it: a miss.
- **The five new fields: their shapes only.** Cells with a complete record and regions of at least 40 cells: South America 6,225 and 95; Australia 2,850 and 49; South and Southeast Asia 5,385 and 100; North America 7,611 and 105; Europe 4,710 and 64. The largest absolute value in each (up to 9.9), which is why the same clip is used. No correlation, no average over time, no map.
- The author knows from general reading that El Niño affects rainfall in South America, Australia and Southeast Asia, and that its reach into Europe is weak. The boxes are plain continental rectangles, not drawn around any published region.

## Data and split

- **Field:** SPEI-3 from the file already held (`data/manifest.toml`), cells with no missing month from 1950-01 to 2024-12, clipped at plus or minus 3, in five boxes (south, north, west, east, degrees):
  - South America: -56, 13, -82, -34
  - Australia: -44, -10.25, 112, 154
  - South and Southeast Asia: -10, 35, 65, 155
  - North America: 15, 60, -130, -60
  - Europe: 35, 70, -10, 40
- **Driver and decoys:** the ONI and 31 decoys per set, 20 sets per field, as before, with fresh seeds, a different range for each field: 12101 to 12120, 12201 to 12220, 12301 to 12320, 12401 to 12420, 12501 to 12520, in the order above.
- **Discovery: 1950-01 to 1999-12** (targets 1951 to 1999). **Confirmation: 2000-01 to 2024-12**, sealed for these fields until the step below is run, once.

## Step 1, naming: the two-gate search exactly as it passed

`links.both`, no change: broad gate and sharp gate on 10-degree regions stepped by 5 degrees with at least 40 cells, lags 0 to 12, 49 whole-year shifts, a candidate named by either gate. Three kinds of run per set: the ONI among the decoys; the ONI left out; the field's years in a seeded random order.

Marks, fixed now:

- **N1:** the ONI is a lead in at least 18 of 20 sets in **each** of South America, Australia, and South and Southeast Asia. These are the three with an entry in our reading (`docs/reading/enso-africa-known-answer.md`, section 4; months there were read from a scanned map and strengths were not checked, so only "El Niño matters here" is taken from it).
- **N2:** a decoy is a lead in at most **8 of the 100** runs with the ONI in, the five fields pooled.
- **N3:** with the ONI left out, any lead in at most 8 of 100.
- **N4:** with the years shuffled, any lead in at most 8 of 100.
- **Reported, marking nothing:** how often the ONI is a lead in North America and in Europe; which gate named what; for each field, the region, calendar month and lag where the ONI's correlation with a region average is largest, with its sign.

Why pooled: Africa allowed 2 of 20 for each kind and measured 1, 1 and 0 of 20 and 0 of 80 in the ruler. At a few per cent per run, fifteen separate marks of 2 in 20 would likely see one fail by chance; 8 in 100 is a tighter rate (8% against 10%) on five times the runs.

No ruler is run on these fields. What the search can hear was measured on Africa only and may differ elsewhere.

## Step 2, the forecast check, run once

It runs only if N2, N3 and N4 pass. **A field enters the pooled score only if the ONI was a lead there in at least 18 of its 20 sets**: the predictor is given what the finder named, nothing else. If no field enters, the confirmation years stay sealed. All five fields are scored and reported; only those that entered count.

Units are the 10-degree region averages (the scale the search hears). For each field, everything is fitted on its discovery years:

- **Baseline (rule 2), chosen per field among three by squared error on five blocks of discovery years, each block predicted from a fit on the others:** zero (the index's long-run average); level (the unit's own mean over the 60 months ending at t-3); linear (one least-squares fit on the unit's own values at t-3, t-4, t-5, t-6 and t-12, the mean of all units at t-3, and the unit's own means over the 12 and 60 months ending at t-3). SPEI is already standardised by calendar month, so the season's average is in the index itself. Nothing later than t-3 is used.
- **Claims:** as in the first rule. For each unit and calendar month, the lag from 4 to 12 with the largest absolute correlation between the ONI and the field, kept if significant by Benjamini-Hochberg at 5% over all units, months and lags 4 to 12.
- **Model:** baseline plus, on claimed unit-months, k times slope times the ONI at its lag. The slope is fitted through the origin on the baseline's discovery residuals. **k is one number per field, from 0 to 1,** the value with least squared error on five blocks of discovery years, with the claims picked and the slopes fitted on the other four each time. The baseline is not refitted inside those blocks; it has nine coefficients.
- **Metric:** S = 1 - (model's squared error) / (baseline's squared error) on the claimed unit-months of 2000 to 2024, **summed over the fields that entered**. Interval: 2,000 draws of the 25 years, the same years drawn for every field, 95%.
- **Control:** the same claims, slopes and k with the ONI shifted by each of 24 whole years within 2000 to 2024.
- **Passes when all three hold for the pooled score:** the interval's lower end is above 0; S is larger than all 24 shifted values; and the model's squared error on those unit-months is below that of **each** of the three baselines alone, so a field whose inner blocks chose the wrong baseline cannot make the driver look good.
- **Reported, marking nothing:** each field on its own; the same at the scale of single cells (neighbours there are the up to 8 cells around, as in the first rule); the chosen baseline, k, the number of claims and their lags; each baseline's skill against zero on all unit-months.

The script refuses a second scoring.

## What changed from the first confirmation rule, all of it after seeing that miss

| | First rule | Here |
|---|---|---|
| Slope size | Each slope shrunk by its own t statistic | One multiplier per field, chosen on held-out blocks inside discovery |
| Baseline | Gradient boosting with latitude and longitude | The best of zero, level and linear on held-out blocks inside discovery |
| Units | Cells | Region averages; cells reported |
| Score | One field | Pooled over the fields where the search named the ONI |
| Pass | Lower end above 0, above all 24 shifts | The same, and below every baseline alone |

Unchanged: lags 4 to 12, the claim rule, S, the year bootstrap, the 24 shifts, one scoring.

## What a pass and a miss would each mean

- **Pass:** on 25 years and on continents the method never saw while it was built, a driver the engine named blind improves a forecast of drought three or more months ahead beyond the best simple baseline. That would be the first result here that meets rule 2 on real data. The link is a known one, so it shows the whole chain works on reality, finder to predictor; it discovers nothing new.
- **Miss:** published as a miss, and these years are then spent for this driver and these fields. With the best-known climate link there is, that would say the forecast step adds nothing measurable at this lead even when the finder is right.
- If a pass: a regional outlook from the 2026 El Niño follows under its own rule, written before it is computed. If a miss: none.

## Limits it carries

- The five fields share the same 25 years and the same handful of El Niño and La Niña events. They are new places, not new years; the interval draws years for that reason and is wide for that reason.
- One source: the fields come from the same station-based product as Africa's, with the same filling where stations are thin.
- Regions overlap, so a cell counts in up to four units.
- The design choices were made on Africa after its confirmation years were seen. Nothing was chosen on the new fields, but the author's general knowledge of where El Niño acts is not blind.
- The naming marks vary only the decoys; there is one real world per field.
- El Niño and La Niña are not mirror images and the link changes by decade; one slope per unit and month averages over both.
- The shift control assumes years are exchangeable; trends weaken that.
- Decoys are independent of each other; real candidate series are not.

## Estimates

Naming: about 40 minutes of machine time. Forecast check: about 10. Tokens to the report: about 200k.

## Results, step 1: naming (2026-11-09, discovery years only; 2000 to 2024 on these fields untouched)

Rows: `results/real-enso-continents.jsonl` (305: 300 runs and one `where` row per field). Run as committed, no deviation. Machine time about 15 minutes (corrected after the independent check: this first said 35; the run's log runs from 22:26:52 to 22:41:20 local time, starting 42 seconds after the rule's commit).

**Every naming mark passed.**

| Mark | Rule | Measured |
|---|---|---|
| N1 | The ONI a lead in at least 18 of 20 in each of the three fields with a published entry | South America **20 of 20**, Australia **19 of 20**, South and Southeast Asia **20 of 20** |
| N2 | A decoy a lead in at most 8 of 100 | 3 of 100 |
| N3 | The ONI left out: any lead in at most 8 of 100 | 3 of 100 |
| N4 | Years shuffled: any lead in at most 8 of 100 | 5 of 100 |

Reported, marking nothing:

| Field | ONI a lead | By the broad gate | By the sharp gate | Where the ONI's correlation with a region average is largest (discovery years) |
|---|---|---|---|---|
| South America | 20 of 20 | 20 | 20 | -0.80, the Guianas (about 6 N, 58 W), January, ONI two months earlier: drier under El Niño |
| Australia | 19 of 20 | 0 | 19 | -0.77, the north (about 13 S, 140 E), November, four months earlier: drier |
| South and Southeast Asia | 20 of 20 | 16 | 20 | -0.83, the southern Philippines and nearby (about 5 N, 125 E), December, one month earlier: drier |
| North America | 20 of 20 | 19 | 20 | +0.79, Florida and the Gulf coast (about 25 N, 84 W), March, two months earlier: wetter |
| Europe | **0 of 20** | 0 | 0 | +0.55, Iberia, November; under the bar (0.65 to 0.72), not named |

- The signs and places are the textbook ones, found with no box drawn: dry over northern South America, northern Australia and the maritime continent, wet over the southern United States in late winter. These were not marks, because our reading gave them only from a scanned map.
- **Europe is the quiet control the design did not have before:** the same engine, the same candidate, a field where El Niño's reach is weak, and it named nothing real in 20 sets.
- On these fields the sharp gate does most of the naming (in Australia all of it). On Africa it was the broad gate. The two gates are both needed.
- False alarms: eleven runs. Counted by run, four came from the sharp gate and seven from the broad gate. One of the four (Australia, seed 12206, years mixed) named two decoys, so counted by naming it is five and seven. The sharp gate's namings were over the bar their row holds by 0.002 to 0.014 (0.689 against 0.675; 0.639 and 0.632 against 0.630; 0.686 against 0.682); the fifth is that last decoy again, in the run with the ONI in, whose row holds the bar from before the ONI was set aside. The 3 of 100 with the ONI left out are the same decoy sets as the 3 with it in, as on Africa. (Reworded 2026-11-09 after the audit below: this first gave only the count by run.)
- No ruler was run here, so what the search cannot hear on these fields is not measured.

**Entering step 2** (the ONI a lead in at least 18 of 20): South America, Australia, South and Southeast Asia, North America. Europe does not enter and is scored for the record only.

## Results, step 2: the forecast check (2026-11-09, scored once on 2000 to 2024, after step 1 was committed)

Rows: kinds `confirmation` and `pooled` in `results/real-enso-continents.jsonl`. Run as committed, no deviation. The script refuses a second scoring. Machine time about 2 minutes.

**It passed.** On the four fields where the search named El Niño, adding it to the baseline cut the squared error of a drought forecast three or more months ahead by 17% on the region-months it made a claim about, on 25 years and four continents the method had never seen.

| | Rule | Measured |
|---|---|---|
| Pooled S on claimed region-months | Interval's lower end above 0 | **S = +0.171, interval +0.120 to +0.220** |
| Against the 24 year-shifted controls | Larger than all 24 | Larger than all 24 (they run from -0.277 to -0.037: the same claims fed the wrong years make the forecast worse) |
| Against each baseline alone | Model's squared error below all three | Below all three: 17% under linear (the one chosen), 26% under zero, 27% under level |

By field, region averages. The first four entered the pooled score; each also meets the pass rule on its own, which was not required. North America does so narrowly: on 57 claims its interval starts at +0.007. (Its multiplier is 0.675 in the row; this table first printed 0.67, corrected 2026-11-09.)

| Field | S | Interval | Shifted controls | Claims (of region-months) | Baseline chosen | k |
|---|---|---|---|---|---|---|
| South America | +0.161 | +0.097 to +0.224 | -0.268 to -0.017 | 353 of 1,140 | linear | 0.76 |
| Australia | +0.129 | +0.068 to +0.183 | -0.107 to +0.051 | 113 of 588 | linear | 0.47 |
| South and Southeast Asia | +0.224 | +0.148 to +0.292 | -0.389 to -0.078 | 260 of 1,200 | linear | 0.77 |
| North America | +0.117 | +0.007 to +0.214 | -0.330 to +0.028 | 57 of 1,260 | linear | 0.68 |
| Europe (did not enter) | none | | | **0 of 768** | zero | 0 |

Reported, marking nothing:

- **Single cells:** pooled S +0.137, interval +0.093 to +0.180, larger than all 24 shifted (-0.217 to -0.031), below every baseline alone. By field +0.131, +0.100, +0.172, +0.089, each with its interval above 0. Europe: no claim in 56,520 cell-months.
- **By year, pooled regions:** the model had less error than the baseline in 22 of the 25 years. The three where it was worse (2001, 2013, 2014) were worse by 1% to 5%. The largest years are 2015 (+0.39), 2011 (+0.35), 2010 and 2022 (+0.32). Of the whole reduction in error, 2015 carries 13%, 2010 11%, 2022 and 2011 8% each. The gain does not rest on one event: without 2015, S is +0.158; without 2015 and 2016, +0.152; without 2010, 2011, 2015 and 2016, +0.130; without those and 2023 and 2024, +0.124. (Corrected after the independent check: this first said no year carried more than 7%, which was each year's share of the baseline's error, not of the gain.)
- **Lags claimed:** 494 of the 783 claims in the four fields are at lag 4, the shortest allowed.
- **How good the baseline is by itself:** against guessing zero on all region-months of 2000 to 2024, +0.10 in South America, +0.02 to +0.04 in the other three. At three months ahead a region's own drought history says little; that is the bar El Niño had to clear, and it is a low one in absolute terms.
- The inner blocks chose k between 0.47 and 0.77 here against 0.39 on Africa: where the link is stronger the slopes need less shrinking, and the rule found that without being told.

### What this says

- **This is the first result in this project that meets rule 2 on real data:** a driver the engine named blind, among 31 decoys, improves an out-of-time forecast beyond the best of three baselines, with a control that fails as it should and a field (Europe) that stays silent as it should.
- **It is a known link.** The chain works end to end on reality: finder, map, predictor. Nothing new about the world has been discovered.
- **What it does not say:** nothing about Africa, where the first confirmation missed and still stands as a miss; nothing about links below what the search can hear; nothing about a region-month where no claim was made (on all region-months of the four fields the gain is much smaller, because 81% of them carry no claim).
- The size, in plain terms: on the places and seasons where it speaks, knowing the state of El Niño four or more months earlier removes about a sixth of the forecast error that own history leaves. The interval says somewhere between an eighth and a fifth.

### Limits, beside this result

Those in "Limits it carries" above, and three that matter for reading the number:

- **The drought index is standardised over its whole record by its makers**, 1901 to 2024, so each value's level and scale carry a little information from later years. That touches the target and the baseline's inputs alike and cannot tell the model which way a given month went, but it is not a strictly out-of-time quantity and is said here. How this is known (read 2026-11-09): the held file's own `call` attribute shows the makers' function run on the whole 1901 to 2024 rainfall file with no reference period given; their code calls `SPEI::spei(d, s, na.rm=TRUE, verbose=FALSE)`, again with none (<https://raw.githubusercontent.com/sbegueria/SPEIbase/master/R/functions.R>, the current code, which is later than the build of this file); and that function's documentation says "The default behavior of the functions is using all the values provided in data for parameter fitting" (<https://raw.githubusercontent.com/sbegueria/SPEI/v1.8.1/R/spei.R>).
- **The gain is measured on the region-months the method chose to speak about** (19% of them in the four fields). On the rest it makes no forecast beyond the baseline.
- **The link is one whose existence was known to the author before the test**, and the five boxes were drawn with that knowledge (four where a link is published, one where it is not). What was blind: which candidate among 32 the search would name, where, when, how large, and every number on 2000 to 2024.

- **The El Niño index is not strictly out of time either.** Its maker measures each five-year stretch against a 30-year average centred on it: "There will be multiple centered 30-year base periods that will be used to define the Oceanic Niño index", for example "ONI values during 1950-1955 will be based on the 1936-1965 base period" (NOAA CPC, <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_change.shtml>, read 2026-11-09). So an index value in the 1990s is measured against an average that includes the 2000s, and the file is the 2026 version of the sea-surface record. Like the drought index's scaling, that cannot tell the model which way a given month went.
- **The forecast step was tuned on Africa's 2000 to 2024**, and those years hold the same El Niño events as the years scored here. The design was shaped by these events, though not by these places. Africa itself scores only +0.033 under it.
- **The shifted control adds little once the interval is above 0.** A slope fed the wrong years can only add error, so every shifted value comes out near or below zero. It guards against a score that is positive for a reason unrelated to the driver's timing; it is not a second, independent test.
- **The script's refusal to score twice is a guard, not a lock.** Git shows the rule and all code in one commit (22:26:10), no change to code after it, and the scoring rows appended once. It cannot show that nothing was run unrecorded.
- **The drought file carries an error its makers have acknowledged** (added 2026-11-09, found while closing the audit below). The held file is SPEIbase 2.11.0. The makers' README, under "Known issue: PET unit conversion (fixed in v2.13.0)" (<https://raw.githubusercontent.com/sbegueria/SPEIbase/master/README.md>, read 2026-11-09), says of versions 2.6 to 2.12.0: "The vector of days per month was recycled along the longitude dimension of the data array instead of along time, so each grid cell's PET was multiplied by a single constant (28, 29, 30 or 31) in every month. All published SPEI datasets from v2.6 to v2.12.0 are affected. The effect is generally small, but it is largest in arid regions where PET dominates the water balance." It says a corrected release "will follow"; the download page listed nothing later than 2.11 when a helper read it that day. PET is the water the air could take up, the evaporation side of the index. **So every drought value in every result of this project comes from an affected file, and what that does to the scores is not measured**, because there is no corrected file to compare with. This session's reading of the quoted description, not the makers' words: each cell's evaporation is off by a factor between 28/31 and 31/28, up to about a tenth, in a pattern that depends on the month and the cell's longitude; it changes the size of evaporation against rain, not the rain. Australia is the driest field here and is where it would matter most. The outlook's scoring rule now says what happens when a corrected file is used (`results/outlook-2026-27.md`).
- **This is not the plan's step 1d, and passing it does not pass 1d** (added 2026-11-09 for the audit below). The Phase 1 plan (`docs/plan-phase-1.md`, "Verdict") asks three things of a forecast of conflict: skill of at least 0.02 with the lower end of a 97.5% interval above 0; skill above every whole-year circular shift, or above all but one of 99 year permutations; and a median shuffled skill under 0.01 in size. This test has drought as its outcome and its own rule, above: the lower end of a 95% interval above 0, 24 whole-year shifts, three baselines. Set beside the plan's marks: the first is met in size (the lower end is +0.120 at 95% and +0.110 at 97.5%, the second from 20,000 draws of the stored years); the second is met in its circular-shift form (above all 24) and the 99 permutations were not run; the third is not met as written, because the median shifted score is -0.120 and not near zero: fed the wrong years, the claims add error. The plan's question is about conflict and nothing here answers it.

### Independent check (2026-11-09, one fresh reader, 131k fresh tokens by the counter)

A reviewer with no part in the work was given the rule text, the rows and the code, and asked to break the result. Its verdict: **"holds with these corrections"**, all of which are now made above. Its report in full, its own implementation and its leak test are in `docs/reviews/2026-11-09-continents-independent-check/` (committed 2026-11-09 for the audit below; until then only this summary was public).

- **Its own implementation from the rule text** (plain loops; from this repo only the data loaders and the region builder) gave the same S, squared errors, claims, lags, multipliers and baseline choice in every field, and pooled S +0.1712 with the same interval and shifted range.
- **Leaks:** it replaced every drought and index value from 2000-01 onward with noise and refitted, in its code and in the project's. Nothing fitted changed. A forecast for month t reads nothing later than t-3; the index at lag 4 holds months t-5 to t-3, and the drought value at t covers t-2 to t.
- **Order:** as in the last limit above.
- **Text against rows:** every number matched except one wrong sentence (the 7%). It also questioned the machine time given for step 1, which was wrong. Both are corrected in place with a note.
- **Its additions, not recomputed here:** drawing three-year blocks instead of single years gives an interval of +0.112 to +0.219, close to the one reported, so two-year events do not make the interval too narrow.

### What happens next

An outlook for the months ahead from the 2026 El Niño, under its own rule written before it is computed (`results/outlook-2026-27.md`).

### Audit of this result (2026-11-09), and what was changed for it

The coordinating session audited this result and the outlook at commit 69c0242, as the project's brief requires once, at the Phase 1 result. Its report is held outside this repo. Its reading: **pass with conditions**, and extend the work to a driver whose answer is not known in advance. It recomputed the pooled score from the rows and found the rule, the code and the scoring in the order claimed. Its five conditions are closed in the commit that adds this section:

1. Which of the plan's marks this result meets and which it does not: the last limit above. The stale clause promising an independent check "next" is gone from the line above; the check had been done.
2. The independent reader's report and code are committed (`docs/reviews/2026-11-09-continents-independent-check/`).
3. The makers' scaling of the drought index and of the ONI is recorded with its sources in `docs/data-sources.md` and `data/manifest.toml`, and the limits above name them. A re-scoring without that scaling is registered below as exploration.
4. Four corrections: North America's multiplier (0.68); the outlook's count of regions pushed wetter in South and Southeast Asia (24, not 23); `STATUS.md` now says the reader found no leak from fitting, which is what it tested; the false alarms are given by run and by naming. And the summaries now say that North America's own interval starts at +0.007.
5. The outlook's scoring rule names the drought file version (`results/outlook-2026-27.md`).

**No claim about conflict, or about any link between domains, follows from this result. The project's own question is still open.** The audit asked for that sentence wherever the result is summarised, and it is right.

### Exploration, registered 2026-11-09 before it is computed: does the makers' scaling move the score

**Exploration on a spent period. It marks nothing, it can neither rescue nor sink the pass above, and no later rule may cite it as a test.** Two limits above say the drought file and the ONI each let later years into the level or scale of earlier values. This measures how far the score moves when that is taken out, as far as it can be here.

On the four entered fields, at the region scale, the forecast step exactly as scored (`forecast.fit` on 1951 to 1999, scored on 2000 to 2024), four ways:

- **A, as tested.** It must reproduce +0.171, and the script stops if it does not.
- **B, drought re-scaled on the fitting years.** In each cell and calendar month, that cell-month's 1950 to 1999 mean is taken off and the values are divided by its 1950 to 1999 spread, before the clip at plus or minus 3 and the region averages. No year after 1999 then sets a cell's zero or its scale. This cannot undo the makers' fit of a distribution to the whole record, only its offset and scale, and it does nothing about the evaporation error.
- **C, El Niño on a fixed base.** In place of the ONI: NOAA's monthly Niño 3.4 anomaly from the same sea-surface product (`nina34.anom.data` on PSL's list, ERSST v6, anomalies from 1981 to 2010; held since the candidate fetch of `results/real-indices.md`, whose rule set it aside as El Niño by another name), with each calendar month's 1950 to 1999 mean taken off, then a three-month mean centred on each month, as the ONI has. Its zero is set by the fitting years and does not move with time. It keeps the ocean's warming, which the ONI's moving base takes out.
- **D, both.**

The naming is not re-run: the search read 1950 to 1999 only, and this is about the scoring. Reported for each: pooled S with its interval, S by field, claims, multipliers and the baseline chosen; and for the two indices, their correlation and means in each period. Code: `scripts/explore_bases.py` (written with this rule; only A has been run, to check that it reproduces). Rows: `results/explore-bases.jsonl`.

**Expectation, written first:** B moves the pooled S by less than 0.02. C lowers it, by up to 0.05, because slopes through zero are fed an index that sits higher after 2000 than the one they were fitted on. Nothing hangs on either guess.

**How it will be worded.** If the interval stays above 0 in every variant, the two limits stand as written: stated, and small. If any variant's interval reaches 0, that is said in the summary of this result wherever it is given.
