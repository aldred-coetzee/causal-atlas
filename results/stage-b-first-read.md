# The first read across the real table: between separate data sets, by country and year

**Outcome: not yet read.**

Rule first, committed before any real series is set beside another (rule 9). Stage B of `docs/plan-finders-and-referee.md`. Authority: decisions 0040, 0055 to 0057, 0059 to 0063. Code: `src/causal_atlas/finders.py`, `src/causal_atlas/referee.py` (unchanged since the label's count), `scripts/run_stage_b.py`. Seeds: `results/seed-ledger.md`. Rows: `results/stage-b-first-read.jsonl`. What has been read against what: `results/spent-ledger.md`.

## What is asked

The owner's aim is to find relationships between many separate data sets, without a hypothesis, that help say what comes next. This is the first time the finders and the referee are let loose on the real table. One question:

**Among the series held by country and year, does anything in one data set help predict a series in another a year or two ahead, beyond that series' own history, on years no finder saw, and again on years nobody has opened?**

Nothing is named beforehand. The swarm proposes from the early years; the referee scores the later years once; what passes is read a last time on the newest ten years.

## What has been looked at

Each series alone: its length, gaps, memory and coverage (`docs/table-first-count.md`), and the coverage counts this rule's panel is cut by. No real series has been set beside another in this table. The pairs read in earlier tests are in the spent ledger and are named below.

## The panel, cut by count and not by hand

- **Years:** 1961 to 2024, sixty-four.
- **Series by country and year** as the table holds them, each with the table's own transform (log, log of one plus, or none).
- **Climate by month made yearly:** the mean of a year's months where at least ten have a value; for counts (sunspots, tornadoes) the sum of twelve months, then the transform. The country drought index (SPEI-3) differs by place; El Niño and the 25 other climate series are the same for every place.
- **A place counts for a series** if it has at least 25 values in 1961 to 1995, 15 in 1996 to 2014 and 8 in 2015 to 2024. Where it does not, that series is missing in that place.
- **Series kept:** at least 60 places count. **Places kept:** those that count for at least a third of the kept series that differ by place. Then series are counted again over the kept places, and need 60.
- Not in this read because they start too late for these years: violence (1989), burned area (1982 to 2018), local food prices (2007), consumer prices by month (2000). They wait for a read with a later split.
- **Groups of places:** Natural Earth's subregions. A subregion with fewer than five kept places is pooled with the other such subregions of its UN region; if that is still under five it joins the smallest subregion of that region that has five.

Counted before this rule, each series alone: about 437 series pass the first count (World Bank 340, crops 94 before the recount, exchange rates 2, drought 1) in about 166 places. The exact numbers are written here when the panel is built and before any read.

## Four data sets, and what a row may name

| Set | Series |
|---|---|
| Crops | FAO's yields, areas and production (`faostat_qcl`) |
| World Bank | the development indicators (`wdi`) |
| Exchange rates | FAO's yearly rates (`faostat_pe`) |
| Climate | drought by country; El Niño and the 25 other climate series |

**A row may name only series outside its outcome's set.** The aim is relationships between separate data sets, and series inside one set are tied by how they are made (area, yield and production of a crop; the World Bank's demographic figures from one model). Every series that differs by place is an outcome in turn.

World Bank series whose source the Bank gives as the Food and Agriculture Organization are FAO's figures passed on. A pass between one of those and a crops series is read as a near copy and said so, never as a result. Which those are is read from the Bank's series file when the result is written.

## Shared movements in the baseline

Every series that differs by place is read as its **departure from that year's middle** (the median over the kept places with a value; a year with fewer than thirty is missing). So what the world did that year is in every baseline before a finder or the referee sees a number, and no row can pass on a movement all places share. The series common to all places are kept as they are.

What this costs, said beforehand: what is predicted is a place's standing against the world's middle that year, not its raw value; and a link through something that moves every place alike is not there to be found between two series that differ by place.

## The finders, as run here

The swarm of decision 0062 as counted in Stage A2, with three changes forced by a table of this width (decision 0063):

1. **The member that tries every pair is not run.** At about 400 series it would hold some 80,000 products. Pairs among the series the single-series members put forward, read from the board, are still tried.
2. **A member posts only rows that name series outside the outcome's set.** The search at the other alignments is cut the same way, so the lift means what it meant.
3. **The pairs-from-the-board member builds only the products it needs.** The same numbers as before.

The finders see 1961 to 1995 and nothing later: thirty-five years, the same as in every count, with the same twenty other alignments. The steward is unchanged: at most forty rows from the whole board, a floor of three on lift, eight a family by turn, then by agreement.

## The referee, and the years

Unchanged. It is given 1961 to 2014 and scores **1996 to 2014**, nineteen years, each forecast from the years before it. **One bar over all forty rows and all outcomes**, at the same rate: where nothing predicts, any pass at all in about one run in twenty. Every pass carries the label of decision 0061.

**2015 to 2024 is not given to the finders or the referee** in any step below until the last.

## Placebos first, on the real series with the links broken

The made-up tables are not the real table. Before the real read, the whole pipeline, as it will run, is put on the real series arranged so that nothing in one set can predict anything in another. Two ways of breaking the links, because each leaves something different standing:

