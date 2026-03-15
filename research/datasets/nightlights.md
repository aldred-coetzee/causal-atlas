# Nighttime Lights: VIIRS and DMSP-OLS

*Last updated: March 2025*

## Overview

Nighttime lights (NTL) data captured from satellite sensors provide a unique proxy for human activity, economic development, urbanisation, and the impacts of conflict and disasters. Two major sensor families have produced the global NTL record:

1. **DMSP-OLS (Defense Meteorological Satellite Program / Operational Linescan System)** -- the legacy record from 1992 to 2013, produced by NOAA's National Geophysical Data Center (now NCEI). Provides annual stable lights composites at ~1 km resolution in uncalibrated digital numbers (DN 0-63).

2. **VIIRS DNB (Visible Infrared Imaging Radiometer Suite / Day-Night Band)** -- the modern successor flying on the Suomi-NPP (launched October 2011) and NOAA-20/JPSS-1 (launched November 2017) satellites. VIIRS offers calibrated radiance measurements at ~500 m resolution with far superior dynamic range and radiometric quality.

Two distinct product families exist for VIIRS nighttime lights:

- **NOAA EOG Composites** -- monthly and annual cloud-free composites produced by the Earth Observation Group (EOG) at the Colorado School of Mines (formerly at NOAA/NGDC). These are the most widely used NTL products in the social sciences.
- **NASA Black Marble (VNP46)** -- a suite of four daily, monthly, and annual products with advanced corrections for lunar BRDF, atmospheric effects, terrain, and stray light. Produced by NASA's VIIRS Land Science Team.

### Why Nighttime Lights Matter

- **Economic activity proxy**: Strong correlation with GDP at national and sub-national levels (R-squared = 0.97 for illuminated area vs. GDP across 21 countries; Henderson et al. 2012). Particularly valuable where official statistics are unreliable or missing.
- **Conflict impact measurement**: Rebel and government-caused deaths are strongly associated with decreases in nighttime lights (100 deaths implying -23% and -14% changes respectively; Li et al. 2017). Night-light-based GDP reestimates often show faster economic deterioration during conflict than official data.
- **Urbanisation monitoring**: Tracking urban expansion, densification, and electrification rates.
- **Disaster impact and recovery**: Power outages, infrastructure destruction, and recovery trajectories can be observed at daily to monthly cadence.
- **Inequality and poverty mapping**: Sub-national wealth estimation where survey data is sparse.

---

## Data Products: Detailed Specifications

### DMSP-OLS Nighttime Lights (Legacy)

| Attribute | Detail |
|---|---|
| **Provider** | Earth Observation Group (EOG), Payne Institute for Public Policy, Colorado School of Mines; originally NOAA/NGDC |
| **Satellites** | DMSP satellites F10 through F18 |
| **Temporal coverage** | 1992--2013 (annual composites) |
| **Spatial resolution** | 30 arc-seconds (~927 m at equator) |
| **Spatial extent** | Global: 180W to 180E, 65S to 75N |
| **Coordinate system** | WGS84 geographic (EPSG:4326) |
| **Data format** | GeoTIFF |
| **Value type** | Digital Number (DN), 6-bit (0--63) |
| **Calibration** | No on-board calibration; values are NOT calibrated radiance |
| **GEE collection** | `NOAA/DMSP-OLS/NIGHTTIME_LIGHTS` |

#### DMSP-OLS Bands

| Band | Description | Range |
|---|---|---|
| `avg_vis` | Average visible band DN, cloud-free observations | 0--63 |
| `stable_lights` | Cleaned persistent lights; ephemeral sources (fires, aurora, boats) removed | 0--63 |
| `cf_cvg` | Cloud-free coverage count (number of observations) | 0--126 |
| `avg_lights_x_pct` | Average DN multiplied by percent frequency of light detection | 0--63 |

#### DMSP-OLS Known Limitations

