# Data sources

Every source this project has checked, used or not: how to get it, and what its licence asks of us.
Last updated 2026-11-09. Licences were read at source on 2026-11-05, unless a row says otherwise, and
can change, so check again before relying on one for something new.

Versions and checksums are in `data/manifest.toml`. Data is never committed here: run the fetch script,
from the repo root, with `uv run python scripts/fetch_<name>.py`. Files land in the ignored `data/raw/`.

| Source | Measures | Status | Access | Licence | Coverage | Resolution | Size | Host |
|---|---|---|---|---|---|---|---|---|
| [UCDP GED 26.1](#ucdp-ged) | Fatal organised violence | Used, outcome | Direct, no login | CC BY 4.0 | 1989 to 2025 | Event, point | 39 MB | Uppsala University, Sweden |
| [SPEIbase 2.11](#speibase) | Drought | Used | Direct, no login | ODbL 1.0, contents DbCL 1.0 | 1901 to 2024-12 | 0.5 degree, monthly | 383 MB | CSIC, Spain |
| [NOAA ONI](#noaa-oni) | El Nino state | Used | Direct, no login | Public domain | 1950 to 2026-09 | One global value, monthly | 7 KB | NOAA PSL, USA |
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
