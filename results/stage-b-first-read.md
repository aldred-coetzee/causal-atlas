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

Counted before this rule, each series alone: about 437 series pass the first count (World Bank 340, crops 94 before the recount, exchange rates 2, drought 1) in about 166 places. The exact numbers are below, under "Made exact", written when the panel was built and before any read.

## Four data sets, and what a row may name

| Set | Series |
|---|---|
| Crops | FAO's yields, areas and production (`faostat_qcl`) |
| World Bank | the development indicators (`wdi`) |
| Exchange rates | FAO's yearly rates (`faostat_pe`) |
| Climate | drought by country; El Niño and the 25 other climate series |

**A row may name only series outside its outcome's set.** The aim is relationships between separate data sets, and series inside one set are tied by how they are made (area, yield and production of a crop; the World Bank's demographic figures from one model). Every series that differs by place is an outcome in turn.

**And not a World Bank series made from another set's figures, with that set** (decision 0064, before any run). World Bank series whose source the Bank gives as the Food and Agriculture Organization are FAO's figures passed on: a row may not name one of them with a crops series. World Bank series that are an exchange rate, or a value turned into dollars at the year's rate ("current US$" or "LCU per US$" in the Bank's name for the series), may not be named with an exchange-rate series. As first written such rows were let through and only called near copies afterwards, and the second kind was not named at all; with forty rows sent under one bar they could have taken the places of everything else. The counts are under "Made exact". **Seven more, after the independent reader and before any run** (decision 0065): the Bank's figures for greenhouse gases from agriculture are worked out from FAO's crop and animal figures, so the three agricultural series, the methane and nitrous oxide totals and the two all-gas totals may not be named with a crops series either.

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

**Places moved round (20 runs, seeds 58001 to 58020).** The crops, the exchange rates and the drought index each get their own random reordering of the places; the World Bank's series stay where they are; the series common to all places are moved round in time, within 1961 to 2014, by 10 to 44 years (made exact before any run, see below). Every series keeps its own years, trend, roughness and gaps, and what the world did in a year still falls in that year. What is broken is which place goes with which.

**Years moved round (8 runs, seeds 58101 to 58108).** Each set is moved round in time, within 1961 to 2014, by its own number of years (after the departure from the middle is taken), the World Bank's by none, any two sets at least ten years apart. Every place stays where it is, with its neighbours, in both the inputs and the outcome. What is broken is which year goes with which; each moved series has one seam.

**Marks.** Runs with any pass, labelled or not: **at most 2 of 20** with places moved round, **at most 1 of 8** with years moved round. (At a true rate of one in twenty, three or more of 20 happens about 8 times in 100, two or more of 8 about 6 times in 100.) What these runs can and cannot see: a false-pass rate of a half is caught nearly always (19 times in 20 by the first, 24 in 25 by the second); a rate of one in five slips past the first about one time in five and the second about one time in two. Holding both marks therefore does not show the rate is one in twenty: a rate of one in ten or a little more would usually hold them too. And the runs are rearrangements of one table, not separate tables, so they count for fewer than their number. The last ten years are the second guard. **If either mark is missed, the real read does not happen under this rule.** What passed falsely is reported, and a new rule is needed.

What neither placebo covers: a shock that hits one region in one year in both sets. That is a real joint movement, and whether it leads or only moves together is what the label says.

## The known answer on the real table (6 runs, seeds 58201 to 58206)

A silence means nothing unless a link of known size would have been heard. On six more tables with places moved round, nine links are planted in each: an outcome and an input from another set, both drawn at random, a steady link one year ahead, in whole groups drawn at random until they hold a quarter of the places and number at least five. Three at about 35%, three at 20% and three at 10% of the outcome's year-to-year movement there. The harness plants them; the finders and the referee are told nothing.

What these runs do not say, noted after the independent reader and before any run. The share is of the outcome's movement from one year to the next, with the input scaled by its own year-to-year movement: it is not the made-up tables' share of what own history leaves, and the two are not set beside each other. For an input that keeps its level for years the same share is a much larger effect on the outcome's level, so each link is reported with how far its input's one year goes with the next, and the heard counts are given apart for inputs with long and short memory. No link is planted from a series common to all places, the kind the known answer (drought) is nearest to. And the planted tables have places moved round, so less else stands on the board than on the real table: a link heard here could still be crowded out of the forty rows there.

