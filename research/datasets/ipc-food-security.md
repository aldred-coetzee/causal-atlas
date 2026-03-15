# IPC — Integrated Food Security Phase Classification

> **Last reviewed:** March 2025
> **Status:** Active, analyses published 2-3 times per year per country
> **Website:** https://www.ipcinfo.org

---

## 1. Overview

The Integrated Food Security Phase Classification (IPC) is a multi-partner initiative that provides the global standard for classifying the severity and magnitude of acute and chronic food insecurity and acute malnutrition. IPC analyses inform billions of dollars in humanitarian funding allocations and serve as the authoritative basis for food security decision-making worldwide.

For Causal Atlas, IPC data is the **gold standard outcome variable** for food security. It integrates evidence from multiple sources (food consumption, livelihoods, malnutrition, mortality) into a single severity classification, making it the most policy-relevant food security indicator available. IPC classifications are the primary dependent variable for causal chains involving drought, conflict, food prices, and displacement.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Founded | 2004 (originally for Somalia, expanded globally) |
| Governance | IPC Global Partnership (FAO, WFP, UNICEF, Save the Children, Oxfam, FEWS NET, CARE, ACF, EU JRC, CILSS, SICA, SADC, IGAD) |
| Global Support Unit | Hosted by FAO in Rome |
| Funding | Multiple donors (USAID, DFID/FCDO, EU, others) |
| Analysis type | Expert consensus based on convergence of evidence |
| Countries covered | 30+ countries with IPC analyses; 18+ with Cadre Harmonise (CH) |
| Population tracked | Hundreds of millions of people per analysis cycle |
| Analysis cadence | Typically 2-3 per country per year (irregular, event-driven) |
| API | Available at api.ipcinfo.org (API key required) |

---

## 2. The IPC Classification System

### IPC Acute Food Insecurity (AFI) Phases

The IPC uses a 5-phase severity scale. Phase classification applies to both areas and households, with slightly different terminology:

| Phase | Area classification | Household classification | Typical indicators |
|-------|--------------------|--------------------------|--------------------|
| **Phase 1** | Minimal | None | Adequate food consumption; stable livelihoods; able to meet essential needs |
| **Phase 2** | Stressed | Stressed | Minimally adequate food consumption; unable to afford some non-food essentials; employing stress coping strategies |
| **Phase 3** | Crisis | Crisis | Food consumption gaps OR marginally adequate with asset depletion; acute malnutrition elevated |
| **Phase 4** | Emergency | Emergency | Large food consumption gaps; very high acute malnutrition; excess mortality; livelihood assets liquidated |
| **Phase 5** | Famine | Catastrophe | Extreme food gaps; very high mortality; complete livelihood collapse; starvation |

### Famine (Phase 5) thresholds

Famine is the most extreme classification. The IPC applies special protocols requiring reliable evidence on **all three** outcomes simultaneously:

| Indicator | Famine threshold |
|-----------|-----------------|
| Food consumption / livelihood change | >20% of households with extreme food gaps |
| Global Acute Malnutrition (GAM) | >30% of children acutely malnourished |
| Crude Death Rate (CDR) | >2 per 10,000 per day |

A Famine classification triggers the highest level of international humanitarian response. Famine declarations are rare — recent examples include South Sudan (2017), Somalia (2022), and Gaza (2024).

### IPC Chronic Food Insecurity (CFI) Classification

A separate 4-level classification for long-term structural food insecurity:

| Level | Name | Description |
|-------|------|-------------|
| Level 1 | Minimal | Food security not a chronic concern |
| Level 2 | Mild | Some chronic food insecurity but manageable |
| Level 3 | Moderate | Chronic food insecurity causing ongoing hardship |
| Level 4 | Severe | Persistent, deeply entrenched food insecurity |

### IPC Acute Malnutrition (AMN) Classification

A 5-phase classification specifically for acute malnutrition, using wasting (weight-for-height), oedema, and Mid-Upper Arm Circumference (MUAC) prevalence thresholds.

---

## 3. IPC vs Cadre Harmonise (CH)

The Cadre Harmonise (CH) is a parallel food security classification tool developed by CILSS for the Sahel and West Africa. It uses the same conceptual framework and phase classifications as the IPC but was developed independently.

