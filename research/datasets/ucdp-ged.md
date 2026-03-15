# UCDP Georeferenced Event Dataset (GED) — Deep Dive

> Last updated: March 2025

---

## 1. Overview

The **Uppsala Conflict Data Program (UCDP)** is the world's foremost academic provider of data on organised violence and armed conflict. Maintained by the Department of Peace and Conflict Research at Uppsala University (Sweden), UCDP has been collecting data since 1946 and is widely used in political science, peace research, and humanitarian analysis.

The **Georeferenced Event Dataset (GED)** is UCDP's most granular product: individual events of organised violence, geo-coded to specific locations with daily temporal precision, from 1989 onward. Each event is researcher-coded from news sources, NGO reports, and official records, following a strict and transparent coding methodology. This makes it distinct from machine-coded datasets like GDELT and a complement to ACLED (which uses a similar but distinct methodology).

- **Maintainer:** Uppsala Conflict Data Program, Uppsala University
- **Principal investigators:** Various (historically Nils Petter Gleditsch, Peter Wallensteen; currently led by the UCDP team)
- **Key publication:** Sundberg, R. and E. Melander (2013). "Introducing the UCDP Georeferenced Event Dataset," *Journal of Peace Research*, 50(4): 523–532.
- **Website:** https://ucdp.uu.se/
- **API documentation:** https://ucdp.uu.se/apidocs/
- **Download centre:** https://ucdp.uu.se/downloads/
- **Current version:** GED v25.1 (covering 1989–2024)

---

## 2. Coverage

### Spatial

- **Global.** All countries worldwide are covered.
- Events are geo-coded to the most precise location identifiable from sources, ranging from exact coordinates (village/town level) to district or province centroids when precision is lower.
- **Precision coding:** Each event has a `where_prec` field indicating spatial precision (see Schema section).
- Coverage quality is best where media reporting is dense. Conflict events in remote areas with poor media coverage may be undercounted.

### Temporal

- **GED range:** 1989–2024 (v25.1)
- **Update cycle:** Annual major releases (e.g., v25.1 covering through end of 2024).
- **Candidate Events Dataset:** Monthly releases with approximately one month lag, providing near-real-time data that is later incorporated into the next annual GED release. Current: v26.0.1 (January 2026).
- **Quarterly candidate releases** are also available for some periods (e.g., v25.01.25.12).

### Types of violence covered

UCDP codes three types of organised violence:

| Type | Code | Definition |
|------|------|------------|
| **State-based conflict** | 1 | Armed conflict between a government and an organised armed group, OR between two governments. At least 25 battle-related deaths per calendar year in a conflict dyad. |
| **Non-state conflict** | 2 | Armed conflict between two organised armed groups, neither of which is a government. At least 25 battle-related deaths per calendar year. |
| **One-sided violence** | 3 | Deliberate use of armed force by a government or organised armed group against civilians. At least 25 deaths per calendar year by the perpetrating actor. |

**Critical threshold:** UCDP uses a **25-death annual threshold** for inclusion. Conflicts or actors that do not reach this threshold in a given year are not included. This is a fundamental difference from ACLED, which has no minimum threshold.

---

## 3. Access

### 3.1 API Access

**Base URL:**
```
https://ucdpapi.pcr.uu.se/api/
```

**Authentication:** Required since February 2026. Requests must include:
```
x-ucdp-access-token: YOUR-TOKEN
```
Tokens are obtained by contacting the API maintainer (mertcan.yilmaz@pcr.uu.se) and describing your research project.

**Rate limit:** 5,000 requests per day (errors count toward this limit).

**API architecture:** RESTful, returning JSON responses. Versioned: each URL is guaranteed to return the same data at the same version indefinitely, enabling reproducible research.

**Endpoint format:**
```
https://ucdpapi.pcr.uu.se/api/<resource>/<version>?<pagesize=x>&<page=x>[&filters]
```

### 3.2 Available API Resources

#### Event-level data

| Resource | Description | Current Version | Historical Versions |
|----------|-------------|----------------|-------------------|
| `gedevents` | Georeferenced Event Dataset | 25.1 | 5.0, 17.1, 17.2, 18.1, 19.1, 20.1, 21.1, 22.1, 23.1, 24.1 |
| `gedevents-candidate` | Monthly/quarterly candidate events | 26.0.1 | Various |

#### Yearly aggregated datasets

| Resource | Description | Version | Coverage |
|----------|-------------|---------|----------|
| `ucdpprioconflict` | UCDP/PRIO Armed Conflict Dataset | 25.1 | 1946–2024 |
| `dyadic` | Dyadic Dataset (opposing actors) | 25.1 | 1946–2024 |
| `nonstate` | Non-State Conflict Dataset | 25.1 | 1989–2024 |
| `onesided` | One-Sided Violence Dataset | 25.1 | 1989–2024 |
| `battledeaths` | Battle-Related Deaths Dataset | 25.1 | 1989–2023 |

### 3.3 GED API Query Parameters

