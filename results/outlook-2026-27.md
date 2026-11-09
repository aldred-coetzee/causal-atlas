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

## Limits

- **One driver.** Everything else that moves drought in these months is absent. The term is a push, not a forecast of the index.
- **One event.** El Niño events differ in where their warming sits and in what follows; a published map of typical effects carries the caption "Not every indicated anomaly occurs with every ENSO event" (`docs/reading/enso-africa-known-answer.md`).
- **The index is at or beyond the largest values the fitting years contain**, so the straight line is being used at its edge. The largest value in the fitting years and in the checked years is reported with the results.
- **The latest index values are provisional** and are revised by their maker.
- **One slope per region and calendar month**, averaging El Niño and La Niña, which are not mirror images.
- **Most claims are at the shortest lag (four months)**, so most of the outlook reaches only to January 2027. Later months rest on fewer claims at longer lags.
- **Regions are 10-degree squares.** Nothing here is about a town, a farm or a person.
- All the limits in `results/real-enso-continents.md`.

## Estimates

Machine time under 5 minutes. Tokens: about 80k.