| Attribute | IPC | Cadre Harmonise (CH) |
|-----------|-----|---------------------|
| Developed by | IPC Global Partnership | CILSS / ECOWAS / UEMOA |
| Geographic scope | Global (30+ countries) | Sahel and West Africa (18+ countries) |
| Phase system | 5 phases (identical scale) | 5 phases (identical scale) |
| Analysis approach | Consensus-based, convergence of evidence | Consensus-based, convergence of evidence |
| Countries | Somalia, Ethiopia, Kenya, DRC, Afghanistan, Yemen, South Sudan, Haiti, etc. | Niger, Mali, Burkina Faso, Chad, Nigeria, Senegal, Mauritania, etc. |
| Integration | Analyses published on IPC website | CH data now available through IPC API |
| API | api.ipcinfo.org | Included in IPC API |

**Convergence effort:** Over recent years, the IPC and CH teams have been working to harmonise their technical processes, resulting in comparable analysis findings across 40+ countries. The IPC website now hosts both IPC and CH analysis results, and the API provides combined access.

---

## 4. Spatial Coverage and Resolution

### Country coverage

IPC/CH analyses are conducted in countries experiencing or at risk of food crises. As of 2025, regular analyses cover:

**Africa:** Somalia, Ethiopia, Kenya, South Sudan, Sudan, DRC, CAR, Mozambique, Madagascar, Zimbabwe, Malawi, Uganda, Burundi, Tanzania, Nigeria (CH), Niger (CH), Mali (CH), Burkina Faso (CH), Chad (CH), Cameroon (CH), Senegal (CH), Mauritania (CH), Guinea (CH), Sierra Leone (CH), Liberia (CH), Gambia (CH), Togo (CH), Benin (CH), Cote d'Ivoire (CH), Ghana (CH)

**Middle East / Asia:** Yemen, Afghanistan, Syria, Pakistan, Myanmar, Sri Lanka, Iraq

**Americas / Caribbean:** Haiti, Guatemala, Honduras, El Salvador

**Coverage is NOT global** — IPC analyses are conducted only where food crises exist or are anticipated. High-income countries are not analysed.

### Spatial units of analysis

IPC analyses are conducted at the sub-national level using administrative boundaries:

| Level | Description | Typical number of areas |
|-------|-------------|------------------------|
| Admin Level 1 | Provinces / States / Regions | 5-40 per country |
| Admin Level 2 | Districts / Counties / Zones | 20-300 per country |
| Admin Level 3 | Sub-districts / Woredas | Used in some countries (e.g., Ethiopia) |
| Urban areas | Specific city/neighbourhood areas | Increasing coverage |
| IDP camps | Individual displacement camps | Where relevant |

**Important:** IPC classifies **areas**, not grid cells. The spatial units are irregular administrative boundaries, not regular grids. This creates a challenge for PRIO-GRID integration.

### Population estimates

Each IPC analysis provides population estimates by phase for each area:

- Total population analysed
- Population in Phase 1 (Minimal)
- Population in Phase 2 (Stressed)
- Population in Phase 3+ (Crisis or worse)
- Population in Phase 3 (Crisis)
- Population in Phase 4 (Emergency)
- Population in Phase 5 (Famine/Catastrophe)

These population estimates are critical — an area classified as Phase 3 with 500,000 people is fundamentally different from a Phase 3 area with 50,000 people.

---

## 5. Temporal Coverage and Resolution

### Analysis periods

IPC analyses cover specific time windows:

| Period type | Description | Typical duration |
|-------------|-------------|-----------------|
| Current | Assessment of present food security situation | Snapshot (1-3 months) |
| Projected (near-term) | Forecast for next period | 3-6 months forward |
| Projected (medium-term) | Longer-range outlook | 6-12 months forward (less common) |

### Analysis cadence

**IPC analyses are NOT monthly.** Typical patterns:

| Country type | Frequency | Timing |
|--------------|-----------|--------|
| Chronic crisis (Somalia, Yemen, South Sudan) | 2-3 times per year | Often aligned with lean/harvest seasons |
| Seasonal crisis (Sahel countries) | 2 times per year | Post-harvest (Nov-Mar) and lean season (Jun-Sep) |
| Acute crisis (triggered by event) | Ad hoc | As needed (conflict escalation, flood, etc.) |

