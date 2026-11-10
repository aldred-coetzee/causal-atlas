# Data sources

Every source this project has checked, used or not: how to get it, and what its licence asks of us.
Last updated 2026-11-10. Licences were read at source on 2026-11-05, unless a row says otherwise, and
can change, so check again before relying on one for something new.

Versions and checksums are in `data/manifest.toml`. Data is never committed here: run the fetch script,
from the repo root, with `uv run python scripts/fetch_<name>.py`. Files land in the ignored `data/raw/`.

| Source | Measures | Status | Access | Licence | Coverage | Resolution | Size | Host |
|---|---|---|---|---|---|---|---|---|
| [UCDP GED 26.1](#ucdp-ged) | Fatal organised violence | Used, outcome | Direct, no login | CC BY 4.0 | 1989 to 2025 | Event, point | 39 MB | Uppsala University, Sweden |
| [SPEIbase 2.11](#speibase) | Drought | Used | Direct, no login | ODbL 1.0, contents DbCL 1.0 | 1901 to 2024-12 | 0.5 degree, monthly | 383 MB | CSIC, Spain |
| [NOAA ONI](#noaa-oni) | El Nino state | Used | Direct, no login | Public domain | 1950 to 2026-09 | One global value, monthly | 7 KB | NOAA PSL, USA |
| [ESA Fire_cci FireCCILT11 v1.1](#esa-fire_cci-fireccilt11) | Burned area | Used, outcome | Direct, no login | ESA CCI terms: any use, with acknowledgement | 1982 to 2018, no 1994 | 0.25 degree, monthly | 7.2 GB | CEDA, United Kingdom |
| [World Bank Real Time Food Prices](#world-bank-real-time-food-prices) | Market food prices | Fetched, set aside unread (decision 0050) | Direct, no login | Open data, citation asked; CC BY 4.0 per the Data Catalog | 2007 to 2026-11 | Market, monthly | 133 MB zipped, 1.2 GB | World Bank, USA |
| [FAOSTAT crops](#faostat-crops-and-livestock-products) | Cereal yield by country | Fetched, outcome under design | Direct, no login | CC BY 4.0 | 1961 to 2024 | Country, yearly | 34 MB zipped, 545 MB | FAO, Italy (file host not checked) |
| [FAO GIEWS FPMA](#fao-giews-fpma) | Market food prices | Checked, not fetched (fallback) | Open API, no login | CC BY 4.0, third-party series excluded | 1987 to 2026 | Market, monthly, no coordinates | 4,938 series | FAO, Italy |
| [Natural Earth](#natural-earth) | Country borders | Used, grid | Direct, no login | Public domain | Fixed release | 1:10m vector | 5 MB | Natural Earth CDN |
| [CHIRPS v3](#chirps) | Rainfall | Checked, not used | Direct, no login | Public domain, per page | 1981 to near present, file not opened | 0.05 degree, monthly | 8.3 GiB | UCSB, USA |
| [WFP food prices](#wfp-food-prices) | Market food prices | Checked, **not fetched** | **Scripted fetching disallowed** | CC BY-IGO, per metadata | 1990 to 2026, per metadata | Market, monthly | 0.62 GB | HDX |

## UCDP GED

- **Data:** <https://ucdp.uu.se/downloads/ged/ged261-csv.zip>. **Codebook:** <https://ucdp.uu.se/downloads/ged/ged261.pdf>. **Terms and citations:** <https://ucdp.uu.se/downloads/>
- **Fetch:** `scripts/fetch_ucdp_ged.py`.
- **Licence requires:** attribution under CC BY 4.0, and citing the publications listed on the downloads page. On 2026-11-05 these included Davies, Pettersson and Oberg, "Organized violence 1989-2025, and violent political protests", Journal of Peace Research, 2026, doi:10.1093/jopres/xjag046. Copy the current list when publishing.
- **Know before use:** an event needs at least one death, so this measures fatal events only. Precision varies: in Africa 75.3% of events are within 25 km and 85.6% are at district level or finer. Some columns can name people; this project drops them at ingest.

## SPEIbase

- **Data:** <https://spei.csic.es/spei_database/nc/spei03.nc>, with other time scales beside it. **About:** <https://spei.csic.es/database.html>
- **Fetch:** `scripts/fetch_spei.py`.
- **Licence requires:** [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/). Anything published from it carries an attribution and ODbL notice. A derivative database stays under ODbL. A public work made from one must offer that database or the method of making it (clause 4.6b), which this repo's public scripts do. Our MIT code is not affected.
- **Know before use:** built from CRU TS 4.09. Station coverage over Africa has not been checked here. Ends a year before the conflict data.
- **Known error in this version (read 2026-11-09).** The makers' README, "Known issue: PET unit conversion (fixed in v2.13.0)" (<https://raw.githubusercontent.com/sbegueria/SPEIbase/master/README.md>): for versions 2.6 to 2.12.0, "The vector of days per month was recycled along the longitude dimension of the data array instead of along time, so each grid cell's PET was multiplied by a single constant (28, 29, 30 or 31) in every month. All published SPEI datasets from v2.6 to v2.12.0 are affected. The effect is generally small, but it is largest in arid regions where PET dominates the water balance." A corrected release "will follow". The held file is 2.11.0 and is affected. The README's version list gives 2.12.0 as built from CRU TS 4.10 to December 2025, and 2.13.0 as the fix; the download page listed nothing later than 2.11 when a helper read it on 2026-11-09. **When a corrected file is out: fetch it, enter it here and in the manifest, and compare it with this one before building anything more on drought.**
- **Standardised on the whole record, not on a reference period.** Each value's level and scale are set from all of 1901 to 2024 at that cell and calendar month, so a value in 1960 carries a little from 2020. Sources, read 2026-11-09: the file's `call` attribute (`spei.nc(sca=i, inPre=./inputData/cru_ts4.09.1901.2024.pre.dat.nc, …)`, no reference period); the makers' code, `speii <- function(d,s) {SPEI::spei(d, s, na.rm=TRUE, verbose=FALSE)$fitted}` (<https://raw.githubusercontent.com/sbegueria/SPEIbase/master/R/functions.R>, the current code, later than this file's build); and the SPEI package's documentation, "The default behavior of the functions is using all the values provided in data for parameter fitting" (<https://raw.githubusercontent.com/sbegueria/SPEI/v1.8.1/R/spei.R>). It also means **every new release changes every value a little**, back to 1901. For an out-of-time test this is a limit to state beside the result.

## NOAA ONI

- **Data:** <https://psl.noaa.gov/data/correlation/oni.data>
- **Fetch:** `scripts/fetch_oni.py`. The file changes as NOAA updates it, so its checksum records one fetch only.
- **Licence requires:** public domain. PSL's own [disclaimer](https://psl.noaa.gov/disclaimer/), read 2026-11-09 and quoted in the next section, settles what the first reading on 2026-11-05 left as partly confirmed. Credit NOAA/OAR/PSL as it asks.
- **Know before use:** a 3-month mean centred on each month, so the value for month t uses month t+1. Nothing here reads it closer than three months before the month forecast.
- **Its zero moves with time, and looks ahead.** NOAA measures each five-year stretch against a 30-year average centred on it: "There will be multiple centered 30-year base periods that will be used to define the Oceanic Niño index", for example "ONI values during 1950-1955 will be based on the 1936-1965 base period" (NOAA CPC, <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_change.shtml>, read 2026-11-09). So a value in the 1990s is measured against an average that includes the 2000s, and the newest values are measured against a base that will change. This takes the ocean's warming out of the index, which is its purpose. For an out-of-time test it is a limit to state. A fixed-base series from the same product is on PSL's list (`nina34.anom.data`, anomalies from 1981 to 2010).

## NOAA PSL monthly time series (the candidate list; 25 kept)

- **Data:** <https://psl.noaa.gov/data/timeseries/month/>, PSL's page "Monthly Mean Time-series". Each series has a page at `…/month/DS/<NAME>/` and a description at `…/month/<NAME>/keyvalues.json`, which names its one or two data files and its maker. 89 series pages, 96 files (read 2026-11-09).
- **Fetch:** `scripts/index_candidates.py fetch`. No account, no key. It saves the page, a listing of every file with its address and PSL's source notes, and the files. The files change as they are updated, so each checksum in `data/manifest.toml` records one fetch.
- **Why the whole list:** a rule, not a choice. All 96 are read to apply the candidate rule of `results/real-indices.md` (complete for 1950-01 to 2024-12, not rainfall, not El Niño by another name, not mostly a trend, not a series already kept); 25 pass and are used. The script prints every file's measurements and why it is in or out.
- **Layout:** a first line with the first and last year, one line per year with twelve values, then the file's missing-value mark on a line of its own (it differs by file: -99.9, -999, -9999, -9.99, -10 and others), then notes. Read the mark from the file; do not assume one.
- **The 25 kept, their makers and terms.** PSL's [disclaimer](https://psl.noaa.gov/disclaimer/), read by this session 2026-11-09: "The information on government servers are in the public domain, unless specifically annotated otherwise", with a request to acknowledge "Data/image provided by the NOAA/OAR/PSL, Boulder, Colorado, USA, from their Web site at https://psl.noaa.gov/". This also settles the ONI entry above, which had found no PSL page. Where a series comes from elsewhere, its maker's terms apply as well:
  - *Computed by PSL from HadISST1.1:* tni.long (Trans-Niño Index), dmi.had.long and dmieast.had.long (Indian Ocean Dipole and its eastern box), tna and tsa (tropical North and South Atlantic), and one of three inputs to pdo.timeseries.sstens (Pacific Decadal Oscillation). HadISST [terms](https://www.metoffice.gov.uk/hadobs/hadisst/terms_and_conditions.html), read by this session: "HadISST1 is subject to Crown copyright protection and is provided under an Open Government Licence"; cite Rayner et al. (2003) and acknowledge www.metoffice.gov.uk/hadobs.
  - *PSL's own, from NOAA products:* whwp (Western Hemisphere Warm Pool), qbo and qbo.50mb (stratospheric wind at 30 and 50 mb).
  - *NOAA Climate Prediction Center:* ao.long (Arctic Oscillation), ea (East Atlantic), pna (Pacific/North American), scand (Scandinavia), wp (West Pacific). *NOAA Oceanview:* noi (Northern Oscillation Index). *NOAA Storm Prediction Center:* tornado.us.mon (United States tornado count).
  - *NCAR method and pressure grids, computed at PSL:* np.long (North Pacific index). NCAR's [page](https://climatedataguide.ucar.edu/climate-data/north-pacific-np-index-trenberth-and-hurrell-monthly-and-winter) gives usage restrictions as "None" and asks for the credit "NP Index Data provided by the Climate Analysis Section, NCAR, Boulder, USA, Trenberth and Hurrell (1994)."
  - *Climatic Research Unit, University of East Anglia:* nao_gib.long and nao_ice.long, the sea-level pressure at Gibraltar and at Iceland from which CRU's North Atlantic Oscillation is formed. CRU's [page](https://crudata.uea.ac.uk/cru/data/nao/): "These datasets are made available under the Open Database License"; cite "Updated from Jones et al. (1997)".
  - *D. Vimont, University of Wisconsin:* amm (Atlantic Meridional Mode), pmm and pmmwind (Pacific Meridional Mode, temperature and wind). No licence is stated on his [page](https://www.aos.wisc.edu/dvimont/MModes/Home.html); it asks for the credit "AMM (or PMM) index provided by http://www.aos.wisc.edu/~dvimont/MModes/Data.html."
  - *E. Di Lorenzo:* npgo (North Pacific Gyre Oscillation). No licence is stated at <http://www.o3d.org/npgo/>; it says the index is free to use and asks for a citation of Di Lorenzo et al. (2008). Values after 2022-12 are marked preliminary by PSL.
  - *University of Lincoln:* gbi.mon (Greenland Blocking Index). No licence stated; cite Hanna, Cropper, Hall and Cappelen (2016), doi:10.1002/joc.4673.
  - *WDC-SILSO, Royal Observatory of Belgium:* sunspot.long (sunspot number; PSL holds version 1.0 and says a newer one exists). SILSO's [data page](https://www.sidc.be/SILSO/datafiles), read by this session: "our sunspot data can be freely downloaded (Licence: CC BY-NC : https://creativecommons.org/licenses/by-nc/4.0 )", with a request for credit to WDC-SILSO. **Non-commercial only**: anyone reusing a result that rests on this series commercially must check that for themselves.
  - The wording for CRU, NCAR, Vimont, Di Lorenzo and Lincoln was read at source by a helper's lookup on 2026-11-09 and reported back; it has not been read a second time by this session. The three with no stated licence are used with the credit asked for and are not redistributed.
- **Know before use:** several are anomalies or patterns computed with years after 1999 in their climatology or their pattern, so each is re-centred and re-scaled on its own 1950 to 1999 calendar months before use; that removes the offset and the scale, not a pattern's shape. Several carry a trend (the highest kept: tornado count 0.19 of variance, eastern Indian Ocean box 0.18, tropical South Atlantic 0.16, PDO 0.15). The tornado count rises with better reporting. Two pairs are close relatives (tna and amm 0.81; Iceland pressure and Greenland blocking 0.75).
- **Read only to apply the rule and not used:** the Niño-region series, the ONI's relative version, the bivariate ENSO series, the Southern Oscillation and the tropical Pacific upper wind (El Niño by another name); the global temperature records of NASA, Berkeley Earth, CRU and the Hadley Centre, and NOAA, and the Pacific warm pool (mostly a trend); two Sierra Nevada rain-gauge series (rainfall); a second PDO (the same as the first). 45 files are incomplete for 1950 to 2024, among them the Jones NAO (11 months missing), the long tropical Atlantic files (1), the Southern Annular Mode, the MEI, the hurricane counts, carbon dioxide, sea level, snow and ice extent, and outgoing longwave radiation; `scripts/index_candidates.py` lists each with its count.

## ESA Fire_cci FireCCILT11

- **Data:** <https://dap.ceda.ac.uk/neodc/esacci/fire/data/burned_area/AVHRR-LTDR/grid/v1.1/>, one folder per year, one NetCDF file per month, 432 files of 16,663,142 bytes. **Catalogue record:** <https://catalogue.ceda.ac.uk/uuid/62866635ab074e07b93f17fbf87a2c1a>. **Terms:** <https://artefacts.ceda.ac.uk/licences/specific_licences/esacci_fire_terms_and_conditions.pdf>. All read 2026-11-10.
- **Fetch:** `scripts/fetch_firecci.py`. It picks up where it stopped, keeps a file only at its full size, and writes the checksum of every file to `data/firecci.sha256`; the manifest holds the checksum of that listing.
- **Licence requires:** "The CCI datasets held on the CCI Open Data Portal may be used by any user for any purpose", on these terms: "Users of the CCI data are required to acknowledge the ESA Climate Change Initiative and the Fire CCI project together with the individual data providers if the data are used in a presentation or publication. Please also cite any relevant dataset DOIs." Users are "encouraged" to tell the programme of their use and to send copies of publications, and "An offer of co-authorship should be considered, if the CCI data constitute a major component of a scientific publication." Rights in the data stay with their producers, and there is no warranty. **Cite as:** Chuvieco, E.; Pettinari, M.L.; Otón, G. (2020): ESA Fire Climate Change Initiative (Fire_cci): AVHRR-LTDR Fire_cci Burned Area Grid product, version 1.1. Centre for Environmental Data Analysis, 28 December 2020. doi:10.5285/62866635ab074e07b93f17fbf87a2c1a. The acknowledgement is in `README.md` and beside each result that uses the data.
- **No account, and none made.** The folder's own note: "Public data: access to these data is available to both registered and non-registered users." Registering with the Fire CCI project is encouraged by the terms, not required; it would send an address to an outside service, so this project has not.
- **Know before use:**
  - **1994 is absent.** The product's README: "Year 1994 is not included in the dataset because there was not enough input data from the LTDR Archive". Every use here treats that year as unknown, never as zero burning.
  - **Each file says how much of a cell was looked at.** Variables: `burned_area` (square metres, the total in the cell), `standard_error`, `fraction_of_burnable_area` ("fraction of the cell that corresponds to vegetated land covers that could burn") and `fraction_of_observed_area` (the share of the burnable area "that was observed during the time interval, and was not marked as unsuitable/not observable", for lack of input data, cloud or sensor failure). **Both "fraction" variables are stored as per cent, 0 to 100, though their `units` attribute says 1** (seen in the files, 2026-11-10); `src/causal_atlas/fire.py` divides by 100. A month with little observed is not a month with little fire. Cloud hides fire, and a dry year is a clear year, so how much is seen is itself tied to the weather.
  - **Several satellites, drifting orbits.** The record is stitched from AVHRR instruments whose overpass time drifted and which replaced one another. The makers correct for this; that cannot be checked here. A change of satellite could look like a change in fire.
  - **Coarse pixels.** About 5 km: small fires are missed, so burning on cropland and at forest edges is under-counted, and the product is trained against a finer one (MODIS) that exists only from 2001.
  - Latitude runs north first in the files; cells are centred at .125, .375, .625 and .875 of a degree, so four of them make one cell of this project's half-degree grid exactly.

## World Bank Real Time Food Prices

- **Data:** <https://microdata.worldbank.org/catalog/4483/download/361260/WLD_RTFP_mkt_2026-11-02.zip>, one zip holding one CSV. **Study page:** <https://microdata.worldbank.org/index.php/catalog/4483>. **Study record, as data:** <https://microdata.worldbank.org/index.php/api/catalog/4483?id_format=id>. **Older and newer releases:** <https://microdata.worldbank.org/index.php/api/catalog/WLD_2021_RTFP_v02_M/resources>. Read 2026-11-10.
- **Fetch:** `scripts/fetch_rtfp.py`. The release is dated in its address; a later release is a different file and needs a new manifest entry.
- **Licence requires:** the study record gives access as "open" and "Public use" and says "The dataset of price estimates is published as open data." A country entry in the Bank's Data Catalog states "License: Creative Commons Attribution 4.0" (read by a helper, not re-checked here). **Cite:** Andrée, B. P. J. (2021). Monthly food price estimates by product and market (Version 2026-11-02). WLD_2021_RTFP_v02_M. Washington, DC: World Bank Microdata Library. <https://doi.org/10.48529/2ZH0-JF55>
- **No account, and none made.** The site has no robots file; its terms say nothing on automated access. One request fetches the whole release.
- **Know before use:**
  - **Most of the file is model output.** Each item has a plain column (`maize`) and estimated columns (`o_`, `h_`, `l_`, `c_` for open, high, low and close, plus `inflation_` and `trust_`). The record says: "Predicted data for missing entries are based on exchange rates, and price data available either at other market locations or from related price items." This project uses the plain columns only (decision 0049). That the plain column is the price as collected is read from the file: it is filled in a minority of months, and the closing estimate equals it in about 90% of those.
  - **Weather is not an input to the estimates,** by the record and the method paper (World Bank WPS 9886), as read; the plain columns do not depend on that.
  - **Outliers:** "To produce smooth price series, outliers in the data are often adjusted using non-parametric density estimation and other techniques." Whether that touches the plain columns is not stated.
  - **Sparse and short.** 2007-01 onwards. Of 3,229 markets, 571 in 33 countries have one cereal with 120 or more observed months and 272 have 180 or more; Mali, Burkina Faso, Niger and Senegal hold 237 of the 571. 37 markets have no coordinates.
  - **Sources behind it** are WFP, FAO and national statistical offices; columns ending `_fao` are FAO's series. Prices are in local currency per the row's `currency`.
  - **Host:** the World Bank, in the United States. No European source with coordinates and a dated release was found (decision 0049).

## FAOSTAT Crops and livestock products

- **Data:** <https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip>, one zip holding one long CSV and four code tables (areas, items, elements, flags). **Page:** <https://www.fao.org/faostat/en/#data/QCL>. **Terms:** <https://www.fao.org/contact-us/terms/db-terms-of-use/en/>. Read 2026-11-10.
- **Fetch:** `scripts/fetch_faostat.py`, then unpack with `python -I -m zipfile -e data/raw/faostat_qcl.zip data/raw/faostat`. The address carries no release date; the server gave the file's last change as 2025-12-31. Check the checksum in the manifest: a later fetch may be a different file.
- **Licence requires:** attribution. The terms say: "Unless specified otherwise in their metadata or webpage, all datasets disseminated through FAO corporate statistical databases (see examples in Annex 1) are licensed under the Creative Commons Attribution-4.0 International licence (CC BY 4.0)", as complemented by the terms themselves, which add that no endorsement by FAO is to be implied and that no attempt is made to identify any person or body in the data. **Cite, in FAO's form:** FAO. 2025. FAOSTAT: Crops and livestock products. Accessed on 10 November 2026. <https://www.fao.org/faostat/en/#data/QCL> Licence: CC-BY-4.0.
- **No account, and none made.** One request fetches the whole domain.
- **Know before use:**
  - **Every figure carries a flag:** A official, E estimated, I imputed, X from another organisation, M missing. This project takes official figures only as the thing to be forecast (decision 0051). Estimated and outside figures are often carried forward: 9% and 19% of them equal the year before, against 1% of official ones.
  - **Yield is not measured.** It is production divided by area harvested (element 5412, kg/ha), so it carries the errors of both, and a national figure is as good as the country's own statistics.
  - **Long official records, counted on yields alone:** country series with 40 or more official years are maize 89, rice 83, wheat 74, sorghum 61, barley 58, millet 38; 116 countries have at least one. 1961 to 2024.
  - **The latest years are less official:** for maize, 88 of 163 figures are official in 2024 against 133 of 161 in 2010.
  - **Countries change.** USSR, Yugoslav SFR, Czechoslovakia, Ethiopia PDR, Sudan (former) and Belgium-Luxembourg end and their successors begin. China appears three times: China, China mainland, and Taiwan. Rows with an area code of 5000 or more are groups of countries, not countries.
  - **Joining to borders:** the M49 code column has a leading apostrophe. With it removed, 139 of the 149 countries holding a cereal with 30 or more official years match Natural Earth's `UN_A3`; the rest are the dissolved states, the China total, Taiwan and Norway (Natural Earth gives those two no code; match them by `ADM0_A3`) and French Guiana (inside France's shape).
  - **National and annual.** Nothing here is by place or by month.

## FAO GIEWS FPMA

- **API, found by a helper in the web tool's own code:** catalogue `https://fpma.fao.org/giews/v4/global/price_module/api/v1/FpmaSerie/`, one series `.../FpmaSeriePrice/<id>/?periodicity=monthly`. **Terms:** <https://www.fao.org/contact-us/terms/db-terms-of-use/en/>. Read by the helper 2026-11-10; not opened by this session.
- **Not fetched.** No fetch script. It is the fallback if the World Bank file proves too short.
- **Licence requires:** "licensed under the Creative Commons Attribution-4.0 International licence", but third-party data "may not be redistributed or reused without the consent of the original data provider". Many series are WFP's, FEWS NET's or a national body's, so each would need its own check.
- **Know before use:** observed prices, source named per series, 4,938 series in 690 markets and 139 countries from 1987; 714 cereal series in 95 countries span 15 years or more (by first and last date, gaps not counted). **No coordinates**: markets would be placed by name. A live service with no dated release.
- **Also checked and closed to us, 2026-11-10:** FEWS NET's data warehouse (its robots file disallows everything and it asks not to be crawled) and WFP's DataBridges (credentials only by email).

## Natural Earth

- **Data:** <https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip>. **Terms:** <https://www.naturalearthdata.com/about/terms-of-use/>
- **Fetch:** `scripts/fetch_natural_earth.py`.
- **Licence requires:** nothing; public domain.
- **Know before use:** borders are one editorial view, fixed in time. It is used only for the land mask and country lookup.

## CHIRPS

- **Data:** <https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/global/netcdf/>, file `chirps-v3.0.monthly.nc`. **About:** <https://www.chc.ucsb.edu/data/chirps>
- **Fetch:** no script yet. The older CHIRPS-2.0 path returned 404 on 2026-11-05.
- **Licence requires:** nothing stated: the page says "CHIRPS data is in the public domain", of CHIRPS generally, so check this for v3.
- **Why not used:** it tied with SPEI on the checks, and a European host broke the tie. It is the natural second rainfall source if drought is ever revisited, at ten times the resolution.

## WFP food prices

- **Dataset page:** <https://data.humdata.org/dataset/global-wfp-food-prices>, 37 yearly CSV files. **Site terms:** <https://data.humdata.org/faqs/terms>
- **Access:** HDX's [`robots.txt`](https://data.humdata.org/robots.txt) disallows `/api/` and `/*.csv$` for all agents, with a crawl delay of 10, and scripted requests got an empty 202 challenge. So there is no fetch script. Files could be saved by hand from a browser. HDX's own API (HAPI) was not tried: it appears to need an email-based identifier, which this project does not give to external services. That is unconfirmed.
- **Licence requires:** CC BY-IGO, as HDX's metadata states; the licence text itself has not been read here.
- **Why not used:** dropped from Phase 1 (decision 0013). The monthly updates would also mean the data has no frozen release.
