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
8a. [deck.gl Ecosystem](#8a-deckgl-ecosystem)
8b. [MapLibre GL JS](#8b-maplibre-gl-js)
9. [ACLED Dashboard & Tools](#9-acled-dashboard--tools)
10. [GDELT Analysis Service](#10-gdelt-analysis-service)
11. [Other Relevant Open-Source Projects](#11-other-relevant-open-source-projects)
12. [OCHA ReliefWeb](#12-ocha-reliefweb)
13. [Pacific Disaster Center (PDC) -- DisasterAWARE](#13-pacific-disaster-center-pdc----disasteraware)
14. [INFORM Model](#14-inform-model)
15. [Global Conflict Risk Index (GCRI)](#15-global-conflict-risk-index-gcri)
16. [CrisisReady / Direct Relief](#16-crisisready--direct-relief)
17. [MapAction](#17-mapaction)
18. [iMMAP](#18-immap)
19. [Humanitarian OpenStreetMap Team (HOT)](#19-humanitarian-openstreetmap-team-hot)
20. [Comparative Summary](#20-comparative-summary)
21. [Implications for Causal Atlas](#21-implications-for-causal-atlas)
22. [Operational Early Warning Systems](#22-operational-early-warning-systems)
23. [Data Visualization Platforms Used by Humanitarian Actors](#23-data-visualization-platforms-used-by-humanitarian-actors)
24. [Novel Platform Ideas Relevant to Causal Atlas](#24-novel-platform-ideas-relevant-to-causal-atlas)

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

### VIEWS 2.0 / Next-Generation Platform (views-platform)

As of March 2025, VIEWS is undergoing a major architectural transition from the legacy `prio-data` GitHub organisation to the new `views-platform` organisation. The new platform represents a ground-up rearchitecture:

**GitHub Organisation:** https://github.com/views-platform

**Key Repositories in views-platform:**

| Repository | Purpose | Key Detail |
|---|---|---|
| `views-pipeline-core` | Main pipeline orchestration: data ingestion, preprocessing, model/ensemble training, evaluation, experiment tracking | The central nervous system of the platform |
| `views-models` | All implemented models at pgm and cm levels, with prediction targets, input data specs, and algorithm configs | Currently supports stepshift models; expanding to other architectures |
| `views-stepshifter` | Stepshifter model class implementation | Wraps the `stepshift` package with VIEWS-specific config |
| `views-hydranet` | HydraNet model class: CNN-LSTM hybrid for spatiotemporal forecasting | Multi-task learning with probabilistic predictions; predicts state-based, non-state, and one-sided violence with uncertainty quantification |
| `views-evaluation` | Stores, calculates, and manages evaluation metrics for time-series forecasting models | Standardised evaluation across all model types |
| `views-dataviz` | Visualisation utilities for forecasts and evaluations | Notebook-friendly plotting |
| `views-data` | Data management and access layer | Successor to the VIEWSER client |

**Stepshift Algorithm -- Deep Dive:**

The stepshift approach (Hegre et al. 2020, Appendix A) is the core forecasting strategy:

1. Instead of recursive multi-step forecasting (where a 6-month-ahead prediction depends on the 5-month prediction, which depends on the 4-month prediction, etc.), stepshift trains **independent models for each forecast horizon**.
2. For a 36-month forecast window, this means 36 separate models, each trained to predict the target variable at a specific future time step.
3. Each model uses the **same feature set** but with different target offsets. The `StepshiftedModels` class in the `stepshift` package handles this transparently with a scikit-learn-compatible API.
4. This avoids error accumulation that plagues recursive approaches.
5. The trade-off: 36x the number of models to train, but each model is simpler and independently evaluable.

```python
# Conceptual stepshift usage (from the stepshift package)
from stepshift.views import StepshiftedModels
import sklearn.ensemble

base_model = sklearn.ensemble.GradientBoostingRegressor()
ssm = StepshiftedModels(base_model, steps=[1, 2, 3, ..., 36])
ssm.fit(X_train, y_train)
predictions = ssm.predict(X_test)  # Returns predictions at each horizon
```

**HydraNet Architecture:**

HydraNet is a more recent addition representing the shift toward deep learning:
- **CNN-LSTM hybrid** architecture that captures both spatial patterns (via convolutional layers over the grid) and temporal dynamics (via LSTM layers).
- **Multi-task learning:** simultaneously predicts state-based conflict, non-state conflict, and one-sided violence -- sharing spatial/temporal representations across tasks.
- **Probabilistic predictions** with uncertainty quantification, addressing a key limitation of point-estimate models.
- Represents the cutting edge of the VIEWS modelling pipeline.

**Data Access (VIEWSER Client):**

Models in the VIEWS pipeline fetch data from a central database via the VIEWSER client by specifying a "queryset" -- a declarative specification of which variables, transformations, and time periods to retrieve:

```python
# Conceptual VIEWSER queryset
from viewser import Queryset, Column
qs = Queryset("my_model_data", "priogrid_month")
qs = qs.with_column(Column("ucdp_ged_best_sb", from_table="ged2_pgm", transforms=[("moving_average", 12)]))
qs = qs.with_column(Column("wdi_ny_gdp_pcap_pp_kd", from_table="wdi_cy"))
data = qs.publish().fetch()
```

**MLOps Stack:**
- **Weights & Biases** for experiment tracking (uses adjective-noun naming convention for model runs).
- **Automated monthly forecast runs** with drift detection and quality assurance checks.
- Industry-grade CI/CD pipeline for model deployment.

### Limitations

- **Single-domain focus** -- VIEWS predicts conflict only. It does not discover cross-domain causal relationships (e.g., drought causing conflict).
- **Prediction, not explanation** -- the pipeline is optimised for forecast accuracy, not for identifying causal mechanisms.
- **Heavy infrastructure** -- the full MLOps pipeline requires significant compute and operational resources.
- **Python ecosystem** -- fortunately aligned with our tech stack direction.
- **CC BY-NC-SA 4.0 licence** -- limits commercial use of the code.
- **Africa and Middle East focus** -- expanding globally but not yet fully global.

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

### Detailed Harmonisation Methods

**NDVI Harmonisation:**
- Source: MODIS satellite imagery.
- Three monthly metrics computed per grid cell: NDVI mean, NDVI min, and NDVI max.
- NDVI mean captures average vegetation coverage; min/max capture within-month variability -- critical for detecting sudden vegetation stress events (e.g., drought onset).
- Raw MODIS NDVI tiles are aggregated to 0.5-degree grid cells using area-weighted averaging.
- Cloud-contaminated pixels are filtered before aggregation.

**Dual-Series Nighttime Lights Harmonisation:**
- This is AfroGrid's most technically complex contribution.
- **Problem:** Two satellite systems measured nighttime lights over different periods: DMSP-OLS (1992-2013) and NPP-VIIRS (2012 onwards). They use different sensors, spatial resolutions, and measurement units. Naive concatenation produces a discontinuity at the 2012/2013 overlap.
- **Solution:** AfroGrid uses the Li et al. (2020) harmonisation method ("A harmonized global nighttime light dataset 1992-2018", Nature Scientific Data), which:
  1. Quantifies monthly VIIRS nighttime light radiance over the continent.
  2. Calculates the statistical relationship between DMSP and VIIRS during the overlap period (2012-2013).
  3. Applies a calibration function to create a continuous, comparable time series spanning the full period.
- This dual-series approach is particularly important for Africa, where DMSP's limited dynamic range poorly captures low-emission rural areas.

**SPEI (Drought) Alignment:**
- SPEI (Standardised Precipitation Evapotranspiration Index) is calculated at the 1-month timescale.
- SPEI incorporates both precipitation and temperature (via potential evapotranspiration), making it more comprehensive than precipitation-only indices.
- Positive SPEI values indicate water surplus; negative values indicate water stress.
- Source: CRU TS / GPCC datasets, which provide global monthly gridded climate data.
- Native resolution (~0.5 degrees) aligns well with PRIO-GRID cells, requiring minimal spatial transformation.

**Conflict Data Alignment:**
- Point-level conflict events (from UCDP-GED, ACLED, SCAD, PITF) are assigned to their containing 0.5-degree grid cell using the event's geocoordinates.
- Monthly counts of events and fatalities are aggregated per grid cell.
- Multiple conflict typologies preserved: state-based, non-state, one-sided violence.
- ACLED provides additional granularity: riots, protests, strategic developments, etc.

**Temporal Alignment Strategy:**
- All variables converted to calendar month observations.
- For variables with finer temporal resolution (e.g., daily ACLED events), monthly sums or means are computed.
- For variables with coarser temporal resolution (e.g., annual population data), values are held constant across all months of the year or linearly interpolated.
- The overlap of temporal coverage varies by source (UCDP-GED from 1989, ACLED from 1997, PITF from 1995, SCAD 1990-2017), creating a "staircase" of available variables across time.

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

### HDX Data Grids

In 2019, HDX introduced **Data Grids** -- curated collections of the most critical datasets for countries with a Humanitarian Response Plan (HRP). Based on extensive user research, Data Grids organise crisis data into six categories:

1. **Affected people** -- displacement, refugees, IDPs, casualties
2. **Coordination and context** -- 3W (Who does What Where), funding, operational presence
3. **Food security, nutrition, and poverty** -- IPC classifications, food prices, malnutrition rates
4. **Geography and infrastructure** -- admin boundaries, roads, health facilities, schools
5. **Health and education** -- health facility locations, disease surveillance, school data
6. **Climate** -- precipitation, temperature, vegetation indices

As of early 2025, approximately **74% of relevant, complete crisis data** is available and up-to-date across 22 humanitarian operations, up from 70% in 2024.

### HDX Quick Charts

HDX provides **Quick Charts** -- auto-generated visualisations for datasets that follow standard schemas. These include key figures, charts, and maps. An open-source JavaScript dashboard built from HDX HAPI data is available for developers to copy and adapt.

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

### Deep Dive: Architecture

**Rendering Pipeline:**
- Kepler.gl is built on **deck.gl** (WebGL/WebGPU rendering) and **MapLibre GL JS** (base map tiles).
- The rendering pipeline: Data -> Redux Store -> Layer Configuration -> deck.gl Layer Instances -> WebGL Draw Calls -> GPU -> Canvas.
- Each layer type (point, hexbin, arc, etc.) maps to a specific deck.gl layer class.
- GPU-accelerated rendering means millions of data points can be rendered at interactive frame rates.

**Redux State Management:**
- The entire map state (datasets, layers, filters, map view, interactions) lives in a Redux store.
- Kepler.gl provides a **reducer** (`keplerGlReducer`) that handles all state transitions.
- **react-palm** middleware manages side effects (data processing, file I/O).
- External applications can dispatch Redux actions to programmatically control the map: add data, change filters, update layer styles, etc.
- This architecture makes kepler.gl highly embeddable but requires developers to understand Redux patterns.

**Dependency Injection / Customisation:**
- Kepler.gl supports replacing UI components via a factory/injection system.
- Developers can override the side panel, map control, tooltip, and other UI elements with custom React components.
- Custom layer types can be added by extending deck.gl layer classes.
- This is critical for Causal Atlas: we can inject causal analysis panels, lag-correlation views, and custom tooltip displays.

### DuckDB-WASM Integration (v3.1+) -- Deep Dive

**Architecture:**
- DuckDB compiled to WebAssembly (WASM) runs entirely in the browser tab.
- Users can write SQL queries that execute against in-browser DuckDB tables.
- DuckDB's spatial extension enables spatial SQL (ST_Contains, ST_Distance, etc.) on GeoParquet data.
- **Spatially partitioned GeoParquet** files on cloud storage (S3, GCS) can be queried without downloading the entire file -- DuckDB reads only relevant row groups/partitions based on the query.

**Workflow:**
1. Drag and drop files (CSV, Parquet, GeoJSON) into kepler.gl to create DuckDB tables.
2. Write SQL queries in the query panel -- including spatial functions.
3. Results are passed directly to the rendering pipeline.
4. Schema panel updates to reflect query results.

**Implications for Causal Atlas:**
- We could serve pre-computed causal analysis results as GeoParquet files on cloud storage.
- Users could query them with SQL in the browser: `SELECT * FROM causal_links WHERE source_domain = 'drought' AND target_domain = 'conflict' AND lag_months BETWEEN 3 AND 6`.
- No backend server required for exploration of pre-computed results.
- **However:** DuckDB-WASM has memory limits (~2-4 GB depending on browser) and the spatial extension may not be fully available in all WASM builds as of early 2025.

### Version History

| Version | Date | Key Changes |
|---|---|---|
| v1.x | 2018-2019 | Original Uber release. Mapbox GL JS dependency. Basic layers. |
| v2.x | 2019-2022 | Added H3, S2 layers. Improved filters. Better embedding API. |
| v3.0 | Dec 2023 | Major rewrite. Migrated from Mapbox GL to MapLibre GL. New layer architecture. Dramatically improved developer experience. |
| v3.1 | Mid 2024 | DuckDB integration. GeoParquet support. AI assistant for SQL generation. Vector tile rendering with PMTiles. |
| v3.2 | Late 2024 | DuckDB improvements, drag-and-drop file loading, schema panel updates. |

### Performance Limits

- File upload limit: **250 MB** in Chrome (Safari handles larger files but with degraded performance).
- Can render **millions of points** with spatial aggregation layers (hexbin, grid, heatmap).
- For raw point layers, performance degrades significantly above ~1-2 million points depending on GPU.
- **No hard limit on number of datasets**, but each additional dataset/layer reduces frame rate.
- UI responsiveness can lag with large datasets due to Redux state management overhead.
- **Recommendation for Causal Atlas:** Pre-aggregate data to PRIO-GRID resolution before sending to kepler.gl. At 0.5-degree resolution, the entire globe is ~260,000 land cells -- well within kepler.gl's comfort zone.

### Kepler.gl Jupyter Widget

- Python package: `keplergl` on PyPI (v0.3.4+ for kepler v3 compatibility).
- Renders an interactive kepler.gl map directly in Jupyter notebooks (Lab and classic).
- Useful for data exploration during research/development before building the web frontend.
- Supports adding data from Pandas DataFrames, GeoDataFrames, and CSV files.
- Map state (layers, filters, styles) can be exported as JSON and reused in the web application.

```python
from keplergl import KeplerGl
import pandas as pd

map_1 = KeplerGl(height=600)
df = pd.read_csv("conflict_data.csv")
map_1.add_data(data=df, name="conflict_events")
map_1  # Renders in notebook
```

### Foursquare Studio vs. Kepler.gl

| Feature | Kepler.gl (Open Source) | Foursquare Studio |
|---|---|---|
| **Cost** | Free, MIT licence | Freemium (generous free tier) |
| **Hosting** | Self-hosted or kepler.gl demo | Cloud-hosted by Foursquare |
| **Layers** | 15+ standard layers | All kepler.gl layers + Flow layer + specialty layers |
| **Analysis** | None | Cluster/outlier analysis, suitability analysis |
| **Collaboration** | None | Shared datasets, maps, team features |
| **Data connectors** | File upload only | Database connectors (Snowflake, BigQuery, etc.) |
| **Publishing** | Export as HTML | Branded/unbranded web publishing with password protection |
| **DuckDB** | Yes (v3.1+) | Yes |
| **Embeddable** | Yes (React component) | No (hosted platform) |

**Decision for Causal Atlas:** Use kepler.gl (open source) as our embedded React component. The embeddability and customisation options are essential; Studio's hosted model does not support deep integration.

### Limitations

- **Visualisation only** -- no statistical analysis, no causal inference, no time-series tools.
- **No built-in temporal animation** for time-series beyond the Trip layer. Time filtering exists but is basic.
- **MapLibre GL base maps** -- requires tile sources for base maps (free options available: OpenStreetMap, Stadia Maps, etc.). No longer requires Mapbox token since v3.0.
- **Complex Redux integration** -- embedding requires understanding Redux middleware and state management.
- **Performance limits** -- while "large-scale", extremely large datasets (100M+ rows) require server-side pre-aggregation.

---

## 8a. deck.gl Ecosystem

**What it is:** The vis.gl framework suite -- a collection of open-source libraries for high-performance geospatial and data visualisation on the web. Kepler.gl is built on top of deck.gl, but understanding the full ecosystem informs our architectural decisions.

**Links:**
- deck.gl: https://deck.gl/
- vis.gl umbrella: https://vis.gl/
- GitHub: https://github.com/visgl/deck.gl

### Framework Components

| Framework | Purpose | Current Version (March 2025) |
|---|---|---|
| **deck.gl** | High-performance WebGPU/WebGL2 visualisation of large datasets | v9.0 |
| **luma.gl** | Low-level WebGPU and WebGL2 rendering and compute | v9.0 |
| **loaders.gl** | Loaders for big data, geospatial, and 3D file formats (GeoJSON, GeoParquet, CSV, Arrow, tiles) | v4.2+ |
| **math.gl** | Math library for 3D and geospatial calculations (coordinate transforms, projections) | v4.0 |

### Key Design Principles

- **Zero-copy binary data:** The ecosystem is optimised for compact binary columnar data (Apache Arrow format) rather than bloated deserialized JavaScript objects. This brings better memory usage and improved load/processing performance on big datasets.
- **GPU-first rendering:** Data flows from binary buffers directly to GPU attribute buffers, minimising CPU overhead.
- **Composable layers:** deck.gl layers are composable -- complex visualisations are built by stacking multiple layers.

### loaders.gl -- Relevant Capabilities

| Loader | Formats | Relevance |
|---|---|---|
| `CSVLoader` | CSV, TSV | Standard tabular data |
| `ArrowLoader` | Apache Arrow IPC | Columnar binary data for performance |
| `ParquetLoader` | Apache Parquet, GeoParquet | Our primary data format |
| `GeoJSONLoader` | GeoJSON | Administrative boundaries, custom regions |
| `MVTLoader` | Mapbox Vector Tiles | Tiled base map data |
| `PMTilesLoader` | PMTiles | Single-file tile archives |

### Implications for Causal Atlas

- **Parquet -> Arrow -> deck.gl** is the optimal data pipeline for browser-based visualisation.
- loaders.gl can read GeoParquet files directly, feeding deck.gl layers without intermediate conversion.
- math.gl handles coordinate transforms needed for grid-cell visualisation.
- The entire pipeline is open source and actively maintained by the OpenJS Foundation.

---

## 8b. MapLibre GL JS

**What it is:** An open-source fork of Mapbox GL JS (forked in December 2020 when Mapbox switched to a non-open-source licence). Provides GPU-accelerated vector tile rendering in the browser. Used by kepler.gl v3+ as its base map rendering engine.

**Links:**
- Website: https://maplibre.org/
- GitHub: https://github.com/maplibre/maplibre-gl-js (~7k stars)
- Documentation: https://maplibre.org/maplibre-gl-js/docs/

### Current Capabilities (March 2025)

- **Full vector tile rendering** with style specification compatible with Mapbox GL styles.
- **3D terrain** and sky rendering.
- **Globe view** (3D globe projection).
- **Custom layer API** for integrating non-tile-based rendering (e.g., deck.gl layers).
- **WebGPU support** in progress.
- **Martin v1.0** (landmark release, November 2025) -- the fastest open-source tile server, integrating well with MapLibre.
- **MapLibre Tile Specification** -- a next-generation tile format redesigned for modern geospatial data volumes, deemed stable as of October 2025.

### Tile Generation with Tippecanoe

**Tippecanoe** (https://github.com/felt/tippecanoe) is the standard tool for creating vector tilesets from large GeoJSON files:

- Automatically chooses detail levels and simplification for each zoom level.
- Produces MBTiles or PMTiles output files.
- Handles millions of features efficiently.
- **PMTiles** format is particularly interesting: single-file tile archives that can be served from any static file host (S3, GitHub Pages, etc.) without a tile server.

**Relevance for Causal Atlas:**
- We could pre-generate vector tiles from PRIO-GRID geometries using tippecanoe.
- Serve tiles as PMTiles files from static storage.
- MapLibre GL renders these tiles efficiently with style-based theming.
- deck.gl layers overlay analysis results on top of the MapLibre base map.
- This stack (MapLibre + deck.gl + PMTiles) is entirely open-source and requires no tile server infrastructure.

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

## 12. OCHA ReliefWeb

**What it is:** The leading humanitarian information source, providing crisis updates, reports, maps, and data since 1996. Managed by OCHA.

**Links:**
- Website: https://reliefweb.int/
- API Documentation: https://apidoc.reliefweb.int/
- ReliefWeb Labs: https://reliefweb.int/labs
- R package (disastr.api): https://github.com/cran/disastr.api

### API Access

- **Publicly accessible** via HTTP GET/POST requests, returning JSON.
- **No authentication required.**
- Rate limits: max 1,000 entries per call, max 1,000 calls per day.
- Content available from 1996 onwards (some UN reports from the 1980s).
- Covers: reports, jobs, training, disasters, countries, sources.
- **Disaster taxonomy:** Standardised disaster type vocabulary via OCHA's Taxonomy as a Service.
- **Publishing API** (in testing): Allows content partners to submit updates, jobs, or training programmatically.

### Data Types

| Resource | Coverage | Use Case |
|---|---|---|
| **Reports** | Since 1996 | Situation reports, assessments, appeals |
| **Disasters** | Since 1981 | Disaster names, types, GLIDE numbers |
| **Countries** | Global | Country profiles with crisis status |
| **Sources** | 2,000+ organisations | Organisation metadata |

### What We Can Reuse

- **Crisis event timeline data** -- ReliefWeb's disaster records provide a structured timeline of crises that could serve as ground truth for validating causal discoveries.
- **Report metadata** -- could inform contextual AI-generated explanations of discovered causal chains.
- **Disaster taxonomy** -- standardised disaster type classification for our event categorisation.

### Limitations

- **Text-heavy** -- primarily reports and analysis, not structured quantitative data.
- **Low API rate limits** (1,000 calls/day) compared to other data sources.
- **No spatial grid** -- data is organised by country, not sub-national units.

---

## 13. Pacific Disaster Center (PDC) -- DisasterAWARE

**What it is:** A multi-hazard early warning and decision support platform used by tens of thousands of disaster management practitioners globally. Developed by the Pacific Disaster Center.

**Links:**
- Website: https://www.pdc.org/
- DisasterAWARE: https://www.pdc.org/disasteraware/
- DisasterAWARE Explore: https://www.pdc.org/explore-disasteraware/

### Capabilities

- **18 hazard types** monitored in real time with impact and risk estimation.
- **Impact modelling:** Highest-resolution all-hazards impact modelling, providing estimates of impacts to population and critical infrastructure within minutes of a hazard event.
- **Global socioeconomic data** including risk and vulnerability information.
- **AI-augmented** information and advanced analytical reports.
- **Smart Alerts** -- notifications when monitored assets are exposed to hazards.
- **API integration** -- users can integrate their own asset data via the DisasterAWARE API.
- **DisasterAWARE Pro 9.0** (latest): Major enhancements to situational awareness and operational readiness.

### What We Can Learn

- PDC demonstrates that multi-hazard, real-time risk assessment at global scale is operationally feasible.
- Their impact analytics (population and infrastructure exposure estimates) are a model for the kind of impact quantification Causal Atlas could perform.
- The Smart Alert pattern (monitoring + threshold-based notification) could inform a Causal Atlas alerting feature.

### Limitations

- **Not open source** -- DisasterAWARE is free for qualified users but the code is proprietary.
- **Response-focused** -- designed for operational disaster response, not research or causal analysis.
- **No causal inference** -- identifies hazard exposure but does not analyse causal chains.
- **No public bulk data access** -- API is for asset monitoring, not data extraction.

---

## 14. INFORM Model

**What it is:** A global, open-source risk assessment framework for humanitarian crises and disasters. Developed by the European Commission Joint Research Centre (JRC) with the Inter-Agency Standing Committee (IASC). Updated twice yearly.

**Links:**
- Website: https://drmkc.jrc.ec.europa.eu/inform-index
- Methodology: https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk/Methodology
- Subnational models: https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Subnational-risk
- HDX datasets: https://data.humdata.org/organization/inform
- Publications: https://drmkc.jrc.ec.europa.eu/inform-index/About/Publications

### Methodology -- Three Dimensions

INFORM assesses risk through three equally weighted dimensions:

| Dimension | Components | Examples |
|---|---|---|
| **Hazard & Exposure** | Natural hazards (earthquake, flood, tsunami, tropical cyclone, drought, epidemic), human hazards (conflict intensity, projected conflict risk) | Seismic hazard, flood risk, drought probability |
| **Vulnerability** | Socio-economic vulnerability (development, inequality, aid dependency), vulnerable groups (uprooted people, other vulnerable groups) | HDI, Gini coefficient, refugee populations |
| **Lack of Coping Capacity** | Institutional (governance, DRR), infrastructure (communication, physical, access to health) | Government effectiveness, mobile phone subscriptions, hospital beds per capita |

### Key Features

- **80 indicators** aggregated into the three dimensions for **191 countries**.
- **Updated twice yearly** (March and September).
- **Open data** -- all source data and calculations downloadable as Excel spreadsheets.
- **Transparent methodology** -- fully documented aggregation and weighting rules.
- **Country profiles** available as individual downloads.
- **Interactive mapping and charting** application.

### INFORM Subnational Risk

INFORM also produces **subnational risk indices** for specific countries/regions, using the same three-dimension methodology but with subnational indicator data:
- Applied to: South Sudan, Guatemala, Bangladesh, Caucasus and Central Asia, South East Europe, and others.
- Shows detailed within-country risk variation.
- Methodology adaptable to different contexts while maintaining comparability.

### What We Can Reuse

- **The three-dimension framework** (hazard, vulnerability, coping capacity) is a well-established analytical structure for understanding risk.
- **Indicator selection** across 80 variables is a curated reference for which data matters.
- **Open data and methodology** are directly usable -- INFORM scores could be a feature in Causal Atlas.
- **Subnational model methodology** is relevant for our admin-level analysis.

### Limitations

- **Country-level primary resolution** (subnational models exist but require custom implementation per country).
- **Static composite index** -- updated twice yearly, not dynamic or real-time.
- **No causal analysis** -- purely descriptive risk scoring.
- **No temporal dimension** -- provides a snapshot, not trends over time.

---

## 15. Global Conflict Risk Index (GCRI)

**What it is:** A quantitative conflict risk model developed by the JRC, based solely on open-source data, providing quantitative input to the EU early warning framework.

**Links:**
- Website: https://drmkc.jrc.ec.europa.eu/initiatives-services/global-conflict-risk-index
- Concept paper: https://publications.jrc.ec.europa.eu/repository/handle/JRC92293
- 2022 revision: https://publications.jrc.ec.europa.eu/repository/handle/JRC131524
- Regression model methodology: https://publications.jrc.ec.europa.eu/repository/handle/JRC108767

### Methodology

**22 indicators** across **five risk pillars:**

| Pillar | Examples |
|---|---|
| **Political** | Regime type, political stability, state fragility |
| **Security** | Prior conflict history, neighbouring conflict, arms imports |
| **Social** | Ethnic fractionalization, youth bulge, inequality |
| **Economic** | GDP growth, unemployment, resource dependence |
| **Environmental** | Climate variability, natural disaster exposure |

**Model approach:**
- Uses **logistic regression** to calculate probability of conflict onset in the next 1-4 years.
- Distinguishes between:
  - **National conflicts** (civil war over national power)
  - **Subnational conflicts** (over secession, autonomy, or resources)
- The 2022 revision: adopted new UCDP conflict definitions, reduced missing values by replacing data sources, systematically compared 14 probability and intensity models, and incorporated short-term predictor projections.
- Serves as one input to the **EU Conflict Early Warning System (EWS)**, developed by the European External Action Service (EEAS).

### What We Can Learn

- **Indicator selection** across five pillars provides a curated list of conflict-relevant variables.
- **Open methodology** with published regression coefficients enables replication and comparison.
- **The distinction between national/subnational conflict types** is important for Causal Atlas's conflict categorisation.
- GCRI's purely quantitative approach (no expert judgment inputs) aligns with Causal Atlas's data-driven philosophy.

### Limitations

- **Country-level only** -- not subnational grid cells.
- **Conflict-only** -- does not cover other domains.
- **Logistic regression only** -- does not capture non-linear or interaction effects.
- **No causal claims** -- identifies statistical predictors, not causal mechanisms.

---

## 16. CrisisReady / Direct Relief

**What it is:** A research-response partnership between Harvard University and Direct Relief that develops data-driven tools for disaster preparedness, response, and recovery.

**Links:**
- Website: https://www.crisisready.io/
- ReadyMapper: https://www.crisisready.io/optimizing-health-response-during-wild-fires-with-real-time-integrated-data/
- LinkedIn: https://www.linkedin.com/company/crisisready
- Direct Relief: https://www.directrelief.org/

### ReadyMapper Platform

CrisisReady's flagship product, launched 2022:

**Data Sources Integrated (12+ datasets):**
- **Population mobility:** Meta's Data For Good high-resolution population density data (near-real-time movement tracking).
- **Social vulnerability:** CDC Social Vulnerability Index (age, disability, car access, socioeconomic factors).
- **Health infrastructure:** Locations of hospitals, clinics, long-term care facilities globally.
- **Power outages:** Real-time utility outage data.
- **Event dynamics:** Fire perimeters, hurricane tracks, flood extents.
- **Demographics:** Elderly population percentage, durable medical equipment reliance, income data.

**Architecture:**
- Originally designed for US wildfires and hurricanes.
- Now scaled to global disasters.
- Designed by Stamen (a data visualisation firm) for usability by emergency managers.
- Produces customisable reports for front-line decision-makers.

### What We Can Learn

- **Multi-source real-time data fusion** with clear operational outputs is a model for Causal Atlas's more research-oriented platform.
- **Population mobility data** (from Meta/mobile operators) is a data source we should investigate for displacement tracking.
- **The report generation pattern** (synthesise complex multi-source data into a shareable document) could inform Causal Atlas's AI-assisted interpretation output.

### Limitations

- **Not open source** -- Harvard/Direct Relief partnership product.
- **Response-focused** -- designed for crisis response, not causal analysis.
- **US-centric** initially, expanding globally.
- **No causal inference** capabilities.

---

## 17. MapAction

**What it is:** A UK-based humanitarian NGO that provides GIS support and rapid mapping during emergencies. Recently developing an automated data pipeline for humanitarian response.

**Links:**
- Website: https://mapaction.org/
- Pipeline blog: https://mapaction.org/accelerating-humanitarian-response-inside-mapactions-automated-data-pipeline/

### Automated Data Pipeline

**Architecture:**
- **Python and Bash scripts** for data processing.
- **Docker container** (Linux) for portability and consistency.
- **Apache Airflow** for workflow orchestration -- schedules and monitors processing steps.
- **Event-driven design** (future): automatic initiation triggered by GDACS disaster alerts.

**Data Sources:**
- HDX (Humanitarian Data Exchange) -- administrative boundaries, population data, humanitarian indicators.
- Google Earth Engine -- satellite imagery, vegetation indices, precipitation.
- OpenStreetMap -- roads, buildings, points of interest.

**Pipeline Steps:**
1. Triggered by a disaster alert or manual configuration.
2. Acquires relevant datasets for the affected area from multiple sources.
3. Processes and standardises data.
4. Produces standardised situation maps within hours.

**Quality Standards:**
- Developing data quality standards for automated humanitarian data processing.
- Aims to make the pipeline publicly available to the broader humanitarian community.

### What We Can Learn

- **Airflow for geospatial pipeline orchestration** is a proven pattern.
- **Docker containerisation** for reproducible data processing environments.
- **Event-driven pipeline triggers** (GDACS alerts) is an interesting model for Causal Atlas.
- **Multi-source integration** (HDX + GEE + OSM) demonstrates practical humanitarian data fusion.

---

## 18. iMMAP

**What it is:** An international not-for-profit providing information management services to humanitarian and development organisations, turning data into actionable knowledge for decision-makers.

**Links:**
- Website: https://immap.org/
- GitHub: https://github.com/iMMAP
- Services: https://immap.org/our-service/

### Key Platforms and Tools

| Tool | Purpose | Detail |
|---|---|---|
| **Humanitarian Spatial Data Center (HSDC)** | Web-based geospatial platform (launched Aug 2023) | Analytics on demographics, disaster risks, climatic changes |
| **ReportHub** | Reporting platform for humanitarian activities | Standardised activity reporting across organisations |
| **3W Matrix** | "Who does What Where" tracking | Maps partners, activities, and geographic coverage for gap analysis |
| **HeRAMS** | Health Resources & Services Availability Monitoring | Maps service availability at each health facility |
| **DHIS2 integration** | Health information system | Standard WHO district health information system |

### What We Can Learn

- iMMAP's HSDC demonstrates demand for integrated geospatial humanitarian analytics.
- Their training programmes (GIS, data management, Power BI, Kobo Toolbox) reveal the skill levels of target users -- Causal Atlas must be accessible to people with basic GIS/data skills.
- The 3W pattern (who-what-where) is relevant for understanding humanitarian operational presence.

---

## 19. Humanitarian OpenStreetMap Team (HOT)

**What it is:** An international team dedicated to humanitarian action and community development through open mapping. Coordinates volunteer mapping of crisis-affected areas.

**Links:**
- Website: https://www.hotosm.org/
- Tasking Manager: https://tasks.hotosm.org/
- GitHub: https://github.com/hotosm

### Products and Tools

| Tool | Purpose | Detail |
|---|---|---|
| **Tasking Manager** | Coordinates distributed volunteer mapping | Divides areas into grid squares; ~12,000 projects; 241 organisations |
| **Field Tasking Manager (FieldTM)** | Coordinated field mapping | OSM survey forms with conflation workflow |
| **Drone Tasking Manager** | Community-driven drone imagery collection | Emerging tool for high-resolution local mapping |
| **Raw Data API** | High-performance OSM data export | Exports OSM data in various GIS formats (GeoJSON, Shapefile, GeoPackage) |

### Data Products

- **Building footprints** -- digitised from satellite imagery by volunteers.
- **Road networks** -- classification and digitisation.
- **Health facility locations** -- mapped from imagery and field surveys.
- **Missing Maps initiative** -- partnership with MSF and Red Cross.

### What We Can Reuse

- **Raw Data API** could provide building footprint and infrastructure data for exposure analysis.
- **Building density** derived from OSM could serve as a proxy for population density in data-sparse areas.
- HOT data is completely open (ODbL licence) and globally available.

---

## 20. Comparative Summary

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
| CausalAI | - | - | - | - | - | - | - | - | X (archived) | X |
| ReliefWeb | X | - | - | - | - | - | X | X | - (data open) | - |
| DisasterAWARE | - | - | - | - | - | - | X | X | - | - |
| INFORM | X | X | - | X | X | - | X | X | X (data) | - |
| GCRI | X | X | - | X | - | - | - | X | X (data) | - |
| CrisisReady | - | - | - | - | X | - | X | US+ | - | - |
| MapAction | - | X | - | - | - | - | X | X | Partial | - |
| iMMAP HSDC | X | X | - | - | X | - | X | Partial | - | - |
| HOT/OSM | - | - | - | - | - | - | - | X | X | - |

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

## 21. Implications for Causal Atlas

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

## 22. Operational Early Warning Systems

> **Date of findings:** March 2025

These systems operationally predict or monitor crises and are directly relevant to Causal Atlas's positioning. They demonstrate what is currently possible in production early warning and where gaps remain for cross-domain causal analysis.

---

### 22.1 FEWS NET (Famine Early Warning Systems Network)

| Attribute | Detail |
|---|---|
| **URL** | https://fews.net/ |
| **Data Portal** | https://fews.net/data (FEWS NET Data Explorer) |
| **USGS Earth Observation** | https://earlywarning.usgs.gov/fews/ |
| **Organisation** | USAID (created 1985), implemented by Chemonics, USGS, NASA, NOAA, UCSB Climate Hazards Center, others |
| **Coverage** | 30+ countries across Africa, Central America, Haiti, Afghanistan, Yemen |
| **Status** | Fully operational since 1985; continuously updated |

**Architecture and Data Pipeline:**

FEWS NET operates through a multi-pillar architecture:
- **Pillar 1 (Technical Analysis):** Field-based teams conducting scenario development, food security classification (using IPC-compatible methodology), and analytical reporting
- **Pillar 2 (Data Hub):** The FEWS NET Data, Learning, and Communications Hub, managed by the American Institutes for Research, provides a web-based Information Management System (IMS) housing ~21 million food security-related data points accessible via API and the FEWS NET Data Explorer (FDE)
- **Pillar 3 (Remote Sensing & Climate):** USGS FEWS NET Project at EROS Center provides satellite image products, derived data, and climate monitoring

**Data Sources and Feeds:**
- **Remote sensing:** CHIRPS rainfall estimates, NDVI vegetation monitoring, MODIS/VIIRS land surface temperature, soil moisture (from NASA FLDAS -- Famine Land Data Assimilation System using Noah 3.6.1 surface model combining MERRA-2 and CHIRPS data)
- **Climate modelling:** Partnerships with NASA, NOAA, UCSB Climate Hazards Center, and NASA Harvest Program for drought/flood early warning
- **Market monitoring:** Staple food prices, cross-border trade flows, macroeconomic indicators
- **Livelihoods:** Livelihood zone baseline profiles documenting how populations sustain themselves under normal and stress conditions
- **Conflict:** Integration of conflict reporting (ACLED, UCDP, local sources) as a key driver of food insecurity
- **Nutrition:** Anthropometric survey data, nutritional surveillance

**Methods:**
- **Scenario development:** Analysts construct "most likely" scenarios for 6-8 month outlook periods, based on convergence of evidence across all data streams
- **IPC-compatible classification:** Food security conditions are classified using phases compatible with the Integrated Food Security Phase Classification (Phase 1: Minimal to Phase 5: Famine)
- **Convergence of evidence:** Qualitative expert judgement guided by quantitative indicators -- NOT a pure statistical model. Analyst expertise is central to the methodology
- **FLDAS modelling:** NASA Land Information System (LIS) adapted for data-sparse developing countries, generating ensemble estimates of soil moisture, evapotranspiration, and other water balance variables

**Lead Time:** 6-8 month outlooks published monthly; emergency alerts issued when rapid deterioration detected

**Accuracy:** FEWS NET has successfully provided advance warning for every major famine since its creation in 1985. Its strength lies in integrating expert knowledge with quantitative data -- a deliberate choice over purely model-driven approaches.

**Output Format:** Monthly reports, food security classification maps (IPC-compatible phases), food security outlooks, market analyses, weather hazards assessments. Machine-readable data via API at fews.net/data.

**Relevance to Causal Atlas:**
- FEWS NET's multi-domain data integration (climate, markets, conflict, livelihoods, nutrition) is the closest operational analogue to what Causal Atlas aims to do analytically
- However, FEWS NET relies heavily on expert judgement rather than automated statistical methods -- precisely the gap Causal Atlas aims to fill
- The ~21 million data points accessible via API could serve as a rich data source for Causal Atlas
- The scenario development methodology could inform how we present causal chain findings to policymakers

---

### 22.2 INFORM Warning

| Attribute | Detail |
|---|---|
| **URL** | https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Warning |
| **Organisation** | Inter-Agency Standing Committee (IASC) Reference Group on Risk, Early Warning and Preparedness + European Commission JRC |
| **Coverage** | Global (191 countries) |
| **Status** | Operational; under active development as forward-looking complement to INFORM Risk |

**What it Does:**
INFORM Warning monitors how crisis and disaster risk is changing and identifies where new or worsening crises could emerge. It is the forward-looking complement to the INFORM Global Risk Index (GRI), which scores structural/baseline risk.

**Data Feeds:**
- Builds on the INFORM GRI framework with its three dimensions: Hazard & Exposure, Vulnerability, and Lack of Coping Capacity
- Uses 80+ indicators from multiple UN and research sources
- Supplements structural risk scores with dynamic/real-time signals of deterioration: conflict escalation, economic shocks, weather anomalies, displacement trends, food price spikes

**Methods:**
- Risk = Hazard & Exposure^(1/3) x Vulnerability^(1/3) x Lack of Coping Capacity^(1/3)
- Composite index combining normalised indicators into functional levels, categories, and dimensions
- Scores range from 0-10 (higher = higher risk)
- Forward-looking indicators overlay trend detection on top of structural risk baselines

**Lead Time:** Designed for anticipatory action -- identifying emerging crises before acute phase. Monthly/quarterly updates.

**Output Format:** Country-level risk scores (Excel, CSV, API), interactive maps, country profiles. Available on HDX: https://data.humdata.org/dataset/inform-global-crisis-severity-index

**Relevance to Causal Atlas:**
- INFORM's composite index methodology demonstrates one approach to multi-domain risk synthesis, but it is fundamentally additive (weighted aggregation) rather than causal
- Causal Atlas could quantify the *causal pathways* underlying INFORM's composite scores -- e.g., how much of a country's risk score change is causally driven by climate vs. conflict vs. economic factors
- Open data availability makes it a strong candidate for integration as a validation benchmark

---

### 22.3 ACLED CAST (Conflict Alert System)

| Attribute | Detail |
|---|---|
| **URL** | https://acleddata.com/platform/cast-conflict-alert-system |
| **Methodology** | https://acleddata.com/methodology/cast-methodology |
| **Organisation** | ACLED |
| **Coverage** | Global, all countries |
| **Status** | Fully operational; merged into unified Early Warning Dashboard (2025) |

**What it Does:**
CAST forecasts the number of political violence events each month for the next six months in every country, predicting three event types: Battles, Explosions/Remote Violence, and Violence Against Civilians, at both country and first administrative division (admin1) levels.

**Data Feeds:**
- Primarily ACLED's own event data (most comprehensive global political violence dataset)
- Supplementary indicators derived from ACLED data: actor-level features, event type distributions, fatality counts, geographic diffusion patterns
- Some external covariates (not fully documented publicly)

**Methods:**
- Four model types fitted per outcome: Random Forest (simple predictors), Random Forest (complex predictors), XGBoost (simple), XGBoost (complex)
- Ensemble of models generates final forecast
- Explainable AI (XAI) component disentangles factors driving each forecast
- Pattern-based predictive modelling accounts for variability in conflict dynamics

**Lead Time:** 1-6 months ahead

**Accuracy:** Varies by context. Stable conflicts with established patterns produce more accurate forecasts; new, volatile conflicts with no historical pattern are harder. Accuracy rates publicly reported on the CAST platform, but ACLED emphasises that "conflict forecast models are never 100% accurate."

**Output Format:** Interactive dashboard with forecast visualisations, downloadable forecasts, trend analysis tools. Integrated with ACLED's Early Warning Dashboard (2025 update) alongside Trendfinder, Conflict Exposure Calculator, and Conflict Index.

**Relevance to Causal Atlas:**
- CAST is single-domain (conflict only) and prediction-focused rather than causal
- Its XAI component for factor decomposition is relevant to Causal Atlas's interpretation layer
- ACLED data is already a key input for Causal Atlas; CAST's forecasts could provide a baseline for comparison
- The 2025 integration of multiple risk tools into a single dashboard is a UX pattern worth studying

---

### 22.4 VIEWS -- Forecast Outputs and Policy Use

| Attribute | Detail |
|---|---|
| **URL** | https://viewsforecasting.org/ |
| **GitHub** | https://github.com/views-platform |
| **Pipeline** | https://github.com/prio-data/views_pipeline |
| **Organisation** | PRIO + Uppsala University |
| **Status** | Operational; monthly forecast releases; awarded Kluz Prize for PeaceTech Special Distinction (2024) |

**Forecast Output Details:**
- Monthly predictions of state-based armed conflict fatalities at two levels:
  - **Country-month (cm):** Global coverage, 1-36 months ahead
  - **PRIO-GRID-month (pgm):** Sub-national predictions for Africa and the Middle East, 1-36 months ahead
- Forecasts include both expected fatality counts and probability distributions (uncertainty quantification)
- January 2026 forecast covers projections through December 2028

**Architecture (as of 2025):**
- Comprehensive MLOps pipeline with centralised logging, model monitoring, and data monitoring
- Branching strategy separating production code from development
- Synchronisation workflows for tightly coupled ML and non-ML components
- Key repositories: views-models, views-stepshifter (time-series forecasts), views-hydranet (spatiotemporal forecasts), views-evaluation (evaluation metrics)
- Monthly update cycle overwrites past 12 months of UCDP-derived data, capturing corrections and updates

**Data Sources:**
- UCDP GED and UCDP Candidate datasets (primary conflict data)
- PRIO-GRID spatial framework
- Supplementary covariates from various socioeconomic and geographic sources

**2023/24 Prediction Challenge:**
- Invited 13 research institutions to submit competing models
- Challenge target: predict conflict fatalities as probability distributions for July 2024 - June 2025
- VIEWS' benchmark model "Conflictology" led rankings for both country- and subnational-level predictions as of February 2025
- Published in *Journal of Peace Research* (Hegre et al., 2024)

**Policy Use:**
- Used by policymakers to anticipate and prepare for potential conflicts
- Designed to increase preparedness for low-probability, high-impact crises
- Monthly release cadence aligns with policy planning cycles

**Relevance to Causal Atlas:**
- VIEWS demonstrates that monthly sub-national forecasting on PRIO-GRID is operationally viable at scale
- Its MLOps pipeline architecture is the most mature open-source model for what Causal Atlas needs
- However, VIEWS is single-domain (conflict) and does not perform causal analysis across domains
- The Prediction Challenge methodology could inform how Causal Atlas benchmarks its own causal discovery methods

---

### 22.5 WFP ADAM (Automatic Disaster Analysis & Mapping)

| Attribute | Detail |
|---|---|
| **URL** | https://geonode.wfp.org/adam.html |
| **Organisation** | World Food Programme |
| **Coverage** | Global (floods, earthquakes, tropical storms) |
| **Status** | Operational; ADAM+ in testing 2024-2025 |

**What it Does:**
ADAM collects, analyses, and maps geospatial and socio-economic information following sudden-onset humanitarian emergencies. Within minutes of an earthquake, it automatically creates a dashboard with magnitude, location, depth, estimated affected population, nearby infrastructure, and distance to the closest WFP facility.

**Data Feeds:**
- Seismic data (USGS, regional networks)
- Tropical storm tracking data (NOAA, JTWC)
- Flood detection (satellite imagery, river gauge networks)
- Population density data (WorldPop, GPW)
- WFP operational presence and facility locations
- Infrastructure data (roads, airports, ports)

**Methods:**
- Automated trigger rules based on event magnitude/severity thresholds
- Spatial intersection of hazard footprints with population and infrastructure layers
- **ADAM+ (2024-2025):** Partnering with the Global Earthquake Model Foundation (GEM) to integrate ground shake data and GEM's structural risk model. Being tested in Afghanistan, Syria, Turkey, Myanmar, and the Philippines.

**Lead Time:** Near-real-time for sudden-onset events (minutes for earthquakes, hours for tropical storms). Essentially reactive, not predictive.

**Output Format:** Automated dashboards with maps, population exposure estimates, infrastructure impact assessments. Published on HDX.

**Relevance to Causal Atlas:**
- ADAM demonstrates automated rapid assessment -- Causal Atlas could complement this with pre-disaster causal risk assessment
- Integration of hazard footprints with socioeconomic data is a pattern Causal Atlas should replicate
- ADAM is reactive; Causal Atlas is analytical/causal -- they serve different but complementary purposes

---

### 22.6 INFORM Severity Index (Global Crisis Severity Index)

| Attribute | Detail |
|---|---|
| **URL** | https://www.acaps.org/en/thematics/all-topics/inform-severity-index |
| **Methodology** | https://www.acaps.org/fileadmin/Dataset/Methodology_files/20240930_ACAPS_Severity_index_data_collection_manual.pdf |
| **Organisation** | ACAPS (managed on behalf of the IASC) |
| **Coverage** | All ongoing humanitarian crises globally |
| **Status** | Operational; updated monthly |

**What it Does:**
Measures the severity of ongoing humanitarian crises (distinct from INFORM Risk, which measures potential future risk). Ranks crises by severity to inform priority-setting and resource allocation.

**Data Feeds:**
- 31 core indicators across three dimensions:
  1. **Impact:** Deaths, displacement, affected population
  2. **Conditions of affected people:** Food security (IPC data), health, WASH, shelter, protection
  3. **Complexity:** Access constraints, operating environment, information landscape
- Data from: IPC, UNHCR, IOM DTM, OCHA, FSNAU, WFP, government sources
- Multi-Sectoral Needs Assessments (MSNAs)
- When main crisis driver is food insecurity: IPC figures used directly

**Methods:**
- All indicators scored on a 1-5 scale
- Aggregation into components, dimensions, and overall severity category
- Mixed-method: quantitative indicators + qualitative analyst assessment
- Compatible with IPC methodology for food security indicators

**Output Format:** Monthly severity rankings, country profiles, downloadable datasets (available on HDX). API access via https://api.acaps.org/

**Relevance to Causal Atlas:**
- The severity scoring framework provides a standardised outcome variable that Causal Atlas could attempt to predict causally
- Monthly cadence matches Causal Atlas's temporal resolution
- Open data via API makes integration straightforward

---

### 22.7 IPC Alert System (Integrated Food Security Phase Classification)

| Attribute | Detail |
|---|---|
| **URL** | https://www.ipcinfo.org/ |
| **Organisation** | IPC Global Partnership (FAO, WFP, UNICEF, + others) |
| **Coverage** | 30+ countries |
| **Status** | Fully operational; the global standard for food security classification |

**What it Does:**
Classifies food security conditions into five phases and triggers humanitarian response protocols at specific thresholds:
- **Phase 1 (Minimal):** No acute food insecurity
- **Phase 2 (Stressed):** Livelihoods under stress; food assistance may be needed
- **Phase 3 (Crisis):** Acute food insecurity; emergency food assistance required
- **Phase 4 (Emergency):** Severe acute food insecurity; urgent action needed
- **Phase 5 (Famine):** Mass starvation and death; immediate full-scale response

**Alert Mechanisms:**
- **Risk of Worsening Phase:** Three alert levels -- Watch, Moderate Risk, High Risk
- **Famine Likely:** Applied to projections as an early warning when evidence is insufficient to confirm Phase 5 but highly suggestive
- **Humanitarian food assistance mapping:** Areas receiving significant food aid are flagged; areas that would be one Phase worse without aid are identified

**Data Feeds:**
- Convergence of evidence from: production data, livestock prices, market prices, civil insecurity, malnutrition rates, WASH indicators, mortality data
- FEWS NET analysis (IPC-compatible)
- National food security surveys and assessments

**Methods:**
- Consensus-based analysis (multiple organisations must agree)
- Evidence convergence using IPC Acute Food Insecurity (AFI) Reference Tables
- Analysis adheres to protocols for units of analysis, humanitarian assistance accounting, evidence documentation, and mapping standards

**Response Trigger:** Phase 3+ classifications trigger humanitarian response planning cycles. Phase 5 (Famine) declarations mobilise maximum international response.

**Relevance to Causal Atlas:**
- IPC phases are the most widely used outcome variable in food security research -- Causal Atlas should support IPC-compatible output
- The "convergence of evidence" methodology is conceptually similar to what Causal Atlas does statistically, but IPC does it through expert consensus
- IPC data is available via FEWS NET and HDX APIs

---

### 22.8 IOM DTM (Displacement Tracking Matrix) Early Warning

| Attribute | Detail |
|---|---|
| **URL** | https://dtm.iom.int/ |
| **Methodology** | https://dtm.iom.int/about/methodological-framework (2nd Edition) |
| **Organisation** | International Organization for Migration (IOM) |
| **Coverage** | 90+ countries |
| **Status** | Operational; DTM Methodological Framework 2nd Edition published |

**What it Does:**
Tracks and monitors displacement and population mobility. Issues Early Warning Flash Alerts and Emergency Event Tracking Reports when displacement events escalate.

**Data Collection:**
- In-depth interviews with community leaders, local government, health workers, teachers, Red Cross workers
- Site assessments for displacement camps and settlement areas
- Flow monitoring at key transit points
- Survey-based needs assessments
- Customisable tool selection per context -- the framework emphasises flexibility to combine methods

**Early Warning Components:**
- **Flash Alerts:** Rapid notifications via mailing lists when displacement events detected
- **Emergency Event Tracking:** Focused reports on escalating situations (e.g., extensively used in Sudan crisis)
- **Baseline assessments:** Population counts and location tracking for ongoing displacement

**Output Format:** Reports, datasets, interactive dashboards. Progress reports published annually. Data available on HDX.

**2024 Performance:** DTM tracked displacement across 90+ countries; Progress 2024 report documents operational reach and data coverage. Natural Hazard Displacement Overview 2025 published covering displacement from natural hazards.

**Relevance to Causal Atlas:**
- DTM displacement data is a key outcome variable for Causal Atlas -- displacement is often the result of causal chains (drought -> food insecurity -> displacement, or conflict -> displacement)
- The flexibility of DTM's methodological framework (combining tools per context) is a design principle Causal Atlas should consider
- DTM data available via DTM API and HDX

---

### 22.9 WFP Conflict Forecast

| Attribute | Detail |
|---|---|
| **URL** | https://innovation.wfp.org/project/conflict-forecast |
| **Organisation** | World Food Programme |
| **Status** | Operational |

**What it Does:**
Predicts armed conflict and disruptive events (protests, riots) by combining ML panel forecasting with NLP analysis. Helps WFP decision-makers visualise conflict events and plan operations.

**Data Feeds:**
- Multiple conflict datasets (ACLED primary)
- Socio-economic indicators
- Population density
- Critical infrastructure and services data
- Subnational-level resolution

**Methods:**
- Machine learning panel forecasting models
- Natural Language Processing for text-based conflict signals
- Subnational predictions

**Related Tool -- PREDICT:**
- Developed in partnership with Danish Refugee Council
- Uses ML to anticipate displacement patterns up to 4 months ahead
- Integrates open-source conflict, food security, and climate data

**Relevance to Causal Atlas:**
- WFP's cross-domain integration (conflict + food security + climate) is the closest operational use case to Causal Atlas's analytical vision
- PREDICT's 4-month displacement forecasting demonstrates practical demand for the kind of causal chain analysis Causal Atlas aims to provide

---

## 23. Data Visualization Platforms Used by Humanitarian Actors

> **Date of findings:** March 2025

What do practitioners ACTUALLY use for decision-making? Understanding operational visualization tools informs Causal Atlas's UI design.

---

### 23.1 HDX Quick Charts

| Attribute | Detail |
|---|---|
| **URL** | https://data.humdata.org/ |
| **Documentation** | https://humanitarian.atlassian.net/wiki/spaces/HDX/pages/40758624/Quick+Charts+JSON+formats |
| **Organisation** | OCHA Centre for Humanitarian Data |

**What it Does:**
Automatically generates up to three charts from any HXL-tagged dataset uploaded to HDX. Users can customise titles, axis labels, and descriptions.

**Technical Architecture:**
- Uses JSON configuration files to define chart types
- Three-level hierarchy: **bites** (single chart definitions) -> **recipes** (collections of bites) -> **cookbooks** (collections of recipes)
- Charts generated based on HXL (Humanitarian Exchange Language) tags in the data
- Supported types: bar charts, line charts, pie charts, choropleth maps

**How It's Used:**
- Rapid data exploration when datasets are uploaded to HDX
- Quick storytelling for situation reports
- Embedded in HDX dataset pages for immediate visual context
- Not designed for deep analysis -- more for quick sense-making

**Relevance to Causal Atlas:**
- HXL tagging convention is worth adopting for interoperability with the humanitarian data ecosystem
- The "auto-generate charts from data tags" concept could inform Causal Atlas's automated visualization of causal relationships
- HDX Quick Charts demonstrates that humanitarians value *speed* over *depth* in initial data exploration

---

### 23.2 ReliefWeb Crisis Figures

| Attribute | Detail |
|---|---|
| **URL** | https://reliefweb.int/ |
| **Data** | https://data.humdata.org/dataset/reliefweb-crisis-figures |
| **Organisation** | OCHA |
| **Status** | Dataset archived; platform continues to operate with alternative approaches |

**What it Does:**
Curated collection of "topline numbers" -- people in need, internally displaced, refugees, food insecure -- for the world's most pressing humanitarian crises. Manually curated by ReliefWeb's editorial team and updated daily.

**Data Sources:**
- CCCM Cluster, FSNAU, FTS, IOM, IPC, OCHA, UNHCR, UNICEF, WFP, and government sources

**Note:** The ReliefWeb Crisis Figures dataset is now archived and no longer updated as a standalone dataset, though ReliefWeb continues to publish thematic figures and visualisations through its main platform.

**Relevance to Causal Atlas:**
- Topline humanitarian metrics (people in need, displaced, food insecure) are key outcome variables for causal analysis
- The standardised metrics demonstrate what policymakers consider "decision-relevant" -- Causal Atlas output should map to these
- The ReliefWeb API remains active for accessing reports and updates

---

### 23.3 OCHA Financial Tracking Service (FTS)

| Attribute | Detail |
|---|---|
| **URL** | https://fts.unocha.org/ |
| **Data on HDX** | https://data.humdata.org/organization/ocha-fts (227 datasets) |
| **Organisation** | OCHA |
| **Status** | Operational; underwent results-oriented transformation since 2022 |

**What it Does:**
Centralised hub for tracking humanitarian funding flows. Provides visibility on where funds come from, where they go, and progress against coordinated plans (Humanitarian Response Plans, Flash Appeals).

**2024 Figures:**
- Total GHO funding tracked: US$23.83bn against US$49.47bn requirements (48.2% coverage)
- Over US$100bn processed since 2022 transformation

**Visualizations:**
- Interactive funding flow dashboards (donor -> recipient -> country/sector)
- Progress bars against plan requirements
- Time-series tracking of funding trends
- Country and sector breakdowns

**Relevance to Causal Atlas:**
- Funding flow data could be a causal variable: does increased funding lead to improved outcomes? What is the lag structure?
- FTS data available via API and on HDX (227 datasets)
- The gap between requirements and funding is itself an outcome Causal Atlas could model causally

---

### 23.4 iMMAP Open Data Cube and Humanitarian Data Infrastructure

| Attribute | Detail |
|---|---|
| **URL** | https://immap.org/ |
| **Organisation** | iMMAP |
| **Status** | Active; phased ODC implementation |

**What it Does:**
iMMAP initiated an Open Data Cube (ODC) project in three phases: Design, Prototype, and Operationalisation. Enables in-house geospatial analytics combining Earth observation data with humanitarian indicators.

**Relevance to Causal Atlas:**
- Demonstrates that humanitarian organisations are actively investing in data cube architectures for integrated analysis
- iMMAP's approach of combining satellite EO with ground-truth humanitarian data is analogous to Causal Atlas's multi-source integration

---

### 23.5 UNHCR Data Visualization Platform

| Attribute | Detail |
|---|---|
| **URL** | https://dataviz.unhcr.org/ |
| **GitHub** | https://github.com/unhcr-dataviz |
| **Organisation** | UNHCR |
| **Status** | Active; 2025 guidelines revision |

**What it Does:**
Provides tools, templates, and guidelines for creating data visualisations within UNHCR. Uses a mix of D3.js custom visualisations and Power BI dashboards.

**Key Features:**
- Standardised chart templates following UNHCR style guidelines
- Animated visualisations of forced displacement over time
- Country-level refugee data dashboards
- IDP crisis tracking visualisations
- 2025 revision updating all chart types, resources, tutorials, and templates

**Relevance to Causal Atlas:**
- UNHCR's approach to standardised visualization templates demonstrates the importance of consistent, branded visual outputs in the humanitarian sector
- Their GitHub repos provide open-source examples of humanitarian data visualization that could inform Causal Atlas's UI

---

### 23.6 Power BI in the Humanitarian Sector

Many UN agencies and humanitarian organisations use Microsoft Power BI for operational dashboards. Key examples:

- **ACAPS:** Published Power BI Training Guide for the Humanitarian Analysis Program (HAP)
- **UNHCR:** Uses Power BI for refugee statistics dashboards alongside custom D3.js visualisations
- **WFP:** VAM (Vulnerability Analysis and Mapping) team uses Power BI for food security monitoring
- **WHO:** Health emergency dashboards (COVID-19, mpox, etc.)
- **OCHA:** Various operational coordination dashboards

**Why Power BI dominates:** Free licensing for nonprofits via Microsoft's Technology for Social Impact programme, low barrier to entry for non-technical analysts, integration with SharePoint and Teams, and embedded publishing for web sharing.

**Relevance to Causal Atlas:**
- The prevalence of Power BI in the sector means Causal Atlas should consider export/embed compatibility with Power BI
- However, Power BI dashboards are typically static (no causal analysis, no temporal lag exploration) -- this is a clear gap Causal Atlas fills
- The fact that most humanitarian visualisation is done in Power BI (a general-purpose BI tool) underscores the lack of purpose-built causal analysis platforms

---

## 24. Novel Platform Ideas Relevant to Causal Atlas

> **Date of findings:** March 2025

Emerging concepts and technologies that could inform Causal Atlas's design or represent future competitive landscape.

---

### 24.1 Digital Twins for Humanitarian Response

**Current State:** Active research area with practical pilots emerging in 2024-2025, but no production-grade humanitarian digital twin exists yet.

**Key Developments:**

- **Digital Risk Twins (DRT):** A 2025 concept (published in npj Natural Hazards) adapting digital twin technology for disaster risk management. Integrates IoT, remote sensing, surveys, and field observations with human-in-the-loop decision-making. URL: https://www.nature.com/articles/s44304-025-00135-x

- **Humanitarian Supply Chain Digital Twins:** Framework demonstrated to significantly reduce response times, optimise resource allocation, and improve multi-agency coordination. Validated using real-world data from UN and Red Cross operations.

- **Crisis Communication Digital Twins:** Frontiers in AI (2026) published research on testing crisis messaging in synthetic populations built from real-world data. Autonomous AI agents embedded in digital twins for emergency preparedness.

- **AR-Digital Twin Framework:** Modular framework linking live data ingestion, hybrid modelling/simulation, and AR interfaces for first responders. Practitioners prioritised situational awareness (71.4%) and real-time information overlays (64.3%).

**Relevance to Causal Atlas:**
- Digital twins require exactly the kind of multi-domain, causally-linked data models that Causal Atlas produces
- Causal Atlas could serve as the "causal engine" powering a humanitarian digital twin
- The synthetic population concept could be used to test how causal chain disruptions propagate through populations

---

### 24.2 Predictive Analytics for Aid Delivery

**Current State:** Growing adoption but significant barriers remain. A 2025 review in ScienceDirect systematically assessed AI in humanitarian aid.

**Key Projects:**
- **WFP PREDICT:** ML-based displacement forecasting (up to 4 months ahead) in partnership with Danish Refugee Council. Uses open-source conflict, food security, and climate data.
- **Forecast-based preparedness:** XGBoost models used to activate agricultural crisis preparedness before events emerge (2024)
- **Fuzzy inference systems:** Used for dynamic shelter activation and evacuation routing decisions (2025)
- **Supply chain optimisation:** AI tested for aid delivery route optimisation, resource allocation across distributed networks, and scenario planning

**Barriers:**
- High cost of AI infrastructure; few humanitarian organisations can invest in specialised skills and tech architecture
- Limited trust in predictive model outputs -- uptake remains constrained by concerns about reliability and validation
- Data availability in crisis contexts is inherently unreliable

**Relevance to Causal Atlas:**
- Causal Atlas's causal chains could improve predictive models by identifying which input variables actually cause outcomes (vs. spurious correlations)
- The trust/validation barrier is critical: Causal Atlas must provide transparent, explainable causal reasoning to gain adoption

---

### 24.3 Causal AI Platforms -- Commercial and Open Source

**The Causal AI landscape as of 2025** has expanded significantly, with both commercial and open-source options:

**Commercial:**

| Platform | Organisation | Key Capability |
|---|---|---|
| **decisionOS** | causaLens | Enterprise Causal AI operating system; cause-and-effect reasoning for business decisions |
| **Dara** (open-source) | causaLens | Python framework for building Causal AI apps; visualise causal graphs interactively |
| **Causaly** | Causaly | Causal AI for life sciences; biomedical knowledge graph with causal reasoning |
| **Databricks Causal AI** | Databricks | Manufacturing root cause analysis using causal inference |

**Open Source (State of the Art):**

| Library | Organisation | Key Capability | Stars | Status |
|---|---|---|---|---|
| **DoWhy** | PyWhy/Microsoft | End-to-end causal inference; graphical causal models + potential outcomes | 7k+ | Active; v0.14 (Nov 2025); time-series support added in v0.13 |
| **EconML** | PyWhy/Microsoft | Heterogeneous treatment effects; ML + econometrics | 4k+ | Active; v0.16.0 (Jul 2025) |
| **Tigramite** | DLR/J. Runge | Time-series causal discovery (PCMCI, PCMCIplus, LPCMCI) | 1.5k+ | Active; v5.2 |
| **CausalNex** | QuantumBlack | Bayesian Networks + causal inference | 2k+ | Maintenance mode |
| **Salesforce CausalAI** | Salesforce | Time series + tabular causal analysis | 600+ | Archived |
| **causal-learn** | CMU | PC, FCI, GES and other discovery algorithms | 1k+ | Active |
| **Tetrad** | CMU | Comprehensive causal discovery (Java, GUI) | -- | Active; longest-standing tool |

**Key Trend:** DoWhy v0.13 (2025) added support for effect estimation over time-series data, making it more directly relevant to Causal Atlas's use case. The PyWhy ecosystem is converging as the primary open-source causal inference stack.

**Relevance to Causal Atlas:**
- Tigramite remains the best fit for Causal Atlas's time-series causal discovery needs (PCMCI specifically designed for large-scale time series)
- DoWhy's new time-series support could complement Tigramite for effect estimation
- The commercial platforms (causaLens, Causaly) demonstrate market demand for causal reasoning tools -- Causal Atlas fills this niche for the humanitarian/research sector at no cost

---

### 24.4 Knowledge Graph Platforms for Crisis Data

**Key Project: KnowWhereGraph**

| Attribute | Detail |
|---|---|
| **URL** | https://knowwheregraph.org/ |
| **Paper** | https://arxiv.org/html/2502.13874v2 |
| **Organisation** | Multi-university consortium (UC Santa Barbara, Wright State, others) |
| **Status** | Active; one of the largest publicly available geospatial knowledge graphs |

**What it is:** A large-scale geospatial knowledge graph integrating 30+ data layers on natural hazards (hurricanes, wildfires), climate variables, soil properties, crop/land cover types, demographics, and human health.

**Applications:**
- Food security and agricultural supply chain analysis
- Sustainability analysis for soil conservation and farm labour
- Delivery of emergency humanitarian aid post-disaster

**Technical Approach:**
- Ontology co-designed with partners in humanitarian relief, food supply chain, and agriculture
- Knowledge graph construction driven by use case demands, data standards, and querying performance
- Semantic web standards (RDF, SPARQL) for interoperability

**Relevance to Causal Atlas:**
- KnowWhereGraph demonstrates that knowledge graphs can integrate the kind of multi-domain geospatial data Causal Atlas needs
- A knowledge graph layer could enhance Causal Atlas by encoding domain knowledge about known causal relationships
- The ontology design methodology (use-case-driven, co-designed with practitioners) is a pattern Causal Atlas should consider
- However, knowledge graphs capture *structural relationships* -- Causal Atlas adds the *statistical/temporal causal discovery* layer on top

---

*This analysis should be revisited quarterly as platforms evolve. Key items to watch: PRIO-GRID v3 reaching Beta status, HDX HAPI graduating from Beta, Kepler.gl DuckDB capabilities maturing, and any new entrants in the cross-domain spatiotemporal analysis space.*
