# Money, births and deaths by country and month: three sources

Read, fetched and counted on 2026-11-11 for the brief in `docs/specs/2026-11-11-parallel-helpers.md` (part B). Fetch: `scripts/fetch_money_people.py`. Adapters: `src/causal_atlas/adapters_money_people.py`, tested on made-up files in `tests/test_adapters_money_people.py`. Nothing here sets one real series beside another; every count below is one series alone, counted by the adapters from the files fetched that day. Places are matched through Natural Earth's two-letter codes (ISO_A2, else ISO_A2_EH) or three-letter codes, by the code rule `table.natural_earth` uses; no two-letter code is claimed by two places.

## 1. BIS statistics, bulk files

**Address.** List of bulk files: https://data.bis.org/bulkdownload ; each file at `https://data.bis.org/static/bulk/WS_<NAME>_csv_flat.zip`. The list holds all five asked for (and others, such as DPP, CPP, XRU, not taken).

**Licence**, read at https://data.bis.org/help/legal : "The use of the statistics is unrestricted, provided that: if the statistics are reproduced, the BIS must be cited in your publication or product as the source of the statistics; if the statistics will be translated into another language, a statement must be included ... that the translation is not an official BIS translation; your use of the statistics must not be potentially misleading, for example by implying endorsement or affiliation with the BIS or any body affiliated with the BIS; if the statistics will be used in a commercial publication or product, their inclusion ... will not result in any additional charge to subscribers or other users; the BIS does not warrant or guarantee the accuracy, completeness or fitness for any contemplated purpose ... nothing in these statistics shall be construed as containing any investment recommendation or advice. No other use is permissible. The BIS reserves the right to alter these terms at any time." The same page: "Most of the data sets rely on national statistics as communicated to the BIS by central banks and other national authorities".

**What "No other use is permissible" rules out**, as read here: it closes the list of conditions; it does not narrow the use, which is "unrestricted". A use that breaks a condition is the use ruled out: reproducing the figures without naming the BIS as source, implying the BIS endorses or is linked to the project, presenting them misleadingly, or charging extra for them. For a public, non-commercial project that keeps the files on its own machine and publishes findings: keeping and analysing the files is permitted; publishing findings and any figures reproduced is permitted with the BIS cited as source and no suggestion of endorsement; findings must not read as investment advice. Not settled by the text: whether committing the raw files to a public repository is "reproducing" (it would be permitted with citation, but the project does not commit data anyway), and the terms can change without notice, so the date read matters. The page gives no citation form; "Source: BIS" with the data set's name and the date fetched meets the condition as written.

**Fetched** 2026-11-11, zips stamped 4 November 2026; each unpacked beside it.

| File | Bytes | SHA-256 |
|---|---|---|
| WS_CBPOL_csv_flat.zip | 4,145,567 | 2306f25a53c31cf97edb4959630e0ea7414cbbb260443d4c7a614daf9540c81f |
| WS_LONG_CPI_csv_flat.zip | 873,148 | 9310d01a9eeffcba9940a294d1181b61a1ab57cf565f5b1a878e2bb00b447be6 |
| WS_SPP_csv_flat.zip | 305,666 | a5dd4cc029e805031d94033bdebc245b64bf624757bae9d5b4033c8591f11694 |
| WS_TC_csv_flat.zip | 1,814,797 | 30b65b768707ef67e2e12f9705d1588079d9663d7519840bc15883b6a69608e8 |
| WS_EER_csv_flat.zip | 6,630,897 | f71d708847132a94aefb3b18d4d637a3f7cf0c8517ee069e2263950f6f3820a0 |

**Series kept, their kind and transform, and coverage** (places, first and last period, values). A price or exchange-rate index is `level`/`log`, as `table.faostat_cp` treats a price index; a per cent is `rate`/`none`, as `table.wdi_shape` treats one. The two rules disagree on an index (`wdi_shape` makes a name holding "index" `index`/`none`); `faostat_cp` was followed because these are price indices like its own, and the project session should choose. Flags: BIS status E is `estimated`, B (break) is `other`, A none; M and H (missing) rows are set aside.

