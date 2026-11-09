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

Rows: `results/real-enso-continents.jsonl` (305: 300 runs and one `where` row per field). Run as committed, no deviation. Machine time about 35 minutes.

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
- False alarms, all eleven runs: four from the sharp gate (by 0.004 to 0.014 over its bar in the three where the row holds the bar that applied) and seven from the broad gate. The 3 of 100 with the ONI left out are the same decoy sets as the 3 with it in, as on Africa.
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

By field, region averages. The first four entered the pooled score; each also meets the pass rule on its own, which was not required.

| Field | S | Interval | Shifted controls | Claims (of region-months) | Baseline chosen | k |
|---|---|---|---|---|---|---|
| South America | +0.161 | +0.097 to +0.224 | -0.268 to -0.017 | 353 of 1,140 | linear | 0.76 |
| Australia | +0.129 | +0.068 to +0.183 | -0.107 to +0.051 | 113 of 588 | linear | 0.47 |
| South and Southeast Asia | +0.224 | +0.148 to +0.292 | -0.389 to -0.078 | 260 of 1,200 | linear | 0.77 |
| North America | +0.117 | +0.007 to +0.214 | -0.330 to +0.028 | 57 of 1,260 | linear | 0.67 |
| Europe (did not enter) | none | | | **0 of 768** | zero | 0 |

Reported, marking nothing:

- **Single cells:** pooled S +0.137, interval +0.093 to +0.180, larger than all 24 shifted (-0.217 to -0.031), below every baseline alone. By field +0.131, +0.100, +0.172, +0.089, each with its interval above 0. Europe: no claim in 56,520 cell-months.
- **By year, pooled regions:** the model had less error than the baseline in 22 of the 25 years. The three where it was worse (2001, 2013, 2014) were worse by 1% to 5%. The gain does not rest on one event: the largest years are 2015 (+0.39), 2011 (+0.35), 2010 and 2022 (+0.32), and no year carries more than 7% of the error being explained.
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

- **The drought index is standardised over its whole record by its makers**, 1901 to the present, so each value's scale carries a little information from later years. That touches the target and the baseline's inputs alike and cannot tell the model which way a given month went, but it is not a strictly out-of-time quantity and is said here.
- **The gain is measured on the region-months the method chose to speak about** (19% of them in the four fields). On the rest it makes no forecast beyond the baseline.
- **The link is one whose existence was known to the author before the test**, and the five boxes were drawn with that knowledge (four where a link is published, one where it is not). What was blind: which candidate among 32 the search would name, where, when, how large, and every number on 2000 to 2024.

### What happens next

An outlook for the months ahead from the 2026 El Niño, under its own rule written before it is computed (`results/outlook-2026-27.md`), and an independent check of this result by a fresh reader.
