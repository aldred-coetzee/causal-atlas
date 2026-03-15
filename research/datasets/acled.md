# ACLED — Armed Conflict Location & Event Data

> **Last reviewed:** March 2026 (significantly expanded)
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

## 12. ACLED API (Current Architecture — Post-Migration)

> **Last verified:** March 2026. ACLED migrated away from the legacy `api.acleddata.com/acled/read` endpoint. The current API is hosted at `acleddata.com/api/`.

### Base URL

```
https://acleddata.com/api/acled/read
```

Response format is controlled by `_format` query parameter: `csv`, `json`, `xml`, or `txt`. JSON is the default.

### Authentication

ACLED now uses **OAuth 2.0 password-grant flow** (replacing the legacy email + key query parameter approach):

**Step 1 — Obtain an access token:**
```bash
curl -X POST https://acleddata.com/oauth/token \
  -d "grant_type=password" \
  -d "client_id=acled" \
  -d "username=YOUR_EMAIL" \
  -d "password=YOUR_PASSWORD"
```

**Response:**
```json
{
  "token_type": "Bearer",
  "expires_in": 86400,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
  "refresh_token": "def50200a1b2c3d4..."
}
```

- **Access token validity:** 24 hours
- **Refresh token validity:** 14 days
- Refresh via POST to the same endpoint with `grant_type=refresh_token` and the refresh token

**Step 2 — Use the token in requests:**
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  "https://acleddata.com/api/acled/read?_format=json&country=Somalia&year=2024&limit=100"
```

**Alternative: Cookie-based authentication** — For browser or Postman-based access, POST credentials to `https://acleddata.com/user/login?_format=json` to get a session cookie and CSRF token.

### Available Endpoints

| Endpoint Path | Purpose |
|---------------|---------|
| `/api/acled/read` | Core event data (political violence, demonstrations, strategic developments) |
| `/api/acled/deleted/read` | Deleted/removed events |
| `/api/cast/read` | CAST conflict forecasts (monthly predictions, up to 6 months ahead) |

### Query Filters (Complete List)

| Filter | Type | Default Operator | Description |
|--------|------|-----------------|-------------|
| `event_id_cnty` | string | LIKE | Event ID (e.g., `SOM12345`) |
| `event_date` | date | = | YYYY-MM-DD; supports `_where=BETWEEN` with pipe-separated range |
| `year` | integer | = | Year filter; supports `_where=>` etc. |
| `time_precision` | integer | = | 1=exact, 2=~week, 3=~month |
| `disorder_type` | string | LIKE | `Political violence`, `Demonstrations`, `Strategic developments` |
| `event_type` | string | LIKE | Main event classification |
| `sub_event_type` | string | LIKE | Sub-classification |
| `actor1` / `actor2` | string | LIKE | Actor name |
| `assoc_actor_1` / `assoc_actor_2` | string | LIKE | Associated actors |
| `inter1` / `inter2` | integer | = | Actor type codes |
| `interaction` | integer | = | Two-digit interaction code |
| `civilian_targeting` | string | LIKE | `"Civilian targeting"` or empty |
| `iso` | integer | = | ISO 3166-1 numeric country code |
| `region` | integer | = | ACLED region code (1–20) |
| `country` | string | = | Country name |
| `admin1` / `admin2` / `admin3` | string | LIKE | Administrative divisions |
| `location` | string | LIKE | Named place |
| `latitude` / `longitude` | float | = | Coordinates (supports `_where`) |
| `geo_precision` | integer | = | 1–3 |
| `source` / `source_scale` | string | LIKE | Source metadata |
| `notes` / `tags` | string | LIKE | Free text / tags |
| `fatalities` | integer | = | Fatality count (supports `_where=>`) |
| `timestamp` | integer | = | Unix timestamp of last update |

**Filter modifiers:**
- `_where` suffix: `=`, `>`, `<`, `>=`, `<=`, `BETWEEN`, `LIKE`
- Multiple values: pipe (`|`) or `:OR:` syntax — e.g., `country=Argentina|Georgia|Brazil`
- URL-encoded operators: `%3E` for `>`, `%3C` for `<`, etc.

**Additional parameters:**
- `export_type`: `dyadic` (default, one row per event) or `monadic` (one row per actor)
- `population`: `TRUE` for best population estimate, `"full"` for 1km/2km/5km/best estimates
- `fields`: pipe-separated list of fields to return (e.g., `fields=event_date|event_type|fatalities`)
- `limit`: max rows per page (default: **5000**)
- `page`: pagination page number (1-indexed)
- `inter_num`: `1` for numeric actor codes, `0` for text labels (default)

### Pagination Model

The API defaults to returning a maximum of **5,000 rows** per request. To retrieve larger datasets:

```python
import requests

BASE = "https://acleddata.com/api/acled/read"
TOKEN = "your_access_token"
headers = {"Authorization": f"Bearer {TOKEN}"}

page = 1
all_data = []

while True:
    params = {
        "_format": "json",
        "country": "Ethiopia",
        "year": 2024,
        "limit": 5000,
        "page": page
    }
    resp = requests.get(BASE, headers=headers, params=params, timeout=60)
    result = resp.json()

    if not result.get("success") or not result.get("data"):
        break

    all_data.extend(result["data"])

    if len(result["data"]) < 5000:
        break  # last page

    page += 1

print(f"Total events retrieved: {len(all_data)}")
```

