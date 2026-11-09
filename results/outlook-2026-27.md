# Outlook: what the 2026 El Niño says about drought by region, to September 2027

Rule first, committed before any number below it is computed (rule 9). Authority: decisions 0040 and 0042. It follows the pass in `results/real-enso-continents.md` ("Results, step 2") and uses that model unchanged. Code: `scripts/outlook.py`.

**This is a test of a research method on months that have not happened. It is not a warning service.** National weather services and the seasonal forecast centres use far more information than one index.

## Why

The forecast check passed on four continents. A method that passed is worth using once on the months ahead: that is what it is for, and it is the one test nobody can have seen, because these numbers go into a public history before the drought data for those months exists.

## What is held, and what the author has seen

- The El Niño index (ONI) to the value centred on 2026-09, which is the mean of August to October 2026, as fetched on 2026-11-05. The author has read the nine 2026 values (-0.39 rising to 2.46). Nothing has been computed from them.
- The drought index (SPEI-3) ends at 2024-12. **So the baseline cannot be run for any month after that, and only El Niño's own term can be given.**

## What is computed

- **Model A, as tested (the headline):** the region-scale model for South America, Australia, South and Southeast Asia and North America, fitted on 1951 to 1999 by `forecast.fit`. These are exactly the claims, lags, slopes and multipliers that were scored on 2000 to 2024.
- **Model B, refitted and untested (shown beside, never as the headline):** the same procedure fitted on 1951 to 2024. More years, but nothing has checked it out of time.
- For each region and each target month from 2025-01 to 2027-09 where the model has a claim for that calendar month and its lag reaches a held index value: **term = multiplier × slope × ONI at (target month - lag)**, in units of the drought index. Negative means drier. It is the shift El Niño adds to what the region's own history would give.
- **A signal** is a term of 0.25 or more in size under model A. The tables show signals; every term is in the rows (`results/outlook-2026-27.jsonl`).
- Left out, on purpose: Africa (its confirmation missed; an unconfirmed forecast is not published beside confirmed ones), Europe (the method made no claim there), and single cells.
- Each region is named by the country its centre falls in, from the Natural Earth boundaries already held. A region is a 10-degree square and usually covers several countries.

## How to read a term: what terms of each size were followed by, 2000 to 2024

Description only. Those years are spent and the author has seen their scores. Fixed now: four bands of term size under model A (under 0.1; 0.1 to 0.25; 0.25 to 0.5; 0.5 and over), pooled over the four fields' claimed region-months. For each band: how many; the share where the outcome fell on the term's side of the baseline; the share where the outcome fell on the term's side of zero (drier or wetter than that place's normal); the mean outcome beyond the baseline in the term's direction, beside the mean size of the term.

## Registered now, to be scored when the data exists

When a release of the drought file covering these months is fetched, model A's terms as committed here are scored against it, once, with the baseline's coefficients as saved in the rows (nothing refitted):

- **Part 1, 2025-01 to 2026-10:** months already past in the world but not in anything held here.
- **Part 2, 2026-11 to 2027-09:** the outlook.
- For each part: S as in the confirmation (1 minus the model's squared error over the baseline's, on the claimed region-months with a term), and the share of signals whose outcome fell on the term's side of the baseline.
- **A hit for part 2: S above 0 and more than half of the signals on the right side.** No interval can be drawn from under three years and one event; it will be reported as one event and not as a test of the method.

