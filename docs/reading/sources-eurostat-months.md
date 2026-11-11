# Eurostat by country and month: eight tables of eight kinds

Read, fetched and counted on 2026-11-11 for the brief in `docs/specs/2026-11-11-parallel-helpers-second-wave.md` (part D). Fetch: `scripts/fetch_eurostat_months.py`. Adapter: `src/causal_atlas/adapters_eurostat.py` (one function, `eurostat_months`, and the cut of each table in `TABLES`), tested on made-up files in `tests/test_adapters_eurostat.py`. Every table code was answered for by the API's list of tables (`https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/all`) and its title below is the API's. Nothing here sets one real series beside another; every count is one series alone, counted by the adapter from the file. Places go through Natural Earth's two-letter codes as `adapters_money_people.iso2_codes` matches them (EL is GR, UK is GB). Building permits (`sts_cobp_m`) was not taken: it holds an index only, for 16 countries.

**The cut rule** (written in the brief before any file was opened): the total over every breakdown; counts as counted, not seasonally adjusted; an index only where no count exists, then unadjusted; where the rule does not settle it, the cut with the most country-months. **A missing month is nothing, not a zero, in all eight**: Eurostat leaves out the row where it has no figure and writes a 0 where it counted none (tourism holds 5 zeros, air 120, asylum 118). So every series is of kind `level` (transform `log` if every value is above zero, else `log1p`), never `count`, whose missing months the table would fill with zeros. **Changed on taking this in:** `eurostat_deaths` and the crude births of the Human Fertility Database (part B), and the protest and dengue series (part A), were of kind `count`; a period with no row is nothing in each, so they are now `level` with the same transform. `count` is kept for series where a period with no row is a zero (the conflict events) or where every period is written (earthquakes).

**What is set aside, in every table:** rows outside the cut; a year's total, an unknown month, a quarter or a year; rows with no value (confidential ones counted among them); forecasts (flag f); groups of countries and Kosovo (no Natural Earth code); DE when the file also holds DE_TOT, FX when it also holds FR. Flags: any holding e is `estimated`, any other `other`.

| Table | Title (API) | Cut kept | Places | First, last month | Values |
|---|---|---|---|---|---|
| une_rt_m | Unemployment by sex and age - monthly data | thousand persons, all ages (TOTAL), both sexes, NSA | 36 | 1983-01, 2026-10 | 13,926 |
| sts_inpr_m | Production in industry - monthly data | PRD, NACE B-D, NSA, index 2021=100 | 36 | 1975-01, 2026-09 | 11,851 |
| sts_trtu_m | Turnover and volume of sales in wholesale and retail trade - monthly data | NETTUR, NACE G47, NSA, index 2021=100 | 36 | 1994-01, 2026-09 | 10,633 |
| nrg_cb_em | Electricity supply, transformation and consumption - monthly data | AIM (available to internal market), E7000, GWh | 39 | 2008-01, 2026-09 | 7,607 |
| tour_occ_nim | Nights spent at tourist accommodation establishments - monthly data | all residences, nights, I551-I553 | 38 | 1990-01, 2026-09 | 11,861 |
| avia_paoc | Air passenger transport by type of schedule, transport coverage and country | passengers on board (PAS_BRD), all coverage and schedules | 36 | 1993-01, 2026-09 | 9,464 |
| migr_asyappctzm | Asylum applicants by type, citizenship, age and sex - monthly data | first-time (FRST), all citizenships, ages, both sexes | 33 | 2008-01, 2026-10 | 6,601 |
| demo_fmonth | Live births (total) by month | number, months M01 to M12 | 48 | 1960-01, 2025-12 | 21,994 |

**Why each cut, and the choices the rule did not settle** (each alternative counted alone, in values): unemployment is a count, so NSA is fixed by the rule although SA has more (14,527; TC 12,704). Industry and retail have no count, so an unadjusted index; the base year was not settled by the rule: I21 11,851 against I15 10,657 (ends 2023-12) and I10 7,836 for industry. Retail: value (NETTUR) or volume (VOL_SLS) was not settled: NETTUR I21 10,633, VOL_SLS I21 10,573, I15 10,147 and 10,087. Energy: electricity or gas was not settled: electricity AIM 7,607 against gas inland consumption in TJ 7,397 (`nrg_cb_gasm`, probed, not kept). Air: on board or carried was not settled: PAS_BRD 9,464, PAS_CRD 9,308. Asylum: first-time is the kind the brief names, though all applicants hold more (7,155).