| Parameter | Type | Multiple Values | Description |
|-----------|------|----------------|-------------|
| `pagesize` | Integer | No | Results per page |
| `page` | Integer | No | Page number |
| `Id` | Integer | Yes (comma-separated) | Event identifier |
| `Country` | Integer | Yes | Gleditsch-Ward country code |
| `Geography` | String | No | Bounding box: `y0 x0,y1 x1` (SW lat lon, NE lat lon) |
| `StartDate` | String | No | Events from this date onward (YYYY-MM-DD) |
| `EndDate` | String | No | Events up to this date (YYYY-MM-DD) |
| `TypeOfViolence` | Integer | Yes | 1=state-based, 2=non-state, 3=one-sided |
| `Dyad` | Integer | Yes | Dyad ID (new format, v5.0+) |
| `Actor` | Integer | Yes | Actor ID — returns all events involving this actor |

**Filter logic:**
- Multiple values within a parameter: **OR** (comma-separated, e.g., `Country=90,91,92`)
- Multiple parameters: **AND** (ampersand-separated)
- Both `StartDate` and `EndDate` filter on the `date_end` field.
- Non-existent filter names are silently ignored.
- Invalid filter values return empty result sets.

**Response structure:**
```json
{
  "TotalCount": 12345,
  "TotalPages": 124,
  "PreviousPageUrl": "...",
  "NextPageUrl": "...",
  "Result": [
    { /* event objects */ }
  ]
}
```

**Important notes:**
- Result ordering within a session is consistent but not sorted by any meaningful field. Client-side sorting is required.
- Out-of-bounds page numbers may cause server errors. Always check `TotalPages`.
- Custom headers cannot be sent from browser address bars — programmatic access required.

### 3.4 Yearly Dataset API Parameters

#### ucdpprioconflict / dyadic
| Parameter | Description |
|-----------|-------------|
| `Country` | Gleditsch-Ward code |
| `Conflict` | conflict_id |
| `Year` | YYYY |
| `ConflictIncompatibility` | Incompatibility code |
| `ConflictType` | Type of conflict code |

#### nonstate
| Parameter | Description |
|-----------|-------------|
| `Country` | Gleditsch-Ward code |
| `Conflict` | conflict_id |
| `Org` | Organisation code |
| `Year` | YYYY |

#### onesided
| Parameter | Description |
|-----------|-------------|
| `Dyad` | actor_id |
| `Country` | Gleditsch-Ward code |
| `Year` | YYYY |

### 3.5 Bulk Download

All datasets are available for direct download from https://ucdp.uu.se/downloads/ in:
- **CSV** (recommended for data analysis)
- **Excel** (.xlsx)
- **R** (.rdata)
- **Stata** (.dta)

For Causal Atlas, the bulk CSV download of GED is likely more practical than paginated API access for initial data loading.

### 3.6 Example API Requests

```bash
# Get events in Syria (GW code 652), 2020, state-based violence
curl -H "x-ucdp-access-token: YOUR-TOKEN" \
  "https://ucdpapi.pcr.uu.se/api/gedevents/25.1?Country=652&StartDate=2020-01-01&EndDate=2020-12-31&TypeOfViolence=1&pagesize=100&page=1"

# Get events in a bounding box (East Africa)
curl -H "x-ucdp-access-token: YOUR-TOKEN" \
  "https://ucdpapi.pcr.uu.se/api/gedevents/25.1?Geography=-12 25,15 52&pagesize=100"

# Count total events (check TotalCount in response)
curl -H "x-ucdp-access-token: YOUR-TOKEN" \
  "https://ucdpapi.pcr.uu.se/api/gedevents/25.1?pagesize=1&page=1"
```

---

## 4. Schema

