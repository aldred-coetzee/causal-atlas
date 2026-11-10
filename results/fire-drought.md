# Each place's own drought and its burned area, four or more months later

Rule first, committed before any counted number and before any burned-area value is set against drought (rule 9). Authority: decisions 0040, 0046 and 0047. Code: `src/causal_atlas/local.py`, `src/causal_atlas/fire.py` (unchanged but for one function split out), `src/causal_atlas/forecast.py` (unchanged), `synth/local_panel.py`, `scripts/run_local.py`. Seeds: `results/seed-ledger.md`. Rows: `results/fire-drought.jsonl`.

Data, both already held and described in `docs/data-sources.md`: burned area from the ESA Climate Change Initiative, Fire CCI project (Chuvieco, E.; Pettinari, M.L.; Otón, G. (2020): AVHRR-LTDR Fire_cci Burned Area Grid product, version 1.1. Centre for Environmental Data Analysis. doi:10.5285/62866635ab074e07b93f17fbf87a2c1a); drought from SPEIbase 2.11.0 (SPEI-3, built from CRU TS 4.09; ODbL 1.0).

## Why

The first test outside climate (`results/fire-enso.md`) asked whether one series, El Niño, leads burned area over whole regions. It missed, and the check of it showed two things: the blind search's controls were flawed (decision 0046), and twenty fitting years are too few when the only evidence is one series against one region's average.

This test spends the same record differently. The driver is not one series for the world: it is **each half-degree cell's own drought**, so in one year a field holds thousands of different driver values beside thousands of outcomes. The years stay the unit of evidence (cells in one year move together and are counted once), but each year now carries far more.

The question: **does a cell's own drought, four or more months earlier, improve a forecast of its burned area beyond what the cell's own history, its neighbours and the season already give, on years never read?** Drought and burned area are named. Where, in which season, at which lag and with which sign are not: each five-degree block finds its own from the fitting years, or finds nothing.

Burned area from this product has a known weakness: how much the satellite sees depends on cloud, and cloud on drought. So the test is run three ways and a link is claimed only when it survives taking out what the satellite's own view explains.

## Seen before this rule

- **Everything listed in `results/fire-enso.md`, "Seen before this rule" and its results:** how much of each field the satellite saw (all years), each field's shape on the fitting years, El Niño against burned area on the fitting years (named nowhere), and El Niño against the share observed on the fitting years (named in South and Southeast Asia and South America).
- **From the independent reader of that result** (`docs/reviews/2026-11-10-fire-enso-independent-check/`), all on the fitting years: the share observed rises with the year in every field (correlation +0.40 to +0.68); burned area is zero in 56% of cell-months and falls with the year in the four tropical and southern fields (about −0.37); the product ranks 1997 only 12th to 13th of 21 years in equatorial Asia.
- **Which burned-area cells have a drought value, and the driver's own shape, over all years** (no burned-area value read against drought):

  | Field | Cells with a drought value, of cells kept | Five-degree blocks | Calendar months of blocks with at least 20 cells in use | Spread of the driver |
  |---|---|---|---|---|
  | Africa | 5,872 of 5,952 | 108 | 619 | 1.06 |
  | South America | 5,861 of 5,968 | 86 | 534 | 1.21 |
  | Australia | 2,624 of 2,673 | 46 | 267 | 1.13 |
  | South and Southeast Asia | 4,299 of 4,367 | 95 | 418 | 1.14 |
  | North America | 5,407 of 5,409 | 99 | 385 | 1.10 |
  | Europe | 2,659 of 2,659 | 61 | 179 | 1.09 |