**This irregular cadence is a major challenge** for time-series analysis. Gaps between analyses can be 4-6 months, and coverage of specific areas may vary between analysis rounds.

### Historical data availability

- IPC analyses archive extends back to approximately 2010-2011 for some countries
- Coverage has expanded significantly since 2016
- Earlier data may have different methodological standards (IPC 2.0 vs 3.0)
- The current methodology is IPC 3.1

---

## 6. Data Access Methods

### Method 1: IPC API (api.ipcinfo.org)

**Registration:**
1. Visit https://www.ipcinfo.org/ipc-country-analysis/api/
2. Submit a request form with your use case
3. IPC validates the request and provides an API key
4. Technical documentation available at https://docs.api.ipcinfo.org/

**Authentication:** API key provided after registration approval

**Available data formats:** JSON, GeoJSON, Vector Tiles

**Key capabilities:**
- Country-level and sub-national analysis results
- Population estimates by phase
- Current and projected periods
- Geographic boundaries (GeoJSON)
- Both IPC and CH analyses

**API endpoints (based on available documentation):**

| Endpoint | Description |
|----------|-------------|
| `/analyses` | List available analyses by country/date |
| `/population` | Population estimates by phase |
| `/areas` | Geographic areas with classifications |
| `/countries` | Country-level metadata |

**Note:** The IPC API is relatively new (launched ~2022) and documentation has been evolving. Access requires approval, and the API may have usage limits (not publicly documented as of March 2025).

### Method 2: HDX (Humanitarian Data Exchange)

IPC data is available on HDX at https://data.humdata.org/organization/ipc with 54+ datasets. This includes:
- Country-level analysis downloads
- Population tables in CSV/Excel
- Geographic boundaries in SHP/GeoJSON
- CH data for West African countries

HDX may be more accessible than the API for bulk historical data.

### Method 3: FEWS NET

The Famine Early Warning Systems Network (FEWS NET) publishes IPC-compatible food security classifications at https://fews.net/data/acute-food-insecurity. FEWS NET provides:
- IPC-compatible classifications for additional countries
- More frequent updates in some contexts
- Detailed scenario narratives
- Machine-readable data downloads

### Method 4: HDX HAPI

The HDX Humanitarian API (HAPI) includes IPC data as one of its standard indicators, accessible via RESTful API. See the `hdx-hapi.md` research file for details.

### Method 5: FAO Data Portal

IPC data is also available via FAO's data portal at https://data.apps.fao.org/catalog/dataset/ipc-info-tool

### Method 6: World Bank Data360

Available at https://data360.worldbank.org/en/dataset/IPC_IPC

---

## 7. Schema and Data Fields

### Typical IPC analysis output structure

Each analysis record contains:

| Field | Type | Description |
|-------|------|-------------|
| `country` | string | Country name |
| `country_code` | string | ISO3 country code |
| `analysis_id` | string | Unique analysis identifier |
| `analysis_date` | date | Date analysis was conducted |
| `analysis_period_start` | date | Start of period being analysed |
| `analysis_period_end` | date | End of period being analysed |
| `period_type` | string | "current" or "projected" |
| `area_name` | string | Name of area (admin unit) |
| `area_code` | string | P-code of area |
| `admin_level` | integer | Administrative level (1, 2, or 3) |
| `area_phase` | integer | Overall phase classification (1-5) |
| `population_total` | integer | Total population analysed in area |
| `population_phase1` | integer | Population in Phase 1 |
| `population_phase2` | integer | Population in Phase 2 |
| `population_phase3` | integer | Population in Phase 3 |
| `population_phase4` | integer | Population in Phase 4 |
| `population_phase5` | integer | Population in Phase 5 |
| `population_phase3plus` | integer | Population in Phase 3 or above (crisis+) |
| `geometry` | GeoJSON | Area boundary polygon |

### Interpreting area vs population classifications

**Area classification:** Each area receives a single phase (1-5) based on the most severe conditions affecting at least 20% of the population. An area classified as Phase 3 means at least 20% of its population is in Phase 3 or worse.

**Population estimates:** The population breakdown shows how many people are in each phase within the area. An area classified as Phase 3 may still have most of its population in Phase 1 or 2 — the classification is driven by the 20% threshold rule.

