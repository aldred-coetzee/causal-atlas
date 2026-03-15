# Displacement Data — IDMC, UNHCR, and IOM DTM

> **Last reviewed:** March 2025
> **Status:** All three sources actively maintained
> **Websites:** https://www.internal-displacement.org | https://www.unhcr.org/refugee-statistics | https://dtm.iom.int

---

## 1. Overview

Displacement data is critical for Causal Atlas because displacement sits at the centre of multiple causal chains: conflict causes displacement, which in turn drives secondary humanitarian crises (food insecurity, health outbreaks, economic disruption). No single data source captures the full picture — three complementary datasets are needed:

| Source | Full name | Focus | Type |
|--------|-----------|-------|------|
| **IDMC** | Internal Displacement Monitoring Centre | Internal displacement (within countries) | Stock and flow estimates |
| **UNHCR** | UN Refugee Agency | Cross-border displacement (refugees, asylum seekers, stateless) | Stock and flow data |
| **IOM DTM** | International Organization for Migration — Displacement Tracking Matrix | Real-time displacement tracking | Operational tracking data |

### What each captures that others do not

| Dimension | IDMC | UNHCR | IOM DTM |
|-----------|------|-------|---------|
| **Internal displacement** | Primary focus | Limited (IDPs under UNHCR mandate only) | Detailed operational tracking |
| **Cross-border refugees** | Not covered | Primary focus | Limited (flow monitoring at borders) |
| **Disaster displacement** | Yes (since 2008) | Limited | Some coverage |
| **Conflict displacement** | Yes (since 1998) | Yes (refugees from conflict) | Yes (operational tracking) |
| **Sub-national detail** | Country-level estimates | Country-level (origin/destination) | Admin 1/2 level; site-level |
| **Near-real-time** | Annual + events | Annual (mid-year updates) | Continuous (operational) |
| **Temporal granularity** | Annual stock + event-level flows | Annual | Varies by operation (weekly to quarterly) |
| **Population categories** | IDPs only | Refugees, asylum seekers, IDPs (mandate), stateless, returnees | IDPs, returnees, migrants |
| **Historical depth** | 1998 (conflict), 2008 (disaster) | 1951 (some indicators) | Varies by operation |

---

## 2. IDMC — Internal Displacement Monitoring Centre

### 2.1 Overview

IDMC is the world's authoritative source on internal displacement. It maintains the Global Internal Displacement Database (GIDD), which provides country-level and sub-national estimates of internal displacement caused by conflict/violence and natural hazard-related disasters.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Organisation | Part of the Norwegian Refugee Council (NRC) |
| Headquarters | Geneva, Switzerland |
| Database | Global Internal Displacement Database (GIDD) |
| Temporal coverage | 1998-present (conflict), 2008-present (disaster) |
| Spatial coverage | Global (~200 countries and territories) |
| Update frequency | Annual (GRID report), plus event-level updates |
| Annual report | Global Report on Internal Displacement (GRID) |
| API | Yes (client_id authentication) |

### 2.2 Key concepts: Stock vs Flow

| Concept | Definition | IDMC term |
|---------|-----------|-----------|
| **Stock** | Total number of people living in displacement at a point in time (usually end of year) | Total number of IDPs |
| **Flow (new displacements)** | Number of new displacement movements during a period | Internal displacements |
| **Distinction** | One person displaced 3 times = 3 displacement movements but 1 IDP in stock | Important for interpretation |

**Critical distinction:** "Internal displacements" (flows) can exceed the total IDP stock because the same person may be displaced multiple times during the year. Flow data captures the scale of displacement events; stock data captures the accumulated displaced population.

### 2.3 Data fields

| Field | Type | Description |
|-------|------|-------------|
| `iso3` | string | ISO3 country code |
| `country_name` | string | Country name |
| `year` | integer | Reference year |
| `conflict_internal_displacements` | integer | New conflict-related displacement movements |
| `disaster_internal_displacements` | integer | New disaster-related displacement movements |
| `conflict_stock_displacement` | integer | Total IDPs from conflict at end of year |
| `disaster_stock_displacement` | integer | Total IDPs from disaster at end of year |
| `hazard_category` | string | For disaster events: geophysical, weather, climate, hydrological |
| `hazard_type` | string | Specific hazard (flood, earthquake, storm, etc.) |
| `event_name` | string | Named event (if applicable) |

