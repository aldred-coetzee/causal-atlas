# HDX HAPI (Humanitarian API) — Deep Dive

> Last updated: March 2025

## 1. Overview

**HDX HAPI** (Humanitarian API) is a REST API that provides standardised, programmatic access to humanitarian indicator data from multiple authoritative sources. Unlike the HDX platform's CKAN-based catalogue API (which returns dataset metadata and file links), HAPI delivers actual data values — population counts, conflict event tallies, food security classifications, displacement figures, and more — in a single, consistently structured interface.

**Maintained by:** The Centre for Humanitarian Data, part of the United Nations Office for the Coordination of Humanitarian Affairs (OCHA). Contact: hdx@un.org.

**Status:** Beta (as of March 2025). Actively seeking user feedback and expanding coverage.

**Launch timeline:**
- Initial beta release: 2024 (v1 endpoints)
- v2 endpoint reorganisation: February 2025, aligning endpoints with HDX data grid categories
- v1 endpoints remain available alongside v2
- Rainfall / climate endpoint added: March 2025

**Key partners / data providers:** ACLED, INFORM, IOM (DTM), OCHA (FTS, HPC Tools, 3W), UNHCR, WFP, IPC, Oxford Poverty and Human Development Initiative (OPHI).

**Homepage:** https://data.humdata.org/hapi
**API documentation / sandbox:** https://hapi.humdata.org/docs
**ReadTheDocs guide:** https://hdx-hapi.readthedocs.io/en/latest/
**OpenAPI spec:** https://hapi.humdata.org/openapi.json
**Terms of use:** https://data.humdata.org/hapi/terms
**Data availability dashboard:** https://data.humdata.org/hapi#data-availability

---

## 2. Coverage

### Spatial extent

HAPI focuses on countries with a Humanitarian Response Plan (HRP) or included in the Global Humanitarian Overview (GHO), but also includes additional countries where upstream data exists (e.g., UNHCR refugee data covers globally, INFORM risk covers all countries). Individual endpoints expose `has_hrp` and `in_gho` boolean filters to distinguish.

Coverage varies by theme — conflict events (ACLED) cover globally from 1997 onward, while operational presence may only have the current year. The live data availability table at https://data.humdata.org/hapi#data-availability shows country-by-theme coverage.

### Temporal range

| Theme | Temporal depth |
|---|---|
| Conflict events (ACLED) | 1997–present |
| Refugees & persons of concern (UNHCR) | 2001–present |
| Returnees (UNHCR) | 2001–present |
| IDPs (IOM DTM) | 2010–present |
| Humanitarian needs (HNO) | 2024–present |
| Food security (IPC/CH) | Varies by country |
| Food prices (WFP) | Varies, often 2010+ |
| Poverty rate (OPHI MPI) | Varies by survey year |
| Operational presence (3W) | Current year typically |
| Funding (FTS) | Varies by appeal |
| National risk (INFORM) | Annual |
| Population (CODs) | Single reference year |
| Rainfall (CHIRPS via WFP) | Admin 1: past 5 years; Admin 2: past 1 year |

### Data themes

HAPI organises data into five thematic categories plus metadata:

1. **Affected People** — IDPs, refugees, returnees, humanitarian needs
2. **Coordination & Context** — Operational presence (3W), funding, conflict events, national risk
3. **Food Security, Nutrition & Poverty** — IPC/CH food security, WFP food prices, MPI poverty rate
4. **Geography & Infrastructure** — Baseline population
5. **Climate** — Rainfall (CHIRPS)
6. **Metadata** — Locations, admin boundaries, sectors, organisations, currencies, commodities, markets, datasets, resources, data availability

---

## 3. Access

### Base URLs

| Version | Base URL |
|---|---|
| v1 | `https://hapi.humdata.org/api/v1/` |
| v2 (current) | `https://hapi.humdata.org/api/v2/` |

Both versions are live. v2 reorganised endpoint paths to match HDX data grid categories.

### Authentication

HAPI does not require a traditional API key or user account. Instead, it requires an **app identifier** — a base64-encoded string combining your application name and email address.

**Generating an app identifier:**

```
GET https://hapi.humdata.org/api/v2/encode_app_identifier?application=my_app_name&email=user@example.com
```

Response:
```json
{
  "encoded_app_identifier": "bXlfYXBwX25hbWU6dXNlckBleGFtcGxlLmNvbQ=="
}
```

The identifier is simply `base64("app_name:email")`.

**Supplying the identifier:** Include it as either:
- Query parameter: `?app_identifier=bXlfYXBwX25hbWU6dXNlckBleGFtcGxlLmNvbQ==`
- HTTP header: `X-HDX-HAPI-APP-IDENTIFIER: bXlfYXBwX25hbWU6dXNlckBleGFtcGxlLmNvbQ==`

### Rate limits

- **1 request per second** (documented in terms of use)
- Maximum **10,000 records per response** (use `offset` and `limit` for pagination)

### Response formats

- **JSON** (default): `output_format=json`
- **CSV**: `output_format=csv`

### Pagination

All data endpoints accept:
- `limit` — number of records to return (0–10,000; default 10,000)
- `offset` — starting position (default 0)

Paginate by incrementing `offset` by `limit` until the response returns fewer records than `limit`.

### Common query parameters (all data endpoints)

| Parameter | Type | Description |
|---|---|---|
| `app_identifier` | string | Required. Base64-encoded app name + email |
| `output_format` | enum | `json` or `csv` (default: `json`) |
| `limit` | int | Max records (default/max: 10,000) |
| `offset` | int | Pagination offset (default: 0) |
| `location_code` | string | ISO 3166-1 alpha-3 country code |
| `location_name` | string | Country name (case-insensitive wildcard) |
| `admin1_code` | string | Admin level 1 p-code |
| `admin1_name` | string | Admin level 1 name |
| `admin2_code` | string | Admin level 2 p-code |
| `admin2_name` | string | Admin level 2 name |
| `admin_level` | int | 0, 1, or 2 |
| `has_hrp` | bool | Country has Humanitarian Response Plan |
| `in_gho` | bool | Country in Global Humanitarian Overview |
| `start_date` | string | Filter by reference period start |
| `end_date` | string | Filter by reference period end |

