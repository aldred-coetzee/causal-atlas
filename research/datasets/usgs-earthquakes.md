# USGS Earthquake Hazards Program — Deep Dive

> Last updated: March 2025

---

## 1. Overview

The **USGS Earthquake Hazards Program** (EHP) is operated by the United States Geological Survey as part of the Advanced National Seismic System (ANSS). It maintains the **Comprehensive Earthquake Catalog (ComCat)**, which is the authoritative, publicly accessible database of global earthquake events. ComCat aggregates seismic data from 27+ contributing networks worldwide, including regional US networks (Alaska, California, Hawaii, Nevada, Utah, Pacific Northwest), national centres (USGS National Earthquake Information Center — NEIC), the Pacific Tsunami Warning Center, the International Seismological Centre (ISC-GEM), and the Global CMT project.

The catalog contains earthquake source parameters (hypocentres, magnitudes, phase picks, amplitudes) and derived products including moment tensor solutions, ShakeMaps, PAGER loss estimates, and "Did You Feel It?" (DYFI) community intensity reports.

- **Maintainer:** U.S. Geological Survey, Earthquake Hazards Program
- **Operational since:** Continuous digital records from ~1970s; ComCat contains events back to 1638 with varying completeness
- **Website:** https://earthquake.usgs.gov/
- **Catalog explorer:** https://earthquake.usgs.gov/earthquakes/search/

---

## 2. Coverage

### Spatial

- **Global coverage.** ANSS and partner networks detect and locate earthquakes worldwide.
- Completeness varies by region: in the continental US, events down to ~M2.0 are reliably catalogued; globally, completeness is approximately M4.0–4.5+.
- Dense station coverage in the US, Japan, Europe, and parts of South America. Sparser in Africa, Central Asia, and deep ocean basins.

### Temporal

- **Historical range:** 1638 to present (early records extremely sparse)
- **Modern instrumental era:** 1970s onward, with significant improvements in detection around 2000+
- **Update frequency:** Real-time feeds update **every minute**. Individual events may be revised for days/weeks after occurrence as additional data arrive and human review occurs.
- **Latency:** Automatic detections appear within minutes; reviewed solutions within hours to days.

---

## 3. Access

### 3.1 FDSN Event Web Service API (Primary Programmatic Access)

**Base URL:**
```
https://earthquake.usgs.gov/fdsnws/event/1/
```

**Endpoints:**

| Endpoint | Purpose |
|----------|---------|
| `/query` | Search and retrieve earthquake data |
| `/count` | Count matching events (same parameters as query) |
| `/catalogs` | List available earthquake catalogs |
| `/contributors` | List available data contributors |
| `/version` | Service version number |
| `/application.json` | Enumerated parameter values |
| `/application.wadl` | WADL interface description |

**Output formats:**

| Format | Content-Type | Notes |
|--------|-------------|-------|
| `geojson` | application/json | Most useful for programmatic access |
| `csv` | text/csv | Flat tabular, good for bulk analysis |
| `quakeml` (default) | application/xml | QuakeML 1.2, richest metadata |
| `kml` | vnd.google-earth.kml+xml | For Google Earth visualisation |
| `text` | text/plain | Plain text |

**Query parameters (comprehensive):**

#### Time filters (ISO8601 format, UTC)
| Parameter | Range/Type | Default | Notes |
|-----------|-----------|---------|-------|
| `starttime` | ISO8601 datetime | NOW - 30 days | |
| `endtime` | ISO8601 datetime | NOW | |
| `updatedafter` | ISO8601 datetime | — | Events modified after this time |

#### Location — Rectangle
| Parameter | Range | Default |
|-----------|-------|---------|
| `minlatitude` | [-90, 90] | -90 |
| `maxlatitude` | [-90, 90] | 90 |
| `minlongitude` | [-360, 360] | -180 |
| `maxlongitude` | [-360, 360] | 180 |

Date line crossing: set `minlongitude < -180` or `maxlongitude > 180`.

#### Location — Circle (all three required together)
| Parameter | Range | Default |
|-----------|-------|---------|
| `latitude` | [-90, 90] | — |
| `longitude` | [-180, 180] | — |
| `maxradius` | [0, 180] degrees | 180 |
| `maxradiuskm` | [0, 20001.6] km | 20001.6 |

`maxradius` and `maxradiuskm` are mutually exclusive. When both rectangle and circle are specified, the intersection is returned.

