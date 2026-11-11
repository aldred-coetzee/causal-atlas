# The held data in one shape: first count, each series alone

Written by `scripts/count_table.py` from `data/table/` (not committed; `scripts/build_table.py` makes it). 1125 series, 241 places, 7,509,854 observations. Nothing in this page sets one series beside another: every number is about a series on its own, or about a group of series counted, never related.

## By domain

| domain | series | places | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | flag none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| climate | 27 | 185 | 1749-01 | 2026-10 | 178,672 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| conflict | 2 | 135 | 1989-01 | 2025-12 | 32,086 | 59.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| crops | 474 | 209 | 1961 | 2024 | 1,485,063 | 0.4% | 58.9% | 29.7% | 8.1% | 3.3% | 0.0% |
| economy | 242 | 215 | 1960 | 2025 | 1,886,488 | 1.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| education | 21 | 211 | 1970 | 2025 | 162,670 | 16.5% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| environment | 107 | 215 | 1960 | 2025 | 980,646 | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| finance | 23 | 225 | 1960 | 2026-07 | 328,425 | 1.9% | 0.0% | 0.0% | 0.0% | 44.3% | 55.7% |
| fire | 1 | 188 | 1982-01 | 2018-12 | 81,216 | 2.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| health | 108 | 215 | 1960 | 2025 | 1,302,097 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| infrastructure | 9 | 213 | 1960 | 2025 | 79,777 | 9.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| prices | 9 | 202 | 2000-01 | 2026-10 | 204,609 | 0.4% | 4.5% | 29.5% | 7.8% | 49.5% | 8.7% |
| public sector | 2 | 174 | 1985 | 2020 | 10,380 | 5.6% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| social | 52 | 215 | 1960 | 2025 | 349,225 | 0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| trade | 48 | 211 | 1960 | 2025 | 428,500 | 7.2% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

## By source

| source | series | places | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | flag none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| candidates | 25 | 1 | 1749-01 | 2026-10 | 34,231 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| faostat_cp | 3 | 202 | 2000-01 | 2026-06 | 186,886 | 0.1% | 4.9% | 32.3% | 8.6% | 54.2% | 0.0% |
| faostat_pe | 3 | 221 | 1970 | 2026-07 | 145,603 | 3.2% | 0.1% | 0.0% | 0.0% | 99.9% | 0.0% |
| faostat_qcl | 474 | 209 | 1961 | 2024 | 1,485,063 | 0.4% | 58.9% | 29.7% | 8.1% | 3.3% | 0.0% |
| firecci | 1 | 188 | 1982-01 | 2018-12 | 81,216 | 2.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| oni | 1 | 1 | 1950-01 | 2026-09 | 921 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| rtfp | 6 | 35 | 2007-01 | 2026-10 | 17,723 | 3.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| spei | 1 | 184 | 1960-01 | 2024-12 | 143,520 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| ucdp_ged | 2 | 135 | 1989-01 | 2025-12 | 32,086 | 59.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| wdi | 609 | 215 | 1960 | 2025 | 5,382,605 | 1.9% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

The span is each place's own, first to last period it has a value. For the conflict counts a missing month means no recorded event (the source lists events, not their absence). Flags exist in the crop source and the two FAOSTAT price sources (`faostat_cp`, `faostat_pe`); everything else reads `none`. Places are those with at least one value in the group; `world` is one place. The 26 climate files (the ONI and the 25 others) are one source line, `candidates` holding the 25; each is listed alone in `data/table/series_description.csv`.

## Memory by domain

The correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least 20 consecutive pairs.

| domain | units | lower quartile | median | upper quartile |
|---|---|---|---|---|
| climate | 210 | 0.68 | 0.72 | 0.76 |
| conflict | 268 | 0.14 | 0.50 | 0.77 |
| crops | 27715 | 0.77 | 0.91 | 0.96 |
| economy | 39024 | 0.76 | 0.94 | 0.99 |
| education | 2933 | 0.88 | 0.96 | 0.99 |
| environment | 18323 | 0.89 | 0.96 | 0.99 |
| finance | 4132 | 0.72 | 0.95 | 0.99 |
| fire | 166 | 0.54 | 0.63 | 0.72 |
| health | 21562 | 0.98 | 0.99 | 1.00 |
| infrastructure | 1680 | 0.91 | 0.98 | 0.99 |
| prices | 689 | 0.97 | 1.00 | 1.00 |
| public sector | 325 | 0.73 | 0.85 | 0.93 |
| social | 9652 | 0.88 | 0.95 | 0.99 |
| trade | 8690 | 0.67 | 0.84 | 0.94 |

## Memory by source

The correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least 20 consecutive pairs.