**Known biases, from each table's own notes** (`https://ec.europa.eu/eurostat/cache/metadata/en/<page>.htm`, read 2026-11-11). *une_rt_m_esms*: "Time series breaks caused by major revisions are flagged until break-free data is provided"; "Data are considered to be final after 6 months"; several countries are monthly estimates joining the quarterly survey to registered unemployment; France changed method in January 2025 and Germany was revised back to 2009. Germany is unadjusted only from 2007, the UK ends 2020-09. *sts_esms*: comparability "is considered to be very good since the year 2000"; "Time series breaks caused by major revisions are flagged"; rebased to 2021 = 100 in 2024 and all series rescaled; the UK kept "until 2020; those data are not revised and not updated". Retail holds Sweden only from 2023, Ireland from 2021 (industry from 2016). *nrg_prd_esms*: "Occasional breaks in time series are present"; provisional months are replaced. *tour_occ_esms*: "breaks can be observed between the reference periods 2011 and 2012"; national thresholds on small establishments "jeopardizes the comparability of the data". *avia_pa_esms*: passengers on board "Includes direct transit passengers (counted at arrivals and departures)", so a country's total counts a domestic passenger twice; "As from 2003 the statistics on air transport are comparable over time"; airports under 15 000 passenger units a year are left out, a break when one crosses it. *migr_asyapp_esms*: "Data are rounded to the nearest 5"; Bulgaria from 2011, France from 2009, Austria held from 2014; definition changed in 2014, 2021 and July 2026 (registered in place of lodged applicants); the UK "until November 2020"; Spain provisional since 2025-03. *demo_fer_esms*: births by "month of occurrence"; "no routine revisions" align the months to the year's total; France here is FR (with the overseas departments) from 1994, metropolitan FX set aside.

**Non-commercial exception** (the copyright notice, read by part B; not read again here): countries outside the EU, EFTA and the acceding and candidate countries. The nine candidates by Eurostat's glossary: Albania, Bosnia and Herzegovina, Georgia, Moldova, Montenegro, North Macedonia, Serbia, Türkiye, Ukraine. Under it: the United States and Japan (unemployment); Andorra, Armenia, Azerbaijan, Belarus, Monaco, Russia and San Marino (births); and perhaps the United Kingdom in all eight (it was a member for most of the months held): not settled.

## Proposed entries for `data/manifest.toml`

