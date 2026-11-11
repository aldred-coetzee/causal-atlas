# The held data in one shape: first count, each series alone

Written by `scripts/count_table.py` from `data/table/` (not committed; `scripts/build_table.py` makes it). 1251 series, 246 places, 8,628,886 observations. Nothing in this page sets one series beside another: every number is about a series on its own, or about a group of series counted, never related.

## By domain

| domain | series | places | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | flag none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| climate | 27 | 185 | 1749-01 | 2026-10 | 178,672 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| conflict | 2 | 135 | 1989-01 | 2025-12 | 32,086 | 59.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| crops | 474 | 209 | 1961 | 2024 | 1,485,063 | 0.4% | 58.9% | 29.7% | 8.1% | 3.3% | 0.0% |
| disasters | 6 | 235 | 1973-01 | 2026-10 | 432,495 | 5.8% | 0.0% | 0.0% | 0.0% | 0.0% | 69.0% |
| economy | 244 | 215 | 1960 | 2026-10 | 1,912,265 | 1.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| education | 21 | 211 | 1970 | 2025 | 162,670 | 16.5% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| energy | 15 | 204 | 1985 | 2026-10 | 111,946 | 0.2% | 0.0% | 0.1% | 0.0% | 0.0% | 99.9% |
| environment | 107 | 215 | 1960 | 2025 | 980,646 | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| finance | 34 | 225 | 1927 | 2026-10 | 452,678 | 1.4% | 0.0% | 0.0% | 0.0% | 32.1% | 67.8% |
| fire | 1 | 188 | 1982-01 | 2018-12 | 81,216 | 2.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| health | 110 | 222 | 1955 | 2025-04 | 1,313,737 | 0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 99.1% |
| infrastructure | 9 | 213 | 1960 | 2025 | 79,777 | 9.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| migration | 1 | 33 | 2008-01 | 2026-10 | 6,601 | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% | 99.6% |
| people | 10 | 215 | 1951 | 2025-12 | 101,854 | 3.8% | 0.0% | 0.0% | 0.0% | 0.4% | 99.6% |
| prices | 82 | 203 | 1661 | 2026-10 | 307,179 | 0.5% | 3.0% | 19.7% | 5.2% | 33.0% | 39.2% |
| public sector | 2 | 174 | 1985 | 2020 | 10,380 | 5.6% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| social | 52 | 215 | 1960 | 2025 | 349,225 | 0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| trade | 49 | 211 | 1960 | 2026-09 | 439,133 | 7.0% | 0.0% | 0.0% | 0.0% | 0.2% | 99.8% |
| travel | 2 | 39 | 1990-01 | 2026-09 | 21,325 | 3.3% | 0.0% | 0.9% | 0.0% | 4.2% | 94.9% |
| unrest | 3 | 159 | 1990-01 | 2020-03 | 169,938 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

## By source

