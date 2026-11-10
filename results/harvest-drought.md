# A country's drought and its cereal harvest that year

Rule first, committed before any counted number and before any real yield is set against drought (rule 9). Authority: decisions 0040 and 0051. Code: `src/causal_atlas/harvest.py`, `src/causal_atlas/yields.py`, `synth/harvest_panel.py`, `scripts/run_harvest.py`, tests in `tests/test_harvest.py`. Seeds: `results/seed-ledger.md`. Rows: `results/harvest-drought.jsonl`.

Data, both held and described in `docs/data-sources.md`: yields from FAOSTAT, Crops and livestock products (FAO, CC BY 4.0; file dated 2025-12-31, 1961 to 2024); drought from SPEIbase 2.11.0 (SPEI-3, built from CRU TS 4.09; ODbL 1.0).

## Why

Two tests outside climate have ended without a link: burned area found nothing, and food prices were set aside because a market's own price already carries the news of a dry season. A harvest is different in the one way that matters here: last year's yield says little about this year's weather. So if weather shows anywhere in a record kept by people and not by instruments, it should show here.

The question: **does the weather of the months up to a harvest, as one drought index averaged over the country, improve an estimate of that year's official yield beyond what the yield's own past and its neighbours' already give, on years never fitted?**

This link is known. Finding it is a rediscovery, and the reason to look is that it would be the first link this project has heard from one domain into another, with a baseline, controls and an out-of-time score. What is given up to ask it is in decision 0051: a country and a year, not a place and a month; no crop calendar and no map of cropland.

## What has been looked at, and what has not

- **Not looked at: any real yield beside any drought value.** `scripts/run_harvest.py real once` is the first time, and it refuses unless the marks below hold.
- **Looked at, each side alone:** the yields (how many records, how long, how rough, how alike neighbours are, how well each baseline forecasts them) and the country drought series (spread, memory, drift, how alike neighbours are). The made-up records were shaped on those.

The real panel: 503 records (a country's series of one cereal with 30 or more official years, in a country the drought file covers) in 141 countries. Wheat 99, maize 117, rice 94, barley 79, sorghum 69, millet 45. From 1986 to 2024, 16,763 official figures have enough past to be forecast, 320 to 480 a year.

## Method

Fixed now. Names in brackets are in `harvest.py`.

- **Outcome.** The log of yield, for each record and year. Only official figures (FAOSTAT flag A) are forecast and scored; estimated and imputed ones are used as past values and never as targets.
- **Every year is forecast from earlier years only.** The baseline is chosen again each year, the slopes fitted again, their weights set again. A test checks that changing everything from a year on leaves every earlier forecast as it was.
- **A record's scale** in a year is the root mean square of its earlier year-on-year changes (at least 0.02). Errors are divided by it and clipped at 4, so a rough record does not outweigh a steady one. A record is forecast once it has ten known earlier years.
- **Baselines, seven** (BASELINES): last year's figure; the mean of the last three and of the last five; a straight line through the last ten and the last twenty; the twenty-year line plus two slopes, shared by all records, on how far the record and its neighbours (the same country, or the same cereal within 1,500 km) stood above their lines the year before; and a blend, the three-year mean moved towards each of the others by a share fitted on earlier years. **The baseline in force in a year is the one with the least error over all earlier years.** On the real yields alone, 1986 to 2024, the blend is best (0.89 in the units above, against 0.96 for the three-year mean and 1.04 for last year's figure).
- **Driver.** Each country's SPEI-3, the mean over its half-degree cells that have a value every month. Six values per harvest year that do not overlap (SEASONS): September and December of the year before, and March, June, September and December of the harvest year. Each is set to mean zero and spread one with the country's own earlier years.
- **The driver's term.** Slopes of the baseline's error on the six values, fitted with a ridge of 10 on earlier years at five scales (SCALES): the record alone; every cereal in its country; the same cereal near by, at 1,500 km and at 4,000 km; the same cereal everywhere. Each scale gives a forecast; the five are added with weights, none below zero, shared by all records and fitted on how the scales' earlier out-of-time forecasts did. The term is clipped at 4. No season, sign or place is named: a cereal's season differs by country and is left to the slopes.
- **Years.** The first year forecast is 1981 and the weights need five years of forecasts behind them, so **1986 to 2024 are scored: 39 years.** The year is the unit of evidence: records in one year share weather and markets, and are counted once.
- **S** is the share of the baseline's squared error that the term removes over the scored years. Its interval is the middle 95% of 2,000 draws of years.
- **Controls: the weather of other years.** The whole forecast is made again with the driver moved by 2, 3, … 63 whole years round its 65-year record: 62 forecasts with the right country, the right months and the wrong years. One year either way is left out, because two of the six values would then be real.
- **The flat driver.** Everything again with each country's and calendar month's mean and straight line over the whole record taken out of the driver, and the shifts of that. This uses the driver's later years, and is a control only.

