# Brief for a helper: the World Bank's development indicators into the one table

Written by the project session before the helper was started. Estimated cost stated beforehand: about 300,000 fresh tokens; the helper stops and reports at about 450,000 by its own estimate, finished or not. Plan: `docs/plan-finders-and-referee.md`, section "The data in one shape". The owner's words for why: "many, many data sets across which we find unexpected correlations for prediction" and "collecting the data and making it consumable and comparable".

## Why this source

The table (`data/table/`, built by `scripts/build_table.py` from adapters in `src/causal_atlas/table.py`; brief `docs/specs/2026-11-10-data-in-one-shape.md`) holds 510 series, nearly all crops, with climate, fire, conflict and prices. It holds nothing on the economy, health, population, energy, trade or schooling. The World Development Indicators are country by year from 1960, in one bulk file, the same shape as the table.

## What to do, in this order

1. **Confirm at source before fetching (rule 4).** Open the World Bank's own pages and confirm: the bulk file's address (expected `https://databank.worldbank.org/data/download/WDI_CSV.zip`), that it needs no account or key, and the licence terms (expected CC BY 4.0 for the data set, with a licence column per indicator in the series file). Quote the licence sentence briefly with its address. If any of the three is not as expected, stop and report.
2. **Fetch script** `scripts/fetch_wdi.py`, in the manner of `scripts/fetch_faostat.py` and `scripts/_download.py`: download to `data/raw/wdi/`, record size and SHA-256. No email address and no identifying header goes to the server.
3. **Manifest and sources page, in the same change:** an entry `[wdi]` in `data/manifest.toml` (source address, licence, date fetched, checksum, coverage, known biases: figures are revised between releases, many are modelled or gap-filled estimates by the Bank or UN agencies, coverage is thin before 1990 for many indicators and for poor countries, and a new release replaces the old file at the same address) and a section in `docs/data-sources.md` in the style of the sections there, with the attribution the licence asks for.
4. **Adapter** in `src/causal_atlas/table.py`, wired into `scripts/build_table.py` as the others are, giving rows for `series` and `obs`:
   - Countries only: drop the file's regional and income aggregates. Map ISO3 codes to the table's `place_id` (UN M49, three-digit text) the way the prices adapter does; codes with no match are set aside and counted in `data/table/notes.json`.
   - **Which indicators, by a count rule and not by hand:** every indicator whose licence in the series file is CC BY 4.0 and for which at least 100 countries each have at least 30 yearly values. State the number kept and dropped by each condition.
   - `series_id` as `wdi:<indicator code>`; `domain` from the first part of the file's topic for the indicator, in short lower-case words (economy, health, population, energy, environment, education, trade, finance, infrastructure, poverty, public sector, social; say what you chose for any that do not fit); `measures` the indicator's name; `unit` from the name where it is given in brackets; `kind` and `transform` by a rule you state (the table's convention: `log` for quantities that cannot be negative and span orders of magnitude, `none` for shares, rates, indices and anything that can be negative); `place_level` country, `period` year; `flag` empty.
5. **Rebuild the table** and extend `scripts/count_table.py` and `docs/table-first-count.md` with the new source: each series alone, by domain: how many series, how many places, first and last year, how many values, share missing inside each series' span, the middle of each domain's year-to-year memory.
6. **Tests** in `tests/test_table.py` on a tiny made-up file the test writes itself: the adapter gives the rows expected, aggregates are dropped, the count rule is applied, a second build gives identical tables. Run the table's tests and report the result.

## The hard rule

**Nothing is set beside anything.** No correlation, regression, plot or count that relates one series to another, in any form, for any pair, including two indicators from this file. Each series is described alone. If a step seems to need a cross-series number, stop and say so in the report.

## Other rules

- Write only: `scripts/fetch_wdi.py`, `src/causal_atlas/table.py`, `scripts/build_table.py`, `scripts/count_table.py`, `tests/test_table.py`, `docs/table-first-count.md`, `data/manifest.toml`, `docs/data-sources.md`, and files under `data/raw/wdi/` and `data/table/`. Change no other file. Do not change how any existing adapter behaves: the existing series must come out identical (check and say). Do not commit, push or install anything. Create no account and register nowhere.
- The network is used only for the World Bank's pages in step 1 and the one download in step 2.
- The downloaded file is untrusted input: its own directory, never executed, Python that reads it run with `-I` (set `sys.path` inside the script).
- Never read a large file into your context. Shapes, heads and counts through DuckDB or a few lines of Python.
- The box is shared with live apps: `nice -n 19`, at most 3 threads. No job you wait on runs longer than about four minutes: start a long download or build in the background with its output to a log under `data/table/`, and come back.
- Python: `.venv/bin/python` from the repo root, `PYTHONPATH=src`. Start every shell command with `cd` to the repo root.
- Match the house style of the repo's code: short functions, a one-line docstring that says what and why, comments only where a choice is not obvious.
- No email address, no absolute home path and no secret in any file you write. The repo is public.

## What to send back

A short report as your final message: what the source pages said (licence sentence and address), what was built and what was not, the table's new size by domain, how many indicators the count rule kept and dropped, every choice this brief did not settle and what you chose, anything in the file that surprised you, the test results, and how long a full build takes.
