# The read of changes counted on made-up tables, beside the read of levels: the rule

Committed 2026-11-12 before any counted number (rule 9). The first real read was silent, and on made-up tables shaped like the real yearly panel the read as counted heard no planted link, because an outcome that keeps its level already holds most of what a link adds (`docs/reading/series-that-keep-their-level.md`; development numbers on smoke seeds). The way proposed there is counted here: the same table with every series written as its change from the year before, read by the same finders and referee. Run by `scripts/run_change.py`; rows kept in `results/change-count.jsonl`.

## What is read

Each table is read twice, each read on its own with its own bar:

- **levels**: the table as it is, by the finders (all members but `pairs`), the steward and the referee as counted, labels on;
- **changes**: every series, outcomes and inputs alike, as its value less its value the year before in the same place (missing where either is missing), then the same finders, steward and referee, nothing in them changed.

The finders see years 0 to 53; the first scored year is 35; the referee's draws are seeded with the table's seed. Both as `scripts/lab_levels.py` `way` and `pipeline` have them at this commit.

## Tables

Made by `scripts/lab_level_worlds.py` (numpy only; shares nothing with the finders or the referee) at its defaults: 166 places in 18 groups, 64 years, 120 series, about a third of values missing, each series' memory between 0.58 and 0.97.

| panel | what is in it | tables | seeds |
|---|---|---|---|
| nothing | nothing predicts | 100 | 63001 to 63100 |
| path_1 | six shared slow paths, each moving a pair of series, no link | 50 | 63201 to 63250 |
| path_2 | the same at twice the size | 50 | 63301 to 63350 |
| links | nine links a table added as the first real read's planted runs added them, three each at shares 0.35, 0.20 and 0.10, each in a quarter of the places | 60 | 63401 to 63460 |
| earlier | the made-up tables of the finders' count (`synth/table_panel.py`, kind `steady`, share 0.35, 120 places, 60 years, 40 series), whose links enter what the outcome's history leaves | 40 | 63501 to 63540 |

A seed the maker refuses makes no table, is written down and is not replaced. No seed of 63001 to 63999 has been used for anything.

## Heard, and a false pass

A planted link is **heard** by a read when a row that read passed names the link's outcome and exactly its input. In the first three panels every pass is false, whatever its label and whether or not it names a shared path's own pair. In `links` a pass is **other** when it names neither a planted input of its outcome nor anything with one.

## Marks

A missed mark is reported as missed.

- **Where nothing predicts** (200 tables): tables with any pass by the read of changes, **at most 16** (a rate of 5% a table gives 10, with two spreads of room). Tables with any pass by either read, **at most 20**: a tenth is the most this session would take to the real table for the two reads together.
- **Heard by the read of changes** in `links` (180 links a share): **at least 50%** at share 0.35 and **at least 18%** at 0.20. Share 0.10 is reported and has no mark.
- **Passes naming nothing planted** by the read of changes in `links`: in **at most 6** of 60 tables.

Reported beside, with no mark: every figure for the read of levels and for either read; each heard share with a 90% interval by tables drawn again; where nothing predicts, how many of the tables with a pass had every pass labelled "together"; and the `earlier` panel, which is there to count what the read of changes loses on links the read of levels hears.

## Not covered

- Links where an input's level drives the outcome's new movement on the tables of 120 series: that path of the maker gave nothing to any read in its one development run and is not understood. The `earlier` panel stands in for it at 40 series.
- Monthly tables, late starts, series tied to one another by construction, the real table's 461 series, memory above 0.97.
- One family of made-up tables; the real table differs in ways none of this measures.
- The harness has had no review but its authors'.

## What follows

If the marks hold, the read of changes goes to the real yearly table as a second read beside the first, under a rule of its own committed first, with the placebo and planted runs redone on the changed table. If a mark is missed it does not.

## Result

Counted once, 2026-11-12, 00:17 to 01:49 UTC, six processes of one thread. 300 tables, each read both ways; 600 rows in `results/change-count.jsonl`; no seed refused. **Every mark holds.**

| mark | limit | counted |
|---|---|---|
| where nothing predicts, tables with any pass by the read of changes | at most 16 of 200 | **2** (1.0%) |
| where nothing predicts, tables with any pass by either read | at most 20 of 200 | **2** |
| links heard by the read of changes, share 0.35 | at least 50% | **116 of 180, 64%** (59% to 70%) |
| links heard by the read of changes, share 0.20 | at least 18% | **40 of 180, 22%** (17% to 28%) |
| `links` tables with a pass by the read of changes naming nothing planted | at most 6 of 60 | **0** |

Beside the marks:

- **Where nothing predicts, by panel**, tables with any pass, levels and changes: `nothing` 0 and 0 of 100; `path_1` 0 and 1 of 50; `path_2` 0 and 1 of 50. The two false passes: seed 63216, a row of one series at lag 1 that is not a path's pair (t 3.47 and 3.34 over a bar of 2.83); seed 63310, a path's own pair, an extreme of one to an extreme of the other (t 3.53 and 8.34 over a bar of 2.27). **Neither carries the "together" label**, so the label would have stopped neither.
- **Share 0.10**: the read of changes heard 6 of 180 (3%, 1% to 6%). A link of that size is out of reach on such a table.
- **The read of levels heard 0 of 540 links** in `links`, at every share, and passed nothing in any of the 200 tables where nothing predicts. So on these tables "either read" is the read of changes.
- **`earlier`** (links that enter what the outcome's history leaves, 40 series, share 0.35): levels heard 118 of 120 (98%), changes 92 of 120 (77%, 72% to 82%), either 120 of 120. The read of changes loses about a fifth of what the read of levels hears there and found the two it missed.
- In `earlier` the table printed by the runner shows passes "naming nothing planted" in 12 tables by levels and 10 by changes. **That figure is the harness's and is not a count of false passes**: the harness does not know a near copy, which the counted runner of the finders' count does (`scripts/run_finders.py` `stands`: a named series that goes with a planted input at 0.5 or more). Those tables were read again as a check, with nothing kept: all 27 such passes (16 and 11) are on an outcome with a planted link and name one series that goes with the link's input at 0.95 or 0.96. A near copy predicts and was counted beside, not as false, in the finders' count; the same holds here. No mark rested on it.

## What it means, and what it does not

- On made-up tables shaped like the real yearly panel, reading every series as its change from the year before hears about two thirds of strong links and a fifth of middling ones where the read of levels hears none, with a false pass in about one table in a hundred where nothing predicts.
- The interval on 2 of 200 runs from about 0.2% to 3%. It is one family of made-up tables. On the real table the placebo runs say what the rate is there, and they come first.
- The read of changes is deaf to small links (share 0.10) and loses some links of the other kind. It is a second read beside the read of levels.
- Not covered stays as listed above: the level-driven kind at 120 series, monthly tables, late starts, tied series, 461 series, memory above 0.97.

**So the read of changes goes to the real yearly table as a second read, under a rule of its own committed first.**