### 2.4 API access

**Base URL:** `https://helix-tools-api.idmcdb.org/external-api/`

**Authentication:** `client_id` query parameter (API key obtained from IDMC)

**Key endpoints:**

| Endpoint | Description |
|----------|-------------|
| `/gidd/public-figure-analyses/` | Detailed methodology and figure evolution |
| `/gidd/disaggregations/disaggregation-geojson/` | Sub-national data with geography |

**Request API access:** Contact IDMC via their website or email (ch.datainfo@idmc.ch)

**Example API request:**
```
https://helix-tools-api.idmcdb.org/external-api/gidd/public-figure-analyses/?client_id=YOUR_API_KEY
```

### 2.5 Alternative data access

- **HDX:** 422+ datasets at https://data.humdata.org/organization/international-displacement-monitoring-centre-idmc
- **Direct download:** GIDD downloadable as Excel/CSV from https://www.internal-displacement.org/database/
- **GRID report data:** Published annually (typically May)

### 2.6 Python access

```python
import requests
import pandas as pd

IDMC_CLIENT_ID = 'your_client_id_here'
BASE_URL = 'https://helix-tools-api.idmcdb.org/external-api'

def get_idmc_data(endpoint='gidd/public-figure-analyses/'):
    """Fetch IDMC displacement data from the API."""
    url = f'{BASE_URL}/{endpoint}'
    params = {'client_id': IDMC_CLIENT_ID}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_idmc_geojson():
    """Fetch sub-national displacement data with geometries."""
    url = f'{BASE_URL}/gidd/disaggregations/disaggregation-geojson/'
    params = {'client_id': IDMC_CLIENT_ID}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Alternative: download from HDX
def download_idmc_from_hdx():
    """Download IDMC data from Humanitarian Data Exchange."""
    # IDMC provides country-level and event-level datasets on HDX
    from hdx.api.configuration import Configuration
    from hdx.data.dataset import Dataset

    Configuration.create(hdx_site='prod', user_agent='CausalAtlas')
    datasets = Dataset.search_in_hdx('IDMC internal displacement', rows=20)
    for ds in datasets:
        print(f"{ds['name']}: {ds['title']}")
    return datasets

# Download GIDD directly (no API key needed)
def download_gidd_csv():
    """Download the full GIDD dataset as CSV."""
    # Check https://www.internal-displacement.org/database/
    # for current download URL (may require manual download)
    pass
```

---

## 3. UNHCR — Refugee Data Finder

### 3.1 Overview

UNHCR's Refugee Data Finder provides the most comprehensive dataset on cross-border forced displacement globally. It covers refugees, asylum seekers, internally displaced persons (under UNHCR mandate), stateless persons, and other populations of concern.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Organisation | UN High Commissioner for Refugees |
| Database | Refugee Population Statistics Database |
| API | REST API at api.unhcr.org (no authentication required) |
| Temporal coverage | 1951-present (some indicators) |
| Spatial coverage | Global |
| Update frequency | Annual (June, with mid-year update) |
| Data model | Origin-destination pairs by population type |

### 3.2 Population categories

| Category | Code | Definition |
|----------|------|------------|
| Refugees | REF | Persons recognised as refugees under 1951 Convention or regional instruments |
| Asylum seekers | ASY | Persons whose asylum claim is pending |
| Internally displaced persons | IDP | IDPs under UNHCR mandate (subset of total IDPs) |
| Stateless persons | STA | Persons not considered nationals by any state |
| Others of concern | OOC | Other populations of concern to UNHCR |
| Host community members | HST | Local host community members affected by displacement |
| Returned refugees | RET | Refugees who have returned to country of origin |
| Returned IDPs | RDP | IDPs who have returned to area of origin |