| source | units | lower quartile | median | upper quartile |
|---|---|---|---|---|
| candidates | 25 | 0.33 | 0.78 | 0.90 |
| faostat_cp | 602 | 0.98 | 1.00 | 1.00 |
| faostat_pe | 610 | 0.94 | 0.99 | 1.00 |
| faostat_qcl | 27715 | 0.77 | 0.91 | 0.96 |
| firecci | 166 | 0.54 | 0.63 | 0.72 |
| oni | 1 | 0.97 | 0.97 | 0.97 |
| rtfp | 87 | 0.92 | 0.97 | 0.99 |
| spei | 184 | 0.69 | 0.72 | 0.75 |
| ucdp_ged | 268 | 0.14 | 0.50 | 0.77 |
| wdi | 105711 | 0.85 | 0.97 | 0.99 |

Memory of a level that trends is high because of the trend alone; this is a description of each series, not a measure of anything predictable. For the conflict counts the months with no row are taken as zero for this one number.

## FAOSTAT consumer prices and exchange rates, each series alone

| series | step | places | places with 120+ monthly values | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | memory (median over places) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| faostat_cp:consumer_prices_food_indices | month | 200 | 199 | 2000-01 | 2026-06 | 62,821 | 0.1% | 11.0% | 0.0% | 18.1% | 70.9% | 1.00 |
| faostat_cp:consumer_prices_general_indices | month | 202 | 202 | 2000-01 | 2026-06 | 63,644 | 0.2% | 3.6% | 0.0% | 7.3% | 89.1% | 1.00 |
| faostat_cp:food_price_inflation | month | 200 | 199 | 2001-01 | 2026-06 | 60,421 | 0.1% | 0.0% | 100.0% | 0.0% | 0.0% | 0.96 |
| faostat_pe:lcu | month | 210 | 207 | 1970-01 | 2026-07 | 122,472 | 3.7% | 0.1% | 0.0% | 0.0% | 99.9% | 1.00 |
| faostat_pe:lcu:year | year | 220 | 0 | 1970 | 2025 | 11,367 | 0.6% | 0.0% | 0.0% | 0.0% | 100.0% | 0.95 |
| faostat_pe:slc:year | year | 221 | 0 | 1970 | 2025 | 11,764 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 0.98 |

Flag `other` is FAOSTAT's X, a figure from an outside organisation. Memory is the correlation of each place's series with itself one period before, after the log the series table names, as above.

## Values the log cannot take

