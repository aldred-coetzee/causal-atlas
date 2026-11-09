# Real known-answer test, second search: two gates, so a regional link can be heard as well as a continental one

Rule first, committed before any run on the seeds named here (rule 9). Authority to run: decision 0040. This follows `results/real-enso-drought.md`, whose instrument check missed (8 of 10 against 9), and does what its last section said would come next. Code: `src/causal_atlas/links.py` (`both`), `scripts/run_enso2.py`. Seeds: `results/seed-ledger.md`.

## Why

The first search added up the whole continent and every month and lag, so it heard El Niño because El Niño is everywhere, and its ruler showed it deaf to anything regional. The project's aim needs links nobody has drawn a box around, so the search has to hear a link that lives in one region and one season.

## Seen before this rule, all of it on the discovery years

Nothing has been computed on the drought field past 1999-12. What its author has seen:

- **Every number in the first results file.** So D1 to D5 are not blind here: El Niño is known to be named by the first search, and its map is known. For this search they check that nothing was lost. Its real tests are the instrument check, the ruler, and after them the sealed confirmation.
- **Two designs tried and dropped**, on development seeds 11901 to 11903. (a) Scoring every region, lag and month against the shifts on a z scale and taking the largest: the largest value among unlinked candidates was 25 to 27 against El Niño's 24, so it lost El Niño. A z over only 50 values cannot rank extremes. (b) Removing a 121-month running mean from the field and the candidates before the search: it did not move the bar, so slow trends are not what sets it, and no filter is used.
- **The bar for a single region, month and lag**, same seeds: the largest absolute correlation between an unlinked candidate and any region's average is 0.66 to 0.72. El Niño's is 0.69, at or just under that bar. A planted link of 40% of variance gave 0.80 to 0.84 over a quarter of the cells and 0.66 to 0.79 over a twentieth; 15% gave 0.54 to 0.69. That is why the sharp gate alone is not enough and both are kept.
- **The search below, as coded, on development seeds 11901 to 11905** (`scripts/run_enso2.py … dev`): El Niño a lead in 5 of 5 sets (by the broad gate in all 5, by the sharp gate too in 2); no lead in 5 of 5 with El Niño left out and in 5 of 5 with the years shuffled. Ruler, 5 sets: the 40% link over a quarter of the cells found in 5 of 5 with 97% to 99% of claims in the planted cells; over a twentieth, 2 of 5; 15% over a quarter, 1 of 5; nothing smaller found; no decoy named in 40 runs. The sharp gate's bar was 0.67 to 0.73.

One region size was tried: 10 degrees square, stepped by 5 degrees, at least 40 cells. It was set before the first development number and not tuned.

## Data and split

As in the first rule: SPEI-3 over 9,695 African cells clipped at plus or minus 3, the ONI, lags 0 to 12, discovery 1950-01 to 1999-12 (targets 1951 to 1999), confirmation 2000-01 to 2024-12 sealed. Decoys as before, 31 per set, with **fresh seeds: 11201 to 11220** for the marks and **11301 to 11310** for the ruler.

## The search: two gates, a candidate named by either

- **Broad gate:** the first rule's search, unchanged. For each candidate and each of its 49 whole-year shifts, the squared correlation with the field summed over lags and months and averaged over cells; each candidate on its own scale; stepping down to at most 5.
- **Sharp gate:** the field is averaged over each of 137 overlapping regions (10 degrees square, stepped by 5 degrees, at least 40 cells). For each candidate and each shift: the largest absolute correlation between the candidate and any one region's average at any one lag and calendar month. A candidate is named when its unshifted value is larger than every shifted value of every candidate left, stepping down to at most 5. Correlations are already on one scale, so nothing is rescaled.
- A candidate named by either gate is a lead. Two gates mean two chances of a false alarm in each run; the marks below are not loosened for that.

Where and when, for a lead: as in the first rule, its correlation at every lag, calendar month and cell, Benjamini-Hochberg at 5%.

## Marks, fixed now, the same numbers as the first rule

- **Instrument check:** a link of 40% of variance planted over 25% of the cells (three consecutive target months, lag 5, from one decoy, as the first rule built it) is found in **at least 9 of 10**, and where found at least 80% of the claimed cell-month-lags lie in the planted cells. If not, the search is not good enough, D1 to D4 do not count as passed, and the confirmation is not run.
- **D1:** the ONI is a lead in at least 18 of 20 sets.
- **D2:** a decoy is a lead in at most 2 of 20 sets.
- **D3, the ONI left out:** any lead in at most 2 of 20 sets.
- **D4, the field's years in a seeded random order:** any lead in at most 2 of 20 sets.
- **D5 is carried from the first results file and not run again:** it tests the ONI's map against the published one and does not depend on which search named the ONI. It passed there (southern Africa -0.36, East Africa +0.37, each beyond all 49 shifts).
- **Reported and marking nothing:** the rest of the ruler (2%, 5%, 15% and 40% of variance over 5% and 25% of cells, 80 runs), which gate named what, and how often a decoy is named in the ruler runs.

One change of wording from the first rule: D1 there said "named, and first". With two gates there is no single order, so D1 here is "a lead". Stated now, before the run.

## Confirmation

Unchanged, as fixed in `results/real-enso-drought.md` and coded in `src/causal_atlas/confirm.py` before the first discovery marks were read. It takes from discovery only which candidate was named; its claims, lags and slopes are its own, fitted on the discovery years. It is run once (`scripts/confirm_enso.py once`, which refuses a second scoring and writes its row to the first results file) **only if the instrument check and D1 to D4 here pass**, after this file's results are committed.

## What a pass and a miss would each mean

- **Pass:** the engine can name a continental driver and a strong regional one, blind, on the real field, with false alarms under control. Then the confirmation asks the question rule 2 asks: does El Niño improve a forecast of drought three months ahead beyond each cell's own history, season and neighbours, on years never touched.
- **Miss on the instrument check:** this pair of gates is still not good enough. Published as a miss; the confirmation years stay sealed.
- **Either way, the ruler is the limit to print beside any later finding:** what size and extent of link this search can and cannot hear in 49 years.

## Limits it carries

Those of the first rule, and:

- The marks other than the instrument check are not blind to the author.
- The ruler's link is planted in a compact patch for three months at one lag. A link scattered over cells that are not neighbours, or spread thinly over many months, is not what the sharp gate is built for.
- Regions are fixed squares. A link along a coast or a river would be split across them.
- Development used five decoy sets. The design was chosen there; the seeds scored here are fresh.

## Estimates

About 25 minutes of machine time for both steps. Tokens to this report: about 150k.
