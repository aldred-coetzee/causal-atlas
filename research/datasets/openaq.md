# OpenAQ — Air Quality Data Platform Deep Dive

> Last updated: March 2025

---

## 1. Overview

**OpenAQ** is an environmental technology nonprofit that operates the world's largest open-source, open-access air quality data platform. Founded in 2015, it aggregates and harmonises air quality measurements from government reference-grade monitors and (since 2021) low-cost air sensors worldwide. The platform ingests data from hundreds of data providers — national environmental agencies, research networks, embassy monitors — and exposes it through a unified API.

- **Organisation:** OpenAQ, Inc. (US-based nonprofit)
- **Website:** https://openaq.org/
- **Platform explorer:** https://explore.openaq.org/
- **API documentation:** https://docs.openaq.org/
- **GitHub:** https://github.com/openaq
- **Current API version:** v3 (v2 is deprecated but still accessible)
- **Licence:** Data is aggregated from many providers with varying licences; OpenAQ itself is open-source (MIT for code). See Section 8 for details.

### Mission

"By providing universal access to air quality data, we empower a global community of changemakers to solve air inequality." OpenAQ emphasises that air pollution is the 2nd leading risk factor for death globally, contributing to 8+ million deaths annually (as of 2021 data), and that only 61% of governments produce air quality data.

---

## 2. Coverage

### Spatial

- **Global coverage** with highly uneven density. Dense monitoring networks exist in:
  - United States (EPA AirNow network — thousands of stations)
  - Europe (EEA network)
  - China (national network — 1,000+ stations)
  - India (CPCB network)
  - Parts of Southeast Asia, Latin America, Australia
- **Sparse or absent coverage** in much of sub-Saharan Africa, Central Asia, Pacific Islands, and the Arctic.
- Total: tens of thousands of monitoring locations worldwide (the exact number fluctuates as stations come online and offline).

### Temporal

- **Historical range:** Data from approximately 2015 onward (when OpenAQ began aggregating), though some providers have historical data going back further.
- **Update frequency:** Near real-time for many government monitors (hourly or sub-hourly measurements). Some providers report daily averages.
- **Latency:** Varies by provider — some measurements appear within minutes, others with hours or days of delay.

### Parameters measured

The platform tracks the six criteria air pollutants plus additional parameters:

| Parameter | Chemical | Typical Unit | Health Relevance |
|-----------|----------|-------------|-----------------|
| PM2.5 | Fine particulate matter (<2.5 μm) | μg/m³ | Respiratory, cardiovascular disease, cancer |
| PM10 | Coarse particulate matter (<10 μm) | μg/m³ | Respiratory disease |
| O3 | Ozone | ppm or μg/m³ | Respiratory irritation, crop damage |
| NO2 | Nitrogen dioxide | ppm or μg/m³ | Respiratory disease, acid rain |
| SO2 | Sulfur dioxide | ppm or μg/m³ | Respiratory disease, acid rain |
| CO | Carbon monoxide | ppm or mg/m³ | Cardiovascular, neurological effects |
| BC | Black carbon | μg/m³ | Climate forcing, respiratory |

Additional parameters vary by provider (e.g., PM1, NO, NOx, benzene, toluene).

---

## 3. Access

### 3.1 API v3 (Current)

**Base URL:**
```
https://api.openaq.org/v3/
```

**Authentication:** Required. Register at https://explore.openaq.org to obtain an API key. Include in requests as:
```
X-API-Key: YOUR-OPENAQ-API-KEY
```

**Rate limits:**

| Tier | Per Minute | Per Hour | Notes |
|------|-----------|----------|-------|
| Free | 60 | 2,000 | Default for registered users |
| Custom | Negotiable | Negotiable | Contact platform@openaq.org |

Exceeding limits returns HTTP 429 (Too Many Requests). Repeated violations can result in temporary or permanent bans.

**Rate limit response headers:**

| Header | Description |
|--------|-------------|
| `x-ratelimit-limit` | Maximum requests allowed in current window |
| `x-ratelimit-used` | Requests consumed in current window |
| `x-ratelimit-remaining` | Requests available before hitting limit |
| `x-ratelimit-reset` | Timestamp when counter resets |

### 3.2 Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /v3/locations` | List and search monitoring locations |
| `GET /v3/locations/{id}` | Get details for a specific location |
| `GET /v3/measurements` | Retrieve individual measurements |
| `GET /v3/sensors` | List sensors at locations |
| `GET /v3/parameters` | List available measured parameters |
| `GET /v3/countries` | List countries with data |
| `GET /v3/providers` | List data providers |
| `GET /v3/manufacturers` | List instrument manufacturers |
| `GET /v3/instruments` | List instrument types |
| `GET /v3/licenses` | List data licences by provider |
| `GET /v3/owners` | List station owners |
| `GET /v3/hours` | Hourly aggregated measurements |