#### Magnitude and depth
| Parameter | Range | Default |
|-----------|-------|---------|
| `minmagnitude` | decimal | — |
| `maxmagnitude` | decimal | — |
| `mindepth` | [-100, 1000] km | -100 |
| `maxdepth` | [-100, 1000] km | 1000 |

#### Event selection
| Parameter | Type | Notes |
|-----------|------|-------|
| `eventid` | string | Specific event; implies all origins/magnitudes |
| `catalog` | string | Filter by catalog source |
| `contributor` | string | Filter by data contributor |
| `includeallorigins` | boolean | Default false |
| `includeallmagnitudes` | boolean | Default false |
| `includedeleted` | boolean/"only" | Default false |
| `includesuperseded` | boolean | Default false (only with eventid) |
| `reviewstatus` | `automatic` / `reviewed` / `all` | Default: all |
| `eventtype` | string | e.g., "earthquake" excludes non-earthquake events |

#### Pagination and ordering
| Parameter | Range | Default |
|-----------|-------|---------|
| `limit` | [1, 20000] | — |
| `offset` | [1, infinity] | 1 |
| `orderby` | `time` / `time-asc` / `magnitude` / `magnitude-asc` | time |

**Hard limit: 20,000 results per query.** Exceeding this returns HTTP 400. For larger extractions, split by time or region.

#### PAGER alert levels
| Parameter | Values |
|-----------|--------|
| `alertlevel` | green / yellow / orange / red |
| `minalertlevel` | green / yellow / orange / red |
| `maxalertlevel` | green / yellow / orange / red |

#### Intensity and felt reports
| Parameter | Range | Notes |
|-----------|-------|-------|
| `maxmmi` | [0, 12] | Modified Mercalli Intensity |
| `mincdi` / `maxcdi` | [0, 12] | Community Determined Intensity (DYFI) |
| `minfelt` | [1, inf] | Minimum DYFI felt report count |

#### Quality metrics
| Parameter | Range |
|-----------|-------|
| `mingap` / `maxgap` | [0, 360] degrees (azimuthal gap) |
| `minsig` / `maxsig` | integer (significance) |

#### Product and format filters
| Parameter | Notes |
|-----------|-------|
| `producttype` | moment-tensor, focal-mechanism, shakemap, losspager, dyfi |
| `productcode` | Specific product code |
| `callback` | JSONP callback (geojson only) |
| `jsonerror` | Return errors as JSON (geojson only) |
| `kmlanimated` | Include timestamps for animation (kml only) |
| `kmlcolorby` | `age` (default) or `depth` (kml only) |
| `nodata` | 204 (default) or 404 when no results |

**Example queries:**

```bash
# All M5+ earthquakes in the last 30 days (GeoJSON)
curl "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=5"

# Earthquakes in East Africa bounding box, 2020-2023, CSV
curl "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2020-01-01&endtime=2023-12-31&minlatitude=-12&maxlatitude=15&minlongitude=25&maxlongitude=52"

# Count of M4+ events near a point (500km radius)
curl "https://earthquake.usgs.gov/fdsnws/event/1/count?latitude=28.2&longitude=84.7&maxradiuskm=500&minmagnitude=4"
```

### 3.2 Real-Time GeoJSON Feeds

Pre-generated feeds updated every minute, optimized for high-traffic applications. USGS recommends these over the query API for real-time display.

**Base URL:** `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/`

| Feed | URL fragment | Content |
|------|-------------|---------|
| Significant, Past Hour | `significant_hour.geojson` | USGS-selected significant events |
| M4.5+, Past Day | `4.5_day.geojson` | Moderate+ earthquakes, last 24h |
| M2.5+, Past Day | `2.5_day.geojson` | Light+ earthquakes, last 24h |
| M1.0+, Past Day | `1.0_day.geojson` | Minor+ earthquakes, last 24h |
| All, Past Day | `all_day.geojson` | All detected events, last 24h |
| M4.5+, Past 7 Days | `4.5_week.geojson` | Moderate+ earthquakes, last week |
| M2.5+, Past 7 Days | `2.5_week.geojson` | Light+ earthquakes, last week |
| All, Past 30 Days | `all_month.geojson` | All detected events, last month |

Time periods available: `hour`, `day`, `week`, `month`. Magnitude thresholds: `significant`, `4.5`, `2.5`, `1.0`, `all`.

### 3.3 Rate Limits and Authentication