```toml
[eurostat_unemployment]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/une_rt_m/M..TOTAL.THS_PER.T.?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat une_rt_m, 'Unemployment by sex and age - monthly data'; the file's own stamp of its last update reads 2026-11-05. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Here: the United States and Japan; whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, une_rt_m, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "55e350ccf46f58f064a0c429b99cdf8bddea0639fc42ddd0e1730ffab4a2453a"
coverage = "3,344,238 bytes. Unemployed persons, thousands, all ages, both sexes, not seasonally adjusted: 36 places, 1983-01 to 2026-10, 13,926 values, 35 places with 120 months or more. The file also holds the seasonally adjusted and trend series, not used. Set aside: EA21, EU27_2020"
known_biases = "Breaks from major revisions are flagged; months are final after six; several countries join the quarterly survey to registered unemployment; France changed method in January 2025, Germany revised back to 2009 and unadjusted only from 2007; the United Kingdom ends 2020-09, Switzerland begins 2010. Some countries fall under the notice's non-commercial exception"

[eurostat_industry]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/sts_inpr_m/M.PRD.B-D.NSA..?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat sts_inpr_m, 'Production in industry - monthly data'; the file's own stamp of its last update reads 2026-11-11. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, sts_inpr_m, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "2b3c3bc1e04324338daa652b1384404025fb0ff03fdf9023a279468fd3b27a7e"
coverage = "2,361,569 bytes. Industrial production (NACE B to D), volume index 2021 = 100, unadjusted: 36 places, 1975-01 to 2026-09, 11,851 values, 35 places with 120 months or more. The file also holds the 2015 and 2010 bases, not used"
known_biases = "An index, not a count. Comparability very good since 2000 by Eurostat's notes; breaks from major revisions are flagged; rescaled to 2021 = 100 in 2024; the United Kingdom stops in 2020 and is not revised; Ireland begins 2016, Ukraine 2021"

[eurostat_retail]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/sts_trtu_m/M..G47.NSA..?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat sts_trtu_m, 'Turnover and volume of sales in wholesale and retail trade - monthly data'; the file's own stamp of its last update reads 2026-11-11. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, sts_trtu_m, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "af9d655625105df3934709abcf9b4c53aeb9919f19ea5c6a11763eaad15670bd"
coverage = "4,678,302 bytes. Net turnover of retail trade (NACE G47), value index 2021 = 100, unadjusted: 36 places, 1994-01 to 2026-09, 10,633 values, 33 places with 120 months or more. The file also holds volume of sales and other bases, not used. Set aside: 704 rows with no value (637 confidential), Kosovo"
known_biases = "An index of value, so prices move it. Comparability very good since 2000 by Eurostat's notes; breaks from major revisions are flagged; rescaled to 2021 = 100 in 2024; Sweden only from 2023, Ireland from 2021; the United Kingdom stops in 2020"

[eurostat_electricity]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nrg_cb_em/M.AIM.E7000.GWH.?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat nrg_cb_em, 'Electricity supply, transformation and consumption - monthly data'; the file's own stamp of its last update reads 2026-11-09. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, nrg_cb_em, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "10520f65a7adcd7309eb872faf72f694a884773a4af15358c9698d3a84d32d6c"
coverage = "614,007 bytes. Electricity available to the internal market, GWh: 39 places, 2008-01 to 2026-09, 7,607 values (84 estimated), 34 places with 120 months or more. Set aside: EU27_2020, Kosovo"
known_biases = "Occasional breaks from changes in national statistics; recent months provisional and replaced. Ukraine 2017-10 to 2022-01 only, the United Kingdom to 2020-10, Iceland 2012-09 to 2024-10"

[eurostat_tourism]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tour_occ_nim/M.TOTAL.NR.I551-I553.?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat tour_occ_nim, 'Nights spent at tourist accommodation establishments - monthly data'; the file's own stamp of its last update reads 2026-11-04. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, tour_occ_nim, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "9e4ef6a0f82cd341bee24d984ae8a25f43f40660f8ee94109394c5160486f2b1"
coverage = "1,058,340 bytes. Nights at hotels, holiday and short-stay accommodation and camping grounds, residents and non-residents: 38 places, 1990-01 to 2026-09, 11,861 values (189 estimated, 5 zeros), 35 places with 120 months or more. Set aside: 90 rows with no value (54 confidential), groups of countries, Kosovo"
known_biases = "Breaks between 2011 and 2012; national thresholds on small establishments harm comparability; Moldova holds six months; the United Kingdom ends 2020-07"

[eurostat_air]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/avia_paoc/M.PAS.PAS_CRD+PAS_BRD.TOTAL.TOTAL.?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat avia_paoc, 'Air passenger transport by type of schedule, transport coverage and country'; the file's own stamp of its last update reads 2026-11-06. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, avia_paoc, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "5ed43fea6b0cd7e2dbc694dce63eda44693e1a79037c75952779282e2a476e49"
coverage = "1,727,332 bytes. Passengers on board at the country's reporting airports, all flights: 36 places, 1993-01 to 2026-09, 9,464 values (120 zeros), 35 places with 120 months or more. The file also holds passengers carried, not used. Set aside: groups of countries, Kosovo"
known_biases = "On board counts direct transit at arrival and departure, and a domestic passenger at both ends; comparable over time only from 2003; airports under 15 000 passenger units a year left out, with breaks as airports cross that line; the United Kingdom 1998-01 to 2020-01"

[eurostat_asylum]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/migr_asyappctzm/M.PER.TOTAL.T.FRST+TOTAL.TOTAL.?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat migr_asyappctzm, 'Asylum applicants by type, citizenship, age and sex - monthly data'; the file's own stamp of its last update reads 2026-11-10. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, migr_asyappctzm, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "647bbf7c1b46cd35130574d4537e5a5e99df317a8c24e2b1ba3f9ad21348ddec"
coverage = "1,248,845 bytes. First-time asylum applicants, all citizenships, ages and both sexes, by the country applied in: 33 places, 2008-01 to 2026-10, 6,601 values (118 zeros), 32 places with 120 months or more. The file also holds all applicants, not used. Set aside: EU27_2020"
known_biases = "Rounded to the nearest 5; definitions changed in 2014, 2021 and July 2026 (registered in place of lodged applicants); Bulgaria from 2011, France from 2009, Austria held from 2014; the United Kingdom to 2020-11; Spain provisional since 2025-03"

[eurostat_births]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_fmonth?format=SDMX-CSV"
fetch_script = "scripts/fetch_eurostat_months.py"
version = "Eurostat demo_fmonth, 'Live births (total) by month'; the file's own stamp of its last update reads 2026-09-30. The address carries no release"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged', except that data for countries outside the EU, EFTA and the acceding and candidate countries 'may not be reused for commercial purposes'. Here: Andorra, Armenia, Azerbaijan, Belarus, Monaco, Russia and San Marino; whether the United Kingdom's figures fall under it was not settled. Cite: Source: Eurostat, demo_fmonth, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "b80fc4e8273e4efc640be91415db0ac9a89c82a4d9efb72dc90a6f2908c010b4"
coverage = "2,060,783 bytes. Live births by month of occurrence: 48 places, 1960-01 to 2025-12, 21,994 values, 44 places with 120 months or more. Set aside: the year's totals and unknown months (5,009 rows), 36 rows with no value, 62 forecasts, groups of countries, Kosovo, DE (Germany from 1991) for DE_TOT (the same territory from 1960), FX (metropolitan France) for FR (from 1994)"
known_biases = "Europe and its neighbours only. Months are not revised to the year's total; France begins in 1994; the United Kingdom ends 2019-06. Births by month overlap the Human Fertility Database's births already held. Some countries fall under the notice's non-commercial exception"
```
