# Brief for a helper: FAOSTAT's consumer prices and exchange rates, by month, into the one table

Written by the project session before the helper was started. Estimated cost stated beforehand: about 150,000 fresh tokens; the helper stops and reports at about 250,000 by its own estimate, finished or not. Why: `docs/reading/months-and-places.md` puts these first of the sources by month, and the table's only prices by month are six series for a few countries. The rules of `docs/specs/2026-11-11-world-bank-indicators.md` under "The hard rule" and "Other rules" hold here word for word, with the file names below in place of that brief's; read them there before starting.

## Already confirmed at source by the project session (rule 4), 2026-11-11

- FAOSTAT's own list of bulk files, `https://bulks-faostat.fao.org/production/datasets_E.json`, names `CP`, "Prices: Consumer Price Indices", updated 2026-10-20, 266,292 rows, 2,090 KB, at `https://bulks-faostat.fao.org/production/ConsumerPriceIndices_E_All_Data_(Normalized).zip`; and `PE`, "Prices: Exchange rates", updated 2026-09-16, 151,212 rows, 1,245 KB, at `https://bulks-faostat.fao.org/production/Exchange_rate_E_All_Data_(Normalized).zip`. No account or key.
- Licence, FAO's terms for its statistical databases (`https://www.fao.org/contact-us/terms/db-terms-of-use/en/`): "all datasets disseminated through FAO corporate statistical databases" "are licensed under the Creative Commons Attribution-4.0 International licence", "Unless specified otherwise in their metadata or webpage"; and it warns of "data provided by third parties which may not be redistributed or reused without the consent of the original data provider".
- The consumer prices metadata (`https://files-faostat.fao.org/production/CP/CP_e.pdf`, read as text and searched): the first sources are the IMF's consumer price indices, gaps filled from UNSD, then OECD, BCEAO, ECCB, UNCTAD and national offices; gaps inside a series are filled by estimation. No sentence in it on licence, reuse, redistribution or consent.

So the network is used only for the two downloads.

## What to do, in this order

1. **Fetch**: add both files to the FAOSTAT fetch (`scripts/fetch_faostat.py`, or a new `scripts/fetch_faostat_prices.py` beside it if that keeps the existing fetch identical), to `data/raw/faostat_prices/`, size and SHA-256 recorded as the others are.
2. **Manifest and sources page, in the same change**: entries in `data/manifest.toml` and a section in `docs/data-sources.md` in the style of those there, with the three facts above, the quotes with their addresses, and the known biases: much of the consumer price data is the IMF's, passed on by FAO under FAO's terms, and the IMF's own terms ask permission for commercial reuse (`https://www.imf.org/en/about/copyright-and-terms`), so the files stay on this box and are never committed or passed on; some months are estimates filling gaps; the base year is 2015 and the whole series is rescaled when it changes; official exchange rates can stand far from the rate people pay; a new release replaces the old file at the same address.
3. **Adapter** in `src/causal_atlas/table.py`, wired into `scripts/build_table.py` as the others are. Look first at each file's columns, items, elements and the values of its months column (through DuckDB or a few lines of Python, never the whole file), and say what they are in the report. Then:
   - Countries only, mapped to `place_id` as the existing FAOSTAT adapter does; aggregates dropped; codes with no match set aside and counted in `data/table/notes.json`.
   - One series for each item and element. Rows for a named month become a series by month (`period` month, written `YYYY-MM` as the table's other monthly series are); rows marked as the year's value, if the file has them, become a separate series by year. `series_id` as `faostat_cp:<slug>` and `faostat_pe:<slug>`, with `:year` added for a yearly one.
   - `domain`: use the word the table's existing price series use for consumer prices; `finance` for exchange rates. `kind` and `transform` by the table's convention: an index or a rate of exchange is a level that cannot be negative and can span orders of magnitude, so `log`; a rate of inflation in percent can be negative, so `none`. `flag` as FAOSTAT gives it, as the existing adapter keeps it.
   - No count rule: every series is kept, and the report says for each how many countries have at least 120 monthly values.
4. **Rebuild the table.** Only the new part needs building if the build allows one part at a time; the existing series must come out identical (check and say). Extend `scripts/count_table.py` and `docs/table-first-count.md` with the new source, each series alone: places, first and last period, values, share missing inside each series' span, share of values carrying an estimate flag, and the middle of its month-to-month memory.
5. **Tests** in `tests/test_table.py` on a tiny made-up file the test writes itself: monthly and yearly rows go to the right series with the right period, aggregates are dropped, flags are kept, a second build gives identical tables. Run the table's tests and report the result.

## Files you may write

`scripts/fetch_faostat.py` or `scripts/fetch_faostat_prices.py`, `src/causal_atlas/table.py`, `scripts/build_table.py`, `scripts/count_table.py`, `tests/test_table.py`, `docs/table-first-count.md`, `data/manifest.toml`, `docs/data-sources.md`, and files under `data/raw/faostat_prices/` and `data/table/`. No other file. Do not commit, push or install anything.

## What to send back

A short report as your final message: what the files hold (items, elements, months, flags), what was built and what was not, the table's new size, coverage for each new series, every choice this brief did not settle and what you chose, anything that surprised you, the test results, and how long the build took.