- **No authentication required.** Fully public API.
- **No documented hard rate limits.** However, USGS asks that automated applications prefer the real-time feeds where possible. The 20,000-result cap per query is the main constraint.
- **Contact for heavy usage:** gs-haz_dev_team_group@usgs.gov
- **Recommended practice:** Use feeds for display applications; use the query API for research extractions.

### 3.4 Bulk Download

Full ComCat extractions can be performed via the query API by splitting into time windows (to stay under the 20,000 limit). The `libcomcat` Python library automates this splitting. QuakeML files for individual events are also downloadable via the detail endpoint.

---

## 4. Schema

### 4.1 CSV / GeoJSON Property Fields

| Field | Type | Description |
|-------|------|-------------|
| `time` | Long (ms since epoch) | Origin time of event (UTC) |
| `latitude` | Decimal | Hypocentre latitude, WGS84, degrees |
| `longitude` | Decimal | Hypocentre longitude, WGS84, degrees |
| `depth` | Decimal (km) | Depth below surface in kilometres |
| `mag` | Decimal | Preferred magnitude value |
| `magType` | String | Magnitude type: ml, mb, mw, mww, mwc, mwr, ms, md, etc. |
| `nst` | Integer | Number of seismic stations used |
| `gap` | Decimal (degrees) | Largest azimuthal gap between stations |
| `dmin` | Decimal (degrees) | Distance to nearest station |
| `rms` | Decimal (seconds) | Root mean square travel time residual |
| `net` | String | Network ID (e.g., us, ci, ak, nc) |
| `id` | String | Unique event identifier (e.g., `us7000abcd`) |
| `updated` | Long (ms since epoch) | Last modification time |
| `place` | String | Textual location description (e.g., "15 km NNE of Ridgecrest, CA") |
| `type` | String | Event type: earthquake, quarry blast, explosion, etc. |
| `horizontalError` | Decimal (km) | Horizontal location uncertainty |
| `depthError` | Decimal (km) | Depth uncertainty |
| `magError` | Decimal | Magnitude uncertainty |
| `magNst` | Integer | Number of stations used for magnitude |
| `status` | String | `automatic` or `reviewed` |
| `locationSource` | String | Network that computed the location |
| `magSource` | String | Network that computed the magnitude |

### 4.2 Additional GeoJSON-only fields

| Field | Type | Description |
|-------|------|-------------|
| `felt` | Integer | Number of DYFI felt reports |
| `cdi` | Decimal | Maximum Community Determined Intensity (DYFI) |
| `mmi` | Decimal | Maximum Modified Mercalli Intensity (ShakeMap) |
| `alert` | String | PAGER alert level: green, yellow, orange, red |
| `tsunami` | Integer | 1 if tsunami advisory issued, 0 otherwise |
| `sig` | Integer | Significance (0–1000+), composite score from magnitude, felt reports, PAGER |
| `ids` | String | Comma-delimited list of all associated event IDs |
| `sources` | String | Comma-delimited list of contributing network codes |
| `types` | String | Comma-delimited list of available product types |
| `code` | String | Event code portion of the ID |
| `tz` | Integer | Timezone offset in minutes from UTC |
| `url` | String | Link to USGS event page |
| `detail` | String | URL to detailed GeoJSON for this event |
| `products` | Object | (detail format only) Full product content including ShakeMap, PAGER, moment tensors |

### 4.3 Magnitude types

| Code | Name | Typical range |
|------|------|---------------|
| `ml` | Local (Richter) | <4 |
| `mb` | Body wave | 4–7 |
| `ms` | Surface wave | 5–8 |
| `mw` | Moment magnitude (generic) | 3.5+ |
| `mww` | W-phase moment magnitude | 5.5+ |
| `mwc` | Centroid moment magnitude | 5+ |
| `mwr` | Regional moment magnitude | 3.5–6 |
| `md` | Duration magnitude | <4 |

### 4.4 Sample GeoJSON Feature

```json
{
  "type": "Feature",
  "properties": {
    "mag": 6.2,
    "place": "45 km NE of Antakya, Turkey",
    "time": 1675728000000,
    "updated": 1675900000000,
    "tz": null,
    "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000jllz",
    "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us6000jllz&format=geojson",
    "felt": 1520,
    "cdi": 8.5,
    "mmi": 8.1,
    "alert": "red",
    "status": "reviewed",
    "tsunami": 1,
    "sig": 890,
    "net": "us",
    "code": "6000jllz",
    "ids": ",us6000jllz,at00s0zfkz,",
    "sources": ",us,at,",
    "types": ",dyfi,focal-mechanism,losspager,moment-tensor,origin,phase-data,shakemap,",
    "nst": 120,
    "dmin": 0.8,
    "rms": 0.85,
    "gap": 25,
    "magType": "mww",
    "type": "earthquake",
    "horizontalError": 4.2,
    "depthError": 3.1,
    "magError": 0.04,
    "magNst": 85,
    "locationSource": "us",
    "magSource": "us"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [36.95, 36.75, 10.0]
  },
  "id": "us6000jllz"
}
```

