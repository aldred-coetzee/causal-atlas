# Brief for one more helper, the third wave

Written by the project session before it was started (rule 7). The owner, 2026-11-11: "Please run what you can in parallel". The first wave is `docs/specs/2026-11-11-parallel-helpers.md`; **its section "What every helper is held to" binds this helper as written there**, and so does its last section on what the project session checks before using anything. Never more than three helpers at once: F starts in the place D left.

Estimated cost, fresh tokens, the helper's own estimate: about 600,000; it stops and reports at 900,000. Figures reported to the owner are counted from transcripts afterwards.

## F. Kinds the table lacks, for the whole world (research and fetch)

**The decision it serves.** The new monthly sources are mostly Europe's. The first read's panel is 166 countries, and the owner's aim is relationships "between many separate data sets". Which of four sources of other kinds, each covering most of the world, can enter the table now?

**Sources, in this order.** Each name and address is a claim until read at source; a source that needs an account, a key, a form or an email address is written down as not usable and left.

1. **People forced to move:** UNHCR's refugee statistics (its public API or bulk download): refugees and asylum seekers by country of origin and by country of asylum, by year. Read its terms of use at its own page.
2. **Tropical cyclones:** NOAA's IBTrACS best-track archive (the CSV of the latest version; the file from 1980 if the whole record is too large to handle lightly). Decide from the archive's own documents which first year gives a record comparable through time, and say why. By country and month: storms whose track passes inside a country's shape, and the strongest wind recorded inside it; and a count for the world.
3. **Electricity by source:** Ember's electricity data (monthly and yearly, by country): generation in all, and from coal, gas, wind, solar, hydro and nuclear. Read its licence at its own page.
4. **Commodity prices for the world:** the World Bank's monthly commodity price data (the "Pink Sheet"): each price as a world series, with the place `world`, as the earthquake world series is held. Read the licence that covers this file, which may differ from the indicators file already held.

**Which cut is kept is fixed here, before any file is opened:** totals and physical quantities as the source gives them; no figure per head or per unit of output (the table's users can make those); a monthly record where the source has one, and the yearly one beside it only where it reaches further back. Where this does not settle a choice, say so and take the cut with the most country-periods. No cut is chosen by looking at how a series moves with another.

**To write:**

- `scripts/fetch_world_kinds.py`: fetches each usable source into `data/raw/unhcr/`, `data/raw/ibtracs/`, `data/raw/ember/`, `data/raw/pink_sheet/` with `scripts/_download.py`, printing size and SHA-256. Run it.
- `src/causal_atlas/adapters_world_kinds.py`: one function a source returning a `table.Part` (models: `src/causal_atlas/adapters_events.py`, `src/causal_atlas/adapters_money_people.py`). The licence text is passed in. For each series: whether a missing period is a zero or nothing, and why.
- `tests/test_adapters_world_kinds.py`: on small made-up files written by the test.
- `docs/reading/sources-world-kinds.md`: for each source, the address, the licence quoted with its address, what was fetched (file, bytes, SHA-256, date), coverage counted from the file, known biases the source's own documents state, the citation asked for, the series a steward should bar from naming each other (and from naming series already held: the World Bank's indicators hold electricity and refugee figures), and a proposed entry for `data/manifest.toml`, every field written out in full.