### 3.3 Data structure

UNHCR data is organised as **origin-destination pairs**: for each year, the number of people of each population type from a specific country of origin living in a specific country of asylum.

| Field | Type | Description |
|-------|------|-------------|
| `year` | integer | Reference year |
| `coo` | string | Country of origin (ISO3) |
| `coo_name` | string | Country of origin name |
| `coa` | string | Country of asylum (ISO3) |
| `coa_name` | string | Country of asylum name |
| `refugees` | integer | Number of refugees |
| `asylum_seekers` | integer | Number of asylum seekers |
| `returned_refugees` | integer | Number of returned refugees |
| `idps` | integer | Number of IDPs (UNHCR mandate) |
| `returned_idps` | integer | Number of returned IDPs |
| `stateless` | integer | Number of stateless persons |
| `ooc` | integer | Others of concern |
| `total` | integer | Total population of concern |

### 3.4 API access

**Base URL:** `https://api.unhcr.org/population/v1/`

**Authentication:** None required (open API)

**Key endpoints:**

| Endpoint | Description |
|----------|-------------|
| `/population/` | Stock figures by year, origin, and asylum country |
| `/asylum-applications/` | Individual asylum applications by year and country |
| `/asylum-decisions/` | Decisions on asylum applications |
| `/demographics/` | Sex and age disaggregated data |
| `/solutions/` | Durable solutions (return, resettlement, naturalisation) |

**Query parameters:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `year` or `year[]` | Year(s) to filter | `year=2023` or `year[]=2022&year[]=2023` |
| `coo` | Country of origin (ISO3) | `coo=SYR` |
| `coa` | Country of asylum (ISO3) | `coa=TUR` |
| `coo_all` | Include all countries of origin | `coo_all=true` |
| `coa_all` | Include all countries of asylum | `coa_all=true` |
| `cf_type` | Code format | `cf_type=ISO` |
| `limit` | Results per page | `limit=100` |
| `page` | Page number | `page=2` |

**Response format:** JSON

### 3.5 Python access

```python
import requests
import pandas as pd

BASE_URL = 'https://api.unhcr.org/population/v1'

def get_unhcr_population(year=None, coo=None, coa=None, limit=1000):
    """
    Fetch UNHCR population data.

    Parameters
    ----------
    year : int or list of int
        Year(s) to query
    coo : str
        Country of origin (ISO3 code)
    coa : str
        Country of asylum (ISO3 code)
    limit : int
        Results per page
    """
    params = {
        'cf_type': 'ISO',
        'limit': limit,
    }
    if year:
        if isinstance(year, list):
            for y in year:
                params.setdefault('year[]', []).append(y)
        else:
            params['year'] = year
    if coo:
        params['coo'] = coo
    if coa:
        params['coa'] = coa

    all_results = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(f'{BASE_URL}/population/', params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' in data:
            all_results.extend(data['items'])
            if len(data['items']) < limit:
                break
            page += 1
        else:
            break

    return pd.DataFrame(all_results)

# Example: Syrian refugees in all countries, 2020-2023
df_syria = get_unhcr_population(year=[2020, 2021, 2022, 2023], coo='SYR')
print(f"Records: {len(df_syria)}")
print(df_syria[['year', 'coa_name', 'refugees']].sort_values('refugees', ascending=False).head(10))

# Example: All refugees in Ethiopia
df_ethiopia = get_unhcr_population(coa='ETH', year=2023)
print(df_ethiopia[['coo_name', 'refugees']].sort_values('refugees', ascending=False))

# R package also available:
# install.packages("refugees")  # CRAN package for UNHCR data
```

### 3.6 Asylum applications and decisions