### 3.3 Common Query Parameters

#### Pagination
| Parameter | Description | Default | Max |
|-----------|-------------|---------|-----|
| `limit` | Results per page | 100 | 1,000 |
| `page` | Page number | 1 | — |

Response metadata includes:
```json
{
  "meta": {
    "page": 1,
    "limit": 100,
    "found": 16492
  },
  "results": [...]
}
```

#### Location filtering
| Parameter | Description |
|-----------|-------------|
| `coordinates` | Lat/lon centre point for radius search |
| `radius` | Search radius in metres |
| `bbox` | Bounding box (min_lon, min_lat, max_lon, max_lat) |
| `countries_id` | Filter by country ID |
| `providers_id` | Filter by provider ID |
| `parameters_id` | Filter by parameter ID |

#### Temporal filtering
| Parameter | Description |
|-----------|-------------|
| `datetimeFrom` | Start of time range (ISO8601) |
| `datetimeTo` | End of time range (ISO8601) |

**Performance note:** For high-volume endpoints (`/measurements`, `/hours`), the documentation strongly recommends using `datetimeFrom` and `datetimeTo` to narrow queries to one year or less, as this leverages database indexes efficiently.

### 3.4 API v2 (Legacy)

**Base URL:** `https://api.openaq.org/v2/`

Still accessible but deprecated. Endpoint names and response formats differ from v3. New integrations should use v3.

### 3.5 AWS Open Data Archive

OpenAQ provides bulk data access through AWS Open Data:
- **S3 bucket:** Historical archive of all measurements
- Useful for large-scale analyses where API rate limits would be prohibitive
- Format: Parquet files partitioned by date
- Details: https://openaq.org/developers/

### 3.6 Example API Requests

```bash
# Get all locations in Kenya
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.openaq.org/v3/locations?countries_id=113&limit=100"

# Get PM2.5 measurements from a specific location, last month
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.openaq.org/v3/measurements?locations_id=8118&parameters_id=2&datetimeFrom=2025-02-01&datetimeTo=2025-03-01&limit=1000"

# Search locations within 50km of Nairobi
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.openaq.org/v3/locations?coordinates=36.82,-1.29&radius=50000"

# List all available parameters
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.openaq.org/v3/parameters"
```

---

## 4. Schema

### 4.1 Location Object (from `/v3/locations`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique location identifier |
| `name` | String | Station name |
| `locality` | String | City or locality name |
| `timezone` | String | IANA timezone |
| `country` | Object | Country info (id, code, name) |
| `owner` | Object | Station owner info |
| `provider` | Object | Data provider info |
| `isMobile` | Boolean | Whether station is mobile |
| `isMonitor` | Boolean | Whether it's a reference-grade monitor (vs. sensor) |
| `instruments` | Array | Instrument details |
| `sensors` | Array | Sensor details (parameter, unit) |
| `coordinates` | Object | `{latitude, longitude}` in WGS84 |
| `bounds` | Array | Geographic bounds (for mobile stations) |
| `datetimeFirst` | String | First measurement timestamp |
| `datetimeLast` | String | Most recent measurement timestamp |
| `licenses` | Array | Applicable data licences |

### 4.2 Measurement Object (from `/v3/measurements`)

| Field | Type | Description |
|-------|------|-------------|
| `value` | Decimal | Measured value |
| `parameter` | Object | Parameter info (id, name, units) |
| `period` | Object | Measurement period (label, interval, datetimeFrom, datetimeTo) |
| `coordinates` | Object | `{latitude, longitude}` |
| `summary` | Object | Statistical summary if aggregated |
| `coverage` | Object | Data completeness information |

### 4.3 Common Parameter IDs

| ID | Name | Display Name | Unit |
|----|------|-------------|------|
| 1 | pm10 | PM10 | μg/m³ |
| 2 | pm25 | PM2.5 | μg/m³ |
| 3 | o3 | Ozone | ppm |
| 4 | co | Carbon Monoxide | ppm |
| 5 | no2 | Nitrogen Dioxide | ppm |
| 6 | so2 | Sulfur Dioxide | ppm |
| 7 | bc | Black Carbon | μg/m³ |

(IDs may vary; confirm via the `/v3/parameters` endpoint.)