| source | series | places | first | last | values | missing inside span | flag official | flag estimated | flag imputed | flag other | flag none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bis_cbpol | 1 | 48 | 1945-01 | 2026-10 | 24,779 | 0.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| bis_eer | 4 | 63 | 1964-01 | 2026-09 | 87,921 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| bis_long_cpi | 2 | 62 | 1661 | 2026-09 | 52,588 | 0.9% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| bis_spp | 1 | 57 | 1927 | 2025 | 2,158 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| bis_tc | 5 | 43 | 1947 | 2025 | 9,395 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| candidates | 25 | 1 | 1749-01 | 2026-10 | 34,231 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| ember | 14 | 204 | 1985 | 2026-10 | 104,339 | 0.2% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| eurostat_air | 1 | 36 | 1993-01 | 2026-09 | 9,464 | 1.1% | 0.0% | 0.0% | 0.0% | 7.2% | 92.8% |
| eurostat_asylum | 1 | 33 | 2008-01 | 2026-10 | 6,601 | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% | 99.6% |
| eurostat_births | 1 | 48 | 1960-01 | 2025-12 | 21,994 | 3.7% | 0.0% | 0.0% | 0.0% | 1.0% | 99.0% |
| eurostat_deaths | 1 | 48 | 1960-01 | 2025-12 | 22,064 | 5.1% | 0.0% | 0.0% | 0.0% | 1.0% | 99.0% |
| eurostat_electricity | 1 | 39 | 2008-01 | 2026-09 | 7,607 | 0.4% | 0.0% | 1.1% | 0.0% | 0.3% | 98.6% |
| eurostat_industry | 1 | 36 | 1975-01 | 2026-09 | 11,851 | 0.0% | 0.0% | 0.0% | 0.0% | 2.2% | 97.8% |
| eurostat_retail | 1 | 36 | 1994-01 | 2026-09 | 10,633 | 0.0% | 0.0% | 0.0% | 0.0% | 6.7% | 93.3% |
| eurostat_tourism | 1 | 38 | 1990-01 | 2026-09 | 11,861 | 5.0% | 0.0% | 1.6% | 0.0% | 1.8% | 96.6% |
| eurostat_unemployment | 1 | 36 | 1983-01 | 2026-10 | 13,926 | 0.0% | 0.0% | 0.0% | 0.0% | 1.1% | 98.9% |
| faostat_cp | 3 | 202 | 2000-01 | 2026-06 | 186,886 | 0.1% | 4.9% | 32.3% | 8.6% | 54.2% | 0.0% |
| faostat_pe | 3 | 221 | 1970 | 2026-07 | 145,603 | 3.2% | 0.1% | 0.0% | 0.0% | 99.9% | 0.0% |
| faostat_qcl | 474 | 209 | 1961 | 2024 | 1,485,063 | 0.4% | 58.9% | 29.7% | 8.1% | 3.3% | 0.0% |
| firecci | 1 | 188 | 1982-01 | 2018-12 | 81,216 | 2.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| hfd_stff | 4 | 43 | 2000-01 | 2025-12 | 31,224 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| ibtracs | 3 | 235 | 1980-01 | 2026-10 | 134,211 | 16.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mass_mobilization | 3 | 159 | 1990-01 | 2020-03 | 169,938 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| oni | 1 | 1 | 1950-01 | 2026-09 | 921 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| opendengue | 2 | 121 | 1955 | 2025-04 | 11,640 | 28.9% | 0.0% | 0.0% | 4.9% | 0.0% | 0.0% |
| pink_sheet | 71 | 1 | 1960 | 2026-10 | 49,982 | 0.5% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| rtfp | 6 | 35 | 2007-01 | 2026-10 | 17,723 | 3.4% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| spei | 1 | 184 | 1960-01 | 2024-12 | 143,520 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| ucdp_ged | 2 | 135 | 1989-01 | 2025-12 | 32,086 | 59.7% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| unhcr | 4 | 213 | 1951 | 2025 | 26,572 | 6.9% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| usgs_quakes | 3 | 235 | 1973-01 | 2025-12 | 298,284 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| wdi | 609 | 215 | 1960 | 2025 | 5,382,605 | 1.9% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |

The span is each place's own, first to last period it has a value. For the conflict counts a missing month means no recorded event (the source lists events, not their absence). Flags exist in the crop source and the two FAOSTAT price sources (`faostat_cp`, `faostat_pe`); everything else reads `none`. Places are those with at least one value in the group; `world` is one place. The 26 climate files (the ONI and the 25 others) are one source line, `candidates` holding the 25; each is listed alone in `data/table/series_description.csv`.

## Memory by domain

The correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least 20 consecutive pairs.

| domain | units | lower quartile | median | upper quartile |
|---|---|---|---|---|
| climate | 210 | 0.68 | 0.72 | 0.76 |
| conflict | 268 | 0.14 | 0.50 | 0.77 |
| crops | 27715 | 0.77 | 0.91 | 0.96 |
| disasters | 364 | -0.01 | -0.00 | 0.09 |
| economy | 39096 | 0.76 | 0.94 | 0.99 |
| education | 2933 | 0.88 | 0.96 | 0.99 |
| energy | 1407 | 0.72 | 0.89 | 0.97 |
| environment | 18323 | 0.89 | 0.96 | 0.99 |
| finance | 4608 | 0.77 | 0.96 | 0.99 |
| fire | 166 | 0.54 | 0.63 | 0.72 |
| health | 21724 | 0.98 | 0.99 | 1.00 |
| infrastructure | 1680 | 0.91 | 0.98 | 0.99 |
| migration | 33 | 0.78 | 0.87 | 0.92 |
| people | 892 | 0.81 | 0.90 | 0.94 |
| prices | 882 | 0.98 | 1.00 | 1.00 |
| public sector | 325 | 0.73 | 0.85 | 0.93 |
| social | 9652 | 0.88 | 0.95 | 0.99 |
| trade | 8726 | 0.67 | 0.84 | 0.94 |
| travel | 73 | 0.80 | 0.85 | 0.89 |
| unrest | 443 | -0.01 | 0.10 | 0.21 |

## Memory by source

The correlation of a place's series with itself one period before (a year for yearly series, a month for monthly), after the log the series table names; lower quartile, median and upper quartile over the series-and-place units that have at least 20 consecutive pairs.