**Read as a link** when all of these hold (`reading`):
1. S is at least 0.2% and its interval is above zero;
2. S is above S under every one of the 62 shifts;
3. the model's error is below the mean of its error under the shifts, with an interval above zero;
4. 1 to 3 hold again with the flat driver;
5. the model's error is below each of the seven baselines' alone;
6. S is above zero without its best year.

**Two variants.** *Year-end* uses all six values: an estimate made when the harvest year closes, about a year before the official figure is published. **It is the result.** *Mid-year* uses the first four, to June of the harvest year. It is reported beside, with its own marks, and is not the result.

**Where it helped before** (`kept`), a second reading, also not the result: records are ranked by the share of their error the term removed in the earlier half of the scored years (1986 to 2004; ten scored years needed), and the top third are scored in the later half (2005 to 2024), with the same done under each shift. It asks whether the places the link shows in are stable enough to be named. Reported: S there, its interval, shifts beaten, and the records.

Also reported, without marks: S by cereal; S under the shifts; the weights; each record's own gain.

## Step 1: made-up records

`synth/harvest_panel.py` shares no code with the detector. A made-up world has about 141 countries in clusters and about 500 records. Moisture is monthly, shared by neighbours, with a slow swing the whole world feels, a memory of a few months and a slight drying in most countries. A record's yield has a level, growth that changes once or twice, a level that wanders and does not come back, a memory, shocks shared with neighbours, rough stretches, late starts, gaps and stretches of unofficial figures, some carried forward. Where there is a link, the mean moisture over a season of two to four months moves the yield, a dry season costing more than a wet one gives; the season's place in the year depends on the cereal and the hemisphere, and in the tropics on the country. **The detector is told none of this, and its six fixed months do not line up with the seasons.**

`run_harvest.py known`, every seed read exactly as the real record will be, 62 shifts. Fresh seeds, never used before.

| Panel | What is in it | Seeds | Mark, year-end | Mark, mid-year |
|---|---|---|---|---|
| Link, 20% | In about half the countries, in patches, the season's moisture takes 20% of the variance of the yield's year-to-year departures | 22001 to 22010 | **read in at least 8 of 10** | at least 8 of 10 |
| Link, 10% | The same at 10% | 22101 to 22110 | measured | not run |
| Link, 5% | The same at 5% | 22201 to 22210 | measured | not run |
| Link in few, 20% | 20%, in a fifth of the countries | 22601 to 22610 | measured | not run |
| Nothing | No link | 22301 to 22330 | **read in at most 1 of 30** | at most 1 of 30 |
| Drift | No link; a drying or wetting that speeds up, and yields bending the same way in the same places | 22401 to 22420 | **at most 1 of 20** | at most 1 of 20 |
| Step | No link from year to year; in patches the climate turns drier for good in one year and yields there drop to a lower path the same year | 22501 to 22520 | **at most 1 of 20** | at most 1 of 20 |

The measured panels are the ruler: the smallest link heard in most seeds is what a silence on the real record would rule out, for a link of this shape.

**If a year-end mark misses, no real yield is set against drought** (`run_harvest.py real once` refuses), and the result is a null about this method. If only a mid-year mark misses, the mid-year reading of the real record is reported as unmarked.

**Before step 2, an independent reader sees this rule, the code and the made-up results.** What it finds is applied and disclosed before any real yield is read.