- **Saturation (top-coding)**: DN values saturate at 63, meaning bright urban cores cannot be distinguished. Radiance-calibrated versions partially address this but exist only for select years.
- **Blooming / overglow**: Light from bright sources bleeds into adjacent pixels, making cities appear larger than they are.
- **No on-board calibration**: Inter-annual and inter-satellite comparisons require intercalibration. Multiple intercalibration approaches exist (e.g., Elvidge et al. 2014; Li et al. 2017; Zhang et al. 2016).
- **Coarse spatial resolution**: ~1 km limits ability to distinguish individual settlements.
- **No radiance units**: Raw DN values are ordinal, not ratio-scale.

#### Intercalibration Resources

Several published intercalibration methods allow construction of consistent 1992--2013 time series:
- **Elvidge et al. (2014)**: Radiance-calibrated series using reference regions
- **Zhang et al. (2016)**: Stepwise calibration (Remote Sensing, 9(6), 637)
- **Chen & Nordhaus (2015)**: CCNL 1992--2013 consistent corrected nighttime lights (Scientific Data)

---

### NOAA EOG VIIRS Monthly Composites

| Attribute | Detail |
|---|---|
| **Provider** | Earth Observation Group (EOG), Payne Institute, Colorado School of Mines |
| **Satellite** | Suomi-NPP (primary), NOAA-20/JPSS-1 (supplementary from 2018) |
| **Temporal coverage** | April 2012 -- present (monthly); 2012--present (annual) |
| **Update frequency** | Monthly (typically ~2 months latency) |
| **Spatial resolution** | 15 arc-seconds (~463 m at equator) |
| **Spatial extent** | 180W to 180E, 65S to 75N |
| **Coordinate system** | WGS84 geographic (EPSG:4326) |
| **Data format** | GeoTIFF (DEFLATE compressed), .gz / .tgz for downloads |
| **Value type** | Calibrated radiance in nanoWatts/cm2/sr (nW/cm2/sr) |

#### Product Configurations

| Configuration | Code | Description |
|---|---|---|
| Cloud-free, no stray light correction | `vcm` / `VCMCFG` | Excludes all data affected by stray light. Less polar coverage but higher quality. |
| Cloud-free, stray light corrected | `vcmsl` / `VCMSLCFG` | Includes stray-light-corrected data. More coverage toward poles but reduced quality in those areas. |

#### Bands (Monthly Composites)

| Band | Description | Units | Range |
|---|---|---|---|
| `avg_rad` | Average DNB radiance, cloud-free observations | nW/cm2/sr | -1.5 to 193,565 |
| `cf_cvg` | Cloud-free coverage count | observations | 0--84 |

Negative `avg_rad` values can occur in areas with very low radiance due to the averaging of noise.

#### Annual Composite Versions

| Version | Years | Key Features |
|---|---|---|
| **V1** | 2012--2020 (monthly); annual available | Original processing; `vcm` configuration only for annual |
| **V2** | 2012--2020 | Consistently processed time series; multiyear maximum median for background zeroing |
| **V2.1** | 2012--2021 | Incremental improvements |
| **V2.2** | 2012--2023 | Latest; methodology shift from nightly to monthly-based composites. Includes average, median, min, max layers. |

#### Google Earth Engine Access

```
// Stray light corrected monthly composites
NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG    // 2014-01 to present
NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG       // 2012-04 to present

// Annual composites
NOAA/VIIRS/DNB/ANNUAL_V21              // Annual V2.1
NOAA/VIIRS/DNB/ANNUAL_V22              // Annual V2.2
```

#### Direct Download

- **Monthly tiled**: `https://eogdata.mines.edu/nighttime_light/monthly/v10/`
- **Monthly non-tiled**: `https://eogdata.mines.edu/nighttime_light/monthly_notile/`
- **Annual V2.2**: `https://eogdata.mines.edu/nighttime_light/annual/v22/`
- **Nightly mosaics**: Available near-real-time via EOG interactive map

**Authentication**: EOG downloads require free registration at `https://eogdata.mines.edu/nighttime_light/`. No API key required for GEE access.

---