### 4.1 GED Event Fields (Complete)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique event identifier |
| `relid` | String | Related event ID (legacy) |
| `year` | Integer | Year of event |
| `active_year` | Integer | Whether the conflict was active that year |
| `code_status` | String | Coding status |
| `type_of_violence` | Integer | 1=state-based, 2=non-state, 3=one-sided |
| `conflict_dset_id` | Integer | Conflict dataset ID (legacy) |
| `conflict_new_id` | Integer | Conflict ID (v5.0+ format) |
| `conflict_name` | String | Name of the conflict |
| `dyad_dset_id` | Integer | Dyad dataset ID (legacy) |
| `dyad_new_id` | Integer | Dyad ID (v5.0+ format) |
| `dyad_name` | String | Name of the dyad |
| `side_a_dset_id` | Integer | Side A dataset ID |
| `side_a_new_id` | Integer | Side A ID (v5.0+) |
| `side_a` | String | Name of Side A (typically government) |
| `side_b_dset_id` | Integer | Side B dataset ID |
| `side_b_new_id` | Integer | Side B ID (v5.0+) |
| `side_b` | String | Name of Side B (typically rebel/opposition group) |
| `number_of_sources` | Integer | Number of sources consulted |
| `source_article` | String | Source article reference |
| `source_office` | String | Source office/organisation |
| `source_date` | String | Source date |
| `source_headline` | String | Source headline |
| `source_original` | String | Original source text |
| `where_prec` | Integer | Spatial precision (1–7, see below) |
| `where_coordinates` | String | Location coordinates description |
| `where_description` | String | Location name/description |
| `adm_1` | String | Admin level 1 (province/state) |
| `adm_2` | String | Admin level 2 (district) |
| `latitude` | Decimal | Event latitude (WGS84) |
| `longitude` | Decimal | Event longitude (WGS84) |
| `geom_wkt` | String | Well-Known Text geometry |
| `priogrid_gid` | Integer | PRIO-GRID cell ID |
| `country` | String | Country name |
| `country_id` | Integer | Gleditsch-Ward country code |
| `region` | String | Region name |
| `event_clarity` | Integer | Clarity of event description (1=clear, 2=unclear) |
| `date_prec` | Integer | Date precision (1–5, see below) |
| `date_start` | String | Event start date (YYYY-MM-DD) |
| `date_end` | String | Event end date (YYYY-MM-DD) |
| `deaths_a` | Integer | Deaths on Side A |
| `deaths_b` | Integer | Deaths on Side B |
| `deaths_civilians` | Integer | Civilian deaths |
| `deaths_unknown` | Integer | Deaths of unknown affiliation |
| `best` | Integer | Best estimate of total deaths |
| `high` | Integer | High estimate of total deaths |
| `low` | Integer | Low estimate of total deaths |
| `gwnoa` | Integer | Gleditsch-Ward number for actor A |
| `gwnob` | Integer | Gleditsch-Ward number for actor B |

### 4.2 Spatial Precision Codes (`where_prec`)

| Code | Description | Typical accuracy |
|------|-------------|-----------------|
| 1 | Exact location identified | Within a few km |
| 2 | Near a named location | ~25 km |
| 3 | Within a second-order admin region (district) | ~50 km |
| 4 | Within a first-order admin region (province) | ~100 km |
| 5 | Within a country, but exact region unknown | Country centroid |
| 6 | International waters or border area | Variable |
| 7 | Location unclear/unknown | Very low precision |

For Causal Atlas, events with `where_prec` >= 5 should be treated with caution or excluded from fine-grained spatial analysis.

### 4.3 Date Precision Codes (`date_prec`)

| Code | Description |
|------|-------------|
| 1 | Exact date known |
| 2 | Accurate to within a few days |
| 3 | Accurate to within a week |
| 4 | Accurate to within a month |
| 5 | Only the year is known |

### 4.4 Fatality Estimates

Each event has three fatality estimates:
- **`best`**: The most likely total death count (deaths_a + deaths_b + deaths_civilians + deaths_unknown, using best judgment when sources conflict)
- **`low`**: Lower bound estimate
- **`high`**: Upper bound estimate

These reflect uncertainty in reporting. The spread between low and high indicates how conflicting the sources are.

### 4.5 Sample Record

```json
{
  "id": 245891,
  "year": 2022,
  "type_of_violence": 1,
  "conflict_new_id": 418,
  "conflict_name": "Ethiopia: Tigray",
  "dyad_name": "Government of Ethiopia - TPLF",
  "side_a": "Government of Ethiopia",
  "side_b": "TPLF",
  "where_prec": 2,
  "where_description": "Near Mekelle, Tigray",
  "adm_1": "Tigray",
  "latitude": 13.497,
  "longitude": 39.475,
  "priogrid_gid": 154821,
  "country": "Ethiopia",
  "country_id": 530,
  "date_prec": 1,
  "date_start": "2022-03-15",
  "date_end": "2022-03-15",
  "deaths_a": 5,
  "deaths_b": 12,
  "deaths_civilians": 3,
  "deaths_unknown": 0,
  "best": 20,
  "low": 15,
  "high": 30,
  "number_of_sources": 4
}
```

---

## 5. Spatial Detail

- **Point locations.** Each event has a single lat/lon coordinate in WGS84.
- **Variable precision.** The `where_prec` field (1–7) indicates how accurate the coordinates are. Precision 1–2 events are located to within a few km; precision 5+ events are placed at country centroids and should not be used for sub-national spatial analysis.
- **PRIO-GRID cell ID included.** Uniquely among conflict datasets, GED includes a `priogrid_gid` field assigning each event to a PRIO-GRID 0.5 x 0.5 degree cell. This is a major advantage for Causal Atlas integration.
- **Admin region coding.** `adm_1` and `adm_2` provide administrative region names, useful for joining with admin-level datasets.
- **WKT geometry.** The `geom_wkt` field provides Well-Known Text geometry (typically a point).
- **Gleditsch-Ward country codes.** Used instead of ISO codes in some fields. Mapping tables are available.

### PRIO-GRID compatibility

**Native.** GED includes `priogrid_gid` directly. No spatial join needed. This makes it the most PRIO-GRID-ready conflict dataset available.

---

## 6. Temporal Detail

