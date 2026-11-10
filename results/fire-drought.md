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

Machine: about 20 seconds a seed for the three outcomes, 164 seeds (148: a miscount, corrected 2026-11-10 after the run), under an hour in one process. Real fields: minutes. Tokens: this rule and its run about 300k; the reader 300k to 450k, from what the last one cost. Overruns are reported beside the result.

## Result, step 1: the made-up panels (2026-11-10, 01:53 to 02:09 UTC)

`run_local.py known`, three processes, 148 seeds, 444 rows in `results/fire-drought.jsonl`; then `run_local.py marks`. **Every mark held.** Nothing was rerun or left out.

| Panel | Mark | Read as a link | Burned area passes | Adjusted passes | What the satellite saw passes |
|---|---|---|---|---|---|
| Link, 20% | at least 7 of 10 | **9 of 10** | 9 | 9 | 0 |
| Link and instrument | at least 7 of 10 | **9 of 10** | 10 | 9 | 10 |
| Nothing | at most 4 of 60 | **1 of 60** | 1 | 1 | 0 |
| Drift only | at most 2 of 24 | **0 of 24** | 1 | 0 | 0 |
| Instrument only | at most 2 of 24; sight at least 22 of 24 | **0 of 24; sight 24 of 24** | 24 | 0 | 24 |
| Link, 10% | none | 6 of 10 | 6 | 7 | 0 |
| Link, 5% | none | 1 of 10 | 1 | 1 | 0 |

**Six at a time, as the real fields are read: 0 of 18 sixes read as a link** (at most 1 allowed). Nothing: S on burned area from −0.0018 to 0.0000 across its ten sixes. Drift only: −0.0002 to +0.0006, adjusted −0.0004 to +0.0005, none passing. Instrument only: burned area passes in all four sixes (S about 1.1%), adjusted in none (−0.0003 to +0.0001), sight in all four (about 19%).

Each empty panel's seeds all together, a measurement:

| Panel | Burned area, S (interval) | Adjusted | Sight |
|---|---|---|---|
| Nothing, 60 seeds | −0.0004 (−0.0005 to −0.0003) | −0.0003 (−0.0005 to −0.0002) | −0.0002 |
| Drift only, 24 | +0.0001 (−0.0003 to +0.0003) | −0.0000 (−0.0004 to +0.0003) | −0.0003 |
| Instrument only, 24 | +0.0109 (+0.0100 to +0.0118), passes | −0.0001 (−0.0002 to +0.0001) | +0.1912, passes |

What this shows, in plain terms:

- **A link of 20% of a season's variance over a fifth of the cells is read 9 times in 10,** with or without an instrument effect beside it. At 10% it is read 6 times in 10; at 5%, once in 10. So a silence on the real fields means "nothing as large as about 10% of a season's variance over a fifth of a field", not "nothing".
- **With nothing there it reads a link once in 60 single panels and never in 18 sets of six.** With nothing there the model costs a little: about 0.04% more error than the baseline.
- **The lean seen on four smoke seeds of the drift panels was chance.** On 24 seeds together it is +0.0001 with an interval across zero, and beyond 3 of the 14 controls.
- **The instrument check works both ways.** With no link and an instrument effect, burned area alone passes 24 times in 24: without the adjusted outcome this test would have reported a link every time. Adjusted passes 0 in 24, and what the satellite saw gives it away 24 in 24.
- **Sizes are small even when the link is real.** With a planted link of 20%, S on burned area is 0.3% to 2.5% (middle 1.7%), because the model's claims spread over far more cell-months than hold the link. A size on the real fields is to be read against that.
- **It does not say where.** 40% of claims fall in planted cells, which are 20% of the cells kept.

Corrections to the rule's own wording, found in the run: the panels hold 148 seeds, not the 164 written under Estimates (a miscount; every registered seed was run). The six patches cover about a fifth of the cells a panel keeps (0.19 to 0.20), not a quarter, because patches overlap and run off the edge. "A quarter" above should be read as "a fifth".

Guess made beforehand: all marks hold, about 70%. They held.