---

## 5. Spatial Detail

- **Point locations.** Each event is a lat/lon/depth point (WGS84).
- **Coordinates in GeoJSON geometry:** `[longitude, latitude, depth_km]` (note: GeoJSON convention is lon/lat, not lat/lon).
- **Precision:** Horizontal uncertainty reported in `horizontalError` (km). Varies from <1 km in dense networks to 10+ km in sparse regions.
- **Depth:** In kilometres below surface. Uncertainty in `depthError`. Many events have depth fixed at default values (e.g., 10 km, 33 km) when poorly constrained.
- **Location descriptions:** The `place` field provides human-readable text (e.g., "15 km NNE of Ridgecrest, CA") but this is derived from coordinates, not the primary spatial data.

### PRIO-GRID compatibility

Earthquake point coordinates can be directly assigned to PRIO-GRID 0.5 x 0.5 degree cells using simple floor division:

```python
prio_lat = int(latitude * 2) / 2  # round to nearest 0.5 degree edge
prio_lon = int(longitude * 2) / 2
```

For Causal Atlas, aggregation to grid cells will involve counting events per cell-month and computing summary statistics (max magnitude, total energy release, event count).

---

## 6. Temporal Detail

- **Timestamp resolution:** Milliseconds (Unix epoch in the `time` field).
- **Origin time accuracy:** Sub-second for well-recorded events; seconds to minutes for historical events.
- **Event duration:** Not recorded — earthquakes are treated as instantaneous point events (the `time` field is the origin time).
- **Update cycle:** Events are initially reported automatically within minutes, then revised by analysts (status changes from `automatic` to `reviewed`). The `updated` field tracks the latest revision.
- **Feed update frequency:** Every minute for real-time feeds.
- **Historical data:** Available back to 1638, but pre-1900 events are sparse and uncertainties are very large. The modern digital era (post-1970s) has the most reliable and complete data.

### Temporal aggregation for Causal Atlas

Monthly aggregation is natural: count events per PRIO-GRID cell per month, with derived columns for max magnitude, total seismic moment, and count by magnitude bin. Daily resolution is available for event-level analysis.

---

## 7. Quality

### Strengths

- **Authoritative and well-maintained.** USGS/ANSS is the gold standard for seismic data.
- **Rapid availability.** Events appear within minutes of occurrence.
- **Human review.** Significant events receive analyst review; `status` field distinguishes automatic from reviewed.
- **Rich metadata.** Uncertainty estimates, station counts, azimuthal gaps — all included.
- **Products ecosystem.** ShakeMap, PAGER, DYFI provide additional impact information beyond the basic catalog.

### Known limitations and biases

- **Magnitude of completeness varies by region.** The global catalog is approximately complete above M4.5, but in poorly instrumented regions (parts of Africa, Central Asia, deep oceans) the threshold is higher. In the US, completeness is down to ~M2.0.
- **Detection network bias.** Events in densely instrumented areas are located more precisely. Remote regions may have horizontal errors of 20+ km.
- **Depth defaults.** When depth is poorly constrained, it is often fixed at canonical values (10 km for shallow, 33 km for "normal") rather than estimated. Check `depthError` — if missing or very large, the depth is unreliable.
- **Non-earthquake contamination.** ComCat includes quarry blasts, mine collapses, nuclear explosions, and other non-tectonic events. Filter using `type=earthquake` or `eventtype=earthquake` to exclude these.
- **Historical catalog incompleteness.** Pre-1970 data has significant gaps. Pre-1900 data is sparse and unreliable for statistical analysis.
- **Magnitude type mixing.** Different events may use different magnitude scales (ml, mb, mw). Mixing scales introduces inconsistency. For research, prefer moment magnitude (mw, mww) and apply magnitude conversion formulas where needed.
- **Aftershock clustering.** Large earthquakes trigger thousands of aftershocks that dominate event counts. Statistical analyses should consider declustering (removing aftershocks) for certain use cases.

### Validation

