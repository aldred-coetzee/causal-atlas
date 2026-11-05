# 1a: data check

**Rule, from `docs/plan-phase-1.md`.** One table: fetchable without a login, licence, years,
resolution, size, host. Each check rests on the source's own page, fetched 2026-11-05. If fewer
than 80% of events are geocoded to the cell or finer, this goes to the owner. Stop if no
fetchable, licensed outcome source exists. Queries report data shape only: no outcome by place or
period has been computed, and prices have not been joined to anything.

## Result

| Source | Fetchable, no login | Licence, at source | Years | Resolution | Size | Host |
|---|---|---|---|---|---|---|
| UCDP GED 26.1 (outcome) | Yes, fetched | CC BY 4.0, cite listed publications | 1989 to 2025 | Event, point | 39 MB zip | Uppsala University, Sweden |
| SPEI-3, SPEIbase 2.11 (drought) | Yes, fetched | ODbL 1.0, contents DbCL | 1901 to 2024-12 | 0.5 degree, monthly | 383 MB | CSIC, Spain |
| CHIRPS v3 (rainfall, alternative) | Yes by listing, not fetched | Public domain (page is for CHIRPS generally) | 1981 to near present, per page; file not opened | 0.05 degree, monthly | 8.3 GiB | UCSB, USA |
| NOAA ONI (ENSO) | Yes, fetched | Public domain per NWS page; no PSL-specific page found | 1950 to 2026-09 | Global, monthly | 7 KB | NOAA PSL, USA |
| WFP food prices via HDX | **Not fetched: see below** | CC BY-IGO, per HDX metadata | 1990 to 2026, per metadata | Market, monthly | 0.62 GB, 37 yearly files | HDX, files on US-East S3 |
| Natural Earth 1:10m countries (grid) | Yes, fetched | Public domain | Boundaries as released | Vector | 5 MB zip | Natural Earth CDN |

Africa in GED 26.1: 74,836 events. Grid: 10,228 cells with their centre in one of Natural Earth's
55 African countries, within 40S to 40N and 20W to 55E, so Cape Verde and Mauritius are outside.
SPEI sits exactly on these cell centres, with 0.02% of cells missing in 1992-01 and none in 2024-12.

## What this changes

**Finding 1: geocoding misses the 80% line, and goes to the owner.** Events by `where_prec`: exact
50.4%, within 25 km 24.9%, second-order admin unit 10.3%, first-order 7.1%, linear or fuzzy feature
6.4%, country 0.8%. To the cell or finer, strictly, is levels 1 and 2: **75.3%**. Adding level 3,
a district's central point, gives 85.6%, though some of those land in a neighbouring cell.

**Finding 2: food prices may not be fetched by script, and goes to the owner.** HDX's `robots.txt`
disallows `/*.csv$` and `/api/` for all agents, with a crawl delay of 10. A browser-style agent got
an empty 202 challenge on every file; the first run saved 37 empty files, now deleted, and the
downloader now refuses empty bodies. This session called the API and tried downloads before reading
`robots.txt`. No price data is held, so the staple list, H2's coverage number and H2's shift count
that the plan and audit asked for cannot be given.

**Finding 3: SPEI ends a year before the outcome.** With a 3-month lead, the last forecastable month
is 2025-03, so E in the split rule must be the last target month with its inputs, not the last month
of the outcome. Blocks: train 1992-01 to 2017-03, validation 2017-04 to 2021-03, held-out 2021-04 to
2025-03. That is 399 months and about 4.08M rows. Nine months of outcome go unused.

**Finding 4: the ONI leaks a month if used as planned.** PSL describes it as a 3-month running mean.
If centred, as the source's description is read here, the value for month t uses month t+1. Features
must therefore use ONI at t-1, not t.

**Finding 5: SPEI over CHIRPS.** Both pass, and a European host breaks the tie, as the plan says.
Its ODbL is share-alike, with Produced Works exempt (4.5b). Publicly using a work from a derivative
database requires offering the database or the method of alteration (4.6b), which the public scripts
do; results need an ODbL notice. MIT on code is untouched. **Limit:** the file's metadata shows it
is built from CRU TS. How well station data covers Africa has not been checked, and thin coverage
would weaken any drought signal, biasing H1 towards "no".

**Finding 6: shifts.** Drought and ONI have 33 whole years in the panel, so 32 circular shifts,
smallest p = 1/33, about 0.030. That misses Bonferroni's 0.025 and meets 0.05, so it matters whether
H2 survives finding 2.

**Other limits.** GED requires at least one death for an event to exist (codebook), so this measures
fatal events only. Months: 4.3% of events span a month boundary, and 8.8% have a date known only to
a month or wider (`date_prec` 4 and 5); events are assigned by `date_start`. Actor names and source
text, which can name people, are dropped at ingest and never published.

No interval applies here: these are counts over the frozen files.
