# Four sources of kinds the table lacks, for most of the world

These were read at source and fetched on 2026-11-11 by `scripts/fetch_world_kinds.py`. They are shaped by `src/causal_atlas/adapters_world_kinds.py` and tested in `tests/test_adapters_world_kinds.py`. Each source sits in its own folder under `data/raw/`.

Coverage below is counted from the files, one series at a time. Nothing here sets one series beside another.

The cut was fixed before any file was opened:
- totals and physical quantities as the source gives them;
- no figure per head or per unit of output;
- a monthly record where one exists, and the yearly one beside it only where it reaches further back.

All four sources are usable now. Two caveats:
- the World Bank's terms leave room for third-party restrictions, and its catalogue record could not be read;
- whether a table derived from any of these may be published is the owner's call.

**Places.** Natural Earth holds no separate place for Kosovo (XKX), French Guiana (GUF), Guadeloupe (GLP), Martinique (MTQ) or Réunion (REU). Rows under those codes are set aside and counted. They are not added to Serbia or to France.

## 1. UNHCR Refugee Population Statistics Database

- **Address.** The population API, `https://api.unhcr.org/population/v1/population/`. It was called twice, with `limit=100000&yearFrom=1951&yearTo=2026`: once with `coo_all=true` (by country of origin) and once with `coa_all=true` (by country of asylum). The API's documentation describes this endpoint as "UNHCR data on displacement at the end of the year".
- **Licence.** Taken from UNHCR's terms of use for datasets at https://www.unhcr.org/terms-use-datasets. The live page answers 403 to a script, so it was read in the archive's copy of 2024-04-24 (https://web.archive.org/web/20240424001504id_/https://www.unhcr.org/terms-use-datasets).
  - Point 1 says the datasets are "licensed under a Creative Commons Attribution International License 4.0 (the "CC BY License")".
  - Point 6 says: "Some datasets and indicators are provided by third parties, and may not be shared, redistributed or reused without the consent of the original data provider". The population figures are UNHCR's own. The methodology page says the data "is sourced primarily from governments and also from UNHCR operations".
- **Citation asked for.**
  - Attribution to "UNHCR Refugee Population Statistics Database" (terms, point 3).
  - The address of the terms is to go with anything shared (terms, point 4).
- **Fetched (2026-11-11).**

  | File | Bytes | SHA-256 |
  |---|---|---|
  | `unhcr/population_by_origin.json` | 2,062,501 | `db81c8140e617a51caec61f0de2c3794215ccc401e004d2f77063ccb5bda25ca` |
  | `unhcr/population_by_asylum.json` | 2,103,954 | `0396ef6f0aa8b68b402346cfbaf7b0b02ba59ecca6b9b00bd19d1d850aa5b50a` |

  The two files hold 7,673 rows (origin) and 7,802 rows (asylum), one row per country and year.
- **Shape.** Four yearly series: refugees under UNHCR's mandate, and asylum seekers (pending cases), each by country of origin and by country of asylum.
  - The source has a row for a country-year only where some figure is not zero.
  - A year with no row is written as nothing. The API does not say whether such a country had no refugees or was not reported.
  - A "0" in a row is written as 0, and a "-" is no figure.
- **Asylum seekers begin in 1993.** In both files, no asylum seeker figure other than "0" appears before 1993. Before then there are 1,487 rows of "0" by origin and 2,442 by asylum. Those early zeros are read as "not collected", so both asylum seeker series begin in 1993.
- **Places set aside.** These are codes that name no country, or have no Natural Earth place:
  - by origin: unknown (UNK) 75 rows, Tibetan (TIB) 62, stateless (XXA) 46, GUF 17, GLP 10, MTQ 4;
  - by asylum: UNK 70, GUF 6;
  - no repeated rows.
- **Coverage.**

  | Series | Places | Years | Values |
  |---|---|---|---|
  | Refugees, by origin | 211 | 1960–2025 | 7,459 |
  | Refugees, by asylum | 194 | 1951–2025 | 7,726 |
  | Asylum seekers, by origin | 211 | 1993–2025 | 6,057 |
  | Asylum seekers, by asylum | 192 | 1993–2025 | 5,330 |

  - Refugees by origin, places reporting: 30 in 1970, 55 in 1980, 93 in 1990, 180 in 2000, 203 in 2025.
  - Refugees by asylum, places reporting: 19 in 1960, 89 in 1980, 111 in 1990, 153 in 2000, 177 in 2025.
  - The early years are thin, and how many places report changes with time.
- **Known biases, from UNHCR's methodology page.** Read in the archive's copy of 2026-01-15 (https://web.archive.org/web/20260115095124id_/https://www.unhcr.org/refugee-statistics/methodology).
  - Collecting these statistics "is challenging", with "the lack of consistent terminology and difficulties in comparing statistics internationally".
  - Venezuelans formerly counted as "Venezuelans displaced abroad" were moved into a new category, "other people in need of international protection", and "This change has been made retroactively in UNHCR's statistics since 2018". That category is not among the series taken.
  - End-year figures for the previous year are published each June, so the latest year may be revised.
  - Palestine refugees under UNRWA's mandate are a separate endpoint and are not in these files.

## 2. NOAA IBTrACS, version v04r01

- **Address.** Product page https://www.ncei.noaa.gov/products/international-best-track-archive. The files come from `https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/` (`access/csv/` and `doc/`).
- **Licence.** Taken from NCEI's open data policy, NCEI-PD-10-2-02 of December 14, 2022 (https://www.ncei.noaa.gov/sites/default/files/2023-12/NCEI%20PD-10-2-02%20-%20Open%20Data%20Policy%20Signed.pdf). Section 4a reads: "Environmental data and information produced by NOAA or any Federal agency are available fully and openly to data users unless explicitly exempt from release by Federal law, regulation or policy. These data are in the public domain in the United States. To serve our international partners and customers, NCEI will work to ensure a Creative Commons CC0 license is applied."
  - The product page mentions an optional user registration. It was not used.
- **Citation asked for** (product page).
  - Knapp, K. R., et al., 2010, Bulletin of the American Meteorological Society 91, 363–376, https://doi.org/10.1175/2009BAMS2755.1.
  - Gahtan, J., K. R. Knapp, C. J. Schreck, H. J. Diamond, J. P. Kossin, M. C. Kruk, 2024: IBTrACS Project, Version 4r01, https://doi.org/10.25921/82ty-9e16 [access date].
- **Fetched (2026-11-11).**

  | File | Bytes | SHA-256 |
  |---|---|---|
  | `ibtracs/ibtracs.since1980.list.v04r01.csv` | 145,355,979 | `e99866ac5e14909495a4cdbd09490b44ff287f56a69c4f12bcdf74355f0b4e75` |
  | `ibtracs/IBTrACS_version4r01_Technical_Details.pdf` | 675,292 | `19a22e4debcb71f1e5745e10cd11475d081c85c67e7eccfea9f8f365172dbd6e` |
  | `ibtracs/IBTrACS_v04r01_column_documentation.pdf` | 67,666 | `b78b8d0a712408766ec76991172dd73095cf60efcfa53c4dfc8196ad170c8d34` |

  The address carries no date, and the file is refreshed in place, so a later fetch will not match byte for byte.
- **First comparable year: 1980.** This comes from the archive's own technical document:
  - Section 8.2: "Since 1980 - This is considered by many to be the modern era, since geostationary satellite coverage was nearly global and polar orbiting data (which does provide global coverage) was more widely available than in previous years."
  - Table 2 gives position errors for each strength of storm "(and larger before 1980)".
  - The archive's own "since 1980" file was therefore taken.
  - The span is 1980-01 to 2026-10, the last whole month before the fetch.
- **What counts as a storm.**
  - Spurs are dropped (1,169 positions). Section 5.3: "When counting TCs, spurs should be ignored in most cases."
  - A storm counts if its strongest wind in the US agencies' column, USA_WIND ("Maximum sustained wind speed in knots: 0 - 300 kts. [1-min. mean]"), reaches 34 knots, tropical-storm strength.
  - A single column with a single averaging period is used everywhere. The document warns that "In most of the rest of the world, a 10 min averaging time is used", so "interbasin comparisons of tropical cyclones around the world becomes problematic".
  - A storm is counted in a country and month when one of its positions in that month lies inside the country's shape.
  - Longitudes above 180 are read as minus 360.
- **Shape.** Three series by month (UTC):
  - storms by country. This is a count, and every country-month is written, with zero where no storm passed.
  - strongest USA_WIND by country. This is a level, written only where a counted storm passed and a position inside the country carries a wind.
  - storms anywhere, as a world series. This is a count.

  A month to which a provisional track contributes is flagged `provisional`. Section 4.2: "Provisional data have not been reanalyzed."
- **Coverage.**
  - The file holds 312,366 positions and 5,017 storms. Of the storms, 4,086 reach the bar and 877 do not. 165 positions fall outside the span, and 264,707 positions lie at sea or outside every shape.
  - Storms by country: 234 places × 562 months = 131,508 values, 78 flagged. 97 countries have a storm in some month, and 2,387 country-months have one.
  - Strongest wind: 2,141 values across 91 places, from 10 to 165 kt, 62 flagged. 246 storm-months have no wind at a position inside the country.
  - World: 562 months, none zero, at most 23 storms in a month, 26 flagged.
- **Known biases, from the technical document.**
  - Section 5.3: "Users should exercise care when counting storms in IBTrACS. Many issues are involved that may lead to inflated or wrong numbers." Among the issues it lists: "Some agencies include reporting on tropical depressions", and in some years sub-tropical storms "have been included in best tracks".
  - Wind averaging periods differ by agency, as above.
  - Provisional tracks may change. Section 4.2: "The final best track data ... are subject to change."
  - Position errors are larger before 1980 and for weak storms (Table 2).
  - A country's count depends on its coastline and size. A storm that stays offshore counts only in the world series.

## 3. Ember electricity data

- **Address.** Monthly page: https://ember-energy.org/data/monthly-electricity-data/ ("Last Updated: 11 Nov 2026"). The files come from `https://files.ember-energy.org/public-downloads/`: `generation/outputs/release_generation_monthly_global.csv`, `generation/outputs/release_generation_yearly_global.csv` and `ember_electricity_data_methodology.pdf`.
- **Licence.** https://ember-energy.org/creative-commons/: "Ember content is released under a Creative Commons Attribution Licence (CC-BY-4.0) This means you're free to share and adapt our work – as long as you credit us." The footer of the monthly page says: "All content is released under a Creative Commons Attribution Licence (CC-BY-4.0)."
- **Citation asked for.** The pages read ask only "credit us", with no set form. Proposed: "Ember, Monthly and Yearly Electricity Data, fetched 2026-11-11, https://ember-energy.org/data/, CC BY 4.0".
- **Fetched (2026-11-11).**

  | File | Bytes | SHA-256 |
  |---|---|---|
  | `ember/release_generation_monthly_global.csv` | 29,104,746 | `e9814d266356024ef4327fa19cc0fabc6a8bd8552d7be85b43405910cefefa38` |
  | `ember/release_generation_yearly_global.csv` | 16,120,810 | `08932763076fa781634371dd1b75d8156f76592710c7e984836ed56a663d5688` |
  | `ember/ember_electricity_data_methodology.pdf` | 1,487,777 | `67c5eaac3bfbeb7e67bb786f9ea9680f67f6f26e75318560562ee52d439de908` |

- **Shape.** Fourteen series in TWh, from rows whose area type is "Country or economy":
  - generation by month: total, coal, gas, wind, solar, hydro and nuclear;
  - the same seven by year, kept because the yearly record reaches further back (1985, against 1998-12) and covers far more places;
  - no shares and nothing per head.

  A missing period is written as nothing.
- **Places set aside.**
  - Monthly: XKX, 220 rows.
  - Yearly: XKX 170, GLP 115, REU 112, GUF 72, MTQ 67.
- **Coverage.**
  - Monthly total: 87 places, 1998-12 to 2026-10, 11,605 values.
  - Monthly by source, in places: coal 63, gas 77, wind 80, solar 78, hydro 81, nuclear 36.
  - Places in the monthly record each January: 4 in 2000, 12 in 2010, 40 in 2015, 83 in 2019, 81 in 2026. So the monthly record is thin before about 2015.
  - Yearly total: 204 places, 1985 to 2025, 5,794 values. Places by year: 22 in 1985, 52 in 1990, 202 in 2000, 193 in 2024, 93 in 2025. The last year is not yet complete.
- **Known biases, from the methodology and the monthly page.**
  - The monthly page says the data cover "88 geographies representing more than 90% of global power demand", collected "from multi-country datasets (EIA, Eurostat, Energy Institute) as well as national sources".
  - "Where conflicts occur, annual data is generally more accurate."
  - "simply summing up monthly values will not produce the same results as our annual values for any given year."
  - Captive power: "This data is generally included in national yearly statistics, but may be excluded from monthly statistics".
  - "Some countries do not report disaggregated generation from fossil fuels; this disaggregation was performed by Ember."
  - In monthly data there are "the few cases where a specific fuel is not available".
  - "Projected data is not released for individual countries on a monthly level". For the latest year, "regional and world figures for this year are estimated".
  - The page says the data is "updated twice a month", so recent months are revised.

## 4. World Bank commodity prices (the "Pink Sheet")

- **Address.** Page https://www.worldbank.org/en/research/commodity-markets. The files come from `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/`: `CMO-Historical-Data-Monthly.xlsx` ("Updated on November 03, 2026") and `CMO-Historical-Data-Annual.xlsx` ("Updated on September 02, 2026").
- **Licence.** The commodity-markets page links, under "Using this Data", to the World Bank's summary terms of use, https://data.worldbank.org/summary-terms-of-use. They say:
  - "Unless indicated otherwise in the data or indicator metadata, you are free to copy, distribute, adapt, display or include the data in other products for commercial or noncommercial purposes at no cost under a Creative Commons Attribution 4.0 International License, with the additional terms below."
  - "Some datasets and indicators are provided by third parties, and may not be redistributed or reused without the consent of the original data provider, or may be subject to additional terms and conditions. Where applicable, these conditions are included in the dataset or indicator metadata."
  - The terms also carry a clause on mediation and arbitration.
- **Not settled.** The workbook names third parties among its sources, among them Bloomberg Finance L.P., S&P Global and Thomson Reuters Datastream, and states no restriction of its own. The catalogue record that would hold "the dataset or indicator metadata" could not be read: the catalogue's API answered "too many requests". So CC BY 4.0 is the licence on the page that covers this file, and whether any one price carries a third party's further terms is not settled.
- **Citation asked for.** "The World Bank: Dataset name: Data source (if known)." (summary terms). Proposed: "The World Bank: World Bank Commodity Price Data (The Pink Sheet), fetched 2026-11-11".
- **Fetched (2026-11-11).**

  | File | Bytes | SHA-256 |
  |---|---|---|
  | `pink_sheet/CMO-Historical-Data-Monthly.xlsx` | 587,760 | `3c8d9d8dbb48342fdbf24777c39a8ce8964cc2fd0958f72f6779e6e4ad99cde2` |
  | `pink_sheet/CMO-Historical-Data-Annual.xlsx` | 3,176,359 | `320b6871339f9042644840df0249e1216f31b873cb731c0a01781232e8a8975d` |

- **Shape.**
  - Every monthly price in nominal US dollars becomes one world series, `pink_sheet:<name>:world`, in the unit the sheet gives, on a log scale.
  - The one index column (Natural gas index, 2010=100) is left out, because it is not a price.
  - The yearly sheet ("Annual Prices (Nominal)") is used only where a price's yearly record begins before its monthly one. Only DAP does: yearly from 1960, monthly from 1967. That gives `pink_sheet:dap:world:year`.
  - Cells marked unavailable ("…" in the monthly sheet; the yearly sheet's notes say 'Periods where data are unavailable are indicated by ".."') are not written: 6,216 monthly and 421 yearly.
  - Eight monthly cells of Rice, Thai 25% are set aside: "#VALUE!" in 1988-08, 1989-06, 1990-06 and 2008-02, and 0 in 2008-03 to 2008-06. A zero is not read as a price.
- **Coverage.**
  - 71 series (70 monthly, 1 yearly), 49,982 values, 1960-01 to 2026-10.
  - Most monthly prices run the whole span.
  - Later starts include WTI (1982), Coal, South African (1984), Rice, Thai 25% and A.1 (1986), Rubber TSR20 (1999), Rapeseed and Sunflower oil (2002-02), and Rice, Viet Namese 5% (2003-12).
  - Barley and Sorghum end in 2020-08, Shrimps, Mexican in 2023-10, and Tobacco in 2026-07.
- **Known biases, from the workbook.**
  - Some columns are joined series. Beef, Lamb, Groundnut oil, Chicken and Potassium chloride change their quote (place or grade) part way through: from January 2024, January 2020, January 2023, September 2021 and January 2020 respectively.
  - "** Rubber TSR20 replaces Rubber RSS3 in Other Raw Materials index from 2018".
  - The latest months of some prices are estimates, said so in the sheet's notes; for example, for Liquefied natural gas (Japan): "recent two months' averages are estimates."
  - The sheet's notes name "World Bank staff estimates" among their sources.
  - These are quoted market prices, mostly at one port or exchange, not prices paid in any country.

## Series a steward should bar from naming each other

These pairs are the same quantity, sums or averages of one another, or the same figure from another release. A link between them says nothing.

- **UNHCR.**
  - Within: refugees by origin with refugees by asylum, and asylum seekers by origin with asylum seekers by asylum. The world totals of each pair are the same people.
  - Within: refugees with asylum seekers for the same side and place, because an asylum seeker recognised moves from one to the other.
  - Already held: `wdi:SM.POP.RHCR.EO` and `wdi:SM.POP.RHCR.EA` are UNHCR's refugee figures by origin and by asylum, republished by the World Bank. Each is barred from naming its UNHCR counterpart.
  - Already held: Eurostat's first-time asylum applicants (`migr_asyappctzm`). Its applicants become UNHCR's pending cases in the same countries of asylum, so it is barred from naming asylum seekers by asylum.
- **IBTrACS.** Within: storms by country, strongest wind by country and storms in the world. The world count holds every country's storms, and the wind series is written only where a storm was counted.
- **Ember.**
  - Within: each monthly total with its own sources.
  - Within: each monthly series with its yearly series of the same name.
  - Already held: every `wdi:EG.ELC.*` production share (coal, natural gas, hydro, nuclear, oil, fossil, renewable) and `wdi:EG.ELC.RNWX.KH`. They are built from the same national electricity statistics.
  - Already held: Eurostat's monthly electricity table (`nrg_cb_em`), which the monthly page names as a source of Ember's monthly data.
- **Pink Sheet.**
  - Crude oil, average with Brent, Dubai and WTI, because it is their mean.
  - Tea, avg 3 auctions with Colombo, Kolkata and Mombasa.
  - DAP monthly with DAP yearly.
  - Not barred: the three sugars (EU, US, world) and the two rubbers (TSR20, RSS3), which are separate quotes rather than sums or averages of one another.
- **Held prices, not barred.** The food prices already held (`rtfp:maize`, `rtfp:rice`, `rtfp:wheat`, `rtfp:wheat_flour`, and the FAOSTAT consumer price indices) are local market prices and national indices, not the same quotes. They are not barred from naming Pink Sheet maize, rice or wheat. A steward who wants such a pair barred should say so before any run, not after.

## Changed on taking this in

Checked by the project session on 2026-11-11 before any use: the seven data checksums recomputed; the adapter's four tests run; places, periods and values of every series counted again through the adapter, all as above; one licence a source read again.

- **UNHCR.** The terms were read again in the same archived copy. Point 1 begins "Except where otherwise provided". The live page refuses a script, so a change since 2024-04-24 would not have been seen.
- **IBTrACS.** The product page has its own terms of use, which the manifest now quotes first: "The IBTrACS data usage policy follows the World Data Center for Meteorology (WDC), which provides full and open access to the data." and "We also use the World Meteorological Organization's Resolution 40 policy as the guide for commercial use of IBTrACS data."
- **Pink Sheet.** Held as not settled: read on this box, nothing made from it published until the catalogue record is read.
- **Names.** The manifest entries are `unhcr`, `ibtracs`, `ember` and `pink_sheet`, the source names the adapter writes.

The sources are in the manifest, `docs/data-sources.md` and the build script. The table is not built again until the first read across it and its confirmation are done.

## Entries proposed for `data/manifest.toml` (as the helper wrote them; the manifest holds them with the changes above)

```toml
[unhcr_population]
source_url = "https://api.unhcr.org/population/v1/population/?limit=100000&yearFrom=1951&yearTo=2026&coo_all=true (and the same with coa_all=true)"
fetch_script = "scripts/fetch_world_kinds.py"
version = "UNHCR Refugee Population Statistics Database, population endpoint as served 2026-11-11 (end-year figures to 2025; the address carries no release)"
licence = "CC BY 4.0 under UNHCR's terms of use for datasets (https://www.unhcr.org/terms-use-datasets, read in the archive's copy of 2024-04-24); attribute 'UNHCR Refugee Population Statistics Database' and give the terms' address; point 6 reserves third-party datasets"
fetched = "2026-11-11"
sha256 = "db81c8140e617a51caec61f0de2c3794215ccc401e004d2f77063ccb5bda25ca"  # population_by_origin.json
asylum_sha256 = "0396ef6f0aa8b68b402346cfbaf7b0b02ba59ecca6b9b00bd19d1d850aa5b50a"  # population_by_asylum.json
coverage = "Yearly. Refugees by origin 211 places 1960-2025 (7,459 values), by asylum 194 places 1951-2025 (7,726); asylum seekers by origin 211 places 1993-2025 (6,057), by asylum 192 places 1993-2025 (5,330)"
known_biases = "Few places report before 1990; asylum seekers only '0' before 1993, read as not collected; a missing country-year is not a zero; terms and comparability differ across countries (UNHCR's methodology page); Venezuelan category changed back to 2018; unknown, stateless and Tibetan origins and four overseas territories set aside; latest year revised"

[ibtracs]
source_url = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.since1980.list.v04r01.csv"
fetch_script = "scripts/fetch_world_kinds.py"
version = "IBTrACS v04r01, the since-1980 file as served 2026-11-11 (refreshed in place); technical details and column documentation fetched beside it"
licence = "Public domain in the United States, CC0 intended (NCEI open data policy NCEI-PD-10-2-02, section 4a); cite Knapp et al. 2010, https://doi.org/10.1175/2009BAMS2755.1, and Gahtan et al. 2024, IBTrACS Project Version 4r01, https://doi.org/10.25921/82ty-9e16"
fetched = "2026-11-11"
sha256 = "e99866ac5e14909495a4cdbd09490b44ff287f56a69c4f12bcdf74355f0b4e75"
technical_details_sha256 = "19a22e4debcb71f1e5745e10cd11475d081c85c67e7eccfea9f8f365172dbd6e"
column_documentation_sha256 = "b78b8d0a712408766ec76991172dd73095cf60efcfa53c4dfc8196ad170c8d34"
coverage = "Global, 1980-01 to 2026-10; 5,017 storms, 4,086 reaching 34 kt on USA_WIND; storms by country 234 places x 562 months (97 countries ever hit, 2,387 country-months with a storm); strongest wind 2,141 values in 91 places; world count 562 months"
known_biases = "Agencies differ in wind averaging (1 vs 10 minutes) and in which weak or sub-tropical systems they record; USA_WIND used everywhere for one standard; provisional tracks flagged and subject to change; position errors larger before 1980; 85% of positions at sea count only in the world series"

[ember_generation]
source_url = "https://files.ember-energy.org/public-downloads/generation/outputs/release_generation_monthly_global.csv (and release_generation_yearly_global.csv)"
fetch_script = "scripts/fetch_world_kinds.py"
version = "Ember monthly and yearly electricity data as served 2026-11-11 (monthly page 'Last Updated: 11 Nov 2026'; updated twice a month); methodology PDF fetched beside it"
licence = "CC BY 4.0 (https://ember-energy.org/creative-commons/: 'free to share and adapt our work – as long as you credit us'); credit Ember"
fetched = "2026-11-11"
sha256 = "e9814d266356024ef4327fa19cc0fabc6a8bd8552d7be85b43405910cefefa38"  # monthly
yearly_sha256 = "08932763076fa781634371dd1b75d8156f76592710c7e984836ed56a663d5688"
methodology_sha256 = "67c5eaac3bfbeb7e67bb786f9ea9680f67f6f26e75318560562ee52d439de908"
coverage = "Generation in TWh: total, coal, gas, wind, solar, hydro, nuclear. Monthly 87 places 1998-12 to 2026-10 (total 11,605 values; 4 places in 2000, 40 in 2015, 83 in 2019); yearly 204 places 1985-2025 (total 5,794 values; 2025 has 93 places)"
known_biases = "Monthly may exclude captive power that yearly includes; months do not sum to the year; fossil split estimated by Ember for some countries; some fuels missing in monthly data; recent months revised; Kosovo and four French overseas departments set aside"

[pink_sheet]
source_url = "https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx (and CMO-Historical-Data-Annual.xlsx)"
fetch_script = "scripts/fetch_world_kinds.py"
version = "World Bank Commodity Price Data (The Pink Sheet): monthly workbook 'Updated on November 03, 2026', annual workbook 'Updated on September 02, 2026'"
licence = "CC BY 4.0 under the World Bank's summary terms of use (https://data.worldbank.org/summary-terms-of-use), 'unless indicated otherwise in the data or indicator metadata'; third parties named among the sources; catalogue metadata not read (429); attribute 'The World Bank: World Bank Commodity Price Data (The Pink Sheet)'"
fetched = "2026-11-11"
sha256 = "3c8d9d8dbb48342fdbf24777c39a8ce8964cc2fd0958f72f6779e6e4ad99cde2"  # monthly
annual_sha256 = "320b6871339f9042644840df0249e1216f31b873cb731c0a01781232e8a8975d"
coverage = "World, nominal US dollars: 70 monthly prices 1960-01 to 2026-10 (most full span; barley and sorghum end 2020-08), DAP yearly from 1960; 71 series, 49,982 values"
known_biases = "Joined series where the quote changes (beef 2024, lamb 2020, groundnut oil 2023, chicken 2021, potassium chloride 2020); recent months partly World Bank estimates; Rice Thai 25% has four error cells and four zeros, set aside; one port or exchange quote, not a local price"
```