Not yet done: the independent reader; no real field has been set against drought.

## Amendment after the independent check (2026-11-10, 02:35 UTC), before any real field is fitted

The reader's report is `docs/reviews/2026-11-10-fire-drought-rule-check/report.md`, saved as it came. It found no leak, and that the code does what this rule says. It found two ways a link could be read where there is none, and showed both on made-up panels of its own. What changes, and why, is decision 0048. Everything below is stricter than the rule above and replaces it where they differ.

**Seen before this amendment.** The reader's panels and looks, in its report. This session's smoke runs, never counted: the reader's two drift seeds (20006, 20004) under the amended verdict; seeds 20901 and 20902 of the new `before` panel; smoke seeds 19901 and 19902 again. The reader's look at real burned area against the share observed on 1982 to 2003, with no drought, run again here with the same numbers. No burned-area value has been set against drought.

1. **A pass needs one thing more.** Each reading is repeated with every driver term, shifted or not, less its own straight line across the scoring years (`local.level`). An outcome passes when it passes as registered above **and** this second reading has its interval above zero and beats all 14 shifts.
2. **New made-up panels** (`synth/local_panel.py`, `before` and `curve`):

   | Panel | What it is | Seeds | Mark |
   |---|---|---|---|
   | before | No link. What is recorded depends on this month's view and the month before's (power 0.3) | 20101 to 20124 | read as a link at most 2 of 24 |
   | curve | No link. Moisture and burning share a drift that quickens (size 6) | 20201 to 20212 | none: measured |

   The four sixes of `before` join the empty sixes: at most 1 of 22 read as a link.
3. **Every panel above is run again under the amended verdict,** same seeds, as rows of kind `made_up_2`. The marks are the ones registered above, now counted on these rows, with the two lines of the table added. `run_local.py fit` refuses the real fields unless all hold. The first run's rows are kept; on the old panels the reading as first registered must come out the same, and that is checked.
4. **The real reading is named** from the three pooled outcomes: "link" when burned area and adjusted burned area pass and the share observed does not; "not separable from what the satellite saw" when all three pass; "no link" otherwise. Under "What each outcome would mean" above, a pass with the share observed also passing is no longer called a link.
5. **`run_local.py score once` scores nothing** unless each model it fits equals the one `fit` recorded (baseline, form, tau, k, counts, lags).
6. **Beside every S:** S under the shifted drivers on average, and S with terms less their line. The headline size is the smaller of the two S. The pooled reading is also given without 2018; that marks nothing.

**Guesses.** Every mark holds on the new rows: 80%. `curve` read as a link: at most 1 of 12. The guesses for the real fields stand, with "a link is read" lowered from a third to a quarter, since a pass is harder and a gain that shows in the satellite's view is no longer called one.

**Corrections of wording, from the reader.** The outcome's mean and spread, and which months are in use, come from 1982 to 2003; "the fitting years" for targets are 1983 to 2003 without 1994. The planted patches cover 0.18 to 0.22 of kept cells by seed (mean 0.198). A pass carries no floor on size: one drift seed passed on burned area with S of 0.01%.

**Limits added.** The instrument check is tested against a same-month effect and a month-before effect of one sign; other forms are not excluded. The panels have one satellite step, the real record several. A link that is itself a steady rise or fall over the scoring years cannot pass.

## Result, step 1 again under the amended verdict (2026-11-10, 02:36 to 02:56 UTC)

184 seeds, 552 rows of kind `made_up_2` in `results/fire-drought.jsonl`. **Every mark held.**

