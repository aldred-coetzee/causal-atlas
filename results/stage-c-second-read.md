# The second read across the real table: the yearly panel read as changes

**The rule.** Written 2026-11-12 with `scripts/run_stage_c.py` and `tests/test_stage_c.py`, and committed before any placebo, planted run or real read on the changed table. Decision 0067. Nothing in it was chosen after seeing a number that sets one real series beside another as changes.

## Why a second read

The first read (`results/stage-b-first-read.md`) was silent, and its own planted runs said why that silence rules out little: on this table none of 54 planted links was heard, even handed to the referee. The cause was found on made-up tables shaped like this one (`docs/reading/series-that-keep-their-level.md`): where an outcome keeps its level from year to year, its own past takes about three quarters of what a link adds, and what is left sits under the bar. Read with every series as its change from the year before, such links are heard. That way was then counted once on 300 made-up tables under marks set first (`results/change-count.md`), and every mark held: a pass on 2 of 200 tables where nothing predicts; planted links heard 116 of 180 at a share of 0.35 and 40 of 180 at 0.20, where the read of levels heard none of 540; no pass naming anything unplanted. It is deaf to a link in which an input's level drives the outcome's new movement, which the read of levels hears best; so it is a second read beside the first, not in its place.

## What is read

- **The table.** The first read's panel, the same file (`data/panel/stage-b/panel.npz`: 461 series, 166 places, 1961 to 2024, built by the count rule of the first read), with **every series, outcomes and inputs alike, as its value less its value the year before in the same place**: missing where either year is missing, and in 1961. Nothing else is changed: the same seventeen groups of places, the same outcomes (every series that differs by place), the same swarm less the member that tries every pair, the same steward (forty rows), the same referee, labels on.
- **Ties.** A row may name only series of another set than its outcome's, less the tied pairs of the first read (decisions 0064 and 0065), unchanged. `docs/tied-series.md` lists ties among series brought into the table since; none of those series is in this panel. A change does not untie a tie and does not make one between sets that the level did not have.
- **Years.** The finders see the changes of 1962 to 1995. The referee is given the years before 2015 and scores 1996 to 2014. The change scored for 1996 is the value of 1996 less that of 1995. **2015 to 2024 are not opened** unless a row passes, and then once, by `confirm once`. The change of 2015 uses the value of 2014 and is among the last ten.

## What is already known, said before it starts

- **1996 to 2014 of this panel have been read once, as levels**: forty rows, none passed, each row's scores published. They were also seen 34 times in rearranged form. So these years are not untouched. What was learned there and could bear on this read: bars of about 3.5 to 5.2; that a row applying in one group or one year can stand above the bar and falls only on breadth; which outcomes the board ranked highest as levels.
- **Nothing in this rule was chosen from those rows.** The choice to read changes came from the planted runs' deafness and from made-up tables. The finders, the steward, the referee, the years, the ties and the rule for the last ten years are as they were. The change is one line of arithmetic with no setting (but see "After the reader" on what the year's middle does to it).
- **Two reads of the same years raise the chance that something passes by chance.** On the made-up tables a pass by either read where nothing predicts came on 2 of 200 tables; the real table is not those tables, and its placebo marks (below) cannot show a rate under about one in ten. For that reason a pass in this read is a **candidate** and nothing more until the last ten years confirm it.

## Steps, in this order, each registered seed once

Seeds are from a fresh block, 64001 to 64999, entered in `results/seed-ledger.md` with this rule. A run's seed draws its rearrangement, its links and the referee's draws.