---

## 5. Spatial Detail

- **Point locations.** Each monitoring station has a fixed lat/lon coordinate in WGS84.
- **Mobile stations:** Some stations (e.g., on vehicles) report changing coordinates. The `isMobile` field indicates this. For these, a bounding box (`bounds`) is provided.
- **No gridded output.** OpenAQ provides raw station data, not interpolated grids. Gridding must be done downstream.
- **Station density is extremely uneven.** Urban areas in wealthy countries may have dozens of monitors within a city; entire countries in sub-Saharan Africa may have zero or one.

### PRIO-GRID compatibility

Station-level data must be aggregated to 0.5 x 0.5 degree grid cells. Many grid cells — especially in data-sparse regions — will have no stations at all. Spatial interpolation or satellite-derived alternatives (e.g., Copernicus CAMS, NASA MERRA-2) may be needed to fill gaps.

```python
import math

def station_to_prio_cell(lat, lon):
    """Assign a station to a PRIO-GRID cell."""
    cell_lat = math.floor(lat * 2) / 2
    cell_lon = math.floor(lon * 2) / 2
    return (cell_lat, cell_lon)
```

For cells with multiple stations, compute the mean, median, or population-weighted average of measurements.

---

## 6. Temporal Detail

- **Measurement frequency:** Varies by station and provider:
  - Hourly averages are most common for reference-grade monitors
  - Some stations report sub-hourly (15-minute or 5-minute averages)
  - Some stations report only daily averages
  - Low-cost sensors may report every few minutes
- **Timestamps:** ISO8601, UTC. Each measurement has a `period` defining the averaging window (e.g., 1 hour from/to).
- **Gaps:** Common. Stations go offline for calibration, maintenance, or malfunction. No backfilling is done by OpenAQ.
- **Seasonal patterns:** Air quality data has strong seasonal and diurnal cycles (e.g., winter heating, summer ozone, morning/evening rush hours). Monthly aggregation for Causal Atlas should be aware of these patterns.

### Temporal aggregation for Causal Atlas

- Aggregate to monthly means per station, then to monthly means per PRIO-GRID cell.
- Track measurement count per cell-month to quantify data completeness.
- Consider computing both mean and maximum (for acute pollution episodes).

---

## 7. Quality

### Strengths

- **Standardised and harmonised.** OpenAQ normalises data from disparate providers into a common schema.
- **Reference-grade and sensor data distinguished.** The `isMonitor` flag separates regulatory-grade instruments from low-cost sensors.
- **Large scale.** The largest open air quality dataset available.
- **Active community.** Widely used by researchers, journalists, and advocates.

### Known limitations and biases

- **Spatial coverage bias.** Dense networks in North America, Europe, and East Asia; sparse in Africa, Central Asia, and small island states. This is a fundamental limitation for global analysis.
- **No quality control by OpenAQ.** Data is aggregated as-is from providers. Erroneous values (negative concentrations, stuck sensors, calibration artifacts) are not filtered. Users must apply their own QA/QC.
- **Unit inconsistency.** Some providers report in μg/m³, others in ppm. OpenAQ attempts to normalise but conversions depend on temperature and pressure assumptions.
- **Temporal gaps.** Stations frequently have missing data periods. Coverage metadata is available but must be checked.
- **Low-cost sensor quality.** Sensors (as opposed to reference monitors) have well-documented accuracy issues, especially for PM2.5 in high-humidity environments. Use `isMonitor=true` to restrict to reference-grade data.
- **Provider lag.** Some government networks publish data with days or weeks of delay. "Real-time" means different things for different providers.
- **Historical depth limited.** Most data starts from 2015–2017. Long-term trend analysis requires supplementing with other sources.

### Quality assurance recommendations

1. Filter for `isMonitor=true` when accuracy matters
2. Remove negative values and implausibly high values (e.g., PM2.5 > 1000 μg/m³)
3. Require minimum measurement count per month (e.g., 75% completeness = 540+ hourly readings)
4. Cross-validate against satellite-derived products (e.g., NASA MERRA-2 PM2.5)

---

## 8. Licence

OpenAQ aggregates data from many providers, each with their own licence terms.

- **OpenAQ platform/code:** MIT licence (open source)
- **Data licences:** Vary by provider. OpenAQ's `/v3/licenses` endpoint lists the licence for each data source. Many government datasets are public domain or CC-BY. Some may have restrictions.
- **Attribution:** OpenAQ requests attribution for the platform. Individual data providers may require their own citations.
- **API access:** Free with registration. No commercial restrictions on API use itself, but downstream data licences must be respected.
- **Bulk data on AWS:** Available under the same provider-specific terms.

