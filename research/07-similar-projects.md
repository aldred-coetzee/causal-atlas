# 07 — Similar Projects and Prior Art

> **Last updated:** March 2025
> **Purpose:** Catalogue projects, platforms, and tools that overlap with the Causal Atlas vision — cross-domain spatiotemporal causal analysis — and distil lessons for our own design.

---

## Table of Contents

1. [Cross-Domain Event Correlation Platforms](#1-cross-domain-event-correlation-platforms)
2. [Multi-Layer Temporal Map Tools](#2-multi-layer-temporal-map-tools)
3. [Humanitarian Data Integration Frameworks](#3-humanitarian-data-integration-frameworks)
4. [Open-Source OSINT Geospatial Platforms](#4-open-source-osint-geospatial-platforms)
5. [Climate-Conflict Analysis Tools](#5-climate-conflict-analysis-tools)
6. ["Atlas of Causality" Type Projects](#6-atlas-of-causality-type-projects)
7. [Academic Research Platforms for Spatiotemporal Causal Analysis](#7-academic-research-platforms-for-spatiotemporal-causal-analysis)
8. [CrisisMappers, Ushahidi, and Crowdsourced Crisis Platforms](#8-crisismappers-ushahidi-and-crowdsourced-crisis-platforms)
9. [GDELT Analysis Tools and Dashboards](#9-gdelt-analysis-tools-and-dashboards)
10. [Conflict Forecasting Systems](#10-conflict-forecasting-systems)
11. [GitHub Repository Survey: Cross-Domain Spatiotemporal Analysis](#11-github-repository-survey-cross-domain-spatiotemporal-analysis)
12. [FEWS NET Data Pipeline](#12-fews-net-data-pipeline)
13. [UN Global Pulse](#13-un-global-pulse)
14. [Flowminder](#14-flowminder)
15. [GRID3](#15-grid3)
16. [Alan Turing Institute -- Humanitarian AI](#16-alan-turing-institute----humanitarian-ai)
17. [Data-Driven Humanitarian Response -- Platform Survey](#17-data-driven-humanitarian-response----platform-survey)
18. [The "Causal Search Engine" Concept](#18-the-causal-search-engine-concept)
19. [PyWhy Ecosystem -- Causal Inference in Python](#19-pywhy-ecosystem----causal-inference-in-python)
20. [World Bank DIME and ImpactAI](#20-world-bank-dime-and-impactai)
21. [Synthesis: Gaps and Opportunities for Causal Atlas](#21-synthesis-gaps-and-opportunities-for-causal-atlas)
22. [Deep GitHub Survey -- Round 2](#22-deep-github-survey----round-2)
23. [Academic Software for Spatiotemporal Causal Analysis](#23-academic-software-for-spatiotemporal-causal-analysis)
24. [Commercial Platforms Doing Similar Things](#24-commercial-platforms-doing-similar-things)

---

## 1. Cross-Domain Event Correlation Platforms

### 1.1 UNEP Strata — Climate Security Early Warning

| Attribute | Detail |
|---|---|
| **URL** | https://unepstrata.org/ |
| **Organisation** | UNEP, University of Edinburgh, Earth Blox |
| **Status** | Active (launched ~2023, ongoing development) |
| **Scope** | Global — identifies convergence of environmental, climate, and socio-economic stresses that could drive conflict, displacement, or fragility |
| **Tech** | Google Earth Engine, Earth Blox platform |
| **Access** | Open-access mapping tool |

**What they built:** A geospatial platform that overlays climate/environmental stressors (precipitation, fires, tree loss, land productivity) with socio-economic risk variables to identify "hotspots" where these converge. Uses a "convergence of evidence" method — different datasets are overlaid and where multiple stressors exceed thresholds simultaneously, those areas are flagged.

**What we can learn:**
- The "convergence of evidence" overlay approach is simple but effective for identifying multi-domain hotspots. It is descriptive rather than causal, however.
- Designed for 130+ UN country teams — proves demand for cross-domain spatiotemporal analysis at the policy level.
- Does not attempt causal inference or time-lagged analysis. This is precisely the gap Causal Atlas would fill.

**Limitations:**
- Correlation/overlay only — no statistical testing of causal links or time lags.
- Dependent on Google Earth Engine infrastructure.
- Not open-source as a standalone tool (Earth Blox is commercial).

---

### 1.2 WFP HungerMap LIVE

| Attribute | Detail |
|---|---|
| **URL** | https://hungermap.wfp.org/ |
| **Organisation** | World Food Programme |
| **Status** | Active, production-grade |
| **Scope** | 90+ countries — near real-time food security monitoring |
| **Tech** | Proprietary; ML models trained on 14 years of data across 63 countries |

**What they built:** An interactive map that monitors food security in real time. Integrates population density, nightlight intensity, rainfall, vegetation index, conflict data, market prices, and macroeconomic indicators. Uses ML models to produce "nowcasts" where direct data is unavailable. Users can overlay different data layers (e.g., conflict over hunger, disasters over food prices).

**What we can learn:**
- Multi-layer overlay with temporal controls is exactly what users want.
- The "nowcast" concept (using ML to fill data gaps) is highly relevant for Causal Atlas.
- Built on a 14-year training period — demonstrates the value of long time series.
- Users can overlay conflict with food security data — but the platform does not test for causal links or quantify lag structures.

**Limitations:**
- Proprietary platform, no public code.
- Descriptive/predictive, not causal.
- Focus exclusively on food security — not general-purpose cross-domain analysis.

---

### 1.3 Live Earth (LeoSight)

| Attribute | Detail |
|---|---|
| **URL** | https://www.liveearth.com/ |
| **Organisation** | Live Earth (commercial) |
| **Status** | Active, commercial product |
| **Tech** | Proprietary; supports 250M+ events/hour |

**What they built:** A commercial real-time geospatial event correlation engine. Ingests events from multiple data streams, correlates them in space and time, and applies ML for anomaly detection and prediction. Supports custom visualisations and real-time alerts.

**What we can learn:**
- Demonstrates that real-time cross-domain event correlation at scale is technically feasible.
- Their focus on "event correlation" in space and time is philosophically close to what we want.
- However, this is a commercial, closed-source product aimed at security/enterprise customers — not researchers or humanitarians.

**Limitations:**
- Not open source, not accessible to researchers.
- Focused on operational security rather than causal discovery.
- No published methodology for statistical causal inference.

---

### 1.4 FINSECURITY Geospatial Stream Correlation Engine

| Attribute | Detail |
|---|---|
| **URL** | https://finsecurity.eu/solutions/geospatial-stream-correlation-engine/ |
| **Status** | EU research project |

**What they built:** Receives events from multiple sources and correlates them in time and space, identifying complex events. Designed for financial security applications.

**What we can learn:**
- Architecture pattern of a "stream correlation engine" is relevant — Causal Atlas could adopt a similar pipeline for ingesting and correlating diverse event streams.
- However, focused on financial crime, not humanitarian/environmental domains.

---

## 2. Multi-Layer Temporal Map Tools

### 2.1 Kepler.gl

| Attribute | Detail |
|---|---|
| **URL** | https://kepler.gl/ |
| **Repo** | https://github.com/keplergl/kepler.gl |
| **Organisation** | Originally Uber, now Foursquare (open-source) |
| **Status** | Active, widely used |
| **Tech** | React, deck.gl, MapLibre GL, WebGL |
| **Licence** | MIT |
| **Stars** | ~10k |

**What they built:** A data-agnostic, high-performance web application for visual exploration of large-scale geospatial datasets. Supports multiple simultaneous layers, time playback with temporal filtering, 3D visualization (hexagons, arcs, heatmaps), and GPU-accelerated rendering.

**What we can learn:**
- **This is our primary candidate for the visualisation layer.** Kepler.gl already supports temporal playback, multi-layer display, and large datasets.
- We can embed kepler.gl as a React component and feed it data from our backend.
- Its temporal filter allows users to scrub through time and see how spatial patterns evolve — exactly what Causal Atlas needs.
- Does NOT do any statistical analysis — it is purely a visualisation tool.

**Limitations:**
- No built-in analytics, correlation testing, or causal inference.
- Performance can degrade with very large datasets (millions of points).
- Limited built-in support for comparing two time series or showing lag relationships.

**Reusability: HIGH** — Use directly as our map visualisation layer.

---

### 2.2 Foursquare Studio (formerly Unfolded Studio)

| Attribute | Detail |
|---|---|
| **URL** | https://foursquare.com/products/studio/ |
| **Status** | Active, freemium commercial product |
| **Tech** | Built on kepler.gl / deck.gl |

**What they built:** A hosted version of kepler.gl with additional features: cross-filtering, aggregation, time-based animation, SQL data connections, team collaboration. Strong support for temporal analysis and animations.

**What we can learn:**
- Shows what kepler.gl can look like with a polished product wrapper.
- Cross-filtering and time-based animation features are exactly what we need.
- The move from open-source kepler.gl to commercial Foursquare Studio shows the market demand.

**Limitations:**
- Freemium/commercial — not fully open.
- No causal analysis capabilities.

---

### 2.3 GeoNode

| Attribute | Detail |
|---|---|
| **URL** | https://geonode.org/ |
| **Repo** | https://github.com/GeoNode/geonode |
| **Status** | Active, mature (OSGEO core project) |
| **Tech** | Python/Django, GeoServer, PostgreSQL/PostGIS, OpenLayers |
| **Licence** | GPL |

**What they built:** A geospatial content management system for publishing, sharing, and managing geospatial data. Supports metadata management, social features (commenting, rating), and role-based access control.

**What we can learn:**
- Good model for the "data catalogue" aspect of Causal Atlas — how to let users discover, browse, and manage datasets.
- Mature data management and metadata infrastructure we could potentially leverage.
- Used by humanitarian organisations globally.

**Limitations:**
- Focused on data management, not analysis or correlation.
- Heavy technology stack (Java-based GeoServer).
- No temporal analysis or causal inference capabilities.

**Reusability: LOW-MEDIUM** — Could inform our data catalogue design, but the full GeoNode stack is heavyweight for our needs.

---

## 3. Humanitarian Data Integration Frameworks

### 3.1 HDX HAPI (Humanitarian API)

| Attribute | Detail |
|---|---|
| **URL** | https://data.humdata.org/hapi |
| **Repo** | https://github.com/OCHA-DAP/hdx-hapi |
| **Organisation** | OCHA Centre for Humanitarian Data |
| **Status** | Active development (v0.9.x as of Oct 2025) |
| **Tech** | Python, FastAPI, SQLAlchemy, PostgreSQL, Docker |
| **Licence** | MIT |
| **Stars** | 7 |

**What they built:** A REST API providing standardised access to curated humanitarian indicators from the HDX Data Grids. Updated daily from source data. Covers population, humanitarian needs, food security, conflict, and coordination data across crisis-affected countries.

**What we can learn:**
- **HAPI is a critical data source for Causal Atlas.** It standardises and aggregates data from multiple humanitarian organisations into a single API.
- The FastAPI + SQLAlchemy architecture is aligned with our planned tech stack.
- Their approach to data standardisation (common schemas across diverse sources) is directly relevant.
- The challenge of harmonising update frequencies (daily vs weekly vs yearly) mirrors our own.

**Limitations:**
- Coverage limited to humanitarian crises (not global environmental or economic data).
- Still in development; API surface may change.
- No analytical capabilities — pure data access.

**Reusability: HIGH** — Use as a data source; learn from their standardisation approach.

---

### 3.2 Humanitarian Data Exchange (HDX)

| Attribute | Detail |
|---|---|
| **URL** | https://data.humdata.org/ |
| **Organisation** | OCHA |
| **Status** | Active, production-grade |
| **Tech** | CKAN (open-source data portal platform) |

**What they built:** The largest open repository of humanitarian data, with 20,000+ datasets from 250+ organisations. Includes conflict data, food security, population, health, and more. Provides a data catalogue, API access, and integration with analysis tools.

**What we can learn:**
- The scale of data already aggregated here is enormous. Many of the datasets Causal Atlas wants to ingest are already catalogued on HDX.
- Their approach to metadata standards, dataset quality, and freshness indicators is instructive.
- HDX Quick Charts and data previews show how to make data immediately accessible.

**Limitations:**
- Data catalogue only — no analytical or correlation capabilities.
- Data quality varies widely across contributors.
- No spatial alignment or temporal normalisation.

**Reusability: HIGH** — Primary discovery mechanism for humanitarian datasets.

---

### 3.3 ACAPS Crisis Data Platform

| Attribute | Detail |
|---|---|
| **URL** | https://www.acaps.org/ |
| **API** | https://api.acaps.org/ |
| **Status** | Active |

**What they built:** Provides the INFORM Severity Index (31 indicators across impact, conditions, and complexity) plus crisis analysis reports. Integrates data from IPC food security classifications, ACLED conflict data, UNHCR displacement data, and other sources into composite severity scores.

**What we can learn:**
- Their methodology for weighting dimensions (impact 30%, conditions 70%, complexity 30%) is a useful reference for how to combine cross-domain indicators.
- The INFORM Severity Index demonstrates a practical approach to multi-domain data integration with clear methodology documentation.

**Limitations:**
- Composite index approach — collapses multi-dimensional data into a single score.
- No causal analysis or time-lagged correlation.
- Country-level granularity (not subnational grid cells).

---

### 3.4 FEWS NET (Famine Early Warning Systems Network)

| Attribute | Detail |
|---|---|
| **URL** | https://fews.net/ |
| **Organisation** | USAID, USGS, NASA |
| **Status** | Active since 1985 |

**What they built:** An integrated early warning system covering 38+ countries, combining satellite imagery, crop monitoring, market price analysis, and climate data. The FEWS NET Data Explorer hosts 22M+ data points across food security domains. Built on the NASA Land Information System (FLDAS) for hydrological modelling.

**What we can learn:**
- 40+ years of operational experience integrating climate and food security data.
- The FLDAS architecture (custom instance of NASA LIS) shows how to adapt large-scale geospatial infrastructure for specific humanitarian applications.
- Their data pipeline from satellite imagery to actionable food security assessments is a model for the kind of end-to-end workflow Causal Atlas needs.

**Limitations:**
- Focused exclusively on food security/famine.
- Proprietary data integration pipeline.
- Does not expose cross-domain causal analysis capabilities to users.

---

### 3.5 INFORM Risk Index

| Attribute | Detail |
|---|---|
| **URL** | https://drmkc.jrc.ec.europa.eu/inform-index |
| **Organisation** | European Commission JRC, IASC |
| **Status** | Active, updated twice yearly |

**What they built:** A global risk assessment covering 191 countries using 80 indicators across three dimensions: hazard & exposure, vulnerability, and lack of coping capacity. Includes natural hazards, conflict, socioeconomic factors, and infrastructure.

**What we can learn:**
- The three-dimensional risk model (hazard, vulnerability, coping capacity) is a well-established framework that Causal Atlas could adopt for structuring cross-domain analysis.
- Open data with transparent methodology — good model for reproducibility.
- Integration of 80 indicators shows the complexity of cross-domain data harmonisation.

**Limitations:**
- Country-level only (not subnational/grid-cell).
- Static risk index, not temporal/dynamic.
- No causal inference — purely descriptive composite scoring.

---

## 4. Open-Source OSINT Geospatial Platforms

### 4.1 Bellingcat Investigation Toolkit

| Attribute | Detail |
|---|---|
| **URL** | https://bellingcat.gitbook.io/toolkit |
| **Repo** | https://github.com/bellingcat |
| **Status** | Active |

**What they built:** A curated collection of OSINT investigation tools plus custom-built tools for geolocation, satellite imagery analysis (RS4OSINT), and social media investigation. Includes Jupyter notebooks for teaching investigation techniques with code.

**What we can learn:**
- Bellingcat's approach to making geospatial analysis accessible to non-technical investigators is instructive.
- Their RS4OSINT (Remote Sensing for OSINT) Google Earth Engine tutorials demonstrate practical satellite imagery analysis workflows.
- The "toolkit" approach — curating and documenting existing tools rather than building everything from scratch — aligns with our philosophy.

**Limitations:**
- Individual investigation tools, not an integrated platform.
- No systematic cross-domain data analysis or causal inference.
- Tools are for manual investigation, not automated analysis.

**Reusability: LOW** — Different use case, but useful as inspiration for documentation and accessibility.

---

### 4.2 OSINT Framework

| Attribute | Detail |
|---|---|
| **URL** | https://osintframework.com/ |
| **Status** | Active |

**What they built:** A comprehensive directory of OSINT tools organised by category (geolocation, social media, public records, etc.). Not a platform itself, but a meta-resource.

**What we can learn:**
- The taxonomy of OSINT data sources is useful for identifying data we might want to ingest.
- Shows the breadth of open-source data available.

---

## 5. Climate-Conflict Analysis Tools

### 5.1 RGCPD (Response-Guided Causal Precursor Detection)

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/semvijverberg/RGCPD |
| **Organisation** | VU Amsterdam |
| **Status** | Active (releases ongoing) |
| **Tech** | Python, uses Tigramite internally |
| **Licence** | Not specified |

**What they built:** A framework to process 3D climate data (gridded NetCDF), identify spatially correlated precursor regions through correlation mapping, and then test these correlations for causality using PCMCI (via Tigramite). Generates "Causal Effect Networks" (CENs) showing the direction, lag, and magnitude of causal links between variables.

**What we can learn:**
- **The two-step pipeline — (1) spatial correlation mapping to identify candidate regions, then (2) causal testing — is highly relevant to Causal Atlas.**
- Their approach of aggregating gridded data into meaningful precursor regions before testing for causality addresses the dimensionality problem we will face.
- Direct integration with Tigramite shows a practical causal inference workflow.
- CEN visualisations effectively communicate complex causal relationships.

**Limitations:**
- Focused on climate teleconnections, not general cross-domain analysis.
- Requires expert knowledge to configure and interpret.
- Not a user-facing platform — research toolbox only.

**Reusability: MEDIUM** — Could adopt their spatial aggregation + causal testing pipeline architecture.

---

### 5.2 Causal4Migrations

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/IPL-UV/Causal4Migrations |
| **Organisation** | Image Processing Lab, University of Valencia |
| **Status** | Research project (last commit ~2022) |
| **Tech** | Python, Jupyter notebooks, Tigramite |
| **Licence** | GPL-3.0 |
| **Stars** | 1 |

**What they built:** Applied PCMCI causal discovery to identify drought-induced displacement drivers in Somalia (2016–2023). Integrated weather data (SPEI drought indices), food/livestock/water prices, conflict fatalities, and IDMC displacement data. Produced district-level causal graphs showing how drought cascades through food security, water availability, conflict, and ultimately displacement.

**What we can learn:**
- **This is the closest existing work to what Causal Atlas aims to do**, albeit at a much smaller scale (three districts in Somalia).
- Demonstrates that PCMCI can successfully identify cross-domain causal chains (drought → food prices → displacement) with time lags.
- Shows the practical challenges of data integration across very different domains.
- The district-level analysis reveals that causal structures vary geographically — a key finding for Causal Atlas.

**Limitations:**
- Extremely small scale (3 districts, 1 country).
- Manual data integration — no automated pipeline.
- Not a platform — a one-off research analysis.
- Only 1 GitHub star, minimal community uptake.

**Reusability: MEDIUM** — The methodology is directly relevant; the code less so (small-scale notebooks).

---

### 5.3 Spatio-Temporal Causality: Conflict and Forest Loss in Colombia

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/runesen/spatio_temporal_causality |
| **Status** | Research project (last commit June 2020) |
| **Tech** | R (67.5%), Python (32.5%), ArcGIS |
| **Licence** | Creative Commons |
| **Stars** | 25 |

**What they built:** Implements causal inference methods for studying the relationship between armed conflict and deforestation in Colombia (2000–2015). Uses spatial block-permutation and temporal block-resampling to test for causal effects while accounting for spatial autocorrelation. Data aggregated into 10km × 10km grid cells.

**What we can learn:**
- Addresses the spatial autocorrelation problem directly — essential for any grid-cell-based causal analysis.
- The block-permutation approach is a practical solution for hypothesis testing with spatially dependent data.
- Demonstrates that causal analysis at grid-cell level (similar to PRIO-GRID) is feasible.
- Integration of Global Forest Change, UCDP GED, road networks, and population data shows practical multi-source data fusion.

**Limitations:**
- Single country, two variables (conflict → forest loss).
- Computationally expensive (used 243 cores for simulations).
- R + ArcGIS workflow is not easily reproducible.
- Academic prototype, not a reusable tool.

**Reusability: LOW** — Methodology is instructive; code is not reusable for our purposes.

---

### 5.4 AfroGrid

| Attribute | Detail |
|---|---|
| **Publication** | Introducing AfroGrid, Scientific Data (2022) |
| **URL** | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LDI5TK |
| **Status** | Published dataset (v1.0), not an active platform |

**What they built:** An integrated, disaggregated 0.5° grid-month dataset covering Africa (1989–2020), combining conflict events (UCDP GED, ACLED), environmental stress (NDVI, rainfall, temperature), and socioeconomic factors (nightlights, population) into a single file. Includes PRIO-GRID and COW country identifiers for integration with other datasets.

**What we can learn:**
- **AfroGrid is the closest existing dataset to what Causal Atlas's data layer would produce** — multi-domain data aligned on a common spatiotemporal grid.
- Their approach to harmonising NDVI time series and dual-series nightlights data addresses real technical challenges we will face.
- The 0.5° resolution matches our planned PRIO-GRID backbone.
- Providing data as a single downloadable file maximises accessibility.

**Limitations:**
- Africa only.
- Static dataset (not a live, updating platform).
- No analytical tools — just the integrated data.
- Limited temporal resolution (monthly).
- No causal analysis capabilities.

**Reusability: HIGH** — Could use AfroGrid as a starting dataset for Africa; adopt their integration methodology.

---

### 5.5 Sahel Predictive Analytics Project

| Attribute | Detail |
|---|---|
| **Publication** | "Moving from Reaction to Action: Anticipating Vulnerability Hotspots in the Sahel" (Nov 2022) |
| **URL** | https://viewsforecasting.org/about/sahel-pa/ |
| **Organisation** | Consortium of 19 institutions, supported by UNHCR, UNDP, UN HLCP |

**What they built:** A multi-institution predictive analytics project combining ML-based conflict forecasting (VIEWS), climate modelling (PIK Potsdam), food security analysis, and strategic foresight. Identified "hotspots of interconnected risks" across 10 Sahel countries by overlaying predictions from multiple models and methodologies.

**What we can learn:**
- Demonstrates the value of combining predictions from multiple domains (climate, conflict, food, displacement) to identify compound risks.
- The consortium approach — bringing together domain experts from different institutions — is a model for how cross-domain analysis should work.
- Their finding that "vulnerability hotspots" are where multiple predicted risks overlap is exactly the kind of insight Causal Atlas should surface.
- First whole-of-UN system approach to multi-domain predictive analytics.

**Limitations:**
- One-off report, not a sustained platform.
- No open-source code or reusable pipeline.
- Focused on the Sahel region only.
- Combines predictions by overlay, not by testing for causal links between domains.

---

## 6. "Atlas of Causality" Type Projects

### 6.1 Causal Map

| Attribute | Detail |
|---|---|
| **URL** | https://www.causalmap.app/ |
| **Status** | Active (v4 launched) |
| **Licence** | Freemium (free for unlimited links, paid for private projects) |

**What they built:** A tool for qualitative causal mapping — extracting causal claims from text (interviews, reports, evaluations) and visualising them as directed graphs. Users code text segments as causal links (A → B) and the tool aggregates and displays the resulting causal network.

**What we can learn:**
- The "causal map" metaphor is powerful and intuitive.
- Their approach to visualising causal networks (directed graphs with edge weights) could inform how we present discovered causal relationships.
- However, this is qualitative (human-coded causal claims from text), not quantitative (statistically discovered causal relationships from data).

**Limitations:**
- Qualitative only — no data-driven causal discovery.
- No spatial or temporal dimension.
- Different domain entirely (programme evaluation, social science).

---

### 6.2 Csql Causal Database

| Attribute | Detail |
|---|---|
| **URL** | https://arxiv.org/html/2601.08109v1 |
| **Status** | Research preprint (Jan 2026) |

**What they built:** A system that extracts causal relationships from academic literature and maps them into a database. Contains 295,459 concept strings and 260,777 directed causal edges spanning 44 publication years. Produces two tables: `atlas_nodes` (concepts) and `atlas_edges` (causal generators).

**What we can learn:**
- The naming convention (`atlas_nodes`, `atlas_edges`) and the concept of a "causal atlas" derived from data are strikingly similar to our project name and vision.
- However, their "causality" is extracted from text (NLP), not discovered from observational data.
- The scale of their database (260k causal edges) shows the richness of published causal knowledge that could inform our hypothesis generation.

**Limitations:**
- Text-mined causality, not empirically validated.
- No spatial or temporal dimension.
- Academic literature focus.

---

### 6.3 Causaly

| Attribute | Detail |
|---|---|
| **URL** | https://www.causaly.com |
| **Status** | Active, commercial |

**What they built:** An AI platform with a large biomedical causal knowledge graph. Uses custom ontologies to map causal relationships across biology, pharmacology, and disease. Commercial product for life sciences R&D.

**What we can learn:**
- Their approach to building domain-specific causal ontologies is relevant — Causal Atlas will need ontologies for the domains it covers (climate, conflict, health, economics).
- However, this is entirely in the biomedical domain.

---

## 7. Academic Research Platforms for Spatiotemporal Causal Analysis

### 7.1 Tigramite

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/jakobrunge/tigramite |
| **Author** | Jakob Runge (DLR, German Aerospace Center) |
| **Status** | Active, well-maintained |
| **Tech** | Python (NumPy, SciPy, Numba, optional PyTorch) |
| **Licence** | GPL-3.0 |
| **Stars** | ~1,600 |
| **Latest** | v5.2 (March 2023) |

**What they built:** The leading open-source Python library for causal discovery in time series data. Implements PCMCI (and variants: PCMCIplus, LPCMCI, RPCMCI, J-PCMCI+) for discovering time-lagged and contemporaneous causal links. Supports linear and non-linear conditional independence tests, handles missing values, and integrates with scikit-learn for prediction.

**What we can learn:**
- **Tigramite is the most likely causal inference engine for Causal Atlas.** It is the de facto standard for time series causal discovery in climate science.
- PCMCI is specifically designed for discovering lagged causal relationships — exactly what we need for cross-domain analysis.
- Multiple projects in our review (Causal4Migrations, RGCPD, CauseME) already use Tigramite, confirming its suitability.
- Supports both linear (ParCorr) and non-linear (CMIknn, GPDC) tests — important since cross-domain relationships may be non-linear.

**Limitations:**
- Designed for moderate-dimensional time series (~10-100 variables), not massive grid-cell datasets.
- No built-in spatial awareness — treats each grid cell independently unless variables are pre-aggregated.
- Computationally expensive for large numbers of variables or long time series.
- No web interface — Python API only.

**Reusability: HIGH** — Core causal inference engine for Causal Atlas.

---

### 7.2 Salesforce CausalAI

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/salesforce/causalai |
| **Status** | **Archived** (read-only as of May 2025) |
| **Tech** | Python, NumPy, scikit-learn, Ray |
| **Licence** | BSD-3-Clause |
| **Stars** | ~316 |

**What they built:** An open-source library for causal discovery and inference on tabular and time series data. Supports PC, GES, LINGAM, GIN algorithms. Includes a no-code web UI, distributed computing via Ray, and benchmarking modules. Handles discrete, continuous, and mixed data types.

**What we can learn:**
- The no-code web UI is a useful reference for making causal analysis accessible to non-programmers.
- Their benchmarking modules for comparing algorithms across datasets are relevant.
- The distributed computing support (Ray) addresses the scalability challenge.

**Limitations:**
- **Archived/read-only** — no longer maintained by Salesforce. This is a significant risk for any project building on it.
- Less focused on time series than Tigramite.
- No spatial awareness.

**Reusability: LOW** — Archived; Tigramite is the better choice for our use case.

---

### 7.3 geocausal (R Package)

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/mmukaigawara/geocausal |
| **CRAN** | https://cran.r-project.org/web/packages/geocausal/ |
| **Authors** | Mukaigawara, Imai, Lyall (Harvard, Yale, Dartmouth) |
| **Status** | Active (CRAN release, 746 commits) |
| **Tech** | R |
| **Stars** | 63 |

**What they built:** An R package for spatiotemporal causal inference based on point-process data. Users provide raw treatment/outcome event locations and timings, specify counterfactual scenarios, and the package estimates causal effects. Handles arbitrary spillover and carryover effects. Originally developed for analysing the causal effect of airstrikes on insurgent violence in Iraq.

**What we can learn:**
- Directly addresses spatiotemporal causal inference — rare among existing tools.
- The explicit modelling of spillover (spatial) and carryover (temporal) effects is highly relevant.
- Point-process approach works well for event data (ACLED, UCDP), though not for continuous indicators.
- Backed by rigorous academic methodology (published in top journals).

**Limitations:**
- R-only — does not integrate easily into a Python/web stack.
- Designed for point-process (event) data, not gridded indicator time series.
- Requires strong statistical expertise to use and interpret.
- Not a platform — a statistical package.

**Reusability: LOW for code, HIGH for methodology** — The spillover/carryover framework should inform our analytical approach.

---

### 7.4 CauseME Platform

| Attribute | Detail |
|---|---|
| **URL** | https://causeme.uv.es/ |
| **Organisation** | University of Valencia, DLR |
| **Status** | Active |

**What they built:** An online benchmarking platform for causal discovery methods. Provides ground-truth datasets (synthetic models mimicking real-world challenges: time delays, autocorrelation, nonlinearity, chaotic dynamics, measurement error). Method developers upload their predictions and the platform evaluates and ranks them.

**What we can learn:**
- CauseME provides a rigorous framework for evaluating which causal discovery methods work best under different conditions.
- We should use CauseME benchmarks to select the best methods for our specific data characteristics.
- The challenge taxonomy (time delays, nonlinearity, missing data, etc.) maps directly to challenges we will face.

**Limitations:**
- Benchmarking platform only — does not do analysis on real-world data.
- Focused on method comparison, not application.

**Reusability: MEDIUM** — Use for method selection and validation, not as infrastructure.

---

### 7.5 CLIMADA (CLIMate ADAptation)

| Attribute | Detail |
|---|---|
| **URL** | https://climada.ethz.ch/ |
| **Repo** | https://github.com/CLIMADA-project/climada_python |
| **Organisation** | ETH Zurich, Weather and Climate Risks Group |
| **Status** | Active, well-maintained |
| **Tech** | Python 3, Conda |
| **Licence** | GPL-3.0 |

**What they built:** A comprehensive framework for probabilistic climate risk assessment. Combines hazard, exposure, and vulnerability data to calculate socioeconomic, human, and ecological impacts. Supports probabilistic impact calculations, climate change scenario analysis, and adaptation measure evaluation. Integrates data from OpenStreetMap, Copernicus Climate Data Store, and many other sources.

**What we can learn:**
- CLIMADA's hazard-exposure-vulnerability framework is a well-tested model for structuring multi-layer analysis.
- Their data integration approach (pulling from many sources into a common framework) is directly relevant.
- The split into core (`climada_python`) and extensions (`climada_petals`) is a good architectural pattern.
- Extensive documentation and community (ETH research group) demonstrates sustainability.

**Limitations:**
- Focused on natural hazards and climate risk, not cross-domain causal analysis.
- Does not include conflict, economic, or health data.
- Risk assessment framework, not causal discovery.

**Reusability: MEDIUM** — Architectural patterns and data integration approaches are relevant; the domain focus is different.

---

### 7.6 DeepCausality

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/deepcausality-rs/deep_causality |
| **Organisation** | Linux Foundation for AI & Data (sandbox project) |
| **Status** | Active |
| **Tech** | Rust |
| **Licence** | Apache-2.0 / MIT dual |

**What they built:** A Rust framework for building systems that reason about cause and effect in complex, dynamic environments. Uses "Causaloids" (composable causal units) operating on an explicit hypergraph "Context" with a safety layer ("Effect Ethos"). Designed for high-performance, real-time causal reasoning.

**What we can learn:**
- Interesting theoretical framework for representing complex causal structures.
- The hypergraph-based context model could represent spatiotemporal relationships.
- Performance-focused Rust implementation relevant if we need real-time processing.

**Limitations:**
- Very early stage, conceptually ambitious but limited practical applications demonstrated.
- Rust ecosystem — does not integrate with our Python-based stack.
- More of a reasoning framework than a discovery tool.

**Reusability: LOW** — Interesting conceptually but not practical for our use case.

---

## 8. CrisisMappers, Ushahidi, and Crowdsourced Crisis Platforms

### 8.1 Ushahidi

| Attribute | Detail |
|---|---|
| **URL** | https://www.ushahidi.com/ |
| **Repo** | https://github.com/ushahidi |
| **Status** | Active |
| **Tech** | PHP/Kohana (v2), Python/PHP/JavaScript/Ionic (v3+), AWS |
| **Licence** | AGPL-3.0 |

**What they built:** The pioneering crisis mapping platform (born during 2008 Kenya post-election violence). Collects reports via SMS, email, Twitter, and web forms. Categorises, maps, and visualises crowdsourced data. Supports AI-assisted triage of incoming reports. Used in hundreds of deployments worldwide.

**What we can learn:**
- Ushahidi proved that crowdsourced geospatial data can be rapidly collected and mapped during crises.
- Their data collection pipeline (multi-channel ingestion → categorisation → mapping) is a useful architectural reference.
- The challenge of data quality in crowdsourced reports is well-documented.

**What they DON'T do that we need:**
- No cross-domain data integration (only user-submitted reports).
- No temporal analysis or time series capabilities.
- No causal inference or statistical analysis.
- No integration with institutional datasets (satellite, economic, health).

**Reusability: LOW** — Different paradigm (crowdsourcing vs. institutional data analysis).

---

### 8.2 CrisisMappers Network

| Attribute | Detail |
|---|---|
| **URL** | https://crisismapping.ning.com/ |
| **Status** | Active (9,600+ members, 160+ countries) |
| **Founded** | 2009 |

**What they built:** Not a platform but a network of 9,600+ practitioners, technologists, researchers, and volunteers at the intersection of humanitarian crises and technology. Members from 3,000+ institutions including 400+ universities and 50+ UN agencies.

**What we can learn:**
- The scale of the community interested in crisis mapping and humanitarian technology.
- The network demonstrates demand for better tools connecting geospatial data, crisis response, and analytical capabilities.
- Potential user base and community for Causal Atlas.

---

### 8.3 Humanitarian OpenStreetMap Team (HOT) & Tasking Manager

| Attribute | Detail |
|---|---|
| **URL** | https://www.hotosm.org/ |
| **Repo** | https://github.com/hotosm |
| **Status** | Active, mature |
| **Tech** | Python, JavaScript, various |

**What they built:** Coordinates volunteer mapping of crisis-affected areas using satellite imagery. The Tasking Manager divides areas into grid cells for distributed mapping. Volunteers digitise buildings, roads, and waterways from satellite imagery. Data available within 24 hours of a crisis activation.

**What we can learn:**
- HOT generates the base geospatial infrastructure (building footprints, road networks) that other analyses depend on.
- Their grid-based task division model is conceptually similar to our PRIO-GRID approach.
- The Missing Maps initiative (HOT + MSF + Red Cross) shows how humanitarian organisations collaborate on geospatial data.

**What they DON'T do:**
- No analytical capabilities — pure data creation.
- No temporal analysis or cross-domain integration.

---

### 8.4 MapAction

| Attribute | Detail |
|---|---|
| **URL** | https://mapaction.org/ |
| **Status** | Active |

**What they built:** Automated data pipeline that integrates data from HDX, Google Earth Engine, and OpenStreetMap for rapid crisis mapping. Produces standardised situation maps within hours of a disaster. Recently developing event-driven pipeline triggered by GDACS disaster alerts.

**What we can learn:**
- Their automated data pipeline (HDX + GEE + OSM → standardised maps) is a practical model for rapid multi-source data integration.
- Event-driven architecture (triggered by GDACS alerts) is an interesting pattern for Causal Atlas's data ingestion.

---

## 9. GDELT Analysis Tools and Dashboards

### 9.1 GDELT Official Analysis Service

| Attribute | Detail |
|---|---|
| **URL** | https://www.gdeltproject.org/data.html |
| **Status** | Active |
| **Tech** | Google BigQuery (free access with 1TB/month processing) |

**What they built:** Fourteen cloud-based analysis tools for geographic, temporal, network, and contextual visualisation of the Event Database and Global Knowledge Graph. Updated every 15 minutes. The underlying dataset covers global news from 1979 to present, coding events by type, actors, location, and "tone" (sentiment).

**What we can learn:**
- GDELT demonstrates that a massive global event database updated in near-real-time is feasible.
- Their BigQuery integration model — free cloud-based querying of massive datasets — is an excellent pattern for data access.
- The 14 built-in analysis tools show what kinds of analysis users want (geographic heatmaps, temporal trends, network analysis, tone/sentiment).
- GDELT's spatial resolution (geocoded to coordinates) is much finer than PRIO-GRID cells.

**Limitations:**
- News-derived data — biased toward events that get media coverage.
- Known issues with geocoding accuracy and event duplication.
- No causal inference capabilities — descriptive statistics and visualisation only.
- Tone/sentiment analysis is crude compared to modern NLP.

---

### 9.2 gdeltPyR

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/linwoodc3/gdeltPyR |
| **Status** | Active |
| **Tech** | Python, Pandas |

**What they built:** A Python framework for retrieving GDELT v1 and v2 data into Pandas DataFrames. Simplifies data access for analysis in Python or R.

**Reusability: MEDIUM** — Useful as a data access library for GDELT integration.

---

### 9.3 GDELT Dashboard (James Lane Conkling)

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/jameslaneconkling/gdelt-dashboard |
| **Status** | Inactive (academic project) |
| **Tech** | Leaflet.js, GeoJSON |

**What they built:** A simple map density grid showing changes in conflict events from the GDELT dataset, with time-based filtering.

**What we can learn:**
- Even a simple temporal map of conflict events is useful. The barrier to building a basic version is low.
- Leaflet-based approach works but kepler.gl/deck.gl would be much more performant.

---

### 9.4 ACLED Community Visualisation Tools

Several community-built tools exist for ACLED data:

| Project | Tech | Features |
|---|---|---|
| [acled_conflict_analysis](https://github.com/datapartnership/acled_conflict_analysis) | Python | Extract, process, analyse, map ACLED data |
| [acled-deckgl](https://github.com/dgmurphy/acled-deckgl) | deck.gl | 3D hexagon heatmap with time slider |
| [Conflict-Crisis-Mapping-Project](https://github.com/RealCaddish/Conflict-Crisis-Mapping-Project) | Leaflet, D3, Turf.js | Situation maps combining ACLED + Ushahidi |
| [acledR](https://dtacled.github.io/acledR/) | R | Official ACLED R package |

**What we can learn:**
- Multiple independent teams have built ACLED visualisation tools, confirming demand.
- The acled-deckgl project using deck.gl with a time slider is closest to our visualisation needs.
- No existing tool combines ACLED with climate or economic data for cross-domain analysis.

---

## 10. Conflict Forecasting Systems

### 10.1 VIEWS (Violence & Impacts Early-Warning System)

| Attribute | Detail |
|---|---|
| **URL** | https://viewsforecasting.org/ |
| **Repo** | https://github.com/views-platform |
| **Legacy Repo** | https://github.com/prio-data/views_pipeline |
| **Organisation** | Uppsala University + PRIO (co-hosted) |
| **Status** | Active, next-generation platform launching ~2024/2025 |
| **Tech** | Python, Jupyter Notebooks (90.6%), PyTorch, Prefect (orchestration), Weights & Biases (experiment tracking) |
| **Licence** | CC BY-NC-SA 4.0 |

**What they built:** The leading open-source conflict forecasting system. Generates monthly predictions of armed conflict fatalities 1–36 months ahead across Africa and the Middle East. The fatalities003 model uses ~200 variables from UCDP, ACLED, PRIO-GRID, World Bank, V-Dem, and FAO. Supports multiple modelling approaches including deep learning, Hidden Markov models, and time series techniques.

**What we can learn:**
- **VIEWS is the single most important prior art project for Causal Atlas.** It operates on the same spatial grid (PRIO-GRID), uses many of the same data sources, and addresses a closely related problem.
- Their modular pipeline architecture (individual models → ensembles → deployment) is a strong reference.
- The step-shift forecasting approach (36-month windows with calibration/test/forecast partitions) is well-designed.
- Their data access layer (VIEWSER) shows how to abstract data retrieval from model code.
- The VIEWS Prediction Challenge (2023/2024) attracted 13 research institutions — demonstrating community engagement.

**Key difference from Causal Atlas:** VIEWS predicts conflict. Causal Atlas discovers cross-domain causal relationships. VIEWS asks "where will conflict happen?" Causal Atlas asks "what causes what, and with what lag?"

**Limitations:**
- Focused exclusively on conflict forecasting (prediction), not causal discovery.
- Does not identify or quantify causal mechanisms — uses features as predictors without testing causality.
- Africa and Middle East only (expanding).
- CC BY-NC-SA licence limits commercial use.
- Pipeline "not yet ready for operational use" despite production deployment.

**Reusability: MEDIUM-HIGH** — Architecture patterns, data integration approach, and community model are all relevant. Data sources overlap substantially.

---

### 10.2 ACLED CAST (Conflict Alert System)

| Attribute | Detail |
|---|---|
| **URL** | https://acleddata.com/platform/conflict-index-dashboard |
| **Status** | Active, production |

**What they built:** Forecasts global political violence events up to 6 months ahead. Monthly updates with accuracy metrics. Part of ACLED's broader Early Warning Dashboard alongside Trendfinder, Conflict Exposure Calculator, and Conflict Index.

**What we can learn:**
- Shows that operational conflict forecasting is valued by the policy community.
- Integration of multiple risk tools (forecast, trend detection, exposure, severity) into a single dashboard is a good UX model.

**Limitations:**
- Proprietary/commercial — code not available.
- Conflict-only, no cross-domain analysis.
- Forecasting, not causal analysis.

---

### 10.3 WFP Conflict Forecast

| Attribute | Detail |
|---|---|
| **URL** | https://innovation.wfp.org/project/conflict-forecast |
| **Status** | Active |

**What they built:** Combines panel forecasting (ML) with NLP to predict armed conflict and disruptive events (protests, riots). Previously released datasets and code, but since 2022, no new reproducible code has been shared.

**What we can learn:**
- The combination of structured data (ML on panel data) with unstructured data (NLP on news) is relevant.
- The deterioration in code sharing (open → closed over time) is a cautionary tale for open-source sustainability.

---

### 10.4 Other Conflict Forecasting Systems

| System | Organisation | Key Feature |
|---|---|---|
| **SAGE** (Situational Awareness Geospatial Enterprise) | UN Peacekeeping | Central event tracking for peacekeeping missions |
| **Probabilistic Conflict Modelling** ([GitHub](https://github.com/fif911/probabilistic_conflict_modelling)) | Academic | ML model with 95% classification accuracy on war prediction |
| **EURIDICE Open-Source AI Framework** | EU project | Open-source AI for conflict forecasting (2025 paper) |

---

## 11. GitHub Repository Survey: Cross-Domain Spatiotemporal Analysis

> **Methodology:** Searched GitHub for repositories matching terms: "spatiotemporal causal", "climate conflict analysis", "humanitarian data pipeline", "geospatial event correlation", "multi-hazard risk", "food security forecasting", "conflict prediction model", "causal discovery spatial". Findings dated March 2025.

### 11.1 Spatiotemporal Causal Discovery

| Repository | Stars | Language | Last Active | Description |
|---|---|---|---|---|
| [jakobrunge/tigramite](https://github.com/jakobrunge/tigramite) | ~1,600 | Python | Active | PCMCI family of algorithms for time series causal discovery. De facto standard. |
| [py-why/causal-learn](https://github.com/py-why/causal-learn) | ~1,000+ | Python | Active | Python translation/extension of Tetrad. PC, GES, LINGAM, FCI, and more. Part of the PyWhy ecosystem. Published in JMLR 2024. |
| [Rose-STL-Lab/SPACY](https://github.com/Rose-STL-Lab/SPACY) | New | Python | 2024 | **Highly relevant.** Discovers latent causal graphs from spatiotemporal data. Uses variational inference with spatial kernel functions to map observational time series to latent representations. ICML 2025 paper. Outperforms baselines on synthetic data and identifies key phenomena from real-world climate data. |
| [yutong-xia/CausalST_Papers](https://github.com/yutong-xia/CausalST_Papers) | ~100 | -- | Active | Curated paper collection on causality in spatiotemporal data. Covers causal inference, discovery, and applications. |
| [paras2612/STREAMS](https://github.com/paras2612/STREAMS) | ~10 | Python | 2024 | Reinforcement learning for causal discovery in spatiotemporal data. LSTM-GCN autoencoder for streamflow prediction. |
| [zlxy9892/ST-CausalConvNet](https://github.com/zlxy9892/ST-CausalConvNet) | ~30 | Python | 2022 | Spatiotemporal causal convolutional network for PM2.5 prediction. |
| [semvijverberg/RGCPD](https://github.com/semvijverberg/RGCPD) | ~50 | Python | Active | Response-Guided Causal Precursor Detection. Two-step pipeline: spatial correlation mapping then PCMCI causal testing. Uses Tigramite internally. |
| [IPL-UV/Causal4Migrations](https://github.com/IPL-UV/Causal4Migrations) | 1 | Python | 2022 | PCMCI applied to drought-displacement causal chains in Somalia. Closest prior art to Causal Atlas at small scale. |
| [runesen/spatio_temporal_causality](https://github.com/runesen/spatio_temporal_causality) | 25 | R/Python | 2020 | Conflict-deforestation causality in Colombia. Block-permutation for spatial autocorrelation. |
| [mmukaigawara/geocausal](https://github.com/mmukaigawara/geocausal) | 63 | R | Active | Spatiotemporal causal inference for point-process data. Handles spillover and carryover effects. Harvard/Yale/Dartmouth. |

**Key finding: SPACY** (Rose-STL-Lab) is the most methodologically advanced new project. Its approach of discovering causal structures in a latent space -- reducing the high-dimensional grid-cell data to a lower-dimensional representation -- directly addresses the scalability challenge Causal Atlas will face. We should study this closely.

### 11.2 Climate-Conflict Analysis

| Repository | Stars | Language | Last Active | Description |
|---|---|---|---|---|
| [prio-data/climate_extremes](https://github.com/prio-data/climate_extremes) | ~5 | Python | Active | ETCCDI climate extremes data for conflict analysis. Quantifies 27 standardised climate extreme indices. Linked to VIEWS pipeline. |
| [prio-data/FEWSNet_to_PG](https://github.com/prio-data/FEWSNet_to_PG) | ~5 | Python | Active | Translates FEWS NET food insecurity data to PRIO-GRID resolution. Multiple translation procedures with interactive pipeline. |
| [prio-data/views_pipeline](https://github.com/prio-data/views_pipeline) | ~20 | Python | Migrated | Legacy VIEWS pipeline. Now migrated to views-platform organisation. |

### 11.3 Food Security Forecasting

| Repository | Stars | Language | Last Active | Description |
|---|---|---|---|---|
| [pietro-foini/ISI-WFP](https://github.com/pietro-foini/ISI-WFP) | ~20 | Python | 2023 | ML model for WFP food security forecasting. Gradient boosted regression trees. Predicts insufficient food consumption trends up to 30 days ahead in 6 countries. |
| [zhou100/FoodSecurityPrediction](https://github.com/zhou100/FoodSecurityPrediction) | ~30 | Python | 2022 | ML for food security prediction in sub-Saharan Africa. 55-84% accuracy. Published in AEPP. |
| [willianck/Predicting-Food-Insecurity](https://github.com/willianck/Predicting-Food-Insecurity) | ~10 | Python | 2022 | Food insecurity prediction with the Alan Turing Institute. Uses RHoMIS survey data. |
| [VectorInstitute/foodprice-forecasting](https://github.com/VectorInstitute/foodprice-forecasting) | ~15 | Python | Active | Mixed ensembles of ML models for Canada's Food Price Report. |

### 11.4 Conflict Prediction Models

| Repository | Stars | Language | Last Active | Description |
|---|---|---|---|---|
| [views-platform](https://github.com/views-platform) | Multiple repos | Python | Active | Full VIEWS 2.0 pipeline. Stepshift, HydraNet, ensemble framework. |
| [fif911/probabilistic_conflict_modelling](https://github.com/fif911/probabilistic_conflict_modelling) | ~20 | Python | 2023 | First publicly available explainable conflict forecasting model. 95% classification accuracy. Country-month level, 14 months ahead. |

### 11.5 Multi-Hazard Risk Assessment

| Repository | Stars | Language | Last Active | Description |
|---|---|---|---|---|
| [BritishGeologicalSurvey/TOMRAP](https://github.com/BritishGeologicalSurvey/TOMRAP) | ~10 | Python | Active | Tool for Multi-hazard Risk Assessment in Python. Combines flood, earthquake, volcanic hazard maps with building data. |
| [Intellia-SME/scikit-event-correlation](https://github.com/Intellia-SME/scikit-event-correlation) | ~15 | Python | 2022 | Event correlation and forecasting over high-dimensional streaming sensor data. |

### 11.6 Causal Discovery Libraries (General)

| Repository | Stars | Language | Last Active | Description |
|---|---|---|---|---|
| [py-why/causal-learn](https://github.com/py-why/causal-learn) | ~1,000+ | Python | Active | Part of PyWhy ecosystem. PC, GES, LINGAM, FCI, GIN, and more. Comprehensive Python causal discovery. |
| [py-why/dowhy](https://github.com/py-why/dowhy) | ~7,000+ | Python | Active | Causal inference library. Explicit causal modelling and assumption testing. |
| [FenTechSolutions/CausalDiscoveryToolbox](https://github.com/FenTechSolutions/CausalDiscoveryToolbox) | ~1,000+ | Python | 2023 | Causal inference in graphs and pairwise settings. Graph structure recovery. |
| [rguo12/awesome-causality-algorithms](https://github.com/rguo12/awesome-causality-algorithms) | ~2,000+ | -- | Active | Comprehensive index of causality algorithms with code. |

---

## 12. FEWS NET Data Pipeline

**What it is:** The Famine Early Warning Systems Network, funded by USAID, provides early warning and analysis on food insecurity in 38+ countries since 1985.

### Open-Source Components

FEWS NET's core analytical pipeline is **not open source**. However, some community-built tools exist:

**prio-data/FEWSNet_to_PG** (https://github.com/prio-data/FEWSNet_to_PG):
- Translates FEWS NET food insecurity classifications to PRIO-GRID 0.5-degree resolution.
- Multiple translation procedures available (different mapping approaches for different research needs).
- Interactive Python pipeline with utility scripts and reusable functions.
- Demonstrates how to bridge admin-boundary-based food security data with grid-cell-based conflict research.

**FEWS NET Data Explorer:**
- Hosts 22M+ data points across food security domains.
- Provides download access (not a REST API).
- Covers: IPC classifications, price data, production estimates, trade data, weather data.

**FLDAS (FEWS NET Land Data Assimilation System):**
- Custom instance of the NASA Land Information System.
- Produces hydrological estimates (soil moisture, evapotranspiration, runoff) for FEWS NET countries.
- Data available through NASA's GES DISC portal.
- Not open source as a system, but outputs are freely accessible.

### What We Can Learn

- 40 years of operational experience integrating climate, market, livelihood, and food security data.
- Their analytical framework (how climate anomalies propagate through food systems) is a model for the causal chains Causal Atlas aims to surface.
- The FEWSNet_to_PG repo demonstrates the practical challenges of mapping admin-boundary data to grid cells.

---

## 13. UN Global Pulse

**What it is:** The UN Secretary-General's flagship innovation initiative on big data, with a network of Pulse Labs in Jakarta, Kampala, and Helsinki.

**Links:**
- Website: https://www.unglobalpulse.org/
- GitHub: (various project-specific repos)

### Published Tools and Methods

| Tool | Purpose | Status |
|---|---|---|
| **Haze Gazer** | Crisis analysis and visualisation for forest/peatland fires in Indonesia | Deployed |
| **Qatalog** | Query, tag, and analyse data from public radio and Facebook posts | Open source platform for UN Country Teams |
| **DISHA** (Data Insights for Social and Humanitarian Action) | Multi-partner initiative for ethical data access and AI solutions | Active partnership |
| **Pulse Lab Cookbook** | Best practices for analysis, technology innovation, community engagement | Published guidelines |

### Approach

Global Pulse pursues a three-fold strategy:
1. **Research** innovative methods for analysing real-time digital data to detect early emerging vulnerabilities.
2. **Assemble** free and open-source technology toolkits for data sharing and hypothesis testing.
3. **Establish** an integrated global network of Pulse Labs.

### What We Can Learn

- UN Global Pulse has demonstrated that novel data sources (social media, mobile phone data, satellite imagery) can provide early warning signals.
- Their open-source tool approach aligns with Causal Atlas's philosophy.
- The DISHA initiative shows growing institutional support for ethical data-driven humanitarian analysis.
- However, their tools tend to be project-specific rather than general-purpose platforms.

---

## 14. Flowminder

**What it is:** A non-profit that uses mobile phone data, satellite imagery, and survey data to generate estimates of human mobility and population distribution in low- and middle-income countries.

**Links:**
- Website: https://www.flowminder.org/
- GitHub: https://github.com/flowminder
- FlowKit: https://www.flowminder.org/news/dial-launching-flowkit-an-open-source-tool-to-support-communities-through-mobile-phone-data-analysis

### FlowKit -- Open Source Tool

**Purpose:** Enables humanitarian workers to inform crisis responses using mobile phone Call Detail Record (CDR) data.

**Key Features:**
- Secure and compliant data access with privacy protections.
- Processing and analysis of CDR data to estimate population movements.
- Produces de-identified aggregates for displacement tracking.
- Released under an open-source licence.

**Applications:**
- 2010 Haiti Earthquake (population displacement tracking)
- 2013 Typhoon, Bangladesh
- 2015 Nepal Earthquake
- 2016 Haiti Hurricane
- Ebola response in West Africa
- COVID-19 mobility monitoring

### What We Can Learn

- **Mobile phone data as a displacement proxy** is highly relevant for Causal Atlas. If we discover that conflict causes displacement, FlowKit-derived mobility data could validate or quantify the displacement.
- **Privacy-preserving data processing** is essential for any tool handling sensitive movement data.
- FlowKit's architecture (secure processing within the mobile operator's infrastructure) addresses the key barrier to accessing mobile data.

### Limitations

- Requires partnership agreements with mobile network operators.
- CDR data availability varies significantly by country.
- Not real-time -- typically weekly or monthly aggregates.
- Python/Docker-based infrastructure.

---

## 15. GRID3

**What it is:** Geo-Referenced Infrastructure and Demographic Data for Development. Works with countries in sub-Saharan Africa to generate, validate, and use geospatial data on population, settlements, infrastructure, and boundaries.

**Links:**
- Website: https://grid3.org/
- Data Hub: https://data.grid3.org/
- HDX: https://data.humdata.org/organization/grid3 (71 datasets)

### Data Products

| Product | Description | Coverage |
|---|---|---|
| **Population estimates** | High-resolution gridded population (100m x 100m) | Multiple African countries |
| **Settlement extents** | Built-up area delineation from satellite imagery | Sub-Saharan Africa |
| **Administrative boundaries** | Validated, standardised boundary datasets | Country-specific |
| **Health facility locations** | Georeferenced health service points | Country-specific |
| **School locations** | Georeferenced educational facilities | Country-specific |

### Methodology

- Combines highest-resolution satellite imagery with dynamic population modelling.
- Uses machine learning for settlement detection and population distribution.
- Partners with government statistical offices for ground truth validation.
- Data published on HDX and their own Data Hub under open licences.

### What We Can Reuse

- **High-resolution population data** for exposure calculations (how many people affected by a causal chain).
- **Health/school facility locations** for infrastructure vulnerability analysis.
- **71 datasets on HDX** already standardised and accessible.
- Complementary to PRIO-GRID -- GRID3 provides higher resolution for Africa that can be aggregated to grid cells.

---

## 16. Alan Turing Institute -- Humanitarian AI

**What it is:** The UK's national institute for data science and artificial intelligence, with several projects relevant to humanitarian data and food security forecasting.

**Links:**
- Website: https://www.turing.ac.uk/
- AI for Human Rights: https://www.turing.ac.uk/ai-human-rights
- Digital Aid event: https://www.turing.ac.uk/events/digital-aid-understanding-digital-challenges-facing-humanitarian-assistance

### Relevant Projects

**Food Insecurity Prediction:**
- Applied data science project predicting food insecurity in developing countries using RHoMIS (Rural Household Multi-Indicator Survey) data.
- Explores automating the assignment of food insecurity levels to households using machine learning.
- Code: https://github.com/willianck/Predicting-Food-Insecurity

**Project Cumulus (Climate Resilience + Food Security):**
- Funded by the Gates Foundation and FCDO.
- Partners: Turing Institute, University of Cambridge, University of Leeds, with universities and meteorological agencies in Ghana and Senegal.
- Goal: co-design more accurate, bespoke weather forecasting systems to help farmers improve crop yields and reduce economic losses.
- Combines AI forecasting with local agricultural knowledge.

**AI for Human Rights:**
- Explores AI applications for monitoring human rights situations.
- Relevant for Causal Atlas's potential to identify causal chains leading to human rights violations.

### What We Can Learn

- Turing's food insecurity prediction work demonstrates that ML can predict food security outcomes using survey + remote sensing data.
- Project Cumulus shows the importance of co-design with local stakeholders -- Causal Atlas should involve domain experts and local researchers.
- Their academic rigour and publication standards are a model for our research-first approach.

---

## 17. Data-Driven Humanitarian Response -- Platform Survey

> **Findings as of March 2025:** Based on OCHA Centre for Humanitarian Data's annual reports and broader sector survey.

### State of Open Humanitarian Data (2024-2025)

- **74% of relevant crisis data** is available and up-to-date across 22 humanitarian operations (up from 70% in 2024).
- **HDX** hosts 18,110+ datasets from 254 locations and 2,147 sources.
- Key gaps remain: sub-national granularity, real-time updates, cross-domain integration.

### Emerging Technologies in Humanitarian Response

| Technology | Application | Examples |
|---|---|---|
| **AI/ML** | Predictive analytics, nowcasting, NLP for report analysis | HungerMap LIVE, VIEWS, WFP Conflict Forecast |
| **LLMs** | Humanitarian data assistant, report summarisation | OCHA's Humanitarian AI Assistant |
| **Crisis mapping** | Rapid situation assessment | HOT, MapAction, Ushahidi |
| **Mobile data** | Population mobility, displacement tracking | Flowminder/FlowKit, Meta Data for Good |
| **Satellite imagery** | Damage assessment, vegetation monitoring, nightlights | GEE, Copernicus, Planet |
| **Blockchain** | Supply chain tracking, identity management | Emerging; limited deployment |

### Key Challenges (from sector surveys)

1. **Limited data literacy** among humanitarian staff.
2. **Lack of interoperable data systems** -- each organisation uses different tools and formats.
3. **Inconsistent data quality** across sources.
4. **Ethical concerns** -- privacy, consent, data protection.
5. **No systematic platform for cross-domain data sharing** -- most data remains siloed by sector.
6. **Gap between data producers and decision-makers** -- analysis often does not reach those who need it.

### Implications for Causal Atlas

- The humanitarian sector has strong demand for cross-domain data integration but lacks the tools.
- Causal Atlas must be designed for users with varying data literacy -- from researchers to programme managers.
- Interoperability with existing systems (HDX, HAPI, CKAN) is essential for adoption.
- Ethical data handling (especially for conflict and displacement data) must be a core design principle.

---

## 18. The "Causal Search Engine" Concept

> **Question:** Is anyone building a searchable database of causal relationships that could be queried like a search engine?

### Existing Projects in This Space

#### 18.1 Csql Causal Database (2026)

| Attribute | Detail |
|---|---|
| **Paper** | https://arxiv.org/html/2601.08109v1 |
| **Status** | Research preprint (Jan 2026) |
| **Scale** | 295,459 concept strings, 260,777 directed causal edges, 44 publication years |
| **Method** | NLP extraction from academic literature |

Produces two tables: `atlas_nodes` (concepts) and `atlas_edges` (causal generators). The naming convention is strikingly similar to Causal Atlas. However, their "causality" is text-mined from published papers, not discovered from observational data.

#### 18.2 Causaly (Commercial)

| Attribute | Detail |
|---|---|
| **URL** | https://www.causaly.com |
| **Domain** | Biomedical |
| **Status** | Active, well-funded commercial product |
| **Method** | Custom NLP + ontologies for biomedical causal knowledge graph |

A "causal search engine" for life sciences R&D. Users can search for causal relationships (e.g., "What causes drug resistance in melanoma?") and get answers sourced from biomedical literature. **This is the closest to the "causal search engine" concept**, but purely in the biomedical domain and based on text, not observational data.

#### 18.3 WikiCausal (IBM Research, 2024)

| Attribute | Detail |
|---|---|
| **Paper** | ISWC 2024 |
| **GitHub** | https://github.com/IBM/wikicausal |
| **Method** | Corpus and evaluation framework for causal knowledge graph construction from Wikipedia |

Extracts causal relations between event concepts from Wikipedia articles. Uses neural question-answering models and concept linking. Evaluates against existing causal relations in Wikidata. Publicly available corpus and framework.

#### 18.4 CausalRAG (2025)

| Attribute | Detail |
|---|---|
| **Paper** | ACL Findings 2025 |
| **Method** | Integrates causal graphs into Retrieval-Augmented Generation systems |

Improves LLM reasoning by incorporating causal graph structures into the retrieval process. Relevant for Causal Atlas's AI-assisted interpretation layer.

#### 18.5 Dimensions Causal Relationship Search (Digital Science / metaphacts, 2024)

| Attribute | Detail |
|---|---|
| **URL** | https://blog.metaphacts.com/identifying-causal-relationships-with-knowledge-graphs-and-large-language-models |
| **Status** | Beta (presented at BioTechX 2024) |
| **Method** | Knowledge graph (32B+ statements) + LLMs for causal relationship extraction |

Uses the Dimensions Knowledge Graph (built on a unified semantic model) to identify causal relationships. Currently focused on scientific literature. Demonstrates growing commercial interest in causal search.

### Analysis: Where Causal Atlas Fits

| Project | Domain | Data Source | Causality Type | Spatial | Temporal |
|---|---|---|---|---|---|
| Csql | General science | Academic papers | Text-mined | No | No |
| Causaly | Biomedical | Biomedical literature | Text-mined (NLP) | No | No |
| WikiCausal | General events | Wikipedia | Text-mined (NLP) | No | No |
| CausalRAG | General | LLM + graphs | Reasoning-enhanced | No | No |
| **Causal Atlas** | **Multi-domain humanitarian** | **Observational data** | **Statistically discovered** | **Yes (grid cells)** | **Yes (monthly)** |

**Key insight:** All existing "causal search" projects extract causal claims from text. **No one is building a searchable database of statistically validated causal relationships discovered from observational spatiotemporal data.** This is Causal Atlas's unique position -- a "causal search engine" grounded in data, not text.

The vision: a user searches "What causes food insecurity in the Sahel?" and gets back statistically validated causal chains (drought -> crop failure -> food price spike -> food insecurity) with lag structures, confidence intervals, and spatial variation, all derived from observational data rather than literature mining.

---

## 19. PyWhy Ecosystem -- Causal Inference in Python

> **Note:** This ecosystem is important enough to warrant its own section, as it represents the most comprehensive open-source causal inference toolkit available.

**Organisation:** https://www.pywhy.org/

| Package | Stars | Purpose | Relevance to CA |
|---|---|---|---|
| **causal-learn** | ~1,000+ | Causal discovery (PC, GES, LINGAM, FCI, GIN, etc.) | Alternative/complement to Tigramite for discovery |
| **dowhy** | ~7,000+ | Causal inference (explicit modelling, assumption testing, do-calculus) | Validating discovered causal relationships |
| **EconML** | ~4,000+ | ML-based causal effect estimation (DML, metalearners, instrumental variables) | Estimating treatment effects |
| **gcm** | Part of dowhy | Graphical causal models | Structural causal modelling |
| **dodiscover** | ~100 | Causal discovery with pandas-like API | Simplified discovery interface |

### causal-learn Deep Dive

Published in JMLR 2024, causal-learn is a Python translation and extension of the CMU Tetrad project. Key features:

**Algorithm Categories:**
1. **Constraint-based:** PC, FCI (handles latent confounders), CPC, CDNOD (non-stationary data)
2. **Score-based:** GES, exact search
3. **Functional causal models:** LINGAM, ANM (additive noise models)
4. **Hidden representation learning:** Causal representation learning methods
5. **Permutation-based:** Methods for causal structure discovery
6. **Granger causality:** Time series methods

**Utilities:**
- Multiple conditional independence tests (Fisher-z, Chi-square, KCI, etc.)
- Score functions (BIC, generalised score)
- Graph operations and evaluation metrics
- Visualisation tools

### Comparison: causal-learn vs Tigramite

| Feature | causal-learn | Tigramite |
|---|---|---|
| **Focus** | General causal discovery (tabular + some time series) | Time series causal discovery (specialised) |
| **Algorithms** | Broad (20+ methods) | Deep (PCMCI family, highly optimised) |
| **Time series** | Granger causality, basic temporal methods | PCMCI, PCMCIplus, LPCMCI, RPCMCI, J-PCMCI+ |
| **Latent confounders** | FCI | LPCMCI |
| **Non-linear** | ANM, KCI-based tests | CMIknn, GPDC |
| **Spatial awareness** | None | None (but RGCPD/SPACY add this) |
| **Community** | PyWhy ecosystem, active development | Jakob Runge (DLR), climate science community |
| **Recommendation** | Complement for validation | **Primary engine for Causal Atlas** |

**Decision:** Use Tigramite/PCMCI as the primary causal discovery engine (optimised for our time series use case), with causal-learn as a validation/comparison tool, and dowhy for explicit causal modelling and assumption testing.

---

## 20. World Bank DIME and ImpactAI

**What it is:** The World Bank's Development Impact Evaluation (DIME) unit facilitates impact evaluations within World Bank projects, with a focus on causal evidence for development policy.

**Links:**
- DIME: https://www.worldbank.org/en/about/unit/unit-dec/impactevaluation
- ImpactAI: https://www.worldbank.org/en/about/unit/unit-dec/impactevaluation/ai

### ImpactAI

- Uses **LLMs to synthesise quantitative causal research evidence** from impact evaluation literature.
- Extracts insights from published impact evaluations to support development financing decisions.
- Delivers aggregated, quantitative research summaries and interactive visualisations.
- Specialises in **causal evidence** -- only surfaces findings from studies with rigorous identification strategies (RCTs, difference-in-differences, regression discontinuity).

### What We Can Learn

- ImpactAI demonstrates the value of AI-assisted synthesis of causal evidence -- exactly what Causal Atlas's interpretation layer aims to do.
- However, ImpactAI works from published literature (text), while Causal Atlas works from observational data (statistical discovery).
- The two approaches are complementary: Causal Atlas discovers causal relationships from data; ImpactAI (or similar) could validate whether those relationships have been confirmed in the literature.

### Limitations

- Literature-based, not data-driven discovery.
- Focus on micro-level development interventions, not macro-level cross-domain causal chains.
- Not publicly available as a tool.

---

## 21. Synthesis: Gaps and Opportunities for Causal Atlas

### 21.1 What Already Exists

The landscape is rich but fragmented:

| Capability | Existing Solutions | Gap for Causal Atlas |
|---|---|---|
| **Data access** | HDX, HAPI, GDELT BigQuery, ACLED API, CHIRPS, ClimateSERV | Already well-served. Build on existing APIs. |
| **Spatial data integration** | PRIO-GRID, AfroGrid, xSub | Grid-cell frameworks exist but cover limited domains/regions. |
| **Conflict forecasting** | VIEWS, ACLED CAST, WFP Conflict Forecast | Strong for prediction but do not test causality. |
| **Causal discovery (time series)** | Tigramite, RGCPD, CausalAI | Mature methods exist but are not applied at scale to cross-domain humanitarian data. |
| **Geospatial visualisation** | Kepler.gl, deck.gl, Foursquare Studio | Excellent open-source tools available. |
| **Crisis mapping** | Ushahidi, HOT, MapAction | Focus on operational response, not analytical research. |
| **Climate-conflict analysis** | Strata, Causal4Migrations, Sahel PA | Small-scale, one-off projects — no sustained platform. |
| **Multi-domain data overlay** | HungerMap LIVE, Strata | Overlay/descriptive only — no causal testing. |

### 21.2 The Gap Causal Atlas Fills

No existing project combines all of these:

1. **Multi-domain data ingestion** — climate, conflict, economic, health, food security, pollution on a common grid.
2. **Automated spatiotemporal alignment** — normalising diverse data sources to a common grid-month framework.
3. **Statistical causal discovery** — going beyond correlation/overlay to test for time-lagged causal relationships.
4. **Interactive visualisation** — letting users explore discovered causal links spatially and temporally.
5. **Open-source and accessible** — not locked behind commercial licensing or institutional access.

The closest projects are:
- **Causal4Migrations** — does cross-domain causal discovery but only for 3 districts in Somalia.
- **VIEWS** — operates at scale on PRIO-GRID but does prediction, not causal discovery.
- **Strata** — does cross-domain overlay globally but without causal inference.
- **AfroGrid** — integrates multi-domain data on PRIO-GRID but has no analytical tools.

Causal Atlas would effectively combine the data integration of AfroGrid, the spatial framework of PRIO-GRID, the causal inference engine of Tigramite, and the visualisation of Kepler.gl into a single, open-source platform.

### 21.3 Key Lessons from Prior Art

1. **Use existing data APIs; do not re-host data.** HDX, HAPI, GDELT BigQuery, and ClimateSERV already solve the data access problem. Our value is in alignment and analysis, not storage.

2. **PRIO-GRID 0.5° cells are the standard.** VIEWS, AfroGrid, and much conflict research uses this grid. We should adopt it without modification.

3. **Tigramite/PCMCI is the causal inference standard for time series.** Multiple independent projects have converged on it. Build on this foundation.

4. **Kepler.gl is the leading open-source geospatial visualisation library.** GPU-accelerated, supports temporal playback, and is actively maintained.

5. **Cross-domain causal discovery at scale has NOT been done.** Every project we found either (a) works across domains but does not test causality, or (b) tests causality but only within a single domain or at tiny scale.

6. **The "causal search engine" concept is emerging but entirely text-based.** Causaly, WikiCausal, Csql, and ImpactAI all extract causal claims from literature. No one is building a searchable database of statistically discovered causal relationships from observational data. This is a genuinely novel contribution.

7. **SPACY (Rose-STL-Lab) solves the scalability problem we will face.** Their variational inference approach to discovering latent causal structures from spatiotemporal data -- reducing high-dimensional grid data to a lower-dimensional latent space -- is directly applicable to our challenge.

8. **The PyWhy ecosystem provides complementary causal tools.** Tigramite for discovery, causal-learn for validation, dowhy for explicit modelling, EconML for effect estimation. We should build on this entire ecosystem, not just Tigramite.

9. **Humanitarian sector needs are clear but unmet.** 74% of crisis data is available, but no platform integrates it across domains for causal analysis. Data literacy varies widely among target users. Ethical data handling is non-negotiable.

10. **Population mobility data** (from Flowminder/FlowKit, Meta Data for Good) is an underexplored data source for validating displacement-related causal chains.

### 21.4 Updated Project Landscape Map

```
                    DATA INTEGRATION
                         |
            PRIO-GRID -- AfroGrid -- HDX HAPI
                |            |           |
                v            v           v
            VIEWS    ClimateSERV    FEWS NET
              |          |              |
              v          v              v
         PREDICTION  DATA ACCESS  FOOD SECURITY
              |          |              |
              v          v              v
    ┌─────────────────────────────────────────┐
    │        GAP: CAUSAL ATLAS FILLS          │
    │                                         │
    │   Multi-domain + Causal Discovery       │
    │   + Interactive Visualisation            │
    │   + AI Interpretation                    │
    └─────────────────────────────────────────┘
              |          |              |
              v          v              v
         Tigramite   Kepler.gl      Claude API
         PCMCI      deck.gl/DuckDB   PyWhy
```

### 21.5 Priority Integration Targets

Based on this expanded survey, the priority integration order for Causal Atlas should be:

1. **Core data pipeline:** PRIO-GRID backbone + UCDP-GED (conflict) + CHIRPS (rainfall) + MODIS NDVI (vegetation) -- replicating and extending AfroGrid globally.
2. **Food security layer:** HDX HAPI (IPC classifications) + WFP food prices + FEWS NET data (via FEWSNet_to_PG methodology).
3. **Causal engine:** Tigramite/PCMCI primary, with SPACY latent-space approach for scalability.
4. **Visualisation:** Kepler.gl v3 embedded React component, DuckDB-WASM for pre-computed result exploration, PMTiles for base map tiles.
5. **Validation:** PyWhy/causal-learn for method comparison, CauseME benchmarks for algorithm selection.
6. **Interpretation:** Claude API for natural language explanation of discovered causal chains, informed by ImpactAI-style literature synthesis.

---

*This document should be updated quarterly. Key items to watch: SPACY's ICML 2025 publication and code release, PyWhy ecosystem evolution, VIEWS 2.0 platform stabilisation, new entrants in the humanitarian data integration space, and commercial "causal search engine" products that may expand beyond biomedical domains.*

6. **Spatial autocorrelation must be handled.** The Colombia forest-conflict study and geocausal R package both emphasise that ignoring spatial dependence leads to false causal claims.

7. **Open-source sustainability is hard.** WFP Conflict Forecast went from open to closed. Salesforce CausalAI was archived. VIEWS is "not yet ready for operational use." Plan for long-term maintenance from the start.

8. **The policy community wants multi-domain overlays.** Strata (130+ UN country teams), HungerMap LIVE (90+ countries), INFORM (191 countries) all demonstrate demand. Adding causal rigour to these overlays would be transformative.

### 11.4 Reusable Components for Causal Atlas

| Component | Source | How to Reuse |
|---|---|---|
| **Spatial grid framework** | PRIO-GRID v3 | Adopt 0.5° WGS84 grid as spatial backbone |
| **Integrated multi-domain data** | AfroGrid | Use as starting dataset for Africa; replicate methodology globally |
| **Causal inference engine** | Tigramite (PCMCI) | Core statistical engine for discovering time-lagged causal links |
| **Spatial causal precursor workflow** | RGCPD | Adopt spatial aggregation → causal testing pipeline |
| **Map visualisation** | Kepler.gl | Embed as React component for interactive map display |
| **Data access APIs** | HDX HAPI, gdeltPyR, ClimateSERVpy | Use existing Python client libraries for data ingestion |
| **ML pipeline architecture** | VIEWS pipeline | Reference for modular, reproducible analytical workflows |
| **Spillover/carryover modelling** | geocausal R package | Methodological framework for spatial/temporal effect propagation |
| **Method benchmarking** | CauseME platform | Validate our methods against established benchmarks |

### 11.5 Projects to Watch

| Project | Why Watch |
|---|---|
| VIEWS next-gen platform | New architecture launching; may expand beyond conflict prediction |
| HDX HAPI | Rapidly evolving API; may add analytical endpoints |
| Strata (UNEP) | Expanding to more environmental stress indicators |
| Tigramite | Active development; J-PCMCI+ for multi-dataset analysis is particularly relevant |
| AfroGrid v2 | Potential expansion beyond Africa |

---

## Sources and Links

### Platforms and Tools
- UNEP Strata: https://unepstrata.org/
- WFP HungerMap LIVE: https://hungermap.wfp.org/
- Live Earth: https://www.liveearth.com/
- Kepler.gl: https://kepler.gl/ | https://github.com/keplergl/kepler.gl
- Foursquare Studio: https://foursquare.com/products/studio/
- GeoNode: https://geonode.org/ | https://github.com/GeoNode/geonode
- HDX: https://data.humdata.org/
- HDX HAPI: https://github.com/OCHA-DAP/hdx-hapi
- ACAPS: https://www.acaps.org/
- FEWS NET: https://fews.net/
- INFORM: https://drmkc.jrc.ec.europa.eu/inform-index
- Ushahidi: https://www.ushahidi.com/ | https://github.com/ushahidi
- HOT: https://www.hotosm.org/ | https://github.com/hotosm
- MapAction: https://mapaction.org/
- GDELT: https://www.gdeltproject.org/
- VIEWS: https://viewsforecasting.org/ | https://github.com/views-platform
- ACLED: https://acleddata.com/
- ClimateSERV: https://climateserv.servirglobal.net/ | https://github.com/SERVIR/ClimateSERV2
- xSub: https://cross-sub.org/
- Bellingcat Toolkit: https://bellingcat.gitbook.io/toolkit | https://github.com/bellingcat
- CrisisMappers: https://crisismapping.ning.com/
- ReliefWeb: https://reliefweb.int/
- CauseME: https://causeme.uv.es/

### Causal Inference Libraries and Tools
- Tigramite: https://github.com/jakobrunge/tigramite
- Salesforce CausalAI: https://github.com/salesforce/causalai (archived)
- geocausal: https://github.com/mmukaigawara/geocausal | https://cran.r-project.org/web/packages/geocausal/
- RGCPD: https://github.com/semvijverberg/RGCPD
- DeepCausality: https://github.com/deepcausality-rs/deep_causality
- Causal Map: https://www.causalmap.app/

### Research Projects
- Causal4Migrations: https://github.com/IPL-UV/Causal4Migrations
- Spatio-temporal causality (Colombia): https://github.com/runesen/spatio_temporal_causality
- AfroGrid: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LDI5TK
- CLIMADA: https://climada.ethz.ch/ | https://github.com/CLIMADA-project/climada_python
- CausalST Papers: https://github.com/yutong-xia/CausalST_Papers

### Community GDELT Tools
- gdeltPyR: https://github.com/linwoodc3/gdeltPyR
- GDELT Dashboard: https://github.com/jameslaneconkling/gdelt-dashboard
- GDELT Doc API Client: https://github.com/alex9smith/gdelt-doc-api

### Key Papers
- Runge et al. (2019). "Detecting and quantifying causal associations in large nonlinear time series datasets." *Science Advances*. https://www.science.org/doi/10.1126/sciadv.aau4996
- Hegre et al. (2019). "ViEWS: A political violence early-warning system." *Journal of Peace Research*. https://journals.sagepub.com/doi/full/10.1177/0022343319823860
- Tollefsen et al. (2012). "PRIO-GRID: A unified spatial data structure." *Journal of Peace Research*. https://journals.sagepub.com/doi/10.1177/0022343311431287
- Zhukov et al. (2019). "Introducing xSub: A new portal for cross-national data on subnational violence." *Journal of Peace Research*. https://journals.sagepub.com/doi/abs/10.1177/0022343319836697
- Mukaigawara et al. (2025). "Spatiotemporal causal inference with arbitrary spillover and carryover effects." https://arxiv.org/html/2504.03464v1
- Runge (2019). "Inferring causation from time series in Earth system sciences." *Nature Communications*. https://www.nature.com/articles/s41467-019-10105-3
- AfroGrid: "Introducing AfroGrid, a unified framework for environmental conflict research in Africa." *Scientific Data* (2022). https://www.nature.com/articles/s41597-022-01198-5

---

## 22. Deep GitHub Survey -- Round 2

> **Date of findings:** March 2025
> **Purpose:** Broader search across GitHub to find additional repositories relevant to Causal Atlas's technical stack and analytical goals.

### 22.1 Food Security Prediction Repositories

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **zhou100/FoodSecurityPrediction** | ~30 | R/Python | 2022 | Replication code for "Machine learning for food security" (AEPP paper). Predicts food insecurity across three sub-Saharan African countries using prices, assets, and weather data. 55-84% accuracy. | Methodology reference for ML-based food security prediction |
| **pietro-foini/ISI-WFP** | ~20 | Python | 2024 | WFP-affiliated ML model using gradient boosted regression trees to forecast insufficient food consumption 30 days ahead. Covers Burkina Faso, Cameroon, Mali, Nigeria, Syria, Yemen. Combines food consumption observations with conflict, weather, and economic shock data. | Directly relevant -- cross-domain food security forecasting with the same data types Causal Atlas would use |
| **michael-hoon/Food-Security-Forecasting** | ~10 | Python | 2024 | EDA on factors affecting food insecurity. | Small project but useful for understanding feature engineering |
| **Busker et al. (2024) -- Horn of Africa** | N/A (paper) | Python | 2024 | Published in *Earth's Future*: "Predicting Food-Security Crises in the Horn of Africa Using Machine Learning." | Peer-reviewed ML for food security prediction in a conflict-affected region |

**Key Finding:** Food security prediction repos are relatively small and fragmented. No comprehensive open-source platform exists for multi-country food security forecasting -- a gap Causal Atlas could fill.

---

### 22.2 Conflict Early Warning Repositories

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **views-platform (org)** | Various | Python | 2025 | VIEWS forecasting platform GitHub organisation. Key repos: views-models (all VIEWS models at pgm and cm levels), views-stepshifter (time-series forecast class), views-hydranet (spatiotemporal forecast class), views-evaluation (evaluation metrics). | Gold standard for conflict forecasting; most mature open-source MLOps pipeline for monthly subnational predictions |
| **prio-data/views_pipeline** | ~50 | Python | 2025 | The operational VIEWS forecasting pipeline for monthly prediction runs. Includes MLOps and QA for all models/ensembles. | Architecture reference for Causal Atlas's own pipeline design |
| **prio-data/viewsforecasting** | ~30 | Python/Jupyter | 2024 | Jupyter notebooks and scripts for performing VIEWS monthly forecasts. | Practical implementation reference |
| **conflictforecast.org** | N/A (web) | N/A | 2025 | Evaluating Worldwide Armed Conflict Risk -- comparison platform for conflict forecasting models. | Benchmarking reference for Causal Atlas's conflict-related causal discoveries |

**Key Finding:** VIEWS dominates the open-source conflict forecasting space. No other project comes close in terms of operational maturity, MLOps sophistication, or forecast coverage.

---

### 22.3 Causal Inference with Spatial Data

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **mmukaigawara/geocausal** | ~80 | R | 2025 | Causal inference for spatiotemporal data; published on CRAN. Implements methods from Mukaigawara et al. (2025) for spatiotemporal causal inference with arbitrary spillover and carryover effects. | Directly relevant -- the only dedicated R package for spatiotemporal causal inference |
| **yutong-xia/CausalST_Papers** | ~150 | Curated list | 2025 | Curated collection of papers on causality in spatiotemporal data and ML. Regularly updated. | Essential reading list for Causal Atlas research |
| **NSAPH-Projects/space (SpaCE)** | ~60 | Python | 2024 | Spatial Confounding Environment -- benchmark datasets for evaluating causal methods tackling spatial confounding. From Harvard. | Benchmark datasets for testing Causal Atlas's spatial causal methods |
| **moprescu/Spatial-CI** | ~20 | Python | 2023 | Spatial causal inference research repository. | Research reference |
| **jakobrunge/tigramite** | 1.5k+ | Python | 2025 | The primary causal discovery library for time series. PCMCI, PCMCIplus, LPCMCI. Extensive tutorials. | Core dependency for Causal Atlas's causal analysis engine |
| **stbachinger/TigramiteGui** | ~20 | Python | 2023 | GUI prototype for Tigramite in Jupyter Notebooks. | UI reference for presenting causal graphs interactively |

**Key Finding:** The geocausal R package and CausalST_Papers curated list are particularly valuable discoveries. SpaCE provides benchmark datasets that could be used to validate Causal Atlas's methods.

---

### 22.4 Humanitarian Dashboard and Crisis Mapping

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **Human-Geomonitor (org)** | Various | Python | 2024 | Citizen researchers building a Humanitarian Crisis Prediction Pipeline using LLMs to aggregate climate, economic, political, and displacement data. | Closest in spirit to Causal Atlas -- aggregating cross-domain humanitarian data with ML/LLM analysis |
| **RealCaddish/Conflict-Crisis-Mapping-Project** | ~30 | JavaScript | 2023 | Crisis-map UIs for conflict data using Leaflet, D3, Turf.js. Includes Ukrainian War Information Mapping Project. | UI/UX patterns for conflict data visualization |
| **unhcr-dataviz (org)** | Various | R/JS | 2025 | UNHCR data visualization tools and templates. D3.js and Power BI based. | Visualization standard reference for humanitarian sector |
| **rodekruis/CommunityRisk** | ~50 | JS/Node | 2023 | Red Cross community risk assessment dashboard. Identifies most affected areas and most vulnerable individuals. Express + Angular. | Risk assessment dashboard design patterns |
| **HTBox/crisischeckin** | ~100 | C# | 2020 | Humanitarian Toolbox project for disaster volunteer coordination. | Less relevant (operational tool, not analytical) |

**Key Finding:** Human-Geomonitor is particularly interesting -- a volunteer-driven project attempting LLM-based humanitarian crisis prediction from aggregated data. Their approach validates the Causal Atlas concept but with different methodology (LLMs vs. statistical causal inference).

---

### 22.5 Climate Impact Assessment Tools

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **CLIMADA-project/climada_python** | ~300 | Python | 2025 | ETH Zurich climate risk assessment framework. Integrates hazard, exposure, vulnerability. Global coverage at 4km for tropical cyclones, river flood, agro drought, winter storms. GNU GPL3. | Directly relevant for climate hazard data and risk methodology |
| **os-climate/physrisk** | ~80 | Python | 2024 | Physical climate risk calculation engine. Bottom-up impact modelling for individual assets. Merged with FINOS (Jun 2024). | Climate risk methodology reference |
| **KKulma/climate-change-data** | ~700 | Curated list | 2024 | Curated list of APIs, open data, and ML/AI projects on climate change. | Comprehensive resource catalogue |
| **openclimatedata (org)** | Various | Python | 2024 | Open Climate Data organisation on GitHub -- various climate data tools and processing scripts. | Data access utilities |
| **CLIMADA-project/climada_petals** | ~50 | Python | 2025 | Extended CLIMADA: additional hazard types and specialised applications beyond core. | Additional hazard modelling capabilities |

**Key Finding:** CLIMADA is the most directly relevant climate risk tool for Causal Atlas. Its hazard-exposure-vulnerability framework at 4km resolution could provide climate hazard layers for our 0.5-degree grid cells (aggregation needed). CLIMADA's API design is a good model for structured hazard data access.

---

### 22.6 Geospatial Pipeline and Data Engineering

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **kontur-io/geocint** | ~100 | Bash/SQL | 2024 | Kontur's open-source ETL pipeline for geospatial data. Extracts to PostgreSQL, transforms via H3 hexagons, loads to production. MIT licence. Uses Make, PostgreSQL, PostGIS, h3-pg. | Mature geospatial ETL reference; H3 hexagon approach is an alternative to PRIO-GRID |
| **jmcarrillog/geospatial-etl** | ~30 | Python | 2022 | ETL tools for geospatial data using GDAL, designed as components for WINGS workflow system. | Simpler ETL reference |
| **duckdb/duckdb-spatial** | ~800 | C++ | 2025 | Official DuckDB spatial extension. GEOMETRY type (Simple Features), reprojection across CRS, 50+ data source import/export. Early stage but rapidly developing. | Core technology for Causal Atlas's data stack |
| **giswqs/duckdb-spatial** | ~100 | Python/Jupyter | 2025 | Code examples for "Spatial Data Management with DuckDB" book. | Learning resource for DuckDB spatial capabilities |
| **Cidree/duckspatial** | ~30 | R | 2024 | R interface to DuckDB spatial extension. Bridges DuckDB spatial with R's ecosystem. | Relevant if Causal Atlas needs R interoperability |

**Key Finding:** DuckDB spatial extension (duckdb-spatial) is maturing rapidly and confirms our tech stack choice. The Geocint pipeline from Kontur demonstrates a production-grade geospatial ETL approach, though it uses PostgreSQL/PostGIS rather than DuckDB/Parquet.

---

### 22.7 PRIO-GRID Ecosystem

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **prio-data/priogrid** | ~40 | R | 2025 | Replication scripts for PRIO-GRID v3.0 dataset generation. Uses sf, terra, exactextractr. | Core spatial framework reference |
| **prio-data/climate_extremes** | ~10 | Python/R | 2024 | Climate extremes data processing for PRIO-GRID. | Data processing patterns for climate variables on PRIO-GRID |
| **prio-data (org)** | Various | Mixed | 2025 | PRIO's GitHub organisation. Hosts VIEWS pipeline, PRIO-GRID, and various research tools. | Primary source for conflict research data tools |

**Key Finding:** The prio-data organisation on GitHub is the most important source of reference implementations for PRIO-GRID-compatible data processing. Their R-based approach will need Python translation for Causal Atlas.

---

### 22.8 Kepler.gl for Analysis

| Repository | Stars | Language | Last Active | Description | Relevance |
|---|---|---|---|---|---|
| **keplergl/kepler.gl** | 10k+ | JavaScript | 2025 | Core Kepler.gl library. React + Redux component for geospatial visualization. Renders millions of points. Donated to OpenJS Foundation. | Primary visualization engine for Causal Atlas |
| **kylebarron/keplergl_cli** | ~100 | Python | 2023 | CLI/Python API for quickly viewing data in Kepler.gl. Simple wrapper. | Useful for development/prototyping |
| **keplergl/kepler.gl-data** | ~50 | Data | 2024 | Sample datasets for Kepler.gl demos. | Example data patterns |

**Key Finding:** Kepler.gl remains the best choice for Causal Atlas's visualization layer. The React/Redux architecture allows deep integration with a custom UI. The OpenJS Foundation stewardship ensures long-term maintenance.

---

### 22.9 Food Security Forecasting -- Academic Repositories

| Repository / Paper | Language | Year | Description | Relevance |
|---|---|---|---|---|
| **WFP food security forecasting** (Comm. Earth & Env., 2024) | Python | 2024 | Reservoir Computing approach for 60-day food consumption forecasting across Mali, Nigeria, Syria, Yemen. Compared ARIMA, XGBoost, LSTM, CNN, RC models. | Methodology comparison for time-series food security prediction |
| **Harmonized Food Insecurity Dataset** (Scientific Data, 2025) | R/Python | 2025 | Monthly sub-national harmonised dataset combining IPC/CH and FEWS NET phases across multiple countries. Designed for comprehensive analysis and predictive modelling. | Critical dataset for Causal Atlas -- harmonised food security data at the temporal and spatial resolution we need |

**Key Finding:** The 2025 Harmonized Food Insecurity Dataset (published in *Scientific Data*) is a particularly important discovery -- it provides monthly sub-national food security data that aligns with Causal Atlas's temporal resolution and could serve as a primary food security outcome variable.

---

## 23. Academic Software for Spatiotemporal Causal Analysis

> **Date of findings:** March 2025

### 23.1 Workshop and Community Ecosystem

The spatiotemporal causal analysis research community is rapidly organising:

- **STCausal Workshop 2024 (1st ACM SIGSPATIAL):** Held October 2024, Atlanta. First dedicated workshop on spatiotemporal causal analysis at a major GIS conference. URL: https://bdal.umbc.edu/stcausal-2024/
- **STCausal@GIScience2025 (2nd Workshop):** Continued at GIScience 2025. Part of concerted effort to build community around spatial causal analysis. URL: https://spatialcausal.github.io/stcausal-2025/
- **Dagstuhl Seminar on Causal Inference for Spatial Data Analytics (2024):** Invitation-only research seminar bringing together leading researchers in spatial causal inference.

This rapid community formation (two workshops and a Dagstuhl seminar in <2 years) signals that spatiotemporal causal analysis is a recognized emerging research area -- exactly where Causal Atlas positions itself.

---

### 23.2 CLIMADA -- ETH Zurich

| Attribute | Detail |
|---|---|
| **URL** | https://climada.ethz.ch/ |
| **GitHub** | https://github.com/CLIMADA-project |
| **Organisation** | Weather and Climate Risks Group, ETH Zurich |
| **Licence** | GNU GPL3 |
| **Language** | Python |
| **Status** | Active; web tool public release planned 2025 |

**What it Does:**
Free, open-source climate risk assessment and adaptation option appraisal framework. Integrates hazard, exposure, and vulnerability data to calculate risk, create probabilistic impact data from event sets, project climate change impacts, and evaluate adaptation measures.

**Key Capabilities:**
- Global coverage at 4km resolution via data API for: tropical cyclones, river flood, agro drought, European winter storms
- Probabilistic risk assessment from event sets
- Climate change impact projections
- Adaptation measure effectiveness evaluation
- CLIMADA Petals module extends core with additional hazard types and specialised applications

**Architecture:**
- Python-based with modular design (Core + Petals)
- Data API for accessing global hazard datasets
- Compatible with standard climate data formats (NetCDF, GeoTIFF)
- Published on HDX for humanitarian use: https://data.humdata.org/organization/eth-zurich-weather-and-climate-risks

**Relevance to Causal Atlas:**
- CLIMADA's hazard layers could feed directly into Causal Atlas as climate exposure variables
- The hazard-exposure-vulnerability framework provides a structured way to think about climate-driven causal chains
- ETH Zurich's Weather and Climate Risks group is a natural academic collaborator for Causal Atlas

---

### 23.3 PRIO and Uppsala Research Ecosystem

The Peace Research Institute Oslo (PRIO) and Uppsala University's Department of Peace and Conflict Research jointly operate the most mature academic conflict forecasting infrastructure:

**Key Tools and Outputs:**

| Tool | Purpose | Status |
|---|---|---|
| **VIEWS** | Monthly conflict forecasts 1-36 months ahead | Operational; monthly releases |
| **PRIO-GRID v3** | Spatial data infrastructure for conflict research | Alpha (v3.0.1); Beta planned |
| **UCDP GED** | Georeferenced event dataset for armed conflict | Continuously updated; download centre at ucdp.uu.se |
| **UCDP Candidate Events** | Near-real-time conflict events (less validated) | Monthly updates |
| **ETH/PRIO Civil Conflict Ceasefire Dataset** | Ceasefire data for civil conflicts | Active dataset |
| **Conflict Trends Reports** | Annual "Conflict Trends: A Global Overview" | Latest: 1946-2024 (published 2025) |

**2024 Prediction Challenge Results:**
- 13 research institutions submitted models
- Models predicted fatalities as probability distributions (not just point estimates)
- VIEWS benchmark "Conflictology" model led rankings as of February 2025
- Published in *Journal of Peace Research* (2024): https://journals.sagepub.com/doi/10.1177/00223433241300862

**Recognition:** VIEWS awarded Kluz Prize for PeaceTech Special Distinction (September 2024).

**Relevance to Causal Atlas:**
- PRIO/Uppsala ecosystem provides the conflict data foundation Causal Atlas needs
- Their prediction challenge methodology could inform benchmarking of Causal Atlas's causal discovery
- PRIO-GRID compatibility is already a Causal Atlas design decision -- these are natural institutional partners

---

### 23.4 geocausal R Package

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/mmukaigawara/geocausal |
| **CRAN** | https://cran.r-project.org/web/packages/geocausal/ |
| **Paper** | Mukaigawara et al. (2025), "Spatiotemporal causal inference with arbitrary spillover and carryover effects" |
| **Language** | R |

The only dedicated statistical package for spatiotemporal causal inference. Handles spillover effects (causal impact on neighbouring units) and carryover effects (persistence of treatment effects over time) -- both critical for the kind of cross-domain causal chains Causal Atlas aims to discover.

**Relevance to Causal Atlas:**
- Methodological reference for handling spatial and temporal spillover/carryover in causal inference
- R-only; Causal Atlas would need to implement equivalent methods in Python or call via rpy2
- The paper's formal framework for spatiotemporal causal inference could inform Causal Atlas's theoretical foundations

---

### 23.5 SpaCE (Spatial Confounding Environment)

| Attribute | Detail |
|---|---|
| **URL** | https://github.com/NSAPH-Projects/space |
| **Organisation** | Harvard NSAPH |
| **Language** | Python |

Provides realistic benchmark datasets for systematically evaluating causal inference methods that address spatial confounding. Important because spatial confounding (unmeasured variables that vary spatially and affect both treatment and outcome) is a major threat to causal inference in geospatial data.

**Relevance to Causal Atlas:**
- SpaCE benchmarks should be used to validate Causal Atlas's causal discovery methods
- Spatial confounding is a critical challenge for grid-cell level causal analysis -- methods tested on SpaCE will be more credible

---

### 23.6 Recent Methodological Advances (2024-2025)

Key papers published since the previous survey:

- **"Data-driven dimensionality reduction and causal inference for spatiotemporal climate fields"** (Physical Review E, 2024). Proposes framework for describing spatiotemporal climate variability with causal relations via fluctuation-response formalism.
- **"Discovering causal relationships between time series with spatial structure"** (arXiv, 2025). New method for causal discovery in time series that explicitly accounts for spatial structure.
- **"Climate change expected to increase conflict risks over the next decades across sub-Saharan Africa"** (The Innovation Geoscience, 2025). ML-based projection: 0.5-1.7 billion people may live in high conflict risk zones by 2050s.
- **"Modelling armed conflict risk under climate change with machine learning and time-series data"** (Nature Communications, 2022 -- highly cited). Foundational paper on ML for climate-conflict prediction.
- **DoWhy-GCM extension** (2024): Extension of DoWhy for causal inference in graphical causal models; enables attribution of distributional changes to causal mechanisms.

---

## 24. Commercial Platforms Doing Similar Things

> **Date of findings:** March 2025
> **Purpose:** Understanding commercial solutions helps position Causal Atlas as an open-source alternative and identifies capabilities to match.

---

### 24.1 Palantir Gotham / Foundry

| Attribute | Detail |
|---|---|
| **URL** | https://www.palantir.com/ |
| **Products** | Gotham (defence/intelligence), Foundry (commercial/enterprise), AIP (AI platform) |
| **Pricing** | Enterprise; reportedly $5M-$100M+ annual contracts |
| **Relevant Use** | Disaster relief organisations, defence agencies, humanitarian coordination |

**Capabilities:**
- Data integration platform that breaks down silos and unifies disparate datasets into a single framework
- Gotham: investigative analysis across all data types; designed for intelligence analysis
- Foundry: "central operating system" for data with back-end (ingestion, transformation) and front-end (analytics, dashboards) tools
- AIP (2023+): LLM integration with Gotham/Foundry for AI-assisted analysis on enterprise data
- Supports federated data sources with dynamic updates
- Multiple analytical workflows in a single workspace

**Humanitarian Use:**
- Palantir has worked with humanitarian organisations, but deployments are controversial due to the company's military/intelligence ties
- Used for COVID-19 response data integration by several governments
- NHS England used Foundry for healthcare data integration

**Relevance to Causal Atlas:**
- Palantir is the commercial benchmark for multi-source data integration and analytical workspaces
- Causal Atlas's data ingestion and harmonisation pipeline should aim for Palantir-like seamlessness, but open-source and focused on causal analysis rather than general-purpose analytics
- Palantir does NOT do automated causal discovery -- it provides a workspace for analysts to explore data manually
- **Key differentiator for Causal Atlas:** Open source, purpose-built for spatiotemporal causal analysis, accessible to humanitarian and academic users who cannot afford Palantir

---

### 24.2 Predata (FiscalNote)

| Attribute | Detail |
|---|---|
| **URL** | https://predata.com/ |
| **Acquired by** | FiscalNote (June 2021) |
| **Founded** | 2015, New York/Washington DC |
| **Focus** | Geopolitical risk forecasting from digital signals |

**How it Works:**
Uses ML to analyse internet metadata (not content/NLP) for patterns in group behaviour -- what people are researching, viewing, and focused on. Synthesises web-based data into unified "risk signals" that anticipate political and economic developments.

**Applications:**
- Anticipating sanctions (e.g., Russia sanctions)
- Taiwan-China tension monitoring
- Currency fluctuation forecasting
- Social unrest prediction

**Relevance to Causal Atlas:**
- Predata demonstrates that "digital signals" (internet metadata) can predict geopolitical events -- a novel data source Causal Atlas could consider
- However, Predata is correlation-based (predictive signals), not causal
- Commercial, closed-source, and focused on financial/security customers -- not humanitarian sector
- **Gap Causal Atlas fills:** Open-source, causally rigorous, and humanitarian-focused

---

### 24.3 Premise Data

| Attribute | Detail |
|---|---|
| **URL** | https://premise.com/ |
| **Focus** | Ground-truth data collection via contributor networks |
| **New Product (2025)** | AEGIS for Humanitarian Assistance |

**What it Does:**
Operates a global network of citizen data contributors who collect ground-truth observational data. Combines satellite imagery detection with on-the-ground validation (e.g., identifying informal settlements in Colombia with iMMAP). Contributors collect survey and observational data on WASH, food security, living conditions, and healthcare access.

**2025 Development -- AEGIS:**
AEGIS for Humanitarian Assistance is a fully remote, fully digital, AI-powered data collection and insights solution for humanitarian needs assessment and crisis monitoring. Initial data collection is self-funded. Premise claims the largest networks of data collectors in crisis-affected countries.

**Relevance to Causal Atlas:**
- Premise provides ground-truth data that could validate Causal Atlas's satellite/model-derived indicators
- AEGIS could become a data source for real-time ground-truth food security and living condition data
- However, Premise is a data collection company, not an analytics/causal inference platform -- complementary rather than competitive

---

### 24.4 Geospark Analytics (Hyperion)

| Attribute | Detail |
|---|---|
| **URL** | https://www.geosparkanalytics.com/ |
| **Product** | Hyperion AI platform |
| **Customers** | NGA (National Geospatial-Intelligence Agency), US defence |
| **Focus** | Real-time global threat intelligence |

**Capabilities:**
- AI-driven open-source intelligence (OSINT) platform
- Automated monitoring and ML-based threat forecasting
- Integrates 6.8 million unique real-time data sources: news, social media, economic indicators, governance factors, travel warnings, weather
- NGA contract for real-time operational insights

**Relevance to Causal Atlas:**
- Hyperion's scale (6.8M data sources) demonstrates what's technically achievable in multi-source integration
- Defence/intelligence focus and pricing puts it far from humanitarian accessibility
- Does not perform causal analysis -- focuses on threat detection and prediction
- **Gap Causal Atlas fills:** Open-source alternative with causal reasoning, designed for humanitarian/research use

---

### 24.5 Orbital Insight (now Privateer)

| Attribute | Detail |
|---|---|
| **URL** | https://www.orbitalinsight.com/ (redirects to Privateer) |
| **Status** | Acquired by Privateer (April 2024) |
| **Previous Product** | TerraScope geospatial intelligence platform |

**What it Did:**
Used computer vision and ML to analyse satellite imagery, phone location, and IoT data. Provided insights on supply chains, commodities, demographics, and geopolitical events. TerraScope (launched 2023) was a self-serve analytics platform for automated analysis of location and satellite imagery data.

**Partnership:** Expanded partnership with Planet Labs for access to daily 3.7m PlanetScope and 0.72cm SkySat imagery, including for humanitarian initiatives.

**Post-Acquisition Status:** Brand absorbed into Privateer (space sustainability company); future of humanitarian-focused capabilities unclear.

**Relevance to Causal Atlas:**
- Demonstrates commercial demand for satellite-imagery-derived analytics at global scale
- Acquisition highlights market consolidation -- smaller players are being absorbed
- **Opportunity for Causal Atlas:** As commercial platforms consolidate or pivot, open-source alternatives become more valuable to humanitarian users

---

### 24.6 Maxar (now Vantor)

| Attribute | Detail |
|---|---|
| **URL** | https://www.maxar.com/ |
| **Open Data Program** | https://www.maxar.com/open-data |
| **Rebranded** | Vantor (October 2025) |
| **Focus** | Satellite imagery, basemaps, 3D terrain |

**Humanitarian Relevance:**
- Open Data Program: Releases before/after satellite imagery for major disasters under Creative Commons 4.0 licence
- Imagery provided free to humanitarian community during crises
- Available on AWS Registry of Open Data: https://registry.opendata.aws/maxar-open-data/
- Supports first responders with spatial intelligence at no cost

**Commercial Products:**
- WorldView constellation: highest-resolution commercial satellite imagery
- Basemaps and 3D terrain data
- 2025: Simplified pricing, elimination of distinctions for imagery <90 days old

**Relevance to Causal Atlas:**
- Maxar/Vantor Open Data Program provides free high-resolution post-disaster imagery
- Satellite imagery could supplement Causal Atlas's coarser MODIS/VIIRS data for event-specific analysis
- However, Maxar provides raw imagery -- Causal Atlas would need to process it (or use derived products like NDVI, nightlights from other sources)

---

### 24.7 PlanetSense (ORNL)

| Attribute | Detail |
|---|---|
| **Paper** | https://arxiv.org/abs/1507.05245 |
| **Organisation** | Oak Ridge National Laboratory |
| **Status** | Research platform (not actively maintained as product) |

**What it Was:**
A real-time streaming and spatiotemporal analytics platform for gathering geo-spatial intelligence from open-source data. Four components: GeoData Cloud (storage), real-time data harvesting, data analytics framework, and web-based visualisation.

Built to combine archived data with heterogeneous real-time streams from social media and volunteered sources, integrated with ML and visualisation tools.

**Relevance to Causal Atlas:**
- PlanetSense's architecture (ingest + analyse + visualise) is conceptually similar to Causal Atlas
- The real-time streaming aspect is relevant if Causal Atlas ever moves beyond monthly analysis
- However, PlanetSense is a 2015 research prototype, not actively maintained

---

### 24.8 Competitive Positioning Summary

| Platform | Open Source | Causal Analysis | Multi-Domain | Humanitarian Focus | Spatial | Temporal | Pricing |
|---|---|---|---|---|---|---|---|
| **Palantir** | No | No (manual) | Yes | Limited | Yes | Yes | $5M+/year |
| **Predata** | No | No (predictive) | Limited | No | No | Yes | Enterprise |
| **Premise** | No | No (data collection) | Yes | Yes | Yes | Yes | Commercial |
| **Geospark/Hyperion** | No | No (predictive) | Yes | No | Yes | Yes | Defence contracts |
| **Orbital/Privateer** | No | No (descriptive) | Limited | Limited | Yes | Limited | Enterprise |
| **VIEWS** | Yes | No (predictive) | No (conflict only) | Yes | Yes | Yes | Free |
| **CLIMADA** | Yes | No (risk assessment) | No (climate only) | Limited | Yes | Limited | Free |
| **Causal Atlas** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Free** |

**Key Insight:** No existing platform -- commercial or open-source -- combines multi-domain data integration with automated causal discovery in a spatiotemporal framework designed for humanitarian use. The commercial platforms that come closest (Palantir, Geospark) are prohibitively expensive and not designed for causal analysis. The open-source platforms that come closest (VIEWS, CLIMADA) are single-domain. Causal Atlas occupies a unique and defensible position.

---

### Additional References (Round 2)

### GitHub Repositories
- ISI-WFP: https://github.com/pietro-foini/ISI-WFP
- FoodSecurityPrediction: https://github.com/zhou100/FoodSecurityPrediction
- Human-Geomonitor: https://github.com/Human-Geomonitor
- SpaCE: https://github.com/NSAPH-Projects/space
- Spatial-CI: https://github.com/moprescu/Spatial-CI
- CausalST_Papers: https://github.com/yutong-xia/CausalST_Papers
- TigramiteGui: https://github.com/stbachinger/TigramiteGui
- CLIMADA: https://github.com/CLIMADA-project/climada_python
- physrisk: https://github.com/os-climate/physrisk
- Geocint: https://github.com/kontur-io/geocint
- DuckDB Spatial: https://github.com/duckdb/duckdb-spatial
- VIEWS Pipeline: https://github.com/prio-data/views_pipeline
- UNHCR Dataviz: https://github.com/unhcr-dataviz
- CommunityRisk: https://github.com/rodekruis/CommunityRisk

### Commercial Platforms
- Palantir: https://www.palantir.com/
- Predata: https://predata.com/
- Premise: https://premise.com/
- Geospark Analytics: https://www.geosparkanalytics.com/
- Maxar/Vantor: https://www.maxar.com/
- CausaLens: https://causalens.com/
- Causaly: https://www.causaly.com/

### Academic Resources
- STCausal 2024: https://bdal.umbc.edu/stcausal-2024/
- STCausal 2025: https://spatialcausal.github.io/stcausal-2025/
- KnowWhereGraph: https://arxiv.org/html/2502.13874v2
- VIEWS Prediction Challenge: https://journals.sagepub.com/doi/10.1177/00223433241300862
- Harmonized Food Insecurity Dataset: https://www.nature.com/articles/s41597-025-05034-4

### Key Papers (Round 2)
- Hegre et al. (2024). "The 2023/24 VIEWS Prediction challenge." *Journal of Peace Research*. https://journals.sagepub.com/doi/10.1177/00223433241300862
- Busker et al. (2024). "Predicting Food-Security Crises in the Horn of Africa Using Machine Learning." *Earth's Future*. https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023EF004211
- WFP food security forecasting (2024). "Forecasting trends in food security with real time data." *Communications Earth & Environment*. https://www.nature.com/articles/s43247-024-01698-9
- "Climate change expected to increase conflict risks" (2025). *The Innovation Geoscience*. https://www.the-innovation.org/article/doi/10.59717/j.xinn-geo.2025.100139
