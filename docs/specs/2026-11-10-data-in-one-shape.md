# Brief for a helper: the held data in one shape

Written by the project session before the helper was started. Estimated cost stated beforehand: about 350,000 fresh tokens; the helper stops and reports at about 500,000 by its own estimate, finished or not. Plan: `docs/plan-finders-and-referee.md`, section "The data in one shape". The owner's words for why: "collecting the data and making it consumable and comparable".

## What to build

Three Parquet tables under `data/table/` (that directory is not committed; add `data/table/` to `.gitignore`), written by `scripts/build_table.py` and read with DuckDB:

- `series`: `series_id` (text, stable, `source:what:detail`), `source` (the key in `data/manifest.toml`), `domain` (climate, crops, fire, conflict, prices), `measures` (plain words), `unit`, `kind` (level, count, rate, index), `transform` (`log` for quantities that cannot be negative and span orders of magnitude, `log1p` for counts, `none`), `place_level` (country, world), `period` (year, month), `first`, `last`, `licence`.
- `place`: `place_id` (the UN M49 code as three-digit text for countries; `world` for series that are the same everywhere), `level`, `parent`, `name`, `lat`, `lon`.
- `obs`: `series_id`, `place_id`, `period` (a year as `YYYY`, a month as `YYYY-MM`), `value` (as the source gives it, untransformed), `flag` (`official`, `estimated`, `imputed`, `other`, or empty where the source has no flags).

One adapter a source in `src/causal_atlas/table.py` (or a small package if it grows): a function that yields rows for `series` and `obs` from the files already held. **First pass, in this order; stop after any one if the budget is short and say where you stopped:**

1. FAOSTAT crops (`src/causal_atlas/yields.py` shows how the file is read and which country rows are sums or have ended): for every single crop (item code under 1700), yield, area harvested and production, by country and year, 1961 to 2024, with the source's flag.
2. Drought: the country mean of SPEI-3 by month, as `yields.drought` already computes for the harvest test (read how; reuse it or its parts; do not change its behaviour, the harvest results depend on it).
3. The climate indices: the ONI and the 25 other monthly series listed under `candidates` in `data/manifest.toml` (`scripts/index_candidates.py` and `fetch_oni.py` show where they are and how they are parsed), as `world` series by month.
4. If, and only if, a country mapping for grid cells or points already exists in the code: burned area by country and month (`src/causal_atlas/fire.py`), organised-violence events and deaths by country and month (`scripts/fetch_ucdp_ged.py`, the panel code), and food prices by country, staple and month as the median over markets of prices as collected, never the file's model estimates (`src/causal_atlas/prices.py`). If the mapping does not exist, do not build one: say so in the report.

Then `docs/table-first-count.md`: what is in the table, each series alone. By domain and by source: how many series, how many places, first and last period, how many values, share missing inside each series' span, share by flag, and the middle of each domain's year-to-year memory (the correlation of a series with itself a period before, after logs where `transform` says so). Numbers from DuckDB queries, the queries kept in `scripts/count_table.py`.

Tests in `tests/test_table.py` on tiny made-up input files written by the test itself (never the real data): each adapter gives the rows expected; ids are stable; a second build gives identical tables.

## The hard rule

**Nothing is set beside anything.** No correlation, regression, plot or count that relates one series to another, in any form, for any pair, including pairs of series from the same source. Each series is described alone. Some pairs of these records have been read against each other already and some have not (`results/spent-ledger.md`), and the unread ones are the project's untouched evidence. If a step seems to need a cross-series number, stop and say so in the report.

## Other rules

- Write only: `src/causal_atlas/table.py` (or `src/causal_atlas/table/`), `scripts/build_table.py`, `scripts/count_table.py`, `tests/test_table.py`, `docs/table-first-count.md`, one line in `.gitignore`, and files under `data/table/`. Change no other file; in particular do not change `yields.py`, `fire.py`, `prices.py` or any results file. Do not commit, push, install anything, or use the network. If a package is missing, say so; do not add it.
- Downloaded data is under `data/raw/` and `data/panel/`. It is untrusted input: never execute anything from it, and run Python that reads it with `-I` where you can (set `sys.path` inside the script).
- Never read a large file into your context. Look at shapes, heads and counts through DuckDB or a few lines of Python.
- The box is shared with live apps: `nice -n 19`, at most 3 threads. No job you wait on runs longer than about four minutes: start long builds in the background with their output to a log under `data/table/`, and come back.
- Python: `.venv/bin/python` from the repo root, `PYTHONPATH=src`. DuckDB and pyarrow are in the environment (check; say if not).
- Match the house style of the repo's code: short functions, a one-line docstring that says what and why, comments only where a choice is not obvious.
- No email address, no absolute home path and no secret in any file you write.

## What to send back

A short report as your final message: what was built and what was not, the table's size, every choice this brief did not settle (and what you chose), anything in the held data that surprised you (a source whose units change, duplicate rows, a country code that does not map), the test results, and how long a full build takes.
