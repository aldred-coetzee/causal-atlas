# The same twenty-five series, with the search's controls corrected

Rule first, committed before any run with the corrected controls on fresh seeds (rule 9). Authority: decisions 0040 and 0044. Code: `scripts/run_indices_2.py`, which runs `scripts/run_indices.py` with three things replaced: the controls, the seeds and the rows file. Seeds: `results/seed-ledger.md`.

## Why

The first attempt (`results/real-indices.md`) stopped at its own instrument check: among 44 candidates, 26 of them real, the search could not reliably hear a planted link and lost El Niño in one region. The cause was found on the fitting years (same file, last section): of the 49 year-moved copies each candidate is judged against, the two next to the real alignment are not controls. One is the series itself at the far end of the lag window, and the series' own near future besides. Real series' real ties were being counted as chance.

## What changes: one thing

**The controls are the copies moved by 2 to 48 whole years** (47 of them), not 1 to 49. The reason for exactly these: a control's window of lags must not touch the real window and must leave a year between them, on either side.

Everything else is as in `results/real-indices.md` and is not repeated here: the 26 real series and 18 decoys, the five fields, the fitting years 1950 to 1999, the two gates, lags 0 to 12, the cap on leads, the stepping down that stops at the first candidate that fails.

## Seen before this rule

- Everything listed in `results/real-indices.md`, and its whole step 1: what the old controls named for each field on the fitting years.
- With the two copies left out, on seven of those naming runs: which real series stand above the first bar of each gate. In South and Southeast Asia: the Pacific wind series, the ONI, the Northern Oscillation, the Indian Ocean Dipole and its eastern pole, the warm pool, and in the broad gate four more near the bar (East Atlantic, Arctic Oscillation, Pacific Meridional Mode, North Pacific Gyre). South America: the ONI, the Northern Oscillation, the warm pool, the tropical South Atlantic, the eastern pole. Australia: the ONI and the Dipole. North America: the ONI, the Northern Oscillation, the Pacific Decadal Oscillation, the eastern pole. Europe: the Scandinavian pattern, Greenland Blocking, the Arctic Oscillation, the Gibraltar North Atlantic Oscillation; not the ONI.
- **So the naming below is not blind, and is not presented as blind.** The real series are the same series on the same years; only the decoys are new. What tests the corrected search is what the author has not seen: planted links, decoys and mixed years on fresh seeds. What tests a named series is the years after 1999, against which no series but the ONI has been set.
- No run with the corrected controls has been made with a planted link or with the years mixed.

## Step 1a: the instrument check and ruler, on 1950 to 1999

As before: a link planted from one decoy into the nearest cells to a seeded centre, in three consecutive calendar months at lag 5; 5%, 15% and 40% of variance over 5% and 25% of the cells; ten decoy sets per field, fresh seeds 15601 to 16010; 300 runs.

**Instrument check, unchanged:** the link of 40% of variance over 25% of the cells is found in at least 45 of the 50 runs, in at least 8 of 10 in every field, and wherever it is found at least 80% of its claimed cell-month-lags lie in the planted cells.

Reported and marking nothing: the rest of the table, and how often a decoy with no link planted is named in these runs.

## Step 1b: naming, on 1950 to 1999

Twenty decoy sets per field, fresh seeds 15101 to 15520, each run repeated with the field's years in a seeded random order. Marks, unchanged:

- **N1:** the ONI is a lead in at least 18 of 20 sets in each of South America, Australia, South and Southeast Asia and North America.
- **N2:** a decoy is a lead in at most 8 of the 100 runs.
- **N3:** with the years mixed, anything is a lead in at most 8 of the 100 runs.
- **A series is named for a field** when it is a lead in at least 18 of that field's 20 sets.

N2 and N3 are the marks that matter most here. Fewer controls mean a lower bar, and these two say whether it is now too low.

**If the instrument check, N1, N2 or N3 misses, step 2 is not run and the years after 1999 stay sealed for these series.** A second miss would be published as that, and a third change to the search would not be made on these fields' fitting years without a fresh reader first.

## Step 2: the forecast check, on 2000 to 2024, once

Exactly as written in `results/real-indices.md`, "Step 2", with nothing changed: the tested model's residual; for each named pair, claims at lags 4 to 12 fitted on the fitting years; S on 2000 to 2024 over the region-months the series claims; a pass when the lower end of S's interval at 1 − 0.05/m is above 0 (m the number of named pairs, 20,000 draws), S is beyond all 24 whole-year shifts, and the full model's error is below each baseline alone. The straight line in time is put through the same step in each field scored. Run once: `scripts/run_indices_2.py confirm once`, which refuses unless every step-1 mark holds and refuses a second scoring.

The first attempt never ran this step, so it is still unspent: no row, no score and no look at any of these series against any year after 1999 exists.

## Guesses, written now so they cannot be adjusted

- The instrument check passes, and the planted link of 40% over 5% of the cells is found in about half the runs where it was found in 11 of 50.
- N1 holds in all four fields. N2 and N3 each come in between 2 and 6 of 100. A miss on either is possible and would mean the old bar was doing more than it should have had to.
- Named: about the lists under "Seen before this rule", which is no guess. With so many named, m will be large (perhaps 20 to 30 pairs), which makes the interval in step 2 wide.
- Step 2: most named series add nothing beyond El Niño at four months or more, because most of them move with El Niño or act within a season. If any pair passes, the author's guess is the tropical South Atlantic for South America, the Indian Ocean Dipole for Australia, or the Pacific Decadal Oscillation for North America. Europe's patterns will make few claims at these lags. No pass at all is the single most likely outcome.

## Limits, stated now

All the limits of `results/real-indices.md` stand. Added:

- **The correction was made after a miss, on the same fitting years.** It follows from a plain defect (a control that is the series itself) and was the narrowest change the reasoning supports, but it was not chosen blind. The marks on fresh seeds and the unread years are the guard, not the author's restraint.
- **The forecast step's own controls have the same weakness and are left as they are.** Its 24 whole-year shifts include the years next to the real one, where a real series is not pure chance. Left in, they can only make a pass harder (decision 0044).
- **A series that nearly repeats itself after whole years** (the stratospheric wind) still meets copies of itself among its controls. If it drove a field it would not be named.
- **Many named pairs, one signal.** Several of these series are El Niño seen from another place. Naming says they are tied to the field, not that they are separate causes.

## Estimates

Step 1: about 55 minutes of machine time (the first attempt took 51). Step 2: about 5 to 10. Tokens to the report: about 300k.
