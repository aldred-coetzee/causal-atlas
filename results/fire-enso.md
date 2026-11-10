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

**Corrected in place on 2026-11-10 after the independent check (last section). What this section first said is given where it is changed; the first text is in commit 3d3d1de.**

A candidate is named when its real alignment beats every year-moved copy of every candidate. If the real alignment and the copies were judged on equal terms, with 19 moved copies the strongest of the candidates would do that by luck once in 20 in each gate, however many candidates there are. Over two gates that is about 1 run in 10 (9.75% if the gates were independent): about 12 of 120. The marks allowed 9, a rate carried over from fields with 47 or 49 copies, where the same arithmetic gives about 4%. On that arithmetic a sound search would have held one such mark about one time in four, and the two separate measurements here together about 7 times in 100 (this first said "about one time in four" for the marks together). That arithmetic was not done before the rule was committed, and the guess written there (2 to 7 of 120) was wrong for the same reason.

**But the terms are not equal, and that arithmetic does not describe this search.** This paragraph first said that 18 of 120 "is above even that floor", that a sound search would give it "about 1 time in 25", and that it could not tell chance from something in the fields. The reader found the cause. Decision 0044 left out the copies a year either side of the real alignment (here the copies moved 1 and 21 years), because they are the series itself. Every copy that remains still has its own neighbours a year either side among the copies, and neighbours a year apart resemble each other (their values correlate at about +0.24). So the real alignment alone has lost the two rivals most likely to beat it, and it comes out on top more often than once in 20.

Measured by the reader on fields with nothing in them, any alarm with the copies as used against any alarm with all 21 copies: the real South and Southeast Asia field with fresh decoys, 15% of 150 runs (10% to 22%) against 7%; the same field detrended, 17% against 6% (87 runs); smooth noise shaped like Africa, 13% against 7% (150); the real North America field, 7% against 7% (150); a made-up field with a strong trend, 44% against 17% (86). Over all 1,055 of its runs the broad gate alarmed with the copies as used and not with all 21 in 54 runs, and the other way round in 8. A spot check by this session with the reader's script on 80 fresh decoy sets for South and Southeast Asia (seeds 19801 to 19880): 14 of 80 against 9 of 80, and no run where all 21 alarmed and the copies as used did not.

**So 18 of 120 is about what this search gives on these fields when nothing is there. It is not a sign of anything in the fields, and the marks missed because of the control set as well as the record's length.** By gate: broad 12, 12 and 10 of 120 for the three kinds, sharp 8, 8 and 8. Kinds 1 and 2 are the same decoys on the same field and gave the same alarms, so they are one measurement, not two.

**The earlier results, one by one** (this paragraph first said "This does not reopen the earlier results" of both). `results/real-enso-continents.md` judged against all 49 copies, on equal terms: its floor is about 4 in 100 and it measured 3, 3 and 5. It is untouched. `results/real-indices-2.md` used the copies moved 2 to 48 years, the same lopsided set as here, so its floor is above the 4 in 100 first given here; the reader's null on a 50-year record gave 4.9% against 2.5% with all 49 (81 runs, too few to size it). Its step 1 stands as measured: a decoy named in 3 of 100 and anything named with the years mixed in 5 of 100, against 8 allowed, and a higher floor only makes those harder to hold. Every pair it named then failed the forecast step, so no claim rests on it. A note is added to that file.

The sentence first in bold here, that the false-alarm rate cannot go below about two in (controls + 1), holds only when every alignment is judged against the same kind of set. **For the set decision 0044 defines, the rate is higher than that and depends on the data.** Decision 0046 records this and sets the search aside until it is put right and measured.

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
- **Mapping does not work at this length.** Where the largest planted link was found, the number of cell-month-lags then claimed ran from 0 to about 10,000, and in 7 of the 55 runs it was 0: the driver is named and nothing can be said about where. Where there were claims, 90% or more lay in the planted cells in all but one run (51%, on 105 claims; first given as 102, corrected 2026-11-10 from the rows).
- A decoy with nothing planted on it was named in 39 of the 360 ruler runs (11 of the 60 decoy sets; the six runs on one set are not independent), about 1 in 9.
- Guessed: Africa, South America and Australia in earshot, the two northern fields doubtful. Wrong on both counts: Australia is the one out, and the northern fields are in.

### Where El Niño stood