### NASA Black Marble (VNP46) Product Suite

The Black Marble suite provides the most scientifically rigorous NTL products with advanced corrections. Produced by NASA Goddard Space Flight Center under Principal Investigator Miguel Roman.

| Product | Name | Resolution | Temporal | Format |
|---|---|---|---|---|
| **VNP46A1** | Daily Gridded DNB (at-sensor, top-of-atmosphere) | 15 arc-sec (~500 m) | Daily | HDF-EOS5 |
| **VNP46A2** | Daily Gap-Filled Lunar BRDF-Adjusted NTL | 15 arc-sec (~500 m) | Daily | HDF-EOS5 |
| **VNP46A3** | Monthly Lunar BRDF-Adjusted NTL Composite | 15 arc-sec (~500 m) | Monthly | HDF-EOS5 |
| **VNP46A4** | Annual Lunar BRDF-Adjusted NTL Composite | 15 arc-sec (~500 m) | Annual | HDF-EOS5 |

#### VNP46A2 Corrections Applied

- Lunar BRDF (bidirectional reflectance distribution function) correction
- Atmospheric correction
- Thermal emission correction
- Terrain correction
- Stray light contamination removal

#### VNP46A3/A4 Composite Layers

The monthly (VNP46A3) product contains **28 layers** providing:
- NTL composite radiance for multiple view zenith angle categories: near-nadir, off-nadir, all angles
- Snow-covered and snow-free status variants
- Number of observations per composite
- Quality assurance flags
- Standard deviation of radiance
- Land-water mask
- Latitude and longitude coordinates

Boxplot-based outlier removal minimises reliance on empirical or regional thresholds.

#### Temporal Coverage

| Satellite | Start Date | Status |
|---|---|---|
| Suomi-NPP (SNPP) | 19 January 2012 | Ongoing (V2.0) |
| NOAA-20 / JPSS-1 | 5 January 2018 | Ongoing (V2.0) |

**Note**: The V2.0 monthly and yearly composite collections were slated for release by late spring 2025.

#### Access Methods

| Method | URL / Identifier |
|---|---|
| **NASA LAADS DAAC** | `https://ladsweb.modaps.eosdis.nasa.gov/` -- search by product shortname |
| **NASA Earthdata Search** | `https://search.earthdata.nasa.gov/` |
| **Google Earth Engine** | `NASA/VIIRS/002/VNP46A2` (daily corrected) |
| **NASA FIRMS** | For fire-filtered variants |

**Authentication**: NASA Earthdata Login required (free registration at `https://urs.earthdata.nasa.gov/`).

---

## Spatial Detail

| Product | Native Resolution | Grid | Tile System |
|---|---|---|---|
| DMSP-OLS | ~927 m (30 arc-sec) | Geographic lat/lon | Full global file |
| NOAA EOG monthly | ~463 m (15 arc-sec) | Geographic lat/lon (EPSG:4326) | 6 tiles or full global |
| NASA Black Marble | ~500 m (15 arc-sec) | Geographic lat/lon | 10x10 degree tiles (h/v) |

### Aggregation to PRIO-GRID

PRIO-GRID v2.0 already includes a `nlights_mean` variable -- mean nighttime light value per 0.5-degree grid cell, derived from the DMSP-OLS stable lights composites. For Causal Atlas:

- VIIRS data at 15 arc-seconds means approximately **3600 VIIRS pixels per 0.5-degree PRIO-GRID cell** (60x60 grid).
- Aggregation options: mean radiance, median radiance, sum of lights (SOL), lit area fraction, maximum radiance.
- Zonal statistics can be computed efficiently using `rasterstats`, `exactextract`, or Google Earth Engine `reduceRegions()`.

---

## Temporal Detail

| Product | Cadence | Latency | Time Span |
|---|---|---|---|
| DMSP-OLS | Annual | N/A (historical archive) | 1992--2013 |
| NOAA EOG monthly | Monthly | ~2 months | 2012--present |
| NOAA EOG annual | Annual | ~6 months | 2012--present |
| Black Marble VNP46A2 | Daily | ~1-3 days | 2012--present |
| Black Marble VNP46A3 | Monthly | TBD (V2.0 release pending) | 2012--present |
| Black Marble VNP46A4 | Annual | TBD | 2012--present |

