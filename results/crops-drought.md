# Other crops and drought: where the drought term has helped a record before, does it go on helping, and is that enough to use?

Rule first, committed before any counted number and before any real yield of these crops is set against drought (rule 9). Authority: decisions 0040 and 0054. Code: `src/causal_atlas/claims.py`, `src/causal_atlas/harvest.py`, `src/causal_atlas/yields.py`, `synth/harvest_panel.py`, `scripts/run_claims.py`, tests in `tests/test_claims.py` and `tests/test_harvest.py`. Seeds: `results/seed-ledger.md`. Rows: `results/crops-drought.jsonl`.

Data, both held and described in `docs/data-sources.md`: yields from FAOSTAT, Crops and livestock products (FAO, CC BY 4.0; file dated 2025-12-31, 1961 to 2024); drought from SPEIbase 2.11.0 (SPEI-3, built from CRU TS 4.09; ODbL 1.0). Nothing new is fetched.

## Why

The cereal test (`results/harvest-drought.md`) read a link and found it too small to use: each country's drought index takes 1.67% off the squared error of a forecast of its cereal yields, about 0.8% of a typical error. The same result said the link is not spread evenly. Ten countries gave more than half of the gain, and the third of records where the term had helped most before 2005 kept 5.3% afterwards while the rest kept nothing.

So the question that follows is not whether there is a link. It is: **in the records where the drought term has gone with the yield before, as known each year from earlier years alone, does it go on helping, and is the gain there large enough to forecast with?**

That reading of the cereals was made after the fact, on a record now spent for this driver. It can be tested only on records not yet read, with the rule written first. The records are the other crops in the same FAO file.

## What has been looked at, and what has not

- **Not looked at: any real yield of the other crops beside any drought value.** `scripts/run_claims.py real once` is the first time, and it refuses unless the year-end marks below hold.
- **Looked at, alone:** the other crops' yields, to count series and build the panel. No baseline has been run on them.
- **Looked at, and used to shape this rule: the cereal record,** which is spent for this driver. Every choice below was tried on it and on made-up records with smoke seeds. What it gave under this rule is in decision 0054 and is a development number: it chose the rule, so it cannot test it.