Date formats accepted: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS`.

String filters are **case-insensitive wildcards**.

### Error codes

| Code | Meaning |
|---|---|
| 400 | Bad request |
| 422 | Validation error (invalid parameters) |
| 500 | Internal server error |

---

## 4. Schema — Available Themes and Endpoints

### 4.1 Affected People

#### 4.1.1 IDPs (Internally Displaced Persons)

**Endpoint (v2):** `GET /api/v2/affected-people/idps`

**Source:** IOM Displacement Tracking Matrix (DTM)

**Update frequency:** Weekly; monthly time series back to 2010

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `reporting_round` | int | DTM reporting round number |
| `assessment_type` | enum | `BA` (Baseline Assessment), `ETT` (Emergency Tracking Tool), `SA` (Site Assessment) |
| `operation` | string | DTM operation name |
| `population` | int | Number of IDPs |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level (0, 1, or 2) |

**Usage note:** To get annual IDP figures, aggregate only the most recent reporting round per operation. Do not sum across rounds as they overlap temporally.

**Query-specific filters:** `location_code`, `admin1_code`, `admin2_code`, `admin_level`, `has_hrp`, `in_gho`, `start_date`, `end_date`

#### 4.1.2 Refugees & Persons of Concern

**Endpoint (v2):** `GET /api/v2/affected-people/refugees-persons-of-concern`

**Source:** UNHCR global statistics

**Update frequency:** Annual; time series from 2001

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `population_group` | enum | See population group codes below |
| `gender` | enum | `f`, `m`, `x`, `u`, `o`, `all` |
| `age_range` | string | Format `[min]-[max]` or `[min]+`; `all` = no disaggregation |
| `min_age` | int | Minimum age in range |
| `max_age` | int | Maximum age in range |
| `population` | int | Number of persons |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `origin_location_code` | string | Origin country ISO-3 |
| `origin_location_name` | string | Origin country name |
| `origin_location_ref` | int | Internal location reference |
| `asylum_location_code` | string | Asylum country ISO-3 |
| `asylum_location_name` | string | Asylum country name |
| `asylum_location_ref` | int | Internal location reference |

**Population group codes:**

| Code | Meaning |
|---|---|
| `REF` | Refugees |
| `ROC` | Refugees in refugee-like situation |
| `ASY` | Asylum seekers |
| `OIP` | Others in need of international protection |
| `IDP` | Internally displaced persons |
| `IOC` | IDPs in IDP-like situation |
| `STA` | Stateless persons |
| `OOC` | Others of concern |
| `HST` | Host community |
| `RST` | Resettled refugees |
| `NAT` | Naturalized refugees |

**Query-specific filters:** `population_group`, `gender`, `age_range`, `population_min`, `population_max`, `origin_location_code`, `origin_location_name`, `origin_has_hrp`, `origin_in_gho`, `asylum_location_code`, `asylum_location_name`, `asylum_has_hrp`, `asylum_in_gho`, `start_date`, `end_date`

#### 4.1.3 Returnees

**Endpoint (v2):** `GET /api/v2/affected-people/returnees`

**Source:** UNHCR (preferred source; IOM used where UNHCR unavailable)

**Update frequency:** Annual; time series from 2001

**Response fields:** Same structure as refugees endpoint. Only includes `RET` (returned refugees) and `RDP` (returned IDPs) population groups.

**Query-specific filters:** Same as refugees endpoint.

#### 4.1.4 Humanitarian Needs

**Endpoint (v2):** `GET /api/v2/affected-people/humanitarian-needs`

**Source:** OCHA HPC Tools API (Humanitarian Needs Overview data)

**Update frequency:** Annual (starting 2024)

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `category` | string | Combination of gender, age, disability, population group |
| `sector_code` | string | Humanitarian sector code |
| `sector_name` | string | Humanitarian sector name |
| `population_status` | enum | `in-need`, `targeted`, `affected`, `reached` |
| `population` | int | Number of persons |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level |

**Critical usage note:** People In Need (PIN) values must **not** be summed across sectors, as populations overlap between sectors. Intersectoral PIN is the correct figure for total people in need.

**Query-specific filters:** `category`, `sector_code`, `sector_name`, `population_status`, `population_min`, `population_max`, `location_code`, `admin1_code`, `admin2_code`, `admin_level`, `has_hrp`, `in_gho`, `start_date`, `end_date`

---

### 4.2 Coordination & Context

#### 4.2.1 Operational Presence (3W — Who does What Where)

**Endpoint (v2):** `GET /api/v2/coordination-context/operational-presence`

**Source:** OCHA country and regional offices

**Update frequency:** Irregular (quarterly or annually, depending on country)

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `org_acronym` | string | Organisation acronym |
| `org_name` | string | Organisation full name |
| `org_type_code` | string | Organisation type code |
| `sector_code` | string | Sector code |
| `sector_name` | string | Sector name |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level |

**Usage note:** Organisation naming is not guaranteed consistent across time periods due to naming variations and institutional changes.

**Query-specific filters:** `sector_code`, `sector_name`, `org_acronym`, `org_name`, `location_code`, `admin1_code`, `admin2_code`, `admin_level`, `has_hrp`, `in_gho`, `start_date`, `end_date`

#### 4.2.2 Funding

**Endpoint (v2):** `GET /api/v2/coordination-context/funding`

**Source:** OCHA Financial Tracking Service (FTS)

**Update frequency:** Annually

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `appeal_code` | string | FTS appeal identifier |
| `appeal_name` | string | Appeal name |
| `appeal_type` | string | Type (flash appeal, HRP, etc.) |
| `requirements_usd` | float | Funding requirements in USD |
| `funding_usd` | float | Funding received in USD |
| `funding_pct` | float | Percentage of requirements funded |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |

**Limitation:** Currently captures only funding associated with appeals; non-appeal funding will be added later.

**Query-specific filters:** `appeal_code`, `appeal_type`, `location_code`, `location_name`, `has_hrp`, `in_gho`, `start_date`, `end_date`

#### 4.2.3 Conflict Events

**Endpoint (v2):** `GET /api/v2/coordination-context/conflict-events`

**Source:** ACLED (Armed Conflict Location & Event Data Project)

**Update frequency:** Weekly updates; data aggregated monthly per administrative region

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `event_type` | enum | `civilian_targeting`, `demonstration`, `political_violence` |
| `events` | int | Number of events in period |
| `fatalities` | int | Number of fatalities in period |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level |

**Usage notes:**
- Event categories are **not mutually exclusive** — events may be counted under multiple types.
- Data is aggregated to monthly counts per admin area. For daily granular data, a separate ACLED registration is required.
- Temporal coverage: 1997–present.

**Query-specific filters:** `event_type`, `location_code`, `admin1_code`, `admin2_code`, `admin_level`, `has_hrp`, `in_gho`, `start_date`, `end_date`

#### 4.2.4 National Risk

**Endpoint (v2):** `GET /api/v2/coordination-context/national-risk`

**Source:** INFORM Risk Index

**Update frequency:** Annually

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `risk_class` | int | Risk classification (1–5) |
| `global_rank` | int | Global ranking |
| `overall_risk` | float | Composite risk score (0–10) |
| `hazard_exposure_risk` | float | Hazard & exposure dimension (0–10) |
| `vulnerability_risk` | float | Vulnerability dimension (0–10) |
| `coping_capacity_risk` | float | Lack of coping capacity dimension (0–10) |
| `meta_missing_indicators_pct` | float | Percentage of missing indicators |
| `meta_avg_recentness_years` | float | Average data recentness in years |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |

**Risk classes:**

| Class | Label | Score range |
|---|---|---|
| 1 | Very Low | 0–1.9 |
| 2 | Low | 2.0–3.4 |
| 3 | Medium | 3.5–4.9 |
| 4 | High | 5.0–6.4 |
| 5 | Very High | 6.5–10.0 |

**Query-specific filters:** `risk_class`, `global_rank_min`, `global_rank_max`, `overall_risk_min`, `overall_risk_max`, `hazard_exposure_risk_min`, `hazard_exposure_risk_max`, `vulnerability_risk_min`, `vulnerability_risk_max`, `coping_capacity_risk_min`, `coping_capacity_risk_max`, `location_code`, `has_hrp`, `in_gho`, `start_date`, `end_date`

---

### 4.3 Food Security, Nutrition & Poverty

#### 4.3.1 Food Security (IPC/CH)

**Endpoint (v2):** `GET /api/v2/food-security-nutrition-poverty/food-security`

**Source:** Integrated Food Security Phase Classification (IPC). Includes Cadre Harmonise (CH) data for Sahel and West Africa, aligned with IPC standards.

**Update frequency:** As needed (follows IPC analysis cycles)

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `ipc_phase` | enum | IPC severity phase (see below) |
| `ipc_type` | enum | IPC projection type |
| `population_in_phase` | int | People in this phase |
| `population_fraction_in_phase` | float | Fraction of total population |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level (0, 1, or 2) |

**IPC phase codes:**

| Code | Meaning |
|---|---|
| `1` | None / Minimal |
| `2` | Stressed |
| `3` | Crisis |
| `4` | Emergency |
| `5` | Catastrophe / Famine |
| `3+` | In Need of Action (aggregation of phases 3, 4, 5) |
| `all` | Total analysed population |

**Query-specific filters:** `ipc_phase`, `ipc_type`, `location_code`, `admin1_code`, `admin2_code`, `admin_level`, `has_hrp`, `in_gho`, `start_date`, `end_date`

#### 4.3.2 Food Prices & Market Monitor

**Endpoint (v2):** `GET /api/v2/food-security-nutrition-poverty/food-prices-market-monitor`

**Source:** World Food Programme Price Database

**Coverage:** ~98 countries, ~3,000 markets

**Update frequency:** Weekly; monthly data resolution

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `commodity_code` | string | Unique commodity identifier |
| `commodity_name` | string | Food item name |
| `commodity_category` | string | Food group (cereals, meat, dairy, oils, vegetables, etc.) |
| `price_flag` | string | Pre-processing characteristics |
| `price_type` | enum | `Farm Gate`, `Retail`, `Wholesale` |
| `price` | float | Commodity cost |
| `unit` | string | Measurement unit (weight or number) |
| `currency_code` | string | ISO-4217 currency code |
| `market_code` | string | Market identifier |
| `market_name` | string | Market name |
| `lat` | float | Market latitude |
| `lon` | float | Market longitude |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level |

**Commodity categories:** Cereals and tubers, meat/fish/eggs, milk and dairy, oil and fats, pulses and nuts, vegetables and fruits, miscellaneous food, non-food.

**Query-specific filters:** `market_code`, `market_name`, `commodity_code`, `commodity_name`, `commodity_category`, `price_flag`, `price_type`, `price_min`, `price_max`, `has_hrp`, `in_gho`

#### 4.3.3 Poverty Rate

**Endpoint (v2):** `GET /api/v2/food-security-nutrition-poverty/poverty-rate`

**Source:** Oxford Poverty and Human Development Initiative (OPHI) — Global Multidimensional Poverty Index (MPI)

**Coverage:** 100+ developing countries. National and admin 1 levels only.

**Update frequency:** Annually (tied to survey availability)

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `mpi` | float | Multidimensional Poverty Index (fraction; product of headcount ratio and intensity) |
| `headcount_ratio` | float | Percentage deprived in 33%+ of weighted indicators |
| `intensity_of_deprivation` | float | Average proportion of deprivation indicators (percentage) |
| `vulnerable_to_poverty` | float | Percentage deprived in 20–33% of indicators |
| `in_severe_poverty` | float | Percentage deprived in 50%+ of indicators |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin_level` | int | Administrative level (0 or 1 only) |