| Panel | Mark | Read as a link | Burned area alone | Adjusted alone | Share observed |
|---|---|---|---|---|---|
| Link, 20% | at least 7 of 10 | **9 of 10** | 9 | 9 | 0 |
| Link, 20%, with an instrument effect | at least 7 of 10 | **9 of 10** | 10 | 9 | 10 |
| Link, 10% | measured | 6 of 10 | 6 | 6 | 0 |
| Link, 5% | measured | 1 of 10 | 1 | 1 | 0 |
| Nothing | at most 4 of 60 | **1 of 60** | 1 | 1 | 0 |
| Drift only | at most 2 of 24 | **0 of 24** | 0 | 0 | 0 |
| Instrument only, same month | at most 2 of 24; share observed at least 22 | **0 of 24** | 23 | 0 | 24 |
| Instrument only, month before (new) | at most 2 of 24 | **0 of 24** | 0 | 0 | 24 |
| Quickening drift (new) | measured | 0 of 12 | 0 | 0 | 0 |
| Empty panels six at a time | at most 1 of 22 | **0 of 22** | | | |

- **The first run is reproduced.** On the seven panels of the first run, all 444 rows give the same S and the same reading as first registered. No seed's reading as a link changed under the amended verdict.
- **What the added condition did.** Eight outcome rows that passed as first registered no longer pass. Four are on the quickening drift: seeds 20203 and 20212 would have been read as a link under the first rule (2 of 12), and are not now. The other four were single outcomes on panels with no link or a weak one (instrument 19516, month-before 20119, drift 19718, link 10% 19208); none was a reading as a link.
- **The quickening drift shows why S under the shifts is quoted.** Median S there is 0.99%, and median S under the shifted drivers is 0.96%: nearly all of it is there whichever years are paired. With terms less their line the median is −0.03%.
- **A planted link is barely touched.** Link 20%: median S 1.67% on burned area, 1.67% with terms less their line; S under the shifted drivers is below zero in every seed (median −1.0%).
- **The month-before panel, pooled over all 24 seeds:** burned area −0.01% (−0.02% to +0.00%), adjusted −0.00% (−0.01% to +0.01%), share observed +19.3%. At the setting above every real field, this effect does not reach the readings.
- Guesses: every mark holds (80%): held. Quickening drift read as a link at most 1 of 12: 0.
- Machine time about 20 minutes over three processes.

## Result, step 2: the real fields on the fitting years only (2026-11-10, 04:15 UTC)

`run_local.py fit`, 18 rows of kind `fit`. Nothing after 2003 was in memory. k is how much of the fitted slopes the fitting years themselves support when one part is held back: 1 is all of it, 0 is none.

| Field | Burned area | Adjusted burned area | Share observed |
|---|---|---|---|
| Africa | k 0.127, by month, 619 block-months, 5584 of 5872 cells, wetter-then-more 58% | k 0.14, by month, 619 block-months, 5584 of 5872 cells, wetter-then-more 59% | k 0.052 |
| South America | k 1, by season, 25 block-months, 205 of 5861 cells, wetter-then-more 57% | k 0.286, by season, 280 block-months, 2914 of 5861 cells, wetter-then-more 33% | k 0.041 |
| Australia | k 0.2, by season, 267 block-months, 2533 of 2624 cells, wetter-then-more 73% | k 0.766, by month, 39 block-months, 1388 of 2624 cells, wetter-then-more 69% | k 0.428 |
| South and Southeast Asia | nothing claimed | k 0.02, by month, 122 block-months, 2824 of 4299 cells, wetter-then-more 49% | k 0.27 |
| North America | k 0.005, by month, 385 block-months, 5176 of 5407 cells, wetter-then-more 47% | k 0.032, by month, 385 block-months, 5176 of 5407 cells, wetter-then-more 47% | k 0.275 |
| Europe | k 0.289, by month, 60 block-months, 1567 of 2659 cells, wetter-then-more 35% | k 0.044, by month, 179 block-months, 2361 of 2659 cells, wetter-then-more 39% | k 0.052 |

