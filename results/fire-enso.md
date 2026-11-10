# A second domain's known answer: El Niño and burned area

Rule first, committed before any number that joins burned area to the ONI, to a decoy or to any other series (rule 9). Authority: decisions 0040 and 0045. Code: `src/causal_atlas/fire.py`, `src/causal_atlas/links.py` (`both`, unchanged), `src/causal_atlas/forecast.py` (unchanged but for letting a year with no data be left out of the fit), `scripts/run_fire.py`. Seeds: `results/seed-ledger.md`.

Burned-area data: ESA Climate Change Initiative, Fire CCI project. Chuvieco, E.; Pettinari, M.L.; Otón, G. (2020): AVHRR-LTDR Fire_cci Burned Area Grid product, version 1.1. Centre for Environmental Data Analysis. doi:10.5285/62866635ab074e07b93f17fbf87a2c1a. Terms and what to know before use: `docs/data-sources.md`.

## Why

Everything tested so far is climate against climate. The aim is relationships between separate data sets. Burned area is the first outcome here that is not a climate index, and it is added the way the review proposed: one data set, with a link others have published to rediscover first. The published link (Chen et al. 2016, Environmental Research Letters 11, 045001; what was read and how little weight its sizes bear is in `docs/reading/second-domain.md`): El Niño leads burned area by a season or more in several regions, most strongly in equatorial Asia. Only that direction and that place are taken from it, no size.

The question is whether this project's chain, unchanged, gets there by itself: the search names El Niño blind among decoys as a driver of burned area, and a forecast built from that beats each region's own history on years never read.

The record is short (37 years, one of them absent) and fire is a seasonal, patchy thing, so the first step measures what the search can hear on it. A silence means nothing until that is known.

## Seen before this rule

- **The product's own documents:** its README, terms, one file's header, and one file's (September 1997) variable ranges. From that file: the two variables named "fraction" are stored as per cent, 0 to 100, though their units attribute says 1. Both are divided by 100 here.
- **How much the satellite saw, with no burned-area value in it.** For cells more than 5% burnable, the mean share of burnable land observed, by year and by calendar month, **over all years including 2004 to 2018**:

  | Field | Cells | Yearly mean share seen | Cell-months with at least 0.2 seen | At least 0.5 |
  |---|---|---|---|---|
  | Africa | 7,225 | 0.57 to 0.69 | 98.4% | 74.4% |
  | South America | 6,445 | 0.43 to 0.56 | 92.0% | 53.5% |
  | Australia | 2,941 | 0.58 to 0.77 | 97.4% | 83.9% |
  | South and Southeast Asia | 5,559 | 0.37 to 0.49 | 80.0% | 36.0% |
  | North America | 7,518 | 0.34 to 0.43 | 68.6% | not noted |
  | Europe | 4,653 | 0.26 to 0.35 | 61.3% | not noted |

  North America and Europe are seen far less in winter (0.19 and 0.10) than in summer (0.59 and 0.55), and about 14% of their cell-months are not seen at all. South and Southeast Asia dips in the monsoon (0.35 in July). Several fields dip in 1984, 1988, 2000 and 2018, and later years are seen a little better than earlier ones (Africa about 0.63 before 2004 and 0.67 after). An earlier table of the same thing was printed on the wrong scale, before the per-cent error was found; it showed nothing this one does not.
- **Each field's shape under the settings below,** from the fitting years only: cells kept, regions of at least 40 cells, the calendar months in use, and the busiest three:

  | Field | Cells kept, of | Regions | Busiest three months | Used months per cell |
  |---|---|---|---|---|
  | Africa | 5,952 of 10,228 | 94 | October to December | 7.3 |
  | South America | 5,968 of 13,248 | 89 | July to September | 6.3 |
  | Australia | 2,673 of 5,712 | 48 | October to December | 6.6 |
  | South and Southeast Asia | 4,367 of 16,200 | 97 | August to October | 5.7 |
  | North America | 5,409 of 12,600 | 97 | July to September | 4.1 |
  | Europe | 2,659 of 7,000 | 55 | July to September | 3.7 |

  The "of" counts every cell in the box, sea included. Also seen: the spread of the standardised values on fitting months in use (0.95 to 0.97), the share of those that are zero because the year is absent or the month unseen (5% to 9%), the share clipped (0.3% to 0.65%), and the same two shares for the series of what the satellite saw (below): 4.5% to 8.4% zero, 0.3% to 1.0% clipped. Counting cell-months "burned in at least 5 fitting years" uses burned area above zero on the fitting years; no value, average, map or series of burned area was looked at.