| Series | Kind / transform | Places | First – last | Values |
|---|---|---|---|---|
| bis_cbpol:policy_rate (end of month, %) | rate / none | 48 | 1945-01 – 2026-10 | 24,779 |
| bis_long_cpi:cpi_index (month) | level / log | 62 | 1913-01 – 2026-09 | 47,830 |
| bis_long_cpi:cpi_index:year | level / log | 62 | 1661 – 2025 | 4,758 |
| bis_spp:nominal_index (mean of four quarters) | level / log | 57 | 1927 – 2025 | 2,158 |
| bis_tc:private_nonfinancial (% GDP, Q4) | rate / none | 43 | 1947 – 2025 | 2,327 |
| bis_tc:private_nonfinancial_banks | rate / none | 43 | 1947 – 2025 | 2,304 |
| bis_tc:households | rate / none | 43 | 1947 – 2025 | 1,687 |
| bis_tc:nonfinancial_corporations | rate / none | 43 | 1947 – 2025 | 1,669 |
| bis_tc:government_nominal | rate / none | 42 | 1947 – 2025 | 1,408 |
| bis_eer:nominal_broad / real_broad | level / log | 63 | 1994-01 – 2026-09 | 24,759 each |
| bis_eer:nominal_narrow | level / log | 25 | 1964-01 – 2026-09 | 18,825 |
| bis_eer:real_narrow | level / log | 26 | 1964-01 – 2026-09 | 19,578 |

Set aside and counted in each part's notes: groups of economies (euro area XM in every file; 4T, 5A, 5R, G2, XW in some), series-level rows with no period (271 in EER, 1,133 in TC), missing rows (53 policy rates, 457 CPI months), 62 property-price years with fewer than four quarters.

**Choices the project session should check.** Property prices and credit are quarterly only, so each was made yearly: property prices as the mean of the year's four quarters (years with all four only), credit as the fourth quarter's end-of-period ratio; placing quarters on months is the alternative. Left out because each can be made from what is kept or the table already holds it: real property prices (nominal over consumer prices), the CPI's year-on-year per cent, credit to the whole non-financial sector (private plus government). Ties a steward should bar when choosing rows: private credit and its two parts (households, corporations) and its bank part; nominal and real, broad and narrow exchange rates; the monthly and yearly CPI.

**Known biases.** National figures passed on by central banks; long CPI and property-price series are spliced from older national sources by the BIS. Euro-area members' policy rates end in 1998-12 (Germany, France, Italy, Spain checked); from 1999 the rate is the euro area's, held under XM and set aside here, so euro members have no policy rate after 1998 unless the project copies the euro-area rate to them. The yearly CPI reaches 1661 for Britain and before 1900 for a few others; most begin in the 20th century. Broad exchange-rate baskets begin in 1994. The address carries no release; a later fetch may revise every value.

## 2. Human Fertility Database, Short-Term Fertility Fluctuations

**Address.** https://www.humanfertility.org/Data/STFF ; files `https://www.humanfertility.org/File/GetDocumentFree/STFF/stff.csv` (crude) and `.../stffadj.csv` (seasonally and calendar adjusted, from 2012). No account needed.

