# Twenty-five real series at once: which does the search name, and does any add to the forecast beyond El Niño

Rule first, committed before any of these series is set against any drought value (rule 9). Authority: decisions 0040 and 0043. Code: `scripts/index_candidates.py` (the candidate rule), `scripts/run_indices.py`, `src/causal_atlas/forecast.py` (`residual`, `after`), `src/causal_atlas/links.py` (`both`). Seeds: `results/seed-ledger.md`.

## Why

The first real result (`results/real-enso-continents.md`) tested one real candidate that the author picked, on a link that is already known. The aim is to find relationships nobody picked. This test hands the search every series a rule lets in, with decoys, and asks three questions in order: can the search still hear a planted link with this many candidates, which real series does it name for each field, and does a named one improve a forecast beyond what own history and El Niño already give.

## The candidates: a rule, not a choice

The list is NOAA PSL's page "Monthly Mean Time-series" (<https://psl.noaa.gov/data/timeseries/month/>, read 2026-11-09): every series with a page of its own there, and the one or two data files that page names. 89 pages, 96 different files. `scripts/index_candidates.py fetch` downloads them all; run without `fetch` it prints the table below from the files. A file is in when, in this order:

1. **It is complete**, with no missing month, from 1950-01 to 2024-12. A month is missing when the file has no row for its year, or holds the file's own missing-value mark there. 45 files are not complete (two of them could not be fetched).
2. **It is not rainfall.** The page's "Precipitation Time-series" section is left out, because the outcome is built from rainfall and a rain gauge inside a field is the outcome measured another way. 2 files (a third rain series had already gone for missing months).
3. **It is not El Niño by another name.** Its largest absolute correlation with the ONI, at any lag from 12 months before to 12 after, on 1951 to 1998, is below 0.6. The ONI stands for the rest. 13 files out, from 0.68 to 1.00: the Niño 1+2, 3, 3.4 and 4 series in two versions each, the ONI itself and its relative version, the bivariate ENSO series, the Southern Oscillation, and the upper wind over the tropical Pacific. The highest kept: whwp 0.56, noi 0.51, tna 0.46, dmieast 0.44.
4. **It is not mostly a trend.** A straight line explains less than 0.25 of its variance on 1950 to 1999. 10 files out, from 0.29 to 0.56: the global and land temperature records of four makers, and the Pacific warm pool in two versions. The highest kept: tornado 0.19, dmieast 0.18, tsa 0.16, pdo 0.15.
5. **It is not a series already kept.** Its correlation at lag 0 with every series kept before it on the page is below 0.9 in absolute value, on 1950 to 1999. 1 file out: the second version of the Pacific Decadal Oscillation, 0.94 with the first. The next highest pair, both kept: tna and amm, 0.81.

Every measurement is taken on the series as it is used here (next paragraph), and none involves a drought value.

**Twenty-five are in**, by the source's file name, in the page's order: tni.long, amm, pmm, pmmwind, dmi.had.long, dmieast.had.long, npgo, pdo.timeseries.sstens, tna, tsa, whwp, ao.long, ea, noi, np.long, pna, scand, wp, gbi.mon, qbo.50mb, qbo, nao_gib.long, nao_ice.long, sunspot.long, tornado.us.mon. What each is, who makes it and under what terms: `docs/data-sources.md`. The list is frozen in `scripts/index_names.py`, and the run refuses to start if the rule no longer gives that list.

Each is used as its departure from its own calendar-month means over 1950 to 1999, divided by its spread over those months. So no year after 1999 sets its zero or its scale. The ONI is used as before, unchanged.

**How the rule was arrived at, so it can be judged.** The three thresholds were set after seeing the measurements, which are properties of the candidates alone. Each sits in the widest gap there is: nothing lies between 0.56 and 0.68, between 0.19 and 0.29, or between 0.81 and 0.94. A first draft used PSL's older list of climate indices and gave thirteen series. It was dropped before any commit and before any number against drought, because one of the thirteen, the Indian Ocean Dipole, was not on that list and had been added by hand. This page is PSL's fuller current listing and lets it in by rule. The rainfall rule and the same-series rule were added with the fuller list, which is where rain gauges and duplicate versions first appeared.

## Seen before this rule