- **A smoke test of the script on noise** shaped like these fields (seeds 18901 and 18999, a scratch rows file, not kept): the code runs; six ruler runs take about 3 seconds on the smallest field. On independent noise a planted link was found even at 5% of variance over a quarter of the cells, which says nothing about the real fields, where neighbouring cells move together.
- **The thresholds below were chosen after seeing the coverage table and before the shapes.** The first draft counted a cell-month as seen at half its burnable land, which the corrected scale showed would drop a quarter to three quarters of the record. 0.2 is the round figure that keeps at least 80% of cell-months in the four tropical and southern fields. That is a choice made with knowledge of how much each field is seen, and of nothing about fire against any driver.
- **Not seen: any correlation, map, time series or average of burned area against the ONI, a decoy, drought or the calendar year.**
- The author knows from this project's drought results where El Niño dries (South America, Australia, South and Southeast Asia, parts of North America; not Europe), and from general reading that the fires of 1997 and 1998 in Indonesia were very large. Both fall in the fitting years.

## Data and split

- **Grid:** the product's quarter-degree cells summed four to one onto this project's half-degree grid. Per cell and month: burned area in km², and the share of the cell's burnable land that was observed.
- **Value:** log(1 + km² burned / share observed). A cell-month counts as **seen** when at least 0.2 of its burnable land was observed. Dividing by the share observed assumes the part not seen burned like the part that was.
- **Standardised** per cell and calendar month on the seen months of the fitting years: less the mean, over the spread. A cell's calendar month is **in use** when it was seen in at least 15 fitting years and burned in at least 5 of them. Everything else is zero, which after standardising means "average for the month": cell-months not in use, months not seen, and all of 1994, which the makers left out. Clipped at plus or minus 3. A cell with no calendar month in use is dropped.
- **Fields:** Africa (this project's panel cells) and the five boxes of `results/real-enso-continents.md`: South America, Australia, South and Southeast Asia, North America, Europe. All six have regions to test.
- **Driver and decoys:** the ONI and 31 decoys per set (`decoy.make`, as before), 20 sets per field.
- **Fitting: 1982-01 to 2003-12.** Target years 1983 to 2003 without 1994: twenty. **Confirmation: 2004-01 to 2018-12, fifteen years,** sealed until step 2 is run, once. No burned-area value from those years enters anything fitted: the standardisation, the cells kept and the months in use all come from the fitting years (tested in `tests/test_fire.py`).

## Step 1a: what the search can hear on this record

`links.both`, unchanged: the broad gate and the sharp gate on 10-degree regions stepped by 5 degrees, lags 0 to 12, a candidate named by either. **Controls: the driver moved by 2 to 20 whole years** round the 22 fitting years, nineteen of them; the copies a year either side of the real alignment are left out, as decision 0044 requires.

A link is planted from the first decoy at lag 5, in the field's three busiest calendar months, in the nearest 5% or 25% of cells to a seeded centre, sized to 5%, 15% or 40% of variance, on cell-months in use only. Ten decoy sets per field, seeds 17701 to 18210; 360 runs.

- **A field is in earshot** when the link of 40% of variance over 25% of the cells is found in at least 8 of its 10 runs.
- Earshot marks nothing and does not decide whether a field goes on to step 2. It decides how a silence in that field is read: in earshot, "no link that large here"; out of earshot, "this record cannot say".
- Reported: the whole table; how often a decoy with nothing planted is named; where the planted link is found, the share of its claims that lie in the planted cells.

## Step 1b: naming, on 1982 to 2003

Twenty decoy sets per field, seeds 17101 to 17620. Four kinds of run per set:

1. the ONI among the 31 decoys;
2. the ONI left out;
3. the field's years in a seeded random order, 1994 left in place;
4. **what the satellite saw in place of what burned**: the share of burnable land observed, standardised the same way, with the ONI among the same decoys.

Marks, fixed now:

- **K1, the known answer:** the ONI is a lead in at least 18 of 20 sets in South and Southeast Asia, the box that holds equatorial Asia.
- **F1:** a decoy is a lead in at most 9 of the 120 runs of kind 1, the six fields pooled.
- **F2:** with the ONI left out, anything is a lead in at most 9 of 120.
- **F3:** with the years mixed, anything is a lead in at most 9 of 120.

9 of 120 is the same rate as the 8 of 100 used before, rounded down.

**Kind 4 marks nothing, and is there because the instrument is tied to the weather.** A dry year is a clear year, so El Niño can change how much the satellite sees. Dividing by the share observed corrects for that only to first order. If the ONI is a lead for what the satellite saw in at least 18 of a field's 20 sets, that is stated beside that field's result, and that field's link is read as "El Niño and burned area as this instrument records it", not yet as fire.

Reported, marking nothing: the ONI's count in every field; which gate named what; for each field, the region, calendar month and lag where the ONI's correlation with a region average is largest, with its sign; the counts for kind 4, decoys included.

## Step 2: the forecast check, on 2004 to 2018, once

It runs only if the ruler and the naming are complete and F1, F2 and F3 hold. **A field enters only if the ONI was a lead there in at least 18 of its 20 sets.** If no field enters, the years stay sealed. K1 is not a condition for running it: a field other than the expected one may enter.

The step is the one that passed on drought (`results/real-enso-continents.md`, "Step 2"), unchanged, on the twenty fitting years:

- **Units:** the 10-degree region averages. Single cells are reported.
- **Baseline (rule 2),** chosen per field among three on five blocks of fitting years: zero (the month's average); level (the unit's own last 60 months); linear (own values 3, 4, 5, 6 and 12 months back, the mean of all units 3 months back, own means over the last 12 and 60 months). Nothing later than three months before the target.
- **Claims:** for each unit and calendar month, the lag from 4 to 12 months with the largest absolute correlation between the ONI and the field, kept if significant by Benjamini-Hochberg at 5%.
- **Model:** baseline plus, on claimed unit-months, k times slope times the ONI at its lag; k one number per field from 0 to 1, chosen on five blocks of fitting years.
- **Metric:** S = 1 − (model's squared error) / (baseline's squared error) on the claimed unit-months of 2004 to 2018, **summed over the fields that entered**. Interval: 2,000 draws of the 15 years, 95%.
- **Control:** the same model with the ONI moved by each of 14 whole years within 2004 to 2018.
- **Passes when all three hold for the pooled score:** the interval's lower end is above 0; S is above all 14 shifted values; the model's error is below that of each of the three baselines alone.
- **Reported, marking nothing:** each field by itself, entered or not; single cells; the baseline chosen, k, the number of claims and their lags; and, if the ONI was named for what the satellite saw in some entered field, the pooled score without those fields.

Run once: `scripts/run_fire.py confirm once`, which refuses unless the conditions above hold and refuses a second scoring.

## What each outcome would mean

- **Recovered:** K1 holds and the pooled score passes. The chain found a published cross-domain link blind and it held on unread years. It would be the first result here whose outcome is not a climate index. It would still be nothing new about the world.
- **The pooled score passes without K1:** El Niño leads burned area out of time in the fields that entered, and the place the literature names loudest was not heard here. Reported as that, not as the registered known answer.
- **Named, but the forecast misses:** the search hears the link on 1982 to 2003 and it does not carry to 2004 to 2018 at four months or more. With fifteen years the interval is wide, so a miss here is weaker evidence than the drought result's pass was.
- **Not named in a field in earshot:** no link there as large as the ruler's, on this record. **Not named in a field out of earshot:** this record cannot say, and that is a limit of the method on short, seasonal records, to be published as one.
- **F1, F2 or F3 misses:** the search is not safe on this record as it stands. Step 2 is not run, the years stay sealed, and nothing is changed and rerun on these fields' fitting years without a fresh reader first.

## Guesses, written now so they cannot be adjusted

- Earshot: Africa, South America and Australia in; South and Southeast Asia in or close; North America and Europe doubtful, with few months in use per cell.
- The ONI named in at least 18 of 20: South and Southeast Asia about 50%, South America 45%, Australia 40%, Africa 35%, North America 30%, Europe 10%. Twenty years is a short fit and the search may hear nothing anywhere.
- F1 to F3: each between 2 and 7 of 120. The controls are nineteen where there were forty-seven, so the bar is coarser; a miss is possible.
- The ONI named for what the satellite saw: in one or two fields, most likely South and Southeast Asia.
- Step 2, if any field enters: a pooled pass about 35%. Recovered as registered: about 20% to 25%.

## Limits, stated now

- **Short.** Twenty target years to fit and fifteen to score. Beating all 14 shifted controls happens by chance once in 15; the interval is the main guard and it will be wide.
- **The instrument.** Several satellites with drifting orbits, stitched by the makers; that cannot be checked here. Pixels of about 5 km miss small fires. How much is seen is tied to cloud and so to the weather; dividing by the share seen corrects that to first order only, and which months count as seen is itself tied to cloud. Kind 4 looks at this and does not remove it.
- **Unseen and absent months are "average", not "no fire".** In the scored years they count as zeros the model is still asked to predict, which works against the model, not for it. Targets in 1995 take their own-history terms from 1994's zeros.
- **Thresholds were chosen after seeing coverage,** as said above, though not against any driver.
- **The significance test counts cell-months that are not in use,** which have no correlation with anything. That makes it stricter than it need be at the scale of cells.
- **The ONI is measured against a moving base** by its makers, so each value carries a little from later years (see the side check in `results/real-enso-continents.md`).
- **The forecast step was built on drought fields** and is carried over unchanged; it may suit fire less well. It is not tuned here.
- **The boxes are continents, not fire regions.** Equatorial Asia is one corner of a box that runs to the Himalaya.
- **One world per field, and a link others published.** A pass shows the chain works across domains on one known case. It does not show the chain finds what is not known.
- No person-level inference: cells of about 50 km and months.

## Estimates

Machine time: under half an hour for both parts of step 1 (840 searches), a few minutes for step 2. Tokens for the whole iteration, an independent reader included: about 500k fresh, to be reported beside the result.

## Result of step 1 (2026-11-10): a miss on every mark; step 2 is not run

Rows: `results/fire-enso.jsonl` (360 ruler runs, 480 naming runs, 6 rows of where the ONI's correlation is largest). Machine time about 12 minutes. No burned-area value after 2003 has been set against anything: **2004 to 2018 stay sealed.**

### The marks

| Mark | Needed | Got | |
|---|---|---|---|
| K1: the ONI a lead in South and Southeast Asia | 18 of 20 | **0 of 20** | missed |
| F1: a decoy a lead, the ONI among the candidates | at most 9 of 120 | **18** | missed |
| F2: anything a lead, the ONI left out | at most 9 of 120 | **18** | missed |
| F3: anything a lead, years mixed | at most 9 of 120 | **18** | missed |

The ONI was a lead in 0 of 20 sets in every field, 0 of 120 in all. No field enters step 2, and F1 to F3 would have stopped it anyway.

### The false-alarm marks could not have been expected to hold, and the author should have seen that before registering them

A candidate is named when its real alignment beats every year-moved copy of every candidate. With 19 moved copies, the strongest of the candidates does that by luck once in 20 in each gate, however many candidates there are. Over two gates that is about 1 run in 10 (9.75% if the gates were independent): about 12 of 120. The marks allowed 9, a rate carried over from fields with 47 or 49 copies, where the same arithmetic gives about 4%. A sound search would have held these marks about one time in four. That arithmetic was not done before the rule was committed, and the guess written there (2 to 7 of 120) was wrong for the same reason.

What was measured, 18 of 120, is above even that floor; a sound search would give 18 or more about 1 time in 25. By gate: broad 12, 12 and 10 of 120 for the three kinds, sharp 8, 8 and 8, against 6 expected in each. Kinds 1 and 2 are the same decoys on the same field and gave the same alarms, so they are one measurement, not two. So there may be something more than the floor on these fields, or it may be chance; this result cannot tell which.

**This does not reopen the earlier results.** With 49 controls the floor is about 4 in 100 and those runs measured 3, 3 and 5; with 47 it is about 4 and they measured 3 and 5 (`results/real-enso-continents.md`, `results/real-indices-2.md`). But it is a property of the search that was not written down before: **the false-alarm rate cannot go below about two in (controls + 1), and the number of whole-year controls is set by the length of the record.**

### What the search can hear on 1982 to 2003

Runs of 10 in which the planted link was found:

| Field | 5% over 5% | 5% over 25% | 15% over 5% | 15% over 25% | 40% over 5% | 40% over 25% | In earshot |
|---|---|---|---|---|---|---|---|
| Africa | 0 | 0 | 0 | 4 | 4 | 9 | yes |
| South America | 0 | 0 | 0 | 1 | 4 | 10 | yes |
| Australia | 0 | 0 | 0 | 0 | 0 | 7 | no |
| South and Southeast Asia | 0 | 0 | 1 | 3 | 3 | 10 | yes |
| North America | 0 | 0 | 0 | 5 | 2 | 10 | yes |
| Europe | 0 | 0 | 0 | 6 | 6 | 9 | yes |

- A link of 40% of variance over a quarter of the cells in one season is heard in 55 of 60 runs; anything smaller in at most a third.
- The bar a region's correlation must clear in the sharp gate was 0.85 to 0.95 across the 120 naming runs. On twenty years, only a nearly exact relationship in some region is named.
- **Mapping does not work at this length.** Where the largest planted link was found, the number of cell-month-lags then claimed ran from 0 to about 10,000, and in 7 of the 55 runs it was 0: the driver is named and nothing can be said about where. Where there were claims, 90% or more lay in the planted cells in all but one run (51%, on 102 claims).
- A decoy with nothing planted on it was named in 39 of the 360 ruler runs (11 of the 60 decoy sets; the six runs on one set are not independent), about 1 in 9.
- Guessed: Africa, South America and Australia in earshot, the two northern fields doubtful. Wrong on both counts: Australia is the one out, and the northern fields are in.

### Where El Niño stood

- **Against burned area it is not close.** It was among the five strongest candidates of either gate in no set in Africa, South America, Australia or Europe, and in the broad gate in 2 of 20 in North America. In South and Southeast Asia it was among the five sharpest in 14 of 20 sets and never the sharpest. Its largest correlation with a region's average there: +0.81, for March, two months back, around 5°N 125°E. That is the sign and the part of the world the published link gives, and it is below the bar (0.87 to 0.93), about where the best decoy stands.
- **Against what the satellite saw it is stronger than against what burned.** In South and Southeast Asia the ONI was among the five strongest in all 20 sets in both gates and the sharpest candidate in 18; in South America among the five strongest in 19 and 20. It was named in 3 of 20 in South and Southeast Asia and in none elsewhere, so by the rule nothing is flagged. But the order is plain: **on this record El Niño shows more clearly in how much of the land the instrument could see than in the burned area it reports.** Any link between El Niño and burned area drawn from this product has that beside it.
- Guessed: the ONI named in South and Southeast Asia about one time in two, and in South America, Australia and Africa a little less. It was named nowhere.

### What this means

- **The known answer was not recovered.** By the rule's own reading: in the five fields in earshot there is no link from El Niño to burned area as large as 40% of a season's variance over a quarter of the field on 1982 to 2003; in Australia this record cannot say. The published link is not contradicted: it is far smaller than that, and was never shown out of sample.
- **The search as built does not suit a record this short.** Two reasons, both arithmetic: with 19 controls its false-alarm floor is about 1 in 10, and on 20 years the bar it sets is a correlation near 0.9. Naming one driver for a whole continent, blind among 32, needs more years than a satellite record has. That is a limit of this method, not a finding about fire.
- **Nothing is changed and rerun on these fields' fitting years without a fresh reader first,** as the rule says. The burned-area years after 2003 are unread and unspent.
- What the short record does have is many places. A driver that differs from cell to cell (local drought, not one ocean index) can be tested across thousands of cells at once, with years as the unit of evidence. That is a different question and a different test, and it needs its own rule and its own known-answer check before it touches these fields.