- **The baseline chosen is the same in every field** for burned area and adjusted burned area (`linear`).
- **Support inside the fitting years is thin.** Only South America's burned-area model keeps its slopes at full size, on a small patch: 205 of 5,861 cells, 25 block-months, all at a lead of seven months. Australia's adjusted model keeps three quarters, on about half its cells. Africa keeps about an eighth over nearly all its cells. North America keeps almost nothing, and South and Southeast Asia nothing at all on burned area.
- **Sign.** "Wetter-then-more" is the share of claimed cell-months where a wetter spell earlier goes with more burned area later. It runs from a third (Europe, South America adjusted) to nearly three quarters (Australia): both directions are present, as fuel growth and dryness would each give.
- **The share observed is itself claimed in every field** (k 0.04 to 0.43). What the satellite could see has some tie to earlier drought within the fitting years, which is why the adjusted outcome and the name "not separable" are there.
- Burned area and adjusted burned area each have k above zero in some field, so the rule allows step 3. Nothing here changes the rule or the guesses.
- Machine time about a minute and a half.

## Result, step 3: 2004 to 2018, scored once (2026-11-10, 04:18 UTC)

`run_local.py score once`: 18 rows of kind `score`, 3 of kind `pooled`, 1 of kind `reading`. Every model fitted was the one step 2 recorded. **The reading is "no link": a quiet null.**

S is the share of squared forecast error the drought term takes off the chosen baseline, on the cell-months the model claimed. "Of 14" is how many year-shifted drivers the real pairing of years beats.

| Six fields together | S (95% interval) | Beats | With terms less their line | S under the shifted drivers, mean | Without 2018 |
|---|---|---|---|---|---|
| Burned area | **-0.03%** (-0.08% to +0.03%) | 14 of 14 | +0.00% (-0.05% to +0.06%) | -0.06% | -0.03% (-0.09% to +0.04%) |
| Adjusted burned area | **-0.03%** (-0.08% to +0.01%) | 13 of 14 | -0.01% (-0.06% to +0.03%) | -0.05% | -0.03% (-0.09% to +0.02%) |
| Share observed | **+0.03%** (-0.04% to +0.10%) | 14 of 14 | +0.03% (-0.04% to +0.10%) | -0.10% | +0.04% (-0.04% to +0.12%) |

| Field by field (marks nothing) | Burned area | Adjusted burned area | Share observed |
|---|---|---|---|
| Africa | -0.06% (-0.16% to +0.06%), 9 of 14 | -0.07% (-0.17% to +0.04%), 7 of 14 | -0.00% (-0.02% to +0.03%), 6 of 14 |
| South America | -0.47% (-0.77% to -0.15%), 6 of 14 | -0.04% (-0.13% to +0.05%), 7 of 14 | +0.07% (+0.00% to +0.14%), 14 of 14 |
| Australia | +0.08% (-0.02% to +0.19%), 14 of 14 | +0.26% (-0.53% to +1.25%), 13 of 14 | -0.23% (-2.40% to +1.87%), 9 of 14 |
| South and Southeast Asia | nothing claimed | -0.01% (-0.03% to +0.01%), 6 of 14 | -0.00% (-0.17% to +0.15%), 12 of 14 |
| North America | +0.00% (+0.00% to +0.01%), 13 of 14 | +0.02% (-0.00% to +0.04%), 14 of 14 | +0.10% (-0.23% to +0.43%), 14 of 14 |
| Europe | -0.22% (-0.50% to +0.08%), 0 of 14 | -0.07% (-0.12% to -0.01%), 0 of 14 | +0.01% (-0.05% to +0.06%), 8 of 14 |

- **No outcome passes, together or in any field.** On burned area the drought term changes the forecast error by −0.03%, with an interval from −0.08% to +0.03%. Nothing is taken off the error. The same holds once what the satellite saw is taken out, and for what the satellite saw itself.
- **The real pairing of years does a little better than the shifted ones** (14 of 14 on burned area, 13 of 14 adjusted), but both sit below zero: the term adds a little error whichever years are paired, and slightly less with the true ones. That is not a gain.
- **Field by field,** Australia is the only one above zero on both outcomes (+0.08% and +0.26%), with intervals that include zero. Europe is worse than all 14 shifts on both. South America's small patch, the one model the fitting years supported at full size, made the forecast worse (−0.47%, interval below zero).
- **Leaving 2018 out changes nothing.**
- **Something the made-up panels did not imitate.** On 2004 to 2018 the simplest baseline that follows a cell's own recent level beats the baseline chosen on the fitting years by 12% of its error on burned area (13% adjusted), in every field (7% to 20%). Inside the fitting years the chosen one was better by 2% to 6%, as it was out of time on every made-up panel. So the record after 2003 does not behave as it did before, and the term was scored against a baseline that had itself gone stale. Two things follow. The registered condition "below each baseline alone" could not have been met by a link smaller than that gap. And how much of a real link this scoring could have heard on these fields is not what the made-up panels measured; it is measured next, on the real fields with a link planted in them.
- **Guesses, for the record:** burned area passes, 55%: it did not. Share observed passes, 60%: it did not. A link read, a quarter: not read.
- Machine time about two and a half minutes.