- ComCat is cross-referenced with the ISC bulletin, GCMT catalog, and regional network bulletins.
- The ISC-GEM catalog provides a reviewed, homogeneous reference for M5.5+ events since 1900.

---

## 8. Licence

- **Public domain.** USGS data produced by the US federal government is not subject to copyright in the United States and is freely available globally.
- **No authentication required.** No API key, no registration.
- **No commercial restrictions.** Can be used for any purpose.
- **Attribution requested:** USGS requests citation when using their data in publications. Suggested citation format is available at https://earthquake.usgs.gov/data/comcat/.
- **Citation DOI for libcomcat:** https://doi.org/10.5066/P91WN1UQ

---

## 9. Interoperability

### Shared identifiers

- **Event IDs** are unique strings (e.g., `us7000abcd`). Prefix indicates the contributing network.
- Events may have multiple IDs from different networks, listed in the `ids` field (comma-delimited). The USGS "preferred" ID is used as the canonical reference.
- No direct linkage to ACLED, UCDP, or other social/conflict datasets — must be joined via spatiotemporal proximity.

### Grid compatibility

- Point coordinates are easily mappable to any grid system (PRIO-GRID, H3, S2, admin boundaries).
- No built-in admin-region coding — must be derived from coordinates using a reverse-geocoding step or spatial join.

### Related USGS products

- **ShakeMap** provides interpolated ground-shaking intensity grids (GeoTIFF, shapefiles) — already gridded data useful for impact estimation.
- **PAGER** provides estimated population exposure and economic loss by shaking intensity level.
- **DYFI** provides crowd-sourced intensity reports with individual location data.

### Integration with other Causal Atlas datasets

- **EM-DAT:** EM-DAT records earthquake disasters; can be cross-referenced by time/location for events that caused significant damage.
- **ACLED / UCDP:** No direct link, but earthquake-affected regions can be analysed for subsequent conflict patterns.
- **World Bank / FAO:** Post-earthquake economic and agricultural impacts.
- **VIIRS Nightlights:** Pre/post-earthquake nightlight changes as a proxy for economic disruption and recovery.

---

## 10. Python Access

### 10.1 libcomcat (official USGS library)

**Repository:** https://code.usgs.gov/ghsc/esi/libcomcat-python (migrated from GitHub)

**Installation:**
```bash
pip install usgs-libcomcat
```

**Key features:**
- Python wrapper around the ComCat FDSN API
- Handles automatic splitting of large queries that exceed the 20,000-event limit
- Downloads derived products (ShakeMaps, moment tensors, phase data)
- Seven command-line tools: `findid`, `getcsv`, `geteventhist`, `getmags`, `getpager`, `getphases`, `getproduct`
- Jupyter notebook tutorials included

**Example — search and retrieve:**
```python
from libcomcat.search import search, get_event_by_id
from libcomcat.dataframes import get_summary_data_frame
from datetime import datetime

# Search for M5+ events in East Africa, 2020
events = search(
    starttime=datetime(2020, 1, 1),
    endtime=datetime(2020, 12, 31),
    minlatitude=-12, maxlatitude=15,
    minlongitude=25, maxlongitude=52,
    minmagnitude=5.0
)

# Convert to pandas DataFrame
df = get_summary_data_frame(events)
print(df[['time', 'latitude', 'longitude', 'magnitude', 'depth']].head())
```

**Example — get detailed event info:**
```python
detail = get_event_by_id("us6000jllz")
print(detail.magnitude, detail.latitude, detail.longitude)
print(detail.hasProduct("shakemap"))  # True/False
```

**Command-line usage:**
```bash
# Download CSV of M4+ events for a region/time
getcsv -b 25 52 -12 15 -s 2020-01-01 -e 2023-12-31 -m 4.0 9.0 -o east_africa_quakes.csv

# Get PAGER results for an event
getpager us6000jllz -o pager_output/
```

### 10.2 ObsPy

**Installation:**
```bash
pip install obspy
```

ObsPy is a comprehensive seismology toolkit that includes an FDSN client for querying ComCat. It returns data as ObsPy `Catalog` objects (QuakeML-based), which is useful for seismological analysis but heavier than needed for simple event retrieval.

```python
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

client = Client("USGS")
cat = client.get_events(
    starttime=UTCDateTime("2020-01-01"),
    endtime=UTCDateTime("2020-12-31"),
    minmagnitude=5.0,
    minlatitude=-12, maxlatitude=15,
    minlongitude=25, maxlongitude=52
)
print(f"Found {len(cat)} events")
for event in cat[:5]:
    origin = event.preferred_origin()
    mag = event.preferred_magnitude()
    print(f"{origin.time} M{mag.mag} ({origin.latitude}, {origin.longitude})")
```