Reported, with no mark: of 18 links a size, how many were heard from the board alone (a sent row naming that input for that outcome passed), how many when the answer was handed over, and the size the referee gave them. This is what a silence in the real read rules out at most, and nothing smaller is ruled out.

## The real read, once

If both marks hold and all six planted runs are in: the swarm on 1961 to 1995, the steward's forty rows, the referee on 1996 to 2014. Once; the script will not do it a second time.

Reported for every row sent: its outcome, the series it names, their sets, its form and places, its lift, its score both ways with the interval, whether it passed, and its label.

## The last ten years

Each row that passed is then read alone on **2015 to 2024**, by the same referee given all sixty-four years, each of those years forecast from the years before it. It is **confirmed** if, both ways it is read, it stands above the bar for one row and takes something off the baseline's error, in at least five groups and five of the ten years. (The referee's own rule of ten scored years cannot be asked of ten years when many series end in 2022 or 2023.) Read once.

## What counts as what

- **A lead between separate data sets:** passed, not labelled, confirmed.
- **Moving together:** passed and labelled. A lead is not shown.
- **Passed, not confirmed:** said so; not a result.
- **A known answer:** the country's drought index against a crop's yield was read in two earlier tests (cereals, and 47 other crops, 1986 to 2024). Such a row is reported as a known answer, never as new.
- **A near copy:** a passed row whose series are one figure under two names in a way the rule above did not catch. Looked for by hand in whatever passes, with the Bank's own description of the series, and said so; never a result.
- **Silence:** no lead. Reported quietly with what the known-answer runs say it rules out.

A pass says a series helps predict. It does not say that changing it would change the outcome.

## What is already spent or seen

- Drought against crop yields: spent, as above.
- Crop yields 1986 to 2024, cereals and others: scored once each against drought only. This session has seen how those years behave for that driver, and nothing of them against anything else. The last ten years are therefore untouched for every pair except drought and yields.
- The World Bank's series and the exchange rates: never read against anything.
- El Niño and the other climate series: read against drought and burned area by grid cell and month, never against a crop or a World Bank series by country and year. A pass from one of them to drought by country would be inside one set and cannot be sent.

The spent ledger is updated in the same commit as each step that reads the real table: the placebos, the known-answer runs, the real read, the last ten years.

## What is expected, said beforehand

