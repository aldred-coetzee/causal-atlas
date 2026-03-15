# Additional Data Sources for Causal Atlas

*Last updated: March 2025*

This file documents supplementary data sources beyond the core datasets covered in individual deep-dive files. These sources are grouped by domain and evaluated for their relevance to Causal Atlas's cross-domain spatiotemporal causal analysis goals.

---

## Table of Contents

- [Humanitarian & Food Security](#humanitarian--food-security)
  - [IPC/CH Food Security Phase Classification](#1-ipcch-food-security-phase-classification)
  - [FEWS NET](#2-fews-net-famine-early-warning-systems-network)
  - [INFORM Risk Index](#3-inform-risk-index)
  - [ACAPS / INFORM Severity Index](#4-acaps--inform-severity-index)
- [Displacement & Migration](#displacement--migration)
  - [IDMC](#5-idmc-internal-displacement-monitoring-centre)
  - [UNHCR Refugee Statistics](#6-unhcr-refugee-statistics)
- [Climate & Earth Observation](#climate--earth-observation)
  - [ERA5 Reanalysis](#7-era5-reanalysis-ecmwf)
  - [JRC Global Surface Water](#8-jrc-global-surface-water)
  - [Hansen Global Forest Change](#9-hansen-global-forest-change)
- [Population & Demographics](#population--demographics)
  - [WorldPop](#10-worldpop)
  - [GPW (Gridded Population of the World)](#11-gpw-gridded-population-of-the-world)
  - [SEDAC Other Datasets](#12-sedac-other-datasets)
- [Governance & Political](#governance--political)
  - [GROWup / EPR](#13-growup--epr-ethnic-power-relations)
  - [V-Dem](#14-v-dem-varieties-of-democracy)
- [Boundaries & Basemaps](#boundaries--basemaps)
  - [Natural Earth](#15-natural-earth)
  - [geoBoundaries](#16-geoboundaries)
  - [GADM](#17-gadm-global-administrative-areas)

---

## Humanitarian & Food Security

### 1. IPC/CH Food Security Phase Classification

**Overview:** The Integrated Food Security Phase Classification (IPC) is a multi-partner initiative that provides a common scale for classifying the severity and magnitude of food insecurity and acute malnutrition. It classifies areas into five phases: Minimal (Phase 1) through Famine (Phase 5). The partnership includes 19 organizations: FAO, WFP, UNICEF, FEWS NET, and others. The Cadre Harmonise (CH) is the equivalent framework used in West Africa and the Sahel.

**Maintained by:** IPC Global Partnership (hosted by FAO)

**Spatial coverage:** 30+ countries globally, with strongest coverage in sub-Saharan Africa, Middle East, and South/Southeast Asia. Data is provided at sub-national administrative unit level (typically admin-2 or admin-3).

**Temporal coverage:** Analyses from approximately 2011 to present. Each analysis covers a "current" period and one or two "projection" periods (typically 3-6 months forward). Analyses are not continuous -- they are produced periodically (typically 2-3 times per year per country) based on consensus-driven analytical exercises.

**Update frequency:** Variable by country; most countries analysed 2-3 times per year.

**Data format:** JSON via REST API; GeoJSON and Vector Tiles for geographic data. Also available as downloadable CSV/Excel through HDX.

**Access method:**
- **IPC API (v2.0):** `https://api.ipcinfo.org/` -- requires an API key (free registration). Documentation at `https://docs.api.ipcinfo.org/`.
- **HDX:** 54+ datasets at `https://data.humdata.org/organization/ipc` -- direct CSV/Excel downloads, no authentication required.
- **R package:** `ripc` on CRAN provides convenient wrappers around the API endpoints.

**Key API endpoints:**
- Areas analysis data (with GeoJSON support): `ipc_get_areas()`
- Country-level summaries: `ipc_get_country()`
- Population estimates by phase: included in area-level responses

**Key fields:** Country, analysis ID, area name, area code, period type (current/projection), phase classification (1-5), population estimates per phase, total population analysed.

**Licence:** Open data, free to use with attribution. IPC data on HDX is typically under CC BY (Creative Commons Attribution).

**Quality notes:** IPC analyses are consensus-based, meaning they represent agreed-upon classifications from multiple organisations -- generally high quality but inherently subjective. Coverage is uneven: some countries have frequent updates while others are analysed rarely. Projections are expert-driven scenarios, not statistical forecasts.

**Relevance to Causal Atlas:** Critical for food security outcome measurement. IPC phase data can serve as a dependent variable in causal analyses: drought (CHIRPS) -> crop failure (NDVI) -> food insecurity (IPC). The sub-national granularity and projection periods make it particularly valuable for testing lagged causal relationships.

**Sources:**
- https://www.ipcinfo.org/
- https://docs.api.ipcinfo.org/
- https://www.ipcinfo.org/ipc-country-analysis/api/
- https://data.humdata.org/organization/ipc
- https://cran.r-project.org/web/packages/ripc/

---

### 2. FEWS NET (Famine Early Warning Systems Network)

**Overview:** FEWS NET is a USAID-funded activity that provides evidence-based analysis on approximately 36 countries to support early warning and early action for food insecurity. It produces food security classifications (IPC-compatible), market price data, cross-border trade data, crop production data, and livelihood zone profiles. Since 1985, FEWS NET has served as a global sentinel for food crises.

**Maintained by:** USAID, with technical support from USGS, NASA, NOAA, USDA, and Chemonics International.

**Spatial coverage:** Approximately 36 countries across Africa (strongest coverage), Central America, Haiti, Afghanistan, Pakistan, Yemen, and other crisis-affected regions. Data is available at sub-national (admin-2/admin-3) and market-level granularity.

**Temporal coverage:** Market price data from early 2000s to present. Food security classifications from 2009 to present (tri-annual). Some remote sensing anomaly products (NDVI, rainfall) extend back to 1982.

**Update frequency:** Food security outlook reports produced three times per year. Market prices updated monthly. Remote sensing products updated every 10 days.

**Data format:** JSON (API), CSV (bulk downloads), PDF (reports), PNG/JPEG/SVG (charts).

**Access method:**
- **FEWS NET Data Warehouse (FDW) API:** REST API at `https://fdw.fews.net/api/`. Supports session-based or JWT token authentication. Public data accessible without auth; registered users get expanded access.
- **FEWS NET Data Explorer (FDE):** Interactive web tool at `https://fews.net/data` for browsing and downloading datasets.
- **USGS FEWS Portal:** Remote sensing products at `https://earlywarning.usgs.gov/fews/`

**Key API endpoints:**
- Market prices: `https://fdw.fews.net/api/marketpricefacts/`
- Cross-border trade: `https://fdw.fews.net/api/tradeflowquantityvalue/`
- Food security classifications: `https://fdw.fews.net/api/ipcphase/`
- Food insecure population estimates: `https://fdw.fews.net/api/ipcpopulationsize/`

**Key fields (market prices):** Country, market name, commodity, unit, currency, price, date, data source.

**Licence:** USAID-funded; data is publicly available. Some datasets may have specific attribution requirements. Check individual dataset metadata.

**Quality notes:** FEWS NET data is analyst-curated and generally high quality. Market price coverage can be patchy in conflict zones where price monitoring networks break down. The 21 million+ data records in the warehouse are standardised and quality-controlled.

**Relevance to Causal Atlas:** Extremely valuable as both an input and validation source. Market price data enables analysis of price transmission chains (global commodity price -> local market price -> food insecurity). Trade flow data reveals cross-border dependencies. The long time series of remote sensing anomalies provides continuous environmental monitoring data.

**Sources:**
- https://fews.net/
- https://fews.net/data
- https://help.fews.net/fdw/fews-net-api
- https://fdw.fews.net/en/docs/api_reference/api_reference.html
- https://earlywarning.usgs.gov/fews/

---

### 3. INFORM Risk Index

**Overview:** INFORM is a global, open-source risk assessment framework for humanitarian crises and disasters, developed by the European Commission's Joint Research Centre (JRC). It quantifies risk using the formula: **Risk = Hazard & Exposure^(1/3) x Vulnerability^(1/3) x Lack of Coping Capacity^(1/3)**. The index covers 191 countries and is built from approximately 80 indicators. It is updated twice yearly (March and September).

**Maintained by:** European Commission Joint Research Centre (JRC/DRMKC), in collaboration with OCHA, UNDP, and other partners.

**Spatial coverage:** 191 countries at national level. Sub-national INFORM indices also exist for some countries/regions.

**Temporal coverage:** Annual data from approximately 2013 to present. Historical time series available for trend analysis.

**Update frequency:** Twice per year (March and September releases).

**Data format:** Excel (XLSX) with all source data and calculation steps. Also available via HDX as CSV.

**Access method:**
- **Direct download:** `https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk/Results-and-data` -- Excel files with full methodology.
- **HDX:** 8 datasets at `https://data.humdata.org/organization/inform`
- **Interactive map/charts:** Available on the INFORM portal.
- **IMF Climate Data:** Climate-driven INFORM Risk at `https://climatedata.imf.org/`

**Three dimensions and their components:**
1. **Hazard & Exposure:** Natural hazards (earthquake, flood, tsunami, tropical cyclone, drought, epidemic) and Human hazards (conflict intensity, projected conflict risk)
2. **Vulnerability:** Socio-economic (development & deprivation, inequality, aid dependency) and Vulnerable groups (uprooted people, health conditions, children under 5, recent shocks, food security)
3. **Lack of Coping Capacity:** Institutional (DRR, governance) and Infrastructure (communication, physical infrastructure, access to health)

**Scoring:** 0.0 to 10.0 scale. Categories: Very Low (0.0-2.1), Low (2.2-3.1), Medium (3.2-4.8), High (4.9-6.7), Very High (6.8-10.0).

**Licence:** Open data, free to use. JRC/European Commission open data policy.

**Quality notes:** Well-regarded composite index but inherits limitations of its constituent indicators. Country-level granularity limits sub-national analysis. The twice-yearly cadence means it captures slow-moving risk trends rather than rapid-onset changes.

**Relevance to Causal Atlas:** INFORM provides a ready-made composite risk score that can be used as a baseline or validation metric. Its component indicators are individually available, allowing decomposition of risk drivers. The index could serve as both a predictor (risk -> crisis occurrence) and a control variable in causal models.

**Sources:**
- https://drmkc.jrc.ec.europa.eu/inform-index
- https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk/Methodology
- https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk/Results-and-data
- https://data.humdata.org/organization/inform

---

### 4. ACAPS / INFORM Severity Index

**Overview:** ACAPS is an independent information provider for the humanitarian community, offering crisis analysis and severity scoring. Their flagship data product, the INFORM Severity Index, measures the severity of 100+ humanitarian crises globally using a composite of 31 indicators across three dimensions: impact, conditions of affected people, and complexity. ACAPS also produces humanitarian access assessments, protection analyses, and crisis-specific briefing notes.

**Maintained by:** ACAPS (Assessment Capacities Project), an independent non-profit.

**Spatial coverage:** 100+ active humanitarian crises globally. Data is typically at crisis/country level, with some sub-national granularity for larger crises.

**Temporal coverage:** INFORM Severity Index data available from approximately 2020 to present. Updated regularly (monthly or more frequently for active crises).

**Data format:** JSON (API), CSV/Excel (downloadable datasets via ACAPS website and HDX).

**Access method:**
- **ACAPS API:** `https://api.acaps.org/` -- RESTful API, freely accessible, documented. Supports filtering by multiple parameters, including historical data.
- **ACAPS Data Portal:** `https://www.acaps.org/en/data` -- browse and download datasets directly.
- **HDX:** 12 datasets at `https://data.humdata.org/organization/acaps`

**Key data products:**
- INFORM Severity Index (crisis severity scoring)
- Humanitarian Access dataset (bureaucratic, physical, and security constraints)
- Crisis risk assessments
- Protection analyses

**Severity scoring:** 1-5 scale across three dimensions:
1. **Impact:** People affected, fatalities, displaced people
2. **Conditions of people affected:** Living standards, coping mechanisms, physical/mental wellbeing
3. **Complexity:** Political, security, cross-border, information, and socio-cultural complexity

**Licence:** Freely available. Attribution required.

**Relevance to Causal Atlas:** The severity index provides a standardised crisis measurement that can be used as an outcome variable. Its regular updates and historical data make it suitable for time-series analysis. The humanitarian access component is particularly interesting -- it can help explain why some crises escalate (restricted access -> worse outcomes).

**Sources:**
- https://api.acaps.org/
- https://www.acaps.org/en/data
- https://data.humdata.org/organization/acaps
- https://reliefweb.int/report/world/acaps-datasets-now-centralised-and-easily-accessible-through-its-new-api

---

## Displacement & Migration

### 5. IDMC (Internal Displacement Monitoring Centre)

**Overview:** IDMC is the world's authoritative source of data and analysis on internal displacement. It maintains the Global Internal Displacement Database (GIDD), which provides annual stock and flow figures for internally displaced persons (IDPs) by country and cause (conflict/violence vs. disasters). IDMC also publishes near-real-time Internal Displacement Updates (IDU) with provisional event-level displacement data.

**Maintained by:** IDMC, part of the Norwegian Refugee Council (NRC).

**Spatial coverage:** Global, covering all countries with reported internal displacement. Approximately 150+ countries/territories. National-level statistics in GIDD; some event-level data in IDU with lat/lon coordinates.

**Temporal coverage:**
- **GIDD (annual stock/flow):** 2008 to present (end-of-year figures)
- **IDU (event-level):** Rolling 180-day window of provisional data, updated daily.

**Update frequency:** GIDD updated annually with validated data (published in the annual GRID report, typically May/June). IDU updated daily with provisional event-level assessments.

**Data format:** JSON via API. CSV/Excel via HDX (422 datasets available).

**Access method:**
- **IDMC API:** Documentation at `https://www.internal-displacement.org/database/api-documentation/`. Provides access to both GIDD and IDU databases.
- **HDX:** 422 datasets at `https://data.humdata.org/organization/international-displacement-monitoring-centre-idmc`
- **R package:** `idmc` on CRAN for loading and wrangling IDMC displacement data.
- **Direct contact:** `ch.datainfo@idmc.ch` for technical API questions.

**Key data fields (IDU events):** id, country, iso3, latitude, longitude, centroid, displacement_type (conflict/disaster), qualifier, figure (number displaced), date, event description.

**Key data fields (GIDD annual):** Country, year, conflict stock, conflict new displacements, disaster new displacements, total IDPs.

**Licence:** Open data. Attribution to IDMC required.

**Quality notes:** GIDD data is carefully curated and validated -- considered the gold standard for internal displacement statistics. IDU data is provisional and subject to revision. Disaster displacement figures tend to be more reliable than conflict displacement figures (harder to track in active conflict zones). The 2024 year-end figure was a record 83.4 million IDPs globally.

**Relevance to Causal Atlas:** Internal displacement is both an outcome (conflict/disaster -> displacement) and a driver (displacement -> resource pressure -> secondary conflict, displacement -> health crises). The event-level IDU data with coordinates enables spatial analysis. Linking displacement data with ACLED conflict events, EM-DAT disasters, and CHIRPS rainfall anomalies could reveal causal chains.

**Sources:**
- https://www.internal-displacement.org/database/api-documentation/
- https://data.humdata.org/organization/international-displacement-monitoring-centre-idmc
- https://cran.r-project.org/web/packages/idmc/
- https://api.internal-displacement.org/sites/default/files/publications/documents/idmc-grid-2025-global-report-on-internal-displacement.pdf

---

### 6. UNHCR Refugee Statistics

**Overview:** UNHCR's Refugee Data Finder provides comprehensive statistics on forcibly displaced and stateless populations worldwide. The data covers refugees, asylum-seekers, internally displaced persons (reported to UNHCR), stateless persons, and other populations of concern. Data is aggregated from government reports, UNHCR field operations, and partner organisations.

**Maintained by:** UNHCR (UN High Commissioner for Refugees).

**Spatial coverage:** Global -- data by country of origin and country of asylum. Approximately 200+ countries/territories. National-level aggregation (no sub-national breakdowns in the public API).

**Temporal coverage:** Population stock data from 1951 to present. Asylum application data from 2000 to present. Solutions data (resettlement, returns) from 2000 to present.

**Update frequency:** Mid-year and end-of-year statistical updates. Annual publication of the Global Trends report (June).

**Data format:** JSON (API responses). CSV/Excel (downloadable via Refugee Data Finder).

**Access method:**
- **UNHCR Refugee Statistics API:** `https://api.unhcr.org/` -- open access, no authentication required. Returns JSON. Full documentation at `https://api.unhcr.org/docs/refugee-statistics.html`.
- **Refugee Data Finder:** `https://www.unhcr.org/refugee-statistics` -- interactive tool with download functionality.
- **Operational Data Portal:** `https://data.unhcr.org/` -- operational/situational data with more granular, real-time information.
- **R packages:** `refugees` and `unhcrrdp` packages available.

**Key API data categories:**
- **Population figures:** End-year stock figures by population type (refugees, asylum-seekers, IDPs, stateless, others of concern) by year, country of origin, and country of asylum.
- **Asylum applications:** Individual applications by year, country of asylum, country of origin.
- **Asylum decisions:** Decisions (granted, rejected, closed) by year, country of asylum, country of origin.
- **Solutions:** Returns, resettlement, naturalisation figures.
- **Demographics:** Age/sex breakdowns where available.

**Licence:** Open data. Free to use with attribution to UNHCR.

**Quality notes:** UNHCR data is the global standard for refugee statistics but has known limitations. Data depends on government reporting, which varies in quality and timeliness. Some countries under-report or don't report at all. Stock figures can lag behind actual movements. Sub-national data is generally not available through the public API (operational data portal has more granular data for specific situations). Stateless population data (4.4 million as of mid-2025) covers 101 countries but is known to be significantly underestimated.

**Relevance to Causal Atlas:** Refugee flows are a key outcome variable and transmission mechanism in cross-domain causal analysis. Conflict (ACLED/UCDP) -> displacement (IDMC) -> refugee outflows (UNHCR) -> host country resource pressure -> secondary effects. Combined with origin-country climate/food security data, refugee flow data can help test hypotheses about climate-driven migration. The long time series (since 1951) enables historical analysis.

**Sources:**
- https://api.unhcr.org/docs/refugee-statistics.html
- https://www.unhcr.org/refugee-statistics
- https://www.unhcr.org/what-we-do/reports-and-publications/data-and-statistics/global-public-api
- https://data.unhcr.org/

---

## Climate & Earth Observation

### 7. ERA5 Reanalysis (ECMWF)

**Overview:** ERA5 is the fifth-generation atmospheric reanalysis produced by the European Centre for Medium-Range Weather Forecasts (ECMWF) for the Copernicus Climate Change Service (C3S). It provides a comprehensive, globally complete, and consistent record of the Earth's atmosphere, land surface, and ocean waves. ERA5 combines vast amounts of historical observations with advanced modelling to produce a gridded dataset of climate variables. It is widely considered the state-of-the-art global reanalysis product.

**Maintained by:** ECMWF, for the Copernicus Climate Change Service (C3S).

**Spatial coverage:** Global, on a regular latitude-longitude grid at approximately 31 km (0.25 degree) horizontal resolution. Atmosphere resolved using 137 vertical levels from the surface to 80 km altitude. ERA5-Land provides enhanced resolution at ~9 km (0.1 degree) for land variables.

**Temporal coverage:** 1940 to present (quality-assured monthly updates within 3 months of real time). Preliminary daily updates available within 5 days of real time.

**Temporal resolution:** Hourly data for most variables. Pre-computed monthly means also available.

**Data format:** GRIB and NetCDF (via CDS API). Files can be large -- global monthly data for a single variable can be several GB.

**Access method:**
- **Climate Data Store (CDS) API:** `https://cds.climate.copernicus.eu/` -- requires free registration and personal access token. Python client: `pip install cdsapi`. Configuration via `~/.cdsapirc` file.
- **New API client:** `ecmwf-datastores-client` package with advanced features (metadata retrieval, async jobs).
- **Google Earth Engine:** Some ERA5 products available as EE assets.
- **Copernicus Climate Data Store web interface:** Interactive selection and download.

**Key variables (selection relevant to Causal Atlas):**
- 2m temperature (mean, min, max)
- Total precipitation
- Surface pressure
- 10m wind speed (u and v components)
- Soil moisture (multiple layers)
- Evaporation
- Surface solar radiation
- Snow depth
- Sea surface temperature

**ERA5 sub-products:**
- ERA5 hourly/monthly on pressure levels (upper-air fields)
- ERA5 hourly/monthly on single levels (surface fields)
- ERA5-Land (enhanced land surface resolution, ~9 km, 1950-present)

**Uncertainty information:** 10-member ensemble of data assimilations at half horizontal resolution and 3-hourly temporal resolution.

**Licence:** Copernicus Licence -- free and open access for all users. Attribution to Copernicus Climate Change Service required. No commercial restrictions.

**Quality notes:** ERA5 is the most widely used reanalysis product in climate research. Known limitations include: (1) reanalysis quality depends on observation density, which is sparse in parts of Africa and over oceans; (2) precipitation estimates can have biases compared to gauge-based datasets like CHIRPS; (3) data volume is enormous -- a full download of all variables is impractical; targeted variable/region extraction is essential.

**Relevance to Causal Atlas:** ERA5 is the most comprehensive climate dataset available for causal analysis. It provides consistent, gap-free global coverage of temperature, precipitation, wind, and dozens of other variables at high spatiotemporal resolution. For Causal Atlas, ERA5 can serve as the primary climate driver dataset: temperature extremes -> crop stress, precipitation anomalies -> flooding/drought, wind patterns -> pollution transport. Its 0.25-degree grid is close to PRIO-GRID's 0.5-degree resolution, making spatial alignment straightforward (aggregate 4 ERA5 cells per PRIO-GRID cell). The 1940-present time series is the longest available among gridded reanalysis products.

**Sources:**
- https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5
- https://cds.climate.copernicus.eu/how-to-api
- https://github.com/ecmwf/cdsapi
- https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5
- https://climatedataguide.ucar.edu/climate-data/era5-atmospheric-reanalysis

---

### 8. JRC Global Surface Water

**Overview:** The JRC Global Surface Water dataset maps the location and temporal distribution of surface water across the globe using the entire Landsat archive. It provides pixel-level statistics on water occurrence, seasonality, change, and transitions over a 37-year period. Developed by the European Commission's Joint Research Centre (JRC) in partnership with Google.

**Maintained by:** European Commission Joint Research Centre (JRC).

**Spatial coverage:** Global (between 78N and 56S latitude). Resolution: 30 metres per pixel (Landsat native resolution).

**Temporal coverage:** March 1984 to December 2021 (v1.4). Generated from 4,716,475 Landsat 5, 7, and 8 scenes.

**Temporal resolution:** Monthly history available per pixel. Two epochs defined for change detection: 1984-1999 and 2000-2021.

**Data format:** GeoTIFF rasters. Each file includes embedded colormaps for GIS display.

**Access method:**
- **Direct download:** `https://global-surface-water.appspot.com/download` -- 10x10 degree tiles. Also available via FTP at `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/`
- **Google Earth Engine:** Asset ID `JRC/GSW1_4/GlobalSurfaceWater` (7-band image) and `JRC/GSW1_4/Metadata` (per-pixel metadata).
- **WMTS:** Web Map Tile Service available via ESRI ArcGIS Online.
- **Global Surface Water Explorer:** Interactive web viewer at `https://global-surface-water.appspot.com/`

**Seven mapping layers (bands):**
1. **Occurrence:** Percentage of time water was present (0-100%)
2. **Occurrence change intensity:** Change in water occurrence between epochs
3. **Seasonality:** Number of months water is present per year
4. **Recurrence:** Frequency of water return in inter-annual cycles
5. **Transitions:** Categorical change type (permanent, seasonal, new, lost, etc.)
6. **Maximum extent:** All pixels ever detected as water
7. **Minimum extent:** Pixels detected as water in every month of every year (perennial)

**Licence:** Copernicus Programme data -- free and open access. Attribution to JRC/EC required.

**Quality notes:** 30m resolution is very high for a global dataset. Cloud cover and Landsat revisit gaps can affect temporal coverage, especially in tropical regions. The dataset only captures surface water visible to optical sensors -- subsurface water, small streams, and water under vegetation are missed. Accuracy validated at >95% for water detection.

**Relevance to Causal Atlas:** Surface water changes are both indicators and drivers of causal chains. Shrinking lakes and rivers signal drought conditions; expanding water bodies indicate flooding. Causal hypotheses: climate change -> water body shrinkage -> pastoral conflict (competition for water resources), dam construction -> downstream water loss -> agricultural impact -> food insecurity. The 30m resolution would need aggregation to PRIO-GRID cells but provides detailed baseline data on water availability trends.

**Sources:**
- https://global-surface-water.appspot.com/
- https://global-surface-water.appspot.com/download
- https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater
- https://data.jrc.ec.europa.eu/collection/id-0084

---

### 9. Hansen Global Forest Change

**Overview:** The Hansen/UMD/Google/USGS Global Forest Change dataset provides global maps of tree cover extent, loss, and gain from 2000 to 2024 at 30-metre resolution. Produced by the University of Maryland's Global Land Analysis and Discovery (GLAD) lab using time-series analysis of Landsat imagery. It is the standard global reference for forest loss monitoring.

**Maintained by:** Matthew Hansen's lab at the University of Maryland, in partnership with Google and USGS.

**Spatial coverage:** Global (all land areas). Resolution: approximately 30 metres (1 arc-second) per pixel.

**Temporal coverage:** Baseline tree cover as of year 2000. Annual tree cover loss from 2001 to 2024 (v1.12, latest version). Tree cover gain from 2000 to 2012 (binary, single period only).

**Temporal resolution:** Annual loss year layer (identifies which year each pixel lost tree cover). No intra-annual temporal detail.

**Data format:** GeoTIFF rasters, unsigned 8-bit values. Delivered as 10x10 degree tiles.

**Access method:**
- **Direct download:** `https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/download.html` -- download individual tiles or bulk URL lists for each layer.
- **Google Earth Engine:** Asset ID `UMD/hansen/global_forest_change_2024_v1_12` -- can be analysed directly in GEE without downloading.
- **Global Forest Watch:** `https://data.globalforestwatch.org/` -- processed derivatives and country statistics.
- **Web visualisation:** `https://glad.earthengine.app/view/global-forest-change`

**Available layers per tile:**
1. **treecover2000:** Percentage tree canopy cover in year 2000 (0-100)
2. **gain:** Binary, tree cover gain 2000-2012
3. **lossyear:** Year of tree cover loss (1-24, corresponding to 2001-2024)
4. **datamask:** Valid data mask (0=no data, 1=land, 2=water)
5. **first:** First Landsat multispectral image
6. **last:** Last Landsat multispectral image

**Data sizes:** Loss, gain, lossyear, datamask compress to <10 GB each globally. treecover2000 ~50 GB. First/last multispectral layers >600 GB each.

**Licence:** Creative Commons Attribution 4.0 (CC BY 4.0). Free for any use with attribution.

**Quality notes:** The dataset defines "tree cover" as canopy closure >25% for vegetation taller than 5 metres -- this means it includes tree plantations and orchards, not just natural forests. Loss detection is more reliable than gain detection. Small-scale selective logging may not be captured. Cloud-persistent regions (e.g., central Congo Basin) may have data gaps.

**Relevance to Causal Atlas:** Deforestation is a key environmental change variable that links to multiple causal chains: deforestation -> soil erosion -> flooding, deforestation -> land conflict, deforestation -> carbon emissions -> climate change, agricultural expansion -> forest loss -> biodiversity loss. The annual lossyear layer enables temporal causal analysis: does deforestation in year Y correlate with increased conflict or displacement in year Y+1? Forest loss can also serve as a proxy for agricultural frontier expansion and economic development pressure.

**Sources:**
- https://developers.google.com/earth-engine/datasets/catalog/UMD_hansen_global_forest_change_2024_v1_12
- https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/download.html
- https://data.globalforestwatch.org/
- https://glad.earthengine.app/view/global-forest-change

---

## Population & Demographics

### 10. WorldPop

**Overview:** WorldPop provides open-access spatial demographic datasets at high resolution for low- and middle-income countries. It uses a "top-down" methodology that disaggregates census/administrative population counts to ~100m grid cells using geospatial covariates (settlement patterns, building footprints from satellite imagery, land cover, infrastructure). WorldPop also produces age/sex structure estimates, urban/rural classifications, and population projections.

**Maintained by:** WorldPop, University of Southampton (UK).

**Spatial coverage:** Global coverage for 242 countries/territories. Resolution: 100m (primary) and 1km (aggregated).

**Temporal coverage:** Annual population estimates for 2015-2030 (projections based on UN population estimates). Some countries have historical estimates going back further.

**Update frequency:** Major updates approximately annually, incorporating new census data and improved covariates.

**Data format:** GeoTIFF rasters. Metadata in JSON via API.

**Access method:**
- **WorldPop REST API:** Root URL `https://www.worldpop.org/rest/data` -- returns JSON metadata and links to downloadable files.
- **WorldPop Hub:** `https://hub.worldpop.org/` -- browse and download by country and data type.
- **WorldPop Portal (STAC):** `https://www.portal.worldpop.org/` -- SpatioTemporal Asset Catalog interface.
- **Google Earth Engine:** Asset `WorldPop/GP/100m/pop`
- **HDX:** 480 datasets at `https://data.humdata.org/organization/worldpop`
- **Python tool:** `wpgpDownloadPy` on GitHub for programmatic bulk downloads.

**Key data products:**
- Population counts (unconstrained and constrained to built-area)
- Age/sex structure disaggregated population
- Urban change mapping
- Internal migration flows (modelled)
- Poverty mapping

**Licence:** Creative Commons Attribution 4.0 (CC BY 4.0). Free for any use with attribution.

**Quality notes:** Accuracy depends heavily on the quality and recency of the underlying census data. The "top-down" methodology redistributes known population totals, so country-level aggregates match official figures, but fine-grained cell-level estimates can be uncertain. In countries with outdated censuses (e.g., Nigeria, DRC), all gridded population products have high uncertainty. Building footprint integration (circa 2020+) significantly improved settlement detection.

**Relevance to Causal Atlas:** Population data is essential as a denominator for per-capita calculations and as a variable in its own right. Causal hypotheses: population growth -> resource pressure -> conflict, urbanisation -> pollution, population density -> disease transmission. WorldPop's 100m resolution enables fine-grained exposure estimation (how many people affected by a flood, in a conflict zone, exposed to pollution). The annual time series allows tracking demographic change as a slow-moving causal variable.

**Sources:**
- https://www.worldpop.org/sdi/introapi/
- https://hub.worldpop.org/
- https://www.portal.worldpop.org/
- https://developers.google.com/earth-engine/datasets/catalog/WorldPop_GP_100m_pop
- https://github.com/wpgp/wpgpDownloadPy

---

### 11. GPW (Gridded Population of the World)

**Overview:** GPW is NASA SEDAC's flagship population dataset. Unlike WorldPop, GPW uses a minimal modelling approach: it simply apportions census population counts into uniform grid cells within administrative units, without using ancillary data to redistribute population. This makes it a "pure census" gridded product -- less spatially precise than WorldPop but more transparent and reproducible.

**Maintained by:** NASA Socioeconomic Data and Applications Center (SEDAC), operated by CIESIN at Columbia University. Note: in April 2025, the SEDAC contract was terminated, but as of June 2025, all datasets were relocated to Earthdata Cloud and remain accessible.

**Spatial coverage:** Global. Resolution: 30 arc-seconds (~1 km at the equator) for v4.

**Temporal coverage:** GPWv4 Revision 11 provides estimates for years 2000, 2005, 2010, 2015, and 2020 (5-year intervals). Earlier versions (GPWv3) cover 1990, 1995, 2000.

**Data format:** GeoTIFF, NetCDF, ASCII rasters. Also available as administrative unit center points (CSV/Shapefile).

**Access method:**
- **NASA Earthdata:** `https://www.earthdata.nasa.gov/data/projects/gpw/data-access-tools` -- requires free NASA Earthdata login.
- **NASA Earthdata Search:** Search for "GPW" in Earthdata Search.
- **Google Earth Engine:** Available as EE assets.
- **Direct catalog links:** Population count, population density, basic demographic characteristics, land/water area.

**Key data products (GPWv4 Rev 11):**
- Population Count: persons per pixel (2000, 2005, 2010, 2015, 2020)
- Population Density: persons per km2 (same years)
- Basic Demographic Characteristics: age/sex breakdown (2010 only)
- Data Quality Indicators: administrative unit levels, source years

**Licence:** Open data, freely available under EOSDIS Data Use and Citation Guidance. No commercial restrictions.

**Quality notes:** GPW's strength is transparency -- it does not model population distribution, so errors are traceable to census inputs. Its weakness is that population is uniformly distributed within administrative units, leading to overestimation in rural areas and underestimation in cities. Best suited for large-area analyses where sub-administrative unit precision is not critical. Only available at 5-year intervals, limiting temporal analysis.

**Relevance to Causal Atlas:** GPW provides a consistent, minimally-modelled population baseline for normalisation. For PRIO-GRID integration, GPW's 30 arc-second resolution maps directly to the grid. The 5-year intervals are coarse but stable anchors for population denominators. Consider using WorldPop for inter-censal years and GPW for cross-validation.

**Sources:**
- https://www.earthdata.nasa.gov/data/projects/gpw/data-access-tools
- https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-gpwv4-popcount-4.0
- https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-gpwv4-popdens-r11-4.11

---

### 12. SEDAC Other Datasets

**Overview:** Beyond GPW, NASA's Socioeconomic Data and Applications Center (SEDAC) hosts dozens of gridded socioeconomic datasets spanning population projections, urban extent, infrastructure, hazard exposure, poverty, and environmental sustainability. SEDAC serves as a bridge between earth science and social science data.

**Maintained by:** NASA SEDAC (formerly at CIESIN/Columbia University; datasets relocated to Earthdata Cloud as of mid-2025).

**Key datasets relevant to Causal Atlas:**

| Dataset | Resolution | Coverage | Description |
|---------|-----------|----------|-------------|
| Global Population Projections (SSPs) | 1/8 degree (~14 km) | 2000-2100 (decadal) | Population projections under Shared Socioeconomic Pathways |
| Global Urban Extent (GRUMP) | 1 km | circa 2000 | Urban vs. rural classification |
| Global Development Potential Indices | ~1 km | Current | Land suitability for renewable energy, fossil fuels, mining, agriculture |
| Poverty Mapping | Variable | Variable | Gridded poverty estimates for select countries |
| Natural Disaster Hotspots | 2.5 arc-min | Historical | Multi-hazard mortality and economic loss risk |
| Environmental Performance Index | Country | Annual | Country-level environmental governance scores |
| Population Exposure to Air Pollution | 1 km | Annual | Population-weighted PM2.5 exposure |

**Access method:** All via NASA Earthdata portal (free registration required). Search at `https://www.earthdata.nasa.gov/centers/sedac-daac`.

**Data format:** GeoTIFF, NetCDF, CSV, Shapefile (varies by dataset).

**Licence:** Open data under EOSDIS Data Use guidance.

**Relevance to Causal Atlas:** SEDAC datasets provide crucial socioeconomic context for causal analysis. Population projections under SSPs enable future scenario modelling. Development potential indices can help explain why deforestation or resource extraction occurs in certain locations. Hazard exposure datasets provide pre-computed risk layers.

**Sources:**
- https://www.earthdata.nasa.gov/centers/sedac-daac
- https://www.earthdata.nasa.gov/news/new-sedac-datasets-offer-global-spatial-population-urban-land-projections-based-shared
- https://www.earthdata.nasa.gov/news/sedac-releases-future-population-scenario-data-global-development-potential-indices

---

## Governance & Political

### 13. GROWup / EPR (Ethnic Power Relations)

**Overview:** The Ethnic Power Relations (EPR) dataset identifies all politically relevant ethnic groups and their access to state power in every country worldwide from 1946 to 2021. It codes whether ethnic groups are included in or excluded from executive state power, and to what degree. The GROWup (Geographical Research On War, Unified Platform) portal provides a web-based interface for accessing EPR and related conflict datasets with spatial overlays.

**Maintained by:** International Conflict Research group at ETH Zurich.

**Spatial coverage:** Global -- all countries with politically relevant ethnic groups. Group settlement areas are geographically coded (polygon boundaries available for most groups).

**Temporal coverage:** 1946 to 2021 (annual observations). Covers 800+ ethnic groups across approximately 180 countries.

**Data format:** CSV (country-year and group-year formats) via GROWup portal. Spatial data (group settlement areas) available as shapefiles/GeoJSON.

**Access method:**
- **GROWup Research Front-End:** `https://growup.ethz.ch/` -- interactive tool for building custom downloads in country-year or group-year format.
- **GROWup Public Front-End:** Visualisation of ethnic settlement patterns, power relations, and terrain data.
- **ETH ICR Data Page:** `https://icr.ethz.ch/data/epr/` -- direct download links for all EPR family datasets.
- **Harvard Dataverse:** `https://dataverse.harvard.edu/dataverse/epr` -- archival access to dataset versions.
- **EPR Atlas:** Detailed documentation of coding decisions and sources per country.

**EPR dataset family includes:**
- **EPR Core:** Group-level power access coding (Monopoly, Dominant, Senior Partner, Junior Partner, Powerless, Discriminated, Self-exclusion)
- **EPR-ED (Ethnic Dimensions of Armed Conflict):** Links ethnic groups to armed conflict events
- **GeoEPR:** Geographic settlement areas of ethnic groups (polygons)
- **ACD2EPR:** Links UCDP armed conflict data to ethnic groups

**Licence:** Academic use -- free for research purposes. Check specific terms for commercial use.

**Quality notes:** Expert-coded dataset with strong academic pedigree (widely cited in conflict research). Coding of "political relevance" is inherently subjective. Group boundaries and identities change over time; the dataset captures snapshots that may miss gradual shifts. Coverage ends at 2021 -- updates may not be frequent.

**Relevance to Causal Atlas:** EPR provides a critical "structural" variable for conflict analysis. Ethnic exclusion from power is one of the strongest predictors of civil conflict. Causal hypotheses: ethnic exclusion -> grievance -> armed conflict, power-sharing changes -> peace/instability. The GeoEPR spatial data enables linking ethnic group territories to PRIO-GRID cells, allowing integration with climate, economic, and conflict data for sub-national causal analysis.

**Sources:**
- https://icr.ethz.ch/data/epr/
- https://growup.ethz.ch/
- https://dataverse.harvard.edu/dataverse/epr
- https://core.ac.uk/download/pdf/43096175.pdf

---

### 14. V-Dem (Varieties of Democracy)

**Overview:** V-Dem is the largest global dataset on democracy, providing over 500 indicators and 245 indices measuring different aspects and conceptions of democracy. It covers virtually all countries from 1789 to the present, with detailed annual assessments produced by a network of 4,200+ country experts. V-Dem captures seven conceptions of democracy: electoral, liberal, participatory, deliberative, egalitarian, majoritarian, and consensual.

**Maintained by:** V-Dem Institute at the University of Gothenburg, Sweden.

**Spatial coverage:** 202 countries/territories (excludes some very small states like Andorra, Monaco, Nauru, etc.). Country-level data only -- no sub-national indicators.

**Temporal coverage:** 1789 to present (annual). Most indicators available from 1900 onward; some extend further back. Current version: v15 (v16 with 2025 data expected March 2026).

**Data format:** CSV, Stata (.dta), R (.rds). No native API, but downloadable files are well-structured.

**Access method:**
- **V-Dem website:** `https://v-dem.net/data/the-v-dem-dataset/` -- direct download of dataset ZIP files (CSV, Stata, SPSS formats). Free registration required.
- **R package:** `vdemdata` on GitHub (`https://github.com/vdeminstitute/vdemdata`) -- loads the full dataset directly into R.
- **World Bank Data360:** `https://data360.worldbank.org/en/dataset/VDEM_CORE` -- subset available.
- **Demscore:** `https://www.demscore.se/` -- integrated database combining V-Dem with other governance datasets.

**Key indicator categories:**
- Electoral democracy index (free and fair elections, suffrage, elected officials)
- Liberal democracy index (rule of law, constraints on executive, civil liberties)
- Deliberative democracy index (public reasoning, justification)
- Participatory democracy index (civil society, direct democracy)
- Egalitarian democracy index (equal protection, resource distribution)
- Corruption index (executive, legislative, judicial, public sector)
- Media freedom indicators
- Civil society indicators
- Rule of law indicators
- Women's political empowerment

**Licence:** Free for academic and non-commercial use. Available under CC BY-SA for derived works. Commercial use may require permission.

**Quality notes:** V-Dem is the gold standard for cross-national democracy measurement, produced by over 4,200 country experts with sophisticated inter-coder reliability methodology (using Bayesian item response theory to combine expert ratings). However, it is country-level only, limiting sub-national analysis. Some indicators involve inherent subjectivity. Expert recruitment can be challenging for closed authoritarian states.

**Relevance to Causal Atlas:** Governance quality and regime type are key structural variables in causal analysis. Causal hypotheses: democratic backsliding -> increased conflict, governance deterioration -> failure to respond to disasters -> humanitarian crisis, corruption -> resource extraction -> environmental degradation. V-Dem's long time series enables analysis of governance transitions and their downstream effects. While country-level, it provides essential context that can be joined to PRIO-GRID data via country identifiers.

**Sources:**
- https://v-dem.net/data/the-v-dem-dataset/
- https://www.v-dem.net/data/
- https://github.com/vdeminstitute/vdemdata
- https://en.wikipedia.org/wiki/V-Dem_Democracy_Indices

---

## Boundaries & Basemaps

These datasets do not contain thematic data for causal analysis but provide the spatial reference framework essential for integrating all other datasets.

### 15. Natural Earth

**Overview:** Natural Earth is a public domain map dataset providing global vector and raster basemap data at three scales: 1:10 million, 1:50 million, and 1:110 million. It includes political boundaries, cultural features (populated places, urban areas, roads, railroads), and physical features (land, ocean, rivers, lakes, glaciers, bathymetry). Designed by cartographers for cartographic applications.

**Maintained by:** Volunteer community of cartographers (Nathaniel Vaughn Kelso and Tom Patterson, with contributors).

**Spatial coverage:** Global. Three scale tiers:
- 1:10m (most detailed) -- suitable for large-format wall maps
- 1:50m -- suitable for medium-scale thematic mapping
- 1:110m -- suitable for small web maps and global overviews

**Boundary levels:** Admin-0 (countries) and Admin-1 (states/provinces) only. No Admin-2 or lower.

**Data format:** Shapefile, SQLite/SpatiaLite, GeoPackage.

**Access method:**
- **Direct download:** `https://www.naturalearthdata.com/downloads/` -- organised by scale and theme.
- **R package:** `rnaturalearth` for programmatic access.
- **Python:** `cartopy` includes Natural Earth data natively.

**Licence:** Public domain. No restrictions whatsoever -- commercial, government, personal use all permitted without attribution (though attribution is appreciated).

**Relevance to Causal Atlas:** Natural Earth is the standard basemap for cartographic output. Its clean, cartographer-designed geometries are ideal for map visualisations in Kepler.gl or custom web maps. Admin-0 and Admin-1 boundaries serve as spatial join keys for country-level and province-level datasets (V-Dem, INFORM, UNHCR). Not suitable as the primary boundary source for sub-national analysis (use geoBoundaries or GADM for that).

**Sources:**
- https://www.naturalearthdata.com/
- https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/
- https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/

---

### 16. geoBoundaries

**Overview:** geoBoundaries is an open-licence global database of political administrative boundaries, maintained by the William & Mary geoLab. It tracks approximately 1 million boundary geometries across 200+ countries/territories. It is the most permissively licensed comprehensive boundary dataset available, making it particularly suitable for open-source projects.

**Maintained by:** William & Mary geoLab (College of William & Mary, Virginia, USA).

**Spatial coverage:** 200+ countries/territories. Administrative levels 0 through 5+ (varies by country).

**Data format:** GeoJSON, Shapefile.

**Access method:**
- **API:** `https://www.geoboundaries.org/api/current/gbOpen/[ISO3]/[ADM-LEVEL]/` -- returns JSON with metadata and download URLs. Use "ALL" for ISO or ADM level to get bulk returns.
- **Direct download:** Browse at `https://www.geoboundaries.org/`
- **Google Earth Engine:** Available in the GEE Community Catalog.
- **R package:** `geobounds` for programmatic access.
- **GitHub:** Full dataset archived at `https://github.com/wmgeolab/geoBoundaries`

**Release types:**
- **gbOpen:** Freely available boundaries under CC BY 4.0 or ODbL. Suitable for any use.
- **gbHumanitarian:** Boundaries validated for humanitarian operations (typically from OCHA CODs).
- **gbAuthoritative:** Official government-provided boundaries (may have more restrictive licences).

**Licence:** CC BY 4.0 for gbOpen (the primary release). Attribution required.

**Quality notes:** Coverage and precision vary by country and administrative level. Higher admin levels (3+) may have less precise geometries. Boundaries are compiled from diverse sources with varying vintage dates. Regular updates as new sources become available. The open-source nature means the community can contribute corrections.

**Relevance to Causal Atlas:** geoBoundaries is the recommended boundary dataset for Causal Atlas due to its open licence (CC BY 4.0), comprehensive API, and multi-level coverage. Use cases: (1) spatial joins to assign point data (ACLED events, market locations) to administrative units, (2) aggregation boundaries for computing zonal statistics from raster data (ERA5, WorldPop), (3) boundary geometries for map visualisations. The API enables automated integration into data pipelines.

**Sources:**
- https://www.geoboundaries.org/
- https://www.geoboundaries.org/api.html
- https://github.com/wmgeolab/geoBoundaries
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7182183/

---

### 17. GADM (Global Administrative Areas)

**Overview:** GADM provides detailed maps and spatial data for all countries and their sub-divisions, with a consistently structured global dataset using uniform attribute naming and level hierarchy. It is one of the most widely used administrative boundary datasets in research and is often the default in GIS tools and academic analyses.

**Maintained by:** Robert Hijmans (UC Davis) and community contributors.

**Spatial coverage:** Global -- all countries. Up to 5 administrative levels (varies by country; many countries have 3-4 levels).

**Data format:** GeoPackage (recommended), Shapefile, KMZ (Google Earth), R spatial data objects (SpatVector via `geodata` package).

**Access method:**
- **Direct download:** `https://gadm.org/download_country.html` -- per-country or whole-world downloads.
- **R package:** `geodata` package includes `gadm()` function for direct access.
- **Python:** Download files and read with `geopandas`.
- No REST API available -- download-only.

**Administrative levels:**
- Level 0: Country boundaries
- Level 1: States/provinces/regions
- Level 2: Districts/counties
- Level 3: Sub-districts/municipalities
- Level 4-5: Lower administrative divisions (available for select countries)

**Key attributes:** GID codes (hierarchical unique identifiers, e.g., "KEN.1.2.3_1"), NAME fields at each level, TYPE fields (province, district, etc.), country ISO codes.

**Licence:** Free for academic and other non-commercial use. **Commercial use is not allowed without permission.** This is a significant restriction compared to geoBoundaries.

**Quality notes:** Generally high-quality geometries with good global coverage. Well-maintained with regular updates. The hierarchical GID system provides stable identifiers for tracking administrative units across versions. However, the non-commercial licence is a limitation for open-source projects that may have downstream commercial users.

**Relevance to Causal Atlas:** GADM is a strong option for administrative boundary data, particularly for academic analysis. However, its non-commercial licence restriction makes geoBoundaries preferable as the primary boundary source for an open-source project like Causal Atlas. GADM can still be used for research and development, and its GID coding system is a useful reference for building administrative unit crosswalks. Consider using GADM boundaries during development and geoBoundaries for production/distribution.

**Sources:**
- https://gadm.org/
- https://gadm.org/download_country.html
- https://www.dante-project.org/datasets/gadm

---

## Summary: Priority Assessment for Causal Atlas

| Dataset | Domain | Spatial Res. | Temporal Res. | API Available | Licence | Priority |
|---------|--------|-------------|---------------|--------------|---------|----------|
| ERA5 Reanalysis | Climate | 0.25 deg (~31 km) | Hourly | Yes (CDS API) | Copernicus (open) | **High** |
| WorldPop | Population | 100m / 1km | Annual | Yes (REST) | CC BY 4.0 | **High** |
| IPC/CH | Food security | Admin unit | Periodic (~3x/yr) | Yes (REST) | Open (HDX) | **High** |
| FEWS NET | Food security | Admin/market | Monthly+ | Yes (REST) | Open (USAID) | **High** |
| IDMC | Displacement | Country/event | Annual/daily | Yes | Open | **High** |
| UNHCR | Refugees | Country | Annual | Yes (REST) | Open | **High** |
| V-Dem | Governance | Country | Annual | No (download) | CC BY-SA | **Medium** |
| geoBoundaries | Boundaries | Multi-level | Static | Yes (REST) | CC BY 4.0 | **High** (infrastructure) |
| INFORM Risk | Risk | Country | Biannual | No (download) | Open (JRC) | **Medium** |
| ACAPS Severity | Humanitarian | Crisis | Monthly | Yes (REST) | Open | **Medium** |
| Hansen Forest | Environment | 30m | Annual | GEE | CC BY 4.0 | **Medium** |
| JRC Surface Water | Environment | 30m | Monthly history | GEE/FTP | Copernicus (open) | **Medium** |
| EPR/GROWup | Governance | Group territory | Annual | No (download) | Academic | **Medium** |
| GPW (SEDAC) | Population | 30 arc-sec | 5-year | Earthdata | Open | **Low** (WorldPop preferred) |
| SEDAC other | Socioeconomic | Variable | Variable | Earthdata | Open | **Low** |
| Natural Earth | Basemap | 1:10m | Static | No | Public domain | **Low** (basemap only) |
| GADM | Boundaries | Multi-level | Static | No | Non-commercial | **Low** (licence issue) |

### Key integration notes

1. **ERA5 + PRIO-GRID alignment:** ERA5's 0.25-degree grid nests cleanly into PRIO-GRID's 0.5-degree cells (4 ERA5 cells per PRIO-GRID cell). This makes ERA5 the natural climate backbone for the project.

2. **WorldPop vs GPW:** Use WorldPop as the primary population layer (100m, annual, API, open licence). Use GPW for cross-validation and as a transparent census-based reference.

3. **geoBoundaries vs GADM:** Prefer geoBoundaries for production use (CC BY 4.0 licence compatible with MIT). Use GADM during development if its geometries are better for a specific country.

4. **IPC + FEWS NET complementarity:** IPC provides the phase classifications; FEWS NET provides the underlying market price and production data that drive those classifications. Together they enable analysis of the full causal chain from price shocks to food insecurity outcomes.

5. **Displacement chain:** IDMC (internal displacement) and UNHCR (cross-border refugees) together cover the full displacement spectrum. Linking these with ACLED conflict events and EM-DAT disasters enables end-to-end causal chain analysis: hazard -> displacement -> secondary effects.

6. **Governance context:** V-Dem (regime type, corruption, civil liberties) and EPR (ethnic power relations) provide the structural political variables that moderate whether environmental shocks translate into conflict or humanitarian crisis.

---

## Additional Sources Discovered Through Deeper Research

### 18. CIESIN/SEDAC Natural Hazards Datasets

The NASA Socioeconomic Data and Applications Center (SEDAC), operated by Columbia University's Center for International Earth Science Information Network (CIESIN), hosts a suite of natural hazard risk datasets.

| Dataset | Description | Resolution | Coverage |
|---|---|---|---|
| **Global Multihazard Mortality Risks** | Combined mortality risk from cyclones, droughts, earthquakes, floods, landslides, volcanoes | 2.5 arc-minute (~5 km) grid | Global |
| **Global Earthquake Mortality Risks** | Mortality risk from earthquakes based on PGA + population | 2.5 arc-minute | Global |
| **Global Flood Mortality Risks** | Mortality risk from floods | 2.5 arc-minute | Global |
| **Global Cyclone Mortality Risks** | Mortality risk from tropical cyclones | 2.5 arc-minute | Global |
| **Global Drought Mortality Risks** | Mortality risk from drought | 2.5 arc-minute | Global |
| **Global Volcano Mortality Risks** | Mortality risk from volcanic eruptions | 2.5 arc-minute | Global |
| **Global Landslide Mortality Risks** | Mortality risk from landslides | 2.5 arc-minute | Global |

**Methodology:** Risk = Hazard frequency × Population exposure × Vulnerability. Mortality loss estimates calibrated against EM-DAT records (1981–2000). Risk classified into deciles.

**Access:** https://sedac.ciesin.columbia.edu/data/collection/ndh (NASA Earthdata login required, free)

**Format:** GeoTIFF rasters, shapefiles

**Licence:** NASA open data policy (free, unrestricted)

**Note:** These datasets are **static** (based on ~2000-era data). They represent baseline hazard risk, not time-varying exposure. Useful as a PRIO-GRID static layer for vulnerability context.

### 19. Global Volcanism Program (Smithsonian Institution)

| Property | Detail |
|---|---|
| **Maintainer** | Smithsonian Institution, National Museum of Natural History |
| **Database** | Volcanoes of the World (VOTW) v5.3.4 (December 2025) |
| **Coverage** | 1,432 Holocene volcanoes; eruption records spanning thousands of years |
| **URL** | https://volcano.si.edu/ |
| **Eruption search** | https://volcano.si.edu/search_eruption.cfm |
| **Volcano search** | https://volcano.si.edu/search_volcano.cfm |
| **API** | None (web search + Excel download) |
| **Format** | Downloadable as Excel/XML from search results |
| **Licence** | Free for research use with citation |

**Key fields:** Volcano name, location (lat/lon), country, type, summit elevation, last known eruption date, VEI (Volcanic Explosivity Index 0-8), eruption type, evidence type.

**Relevance to Causal Atlas:** Volcanic eruptions can affect air quality (SO2, ash), agriculture (ashfall), climate (aerosol cooling), and displacement. VEI 4+ eruptions have regional/global effects. Pre-computed static volcanic hazard zones can be overlaid on PRIO-GRID.

### 20. GloFAS — Global Flood Awareness System (Copernicus)

| Property | Detail |
|---|---|
| **Producer** | ECMWF / European Commission Joint Research Centre (JRC) |
| **Part of** | Copernicus Emergency Management Service (CEMS) |
| **Products** | Daily flood forecasts (since 2011), monthly seasonal streamflow outlooks (since 2017) |
| **Spatial resolution** | 0.05° (~5 km) |
| **Temporal** | Daily forecasts (10-day horizon), monthly seasonal forecasts (7-month horizon) |
| **Data format** | NetCDF |
| **Access** | Early Warning Data Store (EWDS): https://ewds.climate.copernicus.eu/ |
| **Licence** | Copernicus licence (free, attribution required) |
| **URL** | https://global-flood.emergency.copernicus.eu/ |

#### GloFAS Products

| Product | Description | Resolution | Temporal |
|---|---|---|---|
| **GloFAS Forecast** | Real-time ensemble flood forecasts | 0.05° | Daily, 30-day horizon |
| **GloFAS Seasonal** | Seasonal streamflow outlooks | 0.05° | Monthly, 7-month horizon |
| **GloFAS Historical** | River discharge reanalysis | 0.05° | 1979–present |
| **GloFAS Reforecast** | Retrospective forecasts for calibration | 0.05° | 1999–present |

#### GloFAS Seasonal Forecasts

The seasonal forecast produces monthly probability of exceeding specific flood thresholds (2-year, 5-year, 20-year return periods) for 7 months ahead. This is directly useful for anticipatory analysis.

**Access via Python:**
```python
import cdsapi

client = cdsapi.Client()
client.retrieve(
    'cems-glofas-seasonal',
    {
        'system_version': 'version_4_0',
        'variable': 'river_discharge_in_the_last_24_hours',
        'hydrological_model': 'lisflood',
        'year': '2024',
        'month': '01',
        'leadtime_hour': ['24', '720', '2160', '5040'],
        'format': 'grib',
    },
    'glofas_seasonal.grib'
)
```

### 21. Armed Conflict Survey (IISS)

| Property | Detail |
|---|---|
| **Producer** | International Institute for Strategic Studies (IISS) |
| **Product** | Annual Armed Conflict Survey publication |
| **Coverage** | All active armed conflicts globally |
| **Temporal** | Annual, since 2015 (successor to Armed Conflict Database) |
| **Format** | PDF reports + online database |
| **Access** | Subscription required (not open data) |
| **URL** | https://www.iiss.org/publications/armed-conflict-survey |

**Note:** The IISS Armed Conflict Survey is a **commercial product** requiring institutional subscription. It provides expert qualitative assessments rather than machine-readable event data. **Not recommended** for Causal Atlas primary integration due to access restrictions, but useful as a reference for validating our own conflict assessments.

### 22. Global Terrorism Database (START/UMD)

| Property | Detail |
|---|---|
| **Producer** | National Consortium for the Study of Terrorism and Responses to Terrorism (START), University of Maryland |
| **Coverage** | 200,000+ terrorist attacks, 1970–2021 |
| **Spatial** | Global; events geocoded with lat/lon |
| **Format** | Excel, geodatabase |
| **Access** | **Registration required** with personal information; access model has become more restrictive since ~2024 |
| **URL** | https://www.start.umd.edu/gtd/ |
| **Licence** | Academic use free with registration; commercial requires agreement |
| **Codebook** | https://www.start.umd.edu/sites/default/files/2024-10/Codebook.pdf |

**Key fields:** Date, country, region, city, latitude, longitude, attack type, target type, weapon type, perpetrator group, killed, wounded, property damage.

**Note:** As of 2025, GTD access has become more restricted, requiring registration with personal information. The database has not been updated beyond 2021 data as of March 2025. For terrorism events, ACLED and UCDP provide alternative coverage (ACLED codes "explosions/remote violence" and strategic developments; UCDP codes one-sided violence).

### 23. SIPRI Arms Transfers Database

| Property | Detail |
|---|---|
| **Producer** | Stockholm International Peace Research Institute (SIPRI) |
| **Coverage** | International arms transfers, 1950–2025 |
| **Update** | Annual (last updated March 2026) |
| **Metric** | Trend Indicator Values (TIV) — volume-based measure, not financial |
| **URL** | https://www.sipri.org/databases/armstransfers |
| **Trade register** | https://armstransfers.sipri.org/ |
| **API** | No official API; unofficial Python wrapper exists on GitHub |
| **Format** | Web interface output; downloadable as RTF, CSV, HTML, JSON via query parameters |
| **Licence** | Free for research use with citation |

**TIV methodology:** Weapons are valued based on physical/performance characteristics, not contract prices. Used weapons = 40% of new; refurbished = 66%. This creates a consistent volume measure across time and countries.

**Relevance to Causal Atlas:** Arms flows to a country may be a leading indicator of conflict escalation. Country-year TIV imports can serve as a contextual variable alongside WGI governance indicators.

### 24. Global Organized Crime Index (GI-TOC)

| Property | Detail |
|---|---|
| **Producer** | Global Initiative Against Transnational Organized Crime (GI-TOC) |
| **Editions** | 2021, 2023, 2025 |
| **Coverage** | 193 countries |
| **Scale** | 1–10 per indicator; composite criminality and resilience scores |
| **URL** | https://ocindex.net/ |
| **Data download** | https://ocindex.net/downloads (Excel) |
| **Licence** | Free for research use |

**Structure:**
- **Criminality score** (average of 20 indicators): 10 criminal markets (human trafficking, arms trafficking, drug trade — cannabis, cocaine, heroin, synthetic, flora/fauna crimes, non-renewable resource crimes, cyber-dependent crimes) + 5 criminal actor types (mafia-style, criminal networks, state-embedded actors, foreign criminal actors, private militia/security)
- **Resilience score** (average of 12 indicators): Political leadership, government transparency, international cooperation, national policies, judicial system, law enforcement, territorial integrity, anti-money laundering, economic regulatory capacity, victim/witness support, prevention, non-state actors

**Relevance to Causal Atlas:** Organised crime scores provide context for understanding governance failures, illicit economies, and instability drivers that are distinct from (but related to) armed conflict.

### 25. V-Dem (Varieties of Democracy) — Deeper Dive

| Property | Detail |
|---|---|
| **Producer** | V-Dem Institute, University of Gothenburg, Sweden |
| **Current version** | V-Dem v14 (March 2024); v15 and v16 since released |
| **Coverage** | 202 countries, 1789–2023 |
| **Variables** | 500+ V-Dem indicators + 245 indices + 57 external indicators |
| **URL** | https://www.v-dem.net/ |
| **Data access** | Free download (CSV, RDS); R package `vdemdata` |
| **API** | None (download only) |
| **Licence** | CC BY-SA 4.0 |
| **Size** | ~150 MB compressed |

#### Key V-Dem Indices for Causal Atlas

| Index | Description | Range | Relevance |
|---|---|---|---|
| `v2x_polyarchy` | Electoral Democracy Index | 0–1 | Core democracy measure |
| `v2x_libdem` | Liberal Democracy Index | 0–1 | Includes rule of law, civil liberties |
| `v2x_partipdem` | Participatory Democracy Index | 0–1 | Citizen participation |
| `v2x_delibdem` | Deliberative Democracy Index | 0–1 | Public reasoning quality |
| `v2x_egaldem` | Egalitarian Democracy Index | 0–1 | Equal protection and distribution |
| `v2x_corr` | Political Corruption Index | 0–1 | Corruption in various branches |
| `v2x_rule` | Rule of Law Index | 0–1 | Compliance with law, independent judiciary |
| `v2x_civlib` | Civil Liberties Index | 0–1 | Freedom of expression, association, religion |
| `v2x_clphy` | Physical Violence Index | 0–1 | Torture, political killing, forced labor |
| `v2x_freexp_altinf` | Freedom of Expression / Alternative Info | 0–1 | Media freedom, internet censorship |
| `v2xnp_regcorr` | Regime Corruption | 0–1 | Executive, legislative, judicial corruption |

#### R Package Access

```r
# install.packages("remotes")
# remotes::install_github("vdeminstitute/vdemdata")
library(vdemdata)

# Load full dataset
df <- vdem

# Search for variables
find_var("corruption")

# Get info on a variable
var_info("v2x_corr")
```

#### Python Access

```python
import pandas as pd

# After downloading from v-dem.net:
vdem = pd.read_csv("V-Dem-CY-Full+Others-v14.csv", low_memory=False)
print(f"Shape: {vdem.shape}")  # ~27,000 rows × 4,000+ columns
print(f"Countries: {vdem['country_name'].nunique()}")
print(f"Years: {vdem['year'].min()}-{vdem['year'].max()}")

# Key columns for Causal Atlas
cols = ['country_name', 'country_text_id', 'year',
        'v2x_polyarchy', 'v2x_libdem', 'v2x_corr',
        'v2x_rule', 'v2x_civlib', 'v2x_clphy']
df = vdem[cols].dropna(subset=['v2x_polyarchy'])
```

### 26. ACAPS / INFORM Severity Index — Detailed

| Property | Detail |
|---|---|
| **Producer** | ACAPS (Assessment Capacities Project) |
| **Current name** | INFORM Severity Index |
| **Coverage** | ~60-80 active crises globally |
| **Update frequency** | Monthly |
| **Scale** | 1–5 severity categories |
| **Dimensions** | Impact (20%), Conditions of affected people (50%), Complexity (30%) |
| **Indicators** | 31 core indicators |
| **URL** | https://www.acaps.org/en/thematics/all-topics/inform-severity-index |
| **Data download** | https://www.acaps.org/en/data |
| **HDX** | https://data.humdata.org/dataset/inform-global-crisis-severity-index |
| **API** | https://api.acaps.org/ |
| **Licence** | Open data |

#### Severity Categories

| Score | Category | Description |
|---|---|---|
| 1 | Very Low | Situation monitored but minimal humanitarian concern |
| 2 | Low | Localised crisis with limited impact |
| 3 | Medium | Significant humanitarian crisis |
| 4 | High | Major crisis with widespread impact |
| 5 | Very High | Extreme crisis requiring massive international response |

#### The Three Dimensions

**Impact (20%):**
- Number of people affected
- Number of fatalities
- Number of people displaced

**Conditions of affected people (50%):**
- Access to health, education, shelter
- Living standards
- Coping mechanisms
- Physical safety

**Complexity (30%):**
- Operating environment (access, security)
- Political/institutional context
- Social cohesion
- Geographic factors

**Relevance to Causal Atlas:** The INFORM Severity Index provides a validated, monthly, multi-dimensional crisis severity measure that can serve as a **composite outcome variable** for testing causal chains. If drought (CHIRPS) → crop failure (NDVI) → food insecurity (IPC) → crisis severity (INFORM), the entire chain can be tested with monthly data.

### 27. Climate Change Knowledge Portal (World Bank)

See the World Bank deep dive file (`world-bank.md`) for details. Key addition here: the CCKP provides 70+ climate indices pre-computed at 0.25° resolution, available on AWS Open Data, making it a convenient alternative to processing raw ERA5 or CRU TS data.

### Key integration notes (continued)

7. **Natural hazard risk layers:** SEDAC hazard risk grids (earthquake, flood, cyclone, drought) can be aggregated to PRIO-GRID as static vulnerability layers. These complement the dynamic event data from USGS, GloFAS, and EM-DAT.

8. **Flood forecasting chain:** GloFAS seasonal forecasts → GloFAS daily forecasts → JRC Surface Water (observed flooding) → EM-DAT (disaster impact). This chain enables testing of forecast skill and early warning value.

9. **Governance ecosystem:** V-Dem (democratic institutions), WGI (governance quality), FSI (fragility), INFORM Severity (crisis severity), and the Organized Crime Index provide a comprehensive governance context that can be joined to PRIO-GRID cells via country assignment.

10. **Arms and security:** SIPRI arms transfers + GTD terrorism events + UCDP/ACLED conflict events together provide a multi-faceted picture of security dynamics at the country and sub-national levels.

---

## Extended Dataset Catalogue

*Added: March 2025*

The following sections document additional datasets not covered above or in individual deep-dive files, organised by domain. Each entry provides enough detail to evaluate the dataset for Causal Atlas integration.

---

### Climate and Weather (Beyond CHIRPS and ERA5)

#### 28. MERRA-2 (Modern-Era Retrospective Analysis for Research and Applications, Version 2)

**What it is:** NASA's atmospheric reanalysis dataset produced by the Global Modeling and Assimilation Office (GMAO). Complements ERA5 by providing an independent reanalysis with different model physics and assimilation system.

**Maintained by:** NASA GMAO / Goddard Earth Sciences Data and Information Services Center (GES DISC)

**Spatial coverage:** Global, 0.5° latitude x 0.625° longitude (~50 km)

**Temporal coverage:** 1980 to present

**Temporal resolution:** Hourly, 3-hourly, daily, monthly, and monthly diurnal

**Access method:** NASA GES DISC (https://disc.gsfc.nasa.gov/), OPeNDAP, Google Earth Engine (`NASA/GSFC/MERRA/slv/2`)

**Data format:** NetCDF4 (lossy compression)

**Licence:** Open, free. Requires NASA Earthdata login (https://urs.earthdata.nasa.gov/) with "NASA GESDISC DATA ARCHIVE" approval.

**Key variables:** Temperature, humidity, wind speed/direction, precipitation, radiation, soil moisture, surface energy fluxes, aerosol diagnostics (unique strength over ERA5)

**How it relates to Causal Atlas:** Provides an independent check on ERA5 climate fields. Aerosol/air quality reanalysis variables are unique to MERRA-2 and support pollution-health causal chains. Hourly resolution enables sub-daily event analysis.

**Python access:**
```python
# Via the merra package
pip install merra
# Or direct OPeNDAP access with xarray
import xarray as xr
ds = xr.open_dataset('https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/...')
```

**Sources:** https://gmao.gsfc.nasa.gov/gmao-products/merra-2/data-access_merra-2/, https://climatedataguide.ucar.edu/climate-data/nasas-merra2-reanalysis

---

#### 29. CMORPH (CPC Morphing Technique) Precipitation

**What it is:** Satellite-based global precipitation estimates using morphing of passive microwave retrievals with infrared data. Higher spatial/temporal resolution than CHIRPS but shorter record.

**Maintained by:** NOAA CPC / NCEI

**Spatial coverage:** Global, 60°S-60°N

**Spatial resolution:** 8 km x 8 km (full-res) or 0.25° (regridded)

**Temporal coverage:** January 1998 to present

**Temporal resolution:** 30-minute (full-res), hourly, daily

**Access method:** Direct download from NCEI: https://www.ncei.noaa.gov/data/cmorph-high-resolution-global-precipitation-estimates/access/

**Data format:** NetCDF, raw binary

**Licence:** Open, free (NOAA CDR)

**Key variables:** Precipitation rate (mm/hr)

**How it relates to Causal Atlas:** Sub-daily precipitation for extreme event analysis (flash floods, storm impacts). Complements CHIRPS (which is daily/pentadal). Useful for testing short-lag precipitation-to-disaster causal chains.

**Python access:**
```python
import xarray as xr
ds = xr.open_dataset('pr_30min_CMORPH_V1_YYYYMMDD.nc')
```

**Sources:** https://www.ncei.noaa.gov/products/climate-data-records/precipitation-cmorph, https://climatedataguide.ucar.edu/climate-data/cmorph-cpc-morphing-technique-high-resolution-precipitation-60s-60n

---

#### 30. IMERG (GPM Integrated Multi-satellitE Retrievals)

**What it is:** NASA's state-of-the-art merged satellite precipitation product from the Global Precipitation Measurement (GPM) mission. Successor to TRMM-era products.

**Maintained by:** NASA GPM / GES DISC

**Spatial coverage:** Global, 90°S-90°N (wider than CMORPH/CHIRPS)

**Spatial resolution:** 0.1° x 0.1° (~10 km)

**Temporal coverage:** June 2000 to present (reprocessed back to TRMM era)

**Temporal resolution:** 30-minute, daily, monthly

**Access method:** GES DISC, Google Earth Engine (`NASA/GPM_L3/IMERG_V07`), Giovanni

**Data format:** HDF5, NetCDF

**Licence:** Open, free. NASA Earthdata login required.

**Key variables:** Precipitation rate, precipitation type (convective vs stratiform), quality index

**Product tiers:** Early Run (4-hr latency), Late Run (14-hr latency), Final Run (3.5-month latency, gauge-calibrated)

**Current version:** V07 (released 2024, fully reprocessed)

**How it relates to Causal Atlas:** Best available near-global, high-resolution precipitation. 0.1° resolution is finer than PRIO-GRID (0.5°) so can be cleanly aggregated. Precipitation type separation is unique and useful for distinguishing flood-causing events.

**Python access:**
```python
# Via Google Earth Engine
import ee
ee.Initialize()
imerg = ee.ImageCollection('NASA/GPM_L3/IMERG_V07')
```

**Sources:** https://gpm.nasa.gov/data/imerg, https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_V07

---

#### 31. Berkeley Earth Surface Temperature (BEST)

**What it is:** Independent analysis of land and ocean surface temperature using statistical methods designed to handle station discontinuities and inhomogeneities.

**Maintained by:** Berkeley Earth (non-profit)

**Spatial coverage:** Global land + ocean

**Spatial resolution:** 1° x 1° latitude-longitude grid

**Temporal coverage:** 1850 to present (land), 1850 to present (land+ocean)

**Temporal resolution:** Monthly

**Access method:** Direct download from https://berkeleyearth.org/data/

**Data format:** NetCDF4

**Licence:** Open (Creative Commons)

**Key variables:** Temperature anomaly (°C relative to 1951-1980 baseline)

**Note:** As of mid-2025, the 1° x 1° gridded product updates have been paused; high-resolution products available by request.

**How it relates to Causal Atlas:** Temperature anomaly as a driver for heat-health impacts, agricultural stress, and conflict. Independent from CRU TS and ERA5, useful for cross-validation.

**Python access:**
```python
import xarray as xr
ds = xr.open_dataset('Complete_TAVG_LatLong1.nc')
```

**Sources:** https://berkeleyearth.org/data/, https://essd.copernicus.org/articles/12/3469/2020/

---

#### 32. CRU TS (Climatic Research Unit Time-Series)

**What it is:** Station-based gridded monthly climate dataset, the most widely used observational climate dataset in research. Critically, its native 0.5° resolution matches PRIO-GRID exactly.

**Maintained by:** Climatic Research Unit, University of East Anglia

**Spatial coverage:** Global land areas (no ocean)

**Spatial resolution:** 0.5° x 0.5° (matches PRIO-GRID)

**Temporal coverage:** January 1901 to December 2024 (v4.09, released March 2025)

**Temporal resolution:** Monthly

**Access method:** CEDA Archive (https://catalogue.ceda.ac.uk/), AWS Open Data (https://registry.opendata.aws/wbg-cckp/), World Bank CCKP

**Data format:** NetCDF

**Licence:** Open, free (Open Government Licence for public sector information)

**Key variables:** Precipitation (pre), mean temperature (tmp), diurnal temperature range (dtr), max/min temperature (tmx/tmn), cloud cover (cld), vapour pressure (vap), wet day frequency (wet), frost day frequency (frs), potential evapotranspiration (pet)

**How it relates to Causal Atlas:** **Priority dataset** — native 0.5° resolution means zero regridding needed for PRIO-GRID. Long record (1901-present) enables historical causal analysis. PET variable directly supports drought/water balance calculations.

**Python access:**
```python
import xarray as xr
ds = xr.open_dataset('cru_ts4.09.1901.2024.tmp.dat.nc')
# Pre-aggregated to 0.5° — direct PRIO-GRID alignment
```

**Sources:** https://crudata.uea.ac.uk/cru/data/hrg/, https://catalogue.ceda.ac.uk/uuid/9cf07e92afaa405da4f40b6733f362d3/

---

#### 33. TerraClimate

**What it is:** High-resolution monthly climate and water balance dataset combining climatological normals with time-varying anomalies from CRU TS and JRA-55 reanalysis.

**Maintained by:** Climatology Lab, University of Idaho (John Abatzoglou)

**Spatial coverage:** Global land

**Spatial resolution:** ~4 km (1/24th degree)

**Temporal coverage:** 1958 to present

**Temporal resolution:** Monthly

**Access method:** Google Earth Engine (`IDAHO_EPSCOR/TERRACLIMATE`), Microsoft Planetary Computer (Zarr), THREDDS server, direct NetCDF download

**Data format:** NetCDF, Zarr (Planetary Computer)

**Licence:** Open, Creative Commons

**Key variables:** Max/min temperature, precipitation, downward surface shortwave radiation, wind speed, vapour pressure, vapour pressure deficit, snow water equivalent, runoff, actual evapotranspiration (aet), climatic water deficit (def), soil moisture, PDSI (Palmer Drought Severity Index)

**How it relates to Causal Atlas:** Climatic water deficit (def) and PDSI are pre-computed drought indicators — no need to calculate from raw climate variables. 4 km resolution is much finer than PRIO-GRID, enabling sub-grid analysis. Supports drought→agriculture→food security causal chains.

**Python access:**
```python
# Via Planetary Computer
import pystac_client
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(collections=["terraclimate"])
# Or via xarray + THREDDS
import xarray as xr
ds = xr.open_dataset('http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_terraclimate_def_1958_CurrentYear_GLOBE.nc')
```

**Sources:** https://www.climatologylab.org/terraclimate.html, https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_TERRACLIMATE

---

#### 34. SPEI Global Drought Monitor

**What it is:** Pre-computed Standardised Precipitation-Evapotranspiration Index at multiple timescales, updated monthly. SPEI captures drought severity by accounting for both precipitation and evaporative demand.

**Maintained by:** CSIC (Spanish National Research Council), Santiago Begueria and Sergio Vicente-Serrano

**Spatial coverage:** Global land

**Spatial resolution:** 1° (based on CRU TS + GPCC data)

**Temporal coverage:** 1955 to present (updated monthly with ~1 month lag)

**Temporal resolution:** Monthly, at timescales of 1, 3, 6, 12, 24, and 48 months

**Access method:** https://spei.csic.es/database.html (NetCDF download), https://spei.csic.es/map/ (interactive). Also available via Copernicus CDS.

**Data format:** NetCDF, CSV (for point time series)

**Licence:** Open, but last 4 weeks restricted to licensed users on CSIC portal. Copernicus CDS version is fully open.

**Key variables:** SPEI at 1, 3, 6, 12, 24, 48 month timescales

**How it relates to Causal Atlas:** Pre-computed drought index eliminates need to calculate from raw climate data. Multi-timescale SPEI supports testing different lag structures (e.g., SPEI-3 for agricultural drought, SPEI-12 for hydrological drought). Direct input to drought→food security→conflict causal chains.

**Python access:**
```python
import xarray as xr
ds = xr.open_dataset('spei01.nc')  # Downloaded from spei.csic.es
# Or via Copernicus CDS API (cdsapi package)
```

**Sources:** https://spei.csic.es/, https://cds.climate.copernicus.eu/datasets/derived-drought-historical-monthly

---

#### 35. Copernicus Climate Data Store (CDS) — Full Catalogue

**What it is:** One-stop shop for climate data providing access to observations, reanalyses, seasonal forecasts, and climate projections. Extends far beyond ERA5.

**Maintained by:** ECMWF / Copernicus Climate Change Service (C3S)

**Key datasets beyond ERA5:**
- ERA5-Land (enhanced land component, 9 km resolution)
- UERRA (regional European reanalysis, 5.5 km)
- Seasonal forecasts (SEAS5, multiple centres)
- CMIP6 climate projections (downscaled)
- Satellite-derived ECVs (soil moisture, sea surface temperature, fire, lake data, glaciers, etc.)
- Agroclimatic indicators (growing degree days, frost days, etc.)
- Drought indices (SPI, SPEI, soil moisture anomalies)
- Fire danger indices (FWI)

**Access method:** CDS API (`cdsapi` Python package), web interface. Free registration required.

**Data format:** NetCDF, GRIB

**Licence:** Copernicus licence — free, open, with attribution (CC BY 4.0 equivalent for most products)

**How it relates to Causal Atlas:** Single API for dozens of climate-related variables. Agroclimatic indicators and drought indices are pre-computed, saving processing effort. Seasonal forecasts enable predictive causal models.

**Python access:**
```python
pip install cdsapi
# or newer: pip install ecmwf-datastores-client
import cdsapi
c = cdsapi.Client()
c.retrieve('derived-drought-historical-monthly', {...}, 'download.nc')
```

**Sources:** https://cds.climate.copernicus.eu/, https://github.com/ecmwf/cdsapi

---

#### 36. NOAA Climate Data Online (CDO)

**What it is:** Station-based historical weather observations from a global network of weather stations. Complements gridded products by providing point-source measurements.

**Maintained by:** NOAA NCEI

**Spatial coverage:** Global (~100,000+ stations, unevenly distributed)

**Temporal coverage:** Varies by station; some back to 1700s, most from mid-1900s

**Temporal resolution:** Hourly, daily, monthly summaries

**Access method:** REST API (v2) at https://www.ncei.noaa.gov/access/services/data/v1 (token required, 5 req/sec, 10,000/day limit), web interface

**Data format:** JSON (API), CSV (download)

**Licence:** Open, free (US Government public domain)

**Key variables:** Temperature (min, max, mean), precipitation, snowfall, wind, pressure, humidity

**How it relates to Causal Atlas:** Ground-truth validation for gridded products (ERA5, CRU TS). Station density itself is a metadata variable (areas with few stations have less reliable gridded products).

**Python access:**
```python
# pyncei library
pip install pyncei
# Or direct requests
import requests
headers = {'token': 'YOUR_TOKEN'}
r = requests.get('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&...', headers=headers)
```

**Sources:** https://www.ncei.noaa.gov/cdo-web/, https://www.ncdc.noaa.gov/cdo-web/webservices/v2

---

#### 37. FLDAS (FEWS NET Land Data Assimilation System)

**What it is:** Land surface model outputs specifically designed for food security monitoring in Africa and other food-insecure regions. Uses Noah 3.6.1 land surface model driven by CHIRPS rainfall and MERRA-2 meteorology.

**Maintained by:** NASA GSFC / USGS FEWS NET

**Spatial coverage:** Global (strongest focus on Africa)

**Spatial resolution:** 0.1° x 0.1° (~10 km)

**Temporal coverage:** January 1982 to present

**Temporal resolution:** Monthly

**Access method:** Google Earth Engine (`NASA/FLDAS/NOAH01/C/GL/M/V001`), NASA GES DISC (NetCDF), USGS FEWS NET portal (http://earlywarning.usgs.gov/fews)

**Data format:** NetCDF

**Licence:** Open, free for research, education, nonprofit

**Key variables:** Soil moisture (0-10 cm, 10-40 cm, 40-100 cm, 100-200 cm), evapotranspiration, surface runoff, baseflow-groundwater runoff, soil temperature, snow cover

**How it relates to Causal Atlas:** Soil moisture is a critical mediator in drought→crop failure→food crisis causal chains. FLDAS is purpose-built for food security analysis, making it the most directly relevant land surface product for Causal Atlas.

**Python access:**
```python
# Via Google Earth Engine
import ee
fldas = ee.ImageCollection('NASA/FLDAS/NOAH01/C/GL/M/V001')
# Or via xarray from GES DISC
```

**Sources:** https://ldas.gsfc.nasa.gov/fldas, https://developers.google.com/earth-engine/datasets/catalog/NASA_FLDAS_NOAH01_C_GL_M_V001

---

### Conflict, Security, and Governance

#### 38. Global Terrorism Database (GTD)

**What it is:** The most comprehensive unclassified database of terrorist attacks worldwide. Contains 200,000+ events from 1970 to 2020.

**Maintained by:** START (National Consortium for the Study of Terrorism and Responses to Terrorism), University of Maryland

**Spatial coverage:** Global

**Temporal coverage:** 1970-2020 (note: data collection methodology changed significantly in 1998, 2008, and 2012)

**Access method:** Request access via https://www.start.umd.edu/download-global-terrorism-database. As of 2025, access requires registration and personal information submission. Also available on Kaggle for older versions.

**Data format:** CSV/Excel

**Licence:** Academic use; requires registration and agreement to terms

**Key variables:** Date, country, city, latitude/longitude, attack type, target type, weapon type, group name, fatalities, injuries, property damage

**Caveats:** Dataset is no longer actively updated (closed as of ~2022). Methodology changes at 1998 and 2012 create structural breaks in the time series.

**How it relates to Causal Atlas:** Geocoded terrorism events enable spatial analysis of terrorism→economic disruption, terrorism→displacement, and governance→terrorism causal chains. Complements UCDP/ACLED with specific terrorism-focused coding.

**Python access:**
```python
import pandas as pd
gtd = pd.read_csv('globalterrorismdb.csv', encoding='latin-1')
```

**Sources:** https://www.start.umd.edu/research-projects/global-terrorism-database-gtd

---

#### 39. SIPRI Military Expenditure Database (MILEX)

**What it is:** Consistent time series of military spending by country, enabling cross-national and temporal comparison of defence burden.

**Maintained by:** Stockholm International Peace Research Institute (SIPRI)

**Spatial coverage:** Global (173 countries)

**Temporal coverage:** 1949-2024

**Temporal resolution:** Annual

**Access method:** Web interface and Excel download at https://milex.sipri.org/, also available via World Bank API (indicator MS.MIL.XPND.CD)

**Data format:** Excel, CSV

**Licence:** Open access for non-commercial use, with citation required

**Key variables:** Military expenditure in constant USD, current USD, share of GDP, share of government spending, per capita

**How it relates to Causal Atlas:** Military spending as a proxy for security environment and state capacity. Supports arms race→conflict, military spending→development trade-off causal chains.

**Python access:**
```python
# Via World Bank API
import wbgapi as wb
df = wb.data.DataFrame('MS.MIL.XPND.CD', economy='all')
# Or via milRex R package (no direct Python equivalent; download Excel)
```

**Sources:** https://www.sipri.org/databases/milex

---

#### 40. SIPRI Arms Transfers Database

**What it is:** Records international transfers of major conventional weapons using the Trend Indicator Value (TIV) methodology, which measures military resource transfer rather than financial value.

**Maintained by:** SIPRI

**Spatial coverage:** Global

**Temporal coverage:** 1950-2025 (updated March 2026)

**Temporal resolution:** Annual

**Access method:** Web interface at https://armstransfers.sipri.org/, CSV download via "Download as CSV" button on Transfer Register page

**Data format:** CSV

**Licence:** Open access for non-commercial use

**Key variables:** Supplier, recipient, weapon description, weapon designation, TIV (trend indicator value), order date, delivery years, number ordered/delivered

**Caveats:** TIV values should NOT be compared to GDP or financial figures. Best used for trend analysis only.

**How it relates to Causal Atlas:** Arms flows as leading indicators of conflict escalation. Supports arms imports→conflict onset/intensity causal chains.

**Python access:**
```python
import pandas as pd
df = pd.read_csv('trade-register.csv')
```

**Sources:** https://www.sipri.org/databases/armstransfers

---

#### 41. Fragile States Index (FSI)

**What it is:** Annual index ranking 179 countries on 12 indicators of state fragility across social, economic, and political dimensions.

**Maintained by:** Fund for Peace

**Spatial coverage:** Global (179 countries)

**Temporal coverage:** 2006 to present

**Temporal resolution:** Annual

**Access method:** Excel download from https://fragilestatesindex.org/global-data/, also available on Mendeley Data (2006-2024)

**Data format:** Excel, CSV

**Licence:** Open for research use

**Key variables:** 12 sub-indicators: Security Apparatus, Factionalized Elites, Group Grievance, Economic Decline, Uneven Development, Human Flight, State Legitimacy, Public Services, Human Rights, Demographic Pressures, Refugees/IDPs, External Intervention. Total score (0-120, higher = more fragile).

**How it relates to Causal Atlas:** Composite fragility score as both an outcome variable (what drives fragility?) and a contextual variable (does fragility moderate the climate→conflict link?). Annual resolution limits temporal analysis but useful for cross-sectional comparison.

**Python access:**
```python
import pandas as pd
fsi = pd.read_excel('fsi-2024.xlsx')
```

**Sources:** https://fragilestatesindex.org/, https://data.mendeley.com/datasets/bhbcjtgjdm/1

---

#### 42. Polity5

**What it is:** The most widely used dataset for measuring regime type on a -10 (full autocracy) to +10 (full democracy) scale, based on codified characteristics of political authority.

**Maintained by:** Center for Systemic Peace

**Spatial coverage:** Global (167 countries with pop > 500,000)

**Temporal coverage:** 1800-2018

**Temporal resolution:** Annual (with exact dates for regime transitions)

**Access method:** Download from http://www.systemicpeace.org/inscrdata.html

**Data format:** SPSS (.sav), Excel (.xls)

**Licence:** Free for academic use

**Key variables:** polity2 (combined polity score, -10 to +10), democ (democracy score), autoc (autocracy score), durable (regime durability in years), xconst (executive constraints), polcomp (political competition)

**Caveats:** Dataset ends at 2018 and is unlikely to be updated further. V-Dem is the recommended successor for ongoing analysis.

**How it relates to Causal Atlas:** Regime type as a moderator of climate→conflict and economic→conflict causal chains. The "anocracy" hypothesis (intermediate polity scores correlate with higher conflict risk) is testable.

**Python access:**
```python
import pandas as pd
polity = pd.read_excel('p5v2018.xls')
# Or via democracyData R package
```

**Sources:** https://www.systemicpeace.org/polityproject.html

---

#### 43. Freedom House Freedom in the World

**What it is:** Annual assessment of political rights and civil liberties for every country and select territories, using a standardised methodology since 1972.

**Maintained by:** Freedom House

**Spatial coverage:** Global (195 countries + 15 territories)

**Temporal coverage:** 1972 to present

**Temporal resolution:** Annual

**Access method:** Excel download from https://freedomhouse.org/report/freedom-world (direct URL: https://freedomhouse.org/sites/default/files/2025-02/Country_and_Territory_Ratings_and_Statuses_FIW_1973-2024.xlsx)

**Data format:** Excel

**Licence:** Open for research use with attribution

**Key variables:** Political Rights score (1-7, lower = more free), Civil Liberties score (1-7), Status (Free/Partly Free/Not Free), Aggregate score (0-100, 25 indicators)

**How it relates to Causal Atlas:** Civil liberties and political rights as contextual variables that moderate other causal chains (e.g., press freedom → data quality, political repression → protest → conflict).

**Python access:**
```python
import pandas as pd
fh = pd.read_excel('Country_and_Territory_Ratings_and_Statuses_FIW_1973-2024.xlsx')
```

**Sources:** https://freedomhouse.org/report/freedom-world

---

#### 44. Correlates of War (COW)

**What it is:** The foundational quantitative international relations dataset, providing standardised data on interstate wars, militarised disputes, alliances, trade, and state system membership since 1816.

**Maintained by:** Correlates of War Project (consortium of universities)

**Spatial coverage:** Global (all state system members)

**Temporal coverage:** 1816-2014 (varies by sub-dataset)

**Key sub-datasets:**
| Dataset | Coverage | Unit |
|---------|----------|------|
| Interstate Wars (v4.0) | 1816-2010 | War-dyad-year |
| Militarised Interstate Disputes (v5.0) | 1816-2014 | Dispute-dyad-year |
| Bilateral Trade (v4.0) | 1870-2014 | Dyad-year |
| Alliances (v4.1) | 1816-2012 | Alliance-year |
| National Material Capabilities (v6.0) | 1816-2016 | Country-year |

**Access method:** Download from https://correlatesofwar.org/data-sets/

**Data format:** CSV (zipped)

**Licence:** Free for academic use; no redistribution without permission

**How it relates to Causal Atlas:** The National Material Capabilities (CINC scores) provide a standardised measure of state power. Trade data supports economic interdependence→peace/conflict analysis. MID data complements UCDP for pre-2014 analysis.

**Python access:**
```python
import pandas as pd
mids = pd.read_csv('MIDA_5_0.csv')
```

**Sources:** https://correlatesofwar.org/data-sets/

---

#### 45. REIGN (Rulers, Elections, and Irregular Governance)

**What it is:** Monthly leader-level dataset covering leadership tenures, regime types, elections, and irregular governance events (coups, coup attempts) for all independent countries.

**Maintained by:** One Earth Future Foundation (OEF Research)

**Spatial coverage:** Global (201 countries)

**Temporal coverage:** January 1950 to present (updated monthly)

**Temporal resolution:** Monthly (unique among governance datasets)

**Access method:** Direct CSV download from https://oefdatascience.github.io/REIGN.github.io/menu/reign_current.html

**Data format:** CSV

**Licence:** Open

**Key variables:** Leader name, leader gender, leader age, regime type (6 categories), government type, election type, election date, anticipated election, irregular leader change, coup attempt

**How it relates to Causal Atlas:** Monthly temporal resolution aligns with Causal Atlas's primary time unit. Leadership changes and elections as potential triggers or moderators of conflict, economic disruption, and policy change. Coup events are a key outcome variable for governance instability analysis.

**Python access:**
```python
import pandas as pd
reign = pd.read_csv('REIGN_current.csv')
```

**Sources:** https://oefdatascience.github.io/REIGN.github.io/, https://www.oefresearch.org/datasets/reign

---

#### 46. Mass Mobilization Project

**What it is:** Dataset of protest events against governments, coding protester demands, government responses, protest location, and protester identities.

**Maintained by:** David Clark (Binghamton University) and Patrick Regan (University of Notre Dame)

**Spatial coverage:** Global (162 countries)

**Temporal coverage:** 1990-2020

**Temporal resolution:** Event-level (daily dates)

**Access method:** Harvard Dataverse: https://dataverse.harvard.edu/dataverse/MMdata

**Data format:** CSV, Stata

**Licence:** Open academic use

**Key variables:** Country, date, city, protest issue (14 categories), number of protesters, government response type (7 categories: ignore, accommodation, arrests, beatings, shootings, killings, crowd dispersal)

**Caveats:** Data collection may not continue beyond 2020. Related but separate: Mass Mobilization in Autocracies Database (MMAD) covers city-level events with daily resolution.

**How it relates to Causal Atlas:** Protest events as outcome of economic stress, food price shocks, or governance failures. Government response type enables analysis of repression→escalation dynamics.

**Python access:**
```python
import pandas as pd
mm = pd.read_csv('Mass-Mobilization-Protest-Data.csv')
```

**Sources:** https://massmobilization.github.io/, https://dataverse.harvard.edu/dataverse/MMdata

---

#### 47. SCAD (Social Conflict Analysis Database)

**What it is:** Event-level database of social conflict in Africa, Mexico, Central America, and the Caribbean, including protests, riots, strikes, inter-communal violence, and government violence against civilians — event types often missed by UCDP/ACLED.

**Maintained by:** Cullen Hendrix and Idean Salehyan (originally at UT Austin Strauss Center, now at University of Denver)

**Spatial coverage:** All of Africa, Mexico, Central America, Caribbean (countries with pop > 1 million)

**Temporal coverage:** 1990-2017

**Temporal resolution:** Event-level (daily dates)

**Access method:** Download from https://www.strausscenter.org/ccaps-research-areas/social-conflict/database/ or https://korbel.du.edu/sie/social-conflict-analysis-database/

**Data format:** CSV, Stata

**Licence:** Open for academic use

**Key variables:** Event type (9 categories), location (lat/lon for many events), actors, targets, issues, government response, fatalities, duration

**How it relates to Causal Atlas:** Captures lower-intensity social conflict (strikes, protests, communal clashes) that UCDP misses. Particularly strong for African social conflict analysis. Complements ACLED for pre-2018 data.

**Python access:**
```python
import pandas as pd
scad = pd.read_csv('SCAD_2017.csv')
```

**Sources:** https://www.strausscenter.org/ccaps-research-areas/social-conflict/database/

---

### Population, Migration, and Displacement

#### 48. Meta (Facebook) Data for Good — High Resolution Population Density Maps

**What it is:** Population density maps using machine learning on high-resolution satellite imagery to identify buildings, with census population counts allocated to detected settlements. Also provides movement range maps and disaster displacement maps.

**Maintained by:** Meta / CIESIN Columbia University

**Spatial coverage:** Global (~200 countries)

**Spatial resolution:** ~30 m (building footprints), aggregated to various grid sizes

**Temporal coverage:** Baseline maps (various years); movement data from 2020+

**Access method:** Humanitarian Data Exchange (HDX): https://data.humdata.org/organization/meta, AWS Open Data: https://registry.opendata.aws/dataforgood-fb-hrsl/

**Data format:** GeoTIFF, CSV

**Licence:** Creative Commons Attribution (CC BY). Not derived from Facebook user data.

**Key variables:** Population count per grid cell, demographic breakdowns (age, sex), movement range (% change from baseline), crisis displacement estimates

**How it relates to Causal Atlas:** Highest-resolution freely available population data. Enables precise population-at-risk calculations for any hazard event. Movement data supports displacement tracking after disasters.

**Python access:**
```python
import rasterio
# Download from HDX or AWS, then:
with rasterio.open('population_density.tif') as src:
    pop = src.read(1)
```

**Sources:** https://dataforgood.facebook.com/dfg/tools/high-resolution-population-density-maps, https://data.humdata.org/organization/meta

---

#### 49. UNHCR Microdata Library

**What it is:** Anonymised individual-level and household-level survey data from refugee and displaced population assessments, including intentions surveys, livelihoods assessments, and protection monitoring.

**Maintained by:** UNHCR

**Spatial coverage:** 60+ countries (wherever UNHCR operates)

**Temporal coverage:** Various (most surveys from 2015 onwards)

**Access method:** https://microdata.unhcr.org/ — "public use" datasets freely downloadable; "licensed use" datasets require application

**Data format:** CSV, Stata, SPSS

**Licence:** Public Use (CC-equivalent) or Licensed Use (application required)

**Key variables:** Varies by survey; typically includes demographics, displacement history, shelter type, food security, livelihoods, intentions (return, local integration, resettlement), protection concerns

**Current holdings:** 1,049+ datasets (as of March 2026)

**How it relates to Causal Atlas:** Ground-truth data on displaced populations, complementing aggregate UNHCR statistics. Intentions data supports predictive modelling of return/onward movement. Can validate displacement estimates from other sources.

**Python access:**
```python
import pandas as pd
# Download datasets from microdata.unhcr.org, then:
survey = pd.read_csv('unhcr_survey_data.csv')
```

**Sources:** https://microdata.unhcr.org/

---

#### 50. IOM Displacement Tracking Matrix (DTM)

**What it is:** Systematic approach to tracking and monitoring displacement, providing regularly updated displacement figures, flow monitoring, and multi-sectoral needs assessments.

**Maintained by:** International Organization for Migration (IOM)

**Spatial coverage:** 90+ countries

**Temporal coverage:** Varies by country (most operations from 2014+)

**Access method:** REST API v3 at https://dtm.iom.int/data-and-analysis/dtm-api (requires Developer Portal account and subscription key), also on HDX

**Data format:** JSON (API), CSV/Excel (downloads)

**Licence:** Open (humanitarian data sharing)

**Key variables:** IDP figures by admin-1 and admin-2 areas, displacement site characteristics (shelter type, population, services), flow monitoring (movement routes, profiles of people on the move)

**How it relates to Causal Atlas:** Subnational displacement data at admin-1/admin-2 level enables spatial analysis of displacement drivers. Flow monitoring data supports origin-destination analysis for conflict→displacement and disaster→displacement chains.

**Python access:**
```python
import requests
headers = {'Ocp-Apim-Subscription-Key': 'YOUR_KEY'}
r = requests.get('https://dtm.iom.int/api/v3/...', headers=headers)
```

**Sources:** https://dtm.iom.int/data-and-analysis/dtm-api

---

#### 51. GRID3 (Geo-Referenced Infrastructure and Demographic Data for Development)

**What it is:** High-resolution settlement data for sub-Saharan Africa using machine learning on satellite imagery to detect and delineate settlements at ~100 m resolution.

**Maintained by:** CIESIN Columbia University, Flowminder, WorldPop, UNFPA

**Spatial coverage:** 50 countries in sub-Saharan Africa (15 million+ settlements mapped)

**Spatial resolution:** ~100 m (3 arc-seconds)

**Access method:** GRID3 Data Hub: https://data.grid3.org/datasets, HDX

**Data format:** Geodatabase (polygon + point centroids), GeoJSON

**Licence:** Open (CC BY 4.0)

**Key variables:** Settlement extents (polygons), settlement centroids (points), settlement type classification, building footprints (for some countries)

**How it relates to Causal Atlas:** Enables precise identification of populated areas for exposure analysis. Settlement patterns can serve as proxies for urbanisation dynamics. Building density changes over time could indicate displacement or growth.

**Python access:**
```python
import geopandas as gpd
settlements = gpd.read_file('GRID3_NGA_settlement_extents.gpkg')
```

**Sources:** https://grid3.org/, https://data.grid3.org/datasets

---

#### 52. LandScan

**What it is:** Global population distribution database representing a 24-hour average (ambient) population at ~1 km resolution, using multi-source geospatial data fusion.

**Maintained by:** Oak Ridge National Laboratory (ORNL) / National Geospatial-Intelligence Agency (NGA)

**Spatial coverage:** Global

**Spatial resolution:** 30 arc-seconds (~1 km)

**Temporal coverage:** 2000-2023 (annual releases)

**Access method:** Free download from https://landscan.ornl.gov/ (registration required: email, work sector). Also on Google Earth Engine (community dataset).

**Data format:** GeoTIFF

**Licence:** Free and unrestricted as of 2024 (previously restricted). Public domain.

**Key variables:** Ambient (24-hour average) population count per cell. LandScan HD also available at ~100 m for select areas.

**How it relates to Causal Atlas:** 1 km ambient population is ideal for exposure calculations (people in hazard zones at any time of day). Annual time series enables population change tracking as a proxy for displacement/migration.

**Python access:**
```python
import rasterio
with rasterio.open('LandScan_Global_2023.tif') as src:
    pop = src.read(1)
```

**Sources:** https://landscan.ornl.gov/, https://www.nature.com/articles/s41597-025-04817-z

---

#### 53. GHS-POP (Global Human Settlement Population Grid)

**What it is:** Disaggregated population grids at multiple epochs from 1975 to 2030 (including projections), produced by the European Commission's Joint Research Centre using census data and built-up area detection.

**Maintained by:** European Commission JRC (GHSL project)

**Spatial coverage:** Global

**Spatial resolution:** 100 m, 1 km (user choice)

**Temporal epochs:** 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025 (projected), 2030 (projected)

**Access method:** GHSL portal: https://human-settlement.emergency.copernicus.eu/ghs_pop2023.php, Google Earth Engine (`JRC/GHSL/P2023A/GHS_POP`), NASA SEDAC

**Data format:** GeoTIFF

**Licence:** Open, free (CC BY 4.0)

**Key variables:** Residential population count per cell (number of inhabitants)

**How it relates to Causal Atlas:** Multi-epoch population enables historical population change analysis (1975-2020). 100 m resolution is the finest freely available global population grid. Population projections (2025, 2030) support forward-looking analysis.

**Python access:**
```python
# Via Google Earth Engine
import ee
ghs = ee.ImageCollection('JRC/GHSL/P2023A/GHS_POP')
# Or download GeoTIFF and use rasterio
```

**Sources:** https://human-settlement.emergency.copernicus.eu/ghs_pop2023.php

---

### Economic and Trade

#### 54. Nighttime Lights as Economic Indicators

**What it is:** Pre-computed economic indicators derived from nighttime light satellite imagery (DMSP-OLS 1992-2013 and VIIRS 2012-present), used as GDP proxies especially for countries with poor statistical capacity.

**Key datasets:**
- **VIIRS nighttime lights composites** (see nightlights.md for raw data)
- **Henderson, Storeygard & Weil GDP estimates** — derived subnational GDP from lights
- **World Bank quarterly GDP from lights** — experimental quarterly GDP estimates
- **Lessmann & Seidel subnational GDP** — 2005 cross-section at 1° resolution

**Spatial resolution:** Varies; VIIRS is ~500 m, most derived products are at admin-1 or 1° level

**Relationship to raw nightlights:** A 1% change in quarterly GDP associates with ~1.55% change in nighttime light intensity in developing countries.

**How it relates to Causal Atlas:** Subnational GDP proxy where official statistics are unavailable or unreliable. Monthly VIIRS composites enable sub-annual economic tracking. Conflict→economic disruption chains can be tested using light intensity changes around conflict events.

**Sources:** https://www.pnas.org/doi/10.1073/pnas.1017031108, https://blogs.worldbank.org/en/developmenttalk/measuring-quarterly-economic-growth-outer-space

---

#### 55. Observatory of Economic Complexity (OEC)

**What it is:** Platform providing international trade flow data with visualisations, based on UN COMTRADE and national customs data, using HS and SITC product classifications.

**Maintained by:** OEC (oec.world), originally from MIT Media Lab

**Spatial coverage:** Global (200+ countries)

**Temporal coverage:** 1995 to present (HS classification), 1962 to present (SITC)

**Temporal resolution:** Annual, with some monthly/quarterly for premium users

**Access method:** REST API at https://api-v2.oec.world (Tesseract API). Free tier for historical data; Pro/Premium tiers for latest data, subnational, and high-volume access.

**Data format:** JSON (API)

**Licence:** Free tier available; paid tiers for advanced access

**Key variables:** Export value, import value, by product (HS 2/4/6 digit), bilateral trade flows, Economic Complexity Index (ECI), Product Complexity Index (PCI)

**How it relates to Causal Atlas:** Trade flow disruptions as both causes and effects in causal chains. Commodity-specific trade (e.g., wheat imports) directly relevant to food security analysis. ECI as a structural economic indicator.

**Python access:**
```python
import requests
# Free tier — historical data
r = requests.get('https://api-v2.oec.world/tesseract/data?cube=trade_i_baci_a_92&...')
# API token required for authenticated endpoints
```

**Sources:** https://oec.world/en, https://oec.world/en/resources/api

---

#### 56. Global Trade Alert

**What it is:** Database of trade policy interventions (subsidies, tariffs, import bans, export restrictions, etc.) implemented by governments since the 2008 financial crisis. Tracks 60+ types of policy changes.

**Maintained by:** Global Trade Alert / University of St. Gallen

**Spatial coverage:** Global (all WTO members and many non-members)

**Temporal coverage:** November 2008 to present

**Access method:** REST API at https://api.globaltradealert.org/api/v1/data/ (API key required, POST requests), Data Center web interface

**Data format:** JSON (API), Excel/CSV (Data Center exports)

**Licence:** Open for research; API key required

**Key variables:** Implementing jurisdiction, affected jurisdiction, affected products (HS codes), intervention type (60+ categories), implementation date, assessment (liberalising/harmful/ambiguous), affected trade flows

**How it relates to Causal Atlas:** Trade policy shocks (export bans on food, import tariffs) as drivers of food price changes and supply disruptions. Supports policy→trade→food security causal chains.

**Python access:**
```python
import requests
headers = {'Authorization': 'Bearer YOUR_API_KEY'}
r = requests.post('https://api.globaltradealert.org/api/v1/data/', json={...}, headers=headers)
```

**Sources:** https://globaltradealert.org/, https://globaltradealert.org/api-access

---

#### 57. IMF World Economic Outlook (WEO)

**What it is:** Biannual publication with GDP, inflation, unemployment, fiscal, and balance-of-payments data and 5-year projections for 196 countries.

**Maintained by:** International Monetary Fund

**Spatial coverage:** Global (196 countries + country groups)

**Temporal coverage:** 1980 to present + 5-year projections

**Temporal resolution:** Annual

**Access method:** SDMX API at https://data.imf.org/en/datasets/IMF.RES:WEO, web download, `weo` Python package

**Data format:** SDMX (API), Excel/CSV (download)

**Licence:** Open (IMF Copyright/Terms of Use)

**Key variables:** GDP (nominal, PPP, per capita), GDP growth rate, inflation (CPI), unemployment, government revenue/expenditure, current account balance, population

**How it relates to Causal Atlas:** Macroeconomic context for all causal chains. GDP growth and inflation as both drivers and outcomes. Projections enable forward-looking causal analysis.

**Python access:**
```python
pip install weo
import weo
w = weo.download(2025, 1)  # April 2025 release
df = weo.WEO(w).dataframe()
```

**Sources:** https://data.imf.org/en/datasets/IMF.RES:WEO, https://pypi.org/project/weo/

---

#### 58. Commodity Price Indices

**What it is:** Monthly commodity price data covering energy, agriculture, metals, and fertilisers.

**Key sources:**

| Source | Coverage | Access |
|--------|----------|--------|
| **IMF Primary Commodity Prices (PCPS)** | 1957-present, 68 commodities, monthly | SDMX API: https://data.imf.org/Datasets/PCPS |
| **World Bank Pink Sheet** | 1960-present, 72 commodities, monthly | Excel: https://www.worldbank.org/commodities |
| **FAO Food Price Index** | 1990-present, monthly | https://www.fao.org/worldfoodsituation/foodpricesindex/ |

**Data format:** Excel, CSV, SDMX (IMF)

**Licence:** Open

**How it relates to Causal Atlas:** Food and fuel commodity prices as mediators in climate→food security→conflict chains. Wheat, maize, and rice prices are particularly relevant for food crisis analysis. Oil price shocks affect transportation and input costs.

**Python access:**
```python
# IMF PCPS via SDMX
from pandasdmx import Request
imf = Request('IMF')
data = imf.data('PCPS')

# World Bank Pink Sheet
import pandas as pd
pink = pd.read_excel('CMO-Pink-Sheet.xlsx', sheet_name='Monthly Prices')
```

**Sources:** https://data.imf.org/Datasets/PCPS, https://www.worldbank.org/commodities

---

#### 59. LSMS (Living Standards Measurement Study)

**What it is:** Multi-topic household survey programme providing detailed microdata on consumption, income, agriculture, health, education, and labour, with GPS coordinates for many surveys.

**Maintained by:** World Bank

**Spatial coverage:** 40+ countries (strongest in Sub-Saharan Africa and South Asia)

**Temporal coverage:** 1980 to present (survey-specific)

**Access method:** World Bank Microdata Catalog: https://microdata.worldbank.org/index.php/collections/lsms

**Data format:** CSV, Stata (.dta), SPSS

**Licence:** Open access (most surveys); some require application

**Key variables:** Household consumption/expenditure, income, agricultural production (yields, inputs, land), food security, GPS coordinates (displaced for privacy), anthropometrics, education, health

**LSMS-ISA sub-programme:** Integrated Surveys on Agriculture in 8 Sub-Saharan African countries with panel data and GPS-located plots.

**How it relates to Causal Atlas:** Ground-truth household welfare data for validating macro-level causal claims. GPS-located agricultural data supports climate→crop yield→household welfare chains. Panel structure enables within-household causal inference.

**Python access:**
```python
import pandas as pd
# Download from World Bank Microdata Catalog, then:
hh = pd.read_stata('household_data.dta')
```

**Sources:** https://www.worldbank.org/en/programs/lsms, https://microdata.worldbank.org/index.php/collections/lsms

---

### Health (Beyond WHO GHO)

#### 60. Global.health

**What it is:** Open-source epidemiological data platform providing anonymised line-list case data for disease outbreaks, built on MongoDB/Node.js/Python.

**Maintained by:** Global.health initiative (academic consortium)

**Spatial coverage:** Global (100+ countries for COVID-19; expanding to other diseases)

**Temporal coverage:** 2020 to present (COVID-19); expanding

**Access method:** Web platform at https://global.health/, API access, GitHub repositories

**Data format:** JSON (API), CSV (exports)

**Licence:** Open source (CC BY 4.0 for data)

**Key variables:** Case demographics (age, sex), location (country, admin-1), dates (symptom onset, confirmation, outcome), outcome (recovered, died), travel history

**Current holdings:** 100 million+ de-identified records

**How it relates to Causal Atlas:** Line-list disease data for epidemic→displacement, epidemic→economic disruption chains. Spatio-temporal disease spread patterns can be tested against climate, mobility, and infrastructure variables.

**Python access:**
```python
# API access — check global.health for current endpoints
import requests
r = requests.get('https://data.global.health/api/...')
```

**Sources:** https://global.health/

---

#### 61. Africa CDC Disease Surveillance

**What it is:** Continental disease surveillance system producing weekly Epidemic Intelligence Reports covering priority diseases and public health events across Africa.

**Maintained by:** Africa Centres for Disease Control and Prevention

**Spatial coverage:** 55 African Union member states

**Temporal coverage:** 2017 to present

**Access method:** PDF reports downloadable from https://africacdc.org/resources/. Central Data Repository (CDR) launched January 2026 for structured data access.

**Data format:** PDF (weekly reports); structured data via CDR (new)

**Licence:** Open (institutional reports)

**Key variables:** Disease event counts by country, epidemiological week, case fatality rates, response status

**Caveats:** Historically PDF-only, limiting programmatic access. CDR should improve this but is still new.

**How it relates to Causal Atlas:** Africa-specific disease surveillance complements WHO GHO with regional detail. Supports climate→disease, conflict→health system disruption→outbreak causal chains in Africa.

**Sources:** https://africacdc.org/

---

#### 62. DHS (Demographic and Health Surveys)

**What it is:** Nationally representative household surveys providing comparable health and population data across developing countries, with GPS-located survey clusters.

**Maintained by:** ICF International, funded by USAID

**Spatial coverage:** 90+ countries (strongest in Sub-Saharan Africa and South Asia)

**Temporal coverage:** 1984 to present (350+ surveys)

**Access method:** Registration at https://dhsprogram.com/data/ (free for academic use). GPS datasets require additional authorisation. API for aggregate indicators: https://api.dhsprogram.com/

**Data format:** Stata, SPSS, flat ASCII (microdata); Shapefile (GPS clusters)

**Licence:** Free for registered users; no redistribution

**Key variables:** Child mortality, malnutrition (stunting, wasting), vaccination coverage, maternal health, fertility, HIV prevalence, water/sanitation access, household wealth index, GPS cluster locations (displaced: 2 km urban, 5-10 km rural)

**Spatial Data Repository:** https://spatialdata.dhsprogram.com/ provides pre-interpolated surfaces of key indicators

**How it relates to Causal Atlas:** GPS-located health indicators enable spatial analysis of health outcomes against environmental and conflict predictors. Wealth index as a subnational economic proxy. Multiple survey rounds per country enable temporal analysis.

**Python access:**
```python
# DHS API for aggregate indicators
import requests
r = requests.get('https://api.dhsprogram.com/rest/dhs/data?indicatorIds=CM_ECMR_C_NNR&countryIds=ET')
# For microdata: download Stata files and use pandas
import pandas as pd
dhs = pd.read_stata('ETBR71FL.DTA')
```

**Sources:** https://dhsprogram.com/, https://spatialdata.dhsprogram.com/

---

#### 63. MICS (Multiple Indicator Cluster Surveys)

**What it is:** UNICEF's global household survey programme collecting data on child and maternal wellbeing, comparable to DHS but with broader country coverage including middle-income and some high-income countries.

**Maintained by:** UNICEF

**Spatial coverage:** 120+ countries (400+ surveys completed)

**Temporal coverage:** 1995 to present (6 rounds: MICS1 through MICS6)

**Access method:** Registration at https://mics.unicef.org/ (free, approved within 1-2 days). GPS data requires separate request from national partners.

**Data format:** SPSS, CSV

**Licence:** Free for registered researchers

**Key variables:** Similar to DHS: child mortality, nutrition, immunisation, education, water/sanitation, child protection, plus early childhood development, child discipline, child labour

**GPS displacement:** Urban clusters displaced up to 2 km, rural clusters up to 5-10 km

**How it relates to Causal Atlas:** Complements DHS with additional countries and time points. Child wellbeing indicators as outcome variables for conflict→child health, climate→water quality→health chains.

**Sources:** https://mics.unicef.org/

---

#### 64. Malaria Atlas Project (MAP)

**What it is:** Gridded maps of malaria parasite prevalence, incidence, and related metrics produced using geostatistical modelling of survey data and environmental covariates.

**Maintained by:** Malaria Atlas Project, University of Oxford / Curtin University

**Spatial coverage:** Global (focus on malaria-endemic regions: Sub-Saharan Africa, South/Southeast Asia, Latin America)

**Spatial resolution:** 5 km (for modelled surfaces)

**Temporal coverage:** 2000 to present (annual modelled surfaces)

**Access method:** Data portal: https://data.malariaatlas.org/, R package `malariaAtlas`. No official Python package; download rasters and process with Python.

**Data format:** GeoTIFF (rasters), CSV (survey data)

**Licence:** Open (CC BY 3.0)

**Key variables:** Plasmodium falciparum parasite rate (PfPR), P. vivax parasite rate (PvPR), malaria incidence, ITN (insecticide-treated net) coverage, indoor residual spraying coverage, temperature suitability index

**How it relates to Causal Atlas:** Malaria as an outcome of climate (temperature, rainfall) and intervention (bed nets, spraying) variables. Supports climate→malaria transmission, conflict→health system collapse→malaria resurgence chains.

**Python access:**
```python
# Download GeoTIFFs from data.malariaatlas.org, then:
import rasterio
with rasterio.open('PfPR_2020.tif') as src:
    malaria = src.read(1)
```

**Sources:** https://malariaatlas.org/, https://data.malariaatlas.org/

---

#### 65. IHME Global Burden of Disease (GBD)

**What it is:** Comprehensive subnational health metrics covering 292 causes of death, 375 diseases/injuries, and 88 risk factors for 204 countries and 660 subnational locations.

**Maintained by:** Institute for Health Metrics and Evaluation (IHME), University of Washington

**Spatial coverage:** Global (204 countries, 660 subnational units)

**Temporal coverage:** 1990-2023 (GBD 2023)

**Access method:** GBD Results Tool: https://www.healthdata.org/data-tools-practices/interactive-visuals/gbd-results (registration required). CSV download.

**Data format:** CSV

**Licence:** Free for non-commercial use (IHME User Agreement)

**Key variables:** Deaths, DALYs, YLLs, YLDs, prevalence, incidence — by cause, age, sex, year, location. Risk factor attribution (e.g., deaths attributable to air pollution, malnutrition, unsafe water).

**How it relates to Causal Atlas:** Subnational disease burden as an outcome variable for environmental, economic, and conflict exposures. Risk factor attribution data directly supports causal analysis (e.g., pollution→respiratory disease burden, malnutrition→child mortality).

**Python access:**
```python
# Download CSV from GBD Results Tool, then:
import pandas as pd
gbd = pd.read_csv('IHME-GBD_2023_DATA.csv')
```

**Sources:** https://ghdx.healthdata.org/gbd-2023, https://www.healthdata.org/data-tools-practices/interactive-visuals/gbd-results

---

### Land Use and Environment

#### 66. ESA CCI Land Cover

**What it is:** Annual global land cover maps at 300 m resolution using 22 UN FAO LCCS classes, derived from satellite multi-spectral imagery.

**Maintained by:** ESA Climate Change Initiative / Copernicus Climate Change Service (C3S)

**Spatial coverage:** Global

**Spatial resolution:** 300 m

**Temporal coverage:** 1992-2022 (annual maps)

**Access method:** CDS (Copernicus Climate Data Store), ESA CCI viewer: https://maps.elie.ucl.ac.be/CCI/viewer/, Google Earth Engine (`projects/sat-io/open-datasets/ESA/C3S-LC-L4-LCCS`)

**Data format:** NetCDF, GeoTIFF

**Licence:** Open (Copernicus licence, CC BY 4.0 equivalent)

**Key variables:** 22 land cover classes (cropland, forest types, grassland, wetland, urban, bare, water, ice/snow), transition maps between years

**How it relates to Causal Atlas:** 30-year land cover change enables analysis of deforestation→climate feedback, agricultural expansion→conflict, urbanisation→environmental stress chains. Transition maps directly show year-over-year changes.

**Python access:**
```python
# Via Google Earth Engine
import ee
cci = ee.Image('projects/sat-io/open-datasets/ESA/C3S-LC-L4-LCCS/2022')
# Or via CDS API
import cdsapi
c = cdsapi.Client()
c.retrieve('satellite-land-cover', {...}, 'download.nc')
```

**Sources:** https://www.esa-landcover-cci.org/, https://climate.esa.int/en/projects/land-cover/

---

#### 67. MODIS Land Cover (MCD12Q1)

**What it is:** Annual global land cover classification at 500 m resolution using supervised classification of MODIS reflectance data, with multiple classification schemes.

**Maintained by:** NASA LP DAAC

**Spatial coverage:** Global

**Spatial resolution:** 500 m

**Temporal coverage:** 2001-2024 (annual)

**Access method:** Google Earth Engine (`MODIS/061/MCD12Q1`), NASA LP DAAC, USGS EarthExplorer, Zenodo (COG format mosaics)

**Data format:** HDF4 (native), GeoTIFF (processed), Cloud-Optimised GeoTIFF (Zenodo)

**Licence:** Open (NASA data policy)

**Key variables:** Land cover type (IGBP: 17 classes, UMD: 15 classes, LAI: 11 classes), land cover confidence, quality assessment

**How it relates to Causal Atlas:** Complements ESA CCI with different classification and higher spatial resolution. IGBP classification is widely used in climate models. Annual change detection at 500 m enables sub-PRIO-GRID analysis.

**Python access:**
```python
import ee
modis_lc = ee.ImageCollection('MODIS/061/MCD12Q1')
```

**Sources:** https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1

---

#### 68. Global Forest Watch / GLAD Alerts

**What it is:** Near-real-time deforestation monitoring system combining annual tree cover loss maps (Hansen dataset, 30 m) with weekly deforestation alerts (GLAD-L at 30 m, GLAD-S2 at 10 m).

**Maintained by:** World Resources Institute (WRI) / University of Maryland GLAD Lab

**Spatial coverage:** Global (annual loss); pan-tropical (alerts)

**Temporal coverage:** 2000-present (annual loss); 2016-present (GLAD-L alerts); 2019-present (GLAD-S2)

**Spatial resolution:** 30 m (Landsat-based), 10 m (Sentinel-2-based)

**Access method:** GFW Data API: https://data-api.globalforestwatch.org/, Google Earth Engine, direct download from https://data.globalforestwatch.org/

**Data format:** GeoTIFF, JSON/GeoJSON (API)

**Licence:** Creative Commons Attribution 4.0

**Key variables:** Tree cover loss (year), tree cover gain, tree cover 2000, loss alerts (date, confidence)

**How it relates to Causal Atlas:** Deforestation as both a driver (carbon release, land degradation, biodiversity loss) and outcome (economic pressure, conflict-driven land clearing) variable. Weekly alert frequency enables rapid event detection.

**Python access:**
```python
# Via GFW API
import requests
r = requests.get('https://data-api.globalforestwatch.org/...')
# Via Google Earth Engine
import ee
hansen = ee.Image('UMD/hansen/global_forest_change_2023_v1_11')
```

**Sources:** https://www.globalforestwatch.org/, https://glad.umd.edu/dataset/glad-forest-alerts

---

#### 69. FIRMS (Fire Information for Resource Management System)

**What it is:** Near-real-time active fire detection from MODIS and VIIRS sensors, providing global fire locations within minutes to hours of satellite overpass.

**Maintained by:** NASA LANCE (Land, Atmosphere Near real-time Capability for EOS)

**Spatial coverage:** Global

**Spatial resolution:** 375 m (VIIRS), 1 km (MODIS)

**Temporal coverage:** MODIS: November 2000-present; VIIRS: January 2012-present

**Latency:** Ultra Real-Time (< 60 seconds for US/Canada), NRT (< 3 hours globally)

**Access method:** REST API at https://firms.modaps.eosdis.nasa.gov/api/ (MAP_KEY required, free, 5000 requests/10 min limit), web map, email alerts, direct download

**Data format:** CSV, SHP, KML, GeoJSON (API)

**Licence:** Open (NASA data policy)

**Key variables:** Latitude, longitude, brightness temperature, scan/track pixel size, acquisition date/time, satellite, confidence, FRP (fire radiative power), day/night flag

**How it relates to Causal Atlas:** Fire events as indicators of land clearing, conflict-related arson, drought conditions, and agricultural practices. Fire radiative power (FRP) enables intensity analysis. Near-real-time availability supports rapid event assessment.

**Python access:**
```python
import requests
MAP_KEY = 'YOUR_MAP_KEY'
url = f'https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/world/1'
import pandas as pd
fires = pd.read_csv(url)
```

**Sources:** https://firms.modaps.eosdis.nasa.gov/, https://firms.modaps.eosdis.nasa.gov/academy/data_api/

---

#### 70. Copernicus Land Monitoring Service (CLMS) — Global Products

**What it is:** Suite of global land monitoring products derived from satellite observations, covering vegetation, water, energy, and land cover.

**Maintained by:** Copernicus / VITO Remote Sensing

**Key products:**
| Product | Resolution | Frequency | Variables |
|---------|-----------|-----------|-----------|
| CGLS-LC100 | 100 m | Annual | Land cover (23 classes) |
| NDVI/LAI/FAPAR | 300 m / 1 km | 10-daily | Vegetation condition |
| Soil Water Index | 1 km | Daily | Surface/root-zone soil moisture |
| Surface Albedo | 1 km | 10-daily | Surface reflectance |
| Burnt Area | 250 m | Monthly | Fire-affected areas |

**Access method:** Copernicus Data Space Ecosystem (CDSE), Sentinel Hub API, Google Earth Engine (some products). Migration to CDSE completing through 2025.

**Data format:** NetCDF, GeoTIFF

**Licence:** Open (Copernicus licence)

**How it relates to Causal Atlas:** 10-daily vegetation indices (NDVI, LAI) provide high-frequency crop/vegetation monitoring. Soil Water Index complements FLDAS soil moisture. Burnt area maps complement FIRMS active fire detection with total area burned.

**Sources:** https://land.copernicus.eu/en, https://land.copernicus.eu/global/product-access

---

#### 71. SoilGrids

**What it is:** Global gridded maps of soil properties at 250 m resolution, produced using machine learning on point observations and environmental covariates.

**Maintained by:** ISRIC — World Soil Information

**Spatial coverage:** Global

**Spatial resolution:** 250 m

**Depth intervals:** 0-5 cm, 5-15 cm, 15-30 cm, 30-60 cm, 60-100 cm, 100-200 cm

**Access method:** WCS (Web Coverage Service) for subsets, WebDAV for full global downloads, Google Earth Engine (community dataset). REST API temporarily paused as of March 2025.

**Data format:** GeoTIFF (via WCS/WebDAV), VRT (virtual raster format)

**Licence:** CC BY 4.0

**Key variables:** pH, soil organic carbon (SOC), bulk density, clay/silt/sand content, coarse fragments, cation exchange capacity (CEC), total nitrogen, SOC density, SOC stock

**How it relates to Causal Atlas:** Soil properties as static covariates that mediate climate→agriculture relationships (e.g., sandy soils drain faster → more drought-sensitive). SOC maps relevant to carbon sequestration analysis.

**Python access:**
```python
# Via soilgrids Python library
pip install soilgrids
from soilgrids import SoilGrids
sg = SoilGrids()
data = sg.get_coverage_data(service_id='phh2o', coverage_id='phh2o_0-5cm_mean',
                            west=-1.5, south=51.0, east=-1.0, north=51.5)
# Or via Google Earth Engine
import ee
soilgrids = ee.Image('projects/soilgrids-isric/phh2o_mean')
```

**Sources:** https://isric.org/explore/soilgrids, https://soilgrids.org/

---

### Infrastructure and Connectivity

#### 72. OpenCellID

**What it is:** Crowdsourced database of cell tower locations worldwide, serving as a proxy for telecommunications connectivity and infrastructure.

**Maintained by:** Unwired Labs (community-contributed)

**Spatial coverage:** Global (coverage varies; best in populated areas)

**Key metrics:** 2.5 billion+ cell measurements, millions of unique cells

**Access method:** Bulk CSV download from https://opencellid.org/downloads.php (API token required, 2 downloads/day limit), REST API for individual lookups

**Data format:** CSV (compressed, ~3.3 GB uncompressed)

**Licence:** CC BY-SA 4.0

**Key variables:** Radio type (GSM, UMTS, LTE, 5G NR), MCC (Mobile Country Code), MNC (Mobile Network Code), LAC/TAC, CellID, latitude, longitude, range (m), samples, changeable, created/updated timestamps

**Caveats:** Data limited to last 18 months to manage volume. Coverage biased toward areas with active contributors.

**How it relates to Causal Atlas:** Cell tower density as a proxy for connectivity and development. Infrastructure damage during conflict or disasters detectable through tower disappearance. Complements nighttime lights as a development indicator.

**Python access:**
```python
import pandas as pd
cells = pd.read_csv('cell_towers.csv.gz')
```

**Sources:** https://opencellid.org/

---

#### 73. Ookla Speedtest Open Data

**What it is:** Aggregated internet performance metrics (download/upload speed, latency) at ~610 m tile resolution globally, derived from Speedtest by Ookla mobile app tests.

**Maintained by:** Ookla

**Spatial coverage:** Global

**Spatial resolution:** Zoom level 16 web Mercator tiles (~610 m at equator)

**Temporal coverage:** Q1 2019 to present (quarterly updates)

**Access method:** GitHub: https://github.com/teamookla/ookla-open-data, AWS Open Data: https://registry.opendata.aws/speedtest-global-performance/, Google Earth Engine (community)

**Data format:** Apache Parquet (with WKT geometry, EPSG:4326), Shapefile

**Licence:** CC BY-NC-SA 4.0

**Key variables:** Average download speed (kbps), average upload speed (kbps), average latency (ms), number of tests, number of unique devices — for both fixed broadband and mobile (separate layers)

**How it relates to Causal Atlas:** Internet connectivity as a development indicator and potential conflict moderator. Speed/connectivity drops as early indicators of infrastructure disruption. Digital divide analysis.

**Python access:**
```python
import pandas as pd
import geopandas as gpd
# From Parquet on AWS
tiles = pd.read_parquet('s3://ookla-open-data/parquet/performance/type=mobile/year=2024/quarter=4/')
# Convert WKT to geometry
tiles = gpd.GeoDataFrame(tiles, geometry=gpd.GeoSeries.from_wkt(tiles['tile']))
```

**Sources:** https://github.com/teamookla/ookla-open-data

---

#### 74. OSM Infrastructure (OpenStreetMap)

**What it is:** Crowdsourced global map data including roads, buildings, health facilities, schools, water points, and other infrastructure. The most complete open-source infrastructure dataset for many developing countries.

**Maintained by:** OpenStreetMap community

**Spatial coverage:** Global (coverage varies; excellent in many developing countries due to humanitarian mapping efforts like HOT/Missing Maps)

**Access methods:**
- **Overpass API:** Query specific features by bounding box and tags (https://overpass-api.de/api/interpreter)
- **Geofabrik extracts:** Country/region bulk downloads (https://download.geofabrik.de/)
- **HOT Export Tool:** Custom extracts for humanitarian use (https://export.hotosm.org/)
- **Overture Maps:** Processed OSM data on cloud platforms

**Data format:** PBF (bulk), XML, GeoJSON (API)

**Licence:** ODbL (Open Database License) — free use with attribution and share-alike

**Key variables (tags):** `highway=*` (roads), `building=*`, `amenity=hospital/clinic/school`, `natural=water`, `waterway=*`, `power=*` (electricity infrastructure)

**How it relates to Causal Atlas:** Road network density as accessibility/development proxy. Health facility locations for health access analysis. Building footprint changes for urbanisation/destruction monitoring. Humanitarian mapping surge after disasters creates a "digital humanitarian response" signal.

**Python access:**
```python
# Via osmnx library
import osmnx as ox
roads = ox.graph_from_bbox(north, south, east, west, network_type='drive')
buildings = ox.features_from_bbox(north, south, east, west, tags={'building': True})
# Or via Overpass API with requests
```

**Sources:** https://wiki.openstreetmap.org/wiki/Overpass_API, https://download.geofabrik.de/

---

#### 75. Gridfinder — Predicted Electricity Grid Networks

**What it is:** Predictive model of electricity transmission and distribution grid line locations, using nighttime lights and road networks as inputs. Particularly valuable for Africa and South Asia where grid maps are incomplete.

**Maintained by:** Chris Arderne (originally World Bank / Facebook Connectivity)

**Spatial coverage:** Global (strongest value in data-poor regions)

**Spatial resolution:** ~1 km grid cells

**Validation accuracy:** ~75% across 14 validation countries

**Access method:** Download from World Bank Data Catalog: https://datacatalog.worldbank.org/search/dataset/0038055, visualization at https://gridfinder.rdrn.me/, source code on GitHub: https://github.com/carderne/gridfinder

**Data format:** GeoPackage (grid lines), GeoTIFF (targets and LV infrastructure rasters)

**Licence:** CC BY 4.0

**Key variables:** Predicted grid line locations (vector), grid connection targets (binary raster), low-voltage infrastructure density (km/cell)

**How it relates to Causal Atlas:** Electrification as a development indicator and moderator of economic activity. Distance from grid as a vulnerability factor. Complements nighttime lights for areas where light is not visible but grid exists (e.g., dense forest canopy).

**Python access:**
```python
import geopandas as gpd
grid = gpd.read_file('grid.gpkg')
# Or process rasters
import rasterio
with rasterio.open('targets.tif') as src:
    electrified = src.read(1)
```

**Sources:** https://www.nature.com/articles/s41597-019-0347-4, https://github.com/carderne/gridfinder

---

### Cross-Domain Integration Notes (Extended)

11. **Climate data ecosystem:** CRU TS (0.5°, 1901-present) is the priority climate dataset for PRIO-GRID alignment. TerraClimate adds water balance variables at 4 km. FLDAS provides food-security-optimised soil moisture. SPEI Global Drought Monitor provides ready-to-use drought indices. Together these cover: raw climate → derived indices → land surface response.

12. **Precipitation product hierarchy:** For Causal Atlas, prefer IMERG V07 (0.1°, global, 2000-present) as the primary precipitation product, aggregated to PRIO-GRID. CHIRPS (0.05°, 50°S-50°N, 1981-present) for longer record. CMORPH for sub-daily extreme event analysis. CRU TS precipitation for the longest record (1901+).

13. **Governance data stack:** REIGN (monthly, 1950-present) provides the highest temporal resolution for leadership/regime data. Polity5 (annual, 1800-2018) and Freedom House (annual, 1972-present) provide regime quality scores. FSI (annual, 2006-present) measures fragility. V-Dem (already documented) is the most comprehensive.

14. **Conflict data complementarity:** UCDP-GED + ACLED (documented separately) cover armed conflict. GTD adds terrorism events. SCAD adds protests/riots/strikes in Africa. Mass Mobilization adds global protest data. COW provides historical interstate conflict. Together these capture the full spectrum from protests to interstate war.

15. **Population data hierarchy:** For exposure calculations, prefer Meta/CIESIN HRSL (30 m) for highest resolution, LandScan (1 km) for ambient population, GHS-POP (100 m, multi-epoch) for historical population change, WorldPop/GPW (already documented) as alternatives. GRID3 for African settlement delineation.

16. **Economic proxy chain:** Official GDP (IMF WEO, World Bank) → Nighttime lights GDP proxies → Commodity prices (IMF PCPS, Pink Sheet) → Trade flows (OEC, Global Trade Alert) → Household welfare (LSMS, DHS wealth index). This chain allows economic analysis even where official statistics are poor.

17. **Health data complementarity:** DHS/MICS provide GPS-located household health surveys. IHME GBD provides modelled disease burden surfaces. Malaria Atlas Project provides gridded malaria metrics. Global.health provides epidemic line lists. Africa CDC provides regional surveillance. Together these cover: survey-based → modelled → surveillance data.

18. **Land/environment monitoring stack:** ESA CCI (300 m annual, 1992-2022) for long-term land cover change. MODIS MCD12Q1 (500 m, 2001-present) for annual classification. FIRMS for near-real-time fires. Global Forest Watch for deforestation monitoring. SoilGrids for static soil properties. Copernicus CLMS for 10-daily vegetation monitoring.