**Note:** MPI assesses deprivation across health, education, and living standards dimensions. Not available at admin 2 level.

---

### 4.4 Geography & Infrastructure

#### 4.4.1 Baseline Population

**Endpoint (v2):** `GET /api/v2/geography-infrastructure/population`

**Source:** Common Operational Datasets (CODs) from UNFPA and OCHA country offices — "Global Subnational Population Statistics" on HDX.

**Update frequency:** Annually (single reference year per country; no time series)

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `gender` | enum | `f`, `m`, `x`, `all` |
| `age_range` | string | Age grouping; `all` = no disaggregation |
| `min_age` | int | Minimum age |
| `max_age` | int | Maximum age |
| `population` | int | Population count |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | Admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | Admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level (0, 1, or 2) |

**Usage notes:**
- Data is reshaped from wide format (demographic columns) into long format with `gender`, `age_range`, and `population` rows.
- Age disaggregation is inconsistent across countries.
- Higher-level aggregations come from source data, not computed by HAPI.

---

### 4.5 Climate

#### 4.5.1 Rainfall

**Endpoint (v2):** `GET /api/v2/climate/rainfall` (added March 2025)

**Source:** WFP Rainfall Indicators at Subnational Level, derived from CHIRPS v2 (Climate Hazards Group InfraRed Precipitation with Station data)

