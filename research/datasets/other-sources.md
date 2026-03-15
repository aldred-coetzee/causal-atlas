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