**Licence**, read at the STFF page: "STFF data are published under CC BY 4.0 license". The User Agreement (https://www.humanfertility.org/Data/UserAgreement) adds that this "is not the case for the input data which remains under each provider's distribution license", which "should not be used for commercial gain or re-published ... without the explicit permission"; so the input-data archive (STFFinput.zip) was not fetched. The STFF page says the data are preliminary, subject to revision, updated twice a year, last 02-03-2026.

**Citation** asked for (https://www.humanfertility.org/Data/CitationGuidelines): "Human Fertility Database. Max Planck Institute for Demographic Research (Germany) and Vienna Institute of Demography (Austria). Available at www.humanfertility.org (data downloaded on [date])."

**Fetched** 2026-11-11: stff.csv 163,452 bytes, SHA-256 92715a16e7708ef9741b80c4db66b31549f4e41e390366995e9a2ec238c8a981; stffadj.csv 75,144 bytes, SHA-256 d3cd2d2b8acdc501c7bb386a99b3d02bf63456dc8ffdfed44e1ca9d829b95077.

| Series | Kind / transform | Places | First – last | Values |
|---|---|---|---|---|
| hfd_stff:births | count / log1p | 43 | 2000-01 – 2025-12 | 13,059 |
| hfd_stff:tfr | rate / none | 29 | 2000-01 – 2025-11 | 8,755 |
| hfd_stff:births_adjusted | level / log | 29 | 2012-01 – 2025-11 | 4,705 |
| hfd_stff:tfr_adjusted | rate / none | 29 | 2012-01 – 2025-11 | 4,705 |

Births are a count, so a month with zero is a zero and a '.' is no value; adjusted births are a model's output, not a count, so `level`. The crude fertility rate is '.' throughout for 14 whole countries that have births (Bulgaria, Chile, Estonia, Greenland, Croatia, Iceland, Luxembourg, New Zealand, Romania, Singapore, Serbia, Slovakia, Taiwan, Ukraine), hence 29 places against 43. Set aside: parts of countries (Quebec 309, Northern Ireland 802, Scotland 948, England and Wales 912 values); 36 rows with births of unknown month (not spread over months). DEUTNP, FRATNP and GBR_NP are taken as Germany, France and the United Kingdom.

**Known biases.** Preliminary figures, revised later; the start year differs by country; births by month of occurrence or of registration may differ by country (not checked); adjusted series and the fertility rate are the database's estimates.

## 3. Eurostat deaths by month

**Found at source.** A table by country and month exists: `demo_mmonth`, "Deaths (total) by month", 1960–2025, updated 2026-09-23, beside the weekly tables (`demo_r_mwk_ts` by sex from 2000, `demo_r_mweek3` by region). It is the longest record by country and month and was taken. (`demo_fmonth`, live births by month, 1960–2025, also exists and was not fetched.) Address: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_mmonth?format=SDMX-CSV`.

**Licence**, read at https://ec.europa.eu/eurostat/help/copyright-notice : "Reuse of statistical data, metadata, publications, and other dissemination tools published on this website for commercial or non-commercial purposes is authorised provided the source is acknowledged." Changes must be stated, and Eurostat is not to be held responsible for them. The exception: "The following Eurostat data and documents may not be reused for commercial purposes, but non-commercial reuse is possible without restriction: ... Data for countries other than: Member States of the European Union (EU), Member States of the European Free Trade Association (EFTA), official EU acceding and candidate countries. Examples are data for the United States of America, Japan or China." The file holds such countries (among AD, AL, AM, AZ, BA, BY, GE, MC, MD, ME, MK, RS, RU, SM, TR, UA, XK, UK, those not candidates; the candidate list was not read at source). The exception bars only commercial reuse, so it does not restrict this project; it would bind anyone reusing the project's outputs commercially. Citation: the notice asks only that the source be acknowledged ("Source: Eurostat, demo_mmonth", with the date).

**Fetched** 2026-11-11: demo_mmonth.csv, 1,984,573 bytes, SHA-256 9bc9d5582e3a2301cf0dac8ae9a06abdf94c2e6a61141e6d24535d616765a363.

**Coverage**: `eurostat_deaths:deaths`, count / log1p, 48 places, 1960-01 to 2025-12, 22,064 values (222 flagged; 44 places with 120 months or more). Flags: e is `estimated`, any other (p provisional, b break) `other`. Set aside: 4,579 year-total and unknown-month rows, 42 with no value, 50 forecast rows (flag f, all in 2025: Georgia, Moldova, North Macedonia, Serbia, Turkey, Finland, Malta, Bulgaria, Lithuania), groups of countries (EA20, EA21, EEA30_2007, EEA31, EFTA, EU27_2007, EU27_2020, EU28), Kosovo (no Natural Earth country code). By choice: DE (Germany from 1991, 392 rows) in favour of DE_TOT (Germany including the former GDR, from 1960), and FX (metropolitan France, 1960–2012, 528 rows) in favour of FR (1995–2025). EL is Greece, UK the United Kingdom.

**Known biases.** France's record is short (1995 on) because the longer one is metropolitan France only; taking FX before 1995 would join two territories. The United Kingdom ends in 2019. Recent months are provisional and revised. Deaths are by month of occurrence as Eurostat collects them from national offices; definitions were not checked country by country.

## Proposed entries for `data/manifest.toml` (not edited)

```toml
[bis_cbpol]
source_url = "https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip"
fetch_script = "scripts/fetch_money_people.py"
version = "BIS bulk file, flat CSV, zip stamped 2026-11-04; the address carries no release"
licence = "BIS terms (https://data.bis.org/help/legal, read 2026-11-11): use 'unrestricted, provided that' the BIS is cited as source, use is not misleading or implying endorsement, no extra charge in a commercial product; 'No other use is permissible'; terms may change at any time. Cite: Source: BIS, central bank policy rates, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "2306f25a53c31cf97edb4959630e0ea7414cbbb260443d4c7a614daf9540c81f"
coverage = "4,145,567 bytes. Monthly policy rate, end of month: 48 places, 1945-01 to 2026-10, 24,779 values; euro area (XM) and 53 missing rows set aside"
known_biases = "National figures passed on by central banks. Euro-area members end 1998-12; the euro-area rate from 1999 is under XM and not given to members. A new release replaces the file at the same address"

[bis_long_cpi]  # as bis_cbpol, with:
source_url = "https://data.bis.org/static/bulk/WS_LONG_CPI_csv_flat.zip"
sha256 = "9310d01a9eeffcba9940a294d1181b61a1ab57cf565f5b1a878e2bb00b447be6"
coverage = "873,148 bytes. CPI index (2010 = 100): monthly 62 places, 1913-01 to 2026-09, 47,830 values; yearly 62 places, 1661 to 2025, 4,758 values; year-on-year per cent not used"
known_biases = "Spliced by the BIS from older national series; very early years for few countries"

[bis_spp]  # as bis_cbpol, with:
source_url = "https://data.bis.org/static/bulk/WS_SPP_csv_flat.zip"
sha256 = "a5dd4cc029e805031d94033bdebc245b64bf624757bae9d5b4033c8591f11694"
coverage = "305,666 bytes. Nominal residential property price index, quarterly, made yearly as the mean of four quarters: 57 places, 1927 to 2025, 2,158 values; 62 incomplete years and groups set aside; real index not used"
known_biases = "National methods differ (coverage of dwellings, regions, new or existing); spliced long series"

[bis_tc]  # as bis_cbpol, with:
source_url = "https://data.bis.org/static/bulk/WS_TC_csv_flat.zip"
sha256 = "30b65b768707ef67e2e12f9705d1588079d9663d7519840bc15883b6a69608e8"
coverage = "1,814,797 bytes. Credit as per cent of GDP, adjusted for breaks, fourth-quarter value: five series, 42 to 43 places, 1947 to 2025, 1,408 to 2,327 values each"
known_biases = "Private credit contains households, corporations and the bank part: tied series. Start years differ widely by country"

[bis_eer]  # as bis_cbpol, with:
source_url = "https://data.bis.org/static/bulk/WS_EER_csv_flat.zip"
sha256 = "f71d708847132a94aefb3b18d4d637a3f7cf0c8517ee069e2263950f6f3820a0"
coverage = "6,630,897 bytes. Effective exchange rates (2020 = 100), monthly averages: broad nominal and real 63 places, 1994-01 to 2026-09, 24,759 values each; narrow nominal 25 places and real 26, from 1964-01"
known_biases = "Four tied series; broad baskets only from 1994; euro area set aside"

[hfd_stff]
source_url = "https://www.humanfertility.org/File/GetDocumentFree/STFF/stff.csv and .../stffadj.csv"
fetch_script = "scripts/fetch_money_people.py"
version = "STFF, last updated 02-03-2026 per https://www.humanfertility.org/Data/STFF; preliminary, updated twice a year"
licence = "CC BY 4.0 ('STFF data are published under CC BY 4.0 license', https://www.humanfertility.org/Data/STFF, read 2026-11-11); input data not fetched (provider licences, https://www.humanfertility.org/Data/UserAgreement). Cite: Human Fertility Database. Max Planck Institute for Demographic Research (Germany) and Vienna Institute of Demography (Austria). Available at www.humanfertility.org (data downloaded on 11 November 2026)."
fetched = "2026-11-11"
sha256 = "stff.csv 92715a16e7708ef9741b80c4db66b31549f4e41e390366995e9a2ec238c8a981; stffadj.csv d3cd2d2b8acdc501c7bb386a99b3d02bf63456dc8ffdfed44e1ca9d829b95077"
coverage = "163,452 and 75,144 bytes. Births by month 43 places 2000-01 to 2025-12, 13,059 values; crude TFR 29 places, 8,755; adjusted births and TFR 29 places 2012-01 to 2025-11, 4,705 each. Parts of countries and births of unknown month set aside"
known_biases = "Preliminary and revised; start years differ; 14 countries have births but no crude TFR; adjusted series are the database's model output"

[eurostat_deaths]
source_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_mmonth?format=SDMX-CSV"
fetch_script = "scripts/fetch_money_people.py"
version = "demo_mmonth, Deaths (total) by month, updated 2026-09-23"
licence = "Eurostat copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice, read 2026-11-11): reuse 'for commercial or non-commercial purposes is authorised provided the source is acknowledged'; data for countries outside the EU, EFTA and acceding and candidate countries 'may not be reused for commercial purposes, but non-commercial reuse is possible without restriction'. Cite: Source: Eurostat, demo_mmonth, fetched 2026-11-11"
fetched = "2026-11-11"
sha256 = "9bc9d5582e3a2301cf0dac8ae9a06abdf94c2e6a61141e6d24535d616765a363"
coverage = "1,984,573 bytes. Deaths by month: 48 places, 1960-01 to 2025-12, 22,064 values (44 places with 120 months or more); totals, unknown months, forecasts, groups, Kosovo, DE (for DE_TOT) and FX (for FR) set aside"
known_biases = "France from 1995 only; United Kingdom ends 2019; recent months provisional; some countries outside the EU are under the non-commercial exception"
```