**Important:** Pagination calls do **not** count against API rate limits.

### Response Format (JSON Example)

```json
{
  "status": 200,
  "success": true,
  "last_update": 12,
  "count": 2,
  "messages": [],
  "data": [
    {
      "event_id_cnty": "SOM56789",
      "event_date": "2024-03-15",
      "year": "2024",
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
      "notes": "On 15 March 2024, Somali military forces clashed with Al Shabaab militants near Belet Weyne...",
      "fatalities": "3",
      "tags": "",
      "timestamp": "1710720000"
    }
  ],
  "data_query_restrictions": {
    "country": "Somalia"
  }
}
```

### Rate Limits

ACLED does **not** publicly document specific per-minute or per-hour rate limits. In practice:

- The default 5,000-row limit per page acts as a bandwidth constraint
- Pagination calls are explicitly excluded from rate limit counting
- Excessive automated scraping is prohibited by the EULA
- For very large downloads (e.g., full country histories), ACLED recommends using the **bulk download files** rather than repeated API calls
- The unofficial `acled` Python package uses: 3 retries, 0.5s backoff factor, 30s timeout as reasonable defaults
- Token-based auth avoids the overhead of re-authenticating on every request (24h token validity)

### ACLED Access Tool vs API

| Feature | Data Export Tool (Web) | API (Programmatic) |
|---------|----------------------|-------------------|
| **Interface** | Web form with dropdown filters | HTTP GET requests with query parameters |
| **Authentication** | Browser login session | OAuth token or cookie-based |
| **Output formats** | CSV, Excel | JSON (default), CSV, XML, TXT |
| **Row limits** | Determined by export filters | 5,000 per page (paginate for more) |
| **Filtering** | Dropdown menus, date pickers | Query parameters with operators (`_where`) |
| **Best for** | Quick manual downloads, non-technical users | Automated pipelines, reproducible workflows |
| **Pagination** | N/A (single export) | `page` parameter, increment until done |
| **Population data** | Not available | Available via `population=TRUE` parameter |
| **Bulk download files** | Available for download by region/year | Not applicable (use API for filtered queries) |

---

## 13. ACLED Conflict Index

> Source: https://acleddata.com/general-guide/about-conflict-index (verified March 2026)

### What It Measures

The ACLED Conflict Index is a composite measure of conflict intensity for every country and territory in the world. It provides a single score enabling cross-country comparison and temporal tracking of conflict trends.

### The Four Indicators

| Indicator | Question | Measurement |
|-----------|----------|-------------|
| **Deadliness** | How fatal are political violence events? | Total reported fatalities from political violence over 12 months |
| **Danger to Civilians** | How much violence targets civilians? | Count of violent events specifically targeting civilians |
| **Geographic Diffusion** | How widespread is violence? | Proportion of 10km × 10km grid cells in a country experiencing ≥10 political violence events per year |
| **Armed Group Fragmentation** | How many armed groups are active? | Count of distinct rebel groups and political militias operating in the last 12 months (excluding unidentified groups) |

### Calculation Methodology

1. **Compute raw values** for each indicator per country
2. **Scale** — the square root of each indicator value is taken to reduce the dominance of extreme outliers
3. **Weight** — the square root is raised to the power of the indicator's weight. For the weekly index, danger and deadliness carry slightly more weight than diffusion and fragmentation
4. **Sum** — the weighted values are added to form a single composite score
5. **Rank** — countries are ranked by their composite score

The score has a **minimum of 0** and **no theoretical maximum**, since there is no pre-assumed ceiling on conflict intensity.

### Classification Tiers

| Tier | Criteria |
|------|----------|
| **Extreme** | Top 10 countries |
| **High** | Next 20 countries |
| **Turbulent** | Next 20 countries |
| **Low/Inactive** | Remainder |

### Update Cadence

| Version | Frequency | Period Covered |
|---------|-----------|---------------|
| **Annual Conflict Index** | Released in December | Previous December through November |
| **Weekly Conflict Index** | Updated every Wednesday | Rolling window |

### Data Scope

The Index uses only events under the **"Political violence"** disorder type. This excludes protests (unless involving excessive force) and strategic developments. Coverage spans more than 240 countries and territories.

### Relevance for Causal Atlas

The Conflict Index provides a pre-computed severity score per country per time period. This could serve as a higher-level dependent variable or contextual control in cross-domain causal analyses, supplementing raw event counts with a measure of conflict intensity.

---

## 14. Coding Methodology In Detail

### Coder Recruitment and Training

ACLED employs **experienced researchers with knowledge of local contexts and languages**. Coders are typically regional specialists who understand the political landscape, actor networks, and media environment of the countries they cover. Specific formal training protocols are not publicly detailed, but ACLED states that all coders apply guidelines from the Codebook and supplemental documentation.

### Source Materials