- Everything in `results/real-enso-continents.md` and `results/outlook-2026-27.md`: the five fields on 1950 to 1999, and for the ONI model the baseline's and the model's error on 2000 to 2024, by field and year.
- For the candidates, on both lists: whether each month is present, the measurements above, the correlations among them, and for the first list how far each is correlated with itself a year on. **No series other than the ONI has been set against any drought value, in any year.**
- A smoke test of the code with decoys standing in for the 26 real series (seeds 14901 and 14999, never in a count): nothing named on Australia or North America; on Australia, one planted link of 40% and one of 15% of variance over a quarter of the cells were found, and none over a twentieth.
- The author knows some of the published science and expects, from memory and unchecked: the North Atlantic, Arctic, Greenland, East Atlantic and Scandinavian patterns named for Europe at short lags, with little to say months ahead; the Indian Ocean Dipole for Australia and for South and Southeast Asia; the tropical Atlantic series for South America; the Pacific patterns for North America; the tornado count, if anywhere, for North America and at no lead; sunspots and the stratospheric wind for nothing. Written here so it cannot be adjusted afterwards. No mark depends on it.

## The search

The frozen two-gate search (`links.both`), on the discovery years 1950 to 1999 of each of the five fields of `results/real-enso-continents.md`, clipped as there. Candidates in every run: the ONI, the 25 series and 18 decoys, **44 in all**.

Two things differ from the search as confirmed, both stated now:

- **44 candidates, not 32.** The bar a candidate must clear is the largest value among every candidate's 49 shifts, so more candidates raise it a little. That is why the instrument check below is run again and not carried over.
- **The cap on leads.** Each gate could name at most five. With 26 real candidates that could shut a real one out in every set, so the cap is 26 (27 where a link is planted). A candidate is still named only when it beats every shifted value of every candidate left.

## Step 1a: the instrument check and ruler, on 1950 to 1999

As in `results/real-enso-drought-2.md`, now on each of the five fields: a link is planted from one decoy into the nearest cells to a seeded centre, in three consecutive calendar months at lag 5, and the search is asked to find it among the other 43 candidates. Sizes: 5%, 15% and 40% of variance, over 5% and 25% of the cells. Ten decoy sets per field, fresh seeds 13601 to 14010; 300 runs. (2% is not run: neither earlier ruler heard it once.)

**Instrument check, fixed now:** the link of 40% of variance over 25% of the cells is found in **at least 45 of the 50** runs, in **at least 8 of 10 in every field**, and wherever it is found at least 80% of its claimed cell-month-lags lie in the planted cells. The earlier rule asked 9 of 10 on one field. Asking that of each of five fields would fail by chance about one time in three even if the true rate were 95%, so the mark is the same rate pooled, with a floor for each field.

If it misses, the search with this many candidates is not the instrument that was confirmed: step 2 is not run and the years after 1999 stay sealed for these series.

The rest of the table is reported and marks nothing. It is the limit to print beside whatever step 1b names or does not name. The ruler's runs are not naming runs: what they name among the real series counts for nothing.

## Step 1b: naming, on 1950 to 1999

Twenty decoy sets per field, fresh seeds 13101 to 13520. Each run is repeated with the field's years in a seeded random order.

Marks, fixed now:

- **N1:** the ONI is still a lead in at least 18 of 20 sets in each of the four fields where it was before (South America, Australia, South and Southeast Asia, North America). If real company loses it, this is not the search that was confirmed, and step 2 is not run.
- **N2:** a decoy is a lead in at most 8 of the 100 runs.
- **N3:** with the years mixed, anything is a lead in at most 8 of the 100 runs.
- **A series is named for a field** when it is a lead in at least 18 of that field's 20 sets. The sets differ only in their decoys, so this asks that the naming does not hang on which decoys were drawn.

If N1, N2 or N3 misses, step 2 is not run and the years after 1999 stay sealed for these series.

## Step 2: the forecast check, on 2000 to 2024, once

For each field with a named series, at the region scale (the headline) and the cell scale (reported):