**Update frequency:** Every two weeks; dekadal (10-day) measurements

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `resource_hdx_id` | UUID | HDX resource identifier |
| `provider_admin1_code` | string | Admin 1 code from WFP (may differ from COD) |
| `provider_admin2_code` | string | Admin 2 code from WFP |
| `aggregation_period` | enum | Time aggregation period |
| `rainfall` | float | Precipitation in millimetres |
| `rainfall_long_term_average` | float | Long-term average rainfall (mm), baseline 1989–2018 |
| `rainfall_anomaly_pct` | float | Deviation from long-term average (percentage) |
| `number_pixels` | int | Number of source raster pixels used in calculation |
| `version` | enum | `FINAL`, `FORECAST`, `PRELIMINARY` |
| `reference_period_start` | date | Start of reference period |
| `reference_period_end` | date | End of reference period |
| `location_code` | string | ISO-3 country code |
| `location_name` | string | Country name |
| `admin1_code` | string | COD admin 1 p-code |
| `admin1_name` | string | Admin 1 name |
| `admin2_code` | string | COD admin 2 p-code |
| `admin2_name` | string | Admin 2 name |
| `admin_level` | int | Administrative level |

**Coverage limitations:**
- **Admin 1 level:** All countries, past 5 years
- **Admin 2 level:** Only HRP/GHO countries, past 1 year

**Important caveat:** WFP boundary definitions do not perfectly align with COD (Common Operational Dataset) boundaries. The `provider_admin1_code` and `provider_admin2_code` fields reflect WFP's own admin codes, while `admin1_code` and `admin2_code` are the matched COD p-codes.

---

### 4.6 Metadata Endpoints

| Endpoint (v1 paths; v2 equivalent under same structure) | Description |
|---|---|
| `/api/v1/metadata/location` | Countries with p-codes and ISO-3 codes |
| `/api/v1/metadata/admin1` | Admin level 1 divisions with p-codes and parent location references |
| `/api/v1/metadata/admin2` | Admin level 2 divisions with p-codes and hierarchical references |
| `/api/v1/metadata/currency` | ISO-4217 currency codes (from WFP VAM) |
| `/api/v1/metadata/org` | Organisations with normalised names, acronyms, type codes |
| `/api/v1/metadata/org_type` | Organisation type codes from OCHA Digital Services |
| `/api/v1/metadata/sector` | Sector codes and names from Global Coordination Groups |
| `/api/v1/metadata/wfp_commodity` | Food commodities with categories |
| `/api/v1/metadata/wfp_market` | Market locations with geographic coordinates |
| `/api/v1/metadata/dataset` | Dataset metadata linking to HDX CKAN records |
| `/api/v1/metadata/resource` | Resource metadata with download URLs and update dates |
| `/api/v1/metadata/data_availability` | Data availability by sub-category and admin level |

---

## 5. Spatial Detail

### Location encoding

HAPI uses a hierarchical system based on **p-codes** (place codes) from Common Operational Datasets (CODs):

- **Admin level 0 (country):** ISO 3166-1 alpha-3 codes (e.g., `AFG`, `SOM`, `YEM`)
- **Admin level 1 (province/state):** COD p-codes (e.g., `AF01` for Kabul province)
- **Admin level 2 (district):** COD p-codes (e.g., `AF0101` for a district within Kabul)

Country names follow the **UN M49 Standard** short name convention.

### P-code matching

HAPI uses a **length-matching algorithm** to handle p-code format variations across countries. Administrative boundary entries are unique only when combined with their reference period dates (boundaries can change over time).

### Admin level availability by theme

| Theme | Admin 0 | Admin 1 | Admin 2 |
|---|---|---|---|
| IDPs | Yes | Yes | Yes |
| Refugees | Yes (origin/asylum) | No | No |
| Returnees | Yes (origin/asylum) | No | No |
| Humanitarian needs | Yes | Yes | Yes |
| Operational presence | Yes | Yes | Yes |
| Funding | Yes | No | No |
| Conflict events | Yes | Yes | Yes |
| National risk | Yes | No | No |
| Food security (IPC) | Yes | Yes | Yes |
| Food prices | Yes | Yes | Yes |
| Poverty rate | Yes | Yes | No |
| Population | Yes | Yes | Yes |
| Rainfall | No | Yes | Yes (HRP only) |

---

## 6. Temporal Detail — Update Frequency per Theme

| Theme | Source update cycle | HAPI refresh | Temporal granularity |
|---|---|---|---|
| IDPs | Weekly | Daily | Monthly time series |
| Refugees | Annual | Daily | Annual |
| Returnees | Annual | Daily | Annual |
| Humanitarian needs | Annual | Daily | Annual |
| Operational presence | Quarterly–annual | Daily | Period-based |
| Funding | Annual | Daily | Annual |
| Conflict events | Weekly | Daily | Monthly aggregation |
| National risk | Annual | Daily | Annual |
| Food security (IPC) | Per analysis cycle | Daily | Analysis period |
| Food prices | Weekly | Daily | Monthly |
| Poverty rate | Per survey | Daily | Survey year |
| Population | Annual | Daily | Single year |
| Rainfall | Bi-weekly | Daily | Dekadal (10-day) |

HAPI pulls from upstream sources daily. The "daily" refresh refers to the pipeline run frequency, not that source data changes daily.

---

## 7. Quality — Known Issues and Data Completeness

### General issues

- **Beta status:** The API is still in beta. Endpoints, field names, and behaviour may change.
- **Coverage gaps:** Not all countries have data for all themes. The data availability table should be checked before assuming coverage.
- **Historical depth varies dramatically:** Conflict data goes back to 1997; humanitarian needs only to 2024; operational presence often has only the current year.

### Theme-specific quality notes

- **IDPs:** Overlapping reporting rounds can lead to double-counting if not handled correctly. Only use the latest round per operation for annual totals.
- **Refugees:** `all` values in gender/age fields indicate no disaggregation was available, not that all categories were summed.
- **Humanitarian needs:** PIN values must not be summed across sectors due to population overlap.
- **Conflict events:** Event types are not mutually exclusive — an incident can appear under multiple categories. Monthly aggregation means daily patterns are lost.
- **Food prices:** Price comparability across markets is limited due to different units, currencies, and commodity varieties.
- **Operational presence:** Organisation naming inconsistencies over time make longitudinal analysis difficult.
- **Rainfall:** WFP admin boundaries do not perfectly match COD boundaries, introducing spatial misalignment.
- **Population:** Age disaggregation is inconsistent across countries. No time series — single snapshot per country.
- **Poverty rate:** Survey-based, so data may be several years old. Not available at admin 2 level.
- **Funding:** Only appeal-linked funding is included; bilateral and non-appeal funding is missing.

### Data completeness

The HAPI data availability endpoint (`/metadata/data_availability`) and the dashboard at https://data.humdata.org/hapi#data-availability provide programmatic and visual ways to check what data exists for each country and theme.

---