**What this means.** Each place's own drought four to twelve months earlier does not improve the forecast of its burned area in this product beyond the place's own history, on years never read. What the silence can rule out is a link of the kind planted in the made-up panels, **if** the real fields behave as those panels do, and the point above says they do not fully. Burned area's 2004 to 2018 are spent for this driver.

**Limits.** Those above and in the amendment. One product (FireCCILT11), one drought index (SPEI-3, with the evaporation error its makers have acknowledged), leads of four to twelve months only: the same season's drought, which is what fire weather is mostly about, is outside the test by design. Nothing here says drought does not matter to fire.

## After the scoring: what the silence can rule out (rule written 2026-11-10, 04:25 UTC, before it is run; marks nothing)

**Why.** The scoring found that the record after 2003 does not behave as the made-up panels do: the baseline chosen on the fitting years went stale. So the made-up panels' hearing (a link at 20% of variance read 9 times in 10) is not a measure of what this scoring could have heard on the real fields. This measures it directly: a link of known size is added to the real burned area and the whole thing is fitted and scored exactly as the real fields were.

**This is an exploration on spent years.** It reads burned area for 2004 to 2018 against drought again, with a planted term added; the real record's own relation to drought, which read as nothing, is inside every replicate. It marks nothing, changes no reading above, and no later test of burned area can count these years as unread.

**What is planted** (`scripts/explore_planted.py`, rows in `results/explore-planted.jsonl`).
- In each of the six fields, five-degree squares set half a square off the detector's own blocks, taken in random order until they hold a fifth of the field's cells. Each square gets one sign and one lead, four to twelve months, the same all year.
- In those cells, on the months in use from 1983 on, the standardised outcome y becomes sqrt(1 - share) of y plus sqrt(share) times the cell's SPEI-3 that many months earlier, standardised on 1982 to 2003 and scaled to y's own spread in that cell on those years; then clipped at 3 as before. The term is the drought value itself, not the departure the detector reads, as in the made-up panels.
- Sizes: 20%, 10%, 5% and 2% of the outcome's variance in the planted cells. Four replicates each, seeds 21001 to 21004, 21101 to 21104, 21201 to 21204, 21301 to 21304, one generator per seed and field.
- The share observed is not touched, so only burned area and adjusted burned area are fitted and scored, each field by `run_local.scored`, the six pooled by `run_local.pooled`, read by `run_local.verdict`.

**What is reported, per size and outcome.** Pooled S and its interval, how many shifted drivers it beats, S with every term less its line, S under the shifted drivers; whether it passes the amended verdict; and whether it passes **without** the condition "below each baseline alone", which the stale baseline may make unreachable. Also the share of claimed cell-months that fall in planted cells.

**How it will be read, fixed now.**
- A size is "heard" when, in at least 3 of its 4 replicates, both outcomes pass without the baseline condition. The smallest size heard is what the silence rules out, for a link of this shape.
- If 20% is not heard, the scoring could not hear on these fields and the null above says little.
- The count under the full amended verdict is given beside it. If a size is heard without the baseline condition and not with it, then the registered rule could not have read a link of that size as a link on these fields, whatever the data held, and that is said.
- The median pooled S at each size is set beside the real fields' interval (upper end +0.03% on burned area), so the null is stated as a size.