- **Daily resolution.** Events have `date_start` and `date_end` fields (YYYY-MM-DD). Most events are single-day (`date_start == date_end`), but multi-day events (e.g., prolonged battles) span a range.
- **Date precision coded.** The `date_prec` field (1–5) indicates confidence in the date. Most events have precision 1 (exact date known).
- **No sub-daily timestamps.** No time-of-day information.
- **Temporal coverage:** 1989 to present (annual release), with near-real-time candidate events released monthly.

### Temporal aggregation for Causal Atlas

- Aggregate to monthly event counts and fatality totals per PRIO-GRID cell.
- Separate by `type_of_violence` (state-based, non-state, one-sided).
- Consider weighting: event count vs. total `best` fatalities vs. number of events above a fatality threshold.
- For events spanning multiple days, assign to the month of `date_start` (or split proportionally).

---

## 7. Quality

### Strengths

- **Researcher-coded.** Every event is coded by trained researchers following a detailed codebook. This is the gold standard for accuracy in conflict data.
- **Conservative and transparent.** The 25-death threshold and strict inclusion criteria mean that every event in GED is a verified instance of organised violence. Low false-positive rate.
- **Fatality uncertainty quantified.** Low/best/high estimates capture reporting uncertainty explicitly.
- **Spatial and temporal precision coded.** Users can filter by precision level for their analysis needs.
- **Reproducible.** Each API version is permanently frozen. Same query always returns same data.
- **Comprehensive codebook.** Detailed documentation of every coding decision, freely available.
- **Long track record.** UCDP has been coding conflict data since 1946 (yearly data) and 1989 (events).
- **PRIO-GRID cell IDs included.** Pre-computed for spatial analysis.

### Known limitations and biases

- **25-death threshold.** Events below 25 deaths per conflict-year are excluded. This systematically undercounts low-intensity violence, early stages of conflicts, and small-scale communal violence. ACLED has no such threshold.
- **Media bias.** Events in areas with poor media coverage (remote regions, media blackouts, internet shutdowns) are less likely to be captured. UCDP acknowledges this and uses multiple source types to mitigate, but gaps remain.
- **Annual release cycle.** The main GED dataset is updated annually. The monthly candidate events provide interim data but are considered preliminary and may be revised.
- **Lag.** Candidate events have ~1 month lag. The annual dataset has several months of processing time after year-end.
- **Fatality estimation challenges.** In many conflicts, reliable death counts are unavailable. The low/high range can be very wide. Government and rebel sources often provide conflicting numbers.
- **Non-state and one-sided violence harder to capture.** These events often receive less media attention than state-based conflict.
- **No protest or riot coding.** Unlike ACLED, UCDP does not code protests, riots, or non-lethal events. Only armed violence resulting in fatalities is included.
- **Historical coverage only from 1989.** Event-level data starts in 1989. For earlier periods, only yearly aggregated data is available (from 1946).

### Validation

- UCDP data is the most cited conflict dataset in academic literature. It has been extensively validated against alternative sources and other datasets.
- Regular cross-checking against ACLED, SIPRI, and national sources.
- Peer-reviewed methodology publications.
- Inter-coder reliability testing.

---

## 8. Licence

- **Creative Commons Attribution 4.0 (CC BY 4.0).** All UCDP datasets are freely available under this licence.
- **Attribution required.** Users must cite the relevant UCDP publications. Required citations are listed on the download page for each dataset.
- **No commercial restrictions.** CC BY 4.0 allows commercial use with attribution.
- **API access:** Free with token (obtained by contacting UCDP and describing your project).
- **Bulk download:** Free, no registration required for direct file downloads.

### Required citation for GED

> Sundberg, Ralph, and Erik Melander (2013). "Introducing the UCDP Georeferenced Event Dataset." *Journal of Peace Research* 50(4): 523-532.

> Davies, Shawn, Therese Pettersson & Magnus Oberg (2024). "Organized violence 1989-2023, and the return of conflict between states." *Journal of Peace Research* 61(4).

---

## 9. Interoperability

### Shared identifiers

| Identifier | Used in | Notes |
|------------|---------|-------|
| Gleditsch-Ward country codes | UCDP, PRIO-GRID, COW | Standard in political science; mappable to ISO codes |
| `priogrid_gid` | PRIO-GRID, UCDP GED | Direct cell-level linkage |
| Conflict IDs | UCDP datasets (internal) | Consistent across GED, Armed Conflict Dataset, dyadic, etc. |
| Actor IDs | UCDP datasets (internal) | Link actors across events and years |

### UCDP vs. ACLED: Comparison and Complementarity

This is a critical comparison for Causal Atlas, as both are major georeferenced conflict event datasets.

