# Causal Atlas

**An open-source platform for discovering cross-domain causal relationships through spatiotemporal data analysis and visualisation.**

Causal Atlas ingests global event and indicator data from multiple domains — conflict, climate, food security, health, economics, pollution, and more — aligns them on a common spatiotemporal grid, and surfaces statistically significant time-lagged correlations to help researchers, journalists, and policymakers discover how events in one domain ripple into others.

> *"When it comes to climate security and conflict prevention, the only way to anticipate the future is to first examine the past."*

---

## Table of Contents

- [Vision](#vision)
- [The Gap This Project Fills](#the-gap-this-project-fills)
- [Landscape Analysis](#landscape-analysis)
  - [Existing Platforms and Frameworks](#existing-platforms-and-frameworks)
  - [Key Lessons from Prior Work](#key-lessons-from-prior-work)
- [Dataset Catalogue](#dataset-catalogue)
  - [Tier 1 — Seed Datasets](#tier-1--seed-datasets)
  - [Tier 2 — Expansion Datasets](#tier-2--expansion-datasets)
  - [Tier 3 — Aspirational Datasets](#tier-3--aspirational-datasets)
  - [Meta-Platforms and Aggregators](#meta-platforms-and-aggregators)
- [Architecture](#architecture)
  - [Design Principles](#design-principles)
  - [System Components](#system-components)
  - [The Spatiotemporal Grid](#the-spatiotemporal-grid)
  - [Statistical Engine](#statistical-engine)
  - [Visualisation Layer](#visualisation-layer)
- [Technology Stack](#technology-stack)
- [Roadmap](#roadmap)
  - [Phase 1 — Foundation (Weeks 1–3)](#phase-1--foundation-weeks-13)
  - [Phase 2 — Discovery Engine (Weeks 4–6)](#phase-2--discovery-engine-weeks-46)
  - [Phase 3 — Interactive Explorer (Weeks 7–10)](#phase-3--interactive-explorer-weeks-710)
  - [Phase 4 — Community and Scale (Ongoing)](#phase-4--community-and-scale-ongoing)
- [Seed Experiment](#seed-experiment)
- [Known Challenges](#known-challenges)
- [Contributing](#contributing)
- [Licence](#licence)
- [Acknowledgements](#acknowledgements)

---

## Vision

The world generates vast quantities of open, geocoded, timestamped data across dozens of domains: earthquakes, droughts, food prices, armed conflict, disease outbreaks, air quality, migration flows, commodity trade, and more. Individually, each dataset tells a story. Layered together with temporal awareness, they can reveal how events cascade across systems — how a drought six months ago feeds a food price spike today, which feeds civil unrest next month.

Institutions like the UN, World Bank, and PRIO have built domain-specific tools that hint at these connections. But no open-source, general-purpose platform exists that:

1. Ingests data from arbitrary domains into a common spatiotemporal grid
2. Provides automated time-lagged cross-correlation detection across any domain pair
3. Makes results visually explorable with temporal playback
4. Is designed for hypothesis-free discovery rather than testing a specific theory
5. Is community-driven, extensible, and freely available to all

Causal Atlas aims to be that platform.

---

## The Gap This Project Fills

| What exists | What it does well | What it lacks |
|---|---|---|
| **PRIO-GRID / VIEWS** | Rigorous spatial grid, conflict + climate integration | Researcher-only, R-based, no visual explorer, limited domains |
| **WFP HungerMapLIVE** | Multi-layer real-time map, conflict + climate + food | Closed source, food-security-specific, no cross-domain correlation engine |
| **GDELT** | Massive global event capture, real-time, free | Raw data only — no spatial grid alignment, no causal analysis tools |
| **ACLED** | Gold-standard conflict data, geocoded, near-real-time | Single domain (conflict); analysis tools are proprietary |
| **HDX (Humanitarian Data Exchange)** | 18,000+ humanitarian datasets, APIs, open | A catalogue, not an analysis platform — no temporal correlation |
| **Kepler.gl** | Beautiful spatiotemporal visualisation, open source | Visualisation only — no statistical engine, no data ingestion pipeline |
| **AfroGrid** | Cross-domain integrated grid (conflict + climate + socioeconomic) | Africa only, 1989–2020, static dataset not a platform |

**Causal Atlas bridges the gap** between the data (GDELT, ACLED, HDX), the spatial framework (PRIO-GRID), the statistical methods (Granger causality, cross-correlation), and the visualisation tools (Kepler.gl) — into a single, open, extensible platform.

---

## Landscape Analysis

### Existing Platforms and Frameworks

#### PRIO-GRID (Peace Research Institute Oslo)
- **What:** A spatiotemporal grid covering all terrestrial areas at 0.5° × 0.5° resolution (~55km at equator)
- **Contains:** Armed conflict events (UCDP), climate indicators, population, ethnic composition, terrain, nightlight emissions
- **Code:** Open source (R package, v3.0 alpha) — [github.com/prio-data/priogrid](https://github.com/prio-data/priogrid)
- **Key insight:** PRIO-GRID v3.0 is designed as a general-purpose spatial data collection and standardisation tool, not just a static dataset. It automatically downloads source data and handles flexible spatiotemporal configuration. This is the natural backbone for Causal Atlas.

#### VIEWS (Violence & Impacts Early-Warning System)
- **What:** ML-based conflict forecasting system built on PRIO-GRID
- **Integrates:** UCDP conflict data, ETCCDI climate extremes, socioeconomic indicators
- **Forecasts:** Up to 3 years ahead, globally
- **Code:** Partially open — [github.com/prio-data](https://github.com/prio-data)
- **Key insight:** Demonstrates that combining climate extremes with conflict indicators on PRIO-GRID produces meaningful predictions. Their preprocessing pipeline for aligning diverse data sources is a template.

#### GDELT (Global Database of Events, Language, and Tone)
- **What:** Real-time global event database monitoring broadcast, print, and web news in 100+ languages
- **Scale:** 200+ million events from 1979 to present, updated every 15 minutes
- **Access:** 100% free — raw CSV files, Google BigQuery, Python library (gdeltPyR)
- **Caution:** Auto-coded from news text, so contains duplicates, miscodings, and media bias. Research shows significant disparities between GDELT's automated coding and researcher-led datasets like ACLED. Best used as a signal/sentiment layer rather than ground truth.
- **Key insight:** GDELT's Global Knowledge Graph (GKG) captures themes, sentiment, and tone — making it valuable as a "media attention" layer that can serve as a leading indicator.

#### WFP HungerMapLIVE
- **What:** Near-real-time global hunger monitoring covering 94 countries
- **Integrates:** Food security, weather, population, conflict (ACLED), hazards, nutrition, macro-economic data
- **ML models trained on:** Population density, nightlight intensity, rainfall, vegetation index, conflict, market prices, macroeconomic indicators, undernourishment — across 63 countries over 14 years
- **Key insight:** Demonstrates the exact multi-domain integration pattern we want, including overlay capabilities. Their choice of input variables (nightlights, vegetation index, rainfall) validates which data streams are most predictive.

#### AfroGrid
- **What:** Integrated 0.5° grid-month dataset for Africa (1989–2020)
- **Contains:** Conflict events (ACLED, UCDP-GED, SCAD), NDVI vegetation, temperature, precipitation, SPEI drought index, nighttime lights, population
- **Published:** Nature Scientific Data (2022)
- **Key insight:** The most complete template for what we're building globally. Their methodology for standardising data across spatial and temporal scales is directly reusable.

#### HDX (Humanitarian Data Exchange)
- **What:** UN OCHA's open data platform — 18,000+ datasets from 254 locations and 2,147 sources
- **APIs:** CKAN API (general) and HDX HAPI (curated humanitarian indicators)
- **Code:** Open source (CKAN-based) — [github.com/OCHA-DAP](https://github.com/OCHA-DAP)
- **Key insight:** HDX HAPI provides standardised humanitarian indicators designed for interoperability. This is a primary data source for food security, displacement, and funding data.

#### Kepler.gl
- **What:** Open-source geospatial analysis tool for large-scale data visualisation
- **Built on:** MapLibre GL + deck.gl (WebGL), renders millions of points
- **Features:** Time playback, spatial aggregation (hexbin, grid), 3D, arc layers, filtering
- **v3.1:** Now includes DuckDB for in-browser spatial analytics
- **Licence:** MIT
- **Key insight:** This is the visualisation layer for Causal Atlas. It can be embedded as a React component and accepts CSV/GeoJSON — our pipeline just needs to output in those formats.

### Key Lessons from Prior Work

1. **Researcher-led conflict data (ACLED) is far more reliable than auto-coded data (GDELT)** for ground-truth analysis. Use both, but weight them differently.
2. **The 0.5° grid-month resolution** has become a de facto standard in climate-conflict research (PRIO-GRID, AfroGrid). Adopting this provides compatibility with existing research.
3. **Nightlight emissions and NDVI vegetation index** are consistently the most powerful proxy variables for economic activity and agricultural conditions respectively.
4. **Time-lagged analysis is where the value lies.** Simultaneous correlations are often spurious; lagged correlations (especially 1–6 months) reveal actual causal pathways.
5. **Media sentiment (GDELT tone) can be a leading indicator** for conflict events, per published research using PRIO-GRID at daily and monthly intervals.

---

## Dataset Catalogue

### Tier 1 — Seed Datasets

These form the initial cross-domain combination for the seed experiment. All are free, well-documented, geocoded, and have proven interactions.

| Dataset | Domain | Coverage | Resolution | Format | Access |
|---|---|---|---|---|---|
| **ACLED** | Conflict & protest | Global, 1997–present | Event-level (lat/lon, date) | CSV, API | Free (registration required) — [acleddata.com](https://acleddata.com) |
| **EM-DAT** | Natural disasters | Global, 1900–present | Event-level (country/region) | CSV | Free (registration) — [emdat.be](https://www.emdat.be) |
| **WFP Food Prices** | Food commodity prices | 98 countries, ~3,000 markets, 1992–present | Market-level, mostly monthly | CSV, API via HDX | Free — [data.humdata.org/organization/wfp](https://data.humdata.org/organization/wfp) |
| **CHIRPS Rainfall** | Precipitation | Global (50°S–50°N), 1981–present | 0.05° daily / dekadal | GeoTIFF, NetCDF | Free — [chc.ucsb.edu/data/chirps](https://www.chc.ucsb.edu/data/chirps/) |
| **GDELT** | Global events & media sentiment | Global, 1979–present | Event-level, 15-min updates | CSV, BigQuery | Free — [gdeltproject.org](https://www.gdeltproject.org) |

### Tier 2 — Expansion Datasets

Add these once the pipeline is proven with Tier 1.

| Dataset | Domain | Coverage | Resolution | Access |
|---|---|---|---|---|
| **USGS Earthquake API** | Seismic events | Global, real-time + historical | Event-level (lat/lon, time, magnitude) | Free REST API — [earthquake.usgs.gov](https://earthquake.usgs.gov/fdsnws/event/1/) |
| **OpenAQ** | Air quality / pollution | Global, 100+ countries | Station-level, hourly | Free API — [openaq.org](https://openaq.org) |
| **UCDP-GED** | Armed conflict (researcher-coded) | Global, 1989–present | Event-level | Free — [ucdp.uu.se](https://ucdp.uu.se/downloads/) |
| **FEWS NET** | Famine early warning | Vulnerable regions, ongoing | Subnational, monthly | Free — [fews.net](https://fews.net) |
| **IDMC / GIDD** | Internal displacement | Global | Country-level, annual | Free — [internal-displacement.org](https://www.internal-displacement.org/database/) |
| **World Bank Commodity Prices** | Global commodity markets | Global, 1960–present | Monthly | Free — [worldbank.org/en/research/commodity-markets](https://www.worldbank.org/en/research/commodity-markets) |
| **MODIS NDVI** | Vegetation health | Global | 250m–1km, 16-day composites | Free — [earthdata.nasa.gov](https://earthdata.nasa.gov) |
| **WHO GHO** | Disease & health indicators | Global | Country-level, annual | Free — [who.int/data/gho](https://www.who.int/data/gho) |
| **GDACS** | Disaster alerts (real-time) | Global | Event-level | Free API — [gdacs.org](https://www.gdacs.org) |
| **IPC / Cadre Harmonisé** | Food insecurity classification | 30+ countries | Subnational, periodic | Free API — [ipcinfo.org](https://www.ipcinfo.org) |
| **Copernicus Climate Data Store** | Climate extremes (ETCCDI) | Global | Grid-based, various | Free — [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu) |
| **FAO Pesticide Use** | Agricultural chemical use | Global | Country-level, annual | Free — [fao.org/faostat](https://www.fao.org/faostat/en/) |

### Tier 3 — Aspirational Datasets

These require more work to integrate but would add significant value.

| Dataset | Domain | Notes |
|---|---|---|
| **Nighttime Lights (VIIRS)** | Economic activity proxy | NASA/NOAA, global, nightly composites |
| **UN Comtrade** | International trade flows | Country-to-country, commodity-level |
| **AIS Shipping Data** | Maritime trade routes | Global vessel tracking (some commercial) |
| **DHS Surveys** | Health, education, demographics | Household-level, 90+ countries |
| **UK Police API** | Crime (England & Wales) | Street-level, monthly — model for other national APIs |
| **FBI UCR / NIBRS** | Crime (US) | Agency-level, annual |
| **UNESCO UIS** | Education indicators | Country-level, annual |
| **ProMED** | Disease outbreak alerts | Global, event-based |
| **Social Conflict Analysis Database (SCAD)** | Social conflict (Africa, Latin America, Caribbean) | Event-level, 1990–2017 |

### Meta-Platforms and Aggregators

| Platform | What it provides | URL |
|---|---|---|
| **HDX** | 18,000+ humanitarian datasets, standardised API | [data.humdata.org](https://data.humdata.org) |
| **HDX HAPI** | Curated humanitarian indicators API | [docs](https://hdx-hapi.readthedocs.io/) |
| **ClimateSERV** | NASA Earth observation data for food/water security | [climateserv.servirglobal.net](https://climateserv.servirglobal.net) |
| **xSub** | Cross-national subnational violence portal | [x-sub.org](https://x-sub.org) |
| **World Bank Open Data** | Development indicators | [data.worldbank.org](https://data.worldbank.org) |
| **Dateno** | Meta-search across 22M+ datasets globally | [dateno.io](https://dateno.io) |
| **Google BigQuery Public Datasets** | GDELT, NOAA weather, and others at scale | [cloud.google.com/bigquery/public-data](https://cloud.google.com/bigquery/public-data) |

---

## Architecture

### Design Principles

1. **Open everything.** All code, data pipelines, and methodology must be open source and reproducible.
2. **Grid-first.** All data is projected onto a common spatiotemporal grid before analysis. No grid, no analysis.
3. **Domain-agnostic ingestion.** Adding a new data source should require only a configuration file and a lightweight adapter, not architectural changes.
4. **Temporal awareness is core.** Every record has a time dimension. The system reasons about lags, leads, and temporal windows natively.
5. **Separation of concerns.** Ingestion, alignment, analysis, and visualisation are independent modules that communicate through well-defined data formats.
6. **Claude-assisted development.** The project is built with and for AI-assisted coding workflows (Claude Code, etc.).

### System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CAUSAL ATLAS                                 │
├─────────────┬──────────────┬──────────────────┬─────────────────────┤
│  INGESTION  │  ALIGNMENT   │    ANALYSIS      │   VISUALISATION     │
│             │              │                  │                     │
│ Source      │ Spatial grid │ Cross-correlation│ Kepler.gl           │
│ adapters    │ (PRIO-GRID   │ Granger causality│ (temporal playback) │
│ (ACLED,     │  compatible) │ Anomaly detection│                     │
│  GDELT,     │              │ Lag analysis     │ Interactive         │
│  EM-DAT,    │ Temporal     │                  │ dashboards          │
│  WFP,       │ alignment    │ LLM-assisted     │                     │
│  OpenAQ,    │ (monthly     │ interpretation   │ Statistical         │
│  USGS,      │  bins)       │ (Claude API)     │ reports             │
│  ...)       │              │                  │                     │
├─────────────┴──────────────┴──────────────────┴─────────────────────┤
│                     DATA STORE                                      │
│  DuckDB / Parquet files (local-first, cloud-optional)               │
└─────────────────────────────────────────────────────────────────────┘
```

### The Spatiotemporal Grid

Following PRIO-GRID conventions and AfroGrid methodology:

- **Spatial resolution:** 0.5° × 0.5° latitude/longitude cells (~55km at equator)
- **Temporal resolution:** Monthly (primary), with daily granularity available for event data
- **Projection:** WGS84 (EPSG:4326)
- **Cell ID scheme:** Compatible with PRIO-GRID cell identifiers for interoperability
- **Coverage:** Global terrestrial areas (initially; ocean cells optional for shipping/fisheries)

Each grid-cell-month becomes a row with columns from every ingested domain:

```
| cell_id | year | month | acled_events | acled_fatalities | emdat_disasters |
|         |      |       | wfp_price_idx | chirps_precip   | gdelt_tone_avg  |
|         |      |       | openaq_pm25   | usgs_quakes     | ...             |
```

### Statistical Engine

The analysis layer implements multiple approaches, from simple to sophisticated:

1. **Cross-correlation with lag.** For each pair of domain variables, compute Pearson correlation at lags from -12 to +12 months. Flag pairs where |r| > threshold at any lag.
2. **Granger causality testing.** For flagged pairs, run Granger causality tests (via `statsmodels`) to determine if one time series significantly predicts another after controlling for autocorrelation.
3. **Anomaly co-occurrence.** Detect anomalous spikes/drops in each variable (z-score > 2) and measure whether anomalies in one domain precede anomalies in another more than chance would predict.
4. **LLM-assisted interpretation.** Feed statistically significant findings to Claude API for plain-language interpretation, literature cross-referencing, and hypothesis generation.

### Visualisation Layer

Primary: **Kepler.gl** embedded in a web application.

- Drag timeline slider to scrub through months/years
- Toggle domain layers on/off
- Hexagonal aggregation for heat maps
- Arc layers for trade/migration flows
- Side-panel showing correlation statistics for selected region/timeframe

Secondary: **Jupyter notebooks** with Plotly/Matplotlib for detailed statistical exploration.

---

## Technology Stack

| Component | Technology | Why |
|---|---|---|
| **Language** | Python 3.11+ | Ecosystem (GeoPandas, statsmodels, gdeltPyR), community |
| **Data store** | DuckDB + Parquet | Fast analytical queries, zero-config, local-first |
| **Spatial** | GeoPandas, Shapely | Standard geospatial Python stack |
| **Statistical** | statsmodels, scipy, scikit-learn | Granger causality, cross-correlation, anomaly detection |
| **Visualisation** | Kepler.gl (web), Plotly (notebooks) | Best-in-class temporal geo-viz, open source |
| **Web framework** | FastAPI + React | Lightweight API server, Kepler.gl is React-native |
| **LLM integration** | Anthropic Claude API | Interpretation, hypothesis generation, data wrangling assistance |
| **CI/CD** | GitHub Actions | Standard, free for open source |
| **Notebooks** | Jupyter | Exploration, documentation, reproducibility |
| **Package management** | uv or poetry | Modern Python dependency management |

---

## Roadmap

### Phase 1 — Foundation (Weeks 1–3)

**Goal:** Ingest three seed datasets into a common grid and produce a basic temporal map.

- [ ] Repository setup (structure, CI, contributing guidelines, licence)
- [ ] Define the spatiotemporal grid schema (PRIO-GRID compatible)
- [ ] Build ingestion adapter: ACLED → grid (conflict events per cell-month)
- [ ] Build ingestion adapter: EM-DAT → grid (disaster events per cell-month)
- [ ] Build ingestion adapter: WFP food prices → grid (price index per cell-month)
- [ ] Grid alignment pipeline: merge all three into unified Parquet dataset
- [ ] Basic Kepler.gl visualisation: load unified data, enable time playback
- [ ] Jupyter notebook: demonstrate manual cross-correlation between layers

### Phase 2 — Discovery Engine (Weeks 4–6)

**Goal:** Automated correlation scanning and Granger causality testing.

- [ ] Implement pairwise cross-correlation scanner with configurable lag window
- [ ] Implement Granger causality test pipeline
- [ ] Build anomaly detection module (z-score based, per cell time series)
- [ ] Results storage: significant findings as structured JSON/Parquet
- [ ] Add GDELT sentiment layer as fourth data source
- [ ] Add CHIRPS rainfall as fifth data source
- [ ] Notebook: reproduce known drought → food price → conflict causal chain

### Phase 3 — Interactive Explorer (Weeks 7–10)

**Goal:** Web-based dashboard for visual exploration backed by statistical validation.

- [ ] FastAPI backend serving grid data and correlation results
- [ ] React frontend with embedded Kepler.gl
- [ ] Region selection → display correlation matrix and top lagged relationships
- [ ] "What happened before?" query: select an event cluster, find precursor signals
- [ ] Claude API integration for natural-language interpretation of findings
- [ ] Add Tier 2 datasets: USGS earthquakes, OpenAQ air quality, UCDP-GED

### Phase 4 — Community and Scale (Ongoing)

**Goal:** Make it easy for anyone to add data sources and share findings.

- [ ] Plugin system for data source adapters (YAML config + Python class)
- [ ] Community contribution workflow for new adapters
- [ ] Hosted demo instance (likely Streamlit Cloud or similar free tier)
- [ ] Published findings as reproducible notebooks
- [ ] Academic paper describing methodology and initial discoveries
- [ ] Integration with HDX HAPI for standardised humanitarian indicators

---

## Seed Experiment

To validate the tooling before expanding, we will reproduce a **well-documented causal chain**:

### Drought → Crop Failure → Food Price Spike → Civil Unrest

**Region:** Sahel / Horn of Africa (where this chain is best documented)
**Time period:** 2010–2023
**Expected lags:**
- Drought (CHIRPS rainfall deficit) → crop failure (NDVI decline): 1–3 months
- Crop failure → food price spike (WFP market data): 2–4 months
- Food price spike → conflict/protest events (ACLED): 1–6 months

**Success criteria:**
1. Granger causality tests confirm statistically significant (p < 0.05) lagged relationships between these variables in the expected direction
2. The temporal map clearly shows the cascade visually when scrubbing through time
3. The pipeline can reproduce these results from raw data in under 30 minutes on a standard laptop

---

## Known Challenges

### Spurious Correlations
With many domain pairs and lag windows, some significant results will occur by chance. Mitigation: Bonferroni correction, false discovery rate control, and requiring both statistical significance and known mechanistic plausibility (which the LLM can help assess).

### Data Quality Variation
GDELT is auto-coded and noisy; ACLED is researcher-verified and precise. EM-DAT has country-level resolution while ACLED has sub-district. Mitigation: quality metadata per source, weighted analysis, and clear documentation of each source's limitations.

### Temporal Alignment
Some data is daily, some monthly, some irregular. Mitigation: monthly aggregation as the common denominator, with sub-monthly data preserved for detailed analysis.

### Spatial Resolution Mismatch
WFP market data is point-based, CHIRPS is 0.05° raster, EM-DAT is often country-level. Mitigation: the 0.5° grid acts as a common denominator; point data is aggregated upward, raster data is aggregated from finer resolution, and country-level data is distributed or flagged.

### Causality vs. Correlation
Time-lagged correlations are suggestive but not proof of causation. Mitigation: transparent language ("Granger-causes" is a statistical term, not a philosophical one), LLM-assisted interpretation that cites relevant literature, and clear disclaimers.

### Licensing Constraints
Some datasets (EM-DAT, ACLED) require registration and have non-commercial or attribution requirements. Mitigation: document all licence terms per source, never redistribute raw data, and provide ingestion scripts that fetch from original sources.

---

## Contributing

Causal Atlas is designed for community contribution. The highest-impact ways to help:

1. **Add a data source adapter.** Pick any dataset from the catalogue, write an ingestion script following the adapter template, and submit a PR.
2. **Validate findings.** Run the analysis on a region you know well and report whether the discovered correlations match ground truth.
3. **Improve the statistical engine.** Better anomaly detection, spatial autocorrelation handling, or causal inference methods.
4. **Documentation and tutorials.** Jupyter notebooks that demonstrate specific analyses.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Licence

MIT — see [LICENCE](LICENCE) for details.

All data sources retain their original licences. Causal Atlas does not redistribute raw data; it provides ingestion scripts that fetch from original sources. Users are responsible for complying with each data source's terms of use.

---

## Acknowledgements

Causal Atlas builds on the shoulders of:

- **PRIO-GRID** (Tollefsen, Strand & Buhaug, 2012) — the spatial framework that made cross-domain conflict research possible
- **AfroGrid** (2022, Nature Scientific Data) — the template for multi-domain grid integration
- **ACLED** — the gold standard in geocoded conflict event data
- **GDELT** — the ambitious vision of a "computable earth"
- **WFP HungerMapLIVE** — demonstrating that multi-domain temporal map overlays can drive better decisions
- **Kepler.gl** (Uber / Foursquare) — open-source geospatial visualisation that makes the data speak
- **HDX** (UN OCHA) — making humanitarian data accessible to all
- **ClimateSERV** (NASA SERVIR) — lowering the barrier to Earth observation climate data

---

## Project Status

🟡 **Pre-alpha** — Research and design phase. Repository structure being established.

*This project was initiated in March 2026 as an open-source effort to democratise cross-domain spatiotemporal causal discovery.*
