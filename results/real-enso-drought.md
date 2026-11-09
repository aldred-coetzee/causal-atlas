# Real known-answer test: is El Niño named, blind, as a driver of drought over Africa

Rule first, committed before any number that joins the ONI to the drought field (rule 9). Authority to run: decision 0040. Code: `src/causal_atlas/links.py`, `field.py`, `decoy.py`, `scripts/run_enso.py`. Seeds: `results/seed-ledger.md`.

## Why

Every test so far ran on worlds we built. This one runs on real data with an answer science already accepts, on data already held (`docs/review-2026-11-09.md`, step 2). If the search cannot find this link in 50 years, the design is wrong. If it can, it is the first true result on real data and the base for adding data sets.

## Seen before this rule

Shape only: the drought file has 900 months from 1950-01 to 2024-12 on the African cells; 9,695 of 10,228 cells have every month and the rest are dropped; the largest absolute value is 9.2, so values are clipped at plus or minus 3 before anything else. The toy tests in `tests/test_links.py` on made-up numbers. No number joining the ONI to drought has been computed, by this code or any other in this project.

## Data and split

- **Outcome:** SPEI-3, cells by months. The value at month t covers months t-2 to t.
- **Driver:** the ONI. The value at month t is a 3-month mean centred on t, so it uses month t+1. Lags are index lags, 0 to 12 months; a lag of 0 or 1 is not usable for a forecast and none is claimed as one here.
- **Discovery: 1950-01 to 1999-12**, targets 1951 to 1999, 49 years. Everything is chosen, fitted and may be reworked here.
- **Confirmation: 2000-01 to 2024-12**, sealed. The loader holds the whole file, but nothing is computed on the drought field past 1999-12 until the confirmation rule below is run, once.
- **Decoys:** 31 per set, 20 sets, seeds 11001 to 11020: phase-randomised series with the ONI's spectrum, AR(1) series at mixed persistence, noisy cycles of 2 to 7 years. None is linked to anything. These are synthetic and independent; real candidate series are related to each other, which is harder and comes later.

## The search

For each candidate and each whole-year circular shift of it (49 shifts): the squared correlation with the field at each lag and calendar month, averaged over cells, summed over the 13 lags and 12 months. One number per candidate per shift, so the search never has to pick among a candidate's own lags. The gate is the one already in use: each candidate on its own scale over its 50 values, a candidate is named when its unshifted value beats every shifted value of every candidate left, stepping down to at most 5.

Where and when, for a named candidate: its correlation at every lag, calendar month and cell, each tested on 49 years, Benjamini-Hochberg at 5% over all of them.

## Marks, fixed now

There is one real world, so the 20 sets vary only the decoys: these counts measure false alarms and stability, not power.

- **D1:** the ONI is named, and first, in at least 18 of 20 sets.
- **D2:** a decoy is named in at most 2 of 20 sets.
- **D3, the ONI left out:** a lead is named in at most 2 of 20 sets.
- **D4, the field's years put in a seeded random order, ONI in:** a lead is named in at most 2 of 20 sets.
- **D5, the map:** the named driver's map agrees with the published one in the two regions where the answer is firm. Rule under "The accepted answer" below.

## The accepted answer, for D5

From `docs/reading/enso-africa-known-answer.md`; the boxes, seasons, signs and the two correlations were re-read at source (Cai et al. 2025, a review) before this was written. Those figures are rainfall against a Niño3.4 index in the same season; ours is SPEI-3 against the ONI, so signs, places and seasons carry over and sizes do not.

| Region | Box | Season, as SPEI-3 target months | Sign under El Niño | In the mark |
|---|---|---|---|---|
| Southern Africa | 15 to 35° S, 15 to 40° E | December to February rain: January, February, March | Drier (negative) | Yes |
| East Africa | 7° S to 5° N, 29 to 42° E | October to December short rains: December, January | Wetter (positive) | Yes |
| Sahel | 11 to 15° N, 17° W to 40° E | July to September rain: September, October | Drier (negative) | Reported only: weaker, and a second pathway pushes the other way |

For each region: the correlation between the ONI and SPEI-3, averaged over the box's cells, its target months and lags 0 to 4. The published answer is same-season; lags 0 to 4 allow for the two 3-month windows and for the one SPEI paper found, which says the southern African response shows "some months later" (abstract only).

