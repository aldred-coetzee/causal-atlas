# Landscape Analysis: Existing Platforms, Tools, and Projects

> **Last updated:** March 2025
> **Purpose:** Inform build-vs-leverage decisions for Causal Atlas by cataloguing existing open-source and research platforms that do pieces of what we need.

---

## Table of Contents

1. [PRIO-GRID v3](#1-prio-grid-v3)
2. [VIEWS (Violence & Impacts Early-Warning System)](#2-views-violence--impacts-early-warning-system)
3. [AfroGrid](#3-afrogrid)
4. [WFP HungerMapLIVE](#4-wfp-hungermap-live)
5. [ClimateSERV](#5-climateserv)
6. [xSub](#6-xsub)
7. [HDX Platform & HAPI](#7-hdx-platform--hapi)
8. [Kepler.gl](#8-keplergl)
9. [ACLED Dashboard & Tools](#9-acled-dashboard--tools)
10. [GDELT Analysis Service](#10-gdelt-analysis-service)
11. [Other Relevant Open-Source Projects](#11-other-relevant-open-source-projects)
12. [Comparative Summary](#12-comparative-summary)
13. [Implications for Causal Atlas](#13-implications-for-causal-atlas)

---

## 1. PRIO-GRID v3

**What it is:** A spatial data infrastructure for conflict research, providing a standardised 0.5 x 0.5 degree global vector grid with attached socio-economic, political, climatic, and geographic variables. Developed by the Peace Research Institute Oslo (PRIO).

**Links:**
- Website: https://grid.prio.org/
- GitHub (v3 R package): https://github.com/prio-data/priogrid
- Original paper: [Tollefsen, Strand & Buhaug (2012), Journal of Peace Research](https://journals.sagepub.com/doi/10.1177/0022343311431287)
- PRIO page: https://www.prio.org/data/9

### Architecture

PRIO-GRID v3 is a complete rewrite of the earlier dataset as an **R package** (not just a static download). Key architectural decisions:

- **Built on `sf`, `terra`, and `exactextractr`** -- leverages the modern R spatial stack rather than custom infrastructure.
- **Flexible spatio-temporal configuration** -- users can change resolution, extent, and projection. This supports testing the Modifiable Areal Unit Problem (MAUP) or creating custom-region datasets, rather than being locked to 0.5 degrees.
- **Template-based ingestion** -- generates a PRIO-GRID template first, then loads new data to fit the template. Source-specific transformation functions live in `R/data_[source].R` files.
- **Hash-based caching** -- custom builds use 6-character MD5 hashes to identify unique spatial configurations (resolution, extent, CRS) and temporal configurations (resolution, date range), avoiding redundant processing.
- **Automatic memory management** -- when estimated memory exceeds 4GB, `terra` switches to disk-based processing automatically.
- **Status:** v3.0.1 is an unstable Alpha release. A Beta version is planned but not yet released as of March 2025.

### Key Functions

| Function | Purpose |
|---|---|
| `download_priogrid()` | Download the pre-built PRIO-GRID dataset |
| `read_pg_static()` | Load static (time-invariant) variables |
| `read_pg_timevarying()` | Load yearly time-varying variables |
| `load_pgvariable()` | Load individual variables as rasters |
| `pgvariables` | List all available variables |
| `pgsources` | View available data sources and metadata |
| `pg_rawfiles()` | List all downloadable raw source files |
| `download_pg_rawdata()` | Download specific raw source data |
| `pgcitations()` | Get citations for variables |
| `gen_cshapes_gwcode()` | Calculate country codes from CShapes |

### Variables Included

PRIO-GRID contains two categories of variables:

**Static (time-invariant):**
- Terrain: mountains, land cover types, distance to borders, distance to capital, travel time to nearest city
- Geography: latitude, longitude, area, land area percentage

**Yearly (time-varying):**
- **Population:** Gridded Population of the World (GPW), GHSL population grid
- **Climate:** Temperature, precipitation (CRU, CHIRPS), drought indices
- **Vegetation:** NDVI
- **Nighttime lights:** DMSP-OLS, VIIRS
- **Political:** Ethnic Power Relations (EPR), excluded population, country codes (CShapes)
- **Conflict events:** UCDP-GED events aggregated to grid cells

### What We Can Reuse

- **The 0.5-degree grid itself** is the de facto standard for sub-national conflict research. Causal Atlas should be PRIO-GRID compatible -- this is already a key decision.
- **The R package's data ingestion pattern** (template + source-specific adapters) is a good model for our Python ingestion pipeline.
- **The hash-based caching approach** for different spatial configurations is worth adopting.
- **Variable definitions and source metadata** can inform our dataset catalogue.

### Limitations

- **R only** -- no Python bindings. We will need to build Python equivalents.
- **Alpha status** -- the v3 package is not production-stable.
- **No causal analysis** -- PRIO-GRID is purely a data compilation framework. It does not perform any statistical analysis or causal inference.
- **Monthly resolution not native** -- the primary temporal unit is yearly, though some underlying sources have monthly data.
- **No API** -- data is delivered as downloadable files, not via a queryable API.

---

## 2. VIEWS (Violence & Impacts Early-Warning System)

**What it is:** A state-of-the-art conflict forecasting system that generates monthly predictions of armed conflict fatalities 1-36 months ahead, at both country-month and PRIO-GRID-month resolution. Jointly led by Uppsala University and PRIO.

**Links:**
- Website: https://viewsforecasting.org/
- GitHub organisation (prio-data): https://github.com/prio-data
- GitHub organisation (views-platform): https://github.com/views-platform
- Main forecasting pipeline: https://github.com/prio-data/views_pipeline
- Stepshift algorithm: https://github.com/prio-data/stepshift
- Forecasting notebooks: https://github.com/prio-data/viewsforecasting
- Original paper: [Hegre et al. (2019), Journal of Peace Research](https://journals.sagepub.com/doi/full/10.1177/0022343319823860)
- Prediction Challenge paper: [Hegre et al. (2024)](https://journals.sagepub.com/doi/10.1177/00223433241300862)
- PRIO project page: https://www.prio.org/projects/1977

### Forecasting Pipeline

VIEWS operates a sophisticated ML pipeline with the following components:

**Data Infrastructure:**
- Ingests data from **over a dozen trusted providers**, including UCDP-GED (conflict events), World Bank (economic indicators), CRU (climate), V-Dem (political institutions), and many others.
- Data is captured as **hundreds of features** covering conflict history, economic growth, political stability, natural resource deposits, terrain, and vulnerability to natural hazards and climate extremes.
- Two levels of analysis: **country-month (cm)** and **PRIO-GRID-month (pgm)** at 0.5-degree resolution.

**Current Production Model -- Fatalities002:**
- The operational model generates forecasts for state-based armed conflict fatalities during each month in a rolling 3-year window.
- Uses a **stepshift approach** (described in Hegre et al. 2020, Appendix A): instead of recursive multi-step forecasting, each forecast horizon (1 month, 2 months, ..., 36 months) gets its own independently trained model.
- The **stepshift** package implements this with a scikit-learn-like API (`StepshiftedModels` class).
- Models include **XGBoost**, random forests, and other ML algorithms within an ensemble framework.

**MLOps Infrastructure:**
- Industry-grade MLOps, DevOps, and CI/CD pipeline.
- Built-in **drift detection**, quality assurances, and real-time monitoring.
- Monthly automated forecast runs.

### Open-Source Components

The VIEWS codebase is highly modular and openly available:

| Repository | Purpose |
|---|---|
| `views-pipeline-core` | Main pipeline: data ingestion, preprocessing, model training, evaluation, experiment tracking |
| `views-models` | All implemented models at pgm and cm levels |
| `views-stepshifter` | Stepshifter model class for time-series forecasts |
| `views-hydranet` | HydraNet model class for spatiotemporal forecasts |
| `stepshift` | Core stepshifting algorithm package |
| `viewsforecasting` | Jupyter notebooks for exploring and visualising VIEWS data |
| `prediction_competition_2023` | Benchmark models and evaluation scripts for the Prediction Challenge |

### Prediction Challenge (2023/24)

The 2023/24 VIEWS Prediction Challenge invited 13 research institutions to develop conflict fatality forecasting models. Key findings:

- **23 models** were submitted using diverse approaches: quantile-based solutions, ensembles of local random forests, Markov models, sequence-based approaches, dynamic time warping, hierarchical models for zero inflation, and Bayesian methods.
- As of February 2025, VIEWS' benchmark "Conflictology" model leads rankings at both country and subnational levels.
- Results are available on a **live dashboard** for ongoing evaluation.
- The challenge surface important methodological insights about uncertainty quantification in conflict prediction.

### What We Can Reuse

- **The stepshift approach** is directly applicable to any multi-horizon time-lagged prediction task -- including our cross-domain causal analysis.
- **The modular pipeline architecture** (separate repos for core, models, data) is a good pattern for Causal Atlas.
- **The VIEWS API and data** can serve as an input layer for conflict predictions within Causal Atlas.
- **Evaluation methodology** from the Prediction Challenge provides benchmarks for assessing causal claims.

### Limitations

- **Single-domain focus** -- VIEWS predicts conflict only. It does not discover cross-domain causal relationships (e.g., drought causing conflict).
- **Prediction, not explanation** -- the pipeline is optimised for forecast accuracy, not for identifying causal mechanisms.
- **Heavy infrastructure** -- the full MLOps pipeline requires significant compute and operational resources.
- **Python ecosystem** -- fortunately aligned with our tech stack direction.

---

## 3. AfroGrid

**What it is:** An integrated, disaggregated 0.5-degree grid-month dataset combining conflict, environmental stress, and socioeconomic variables for Africa, covering 1989-2020. Published in Nature Scientific Data.

**Links:**
- Paper: [Linke & Ruether (2022), Nature Scientific Data](https://www.nature.com/articles/s41597-022-01198-5)
- Data: [Harvard Dataverse, AfroGrid V1.0](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LDI5TK)
- ResearchGate: https://www.researchgate.net/publication/359535368

### Integration Methodology

AfroGrid's core contribution is **demonstrating how to harmonise multi-domain data onto a common spatiotemporal grid**. Their approach:

1. **Spatial standardisation:** All variables are mapped to the PRIO-GRID 0.5-degree cells. Latitude and longitude for each cell centroid are included for easy merging.
2. **Temporal standardisation:** All variables are aggregated to monthly resolution (grid-month observations).
3. **Identifier alignment:** Each row includes month/year indicators, PRIO-GRID cell IDs, and Correlates of War (COW) country IDs, enabling easy joins with external datasets.
4. **Single-file delivery:** Everything is combined into one flat file, maximising accessibility regardless of user software background.

### Domains and Variables

| Domain | Variables | Source(s) |
|---|---|---|
| **Conflict** | State-based, non-state, one-sided violence events and fatalities | UCDP-GED, ACLED, SCAD, PITF |
| **Vegetation** | NDVI mean, min, max (monthly variability) | MODIS |
| **Climate** | Temperature, precipitation, SPEI (drought index at 1-month scale) | CRU, GPCC |
| **Nighttime lights** | Harmonised dual-series (DMSP-OLS + VIIRS) | Li et al. harmonisation |
| **Population** | Population density | GPW, LandScan |

**Key innovation:** AfroGrid includes **NDVI and dual-series harmonised nighttime lights** that previously required advanced computational expertise to produce. By pre-computing these, they lower the barrier for researchers without remote sensing skills.

**Temporal coverage by source:**
- UCDP-GED: from 1989
- ACLED: from 1997
- PITF: from 1995
- SCAD: 1990-2017
- SPEI accounts for both precipitation and temperature -- positive values indicate water surplus, negative values indicate water stress.

### What We Can Reuse

- **The integration methodology is our closest prior art.** AfroGrid does exactly what Causal Atlas aims to do, but limited to Africa, limited to ~5 domains, and delivered as a static file rather than a dynamic platform.
- **Variable selection** -- their choice of NDVI, nightlights, SPEI, temperature, precipitation, and conflict events is a strong starting point.
- **The dual-series nightlight harmonisation** approach is worth studying for our own nightlights integration.
- **PRIO-GRID + COW identifier alignment** is the right pattern for interoperability.

### Limitations

- **Africa only** -- no global coverage.
- **Static dataset** -- a fixed file for 1989-2020, not a live-updating system.
- **No causal analysis** -- provides the integrated data but does not perform any statistical analysis.
- **No API** -- single-file download only.
- **Limited domains** -- does not cover food prices, health, air quality, earthquakes, or other domains Causal Atlas targets.
- **Monthly only** -- no daily or weekly granularity.

---

## 4. WFP HungerMap LIVE

**What it is:** A real-time, AI-powered global hunger monitoring system that tracks food security in 90+ countries using machine learning nowcasting, live survey data, and satellite/economic indicators. Developed by WFP's Hunger Monitoring Unit.

**Links:**
- Live platform: https://hungermap.wfp.org/
- Innovation page: https://innovation.wfp.org/project/hungermap-live
- WFP launch announcement: https://www.wfp.org/stories/wfp-launches-hungermap-live
- Alibaba collaboration: https://www.businesswire.com/news/home/20190925005712/en/Alibaba-WFP-Unveil-Generation-Machine-Learning-Technology

### Architecture (Publicly Known)

HungerMap LIVE is not open source, but the following is publicly documented:

**Data Pipeline:**
- Ingests streams of publicly available data on food security, nutrition, conflict, weather, and macro-economic indicators.
- Sources include: Pacific Disaster Centre (hazards), World Bank (population, economics), NASA (vegetation/NDVI), WFP's own near-real-time monitoring surveys, market price data.
- A unified **data warehouse** brings all information streams together.

**ML/AI Approach:**
- **Nowcasting models** estimate hunger levels in areas where daily surveys are cost-prohibitive.
- Predictive features include: population density, nighttime light intensity, rainfall, vegetation index (NDVI), conflict events, market food prices, macro-economic indicators, and undernourishment rates.
- Developed in collaboration with Alibaba Cloud's machine learning team (2019 onwards).
- Models produce near-real-time, granular estimates of food security situations.

**Near-Real-Time Monitoring:**
- Live phone surveys via call centres collect daily food security information.
- These systems provide daily estimates over rolling 30- or 60-day windows.
- Currently operational in 36+ countries.

**Visualisation:**
- Interactive map with overlayable data layers (conflict, hazards, hunger, weather).
- Country-level and sub-national views.
- Available at global, regional, and country levels.

### What We Can Learn

- **The nowcasting approach** (using satellite/proxy data to estimate ground-truth indicators) is highly relevant. Causal Atlas could adopt similar methods to fill data gaps.
- **Multi-source data fusion** architecture is a proven model for combining disparate indicators.
- **The overlay approach** -- letting users see how different phenomena interlink -- is exactly the UX pattern Causal Atlas needs.

### Limitations

- **Closed source** -- the platform, models, and data pipeline are proprietary.
- **Single-domain focus** -- food security only (though it integrates multi-domain inputs).
- **No causal inference** -- it nowcasts food security status, it does not identify causal chains.
- **No public API** for accessing the underlying data or model outputs programmatically.
- **WFP institutional tool** -- designed for WFP operations, not for general research.

---

## 5. ClimateSERV

**What it is:** An open-source web application developed by NASA SERVIR that enables users to visualise, analyse, and download climate-related earth observation datasets for water and food security applications.

**Links:**
- Application: https://climateserv.servirglobal.net/
- Documentation: https://climateserv.readthedocs.io/
- GitHub (ClimateSERV2): https://github.com/SERVIR/ClimateSERV2
- Python package (ClimateSERVpy): https://github.com/SERVIR/ClimateSERVpy
- PyPI: https://pypi.org/project/climateserv/
- API documentation: https://climateserv.servirglobal.net/develop-api
- Journal paper: [Environmental Modelling & Software (2025)](https://www.sciencedirect.com/science/article/pii/S1364815225003937)

### Technical Architecture

**Backend:**
- Built on **Django** (Python web framework).
- Uses **Celery** task queue for asynchronous data processing.
- Two **conda environments**: one for the database, one for the application.
- Follows NASA's **Open Science** initiative -- free and open-source software throughout.
- Licensed under MIT licence (ClimateSERVpy).

**Frontend:**
- Web-based UI for visualisation and analysis.
- Map interface for spatial data exploration.

**API:**
- REST API for programmatic data access.
- Supports spatial aggregation queries: users submit a geometry (polygon/point) and get time-series statistics back.
- Asynchronous request pattern: submit request, poll for completion, download results.
- Available through web, API, and Python package.

### Available Datasets

| Dataset ID | Name | Type |
|---|---|---|
| 0 | UCSB CHIRPS Rainfall | Precipitation |
| 1, 2, 5, 28 | eMODIS NDVI (West/East/Southern Africa, Central Asia) | Vegetation |
| 26 | IMERG 1 Day (late) | Precipitation |
| 29, 33 | ESI 4-week / 12-week | Evaporative Stress |
| 31 | CHIRPS GEFS Anomalies | Precipitation forecast |
| 32 | CHIRPS GEFS Precipitation | Precipitation forecast |
| 37, 38, 39 | NASA-USDA Enhanced SMAP Soil Moisture (profile, surface, anomaly) | Soil moisture |

Additional datasets can be accessed by ID even when documentation has not yet been updated.

### Python Package (ClimateSERVpy)

```python
# Example: Download CHIRPS rainfall data
import climateserv
climateserv.api.request_data(
    dataset_type=0,           # CHIRPS
    operation_type=5,         # Average
    earliest_date="01/01/2020",
    latest_date="01/31/2020",
    geometry_coords=[...],    # GeoJSON polygon coordinates
    output_file="output.csv"
)
```

Installable via pip or conda. Outputs data in formats ready for immediate analysis.

### Usage Scale

Over 1 million data access events from 11,000+ distinct users across 162 countries in the 2023-2024 period.

### What We Can Reuse

- **ClimateSERVpy as a data source** -- we can directly use this Python package to ingest climate data (CHIRPS rainfall, NDVI, soil moisture, ESI) into Causal Atlas.
- **The API pattern** (submit geometry + time range, get time-series back) is a clean model for our own data access layer.
- **The dataset catalogue structure** (ID-based, with metadata) is a useful pattern.
- **Django + Celery architecture** for async processing is a proven pattern we might consider.

### Limitations

- **Climate data only** -- no conflict, economic, health, or other domain data.
- **Regional NDVI** -- eMODIS NDVI is available only for specific regions (West/East/Southern Africa, Central Asia), not globally.
- **Asynchronous API** -- requires polling for results, which adds complexity.
- **No causal analysis** -- purely a data access and visualisation tool.
- **Spatial aggregation only** -- returns statistics for geometries, not raw gridded rasters via the API.

---

## 6. xSub

**What it is:** A "database of databases" for disaggregated research on political conflict. xSub consolidates micro-level, subnational event data from 22 sources into consistent spatial and temporal units.

**Links:**
- Portal: https://www.x-sub.org/
- Paper: [Zhukov, Davenport & Kostyuk (2019), Journal of Peace Research](https://journals.sagepub.com/doi/10.1177/0022343319836697)
- CRAN R package: https://cran.r-project.org/web/packages/xSub/index.html
- University of Michigan project page: https://cps.isr.umich.edu/projects/xsub-cross-national-data-of-sub-national-violence-2/
- Full paper PDF: https://zhukovyuri.github.io/files/2019_ZDK_JPR.pdf

### Methodology

xSub's core innovation is **standardising conflict data across 22 different event data sources** into a consistent schema:

**Actor Classification:**
- Side A: Government forces
- Side B: Opposition forces
- Side C: Civilians
- Side D: Unaffiliated actors

**Action Classification:**
- 4 general categories, 27 specific sub-categories
- Includes any use of force, indirect force, and other action types

**Spatial Units:**
| Level | Description |
|---|---|
| `adm0` | Country |
| `adm1` | Province |
| `adm2` | District |
| `priogrid` | PRIO-GRID 0.5-degree cell |
| `clea` | Electoral constituency |

**Temporal Units:** Year, month, week, day

### Coverage

- **195 countries** (1968-2019)
- **22 event data sources**, including both large collections (ACLED, UCDP-GED) and individual scholar datasets

### R Package

```r
# Example: Get ACLED data for Nigeria at PRIO-GRID monthly resolution
library(xSub)
df <- get_xSub(
  data_source = "ACLED",
  country = "Nigeria",
  space_unit = "priogrid",
  time_unit = "month"
)
```

The R package provides functionality beyond the website: direct import into R and merging datasets across countries.

### What We Can Reuse

- **The standardisation methodology** (actor/action classification across sources) is valuable for our conflict data integration layer.
- **PRIO-GRID compatibility** -- xSub already outputs data at priogrid resolution.
- **Multi-source harmonisation** lessons -- how they handle discrepancies between ACLED, UCDP-GED, SCAD, etc.
- **The "database of databases" concept** aligns with Causal Atlas's goal of integrating across sources.

### Limitations

- **Conflict data only** -- no climate, economic, health, or other domain data.
- **R only** -- no Python package (though the data files can be used from any language).
- **Static archive** -- data goes to 2019 and may not be actively updated.
- **No analysis tools** -- provides standardised data but no statistical or causal analysis.
- **No API** -- web portal and R package only.

---

## 7. HDX Platform & HAPI

**What it is:** The Humanitarian Data Exchange (HDX) is OCHA's open platform for sharing humanitarian data across crises and organisations, based on CKAN. HDX HAPI (Humanitarian API) is a newer API layer providing direct access to standardised indicator data.

**Links:**
- HDX Platform: https://data.humdata.org/
- HDX HAPI: https://data.humdata.org/hapi
- HDX HAPI Documentation: https://hdx-hapi.readthedocs.io/
- HDX Python API: https://hdx-python-api.readthedocs.io/
- GitHub (hdx-python-api): https://github.com/OCHA-DAP/hdx-python-api
- GitHub (OCHA-DAP): https://github.com/OCHA-DAP
- Developer Resources: https://data.humdata.org/faqs/devs
- HAPI announcement: https://centre.humdata.org/announcing-the-hdx-humanitarian-api/

### Platform Architecture

**CKAN Foundation:**
- HDX is built on **CKAN**, an open-source data management system.
- Supports dataset metadata search, resource management, and organisation hierarchies.
- Standard CKAN API for metadata operations.

**Two API Layers:**

| API | Purpose | Capability |
|---|---|---|
| **HDX CKAN API** | General-purpose catalogue API | Search, read/write dataset metadata. Cannot query data *within* resources. |
| **HDX HAPI** | Curated indicator API (launched June 2024) | Direct access to standardised data. Supports queries within datasets, filtering by theme/location/time. |

### HDX HAPI Data Categories

HDX HAPI consolidates and standardises:

- **Conflict events** (sourced from ACLED)
- **Food security** (IPC/CH classifications)
- **Food prices** (WFP)
- **Internally displaced persons** (IOM DTM)
- **Humanitarian needs** (HNO/HRP)
- **Operational presence** (3W -- Who does What Where)
- **Poverty rates**
- **Population** statistics

**Geographic coverage:** All countries where data is available (expanded from initial 25 HRP countries). About half of the data reaches admin-2 (district) level granularity.

**Access:** No account needed, but requires an **app identifier** (generated via the API).

### HDX Python API (hdx-python-api)

- Mature library supporting **Python 3** (currently developed on 3.13).
- High test coverage.
- Objects like datasets and resources are represented as Python classes.
- Supports both pushing and pulling data from HDX.
- Uses CKAN JSON API under the hood.

```python
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

Configuration.create(hdx_site="prod", user_agent="causal-atlas")
datasets = Dataset.search_in_hdx("food prices", rows=10)
```

### What We Can Reuse

- **HDX HAPI as a data source** -- direct API access to conflict, food security, displacement, and food price data at sub-national resolution. This should be a primary ingestion target for Causal Atlas.
- **hdx-python-api** for metadata search and resource discovery.
- **The standardisation approach** -- HAPI's category-based data model is a useful reference for our own schema design.
- **The CKAN pattern** -- if we ever need a data catalogue layer, CKAN is proven at scale.

### Limitations

- **Humanitarian focus** -- does not cover climate, pollution, earthquakes, or non-humanitarian indicators.
- **HAPI is still in Beta** (as of March 2025) -- API stability not guaranteed.
- **CKAN API cannot query data within resources** -- only metadata. This is why HAPI was built.
- **Coverage gaps** -- not all countries have data for all indicators.
- **No spatial grid** -- data is organised by administrative boundaries, not grid cells. Spatial alignment to PRIO-GRID would require a mapping step.

---

## 8. Kepler.gl

**What it is:** An open-source, WebGL-powered geospatial visualisation tool for large-scale datasets. Originally created by Uber, now maintained by Foursquare. Available as a standalone web app and as a React/Redux component for embedding.

**Links:**
- Website/Demo: https://kepler.gl/
- Documentation: https://docs.kepler.gl/
- GitHub: https://github.com/keplergl/kepler.gl
- NPM: https://www.npmjs.com/package/kepler.gl (v3.2.5 as of March 2025)
- Release notes: https://docs.kepler.gl/release-notes
- Foursquare blog (v3.1): https://foursquare.com/resources/blog/products/foursquare-brings-enterprise-grade-spatial-analytics-to-your-browser-with-kepler-gl-3-1/

### Latest Capabilities (v3.x)

**DuckDB Integration (v3.1+):**
- Embeds **DuckDB as an in-browser analytical engine**.
- Users can write and execute SQL queries directly within kepler.gl.
- Supports reading **spatially partitioned GeoParquet files from cloud storage** without downloading entire datasets.
- DuckDB's spatial extension enables complex spatial queries by reading only relevant data partitions.
- Drag-and-drop file support to create DuckDB tables.
- Schema panel updates when running queries.

**AI Assistant:**
- Can edit the map and generate SQL from natural language.
- SQL passed to DuckDB for execution.

**Layer Types:**

| Layer | Description |
|---|---|
| Point | Individual data points (default) |
| Arc | 3D lines between two points |
| Line | 2D lines between points |
| Grid | Square grid aggregation |
| Hexbin | Hexagonal aggregation with metrics (count, avg, max, min, median, sum, mode) |
| Polygon | GeoJSON polygons |
| Cluster | Geospatial radius-based clustering |
| Icon | Custom icon markers |
| H3 | Uber's H3 hexagonal hierarchical spatial index |
| Heatmap | Intensity-weighted geographic heatmaps |
| GeoJSON | All RFC 7946 geometry types (Point, LineString, Polygon, Multi*) |
| Trip | Animated path visualisation |
| S2 | S2 geometry cells |

### Embedding Architecture

```javascript
import KeplerGl from 'kepler.gl';
import { addDataToMap } from 'kepler.gl/actions';

// KeplerGl is a React component using Redux for state management
// Requires react-palm middleware for side effects
<KeplerGl
  id="map"
  mapboxApiAccessToken={MAPBOX_TOKEN}
  width={800}
  height={600}
/>

// Add data programmatically
store.dispatch(addDataToMap({
  datasets: { info: { label: 'Events', id: 'events' }, data: processedData },
  config: mapConfig
}));
```

- **React + Redux** component architecture.
- **Dependency injection** system for replacing UI components.
- Supports **custom layer groups** for toggling visibility.
- Full programmatic control via Redux actions.

### What We Can Reuse

- **Kepler.gl is our primary visualisation candidate.** The DuckDB integration means we can potentially query Parquet files directly in the browser without a backend.
- **H3 layer support** provides an alternative spatial indexing option to raw lat/lon grids.
- **The hexbin/grid aggregation** layers are natural fits for PRIO-GRID visualisation.
- **GeoParquet + DuckDB** pipeline aligns perfectly with our DuckDB/Parquet data stack.
- **Embeddable React component** fits our FastAPI + React architecture.

### Limitations

- **Visualisation only** -- no statistical analysis, no causal inference, no time-series tools.
- **No built-in temporal animation** for time-series beyond the Trip layer. Time filtering exists but is basic.
- **Mapbox dependency** -- requires a Mapbox API token for base maps (free tier available).
- **Complex Redux integration** -- embedding requires understanding Redux middleware and state management.
- **Performance limits** -- while "large-scale", extremely large datasets (100M+ rows) may still require server-side pre-aggregation.

---

## 9. ACLED Dashboard & Tools

**What it is:** A suite of interactive visualisation and analysis tools for Armed Conflict Location & Event Data, covering political violence and protests globally from 1997 to present.

**Links:**
- Main site: https://acleddata.com/
- Data Export Tool: https://acleddata.com/conflict-data/data-export-tool
- Conflict Index: https://acleddata.com/platform/conflict-index-dashboard
- Conflict Exposure Calculator: https://acleddata.com/conflict-exposure/
- API Documentation: https://acleddata.com/acled-api-documentation
- Data Platforms overview: https://acleddata.com/conflict-data/data-platforms

### Tool Suite

ACLED offers an integrated set of tools (merged into a unified **Early Warning Dashboard** in 2025):

**ACLED Explorer:**
- Filter and summarise data from the past year.
- Filters by location, actor, event type, date.
- Country profiles with subnational breakdown.
- Trend views by events, fatalities, and civilians exposed.
- Export to CSV/XLS.

**Conflict Alert System (CAST):**
- Forecasts political violence events **up to 6 months ahead**.
- Monthly updates with accuracy metrics for previous forecasts.
- Line graph with time-range slider (historical + forecasted).
- Bar chart visualisation of events behind forecasts.

**Trendfinder:**
- Identifies statistically significant changes in political violence and protest.
- Historical context and early warning signals.

**Conflict Index:**
- Severity ranking combining **4 indicators**: fatalities, events, locations, and actors.
- Provides comparable cross-country conflict severity scores.

**Conflict Exposure Calculator:**
- Integrates ACLED data with **WorldPop** population estimates.
- Estimates civilians living within **1, 2, and 5 km** of each conflict event.
- Filterable by event type, actor type, location, and time.

### API Access

- REST API with event-level data access.
- Requires free registration for an access key.
- Supports filtering by location, event type, date range, actor.
- Full 1997-present archive available.

### Design Approach

ACLED dashboards are designed to include maximum data density while allowing users to self-select depth. Heavy use of **Tableau tooltips** for definitions and contextual explanations. The 2025 unified dashboard uses a **shared header** -- set date range, geography, and filters once and carry across modules.

### What We Can Learn

- **The overlay of conflict data with population exposure** is a powerful analytical pattern we should adopt.
- **CAST's forecasting visualisation** (historical trend + forecast uncertainty) is a good UX reference for our temporal views.
- **The unified filter header** pattern (set once, apply everywhere) is essential for multi-domain exploration.
- **Conflict Index methodology** (composite severity score) could inspire similar indices across domains.

### Limitations

- **Conflict data only** -- no cross-domain integration.
- **Not open source** -- dashboards and analysis tools are proprietary.
- **API requires registration** and has usage limits.
- **No causal analysis** -- descriptive and predictive, but not explanatory.
- **Tableau-based** -- not embeddable in custom applications.

---

## 10. GDELT Analysis Service

**What it is:** The Global Database of Events, Language, and Tone -- a real-time database monitoring the world's broadcast, print, and web news in 100+ languages, extracting events, entities, themes, and sentiment. Updated every 15 minutes.

**Links:**
- Main site: https://www.gdeltproject.org/
- Analysis Service: https://analysis.gdeltproject.org/
- Data access page: https://www.gdeltproject.org/data.html
- GitHub (web interface): https://github.com/gdelt/gdelt.github.io
- BigQuery demos: https://blog.gdeltproject.org/a-compilation-of-gdelt-bigquery-demos/
- DOC API: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- GEO API: https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/
- TV API: https://blog.gdeltproject.org/gdelt-2-0-television-api-debuts/

### Data Infrastructure

**Two Main Databases:**

| Database | Content | Update Frequency |
|---|---|---|
| **Event Database** | 300+ categories of physical activities (riots, protests, diplomacy, etc.), georeferenced | Every 15 minutes |
| **Global Knowledge Graph (GKG)** | Entities, themes, locations, emotions, quotes from individual news articles | Every 15 minutes |

**Coverage:**
- From January 1979 to present.
- 100+ languages (65 live-translated via Google Jigsaw support).
- Quarter-billion+ event records.
- Globally georeferenced to city/mountaintop level.
- 100% free and open.

**Data Format:** Tab-separated values (.CSV extension) in zip files. Also available via Google BigQuery.

### APIs

| API | Purpose | Window |
|---|---|---|
| **DOC 2.0** | Search news articles, images (VGKG) | Rolling 3 months |
| **GEO 2.0** | Geographic analysis of news coverage | Variable |
| **TV 2.0** | US and international television news analysis | 9+ years |
| **Context 2.0** | Contextual analysis | Variable |
| **BigQuery** | Full SQL access to all datasets | All history |

All APIs support JSON/JSONP output for web integration.

### Analysis Service Visualisation Tools

14 tools available without technical expertise:

- **TimeMapper Visualiser** -- time-coded Google Earth KML files for spatiotemporal exploration
- **Word Cloud Visualiser** -- theme/entity clouds from the GKG
- **Geographic visualisers** -- mapping event distributions
- **Network visualisers** -- entity relationship graphs
- **Temporal visualisers** -- trend analysis over time
- Results delivered via email.

### BigQuery Integration

- All GDELT datasets available in Google BigQuery, updated every 15 minutes.
- Enables SQL queries at unlimited scale with near-real-time response.
- Can export to CartoDB, Gephi, and other visualisation platforms.
- Free within Google Cloud's BigQuery free tier (1TB/month queries).

### What We Can Reuse

- **GDELT as a data source** -- the event database provides near-real-time conflict/protest/political event data with global coverage and deep historical archive.
- **BigQuery access pattern** -- for large-scale querying, the BigQuery approach is powerful and cost-effective.
- **The GKG's thematic coding** could help identify emerging issues (disease outbreaks, economic crises) before they appear in structured datasets.
- **15-minute update cycle** is the gold standard for near-real-time.

### Limitations

- **News-derived data** -- subject to media bias, reporting gaps, and duplicates. Not ground-truth.
- **Geocoding quality varies** -- automated geocoding from news text is inherently noisy.
- **No standardised event ontology** -- CAMEO coding is broad and can be inconsistent.
- **Not open source** -- the data is open, but the processing pipeline is proprietary.
- **BigQuery dependency** -- full-scale analysis requires Google Cloud infrastructure.
- **No causal analysis** -- purely descriptive event data.
- **Raw data is massive** -- requires significant processing to extract usable signals.

---

## 11. Other Relevant Open-Source Projects

### 11.1 Salesforce CausalAI Library

**What it is:** An open-source Python library for causal analysis of time series and tabular data.

**Links:**
- GitHub: https://github.com/salesforce/causalai
- Documentation: https://opensource.salesforce.com/causalai/latest/index.html
- Paper: [arXiv:2301.10859](https://arxiv.org/html/2301.10859)

**Key Features:**
- Supports **causal discovery** and **causal inference** for both tabular and time series data.
- Handles linear and non-linear causal relationships.
- Multi-processing for speed-up.
- Includes Markov Blanket discovery algorithms.

**Time Series Algorithms:**
| Algorithm | Description |
|---|---|
| **PC Algorithm** | General-purpose constraint-based causal discovery |
| **VARLINGAM** | VAR + LiNGAM for time-lagged and contemporaneous causal connections |
| **Granger Causality** | Standard Granger causal discovery |

**Benchmarking:** Built-in modules for comparing algorithms with varying graph sparsity, sample complexity, SNR, noise type, and max lag.

**UI:** Provides a no-code UI for uploading data and running algorithms.

**Relevance to Causal Atlas:** This is a candidate library for our causal analysis engine. The benchmarking capabilities are particularly useful for validating results.

### 11.2 Tigramite (PCMCI)

**What it is:** A Python package for causal inference focused on time series data, implementing the PCMCI family of algorithms.

**Links:**
- GitHub: https://github.com/jakobrunge/tigramite
- Documentation: https://jakobrunge.github.io/tigramite/
- Paper: [Runge et al. (2019), Science Advances](https://www.science.org/doi/10.1126/sciadv.aau4996)

**Key Features:**
- **PCMCI** -- estimates time-lagged causal links via condition-selection + momentary conditional independence testing. Avoids conditioning on irrelevant variables, leading to higher detection power.
- **PCMCIplus** -- identifies the full (lagged + contemporaneous) causal graph up to Markov equivalence class.
- **LPCMCI** -- handles latent confounders.
- **RPCMCI** -- handles regime-dependent causal relationships.
- Supports both **linear and non-parametric** conditional independence tests.
- Works with **continuous and discrete** data.
- Built-in **causal effect estimation** and **mediation pathway analysis**.
- **Optimal predictor selection** for causal forecasting.
- High-quality plotting functions.

**Relevance to Causal Atlas:** Tigramite/PCMCI is likely the most important single library for our causal discovery pipeline. It is specifically designed for the exact problem we face: discovering time-lagged causal relationships in multivariate time series with potential confounders. The PCMCI algorithm's ability to handle high-dimensional data efficiently makes it suitable for multi-domain spatiotemporal analysis.

### 11.3 CausalST Papers Collection

**Link:** https://github.com/yutong-xia/CausalST_Papers

A curated collection of papers on causality in spatiotemporal data, covering causal inference, causal discovery, and applications to areas like air quality forecasting. Useful as a literature survey resource.

### 11.4 FEWS NET (Famine Early Warning Systems Network)

**What it is:** USAID-funded system that provides early warning and analysis on food insecurity. Not a single tool but an ecosystem of data, analysis, and reporting.

**Relevance:** FEWS NET produces the IPC food security classifications used by HDX HAPI and integrates climate, market, and livelihood data in their analysis. Their analytical framework (how climate anomalies propagate through food systems to food insecurity) is a model for the causal chains Causal Atlas aims to surface.

### 11.5 Google Earth Engine

**What it is:** A planetary-scale platform for earth science data and analysis, with a multi-petabyte catalogue of satellite imagery and geospatial datasets.

**Relevance:** Not a competitor but a potential upstream data source. Earth Engine hosts many datasets we need (MODIS NDVI, CHIRPS, VIIRS nightlights, population, land cover). The `earthengine-api` Python package enables programmatic access. Free for research use.

---

## 12. Comparative Summary

### Coverage Matrix

| Platform | Conflict | Climate | Food Security | Economy | Health | Pollution | Disasters | Global | Open Source | Causal Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| PRIO-GRID v3 | X | X | - | X | - | - | - | X | X | - |
| VIEWS | X | (input) | - | (input) | - | - | - | X | X | - |
| AfroGrid | X | X | - | X | - | - | - | Africa | X (data) | - |
| HungerMap LIVE | (input) | (input) | X | (input) | - | - | - | X | - | - |
| ClimateSERV | - | X | - | - | - | - | - | X | X | - |
| xSub | X | - | - | - | - | - | - | X | X | - |
| HDX HAPI | X | - | X | - | - | - | - | X | X | - |
| Kepler.gl | - | - | - | - | - | - | - | X | X | - |
| ACLED | X | - | - | - | - | - | - | X | - (data open) | - |
| GDELT | X | - | - | - | - | - | - | X | - (data open) | - |
| Tigramite | - | - | - | - | - | - | - | - | X | X |
| CausalAI | - | - | - | - | - | - | - | - | X | X |

**Key observation:** No existing platform combines multi-domain data integration with causal analysis. This is the gap Causal Atlas fills.

### Spatial Resolution Comparison

| Platform | Resolution | Grid System |
|---|---|---|
| PRIO-GRID | 0.5 x 0.5 degrees | Custom vector grid |
| VIEWS | 0.5 x 0.5 degrees | PRIO-GRID |
| AfroGrid | 0.5 x 0.5 degrees | PRIO-GRID |
| ClimateSERV | 0.05 degrees (CHIRPS) | Raster |
| xSub | Multiple (admin0-2, priogrid, clea) | PRIO-GRID compatible |
| HDX HAPI | Admin 0-2 | Administrative boundaries |
| GDELT | Point (city-level geocoding) | Lat/lon |
| ACLED | Point (event-level) | Lat/lon |

### Technology Stack Comparison

| Platform | Language | Data Format | API | Visualisation |
|---|---|---|---|---|
| PRIO-GRID v3 | R | Raster/sf | No | No |
| VIEWS | Python | Custom DB | Yes (API + notebooks) | Notebooks |
| AfroGrid | N/A | CSV | No | No |
| ClimateSERV | Python/Django | Raster | Yes (REST + Python pkg) | Web map |
| xSub | R | CSV/RData | No (R pkg) | No |
| HDX HAPI | Python | JSON/CSV | Yes (REST + Python pkg) | Web portal |
| Kepler.gl | JS/React | GeoJSON/CSV/Parquet | N/A (client-side) | WebGL maps |
| ACLED | N/A | CSV/JSON | Yes (REST) | Tableau dashboards |
| GDELT | N/A | TSV | Yes (REST + BigQuery) | Analysis Service |

---

## 13. Implications for Causal Atlas

### What We Can Directly Leverage

1. **PRIO-GRID spatial backbone** -- adopt the 0.5-degree grid as our primary spatial unit. Design Python adapters following the R package's template-based pattern.

2. **Data source APIs/packages for ingestion:**
   - ClimateSERVpy for CHIRPS rainfall, NDVI, soil moisture
   - hdx-python-api + HDX HAPI for food security, displacement, conflict
   - ACLED API for detailed conflict event data
   - GDELT BigQuery for news-derived event data
   - VIEWS API for conflict forecasts (as an additional input/validation layer)

3. **Kepler.gl for visualisation** -- embed as a React component with DuckDB/Parquet backend. The hexbin and H3 layers are natural fits for gridded data.

4. **Tigramite (PCMCI) for causal discovery** -- this should be our primary causal analysis engine for time-lagged multivariate causal inference.

5. **Salesforce CausalAI for benchmarking** -- use alongside Tigramite for algorithm comparison and validation.

6. **AfroGrid's methodology** as a template for multi-domain data harmonisation onto PRIO-GRID cells.

7. **VIEWS' stepshift approach** for multi-horizon forecasting once causal relationships are identified.

### What We Must Build

1. **Multi-domain data ingestion pipeline** -- no existing tool ingests data from conflict, climate, food security, health, pollution, and economic sources into a common grid. We need adapters for each source.

2. **Temporal alignment layer** -- converting daily/weekly/irregular data to monthly grid-cell observations with appropriate aggregation methods. AfroGrid does this manually; we need it automated.

3. **Cross-domain causal discovery engine** -- wrapping Tigramite/CausalAI with spatiotemporal awareness, running causal analysis across domain pairs at each grid cell or region.

4. **Interactive causal exploration UI** -- no existing tool provides an interface for exploring discovered causal relationships across domains and geographies. This is the core novel contribution.

5. **AI-assisted interpretation layer** -- using Claude API to explain discovered causal chains in natural language, contextualising statistical findings with domain knowledge.

6. **Data quality and provenance tracking** -- metadata about source reliability, update frequency, coverage gaps, and citation requirements.

### Build vs. Leverage Decision Matrix

| Component | Decision | Rationale |
|---|---|---|
| Spatial grid | **Leverage** PRIO-GRID | De facto standard, maximises interoperability |
| Climate data access | **Leverage** ClimateSERVpy, Earth Engine | Mature APIs, no need to rebuild |
| Conflict data access | **Leverage** ACLED API, UCDP API, HDX HAPI | Well-documented APIs with good coverage |
| Food security data | **Leverage** HDX HAPI, WFP APIs | Established data pipelines |
| Data harmonisation | **Build** (informed by AfroGrid methodology) | No existing automated tool for multi-domain harmonisation |
| Causal discovery | **Leverage** Tigramite + CausalAI | Mature, well-tested algorithms |
| Causal analysis pipeline | **Build** (wrapping existing libraries) | Novel integration of causal methods with spatiotemporal data |
| Visualisation engine | **Leverage** Kepler.gl | Best-in-class open-source geospatial viz |
| Causal exploration UI | **Build** | Core novel contribution, nothing exists |
| Interpretation layer | **Build** (using Claude API) | Novel AI-assisted explanation |
| Data storage | **Leverage** DuckDB + Parquet | Proven stack, Kepler.gl native support |
| Web framework | **Leverage** FastAPI + React | Standard stack |
| MLOps pipeline | **Leverage** patterns from VIEWS | Proven at scale for monthly forecasting |

### Key Takeaway

The landscape analysis confirms that **no existing platform does what Causal Atlas aims to do**. The closest precedents are:
- **AfroGrid** -- multi-domain data on a common grid, but static, Africa-only, and no analysis
- **VIEWS** -- sophisticated ML pipeline on PRIO-GRID, but single-domain (conflict) and prediction-focused
- **Tigramite** -- excellent causal discovery algorithms, but no data integration or visualisation

Causal Atlas's unique value proposition is the **combination** of multi-domain data harmonisation, automated causal discovery, interactive visualisation, and AI-assisted interpretation. Each individual component can leverage existing tools; the integration is what we must build.

---

*This analysis should be revisited quarterly as platforms evolve. Key items to watch: PRIO-GRID v3 reaching Beta status, HDX HAPI graduating from Beta, Kepler.gl DuckDB capabilities maturing, and any new entrants in the cross-domain spatiotemporal analysis space.*