## Step 2: the real record, once

`run_harvest.py real once` (refuses a second run): year-end, then mid-year. There is no fitting step before it: every setting above was fixed on made-up records and on each side alone, and every scored year is forecast from the years before it.

## What each outcome would mean

- **Read as a link, year-end.** Knowing how dry each country was in the months to its harvest improves an estimate of the official yield, on years never fitted, beyond the yield's own past, and not through a shared drift. A known link, heard blind to season, sign and place. It gets an independent reader before it is called a finding. **The size is given with its plain meaning: S under 1% is present but too small to forecast with; 1% to 5% a real but small aid; 5% or more a usable aid.**
- **Read mid-year as well.** The same with the weather to June only, which is before the main harvest in most of the north.
- **Not read.** A quiet null: country-mean drought, with no crop calendar and no cropland map, adds nothing this test can hear to a national yield's own past. What it can hear is on the measured panels.
- **A made-up mark misses.** A null about the method. The real record stays unread against drought.

A pass does not show cause, and does not say drought acts alone: SPEI rises and falls with heat as well as rain.

## Guesses, written now so they cannot be adjusted

- Made-up marks, year-end: all hold, about 80%. Most likely to miss: the 20% link at 8 of 10.
- The real record read as a link, year-end: about 60%. Mid-year, given year-end: about 70%.
- If read, S between 0.5% and 3%; 5% or more, one chance in ten.
- The top third in the later half: S about twice the whole panel's.

## Changes made after seeing a smoke result

Smoke runs are made-up records on seeds 21901 to 21918, never counted. What changed because of them or beside them:

1. **The made-up records were reshaped twice on the real sides alone.** First to the real record's shape (how many records, how rough, how alike neighbours are, the driver's memory and drift). Then, after the baselines were run on the real yields alone and trend lines did worse there than on made-up ones, a wandering level was added and growth lowered, until the seven baselines' errors stood in about the real order and size (made-up: all about 5% harder).
2. **The blend baseline was added** after seeing on the real yields alone that no single baseline was clearly best. It is stronger than the six before it, which makes a pass harder.
3. **A multiplier for each record,** meant to turn the term down where it had not helped, was tried in two forms and dropped: S fell on every smoke record with a link.
4. **The least size, 0.2%,** was added after a no-link smoke record came close to passing with a term of almost nothing, where S is zero to three places and its interval has no width.
5. **The step panel** was added to try a way of fooling the test, not after a failure. It was not read as a link on smoke.
6. **The "where it helped before" reading** was added after seeing that the gain on smoke sat in the linked records and that the other records lost a little.

On smoke, year-end: 20% read 4 times in 4; 10% read 2 in 2, narrowly; 5% not read, 0 in 2; nothing, drift and step not read, 0 in 7. With a link of 20% in half the countries S was about 1.2% to 1.4%: about 3% to 4% in the linked records and a loss of about 1% in the others.

## Limits, stated now

- **It hears a small part of what is there.** A link taking 20% of a record's departures gives a pooled S a little over 1%. One index for a whole country, six fixed months and slopes shared across unlike places lose most of it. A small S on the real record is not a small effect of weather on harvests.
- **A country is not its cropland.** The drought mean covers desert, forest and mountain with the fields. Nine countries have fewer than five cells.
- **Official figures are not measurements.** They are reported by governments, sometimes revised, sometimes smoothed. If any office used weather to make its estimate, the test would hear that as a link. Not checked.
- **The lead is short and partly notional.** The year-end estimate comes about a year before FAO publishes, but national figures appear sooner. The mid-year estimate uses the yield of the year before, which FAO has not published by June.
- **The controls are 62 and not independent** of each other; the interval treats the 39 years as independent, and a record's errors in neighbouring years are not quite.
- **Something else may sit behind both.** El Niño leads drought in much of the world. That would be a chain and not a false link, but it is not separated here.
- **Step and drift panels use one strength each,** a guess.
- **The drought file** carries an error its makers have acknowledged; a corrected file is not yet out.
- **No person-level inference:** the unit is a country, a cereal and a year.