| Dimension | UCDP GED | ACLED |
|-----------|----------|-------|
| **Coding method** | Researcher-coded (human coders, codebook) | Research assistant-coded with AI assistance |
| **Inclusion threshold** | 25 deaths/year per conflict dyad | No minimum threshold |
| **Event types** | Armed violence only (battles, one-sided violence) | Battles, protests, riots, strategic developments, non-violent events |
| **Temporal coverage** | 1989–present | 1997–present (varies by region; Africa from 1997, global from 2018) |
| **Spatial coverage** | Global (1989+) | Global (phased expansion, full global from 2018) |
| **Update frequency** | Annual (monthly candidates) | Weekly (near real-time) |
| **Fatality estimates** | Low/best/high for every event | Best estimate only; many events have 0 or unreported |
| **Spatial precision** | Coded 1–7 with coordinates | Coded 1–3, coordinates assigned |
| **PRIO-GRID ID** | Included natively | Not included (must compute) |
| **API** | RESTful JSON, token required | RESTful JSON, token required |
| **Licence** | CC BY 4.0 | Free for non-commercial; commercial requires agreement |
| **Riots/protests** | Not coded | Coded |
| **Strategic developments** | Not coded | Coded (troop movements, agreements, etc.) |

**Key complementarity for Causal Atlas:**
- Use UCDP as the **conservative, research-validated baseline** for armed violence.
- Use ACLED for **broader event coverage** including protests, riots, and sub-threshold violence.
- Cross-validate: events appearing in both datasets provide higher confidence.
- UCDP's fatality uncertainty ranges (low/best/high) are unavailable in ACLED.
- UCDP's PRIO-GRID cell IDs eliminate a spatial join step.

### Integration with other Causal Atlas datasets

| Dataset | Linkage | Notes |
|---------|---------|-------|
| PRIO-GRID | Native `priogrid_gid` | Direct cell-level join |
| ACLED | Spatiotemporal matching | No shared event IDs; match by location + date |
| EM-DAT | Country + year | EM-DAT uses ISO codes; need GW-to-ISO mapping |
| WFP Food Prices | Admin region + month | UCDP `adm_1` can be matched to WFP market locations |
| CHIRPS | PRIO-GRID cell + month | Rainfall as a covariate |
| VIIRS Nightlights | PRIO-GRID cell + month | Economic impact proxy |
| World Bank | Country + year | National-level context |
| HDX HAPI | Admin region + month | Displacement and humanitarian indicators |

### ID mapping resources