*Added 2026-11-09, before any drought value after 2024-12 is held, to close a condition of the audit recorded in `results/real-enso-continents.md`.* **Which drought file, and what a new one changes.** The terms and the saved coefficients were fitted on SPEIbase 2.11.0 (built from CRU TS 4.09, ending 2024-12; checksum in `data/manifest.toml`). That version will never cover these months. A later release differs in two ways. Its makers fit the index to the whole record each time, so with more years every value moves a little, back to 1901. And the makers say releases 2.6 to 2.12.0, ours among them, carry an error in the evaporation side of the index, corrected from 2.13.0: "The effect is generally small, but it is largest in arid regions" (<https://raw.githubusercontent.com/sbegueria/SPEIbase/master/README.md>, read 2026-11-09). So the outcome will be on a slightly different scale from the one the coefficients were fitted on. Fixed now:

- The scoring uses the first SPEIbase release of the three-month index that covers the part being scored, with its version and checksum entered in the manifest when fetched. The makers' corrected series is the better measurement, and it is not passed over for an uncorrected one in order to match.
- The terms and the saved baseline coefficients are used as committed. Nothing is refitted or rescaled. The earlier months the baseline reads are taken from the same new file.
- Beside the score, as description: on region averages for 2000-01 to 2024-12, the correlation and the mean absolute difference between the new file and the one held now, by field; and the tested model's S on 2000 to 2024 recomputed on the new file with everything frozen, to set beside +0.171.
- If that recomputed S is further than 0.03 from +0.171, the outlook's score is reported as made on a changed scale, and a hit is not called a clean one. This can only weaken a claimed hit.

## Limits

- **One driver.** Everything else that moves drought in these months is absent. The term is a push, not a forecast of the index.
- **One event.** El Niño events differ in where their warming sits and in what follows; a published map of typical effects carries the caption "Not every indicated anomaly occurs with every ENSO event" (`docs/reading/enso-africa-known-answer.md`).
- **The index is at or beyond the largest values the fitting years contain**, so the straight line is being used at its edge. The largest value in the fitting years and in the checked years is reported with the results.
- **The latest index values are provisional** and are revised by their maker.
- **One slope per region and calendar month**, averaging El Niño and La Niña, which are not mirror images.
- **Most claims are at the shortest lag (four months)**, so most of the outlook reaches only to January 2027. Later months rest on fewer claims at longer lags.
- **Regions are 10-degree squares.** Nothing here is about a town, a farm or a person.
- All the limits in `results/real-enso-continents.md`. One was added there on 2026-11-09, after this outlook was published: the held drought file carries an evaporation error its makers have acknowledged, largest in dry regions. The model behind these terms was fitted on that file. Australia, where nearly every region carries a signal, is the driest of the four fields.
- Added 2026-11-09 after a side check recorded in that file (not a test): with El Niño measured on a fixed base instead of NOAA's moving one, the four fields together still pass and North America by itself does not. North America's 25 signals here rest on the weakest of the four fields.
- Nothing here is about conflict, or about any link between domains.

## Estimates

Machine time under 5 minutes. Tokens: about 80k.

## Results (2026-11-09)

Rows: `results/outlook-2026-27.jsonl` (kinds `driver`, `model`, `term`, `band`). The script was written after this rule was committed and run once. One addition after seeing the numbers is marked as such.

**The driver.** The index stood at 2.46 for August to October 2026, up from -0.39 in January. The largest value in the fitting years is 2.37 and in the checked years 2.59 (2015 to 2016). So the index is already past anything the model was fitted on, and inside what it was checked on by a small margin.

**The models.** The refit keeps nearly every claim of the tested model and adds more.

| Field | Claims as tested | Claims in the refit | In both | Multiplier as tested | In the refit |
|---|---|---|---|---|---|
| South America | 353 | 450 | 338 | 0.76 | 0.82 |
| Australia | 113 | 219 | 112 | 0.47 | 0.60 |
| South and Southeast Asia | 260 | 384 | 250 | 0.77 | 0.81 |
| North America | 57 | 141 | 55 | 0.68 | 0.73 |

**How to read a term: what followed terms of each size in 2000 to 2024** (description; 19,575 claimed region-months).

| Size of term | How many | Outcome on the term's side of the baseline | On the term's side of normal | Mean outcome beyond the baseline, in the term's direction | Mean size of term |
|---|---|---|---|---|---|
| under 0.1 | 5,787 | 57% | 58% | 0.14 | 0.05 |
| 0.1 to 0.25 | 7,473 | 65% | 67% | 0.28 | 0.17 |
| 0.25 to 0.5 | 4,849 | 73% | 76% | 0.44 | 0.35 |
| 0.5 and over | 1,466 | 84% | 87% | 0.68 | 0.67 |

The larger the term, the more often the outcome went its way, and the terms were not oversized: what followed was on average as large as the term or larger.

*Added after seeing the outlook's sizes:* terms of 1.0 or more occurred 62 times in the checked years, all in 2015 and 2016, and 60 of them were followed by an outcome on their side. The largest was 1.22. **Of the outlook's 431 terms, 120 are 1.0 or more and 42 are 1.25 or more, larger than any term the check ever scored.** For those the table above is a guide from one earlier event, not a measured rate.

**The outlook, November 2026 to September 2027, model as tested.** 431 terms, 413 of them signals. Of the signals, 385 are also claims in the refit, and all 385 have the same sign there. By target month: November 112, December 124, January 107, February 27, March 20, April 11, May 6, June 2, July 1, August 3, September none. Each month named is the last of the three the drought index covers.

| Field | Push | Signals (regions) | Months | Median term | Region centres fall in |
|---|---|---|---|---|---|
| South and Southeast Asia | Drier | 91 (36) | Nov to Feb | -1.07 | Indonesia and the seas among its islands, Malaysia, the Philippines, Papua New Guinea; a few in India and Bangladesh |
| South and Southeast Asia | Wetter | 35 (24) | mostly Jan, then Mar to Aug | +0.95 | China, Japan; a few in Malaysia, India, Pakistan |
| Australia | Drier | 90 (42 of 49) | Nov to Jan | -0.51 | Australia, nearly all of it |
| South America | Drier | 113 (33) | Nov to Apr | -0.76 | Brazil north of 19°S, Venezuela, Colombia, Guyana, Suriname, French Guiana, Panama |
| South America | Wetter | 59 (27) | Nov to Feb | +0.84 | Argentina, southern Brazil, Chile, Uruguay, Paraguay |
| North America | Wetter | 21 (15) | Dec to Mar | +0.78 | Mexico, the southern United States and the Gulf coast (centres 19°N to 32°N) |
| North America | Drier | 4 (3) | Jan, Feb | -0.78 | Canada at 50°N, 100°W to 110°W |

The strongest single terms: about -1.5 for November over New Guinea and Borneo (centres near 3°S 135°E and 4°S 115°E), about +1.4 to +1.5 for December over southern Brazil and Uruguay (near 30°S 53°W), and about -1.4 for January and February over Guyana and eastern Venezuela (near 6°N 58°W).

**Registered for later scoring:** 1,749 terms under the tested model in all: 1,318 for 2025-01 to 2026-10 (148 signals) and the 431 above.

*Corrected 2026-11-09:* the table first gave 23 regions for South and Southeast Asia pushed wetter. The rows hold 24; two of them have centres that print alike.

### What this says

- **If this El Niño acts as those in the record did, the three-month periods ending November 2026 to January 2027 are pushed drier across Indonesia and its neighbours, most of Australia and the north of South America, and wetter in south-eastern South America, Mexico and the southern United States.** The signs and places are the textbook ones. The method was not given them: it found them in 1951 to 1999 and they held up in 2000 to 2024.
- **How much weight a term can bear:** in the checked years a term of 0.5 or more went the right way about five times in six. That is a rate over many events and places. It is not a probability for this event, and the largest terms here are beyond what was checked.
- **What it does not say:** how dry or wet any place will be. The term is El Niño's push on top of whatever else is happening, and nothing else is in it. It says nothing after about February for most regions, nothing about Africa or Europe, and nothing below the scale of a 10-degree square.
- **It can fail, in public.** These rows are in the repository's history before the drought data for these months exists, with the scoring rule above.
