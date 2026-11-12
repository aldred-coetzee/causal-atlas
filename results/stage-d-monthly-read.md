# The first read across the real table by month

**The rule.** Written 2026-11-12 with `scripts/run_stage_d.py` and `tests/test_stage_d.py`, and committed before any placebo, planted run or real read on the monthly panel. Decision 0069. Nothing in it was chosen after seeing a number that sets one real monthly series beside another. What was looked at before it was written: each series' own coverage (how many places and months it has), which is how the panel is built.

## Why this read

The two reads of the yearly table were silent. The monthly method could not be used on real data until now because it called same-month ties leads; that was fixed and counted on made-up tables (`results/monthly-lead-count.md`, decision 0068): with a lead defined as a pass that is not labelled as moving together, no same-month tie was called a lead in 120 tables, tables where nothing predicts gave no lead in 180, steady links were heard 97% to 98% of the time down to a share of 0.04 with gaps and late starts, and no lead named anything unplanted. The monthly table has ten to twelve times the points of the yearly one. This is the first time real monthly series from separate data sets are set beside each other.

## What is read

- **The panel.** Country by month, January 1980 to December 2024 (540 months), from the one table (`data/table/`), built by a count rule with no choice by hand (`run_stage_d.py panel`):
  - every monthly series, with the table's own transform (log, log of one plus, or none);
  - a series common to all places is copied to every place;
  - a source that writes no row for a month with no event (the conflict events record, watched worldwide from 1989) is nought in such a month from 1989-01 to 2025-12: an assumption taken from the source's stated global coverage;
  - a place **counts** for a series if it has at least 96 valued months in 1980 to 2008, at least 108 of the 132 months of 2009 to 2019, and at least 48 of the 60 months of 2020 to 2024;
  - a series that differs by place is kept if it counts in at least 40 places lying in at least 8 groups of places; a common series is kept if it meets all three counts;
  - a place is kept if it counts for at least half of the kept series that differ by place (half, not the yearly read's third: five series are nought-filled everywhere, so a third would keep every territory);
  - groups of places are Natural Earth's subregions, one smaller than five places pooled within its UN region;
  - each series that differs by place is held as its departure from that month's middle (median) across places, where at least 30 places have a value.
  - **What this gives:** 106 series, 202 places, 18 groups. 92 series are common to all places (64 commodity prices, 27 climate indices, world earthquakes). 14 differ by place and are the outcomes: exchange rates (three series), consumer prices (four), births, storms, drought, conflict deaths and events, earthquakes (count and energy).
  - **What the count rule leaves out, said now:** protests (the record ends 2020-03) and burned area (ends 2018) cannot be confirmed on 2020 to 2024 and fall out; so do dengue, electricity generation, local market food prices and every Europe-only series (too few places, too few groups, or too late a start). A later read with an earlier split, or with European groups, would be a new rule.
- **Sets.** A row may name only series from another set than its outcome's. Sets are by source: prices and money (commodity prices, consumer prices, exchange rates, policy rates, local food prices); climate (every climate index, drought, storms, burned area); earthquakes; conflict and protest; health and people; energy and activity; asylum. Every tie in `docs/tied-series.md` between monthly series lies inside one set, so no further list of tied pairs is needed.
- **Months.** The finders see 1980-01 to 2008-12. The referee is given the months before 2020 and scores 2009-01 to 2019-12 (132 months; a row must apply in at least 120 of them and in at least five groups, the monthly settings as counted). **2020 to 2024 are not opened** unless a row passes, and then once.
- **The read** is `causal_atlas.months` as counted on made-up tables (season taken out, the month members, the steward's forty rows, the referee drawing whole years, labels on), **less two members the table is too wide for**: the one that tries every pair, as in the yearly reads, and the one that tries every series against which side of its own past each common series stood (92 common series here make some ten thousand terms; a rehearsal on a made-up table of the panel's shape ran out of memory on it). The counted read had both; the planted runs below measure this read as it is. A sign that turns with a common series' state is therefore not looked for. A rehearsal on a made-up table of this shape with nothing linked (smoke seed 60911) took 143 seconds, posted 3,948 rows, sent 2 and passed none.

## What is already known, said before it starts

- The yearly reads set yearly forms of some of these series beside each other on 1996 to 2014 (drought, exchange rates, climate indices) and were silent, with every row published. Nothing in this rule was chosen from those rows. The monthly values of 2009 to 2019 have not been set beside each other.
- `results/spent-ledger.md` was consulted. Burned area against drought and El Niño, the harvest and crop records, and the local market food prices are spent or reserved there; none of those series is in this panel.
- **Known answers, named now.** A passed row of one of these kinds is reported as a known answer, not as a discovery: drought or a climate index leading food prices or food price inflation; conflict leading the exchange rate or prices, or the reverse; a commodity price (oil, food) leading conflict; an El Niño index leading conflict (a published and disputed claim).
- **Impossible leads, a built-in check.** No series outside the climate set can lead a place's drought or storms, and nothing here can lead its earthquakes. A lead whose outcome is drought, storms or earthquakes is counted as a **false lead** and reported as such, in the real read as in the placebos. (After the reader: counted apart as **implausible** and read by hand; see below.)

## Steps, in this order, each registered seed once

Seeds are from a fresh block, 66001 to 66999, entered in `results/seed-ledger.md` with this rule. A run's seed draws its rearrangement, its links and the referee's draws.

1. **Places moved (20 runs, seeds 66001 to 66020).** Every set but prices and money has its series that differ by place given one reordering of the places, its own. Each set's common series (prices and money's too) are moved round by that set's own whole number of years within the months before 2020, any two sets at least four years apart and each at least four years from where it was. **Mark: at most 2 of 20 runs with any lead.**
2. **Years moved (8 runs, seeds 66101 to 66108).** Every set but prices and money is moved round, whole, by its own whole number of years within the months before 2020, at least four years apart as above. **Mark: at most 1 of 8 runs with any lead.**
3. **Planted (12 runs, seeds 66201 to 66212).** Places moved as in step 1; then six links a table, two each at shares 0.20, 0.10 and 0.04 of the outcome's month-to-month movement: an outcome and an input from another set, both differing by place, the input one to six months before, in whole groups of places until the places where both series move are a quarter of all and lie in five groups. No mark: these runs are the measure of what a silence would rule out. Reported by size: links sent, heard as a lead from the board, a lead when handed to the referee; runs with a lead naming nothing planted.
4. **The real read, once (referee's draws: seed 66900).** Refused by the script unless both marks hold and all twelve planted runs are in; a marker made with an exclusive create stops a second start.
5. **2020 to 2024, once (seed 66901), only if a row passed.** Each passed row is sent again, alone, to the referee given every month with January 2020 as the first scored month, labels off. **Confirmed:** above the bar for one row and something off the baseline's error, both ways the row is read, in at least five groups and at least 36 months.

Time is moved by whole years so that a month stays in its season, and within the months before 2020 only. A test holds that nothing of 2020 to 2024 reaches the months read in any rearrangement or planted table (`tests/test_stage_d.py`). No confirmation is run on a placebo or planted table.

**If a mark is missed** the real read is not made under this rule. The miss is reported with its rows and the cause looked for on made-up tables.

## What counts as what

- **A candidate lead:** passed in the real read and not labelled as moving together. Not a result. Reported with its scores; 2020 to 2024 are opened for it.
- **A lead between separate data sets:** a candidate confirmed on 2020 to 2024. It says one series helps predict another some months ahead beyond the outcome's own history, season and neighbours, in the places named. Reported with its size and interval, the places and months it applies in, and every limit below. It does not say that changing the input would change the outcome.
- **Moving together:** passed and labelled. A lead is not shown. Reported apart.
- **A known answer, a false lead:** as named above; and whatever passes is read by hand against the sources' own descriptions for a near copy.
- **Silence:** no row passed. Reported quietly beside what the planted runs heard, and worth only what they heard.

## Limits known beforehand

- **The month's middle.** Holding a series as its departure from the month's middle puts a move of the middle place into every place that month. Reordering places does not break that part; only the years-moved placebo does. A pass carried by it would be a relation between months, not between places. For series that are mostly nought the middle is nought and nothing is taken off.
- **Counts that are mostly nought** (conflict, storms, earthquakes in most places): a row on them can score far above the bar in a few places by dividing by almost nothing. The breadth conditions (five groups, 120 months) are what stop it. The placebos show whether they do here.
- **Fourteen outcomes, seven of them prices and money**, which cannot be named for each other. So what can be heard is mostly: climate, conflict and earthquakes against prices and exchange rates, and the reverse; and conflict against climate. Commodity prices can be named only for outcomes outside prices and money.
- **The planted links run between series that differ by place.** A link from a common series (an index, a commodity price) to places is not planted, so a silence says less about those.
- **The confirmation months hold the pandemic.** A true lead may fail there, and a row on prices may pass there for the wrong reason. How often a false pass would also be confirmed is not known.
- **Placebo marks bound the false-lead rate only loosely** (about one in ten), and do not cover a shock common to two sets in one region. The untouched months are the second guard.
- Conflict counts depend on reporting; consumer price and exchange rate series are partly filled by their makers. Whatever passes is read against the source's description before it is called anything.
- One table, one arrangement, forty rows of a much larger board, eighteen groups.
- No person-level inference: countries and months only.

## Before any run

An independent reader, with no part in the work, reads this rule and the code before the first placebo (`docs/specs/2026-11-12-stage-d-rule-check.md`). It runs nothing on the real table and reads no real values. What it finds is settled, and written below, before step 1.

## After the reader, before any run

The reader's report is `docs/reviews/2026-11-12-stage-d-rule-check/report.md` (its own write was refused by the box, so the project session saved its text unchanged; its check script is beside it). It ran nothing on the real table. It found that nothing of 2020 to 2024 can reach a run, the rearrangements, the hearing test, the nought-filling, the sets and the guards sound. Settled on its findings, before step 1:

1. **A lead on drought, storms or earthquakes is now counted apart by the code**, in every placebo step and in the real read (a test holds the sets). It is called **implausible**, not false: the reader is right that the claim is about causes, not prediction (markets price El Niño forecasts; oil prices can come before induced earthquakes). Each one is read by hand. In a placebo it still counts toward the mark as any lead does.
2. **The panel is pinned.** Every kept run records the checksum of the panel file it read; every step refuses if the file is not the one the kept runs read; `panel` refuses to build again once a run is kept (a test holds it). The checksum begins 979b3c82c75354cb.
3. **Planted links are reported apart for outcomes that are counts, mostly nought** (conflict, storms, earthquakes). There a planted link is nearly all of the outcome's movement in its quiet months, so hearing it says little about real links into counts. What a silence rules out is read from the links into outcomes that are not counts.
4. **Said, and left as they are:** the stated share is of raw month-to-month movement, season included, while the read takes the season out, so for seasonal outcomes (births, storms) a link's real size differs from its label. The places placebo and the planted runs scramble each place's neighbours in every set but prices and money, so the neighbour part of the baseline is weaker there than in the real read. Where the groups run out a planted link covers fewer than a quarter of the places (births have about 40). The 97% to 98% heard on made-up tables was on tables of 16 series, not of this panel's shape, and with two members this read leaves out; only the planted runs here say what this read hears.
5. **A true lead can be labelled as moving together and so not count.** The reader saw it on a made-up table. The planted runs report, beside leads, how many planted links passed when handed over; the gap between the two is what the label costs, and a silence is read with it.
6. **Confirmation scores five years** that hold the pandemic, against a bar of about 2 for one row. It is weak evidence either way, and how often a false pass would be confirmed is not known. That sentence goes beside any confirmation reported.
7. **Not checked by the reader, said:** the builder against the real files; what the two left-out members cost on a table of this shape; whether six planted links in one table disturb each other. The builder decides which places and series are kept by whether values are present in each stretch, 2020 to 2024 included, never by what they are.

## The spent ledger

`results/spent-ledger.md` takes a row with the placebo and planted runs and a row with the real read, each in the commit that reports it.

## Result

### Steps 1 to 3: the placebos and the planted links (2026-11-12, 05:07 to 06:13 UTC)

Forty runs, each registered seed once, every one on the panel whose checksum begins 979b3c82c75354cb. Rows: `results/stage-d-monthly-read.jsonl`. The runner's table:

```
places: 20 of 20 runs, 0 with any lead (at most 2): holds; with any pass 0; leads on drought, storms or earthquakes 0 of 0 leads
   rows posted, middle 3948; sent, middle 4; bar, middle 2.35; seconds, middle 156
years: 8 of 8 runs, 0 with any lead (at most 1): holds; with any pass 0; leads on drought, storms or earthquakes 0 of 0 leads
   rows posted, middle 3948; sent, middle 6; bar, middle 2.64; seconds, middle 161
planted: 12 of 12 runs
   20%, outcome not a count: 14 links; sent 14; heard as a lead from the board 9; a lead when handed over 11 (a pass 11); places, middle 52; rank on its outcome's board, middle 0 (0 not posted)
   20%, outcome a count, mostly nought: 10 links; sent 9; heard as a lead from the board 4; a lead when handed over 1 (a pass 4); places, middle 54; rank on its outcome's board, middle 0 (0 not posted)
   10%, outcome not a count: 15 links; sent 12; heard as a lead from the board 7; a lead when handed over 7 (a pass 7); places, middle 51; rank on its outcome's board, middle 0 (0 not posted)
   10%, outcome a count, mostly nought: 9 links; sent 6; heard as a lead from the board 3; a lead when handed over 4 (a pass 5); places, middle 38; rank on its outcome's board, middle 1 (0 not posted)
   4%, outcome not a count: 14 links; sent 10; heard as a lead from the board 4; a lead when handed over 7 (a pass 7); places, middle 51; rank on its outcome's board, middle 0 (0 not posted)
   4%, outcome a count, mostly nought: 10 links; sent 7; heard as a lead from the board 1; a lead when handed over 1 (a pass 3); places, middle 47; rank on its outcome's board, middle 2 (0 not posted)
   runs with a lead that names no planted link: 9
```

**Both placebo marks hold, with nothing to spare needed.** With places moved round, no run of 20 had a lead, or any pass at all (the mark allowed 2). With whole years moved round, none of 8 (the mark allowed 1). So on this table, with every real link across sets broken, the read named nothing.

**What the read hears on this table.** Links whose outcome is not a count, heard as a lead from the whole board: 9 of 14 at a share of 20% of the outcome's month-to-month movement, 7 of 15 at 10%, 4 of 14 at 4%. Into outcomes that are counts and mostly nought (conflict, storms, earthquakes): 4 of 10, 3 of 9, 1 of 10. So a silence in the real read would rule out most strong steady leads into prices, exchange rates, births and drought, about half of the middling ones, and little of the weak ones or of anything into the counts. That is far more than the yearly reads could hear (10, 3 and 1 of 36).

**What the label costs.** Handed over directly, every planted link into an outcome that is not a count that passed was also called a lead (11 of 11, 7 of 7, 7 of 7). Into counts, 4 of 12 passes were called leads; the rest were labelled as moving together. So the label throws away true leads into counts, and not elsewhere.

**Leads that name no planted link: 9 of 12 runs, and what they are** (a look after the runs, not in the rule). The 52 leads across the twelve runs: 33 name the planted input on the planted outcome; 18 are on the planted outcome and name the planted input's sibling from the same source (earthquake moment for earthquake count, conflict events for conflict deaths, the food price index for food price inflation); 1 is a gathered row on a planted outcome. **None is on an outcome with no planted link.** So a real lead says which outcome and which source; it does not say which series of that source.

**Deviation, disclosed.** Four planted runs (66203, 66206, 66209, 66212) were cut off by the session's time limit before they finished, kept nothing, and were started again with the same seeds; each seed has one kept row. Planted runs take about four minutes, not two and a half.

**Next:** step 4, the real read, once.

### Step 4: the real read, made once (2026-11-12, 06:14 to 06:17 UTC): silence

Seed 66900, the same panel file. The finders posted 3,948 rows from 1980 to 2008; eleven were sent to the referee, which scored them on 2009 to 2019 against a bar of 3.13. **None passed.** There is no lead, so nothing is called implausible, **step 5 is not run and 2020 to 2024 stay unopened.** Every row sent (the two numbers after `t` are the two reads; a pass needs both over the bar):

```
real: 3948 rows posted, 11 sent, bar 3.13, 0 passed, 0 of them leads, 0 of those on drought, storms or earthquakes (implausible)
        ['candidates:noi.data:monthly', 'oni:oni:nino34_3month'] (climate) -> bis_eer:real_broad: pairs from the board, product, places 73, lift 4.23, t [-0.68, -0.69], s [-0.0238, -0.0274], moving together None
        13 (climate, conflict and protest, earthquakes, prices and money) -> hfd_stff:births: components, mode, places 81, lift 4.02, t [1.39, -0.49], s [0.0203, -0.0037], moving together None
        ['pink_sheet:copper:world', 'pink_sheet:wheat_us_srw:world'] (prices and money) -> spei:spei3:country_mean: pairs from the board, product, places 58, lift 4.14, t [0.46, 0.58], s [-0.0013, 0.0004], moving together None
        5 (prices and money) -> ibtracs:storms:country_total: gathered 5, mode, places 160, lift 4.02, t [6.87, 0.45], s [0.2916, -0.0081], moving together None
        ['pink_sheet:gold:world', 'pink_sheet:wheat_us_srw:world'] (prices and money) -> spei:spei3:country_mean: pairs from the board, product, places 58, lift 3.23, t [0.54, 0.68], s [-0.0031, 0.0002], moving together None
        20 (prices and money) -> ibtracs:storms:country_total: gathered 20, mode, places 160, lift 3.64, t [6.09, -0.09], s [0.2586, -0.1208], moving together None
        ['pink_sheet:coal_australian:world', 'pink_sheet:gold:world'] (prices and money) -> spei:spei3:country_mean: pairs from the board, product, places 54, lift 3.22, t [0.68, 0.56], s [-0.001, 0.0005], moving together None
        10 (prices and money) -> ibtracs:storms:country_total: gathered 10, mode, places 160, lift 3.59, t [6.91, 0.2], s [0.2899, -0.0908], moving together None
        ['candidates:tni.long.data:monthly', 'hfd_stff:births'] (climate, health and people) -> faostat_cp:food_price_inflation: pairs from the board, product, places 76, lift 3.12, t [-1.15, 0.24], s [-0.0078, -0.0029], moving together None
        12 (conflict and protest, earthquakes, health and people, prices and money) -> ibtracs:storms:country_total: components, mode, places 40, lift 3.19, t [None, None], s [nan, nan], moving together None
        ['pink_sheet:gold:world', 'pink_sheet:soybean_meal:world'] (prices and money) -> spei:spei3:country_mean: pairs from the board, product, places 61, lift 3.04, t [0.56, 0.63], s [-0.0035, -0.0011], moving together None
```

**What the silence is worth.** By the planted runs above: a steady lead of one to six months from a series of one source to an outcome of another, in at least a quarter of the places, holding from 1980 through 2019, would probably have been heard if strong (about two in three at a fifth of the outcome's monthly movement), about half the time if middling, about a quarter if weak; into prices, exchange rates, births and drought. Into conflict, storm and earthquake counts little would have been heard, so the silence says little there.

**What it does not say.** Nothing of links inside one source's set (they were not allowed). Nothing of links that hold in a few places, that switch on and off, that started after 2008 or run longer than the finders look. Nothing of protests, fire, dengue, electricity or the European series, which the count rule left out. Nothing of the two finder members left out for memory. The neighbours' part of the baseline was weaker in the placebos than here.

**The nearest rows, said and not counted.** Three rows have gathered commodity prices ahead of storm counts with one read far over the bar (6.1 to 6.9) and the other near nought (-0.09 to 0.45). A pass needs both, the outcome is one where a lead would be called implausible, and commodity prices and storm counts both have strong shared swings in 2009 to 2019. It is not a result and is not followed up outside a rule.

**Spent.** 2009 to 2019 of this panel are now read once in the real arrangement, across sets. `run_stage_d.py real once` must never be run again or forced, its marker file never removed, and `confirm once` is not to be run.