| source | units | lower quartile | median | upper quartile |
|---|---|---|---|---|
| bis_cbpol | 48 | 0.98 | 0.99 | 1.00 |
| bis_eer | 177 | 0.98 | 0.99 | 1.00 |
| bis_long_cpi | 122 | 1.00 | 1.00 | 1.00 |
| bis_spp | 46 | 0.98 | 1.00 | 1.00 |
| bis_tc | 205 | 0.94 | 0.97 | 0.99 |
| candidates | 25 | 0.33 | 0.78 | 0.90 |
| ember | 1368 | 0.73 | 0.90 | 0.97 |
| eurostat_air | 36 | 0.86 | 0.88 | 0.91 |
| eurostat_asylum | 33 | 0.78 | 0.87 | 0.92 |
| eurostat_births | 48 | 0.74 | 0.86 | 0.91 |
| eurostat_deaths | 48 | 0.65 | 0.71 | 0.74 |
| eurostat_electricity | 39 | 0.68 | 0.73 | 0.81 |
| eurostat_industry | 36 | 0.60 | 0.78 | 0.91 |
| eurostat_retail | 36 | 0.83 | 0.92 | 0.97 |
| eurostat_tourism | 37 | 0.77 | 0.81 | 0.84 |
| eurostat_unemployment | 36 | 0.95 | 0.99 | 0.99 |
| faostat_cp | 602 | 0.98 | 1.00 | 1.00 |
| faostat_pe | 610 | 0.94 | 0.99 | 1.00 |
| faostat_qcl | 27715 | 0.77 | 0.91 | 0.96 |
| firecci | 166 | 0.54 | 0.63 | 0.72 |
| hfd_stff | 130 | 0.81 | 0.91 | 0.96 |
| ibtracs | 107 | -0.00 | -0.00 | 0.13 |
| mass_mobilization | 443 | -0.01 | 0.10 | 0.21 |
| oni | 1 | 0.97 | 0.97 | 0.97 |
| opendengue | 162 | 0.49 | 0.76 | 0.87 |
| pink_sheet | 71 | 0.99 | 0.99 | 1.00 |
| rtfp | 87 | 0.92 | 0.97 | 0.99 |
| spei | 184 | 0.69 | 0.72 | 0.75 |
| ucdp_ged | 268 | 0.14 | 0.50 | 0.77 |
| unhcr | 666 | 0.84 | 0.91 | 0.94 |
| usgs_quakes | 257 | -0.01 | -0.00 | 0.09 |
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
| disasters | 0 | 2,141 | 408,447 | 432,495 |
| economy | 0 | 551,167 | 37,863 | 1,912,265 |
| education | 0 | 61,784 | 1,023 | 162,670 |
| energy | 0 | 19,212 | 21,825 | 111,946 |
| environment | 0 | 214,137 | 60,325 | 980,646 |
| finance | 0 | 267,023 | 117 | 452,678 |
| fire | 0 | 0 | 23,224 | 81,216 |
| health | 0 | 226,427 | 3,603 | 1,313,737 |
| infrastructure | 0 | 0 | 8,872 | 79,777 |
| migration | 0 | 0 | 118 | 6,601 |
| people | 0 | 26,699 | 3,280 | 101,854 |
| prices | 0 | 246,758 | 131 | 307,179 |
| public sector | 0 | 0 | 27 | 10,380 |
| social | 0 | 12,801 | 552 | 349,225 |
| trade | 0 | 51,246 | 7,004 | 439,133 |
| travel | 0 | 0 | 125 | 21,325 |
| unrest | 0 | 0 | 156,729 | 169,938 |

A value at or below zero in a series whose transform is `log` is left out of the memory number and nowhere else.

## What the build set aside

