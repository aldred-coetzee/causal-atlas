# FIRMS — Fire Information for Resource Management System

> **Last reviewed:** March 2025
> **Status:** Active, near-real-time (3-hour latency globally, real-time for US/Canada)
> **Website:** https://firms.modaps.eosdis.nasa.gov

---

## 1. Overview

The Fire Information for Resource Management System (FIRMS) is operated by NASA's Land, Atmosphere Near real-time Capability for EOS (LANCE) and distributes active fire detection data from the MODIS and VIIRS satellite instruments. FIRMS provides global fire detection data in near-real-time with approximately 3-hour latency from satellite observation, making it one of the most timely and widely-used fire monitoring datasets available.

For Causal Atlas, FIRMS is critical because fire data intersects multiple causal domains: agricultural burning affects air quality and health outcomes, conflict-related arson creates detectable signals, deforestation fires contribute to climate change, and wildfire patterns respond to drought and climate conditions. FIRMS data is used extensively by organisations including FEWS NET, the Bellingcat investigative journalism network, Amazon deforestation monitoring programmes, and African agricultural monitoring systems.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Operator | NASA LANCE / EOSDIS |
| Instruments | MODIS (Terra + Aqua), VIIRS (Suomi NPP, NOAA-20, NOAA-21) |
| Detection type | Thermal anomaly (active fire / hotspot) |
| Latency | ~3 hours (global NRT), real-time (US/Canada) |
| MODIS resolution | 1 km (at nadir) |
| VIIRS resolution | 375 m (I-Band) |
| MODIS archive | November 2000 - present (Collection 6.1) |
| VIIRS S-NPP archive | January 2012 - present |
| VIIRS NOAA-20 archive | January 2020 - present |
| VIIRS NOAA-21 archive | 2023 - present |
| Output formats | CSV, SHP, KML, JSON, GeoJSON |
| Cost | Free |
| API | REST API with MAP_KEY authentication |

### Active fire vs burned area products

FIRMS provides two fundamentally different types of fire information:

| Product | Type | Spatial resolution | Temporal | What it detects |
|---------|------|-------------------|----------|-----------------|
| **MCD14ML** (MODIS active fire) | Point detections | 1 km | Per-overpass (~4x/day) | Fires burning at time of satellite overpass |
| **VNP14IMG** (VIIRS S-NPP active fire) | Point detections | 375 m | Per-overpass | Fires burning at time of satellite overpass |
| **VJ114IMG** (VIIRS NOAA-20 active fire) | Point detections | 375 m | Per-overpass | Fires burning at time of satellite overpass |
| **VJ214IMG** (VIIRS NOAA-21 active fire) | Point detections | 375 m | Per-overpass | Fires burning at time of satellite overpass |
| **MCD64A1** (MODIS burned area) | Gridded monthly | 500 m | Monthly | Cumulative area burned during month |

**Key distinction:** Active fire detections are snapshots — they only detect fires burning at the exact moment of satellite overpass. Short-duration fires or those obscured by clouds are missed. The burned area product (MCD64A1) captures the cumulative footprint but at monthly temporal resolution and with a delay.

---

## 2. Spatial Coverage and Resolution

### Global coverage

- **MODIS:** Global coverage from Terra (10:30 AM/PM equatorial crossing) and Aqua (1:30 PM/AM equatorial crossing) satellites
- **VIIRS:** Global coverage from Suomi NPP (1:30 PM/AM), NOAA-20 (1:30 PM/AM, offset orbit), and NOAA-21
- Combined instruments provide multiple observations per day at most locations

### Spatial resolution

| Instrument | Pixel size at nadir | Pixel size at scan edge | Swath width |
|------------|--------------------|-----------------------|-------------|
| MODIS | 1 km | Up to 2 km | 2,330 km |
| VIIRS (I-Band) | 375 m | ~750 m | 3,060 km |

**VIIRS advantages over MODIS:**
- 375 m resolution detects smaller fires (1/7th the area)
- Better response over relatively small fire areas
- Improved nighttime performance
- Fewer pixel growth artefacts at scan edges
- Wider swath means fewer coverage gaps

### Detection coordinates

Fire detections are reported as point locations (latitude/longitude of pixel centre), not polygons. The actual fire could be anywhere within the pixel footprint.

---

## 3. Temporal Coverage and Resolution

