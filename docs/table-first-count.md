# The held data in one shape: first count, each series alone

Written by `scripts/count_table.py` from `data/table/` (not committed; `scripts/build_table.py` makes it). 510 series, 218 places, 1,794,760 observations. Nothing in this page sets one series beside another: every number is about a series on its own, or about a group of series counted, never related.

## By domain

| domain | series | places | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | flag none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| climate | 27 | 185 | 1749-01 | 2026-10 | 178,672 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| conflict | 2 | 135 | 1989-01 | 2025-12 | 32,086 | 59.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| crops | 474 | 209 | 1961 | 2024 | 1,485,063 | 0.4% | 58.9% | 29.7% | 8.1% | 3.3% | 0.0% |
| fire | 1 | 188 | 1982-01 | 2018-12 | 81,216 | 2.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| prices | 6 | 35 | 2007-01 | 2026-10 | 17,723 | 3.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

## By source

| source | series | places | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | flag none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| candidates | 25 | 1 | 1749-01 | 2026-10 | 34,231 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| faostat_qcl | 474 | 209 | 1961 | 2024 | 1,485,063 | 0.4% | 58.9% | 29.7% | 8.1% | 3.3% | 0.0% |
| firecci | 1 | 188 | 1982-01 | 2018-12 | 81,216 | 2.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| oni | 1 | 1 | 1950-01 | 2026-09 | 921 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| rtfp | 6 | 35 | 2007-01 | 2026-10 | 17,723 | 3.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| spei | 1 | 184 | 1960-01 | 2024-12 | 143,520 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| ucdp_ged | 2 | 135 | 1989-01 | 2025-12 | 32,086 | 59.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

The span is each place's own, first to last period it has a value. For the conflict counts a missing month means no recorded event (the source lists events, not their absence). Flags exist only in the crop source; everything else reads `none`. Places are those with at least one value in the group; `world` is one place. The 26 climate files (the ONI and the 25 others) are one source line, `candidates` holding the 25; each is listed alone in `data/table/series_description.csv`.

## Memory by domain

The correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least 20 consecutive pairs.

| domain | units | lower quartile | median | upper quartile |
|---|---|---|---|---|
| climate | 210 | 0.68 | 0.72 | 0.76 |
| conflict | 268 | 0.14 | 0.50 | 0.77 |
| crops | 27715 | 0.77 | 0.91 | 0.96 |
| fire | 166 | 0.54 | 0.63 | 0.72 |
| prices | 87 | 0.92 | 0.97 | 0.99 |

## Memory by source

The correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least 20 consecutive pairs.

| source | units | lower quartile | median | upper quartile |
|---|---|---|---|---|
| candidates | 25 | 0.33 | 0.78 | 0.90 |
| faostat_qcl | 27715 | 0.77 | 0.91 | 0.96 |
| firecci | 166 | 0.54 | 0.63 | 0.72 |
| oni | 1 | 0.97 | 0.97 | 0.97 |
| rtfp | 87 | 0.92 | 0.97 | 0.99 |
| spei | 184 | 0.69 | 0.72 | 0.75 |
| ucdp_ged | 268 | 0.14 | 0.50 | 0.77 |

Memory of a level that trends is high because of the trend alone; this is a description of each series, not a measure of anything predictable. For the conflict counts the months with no row are taken as zero for this one number.

## Values the log cannot take

| domain | log-series values at or below zero | values of log series | values equal to zero | all values |
|---|---|---|---|---|
| climate | 0 | 0 | 134 | 178,672 |
| conflict | 0 | 0 | 587 | 32,086 |
| crops | 85 | 475,447 | 41,218 | 1,485,063 |
| fire | 0 | 0 | 23,224 | 81,216 |
| prices | 0 | 17,723 | 0 | 17,723 |

A value at or below zero in a series whose transform is `log` is left out of the memory number and nowhere else.

## What the build set aside

```
{
 "drought": {
  "countries tried": 234,
  "countries with a drought series": 184
 },
 "faostat": {
  "rows of the China total (M49 159)": 21158,
  "rows with no value (all flagged M)": 72442
 },
 "fire": {
  "land cells with burnable land": 62649,
  "of them inside no country": 6772
 },
 "ged": {
  "events in the file": 417968,
  "events inside a country's shape": 414397,
  "events outside every shape (set aside)": 3571,
  "events with no coordinates (set aside)": 0
 },
 "indices": {},
 "prices": {
  "ISO3 codes with no Natural Earth match (set aside)": []
 }
}
```

## What the first count showed

- **Crops are 158 of the 259 items under code 1700.** The brief's "single crop" is read as an item with an area-harvested row; the rest are processed products and livestock products (oils, wine, milk, meat). Each crop has up to three series: yield, area harvested, production.
- **The crop file is UTF-8**, not Latin-1 as `yields.py` reads it (that only damages accents in names, which `yields.py` does not use). The table reads it as UTF-8.
- **Estimated and imputed figures are over a third of the crop values** (flag shares above). The flag is kept on every value so a finder or the referee can set them aside.
- **Eleven crop places have no Natural Earth shape**: the ended countries (Belgium-Luxembourg, Czechoslovakia, Ethiopia PDR, Sudan (former), USSR, Yugoslav SFR, Serbia and Montenegro) and four overseas departments of France. They keep the source's name and no latitude or longitude.
- **Drought exists for 184 of Natural Earth's 234 coded countries**: the rest have no half-degree cell centre inside them with a value in every month, which is the rule of the harvest test, kept as it is.
- **Fire: about 11% of burnable half-degree cells have their centre in no country** (coastal cells), so they are in no country's total. Zero burned area is common (about 29% of country-months). The makers' 1994 gap is a gap, not a zero.
- **Conflict: 0.9% of events fall outside every country shape** and are set aside; a country-month with no event has no row.
- **The climate files run well beyond the years the earlier tests used** (the sunspot series from 1749, the ocean indices from 1870, most to 2026); the table keeps every month the file holds. The manifest's "1950 to 2024" describes the window those tests used.
- **Prices**: 35 of the file's 37 countries have a staple price as collected. Values are in each country's own currency, so levels are not comparable between countries until they are brought to each series' own past.
- **Values at or below zero under a `log` transform** are the 85 zero yields; area and production, which hold many zeros, carry `log1p`.