- **D5 passes** when, in southern Africa and in East Africa both, that average has the expected sign and is further in that direction than the same average for every one of the 49 whole-year shifts of the ONI.
- Reported beside it and marking nothing: the Sahel row; the share of each box's cells with any significant entry in the window; and the share of those entries with the expected sign.
- **A known reason D5 could miss in southern Africa:** the review gives that correlation as 0.15 for 1931 to 1970 against -0.69 for 1971 to 2010. Discovery runs 1950 to 1999, so about 20 of its 49 years are in the weak period. A miss there is published as a miss.
- No region is used as a place where nothing should be found: the reading found no source stating one. The Sahara is left in the search unmasked; SPEI is unstable where there is almost no rain, and that is a limit, not a filter chosen here.

## The ruler: the smallest link this search hears on the real field

On the discovery years, a link from one decoy is added to the real field: in the nearest cells to a seeded centre covering 5% or 25% of the cells, in three consecutive target months, at lag 5, sized to be 2%, 5%, 15% or 40% of the variance in those cell-months. Seeds 11101 to 11110, 80 runs. Found means that decoy is named.

- **Instrument check:** at 40% and 25% of cells it is found in at least 9 of 10, and at least 80% of the claimed cell-month-lags lie in the planted cells. If not, the search is broken and D1 to D5 are not read.
- The rest is a measurement and passes nothing: it is the limit reported beside the answer.

## Confirmation, fixed now, run once after discovery is frozen and committed

- **Baseline (rule 2):** each cell's own history, the season and its neighbours: gradient boosting (scikit-learn `HistGradientBoostingRegressor`, 200 rounds, defaults, fixed seed) on the cell's own SPEI at months t-3, t-4, t-5, t-6 and t-12, the mean of its up to 8 neighbours at t-3, the calendar month, latitude and longitude, fitted on discovery targets.
- **Claims:** for each candidate named in discovery, and each cell and calendar month, the lag from 4 to 12 with the largest absolute correlation, kept if significant by Benjamini-Hochberg at 5% over all cells, months and lags 4 to 12. Lag 4 is the shortest a forecast three months ahead can use, given the ONI's centring.
- **Model:** baseline plus, on claimed cell-months, slope times the candidate at its lag. The slope is fitted on the baseline's discovery residuals and shrunk by 1 - 1/t², t being its t statistic, floored at 0.
- **Metric:** S = 1 - (model's squared error) / (baseline's squared error) on confirmation targets, on claimed cell-months (headline) and on all cell-months. Interval: 2,000 bootstrap draws of the 25 years, 95%.
- **Control:** the same claims with the candidate shifted by each of 24 whole years within the confirmation period.
- **Passes** when S on claimed cell-months has its interval's lower end above 0 and is larger than all 24 shifted values. That is the first result here that meets rule 2 on real data. A miss is published as a miss, and the confirmation period is then spent for this driver and field.

## Limits it carries

- East Africa's link runs partly through the Indian Ocean Dipole, which is not among the candidates here.
- El Niño and La Niña are not mirror images and the link changes by decade; a correlation averages over both.
- Where no station is near, the source rainfall is filled with the long-run average, which damps any signal there.
- A known link, so passing shows the engine works on reality; it discovers nothing new.
- One driver, one field, one continent. Decoys independent of each other.
- The drought file is built from station data, thin over parts of Africa and thinner in early decades.
- The shift test assumes the years are exchangeable; slow trends in the field weaken that.
- Per-cell tests treat years as independent.

## Estimates

Discovery and ruler: minutes of machine time. Tokens to the discovery report: about 400k including the two readings; estimates here have run low.

## Results (2026-11-09, discovery years only; the confirmation years are untouched)

Rows: `results/real-enso-drought.jsonl` (143). Run as committed, no deviation. Machine time 14 minutes.

**The instrument check missed, by one: 8 of 10 against a mark of 9.** By the rule above the search is then not good enough and D1 to D5 are not counted as passed. Their numbers are given because they are what was measured, not as a pass.

| Mark | Rule | Measured |
|---|---|---|
| Instrument check | Link of 40% of variance over 25% of cells found in at least 9 of 10; at least 80% of claims in the planted cells | **8 of 10: missed.** Where found, 96% to 99% of claims were in the planted cells |
| D1 | El Niño named first in at least 18 of 20 | 19 of 20. In the other set nothing was named: one decoy's shifted value was higher |
| D2 | A decoy named in at most 2 of 20 | 0 of 20 |
| D3 | El Niño left out: any lead in at most 2 of 20 | 0 of 20 |
| D4 | Years shuffled: any lead in at most 2 of 20 | 0 of 20 |
| D5 | Right sign and beyond all 49 shifts, in southern Africa and East Africa | Southern Africa: average correlation -0.36, beyond all 49. East Africa: +0.37, beyond all 49 |

