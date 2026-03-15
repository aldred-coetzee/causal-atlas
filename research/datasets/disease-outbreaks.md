# Disease Outbreak and Health Data Sources

> **Last updated:** March 2025
> **Status:** Deep research — comprehensive source catalogue for Causal Atlas

This file covers the major global disease outbreak and health data sources relevant to cross-domain causal analysis. Each source is assessed for API access, schema, spatial/temporal resolution, licensing, and relevance to the Causal Atlas project.

---

## Table of Contents

1. [WHO Global Health Observatory (GHO)](#1-who-global-health-observatory-gho)
2. [ProMED (Program for Monitoring Emerging Diseases)](#2-promed-program-for-monitoring-emerging-diseases)
3. [IHME Global Burden of Disease (GBD)](#3-ihme-global-burden-of-disease-gbd)
4. [WHO Disease Outbreak News (DONs)](#4-who-disease-outbreak-news-dons)
5. [HealthMap and BEACON](#5-healthmap-and-beacon)
6. [Other WHO Data Portals and Supplementary Sources](#6-other-who-data-portals-and-supplementary-sources)
7. [CMU Delphi Epidata API](#7-cmu-delphi-epidata-api)
8. [CDC NNDSS / WONDER](#8-cdc-nndss--wonder)
9. [Cross-Source Comparison](#9-cross-source-comparison)
10. [Relevance to Causal Atlas](#10-relevance-to-causal-atlas)

---

## 1. WHO Global Health Observatory (GHO)

### Overview

The GHO is WHO's primary statistical data repository, providing access to **over 1,000 health indicators** for all 194 WHO Member States. It covers mortality, burden of disease, communicable and non-communicable diseases, health systems, environmental health, the Sustainable Development Goals (SDGs), and more.

- **URL:** https://www.who.int/data/gho
- **Operator:** World Health Organization
- **Data type:** Aggregated national/subnational health statistics

### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | 194 WHO Member States; some indicators have subnational breakdowns |
| **Temporal** | Varies by indicator; many go back to 1990 or earlier; annual resolution for most |
| **Thematic** | 1,000+ indicators across infectious disease, NCDs, mortality, maternal/child health, environmental health, health systems, SDG targets |

### API Access

The GHO provides a free, unauthenticated **OData v4 API**.

| Property | Value |
|----------|-------|
| **Base URL** | `https://ghoapi.azureedge.net/api/` |
| **Authentication** | None required |
| **Rate limits** | Not formally documented; appears generous for reasonable use |
| **Format** | JSON (OData v4) |
| **Deprecation notice** | WHO has announced the current OData API will be deprecated near end of 2025 in favour of a new OData implementation |

#### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/Indicator` | List all available indicators with codes and names |
| `/api/{IndicatorCode}` | Retrieve all data for a specific indicator |
| `/api/DIMENSION/COUNTRY/DimensionValues` | List all country dimension values |
| `/api/Indicator?$filter=contains(IndicatorName,'malaria')` | Filter indicators by keyword |

#### Example: Fetch Cholera Cases

```
GET https://ghoapi.azureedge.net/api/CHOLERA_0000000001
```

Returns JSON with all country-year observations of reported cholera cases.

### Response Schema (JSON)

Each data value in the API response contains these fields:

| Field | Type | Description |
|-------|------|-------------|
| `Id` | integer | Unique record identifier |
| `IndicatorCode` | string | Code for the health indicator |
| `SpatialDimType` | string | Type of spatial dimension (e.g., "COUNTRY") |
| `SpatialDim` | string | ISO 3166-1 alpha-3 country code (e.g., "BDI") |
| `TimeDimType` | string | Type of time dimension (e.g., "YEAR") |
| `TimeDim` | integer | Year of observation |
| `Dim1Type` | string | Additional dimension type (e.g., "SEX") |
| `Dim1` | string | Additional dimension value |
| `Dim2Type` | string | Second additional dimension type |
| `Dim2` | string | Second additional dimension value |
| `Dim3Type` | string | Third additional dimension type |
| `Dim3` | string | Third additional dimension value |
| `DataSourceDimType` | string | Data source dimension type |
| `DataSourceDim` | string | Data source identifier |
| `Value` | string | String representation of the value |
| `NumericValue` | float/null | Numeric value (null for non-numeric indicators) |
| `Low` | float/null | Lower confidence/uncertainty bound |
| `High` | float/null | Upper confidence/uncertainty bound |
| `Comments` | string/null | Additional notes |
| `Date` | string | Date the record was last modified |
| `TimeDimensionValue` | string | Time dimension as string |
| `TimeDimensionBegin` | string | Start of time period (ISO 8601) |
| `TimeDimensionEnd` | string | End of time period (ISO 8601) |

### Key Indicator Codes for Causal Atlas

| Indicator Code | Description |
|----------------|-------------|
| `CHOLERA_0000000001` | Number of reported cholera cases |
| `CHOLERA_0000000002` | Cholera case fatality rate |
| `MALARIA_EST_INCIDENCE` | Estimated malaria incidence per 1,000 population at risk |
| `MALARIA_EST_DEATHS` | Estimated malaria deaths |
| `MDG_0000000020` | Tuberculosis incidence per 100,000 |
| `WHS3_49` | Measles immunization coverage among 1-year-olds |
| `WHS4_100` | Life expectancy at birth |
| `NCDMORT3070` | Probability of dying from any NCD between ages 30-70 |
| `WSH_WATER_BASIC` | Population using basic drinking water services (%) |
| `AIR_41` | Ambient air pollution (PM2.5 annual mean) |

Use `/api/Indicator?$filter=contains(IndicatorName,'cholera')` to discover more codes interactively.

### Python Access

#### Direct requests (recommended)

```python
import requests
import pandas as pd

BASE_URL = "https://ghoapi.azureedge.net/api"

# List all indicators matching "cholera"
resp = requests.get(f"{BASE_URL}/Indicator", params={
    "$filter": "contains(IndicatorName,'cholera')"
})
indicators = resp.json()["value"]

# Fetch cholera cases for all countries
resp = requests.get(f"{BASE_URL}/CHOLERA_0000000001")
data = resp.json()["value"]
df = pd.DataFrame(data)

# Filter to a specific country and time range
resp = requests.get(f"{BASE_URL}/CHOLERA_0000000001", params={
    "$filter": "SpatialDim eq 'ETH' and TimeDim ge 2010"
})
```

#### Third-party libraries

| Library | Install | Notes |
|---------|---------|-------|
| `apidatawho` | `pip install apidatawho` | Utility functions for GHO dimensions, indicators, data |
| `WHO_GHO_API_client` | Available on TestPyPI | Wrapper returning pandas DataFrames |
| `ghoclient` | `pip install ghoclient` | Python client by F.C. Coelho |

### Licence

- **CC BY-NC-SA 3.0 IGO** (Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Intergovernmental Organization)
- Attribution to WHO required
- **Non-commercial use only** without separate permission
- Commercial use requires written WHO permission
- Source: https://www.who.int/about/policies/publishing/copyright

### Quality Issues and Limitations

- Country-level only for most indicators; no grid-cell resolution
- Reporting quality varies significantly by country and indicator
- Some indicators are modelled estimates, others are raw reported counts — metadata clarifies which
- Annual temporal resolution for most indicators limits lag analysis at finer scales
- Data completeness gaps for conflict-affected countries (precisely where cross-domain analysis matters most)
- Planned API deprecation (end of 2025) means ingestion code may need updating

---

## 2. ProMED (Program for Monitoring Emerging Diseases)

### Overview

ProMED (officially ProMED-mail) is the world's longest-running outbreak early warning system, operated since 1994 by the International Society for Infectious Diseases (ISID). It disseminates rapid alerts about outbreaks of infectious diseases, toxin exposures, and food safety events affecting human, animal, and plant health. Reports are curated by a network of expert moderators who review submissions from physicians, veterinarians, epidemiologists, and media sources worldwide.

- **URL:** https://www.promedmail.org/
- **Operator:** ISID (International Society for Infectious Diseases)
- **Data type:** Unstructured/semi-structured event reports (curated prose)

### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | Global — reports from nearly every country; locations mentioned in free text |
| **Temporal** | Archive from 1994 to present; reports published as events occur (near real-time) |
| **Thematic** | All infectious diseases, zoonoses, food safety, plant diseases, toxin exposures |
| **Volume** | ~31 years of reports; thousands of reports per year |

### Current Status (March 2025)

ProMED faced a **major operational crisis in August 2023** when 21 of 38 paid editors and moderators went on strike due to lack of institutional support from ISID. The service continued in a limited capacity. As of late 2024, ProMED entered a strategic alliance with **samdesk** for next-generation detection and monitoring. A new user experience is planned for 2025.

**Access model has changed:** ProMED now requires login credentials and operates a subscription-based model with tiered access to different types/amounts of information and archive search depth. This is a significant change from its previously fully open model.

### Data Access

| Method | Detail |
|--------|--------|
| **Web interface** | https://www.promedmail.org/ — requires free registration; full archive search may require paid subscription |
| **Email subscription** | Free email alerts for new reports |
| **Formal API** | **None** — no official structured data API exists |
| **Scraping** | Possible via AJAX endpoint (see below), but not officially supported |

#### Scraping Approach (from EcoHealth Alliance GRITS project)

The ProMED website exposes an internal AJAX endpoint used by the web interface:

```
POST https://promedmail.org/ajax/getPost.php
```

Parameters: post ID. Returns HTML content of the report.

The EcoHealth Alliance's `grits-api` project (https://github.com/ecohealthalliance/grits-api) includes a `scrape_promed.py` script demonstrating this approach.

### Data Structure (Semi-Structured)

Each ProMED report contains:

| Field | Type | Notes |
|-------|------|-------|
| Post ID | integer | Unique report identifier |
| Date | date | Publication date |
| Subject line | text | Disease name, location, often structured as "DISEASE - COUNTRY (REGION)" |
| Body text | prose | Narrative report with epidemiological details |
| Disease name(s) | text (in body) | Not in a structured field; must be extracted via NLP |
| Location(s) | text (in body) | Place names in free text; no coordinates |
| Case counts | text (in body) | Mentioned in narrative; inconsistent formatting |
| Related posts | list | Links to prior ProMED reports on the same event |
| Source | text | Original source (news article, official report, etc.) |

### Spatial Detail

- **No geocoding** — locations are mentioned in free text only
- Subject lines often follow the pattern `DISEASE - COUNTRY (REGION/STATE)` but this is not consistently structured
- Researchers have used NLP and gazetteers to extract and geocode locations from ProMED text (see academic literature on ProMED text mining)
- Resolution is typically country or subnational admin level, never grid-cell

### Python Access

```python
import requests

# Fetch a specific ProMED post by ID (unofficial approach)
post_id = "8716979"  # example
resp = requests.post(
    "https://promedmail.org/ajax/getPost.php",
    data={"postId": post_id}
)
html_content = resp.text
# Then parse with BeautifulSoup or similar
```

Academic approaches to structured extraction:
- **TextRank keyword extraction** + word co-occurrence networks (Lyon et al., 2021, JRSS Series A)
- **LLM-based extraction** using ensemble approaches (Springer, 2024)
- **GRITS project** by EcoHealth Alliance for automated classification

### Licence

- Reports are copyrighted by ISID/ProMED
- Free access for personal/research use has historically been available, but the new subscription model may restrict archive access
- No explicit open data licence (not CC-licensed)
- Scraping is not explicitly authorised; check current terms of service

### Quality Issues and Limitations

- **Unstructured data** — all epidemiological information is in narrative prose, requiring NLP for structured extraction
- **No official API** — fragile scraping approach that may break
- **Subscription model** — unclear what data access tiers allow for research/bulk access
- **Inconsistent reporting** — disease names, locations, case counts vary in format across reports
- **Moderation crisis** — reduced editorial capacity since 2023 may affect data quality and completeness
- **No geocoding** — location extraction is a manual/NLP challenge
- **Bias toward English-language sources** and regions with media coverage

---

## 3. IHME Global Burden of Disease (GBD)

### Overview

The Global Burden of Disease Study, coordinated by the Institute for Health Metrics and Evaluation (IHME) at the University of Washington, is the most comprehensive effort to measure epidemiological levels and trends worldwide. GBD provides estimates for mortality, morbidity, and disability from hundreds of diseases, injuries, and risk factors for every country and many subnational locations.

- **URL:** https://www.healthdata.org/research-analysis/gbd-data
- **Operator:** IHME, University of Washington
- **Latest release:** GBD 2023 (released October 2025)
- **Previous major releases:** GBD 2021, GBD 2019, GBD 2017, GBD 2016, GBD 2015, GBD 2013, GBD 2010

### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | 204 countries and territories + **660 subnational locations** |
| **Temporal** | 1990-2023 (GBD 2023); annual estimates |
| **Causes** | 292 causes of death, 375 diseases and injuries |
| **Risk factors** | 88 risk factors |
| **Measures** | Deaths, DALYs, YLLs, YLDs, prevalence, incidence |
| **Demographics** | By age group and sex |

### Key Metrics

| Measure | Description | Relevance |
|---------|-------------|-----------|
| **DALYs** | Disability-Adjusted Life Years | Overall disease burden combining mortality and morbidity |
| **YLLs** | Years of Life Lost | Premature mortality component |
| **YLDs** | Years Lived with Disability | Morbidity/disability component |
| **Deaths** | Number of deaths by cause | Direct mortality |
| **Prevalence** | Number of existing cases at a point in time | Current disease burden |
| **Incidence** | Number of new cases in a time period | Disease dynamics and trends |

### Data Access

#### GBD Results Tool (primary method)

- **URL:** https://vizhub.healthdata.org/gbd-results/
- **Account required:** Yes (free registration)
- **Download format:** CSV
- **Row limit:** 100,000 rows per request
- **Selection:** Choose measure, location, cause, age, sex, year, metric (number, rate, percent)

#### GBD Compare (visualization)

- **URL:** https://www.healthdata.org/data-tools-practices/interactive-visuals/gbd-compare
- Treemap visualizations, not for bulk download

#### API

- **No official API exists** as of March 2025
- IHME has stated: "IHME has no data APIs available at this time"
- The former SDG API has been discontinued

#### Bulk Data Files

- Available via the Global Health Data Exchange (GHDx): https://ghdx.healthdata.org/gbd-2023
- Location hierarchy files, cause hierarchy files, and codebooks downloadable as ZIP/XLSX
- Key reference file: `IHME_GBD_2023_A3_MEASURE_METRIC_DEFINITIONS_Y2025M10D24.XLSX`

### CSV Schema (GBD Results Tool export)

Based on the GBD Results Tool User Guide and codebook documentation, the CSV export contains these columns:

| Column | Type | Description |
|--------|------|-------------|
| `measure_id` | integer | Numeric ID for measure type |
| `measure_name` | string | "Deaths", "DALYs", "Prevalence", etc. |
| `location_id` | integer | IHME location ID |
| `location_name` | string | Country or subnational name |
| `sex_id` | integer | 1=Male, 2=Female, 3=Both |
| `sex_name` | string | "Male", "Female", "Both" |
| `age_id` | integer | IHME age group ID |
| `age_name` | string | Age group label (e.g., "15-49 years") |
| `cause_id` | integer | IHME cause ID |
| `cause_name` | string | Disease/injury name |
| `metric_id` | integer | 1=Number, 2=Percent, 3=Rate |
| `metric_name` | string | "Number", "Percent", "Rate" |
| `year` | integer | Year of estimate |
| `val` | float | Point estimate |
| `upper` | float | Upper 95% uncertainty interval |
| `lower` | float | Lower 95% uncertainty interval |

### Subnational Coverage

GBD 2023 provides subnational estimates for 660 locations. Countries with subnational data include (non-exhaustive):
- Brazil, China, India, Indonesia, Japan, Kenya, Mexico, Nigeria, Russia, South Africa, United Kingdom, United States, and others
- The full hierarchy is available in the GBD 2023 Location Hierarchy file on GHDx

### Python Access

No official Python API client exists. Workarounds:

```python
# Option 1: Use ddf_utils IHMELoader for bulk download
# pip install ddf_utils
from ddf_utils.factory.ihme import IHMELoader
loader = IHMELoader()

# Option 2: Use gbd_mapping for metadata
# pip install gbd_mapping
# https://github.com/ihmeuw/gbd_mapping
from gbd_mapping import causes, risk_factors

# Option 3: Manual CSV download from GBD Results Tool
# 1. Register at healthdata.org
# 2. Configure query at vizhub.healthdata.org/gbd-results/
# 3. Download CSV, then load with pandas
import pandas as pd
df = pd.read_csv("IHME-GBD_2023_DATA-xxxxx.csv")
```

### Licence

- **IHME Free-of-Charge Non-Commercial User Agreement**
- Non-commercial use: Free
- Commercial use: Requires separate agreement with IHME
- Visualisation screenshots: **CC BY-NC-ND 4.0** (Attribution-NonCommercial-NoDerivatives)
- Citation required — suggested format provided on GHDx for each dataset
- Source: https://www.healthdata.org/data-tools-practices/data-practices/terms-and-conditions

### Quality Issues and Limitations

- **No API** — cannot automate data ingestion; must use manual CSV download or unofficial workarounds
- **100,000 row limit** per query — large requests (e.g., all causes x all countries x all years) require multiple downloads
- **Annual resolution only** — no monthly or daily data; limits sub-annual lag analysis
- **Country/subnational only** — no grid-cell resolution; subnational not available for all countries
- **Modelled estimates** — GBD values are model outputs, not raw surveillance data; uncertainty intervals reflect this
- **Publication lag** — GBD 2023 data was released in October 2025, so there is roughly a 2-year lag
- **Account required** — automated pipelines may face issues with authentication

---

## 4. WHO Disease Outbreak News (DONs)

### Overview

WHO Disease Outbreak News (DONs) are official WHO communications about confirmed acute public health events or potential events of concern. Published since 1996, they cover emerging and re-emerging infectious diseases, unusual clusters, and events that may constitute a Public Health Emergency of International Concern (PHEIC).

- **URL:** https://www.who.int/emergencies/disease-outbreak-news
- **Operator:** World Health Organization
- **Data type:** Semi-structured event reports (narrative with some structured metadata)

### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | Global — any WHO Member State |
| **Temporal** | January 1996 to present |
| **Volume** | ~2,789 reports from 1996-2019 (pre-COVID); continued since 2020 |
| **Thematic** | Emerging/re-emerging infectious disease events |

### API Access

WHO provides a RESTful API for DONs:

| Property | Value |
|----------|-------|
| **Base URL** | `https://www.who.int/api/news/diseaseoutbreaknews` |
| **Authentication** | None required |
| **Format** | JSON |
| **Documentation** | https://www.who.int/api/news/diseaseoutbreaknews/sfhelp |

#### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/news/diseaseoutbreaknews` | List DON items |
| `GET /api/news/diseaseoutbreaknews({key})` | Get specific DON by key |
| `GET /api/news/diseaseoutbreaknews({key})/Regions` | Get regions for a DON |
| `GET /api/news/diseaseoutbreaknews({key})/Response_ContentBlock` | Response section |
| `GET /api/news/diseaseoutbreaknews({key})/FurtherInformation_ContentBlock` | Further info |

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `DonId` | string | Unique DON identifier |
| `Title` | string | Report title |
| `PublicationDate` | datetime | Date of publication |
| `PublicationDateAndTime` | datetime | Full publication timestamp |
| `Summary` | HTML/text | Summary of the event |
| `Overview` | HTML/text | Overview section |
| `Epidemiology` | HTML/text | Epidemiological details (narrative) |
| `Assessment` | HTML/text | WHO risk assessment |
| `Advice` | HTML/text | WHO advice/recommendations |
| `Response` | HTML/text | Response measures taken |
| `FurtherInformation` | HTML/text | Links and references |
| `regionscountries` | string | Associated regions/countries |
| `UrlName` | string | URL slug |
| `ItemDefaultUrl` | string | Full URL to the DON page |
| `LastModified` | datetime | Last modification timestamp |

### Structured Retrospective Databases

Because the DON reports are largely narrative prose, researchers have created structured databases from them:

#### CGHSS DON Database (Georgetown University)

- **Repository:** https://github.com/cghss/dons
- **Coverage:** All 2,789 reports from January 1996 to December 2019
- **Repository 2:** https://github.com/cghss/dons2 — covers 2020-2023
- **Structured fields extracted:** Disease name, country, date, case counts, deaths, actions taken
- **Published:** Carlson et al. (2023), "The World Health Organization's Disease Outbreak News: a retrospective database"

#### Epidemiological Knowledge Graph (eKG)

- **Published:** 2025, Scientific Data (Nature)
- Uses ensemble LLM approaches to extract structured epidemiological data from DON text
- Extracts: disease names, involved countries, event dates, total cases, deaths
- Daily-updated dataset available
- Reference: https://www.nature.com/articles/s41597-025-05276-2

### Python Access

```python
import requests

# Fetch recent DONs
resp = requests.get("https://www.who.int/api/news/diseaseoutbreaknews")
dons = resp.json()["value"]

for don in dons[:5]:
    print(f"{don['PublicationDate']}: {don['Title']}")
    print(f"  URL: {don['ItemDefaultUrl']}")

# Fetch a specific DON by key
key = dons[0]["DonId"]
resp = requests.get(f"https://www.who.int/api/news/diseaseoutbreaknews('{key}')")
detail = resp.json()
```

### Licence

- Same as WHO general: **CC BY-NC-SA 3.0 IGO**
- Attribution required, non-commercial use

### Quality Issues and Limitations

- **Narrative prose** — epidemiological details are in HTML text, not structured fields
- **Inconsistent reporting** — disease names, case counts, and location specificity vary across reports
- **No geocoding** — countries/regions mentioned in text, no coordinates
- **Selection bias** — DONs cover only events WHO deems noteworthy; not a comprehensive surveillance system
- **Temporal gaps** — reporting frequency varies; some diseases overrepresented
- **HTML content** — requires HTML parsing to extract text from API response fields
- The CGHSS structured database and the eKG are far more useful for computational analysis than raw DONs

---

## 5. HealthMap and BEACON

### 5.1 HealthMap

#### Overview

HealthMap (founded 2006) is an automated real-time disease surveillance system developed by a team at Boston Children's Hospital. It aggregates data from online news, official reports, eyewitness accounts, and expert discussions to provide a unified view of the global state of infectious diseases.

- **URL:** https://healthmap.org/
- **Operator:** Boston Children's Hospital / Harvard Medical School
- **Data type:** Aggregated event-based surveillance from open sources

#### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | Global; events geocoded to varying resolution |
| **Temporal** | Real-time; archive from 2006 to present |
| **Sources** | 20,000+ websites; ~300 reports collected per day |
| **Thematic** | All infectious diseases affecting humans and animals |

#### Data Access

- **Web interface:** http://www.healthmap.org/en/ — interactive map with event markers
- **Mobile app:** "Outbreaks Near Me" for real-time alerts
- **API:** **No public API documented** as of March 2025
- **Data format:** Events displayed on map with source links; no bulk download
- Data has been incorporated into WHO's **Epidemic Intelligence from Open Sources (EIOS)** system

#### Quality Issues

- Automated classification has error rates; expert review improves but does not eliminate misclassification
- 85% of sources are news media, which introduces media attention bias
- Geocoding quality varies — some events geolocated to city level, others only to country
- No documented bulk data access for researchers

### 5.2 BEACON (Biothreats Emergence, Analysis and Communications Network)

#### Overview

BEACON is a new open-source disease surveillance platform that launched in beta on **April 24, 2025**. It builds on HealthMap's decades of experience and combines AI/LLM-driven analysis with a global network of human experts. It represents the next generation of the HealthMap approach.

- **URL:** https://beaconbio.org/
- **Operator:** Boston University Center on Emerging Infectious Diseases + Hariri Institute + HealthMap (Boston Children's Hospital)
- **Status:** Beta launched April 2025; operational as of late 2025
- **Funding:** $6 million from NSF, Gates Foundation, private donors, Boston University

#### Coverage (as of November 2025)

| Dimension | Detail |
|-----------|--------|
| **Spatial** | 195 countries and territories; active users in 168 countries |
| **Temporal** | Real-time |
| **Diseases** | 100+ diseases tracked |
| **Reports** | ~600 outbreaks in 1,300+ disease reports (first 7 months of operation) |

#### Key Features

- **Open-source** — code and data intended to be openly available
- Uses LLMs for automated analysis and contextualisation of disease reports
- Partnerships with WHO EIOS, World Organisation for Animal Health, CEPI, state health departments, CDC Center for Forecasting and Outbreak Analytics
- Combines automated processing with human expert verification

#### Data Access

- Platform accessible at beaconbio.org
- Being open-source, data access is intended to be more transparent than HealthMap
- Specific API documentation not yet fully available as of March 2025 (pre-beta)
- Published description: Gade et al. (2024), "BEACON for Novel Disease Threats," Journal of Infectious Diseases

#### Relevance

BEACON is the most promising emerging source for real-time, structured disease event data. Its open-source nature and institutional partnerships make it a strong candidate for Causal Atlas integration once its API matures.

---

## 6. Other WHO Data Portals and Supplementary Sources

### 6.1 WHO Data Portal Ecosystem

WHO operates several interconnected data platforms:

| Platform | URL | Description |
|----------|-----|-------------|
| **Global Health Observatory (GHO)** | https://www.who.int/data/gho | Primary indicator repository (see Section 1) |
| **WHO Data** | https://www.who.int/data | Landing page for all WHO data resources |
| **GHO Data Repository (legacy)** | https://apps.who.int/gho/data/ | Older interface; still accessible |
| **Health Inequality Data Repository** | Via WHO Data | Disaggregated data for equity analysis |
| **OpenWHO** | https://openwho.org/ | Primarily an eLearning platform; includes health inequality monitoring channel; not a data source |
| **WHO Situation Dashboard** | Via HDX | CSV extracts of situation data (e.g., COVID-19) available on UNOCHA's HDX |

### 6.2 WHO Athena API (Legacy)

The older Athena API provides alternative access to some GHO data:

- **Base URL:** `https://apps.who.int/gho/athena/api/`
- **Formats:** XML, JSON, CSV
- **Documentation:** https://www.who.int/data/gho/info/athena-api-examples
- Being superseded by the OData API

Example:
```
https://apps.who.int/gho/athena/data/xmart.csv?target=GHO/CHOLERA_0000000001&profile=crosstable&filter=COUNTRY:*;REGION:AFR;
```

### 6.3 Global Health Estimates (GHE)

- WHO produces its own burden of disease estimates (separate from IHME GBD)
- Available via GHO as specific indicators
- Covers cause-specific mortality, DALYs, and life expectancy
- Annual updates, country-level

### 6.4 IHR Event Information Site

- Tracks events reported under the International Health Regulations (2005)
- Not publicly accessible; restricted to WHO Member State focal points
- Events that are publicly communicated become DONs or Emergency Situation Reports

---

## 7. CMU Delphi Epidata API

### Overview

The Delphi Epidata API, maintained by Carnegie Mellon University's Delphi research group, provides open access to epidemiological surveillance data, primarily for the United States but with some international coverage.

- **URL:** https://cmu-delphi.github.io/delphi-epidata/
- **GitHub:** https://github.com/cmu-delphi/delphi-epidata
- **Data type:** Time series surveillance signals

### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | Primarily US (state, county, HRR levels); some international (Taiwan NIDSS dengue) |
| **Temporal** | Historical and near real-time; varies by signal |
| **Diseases** | Influenza, COVID-19, dengue, norovirus, and others |
| **Signals** | 500+ different surveillance signals |

### API Access

| Property | Value |
|----------|-------|
| **Base URL** | `https://api.delphi.cmu.edu/epidata/` |
| **Authentication** | Anonymous access for most endpoints |
| **Format** | JSON |
| **Rate limits** | Not restrictive for reasonable use |

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/fluview/` | CDC ILINet influenza data |
| `/nidss_dengue/` | Taiwan NIDSS dengue data |
| `/covidcast/` | COVIDcast multi-source COVID-19 signals |
| `/sensors/` | Digital surveillance sensor data (some deprecated) |

### Python Access

```python
# Legacy client
# pip install delphi-epidata
from delphi_epidata import Epidata

# Fetch ILINet flu data
res = Epidata.fluview(regions=['nat'], epiweeks=[202401, 202452])
```

### Relevance to Causal Atlas

- Strong for US-focused disease-climate or disease-conflict analysis
- Limited international coverage constrains global cross-domain analysis
- Good model for how a disease signal API should work
- COVIDcast infrastructure shows how multiple signals can be harmonised

---

## 8. CDC NNDSS / WONDER

### Overview

The National Notifiable Diseases Surveillance System (NNDSS) collects data on nationally notifiable infectious diseases reported by US state and territorial health departments to CDC.

- **URL:** https://wonder.cdc.gov/nndss.html (annual data) and https://data.cdc.gov (weekly data, migrated January 2025)
- **Operator:** US CDC
- **Scope:** United States only

### Coverage

| Dimension | Detail |
|-----------|--------|
| **Spatial** | US national, state, and territory level |
| **Temporal** | Weekly tables; annual summaries since 1994 |
| **Diseases** | ~120 nationally notifiable conditions |

### 2025 Changes

In January 2025, CDC migrated NNDSS weekly and annual tables:
- Weekly PDF/text tables moved to **CDC Stacks** and **data.cdc.gov**
- Annual summary interactive queries remain on **CDC WONDER**
- HTML format updated for improved user experience

### Relevance to Causal Atlas

- US-only scope limits direct utility for a global platform
- Useful as validation data for US regions
- data.cdc.gov provides machine-readable formats (CSV, API) for US disease surveillance

---

## 9. Cross-Source Comparison

| Feature | WHO GHO | ProMED | IHME GBD | WHO DONs | HealthMap/BEACON | Delphi Epidata |
|---------|---------|--------|----------|----------|------------------|----------------|
| **API** | OData (free, no auth) | None | None | REST (free, no auth) | None / TBD | REST (free, no auth) |
| **Format** | JSON | HTML/text | CSV | JSON (HTML content) | Web only | JSON |
| **Spatial resolution** | Country | Free text | Country + 660 subnational | Country | Geocoded events | US state/county |
| **Temporal resolution** | Annual | Event-based (real-time) | Annual | Event-based | Real-time | Weekly |
| **Temporal coverage** | 1990+ | 1994+ | 1990-2023 | 1996+ | 2006+ | Varies |
| **Structured data** | Yes | No | Yes | Semi-structured | Semi-structured | Yes |
| **Disease breadth** | 1,000+ indicators | All infectious | 375 diseases | Emerging events | All infectious | Flu, COVID, dengue |
| **Licence** | CC BY-NC-SA 3.0 IGO | Proprietary/subscription | Non-commercial | CC BY-NC-SA 3.0 IGO | Varies | Open |
| **Automation-friendly** | High | Low | Low | Medium | Low / TBD | High |

---

## 10. Relevance to Causal Atlas

### Cross-Domain Causal Chains Involving Disease Data

Disease outbreak data is central to several key causal chains Causal Atlas aims to investigate:

#### Climate to Disease

Published research documents lag structures for climate-disease relationships:

- **Temperature/rainfall to cholera:** 4-8 week lag from rainfall events to cholera case peaks (multiple studies)
- **Temperature to malaria transmission:** Seasonal and interannual variation driven by temperature thresholds for parasite development; 1-3 month lags documented
- **Flooding to diarrheal disease:** 1-4 week lag from flood events to case spikes
- **Drought to malnutrition to disease vulnerability:** Multi-month cascading chain
- **El Nino to disease outbreaks:** Well-documented for cholera, dengue, malaria at 3-6 month lags

Methodological reference: Distributed Lag Non-Linear Models (DLNMs) are the standard approach for characterising non-linear, delayed climate-disease associations (Gasparrini et al.).

#### Disease to Conflict

- COVID-19 showed a positive influence on demonstrations with a one-month lag, and a negative relationship with non-state violent conflict
- Disease outbreaks can destabilise governance, especially in fragile states
- Epidemic responses can trigger social unrest (lockdowns, quarantine enforcement)

#### Disease to Economic Impact

- Disease burden (DALYs, mortality) correlates with reduced economic productivity
- Outbreak events trigger trade restrictions, tourism decline, market disruptions
- GBD data enables quantification of disease burden for economic impact analysis

#### Conflict to Disease

- Conflict disrupts health systems, enabling disease outbreaks
- Displacement creates conditions for epidemic transmission
- This bidirectional relationship is critical for the Causal Atlas

### Recommended Data Integration Strategy

For the Causal Atlas, disease data should be integrated at multiple levels:

1. **Structured annual indicators (WHO GHO):** Use as the baseline for country-level disease burden time series. Best for long-term trend analysis and Granger causality testing against annual economic/conflict indicators. Map to PRIO-GRID cells by country assignment.

2. **Comprehensive disease burden estimates (IHME GBD):** Use for disease-specific DALYs, mortality, and prevalence. Provides uncertainty intervals critical for statistical methods. Subnational data available for 660 locations. Download CSV batches covering relevant causes and years.

3. **Event-based outbreak data (WHO DONs + CGHSS structured database):** Use for event-level analysis of outbreak timing relative to climate events, conflict, and food security. The CGHSS structured database (GitHub) and the eKG (Nature Scientific Data) provide pre-extracted structured data from DON narratives.

4. **Real-time surveillance (BEACON):** Monitor for integration once API matures. Open-source philosophy aligns with Causal Atlas values. Could provide the most timely disease event signals.

5. **US-specific analysis (Delphi Epidata):** Use for high-resolution US disease signals if doing US-focused case studies.

### Spatial Resolution Challenge

All disease data sources operate at **country or subnational administrative level**, not grid-cell level. To align with the PRIO-GRID 0.5-degree spatial backbone:

- Country-level data: Assign uniform values to all grid cells within a country (crude but common approach)
- Subnational data (GBD 660 locations): Assign to grid cells within subnational boundaries
- Event data (DONs, ProMED): Geocode to coordinates where possible, then assign to nearest PRIO-GRID cell
- Consider population-weighted downscaling for indicators like disease incidence

### Temporal Resolution Challenge

Most structured disease data is **annual**, while Causal Atlas targets **monthly** primary resolution:

- GHO and GBD provide only annual data — cannot support monthly lag analysis
- DON event data provides precise dates, enabling monthly or even weekly aggregation
- ProMED/BEACON provide event-level timestamps
- For monthly analysis, event-based sources (DONs, BEACON) are more useful than aggregate indicator sources (GHO, GBD)
- Monthly disease data for specific diseases may be available from national surveillance systems (e.g., IHR weekly reports, national malaria programs)

### Priority Actions

1. **Immediately usable:** WHO GHO OData API for annual country-level indicators (no auth needed)
2. **High value, manual effort:** IHME GBD CSV downloads for disease burden estimates
3. **Structured event data:** CGHSS DON database (GitHub, ready to use) for outbreak event timeline analysis
4. **Watch and integrate:** BEACON as it matures in 2025-2026
5. **Investigate:** Whether the upcoming WHO OData API replacement (post-2025 deprecation) offers improvements
6. **Consider:** National-level monthly surveillance data from WHO IHR or disease-specific programs for higher temporal resolution

---

## Sources

### WHO GHO
- WHO GHO Portal: https://www.who.int/data/gho
- GHO OData API documentation: https://www.who.int/data/gho/info/gho-odata-api
- GHO Indicator Metadata Registry: https://www.who.int/data/gho/indicator-metadata-registry
- WHO Copyright Policy: https://www.who.int/about/policies/publishing/copyright
- Python GHO API example: https://gist.github.com/rruntsch/fbc05a837dc9098219ff4a4e98a5f3c7
- `apidatawho` PyPI package: https://pypi.org/project/apidatawho/

### ProMED
- ProMED website: https://www.promedmail.org/
- ISID Surveillance: https://isid.org/surveillance/
- ISID Future of ProMED: https://isid.org/futureofpromed/
- EcoHealth Alliance GRITS scraper: https://github.com/ecohealthalliance/grits-api/blob/master/scraper/scrape_promed.py
- Lyon et al. (2021), "Using Text Mining to Track Outbreak Trends in Global Surveillance," JRSS Series A: https://academic.oup.com/jrsssa/article/184/4/1245/7068837
- Harvesting data from ProMED-mail: https://www.ijidonline.com/article/S1201-9712(16)31497-7/fulltext
- STAT News, ProMED crisis (2023): https://www.statnews.com/2023/08/03/promed-early-warning-system-on-disease-outbreaks-appears-near-collapse/

### IHME GBD
- GBD Results Tool: https://vizhub.healthdata.org/gbd-results/
- GBD 2023 Data Resources: https://ghdx.healthdata.org/gbd-2023
- IHME Data Access: https://www.healthdata.org/data-tools-practices/data-access
- GBD Data and Tools Guide: https://www.healthdata.org/research-analysis/about-gbd/gbd-data-and-tools-guide
- IHME Terms and Conditions: https://www.healthdata.org/data-tools-practices/data-practices/terms-and-conditions
- `gbd_mapping` Python package: https://github.com/ihmeuw/gbd_mapping

### WHO DONs
- WHO DON page: https://www.who.int/emergencies/disease-outbreak-news
- WHO DON API documentation: https://www.who.int/api/news/diseaseoutbreaknews/sfhelp
- CGHSS DON database (1996-2019): https://github.com/cghss/dons
- CGHSS DON database (2020-2023): https://github.com/cghss/dons2
- Epidemiological Knowledge Graph from DONs (2025): https://www.nature.com/articles/s41597-025-05276-2

### HealthMap and BEACON
- HealthMap: https://healthmap.org/
- HealthMap PMC overview: https://pmc.ncbi.nlm.nih.gov/articles/PMC2274789/
- BEACON launch press release (April 2025): https://www.bu.edu/ceid/2025/04/23/press-release-infectious-disease-surveillance-platform-beacon-launches-as-a-new-open-source-global-resource/
- BEACON publication, Journal of Infectious Diseases: https://academic.oup.com/jid/article/233/2/e287/8407011
- WBUR article on BEACON (September 2025): https://www.wbur.org/news/2025/09/12/boston-ai-biothreat-tracker-beacon-cdc-diseases-global-health

### Delphi Epidata
- Delphi Epidata API: https://cmu-delphi.github.io/delphi-epidata/
- GitHub: https://github.com/cmu-delphi/delphi-epidata

### CDC NNDSS
- NNDSS data tables: https://www.cdc.gov/nndss/infectious-disease/index.html
- CDC WONDER: https://wonder.cdc.gov/nndss.html

### Climate-Disease Causal Research
- Causal inference for climate-infectious disease: https://www.nature.com/articles/s41559-024-02594-3
- Climate change and infectious diseases: https://pmc.ncbi.nlm.nih.gov/articles/PMC6974868/
- Climate-driven early warning systems for infectious disease: https://www.sciencedirect.com/science/article/pii/S0013935124004729
- COVID-19 and conflict risk under climate change: https://pmc.ncbi.nlm.nih.gov/articles/PMC10256592/

---

## 11. WHO EWARS (Early Warning, Alert and Response System)

### Overview

EWARS is WHO's deployable disease surveillance system designed for emergency settings — conflict zones, post-disaster areas, refugee camps — where routine health surveillance has broken down.

- **URL:** https://www.who.int/emergencies/surveillance/early-warning-alert-and-response-system-ewars/
- **Operator:** WHO Health Emergencies Programme
- **Deployment:** Can be set up within **48 hours** of an emergency declaration
- **Status:** Operational system deployed in multiple crises

### How EWARS Works

1. **Configuration:** Disease list and alert thresholds are defined for the specific emergency (e.g., cholera, measles, acute watery diarrhea)
2. **Data collection:** Health facilities report cases via EWARS mobile app (online/offline capable)
3. **Two reporting streams:**
   - **Immediate alerts:** Triggered when a single case of a notifiable disease (e.g., cholera, Ebola) is reported
   - **Weekly reports:** Aggregated case counts by disease, site, age group, and sex
4. **Alert management:** Automatic threshold-based alerts trigger SMS/email notifications
5. **Response:** Rapid Response Teams investigate alerts, classify risk, and initiate response

### Diseases Under Surveillance

EWARS typically monitors 10-15 priority diseases per deployment, including:
- Acute watery diarrhea / cholera
- Acute bloody diarrhea / dysentery
- Suspected measles
- Acute flaccid paralysis (polio indicator)
- Acute jaundice syndrome (hepatitis)
- Meningitis
- Acute hemorrhagic fever syndrome (Ebola, Marburg indicators)
- Severe acute respiratory infection (SARI)
- Acute malnutrition
- Malaria (in endemic areas)

### EWARS Deployments (Selected)

| Crisis | Year | Context |
|---|---|---|
| **Rohingya refugee crisis, Bangladesh** | 2017–present | 900,000+ refugees in Cox's Bazar |
| **Syria crisis** | 2013–present | Conflict-affected areas |
| **Yemen crisis** | 2016–present | Cholera outbreak surveillance |
| **Cyclone Idai, Mozambique** | 2019 | Post-disaster surveillance |
| **Ukraine conflict** | 2022–present | Conflict-disrupted health system |
| **Sudan crisis** | 2023–present | Conflict and displacement |

### Data Access

**EWARS data is NOT publicly accessible.** It is shared only with:
- WHO country offices and headquarters
- Ministry of Health of the affected country
- Humanitarian health cluster partners (on a need-to-know basis)

Weekly bulletins may be published for some deployments (e.g., Syria EWARN bulletins via WHO EMRO: https://www.emro.who.int/syr/publications-other/ewars-weekly-bulletin.html), but raw data is not released.

### Relevance to Causal Atlas

EWARS is the most granular disease surveillance data available for emergency settings, but its restricted access limits direct use. However:
- **Aggregated EWARS data** sometimes appears in WHO situation reports and humanitarian bulletins
- **The EWARS framework** informs what diseases to track in crisis contexts
- **Future possibility:** Advocacy for open data sharing from EWARS deployments could significantly enhance Causal Atlas's disease layer in conflict-affected regions

---

## 12. WHO IHR Monitoring and Evaluation Framework

### International Health Regulations (2005)

The IHR (2005) is a binding international legal instrument requiring all 196 signatory states to develop core public health capacities for detecting, assessing, reporting, and responding to public health events.

### IHR Monitoring Tools

| Tool | Type | Frequency | Coverage | Public? |
|---|---|---|---|---|
| **SPAR** (States Parties Self-Assessment Annual Reporting) | Self-assessment | Annual (mandatory) | 196 countries | Yes |
| **JEE** (Joint External Evaluation) | External evaluation | Every ~5 years (voluntary) | 130+ countries evaluated | Yes |
| **AAR** (After Action Review) | Post-event review | After significant events | Variable | Sometimes |
| **Simulation Exercises** | Tabletop/functional exercises | Variable | Variable | Sometimes |

### SPAR (e-SPAR) — Detailed

The electronic SPAR (e-SPAR) is the primary quantitative tool for monitoring IHR implementation.

**Version:** SPAR 2nd edition (2021), expanded from the original version
**Capacities assessed:** 15 core capacities, 35 indicators
**Scale:** 1–5 per indicator (1 = no capacity, 5 = sustainable capacity)

| Capacity | Indicators |
|---|---|
| 1. Policy, legal and normative instruments | 2 |
| 2. IHR coordination and national IHR focal point functions | 3 |
| 3. Financing | 1 |
| 4. Laboratory | 3 |
| 5. Surveillance | 3 |
| 6. Human resources | 2 |
| 7. Health emergency management | 3 |
| 8. Health service provision | 2 |
| 9. Infection prevention and control | 2 |
| 10. Risk communication and community engagement | 2 |
| 11. Points of entry | 2 |
| 12. Zoonotic events and the human-animal-environment interface | 2 |
| 13. Food safety | 2 |
| 14. Chemical events | 2 |
| 15. Radiation emergencies | 2 |

### Data Access

- **SPAR data:** Available through WHO GHO: https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/international-health-regulations-ihr
- **e-SPAR platform:** https://extranet.who.int/e-spar (requires WHO login for some features)
- **JEE reports:** Published on WHO website per country: https://www.who.int/emergencies/operations/international-health-regulations-monitoring-evaluation-framework/joint-external-evaluations

### Relevance to Causal Atlas

SPAR scores provide a **country-level health system preparedness indicator** that can serve as a moderating variable:
- Countries with low SPAR scores (weak surveillance, limited lab capacity) may experience worse disease outcomes after climate shocks or conflict
- SPAR scores can be used alongside WGI governance indicators as contextual variables
- The disconnect between SPAR self-assessment and JEE external evaluation can indicate governance quality

---

## 13. Wastewater Surveillance as Emerging Data Source

### Overview

Wastewater-based epidemiology (WBE) has emerged post-COVID as a powerful tool for community-level pathogen surveillance. It provides early, non-invasive detection of pathogen circulation at the population level.

### How It Works

1. **Sample collection:** Wastewater is collected from municipal sewage systems, treatment plants, or specific buildings
2. **Laboratory analysis:** RT-qPCR or sequencing detects pathogen genetic material (RNA/DNA)
3. **Normalisation:** Pathogen signal is normalised against population markers (e.g., PMMoV for SARS-CoV-2) or flow rate
4. **Trend analysis:** Concentration trends indicate rising or declining community infection

### Current Global Infrastructure

| Network | Scope | Pathogens | Notes |
|---|---|---|---|
| **US CDC National Wastewater Surveillance System (NWSS)** | ~1,400 US sites | SARS-CoV-2, RSV, Influenza A, Avian H5, Mpox | Most mature system; public dashboard |
| **GLOWACON** (Global Consortium for WES) | International | Multiple | WHO-supported; connecting national programs |
| **European surveillance** | EU/EEA | SARS-CoV-2, Polio | EU Recommendation for WBE since 2021 |
| **Aircraft wastewater** | Emerging concept | Multiple | Monitoring international travel routes |

### Data Access

- **US CDC NWSS Dashboard:** https://www.cdc.gov/nwss/ — publicly accessible, county-level trends
- **No global standardised database exists** as of March 2025
- **Research datasets:** Published alongside individual studies; no unified API

### Relevance to Causal Atlas

Wastewater surveillance is in its early stages as a global data source. For Causal Atlas:
- **Not yet ready** for systematic integration due to fragmented, non-standardised data
- **Watch for:** GLOWACON standardisation efforts and potential WHO-managed global database
- **Potential future use:** Early pathogen detection signals that precede clinical case reporting by 1-2 weeks
- **Key advantage:** Captures asymptomatic infections missed by clinical surveillance

---

## 14. Genomic Surveillance Data (GISAID)

### Overview

GISAID (Global Initiative on Sharing All Influenza Data) is the world's largest repository of pathogen genomic sequences, critical for tracking pathogen evolution and emergence.

| Property | Detail |
|---|---|
| **URL** | https://gisaid.org/ |
| **Founded** | 2008 (originally for influenza; expanded to SARS-CoV-2 in 2020) |
| **Pathogens covered** | Influenza, SARS-CoV-2, RSV, Mpox, Dengue, Chikungunya, Zika |
| **Databases** | EpiFlu (influenza), EpiCoV (SARS-CoV-2), EpiRSV, EpiPox, EpiArbo |
| **Total sequences** | 16+ million SARS-CoV-2 sequences (largest COVID genomic database) |
| **Contributors** | Labs and public health agencies in 190+ countries |

### Data Access Model

GISAID uses a unique **"share with care"** model:
- **Registration required:** Users must agree to the GISAID Database Access Agreement (DAA)
- **No open bulk download:** Data cannot be redistributed freely
- **Attribution required:** Contributors must be acknowledged
- **API access:** Available for authenticated users with institutional affiliation
- **EpiCoV API:** Provides programmatic access to SARS-CoV-2 metadata and sequences

### Relevance to Causal Atlas

Genomic surveillance data is **not directly suitable** for spatiotemporal causal analysis at the PRIO-GRID level because:
- Sequencing coverage is extremely uneven (dense in wealthy countries, sparse elsewhere)
- Data represents variants/lineages, not case counts
- GISAID's access restrictions prevent free redistribution

However, **aggregated genomic surveillance metrics** could be useful:
- **Variant emergence detection** as an early warning signal
- **Phylogeographic analysis** for tracking pathogen spread patterns
- **Country-level sequencing coverage** as a health system capacity indicator