```python
def get_unhcr_asylum_applications(year=None, coa=None, limit=1000):
    """Fetch asylum application data."""
    params = {'cf_type': 'ISO', 'limit': limit}
    if year:
        params['year'] = year
    if coa:
        params['coa'] = coa

    response = requests.get(f'{BASE_URL}/asylum-applications/', params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json().get('items', []))

def get_unhcr_asylum_decisions(year=None, coa=None, limit=1000):
    """Fetch asylum decision data."""
    params = {'cf_type': 'ISO', 'limit': limit}
    if year:
        params['year'] = year
    if coa:
        params['coa'] = coa

    response = requests.get(f'{BASE_URL}/asylum-decisions/', params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json().get('items', []))
```

---

## 4. IOM DTM — Displacement Tracking Matrix

### 4.1 Overview

IOM's Displacement Tracking Matrix (DTM) provides real-time operational tracking of displaced populations. Unlike IDMC (annual estimates) and UNHCR (annual stock data), DTM provides sub-national, frequently updated data from field operations in crisis-affected countries.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Organisation | International Organization for Migration (IOM) |
| Operations | 91 countries (as of 2025) |
| API | REST API v3 (subscription key required) |
| Developer portal | https://dtm.iom.int/data-and-analysis/dtm-api |
| Spatial resolution | Country, Admin 1, Admin 2 levels |
| Update frequency | Varies by operation (weekly to quarterly) |
| Data sensitivity | Only non-sensitive, aggregated IDP figures |

### 4.2 DTM components

| Component | Description | Data type |
|-----------|-------------|-----------|
| **Baseline Assessments** | Comprehensive assessments of displacement in an area | IDP counts, locations, basic demographics |
| **Multi-Sectoral Location Assessments (MSLA)** | Detailed assessments at displacement sites | Shelter, WASH, health, food, education needs |
| **Mobility Tracking** | Tracking of IDP movements over time | Flow data, population changes |
| **Flow Monitoring** | Monitoring at transit points (borders, routes) | Cross-border and internal movement flows |
| **Emergency Tracking** | Rapid assessments following sudden events | Event-triggered displacement estimates |

### 4.3 API v3 access

**Released:** August 2025

**Registration:**
1. Visit https://dtm.iom.int/data-and-analysis/dtm-api
2. Create a developer account on the DTM Developer Portal
3. Review v3 documentation
4. Generate a subscription key

**API characteristics:**
- REST API returning JSON
- Standard HTTP response codes
- User authentication tokens required
- API Query Builder available on the portal

**Key data points in v3:**
- IDP figures at country, Admin 1, and Admin 2 levels
- **Drivers of displacement** (new in v3): conflict, disaster, etc.
- **Sex disaggregation** (new in v3): male/female breakdown
- **Origins** (new in v3): broad origin areas of displaced people

**Data coverage:**
- Data from baseline assessments and multi-sectoral location assessments
- Non-sensitive, aggregated figures only
- A Data Coverage Matrix tool shows available data by country and operation

### 4.4 Alternative access

- **HDX:** DTM datasets available at https://data.humdata.org per country per operation round
- **DTM website:** Direct download of reports and datasets at https://dtm.iom.int
- **DTM Portals:** Country-specific DTM portals with interactive maps and downloads

### 4.5 Python access

```python
import requests
import pandas as pd

# DTM API v3
DTM_SUBSCRIPTION_KEY = 'your_subscription_key_here'
DTM_BASE_URL = 'https://dtm.iom.int/api/v3'  # Verify current URL from developer portal

def get_dtm_data(country=None, admin_level=None):
    """
    Fetch DTM displacement data.

    Note: Exact endpoint structure should be verified from the
    DTM Developer Portal documentation after registration.
    """
    headers = {
        'Authorization': f'Bearer {DTM_SUBSCRIPTION_KEY}',
        'Accept': 'application/json'
    }
    params = {}
    if country:
        params['country'] = country
    if admin_level:
        params['admin_level'] = admin_level

    response = requests.get(f'{DTM_BASE_URL}/idps', headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Community Python package (may be useful)
# pip install dtmapi
# See: https://pypi.org/project/dtmapi/

# Alternative: HDX download
def download_dtm_from_hdx(country_name):
    """Download DTM data from HDX for a specific country."""
    from hdx.api.configuration import Configuration
    from hdx.data.dataset import Dataset

    Configuration.create(hdx_site='prod', user_agent='CausalAtlas')
    datasets = Dataset.search_in_hdx(f'DTM {country_name}', rows=20)
    for ds in datasets:
        print(f"{ds['name']}: {ds['title']}")
    return datasets
```