**Humanitarian Food Assistance (HFA):** Some analyses include scenarios with and without humanitarian food assistance, showing what would happen if aid were removed.

---

## 8. Quality and Known Issues

### Strengths

- **Gold standard:** Most widely accepted and policy-relevant food security classification
- **Multi-evidence convergence:** Draws on multiple data sources, not a single indicator
- **Expert consensus:** Analysts debate and agree on classifications, reducing individual bias
- **Standardised methodology:** IPC 3.1 manual provides detailed protocols and reference tables
- **Population estimates:** Quantifies number of affected people, not just severity

### Known issues and limitations

| Issue | Detail | Impact on Causal Atlas |
|-------|--------|----------------------|
| **Irregular cadence** | Analyses are not monthly; gaps of 4-6 months between rounds | Requires interpolation or handling of irregular time series |
| **Coverage gaps** | Not all areas analysed every round; some areas dropped/added | Incomplete spatial panels |
| **Political interference** | Some governments contest unfavourable classifications, especially Famine declarations | Potential classification bias in politically sensitive contexts |
| **Methodological changes** | IPC 2.0 → 3.0 → 3.1 transitions affect comparability | Pre-2016 data may not be directly comparable |
| **Lag in reporting** | Analysis reflects conditions at time of assessment; publication may lag | Outdated by time of publication |
| **Subjectivity** | Despite protocols, expert consensus introduces human judgment | Some inter-analyst variability |
| **No household-level data** | Classifications are for areas, not individual households | Cannot capture within-area heterogeneity |
| **Projected period uncertainty** | Projections depend on assumptions about future conditions | Projected phases less reliable than current |
| **Urban coverage gaps** | Historically focused on rural areas; urban food insecurity underrepresented | Improving but still incomplete |
| **Humanitarian assistance accounting** | Difficult to assess what phase people "would be in" without aid | Phase 3+ with assistance may be Phase 4-5 without it |

### Data quality scoring

IPC analyses include evidence quality levels:
- **Acceptable:** Meets minimum evidence requirements
- **Medium:** Good evidence base
- **High:** Strong, multi-source evidence base

Areas with "*" (asterisk) in some analyses indicate limited evidence or methodological caveats.

---

## 9. Licence and Terms

### Data access terms

- IPC data is published for **open access** and humanitarian use
- The IPC API requires registration and approval of use case
- Attribution to IPC is required when using data
- HDX-hosted datasets follow HDX terms of use
- No explicit commercial restrictions documented, but primary audience is humanitarian

### Attribution

> "Source: IPC/Cadre Harmonise — www.ipcinfo.org"

---

## 10. Python Access

### Via IPC API

```python
import requests
import pandas as pd

IPC_API_KEY = 'your_api_key_here'
BASE_URL = 'https://api.ipcinfo.org'

def get_ipc_analyses(country_code=None, year=None):
    """
    Fetch IPC analysis data.

    Note: Exact endpoint structure may vary — check docs.api.ipcinfo.org
    for current specification after obtaining API key.
    """
    headers = {
        'Authorization': f'Bearer {IPC_API_KEY}',
        'Accept': 'application/json'
    }
    params = {}
    if country_code:
        params['country'] = country_code
    if year:
        params['year'] = year

    response = requests.get(f'{BASE_URL}/analyses', headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Example
analyses = get_ipc_analyses(country_code='SOM', year=2024)
```

### Via HDX (no API key needed)

```python
import pandas as pd
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

# Initialize HDX
Configuration.create(hdx_site='prod', user_agent='CausalAtlas')

# Search for IPC datasets
datasets = Dataset.search_in_hdx('IPC', rows=50)
for ds in datasets:
    print(f"{ds['name']}: {ds['title']}")

# Download a specific dataset
dataset = Dataset.read_from_hdx('cadre-harmonise')
resources = dataset.get_resources()
for r in resources:
    url, path = r.download()
    print(f"Downloaded: {path}")
```

### Via FEWS NET

```python
import requests
import pandas as pd

# FEWS NET provides IPC-compatible data
# Check https://fews.net/data for current download options

def download_fewsnet_ipc(country='SO', format='csv'):
    """Download FEWS NET food security classification data."""
    # Note: FEWS NET download URLs may change; check website
    url = f'https://fdw.fews.net/api/ipcpackage/?country_code={country}&format={format}'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse based on format
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        print(f"Error: {response.status_code}")
        return None
```