### Key provider licence examples

| Provider | Licence | Notes |
|----------|---------|-------|
| US EPA (AirNow) | Public domain | US government data |
| EEA (Europe) | Open data, attribution required | |
| CPCB (India) | Generally open | Terms vary |
| China MEE | Public data | Redistribution terms unclear |

Always check the `licenses` field in location responses for the specific terms applicable to each station.

---

## 9. Interoperability

### Shared identifiers

- **Country codes:** OpenAQ uses ISO 3166-1 alpha-2 country codes.
- **Station IDs:** OpenAQ assigns unique integer IDs. Provider-specific station codes are also available, enabling cross-referencing with national databases.
- **No grid assignment built in.** Must be derived from coordinates.

### Integration with other Causal Atlas datasets

| Dataset | Linkage | Notes |
|---------|---------|-------|
| PRIO-GRID | Spatial join by coordinates | Many cells will be empty |
| WHO GBD / IHME | Health outcomes linked to pollution exposure | Key causal chain |
| VIIRS Nightlights | Urbanisation proxy correlated with pollution | |
| ACLED / UCDP | Conflict regions often lack monitors; pollution from conflict (burning, industrial damage) | |
| CHIRPS / Climate | Weather affects pollution dispersion (temperature inversions, wind) | |
| World Bank | GDP per capita correlates with monitoring density and pollution trends | |
| FAO | Agricultural burning is a major PM2.5 source | |

### Complementary air quality data sources