| Source | Start date | Temporal resolution | Latency (NRT) |
|--------|-----------|--------------------|-|
| MODIS Terra (MOD14) | Nov 2000 | Per-overpass (~2x/day) | ~3 hours |
| MODIS Aqua (MYD14) | Jul 2002 | Per-overpass (~2x/day) | ~3 hours |
| VIIRS S-NPP (VNP14IMG) | Jan 2012 | Per-overpass (~2x/day) | ~3 hours |
| VIIRS NOAA-20 (VJ114IMG) | Jan 2020 | Per-overpass (~2x/day) | ~3 hours |
| VIIRS NOAA-21 (VJ214IMG) | 2023 | Per-overpass (~2x/day) | ~3 hours |
| MCD64A1 burned area | Nov 2000 | Monthly | ~2 months |

### NRT vs Standard (Science Quality) data

- **NRT (Near Real-Time):** Available within ~3 hours; uses predicted satellite ephemeris; suitable for monitoring
- **Standard (Science Quality):** Available with ~2-month delay; uses definitive ephemeris; better geolocation; recommended for research
- Product identifiers have `_NRT` suffix for near-real-time data

---

## 4. Data Access Methods

### Method 1: FIRMS REST API (Primary)

**Registration:**
1. Create a free NASA Earthdata account at https://urs.earthdata.nasa.gov
2. Request a MAP_KEY at https://firms.modaps.eosdis.nasa.gov/api/map_key/
3. MAP_KEY is emailed immediately

**Rate limit:** 5,000 transactions per 10-minute interval

**API endpoints:**

| Endpoint | URL pattern | Description |
|----------|------------|-------------|
| Area (CSV) | `https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA}/{DAYS}` | Fire data for bounding box |
| Area (JSON) | `.../api/area/json/{MAP_KEY}/{SOURCE}/{AREA}/{DAYS}` | Same, JSON format |
| Country (CSV) | `.../api/country/csv/{MAP_KEY}/{SOURCE}/{COUNTRY_CODE}/{DAYS}` | Fire data by country (ISO3) |
| Data availability | `.../api/data_availability/csv/{MAP_KEY}/{SOURCE}` | Check available date range |

**Source codes:**

| Code | Description |
|------|-------------|
| `MODIS_NRT` | MODIS NRT (Combined Terra + Aqua) |
| `MODIS_SP` | MODIS Standard Processing |
| `VIIRS_SNPP_NRT` | VIIRS S-NPP NRT |
| `VIIRS_SNPP_SP` | VIIRS S-NPP Standard |
| `VIIRS_NOAA20_NRT` | VIIRS NOAA-20 NRT |
| `VIIRS_NOAA21_NRT` | VIIRS NOAA-21 NRT |

**Day range:** 1-10 for NRT data. For historical data, append `/{DATE}` in YYYY-MM-DD format.

### Method 2: Archive download

Full archive downloads available at https://firms.modaps.eosdis.nasa.gov/download/ in CSV, SHP, and KML formats, organised by:
- Global files (entire globe for a date range)
- Country-level files
- Annual summaries

### Method 3: Google Earth Engine