The real panel: **2,339 records** (a country's series of one crop with 30 or more official years, in a country the drought file covers) of **47 crops** in **139 countries**; 78,552 official figures from 1986 to 2024. A crop is in when it is a single crop in FAOSTAT (item code under 1700), is not one of the six cereals already read, and has at least 30 such series. Chosen by that count alone; no crop was picked or dropped for being thought rain-fed or irrigated. The 503 cereal records run beside them.

## Method

Fixed now. Names in brackets are in `claims.py` unless said.

- **The forecast is the cereal test's, unchanged** (`harvest.run`; `results/harvest-drought.md`, Method): log yield; every year forecast from earlier years only; seven baselines, the one in force chosen again each year; each country's SPEI-3 at six months that do not overlap; slopes at five scales added with shared weights; 1986 to 2024 scored; 62 other-year shifts; the flat driver. For each record and scored year it gives the baseline's error and the drought term.
- **All records run together, cereals and other crops.** The cereals inform the baseline chosen each year, the slopes shared within a country and the shared weights. **Only the other crops' records are scored, and only they can claim** (`only`).
- **The claim** (`standing`, `claimed`). Each year, for each record: the slope, through the origin, of the baseline's error on the drought term over the record's own earlier scored years, at least ten of them (LEAST). The record **claims** that year when the slope stands **1.5 or more of its standard errors above zero** (MAIN). So the first claims can fall in 1996.
- **The forecast on a claim** is the baseline plus the term times that slope, the slope held between 0 and 1 (CAP): a record's past may shrink its term, not enlarge it. Where a record does not claim, it is not forecast with drought and not scored here.
- **S on the claims** is the share of the baseline's squared error, over every record-year that claims, that this forecast removes. Beside it, always, the plain size: the share of a typical error, 1 − √(1 − S) (`plain`).
- **The interval** is the middle 95% of 2,000 draws in which countries and years are both drawn again (`two_way`), as decision 0053 found it should be.
- **Controls.** Under each of the 62 shifts the driver's term is a different one, so each shift makes **its own claims** by the same rule and has its own S on them. A shift with no claims counts as S of zero. The same again with the flat driver: its own forecast, its own claims, its own shifts.

**Read** when all of these hold, with the driver as it fell and again with the flat driver (`reading`):
1. at least 30 records in at least 15 countries claim at some time (FEW);
2. S on the claims has an interval above zero;
3. S on the claims is above S on the claims of every one of the 62 shifts;
4. S on the claims is above zero without its best year;
5. on the record-years that claim, the forecast's error is below each of the seven baselines' alone.

**The size reported is the smaller of S with the driver as it fell and S with the flat driver.** Its words are the cereal test's, fixed before that result, with one addition:

| Size, of squared error | Of a typical error | Word |
|---|---|---|
| not read | | not read |
| under 1% | under 0.5% | too small to forecast with |
| 1% to 5% | 0.5% to 2.5% | a real but small aid |
| 5% or more, and the lower end of both intervals at 1% or more | 2.5% or more | a usable aid |
| 5% or more, a lower end under 1% | | may be a usable aid; not settled |

**Two variants,** as before. *Year-end* uses all six values of the driver and **is the result.** *Mid-year* uses the first four, to June of the harvest year; it is reported beside, with its own marks on two panels.

**Reported without marks:** the same reading with claims at 1.0 and at 2.0 standard errors (LEVELS); how much of the error that could have been claimed was; S, with the term as it stands, on the record-years that could have claimed and did not; S on the claims with the term as it stands and not scaled; the cereal test's own six conditions on all the other crops' records, with the two-way interval (`pooled`); the weights; the baselines chosen; and, for the real record, the claims and their gain by crop, by country and by record.

## Step 1: made-up records

`synth/harvest_panel.py` shares no code with the detector; what a world is made of is in `results/harvest-drought.md`, step 1. For this test a world has **six crops that stand for the cereals** and a number of others. The six are grown as widely as cereals and are linked, at 20% of variance, wherever their country is (about half the countries, in patches), as in the cereal test's link panel. Each other crop is grown in a tenth to two thirds of countries, with its own season. They run exactly as the real record will: the six beside, not scored.

Most worlds are small, six crops and twelve others (about 500 to 700 scored records), so that enough seeds can be run. Two panels are the size of the real record, six and forty-seven. The detector is told nothing of any of this.

`run_claims.py known`, 62 shifts, fresh seeds never used before.

| Panel | What is in it | Seeds | Mark, year-end | Mark, mid-year |
|---|---|---|---|---|
| Leak | The six linked; **no other crop linked anywhere** | 25001 to 25020 | **read in at most 1 of 20** | at most 1 of 20 |
| Leak and drift | The same, with a drying or wetting that speeds up and yields bending the same way in the same places | 25101 to 25110 | **at most 1 of 10** | not run |
| Leak and step | The same, with a climate that turns drier for good in patches and yields there dropping the same year | 25201 to 25210 | **at most 1 of 10** | not run |
| Nothing | No link in any crop | 25301 to 25310 | **at most 1 of 10** | not run |
| Link, 35% | Each other crop is rain-fed with chance a half, and where rain-fed is linked, at 35% of variance, wherever its country is: a fifth to a third of the scored records | 25401 to 25410 | **read in at least 8 of 10** | at least 8 of 10 |
| Weak link, 20% | The same at 20% | 25801 to 25810 | measured | not run |
| Link in few, 35% | 35%, each other crop rain-fed with chance a fifth: about a tenth of the scored records | 25501 to 25510 | measured | not run |
| Leak, full size | As Leak, six crops and forty-seven others | 25601 to 25605 | **at most 1 of 5** | not run |
| Link, full size | As Link, 35%, six and forty-seven | 25701 to 25705 | measured | not run |

**The leak panels are the null that matters.** The real cereals are linked, and they run beside the other crops; if their link could show up as a gain in crops that have none, this test would be worthless. So every no-link panel but one has the cereal-like crops linked.

**Why 35% and not 20% for the mark.** On smoke, a 20% link in a sixth of the scored records was not read (one seed), and 35% and 50% were (two seeds each). A mark set where the method is known to miss would only stop the test. The weak panel measures what happens at 20%. **So a silence on the real record would rule out only a strong link in a good share of the records,** and the measured panels say how strong.

**If a year-end mark misses, no real yield of these crops is set against drought** (`run_claims.py real once` refuses), and the result is a null about this method. If only a mid-year mark misses, the mid-year reading of the real record is reported as unmarked.

**Before step 2, an independent reader sees this rule, the code and the made-up results.** What it finds is applied and disclosed before any real yield of these crops is read.

## Result, step 1: the made-up records (2026-11-10)

`run_claims.py known`, all nine panels, 95 seeds, 62 shifts, run from 08:28 to 10:15 UTC; 120 rows in `results/crops-drought.jsonl`. **Every mark holds, year-end and mid-year.** Read means read at 1.5 standard errors, the level the verdict uses. S is the share of the baseline's squared error removed on the claims, with the driver as it fell.

| Panel | Seeds | Read, year-end | Mark | Read, mid-year | Mark | S on the claims, year-end: middle world (lowest to highest) |
|---|---|---|---|---|---|---|
| Leak | 20 | **0** | at most 1: holds | **0** | at most 1: holds | −0.18% (−0.76% to 0.55%) |
| Leak and drift | 10 | **0** | at most 1: holds | not run | | −0.12% (−0.35% to 0.58%) |
| Leak and step | 10 | **0** | at most 1: holds | not run | | −0.02% (−0.87% to 0.20%) |
| Nothing | 10 | **0** | at most 1: holds | not run | | −0.01% (−0.08% to 0.02%) |
| Link, 35% | 10 | **10** | at least 8: holds | **9** | at least 8: holds | 4.41% (2.50% to 5.74%); mid-year 3.68% (2.02% to 5.25%) |
| Weak link, 20% | 10 | 4 | measured | not run | | 1.20% (0.27% to 2.33%) |
| Link in few, 35% | 10 | 5 | measured | not run | | 1.83% (−1.40% to 3.76%) |
| Leak, full size | 5 | **0** | at most 1: holds | not run | | −0.00% (−0.06% to 0.08%) |
| Link, full size | 5 | 5 | measured | not run | | 3.04% (2.12% to 6.22%) |

At the two other levels, reported and deciding nothing: at 1.0 the counts are the same but for mid-year link, 10; at 2.0, link 9 and 8, few 4, weak 1, full size 5. No world without a link in the other crops was read at any level.

**What the no-link worlds show.**

- **The cereals beside do not make a gain in crops that have none.** In 45 year-end and 20 mid-year worlds where the six cereal-like crops are linked and no other crop is, with a drift, with a step, at the small size and at the real one, the claims gained nothing: the middle world lost a little (−0.09% year-end), the best gained 0.58%, and in no world, under either driver, at any level, was the interval above zero (the highest lower end, −0.11%).
- **The other-years controls alone would not have held that, and the interval did.** In those worlds the claims beat all 62 shifts in 3 of 45 year-end (2 of 45 with the flat driver, 1 of 45 with both) and in 3 of 20 mid-year (both drivers in 2), where a fair control would be beaten about once in 63. The likely reason, not yet checked: the linked crops beside give the term some size under the true alignment, and under another year's weather the shared weights fall to nearly nothing, so the shifts' scores sit close to zero while the true alignment's scatters more widely around a small loss. So "beats every shift" is a weaker condition here than it looks, and what kept every one of these worlds unread was the interval. The independent reader is asked to measure this.
- **With no link in any crop** the weights are nearly zero, the term is nearly nothing and S is within a tenth of a percent of zero.

**What the link worlds show.**

- **A 35% link in about a quarter of the scored records is read**: 15 of 15 year-end (small and real size), 9 of 10 mid-year. The one miss (seed 25405, mid-year) had S 2.39% and an interval from −0.20%; it failed on the interval alone.
- **The size it reads is 2.1% to 6.2% of squared error on the claims** (1.1% to 3.2% of a typical error); the word was "a usable aid" in 7 of the 15 year-end worlds and "a real but small aid" in 8. In those worlds the linked records, a sixth to two fifths of the scored, gained 3.5% to 7.7% over all their years; the records with no link lost 0.3% to 1.0%; between a half and four fifths of the claimed record-years were in linked records; the claims covered 11% to 20% of the squared error that could have been claimed. **So the number reported on a real record is smaller than the link in the records that carry it**, because a third or so of the claims are chance claims in records with none, and because the term is shrunk by weights shared with records that have no link.
- **A 20% link in about a quarter of the records is read in 4 of 10.** All ten beat all 62 shifts; the six misses failed on the interval alone (S 0.27% to 1.43%). Where read, "a real but small aid".
- **A 35% link in about a tenth of the records is read in 5 of 10.** Two of the ten worlds drew no rain-fed crop, so had no linked record at all, and were rightly not read (S −0.67% and −1.40%, beating none of the 62 shifts). Of the eight with any link (6% to 13% of records), five were read, at 1.8% to 3.8%; the three misses failed on the interval alone.
- **Read by a whisker** (lower end of the interval under 0.2%): year-end 25507 (0.14%), 25804 (0.06%), 25805 (0.03%), 25810 (0.12%); mid-year 25403 (0.08%).
- **Beside, deciding nothing: the claim hears a link in few records where the cereal test's pooled reading does not.** Over all scored records, as the cereals were read, the same worlds pass in 13 of 15 at 35% in a quarter, 2 of 10 at 20%, and 0 of 10 at 35% in a tenth.

**What a silence on the real record would rule out, and would not.** It would rule out a link taking 35% or more of the year-to-year departures in a quarter or more of these crops' records. It would not rule out 20% in a quarter (missed 6 times in 10), or 35% in a tenth (missed 3 times in 8). The real cereals, for comparison, gave 1.67% over all records and, in development, 6.3% on the claims.

**The guess** was that all year-end marks would hold, about 70%. They held.

## Step 2: the real record, once

`run_claims.py real once` (refuses a second run): year-end, then mid-year, both read before either is written. No fitting step comes before it.

## What each outcome would mean

- **Read, "a usable aid".** In the records where drought had gone with a crop's yield before, using it takes 5% or more off the squared error of the yield forecast (2.5% or more of a typical error), on years never fitted, on records not read before, against the same forecast with other years' weather. The first result here that is large enough to forecast with, for part of the record. It gets an independent reader before it is called a finding.
- **Read, "a real but small aid" or "too small to forecast with".** The rule carries to other crops; the gain is there and is small.
- **Not read.** A quiet null. Either the other crops carry too little of this link for the method to hear (what it can hear is on the measured panels), or the cereal pattern, a stable set of records where the term helps, does not carry beyond cereals.
- **A made-up mark misses.** A null about the method. The other crops stay unread against drought.

A pass would not show cause, would not be independent of the cereal result (same countries, same weather years, same statistics offices), and would say nothing about any one record: a claim is a rule for using the term, not a named link.

## Guesses, written now so they cannot be adjusted

- Made-up marks, year-end: all hold, about 70%. Most likely to miss: the 35% link at 8 of 10.
- The real record read, year-end: about 40%. Mid-year, given year-end: about 50%.
- If read, a size between 1.5% and 5%; "a usable aid", about one chance in eight overall.
- If read, most of the gain in under ten crops, with root crops, pulses and oil crops ahead of vegetables and fruit.

## What was tried while shaping the rule

All on the spent cereal record and on made-up records with smoke seeds 21940 to 21946 and 21990 to 21999, never counted. The reasons are in decision 0054.

1. **The claim from a record's own slope,** not from its past gain: more record-years at the same size.
2. **The cap of 1.** A cap of 2 gave a larger point size on the cereal record and an interval that at mid-year included zero.
3. **Dropped,** each for doing worse: one scale's forecast and not the weighted five; the scale that had done best for the record; the mean of the scales; weights fitted record by record; weights fitted crop by crop.
4. **The cereals beside.** On smoke, with the six linked and no other crop linked, running them beside gave no gain in the others; where others were linked, a little more with them than without. Those runs were made before the cap was fixed at 1.
5. **Condition 5,** below every baseline alone on the claims, was added to match the cereal test's fifth condition, not after a failure.
6. **The mark's link was raised from 20% to 35%** after the smoke runs above.

On smoke through this script, year-end, at 1.5 standard errors: 20% not read (S on the claims 0.6%, interval −0.4% to 1.6%); 35% read twice in two (6.8% and 5.3%; lower ends 3.2% and 2.7%); 50% read twice in two; leak not read, twice in two (−0.3% and −0.5%, each beating none of its shifts). About three quarters to four fifths of the claims at 35% fell in linked records. In the leak worlds, claims made by chance held about 5% of the squared error that could have been claimed.

## Limits, stated now

- **It hears strong links only.** A link taking 20% of a record's departures, in a sixth of the records, was not heard on smoke. The claim needs ten scored years and a slope that stands clear of zero, and the shared weights shrink the term when most records carry nothing.
- **Not independent of the cereals,** as said above; and the cereal record shaped the rule.
- **The made-up records are shaped on cereal yields.** Vegetables, fruit and fibre crops may be rougher, more often estimated, or reported differently. The other crops' yields were not examined to check.
- **The small made-up worlds have a larger share of cereal-like records** (more than four in ten) than the real record (about one in six). That is the harder case for a leak and flatters how well a link is heard; the two full-size panels are there for that.
- **Dilution.** Irrigated and tree crops are in because the count rule let them in. Choosing rain-fed field crops by hand would need knowledge the method is not given (decision 0054).
- **Claims by chance.** At 1.5 standard errors a record with no link claims now and then. What is tested is the forecast on all claims together.
- **A claim comes late.** Ten scored years are needed, so nothing is claimed before 1996, and a record whose link is new is missed.
- **Every limit of the cereal result applies:** a country mean and not cropland; official figures are not measurements and some may be made with weather; heat and El Niño not separated; the drought file carries an acknowledged error; the lead is short and partly notional.
- **The controls are 62 and not independent** of each other.
- **No person-level inference:** the unit is a country, a crop and a year.