ACLED coders work from **structured and regularly reviewed lists of secondary sources**, accessed through a proprietary **sourcing platform** that ensures the same sources are checked every week in a consistent manner. Source types include:

- **National media** — state and private outlets in local languages
- **International wire services** — AFP, AP, Reuters, Xinhua
- **Subnational and ethnic media** — e.g., Kachinland News for Myanmar, Oromiya Media Network for Ethiopia
- **Diaspora media** — for countries with restricted press freedom (e.g., ESAT, Zehabesha for Ethiopia)
- **NGO and human rights reports** — Amnesty International, Human Rights Watch
- **Social media** — used cautiously as supplementary verification
- **Governmental and UN sources** — official statements, OCHA sitreps
- **New media** — journalist accounts, monitoring groups

### The Three-Stage Review Process

ACLED uses a **weekly coding and review cycle** with three hierarchical review stages:

**Stage 1: Intra-Coder Reliability**
- Individual researchers code events for their assigned countries
- They self-review for internal consistency (e.g., same actor coded the same way, same event type applied to similar situations)
- Difficult decisions are flagged and discussed with team members and Research Managers

**Stage 2: Inter-Coder Reliability (Regional)**
- A **Regional Research Manager** reviews all coded data from their region
- Cross-checks coding decisions across different country researchers within the same region
- Ensures consistent application of the methodology (e.g., "armed clash" vs "government regains territory" coded consistently across Nigeria and Niger)

**Stage 3: Global Consistency**
- A **global methodology team** conducts a final review
- Ensures inter-region consistency (e.g., protest coding in Latin America matches protest coding in Africa)
- Validates that the methodology is applied consistently worldwide

### Disagreement Resolution

- Researchers pose questions to team members and Research Managers daily
- Difficult coding decisions are escalated through the regional and global hierarchy
- No formal external arbitration process is documented — resolution is internal and hierarchical
- New methodological insights trigger **systematic quality assurance reviews** of previously coded data

### Automated Data Cleaning

After manual review, data are sent to the **Data Management team** for:
- Automated data cleaning and formatting checks
- Validation of field values against allowed ranges
- Consistency checks (e.g., coordinates match country, actor types match interaction codes)

### Source Transparency

ACLED records sources in the `source` field (semicolon-separated) and tags them by geographic scope in `source_scale`. This enables users to assess the provenance and potential biases of individual event records.

---

## 15. Complete Sub-Event Type Reference

> Based on the ACLED Codebook (October 2024 edition). The dataset records **6 event types** and **25 sub-event types**, classified under **3 disorder types**.

### Disorder Type: Political Violence

#### Event Type: Battles (3 sub-event types)
| Sub-Event Type | Description | Example |
|---------------|-------------|---------|
| **Armed clash** | Confrontation between armed groups without clear territorial outcome | Al Shabaab and Somali military exchange fire near a checkpoint in Hiiraan |
| **Government regains territory** | State forces recapture an area from non-state actors | Nigerian army retakes village from ISWAP fighters in Borno state |
| **Non-state actor overtakes territory** | Rebel group or militia seizes and holds territory | Taliban captures district centre in Helmand province |

#### Event Type: Explosions/Remote violence (6 sub-event types)
| Sub-Event Type | Description | Example |
|---------------|-------------|---------|
| **Air/drone strike** | Aerial bombardment by manned aircraft or unmanned drones | US drone strike targets Al Qaeda leader in Yemen |
| **Suicide bomb** | Self-detonating explosive attack | ISIS suicide bomber detonates at market in Baghdad |
| **Shelling/artillery/missile attack** | Indirect fire using heavy weapons | Russian artillery shells residential area in Kharkiv |
| **Remote explosive/landmine/IED** | Pre-placed explosive device | Roadside IED detonates against military convoy in Mali |
| **Grenade** | Hand-thrown explosive device | Grenade thrown at police station in Burundi |
| **Chemical weapon** | Use of chemical agents | Chlorine gas attack on rebel-held area in Syria |

#### Event Type: Violence against civilians (3 sub-event types)
| Sub-Event Type | Description | Example |
|---------------|-------------|---------|
| **Attack** | Direct physical violence against civilians by an organised group | Militia attacks village, killing 12 civilians in Ituri, DRC |
| **Abduction/forced disappearance** | Kidnapping or enforced disappearance | Boko Haram abducts 43 people from rural community in Adamawa |
| **Sexual violence** | Rape, sexual assault, or other sexual violence as a tactic | Armed group systematically commits sexual violence in South Kivu |

### Disorder Type: Demonstrations

#### Event Type: Protests (3 sub-event types)
| Sub-Event Type | Description | Example |
|---------------|-------------|---------|
| **Peaceful protest** | Non-violent demonstration by 3+ people | Thousands march against corruption in Nairobi |
| **Protest with intervention** | Authorities intervene to disperse but without excessive force | Police use tear gas to disperse anti-government protesters in Beirut |
| **Excessive force against protesters** | State forces use lethal or disproportionate force | Security forces open fire on protesters, killing 5 in Khartoum |

