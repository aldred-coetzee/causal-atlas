# Briefs for two helpers, the sixth wave

Written by the project session before either is started (rule 7). The first wave is `docs/specs/2026-11-11-parallel-helpers.md`; **its section "What every helper is held to" binds each helper here**, and so does its last section on what the project session checks. With G2 still out these make three at once.

## H. The monthly read made ready for a count (build; about 400,000 fresh tokens, stops and reports at 700,000)

**The decision it serves.** `docs/reading/reading-by-month.md` recommends reading monthly series with the season taken out first and settings counted in months, and gives the change the package would need as an unapplied patch (`data/panel/monthly/monthly-read.patch` in the main checkout). Before a count is registered the change has to exist, be shown to leave every yearly counted result as it is, and fit this box.

**To do, in a separate working copy on a branch, committed there and not pushed; the project session reads the diff and decides:**
1. Apply the patch. `referee.py` and `finders.py` may gain only optional arguments whose default is the counted path; nothing counted may change. Show it: the tests the patch brings, the whole test suite, and registered made-up worlds re-read to their stored rows exactly (say which and how many).
2. Find why one linked world at 120 places by 600 months peaked at 5.3 GB, and bring a monthly read under 2 GB a process, without changing any result.
3. Settle from the code, and say plainly, whether the ridge setting and the baselines' minimum past need counting in months.
4. Draft, as a file not committed to `results/`, the rule for a monthly count on made-up tables: worlds, marks, seeds (a fresh block is named by the project session, not the helper), runtime. No counted seed is used; smoke seeds 60943 to 60999 only, each listed.

Made-up tables only; nothing real is read. `synth/` and `scripts/run_stage_b.py` are not edited.

## I. Tied series among the new sources (listing from descriptions; mechanical; about 150,000 fresh tokens, stops at 250,000)

**The decision it serves.** Before any read across the table, series that are the same thing, or made from one another, must be barred from being set beside each other, or a read reports an identity as a discovery.

**To do:** from the series' descriptions in `data/table/series.parquet` (names, units, sources: metadata only) and the helpers' notes `docs/reading/sources-*.md`, write `docs/tied-series.md`: every pair or group among the 126 new series, and between them and the held ones, that is one quantity twice, a sum and its parts, an index and its components, a rate and the level it is made from, or one source republished by another. Each with its reason in a line and the series ids. Known candidates to check, not a full list: BIS credit totals and parts; BIS exchange rates against FAOSTAT's; consumer price indices in BIS, FAOSTAT and the World Bank; the four fertility series; fertility-database births against Eurostat births; UNHCR against the World Bank's refugee series and Eurostat asylum; Ember against the World Bank's and Eurostat's electricity; the commodity file's averages and indices against their parts; held food prices against the commodity file's maize, rice and wheat.

**No value of any series is read and no number relating one series to another is computed**: the listing is from descriptions and the sources' own documentation only. Where a tie cannot be told from descriptions, say so; do not test it on the data.