```
{
 "bis_cbpol": {
  "places with no Natural Earth match (set aside; rows)": {
   "XM Euro area": 334
  },
  "rows in the file": 734711,
  "rows marked missing or with no value (set aside)": 53,
  "rows of the kept series": 25166,
  "series-level rows with no time period (not observations)": 0
 },
 "bis_eer": {
  "places with no Natural Earth match (set aside; rows)": {
   "XM Euro area": 2292
  },
  "rows in the file": 1214168,
  "rows marked missing or with no value (set aside)": 0,
  "rows of the kept series": 90213,
  "series-level rows with no time period (not observations)": 271
 },
 "bis_long_cpi": {
  "places with no Natural Earth match (set aside; rows)": {
   "XM Euro area": 477
  },
  "rows in the file": 106225,
  "rows marked missing or with no value (set aside)": 457,
  "rows of the kept series": 53522,
  "series-level rows with no time period (not observations)": 0
 },
 "bis_spp": {
  "places with no Natural Earth match (set aside; rows)": {
   "4T Emerging market economies (aggregate)": 74,
   "5R Advanced economies": 74,
   "XM Euro area": 206,
   "XW World": 74
  },
  "rows in the file": 35860,
  "rows marked missing or with no value (set aside)": 0,
  "rows of the kept series": 9179,
  "series-level rows with no time period (not observations)": 0,
  "years with fewer than four quarters (not made into a year)": 62
 },
 "bis_tc": {
  "places with no Natural Earth match (set aside; rows)": {
   "4T Emerging market economies (aggregate)": 458,
   "5A All reporting economies": 443,
   "5R Advanced economies": 541,
   "G2 G20 economies": 468,
   "XM Euro area": 552
  },
  "rows in the file": 188399,
  "rows marked missing or with no value (set aside)": 0,
  "rows of the kept series": 39891,
  "series-level rows with no time period (not observations)": 1133
 },
 "drought": {
  "countries tried": 234,
  "countries with a drought series": 184
 },
 "ember": {
  "rows of countries with no Natural Earth match (set aside; by month)": {
   "XKX": 220
  },
  "rows of countries with no Natural Earth match (set aside; by year)": {
   "GLP": 115,
   "GUF": 72,
   "MTQ": 67,
   "REU": 112,
   "XKX": 170
  },
  "rows with no generation figure (set aside; by month)": 0,
  "rows with no generation figure (set aside; by year)": 0
 },
 "eurostat_air": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EU27_2007": 157,
   "EU27_2020": 219,
   "EU28": 145,
   "XK": 18
  },
  "of which marked confidential": 0,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 19850,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 9847,
  "rows with no value (set aside)": 0,
  "values equal to zero": 120
 },
 "eurostat_asylum": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EU27_2020": 151
  },
  "of which marked confidential": 0,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 14070,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 7318,
  "rows with no value (set aside)": 0,
  "values equal to zero": 118
 },
 "eurostat_births": {
  "codes set aside because the file holds the longer or whole record (rows)": {
   "DE": 776,
   "FX": 636
  },
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EA20": 144,
   "EA21": 48,
   "EEA30_2007": 270,
   "EEA31": 270,
   "EFTA": 548,
   "EU27_2007": 270,
   "EU27_2020": 336,
   "EU28": 270,
   "XK": 132
  },
  "of which marked confidential": 36,
  "rows flagged as a forecast (set aside)": 62,
  "rows in the file": 30801,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 5009,
  "rows outside the cut (not used)": 0,
  "rows with no value (set aside)": 36,
  "values equal to zero": 0
 },
 "eurostat_deaths": {
  "codes set aside by choice (rows)": {
   "DE": 392,
   "FX": 528
  },
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EA20": 114,
   "EA21": 126,
   "EEA30_2007": 180,
   "EEA31": 168,
   "EFTA": 605,
   "EU27_2007": 228,
   "EU27_2020": 306,
   "EU28": 216,
   "XK": 156
  },
  "rows flagged as a forecast (set aside)": 50,
  "rows in the file": 29754,
  "rows of the year's total or an unknown month (not used)": 4579,
  "rows with no value (set aside)": 42
 },
 "eurostat_electricity": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EU27_2020": 187,
   "XK": 56
  },
  "of which marked confidential": 0,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 7850,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 0,
  "rows with no value (set aside)": 0,
  "values equal to zero": 0
 },
 "eurostat_industry": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {},
  "of which marked confidential": 0,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 30488,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 18637,
  "rows with no value (set aside)": 0,
  "values equal to zero": 0
 },
 "eurostat_retail": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "XK": 12
  },
  "of which marked confidential": 637,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 57842,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 46493,
  "rows with no value (set aside)": 704,
  "values equal to zero": 0
 },
 "eurostat_tourism": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EU25": 72,
   "EU27_2007": 72,
   "EU27_2020": 188,
   "EU28": 72,
   "XK": 91
  },
  "of which marked confidential": 54,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 12446,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 0,
  "rows with no value (set aside)": 90,
  "values equal to zero": 5
 },
 "eurostat_unemployment": {
  "codes set aside because the file holds the longer or whole record (rows)": {},
  "codes with no Natural Earth match: groups of countries and others (set aside; rows)": {
   "EA21": 321,
   "EU27_2020": 321
  },
  "of which marked confidential": 0,
  "rows flagged as a forecast (set aside)": 0,
  "rows in the file": 43071,
  "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": 0,
  "rows outside the cut (not used)": 28503,
  "rows with no value (set aside)": 0,
  "values equal to zero": 0
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
 "hfd_stff": {
  "country codes with no whole-country match (set aside; values)": {
   "CAN_QUE": 309,
   "GBRTENW": 912,
   "GBR_NIR": 802,
   "GBR_SCO": 948
  },
  "rows with births of unknown month (not used)": 36
 },
 "ibtracs": {
  "country-months with a storm": 2387,
  "country-months with a storm but no wind at a position inside (no wind written)": 246,
  "positions in the file": 312366,
  "positions of counted storms in no country's shape, at sea (world series only)": 264707,
  "positions of counted storms outside the span (set aside)": 165,
  "positions on spur tracks (set aside)": 1169,
  "storms in the file": 5017,
  "storms set aside: no USA_WIND, or below 34.0 kt": 877,
  "storms whose strongest USA_WIND reaches 34.0 kt (counted)": 4086
 },
 "indices": {},
 "mass_mobilization": {
  "country codes of states that ended or split (set aside; protests)": {
   "Czechoslovakia": 4,
   "East Germany": 11,
   "USSR": 60,
   "West Germany": 2,
   "Yugoslavia": 36,
   "Yugoslavia, then Serbia and Montenegro": 103
  },
  "country codes with no Natural Earth match (set aside; protests)": {
   "341": 20
  },
  "protests counted": 15003,
  "protests in the file": 15239,
  "protests starting outside a watched country-month (set aside)": 0,
  "protests with no start month (set aside)": 0,
  "rows in the file": 17145
 },
 "opendengue": {
  "countries with no Natural Earth match (set aside; rows)": {
   "BES": 193,
   "GLP": 171,
   "GUF": 149,
   "MTQ": 252,
   "MYT": 10,
   "REU": 7,
   "TKL": 163
  },
  "months with both a month row and whole weeks (the month row kept)": 0,
  "months with some of their weeks missing (not written)": 817,
  "rows by step": {
   "Month": 3166,
   "Week": 22883,
   "Year": 3491
  },
  "rows in the file": 29540,
  "rows whose span is not a whole calendar month, a seven-day week or a calendar year (set aside)": 0,
  "rows with no value (set aside)": 0,
  "years from a year row": 3304,
  "years summed from twelve months": 540,
  "years with both a year row and twelve written months (the year row kept)": 0
 },
 "pink_sheet": {
  "annual prices with no monthly column of the same name (not written)": [],
  "cells marked unavailable (not written; annual)": 421,
  "cells marked unavailable (not written; monthly)": 6216,
  "cells that are not numbers above zero (set aside; annual)": {},
  "cells that are not numbers above zero (set aside; monthly)": {
   "Rice, Thai 25% 1988M08: #VALUE!": 1,
   "Rice, Thai 25% 1989M06: #VALUE!": 1,
   "Rice, Thai 25% 1990M06: #VALUE!": 1,
   "Rice, Thai 25% 2008M02: #VALUE!": 1,
   "Rice, Thai 25% 2008M03: 0": 1,
   "Rice, Thai 25% 2008M04: 0": 1,
   "Rice, Thai 25% 2008M05: 0": 1,
   "Rice, Thai 25% 2008M06: 0": 1
  },
  "index columns left out": [
   "Natural gas index"
  ],
  "prices whose yearly record begins earlier than the monthly (yearly written)": [
   "DAP (1960, monthly from 1967)"
  ]
 },
 "prices": {
  "ISO3 codes with no Natural Earth match (set aside)": []
 },
 "unhcr": {
  "codes with more than one row in a year (their figures summed; rows)": {},
  "codes with no Natural Earth match (set aside; rows)": {
   "GLP (Guadeloupe; by origin)": 10,
   "GUF (French Guiana; by asylum)": 6,
   "GUF (French Guiana; by origin)": 17,
   "MTQ (Martinique; by origin)": 4,
   "TIB (Tibetan; by origin)": 62,
   "UNK (Unknown; by asylum)": 70,
   "UNK (Unknown; by origin)": 75,
   "XXA (Stateless; by origin)": 46
  },
  "rows in the file (by asylum)": 7802,
  "rows in the file (by origin)": 7673
 },
 "usgs_quakes": {
  "earthquakes in the files": 287309,
  "earthquakes of magnitude 5.0 or more, 1973 to 2025": 87867,
  "epicentres in no country's shape, at sea or off the map (world series only)": 69872,
  "epicentres inside a country's shape": 17995
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