Beside D5 and marking nothing: the Sahel -0.25, beyond all 49 shifts. Cells with a significant entry in the window: 38% (southern Africa), 36% (East Africa), 5% (Sahel); every one of those entries has the published sign. Over the whole continent, 37% of cells have at least one significant month and lag (25% at lags 4 to 12); the smallest significant correlation is 0.46 in size.

**The ruler: this search hears only very broad, very strong links.**

| Share of variance in the linked cell-months | Over 5% of cells | Over 25% of cells |
|---|---|---|
| 2% | 0 of 10 | 0 of 10 |
| 5% | 0 of 10 | 0 of 10 |
| 15% | 0 of 10 | 1 of 10 |
| 40% | 0 of 10 | 8 of 10 |

A link confined to a twentieth of the continent is not heard at any size tried. El Niño was named in all 80 ruler runs. One decoy was named falsely in 1 of the 10 ruler decoy sets (in 2 of its 8 runs).

### What this says

- **El Niño is found blind, on real data, among 31 decoys, with no false alarm in 60 control runs, and its map has the published places, seasons and signs.** That is the first thing in this project found on real data that matches an answer science already holds. It is on the discovery years and against decoys that are unrelated to each other; it is not yet a forecast and has not met rule 2.
- **But the search is blunt.** It adds up the whole continent and all months and lags, so it hears El Niño because El Niño is everywhere, and it would miss a strong link confined to one region or one season. A search like that is no use for the project's aim, which needs links nobody has drawn a box around.
- **Why the instrument check is the one that matters:** the five discovery marks only show that a search can find the loudest known signal. The check asks whether it could find something else of that kind. It could not, reliably.

### What happens next

The confirmation is not run: the rule ties it to a discovery that is frozen, and this one is not. The search is sharpened on the discovery years (a statistic that looks region by region and month by month, not at the continent's total), under a new rule file with fresh decoy and ruler seeds, committed before it is run. What the next rule must say plainly: these D1 to D5 numbers are now known to its author, so for the sharpened search they are a check that nothing was lost, and its real tests are the instrument check, the ruler and the sealed confirmation.

## Confirmation result (2026-11-09, scored once on 2000 to 2024, after `results/real-enso-drought-2.md` passed its marks and was committed)

Row: the `confirmation` line in `results/real-enso-drought.jsonl`. Run as committed, no deviation. The script refuses a second scoring.

**A miss.** Adding El Niño to the baseline did not improve the forecast of drought three or more months ahead on the years held back.

| | Rule | Measured |
|---|---|---|
| S on claimed cell-months | Interval's lower end above 0 | **S = -0.093, interval -0.250 to +0.043. Missed.** The forecast with El Niño had 9% more squared error than the baseline alone |
| Against the 24 year-shifted controls | Larger than all 24 | Larger than all 24 (they run from -0.152 to -0.382) |
| S on all cell-months, beside it | Marks nothing | -0.002, interval -0.005 to +0.001 |
| Claims | | 2,256 cell-months in 1,520 of 9,695 cells |
| Baseline's own skill on 2000 to 2024, beside it | Marks nothing | R² = -0.10: worse than predicting the period's average |

What this says, and no more:

- **El Niño is found and mapped correctly, and it still did not make the forecast better.** Finding a link and forecasting with it are different things, and rule 2 is about the second.
- **The El Niño term carries real information:** with the true years it does much better than with any of the 24 wrong alignments. But as fitted on 1950 to 1999 it adds more error than it removes. Two readings fit that, and this result does not tell them apart: the slopes are too large because each was picked as the best of 9 lags among thousands of cells, or the link itself changed after 2000 (the review this test rests on says it did, in both regions).
- **The baseline is poor on these years.** Fitted on 1950 to 1999, it does worse on 2000 to 2024 than a flat guess. So "beyond the baseline" was a low bar here and the El Niño term still did not clear it.
- **The confirmation period is now spent for this driver and this field.** Anything further computed on Africa's 2000 to 2024 drought with El Niño is exploration and is labelled so; it cannot confirm anything.