1. **Places moved (20 runs, seeds 64001 to 64020).** Crops, exchange rates and the drought index each take their own reordering of the places; every series is then changed; the series common to all places are then moved round by 10 to 44 years within the years before 2015. **Mark: at most 2 of 20 runs with any pass.**
2. **Years moved (8 runs, seeds 64101 to 64108).** Every series is changed; each set but the World Bank's is then moved round by its own number of years within the years before 2015, any two sets at least ten years apart. **Mark: at most 1 of 8 runs with any pass.**
3. **Planted (12 runs, seeds 64201 to 64212).** Places moved as in step 1; nine links planted as in the first read, **in the values as they stand, before the change** (three each at shares 0.35, 0.20 and 0.10 of the outcome's year-to-year movement, an input from another set, in whole groups holding at least a quarter of the places); then changed, then the common series moved. This is how links were planted in the count on made-up tables. No mark: these runs are the measure of what a silence would rule out. Reported: links heard from the board, and passed when handed over, by size; runs with a pass naming nothing planted.
4. **The real read, once (referee's draws: seed 64900).** Refused by the script unless both marks hold and all twelve planted runs are in, and refused a second time.
5. **The last ten years, once (seed 64901), only if a row passed.** Each passed row is sent again, alone, to the referee given every year with 2015 as the first scored year, on the changed table, labels off. **Confirmed** as in the first read: above the bar for one row and something off the baseline's error, both ways the row is read, in at least five groups and at least five years.

Years are moved round **after** the change, so that no change is taken across the seam where a moved series wraps, and within the years before 2015 only. A test holds that nothing of 2015 to 2024 reaches the years read in any rearrangement (`tests/test_stage_c.py`).

**If a mark is missed** the real read is not made under this rule. The miss is reported with its rows, and the cause looked for on made-up tables, as with the monthly count.

## What counts as what

As in the first read's rule, with this added:

- **A candidate:** passed in the real read, not labelled as moving together. Not a result. It is reported as a candidate with its scores, and the last ten years are opened for it.
- **A lead between separate data sets, in changes:** a candidate confirmed on 2015 to 2024. It says that one series' change helps predict another's change a year ahead beyond the outcome's own history, season and neighbours, in the places named. It is reported with its size and interval, the places and years it applies in, and every limit below. It does not say that changing the input would change the outcome.
- **Moving together:** passed and labelled. A lead is not shown.
- **A near copy, a known answer:** as in the first read; looked for by hand in whatever passes, with the source's own description of the series.
- **Silence:** no row passed. Reported quietly beside what the planted runs of step 3 heard. The first read's silence covers no kind of link (it heard none of its planted links), so only this read's planted runs give a silence any weight, and only for a change leading a change at the sizes they hear.

## Limits known beforehand

- The read of changes is deaf to a link in which an input's level moves the outcome's new movement (counted: 77% heard against the level read's 98% on the earlier made-up kind; none in G2's harder case).
- A series that seldom moves (a rule in force, a count that is mostly nought) is mostly nought as changes; a row on it can score far above the bar in one group or year by dividing by almost nothing. The breadth condition is what stops such a row, as in the first read's placebos.
- A missing year costs two changes. About a third of place-years are missing as levels; more are as changes.
- One table, one arrangement of years, one year ahead, yearly values, forty rows of a board of tens of thousands. Seventeen large groups, so the bar is wide.
- The placebos do not cover a regional shock common to two sets, and bound the false-pass rate only loosely.
- Many World Bank series are estimates smoothed or filled in by their makers; a change of such a series is partly the maker's model. Whatever passes is read against the source's description before it is called anything.
- No person-level inference: countries and years only.

## Before any run

An independent reader, with no part in the work, reads this rule and the code before the first placebo (`docs/specs/2026-11-12-stage-c-rule-check.md`). It runs nothing on the real table and reads no real values. What it finds is settled, and written under "After the reader" below, before step 1.

## After the reader, before any run

The reader's report is `docs/reviews/2026-11-12-stage-c-rule-check/report.md` (its own write was refused by the box, so the project session saved its text unchanged; its check script is beside it). It ran nothing on the real table. It found no way for the last ten years to reach a run, the rearrangements and the bookkeeping sound, and `confirm` right. Settled on its findings, before step 1:

1. **A year-wide move sits in every place's change, and the rule now says so.** The panel holds each series that differs by place as its departure from the year's middle; the change of that is the place's change less the change of the middle, so a move of the middle place, or places entering and leaving, is carried into every place that year. The count on made-up tables used the same arithmetic and its marks were met with it; the arithmetic is kept so the read is the one counted. But: the places-moved placebo does not break this part (reordering places leaves a year's middle where it was); only the years-moved placebo does. And a pass carried by it would be a relation between years over nineteen points, not a lead in the places named. So **each passed row is read once more, in the same command, on the changed table with the year's middle of the changes taken off, against the real read's own bar** (`recentred`; a test holds it). A candidate that does not stay above the bar both ways there is reported as **a year-wide move, not a lead in the places named**, and is not called a lead even if confirmed. This is a check beside the pass, fixed here before any number; it is not a second read and adds no pass.
2. **A step run once cannot be started twice.** The real read and the last ten years each make a marker with an exclusive create before they start (a test holds it). Placebo and planted seeds are given to processes in lists that do not overlap.
3. **Inflation is a known answer, named now.** As changes, the two exchange-rate series, the World Bank's series in current local currency and its price series (consumer prices, the deflator) are largely inflation, which persists from year to year. A passed row that names an exchange-rate series with one of those, either way round, is reported as a known answer, never as a lead. The first read's ties stay as they were, so such rows may take some of the forty places. A redenomination is one very large change in the local-currency rate; the referee clips it, and it widens that place's spread afterwards.
4. **The silence paragraph** claimed more than stands behind it and is corrected above.
5. **How often a false pass would also be confirmed is not known** for the read of changes. (For levels, the first read's reader found the confirmation rule met by chance in 0 of 80 tries on made-up tables.) The change of 2015 uses the value of 2014, a year read twice.
6. **Smaller things, left as they are and said:** where a planted link's input is missing nothing is added that year, which as a change is a jump in the outcome; it makes links harder to hear, as it did in the count, so a silence is undersold. The planted table's split by the input's memory is of levels, not changes. A confirmed row's label from the real read is printed beside it.

## The spent ledger

`results/spent-ledger.md` takes a row with the placebo and planted runs and a row with the real read, each in the commit that reports it. After this read, 1996 to 2014 of this panel will have been read twice, once each way; 2015 to 2024 stay unopened unless a row passes.

## Result

Not yet run.
