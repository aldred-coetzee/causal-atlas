# ACLED — Armed Conflict Location & Event Data

> **Last reviewed:** March 2025
> **Status:** Active, weekly updates
> **Website:** https://acleddata.com

---

## 1. Overview

The Armed Conflict Location & Event Data Project (ACLED) is a disaggregated conflict and protest dataset that records individual political violence and demonstration events worldwide. It is widely regarded as the highest-quality and most widely used near-real-time source of sub-national conflict event data.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Founded | 2005, by Prof. Clionadh Raleigh (University of Sussex, now University of Edinburgh) |
| Organisation | Registered 501(c)(3) non-profit in the United States |
| Headquarters | Madison, Wisconsin (legal); distributed global team |
| Tagline | "Clarity in Crisis" |
| Funding | United Nations Complex Risk Analytics Fund (CRAF'd), various government and foundation donors |
| Total events | Over 1.4 million recorded events (as of early 2025) |
| Countries | 250+ countries and territories |
| Update cadence | Weekly (typically Friday releases) |

ACLED was originally focused on African conflict events. It has progressively expanded to achieve global coverage. The dataset is a "living dataset" — all figures are subject to revision as new information emerges. Events are coded by trained regional researchers who review local, national, and international media sources, NGO reports, and other documentation.

### Coverage expansion timeline

| Year | Milestone |
|------|-----------|
| 2005 | Project founded; initial coverage of African conflict |
| 2010 | Comprehensive Africa coverage established (back-coded to 1997) |
| 2016 | South Asia and Southeast Asia added |
| 2018 | Middle East coverage added |
| 2019 | Global expansion: Europe, Central Asia, Latin America, East Asia, Oceania |
| 2020 | United States coverage added; "conflict categories" system introduced |
| 2021–present | Continuous refinement, methodology updates, automated tagging systems |

---

## 2. Coverage

### Spatial extent

ACLED now covers **all countries and territories globally**, organised into six macro-regions:

- **Africa** (data from 1997)
- **Asia-Pacific** (data from 2010 for South/Southeast Asia; 2018+ for others)
- **Europe and Central Asia** (data from 2018)
- **Latin America and the Caribbean** (data from 2018)
- **Middle East** (data from 2017)
- **United States and Canada** (data from 2020)

Coverage start dates vary by country. African countries generally have the deepest historical coverage (back to 1997). Newer regions may only go back to 2018 or 2019. Check ACLED's coverage documentation for exact country-level start dates.

### Temporal range

- **Earliest data:** 1 January 1997 (select African countries)
- **Latest data:** Updated weekly, typically within 1–2 weeks of real-world events
- **Resolution:** Daily (individual event dates)

### Update frequency

- **Weekly releases** every Friday
- Data undergoes a review cycle: events are coded, reviewed by senior researchers, quality-checked, and then published
- Back-coding and corrections are applied retroactively as new information surfaces

---

## 3. Access

### Registration requirement

All data access requires a free **myACLED account**:
1. Register at https://acleddata.com (email + password)
2. Receive an **API key** associated with your registered email
3. Use email + API key for all API requests

### Access methods

| Method | Description |
|--------|-------------|
| **Data Export Tool** | Web-based UI with filters for region, country, date, event type. Exports CSV/Excel. |
| **Bulk download files** | Pre-packaged regional data files (requires login) |
| **REST API** | Programmatic access with query parameters |
| **ACLED Explorer** | Interactive dashboard for last-year data with country profiles |
| **CAST** | Conflict Alert System — forecasts, not raw data |

### API details

**Base URL (legacy):**
```
https://api.acleddata.com/acled/read
```

**Authentication:** Query parameters (not headers):
- `key` — your API key
- `email` — your registered email

**Note on API versioning:** ACLED migrated to an OAuth-based authentication system in 2024–2025. The legacy endpoint above may be deprecated or require updated authentication. Check https://acleddata.com/acled-api-documentation/ for current endpoints.

**Example API call (legacy format):**
```
https://api.acleddata.com/acled/read?key=YOUR_KEY&email=YOUR_EMAIL&country=Somalia&year=2023&limit=100
```

**Key query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | string | API key (required) |
| `email` | string | Registered email (required) |
| `terms` | string | Set to `accept` to accept terms |
| `country` | string | Country name filter |
| `iso` | integer | ISO 3166-1 numeric country code |
| `region` | integer | ACLED region code (1–20) |
| `year` | integer | Year filter |
| `event_date` | string | Date filter (YYYY-MM-DD), supports pipe `\|` for ranges |
| `event_date_where` | string | Operator: `=`, `>`, `<`, `>=`, `<=`, `BETWEEN` |
| `event_type` | string | Event type filter |
| `sub_event_type` | string | Sub-event type filter |
| `actor1` | string | Primary actor name (supports `LIKE`) |
| `interaction` | integer | Interaction code filter |
| `latitude` | float | Latitude filter |
| `longitude` | float | Longitude filter |
| `fatalities` | integer | Fatality count filter |
| `fatalities_where` | string | Operator for fatalities |
| `limit` | integer | Max records to return (default varies) |
| `page` | integer | Pagination page number |
| `fields` | string | Pipe-separated list of fields to return |
| `export_type` | string | `json` (default), `csv`, `xml`, `xlsx`, `txt` |

**Response format (JSON):**
```json
{
  "status": 200,
  "success": true,
  "count": 100,
  "data": [
    {
      "event_id_cnty": "SOM12345",
      "event_date": "2023-06-15",
      "year": "2023",
      "time_precision": "1",
      "disorder_type": "Political violence",
      "event_type": "Battles",
      "sub_event_type": "Armed clash",
      "actor1": "Military Forces of Somalia (2012-)",
      "assoc_actor_1": "",
      "inter1": "1",
      "actor2": "Al Shabaab",
      "assoc_actor_2": "",
      "inter2": "2",
      "interaction": "12",
      "civilian_targeting": "",
      "iso": "706",
      "region": "Eastern Africa",
      "country": "Somalia",
      "admin1": "Hiiraan",
      "admin2": "Belet Weyne",
      "admin3": "",
      "location": "Belet Weyne",
      "latitude": "4.7356",
      "longitude": "45.2037",
      "geo_precision": "1",
      "source": "Garowe Online; Halgan Media",
      "source_scale": "Subnational",
      "notes": "On 15 June 2023, Somali military forces clashed with...",
      "fatalities": "5",
      "tags": "",
      "timestamp": "1687392000"
    }
  ]
}
```

### Rate limits

ACLED does not publicly document specific rate limits. In practice:
- Free academic/research accounts are subject to unspecified throttling
- Excessive automated scraping is explicitly prohibited by the EULA
- The unofficial `acled` Python package defaults to: 3 retries, 0.5s backoff factor, 30s request timeout
- For large-scale data needs, bulk file downloads are recommended over repeated API calls

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/acled/read` | Main event data |
| `/acled/read` (with deleted filter) | Deleted/removed events |
| CAST endpoint | Conflict forecasts (separate from event data) |
| Actor endpoint | Actor metadata |
| Country endpoint | Country reference data |
| Region endpoint | Region reference data |

---

## 4. Schema

### Complete field listing

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `event_id_cnty` | string | Unique alphanumeric event identifier (e.g., `ETH9766`) |
| `event_date` | date (YYYY-MM-DD) | Date the event occurred |
| `year` | integer | Year of the event |
| `time_precision` | integer (1–3) | Temporal precision: 1=exact date, 2=approximate (within a week), 3=estimated (within a month) |
| `disorder_type` | string | Broad category: `Political violence`, `Demonstrations`, `Strategic developments` |
| `event_type` | string | Main event classification (6 types — see below) |
| `sub_event_type` | string | Specific event sub-classification (25 types — see below) |
| `actor1` | string | Name of the primary actor involved |
| `assoc_actor_1` | string | Associated/allied actors to actor1 (semicolon-separated) |
| `inter1` | integer (1–8) | Actor type code for actor1 |
| `actor2` | string | Name of the secondary actor (if any) |
| `assoc_actor_2` | string | Associated/allied actors to actor2 |
| `inter2` | integer (1–8) | Actor type code for actor2 |
| `interaction` | integer | Two-digit code combining actor types (see interaction table) |
| `civilian_targeting` | string | `"Civilians targeted"` or empty |
| `iso` | integer | ISO 3166-1 numeric country code |
| `region` | string | ACLED macro-region name (e.g., "Eastern Africa") |
| `country` | string | Country or territory name |
| `admin1` | string | First-level administrative division |
| `admin2` | string | Second-level administrative division |
| `admin3` | string | Third-level administrative division |
| `location` | string | Named place or neighbourhood |
| `latitude` | float | Latitude in decimal degrees (WGS84 / EPSG:4326, 4 decimal places) |
| `longitude` | float | Longitude in decimal degrees (WGS84 / EPSG:4326, 4 decimal places) |
| `geo_precision` | integer (1–3) | Spatial precision: 1=exact location, 2=nearest named place, 3=admin region centroid |
| `source` | string | Source name(s), semicolon-separated |
| `source_scale` | string | Geographic scope of source: `Local`, `Subnational`, `National`, `Regional`, `International` |
| `notes` | string | Free-text narrative description of the event |
| `fatalities` | integer | Reported number of fatalities (conservative estimate; 0 if unknown) |
| `tags` | string | Semicolon-separated structured metadata labels |
| `timestamp` | integer | Unix timestamp of when the record was uploaded/updated |

### Event types and sub-event types

#### Battles (Disorder type: Political violence)
- **Government regains territory** — state forces recapture territory from non-state actors
- **Non-state actor overtakes territory** — rebels/militia seize territory
- **Armed clash** — confrontation between armed groups without clear territorial change

#### Explosions/Remote violence (Disorder type: Political violence)
- **Chemical weapon**
- **Air/drone strike**
- **Suicide bomb**
- **Shelling/artillery/missile attack**
- **Remote explosive/landmine/IED**
- **Grenade**

#### Violence against civilians (Disorder type: Political violence)
- **Sexual violence**
- **Attack**
- **Abduction/forced disappearance**

#### Protests (Disorder type: Demonstrations)
- **Excessive force against protesters**
- **Protest with intervention**
- **Peaceful protest**

#### Riots (Disorder type: Demonstrations)
- **Violent demonstration**
- **Mob violence**

#### Strategic developments (Disorder type: Strategic developments)
- **Agreement**
- **Arrests**
- **Change to group/activity**
- **Disrupted weapons use**
- **Headquarters or base established**
- **Looting/property destruction**
- **Non-violent transfer of territory**
- **Other**

### Actor type codes (inter1 / inter2)

| Code | Actor Type | Definition |
|------|-----------|------------|
| 1 | State forces | Military, police, government-armed actors |
| 2 | Rebel groups | Organisations seeking national regime change via violence |
| 3 | Political militia | Armed groups aligned with political elites; indirect state links |
| 4 | Identity militia | Communal, ethnic, religious, or clan-based armed groups |
| 5 | Rioters | Unorganised mobs engaging in spontaneous violence |
| 6 | Protesters | Peaceful demonstrators (3+ persons) |
| 7 | Civilians | Unarmed non-combatants |
| 8 | External/Other forces | International organisations, private security, foreign militaries |

### Interaction codes

The `interaction` field is a two-digit code representing the combination of actor types involved, standardised so the lower-numbered actor type comes first:

| Code | Interaction |
|------|------------|
| 10 | State forces only |
| 11 | State forces vs. State forces |
| 12 | State forces vs. Rebel group |
| 13 | State forces vs. Political militia |
| 14 | State forces vs. Identity militia |
| 15 | State forces vs. Rioters |
| 16 | State forces vs. Protesters |
| 17 | State forces vs. Civilians |
| 18 | State forces vs. External/Other forces |
| 20 | Rebel group only |
| 22 | Rebel group vs. Rebel group |
| 23 | Rebel group vs. Political militia |
| 24 | Rebel group vs. Identity militia |
| 25 | Rebel group vs. Rioters |
| 26 | Rebel group vs. Protesters |
| 27 | Rebel group vs. Civilians |
| 28 | Rebel group vs. External/Other forces |
| 30 | Political militia only |
| 33 | Political militia vs. Political militia |
| 34 | Political militia vs. Identity militia |
| 35 | Political militia vs. Rioters |
| 36 | Political militia vs. Protesters |
| 37 | Political militia vs. Civilians |
| 38 | Political militia vs. External/Other forces |
| 40 | Identity militia only |
| 44 | Identity militia vs. Identity militia |
| 45 | Identity militia vs. Rioters |
| 46 | Identity militia vs. Protesters |
| 47 | Identity militia vs. Civilians |
| 48 | Identity militia vs. External/Other forces |
| 50 | Rioters only |
| 55 | Rioters vs. Rioters |
| 56 | Rioters vs. Protesters |
| 57 | Rioters vs. Civilians |
| 58 | Rioters vs. External/Other forces |
| 60 | Protesters only |
| 66 | Protesters vs. Protesters |
| 67 | Protesters vs. Civilians |
| 68 | Protesters vs. External/Other forces |
| 78 | External/Other forces vs. Civilians |
| 80 | External/Other forces only |

### Precision codes

**Temporal precision (`time_precision`):**
| Value | Meaning |
|-------|---------|
| 1 | Exact date known |
| 2 | Date accurate within approximately one week |
| 3 | Date estimated to within a month |

**Geographic precision (`geo_precision`):**
| Value | Meaning |
|-------|---------|
| 1 | Exact location identified (named settlement, specific site) |
| 2 | Nearest named location used as proxy |
| 3 | Centroid of the smallest known administrative unit used |

---

## 5. Spatial Detail

### Location encoding

ACLED encodes location as **point coordinates** (latitude/longitude in WGS84 / EPSG:4326), not as polygons or grid cells. Each event has:

- **`latitude` / `longitude`** — decimal degrees to 4 decimal places (~11m precision at equator)
- **`location`** — named place (city, town, village, neighbourhood)
- **`admin1` / `admin2` / `admin3`** — hierarchical administrative divisions
- **`country`** and **`iso`** — country-level identifiers
- **`geo_precision`** — precision indicator (1–3) signalling how reliable the coordinates are

### Implications for grid-based analysis

Since ACLED provides point data, mapping to a grid (such as PRIO-GRID 0.5° × 0.5° cells) is straightforward via spatial join:

```python
# Assign ACLED events to PRIO-GRID cells
import math

def point_to_prio_grid(lat, lon):
    """Convert lat/lon to PRIO-GRID cell ID (0.5° resolution)."""
    row = int((lat + 90) / 0.5)
    col = int((lon + 180) / 0.5)
    return row * 720 + col  # 720 columns at 0.5° resolution
```

**Caveats:**
- Events with `geo_precision=3` are placed at administrative unit centroids, which may cluster events artificially at those points
- For any aggregation to grid cells, it is critical to distinguish precision levels and potentially weight or flag low-precision events
- Urban areas will have higher precision (1) while rural/remote events often have lower precision (2–3)

### Admin boundary alignment

ACLED uses **GADM** (Global Administrative Areas Database) as its reference for administrative boundaries. The `admin1`, `admin2`, and `admin3` fields correspond to GADM levels, facilitating joins with other datasets that use GADM coding.

---

## 6. Temporal Detail

### Timestamp resolution

- **Primary resolution:** Daily (YYYY-MM-DD format in `event_date`)
- Each event is associated with a single date
- Multi-day events are typically coded on the start date or the date of the most significant activity
- The `year` field is extracted separately for convenience

### Temporal precision

The `time_precision` field explicitly flags date reliability:
- **1:** Exact date — the event is known to have occurred on this specific day
- **2:** Approximate — the date is accurate to within about one week
- **3:** Estimated — the event occurred sometime within the coded month

### Update cycle

- **Weekly releases** (Fridays)
- New events are coded by regional research teams during the week
- Senior researchers review and quality-check coded events
- Events may be revised retroactively when new information becomes available
- The `timestamp` field records when a record was last uploaded or modified

### Implications for time-series analysis

- For monthly aggregation (Causal Atlas primary temporal unit), ACLED is well-suited: sum events per cell per month
- The weekly update cadence means near-real-time analysis is feasible at ~1-week latency
- Back-corrections mean that any cached data should be periodically refreshed
- Low temporal-precision events (`time_precision=3`) should be handled carefully in daily analyses; they are more reliable at monthly resolution

---

## 7. Quality

### Strengths

- **No fatality threshold:** Unlike UCDP-GED which requires at least 1 battle death, ACLED records events with zero fatalities (protests, strategic developments, etc.), providing broader coverage of political instability
- **Conservative fatality estimates:** When conflicting reports exist, ACLED uses the lowest credible figure
- **Hierarchical event merging:** Multiple violence types occurring simultaneously are merged into a single event to avoid double-counting
- **Dedicated civilian targeting field:** Distinguishes intentional targeting from incidental harm
- **Living dataset:** Retroactive corrections as new information emerges
- **Transparent methodology:** Codebook, methodology papers, and researcher guides publicly available

### Known biases and limitations

**Media bias / reporting bias:**
- Events in areas with limited media coverage (remote rural areas, conflict zones where journalists cannot operate) are likely under-reported
- Countries with press freedom restrictions may have systematically lower event counts
- Urban events receive better coverage and higher geo-precision than rural events
- English-language media bias may affect coding in non-English-speaking regions, though ACLED employs multilingual researchers

**Fatality estimation challenges:**
- Fatality figures are among the least reliable fields — parties to conflicts routinely exaggerate or minimise casualty numbers
- Conservative estimation means ACLED fatality counts are likely lower bounds
- When no fatality information is available, events are coded with `fatalities=0`, which is indistinguishable from confirmed zero-fatality events

**Temporal consistency:**
- Coverage start dates differ by region (1997 for Africa, 2018+ for most others), creating temporal asymmetry
- Coding methodologies have evolved over time — events coded in 2005 may not be directly comparable to those coded in 2023
- The introduction of "conflict categories" in 2020 and new sub-event types over time can create discontinuities in time series

**Spatial precision variation:**
- `geo_precision=3` events (admin centroid) can create artificial spatial clustering
- The proportion of low-precision events varies by country and time period
- Coordinate precision (4 decimal places) implies false precision — the actual accuracy depends on the `geo_precision` code

**Comparison with UCDP-GED:**
- ACLED and UCDP-GED are the two major disaggregated conflict event datasets
- ACLED records more events because it has no fatality minimum and includes protests and strategic developments
- UCDP-GED focuses exclusively on organised violence with at least 1 death
- Academic comparisons show significant divergences in event counts and fatality estimates for the same conflicts
- Raleigh, Kishi, and Linke (2023) argue that "political instability patterns are obscured by conflict dataset scope conditions" — the choice of dataset materially affects analytical conclusions
- Reference: Raleigh, C., Kishi, R., & Linke, A. (2023). "Political instability patterns are obscured by conflict dataset scope conditions." *Humanities and Social Sciences Communications*, 10, 74.

**Other validation literature:**
- Eck, K. (2012). "In data we trust? A comparison of UCDP GED and ACLED conflict events datasets." *Cooperation and Conflict*, 47(1), 124–141. — Early systematic comparison finding significant discrepancies between the two datasets
- Donnay, K. et al. (2019). "Integrating conflict event data." *Journal of Conflict Resolution*, 63(5), 1337–1364. — Proposes methods for reconciling different conflict event datasets
- Hammond, J. & Weidmann, N.B. (2014). "Using machine-coded event data for the micro-level study of political violence." *Research & Politics*, 1(2). — Comparison of hand-coded (ACLED) vs. machine-coded (GDELT) data quality

---

## 8. Licence

### End User License Agreement (EULA)

ACLED's EULA (as of 2024/2025) is **restrictive** compared to fully open datasets:

| Aspect | Terms |
|--------|-------|
| **Licence type** | Royalty-free, non-exclusive, non-transferable, non-sublicensable |
| **Non-commercial use** | Permitted for academic research and non-commercial purposes |
| **Commercial use** | **Requires a separate corporate licence** — commercial entities must contact ACLED before accessing data |
| **Redistribution** | Prohibited in raw form. Only "transformative" derivative works may be published, and they must not allow reverse-engineering of the underlying dataset |
| **Scraping** | Explicitly prohibited |
| **Credential sharing** | Prohibited |
| **AI/ML training** | **Explicitly prohibited** (Section 7): ACLED content cannot be used to train, test, or develop ML models, LLMs, or AI systems that function as ACLED substitutes, allow third-party access, or exceed licensing scope |
| **Competitor use** | Content cannot be provided to ACLED's competitors under any circumstances |
| **Termination** | Access suspended for material breach; auto-terminates after 3 months of inactivity or uncured breach within 5 days of notice |
| **Warranty** | Provided "AS IS" with no warranties on accuracy or availability |
| **Governing law** | Wisconsin state law; Madison, Wisconsin courts |

### Attribution requirements

All external use requires strict attribution per ACLED's Attribution Policy:

**Standard citation format:**
> ACLED (Armed Conflict Location & Event Data). [Year]. [Data description/filters]. Accessed [date]. www.acleddata.com.

**Academic papers must also cite:**
> Raleigh, C., Kishi, R., & Linke, A. (2023). "Political instability patterns are obscured by conflict dataset scope conditions." *Humanities and Social Sciences Communications*, 10, 74.

And reference the **ACLED Codebook** with its publication date (most recent: 3 October 2024).

**Additional rules:**
- Data visualisations must include attribution directly on the visual
- Shared data files must include a source column: `"ACLED, accessed on [date]. www.acleddata.com"`
- ACLED logo use is reserved exclusively for official ACLED or joint products
- Social media posts with ACLED visuals must tag ACLED's official accounts

### Implications for Causal Atlas

The ACLED EULA creates significant constraints for an open-source project:
- **Raw data cannot be redistributed** — Causal Atlas cannot bundle or serve ACLED data directly
- **AI/ML restrictions** — Using ACLED data to train models that compete with ACLED's own products is prohibited
- **Transformative use is permitted** — Aggregated statistics (e.g., event counts per grid cell per month) likely qualify as transformative, but legal review is advisable
- **Attribution is mandatory** — Must be prominently displayed in any output
- Users would need their own ACLED accounts to pull fresh data through Causal Atlas

---

## 9. Interoperability

### Shared identifiers with other datasets

| Dataset | Shared Identifier | Notes |
|---------|-------------------|-------|
| **PRIO-GRID** | Lat/lon → grid cell | Point-to-grid spatial join; ACLED is one of PRIO-GRID's source datasets |
| **UCDP-GED** | Country (ISO), date, location | No shared event IDs; requires fuzzy matching for event-level linking |
| **GADM** | admin1/admin2/admin3 | ACLED uses GADM administrative boundaries |
| **ISO 3166** | `iso` field (numeric) | Standard country codes enable joining with World Bank, FAO, WHO, etc. |
| **GDELT** | No direct identifiers | Different coding methodologies; geographic/temporal overlap |
| **HDX HAPI** | Country (ISO), admin levels | HDX HAPI uses p-codes which differ from GADM; requires boundary crosswalk |

### Grid compatibility (PRIO-GRID)

ACLED point events can be mapped to PRIO-GRID 0.5° × 0.5° cells using a simple spatial join. PRIO-GRID v3 already incorporates ACLED data as one of its conflict layers, validating this approach.

**Aggregation strategy for Causal Atlas:**
1. Assign each ACLED event to a PRIO-GRID cell based on lat/lon
2. Aggregate to monthly counts per cell (matching our temporal unit)
3. Create separate count variables for: total events, battles, protests, riots, violence against civilians, fatalities
4. Flag the proportion of low-precision events (geo_precision ≥ 2) per cell-month
5. Consider weighting or excluding geo_precision=3 events in analyses sensitive to spatial accuracy

---

## 10. Python Access

### Official tools

ACLED does not provide an official Python library. Data access is through their REST API or web export tool.

### Unofficial libraries

#### `acled` (PyPI)

The most feature-complete unofficial wrapper as of March 2025.

```bash
pip install acled
```

| Attribute | Detail |
|-----------|--------|
| Package | `acled` |
| Version | 0.2.4 (July 2025) |
| Author | Blaze Burgess |
| Licence | GPLv3 |
| Status | Beta |
| Python | >=3.8 |
| Repository | https://github.com/blazeiburgess/acled |

**Authentication setup:**
```bash
# Option 1: Environment variables
export ACLED_API_KEY="your_key_here"
export ACLED_EMAIL="your_email_here"

# Option 2: CLI login
acled auth login
```

**Basic usage:**
```python
from acled import AcledClient

client = AcledClient()  # uses env vars
# Or: client = AcledClient(api_key="...", email="...")

# Fetch events for a specific country and year
events = client.get_data(country='Somalia', year=2023, limit=100)

for event in events:
    print(event['event_id_cnty'], event['event_date'], event['event_type'])

# Date range filtering (pipe-separated start|end)
events = client.get_data(
    country='Yemen',
    event_date='2023-01-01|2023-06-30',
    event_type='Battles',
    limit=500
)

# Advanced filtering with operators
events = client.get_data(
    country='Nigeria',
    fatalities=5,
    fatalities_where='>',
    limit=100
)

# Other endpoints
actors = client.get_actor_data(limit=10)
countries = client.get_country_data(limit=10)
regions = client.get_region_data(limit=10)
actor_types = client.get_actor_type_data(limit=10)
```

**Data models provided:**
- `AcledEvent` — main event fields
- `Actor` — actor_name, first_event_date, last_event_date, event_count
- `Country` — country, iso, iso3, event_count
- `Region` — region, region_name, event_count
- `ActorType` — actor_type_id, actor_type_name, event_count

**Enums available:**
- `TimePrecision`: EXACT_DATE (1), APPROXIMATE_DATE (2), ESTIMATED_DATE (3)
- `DisorderType`: POLITICAL_VIOLENCE, DEMONSTRATIONS, STRATEGIC_DEVELOPMENTS
- `ExportType`: JSON, XML, CSV, XLSX, TXT
- `Regions`: WESTERN_AFRICA (1) through ANTARCTICA (20)

**Configuration:**
- `ACLED_MAX_RETRIES`: Default 3
- `ACLED_RETRY_BACKOFF_FACTOR`: Default 0.5
- `ACLED_REQUEST_TIMEOUT`: Default 30 seconds

**CLI:**
```bash
acled data --country Syria --year 2024 --limit 10
acled data --country Nigeria --format table
acled data --output events.json
```

### Direct API access with requests

For maximum control or if the unofficial library breaks:

```python
import requests
import pandas as pd

API_BASE = "https://api.acleddata.com/acled/read"

params = {
    "key": "YOUR_API_KEY",
    "email": "YOUR_EMAIL",
    "terms": "accept",
    "country": "Ethiopia",
    "year": 2023,
    "event_type": "Battles",
    "limit": 500,
    "page": 1
}

response = requests.get(API_BASE, params=params, timeout=30)
data = response.json()

if data.get("success"):
    df = pd.DataFrame(data["data"])
    print(f"Retrieved {len(df)} events of {data['count']} total")

    # Convert types
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["fatalities"] = df["fatalities"].astype(int)
    df["event_date"] = pd.to_datetime(df["event_date"])

    print(df[["event_date", "event_type", "location", "fatalities"]].head())
```

### Pagination for bulk download

```python
def fetch_all_acled(country, year, api_key, email):
    """Fetch all events for a country-year, handling pagination."""
    all_events = []
    page = 1
    page_size = 5000

    while True:
        params = {
            "key": api_key,
            "email": email,
            "terms": "accept",
            "country": country,
            "year": year,
            "limit": page_size,
            "page": page
        }

        resp = requests.get(API_BASE, params=params, timeout=60)
        data = resp.json()

        if not data.get("success") or not data.get("data"):
            break

        all_events.extend(data["data"])

        if len(data["data"]) < page_size:
            break  # last page

        page += 1

    return pd.DataFrame(all_events)
```

### PRIO-GRID assignment example

```python
import numpy as np

def assign_prio_grid(df):
    """Add PRIO-GRID cell ID to ACLED DataFrame."""
    df = df.copy()
    df["lat"] = df["latitude"].astype(float)
    df["lon"] = df["longitude"].astype(float)

    # PRIO-GRID uses 0.5° cells from -90 to 90 lat, -180 to 180 lon
    df["grid_row"] = ((df["lat"] + 90) / 0.5).astype(int)
    df["grid_col"] = ((df["lon"] + 180) / 0.5).astype(int)
    df["prio_grid_id"] = df["grid_row"] * 720 + df["grid_col"]

    return df


def monthly_grid_aggregation(df):
    """Aggregate ACLED events to monthly grid-cell counts."""
    df = df.copy()
    df["event_date"] = pd.to_datetime(df["event_date"])
    df["year_month"] = df["event_date"].dt.to_period("M")
    df["fatalities"] = df["fatalities"].astype(int)

    agg = df.groupby(["prio_grid_id", "year_month"]).agg(
        total_events=("event_id_cnty", "count"),
        total_fatalities=("fatalities", "sum"),
        battles=("event_type", lambda x: (x == "Battles").sum()),
        protests=("event_type", lambda x: (x == "Protests").sum()),
        riots=("event_type", lambda x: (x == "Riots").sum()),
        violence_against_civilians=("event_type", lambda x: (x == "Violence against civilians").sum()),
        explosions=("event_type", lambda x: (x == "Explosions/Remote violence").sum()),
        low_precision_pct=("geo_precision", lambda x: (x.astype(int) >= 2).mean()),
    ).reset_index()

    return agg
```

---

## 11. Relevance to Causal Atlas

### Domains served

ACLED is the **primary conflict and political instability data source** for Causal Atlas. It covers:
- Armed conflict (battles, remote violence)
- Political violence against civilians
- Protest and demonstration activity
- Strategic military/political developments

### Causal chains ACLED can illuminate

ACLED data, combined with other Causal Atlas sources, can test hypotheses about:

| Causal Chain | Other Data Needed | Expected Lag |
|-------------|-------------------|--------------|
| **Drought → conflict** | CHIRPS rainfall, NDVI vegetation | 3–12 months |
| **Food price spikes → protests/riots** | WFP food prices, FAO data | 1–3 months |
| **Conflict → displacement/migration** | UNHCR, IOM DTM, HDX HAPI | 0–6 months |
| **Conflict → food insecurity** | IPC/CH classifications, WFP | 1–6 months |
| **Elections → political violence** | Election calendars | -3 to +3 months |
| **Natural disasters → conflict** | EM-DAT, USGS earthquakes | 1–12 months |
| **Economic shocks → unrest** | World Bank, nightlights | 3–12 months |
| **Conflict → health outcomes** | WHO, disease outbreaks | 1–12 months |
| **Air pollution → protests** | OpenAQ | 1–6 months |
| **Conflict spillover (spatial)** | ACLED itself (neighbouring cells) | 1–3 months |

### Integration priority

**HIGH** — ACLED should be one of the first datasets integrated into Causal Atlas. It provides the dependent variable (conflict/instability events) for many of the cross-domain causal chains we want to investigate, and the response variable for others (conflict as a cause of displacement, health impacts, etc.).

### Integration approach

1. **Ingestion:** Pull via API or bulk download, store as Parquet
2. **Gridding:** Assign to PRIO-GRID cells via lat/lon spatial join
3. **Aggregation:** Monthly event counts and fatality sums per grid cell, broken down by event type
4. **Quality flags:** Track geo_precision and time_precision distributions per cell-month
5. **Refresh:** Weekly incremental updates via API, with periodic full refresh to capture back-corrections
6. **Licence compliance:** Do not redistribute raw ACLED data; only serve aggregated/transformed derivatives; require users to accept attribution terms

---

## 12. Sources

### Official ACLED resources

- **Website:** https://acleddata.com
- **Codebook (2024):** https://acleddata.com/knowledge-base/codebook/
- **API documentation hub:** https://acleddata.com/acled-api-documentation/
- **Knowledge Base:** https://acleddata.com/knowledge-base/
- **EULA:** https://acleddata.com/eula/
- **Attribution Policy:** https://acleddata.com/attributionpolicy/
- **Data Export Tool:** https://acleddata.com/data-export-tool/
- **Curated data files:** https://acleddata.com/curated-data-files/

### Academic references

- Raleigh, C., Linke, A., Hegre, H., & Karlsen, J. (2010). "Introducing ACLED: An Armed Conflict Location and Event Dataset." *Journal of Peace Research*, 47(5), 651–660. https://doi.org/10.1177/0022343310378914 — **The founding paper**
- Raleigh, C., Kishi, R., & Linke, A. (2023). "Political instability patterns are obscured by conflict dataset scope conditions." *Humanities and Social Sciences Communications*, 10, 74. — **ACLED's recommended citation**
- Eck, K. (2012). "In data we trust? A comparison of UCDP GED and ACLED conflict events datasets." *Cooperation and Conflict*, 47(1), 124–141. — **Systematic comparison of ACLED vs. UCDP**
- Donnay, K., Dunford, E.T., McGrath, E.C., Backer, D., & Cunningham, D.E. (2019). "Integrating conflict event data." *Journal of Conflict Resolution*, 63(5), 1337–1364. — **Methods for reconciling conflict datasets**
- Hammond, J. & Weidmann, N.B. (2014). "Using machine-coded event data for the micro-level study of political violence." *Research & Politics*, 1(2). — **Hand-coded vs. machine-coded quality comparison**

### Python tools

- `acled` PyPI package: https://pypi.org/project/acled/ (unofficial, v0.2.4)
- GitHub: https://github.com/blazeiburgess/acled
- ACLED data pipeline example: https://github.com/19Vermouth/ACLED-data-pipeline

### Related Causal Atlas research files

- `research/datasets/ucdp-ged.md` — Complementary conflict dataset
- `research/datasets/prio-grid.md` — Spatial backbone framework
- `research/datasets/hdx-hapi.md` — Humanitarian data API
- `research/03-causal-chains.md` — Cross-domain causality literature
- `research/04-statistical-methods.md` — Analytical methods