FIRMS is available in GEE as:
- `FIRMS` — MODIS Collection 6 active fire data
- Community catalogue includes VIIRS and MODIS vector data (https://gee-community-catalog.org/projects/firms_vector/)

### Method 4: Direct HTTPS download

NRT files updated continuously at:
```
https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/
https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/
https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/
```

---

## 5. Schema and Data Fields

### MODIS active fire fields (MCD14ML / MCD14DL)

| Field | Type | Description |
|-------|------|-------------|
| `latitude` | float | Centre of 1 km fire pixel |
| `longitude` | float | Centre of 1 km fire pixel |
| `brightness` | float | Brightness temperature (K) in channel 21/22 (3.9 μm) |
| `scan` | float | Along-scan pixel size (km) |
| `track` | float | Along-track pixel size (km) |
| `acq_date` | string | Acquisition date (YYYY-MM-DD) |
| `acq_time` | string | Acquisition time (HHMM UTC) |
| `satellite` | string | "Terra" or "Aqua" |
| `instrument` | string | "MODIS" |
| `confidence` | integer | Detection confidence (0-100%) |
| `version` | string | Collection/version (e.g., "6.1NRT") |
| `bright_t31` | float | Brightness temperature (K) in channel 31 (11 μm) |
| `frp` | float | Fire Radiative Power (MW) |
| `daynight` | string | "D" (day) or "N" (night) |

### VIIRS active fire fields (VNP14IMG / VJ114IMG)

| Field | Type | Description |
|-------|------|-------------|
| `latitude` | float | Centre of 375 m fire pixel |
| `longitude` | float | Centre of 375 m fire pixel |
| `bright_ti4` | float | Brightness temperature (K) in I-4 channel (3.7 μm) |
| `scan` | float | Along-scan pixel size (km) |
| `track` | float | Along-track pixel size (km) |
| `acq_date` | string | Acquisition date (YYYY-MM-DD) |
| `acq_time` | string | Acquisition time (HHMM UTC) |
| `satellite` | string | "N" (S-NPP), "1" (NOAA-20), "2" (NOAA-21) |
| `instrument` | string | "VIIRS" |
| `confidence` | string | "low", "nominal", or "high" |
| `version` | string | Collection/version (e.g., "2.0NRT") |
| `bright_ti5` | float | Brightness temperature (K) in I-5 channel (11.4 μm) |
| `frp` | float | Fire Radiative Power (MW) |
| `daynight` | string | "D" (day) or "N" (night) |
| `type` | integer | 0 = presumed vegetation fire, 1 = active volcano, 2 = other static land source, 3 = offshore detection |

### Key field differences: MODIS vs VIIRS

| Field | MODIS | VIIRS |
|-------|-------|-------|
| Brightness channel | `brightness` (Ch 21/22, 3.9 μm) | `bright_ti4` (I-4, 3.7 μm) |
| Secondary channel | `bright_t31` (Ch 31, 11 μm) | `bright_ti5` (I-5, 11.4 μm) |
| Confidence | Integer 0-100% | Categorical: low/nominal/high |
| Fire type | Not available | `type` field (0-3) |

### Fire Radiative Power (FRP)

FRP is a measure of the radiant heat output of detected fires, measured in megawatts (MW). It is proportional to the rate of biomass combustion and can be used to:
- Estimate emissions (smoke, CO₂, particulate matter)
- Compare fire intensity across regions and time
- Distinguish agricultural burns (low FRP) from wildfires (high FRP)
- Identify industrial sources (persistent, consistent FRP)

---

## 6. Quality and Known Issues

### Detection limitations

| Issue | Detail | Impact |
|-------|--------|--------|
| **Cloud cover** | Fires under clouds are completely invisible to optical/thermal sensors | Systematic undercount in cloudy/wet season; tropics most affected |
| **Overpass timing** | Fires must be burning at exact time of satellite overpass | Short-duration fires missed; diurnal bias (fires peak in afternoon) |
| **Small fires** | MODIS misses fires < ~100 m²; VIIRS detects down to ~25 m² | Use VIIRS for small fire detection |
| **Sun glint** | Reflected sunlight on water/metal surfaces can trigger false detections | Coastal areas, lakes, industrial sites; algorithms attempt to filter |
| **Hot surfaces** | Bare soil, volcanic activity, industrial heat sources | `type` field in VIIRS helps (type ≠ 0); MODIS lacks this |
| **Night vs day differences** | Nighttime detection has lower threshold (less background thermal noise) | More small fires detected at night; creates apparent diurnal bias |
| **Pixel size at scan edge** | Both MODIS and VIIRS pixels grow at scan edges | Edge-of-swath detections have poorer geolocation |
| **Smoke/haze** | Thick smoke reduces detection capability | During intense fire seasons, some fires self-obscure |

### Confidence interpretation

**MODIS confidence (0-100%):**
- \>80%: High confidence — very likely a fire
- 30-80%: Nominal — probable fire, may include some false alarms
- <30%: Low — possible fire or false alarm

**VIIRS confidence categories:**
- "high": Very likely a fire
- "nominal": Probable fire
- "low": Possible fire; may be false alarm from sun glint, hot surface, etc.

**Recommendation for Causal Atlas:** Use only "nominal" and "high" confidence detections for analysis. Filter out `type != 0` in VIIRS data to exclude volcanoes and industrial sources (unless those are the target of analysis).

### False detection sources

- Sun glint over water bodies and metallic surfaces (rooftops, solar panels)
- Gas flares at oil/gas facilities (persistent, identifiable by location stability)
- Volcanic activity (identifiable via VIIRS `type` field and known volcano locations)
- Hot desert surfaces (rare, mostly filtered by algorithms)

---

## 7. Burned Area Product (MCD64A1)

The burned area product complements active fire detections by providing the cumulative area burned per month.

| Attribute | Detail |
|-----------|--------|
| Product ID | MCD64A1 (Collection 6.1) |
| Resolution | 500 m |
| Temporal | Monthly |
| Coverage | Global land |
| Start date | November 2000 |
| Format | HDF4 (MODIS sinusoidal tiles) |
| Access | LPDAAC, AppEEARS, GEE |
| GEE collection | `MODIS/061/MCD64A1` |

**Key fields:**
- `BurnDate`: Day of burn (1-366) within the reporting month
- `Uncertainty`: Estimated uncertainty in days
- `QA`: Quality assessment bits
- `FirstDay`: First day of reliable detection
- `LastDay`: Last day of reliable detection

**Relationship to active fire data:**
- 44% of MCD64A1 burned cells were detected on the same day as an active fire
- 68% within 2 days of an active fire detection
- Burned area product captures fires missed by active fire (short-duration, under cloud at overpass time)
- Active fire provides timing; burned area provides extent

**VIIRS burned area:** A VIIRS burned area product has recently been added to FIRMS, offering improved resolution over the MODIS MCD64A1 product.

---

## 8. Licence and Citation

### Licence

NASA data are in the **public domain** under NASA's full and open data policy. There are no restrictions on use, redistribution, or commercial application.

### Citation requirements

When using FIRMS/LANCE data, include the following acknowledgment:

> "We acknowledge the use of data and/or imagery from NASA's Fire Information for Resource Management System (FIRMS) (https://earthdata.nasa.gov/firms), part of NASA's Earth Observing System Data and Information System (EOSDIS)."

For MODIS active fire, cite:
> Giglio, L., Schroeder, W., & Justice, C.O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment*, 178, 31-41.

For VIIRS active fire, cite:
> Schroeder, W., et al. (2014). The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment. *Remote Sensing of Environment*, 143, 85-96.

For burned area, cite:
> Giglio, L., et al. (2018). The Collection 6 MODIS burned area mapping algorithm and product. *Remote Sensing of Environment*, 217, 72-85.

---

## 9. Python Access and Processing

### Download via FIRMS API

```python
import pandas as pd
import requests

MAP_KEY = 'your_map_key_here'

# Download VIIRS S-NPP fire data for a country (ISO3 code)
def get_firms_country(country_iso3, source='VIIRS_SNPP_NRT', days=10):
    """Download FIRMS fire data for a country."""
    url = (f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/'
           f'{MAP_KEY}/{source}/{country_iso3}/{days}')
    df = pd.read_csv(url)
    return df

# Download for a bounding box (W,S,E,N)
def get_firms_area(west, south, east, north,
                   source='VIIRS_SNPP_NRT', days=10, date=None):
    """Download FIRMS fire data for a bounding box."""
    area = f'{west},{south},{east},{north}'
    url = (f'https://firms.modaps.eosdis.nasa.gov/api/area/csv/'
           f'{MAP_KEY}/{source}/{area}/{days}')
    if date:
        url += f'/{date}'  # YYYY-MM-DD for historical data
    df = pd.read_csv(url)
    return df

# Example: Get fires in Ethiopia, last 5 days
df_ethiopia = get_firms_country('ETH', days=5)
print(f"Fire detections: {len(df_ethiopia)}")
print(df_ethiopia.head())
```

### Download archive data

```python
import pandas as pd

# Full annual archive files (large!)
# Available at: https://firms.modaps.eosdis.nasa.gov/download/

# MODIS archive (2000-present)
modis_url = ('https://firms.modaps.eosdis.nasa.gov/data/active_fire/'
             'modis-c6.1/csv/MODIS_C6_1_Global_MCD14DL_NRT_{date}.csv')

# VIIRS S-NPP archive (2012-present)
viirs_url = ('https://firms.modaps.eosdis.nasa.gov/data/active_fire/'
             'suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_VNP14IMGTDL_NRT_{date}.csv')
```

### Aggregate to PRIO-GRID

```python
import pandas as pd
import numpy as np

def firms_to_priogrid(df, grid_size=0.5):
    """
    Aggregate FIRMS fire detections to PRIO-GRID cells.

    Returns DataFrame with fire count, mean FRP, and max FRP
    per grid cell per month.
    """
    # Parse date
    df['date'] = pd.to_datetime(df['acq_date'])
    df['year_month'] = df['date'].dt.to_period('M')

    # Assign to grid cells
    df['grid_lat'] = np.floor(df['latitude'] / grid_size) * grid_size + grid_size / 2
    df['grid_lon'] = np.floor(df['longitude'] / grid_size) * grid_size + grid_size / 2

    # Filter to high-confidence vegetation fires only
    if 'type' in df.columns:  # VIIRS
        df = df[df['type'] == 0]  # Presumed vegetation fire
        df = df[df['confidence'].isin(['nominal', 'high'])]
    else:  # MODIS
        df = df[df['confidence'] >= 30]

    # Aggregate per grid cell per month
    agg = df.groupby(['grid_lat', 'grid_lon', 'year_month']).agg(
        fire_count=('frp', 'count'),
        mean_frp=('frp', 'mean'),
        max_frp=('frp', 'max'),
        total_frp=('frp', 'sum'),
        day_fire_count=('daynight', lambda x: (x == 'D').sum()),
        night_fire_count=('daynight', lambda x: (x == 'N').sum()),
    ).reset_index()

    return agg

# Example usage
df = get_firms_country('COD', source='VIIRS_SNPP_NRT', days=10)
grid_data = firms_to_priogrid(df)
print(grid_data.head())
```

### Combine MODIS and VIIRS

```python
def combine_firms_sources(country_iso3, days=10):
    """
    Combine fire detections from multiple FIRMS sources.
    De-duplicate where MODIS and VIIRS detect same fire.
    """
    sources = {
        'MODIS_NRT': get_firms_country(country_iso3, 'MODIS_NRT', days),
        'VIIRS_SNPP_NRT': get_firms_country(country_iso3, 'VIIRS_SNPP_NRT', days),
        'VIIRS_NOAA20_NRT': get_firms_country(country_iso3, 'VIIRS_NOAA20_NRT', days),
    }

    for source_name, df in sources.items():
        df['source'] = source_name

    combined = pd.concat(sources.values(), ignore_index=True)

    # Note: De-duplication across MODIS/VIIRS is non-trivial due to
    # different pixel sizes and overpass times. For grid-level aggregation,
    # counting all detections (with source tracking) is often acceptable.

    return combined
```

---

## 10. Interoperability with Other Causal Atlas Datasets

### Direct relationships

| Dataset | Relationship | Integration approach |
|---------|-------------|---------------------|
| **ACLED** | Conflict-related arson produces fire detections | Spatial-temporal join; fire spikes near conflict events may indicate arson |
| **OpenAQ** | Agricultural/wildfire → air quality degradation | Fire FRP correlates with PM2.5/PM10 spikes; time-lagged analysis |
| **ERA5** | Temperature, humidity, wind drive fire weather | Fire Weather Index computation; drought → fire risk |
| **CHIRPS** | Drought precedes fire seasons | Low CHIRPS anomalies → increased fire activity (1-3 month lag) |
| **NDVI/MODIS** | Fire destroys vegetation; post-fire NDVI recovery | Pre/post-fire NDVI change detection |
| **IPC food security** | Agricultural burning → food production; fire → displacement | Fire in cropland areas → food security impacts |
| **Nightlights (VIIRS)** | Conflict-related fires visible at night | Cross-reference nighttime fires with nightlight changes |
| **EM-DAT** | Wildfire disaster events | FIRMS provides spatial detail for EM-DAT wildfire records |

### Notable analysis applications

- **Bellingcat** uses FIRMS extensively to monitor conflict zones (Ukraine, Syria, Gaza) — fire spikes correlate with military operations and can verify reported attacks
- **INPE DETER** uses FIRMS for Amazon deforestation monitoring
- **FEWS NET** monitors agricultural burning patterns in Africa as food security indicators
- **Global Forest Watch** integrates FIRMS fires with tree cover loss data

---

## 11. Fire in Causal Chains

### Agricultural burning → air quality → health

1. Seasonal agricultural burning (crop residue, land clearing) detected by FIRMS
2. Fire radiative power (FRP) estimates emissions intensity
3. Smoke transport modelled using ERA5 wind fields
4. Air quality degradation measured by OpenAQ
5. Respiratory health outcomes in downwind populations

### Conflict → arson → displacement

1. Armed conflict events recorded by ACLED/UCDP
2. Conflict-related fires detected by FIRMS (elevated fire counts near conflict locations)
3. Displacement triggered (IDMC/UNHCR data)
4. Secondary humanitarian effects (food insecurity, health)

### Deforestation → climate → cascading effects

1. Deforestation fires detected by FIRMS in tropical forests
2. Land cover change confirmed by NDVI decline
3. Reduced evapotranspiration changes local climate (ERA5)
4. Downstream effects on precipitation patterns

### Drought → wildfire → ecosystem damage

1. Precipitation deficit (CHIRPS/ERA5) creates dry conditions
2. Vegetation stress (NDVI decline)
3. Fire outbreak detected by FIRMS
4. Air quality degradation (OpenAQ)
5. Ecosystem recovery or degradation (NDVI monitoring)

---

## 12. Relevance to Causal Atlas

### Why FIRMS is essential

FIRMS provides a unique real-time signal that bridges multiple causal domains:
- **Environmental:** Fires are both a cause and consequence of environmental change
- **Conflict:** Fire is used as a weapon and creates a detectable signal of violence
- **Food security:** Agricultural burning patterns indicate farming practices; uncontrolled fires destroy crops
- **Health:** Biomass burning is a major source of air pollution in developing countries
- **Displacement:** Fire can trigger and indicate displacement events

### Priority implementation

1. **Phase 1:** Ingest VIIRS S-NPP + NOAA-20 fire data for all PRIO-GRID cells (2012-present)
2. **Phase 2:** Compute monthly fire metrics per grid cell (count, mean/max FRP, day/night ratio)
3. **Phase 3:** Cross-correlate with ACLED conflict events, OpenAQ air quality, CHIRPS precipitation
4. **Phase 4:** Build causal chain models (drought → fire → air quality → health)

### Recommended data sources by priority

1. **VIIRS S-NPP (VNP14IMG):** Best combination of resolution (375 m) and temporal coverage (2012+)
2. **VIIRS NOAA-20 (VJ114IMG):** Additional observations from 2020+
3. **MODIS (MCD14ML):** Longest record (2000+) for climate trend analysis
4. **MCD64A1 burned area:** Monthly cumulative extent for seasonal analysis

### Storage estimate

| Data | Approximate size |
|------|-----------------|
| VIIRS S-NPP global CSV, 1 year | ~2-5 GB |
| VIIRS S-NPP global CSV, 2012-present | ~30-60 GB |
| MODIS global CSV, 2000-present | ~20-40 GB |
| Aggregated to PRIO-GRID monthly (all sources) | ~500 MB |

---

## Sources

- NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/
- FIRMS FAQ and data documentation: https://www.earthdata.nasa.gov/data/tools/firms
- FIRMS API documentation: https://firms.modaps.eosdis.nasa.gov/api/area/
- FIRMS Python tutorial: https://firms.modaps.eosdis.nasa.gov/content/academy/data_api/firms_api_use.html
- FIRMS archive download: https://firms.modaps.eosdis.nasa.gov/download/
- Active fire data attributes: https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs
- VIIRS I-Band 375m documentation: https://www.earthdata.nasa.gov/data/instruments/viirs/viirs-i-band-375-m-active-fire-data
- MODIS active fire user guide: https://modis-fire.umd.edu/files/MODIS_C6_C6.1_Fire_User_Guide_1.0.pdf
- MCD64A1 burned area: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mcd64a1-061
- MODIS burned area algorithm: https://pmc.ncbi.nlm.nih.gov/articles/PMC6136150/
- LANCE citation guidelines: https://earthdata.nasa.gov/earth-observation-data/near-real-time/citation
- Bellingcat FIRMS guide: https://www.bellingcat.com/resources/2022/10/04/scorched-earth-using-nasa-fire-data-to-monitor-war-zones/
- FIRMS in GEE: https://developers.google.com/earth-engine/datasets/catalog/FIRMS
- GEE community FIRMS vectors: https://gee-community-catalog.org/projects/firms_vector/
- VIIRS burned area on FIRMS: https://www.earthdata.nasa.gov/news/blog/viirs-global-burned-area-product-added-firms
- Giglio, L., Schroeder, W., & Justice, C.O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment*, 178, 31-41.
- Schroeder, W., et al. (2014). The New VIIRS 375 m active fire detection data product. *Remote Sensing of Environment*, 143, 85-96.
- Giglio, L., et al. (2018). The Collection 6 MODIS burned area mapping algorithm and product. *Remote Sensing of Environment*, 217, 72-85.
