# Briefs for two more helpers, the second wave

Written by the project session before either was started (rule 7). The owner, 2026-11-11: "Please run what you can in parallel". The first wave is `docs/specs/2026-11-11-parallel-helpers.md`; **its section "What every helper is held to" binds these two as written there**, and so does its last section on what the project session checks before using anything. Never more than three helpers at once: D starts in the place B left; E starts when A or C is back.

Estimated cost, fresh tokens, each helper's own estimate: D about 500,000, E about 900,000; each stops and reports at one and a half times its figure. Figures reported to the owner are counted from transcripts afterwards.

## D. Eurostat by country and month: kinds the table does not hold (research and fetch)

**The decision it serves.** The owner's aim is relationships "between many separate data sets"; the table's kinds are still few (crops, climate, conflict, prices, the World Bank's yearly file, and now money, births and deaths). Eurostat is European infrastructure, answers without a key, and its reuse notice has been read (`docs/data-sources.md`, "Eurostat deaths by month"). Which of its monthly tables of other kinds can enter the table now?

**What to find, at source.** From the API's own list of tables (`https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/all` or the catalogue it points to), up to eight monthly tables by country, each of a different kind, from this list of kinds: unemployment, industrial production, retail trade, energy supplied or used (electricity, gas), nights spent at tourist accommodation, air passengers, first-time asylum applicants, live births by month, building permits. A table code is a claim until the API answers for it. For each: the longest record, the most countries, a size under about 50 MB as fetched (ask the API for the totals only where a table is broken down by citizenship, sector or partner).

**Which cut of each table is kept is fixed by this rule, written here before any file is opened:** the total over every breakdown (all ages, both sexes, all sectors named by the table as its total); counts and physical quantities as counted, not seasonally adjusted, where the table offers both; an index only where no count exists, then the unadjusted one. Where the rule does not settle a choice, say so and take the cut with the most country-months. No cut is chosen by looking at how a series moves with another.

**To write:**

- `scripts/fetch_eurostat_months.py`: fetches each table into `data/raw/eurostat/<table>/` with `scripts/_download.py`, printing size and SHA-256. Run it.
- `src/causal_atlas/adapters_eurostat.py`: one general function for a table in Eurostat's SDMX-CSV layout with a stated cut, returning a `table.Part`; it may import `iso2_codes` and `eurostat_flag` from `adapters_money_people.py` and must not edit that file. Groups of countries, forecasts and codes with no place are set aside and counted. Whether a missing month is a zero or nothing: say which and why, table by table.
- `tests/test_adapters_eurostat.py`: on small made-up files written by the test.
- `docs/reading/sources-eurostat-months.md`: for each table, its code and title as the API gives them, the cut kept and why, bytes, SHA-256, date, coverage counted from the file (places, first and last month, values), known biases the table's own notes state (breaks in series, provisional months, changes of definition), whether any country in it falls under the notice's non-commercial exception, and a proposed entry for `data/manifest.toml` as full text, every field written out. One page.

## E. Reading by month: what the finders and the referee need before a monthly table is read (design)

**The decision it serves.** The finders and the referee were counted on yearly tables of about sixty years. The table now holds many monthly series (drought, fire, conflict, prices, exchange rates, policy rates, births, deaths), and nothing can read them at their own step: made yearly, a link that runs its course inside a year is lost. Before a rule for a monthly read is written, what has to change, and what can stay as counted?

**Questions, in order:**

1. Given a monthly made-up table (several hundred months, a season in every series, each month close to the one before), what do the finders and the referee as they are do where nothing predicts: how often does anything pass? Show where the false passes come from, if there are any: the season, the nearness of neighbouring months, or the bar's way of drawing years again.
2. Three ways to read by month, each prototyped on smoke worlds with a link planted at a lag of one to six months and on worlds where nothing predicts: (a) months with the season taken out, the bar drawing whole years again; (b) a monthly driver made into a few yearly features (its peak, its worst three months, months beyond a level) set against a yearly outcome; (c) one calendar month at a time across years. For each: what is heard, what passes falsely, what it costs in rows and time.
3. What baseline is fair by month: the same month in earlier years, the months just before, neighbours? State the one to register and why (rule 2: nothing counts unless it beats the place's own history and season).
4. What a registered count for the chosen way would need: worlds, marks, seeds, runtime on this box.

**Rules particular to E:**

- Made-up tables only. Nothing under `data/raw/`, `data/table/` or `data/panel/stage-b/` is read.
- `src/causal_atlas/finders.py`, `referee.py` and everything under `src/causal_atlas/synth/` are read and imported, never edited. If the generator cannot make a monthly world, the helper writes its own maker in `scripts/lab_monthly_worlds.py`, sharing no code with any prototype that proposes or scores; only the harness imports it (rule 3).
- Smoke seeds 60001 to 60999 only, each one used listed in the notes file. Never in a count. Every number is a development number and is called one.
- One process at a time, one thread, under 1.5 GB; outputs under `data/panel/monthly/`.

**To write:** `scripts/lab_monthly.py` (prototypes and harness), `scripts/lab_monthly_worlds.py` if needed, `docs/reading/reading-by-month.md` (two pages at most: what was found on each question, the way recommended with its settings and baseline, what was tried and dropped, the seeds used, what is not known).