### Temporal Overlap

DMSP-OLS and VIIRS overlap during 2012--2013, enabling cross-calibration. Several studies (e.g., Elvidge et al. 2017; Li et al. 2017) provide harmonised NTL time series spanning 1992--present by calibrating DMSP to VIIRS radiance levels.

### Known Temporal Gaps

- **June--August 2022**: SNPP satellite anomaly caused data gaps (June 1-27, July 1-26); NOAA-20 data substituted for August.
- **Polar regions**: Reduced coverage in boreal summer due to midnight sun preventing nighttime observations.
- **Cloud cover**: Persistent cloud cover (e.g., tropical regions) can reduce monthly composite quality; `cf_cvg` band indicates coverage.

---

## Quality and Limitations

### Signal Sources (What NTL Actually Measures)

NTL captures ALL sources of nighttime visible light:
- Artificial lighting (cities, roads, industrial facilities)
- Gas flares (oil/gas extraction sites)
- Fishing boats (especially squid boats using bright lights)
- Wildfires and agricultural burning
- Aurora (at high latitudes)
- Moonlit clouds (corrected in Black Marble, not in raw data)

Only the annual EOG composites and Black Marble products attempt to filter ephemeral sources.

### Limitations as Economic Proxy

- **Saturation at high GDP levels**: NTL grow only about half as fast as GDP in advanced economies (Henderson et al. 2012).
- **Agricultural GDP invisible**: NTL are significantly less responsive to agricultural GDP; rural economic activity is poorly captured.
- **Population density dependence**: Elasticity of NTL to GDP varies with population density.
- **Urban bias**: NTL primarily captures urban/peri-urban activity; rural areas may show zero radiance despite economic activity.
- **Gas flare contamination**: Major oil-producing regions show high radiance unrelated to population or economic activity (e.g., Niger Delta, Bakken Formation, Siberia).

### Product-Specific Quality Issues

| Issue | DMSP-OLS | NOAA EOG VIIRS | Black Marble |
|---|---|---|---|
| Saturation/top-coding | Severe (DN 0-63) | None (calibrated radiance) | None |
| Overglow/blooming | Significant | Reduced but present | Minimal |
| Stray light contamination | N/A | `vcm` excludes; `vcmsl` corrects | Fully corrected |
| Lunar illumination effects | Not corrected | Not corrected | Fully corrected (BRDF) |
| Atmospheric effects | Not corrected | Not corrected | Fully corrected |
| Inter-annual consistency | Requires intercalibration | V2.x provides consistent series | Consistent within version |

---

## Licence and Terms of Use

| Product | Licence | Restrictions |
|---|---|---|
| DMSP-OLS (NOAA) | Public domain | No copyright, no restrictions on lawful use |
| NOAA EOG VIIRS | Creative Commons Attribution 4.0 (CC BY 4.0) | Proper citation required |
| NASA Black Marble | NASA open data policy | Free for all uses; citation requested |

### Citation Requirements

**NOAA EOG products**:
> Elvidge, C.D., Zhizhin, M., Ghosh, T., Hsu, F-C., Taneja, J. (2021). Annual Time Series of Global VIIRS Nighttime Lights Derived from Monthly Averages: 2012 to 2019. Remote Sensing, 13(5), 922.

**NASA Black Marble**:
> Roman, M.O. et al. (2018). NASA's Black Marble nighttime lights product suite. Remote Sensing of Environment, 210, 113-143. DOI: 10.1016/j.rse.2018.03.017

---

## Interoperability with Other Causal Atlas Datasets

