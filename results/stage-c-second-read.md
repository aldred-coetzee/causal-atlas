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

### The placebos and the known answer (all 40 runs in, 2026-11-12, 02:14 to 03:01 UTC)

Rows: `results/stage-c-second-read.jsonl`. Each registered seed once, in six processes whose seed lists did not overlap.

- **Places moved: 0 of 20 runs with any pass. The mark (at most 2) holds.** About 70,213 rows posted a run, forty sent, bar 3.71 in the middle run.
- **Years moved: 0 of 8 runs with any pass. The mark (at most 1) holds.** Bar 3.42 in the middle run.
- **Planted, 12 runs, 36 links of each size.** Heard from the board (sent by the steward and passed): **10 of 36 at a share of 0.35, 3 of 36 at 0.20, 1 of 36 at 0.10.** Passed when handed to the referee: 14, 8 and 4 of 36. Sent by the steward: 20, 12 and 3. The first read, of levels, heard 0 of 54 either way on this table. This is lower than on the made-up tables of the count (64% and 22% from the board), as the real table has more gaps and outcomes that seldom move.
- **Five planted runs had a pass that names no planted link exactly; each was looked at, and none is unexplained.** All five are on an outcome that had a link planted. Three name a row of several series gathered together that holds the planted input (`faostat_pe:lcu:year`, `faostat_pe:slc:year`, `spei:spei3:country_mean`). Two name a near copy of the planted input from its own set: `wdi:NE.CON.TOTL.ZS` where `wdi:NY.GDS.TOTL.ZS` was planted (consumption and saving, each as a share of the same total), and `wdi:SP.POP.0014.MA.IN` where `wdi:SP.POP.0014.TO` was planted (boys under fifteen, and all children under fifteen). So a pass on the real table may name a close relative of the series that carries a link, or a bundle holding it; that was to be read by hand in whatever passed.

### The real read (made once, 2026-11-12, 03:02 to 03:08 UTC): silence

**No row passed. No candidate, no lead.** The swarm posted 70,213 rows from the changes of 1962 to 1995; the steward sent forty; the referee scored them on 1996 to 2014 with a bar of 3.63 over the forty. None passed, so nothing is labelled, the check with the year's middle of the changes taken off had nothing to read, and **the last ten years are not opened**.

How far from passing. In 8 of the 40 rows something came off the baseline's error both ways the row was read; in 4 a score could not be worked out. The highest pair of scores on a row that applies widely was 1.69 and 1.66, under half the bar (a Scandinavian pressure pattern against the area harvested of one crop, in all places). One row stood above the bar one way, 4.31, and far below it the other, 1.27 (a Pacific and North American pressure pattern against one crop's production); it applies in two to four of the nineteen years and would have fallen on breadth as well. None of the forty names an exchange rate with a price or local-currency series, so the known answer of inflation did not take places on the board.