## Result, step 1: the made-up records (2026-11-10, 06:26 UTC)

Run at commit 363c2fa, the rule as above, 190 runs on 110 records, 62 shifts each. **Every mark held.** Rows: `results/harvest-drought.jsonl`.

| Panel | Year-end: read as a link | Pooled S, lowest, middle, highest | Mid-year: read as a link |
|---|---|---|---|
| Link, 20% | **9 of 10** (mark: at least 8) | +0.37%, +0.79%, +1.14% | **8 of 10** (at least 8) |
| Link, 10% | 3 of 10 (measured) | +0.04%, +0.17%, +0.30% | not run |
| Link, 5% | 0 of 10 (measured) | −0.04%, +0.05%, +0.13% | not run |
| Link in few, 20% | 2 of 10 (measured) | +0.01%, +0.15%, +0.59% | not run |
| Nothing | **0 of 30** (mark: at most 1) | −0.09%, −0.02%, +0.03% | **0 of 30** |
| Drift | **0 of 20** (at most 1) | −0.10%, −0.01%, +0.12% | **0 of 20** |
| Step | **0 of 20** (at most 1) | −0.25%, −0.05%, +0.01% | **0 of 20** |

In plain terms:

- **No false link in 140 readings** of records with none in them (70 records, read year-end and mid-year).
- **The ruler.** A link taking a fifth of a linked record's year-to-year departures, in half the countries, is heard nine times in ten. At a tenth it is heard three times in ten; at a twentieth, never; at a fifth in only a fifth of the countries, twice in ten. So a silence on the real record would rule out a link of about the first size and shape and nothing smaller.
- **What is heard is a small part of what is there,** and smaller than the smoke runs suggested: the pooled S for the 20% link has a middle of 0.8% (smoke: 1.2% to 1.4%). In the linked records the term removes about 2.3% of the error; in the others it adds about 0.7%.
- **The mid-year mark held with nothing to spare** (8 of 10, 8 needed). The two it missed had intervals reaching zero (lowest ends −0.20% and −0.01%).
- **Where it helped before:** on the 20% link the top third by earlier gain were 73% linked records (half would be chance), and the term removed a middle 1.6% of their error in the later years, twice the whole panel's; clear of zero and of every shift in 9 of 10. On records with nothing in them that reading was clear in none of 30, none of 20 and none of 20 year-end, and in 0, 1 and 1 mid-year (drift, step). It is not a verdict and has no mark.
- The one 20% record not read year-end (seed 22002) had S +0.37% with an interval from −0.11%.

Guesses against this: "all year-end marks hold, about 80%" held. "Most likely to miss: the 20% link" was the closest (9 against 8).

Next: the independent reader, before any real yield is read.

## Amendment after the independent check (2026-11-10, 06:52 UTC), before any real yield is read

The reader's report, scripts and logs are in `docs/reviews/2026-11-10-harvest-rule-check/`; the reasons are in decision 0052. Its verdict: **the real scoring may go ahead after these changes.** It found no leak (its own test, not this repo's), reproduced the table above from the rows and three seeds from scratch, and found the real path as the rule says. No change below makes a pass easier, and none changes which made-up record was read as a link.

**What it found, on made-up records of its own (seeds 23001 to 23088):**

1. **The shifted years do not guard against a drift shared by drought and yields; only the flat driver does.** With a slow shared drift and no link, the model's side met every condition and beat all 62 shifts in 6 of 37 records, with S up to 1.56%. The flat driver stopped every one (0 of 37 read as a link). On the counted drift records above the true years beat all 62 shifts in 4 of 20, where chance would give about 0.3. So a pass is protected, but S itself can be raised by drift.
2. **The ruler is the best case.** In the made-up records the drought series the test sees is exactly what moves the yield. With a blurred series (correlation 0.71 with what acts), the 20% link was read 5 times in 8, not 9 in 10, and S about halved.
3. **A cause shared by both passes as a link.** A year-to-year swing put into both moisture and yields, with no path from one to the other, was read as a link 4 times in 4 (S 1.5% to 2.7%), with the flat driver too.
4. Places where the words above and the code differ; none changes a number.

