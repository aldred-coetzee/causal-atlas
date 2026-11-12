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

Not yet run.