| Dataset | Relationship | Integration Notes |
|---|---|---|
| **PRIO-GRID** | NTL already included as `nlights_mean` (DMSP). VIIRS aggregation straightforward via zonal stats. | Match temporal resolution to PRIO-GRID monthly/annual structure. |
| **ACLED / UCDP-GED** | Conflict events can be spatially joined to NTL grid cells. NTL change before/after conflict onset is a standard analytical approach. | Buffer events to grid cell or use point-to-raster extraction. |
| **World Bank WDI** | GDP correlation validation. NTL can supplement GDP data in countries with poor national accounts. | Country-level aggregation of NTL sum-of-lights for comparison. |
| **CHIRPS / NDVI** | Cross-domain: NTL (economic) vs. vegetation/rainfall (environmental). Time-lagged correlations may reveal drought impact on economic activity. | Same PRIO-GRID spatial framework enables direct comparison. |
| **WFP food prices** | NTL in market towns may correlate with food price dynamics and market functioning. | Market location coordinates for point extraction. |
| **EM-DAT** | Disaster impact visible as NTL drops; recovery visible as NTL recovery. | Spatial and temporal matching of disaster events to NTL imagery. |

---

## Python Access

### Google Earth Engine (via `ee` Python API)

```python
import ee
ee.Authenticate()
ee.Initialize()

# NOAA EOG monthly stray-light-corrected composites
ntl = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG') \
    .filterDate('2020-01-01', '2020-12-31') \
    .select('avg_rad')

# Compute annual mean radiance
annual_mean = ntl.mean()

# Reduce to PRIO-GRID-like regions
grid_cell = ee.Geometry.Rectangle([36.0, -1.0, 36.5, -0.5])  # Example 0.5 deg cell
stats = annual_mean.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=grid_cell,
    scale=500
)
print(stats.getInfo())
```

### BlackMarblePy (World Bank package for NASA VNP46)

```python
# pip install blackmarblepy
from blackmarble.bm_raster import bm_raster
from blackmarble.bm_extract import bm_extract
import geopandas as gpd

# Requires NASA Earthdata bearer token
bearer_token = "YOUR_NASA_BEARER_TOKEN"

# Load region of interest as GeoDataFrame
roi = gpd.read_file("admin_boundaries.shp")

# Get monthly NTL raster
raster = bm_raster(
    roi,
    product_id="VNP46A3",       # Monthly composite
    date="2023-06-01",
    bearer=bearer_token
)

# Extract aggregated statistics
stats_df = bm_extract(
    roi,
    product_id="VNP46A3",
    date=["2020-01-01", "2020-12-01"],
    bearer=bearer_token
)
```

### Direct Download with `rasterio`

```python
import rasterio
import numpy as np

# After downloading GeoTIFF from EOG
with rasterio.open('VIIRS_2023_global.tif') as src:
    data = src.read(1)  # avg_rad band
    profile = src.profile
    transform = src.transform

    # Mask negative/nodata values
    data = np.where(data < 0, 0, data)

    # Get value at specific coordinates
    row, col = src.index(36.8, -1.3)  # lon, lat (Nairobi)
    radiance = data[row, col]
    print(f"Radiance at Nairobi: {radiance:.2f} nW/cm2/sr")
```

### NASA `earthaccess` for Black Marble HDF5

```python
import earthaccess

earthaccess.login()

# Search for VNP46A3 monthly composite
results = earthaccess.search_data(
    short_name="VNP46A3",
    temporal=("2023-01-01", "2023-12-31"),
    bounding_box=(32, -5, 42, 5)  # East Africa
)

# Download locally
files = earthaccess.download(results, local_path="./vnp46a3/")
```

### Zonal Statistics with `rasterstats`

```python
from rasterstats import zonal_stats
import geopandas as gpd

# PRIO-GRID cells as vector polygons
grid = gpd.read_file("priogrid_cells.shp")

# Compute zonal statistics
stats = zonal_stats(
    grid,
    'VIIRS_2023_monthly.tif',
    stats=['mean', 'sum', 'count', 'std', 'max'],
    geojson_out=True
)
```

---

## Relevance to Causal Atlas

### Primary Use Cases