### 10.3 Direct API with requests

For simple use cases, direct HTTP requests are straightforward:

```python
import requests
import pandas as pd
from io import StringIO

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {
    "format": "csv",
    "starttime": "2020-01-01",
    "endtime": "2023-12-31",
    "minmagnitude": 4.0,
    "minlatitude": -12, "maxlatitude": 15,
    "minlongitude": 25, "maxlongitude": 52,
    "orderby": "time",
    "limit": 20000
}
response = requests.get(url, params=params)
df = pd.read_csv(StringIO(response.text))
print(df.shape)
print(df.columns.tolist())
```

### 10.4 Recommended approach for Causal Atlas

Use `libcomcat` for bulk historical data extraction (it handles the 20,000-event pagination automatically). For ongoing ingestion, poll the real-time GeoJSON feeds (`all_day.geojson`) every few minutes. Convert to a standardised schema and assign PRIO-GRID cell IDs during ingestion.

---

## 11. Relevance to Causal Atlas

### Domain

Seismic events / natural disasters / geophysical hazards.

### Causal chains earthquakes can illuminate

1. **Earthquake -> Displacement -> Humanitarian crisis.** Major earthquakes trigger population displacement, camp formation, and aid dependency. Lag: days to weeks.

2. **Earthquake -> Infrastructure destruction -> Economic decline.** VIIRS nightlights and World Bank GDP data can capture post-earthquake economic impact. Lag: weeks to months.

3. **Earthquake -> Agricultural disruption -> Food insecurity.** Ground deformation, irrigation damage, and rural displacement affect agricultural output. Lag: months (one growing season).

4. **Earthquake -> Health system disruption -> Disease outbreaks.** Destruction of hospitals and water systems leads to waterborne disease. Lag: weeks.

5. **Earthquake -> Political instability.** Poorly managed disaster response has historically contributed to political unrest and regime instability (e.g., Haiti 2010, Iran 2003). Lag: months to years.

6. **Earthquake -> Tsunami -> Coastal devastation.** The `tsunami` flag identifies events with tsunami potential. Lag: minutes to hours (the tsunami itself), but cascading effects over months.

7. **Seismic swarms -> Volcanic activity -> Climate effects.** Earthquake clusters can indicate volcanic unrest, with potential ash/SO2 emissions affecting regional climate and air quality.

### Integration priority

Earthquakes are episodic, high-impact events. For Causal Atlas, the primary analytical approach is:
- **Event-triggered analysis:** When a significant earthquake occurs in a PRIO-GRID cell, examine time series of other indicators (food prices, conflict events, nightlights, displacement) in that cell and neighbours for pre/post changes.
- **Monthly aggregation:** For statistical modelling (Granger causality, transfer entropy), aggregate to event counts and max magnitudes per cell-month.

### Complementary datasets

| Dataset | Relationship to earthquake data |
|---------|-------------------------------|
| EM-DAT | Disaster-level impact records (deaths, damage, affected population) |
| VIIRS Nightlights | Pre/post economic proxy |
| WFP Food Prices | Post-earthquake food price spikes |
| ACLED / UCDP | Post-disaster conflict and unrest |
| HDX HAPI | Displacement and humanitarian needs |
| CHIRPS | Context — was drought already affecting the region? |

---

## 12. Sources

- USGS Earthquake Hazards Program: https://earthquake.usgs.gov/
- FDSN Event Web Service documentation: https://earthquake.usgs.gov/fdsnws/event/1/
- ComCat documentation: https://earthquake.usgs.gov/data/comcat/index.php
- ComCat event terms (field definitions): https://earthquake.usgs.gov/data/comcat/data-eventterms.php
- GeoJSON feed documentation: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
- CSV feed documentation: https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php
- libcomcat Python library: https://code.usgs.gov/ghsc/esi/libcomcat-python (DOI: https://doi.org/10.5066/P91WN1UQ)
- ObsPy FDSN client: https://docs.obspy.org/packages/obspy.clients.fdsn.html
- ANSS networks: https://earthquake.usgs.gov/monitoring/anss/
- Real-time feeds: https://earthquake.usgs.gov/earthquakes/feed/
- USGS contact for API issues: gs-haz_dev_team_group@usgs.gov