On made-up tables links were heard at 20% to 35% of what own history leaves, in a quarter of places (a different measure of size from the planted runs' here, and not to be read across). The real links measured in this project so far were a few per cent. By country and year there are about 166 places, fewer than any made-up table that heard most kinds. So silence is a likely outcome, and it would rule out only links of the size the known-answer runs hear. The strongest forty rows of a table this wide may also be links any economist or agronomist would call obvious; they are reported as they fall.

## Limits, said beforehand

- Country and year only. One and two years ahead only. Links inside the year are not proposed.
- Standing against the world's middle, not raw values.
- Forty rows of a board of tens of thousands: a first read, not a census.
- A term gathered from many series speaks only where every one of them has a value, so on a table with gaps the modes family says little. Many weak series together are barely tested here.
- Many World Bank figures are estimates or gap-filled without a flag, and are revised between releases. A figure filled in or revised with later years in hand can carry something of those years into an earlier one; that cannot be checked from here, and a lead from such a series is weaker evidence for it.
- The sorting under "What counts as what" is done by hand from the rows the script lists; the script does not do it.
- The placebos do not cover a regional shock common to two sets.
- No person-level inference: countries and years only.

## Before the referee's years are opened

- A rehearsal on made-up tables (smoke seeds only) of the swarm as it runs here, with sets given to the series and the departure from the middle taken: development, no marks.
- An independent reader, with no part in this work, reads this rule and the code before the real read: can anything from 1996 on reach the board; are the placebos fair; does the last step give a second look. Brief in `docs/specs/`, committed before it starts.

## Made exact when the code was written, before any run

Written with `scripts/run_stage_b.py` and before any placebo, planted run or real read. Nothing here was chosen after seeing a number that sets one real series beside another.

**The panel, by the count rule** (`run_stage_b.py panel`; each series alone): **461 series in 166 places**, 64 years. World Bank 341, crops 91, exchange rates 2, drought by country 1: 435 series that differ by place, each an outcome in turn. Common to all places: El Niño and the 25 other climate series, 26. A series that differs by place has between 60 and 166 places, middle 99; about a third of its place-years (34.5%) are missing. 3,025,236 values: 1,609,813 in 1961 to 1995, 930,744 in 1996 to 2014, 484,679 in 2015 to 2024.

**Seventeen groups of places:** Caribbean 14, Central America 11, Eastern Africa 16, Eastern Asia 7, Melanesia 5, Middle Africa 9, Northern Africa 6, Northern Europe 8, Oceania other 6 (pooled), South America 12, South-Eastern Asia 11, Southern Africa 5, Southern Asia 9, Southern Europe 10, Western Africa 16, Western Asia 14, Western Europe 7. The made-up tables had groups of five places, 24 to 96 of them; these are fewer and larger, and the referee's bar draws groups again, so it is wider here.

**Ties between sets a row may not name** (read from the Bank's list of its series, `WDISeries.csv`, each series alone). Of the 341 World Bank series, 22 give the Food and Agriculture Organization as source (land, fertiliser, cereal yield and production, the production indices, fisheries, fresh water, population density) and 7 are emissions from agriculture or totals they are a large part of (decision 0065), and these 29 may not be named with any of the 91 crops series; 54 are a rate or in current dollars (52 "current US$", 2 "LCU per US$") and may not be named with either exchange-rate series. That is 2,747 of the 43,613 pairs of series in different sets (2,110 before the seven were added). Series in constant dollars, in local currency or as a share are left in. The planted links draw their inputs under the same rule.

**Years are moved round within 1961 to 2014 only.** The rule as first written moved the common series "by 10 to 54 years", which over sixty-four years would have carried values of 2015 to 2024 into the years the finders and the referee see. Nothing of the last ten years enters a placebo or a planted run: the common series move by 10 to 44 years of the fifty-four, and in the years-moved placebo the sets stand at least ten years apart round the fifty-four.

**Planted links.** Nine distinct outcomes a table, drawn among the series that differ by place; each input drawn among the series that differ by place in another set and not among the nine. Whole groups are drawn until they hold at least a quarter of the places and number at least five, because the referee passes no row that applies in fewer than five groups. The link adds to the outcome a multiple of the input the year before, sized place by place so that the year-to-year changes of what is added are the stated share (35%, 20%, 10%) of the outcome's year-to-year movement there afterwards; spreads are taken over 1961 to 2014. The answer handed over is the plain line on that input one year before, in those places. Beside each link: the input's year-to-year memory, whether a row naming it alone for that outcome was sent, and where it stood on its outcome's board.

**Seeds.** A placebo or planted run's seed draws its rearrangement, its links and the referee's draws. The real read's referee draws are seed 58900; the last ten years', 58901.

**After the independent reader, before any run** (`docs/reviews/2026-11-11-stage-b-rule-check/report.md`; decision 0065). The reader ran nothing on the real table. Changed on its findings: seven more tied series, as above; a gathered row could have named a series it may not, or the outcome itself, when a series that may be named has no standing for that outcome, and now cannot (a test holds it; the counted boards are unchanged); the script's refusals can no longer be switched off; the placebo marks count registered seeds, each kept once, where they counted rows; the real read also waits for the six planted runs; and what the marks and the planted runs do not say is written under each. Left as they are, with the reason: the marks themselves (more runs would say more, at about 25 minutes each; the last ten years are the second guard); the size of a planted link (stated as it is made, not changed); no link planted from a common series (the plan plants between series that differ by place; said as a limit).

## Deviations

None yet.

## Result

Not yet read.