## 8. Licence

- **Platform content licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), except where otherwise noted by individual data providers
- **Rate limit:** 1 request per second
- **App identifier required:** For tracking and usage analytics (not authentication in the traditional sense)
- **Analytics:** OCHA logs API calls and uses Google Analytics, Mixpanel, and Hotjar for usage analysis. No personally identifying information is sent to these services.
- **Disclaimer:** Data does not represent the opinions of OCHA or the United Nations. No endorsement of territorial claims.
- **Individual dataset licences:** Some upstream datasets (e.g., ACLED) have their own licence terms that apply in addition to the CC BY 4.0 platform licence. Always check `resource_hdx_id` metadata for specific terms.

---

## 9. Interoperability

### P-code compatibility

HAPI's spatial framework is built on COD (Common Operational Dataset) p-codes, which are the standard location identifiers across the humanitarian data ecosystem. This means HAPI data is directly joinable with:

- **HDX datasets** that use COD p-codes (the vast majority of humanitarian datasets on HDX)
- **OCHA tools** (ReliefWeb, HPC Tools, Financial Tracking Service)
- **IPC/CH analyses** which report by COD admin regions
- **WFP VAM** food security assessments

### ISO-3 country codes

All country-level data uses ISO 3166-1 alpha-3 codes, compatible with virtually all international datasets including World Bank, FAO, WHO, UNHCR, and more.

### Links to other humanitarian datasets

- **ACLED:** HAPI's conflict data is a monthly aggregation of ACLED. For event-level data, use ACLED directly.
- **IPC/CH:** HAPI reproduces IPC phase classifications. The IPC's own API provides additional detail.
- **WFP food prices:** HAPI mirrors the WFP VAM food price database with standardised admin codes.
- **UNHCR:** Refugee and returnee data mirrors UNHCR's population statistics database.
- **IOM DTM:** IDP data comes from DTM. IOM's own API provides additional assessment detail.
- **INFORM:** Risk scores are from the INFORM Risk Index.
- **CHIRPS:** Rainfall data is CHIRPS v2, reprocessed by WFP per admin boundary.

### Relationship to HDX CKAN API

HAPI is complementary to (not a replacement for) the HDX CKAN API. The CKAN API provides dataset metadata, search, and file download URLs. HAPI provides the actual data values from curated datasets. The `resource_hdx_id` field in HAPI responses links back to the HDX CKAN resource, allowing you to retrieve full dataset metadata, provenance, and download the raw files.

### Mapping to PRIO-GRID

HAPI data is at **administrative boundary level**, not grid-cell level. To integrate with PRIO-GRID (0.5 degree cells), spatial interpolation or area-weighted disaggregation is needed. This is a common challenge — the PRIO-GRID project itself handles this for selected indicators. For Causal Atlas, admin-to-grid conversion is a key data integration task (see `research/06-data-integration.md`).

---

## 10. Python Access

### Option A: Direct HTTP requests (recommended for HAPI)

The `hdx-python-api` library (see below) is designed for the HDX CKAN platform, not specifically for HAPI. For HAPI, direct HTTP requests are the standard approach.

**Basic example with pagination:**

```python
import json
import time
from urllib import request, parse

# Generate or hardcode your app identifier
APP_IDENTIFIER = "bXlfYXBwX25hbWU6dXNlckBleGFtcGxlLmNvbQ=="

def fetch_hapi(theme, params, limit=1000):
    """Fetch all pages from a HAPI endpoint."""
    base_url = f"https://hapi.humdata.org/api/v2/{theme}"
    params["app_identifier"] = APP_IDENTIFIER
    params["output_format"] = "json"
    params["limit"] = limit

    all_results = []
    offset = 0

    while True:
        params["offset"] = offset
        query_string = parse.urlencode(params)
        url = f"{base_url}?{query_string}"

        with request.urlopen(url) as response:
            data = json.loads(response.read())
            results = data["data"]
            all_results.extend(results)

            if len(results) < limit:
                break

        offset += limit
        time.sleep(1)  # respect rate limit

    return all_results

# Example: Get conflict events for Somalia
events = fetch_hapi(
    "coordination-context/conflict-events",
    {"location_code": "SOM", "start_date": "2023-01-01"}
)

# Example: Get IPC food security data for Yemen
food_security = fetch_hapi(
    "food-security-nutrition-poverty/food-security",
    {"location_code": "YEM", "ipc_phase": "3+"}
)

# Example: Get IDPs for Afghanistan at admin 1 level
idps = fetch_hapi(
    "affected-people/idps",
    {"location_code": "AFG", "admin_level": "1"}
)

# Example: Get rainfall data
rainfall = fetch_hapi(
    "climate/rainfall",
    {"location_code": "ETH", "admin_level": "1"}
)
```

**Using the `requests` library with pandas:**

```python
import requests
import pandas as pd
import time

APP_IDENTIFIER = "bXlfYXBwX25hbWU6dXNlckBleGFtcGxlLmNvbQ=="
BASE = "https://hapi.humdata.org/api/v2"

def hapi_to_dataframe(theme, params, limit=10000):
    """Fetch HAPI data into a pandas DataFrame."""
    params.update({
        "app_identifier": APP_IDENTIFIER,
        "output_format": "json",
        "limit": limit,
    })

    frames = []
    offset = 0

    while True:
        params["offset"] = offset
        resp = requests.get(f"{BASE}/{theme}", params=params)
        resp.raise_for_status()
        data = resp.json()["data"]
        if not data:
            break
        frames.append(pd.DataFrame(data))
        if len(data) < limit:
            break
        offset += limit
        time.sleep(1)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# Get food prices for Nigeria
df = hapi_to_dataframe(
    "food-security-nutrition-poverty/food-prices-market-monitor",
    {"location_code": "NGA"}
)
print(df.head())
print(f"Total records: {len(df)}")
```

**CSV download (for bulk ingestion):**

```python
import requests

url = (
    "https://hapi.humdata.org/api/v2/coordination-context/conflict-events"
    "?output_format=csv"
    "&location_code=SOM"
    "&app_identifier=bXlfYXBwX25hbWU6dXNlckBleGFtcGxlLmNvbQ=="
    "&limit=10000"
)

resp = requests.get(url)
with open("somalia_conflict.csv", "w") as f:
    f.write(resp.text)
```

### Option B: hdx-python-api (for HDX platform, not HAPI specifically)

The `hdx-python-api` library is maintained by OCHA-DAP for interacting with the HDX CKAN platform — searching datasets, downloading files, pushing data. It is **not** a HAPI client, but useful for retrieving the raw dataset files that HAPI sources from.