**What this silence is worth: something, for one kind of link, and not much more.** The planted runs are the measure. On this table, read this way, a steady link in which one series' change moves another's change a year later, in whole groups holding at least a quarter of the places, was heard from scratch about 3 times in 10 at a share of 0.35 of the outcome's year-to-year movement, under 1 in 10 at 0.20, and hardly at all at 0.10. So: had there been several such strong links between crops, exchange rates, the climate and drought series and the World Bank's indicators, one would probably have been heard, and none was; a single strong one would more likely than not have been missed; weaker ones would mostly have been missed. It says nothing about a link in which an input's level drives the outcome's movement (the first read's kind, where that read was deaf here), about links at other distances than one year, links inside one set, links in a few places, bursts, or links between months. It is not evidence that the sets are unrelated.

**Limits, beside those said beforehand.** One table, one arrangement of years (34 changes seen, 19 scored), one year ahead, yearly values. Forty rows of about 70,000: a link ranked forty-first was never scored, and in the planted runs the steward sent 20 of 36 strong links, so the board's ranking, not only the referee's bar, is where links are lost. These nineteen years have now been read twice. Nothing was changed in the finders, the steward or the referee after any run was seen.

Every row sent, in the order sent. A score or share of "none" could not be worked out.

| Outcome | Series named | Their sets | Finder | Places | Lift | Score, two ways | Share taken off the baseline's error, two ways (with its interval) | Groups, years it applies in | Passed |
|---|---|---|---|---|---|---|---|---|---|
| `wdi:TX.VAL.MRCH.OR.ZS` | `candidates:scand.data:monthly` | climate | slope: lag 1 | 66 | 6.50 | -0.73, -0.74 | -0.072 (-0.223 to 0.016); -0.071 (-0.217 to 0.015) | 7, 19 | no |
| `wdi:AG.PRD.CREL.MT` | `candidates:dmi.had.long.data:monthly` | climate | shape: hinge 0.2 | 161 | 7.09 | 0.08, 0.19 | -0.096 (-0.369 to 0.137); -0.118 (-0.579 to 0.193) | 16, 3 | no |
| `wdi:SE.PRM.DURS` | `faostat_qcl:production:358` | crops | extremes: tail 0.1 to event 0.1 | 79 | 28.53 | -3.77, -4.45 | -0.674 (none to -0.443); -0.621 (none to -0.452) | 3, 4 | no |
| `faostat_qcl:area_harvested:15` | `wdi:NE.CON.PRVT.KD`, `wdi:NE.CON.TOTL.CN` | world bank | pairs: pairs from the board | 52 | 7.49 | -0.36, -0.70 | -0.014 (-0.039 to 0.009); -0.013 (-0.036 to 0.008) | 6, 19 | no |
| `wdi:NY.GDP.MKTP.KD.ZG` | 94 series together | climate, crops, exchange rates | modes: components | 116 | 6.59 | none, none | none (none to none); none (none to none) | 0, 0 | no |
| `faostat_qcl:area_harvested:567` | `candidates:scand.data:monthly` | climate | slope: lag 1 | all | 5.33 | 1.69, 1.66 | 0.051 (-0.021 to 0.122); 0.050 (-0.019 to 0.122) | 14, 19 | no |
| `faostat_qcl:area_harvested:125` | `candidates:whwp.data:monthly`, `faostat_pe:lcu:year` | climate, exchange rates | shape: sign by state | 116 | 5.31 | -1.58, -1.53 | -0.084 (-0.179 to -0.009); -0.064 (-0.138 to -0.006) | 11, 19 | no |
| `wdi:EN.GHG.CH4.AG.MT.CE.AR5` | `candidates:tornado.us.mon.data:monthly` | climate | extremes: tail 0.1 to event 0.1 | 161 | 13.76 | -0.11, -0.18 | -1.530 (-8.372 to -0.189); -0.805 (-4.989 to 0.030) | 16, 5 | no |
| `faostat_qcl:yield:242` | `wdi:NE.RSB.GNFS.ZS`, `wdi:TX.VAL.MRCH.R3.ZS` | world bank | pairs: pairs from the board | 70 | 6.56 | 0.74, 0.52 | 0.004 (-0.012 to 0.018); 0.002 (-0.015 to 0.017) | 7, 19 | no |
| `wdi:NY.GDP.PCAP.KD.ZG` | 94 series together | climate, crops, exchange rates | modes: components | 116 | 5.65 | none, none | none (none to none); none (none to none) | 0, 0 | no |
| `wdi:DT.DOD.MWBG.CD` | `faostat_qcl:area_harvested:176` | crops | slope: lag 1 | all | 5.31 | 0.09, 0.17 | -0.007 (-0.032 to 0.013); -0.004 (-0.022 to 0.012) | 11, 19 | no |
| `wdi:NY.GDP.PCAP.KD.ZG` | `faostat_qcl:yield:388` | crops | shape: sign by place | 57 | 5.22 | 0.26, 0.18 | -0.102 (-0.210 to 0.003); -0.099 (-0.206 to -0.000) | 5, 19 | no |
| `faostat_qcl:area_harvested:156` | `wdi:EN.GHG.CO2.TR.MT.CE.AR5` | world bank | extremes: tail 0.9 to event 0.1 | 117 | 12.97 | 0.04, -0.05 | -0.255 (-1.168 to 0.027); -0.221 (-1.178 to 0.017) | 11, 16 | no |
| `wdi:TG.VAL.TOTL.GD.ZS` | `candidates:qbo.50mb.data:monthly`, `faostat_qcl:production:236` | climate, crops | pairs: pairs from the board | 92 | 5.06 | 1.19, 1.16 | 0.004 (-0.026 to 0.033); 0.006 (-0.019 to 0.030) | 9, 19 | no |
| `wdi:TM.VAL.MANF.ZS.UN` | 94 series together | climate, crops, exchange rates | modes: components | 53 | 5.17 | none, none | none (none to none); none (none to none) | 0, 0 | no |
| `wdi:SP.POP.GROW` | `faostat_qcl:production:490` | crops | slope: lag 1 | 118 | 4.91 | 1.41, 1.17 | 0.003 (-0.014 to 0.024); 0.002 (-0.016 to 0.023) | 11, 19 | no |
| `faostat_qcl:yield:403` | `candidates:tni.long.data:monthly`, `wdi:SP.POP.65UP.TO` | climate, world bank | shape: sign by state | 128 | 5.11 | 0.24, 0.15 | -0.019 (-0.074 to 0.033); -0.027 (-0.093 to 0.031) | 13, 19 | no |
| `faostat_qcl:area_harvested:560` | `wdi:NY.GDP.MKTP.KN` | world bank | extremes: tail 0.1 to event 0.1 | 60 | 11.78 | 0.01, 0.16 | -0.861 (-14.393 to -0.104); 0.018 (-7.933 to 0.243) | 4, 10 | no |
| `wdi:SP.DYN.LE00.FE.IN` | `candidates:dmi.had.long.data:monthly`, `candidates:noi.data:monthly` | climate | pairs: pairs from the board | all | 4.98 | -0.62, -0.70 | -0.104 (-0.225 to -0.003); -0.094 (-0.203 to -0.002) | 17, 19 | no |
| `wdi:NV.AGR.TOTL.KD.ZG` | 10 series together | climate, crops | modes: gathered 10 | 98 | 4.73 | 1.33, 1.20 | 0.035 (-0.080 to 0.124); 0.029 (-0.071 to 0.109) | 6, 19 | no |
| `wdi:NE.EXP.GNFS.ZS` | `faostat_qcl:yield:426` | crops | slope: lag 1 | 79 | 4.73 | 0.19, 0.32 | -0.030 (-0.079 to 0.011); -0.021 (-0.066 to 0.018) | 9, 19 | no |
| `faostat_qcl:production:122` | `candidates:pna.data:monthly` | climate | shape: hinge 0.8 | 135 | 5.02 | 4.31, 1.27 | 0.176 (-0.111 to 0.317); 0.065 (-0.056 to 0.206) | 13, 2 | no |
| `wdi:EN.GHG.CO2.WA.MT.CE.AR5` | `candidates:tsa.data:monthly` | climate | extremes: tail 0.1 to event 0.9 | 143 | 11.03 | 0.25, 1.76 | -1.276 (-3.176 to -0.441); -0.164 (-0.832 to 0.150) | 14, 1 | no |
| `faostat_qcl:production:44` | `wdi:EN.URB.MCTY.TL.ZS`, `wdi:TX.VAL.FOOD.ZS.UN` | world bank | pairs: pairs from the board | 67 | 4.91 | 0.37, 0.53 | -0.002 (-0.034 to 0.026); 0.001 (-0.025 to 0.025) | 7, 19 | no |
| `wdi:NY.GNP.MKTP.CN` | 94 series together | climate, crops, exchange rates | modes: components | 108 | 4.50 | none, none | none (none to none); none (none to none) | 0, 0 | no |
| `faostat_qcl:production:574` | `wdi:TX.VAL.MRCH.RS.ZS` | world bank | slope: lag 2 | 89 | 4.13 | 0.16, 0.09 | -0.029 (-0.069 to 0.010); -0.029 (-0.067 to 0.008) | 8, 19 | no |
| `wdi:NE.CON.TOTL.KN` | `candidates:ea.data:monthly` | climate | shape: hinge 0.2 | 152 | 4.97 | -1.91, -1.81 | -3.384 (-5.629 to -0.277); -3.740 (-6.648 to -0.271) | 15, 4 | no |
| `wdi:NY.GDP.FCST.CD` | `candidates:tna.data:monthly` | climate | extremes: tail 0.1 to event 0.1 | all | 11.02 | -0.92, -0.92 | -13.441 (-50.467 to -5.145); -13.441 (-50.467 to -5.145) | 17, 2 | no |
| `wdi:SP.POP.65UP.TO` | `faostat_qcl:area_harvested:44`, `faostat_qcl:production:372` | crops | pairs: pairs from the board | 89 | 4.70 | 0.64, 0.81 | -0.021 (-0.124 to 0.058); -0.002 (-0.095 to 0.067) | 11, 19 | no |
| `wdi:SP.POP.TOTL.MA.ZS` | 5 series together | climate | modes: gathered 5 | all | 3.84 | 0.99, 1.06 | -0.075 (-0.277 to 0.072); -0.063 (-0.248 to 0.074) | 17, 19 | no |
| `wdi:NV.SRV.TOTL.ZS` | `faostat_qcl:area_harvested:401` | crops | slope: lag 2 | 82 | 3.74 | -0.21, -0.01 | -0.042 (-0.121 to 0.022); -0.032 (-0.112 to 0.036) | 6, 19 | no |
| `wdi:NY.GDP.MKTP.KD.ZG` | `faostat_qcl:yield:388` | crops | shape: sign by place | 57 | 4.82 | 0.39, 0.33 | -0.092 (-0.192 to 0.016); -0.089 (-0.191 to 0.009) | 5, 19 | no |
| `wdi:NE.DAB.TOTL.CD` | `faostat_qcl:production:463` | crops | extremes: tail 0.1 to event 0.1 | 62 | 10.94 | -0.02, -0.08 | -0.592 (-8.580 to 0.069); -0.857 (-10.436 to 0.037) | 6, 13 | no |
| `wdi:SE.PRM.ENRL` | `candidates:ao.long.data:monthly`, `faostat_qcl:area_harvested:403` | climate, crops | pairs: pairs from the board | 117 | 4.64 | 0.14, 0.08 | -0.036 (-0.110 to 0.013); -0.028 (-0.091 to 0.017) | 12, 19 | no |
| `wdi:SP.POP.TOTL.FE.ZS` | 5 series together | climate | modes: gathered 5 | all | 3.84 | 0.99, 1.06 | -0.075 (-0.277 to 0.072); -0.063 (-0.248 to 0.074) | 17, 19 | no |
| `wdi:AG.PRD.CREL.MT` | `candidates:nao_gib.long.data:monthly` | climate | slope: lag 1 | 117 | 3.71 | 1.44, 1.46 | 0.037 (-0.055 to 0.129); 0.040 (-0.051 to 0.132) | 11, 19 | no |
| `wdi:SP.POP.65UP.TO` | `faostat_qcl:area_harvested:619` | crops | shape: hinge 0.2 | 134 | 4.66 | 0.63, 0.76 | 0.009 (-0.823 to 0.241); 0.039 (-0.794 to 0.284) | 14, 19 | no |
| `wdi:SE.SEC.DURS` | `faostat_qcl:production:567` | crops | extremes: tail 0.1 to event 0.1 | 92 | 10.77 | 0.03, -32.32 | -0.000 (none to 0.019); -1.022 (none to -0.744) | 3, 6 | no |
| `faostat_qcl:area_harvested:401` | `wdi:DT.ODA.ODAT.GN.ZS`, `wdi:NE.GDI.FTOT.CD` | world bank | pairs: pairs from the board | 68 | 4.34 | 0.14, -0.09 | -0.023 (-0.068 to 0.026); -0.035 (-0.093 to 0.012) | 6, 19 | no |
| `faostat_qcl:yield:176` | 5 series together | climate, world bank | modes: gathered 5 | 84 | 3.73 | -1.16, -1.23 | -0.081 (-0.175 to -0.019); -0.080 (-0.169 to -0.023) | 7, 19 | no |

### The last ten years

Not opened: nothing passed. 2015 to 2024 of this panel stay unread, for a later rule. `confirm once` is not to be run.

## Deviations

None from the rule as it stood after the reader. The 40 placebo and planted runs were made in six processes at once; the real read alone.