**Limits, known before it runs.**
- **The planted link is an easy shape.** It is added to every month in use, including cell-months where nothing burned, and it is straight-line in the standardised outcome. A real link acts only where and when something burns. At the same nominal share it is also stronger than the made-up panels' link, whose share is of the hidden strength behind the burning and not of what is recorded. So "heard" here is a ceiling: a size not heard here would not be heard in a real shape either; a size heard here might still be missed in a real shape. The made-up panels cover the real shape on a well-behaved record; this covers the real record with an easy shape.
- Four replicates a size: counts of 0 to 4, coarse.
- One lead per square, the same all year, a fifth of the cells: one pattern among many a real link could take.
- Before this was written the planting was checked on one field's fitting years with a throwaway generator (Europe, 1983 to 2003: a fifth of cells planted, nothing changed outside them or off the months in use, the outcome's spread unchanged). Nothing was fitted or scored.

**Guesses.** Heard without the baseline condition, of 4: 20%, 4; 10%, 4; 5%, 3; 2%, 1. Under the full amended verdict: 20%, 1; the rest, 0. So the guess is that 5% is the smallest size heard and that the registered rule could not have read it.

### Result (2026-11-10, 04:26 to 04:30 UTC)

16 rows in `results/explore-planted.jsonl`. Machine time about four minutes on four threads.

| Planted, in a fifth of the cells | Burned area: pooled S, median (range) | Adjusted: pooled S, median (range) | Heard, both outcomes, without the baseline condition | Under the full amended verdict |
|---|---|---|---|---|
| 20% of variance | +0.32% (+0.30% to +0.38%) | +0.32% (+0.27% to +0.41%) | **4 of 4** | 0 of 4 |
| 10% | +0.06% (+0.04% to +0.12%) | +0.08% (+0.04% to +0.11%) | 1 of 4 | 0 of 4 |
| 5% | +0.01% (-0.02% to +0.02%) | +0.00% (-0.01% to +0.04%) | 0 of 4 | 0 of 4 |
| 2% | -0.01% (-0.02% to -0.01%) | -0.02% (-0.03% to -0.01%) | 0 of 4 | 0 of 4 |
| The real fields, nothing planted | -0.03% (-0.08% to +0.03%) | -0.03% (-0.08% to +0.01%) | | |

- **By the reading fixed beforehand, 20% is the smallest size heard.** The silence rules out a link that moves a fifth of the variance in a fifth of the cells, in this easy shape. It does not rule out one half that size, and a link at 5% or 2% scores the same as no link at all.
- **The registered rule could not have read any of these as a link.** Not one of the 32 pooled readings is below every baseline alone. On the scoring years the plain level of a cell's last five years has 13% to 14% less error than the baseline chosen on the fitting years, and the month's average 2% less, and a drought term worth a third of a percent cannot make that up. So on these fields the rule, as registered, was unable to say "link" whatever the data held.
- **Every replicate beats all 14 shifted drivers,** down to 2%, where S is below zero. The real record beats 14 on burned area and 13 on the adjusted outcome. On these fields "beats all 14" is met with nothing behind it; the interval is what carries the reading.
- **The search hears little of what is planted.** A link at 20% in a fifth of the cells, found in full, would take about 4% off the pooled error. It takes 0.3%. And the claims are not placed: a fifth of claimed cell-months fall in planted cells, which is the share planted.
- **Guesses:** heard without the baseline condition, 4, 4, 3, 1 of 4 for 20%, 10%, 5%, 2%: it was 4, 1, 0, 0. Under the full verdict, 1 of 4 at 20%: it was 0. The search hears less than guessed.

**One thing about the planting, seen only after it ran.** The limits above call the planted link an easy shape. Its placement is the opposite: squares set half a square off the detector's blocks are cut in four by them, so no block ever holds a planted square whole, and a slope shared across a block is diluted to a quarter. That is the least favourable placement for this detector, and it pulls against "what is heard is a ceiling". A real link has no reason to sit on the detector's blocks either, but none to sit astride them. So the same check is run once more with the squares on the detector's own blocks, the most favourable placement, to bracket it.

