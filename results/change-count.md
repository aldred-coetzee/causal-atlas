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