#### Event Type: Riots (2 sub-event types)
| Sub-Event Type | Description | Example |
|---------------|-------------|---------|
| **Violent demonstration** | Protesters engage in violence (arson, vandalism, clashes with police) | Rioters burn government buildings during anti-austerity protests in Santiago |
| **Mob violence** | Spontaneous communal violence by unorganised crowd | Mob attacks suspected thieves in Lagos market |

### Disorder Type: Strategic Developments

#### Event Type: Strategic developments (8 sub-event types)
| Sub-Event Type | Description | Example |
|---------------|-------------|---------|
| **Agreement** | Ceasefire, peace deal, or negotiated settlement | Government and rebel group sign ceasefire in Juba |
| **Arrests** | Detention of political actors, activists, or armed group members | Security forces arrest opposition leader in Minsk |
| **Change to group/activity** | Mergers, splits, name changes, operational shifts by armed groups | AQIM faction splits to form new group in northern Mali |
| **Disrupted weapons use** | Interception or defusing of weapons before use | Security forces defuse IED on highway in Kabul |
| **Headquarters or base established** | Creation of new military or armed group base | Rebel group establishes new camp in Beni territory |
| **Looting/property destruction** | Deliberate destruction or seizure of property | Armed group loots medical facilities in Tigray |
| **Non-violent transfer of territory** | Territory changes hands without combat (withdrawal, handover) | Rebel group withdraws from town under ceasefire terms |
| **Other** | Events not fitting other sub-types | Military announces new deployment to border region |

---

## 16. ACLED-UCDP Crosswalk and Dataset Comparisons

### ACLED vs UCDP-GED: Detailed Comparison

The two most widely used disaggregated conflict event datasets are ACLED and UCDP-GED (Uppsala Conflict Data Program Georeferenced Event Dataset). They have fundamental differences in scope, methodology, and resulting data.

| Dimension | ACLED | UCDP-GED |
|-----------|-------|----------|
| **Fatality threshold** | None — records events with 0 fatalities | Minimum 1 direct battle death required |
| **Event scope** | Political violence, demonstrations, strategic developments | Organised violence only (state-based, non-state, one-sided) |
| **Conflict definition** | Any politically motivated event | Must be part of a conflict with 25+ battle deaths/year (state-based) |
| **Coding method** | Human coders using multiple source types | Human coders primarily using news sources |
| **Typical event counts** | ~500–2,000+ events/week globally | ~15,000–20,000 events/year globally |
| **Temporal coverage** | 1997–present (Africa), 2010–2018+ (others) | 1989–present (global) |
| **Spatial precision** | 4 decimal places with 3-level precision coding | 6 decimal places with 7-level precision coding |
| **Update frequency** | Weekly | Annual (with some delay) |
| **Protests included** | Yes (3 sub-event types) | No |
| **Strategic developments** | Yes (8 sub-event types) | No |
| **Actor taxonomy** | 8 actor types | Organised actors only (state, rebel, communal militia) |
| **Fatality methodology** | Conservative (lowest credible figure) | "Best estimate" with low/high bounds |
| **Licence** | Non-commercial free; commercial requires licence; AI/ML training prohibited | CC-BY 4.0 (fully open) |

### Key Findings from Comparative Studies

**Eck (2012)** — The foundational comparison study:
- Found that ACLED and UCDP-GED agree on the occurrence of large, highly visible events but diverge significantly on smaller events
- Event counts differ substantially: ACLED records many more events because of its broader scope
- Fatality estimates diverge even for the same events — different source triangulation leads to different figures
- Warned that "those interested in subnational analyses of conflict should be wary of ACLED's data because of uneven quality-control issues"

**Raleigh, Kishi & Linke (2023)** — ACLED's own comparison:
- Demonstrated that analytical conclusions about conflict patterns change materially depending on which dataset is used
- Argued that UCDP's fatality threshold obscures patterns of political instability that fall below the 1-death threshold
- Showed that scope conditions (what counts as an "event") drive divergences more than coding errors

**Donnay et al. (2019)** — Integration methodology:
- Proposed methods for reconciling ACLED and UCDP-GED at the event level
- Found that fuzzy matching on date, location, and actors can link ~40–60% of UCDP events to ACLED events
- Remaining divergences stem from genuinely different coding decisions, not just matching failures

### No Formal Crosswalk Exists

There is **no published formal crosswalk table** that maps individual ACLED events to UCDP-GED events. Event-level linking requires fuzzy matching on:
- Date (±3 days to account for temporal precision differences)
- Location (within ~50km to account for different geocoding approaches)
- Actors (string similarity matching)
- Event type (conceptual mapping, not 1:1)

### Multi-Dataset Comparison Table