1. The model as tested: baseline and El Niño term, fitted on 1951 to 1999 exactly as scored before (the code checks it against the scored row). What it leaves on every month is the residual: the baseline's residual, less the El Niño term where El Niño claims. For Europe, where El Niño made no claim, that is the baseline's residual alone.
2. For a named series, the same forecast step as before, applied to that residual instead of the drought value: for each region and calendar month the lag from 4 to 12 months with the largest correlation, kept where significant (Benjamini-Hochberg at 5%); a slope through the origin; one multiplier between 0 and 1 from five blocks of the fitting years. Lags start at 4 for every series, as for the ONI, so every forecast is made at least three months ahead.
3. S = 1 − (error with the series' term) / (error without it), over the region-months the series claims, on 2000 to 2024. "Without it" is the baseline plus El Niño, so S above 0 means the series adds something that own history and El Niño do not.

**A pair (series, field) passes when all three hold:**

- the lower end of S's interval is above 0. The interval is taken at 1 − 0.05/m, where m is the number of pairs named in step 1b whether or not they go on to make a claim, so that across all pairs the chance of any false pass by this mark is held near 5%. From 20,000 draws of years;
- S is beyond all 24 whole-year shifts of the series;
- the full model's error is below each of the three baselines alone on the same region-months.

A named series with no claim at lags 4 to 12 makes no forecast and is reported as that: related, with nothing to say three months ahead.

**Reported, marking nothing:** claims, lags, the multiplier, S by year, the cell scale. And **a straight line in time** put through the same step in each field scored. Several of these series carry a trend, the drought index has one in places, and whole-year shifts do not guard against two trends. Wording fixed now: where a passing series' S is not above the line's S in that field, the pass is described as not told apart from a trend.

The step is run once (`scripts/run_indices.py confirm once`, which refuses a second scoring), after the results of step 1 are committed. After it these fields' later years are spent for these series.

## What each outcome would mean

- **Instrument check missed:** with 44 candidates the search is too deaf on these fields. Published as that; the search needs work before real candidates are judged by it.
- **Nothing beyond the ONI named:** at the size the ruler says this search can hear, El Niño is the only one of these 26 that drives drought on these fields in 49 years. A plain result, published as that, with the ruler beside it.
- **Named, but no pass:** related in the fitting years, and either not usable months ahead or not holding up after 1999.
- **A pass:** the first relationship this project found without being pointed at it. It would then be read against the published science, at source, before anything is said about it.

Whatever comes out is about climate series and drought. It says nothing about conflict, prices or any link between domains, and the project's own question stays open.

## Limits, stated now

- The fields' years after 1999 are not unread: they were scored once for the ONI. No other series has been set against them, and the forecast step is not changed by what was seen. The forecast step itself was shaped on Africa's later years before it was fixed, and Africa is not in this test for that reason.
- The series are not independent of each other or of El Niño (the closest kept pair is correlated 0.81). Naming does not say which of two related series is the driver, or which way a link runs. Step 2 removes El Niño only where and as the tested model claims it, and scores each pair on its own: two passes in one field may be one signal counted twice.
- A series with a trend can be named because the field has a trend. The straight-line control in step 2 is the guard; naming has none.
- The makers revise these series. Several are patterns computed from the whole record, later years included, so a pattern's shape can carry knowledge of years after 1999. Re-centring on 1950 to 1999 removes the offset and the scale, not that.
- Drought here is SPEI-3 from one file, standardised by its makers over the whole record, and the ONI is NOAA's, on base periods that move with time. Both let later years into the level of earlier values.
- The interval at 1 − 0.05/m comes from draws of 25 years. For many pairs it reaches far into the tail of those draws and is rough.
- Lags 4 to 12 only: a link that acts within three months cannot pass step 2, by design.
- Forty-nine fitting years. Slow series (pdo, npgo, the Atlantic ones, sunspots) complete between one and five swings in that time; their shifted controls allow for this at naming, and nothing else does.
- The tornado count and the sunspot number are not climate patterns. They are in because the rule lets them in, which is the point of a rule; a result for either is read with that in mind.

## Estimates

Step 1a: about 25 minutes of machine time. Step 1b: about 15. Step 2: about 5. Tokens to the report: about 300k.

## Results of step 1 (run 2026-11-09, 22:32 to 23:23 UTC; rows in `results/real-indices.jsonl`)

Everything above this line was committed before any of these numbers existed. 500 runs, all on 1950 to 1999.

### Step 1a. The instrument check: missed, on all three parts

| Part of the mark | Asked | Got |
|---|---|---|
| The link of 40% of variance over 25% of the cells found, pooled | at least 45 of 50 | **42 of 50** |
| The same, in every field | at least 8 of 10 | South America 9, Australia 10, **South and Southeast Asia 4**, North America 9, Europe 10 |
| Where found, share of claims in the planted cells | at least 0.80 | 41 runs between 0.85 and 1.00; **one at 0.73** (South America, seed 13608) |

The ruler, found out of 10, by share of variance and share of cells:

| Field | 5% over 5% | 5% over 25% | 15% over 5% | 15% over 25% | 40% over 5% | 40% over 25% |
|---|---|---|---|---|---|---|
| South America | 0 | 0 | 0 | 0 | 0 | 9 |
| Australia | 0 | 0 | 0 | 1 | 4 | 10 |
| South and Southeast Asia | 0 | 0 | 0 | 0 | 0 | 4 |
| North America | 0 | 0 | 0 | 0 | 3 | 9 |
| Europe | 0 | 0 | 0 | 0 | 4 | 10 |
| All five | 0 of 50 | 0 of 50 | 0 of 50 | 1 of 50 | 11 of 50 | 42 of 50 |

For scale, and not a like-for-like comparison because the field differs: on Africa with 32 candidates, of which one was real, the same search found 40% over 5% in 9 of 10, 40% over 25% in 10 of 10 and 15% over 25% in 5 of 10 (`results/real-enso-drought-2.md`).

A decoy that had no link planted was named in 6 of the 300 runs. All six are one decoy set (Australia, seed 13709) and the same decoy each time.

### Step 1b. Naming: N1 missed, N2 and N3 held

| Mark | Asked | Got |
|---|---|---|
| N1: the ONI still a lead where it was before | at least 18 of 20 in each of four fields | South America 20, Australia 20, North America 20, **South and Southeast Asia 0** |
| N2: a decoy a lead | at most 8 of 100 | 0 |
| N3: anything a lead with the years mixed | at most 8 of 100 | 2 (North America 13401, the tropical South Atlantic series, by the sharp gate at 0.719 against a bar of 0.695; Europe 13506, a decoy, by the broad gate) |

In South and Southeast Asia the ONI was the third-ranked candidate in the broad gate and the second in the sharp gate, behind real series in both, and the search stops at the first candidate that fails to clear the bar.

### What follows from the rule

**Step 2 is not run. The years after 1999 stay sealed for all 25 series.** The rule said that if the instrument check or N1 missed, this is not the search that was confirmed, and it is not. This is the first of the outcomes written above: with 44 candidates, 26 of them real, the search is too deaf on these fields, and it needs work before real candidates are judged by it.

### What the search named, which by the rule counts for nothing

Recorded because the rows hold it. No claim is made from it, and none of these pairs has been set against any year after 1999. Sets out of 20 in which a series was a lead:

| Field | At 18 or more | Below 18 |
|---|---|---|
| South America | ONI 20, tropical South Atlantic (tsa) 19, Northern Oscillation (noi) 19 | |
| Australia | ONI 20 | Indian Ocean Dipole (dmi) 8 |
| South and Southeast Asia | Pacific Meridional Mode wind (pmmwind) 20 | ONI 0 |
| North America | ONI 20, noi 20, eastern Indian Ocean pole (dmieast) 19 | Pacific Decadal Oscillation 16 |
| Europe | Scandinavian pattern 20, North Atlantic Oscillation (Gibraltar) 20, Arctic Oscillation 19, Greenland Blocking 19 | East Atlantic 12 |

Against the guesses written above before the run: Europe's list is the one guessed. The tropical Atlantic for South America and Pacific patterns for North America were guessed. The Indian Ocean Dipole for Australia fell short, and it was not named for South and Southeast Asia. Sunspots, the stratospheric wind and the tornado count were named for nothing, as guessed. The eastern Indian Ocean pole for North America was not guessed. A search that has just failed its own check cannot tell which of these are real.

### One thing the rows show about why

In every field the sharp gate's bar is the same number in all 20 decoy sets: 0.777 in South America, 0.726 in Australia, 0.854 in South and Southeast Asia, 0.777 in North America, and 0.675 in Europe in 17 sets of 20 (0.689, 0.696 and 0.704 in the other three). Decoys differ from set to set, so a bar that does not move is being set by the shifted copies of a real series, not by a decoy. One bar is shared by every candidate, so one real series whose shifted copies still correlate strongly with a region raises the bar for all the others, the planted link and the ONI included. With one real candidate among 31 decoys that could happen only through the ONI; with 26 it is the rule. Which series set the bar, and what to do about it, is the next piece of work, on the fitting years only.

### Disclosures

- **Order of looking.** The ruler ran first and its rows were looked at while it ran. They showed tsa and noi named on South America before any naming row existed, and South America's line of the ruler table was seen at 110 rows. The rule says the ruler's namings count for nothing; the naming marks are counts fixed in advance and no choice was open between the two.
- **Machine time:** 51 minutes (ruler 37, naming 14) against 40 estimated, on a box that was busy with other work for the first half.
- **A code change during the run,** committed separately: the runs skip rows already made, so a stopped run can be picked up. It was not needed; the run finished unbroken, and the change touches no rule, seed or mark.