- **Smoke runs of the method on made-up panels, seeds 19901, 19902, 19903 and 19999,** never in a count. The design below was reached on them, and each change is listed because each was made after seeing a result:
  1. Block-months were first picked by a false-discovery cut. It was too strict: a planted link was rarely claimed. Replaced by keeping part of every slope according to how sure it is, with the threshold chosen inside the fitting years.
  2. With one slope per calendar month a planted link was heard too seldom. A second form was added, one lag and slope per block for its whole season, and the fitting years choose between the two. The generator at first gave every patch one lag for its whole season, which is that form's own assumption; half its patches now have a lag that grows through the season.
  3. The share observed was first taken out with a straight line. A panel with no link except through the instrument then passed. Replaced by bands of the share observed, whatever the shape.
  4. With the driver used as it comes, a panel holding nothing but a drift shared by driver and outcome passed. The driver is now read as its departure from the cell's own last five years.
  5. Pooling the four smoke seeds as the six real fields will be pooled, the drift panels leaned slightly positive (below). So the empty panels are also read six at a time, with a mark, and the drift and instrument panels were widened from 10 seeds to 24.

  The numbers of stages 1 to 4 were scratch output and are not kept. With the design as it now stands, by seed:

  | Panel | Read as a link | Burned area passes | Adjusted passes | What the satellite saw passes |
  |---|---|---|---|---|
  | Link, 20% of variance | 4 of 4 | 4 | 4 | 0 of the 2 noted |
  | Link, 10% | 3 of 4 | not noted | not noted | not noted |
  | Link, 5% (two seeds) | 0 of 2 | 0 | 0 | 0 |
  | Link and instrument | 4 of 4 | 4 | 4 | 4 |
  | Nothing | 0 of 4 | 0 | 0 | 0 |
  | Drift only | 0 of 4 | 0 | 0 | 0 |
  | Instrument only | 0 of 4 | 4 | 0 | 4 |

  Sizes: with a link of 20%, S of 0.8% to 1.6% on burned area; instrument only, 1.1% to 1.7% on burned area, about zero adjusted, 18% to 21% on what the satellite saw. The four seeds read together: nothing, −0.0002 (−0.0008 to +0.0003) and adjusted −0.0007; instrument only, burned area +0.0144 (passes), adjusted 0.0000 (−0.0007 to +0.0007, does not pass); **drift only, +0.0002 and adjusted +0.0003 (−0.0003 to +0.0009), beyond all 14 controls, not passing only because the interval reaches zero.**
- **Where claims fall:** with a link planted in a quarter of the cells, 30% to 50% of the model's claims lie in those cells. It says the driver helps over the field. It does not say where.
- **The marks below were set after these runs.** They are counts on fresh seeds.
- **Not seen: any correlation, map, average or forecast of burned area against drought, on any year.** The real fields have not been passed to this code except to count cells.
- The author knows from general reading, not looked up for this rule, that wet seasons build fuel in dry grasslands and that drought dries forests, so links of either sign at these lags would surprise nobody. Nothing about place, size or sign is taken from that.

## Data and split

- **Outcome:** burned area exactly as in `results/fire-enso.md`: log(1 + km² burned / share observed), standardised per cell and calendar month on the seen months of the fitting years; a cell-month is seen at 0.2 of its burnable land observed; a cell's calendar month is in use when seen in at least 15 fitting years and burned in at least 5; all else zero; clipped at plus or minus 3. Same six fields, less the cells with no drought value (table above).
- **Driver:** the cell's SPEI-3, clipped at plus or minus 3, read as its **departure from the cell's own mean for the same calendar month over the five years before**. Nothing later than a value goes into it. SPEI from 1977 to 1981 supplies the years before the fire record starts.
- **Lags: 4 to 12 months.** SPEI-3 at lag 4 covers the months six to four before the month forecast.
- **Fitting:** target years 1983 to 2003 without 1994, twenty. **Scoring: 2004 to 2018, fifteen years, once.** Nothing from the scoring years enters anything fitted (tested).
- **Three outcomes, each through the same steps:**
  - **plain:** burned area as above;
  - **adjusted:** burned area less what the share observed in the same month explains of it. Per five-degree block and calendar month, the cell-months in use are put in five bands of the standardised share observed (cuts at −1.5, −0.5, 0.5, 1.5); each band's mean burned area over the fitting years, pulled toward zero where the band is thin (count over count + 5), is taken off;
  - **sight:** the standardised share observed itself, in place of burned area. Not an outcome of interest: it shows whether drought leads what the satellite could see.