| Feature | ACLED | UCDP-GED | SCAD | GTD | GDELT |
|---------|-------|----------|------|-----|-------|
| **Type** | Human-coded | Human-coded | Human-coded | Human-coded | Machine-coded |
| **Focus** | Political violence & protests | Organised violence | Social conflict (excl. civil war) | Terrorism | All media-reported events |
| **Temporal range** | 1997–present | 1989–present | 1990–2015 | 1970–2020 | 1979–present |
| **Geographic scope** | Global (since 2022) | Global | Africa, Latin America, Middle East | Global | Global |
| **Fatality threshold** | None | ≥1 battle death | None | None | N/A |
| **Update frequency** | Weekly | Annual | Discontinued | Discontinued (2020) | Every 15 minutes |
| **Typical events/year** | ~100,000+ | ~15,000–20,000 | ~3,000–5,000 | ~8,000–15,000 | Millions |
| **Source methodology** | Multi-source, multilingual | Primarily news media | AP and AFP wire services | Multiple open sources | Automated NLP on news |
| **Status (2026)** | Active | Active | Inactive (last update 2016) | Inactive (ended 2020) | Active |
| **Licence** | Restrictive EULA | CC-BY 4.0 | Open for research | Open for research | Fully open |
| **Primary citation** | Raleigh et al. (2023) | Sundberg & Melander (2013) | Salehyan et al. (2012) | START (2021) | Leetaru & Schrodt (2013) |

**Notes on inactive datasets:**
- **SCAD** (Social Conflict Analysis Database): Created by Cullen Hendrix and Idean Salehyan. Covers Africa (1990–2015), Latin America and select Middle East countries. Uses only AP and AFP wire services. Explicitly excludes events that are part of organized armed conflicts as defined by UCDP. 10% double-coding for reliability. Last updated 2016.
- **GTD** (Global Terrorism Database): Created by START at University of Maryland. 200,000+ incidents 1970–2020 (data from 1993 excluded due to loss). Data collection evolved across multiple organizations (Pinkerton 1970–1997, CETIS 1998–2008, ISVG 2008–2011, START 2012–2020). Uses ML/data mining to identify candidate articles. Ended in 2020.
- **PITF** (Political Instability Task Force): Country-level dataset of instability events (ethnic wars, revolutionary wars, adverse regime changes, genocides). Not event-level disaggregated — operates at country-year level. Maintained by CIA-funded research program since 1994. Data availability is restricted.

---

## 17. Country-Specific Coding Challenges

### Myanmar

Myanmar presents some of the most complex coding challenges in the ACLED dataset due to actor proliferation, geographic ambiguity, and source constraints.

**Actor identification:**
- Dozens of Ethnic Armed Organizations (EAOs) operate simultaneously, many with political and armed wings coded together (e.g., "KIO/KIA" for the Kachin Independence Organisation/Army)
- Splintered factions are distinguished using years (e.g., three distinct DKBA iterations)
- Post-February 2021 coup: massive proliferation of new resistance forces, requiring three new coding categories:
  - **PDF** — People's Defense Force, NUG-directed, coded only when sources explicitly reference NUG command
  - **PDF – [Location]** — Autonomous local defense forces incorporating geography into formal names
  - **Unidentified Anti-Coup Armed Groups** — unnamed or unaffiliated resistance forces
- Alliance coding: the Northern Alliance (NA-B) and Brotherhood Alliance are coded as primary actors only when all members fight jointly

**Geographic coding:**
- Village names vary significantly between Shan and Burmese transliterations (e.g., "Mong" vs "Mine" for the same place)
- Multiple villages share identical names — disambiguation requires cross-referencing with armed group battalion locations and known conflict areas
- Kayin state sources reference traditional Kayin nation boundaries that diverge from Myanmar's official administrative divisions
- ACLED standardises names using English transliteration of Burmese names, consulting MIMU (Myanmar Information Management Unit) boundary data

**Source challenges:**
- Journalists face imprisonment for conflict reporting; two Reuters journalists were detained after reporting the Inn Din mass killing
- Since the coup, the military has directly targeted journalists, forcing outlets underground or into exile
- ACLED prioritises subnational ethnic media (Kachinland News, Shan Herald Agency) over national outlets for battlefield reporting
- Facebook prevalence of disinformation restricts social media utility as a source
- "Peopleless protests" (objects arranged as protest symbols) are excluded from protest coding because ACLED requires 3+ people physically present — coded as "Strategic developments" instead

**Fatality coding:**
- Post-coup fatality increases were validated with external experts rather than automatically discounted
- Unknown fatalities are conservatively coded as 3
- ACLED acknowledges that "fatality numbers are frequently the most biased and poorly reported component of conflict data"

**Rakhine State (2017):**
- Documenting Rohingya mass violence required innovative approaches due to military access restrictions
- Human rights organizations documented abuses through refugee interviews in Bangladesh, but lacked precise time/location detail
- ACLED only coded events with sufficient date, actor, and location specificity, resulting in incomplete documentation despite known large-scale atrocities

### Ethiopia

Ethiopia's primary challenge is its **tightly controlled media environment**.

**Sourcing structure:**
- Approximately **one-third** of Ethiopian events contain information from diaspora media sources
- Diaspora sources (e.g., Oromiya Media Network, ESAT, Zehabesha) provide coverage of events that in-country sources cannot or will not report
- International wire services (AFP, AP, Xinhua) account for ~13% of events since 2018
- National sources account for ~20% (Ethiopian Broadcasting Corporation, Addis Standard)
- Human rights organizations and new media collectively represent ~10%