**What is changed:**

- **The size reported is the smaller of S and S with the flat driver** (`reading`'s `size`), each given with its interval. The size words (under 1%, 1% to 5%, 5% or more) are applied to that. The verdict is unchanged: condition 4 already required the flat driver's S to be at least 0.2%, so no reading of any made-up record changes, and none was run again. This can lower the size reported and cannot raise it.
- **"Not through a shared drift"** is withdrawn. A pass says: not through a drift that a straight line for each country and calendar month removes.
- **What a silence would rule out** is a link of the size on the ruler *in the index as measured*. A real effect that a country's mean SPEI-3 at these six months only partly catches could be larger and still be missed.
- **What a pass would mean:** drought at these months helps to forecast the official yield. It does not say drought lowers yields. Heat, rain tied to El Niño and any other weather that moves with the index are not separated, and a cause shared by the index and the yield would be read as a link every time.
- **`run_harvest.py real once` reads both variants before it writes either,** so a run that stops part-way leaves nothing behind and can be started again without a second look at anything.

**The words corrected to the code** (the code is unchanged in each):

- "The term is clipped at 4": each scale's forecast is clipped at 4; their weighted sum is not. The weights summed to 0.89 at most on every counted record.
- "Ten known earlier years": a record is forecast in a year when it has nine consecutive known year-on-year changes behind it for its scale; the ten-year line needs 6 of its 10 years and the twenty-year line 8 of its 20.
- "Last year's figure" is the three-year mean where last year's is missing.
- Targets are figures flagged A only. Figures flagged E (estimated) and X (from international organisations) are both left out of the targets and kept as past values.

**Not done, and why:** no drift record was added with a mark, because the flat driver stopped every drift the reader tried and the change above covers the size. The made-up driver was not blurred and run again, because that would only move the ruler, which is now said to be the best case.

What the reader did not check is listed in its report: the mid-year variant on its own records, published effect sizes, FAO's revisions, crop calendars.

## Result, step 2: the real record (scored once, 2026-11-10, 06:52 UTC, at commit 55db33f)

`run_harvest.py real once` was run once. Both variants were read before either was written; the rows are the two of kind `real` in `results/harvest-drought.jsonl`. The script now refuses a second run: the harvest record 1986 to 2024 is spent for this driver.

**Read as a link, year-end and mid-year.** 503 records in 141 countries, 16,763 official figures forecast, each from the years before it.

| | Year-end (the result) | Mid-year (weather to June only) |
|---|---|---|
| **Size reported** (the smaller of the two below) | **1.67%** | **1.11%** |
| S, the share of the baseline's error removed | 1.67% (interval 0.97% to 2.35%) | 1.11% (0.49% to 1.73%) |
| S with the flat driver (each country's trend and season taken out) | 2.24% (1.47% to 2.97%) | 1.48% (0.81% to 2.14%) |
| Other-year controls beaten (the weather of 62 other years) | 62 of 62; their mean −0.05%, their largest +0.01% | 62 of 62; mean −0.05%, largest +0.01% |
| Excess over the mean control | 1.71% (1.02% to 2.39%) | 1.16% (0.54% to 1.77%) |
| The same with the flat driver | 62 of 62; excess 2.28% (1.51% to 3.02%) | 62 of 62; excess 1.53% (0.86% to 2.18%) |
| Error below each of the seven baselines used alone | all seven | all seven |
| S without its best year | 1.51% | 0.95% |
| Years in which the drought term helped | 32 of 39 | 26 of 39 |
| S, 1986 to 2004 / 2005 to 2024 | 1.77% / 1.56% | 1.13% / 1.09% |
| The third of records where it had helped most before 2005, scored 2005 to 2024 (136 of 408 ranked) | 5.32% (3.90% to 6.73%), 62 of 62 | 3.88% (2.73% to 5.06%), 62 of 62 |

All six conditions of the verdict hold in both variants. By the size words fixed beforehand, 1% to 5% is **a real but small aid**.

**In plain terms:**

- Knowing how dry each country was in the months to its harvest takes about one part in sixty off the error of a forecast of its official cereal yield, on years the forecast was never fitted to. The honest range is one part in a hundred to one part in forty. With the weather known only to June it is about one part in ninety.
- The weather of any other year does nothing: 62 wrong years each change the error by a hundredth of a percent or less. So the gain belongs to the right year's weather, not to having six more numbers to fit.
- It does not rest on a trend: with each country's trend and season removed from the drought index the gain is larger, not smaller. It does not rest on one year, or on one half of the record.
- It is uneven. By cereal, year-end: millet 2.35%, maize 2.12%, wheat 1.94%, barley 1.76%, sorghum 1.48%, rice 0.32%. Mid-year: barley 1.94%, wheat 1.84%, sorghum 1.20%, maize 0.82%, millet 0.71%, rice 0.04%. Rice, mostly irrigated or flooded, shows next to nothing; the cereals harvested by midsummer keep their gain when the weather stops at June, and those harvested in autumn lose most of it. These fit what is known about crops, and they were not tested: no interval was computed by cereal.
- Where the term had helped in the past it went on helping, about three times as much as on the whole panel: 5.3% (3.9% to 6.7%) in 2005 to 2024 for the third of records chosen on the years before 2005 alone. That third is 136 records in 76 countries. This reading was registered as reported beside the result, not as the result.
- Record by record (488 records with 20 or more scored years) the term helped in 56% and hurt in 44%; the middle record gains 0.7%; a quarter gain more than 5% and an eighth lose more than 5%. Largest gains, year-end: Australia wheat +28% and barley +24%, Hungary millet +24%, North Macedonia maize +22%, Argentina maize +22% and sorghum +21%, Slovenia maize +20%, Kyrgyzstan maize +19%, Republic of Korea rice +19%, Zimbabwe maize +19%. Largest losses: China wheat −27%, Democratic Republic of the Congo rice −21%, China rice −19%, India barley −17%, Indonesia rice −16%, Côte d'Ivoire maize −16%. Each of these is one noisy number with no interval and names nothing by itself. A guess, not tested: the losses are large countries whose mean says little about their cropland, and irrigated crops.
- Against the made-up ruler: the real size is larger than any made-up record with a link taking 20% of a linked record's year-to-year variance in half the countries (0.4% to 1.1%). The ruler was not run above 20%, and it is the best case for the method, so the real link in the index is at least that strong and how much stronger is not measured.

**The guesses, against what came:** read as a link year-end, about 60%: it was. Mid-year given year-end, about 70%: it was. S between 0.5% and 3%: 1.67%. 5% or more, one chance in ten: no. The top third about twice the whole panel's: about three times.

**What this is and is not.**

- It is the first time in this project that a series from one domain (weather) has improved a forecast in another (official farm statistics) under the project's own rules: the rule written first, made-up records with and without a link, controls, every year forecast from the years before it, and one scoring.
- It is a link everyone knew. Nothing new about the world is claimed. What was not given to the method is which months matter for which crop, in which countries, and with which sign.
- It does not show cause. Heat, and rain tied to El Niño, move with the index and are not separated. A cause shared by the index and the yield would be read as a link every time (the independent check measured this on made-up records).
- It is a country's mean over all its land, not its cropland, and a calendar year, not a season.
- The lead is short and partly notional. Year-end uses weather to December of the harvest year, after most harvests; mid-year, to June, is ahead of the harvest in most of the north and behind it in much of the south. What the term is ahead of is the official figure, which FAO publishes more than a year later.
- Official yields may themselves be estimated with the help of the weather in some countries. If so, part of this is the index forecasting a statistician's model and not a harvest. This is not measured.
- It is small. One part in sixty is no use for a single country's planning. The 5% in the chosen third is nearer to useful and is the thing to test next, on its own rule.
- The drought file carries the error its makers have acknowledged, and FAO revises past figures; the file read is the one fetched and entered in the manifest.

**Not yet a finding.** As registered, it gets an independent reader first. What that reader is asked: to rebuild the score from the words above without this code's forecast step, to look for a leak on the real path, to see whether a few countries or a few years carry it, and to say what else could produce it.