For global gridded coverage (filling OpenAQ's spatial gaps), consider:

| Source | Type | Resolution | Notes |
|--------|------|-----------|-------|
| NASA MERRA-2 | Reanalysis + satellite | 0.5° x 0.625°, hourly | Modeled PM2.5, uses satellite AOD |
| Copernicus CAMS | Reanalysis + forecast | 0.1°–0.75°, hourly | European Centre, global coverage |
| Satellite AOD (MODIS, VIIRS) | Remote sensing | 1 km – 10 km | Aerosol optical depth, proxy for PM2.5 |
| van Donkelaar et al. | Research product | 0.01° | Annual PM2.5 surfaces from satellite + model fusion |

These gridded products can fill the spatial gaps where OpenAQ has no ground stations, while OpenAQ ground truth can validate satellite-derived estimates.

---

## 10. Python Access

### 10.1 Official OpenAQ Python SDK

**Repository:** https://github.com/openaq/openaq-python
**Documentation:** https://python.openaq.org/

**Installation:**
```bash
pip install openaq
```

**Current version:** v0.7.0 (January 2025). Pre-v1.0, under active development. Supports Python 3.10+.

**Features:**
- Synchronous (`OpenAQ`) and asynchronous (`AsyncOpenAQ`) clients
- Comprehensive type annotations
- Deserialized response objects with `.json()` and `.dict()` methods
- Handles authentication and pagination

**Example — get locations in a country:**
```python
from openaq import OpenAQ

client = OpenAQ(api_key="YOUR_API_KEY")

# Get monitoring locations in Kenya
locations = client.locations.list(countries_id=113, limit=100)
for loc in locations.results:
    print(f"{loc.name}: ({loc.coordinates.latitude}, {loc.coordinates.longitude})")

client.close()
```

**Example — get PM2.5 measurements:**
```python
from openaq import OpenAQ

client = OpenAQ(api_key="YOUR_API_KEY")

# Get recent PM2.5 measurements from a location
measurements = client.measurements.list(
    locations_id=8118,
    parameters_id=2,  # PM2.5
    datetime_from="2025-02-01",
    datetime_to="2025-03-01",
    limit=1000
)
for m in measurements.results:
    print(f"{m.period.datetimeFrom}: {m.value} {m.parameter.units}")

client.close()
```

### 10.2 Direct API with requests

```python
import requests
import pandas as pd

API_KEY = "YOUR_API_KEY"
BASE = "https://api.openaq.org/v3"
headers = {"X-API-Key": API_KEY}

# Search for locations near a point
response = requests.get(f"{BASE}/locations", headers=headers, params={
    "coordinates": "36.82,-1.29",  # Nairobi
    "radius": 50000,               # 50km
    "limit": 100
})
locations = response.json()["results"]

# Get measurements for each location
all_measurements = []
for loc in locations:
    resp = requests.get(f"{BASE}/measurements", headers=headers, params={
        "locations_id": loc["id"],
        "parameters_id": 2,  # PM2.5
        "datetimeFrom": "2024-01-01",
        "datetimeTo": "2024-12-31",
        "limit": 1000
    })
    if resp.status_code == 200:
        all_measurements.extend(resp.json()["results"])

df = pd.json_normalize(all_measurements)
print(f"Collected {len(df)} PM2.5 measurements")
```

### 10.3 AWS Open Data (bulk access)

For large-scale analyses, bypass the API entirely:

```python
import pandas as pd

# OpenAQ data on AWS is in Parquet format, partitioned by date
# Example using s3fs or boto3 (requires AWS credentials or public access)
df = pd.read_parquet("s3://openaq-data-archive/records/csv.gz/provider=airnow/...")
```

### 10.4 Recommended approach for Causal Atlas

1. Use the API for targeted queries (specific countries, parameters, time ranges).
2. For global bulk extraction, use the AWS Open Data archive.
3. Filter for `isMonitor=true` to restrict to reference-grade measurements.
4. Aggregate to monthly means per station, then assign to PRIO-GRID cells.
5. Track station count per cell-month for completeness metadata.
6. Supplement with satellite-derived gridded products (MERRA-2, CAMS) for cells without stations.

---

## 11. Relevance to Causal Atlas

### Domain

Air quality / environmental health / pollution.

### Causal chains air quality data can illuminate

1. **Air pollution -> Respiratory and cardiovascular mortality.** The most direct and well-established causal chain. PM2.5 is the most studied pollutant. WHO estimates 4.2 million deaths annually from ambient air pollution. Lag: acute effects within days; chronic effects over years.

2. **Agricultural burning -> PM2.5 spikes -> Health impacts.** Crop residue burning (South/Southeast Asia, sub-Saharan Africa) causes seasonal PM2.5 spikes. Linkable to FAO crop calendars and MODIS fire data. Lag: days.

3. **Urbanisation / industrialisation -> Pollution -> Health burden.** VIIRS nightlights as a proxy for urbanisation, correlated with NO2 and PM2.5 trends. Lag: years.

4. **Conflict -> Industrial destruction -> Pollution spikes.** Bombing of factories, oil facilities, and power plants causes acute pollution events. Linkable to ACLED/UCDP event data. Lag: days.

5. **Climate / meteorology -> Pollution dispersion.** Temperature inversions trap pollutants; wind patterns transport pollution across borders. CHIRPS precipitation data (washout effect) and temperature data are relevant covariates.

6. **Wildfire -> Air quality degradation -> Health / displacement.** Increasingly relevant with climate change. Lag: immediate to weeks.

7. **Economic development -> Vehicle emissions -> Urban NO2.** World Bank GDP growth correlated with fleet size and emission trends.

8. **Air quality -> Property values / economic inequality.** Documented in US and European studies. Environmental justice dimension.

### Key analytical considerations

- Air quality data has strong **seasonality** and **diurnal patterns** that must be accounted for in causal analysis.
- The **spatial coverage gaps** are a serious limitation — precisely the regions of greatest interest for humanitarian analysis (conflict zones, least-developed countries) often lack monitoring.
- **Satellite-derived air quality** (MERRA-2, CAMS) can provide wall-to-wall coverage but with lower accuracy than ground stations.
- For causal analysis, consider using OpenAQ as **ground truth** for calibrating satellite-derived gridded products, then using the gridded products for the actual spatiotemporal modelling.

---

## 12. Sources

- OpenAQ website: https://openaq.org/
- OpenAQ API documentation: https://docs.openaq.org/
- OpenAQ API quick start: https://docs.openaq.org/using-the-api/quick-start
- OpenAQ rate limits: https://docs.openaq.org/using-the-api/rate-limits
- OpenAQ pagination: https://docs.openaq.org/using-the-api/pagination
- OpenAQ Python SDK: https://github.com/openaq/openaq-python (docs: https://python.openaq.org/)
- OpenAQ Explorer: https://explore.openaq.org/
- OpenAQ AWS Open Data: https://registry.opendata.aws/openaq/
- WHO air quality health impacts: https://www.who.int/health-topics/air-pollution
- van Donkelaar et al. (2021), "Monthly Global Estimates of Fine Particulate Matter and Their Uncertainty," *Environmental Science & Technology*, https://doi.org/10.1021/acs.est.1c05309
- MERRA-2 PM2.5: https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/
- Copernicus CAMS: https://atmosphere.copernicus.eu/
- OpenAQ "Why Air Quality" page: https://openaq.org/why-air-quality/
