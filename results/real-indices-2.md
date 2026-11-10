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

## Results of step 1 (run 2026-11-09 23:36 to 2026-11-10 00:08 UTC; rows in `results/real-indices-2.jsonl`)

Everything above this line was committed before any of these numbers existed. 500 runs, all on 1950 to 1999.

### Step 1a. The instrument check: held

| Part of the mark | Asked | Got | With the old controls |
|---|---|---|---|
| The link of 40% of variance over 25% of the cells found, pooled | at least 45 of 50 | **49 of 50** | 42 |
| The same, in every field | at least 8 of 10 | South America 10, Australia 9, South and Southeast Asia 10, North America 10, Europe 10 | 9, 10, 4, 9, 10 |
| Where found, share of claims in the planted cells | at least 0.80 | 49 runs between 0.88 and 1.00 | one at 0.73 |

The one run not found is Australia, seed 15709.

The ruler, found out of 10, by share of variance and share of cells:

| Field | 5% over 5% | 5% over 25% | 15% over 5% | 15% over 25% | 40% over 5% | 40% over 25% |
|---|---|---|---|---|---|---|
| South America | 0 | 0 | 0 | 0 | 0 | 10 |
| Australia | 0 | 0 | 0 | 1 | 1 | 9 |
| South and Southeast Asia | 0 | 0 | 0 | 5 | 6 | 10 |
| North America | 0 | 1 | 1 | 4 | 7 | 10 |
| Europe | 0 | 0 | 0 | 0 | 4 | 10 |
| All five | 0 of 50 | 1 of 50 | 1 of 50 | 10 of 50 | 18 of 50 | 49 of 50 |
| All five, old controls | 0 | 0 | 0 | 1 | 11 | 42 |

So with 44 candidates this search hears a large, wide link nearly every time, a large narrow one or a middling wide one in a fifth to a third of runs, and nothing small. A link it does not name is not shown to be absent. South America is the hardest field: nothing below the largest size was found there.

A decoy that had no link planted was named in 8 of the 300 runs: one decoy in all six runs of one Australian set (seed 15707), once more in Australia (15708), once in South and Southeast Asia (15806). Reported, marking nothing; by decoy set that is 3 of 50.

### Step 1b. Naming: N1, N2 and N3 held

| Mark | Asked | Got |
|---|---|---|
| N1: the ONI a lead where it was before | at least 18 of 20 in each of four fields | South America 20, Australia 20, South and Southeast Asia 20, North America 20 |
| N2: a decoy a lead | at most 8 of 100 | 3 (South America 15113 and 15119, North America 15420; in each beside several real series) |
| N3: anything a lead with the years mixed | at most 8 of 100 | 5 (South America 15105, a decoy; South and Southeast Asia 15301, 15308 and 15312: the Arctic Oscillation, a decoy, the Iceland North Atlantic Oscillation; North America 15406, the Indian Ocean Dipole) |

In Europe the ONI was a lead in 0 of 20, as in every earlier test.

**Named (a lead in at least 18 of 20 sets), beyond the ONI: 16 pairs.**

| Field | Named | Below 18 |
|---|---|---|
| South America | Northern Oscillation (noi) 20, warm pool (whwp) 20, tropical South Atlantic (tsa) 18 | eastern Indian Ocean pole (dmieast) 8, Atlantic Meridional Mode 1 |
| Australia | Indian Ocean Dipole (dmi) 19 | noi 6 |
| South and Southeast Asia | Pacific Meridional Mode wind (pmmwind) 20, dmi 20, dmieast 20, whwp 20, noi 20 | Pacific Meridional Mode 10, Arctic Oscillation 10, East Atlantic 10, North Pacific Gyre 8, Scandinavian 5 |
| North America | dmieast 20, Pacific Decadal Oscillation (pdo) 20, noi 20 | Pacific/North American pattern 12 |
| Europe | Scandinavian (scand) 20, North Atlantic Oscillation, Gibraltar (nao_gib) 19, Arctic Oscillation (ao) 18, Greenland Blocking (gbi) 18 | |

Nothing was named anywhere for the sunspot number, the tornado count, either stratospheric wind series, or ten of the other series.

### What follows from the rule

Every mark of step 1 held, so step 2 is run, once, on these 16 pairs: m = 16, and the interval is taken at 1 − 0.05/16. This is the search the first attempt was meant to test, with its controls put right.

What the naming says and does not: these series are tied to drought in these fields in 1950 to 1999 more strongly than 47 displaced copies of any candidate. It does not say they are separate causes. Most of those named outside Europe are El Niño seen from another place or moving with it, and three false-alarm runs in a hundred is what the search costs.

### Against the guesses

- Instrument check passes: yes. The 40% over 5% link "in about half": 18 of 50, a third. Better than 11, less than guessed.
- N1 holds in all four: yes. N2 and N3 between 2 and 6: 3 and 5.
- Named: the lists seen beforehand, as said, which was no guess. Not seen beforehand: none of the 16. m guessed at 20 to 30; it is 16, because the series near the bar in South and Southeast Asia stopped at 10 of 20.

### Disclosures