### The same, with the planted squares on the detector's blocks (rule written 2026-11-10, 04:32 UTC, before it is run; marks nothing)

Everything as above, except that the planted squares are the detector's own five-degree blocks. Seeds 21401 to 21404 (20%), 21501 to 21504 (10%), 21601 to 21604 (5%), 21701 to 21704 (2%). Read the same way: a size is heard when both outcomes pass without the baseline condition in at least 3 of 4. The two placements bracket what the silence rules out; the statement made from them names both.

**Guesses.** Heard, of 4: 20%, 4; 10%, 4; 5%, 2; 2%, 0. Pooled S at 20% about 1.5%. Under the full verdict, 0 at every size.

### Result, squares on the detector's blocks (2026-11-10, 04:32 to 04:36 UTC)

16 more rows in the same file (`placement` is `aligned`). Machine time about four minutes.

| Planted, in a fifth of the cells | Squares astride the blocks: pooled S, median | Heard | Squares on the blocks: pooled S, median (range) | Heard | Full amended verdict, either placement |
|---|---|---|---|---|---|
| 20% of variance | +0.32% | 4 of 4 | +4.12% (+3.61% to +5.50%) | 4 of 4 | 0 of 8 |
| 10% | +0.06% | 1 of 4 | +1.69% (+1.31% to +1.95%) | 4 of 4 | 0 of 8 |
| 5% | +0.01% | 0 of 4 | +0.60% (+0.49% to +0.70%) | **4 of 4** | 0 of 8 |
| 2% | -0.01% | 0 of 4 | +0.09% (+0.07% to +0.12%) | 2 of 4 | 0 of 8 |

S is for burned area; the adjusted outcome is within 0.4 points of it at every size. "Heard" is both outcomes passing without the baseline condition.

- **Placement moves the answer more than size does.** On the detector's blocks a link is found nearly in full (4.1% at 20%, where 4% is everything) and 5% is heard every time. Astride them the same link scores a thirteenth as much and only 20% is heard. Claims fall in planted cells 41% of the time on the blocks at 20%, against 23% astride them.
- **Under the full amended verdict nothing passes, 0 of 64 pooled readings,** even a link that takes 4% off the error. The condition "below each baseline alone" fails every time: on the scoring years the plain level has 13% to 14% less error than the chosen baseline.
- **Guesses:** heard on the blocks 4, 4, 2, 0: it was 4, 4, 4, 2. Pooled S at 20% about 1.5%: it was 4.1%. Full verdict 0 at every size: held.

### What the silence rules out, and what this says about the test

- **Ruled out, in this easy shape:** a link moving 5% or more of the variance of burned area in a fifth of the cells, if it is laid out in areas the detector's five-degree blocks sit inside; 20% or more if it sits in five-degree patches astride them. A real link that covers a region several blocks wide is nearer the first case than the second. Put as a size: the real fields' reading, at most +0.03%, is below what a 2% link on the blocks gave (+0.07% to +0.12%).
- **Not ruled out:** anything smaller; a link of a real shape, which acts only where something burns, at the same nominal size; the same season's drought; other leads.
- **The registered rule was broken on these fields.** It could not have returned "link" for any link tried here. The reading "no link" above stands, because S itself, which does not depend on that condition, sits on zero with a narrow interval. But had S been clearly above zero the rule would still have said "no link", and that would have been wrong. The made-up panels did not catch this because their record does not change its behaviour between the fitting and the scoring years.
- **Three faults in the test, for whatever is built next:**
  1. A baseline chosen once on the fitting years can go stale. The condition should be that the term improves each baseline it is added to, or the baseline should be re-chosen as the years go by using only the past.
  2. Slopes shared within fixed blocks lose most of a link that does not sit on them. Blocks at more than one offset, or slopes smoothed across neighbours, would not.
  3. Made-up panels need a record that changes its behaviour part-way, since the real one did.
- "Beats all 14 shifted drivers" carries no weight on these fields by itself: it was met at every size, including where S was below zero.
