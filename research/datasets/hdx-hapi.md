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