- **PyPI:** https://pypi.org/project/hdx-python-api/
- **GitHub:** https://github.com/OCHA-DAP/hdx-python-api
- **Version (as of March 2025):** 6.6.5
- **Python requirement:** >= 3.10
- **Licence:** MIT
- **Install:** `pip install hdx-python-api`

```python
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

# Initialise with HDX production server
Configuration.create(
    hdx_site="prod",
    user_agent="causal_atlas",
    hdx_read_only=True,
)

# Search for HAPI-related datasets
datasets = Dataset.search_in_hdx("hapi", rows=10)
for ds in datasets:
    print(ds["name"], ds["title"])

# Get a specific dataset by name
dataset = Dataset.read_from_hdx("hdx-hapi-food-security")
resources = dataset.get_resources()
for r in resources:
    print(r["name"], r["url"])
```

---

## 11. Relevance to Causal Atlas

HDX HAPI is highly relevant to Causal Atlas as a unified gateway to multiple humanitarian indicator streams:

### Direct use cases

| HAPI Theme | Causal Atlas application |
|---|---|
| **Conflict events** | Conflict indicator layer; correlate with food prices, displacement, rainfall |
| **IDPs** | Displacement outcome variable; correlate with conflict, climate, food security |
| **Refugees / returnees** | Cross-border displacement flows; origin-destination analysis |
| **Food security (IPC)** | Food crisis severity; correlate with rainfall anomalies, conflict, economic shocks |
| **Food prices** | Economic stress indicator; early warning signal for food insecurity |
| **Rainfall** | Climate variable; drought detection via anomaly percentage |
| **Population** | Denominator for per-capita normalisation of all other indicators |
| **Poverty rate (MPI)** | Structural vulnerability baseline |
| **National risk (INFORM)** | Composite risk context for interpreting other signals |
| **Funding** | Humanitarian response intensity; correlate with crisis severity |

### Key advantages for Causal Atlas

1. **Standardised admin codes (p-codes):** All HAPI themes share the same spatial reference system, enabling direct joins across themes without geocoding.
2. **Single API for multiple domains:** Reduces the number of upstream integrations needed. Conflict, food security, displacement, climate, and population from one source.
3. **Pre-aggregated monthly data:** Conflict events and rainfall data at monthly/dekadal resolution align well with the Causal Atlas monthly temporal resolution.
4. **Consistent format:** JSON/CSV output with uniform field naming conventions.

### Limitations for Causal Atlas

1. **Admin-boundary spatial model vs. PRIO-GRID:** HAPI reports at admin levels, not grid cells. Area-weighted interpolation is needed to map to 0.5-degree cells. This is a significant data integration task.
2. **No raw event-level data:** Conflict events are monthly aggregates, not individual incidents with coordinates. For point-level conflict data, ACLED must be accessed directly.
3. **Variable temporal depth:** Some themes have decades of history, others only a year or two. Cross-domain lag analysis requires overlapping time series.
4. **Beta status:** API stability is not guaranteed. Field names and endpoint paths may change.
5. **Rate limits:** 1 req/s with 10k record cap requires careful pagination for bulk ingestion. A full download of all HAPI data for all countries would take considerable time.

### Recommended integration strategy

- Use HAPI as the **primary source for humanitarian indicators** (IPC food security, displacement, humanitarian needs, funding).
- Use HAPI conflict data for quick prototyping, but switch to **direct ACLED access** for production (event-level, daily granularity, coordinates).
- Use HAPI rainfall as a convenient admin-level climate indicator, but supplement with **raw CHIRPS rasters** for grid-cell-level analysis.
- Use HAPI population data for **per-capita normalisation** of counts.
- Build an adapter that paginates through all HAPI themes for a given country and time range, storing results in DuckDB/Parquet with p-code keys for joining.

---

## 12. Sources

---

## 13. P-Codes: The UN OCHA Administrative Boundary System

P-codes (Place Codes) are the spatial backbone of HAPI and the broader humanitarian data ecosystem. Understanding them is essential for working with HAPI data.

### What Are P-Codes?

P-codes are standardised location identifiers assigned by UN OCHA to administrative divisions in countries with humanitarian operations. They are part of the **Common Operational Datasets (CODs)** — the authoritative reference data agreed upon by the humanitarian community for each country.

### P-Code Structure

P-codes follow a hierarchical alphanumeric pattern:

| Level | Format | Example | Meaning |
|---|---|---|---|
| Admin 0 (country) | ISO 3166-1 alpha-3 | `AFG` | Afghanistan |
| Admin 1 (province) | Country prefix + sequence | `AF01` | Kabul Province |
| Admin 2 (district) | Admin 1 prefix + sequence | `AF0101` | A district within Kabul |
| Admin 3 (sub-district) | Admin 2 prefix + sequence | `AF010101` | Sub-district (where available) |

**Key rules:**
- The country prefix uses ISO 3166-1 alpha-2 codes (2 letters), not alpha-3
- Subsequent levels append 2-digit numeric sequences
- P-code length indicates admin level: 4 chars = admin 1, 6 chars = admin 2, 8 chars = admin 3
- P-codes are **not** globally standardised across all countries — some countries use different length patterns

### P-Code Sources

| Source | Description | URL |
|---|---|---|
| **COD Administrative Boundaries** | Official shapefiles + gazetteers per country | https://data.humdata.org/search?q=cod-ab |
| **Global P-Code List** | Master list maintained by OCHA | Via HAPI metadata endpoints |
| **ITOS Service** | OCHA Information Technology and Operations Section manages COD production | https://cod.unocha.org/ |

### P-Code Matching Challenges