**Places moved round (20 runs, seeds 58001 to 58020).** The crops, the exchange rates and the drought index each get their own random reordering of the places; the World Bank's series stay where they are; the series common to all places are moved round in time by 10 to 54 years. Every series keeps its own years, trend, roughness and gaps, and what the world did in a year still falls in that year. What is broken is which place goes with which.

**Years moved round (8 runs, seeds 58101 to 58108).** Each set is moved round in time by its own number of years (after the departure from the middle is taken), the World Bank's by none, any two sets at least ten years apart. Every place stays where it is, with its neighbours, in both the inputs and the outcome. What is broken is which year goes with which; each moved series has one seam.

**Marks.** Runs with any pass, labelled or not: **at most 2 of 20** with places moved round, **at most 1 of 8** with years moved round. (At a true rate of one in twenty, three or more of 20 happens about 8 times in 100, two or more of 8 about 6 times in 100.) What these runs can and cannot see: a false-pass rate of a half is caught nearly always (19 times in 20 by the first, 24 in 25 by the second); a rate of one in five slips past the first about one time in five and the second about one time in two. The last ten years are the second guard. **If either mark is missed, the real read does not happen under this rule.** What passed falsely is reported, and a new rule is needed.

What neither placebo covers: a shock that hits one region in one year in both sets. That is a real joint movement, and whether it leads or only moves together is what the label says.

## The known answer on the real table (6 runs, seeds 58201 to 58206)

A silence means nothing unless a link of known size would have been heard. On six more tables with places moved round, nine links are planted in each: an outcome and an input from another set, both drawn at random, a steady link one year ahead, in whole groups drawn at random until they hold a quarter of the places. Three at about 35%, three at 20% and three at 10% of the outcome's year-to-year movement there. The harness plants them; the finders and the referee are told nothing.

Reported, with no mark: of 18 links a size, how many were heard from the board alone (a sent row naming that input for that outcome passed), how many when the answer was handed over, and the size the referee gave them. This is what a silence in the real read rules out, and nothing smaller is ruled out.

## The real read, once

If both marks hold: the swarm on 1961 to 1995, the steward's forty rows, the referee on 1996 to 2014. Once; the script will not do it a second time.

Reported for every row sent: its outcome, the series it names, their sets, its form and places, its lift, its score both ways with the interval, whether it passed, and its label.

## The last ten years

Each row that passed is then read alone on **2015 to 2024**, by the same referee given all sixty-four years, each of those years forecast from the years before it. It is **confirmed** if, both ways it is read, it stands above the bar for one row and takes something off the baseline's error, in at least five groups and five of the ten years. (The referee's own rule of ten scored years cannot be asked of ten years when many series end in 2022 or 2023.) Read once.

## What counts as what

- **A lead between separate data sets:** passed, not labelled, confirmed.
- **Moving together:** passed and labelled. A lead is not shown.
- **Passed, not confirmed:** said so; not a result.
- **A known answer:** the country's drought index against a crop's yield was read in two earlier tests (cereals, and 47 other crops, 1986 to 2024). Such a row is reported as a known answer, never as new.
- **A near copy:** as above.
- **Silence:** no lead. Reported quietly with what the known-answer runs say it rules out.

A pass says a series helps predict. It does not say that changing it would change the outcome.

## What is already spent or seen

- Drought against crop yields: spent, as above.
- Crop yields 1986 to 2024, cereals and others: scored once each against drought only. This session has seen how those years behave for that driver, and nothing of them against anything else. The last ten years are therefore untouched for every pair except drought and yields.
- The World Bank's series and the exchange rates: never read against anything.
- El Niño and the other climate series: read against drought and burned area by grid cell and month, never against a crop or a World Bank series by country and year. A pass from one of them to drought by country would be inside one set and cannot be sent.

The spent ledger is updated in the same commit as each step that reads the real table: the placebos, the known-answer runs, the real read, the last ten years.

## What is expected, said beforehand

On made-up tables links were heard at 20% to 35% of what own history leaves, in a quarter of places. The real links measured in this project so far were a few per cent. By country and year there are about 166 places, fewer than any made-up table that heard most kinds. So silence is a likely outcome, and it would rule out only links of the size the known-answer runs hear. The strongest forty rows of a table this wide may also be links any economist or agronomist would call obvious; they are reported as they fall.

## Limits, said beforehand

- Country and year only. One and two years ahead only. Links inside the year are not proposed.
- Standing against the world's middle, not raw values.
- Forty rows of a board of tens of thousands: a first read, not a census.
- A term gathered from many series speaks only where every one of them has a value, so on a table with gaps the modes family says little. Many weak series together are barely tested here.
- Many World Bank figures are estimates or gap-filled without a flag, and are revised between releases.
- The placebos do not cover a regional shock common to two sets.
- No person-level inference: countries and years only.

## Before the referee's years are opened

- A rehearsal on made-up tables (smoke seeds only) of the swarm as it runs here, with sets given to the series and the departure from the middle taken: development, no marks.
- An independent reader, with no part in this work, reads this rule and the code before the real read: can anything from 1996 on reach the board; are the placebos fair; does the last step give a second look. Brief in `docs/specs/`, committed before it starts.

## Deviations

None yet.

## Result

Not yet read.