### Handling irregular temporal resolution

```python
import pandas as pd
import numpy as np

def ipc_to_monthly(ipc_data, start_col='analysis_period_start',
                   end_col='analysis_period_end', phase_col='area_phase'):
    """
    Expand IPC analysis periods to monthly time series.

    IPC analyses cover multi-month periods. This function creates
    monthly records by forward-filling the classification for each
    month within the analysis period.
    """
    monthly_records = []

    for _, row in ipc_data.iterrows():
        start = pd.Timestamp(row[start_col])
        end = pd.Timestamp(row[end_col])
        months = pd.date_range(start, end, freq='MS')

        for month in months:
            record = row.to_dict()
            record['month'] = month
            monthly_records.append(record)

    df_monthly = pd.DataFrame(monthly_records)
    return df_monthly

def interpolate_ipc_gaps(df, area_col='area_code', month_col='month',
                         phase_col='area_phase'):
    """
    Fill gaps between IPC analysis periods.

    Options:
    - Forward-fill: carry last known classification until next analysis
    - Linear interpolation: for population estimates
    - Flag as 'no data': most conservative approach
    """
    # Create complete monthly index per area
    all_months = pd.date_range(df[month_col].min(), df[month_col].max(), freq='MS')
    areas = df[area_col].unique()

    complete_index = pd.MultiIndex.from_product([areas, all_months],
                                                 names=[area_col, month_col])
    df_complete = df.set_index([area_col, month_col]).reindex(complete_index)

    # Forward fill phases (carry last known classification)
    df_complete[phase_col] = df_complete.groupby(level=0)[phase_col].ffill()

    # Flag interpolated vs observed
    df_complete['is_observed'] = df_complete['analysis_id'].notna()

    return df_complete.reset_index()
```

---

## 11. Interoperability with Other Causal Atlas Datasets

### Direct causal relationships

| Dataset | Relationship to IPC | Lag structure |
|---------|--------------------|-|
| **CHIRPS (precipitation)** | Drought → crop failure → food insecurity | 1-6 months (depends on crop calendar) |
| **ERA5 (temperature)** | Heat stress → crop damage → food insecurity | 1-3 months |
| **WFP food prices** | Price spikes → reduced food access → higher IPC phases | 1-3 months |
| **ACLED (conflict)** | Conflict → market disruption → food insecurity | 0-6 months |
| **FIRMS (fires)** | Cropland fires → food production loss | 1-6 months |
| **NDVI (vegetation)** | Low NDVI → poor harvest → food insecurity | 1-4 months |
| **IDMC/UNHCR (displacement)** | Food insecurity → displacement (and reverse) | Bidirectional, 0-3 months |
| **Disease outbreaks** | Food insecurity → malnutrition → disease vulnerability | 1-6 months |
| **Nightlights** | Economic decline → reduced food purchasing power | 3-12 months |

### Integration challenges with PRIO-GRID

IPC data uses **administrative boundaries** as spatial units, while PRIO-GRID uses **regular 0.5° grid cells**. Integration approaches:

1. **Area-weighted overlay:** Distribute IPC phase/population data to grid cells based on the proportion of each admin area falling in each grid cell
2. **Centroid assignment:** Assign IPC values to the grid cell containing the admin area centroid (lossy for large admin areas)
3. **Population-weighted overlay:** Use gridded population data (e.g., WorldPop) to distribute IPC population estimates to grid cells
4. **Dual spatial framework:** Maintain both admin-area and grid-cell representations, linking via spatial join

**Recommendation:** Use population-weighted overlay (option 3). This respects both the spatial boundaries of IPC analyses and the grid-cell framework of other datasets.

### Academic research using IPC data

IPC data has been used in numerous academic studies on food security and its drivers:

- Drought-food insecurity links in the Horn of Africa (using CHIRPS + IPC)
- Conflict-food insecurity dynamics in South Sudan, Yemen, and Nigeria
- Climate variability and food security in the Sahel
- Food price transmission and food security outcomes
- Displacement and host community food security impacts