**Known biases:**
- Diaspora media have acknowledged political biases — they are not neutral observers
- ACLED triangulates diaspora reports with other source types before coding
- Government internet shutdowns during security crises (e.g., Tigray conflict 2020–2022) create significant information blackouts
- Rural and remote areas, particularly where insurgencies are active, have the weakest source coverage

**Historical context:**
- Decades of state persecution of journalists created weak journalistic institutions
- PM Abiy Ahmed's 2018 reforms improved but did not fully solve the media freedom deficit
- The 2020–2022 Tigray conflict exposed extreme sourcing challenges when communications were cut to an entire region for months

### Democratic Republic of Congo (DRC)

The DRC presents challenges due to:
- **Geographic vastness and inaccessibility** — eastern DRC conflict zones are among the most remote on earth
- **Extreme actor fragmentation** — dozens of armed groups, many unnamed or ephemeral
- **Multiple simultaneous conflicts** — ADF, M23, Mai-Mai groups, and intercommunal violence operating in overlapping territories
- **Low source density** — limited media presence in active conflict areas, especially Ituri, North Kivu, and South Kivu provinces
- **Historical depth** — DRC coverage extends back to 1997, but earlier coding relied on fewer sources and less standardised methodology
- Over 200,000 individual events coded since 1997, with approximately 11,000+ events for DRC specifically

---

## 18. ACLED's Use of Automation and NLP

### ACLED's Sourcing Platform

ACLED uses a proprietary **sourcing platform** to systematically monitor and review news sources. This platform ensures:
- The same sources are checked every week in a consistent manner
- New sources can be added and integrated into the review workflow
- Source coverage is tracked by country and region

### NLP and Machine Learning for Analysis

ACLED has published guidance on using NLP techniques to analyse the free-text `notes` column in their data. Two primary approaches are recommended:

**1. Keyword-Based Search:**
- Useful for quick filtering (e.g., finding events mentioning "drone" or "IED")
- Limitations: misses synonyms, requires manual refinement, not scalable

**2. Classification Models (SetFit / Few-Shot Learning):**
- ACLED recommends **SetFit** (Sentence Transformer Fine-tuning) models for classifying events from the notes column
- Few-shot models achieve high accuracy with minimal training data (10–20 labeled examples)
- Can be used to identify sub-patterns not captured by the standard coding taxonomy (e.g., distinguishing kidnap-for-ransom from political kidnapping)

### ACLED's Internal Automation

ACLED has not published detailed information about its internal NLP pipeline. What is known:
- The core coding remains **human-driven** — ACLED distinguishes itself from machine-coded datasets (like GDELT) precisely through expert human judgment
- Automated **data cleaning and formatting checks** are applied after manual review
- The sourcing platform likely uses automated source monitoring and alerting
- ACLED has progressively incorporated automated tools to support (not replace) human coders

This is fundamentally different from GDELT's fully automated NLP pipeline. ACLED uses technology to support human coders; GDELT replaces them entirely.

---

## 19. Access Tiers and Cost

### Current Access Model (as of 2026)

| Tier | Cost | Access |
|------|------|--------|
| **Free (myACLED)** | Free | Dashboards, aggregated data, Data Export Tool, API with standard limits |
| **Academic/Research** | Free | Full disaggregated event data for non-commercial academic research |
| **Humanitarian/NGO** | Free | Full access for humanitarian organisations |
| **Public Sector** | Requires licence | Government departments need a public-sector licence — contact sales@acleddata.com |
| **Commercial/Corporate** | Requires licence | Corporate entities must obtain a commercial licence before accessing data |

### Commercial Licence

ACLED does not publicly list commercial pricing. The commercial licence:
- Is negotiated on a case-by-case basis — contact sales@acleddata.com
- Pricing is not disclosed on the website (common for data vendors)
- Covers use of ACLED data in commercial products, consulting, or revenue-generating applications

### Embargo Period

When ACLED expands to new regions, there is typically:
- An initial **back-coding period** where historical events are coded retroactively
- A **launch date** after which real-time weekly updates begin
- No formal "embargo" in the journal-publishing sense — data for new regions are released as soon as back-coding and quality review are complete
- The most recent major expansion (February 2022) brought ACLED to full global coverage by adding Canada, Oceania, Antarctica, and remaining small states with data back to 2021

---

## 20. Worked Python Pipeline: API → DataFrame → PRIO-GRID → Parquet