1. **Economic activity layer**: Nighttime lights serve as the primary sub-national economic activity indicator, especially critical for countries lacking reliable GDP sub-national estimates. Provides a continuous, objective measure at monthly cadence.

2. **Conflict impact quantification**: Pre/post conflict NTL change is a validated approach to measuring economic impact of conflict events. Can be cross-referenced with ACLED/UCDP event data.

3. **Disaster impact and recovery**: Combined with EM-DAT disaster events, NTL drops and recovery trajectories can quantify disaster economic impact.

4. **Cross-domain causal chains**: NTL bridges environmental data (NDVI, CHIRPS rainfall) to economic outcomes. Example causal chains:
   - Drought (CHIRPS) -> crop failure (NDVI) -> reduced economic activity (NTL)
   - Conflict (ACLED) -> population displacement -> NTL decrease
   - Natural disaster (EM-DAT) -> infrastructure destruction -> NTL drop -> recovery trajectory

5. **Urbanisation and development tracking**: Long-term trends in NTL reveal urbanisation patterns, electrification progress, and development trajectories.

### Recommended Products for Causal Atlas

| Use Case | Recommended Product | Rationale |
|---|---|---|
| Monthly time series (2014--present) | NOAA EOG `VCMSLCFG` monthly | Broadest coverage, calibrated radiance, easy access via GEE |
| Historical series (1992--2013) | DMSP-OLS with intercalibration | Only option for pre-2012 data |
| Long harmonised series (1992--present) | DMSP-VIIRS harmonised products | Published calibration methods exist |
| Daily event-level analysis | NASA Black Marble VNP46A2 | Daily corrected radiance for rapid-onset events |
| Highest scientific quality | NASA Black Marble VNP46A3/A4 | Full atmospheric/BRDF correction |

### Integration Strategy

1. **Start with NOAA EOG monthly composites** via Google Earth Engine for ease of access and broad temporal coverage.
2. **Aggregate to 0.5-degree PRIO-GRID cells** using zonal mean and sum-of-lights.
3. **Store as monthly Parquet time series** per grid cell.
4. **Cross-reference with DMSP-OLS** for pre-2012 analysis using published intercalibration coefficients.
5. **Use Black Marble for validation** and for event-level (daily) analysis when needed.

---

## Sources

- NASA Black Marble product page: https://blackmarble.gsfc.nasa.gov/
- NASA VIIRS Land products: https://viirsland.gsfc.nasa.gov/Products/NASA/BlackMarble.html
- Black Marble User Guide (Collection 2.0): https://viirsland.gsfc.nasa.gov/PDF/BlackMarbleUserGuide_Collection2.0.pdf
- NOAA EOG VIIRS products: https://eogdata.mines.edu/products/vnl/
- DMSP-OLS products: https://eogdata.mines.edu/products/dmsp/
- GEE NOAA monthly: https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG
- GEE DMSP-OLS: https://developers.google.com/earth-engine/datasets/catalog/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS
- GEE VNP46A2: https://developers.google.com/earth-engine/datasets/catalog/NASA_VIIRS_002_VNP46A2
- LAADS DAAC VNP46A3: https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A3/
- World Bank Open Nighttime Lights: https://worldbank.github.io/OpenNightLights/
- BlackMarblePy: https://worldbank.github.io/blackmarblepy/
- Henderson, Storeygard, Weil (2012). "Measuring Economic Growth from Outer Space." American Economic Review, 102(2), 994-1028.
- Elvidge et al. (2017). "VIIRS night-time lights." International Journal of Remote Sensing, 38(21), 5860-5879.
- Roman et al. (2018). "NASA's Black Marble nighttime lights product suite." Remote Sensing of Environment, 210, 113-143.
- Chen & Nordhaus (2015). "A consistent and corrected nighttime light dataset (CCNL 1992-2013)." Scientific Data.
- Li & Li (2014). "Night-Time Light Data: A Good Proxy Measure for Economic Activity?" PLOS ONE, 10(10), e0139779.
