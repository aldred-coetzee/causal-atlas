# EM-DAT: The International Disaster Database

**Deep-dive research for Causal Atlas**
**Last updated:** March 2025

---

## 1. Overview

EM-DAT (Emergency Events Database) is the most widely used global database of natural and technological disasters. It records the occurrence and impacts of mass disasters worldwide from 1900 to the present, with systematic recording beginning in 1988.

| Attribute | Detail |
|---|---|
| **Full name** | Emergency Events Database (EM-DAT) |
| **Maintained by** | Centre for Research on the Epidemiology of Disasters (CRED), UCLouvain, Brussels, Belgium |
| **Founded** | 1988, as a joint initiative between CRED and the World Health Organization (WHO) |
| **Funding** | Belgian Government; USAID Bureau for Humanitarian Assistance (formerly OFDA) from 1999 through early 2025 |
| **Current version** | 2025.10 (as of March 2025) |
| **Record count** | ~27,000+ disaster events |
| **Website** | [https://www.emdat.be/](https://www.emdat.be/) |
| **Documentation** | [https://doc.emdat.be/](https://doc.emdat.be/) |
| **Public portal** | [https://public.emdat.be/](https://public.emdat.be/) |
| **Descriptor paper** | Delforge et al. (2025), DOI: [10.1016/j.ijdrr.2025.105509](https://doi.org/10.1016/j.ijdrr.2025.105509) |

### Purpose

EM-DAT serves humanitarian action, disaster preparedness, decision-making, vulnerability assessment, and risk evaluation. It is compiled from UN agencies, non-governmental organisations, insurance companies, research institutes, and press agencies.

### Entry Criteria

A disaster is included in EM-DAT if it meets **at least one** of the following thresholds:

1. **At least 10 deaths** (including dead and missing)
2. **At least 100 people affected** (injured, affected, or homeless)
3. **A declaration of a state of emergency**
4. **A call for international assistance**

Additionally, at least **two distinct sources** must be attached to an entry before it is made public.

For historical events lacking quantitative data, supplementary criteria include designation as "the worst disaster in a country or region" or events producing "considerable damage."

> **Note:** The thresholds of 10 and 100 are acknowledged by CRED as arbitrary. This creates a significant threshold bias -- see Section 7 for details.

---

## 2. Coverage

### Spatial Extent

- **Global** coverage at the **country level** (primary unit)
- Sub-national location data available for non-biological natural hazards since 2000 (see Section 5)
- Uses ISO 3166 alpha-3 country codes and UN M49 regional classification

### Temporal Range

- Records from **1900 to present**
- Systematic, reliable recording from **1988 onward** (when CRED took over the database)
- Significant increase in recorded events from the **1960s** (coinciding with OFDA creation in 1973)
- CRED recommends **excluding pre-2000 data from trend analyses** due to reporting improvements inflating apparent disaster counts

### Update Frequency

- **Weekly** updates to the public table
- Country profile summaries on HDX updated weekly
- Annual year-in-review publications (CRED Crunch series)

---

## 3. Access

### 3.1 Public Portal (Primary Access)

| Detail | Value |
|---|---|
| **URL** | [https://public.emdat.be/](https://public.emdat.be/) |
| **Registration** | Required (free for non-commercial use) |
| **Download format** | Microsoft Excel (.xlsx) flat table |
| **Interface** | Web-based "Access Data" tab and Toolbox with filtering |

**Registration process:** Create an account at public.emdat.be, agree to the Terms of Use, then access data through the portal's query interface. Filtering by country, year range, disaster type, etc. is available before download.

### 3.2 GraphQL API

| Detail | Value |
|---|---|
| **Endpoint** | `https://api.emdat.be/v1` |
| **Interactive explorer** | [https://api.emdat.be/](https://api.emdat.be/) (GraphiQL interface) |
| **Authentication** | API key passed as HTTP header: `{"Authorization": "<your-api-key>"}` |
| **API key source** | Obtained after registration on public.emdat.be |
| **Query language** | GraphQL |
| **Documentation** | [API Cookbook (PDF)](https://files.emdat.be/docs/emdat_api_cookbook.pdf), [Python guide (PDF)](https://files.emdat.be/docs/emdat_api_python.pdf), [R guide (PDF)](https://files.emdat.be/docs/emdat_api_rlang.pdf) |

**Key query:** `public_emdat` -- has 2 implicit limitations activated by default. Queries support commenting with `#`.

**Example GraphQL query:**
```graphql
{
  public_emdat(
    filters: {
      disaster_type: "Flood"
      country: "BGD"
      from: 2000
      to: 2023
    }
  ) {
    disno
    classif_key
    group
    subgroup
    type
    subtype
    country
    start_year
    total_deaths
    total_affected
    total_dam
  }
}
```

### 3.3 UCLouvain Dataverse (Archive)

- EM-DAT Archive hosted on the UCLouvain Dataverse
- FAIR-compliant versioned snapshots
- Licence: **CC-BY-NC-ND** (Creative Commons Attribution-NonCommercial-NoDerivatives)
- Recommended for reproducible scientific research

### 3.4 Humanitarian Data Exchange (HDX)

- Aggregated country profile summaries available at [HDX - CRED](https://data.humdata.org/organization/cred)
- Updated weekly
- Publicly accessible via the HDX API (no registration required for HDX)
- Includes HXL metadata tagging for machine-readable annotations
- Columns: Year, Country, ISO code, disaster classifications, event counts, affected persons, deaths, damage in USD

### 3.5 EM-VIEW Dashboard

- EM-VIEW is a visualisation/dashboard tool for the EM-DAT user community
- Designed to speed up data visualisation capacity
- Recently released alongside the EM-DAT Archive product

---

## 4. Schema -- Full Field Dictionary

The EM-DAT public table contains the following fields (as of version 2025.10):

### 4.1 Identification Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `DisNo.` | ID (8-digit + ISO) | Mandatory | Unique identifier: 4-digit year + 4-digit sequence number. ISO country code appended in public table. Example: `2024-0001-BGD` |
| `Historic` | Yes/No | Mandatory | Binary flag for pre-2000 disasters (based on Start Year). Signals lower data quality. |
| `Classification Key` | ID (15-char) | Mandatory | Unique string encoding the full classification hierarchy (Group > Subgroup > Type > Subtype) |
| `External IDs` | IDs List | Optional | Identifiers from external sources (GLIDE, USGS, DFO, HANZE). Format: `source:identifier` separated by pipe `|` |
| `Event Name` | Text | Optional | Short name (e.g., storm name, disease name) |

### 4.2 Classification Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Disaster Group` | Name | Mandatory | Primary level: **Natural** or **Technological** |
| `Disaster Subgroup` | Name | Mandatory | Secondary level (e.g., Meteorological, Geophysical, Industrial accident) |
| `Disaster Type` | Name | Mandatory | Tertiary level (e.g., Earthquake, Flood, Storm) |
| `Disaster Subtype` | Name | Mandatory | Quaternary level (e.g., Tropical cyclone, Flash flood, Ground movement) |
| `Associated Types` | Names List | Optional | Secondary disaster types cascading from or co-occurring with primary type. Pipe-separated. |

### 4.3 Geographic Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `ISO` | ID (3-letter) | Mandatory | ISO 3166 alpha-3 country code. Includes non-standard codes for historical entities (e.g., `YUG`, `CSK`, `SUN`) |
| `Country` | Name | Mandatory | Country name per UN M49 Standard |
| `Subregion` | Name | Mandatory | UN M49 subregion (auto-linked to country) |
| `Region` | Name | Mandatory | UN M49 region/continent (auto-linked to country) |
| `Location` | Text | Optional | Geographical location name from sources (city, province, etc.) |
| `Latitude` | Degrees [-90, 90] | Optional | North-South coordinate. Mainly for earthquakes and volcanic activity |
| `Longitude` | Degrees [-180, 180] | Optional | East-West coordinate. Mainly for earthquakes and volcanic activity |
| `River Basin` | Text | Optional | Name of affected river basins (typically for floods) |

### 4.4 Administrative Unit Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Admin Units` | JSON Array | Optional | **DEPRECATED (2025)**. FAO GAUL 2015 administrative units (up to Admin-2) |
| `GADM Admin Units` | JSON Array | Optional | GADM v4.1 administrative units. Includes migration metadata from GAUL matching |

### 4.5 Context Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Origin` | Text | Optional | Contextual factors (e.g., "heavy rains", "drought") |
| `OFDA/BHA Response` | Yes/No | Optional | **DEPRECATED (2025)**. Whether OFDA/BHA responded |
| `Appeal` | Yes/No | Mandatory | Whether international assistance was requested |
| `Declaration` | Yes/No | Mandatory | Whether a state of emergency was declared |
| `AID Contribution ('000 US$)` | Monetary | Optional | **DEPRECATED (2015)**. Relief contributions via OCHA FTS, in thousands USD |
| `Magnitude` | Varies | Optional | Intensity measure (disaster-type-dependent units) |
| `Magnitude Scale` | Text | Optional | Unit for the Magnitude field (e.g., Richter, km/h, Celsius) |

### 4.6 Temporal Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Start Year` | Numeric | Mandatory | Year of disaster occurrence |
| `Start Month` | Numeric | Optional | Month of occurrence (blank for gradual-onset events) |
| `Start Day` | Numeric | Optional | Day of occurrence (blank for gradual-onset events) |
| `End Year` | Numeric | Optional | Year of disaster conclusion |
| `End Month` | Numeric | Optional | Month of conclusion |
| `End Day` | Numeric | Optional | Day of conclusion |

### 4.7 Human Impact Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Total Deaths` | Numeric | Optional | Total fatalities (deceased + missing combined) |
| `No. Injured` | Numeric | Optional | People with physical injuries, trauma, or illness requiring immediate medical assistance |
| `No. Affected` | Numeric | Optional | People requiring immediate assistance |
| `No. Homeless` | Numeric | Optional | People requiring shelter (house destroyed or heavily damaged) |
| `Total Affected` | Numeric | Optional | Sum of Injured + Affected + Homeless |

### 4.8 Economic Impact Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Reconstruction Costs ('000 US$)` | Monetary | Optional | Cost for replacement of lost assets (unadjusted, thousands USD) |
| `Reconstruction Costs, Adjusted ('000 US$)` | Monetary | Optional | CPI-adjusted version |
| `Insured Damage ('000 US$)` | Monetary | Optional | Economic damage covered by insurance (unadjusted) |
| `Insured Damage, Adjusted ('000 US$)` | Monetary | Optional | CPI-adjusted version |
| `Total Damage ('000 US$)` | Monetary | Optional | All economic losses directly or indirectly due to the disaster (unadjusted) |
| `Total Damage, Adjusted ('000 US$)` | Monetary | Optional | CPI-adjusted version |
| `CPI` | Ratio | Optional | Consumer Price Index from OECD used for inflation adjustment |

### 4.9 Metadata Fields

| Field Name | Type | Required | Description |
|---|---|---|---|
| `Entry Date` | Date | Mandatory | Date the record was created in EM-DAT |
| `Last Update` | Date | Mandatory | Last modification date (may reflect non-public field edits) |

### Important Notes on Schema

- **Empty cells** are ambiguous: they may indicate no impact, unknown impact, or unreported data. There is no distinction between these cases.
- **Three deprecated fields**: `OFDA/BHA Response`, `AID Contribution`, and `Admin Units` (GAUL 2015).
- **Economic fields** come in both unadjusted and CPI-adjusted pairs.
- All monetary values are in **thousands of US dollars**.

---

## 5. Spatial Detail

### Primary Spatial Unit

EM-DAT is fundamentally a **country-level** database. The `ISO` field (ISO 3166 alpha-3) is the primary geographic identifier. Impact variables (deaths, affected, damage) are reported at the country level and are **not disaggregated** to sub-national administrative units.

### Sub-national Location Data

- The `Location` field provides free-text descriptions of affected areas (cities, provinces, etc.)
- Between 2014 and 2025, EM-DAT used **FAO GAUL 2015** administrative unit layers (up to Admin-2 / district level) to encode affected regions
- From 2025/2026 onward, EM-DAT has transitioned to **GADM v4.1** as the geocoding standard
- Sub-national geocoding has been completed only for **non-biological natural-hazard data since 2000**
- As of January 2026, approximately **90% of GAUL 2015 footprints** have been matched to corresponding GADM 4.1 footprints

### GADM Migration Methodology

Four translation methods were used to map GAUL units to GADM:
1. **Jaccard Index overlap matching** (`jaccard1`, `jaccard2`)
2. **One-to-many puzzle composition** (`puzzle1_1`, `puzzle1_2`, `puzzle2_2`)
3. **Buffer + Hausdorff distance** for isolated territories (`bufhaus1`, `bufhaus2`)
4. **Upward fallback strategy** (`parent2_1`, `within2_1`)

Polygons were simplified using a Douglas-Peucker implementation with tolerance of 0.005 degrees (~550 m at the equator), using WGS 84 (EPSG 4326).

### Latitude/Longitude

Point coordinates (`Latitude`, `Longitude`) are available **mainly for earthquakes and volcanic activity**. Coverage for other disaster types is sparse.

### GDIS: Geocoded Disaster Locations Dataset

A critical companion dataset for sub-national spatial analysis:

| Attribute | Detail |
|---|---|
| **Full name** | Geocoded Disasters (GDIS) Dataset |
| **Authors** | Rosvold, E. L. & Buhaug, H. (2021) |
| **Published in** | *Scientific Data*, DOI: [10.1038/s41597-021-00846-6](https://doi.org/10.1038/s41597-021-00846-6) |
| **Coverage** | 39,953 locations for 9,924 unique disasters, 1960--2018 |
| **Disaster types** | Floods, storms, earthquakes, landslides, droughts, volcanic activity, extreme temperatures |
| **Spatial resolution** | Up to Admin-3 (district/commune), majority at Admin-1 (state/province) |
| **Format** | GIS polygons + centroid lat/lon coordinates |
| **Access** | [NASA SEDAC](https://sedac.ciesin.columbia.edu/data/set/pend-gdis-1960-2018), open access |

GDIS is essential for connecting EM-DAT records to other sub-national data sources (e.g., PRIO-GRID cells).

---

## 6. Temporal Detail

### Timestamp Resolution

- **Year** is mandatory (`Start Year`)
- **Month** and **day** are optional for both start and end dates
- For **sudden-onset events** (earthquakes, cyclones), day-level precision is typically available
- For **gradual-onset events** (droughts, epidemics), month and day fields are frequently blank
- No intra-day (hour/minute) timestamps are recorded

### Implications for Causal Atlas

- Monthly aggregation is feasible for most post-2000 data, but expect missing months for gradual-onset events
- Precise start/end dates enable temporal lag analysis for sudden-onset disasters
- For drought events, temporal boundaries are inherently fuzzy and may not align well with monthly grids

---

## 7. Quality -- Known Biases, Gaps, and Limitations

EM-DAT's own documentation is unusually transparent about its limitations. The following is drawn from [EM-DAT Known Issues and Limitations](https://doc.emdat.be/docs/known-issues-and-limitations/), supplemented by academic validation studies.

### 7.1 Three Core Data Quality Problems

1. **Missing events** -- Disaster occurrences not captured in EM-DAT at all
2. **Incomplete records** -- Existing events lacking values for impact variables
3. **Inaccurate attributes** -- Recorded events with values that diverge from other sources

### 7.2 Threshold Bias

The entry criteria (10+ deaths or 100+ affected) systematically exclude small-scale disasters. However, research has shown that **cumulative mortality from low-mortality events (2000--2022) exceeded that from higher-mortality events**, indicating substantial undercounting of small but collectively significant disasters.

### 7.3 Time Bias

- Pre-1960s data is extremely sparse
- The 1960s--1990s saw a dramatic increase in recorded events due to institutional developments (OFDA, CRED) and communications technology (satellites, personal computers, the web), not necessarily an actual increase in disasters
- **CRED recommends excluding pre-2000 data from trend analyses**
- Events flagged with `Historic = Yes` are pre-2000 and should be treated with caution

### 7.4 Geographic Bias

- **Sub-Saharan Africa** has notably worse coverage for both disaster occurrence and impact variables
- Heat waves are particularly underreported in Africa
- Approximately **52% of recorded heatwave events** are concentrated in just 9 countries (Japan, India, Pakistan, USA, and 4 Western European nations)
- Disaster reporting quality correlates with national institutional capacity and media infrastructure

### 7.5 Hazard-Related Bias

- **Biological hazards** (epidemics) and **extreme temperature events** (heat waves) have systematically lower coverage and data quality compared to other hazard types
- Droughts often have underreported indirect mortality
- Compound events (e.g., cyclone + flood + landslide) are difficult to represent in EM-DAT's flat table structure

### 7.6 Accounting Bias

- **Economic losses** are reported less frequently than human impact variables
- **Insured damages** are overrepresented versus uninsured damages, creating a geographic wealth bias (developed countries have higher insurance penetration)
- Missing values in impact fields are ambiguous (no impact vs. unknown vs. unreported)

### 7.7 Systemic Bias

Different reporting institutions use different methodologies for measuring deaths, affected populations, and economic costs. There is no universally applied protocol for:
- Event start and end dates
- Geographic disaster extent
- Impact metrics definitions
- Disaster type classification

This was termed "systemic bias" by Gall et al. (2009).

### 7.8 Validation Studies

**Panwar & Sen (2020)** -- "Disaster Damage Records of EM-DAT and DesInventar: A Systematic Comparison" (*Economics of Disasters and Climate Change*):
- Compared EM-DAT and DesInventar for 70 countries over 1995--2013 (droughts, floods, earthquakes, storms)
- DesInventar recorded a **greater number of events** (captures sub-threshold disasters)
- For hand-matched events, EM-DAT showed **larger mean disaster damages** and higher statistical range
- Basic differences in data collection methods influence recorded damage magnitude
- DOI: [10.1007/s41885-019-00052-0](https://doi.org/10.1007/s41885-019-00052-0)

**Mountain region analysis** (Springer, various authors):
- Compared EM-DAT, DesInventar, NatCatSERVICE, and Sigma for mountain disasters
- Found fatality numbers are the most reliable loss parameter
- Affected persons and economic loss are less trustworthy and highly database-dependent

**General findings from validation literature:**
- EM-DAT is the only comprehensive, free-access disaster loss database with effective global coverage
- No current impact database is completely accurate
- Fatality data is the most reliable variable; economic data is the least

---

## 8. Licence and Terms of Use

### Non-Commercial Use (Free)

Eligible entities for free access:
- Academic organisations and universities
- Non-profit research institutions
- International public organisations (UN agencies, multilateral banks, national governments)
- Media agencies (journalists, press agencies)

**Conditions:**
- Must register on [public.emdat.be](https://public.emdat.be/)
- Must accept the [Terms of Use](https://doc.emdat.be/docs/legal/terms-of-use/)
- Must provide proper citation in all published materials

### Commercial Use (Paid)

- Requires a separate [Database License Agreement](https://doc.emdat.be/docs/legal/database-license-agreement/)
- Annual paid subscription (pricing negotiated individually)
- Contact: Regina Below (regina.below@uclouvain.be)
- Must describe commercial purpose and number of users

### Prohibited Uses

- Reproducing, copying, or distributing EM-DAT or a substantial part
- Reverse engineering, decompiling, or disassembling the database
- Developing competing or substitute databases
- Bypassing security systems
- Sharing data via Internet to unauthorised parties
- Removing copyright notices
- Using for commercial purposes without a separate licence

### Citation Requirements

All publications must include a "Proper Citation" with:
- Year of access
- The acronym "EM-DAT" (with dash) plus product specificity
- Corresponding URL or DOI

**Example citation:** `EM-DAT, CRED / UCLouvain, Brussels, Belgium -- www.emdat.be (D. Guha-Sapir)`

For scientific publications, also cite the 2025 descriptor paper:
> Delforge, D., Wathelet, V., Below, R., Lanfredi Sofia, C., Tonnelier, M., van Loenhout, J. A. F. & Speybroeck, N. (2025). EM-DAT: the Emergency Events Database. *International Journal of Disaster Risk Reduction*, 105509. DOI: [10.1016/j.ijdrr.2025.105509](https://doi.org/10.1016/j.ijdrr.2025.105509)

### Archive Licence

The EM-DAT Archive on UCLouvain Dataverse is published under **CC-BY-NC-ND** (Creative Commons Attribution-NonCommercial-NoDerivatives).

### Implications for Causal Atlas

Causal Atlas is open source and non-commercial, so free access should be available. However:
- We **cannot redistribute** EM-DAT data directly in our repository or via our API
- Users would need their own EM-DAT registration, or we ingest and transform data sufficiently that it constitutes derived analysis rather than reproduction
- The CC-BY-NC-ND licence on the Archive is restrictive -- no derivative works allowed
- We should consult with CRED about our intended use case

---

## 9. Interoperability -- Shared Identifiers

### Country Codes

- **ISO 3166 alpha-3** codes in the `ISO` field -- directly compatible with virtually all other international datasets
- **UN M49** standard for region/subregion -- compatible with UN statistical datasets
- Non-standard historical codes (`YUG`, `CSK`, `SUN`) need special handling

### External Event Identifiers

The `External IDs` field links EM-DAT records to:
- **GLIDE** (GLobal IDEntifier) numbers -- the international standard for disaster event identification
- **USGS** earthquake IDs -- linkable to USGS earthquake catalogue
- **DFO** (Dartmouth Flood Observatory) IDs
- **HANZE** (Historical Analysis of Natural Hazards in Europe) IDs

### Administrative Boundaries

- **GADM v4.1** admin units (current) -- compatible with GADM-based datasets worldwide
- **FAO GAUL 2015** (deprecated but still in data) -- compatible with older datasets using GAUL

### Linking to Other Causal Atlas Datasets

| Dataset | Linking mechanism | Feasibility |
|---|---|---|
| **ACLED** (conflict) | ISO country code + date overlap | Good at country-month level |
| **UCDP-GED** (conflict) | ISO country code + date overlap | Good at country-month level |
| **WFP food prices** | ISO country code + month/year | Good at country-month level |
| **CHIRPS** (rainfall) | Requires GDIS geocoding for sub-national link | Moderate -- only for geocoded events |
| **PRIO-GRID** | Requires GDIS or GADM admin unit geocoding | Moderate -- limited to geocoded events post-2000 |
| **World Bank indicators** | ISO country code + year | Good at country-year level |
| **HDX HAPI** | ISO country code + admin level | Good via HDX standardisation |
| **USGS earthquakes** | External IDs field (USGS IDs) or lat/lon matching | Good for earthquakes specifically |
| **OpenAQ** (air quality) | ISO country code; sub-national requires geocoding | Limited |
| **MODIS NDVI** | Requires GDIS geocoding for spatial join | Moderate |
| **VIIRS nightlights** | Requires GDIS geocoding for spatial join | Moderate |

---

## 10. Python Access

### 10.1 Direct Pandas Access (Recommended)

The simplest and most common method:

```python
import pandas as pd

# Download .xlsx from public.emdat.be after registration
df = pd.read_excel('public_emdat_2025-03-01.xlsx')

# Inspect structure
print(df.info())
print(df.columns.tolist())
print(df.head())

# Filter: floods in Bangladesh since 2000
floods_bgd = df[
    (df['Disaster Type'] == 'Flood') &
    (df['ISO'] == 'BGD') &
    (df['Start Year'] >= 2000)
][['DisNo.', 'Start Year', 'Start Month', 'Total Deaths', 'Total Affected', 'Total Damage (\'000 US$)']]

# Aggregate by year
annual = floods_bgd.groupby('Start Year').agg({
    'Total Deaths': 'sum',
    'Total Affected': 'sum'
}).reset_index()
```

**Dependencies:** `pandas`, `openpyxl` (for reading .xlsx)

### 10.2 GraphQL API Access (Python)

```python
import requests
import pandas as pd

API_URL = "https://api.emdat.be/v1"
API_KEY = "your-api-key-here"  # Obtained from public.emdat.be after registration

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

query = """
{
  public_emdat(
    filters: {
      disaster_type: "Flood"
      country: "BGD"
      from: 2000
      to: 2024
    }
  ) {
    disno
    country
    type
    subtype
    start_year
    start_month
    total_deaths
    total_affected
    total_dam
  }
}
"""

response = requests.post(API_URL, json={"query": query}, headers=headers)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data['data']['public_emdat'])
```

**Using the `gql` library (recommended by EM-DAT docs):**

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="https://api.emdat.be/v1",
    headers={"Authorization": "your-api-key-here"}
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
{
  public_emdat(
    filters: {
      disaster_type: "Earthquake"
      from: 2010
      to: 2024
    }
  ) {
    disno
    country
    start_year
    start_month
    magnitude
    total_deaths
    total_affected
  }
}
""")

result = client.execute(query)
```

**Dependencies:** `gql`, `requests`, `requests-toolbelt`

### 10.3 pyEmdat Library (GFDRR)

Third-party library from the Global Facility for Disaster Reduction and Recovery:

| Attribute | Detail |
|---|---|
| **Repository** | [https://github.com/GFDRR/pyEmdat](https://github.com/GFDRR/pyEmdat) |
| **Documentation** | [https://pyemdat.readthedocs.io/](https://pyemdat.readthedocs.io/) |
| **Status** | Low activity (30 commits on master), may be unmaintained |
| **Input** | Requires pre-downloaded EM-DAT Excel file |

```python
from emdat_df import emdat

# Load from downloaded Excel file
ED = emdat('path/to/my_EMDAT_download.xlsx')

# Time series of disaster counts by type
df = ED.disaster_count_timeseries(
    1960, 2020,
    countries='all',
    disastertype=['Storm', 'Flood', 'Earthquake', 'Volcanic activity', 'Landslide']
)
```

**Features:**
- Load and clean EM-DAT data
- Summarise disaster statistics by country (single period and time series)
- Summarise statistics by hazard type
- Combine with World Development Indicators (population, GNI) via World Bank API

**Caveat:** Given low maintenance activity, direct pandas access is likely more reliable for production use.

### 10.4 HDX Access (No Registration Required)

```python
import requests
import pandas as pd

# HDX CRED datasets page
hdx_url = "https://data.humdata.org/api/3/action/package_show?id=emdat-country-profiles"
response = requests.get(hdx_url)
resources = response.json()['result']['resources']

# Find and download CSV resource
for r in resources:
    if r['format'] == 'CSV':
        df = pd.read_csv(r['url'])
        break
```

**Note:** HDX provides aggregated country-level summaries, not individual disaster event records.

---

## 11. Relevance to Causal Atlas

### Domains Covered

EM-DAT spans multiple domains critical to Causal Atlas:

| Domain | EM-DAT Coverage |
|---|---|
| **Natural disasters** | Earthquakes, floods, storms, droughts, wildfires, volcanic eruptions, landslides |
| **Biological hazards** | Epidemics (bacterial, viral, parasitic, fungal, prion diseases), infestations |
| **Climatological events** | Droughts, wildfires, glacial lake outburst floods |
| **Extreme weather** | Heat waves, cold waves, severe winter conditions, fog |
| **Technological disasters** | Industrial accidents, chemical spills, explosions, radiation events, transport accidents |
| **Economic impacts** | Total damage, insured damage, reconstruction costs (unadjusted and CPI-adjusted) |
| **Human impacts** | Deaths, injuries, affected populations, homelessness |

### Causal Chains EM-DAT Can Support

1. **Disaster -> Food insecurity**: Floods/droughts destroying crops, disrupting supply chains. Link EM-DAT disaster records to WFP food price data by country and month.

2. **Disaster -> Conflict escalation/de-escalation**: Research shows ~29% of armed conflicts escalate after climate disasters, ~33% de-escalate (dependent on relative power shifts). Link EM-DAT to ACLED/UCDP-GED by country and temporal overlap.

3. **Disaster -> Economic disruption**: Total damage and reconstruction cost fields provide direct economic impact data. Link to World Bank indicators and VIIRS nightlights for validation.

4. **Disaster -> Migration/displacement**: `No. Homeless` and `No. Affected` fields capture displacement. Link to UNHCR/IOM displacement data.

5. **Disaster -> Health outcomes**: Epidemic records plus disaster aftermath health effects. Link to WHO/IHME data.

6. **Climate -> Disaster frequency**: Temporal trends in disaster occurrence by type. Link to CHIRPS rainfall and temperature anomaly data.

7. **Disaster -> Disaster cascades**: The `Associated Types` field captures cascading events (e.g., earthquake -> tsunami, storm -> flood -> landslide).

### Integration Strategy for Causal Atlas

**Recommended approach:**

1. **Ingest via GraphQL API** for programmatic access to individual event records
2. **Primary join key:** ISO country code + year/month for country-level analysis
3. **Sub-national analysis:** Use GDIS dataset (1960--2018) or GADM admin units (post-2000) to create spatial joins with PRIO-GRID cells
4. **Temporal alignment:** Aggregate to monthly resolution using `Start Year` + `Start Month`; handle missing months via imputation or flagging
5. **Store disaster counts and impact metrics** as time series per country-month or grid cell-month
6. **Handle missing data explicitly** -- distinguish "no disasters occurred" from "no data available" using the `Historic` flag and known geographic biases

**Limitations to manage:**
- Threshold bias means small but cumulatively significant events are missed
- Sub-national geocoding only available for non-biological natural hazards post-2000
- Impact variables are not disaggregated below country level
- Economic data has significant gaps, especially in developing countries
- Pre-2000 trend analysis is unreliable due to reporting improvements

---

## 12. Sources

### Primary Documentation
- EM-DAT Homepage: [https://www.emdat.be/](https://www.emdat.be/)
- EM-DAT Documentation Portal: [https://doc.emdat.be/](https://doc.emdat.be/)
- EM-DAT Public Portal: [https://public.emdat.be/](https://public.emdat.be/)
- EM-DAT Introduction: [https://doc.emdat.be/docs/introduction/](https://doc.emdat.be/docs/introduction/)
- Data Structure and Content: [https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/](https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/)
- Entry Criteria: [https://doc.emdat.be/docs/protocols/entry-criteria/](https://doc.emdat.be/docs/protocols/entry-criteria/)
- Spatial Information and Geocoding: [https://doc.emdat.be/docs/data-structure-and-content/spatial-information/](https://doc.emdat.be/docs/data-structure-and-content/spatial-information/)
- Data Accessibility: [https://doc.emdat.be/docs/data-accessibility/](https://doc.emdat.be/docs/data-accessibility/)
- Known Issues and Limitations: [https://doc.emdat.be/docs/known-issues-and-limitations/](https://doc.emdat.be/docs/known-issues-and-limitations/)
- Specific Biases: [https://doc.emdat.be/docs/known-issues-and-limitations/specific-biases/](https://doc.emdat.be/docs/known-issues-and-limitations/specific-biases/)
- General Issues: [https://doc.emdat.be/docs/known-issues-and-limitations/general-issues/](https://doc.emdat.be/docs/known-issues-and-limitations/general-issues/)
- Terms of Use: [https://doc.emdat.be/docs/legal/terms-of-use/](https://doc.emdat.be/docs/legal/terms-of-use/)
- Citation Policy: [https://doc.emdat.be/docs/legal/citation-policy/](https://doc.emdat.be/docs/legal/citation-policy/)
- Commercial Licence: [https://doc.emdat.be/docs/legal/database-license-agreement/](https://doc.emdat.be/docs/legal/database-license-agreement/)
- Disaster Classification System: [https://doc.emdat.be/docs/data-structure-and-content/disaster-classification-system/](https://doc.emdat.be/docs/data-structure-and-content/disaster-classification-system/)
- Python Tutorial 1: [https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_1/](https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_1/)
- Python Tutorial 2: [https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/](https://doc.emdat.be/docs/additional-resources-and-tutorials/tutorials/python_tutorial_2/)

### API Documentation
- GraphQL API Cookbook: [https://files.emdat.be/docs/emdat_api_cookbook.pdf](https://files.emdat.be/docs/emdat_api_cookbook.pdf)
- Python API Guide: [https://files.emdat.be/docs/emdat_api_python.pdf](https://files.emdat.be/docs/emdat_api_python.pdf)
- R API Guide: [https://files.emdat.be/docs/emdat_api_rlang.pdf](https://files.emdat.be/docs/emdat_api_rlang.pdf)
- GraphiQL Interface: [https://api.emdat.be/](https://api.emdat.be/)

### External Data Products
- HDX Country Profiles: [https://data.humdata.org/organization/cred](https://data.humdata.org/organization/cred)
- GDIS Dataset (NASA SEDAC): [https://sedac.ciesin.columbia.edu/data/set/pend-gdis-1960-2018](https://sedac.ciesin.columbia.edu/data/set/pend-gdis-1960-2018)
- GADM v4.1: [https://gadm.org/](https://gadm.org/)
- Monty Extension (IFRC): [https://ifrcgo.org/monty-stac-extension/model/sources/EM-DAT/](https://ifrcgo.org/monty-stac-extension/model/sources/EM-DAT/)

### Python Libraries
- pyEmdat (GFDRR): [https://github.com/GFDRR/pyEmdat](https://github.com/GFDRR/pyEmdat)
- pyEmdat docs: [https://pyemdat.readthedocs.io/](https://pyemdat.readthedocs.io/)

### Academic Papers

- Delforge, D., Wathelet, V., Below, R., Lanfredi Sofia, C., Tonnelier, M., van Loenhout, J. A. F. & Speybroeck, N. (2025). EM-DAT: the Emergency Events Database. *International Journal of Disaster Risk Reduction*, 105509. DOI: [10.1016/j.ijdrr.2025.105509](https://doi.org/10.1016/j.ijdrr.2025.105509)

- Rosvold, E. L. & Buhaug, H. (2021). GDIS, a global dataset of geocoded disaster locations. *Scientific Data*, 8, 61. DOI: [10.1038/s41597-021-00846-6](https://doi.org/10.1038/s41597-021-00846-6)

- Panwar, V. & Sen, S. (2020). Disaster Damage Records of EM-DAT and DesInventar: A Systematic Comparison. *Economics of Disasters and Climate Change*, 4(2). DOI: [10.1007/s41885-019-00052-0](https://doi.org/10.1007/s41885-019-00052-0)

- Gall, M., Borden, K. A. & Cutter, S. L. (2009). When do losses count? Six fallacies of natural hazards loss data. *Bulletin of the American Meteorological Society*, 90(6), 799-809.

- CRED (various). CRED Crunch series (regular disaster statistics publications): [https://www.emdat.be/publications/](https://www.emdat.be/publications/)

### Wikipedia
- Centre for Research on the Epidemiology of Disasters: [https://en.wikipedia.org/wiki/Centre_for_Research_on_the_Epidemiology_of_Disasters](https://en.wikipedia.org/wiki/Centre_for_Research_on_the_Epidemiology_of_Disasters)