## Method

1. **Baseline.** Three candidates as before (`forecast.py`): the long-run average; the cell's last 60 months; one least-squares fit over all cells on own values 3, 4, 5, 6 and 12 months back, the neighbours' mean 3 months back, and own trailing means of 12 and 60 months, fitted on cell-months in use. The one with the least error across five folds of the fitting years is the baseline. The driver is fitted to what it leaves.
2. **Evidence.** For each lag, calendar month and five-degree block with at least 20 cells in use that month: one number per fitting year, the sum over the block's cells of driver times residual. Its mean over the twenty years is set against its spread over the years (a t). A block's lag is the one with the surest t; its slope is the least-squares slope at that lag. Two forms: by calendar month, or one lag and slope per block from all its tested months together.
3. **How much is kept.** A slope is multiplied by max(0, 1 − (τ/|t|)²). A block-month is claimed when any of its slope is kept. Every kept slope is then sized by one number k in 0 to 1.
4. **Chosen inside the fitting years, together:** the form, τ among 0, 1, 1.5, 2, 2.5 and 3, and k, by least error on each fold of years with the evidence taken from the other folds. **k = 0 means nothing held up, and the model claims nothing.**
5. **Scoring.** On the claimed cell-months of the scoring years: S = 1 − (model's squared error / baseline's). A 95% interval from 2,000 draws of years. **Controls: the whole field's driver for each scoring year replaced by another scoring year's, circularly, all 14 shifts,** each scored exactly as the real alignment is. Each baseline's error alone on the same cell-months.
6. **An outcome passes** when the interval's low end is above zero, S is above S under every one of the 14 shifts, and the model's error is below each baseline's alone (`run_continents.verdict`, unchanged).
7. **The reading. A link from drought to burned area is claimed only when plain and adjusted both pass.** Sight is reported beside it. If sight passes too, the link is reported as not fully separable from the instrument.
8. **The six real fields are read together:** squared errors summed over fields year by year, then steps 5 to 7. Each field's own numbers are reported and mark nothing.

## Step 1: made-up panels (rule 3)

`synth/local_panel.py` imports nothing from the detector (tested). A panel is 60 by 100 half-degree cells over 37 years with one year absent, put through the same preparation as a real field. Burning has a four-month season that moves with latitude, fine noise, a shock each year shared over wide areas, carry-over from the year before, zeros, stray fires out of season, and a later satellite that records more. Seen share has its own cloud and gaps.

| Panel | What is in it | Seeds | Mark |
|---|---|---|---|
| Link, 20% | In six round patches over a quarter of the cells, burning in season follows moisture some months before, sign by patch; 20% of the variance of burning's strength there | 19101 to 19110 | **read as a link in at least 7 of 10** |
| Link, 10% | The same at 10% | 19201 to 19210 | none: measures what can be heard |
| Link, 5% | The same at 5% | 19301 to 19310 | none: measures what can be heard |
| Nothing | Burning owes nothing to moisture | 19401 to 19460 | **at most 4 of 60** |
| Instrument only | No link; the share observed follows moisture five months before, and what is recorded falls as its cube | 19501 to 19524 | **read as a link in at most 2 of 24, and sight passes in at least 22 of 24** |
| Link and instrument | Both | 19601 to 19610 | **at least 7 of 10** |
| Drift only | No link; one wide map times a straight line through the record, added alike to moisture and to burning | 19701 to 19724 | **at most 2 of 24** |

**And read six at a time, as the real fields are:** the three empty panels (nothing, instrument only, drift only) in runs of six consecutive seeds with their errors summed, 10 + 4 + 4 sixes. **Mark: at most 1 of the 18 sixes is read as a link.** Each empty panel's seeds all together are also reported, as a measurement.

**If any mark misses, the real fields are not set against drought** (`run_local.py fit` refuses) and the result is a null about this method.

## Step 2: the real fields, fitting years only