- Country-specific variations in format (some use 3 characters per level instead of 2)
- P-codes can change when administrative boundaries are redrawn
- Multiple COD versions may exist for a country — HAPI tracks the reference period
- WFP, IPC, and other organisations sometimes use their own admin codes that must be crosswalked to COD p-codes (HAPI's `provider_admin1_code` fields handle this)

### Using P-Codes in Python

```python
def parse_pcode(pcode):
    """Parse a p-code into its hierarchical components."""
    if len(pcode) <= 3:
        return {'country': pcode, 'admin_level': 0}
    country = pcode[:2]
    levels = {'country_iso2': country, 'admin_level': 0}
    remaining = pcode[2:]
    level = 1
    while remaining:
        chunk = remaining[:2]
        levels[f'admin{level}_code'] = pcode[:2 + level * 2]
        levels['admin_level'] = level
        remaining = remaining[2:]
        level += 1
    return levels

# Example:
# parse_pcode('AF0101') → {'country_iso2': 'AF', 'admin_level': 2, 'admin1_code': 'AF01', 'admin2_code': 'AF0101'}
```

---

## 14. IPC/CH Food Security Phase Classification — Detailed Reference

The IPC (Integrated Food Security Phase Classification) data in HAPI is one of the most valuable themes for Causal Atlas. Here is a detailed reference.

### The Five IPC Acute Food Insecurity Phases

| Phase | Area Classification | Household Classification | Key Indicators | Typical Response |
|---|---|---|---|---|
| **Phase 1** | Minimal | None | Food consumption adequate, stable livelihoods, minimal food assistance | No action required |
| **Phase 2** | Stressed | Stressed | Minimally adequate food consumption, cannot afford some non-food expenditures, employing stress-level livelihood coping | Disaster risk reduction, livelihood protection |
| **Phase 3** | Crisis | Crisis | Food consumption gaps, acute malnutrition above normal, accelerated depletion of livelihood assets, employing crisis-level coping | Urgent action to protect livelihoods, prevent mortality |
| **Phase 4** | Emergency | Emergency | Large food consumption gaps, very high acute malnutrition, excess mortality, irreversible livelihood asset liquidation | Emergency food assistance, save lives |
| **Phase 5** | Famine | Catastrophe | Extreme food consumption gaps, mass starvation and death, complete collapse of livelihoods | Immediate large-scale humanitarian response |

### Phase 3+ Aggregation

HAPI provides a `3+` phase code that sums populations in Phases 3, 4, and 5. This represents the total population "in need of action" — the standard headline figure used in humanitarian planning.

### IPC Type Codes

| Code | Meaning | Description |
|---|---|---|
| `current` | Current situation | Analysis of the present food security situation |
| `first_projection` | Near-term projection | Typically 3-4 months ahead |
| `second_projection` | Medium-term projection | Typically 6-8 months ahead |

### Cadre Harmonisé (CH)

The Cadre Harmonisé is the West and Central African adaptation of IPC, used in 17 Sahel and coastal countries. CH uses the same 5-phase scale and is harmonised with IPC standards. In HAPI, CH data appears alongside IPC data under the food security endpoint.

### Analysis Cycle

IPC/CH analyses are not published on a fixed schedule — they follow country-specific analysis cycles, typically:
- **Twice per year** for most countries (lean season and post-harvest)
- **More frequently** for acute crises (e.g., Somalia, South Sudan, Yemen may have 3-4 analyses per year)
- **Less frequently** for stable countries

### Key Analytical Caveats

1. **Phase classifications are consensus-based:** Analysts from multiple organisations agree on classifications through a facilitated process. This adds credibility but also subjectivity.
2. **Area vs household classification:** Phase 1 is "None" for households but "Minimal" for areas. Phase 5 is "Catastrophe" for households but "Famine" for areas. The Famine classification requires that ≥20% of households are in Phase 5, plus GAM ≥30% and CDR ≥2/10,000/day.
3. **Population estimates are not additive across phases within a single analysis** — use the `all` population total as the denominator.
4. **Coverage gaps:** Not all countries have IPC/CH analyses. Coverage is concentrated in food-insecure regions of sub-Saharan Africa, Middle East, and parts of Asia.

---

## 15. API Response Examples (JSON)

### Example: Food Security (IPC) Response

```json
{
  "data": [
    {
      "resource_hdx_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "ipc_phase": "3+",
      "ipc_type": "current",
      "population_in_phase": 4200000,
      "population_fraction_in_phase": 0.28,
      "reference_period_start": "2024-10-01",
      "reference_period_end": "2025-01-31",
      "location_code": "YEM",
      "location_name": "Yemen",
      "admin1_code": "YE17",
      "admin1_name": "Al Hudaydah",
      "admin2_code": null,
      "admin2_name": null,
      "admin_level": 1
    }
  ]
}
```

### Example: Conflict Events Response

```json
{
  "data": [
    {
      "resource_hdx_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "event_type": "political_violence",
      "events": 47,
      "fatalities": 132,
      "reference_period_start": "2024-11-01",
      "reference_period_end": "2024-11-30",
      "location_code": "SOM",
      "location_name": "Somalia",
      "admin1_code": "SO18",
      "admin1_name": "Banadir",
      "admin2_code": "SO1801",
      "admin2_name": "Mogadishu",
      "admin_level": 2
    }
  ]
}
```

### Example: Population Response

```json
{
  "data": [
    {
      "resource_hdx_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "gender": "all",
      "age_range": "all",
      "min_age": null,
      "max_age": null,
      "population": 1250000,
      "reference_period_start": "2023-01-01",
      "reference_period_end": "2023-12-31",
      "location_code": "ETH",
      "location_name": "Ethiopia",
      "admin1_code": "ET04",
      "admin1_name": "Oromia",
      "admin2_code": "ET0405",
      "admin2_name": "West Arsi",
      "admin_level": 2
    }
  ]
}
```

### Example: Rainfall Response

```json
{
  "data": [
    {
      "resource_hdx_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
      "provider_admin1_code": "ET04",
      "provider_admin2_code": null,
      "aggregation_period": "dekad",
      "rainfall": 42.5,
      "rainfall_long_term_average": 55.3,
      "rainfall_anomaly_pct": -23.1,
      "number_pixels": 8432,
      "version": "FINAL",
      "reference_period_start": "2024-10-01",
      "reference_period_end": "2024-10-10",
      "location_code": "ETH",
      "location_name": "Ethiopia",
      "admin1_code": "ET04",
      "admin1_name": "Oromia",
      "admin2_code": null,
      "admin2_name": null,
      "admin_level": 1
    }
  ]
}
```

---

## 16. Complete Python Wrapper for All HAPI Endpoints

```python
"""
Comprehensive HAPI Python client for Causal Atlas.
Covers all v2 endpoints with pagination, rate limiting, and DataFrame output.
"""

import time
import base64
import requests
import pandas as pd
from typing import Optional, Dict, List, Any


class HAPIClient:
    """Client for the HDX Humanitarian API (HAPI) v2."""

    BASE_URL = "https://hapi.humdata.org/api/v2"
    RATE_LIMIT_SECONDS = 1.0
    MAX_LIMIT = 10_000

    # All available data endpoints
    ENDPOINTS = {
        # Affected People
        'idps': 'affected-people/idps',
        'refugees': 'affected-people/refugees-persons-of-concern',
        'returnees': 'affected-people/returnees',
        'humanitarian_needs': 'affected-people/humanitarian-needs',
        # Coordination & Context
        'operational_presence': 'coordination-context/operational-presence',
        'funding': 'coordination-context/funding',
        'conflict_events': 'coordination-context/conflict-events',
        'national_risk': 'coordination-context/national-risk',
        # Food Security, Nutrition & Poverty
        'food_security': 'food-security-nutrition-poverty/food-security',
        'food_prices': 'food-security-nutrition-poverty/food-prices-market-monitor',
        'poverty_rate': 'food-security-nutrition-poverty/poverty-rate',
        # Geography & Infrastructure
        'population': 'geography-infrastructure/population',
        # Climate
        'rainfall': 'climate/rainfall',
        # Metadata
        'locations': 'metadata/location',
        'admin1': 'metadata/admin1',
        'admin2': 'metadata/admin2',
        'data_availability': 'metadata/data-availability',
    }

    def __init__(self, app_name: str, email: str):
        """Initialize with app name and email for identifier generation."""
        raw = f"{app_name}:{email}"
        self.app_identifier = base64.b64encode(raw.encode()).decode()
        self._last_request_time = 0.0

    def _rate_limit(self):
        """Enforce 1 request per second."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.RATE_LIMIT_SECONDS:
            time.sleep(self.RATE_LIMIT_SECONDS - elapsed)
        self._last_request_time = time.time()

    def _fetch_page(self, endpoint: str, params: Dict) -> Dict:
        """Fetch a single page from the API."""
        self._rate_limit()
        params['app_identifier'] = self.app_identifier
        params['output_format'] = 'json'
        url = f"{self.BASE_URL}/{endpoint}"
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def fetch(self, theme: str, params: Optional[Dict] = None,
              limit: int = 10_000) -> pd.DataFrame:
        """
        Fetch all pages from a HAPI endpoint into a DataFrame.

        Args:
            theme: Key from ENDPOINTS dict (e.g., 'conflict_events', 'food_security')
            params: Query parameters (location_code, start_date, etc.)
            limit: Records per page (max 10,000)

        Returns:
            pd.DataFrame with all results
        """
        endpoint = self.ENDPOINTS[theme]
        params = dict(params or {})
        params['limit'] = min(limit, self.MAX_LIMIT)

        frames = []
        offset = 0

        while True:
            params['offset'] = offset
            result = self._fetch_page(endpoint, params)
            data = result.get('data', [])
            if not data:
                break
            frames.append(pd.DataFrame(data))
            if len(data) < params['limit']:
                break
            offset += params['limit']

        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)

    # Convenience methods for each theme
    def get_idps(self, **kwargs) -> pd.DataFrame:
        return self.fetch('idps', kwargs)

    def get_refugees(self, **kwargs) -> pd.DataFrame:
        return self.fetch('refugees', kwargs)

    def get_returnees(self, **kwargs) -> pd.DataFrame:
        return self.fetch('returnees', kwargs)

    def get_humanitarian_needs(self, **kwargs) -> pd.DataFrame:
        return self.fetch('humanitarian_needs', kwargs)

    def get_operational_presence(self, **kwargs) -> pd.DataFrame:
        return self.fetch('operational_presence', kwargs)

    def get_funding(self, **kwargs) -> pd.DataFrame:
        return self.fetch('funding', kwargs)

    def get_conflict_events(self, **kwargs) -> pd.DataFrame:
        return self.fetch('conflict_events', kwargs)

    def get_national_risk(self, **kwargs) -> pd.DataFrame:
        return self.fetch('national_risk', kwargs)

    def get_food_security(self, **kwargs) -> pd.DataFrame:
        return self.fetch('food_security', kwargs)

    def get_food_prices(self, **kwargs) -> pd.DataFrame:
        return self.fetch('food_prices', kwargs)

    def get_poverty_rate(self, **kwargs) -> pd.DataFrame:
        return self.fetch('poverty_rate', kwargs)

    def get_population(self, **kwargs) -> pd.DataFrame:
        return self.fetch('population', kwargs)

    def get_rainfall(self, **kwargs) -> pd.DataFrame:
        return self.fetch('rainfall', kwargs)

    def get_locations(self, **kwargs) -> pd.DataFrame:
        return self.fetch('locations', kwargs)

    def get_admin1(self, **kwargs) -> pd.DataFrame:
        return self.fetch('admin1', kwargs)

    def get_admin2(self, **kwargs) -> pd.DataFrame:
        return self.fetch('admin2', kwargs)

    def get_data_availability(self, **kwargs) -> pd.DataFrame:
        return self.fetch('data_availability', kwargs)


# Usage example:
# client = HAPIClient("causal_atlas", "user@example.com")
#
# # Get IPC food security data for Yemen
# ipc = client.get_food_security(location_code="YEM", ipc_phase="3+")
#
# # Get conflict events for Somalia, 2023+
# conflict = client.get_conflict_events(location_code="SOM", start_date="2023-01-01")
#
# # Get all rainfall data for Ethiopia at admin 1
# rain = client.get_rainfall(location_code="ETH", admin_level=1)
#
# # Get data availability across all themes
# avail = client.get_data_availability()
```

---

## 17. Sources

| Resource | URL |
|---|---|
| HDX HAPI homepage | https://data.humdata.org/hapi |
| API documentation / sandbox (Swagger UI) | https://hapi.humdata.org/docs |
| OpenAPI specification | https://hapi.humdata.org/openapi.json |
| ReadTheDocs documentation | https://hdx-hapi.readthedocs.io/en/latest/ |
| Getting started guide | https://hdx-hapi.readthedocs.io/en/latest/getting-started/ |
| Code examples | https://hdx-hapi.readthedocs.io/en/latest/examples/ |
| Data usage guides | https://hdx-hapi.readthedocs.io/en/latest/data_usage_guides/ |
| Enum reference | https://hdx-hapi.readthedocs.io/en/latest/data_usage_guides/enums/ |
| Changelog | https://hdx-hapi.readthedocs.io/en/latest/changelog/ |
| Terms of use | https://data.humdata.org/hapi/terms |
| Data availability dashboard | https://data.humdata.org/hapi#data-availability |
| HAPI datasets on HDX | https://data.humdata.org/organization/hdx-hapi |
| HAPI pipelines (GitHub) | https://github.com/OCHA-DAP/hapi-pipelines |
| hdx-python-api (PyPI) | https://pypi.org/project/hdx-python-api/ |
| hdx-python-api (GitHub) | https://github.com/OCHA-DAP/hdx-python-api |
| HDX platform | https://data.humdata.org/ |
| OCHA Centre for Humanitarian Data | https://centre.humdata.org/ |