| domain | log-series values at or below zero | values of log series | values equal to zero | all values |
|---|---|---|---|---|
| climate | 0 | 0 | 134 | 178,672 |
| conflict | 0 | 0 | 587 | 32,086 |
| crops | 85 | 475,447 | 41,218 | 1,485,063 |
| economy | 0 | 525,390 | 37,863 | 1,886,488 |
| education | 0 | 61,784 | 1,023 | 162,670 |
| environment | 0 | 214,137 | 60,325 | 980,646 |
| finance | 0 | 176,944 | 36 | 328,425 |
| fire | 0 | 0 | 23,224 | 81,216 |
| health | 0 | 226,427 | 924 | 1,302,097 |
| infrastructure | 0 | 0 | 8,872 | 79,777 |
| prices | 0 | 144,188 | 131 | 204,609 |
| public sector | 0 | 0 | 27 | 10,380 |
| social | 0 | 12,801 | 552 | 349,225 |
| trade | 0 | 40,613 | 7,004 | 428,500 |

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
 "faostat_cp": {
  "areas with no Natural Earth match (set aside; rows)": {
   "French Guiana": 942,
   "Guadeloupe": 942,
   "Martinique": 942,
   "Netherlands Antilles (former)": 192,
   "R\u00e9union": 938,
   "Sub-Saharan Africa": 1884
  },
  "rows in the file": 266292,
  "rows of groups of countries (area code 5000 or more; dropped)": 73476,
  "rows of the China total (dropped)": 0,
  "rows with a months code that is neither a month nor the year (set aside)": 0,
  "rows with no value (flagged L)": 90
 },
 "faostat_pe": {
  "areas with no Natural Earth match (set aside; rows)": {
   "Czechoslovakia": 176,
   "French Guiana": 790,
   "Guadeloupe": 790,
   "Martinique": 790,
   "Mayotte": 385,
   "Netherlands Antilles (former)": 536,
   "R\u00e9union": 443,
   "Sudan (former)": 41,
   "Yugoslav SFR": 295
  },
  "rows in the file": 151212,
  "rows in two currencies for one country and period (set aside)": 1342,
  "rows of groups of countries (area code 5000 or more; dropped)": 0,
  "rows of the China total (dropped)": 0,
  "rows with a months code that is neither a month nor the year (set aside)": 0,
  "rows with no value (flagged L)": 21
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
 },
 "wdi": {
  "aggregate and unclassified codes in the data file (dropped)": 48,
  "country codes with no Natural Earth match (set aside)": [
   "CHI",
   "XKX"
  ],
  "dropped by licence (not CC BY-4.0 in the series file)": 9,
  "dropped by the count rule after the licence": 880,
  "dropped by the count rule alone (100 countries with 30 yearly values; any licence)": 885,
  "indicators in the series file": 1498,
  "indicators kept": 609,
  "kept by domain": {
   "economy": 242,
   "education": 21,
   "environment": 107,
   "finance": 20,
   "health": 108,
   "infrastructure": 9,
   "public sector": 2,
   "social": 52,
   "trade": 48
  },
  "kept by kind and transform": {
   "index/none": 9,
   "level/log": 122,
   "level/log1p": 99,
   "level/none": 77,
   "rate/none": 302
  },
  "values in those codes (dropped)": 1539985,
  "values in those codes (set aside)": 23771
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
- **World Development Indicators (added 2026-11-11): 609 of 1,498 indicators kept, by a count rule.** Kept: licence `CC BY-4.0` in the series file (9 dropped: 6 SIPRI terms, 3 CC BY 3.0 IGO) and at least 100 countries (of those that map to the table's places) each with at least 30 yearly values (880 of the 1,489 licensed indicators dropped; 885 fail the count rule whatever their licence). 215 places carry values; 217 country rows in the Bank's country file, of which the Channel Islands and Kosovo have no Natural Earth match and are set aside (23,771 values); 48 regional and income aggregates (1,539,985 values) are dropped; the file's `INX` code has no values.
- **WDI domains follow the first part of the Bank's topic, as the brief said.** Thirteen first parts became nine domains (economic policy and debt is economy, private sector and trade and trade are trade, gender and social protection are social, policy and institutions is public sector; none of the kept indicators has a topic that fits no domain). So **population is not a domain**: the 64 kept indicators whose topic names population sit under health, and the 23 under energy production and use sit under environment.
- **WDI kind and transform follow the name and unit text and the lowest value**: shares, rates and ratios (a percent sign, "per 1,000", rate, growth, ratio, share) are `rate`, `none`; indices and scores are `index`, `none`; the rest are quantities, `level` with `log` if every value is above zero, `log1p` if the lowest is zero, `none` if any is negative (302 rate, 9 index, 122 log, 99 log1p, 77 none). None is `count`: this page fills the months with no row with zero for count series only, and a missing year in a World Development Indicator is not a zero. The unit is the bracket that ends the name, else the series file's unit of measure; the bracket is sometimes not a unit ("GPI", "GDP").
- **WDI figures carry no flag here**, though many are estimates or gap-filled by the Bank or UN agencies; the file's footnotes are not used. The newest years are thin: 100,646 values in 2023, 89,512 in 2024, 57,622 in 2025, among the kept series. Education (16.5%), trade (7.2%) and infrastructure (9.0%) have the most missing inside their spans.
- **The memory of the World Development Indicators is that of trending levels** (median 0.97, lower quartile 0.85): a description of each series, not a measure of anything predictable.
- **FAOSTAT consumer prices and exchange rates (added 2026-11-11): six series, 332,489 values, by month.** `faostat_cp` holds the general and the food consumer price index (2015 = 100) and the food price inflation (percent), months only (the file has no year's-value rows), 2000-01 to 2026-06 (inflation from 2001), in 202 places; the file's weighted-average and median items are for groups of countries only and give no series. `faostat_pe` holds the official exchange rate in local currency units per US dollar by month (1970-01 to 2026-07) and by year, and the standard local currency element by year only (the restatement of old years in the current currency), in 221 places. Dropped or set aside, all counted in the notes above: 73,476 group rows in the price file (area codes 5000 and over), 111 rows with no value (flag L), the places with no Natural Earth match (Sub-Saharan Africa, a group with a low code, and French Guiana, Guadeloupe, Martinique, Mayotte, Netherlands Antilles, Reunion, the ended Czechoslovakia, Sudan (former) and Yugoslav SFR), and 1,342 exchange-rate rows where a country has two currencies in one period (a changeover; the level in local units is ambiguous there).
- **FAOSTAT price flags: X is most of the values.** In the consumer price file 54% are X (from an outside organisation, kept as `other`), 32% E and 9% I, 5% official; every food inflation value is flagged E. In the exchange rate file 99.9% are X. Base year 2015 is in the unit text; FAO rescales the whole index if it changes. The two price indices and the exchange rates are levels that trend or jump at a redenomination, so their memory is near 1.00 (inflation 0.96, a description of each series and not of anything predictable). Values in the price index run from 0.67 to 2.9 trillion (the log keeps them usable), and inflation from -67% to 372,000%.
- **Values at or below zero under a `log` transform** are the 85 zero yields; area and production, which hold many zeros, carry `log1p`.