---

## 5. Cross-Dataset Comparison and Integration

### 5.1 What each source captures

| Dimension | IDMC (GIDD) | UNHCR | IOM DTM |
|-----------|-------------|-------|---------|
| **Primary unit** | Country | Country pair (origin-destination) | Admin area / site |
| **Temporal granularity** | Annual + events | Annual | Operational (varies) |
| **Population counted** | All IDPs | Refugees, asylum seekers, stateless | IDPs at tracked sites |
| **Disaster displacement** | Comprehensive | Minimal | Some |
| **Conflict displacement** | Comprehensive | Refugees from conflict | Detailed operational |
| **Sub-national detail** | Limited (improving) | Limited | Detailed (Admin 1/2, sites) |
| **Flow data** | New displacements/year | Solutions, returns | Flow monitoring points |
| **API accessibility** | Moderate (client_id) | Excellent (open, no auth) | Good (subscription key) |
| **Data lag** | Annual report + events | Annual (June release) | Operational (varies) |

### 5.2 Overlap and double-counting risks

**IDMC vs UNHCR IDPs:** IDMC provides the most comprehensive IDP estimates. UNHCR tracks only IDPs under its mandate (a subset). For internal displacement, use IDMC as the primary source.

**IDMC vs DTM:** IDMC uses DTM data as one of its inputs. IDMC provides country-level totals; DTM provides sub-national operational detail. They should be used as complementary, not additive.

**UNHCR refugees vs IDMC IDPs:** These measure different populations (cross-border vs internal displacement) and can be summed to estimate total forced displacement.

### 5.3 Recommended integration approach

```python
import pandas as pd

def integrate_displacement_sources(year, country_iso3):
    """
    Integrate displacement data from IDMC, UNHCR, and DTM.

    Returns a unified view of displacement for a country-year.
    """
    result = {
        'country': country_iso3,
        'year': year,
    }

    # IDMC: Internal displacement stock and flows
    idmc_data = get_idmc_data()  # Requires parsing
    # result['idps_conflict_stock'] = ...
    # result['idps_disaster_stock'] = ...
    # result['new_conflict_displacements'] = ...
    # result['new_disaster_displacements'] = ...

    # UNHCR: Cross-border displacement
    unhcr_data = get_unhcr_population(year=year, coo=country_iso3)
    result['refugees_from_country'] = unhcr_data['refugees'].sum()
    result['asylum_seekers_from_country'] = unhcr_data['asylum_seekers'].sum()

    unhcr_hosted = get_unhcr_population(year=year, coa=country_iso3)
    result['refugees_hosted'] = unhcr_hosted['refugees'].sum()
    result['asylum_seekers_hosted'] = unhcr_hosted['asylum_seekers'].sum()

    # DTM: Sub-national operational data (if available)
    # dtm_data = get_dtm_data(country=country_iso3)
    # result['dtm_tracked_idps'] = ...
    # result['dtm_sites'] = ...

    # Total forced displacement estimate
    # result['total_displaced'] = (
    #     result['idps_conflict_stock'] +
    #     result['idps_disaster_stock'] +
    #     result['refugees_from_country']
    # )

    return result
```

---

## 6. Spatial Coverage and Resolution

### IDMC spatial detail

- **Primary:** Country-level estimates
- **Improving:** Sub-national disaggregation available for some countries via GeoJSON endpoint
- **Event data:** Individual disaster events with some location detail
- **PRIO-GRID integration:** Requires country-to-grid-cell mapping (simple for country-level data)

### UNHCR spatial detail

- **Primary:** Country-of-origin to country-of-asylum pairs
- **Demographics data:** Includes some location detail (urban/rural, camp/settlement names)
- **No sub-national estimates** in the standard population dataset
- **PRIO-GRID integration:** Country-level only (distributed to grid cells by population weight)