```python
"""
Complete ACLED data pipeline:
  1. Authenticate via OAuth
  2. Fetch all events for a country-year
  3. Convert to pandas DataFrame
  4. Assign PRIO-GRID cell IDs
  5. Aggregate to monthly time series per grid cell
  6. Write to Parquet
"""

import requests
import pandas as pd
import numpy as np
from pathlib import Path


# --- Step 1: Authenticate ---

def get_acled_token(username: str, password: str) -> str:
    """Obtain OAuth access token from ACLED API."""
    resp = requests.post(
        "https://acleddata.com/oauth/token",
        data={
            "grant_type": "password",
            "client_id": "acled",
            "username": username,
            "password": password,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


# --- Step 2: Fetch all events with pagination ---

def fetch_acled_events(
    token: str,
    country: str,
    year: int,
    page_size: int = 5000,
) -> pd.DataFrame:
    """Fetch all ACLED events for a country-year, handling pagination."""
    base_url = "https://acleddata.com/api/acled/read"
    headers = {"Authorization": f"Bearer {token}"}
    all_records = []
    page = 1

    while True:
        params = {
            "_format": "json",
            "country": country,
            "year": year,
            "limit": page_size,
            "page": page,
        }
        resp = requests.get(base_url, headers=headers, params=params, timeout=60)
        resp.raise_for_status()
        result = resp.json()

        if not result.get("success") or not result.get("data"):
            break

        all_records.extend(result["data"])
        print(f"  Page {page}: {len(result['data'])} events")

        if len(result["data"]) < page_size:
            break
        page += 1

    df = pd.DataFrame(all_records)
    print(f"Total: {len(df)} events for {country} in {year}")
    return df


# --- Step 3: Type conversion ---

def clean_acled_df(df: pd.DataFrame) -> pd.DataFrame:
    """Convert string fields to appropriate types."""
    df = df.copy()
    df["event_date"] = pd.to_datetime(df["event_date"])
    df["year"] = df["year"].astype(int)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").fillna(0).astype(int)
    df["geo_precision"] = pd.to_numeric(df["geo_precision"], errors="coerce").fillna(3).astype(int)
    df["time_precision"] = pd.to_numeric(df["time_precision"], errors="coerce").fillna(3).astype(int)
    return df


# --- Step 4: PRIO-GRID assignment ---

def assign_prio_grid(df: pd.DataFrame, resolution: float = 0.5) -> pd.DataFrame:
    """Assign PRIO-GRID cell IDs based on lat/lon coordinates."""
    df = df.copy()
    df = df.dropna(subset=["latitude", "longitude"])
    ncols = int(360 / resolution)  # 720 columns at 0.5°
    df["grid_row"] = np.floor((df["latitude"] + 90) / resolution).astype(int)
    df["grid_col"] = np.floor((df["longitude"] + 180) / resolution).astype(int)
    df["prio_gid"] = df["grid_row"] * ncols + df["grid_col"]
    return df


# --- Step 5: Monthly aggregation ---

def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate events to monthly counts per PRIO-GRID cell."""
    df = df.copy()
    df["year_month"] = df["event_date"].dt.to_period("M")

    agg = df.groupby(["prio_gid", "year_month"]).agg(
        total_events=("event_id_cnty", "count"),
        total_fatalities=("fatalities", "sum"),
        battles=("event_type", lambda x: (x == "Battles").sum()),
        explosions=("event_type", lambda x: (x == "Explosions/Remote violence").sum()),
        violence_against_civilians=("event_type", lambda x: (x == "Violence against civilians").sum()),
        protests=("event_type", lambda x: (x == "Protests").sum()),
        riots=("event_type", lambda x: (x == "Riots").sum()),
        strategic_developments=("event_type", lambda x: (x == "Strategic developments").sum()),
        mean_geo_precision=("geo_precision", "mean"),
        low_precision_pct=("geo_precision", lambda x: (x >= 2).mean()),
        low_time_precision_pct=("time_precision", lambda x: (x >= 2).mean()),
    ).reset_index()

    # Convert Period to string for Parquet compatibility
    agg["year_month"] = agg["year_month"].astype(str)
    return agg


# --- Step 6: Write to Parquet ---

def save_to_parquet(df: pd.DataFrame, output_path: str) -> None:
    """Save DataFrame to Parquet with compression."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, engine="pyarrow", compression="snappy", index=False)
    print(f"Saved {len(df)} rows to {output_path}")


# --- Full pipeline ---

def run_pipeline(
    username: str,
    password: str,
    country: str,
    year: int,
    output_dir: str = "./data/acled",
):
    """Run the complete ACLED → PRIO-GRID → Parquet pipeline."""
    print(f"=== ACLED Pipeline: {country} {year} ===")

    token = get_acled_token(username, password)
    raw_df = fetch_acled_events(token, country, year)

    if raw_df.empty:
        print("No events found.")
        return

    clean_df = clean_acled_df(raw_df)
    gridded_df = assign_prio_grid(clean_df)
    monthly_df = aggregate_monthly(gridded_df)

    output_path = f"{output_dir}/{country.lower().replace(' ', '_')}_{year}_monthly_grid.parquet"
    save_to_parquet(monthly_df, output_path)

    # Summary statistics
    print(f"\nSummary:")
    print(f"  Raw events: {len(raw_df)}")
    print(f"  Grid cells with events: {monthly_df['prio_gid'].nunique()}")
    print(f"  Months covered: {monthly_df['year_month'].nunique()}")
    print(f"  Total fatalities: {monthly_df['total_fatalities'].sum()}")
    print(f"  Mean geo precision: {gridded_df['geo_precision'].mean():.2f}")


# Usage:
# run_pipeline("your@email.com", "your_password", "Somalia", 2024)
```