The 2025 publication in *Scientific Data* (doi:10.1038/s41597-025-05034-4) describes a Harmonized Food Insecurity Dataset (HFID) that consolidates IPC/CH data with other sources into a monthly, sub-national panel dataset — highly relevant for Causal Atlas.

---

## 12. Relevance to Causal Atlas

### Why IPC is essential

IPC is the **primary food security outcome variable** for Causal Atlas. It provides:
- A standardised severity scale comparable across countries and time
- Population estimates (not just severity classifications)
- Both current and projected assessments
- The most policy-relevant food security measure available
- Sub-national spatial resolution in crisis-affected countries

### Key limitations to address

1. **Irregular temporal resolution:** IPC analyses are not monthly. The HFID dataset partially addresses this by harmonising to monthly frequency.
2. **Non-grid spatial units:** Administrative boundaries don't align with PRIO-GRID. Population-weighted spatial overlay is needed.
3. **Limited geographic scope:** Only crisis-affected countries. Cannot assess food security in stable countries.
4. **Backward-looking:** IPC classifications describe conditions during the analysis period; they are not predictive (though projections are provided).

### Implementation priority

1. **Phase 1:** Obtain IPC API access; download all available historical analyses
2. **Phase 2:** Build admin-area to PRIO-GRID spatial crosswalk using population-weighted overlay
3. **Phase 3:** Create monthly time series using HFID methodology (expand analysis periods, forward-fill gaps)
4. **Phase 4:** Cross-correlate with CHIRPS drought, WFP prices, ACLED conflict to validate causal chains
5. **Phase 5:** Use IPC as target variable for causal discovery (which combinations of climate, conflict, and economic variables best predict IPC transitions?)

### Causal chains terminating at IPC

- **Climate chain:** Low CHIRPS → low NDVI → poor harvest → high food prices → IPC Phase 3+
- **Conflict chain:** ACLED events → market disruption → supply chain breakdown → IPC Phase 3+
- **Price chain:** Global commodity prices → local WFP food prices → reduced access → IPC Phase 3+
- **Displacement chain:** Conflict/disaster → displacement (IDMC) → host community pressure → IPC Phase 3+
- **Compound chain:** Drought + conflict → crop failure + market disruption → IPC Phase 4/5

---

## Sources

- IPC website: https://www.ipcinfo.org
- IPC Overview and Classification System: https://www.ipcinfo.org/ipcinfo-website/ipc-overview-and-classification-system/en/
- IPC Acute Food Insecurity Classification: https://www.ipcinfo.org/ipcinfo-website/ipc-overview-and-classification-system/ipc-acute-food-insecurity-classification/en/
- IPC API page: https://www.ipcinfo.org/ipc-country-analysis/api/
- IPC API documentation: https://docs.api.ipcinfo.org/
- IPC API launch announcement: https://www.ipcinfo.org/ipcinfo-website/featured-stories/news-details/en/c/1155546/
- IPC Famine fact sheet: https://www.ipcinfo.org/ipcinfo-website/resources/resources-details/en/c/1129202/
- IPC FAQs: https://www.ipcinfo.org/ipcinfo-website/faqs/en/
- Cadre Harmonise on IPC: https://www.ipcinfo.org/ch/
- CH-IPC collaboration: https://www.ipcinfo.org/ipcinfo-website/where-what/the-ch-ipc-collaboration/en/
- CH on HDX: https://data.humdata.org/dataset/cadre-harmonise
- IPC on HDX: https://data.humdata.org/organization/ipc
- IPC on World Bank Data360: https://data360.worldbank.org/en/dataset/IPC_IPC
- IPC on FAO: https://data.apps.fao.org/catalog/dataset/ipc-info-tool
- FEWS NET acute food insecurity: https://fews.net/data/acute-food-insecurity
- Harmonized Food Insecurity Dataset (HFID): https://www.nature.com/articles/s41597-025-05034-4
- IPC Wikipedia: https://en.wikipedia.org/wiki/Integrated_Food_Security_Phase_Classification
- FSC Handbook IPC section: https://handbook.fscluster.org/docs/671-integrated-phase-classification
- CH Handbook section: https://handbook.fscluster.org/docs/672-cadre-harmonis%C3%A9
- CH-IPC API on ReliefWeb: https://reliefweb.int/report/world/cadre-harmonise-ch-integrated-food-security-phase-classification-ipc-application-programming-interface-api