### IOM DTM spatial detail

- **Admin 1 and Admin 2** level IDP figures
- **Site-level data** from multi-sectoral location assessments (point locations)
- **Flow monitoring points** at specific transit locations
- **Best sub-national displacement data** among the three sources
- **PRIO-GRID integration:** Admin 2 areas can be overlaid with grid cells using spatial join

---

## 7. Temporal Coverage and Resolution

| Source | Temporal coverage | Granularity | Update cycle |
|--------|------------------|-------------|--------------|
| IDMC (conflict stock) | 1998-present | Annual (end-year) | Annual (GRID report, May) |
| IDMC (disaster stock) | 2008-present | Annual (end-year) | Annual |
| IDMC (new displacements) | 2008-present | Annual + events | Annual + event-level |
| UNHCR (population) | 1951-present (varies) | Annual (mid-year) | Annual (June release) |
| UNHCR (asylum) | 2000-present | Annual | Annual |
| IOM DTM | Varies by operation | Per assessment round | Operational (weekly-quarterly) |

**Key limitation:** None of these sources provides truly monthly displacement data at global scale. DTM is the most temporally granular but only covers countries with active operations.

---

## 8. Quality and Known Issues

### IDMC

| Issue | Detail |
|-------|--------|
| **Stock data challenges** | Difficulty tracking when displacement ends; stock figures may be inflated |
| **Disaster displacement estimation** | Relies on models and media reports; actual figures uncertain |
| **Historical revisions** | Figures revised annually; historical data changes documented in GIDD_HistoricalChanges files |
| **Methodological evolution** | Pre-2008 disaster data not available; methods have changed over time |
| **Sub-national gaps** | Country-level totals more reliable than sub-national breakdown |

### UNHCR

| Issue | Detail |
|-------|--------|
| **Registration gaps** | Not all refugees are registered with UNHCR; some countries handle registration independently |
| **Annual granularity** | Stock data is end-of-year snapshot; misses within-year dynamics |
| **Government data dependency** | Some countries provide data directly; quality varies |
| **IDP coverage** | Only IDPs under UNHCR mandate; not comprehensive IDP count (use IDMC) |
| **Stateless data quality** | Stateless person estimates highly uncertain in many countries |

### IOM DTM

| Issue | Detail |
|-------|--------|
| **Operational coverage** | Only active in countries with IOM operations; not globally uniform |
| **Assessment frequency** | Varies widely by country (weekly in some, quarterly in others) |
| **Non-sensitive data only** | API provides only aggregated, non-sensitive figures |
| **Methodology variation** | Different DTM components use different methodologies |
| **Temporal comparability** | Assessment rounds not aligned across countries |

---

## 9. Licence and Terms

| Source | Licence | Attribution required | Commercial use |
|--------|---------|---------------------|----------------|
| IDMC | Open access (terms at internal-displacement.org/terms-of-use) | Yes — cite IDMC/GIDD | Check terms |
| UNHCR | CC-BY 4.0 (most datasets on Operational Data Portal) | Yes — cite UNHCR | Permitted under CC-BY |
| IOM DTM | Open access for humanitarian use | Yes — cite IOM DTM | Check terms per dataset |

### Citation formats

**IDMC:**
> Internal Displacement Monitoring Centre (IDMC). Global Internal Displacement Database (GIDD). [Year]. https://www.internal-displacement.org/database/

**UNHCR:**
> UNHCR. Refugee Data Finder. [Year]. https://www.unhcr.org/refugee-statistics/

**IOM DTM:**
> International Organization for Migration (IOM). Displacement Tracking Matrix (DTM). [Year]. https://dtm.iom.int/

---

## 10. Displacement in Causal Chains

### The displacement causal chain model

Displacement is both an **outcome** (caused by conflict, disasters, etc.) and a **driver** (causing secondary humanitarian effects):