---

## 21. Sources

### Official ACLED resources

- **Website:** https://acleddata.com
- **Codebook (October 2024):** https://acleddata.com/methodology/acled-codebook
- **Codebook PDF (October 2024):** https://acleddata.com/sites/default/files/wp-content-archive/uploads/dlm_uploads/2024/10/ACLED-Codebook-2024-7-Oct.-2024.pdf
- **API documentation hub:** https://acleddata.com/acled-api-documentation/
- **API Getting Started:** https://acleddata.com/api-documentation/getting-started
- **ACLED Endpoint reference:** https://acleddata.com/api-documentation/acled-endpoint
- **API Elements guide:** https://acleddata.com/api-documentation/elements-acleds-api
- **CAST Endpoint:** https://acleddata.com/api-documentation/cast-endpoint
- **Knowledge Base:** https://acleddata.com/knowledge-base/
- **Coding & Review Process:** https://acleddata.com/methodology/how-does-acled-code-and-review-data-ensure-quality
- **Quality Assurance FAQ:** https://acleddata.com/faq/how-quality-acled-data-ensured
- **EULA:** https://acleddata.com/eula/
- **Attribution Policy:** https://acleddata.com/attributionpolicy/
- **Data Export Tool:** https://acleddata.com/conflict-data/data-export-tool
- **Curated data files:** https://acleddata.com/curated-data-files/
- **Conflict Index:** https://acleddata.com/general-guide/about-conflict-index
- **Weekly Conflict Index:** https://acleddata.com/platform/weekly-conflict-index
- **Country/time-period coverage:** https://acleddata.com/methodology/countrytime-period-coverage
- **Myanmar methodology:** https://acleddata.com/knowledge-base/acled-methodology-and-coding-decisions-around-political-violence-and-demonstrations-in-myanmar/
- **Ethiopia sourcing:** https://acleddata.com/methodology/how-does-acled-source-events-ethiopia
- **NLP analysis guide:** https://acleddata.com/methodology/how-analyze-acleds-notes-column-using-natural-language-processing-nlp
- **Coding Review Process PDF (v2, 2020):** https://acleddata.com/sites/default/files/wp-content-archive/uploads/2021/11/ACLED_Coding-Review-Process_v2_September-2020.pdf
- **Comparing Conflict Data (working paper):** https://acleddata.com/sites/default/files/wp-content-archive/uploads/2022/02/ACLED_WorkingPaper_ComparisonAnalysis_2019.pdf
- **myACLED FAQs:** https://acleddata.com/myacled-faqs

### Academic references

- Raleigh, C., Linke, A., Hegre, H., & Karlsen, J. (2010). "Introducing ACLED: An Armed Conflict Location and Event Dataset." *Journal of Peace Research*, 47(5), 651–660. https://doi.org/10.1177/0022343310378914 — **The founding paper**
- Raleigh, C., Kishi, R., & Linke, A. (2023). "Political instability patterns are obscured by conflict dataset scope conditions." *Humanities and Social Sciences Communications*, 10, 74. — **ACLED's recommended citation**
- Eck, K. (2012). "In data we trust? A comparison of UCDP GED and ACLED conflict events datasets." *Cooperation and Conflict*, 47(1), 124–141. — **Systematic comparison of ACLED vs. UCDP**
- Donnay, K., Dunford, E.T., McGrath, E.C., Backer, D., & Cunningham, D.E. (2019). "Integrating conflict event data." *Journal of Conflict Resolution*, 63(5), 1337–1364. — **Methods for reconciling conflict datasets**
- Hammond, J. & Weidmann, N.B. (2014). "Using machine-coded event data for the micro-level study of political violence." *Research & Politics*, 1(2). — **Hand-coded vs. machine-coded quality comparison**
- Salehyan, I., Hendrix, C.S., Hamner, J., Case, C., Linebarger, C., Stull, E., & Williams, J. (2012). "Social Conflict in Africa: A New Database." *International Interactions*, 38(4), 503–511. — **SCAD methodology**
- Sundberg, R. & Melander, E. (2013). "Introducing the UCDP Georeferenced Event Dataset." *Journal of Peace Research*, 50(4), 523–532. — **UCDP-GED founding paper**
- START (2021). "Global Terrorism Database Codebook." University of Maryland. — **GTD methodology**

### Python tools

- `acled` PyPI package: https://pypi.org/project/acled/ (unofficial, v0.2.4)
- GitHub: https://github.com/blazeiburgess/acled
- `acledR` R package: https://dtacled.github.io/acledR/
- `acled.api` R package: https://cran.r-project.org/web/packages/acled.api/
- ACLED data pipeline example: https://github.com/19Vermouth/ACLED-data-pipeline

### Related Causal Atlas research files

- `research/datasets/ucdp-ged.md` — Complementary conflict dataset
- `research/datasets/prio-grid.md` — Spatial backbone framework
- `research/datasets/hdx-hapi.md` — Humanitarian data API
- `research/03-causal-chains.md` — Cross-domain causality literature
- `research/04-statistical-methods.md` — Analytical methods

---

*Last updated: March 2026*