- **Order of looking.** One ruler row was looked at while the run was going, to see that it had started (South America, seed 15601, the smallest link: not found, and the ONI, noi, whwp and tsa named). After that only the row count, until the marks were printed at the end.
- **Machine time:** 32 minutes (ruler 19, naming 13) against 55 estimated.
- **The naming was not blind,** as stated in the rule above. The marks were.

## Results of step 2 (run once, 2026-11-10 00:10 to 00:12 UTC, from d306ee9; rows in `results/real-indices-2.jsonl`)

Step 1's results were committed before this step ran. It ran once. These fields' years after 1999 are now spent for these 16 pairs.

**No pair passes.** This is the third outcome written beforehand: named, but no pass.

Region scale, the headline. A claim is one region in one calendar month at one lag of 4 to 12 months, kept only where it is significant on the fitting years in what own history and El Niño leave. For scale, El Niño's own term claimed 353, 113, 260 and 57 region-months in the four fields where it was named.

| Field | Series | Claims | S | Interval at 1 − 0.05/16 | Beyond the 24 shifts | Below every baseline |
|---|---|---|---|---|---|---|
| South America | tropical South Atlantic | 1 | +0.039 | −0.301 to +0.240 | 24 | yes |
| South America | warm pool | 0 | | | | |
| South America | Northern Oscillation | 0 | | | | |
| Australia | Indian Ocean Dipole | 0 | | | | |
| South and Southeast Asia | Pacific Meridional Mode wind | 1 | −0.000 | −0.019 to +0.015 | 10 | no |
| South and Southeast Asia | Indian Ocean Dipole | 3 | −0.018 | −0.053 to +0.016 | 15 | no |
| South and Southeast Asia | eastern Indian Ocean pole | 14 | −0.035 | −0.163 to +0.097 | 17 | yes |
| South and Southeast Asia | warm pool | 0 | | | | |
| South and Southeast Asia | Northern Oscillation | 0 | | | | |
| North America | eastern Indian Ocean pole | 0 | | | | |
| North America | Pacific Decadal Oscillation | 2 | −0.114 | −0.453 to +0.376 | 14 | no |
| North America | Northern Oscillation | 0 | | | | |
| Europe | Arctic Oscillation | 1 | −0.018 | −0.255 to +0.202 | 15 | no |
| Europe | Scandinavian | 0 | | | | |
| Europe | Greenland Blocking | 0 | | | | |
| Europe | North Atlantic Oscillation, Gibraltar | 0 | | | | |

- **Ten of the 16 pairs make no claim at all** at four months or more. By the wording fixed beforehand: related, with nothing to say three months ahead.
- **Six make a claim, on 1 to 14 region-months of the 768 to 1,260 a field has, and none adds to the forecast.** Five have S at or below zero. The sixth, the tropical South Atlantic for South America, has S of +0.039 on a single region-month: beyond all 24 shifts and below every baseline, with an interval from −0.30 to +0.24. One region in one month of the year is no evidence either way.

Cell scale, reported and marking nothing: three pairs make claims. The tropical South Atlantic for South America, 70 cell-months, S +0.002 (−0.158 to +0.130); the eastern Indian Ocean pole for South and Southeast Asia, 137, S +0.008 (−0.122 to +0.100); the Arctic Oscillation for Europe, 22, S −0.088 (−0.652 to +0.305). None would pass.

The straight line in time, marking nothing: at the region scale it makes no claim in four fields, and in North America 20 claims with S of −2.92, which is to say a trend fitted on 1950 to 1999 made the forecast far worse after. No pair passed, so there is no pass to set against it.

### What this says, and what it does not

- **About these series:** eleven of them are tied to drought in one or more of these fields in 1950 to 1999, strongly enough to be named among decoys. Once each region's own recent history and El Niño are in the forecast, none of them says anything usable four or more months ahead about 2000 to 2024. Most of those named outside Europe move with El Niño; Europe's four made one claim between them at these lags. That is roughly what the author guessed, and it was the outcome named beforehand as the most likely.
- **About the search:** with its controls corrected it handles 26 real series and 18 decoys at once and passes its checks. That is the thing this iteration was built to find out, and it stands whatever step 2 said.
- **Not shown:** that these series have no lagged effect. The forecast step asks for significance on 49 fitting years in a residual, then a gain over 25 scored years at a level set for 16 pairs. No planted link was put through this step with a second driver, so how large an added effect it would have caught is not measured. Links inside three months cannot pass by design.
- **Not about anything but climate series and drought.** The project's question, a link between domains, is still open.

### Against the guesses

Most named series add nothing beyond El Niño: yes. If any passed, the tropical South Atlantic for South America, the Dipole for Australia or the Pacific Decadal Oscillation for North America: none passed; the first was the only pair with S above zero, the Dipole made no claim for Australia, the third was negative. Europe's patterns make few claims: one, of four series. No pass at all: as guessed.

### Disclosures

- **Machine time:** under 2 minutes against 5 to 10 estimated.
- **One step, one run.** The script refuses a second scoring.
- Nothing passed, so the independent check and the reading against published science that a pass would have had are not run.