```
[CAUSES]                    [DISPLACEMENT]              [SECONDARY EFFECTS]

Conflict (ACLED/UCDP) ──┐                          ┌── Food insecurity (IPC)
                         │                          │
Disaster (EM-DAT)    ────┤                          ├── Health outcomes (WHO)
                         ├──> Displacement ─────────┤
Climate (ERA5/CHIRPS) ───┤    (IDMC/UNHCR/DTM)      ├── Economic disruption (nightlights)
                         │                          │
Persecution          ────┘                          ├── Host community strain
                                                    │
                                                    └── Further conflict (ACLED)
```

### Key causal relationships documented in literature

1. **Conflict → displacement:** Well-established. ACLED event spikes precede displacement increases by 0-3 months.

2. **Displacement → food insecurity:** Formerly displaced households have ~5% lower food expenditure and ~6% lower calorie intake than non-displaced neighbours. IDP influx negatively impacts food security in host communities.

3. **Displacement → health:** Children exposed to conflict-related displacement in Burundi had significantly higher stunting rates. One year of conflict exposure causally increased boys' mortality risk by 25 percentage points in Burundi.

4. **Displacement → secondary conflict:** Displacement creates resource competition in host areas, potentially triggering new conflict episodes.

5. **Disaster → displacement:** Sudden-onset disasters (floods, earthquakes, storms) cause rapid displacement spikes detectable in IDMC event data.

6. **Climate → displacement:** Drought drives pastoral displacement; slow-onset climate change increasingly linked to displacement in semi-arid regions.

### Lag structures

| Causal link | Typical lag | Evidence quality |
|-------------|------------|-----------------|
| Conflict event → displacement movement | 0-4 weeks | Strong (ACLED → IDMC events) |
| Displacement → food insecurity in host area | 1-6 months | Moderate |
| Drought → pastoral displacement | 2-6 months | Moderate |
| Displacement → disease outbreak | 2-8 weeks | Moderate |
| Food insecurity → cross-border flight | 1-6 months | Limited |
| Displacement → economic disruption | 3-12 months | Limited |

---

## 11. Interoperability with Other Causal Atlas Datasets

| Dataset | Relationship | Integration approach |
|---------|-------------|---------------------|
| **ACLED** | Conflict events → displacement | Spatial-temporal correlation; ACLED events as predictor of displacement flows |
| **IPC** | Displacement → food insecurity → displacement (feedback loop) | IPC areas with IDP camps; displacement as predictor of IPC phase |
| **CHIRPS/ERA5** | Climate extremes → displacement | Drought/flood anomalies as displacement predictors |
| **EM-DAT** | Disaster events → displacement | Match IDMC disaster displacement to EM-DAT events |
| **WFP food prices** | Displacement → price pressure in host areas | Price spikes in areas receiving displaced populations |
| **FIRMS** | Conflict-related arson → displacement | Fire detection as early indicator of displacement-causing events |
| **Nightlights** | Economic impact of displacement | Nightlight changes in origin (decline) and destination (may increase) areas |
| **OpenAQ** | Displacement camp conditions → health | Air quality in and near large displacement camps |

### PRIO-GRID integration approach

| Source | Spatial granularity | PRIO-GRID mapping method |
|--------|--------------------|-|
| IDMC (country) | Country-level | Distribute to grid cells using population weight |
| IDMC (sub-national) | Admin areas (improving) | Overlay admin boundaries with grid cells |
| UNHCR | Country origin-destination | Country-level to grid (population-weighted) |
| DTM (Admin 2) | Admin 2 level | Spatial join admin 2 boundaries with grid cells |
| DTM (sites) | Point locations | Direct point-to-grid assignment |

---

## 12. Relevance to Causal Atlas

### Why displacement data is essential

Displacement is the **central mediating variable** in many humanitarian causal chains. Without displacement data, we cannot:
- Distinguish direct conflict impacts from displacement-mediated impacts
- Model the geographic spread of humanitarian crises from origin to host areas
- Quantify the secondary effects of displacement on food security, health, and economic outcomes
- Track the temporal sequence: conflict → displacement → secondary crisis

### Implementation priority