UCDP uses Gleditsch-Ward country codes, not ISO. A mapping table is needed:
- GW to ISO: Available from the Correlates of War project (https://correlatesofwar.org/)
- UCDP provides translation tables for pre-v17.1 to post-v17.1 actor and dyad IDs.

---

## 10. Python Access

### 10.1 Direct API with requests

```python
import requests
import pandas as pd

TOKEN = "YOUR-UCDP-TOKEN"
BASE = "https://ucdpapi.pcr.uu.se/api"
headers = {"x-ucdp-access-token": TOKEN}

def fetch_all_ged_events(version="25.1", **filters):
    """Fetch all GED events matching filters, handling pagination."""
    url = f"{BASE}/gedevents/{version}"
    params = {"pagesize": 1000, "page": 1, **filters}

    all_results = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        all_results.extend(data["Result"])

        if params["page"] >= data["TotalPages"]:
            break
        params["page"] += 1

    return pd.DataFrame(all_results)

# Get all state-based conflict events in Ethiopia, 2020-2023
df = fetch_all_ged_events(
    Country=530,            # Gleditsch-Ward code for Ethiopia
    StartDate="2020-01-01",
    EndDate="2023-12-31",
    TypeOfViolence=1        # State-based
)
print(f"Events: {len(df)}")
print(df[['date_start', 'side_a', 'side_b', 'best', 'latitude', 'longitude']].head())
```

### 10.2 Bounding box query

```python
# Events in East Africa bounding box
df = fetch_all_ged_events(
    Geography="-12 25,15 52",  # SW lat lon, NE lat lon
    StartDate="2022-01-01",
    EndDate="2022-12-31"
)

# Summarise by type of violence
print(df.groupby('type_of_violence')['best'].agg(['count', 'sum', 'mean']))
```

### 10.3 Bulk download approach (recommended for large analyses)

```python
import pandas as pd

# Download GED CSV from UCDP website (faster than paginating the API)
# URL: https://ucdp.uu.se/downloads/ged/ged251-csv.zip
df = pd.read_csv("ged251.csv")

print(f"Total events: {len(df)}")
print(f"Years: {df['year'].min()}-{df['year'].max()}")
print(f"Countries: {df['country'].nunique()}")
print(f"Total best-estimate fatalities: {df['best'].sum():,}")

# Filter and aggregate for Causal Atlas
monthly = (
    df.assign(month=pd.to_datetime(df['date_start']).dt.to_period('M'))
    .groupby(['priogrid_gid', 'month', 'type_of_violence'])
    .agg(
        event_count=('id', 'count'),
        fatalities_best=('best', 'sum'),
        fatalities_low=('low', 'sum'),
        fatalities_high=('high', 'sum'),
        civilian_deaths=('deaths_civilians', 'sum')
    )
    .reset_index()
)
print(monthly.head())
```

### 10.4 Using the UCDP/PRIO Armed Conflict Dataset

```python
# For yearly conflict-level data (goes back to 1946)
response = requests.get(
    f"{BASE}/ucdpprioconflict/25.1",
    headers=headers,
    params={"Country": 530, "pagesize": 100}
)
conflicts = pd.DataFrame(response.json()["Result"])
```

### 10.5 Third-party Python packages

There is no widely-used dedicated Python package for UCDP (unlike libcomcat for USGS). The API is simple enough that `requests` + `pandas` is the standard approach. Some researchers have published utility scripts:
- `ucdp` on PyPI exists but is minimally maintained.
- The `views_data` package from the VIEWS project (which uses UCDP data) may be useful: https://github.com/prio-data/views_data

### 10.6 Recommended approach for Causal Atlas

1. **Initial load:** Bulk download the GED CSV from the UCDP website (much faster than API pagination for the full dataset).
2. **Monthly updates:** Use the candidate events API to fetch new events, checking against the `NextPageUrl` for pagination.
3. **Annual refresh:** When a new GED version is released, download the full CSV and replace the prior version.
4. **PRIO-GRID aggregation:** Use the native `priogrid_gid` field — no spatial join needed.
5. **Combine with ACLED:** Load ACLED data, compute PRIO-GRID cell IDs (ACLED lacks them natively), and join on cell + month.

---

## 11. Relevance to Causal Atlas

### Domain

Armed conflict / organised violence / political violence.

### Causal chains UCDP data can illuminate

1. **Drought/food crisis -> Armed conflict escalation.** Correlate CHIRPS rainfall anomalies and WFP food price spikes with subsequent changes in UCDP event counts per cell. Published literature finds modest but statistically significant effects with 3–12 month lags.

2. **Armed conflict -> Displacement -> Humanitarian crisis.** Conflict events (especially one-sided violence) drive civilian displacement. HDX HAPI displacement data can be analysed in the wake of UCDP event clusters.

3. **Armed conflict -> Economic decline.** VIIRS nightlight reductions in conflict-affected PRIO-GRID cells. Lag: months.

4. **Armed conflict -> Food insecurity.** Destruction of agricultural infrastructure, market disruption, movement restrictions. WFP food prices and FAO production data as outcomes. Lag: months to one growing season.

5. **Armed conflict -> Health system disruption.** Attacks on health facilities, displacement of health workers. Disease outbreaks (WHO, ProMED) as downstream indicators.

6. **Natural disaster -> Conflict (contested).** Earthquakes, floods, droughts as potential triggers for conflict. USGS earthquake and EM-DAT disaster data as inputs. Lag: months to years. Evidence is mixed and context-dependent.

7. **Conflict contagion / spatial diffusion.** Conflict in one PRIO-GRID cell may increase conflict risk in neighbouring cells. Spatial lag models and Moran's I applied to UCDP monthly cell counts.

8. **Economic inequality -> Conflict onset.** World Bank Gini coefficients and GDP per capita as structural predictors. Long-term lags (years).

### Why both UCDP and ACLED matter for Causal Atlas

- **UCDP provides the research-validated, conservative baseline.** Every event has been human-coded, fatality estimates include uncertainty ranges, and the 25-death threshold ensures all events represent significant organised violence.
- **ACLED provides broader coverage.** Protests, riots, and low-level violence that UCDP excludes may be important leading indicators of escalation.
- **Cross-validation.** When UCDP and ACLED agree on event counts and locations, confidence is high. Discrepancies can flag data quality issues or methodological differences.
- **The VIEWS forecasting project** (https://viewsforecasting.org/) uses UCDP as its primary conflict data source and PRIO-GRID as its spatial framework — exactly matching Causal Atlas's approach.

---

## 12. Sources

- UCDP website: https://ucdp.uu.se/
- UCDP API documentation: https://ucdp.uu.se/apidocs/
- UCDP download centre: https://ucdp.uu.se/downloads/
- Sundberg, R. and E. Melander (2013). "Introducing the UCDP Georeferenced Event Dataset." *Journal of Peace Research*, 50(4): 523–532. https://doi.org/10.1177/0022343313484347
- Davies, S., T. Pettersson & M. Oberg (2024). "Organized violence 1989-2023, and the return of conflict between states." *Journal of Peace Research*, 61(4).
- Pettersson, T. (2024). "UCDP/PRIO Armed Conflict Dataset Codebook, v25.1." Uppsala University. https://ucdp.uu.se/downloads/
- UCDP methodology overview: https://ucdp.uu.se/methodology
- UCDP definitions: https://www.uu.se/en/department/peace-and-conflict-research/research/ucdp/definitions/
- Gleditsch-Ward country codes: https://correlatesofwar.org/
- VIEWS forecasting project (uses UCDP + PRIO-GRID): https://viewsforecasting.org/
- ACLED comparison: https://acleddata.com/ (see Raleigh et al., 2010, "Introducing ACLED," *Journal of Peace Research*, 47(5): 651–660)
- PRIO-GRID framework: https://grid.prio.org/
- UCDP API contact for tokens: mertcan.yilmaz@pcr.uu.se
- UCDP accessibility statement: https://www.uu.se/en/department/peace-and-conflict-research/research/ucdp/ucdp-conflict-encyclopedia-ucdp-database/accessibility-statement

---

## 13. UCDP Coding Methodology — Detailed

Understanding how UCDP codes events is essential for interpreting the data correctly.

### Source Collection

UCDP uses a systematic source collection process:

1. **Primary sources:** Newswire services (Reuters, AFP, AP), major international newspapers, regional news agencies
2. **Secondary sources:** NGO reports (Human Rights Watch, Amnesty International, ICG), official government statements, UN reports, academic publications
3. **Local sources:** Local media outlets, civil society monitoring organisations

Each event record includes `number_of_sources`, `source_article`, `source_office`, and `source_original` fields documenting the evidentiary basis.

### Coding Process

1. **Event identification:** Trained researchers scan sources daily for reports of organised violence worldwide
2. **Eligibility check:** Does the event involve an organised armed group? Does it result in at least one direct death? Is it part of a conflict that has or will reach the 25-death annual threshold?
3. **Georeferencing:** The event is assigned coordinates based on the most specific location information available. A precision code (1-7) records confidence
4. **Date assignment:** Start and end dates are assigned. Precision code (1-5) records confidence
5. **Fatality estimation:** Low, best, and high estimates are derived from cross-referencing multiple sources. When sources conflict, the coder applies structured judgment rules
6. **Actor identification:** Both sides (Side A and Side B) are identified and linked to standing actor and dyad records
7. **Review:** Events are peer-reviewed by at least one additional coder. Disputed codings are resolved through discussion

### The 25-Death Threshold — Detailed Implications

UCDP's definition of armed conflict requires **at least 25 battle-related deaths per calendar year per conflict dyad**. This has several important implications:

| Implication | Detail |
|---|---|
| **Inclusion criterion** | A new conflict is only added to the database when it first reaches 25 deaths in a dyad in a calendar year |
| **Activity criterion** | An existing conflict is "active" in a given year if any of its dyads produce 25+ deaths |
| **Sub-threshold violence** | Events below 25 deaths per year per dyad are excluded entirely. This systematically undercounts low-intensity, early-stage, or de-escalating conflicts |
| **Calendar year boundary** | If a conflict produces 24 deaths in December and 24 deaths in January, neither year reaches the threshold, even though 48 people died in a 2-month period |
| **Dyad-level counting** | Deaths are counted per dyad, not per conflict. A conflict with 3 dyads could have 24+24+24 = 72 deaths and still not meet the threshold in any single dyad |
| **War threshold** | A separate threshold of 1,000 battle-related deaths per year per conflict defines "war" (major armed conflict) versus lower-intensity "minor" conflicts |

### Battle-Related Deaths — What Counts

UCDP counts **battle-related deaths** specifically:

- **Included:** Combatant deaths in battle, civilians killed in crossfire, targeted killings of civilians by armed actors (one-sided violence), deaths from IEDs and landmines in conflict contexts
- **Excluded:** Deaths from disease, famine, or displacement caused by conflict (indirect deaths); criminal violence not linked to organised armed groups; executions by state in non-conflict contexts; isolated incidents that cannot be linked to a conflict dyad

---

## 14. UCDP Dyad Structure

### What Is a Dyad?

A dyad is a pair of opposing actors in an armed conflict. Every GED event belongs to exactly one dyad.

### Dyad Components

| Component | Description | Example |
|---|---|---|
| **Side A** | Typically the government side. Always includes a state actor in state-based conflicts | "Government of Ethiopia" |
| **Side B** | The opposing side. A rebel group, opposition movement, or another state | "TPLF" (Tigray People's Liberation Front) |
| **Dyad name** | Formatted as "Side A - Side B" | "Government of Ethiopia - TPLF" |
| **Dyad ID** | Unique identifier (post-v5.0 format: `dyad_new_id`) | 418 |

### Types of Dyads

| Conflict Type | Side A | Side B | Example |
|---|---|---|---|
| **State-based: Government vs. rebel** | State government | Non-state armed group | "Government of Colombia - FARC" |
| **State-based: Interstate** | State government | Another state government | "Government of Russia - Government of Ukraine" |
| **Non-state** | Non-state armed group | Another non-state armed group | "ISIS - Al-Nusra Front" |
| **One-sided violence** | State or non-state actor | Civilians (implicit, not named) | "Government of Myanmar" targeting Rohingya civilians |

### Secondary Parties

Secondary warring parties are states that intervene by sending troops to support a primary party. Key rules:
- Secondary parties do **not** create new dyads
- A secondary party does not need to independently cause 25 deaths to be classified as active
- Secondary parties are tracked in the UCDP/PRIO Armed Conflict Dataset and the Dyadic Dataset, but GED events are coded under the primary dyad

### Conflict Hierarchy

```
Conflict (e.g., "Syria: Government")
├── Dyad 1: Government of Syria - Free Syrian Army
│   ├── Event 1 (battle, Aleppo, 2013-02-15, 12 deaths)
│   ├── Event 2 (battle, Homs, 2013-02-16, 8 deaths)
│   └── ...
├── Dyad 2: Government of Syria - ISIS
│   ├── Event 1 (battle, Raqqa, 2014-08-20, 25 deaths)
│   └── ...
└── Dyad 3: Government of Syria - Kurdish YPG
    └── ...
```

### Incompatibility

Each state-based conflict is coded with an "incompatibility" — the stated disputed issue:

| Code | Type | Description |
|---|---|---|
| 1 | Territory | Control over a specific territory (e.g., secession, autonomy) |
| 2 | Government | Control over the central government (regime change, power sharing) |
| 3 | Both | Dispute over both territory and government |

---

## 15. UCDP Candidate Events Dataset

### Purpose

The UCDP Candidate Events Dataset provides **near-real-time** conflict event data, released monthly with approximately 1 month of lag. It serves as an interim dataset before events are incorporated into the annual GED release after full verification.

### Key Characteristics

| Property | Candidate Events | GED (Annual) |
|---|---|---|
| **Release cycle** | Monthly (sometimes quarterly) | Annual |
| **Lag** | ~1 month | ~6-12 months |
| **Verification level** | Preliminary coding, fewer sources | Full verification, multi-source cross-referencing |
| **Coverage** | Most recent 4-18 months | Full 1989-present |
| **Schema** | Identical to GED | Identical to Candidate |
| **Revisions** | Events may be revised or removed in later releases | Considered final within each version |
| **API resource** | `gedevents-candidate` | `gedevents` |

### Candidate Data Quality

According to Hegre et al. (2020, "Introducing the UCDP Candidate Events Dataset"), the candidate data captures **approximately 90% of events** that eventually appear in the final GED, though:
- Some events are merged or split during verification
- Fatality estimates may be revised (typically upward)
- A small proportion (~5-10%) of candidate events are ultimately excluded
- Spatial and temporal precision may improve in the final version

### Access

```python
# Fetch candidate events via API
response = requests.get(
    f"{BASE}/gedevents-candidate/26.0.1",
    headers=headers,
    params={"Country": 530, "pagesize": 100}
)
```

### Relevance to Causal Atlas

The Candidate Events Dataset enables **near-real-time monitoring** — essential for an operational causal analysis system. The recommended approach:

1. Use GED for historical analysis and model training
2. Use Candidate Events for the most recent months
3. When a new GED version is released, replace candidate data with verified GED data
4. Track revisions: compare candidate vs. final GED to quantify measurement uncertainty

---

## 16. UCDP/PRIO Armed Conflict Dataset vs. GED

UCDP produces multiple datasets at different levels of aggregation. Understanding the hierarchy is important:

| Dataset | Unit of Analysis | Temporal Resolution | Coverage | Primary Use |
|---|---|---|---|---|
| **GED (Georeferenced Event Dataset)** | Individual event | Daily | 1989-present | Event-level spatial analysis |
| **UCDP/PRIO Armed Conflict Dataset** | Conflict-year | Yearly | 1946-present | Conflict onset/duration analysis |
| **Dyadic Dataset** | Dyad-year | Yearly | 1946-present | Actor-level analysis |
| **Non-State Conflict Dataset** | Conflict-year | Yearly | 1989-present | Non-state violence trends |
| **One-Sided Violence Dataset** | Actor-year | Yearly | 1989-present | Violence against civilians |
| **Battle-Related Deaths Dataset** | Dyad-year | Yearly | 1989-present | Fatality-focused analysis |
| **Candidate Events Dataset** | Individual event | Daily | Recent months | Near-real-time monitoring |

### UCDP/PRIO Armed Conflict Dataset — Detail

This is the most widely used dataset in conflict studies. It provides **conflict-year** observations:

| Field | Description |
|---|---|
| `conflict_id` | Unique conflict identifier |
| `location` | Countries where the conflict takes place |
| `side_a` | Government side |
| `side_b` | Opposition side(s) |
| `incompatibility` | What the conflict is about (territory, government, or both) |
| `intensity_level` | 1 = minor (25-999 deaths/year), 2 = war (1000+ deaths/year) |
| `type_of_conflict` | 1 = extrasystemic, 2 = interstate, 3 = intrastate, 4 = internationalised intrastate |
| `start_date` | First date the conflict reached 25 deaths |
| `start_date2` | Date of current episode of activity |
| `ep_end` | Whether the conflict ended that year |
| `ep_end_date` | Date of conflict termination |
| `gwno_a` | Gleditsch-Ward number for Side A |
| `gwno_a_2nd` | Second state on Side A (if any) |
| `gwno_b` | Gleditsch-Ward number for Side B (if state) |
| `gwno_b_2nd` | Second state on Side B |
| `gwno_loc` | Country of conflict location |
| `region` | World region |
| `year` | Year of observation |
| `version` | Dataset version |

**Key advantage over GED:** Covers 1946-present (vs. GED's 1989-present), enabling long-run historical analysis of conflict trends, onset patterns, and duration.

**For Causal Atlas:** Use the Armed Conflict Dataset for country-year context (is a conflict active? what type? what intensity?) and GED for spatially disaggregated event analysis at the cell-month level.
