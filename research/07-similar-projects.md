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
11. [Synthesis: Gaps and Opportunities for Causal Atlas](#11-synthesis-gaps-and-opportunities-for-causal-atlas)

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

## 11. Synthesis: Gaps and Opportunities for Causal Atlas

### 11.1 What Already Exists

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

### 11.2 The Gap Causal Atlas Fills

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

### 11.3 Key Lessons from Prior Art

1. **Use existing data APIs; do not re-host data.** HDX, HAPI, GDELT BigQuery, and ClimateSERV already solve the data access problem. Our value is in alignment and analysis, not storage.

2. **PRIO-GRID 0.5° cells are the standard.** VIEWS, AfroGrid, and much conflict research uses this grid. We should adopt it without modification.

3. **Tigramite/PCMCI is the causal inference standard for time series.** Multiple independent projects have converged on it. Build on this foundation.

4. **Kepler.gl is the leading open-source geospatial visualisation library.** GPU-accelerated, supports temporal playback, and is actively maintained.

5. **Cross-domain causal discovery at scale has NOT been done.** Every project we found either (a) works across domains but does not test causality, or (b) tests causality but only within a single domain or at tiny scale.

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