1. **Phase 1:** Ingest UNHCR population data (easiest — open API, no authentication)
2. **Phase 2:** Obtain IDMC API access and ingest GIDD data
3. **Phase 3:** Register for DTM API and ingest sub-national displacement data
4. **Phase 4:** Build integrated displacement index combining all three sources
5. **Phase 5:** Cross-correlate with ACLED (causes) and IPC/health outcomes (effects)

### Key analysis opportunities

- **Conflict → displacement → food insecurity chain:** Use ACLED events → IDMC/DTM displacement → IPC phase transitions
- **Disaster → displacement → health outcomes:** Use EM-DAT events → IDMC disaster displacement → disease outbreak data
- **Displacement host community impact:** DTM site locations → nearby IPC/food price/health changes
- **Early warning:** Can ACLED conflict patterns predict displacement flows 1-3 months ahead?
- **Origin vs destination analysis:** UNHCR origin-destination data enables tracking impact in both sending and receiving areas

### Storage estimate

| Data source | Approximate size |
|-------------|-----------------|
| IDMC GIDD full download | ~50 MB (CSV) |
| UNHCR population data (all years, all countries) | ~200 MB (JSON) |
| DTM data (varies by country) | ~1-5 GB total across all operations |
| Integrated displacement database | ~500 MB - 2 GB |

---

## Sources

### IDMC
- IDMC website: https://www.internal-displacement.org
- GIDD database: https://www.internal-displacement.org/database/
- GIDD API documentation: https://www.internal-displacement.org/database/api-documentation/
- IDMC API endpoint: https://helix-tools-api.idmcdb.org/external-api/
- IDMC on HDX: https://data.humdata.org/organization/international-displacement-monitoring-centre-idmc
- IDMC GRID 2025 report: https://api.internal-displacement.org/sites/default/files/publications/documents/idmc-grid-2025-global-report-on-internal-displacement.pdf
- IDMC terms of use: https://www.internal-displacement.org/terms-of-use/

### UNHCR
- Refugee Data Finder: https://www.unhcr.org/refugee-statistics
- API documentation: https://api.unhcr.org/docs/refugee-statistics.html
- How to use the API: https://www.unhcr.org/refugee-statistics/insights/explainers/forcibly-displaced-api.html
- Global public API: https://www.unhcr.org/what-we-do/reports-and-publications/data-and-statistics/global-public-api
- Data content/methodology: https://www.unhcr.org/refugee-statistics/methodology/data-content
- R package (refugees): https://cran.r-project.org/web/packages/refugees/refugees.pdf

### IOM DTM
- DTM website: https://dtm.iom.int/
- DTM API: https://dtm.iom.int/data-and-analysis/dtm-api
- DTM API v3 release: https://dtm.iom.int/updates/dtm-releases-version-30-its-api-drivers-origins-and-sex
- DTM data coverage: https://dtm.iom.int/data-and-analysis/dtm-api/data-coverage
- Mobility Tracking: https://dtm.iom.int/operations/mobility-tracking
- Flow Monitoring: https://dtm.iom.int/domain/migrationiomint
- DTM Python package: https://pypi.org/project/dtmapi/
- DTM on Medium: https://medium.com/un-global-pulse-ap/displacement-tracking-matrix-dtm-api-revolutionizing-access-to-displacement-data-9122bbcbbde8

### Academic references
- Food Insecurity and Conflict Dynamics: Causal Linkages and Complex Feedbacks. *Stability: International Journal of Security and Development*. https://stabilityjournal.org/articles/sta.bm
- Armed conflicts, forced displacement and food security in host communities. *World Development*. https://www.sciencedirect.com/science/article/abs/pii/S0305750X22001814
- Impact of conflict on food security: evidence from Ethiopia and Malawi. *Agriculture & Food Security*. https://agricultureandfoodsecurity.biomedcentral.com/articles/10.1186/s40066-023-00447-z
- Pathways to food insecurity in the context of conflict. *Conflict and Health*. https://link.springer.com/article/10.1186/s13031-022-00470-0
