# Data sources

Every source this project has checked, used or not: how to get it, and what its licence asks of us.
Last updated 2026-11-05. Licences were read at source on that date, unless a row says otherwise, and
can change, so check again before relying on one for something new.

Versions and checksums are in `data/manifest.toml`. Data is never committed here: run the fetch script,
from the repo root, with `uv run python scripts/fetch_<name>.py`. Files land in the ignored `data/raw/`.

| Source | Measures | Status | Access | Licence | Coverage | Resolution | Size | Host |
|---|---|---|---|---|---|---|---|---|
| [UCDP GED 26.1](#ucdp-ged) | Fatal organised violence | Used, outcome | Direct, no login | CC BY 4.0 | 1989 to 2025 | Event, point | 39 MB | Uppsala University, Sweden |
| [SPEIbase 2.11](#speibase) | Drought | Used | Direct, no login | ODbL 1.0, contents DbCL 1.0 | 1901 to 2024-12 | 0.5 degree, monthly | 383 MB | CSIC, Spain |
| [NOAA ONI](#noaa-oni) | El Nino state | Used | Direct, no login | Public domain, partly confirmed | 1950 to 2026-09 | One global value, monthly | 7 KB | NOAA PSL, USA |
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

## NOAA ONI

- **Data:** <https://psl.noaa.gov/data/correlation/oni.data>
- **Fetch:** `scripts/fetch_oni.py`. The file changes as NOAA updates it, so its checksum records one fetch only.
- **Licence requires:** nothing stated specifically. The [NWS disclaimer](https://www.weather.gov/disclaimer) puts its pages in the public domain "unless specifically noted otherwise", but that is another NOAA office's wording and no PSL page was found. Treat as partly confirmed. Credit NOAA regardless.
- **Know before use:** a 3-month running mean, so this project uses it a month back to avoid seeing the future.

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