`run_local.py fit`: each field and outcome fitted with nothing after 2003 in memory. Reported: baseline, form, τ, k, block-months and cells claimed, lags, share of positive slopes. **If k = 0 in every field for plain, or in every field for adjusted, nothing is scored** and 2004 to 2018 stay sealed for this driver.

**Before this step, an independent reader sees this rule, the code and the made-up results.** What it finds is applied and disclosed before any real field is fitted.

## Step 3: 2004 to 2018, once

`run_local.py score once` (refuses a second run). All fields and outcomes scored, then read together as in the method.

## What each outcome would mean

- **Link (plain and adjusted pass, pooled).** A lead from one domain to another, found without naming where, when or which way: knowing a place's drought four or more months ahead cuts its burned-area forecast error, on years never read, and not only through what the satellite could see. It gets an independent reader before it is called a finding. Then a further rule asks whether it survives taking El Niño out. **The size is given with its plain meaning. A pooled S under 1% is reported as present but too small to forecast with.**
- **Link, and sight passes too.** As above, with: drought also leads what the satellite sees, and the adjustment may not take all of that out.
- **Plain passes, adjusted does not.** Drought leads what this product reports. It cannot be told from drought leading what the satellite could see. No link claimed.
- **Neither passes.** A quiet null: no lead that this test can hear. What it can hear is the measurement on the 10% and 5% panels.
- **A made-up mark misses.** A null about the method. The real fields stay unread against drought.

A pass does not show cause, does not say where, and does not say drought acts by itself.

## Guesses, written now so they cannot be adjusted

- Made-up marks: all hold, about 70%. Most likely to miss: the sixes, or the link and instrument panels.
- Real fields, plain passes: about 55%. Adjusted passes given plain does: about 60%. So a link is read: about a third.
- Sight passes: about 60%. SPEI-3 carries over from month to month, so drought four months back still says something about cloud now.
- If a link is read, its pooled size: under 2%, more likely than not under 1%.

## Limits, stated now

- **It does not say where.** On the smoke runs a third to a half of the claims fell in the planted quarter of the cells.
- **Something else may sit behind both.** El Niño leads drought in four of these fields and shows in what the satellite sees. A pass here is not a drought effect until that is taken out.
- **Cloud.** Counting a cell-month as seen at 0.2 selects on cloud, and so on drought. Months not seen count as "average for the month", in fitting and in scoring. The adjusted outcome and the instrument panels address the first; the second is not measured.
- **Shared drift.** The share observed rises and burned area falls through the record; the driver may drift too. Departures from a five-year mean leave a steady drift as a constant, not as nothing. A gain from that should not beat the year-shifted controls, which keep it, but they are 14: one chance in 15 for each outcome. The drift panels use one strength of drift, a guess. Reported beside any pass: S under the shifts. If their mean is itself above zero, part of the gain is not tied to the year.
- **Breaks.** 1994 is absent and the record is stitched from several satellites. The made-up panels have one break of one kind.
- **Fifteen scoring years, 14 controls.** The interval rests on fifteen years.
- **The drought file** is scaled by its makers on 1901 to 2024, later years included, and carries their acknowledged evaporation error (versions 2.6 to 2.12.0).
- **Year-to-year departures only.** A link that works through slow change is thrown away with the drift.
- **The product itself.** It does not show 1997 as a large fire year in equatorial Asia. A null here may be the product's.
- **The made-up panels are the author's guesses,** written in the same hours as the detector and changed beside it (listed above). Their early years have fewer years before them than the real driver has.
- **Per-seed marks, pooled reading.** The sixes mark is the one that matches how the real fields are read; it rests on 18 sixes.
- **Many places at once is handled by one pooled verdict,** not by a correction per place. No single block's claim is a finding.

## Estimates

Machine: about 20 seconds a seed for the three outcomes, 164 seeds, under an hour in one process. Real fields: minutes. Tokens: this rule and its run about 300k; the reader 300k to 450k, from what the last one cost. Overruns are reported beside the result.