- **Against burned area it is not close.** It was among the five strongest candidates of either gate in no set in Africa, South America, Australia or Europe, and in the broad gate in 2 of 20 in North America. In South and Southeast Asia it was among the five sharpest in 14 of 20 sets and never the sharpest. Its largest correlation with a region's average there: +0.81, for March, two months back, around 5°N 125°E. That is the sign and the part of the world the published link gives, and it is below the bar (0.87 to 0.93), about where the best decoy stands.
- **Against what the satellite saw it is stronger than against what burned.** In South and Southeast Asia the ONI was among the five strongest in all 20 sets in both gates and the sharpest candidate in 18; in South America among the five strongest in 19 and 20. It was named in 3 of 20 in South and Southeast Asia and in none elsewhere, so by the rule nothing is flagged. But the order is plain: **on this record El Niño shows more clearly in how much of the land the instrument could see than in the burned area it reports.** Any link between El Niño and burned area drawn from this product has that beside it.
- **The two were not heard on equal terms** (added 2026-11-10 from the independent check). The share observed has a value in every cell-month and rises with the year in every field (the field mean correlates with the year at +0.40 to +0.68: the instrument sees more in later years). Burned area is zero in 56% of cell-months and falls with the year in the four tropical fields (about −0.37). A dense series with a trend is easier for this search to tie to an index than a sparse one. The reader also confirmed the +0.81 (its figure +0.805) and found it a weak place to look: in March only 15 of that region's 66 cells are in use, and there burned area correlates 0.66 with the raw share observed. Against the share observed the ONI's best is +0.88, over the Philippines in February, one month back, and 0.85 to 0.92 with any one year left out.
- **The known answer may not be in this record** (added 2026-11-10 from the independent check). The fires the published link is best known for are those of 1997 in equatorial Asia. In this product, burned area for August to October 1997 ranks 13th of the 21 fitting years on Borneo and 12th on Sumatra. Why the product does not show that year as large was not looked into. No search could have recovered the link from a record that does not hold its largest event.
- Guessed: the ONI named in South and Southeast Asia about one time in two, and in South America, Australia and Africa a little less. It was named nowhere.

### What this means

- **The known answer was not recovered.** By the rule's own reading: in the five fields in earshot there is no link from El Niño to burned area as large as 40% of a season's variance over a quarter of the field on 1982 to 2003; in Australia this record cannot say. The published link is not contradicted: it is far smaller than that, and was never shown out of sample.
- **The search as built did not work on this record, and the record's length is only part of why** (corrected 2026-11-10 after the independent check; this first gave "two reasons, both arithmetic" and said the search "needs more years than a satellite record has", which was not shown). Three things, not separated from each other here: the control set raises false alarms (above; decision 0046); blind among 32 candidates, over every region, calendar month and lag, on 20 years, the bar it sets is a correlation near 0.9, and how much of that is the short record and how much the breadth of the search was not measured; and the product does not show the event the known answer rests on. That is a limit of this method and this product, not a finding about fire.
- **Nothing is changed and rerun on these fields' fitting years without a fresh reader first,** as the rule says. The burned-area years after 2003 are unread and unspent.
- What the short record does have is many places. A driver that differs from cell to cell (local drought, not one ocean index) can be tested across thousands of cells at once, with years as the unit of evidence. That is a different question and a different test, and it needs its own rule and its own known-answer check before it touches these fields.

### Independent check (2026-11-10, one fresh reader, 455k fresh tokens by the counter against 200k estimated)

A reviewer with no part in the work was given the rule, the rows and the code, and asked to break the result. Its verdict: **"Holds with corrections"**: the miss stands, the forecast step was rightly not run, and the explanation given for the false alarms was wrong. The corrections are made above, in place, each with a note. Its report in full and its sixteen scripts are in `docs/reviews/2026-11-10-fire-enso-independent-check/`. The reader could not write its own report file; this session saved the text it handed back, unchanged.

- **Data step:** South and Southeast Asia's fitting years rebuilt from the raw files by its own code: the same cells, the same months in use, the same values (113 differed until it stored the share observed as the project does, a rounding at the 0.2 threshold; then none). Both "fraction" variables are per cent, confirmed at source.
- **Leaks:** every burned-area value from 2004 on replaced by noise, twice; the fitting-year field is identical (checked for South and Southeast Asia and Europe) and South and Southeast Asia's step 1 rows come out as committed. The decoys take their spectrum from the whole El Niño index, 1982 to 2018: that is the driver, not burned area.
- **Text against rows:** every number matched except one (105 claims, not 102).
- **The false alarms:** the cause is the control set of decision 0044, measured on nulls as given above. This session reran its recount (matches) and spot-checked its central finding on fresh seeds (above).
- **El Niño and the share observed:** confirmed, and not explained away by the share observed being near-constant (it is not: a median spread of 0.10 on a median of 0.40). But the two series are not heard on equal terms, as added above.
- **1997:** as added above.
- **The reader's cost:** 455,405 fresh tokens against the 200k this session estimated, one rewrite of its context among them. An overrun, reported here as decisions 0035 and 0036 say.
- **Not checked by it:** why 1997 is small in the product; machine times; the exact size of the raised floor in `results/real-indices-2.md`.
- **Its cautions for a test of local drought against burned area** are taken into that test's rule (`results/fire-drought.md`): drought brings clear sky, so more is seen; shared trends; the years, not the cells, are the samples; shared seasons; El Niño may stand behind both; months not observed; breaks in the record; many places tested at once.
