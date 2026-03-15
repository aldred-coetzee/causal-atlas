# ERA5 — ECMWF Reanalysis v5

> **Last reviewed:** March 2025
> **Status:** Active, continuously updated (5-day lag from present)
> **Website:** https://cds.climate.copernicus.eu

---

## 1. Overview

ERA5 is the fifth-generation global atmospheric reanalysis dataset produced by the European Centre for Medium-Range Weather Forecasts (ECMWF) as part of the Copernicus Climate Change Service (C3S). It provides hourly estimates for a vast number of atmospheric, ocean-wave, and land-surface variables, covering the entire globe from January 1940 to within 5 days of the present.

ERA5 is widely regarded as the most comprehensive reanalysis product available and serves as the de facto standard climate baseline for research, operational meteorology, and cross-domain analysis. For Causal Atlas, ERA5 is the single most important climate/weather dataset — it provides consistent, gap-free, global coverage of temperature, precipitation, wind, soil moisture, radiation, and dozens of other variables that form the environmental backbone of cross-domain causal analysis.

**Key facts:**

| Attribute | Detail |
|-----------|--------|
| Producer | ECMWF / Copernicus Climate Change Service (C3S) |
| Type | Global atmospheric reanalysis (model + observations) |
| Temporal coverage | 1940-01-01 to present (5-day lag) |
| Native temporal resolution | Hourly |
| Aggregated products | Daily, monthly means available |
| Native spatial resolution | ~31 km (0.25° x 0.25° lat/lon grid) |
| Vertical levels | 137 hybrid sigma/pressure model levels (surface to ~80 km) |
| Pressure levels | 37 standard levels (1000 hPa to 1 hPa) |
| Number of variables | 200+ across single levels, pressure levels, and model levels |
| Total dataset size | ~5 petabytes (full archive) |
| Data format | GRIB, NetCDF (via CDS) |
| Predecessor | ERA-Interim (1979-2019, now superseded) |
| Citation | Hersbach et al. (2020), QJRMS, doi:10.1002/qj.3803 |

### ERA5 vs ERA5-Land

ERA5-Land is a companion product that replays the land component of ERA5 at enhanced resolution:

| Attribute | ERA5 | ERA5-Land |
|-----------|------|-----------|
| Spatial resolution | ~31 km (0.25°) | ~9 km (0.1°) |
| Coverage | Global (land + ocean + atmosphere) | Land only |
| Temporal coverage | 1940-present | 1950-present |
| Variables | 200+ (atmosphere, ocean, land) | ~50 (land surface only) |
| Atmospheric forcing | Self-consistent | Driven by ERA5 atmospheric fields |
| Key variables | All | Soil moisture, soil temperature, snow, evaporation, runoff, skin temperature, lake variables |

ERA5-Land is particularly valuable when higher spatial resolution is needed for land-surface variables like soil moisture, evaporation, and snow cover.

---

## 2. Spatial Coverage and Resolution

### Native grid

- **Atmosphere:** 0.25° x 0.25° regular lat/lon grid (~31 km at equator)
- **Ocean waves:** 0.5° x 0.5° regular lat/lon grid
- **ERA5-Land:** 0.1° x 0.1° regular lat/lon grid (~9 km at equator)
- **Coverage:** Fully global, including polar regions and oceans
- **Vertical:** 137 model levels; data also interpolated to 37 pressure levels, 16 potential temperature levels, and 1 potential vorticity level

### Grid specifications

The native ERA5 grid provides approximately:
- 721 latitude points (90°N to 90°S at 0.25° spacing)
- 1440 longitude points (0°E to 359.75°E at 0.25° spacing)
- Total: ~1,038,240 grid cells per level per timestep

### Re-gridding options

The CDS API supports on-the-fly regridding using the `grid` parameter. Users can request data at coarser resolutions (e.g., 0.5°, 1.0°, 2.5°) without needing to download at native resolution first.

---

## 3. Temporal Coverage and Resolution

| Product | Temporal range | Resolution | Update frequency |
|---------|---------------|------------|------------------|
| ERA5 hourly | 1940-present | Hourly | ~5-day lag |
| ERA5 monthly means | 1940-present | Monthly | Monthly |
| ERA5 monthly means by hour of day | 1940-present | Monthly (diurnal cycle) | Monthly |
| ERA5-Land hourly | 1950-present | Hourly | ~5-day lag |
| ERA5-Land monthly | 1950-present | Monthly | Monthly |

### Preliminary vs final data

- **ERA5T (preliminary):** Available within 5 days, produced with a shorter data assimilation window
- **ERA5 (final):** Consolidated product, available with approximately 2-3 month lag
- For most Causal Atlas purposes, ERA5T is sufficient; differences are minimal

---

## 4. Key Variables for Causal Atlas

ERA5 provides 200+ variables. The most relevant for cross-domain causal analysis include:

### Surface / single-level variables

| Variable | CDS name | Unit | Notes |
|----------|----------|------|-------|
| 2m temperature | `2m_temperature` | K | Most-used climate variable |
| 2m dewpoint temperature | `2m_dewpoint_temperature` | K | Humidity proxy |
| Total precipitation | `total_precipitation` | m | Accumulated; requires differencing for rates |
| 10m u-component of wind | `10m_u_component_of_wind` | m/s | Eastward wind |
| 10m v-component of wind | `10m_v_component_of_wind` | m/s | Northward wind |
| Surface pressure | `surface_pressure` | Pa | |
| Mean sea level pressure | `mean_sea_level_pressure` | Pa | |
| Sea surface temperature | `sea_surface_temperature` | K | Oceanic only |
| Skin temperature | `skin_temperature` | K | Combined land/ocean surface |
| Soil temperature (levels 1-4) | `soil_temperature_level_1` etc. | K | Depths: 0-7, 7-28, 28-100, 100-289 cm |
| Volumetric soil water (levels 1-4) | `volumetric_soil_water_layer_1` etc. | m³/m³ | Same depth layers |
| Snow depth | `snow_depth` | m water equiv. | |
| Evaporation | `evaporation` | m | Accumulated |
| Surface solar radiation downwards | `surface_solar_radiation_downwards` | J/m² | Accumulated |
| Surface net thermal radiation | `surface_net_thermal_radiation` | J/m² | Accumulated |
| Total cloud cover | `total_cloud_cover` | 0-1 | Fraction |
| Leaf area index (high/low vegetation) | `leaf_area_index_high_vegetation` | m²/m² | Vegetation state |
| Potential evaporation | `potential_evaporation` | m | Drought indicator |

### Pressure-level variables

| Variable | Levels available | Unit |
|----------|-----------------|------|
| Temperature | 37 levels (1000-1 hPa) | K |
| Geopotential | 37 levels | m²/s² |
| U/V wind components | 37 levels | m/s |
| Relative humidity | 37 levels | % |
| Specific humidity | 37 levels | kg/kg |
| Vertical velocity | 37 levels | Pa/s |
| Divergence | 37 levels | s⁻¹ |
| Vorticity | 37 levels | s⁻¹ |

### Standard pressure levels

1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1 hPa

---

## 5. Data Access Methods

### Method 1: CDS API (Primary)

The Copernicus Climate Data Store (CDS) API is the primary programmatic access method.

**Registration:**
1. Create an ECMWF account at https://cds.climate.copernicus.eu
2. Accept the licence terms for ERA5 datasets
3. Obtain a Personal Access Token from your profile page

**Configuration:**

Create `~/.cdsapirc`:
```
url: https://cds.climate.copernicus.eu/api
key: YOUR_PERSONAL_ACCESS_TOKEN
```

**Important (2024-2025 migration):** The CDS infrastructure migrated to a new platform (CDS-Beta) in September 2024. Users must:
- Use the new CDS URL: `https://cds.climate.copernicus.eu/api`
- Use Personal Access Tokens (not the old UID:key format)
- Update API request syntax (some parameter names changed)
- Install the latest `cdsapi` package

**Installation:**
```bash
pip install cdsapi
```

**Example — download monthly mean 2m temperature:**
```python
import cdsapi

client = cdsapi.Client()

client.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': '2m_temperature',
        'year': [str(y) for y in range(2000, 2024)],
        'month': [f'{m:02d}' for m in range(1, 13)],
        'time': '00:00',
        'data_format': 'netcdf',
        'download_format': 'unarchived',
        'area': [40, -20, -40, 55],  # N, W, S, E (Africa + Europe)
    },
    'era5_monthly_t2m_africa.nc'
)
```

**Example — download daily precipitation for a region:**
```python
import cdsapi

client = cdsapi.Client()

client.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': 'total_precipitation',
        'year': '2023',
        'month': ['01', '02', '03'],
        'day': [f'{d:02d}' for d in range(1, 32)],
        'time': ['00:00', '06:00', '12:00', '18:00'],
        'data_format': 'netcdf',
        'area': [15, 30, -5, 50],  # East Africa
        'grid': [0.5, 0.5],  # Request at 0.5° for PRIO-GRID
    },
    'era5_precip_east_africa_2023_q1.nc'
)
```

**Rate limits and quotas:**
- Requests are queued; large requests may take hours
- No strict rate limit, but concurrent request limits apply
- Very large requests may be split automatically
- Monthly data is much faster to retrieve than hourly

### Method 2: Google Earth Engine (GEE)

ERA5 is available in Google Earth Engine with the following collections:

| Collection ID | Temporal | Variables |
|---------------|----------|-----------|
| `ECMWF/ERA5_LAND/HOURLY` | Hourly | 50+ land variables |
| `ECMWF/ERA5_LAND/DAILY_AGGR` | Daily | 50+ land variables |
| `ECMWF/ERA5_LAND/MONTHLY_AGGR` | Monthly | 50+ land variables |
| `ECMWF/ERA5/DAILY` | Daily | 9 atmospheric variables |
| `ECMWF/ERA5/MONTHLY` | Monthly | 9 atmospheric variables |
| `ECMWF/ERA5/HOURLY` | Hourly | 9 atmospheric variables |

**GEE limitations:**
- Only 9 atmospheric variables available (temperature, dewpoint, precipitation, pressure, wind)
- ERA5-Land has better coverage (~50 variables)
- GEE ERA5 monthly data coverage may lag (historical coverage up to ~2020 for some collections)
- No pressure-level data available

**GEE advantage:**
- No download needed — compute on Google infrastructure
- Easy spatial aggregation (e.g., to PRIO-GRID cells)
- Free for research/education/nonprofit use

### Method 3: WeatherBench / Cloud-Optimised Archives

- **WeatherBench 2:** Cloud-optimised ERA5 subset on Google Cloud Storage in Zarr format, designed for ML weather prediction benchmarks. Accessible at https://github.com/pangeo-data/WeatherBench
- **ARCO-ERA5:** Analysis-Ready, Cloud-Optimized ERA5 on Google Cloud (https://github.com/google-research/arco-era5), providing the full ERA5 archive in Zarr format — ~1 PB
- **AWS Open Data:** ERA5 available on Amazon S3 (registry.opendata.aws/ecmwf-era5/)
- **Microsoft Planetary Computer:** ERA5 available (planetarycomputer.microsoft.com/dataset/era5-pds)

### Method 4: Alternative high-level clients

```bash
pip install ecmwf-datastores-client  # New official ECMWF package with advanced features
pip install era5cli                   # Community CLI for ERA5 downloads
```

---

## 6. Schema and Data Format

### Native format: GRIB

ERA5 is natively stored in GRIB (GRIdded Binary) format, the WMO standard for meteorological data. GRIB files are self-describing and highly compressed.

### NetCDF (converted on request)

When requesting via CDS API with `'data_format': 'netcdf'`, data is served as NetCDF4/CF-compliant files.

**Typical NetCDF structure:**
```
Dimensions:
  longitude: 1440 (0.25° global)
  latitude: 721
  time: N (hourly, daily, or monthly steps)

Variables:
  t2m(time, latitude, longitude) — 2m temperature [K]
  tp(time, latitude, longitude)  — total precipitation [m]
  ...

Attributes:
  Conventions: CF-1.6
  history: "YYYY-MM-DD HH:MM:SS GMT by grib_to_netcdf-..."
```

### Working with ERA5 in Python (xarray)

```python
import xarray as xr

# Open a downloaded ERA5 NetCDF file
ds = xr.open_dataset('era5_monthly_t2m.nc')

# Convert temperature from Kelvin to Celsius
ds['t2m_celsius'] = ds['t2m'] - 273.15

# Select a specific region (East Africa)
east_africa = ds.sel(latitude=slice(15, -5), longitude=slice(30, 50))

# Compute monthly climatology
climatology = east_africa.groupby('time.month').mean('time')

# Compute anomalies
anomalies = east_africa.groupby('time.month') - climatology

# Aggregate to 0.5° for PRIO-GRID compatibility
coarsened = east_africa.coarsen(latitude=2, longitude=2, boundary='trim').mean()
```

### Handling accumulated variables

Many ERA5 variables (precipitation, radiation, evaporation) are **accumulated** from the start of the forecast. To get instantaneous rates or period totals:

```python
import xarray as xr

ds = xr.open_dataset('era5_hourly_precip.nc')

# For hourly data: precipitation is accumulated since 00:00 or 12:00
# To get hourly precipitation, take the difference between consecutive steps
hourly_precip = ds['tp'].diff('time')

# For monthly means product: values are already averaged (no differencing needed)

# Convert from metres to mm
hourly_precip_mm = hourly_precip * 1000
```

---

## 7. Quality and Known Issues

### Strengths

- **Gap-free global coverage:** Unlike station or satellite data, reanalysis fills all spatial and temporal gaps
- **Physical consistency:** All variables are dynamically consistent (energy, mass, moisture budgets approximately balanced)
- **Long record:** Back to 1940 (though pre-1979 data quality is lower due to sparse observations)
- **Uncertainty estimates:** ERA5 provides a 10-member ensemble at reduced resolution (63 km) for uncertainty quantification
- **Continuous improvement:** Benefits from advances in data assimilation and model physics since ERA-Interim

### Known issues and biases

| Issue | Detail | Impact on Causal Atlas |
|-------|--------|----------------------|
| **Tropical precipitation biases** | Largest errors in tropics; overestimates light rain, underestimates extremes; errors track ITCZ seasonally | High — affects drought/flood detection in Africa, South/Southeast Asia |
| **West African dry bias** | Difficulty resolving mesoscale convective systems | High — directly affects Sahel causal chains |
| **Southeast Asian wet bias** | Model issues with Meiyu front in July | Medium — affects East Asian analyses |
| **Extreme precipitation underestimation** | ERA5 struggles with tropical cyclones and convective extremes | Medium — use CHIRPS for precipitation-critical applications |
| **Pre-1979 data quality** | Before satellite era, fewer observations available | Low — most Causal Atlas analyses focus on post-2000 |
| **2025 production issue** | In early 2025, a technical issue caused many satellite observations to not be assimilated, affecting mainly tropical humidity | Medium — check data quality flags for Jan 2025+ |
| **Soil moisture limitations** | ERA5 soil moisture is model-derived, not directly observed | Medium — consider supplementing with SMAP satellite data |
| **Mountain precipitation** | Underperformance in high-altitude regions due to inadequate resolution of orographic effects | Medium — affects analyses in Ethiopian highlands, Andes, Himalayas |
| **Cold bias over Canadian prairies** | Near-surface temperature biases documented in winter | Low — limited impact for typical Causal Atlas regions |

### Comparison with observational datasets

| Comparison | Finding | Recommendation |
|------------|---------|----------------|
| ERA5 vs CHIRPS (precipitation) | CHIRPS generally better for Africa, especially high-altitude; ERA5 better where station density is low | Use CHIRPS as primary precipitation for Africa; ERA5 as complement |
| ERA5 vs CRU (temperature) | ERA5 shows stronger warming trends than CRU; good agreement on interannual variability | Either is suitable; ERA5 preferred for higher spatial/temporal resolution |
| ERA5 vs gauge observations | Generally good correlation (r > 0.7) for temperature; precipitation more variable by region | Validate ERA5 precipitation against local gauges when possible |
| ERA5-Land vs SMAP (soil moisture) | ERA5-Land soil moisture correlates well (r ≈ 0.69) with observations | ERA5-Land suitable for soil moisture when SMAP not available |

---

## 8. Licence and Citation

### Licence

ERA5 data is provided under the **Licence to Use Copernicus Products**, which is:
- Free of charge
- Worldwide
- Non-exclusive
- Royalty-free
- Perpetual
- Permits commercial and non-commercial use

**Important change (July 2025):** The Copernicus licence is being replaced with **Creative Commons Attribution (CC-BY)** from 2 July 2025 onwards, significantly simplifying usage terms.

### Attribution requirements

When using ERA5 data, you must acknowledge the source:

> "Generated using Copernicus Climate Change Service information [Year]."

For modified/derived products:

> "Contains modified Copernicus Climate Change Service information [Year]."

### Academic citation

Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999-2049. doi:10.1002/qj.3803

---

## 9. Storage Requirements

ERA5 is one of the largest climate datasets in existence. Storage estimates for Causal Atlas:

| Scope | Estimated size |
|-------|---------------|
| Full ERA5 archive (all variables, all levels, global) | ~5 PB |
| ERA5 hourly, 9 surface variables, global, 1979-present | ~7 TB |
| ERA5 monthly means, all single-level variables, global | ~500 GB |
| ERA5 monthly, 10 key variables, Africa only (1990-present) | ~5-10 GB |
| ERA5 monthly, 10 key variables, global, 0.5° grid (1990-present) | ~20-50 GB |
| ERA5-Land monthly, all variables, global (1950-present) | ~200 GB |

**Recommendation for Causal Atlas:**
- Start with **monthly means** for key variables (temperature, precipitation, soil moisture, wind, evaporation) at 0.5° resolution
- This is manageable at ~20-50 GB for global coverage
- Use DuckDB/Parquet for efficient querying once aggregated to PRIO-GRID
- Only download hourly/daily data for specific event studies or validation

---

## 10. Processing for PRIO-GRID Compatibility

### Aggregation from 0.25° to 0.5°

ERA5's native 0.25° grid maps cleanly to PRIO-GRID's 0.5° cells — each PRIO-GRID cell contains exactly 4 (2x2) ERA5 grid cells.

```python
import xarray as xr
import numpy as np

def era5_to_priogrid(ds, var_name, method='mean'):
    """
    Aggregate ERA5 data (0.25°) to PRIO-GRID (0.5°) resolution.

    Parameters
    ----------
    ds : xarray.Dataset
        ERA5 dataset at 0.25° resolution
    var_name : str
        Variable name to aggregate
    method : str
        'mean' for intensive variables (temperature, pressure)
        'sum' for extensive variables (precipitation, evaporation)
    """
    # Ensure latitude goes from south to north
    if ds.latitude[0] > ds.latitude[-1]:
        ds = ds.sortby('latitude')

    # Coarsen by factor of 2 in both dimensions
    if method == 'mean':
        coarsened = ds[var_name].coarsen(
            latitude=2, longitude=2, boundary='trim'
        ).mean()
    elif method == 'sum':
        coarsened = ds[var_name].coarsen(
            latitude=2, longitude=2, boundary='trim'
        ).sum()

    # Align grid cell centres to PRIO-GRID convention
    # PRIO-GRID cell centres are at 0.25° offsets (e.g., -179.75, -179.25, ...)
    # ERA5 coarsened centres should already align if starting from 0.0°

    return coarsened

# Example usage
ds = xr.open_dataset('era5_monthly_t2m.nc')
t2m_priogrid = era5_to_priogrid(ds, 't2m', method='mean')

# For precipitation (extensive variable — needs summing, not averaging)
ds_precip = xr.open_dataset('era5_monthly_precip.nc')
precip_priogrid = era5_to_priogrid(ds_precip, 'tp', method='sum')
```

**Alternative: request 0.5° directly from CDS:**
```python
client.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': '2m_temperature',
        'year': '2023',
        'month': [f'{m:02d}' for m in range(1, 13)],
        'time': '00:00',
        'data_format': 'netcdf',
        'grid': [0.5, 0.5],  # Direct 0.5° output
    },
    'era5_t2m_05deg.nc'
)
```

### Variable-specific aggregation rules

| Variable type | Aggregation method | Examples |
|---------------|-------------------|----------|
| Intensive (state) | Area-weighted mean | Temperature, pressure, humidity, soil moisture |
| Extensive (flux) | Sum | Precipitation, evaporation, runoff |
| Wind speed | Vector mean or scalar mean | u/v wind components (vector), wind speed (scalar) |
| Categorical | Mode or fraction | Cloud cover (fraction mean) |

---

## 11. Interoperability with Other Causal Atlas Datasets

### Direct complementarity

| Dataset | Relationship | Integration notes |
|---------|-------------|-------------------|
| CHIRPS | Overlapping precipitation coverage | ERA5 gap-fills where CHIRPS has missing data; CHIRPS preferred for Africa precipitation |
| PRIO-GRID v3 | Already includes ERA5-derived variables | PRIO-GRID provides pre-aggregated ERA5 temperature and precipitation |
| ACLED / UCDP | Climate→conflict causal chains | ERA5 provides environmental context for conflict events |
| WFP food prices | Climate→food price chains | Drought (via precipitation anomalies) drives food prices |
| NDVI/MODIS | Vegetation response to climate | ERA5 precipitation/temperature explain NDVI variation |
| OpenAQ | Weather→air quality chains | Wind and temperature inversions affect pollution dispersion |
| IPC food security | Climate→food security chains | ERA5 drought indicators link to IPC classifications |
| FIRMS fires | Fire weather conditions | ERA5 provides temperature, humidity, wind that drive fire risk |
| EM-DAT | Disaster context | ERA5 provides meteorological conditions for recorded disaster events |

### Shared identifiers and grids

- ERA5 at 0.5° aligns perfectly with PRIO-GRID
- ISO country codes via coordinate-to-country mapping
- Temporal alignment straightforward (ERA5 has continuous daily/monthly data)

### How VIEWS and AfroGrid use ERA5

- **VIEWS (ViEWS — Violence Early-Warning System):** Uses ERA5-derived climate variables (temperature, precipitation, drought indices) aggregated to PRIO-GRID cells as features in conflict prediction models. ERA5 is a core data source for their climate covariates.
- **AfroGrid:** Incorporates ERA5 climate data alongside conflict and socioeconomic variables, using the PRIO-GRID spatial framework. ERA5 temperature and precipitation anomalies serve as input features.
- **PRIO-GRID v3:** Directly includes ERA5-derived variables (temperature, precipitation) as standard grid-level attributes, providing ready-made PRIO-GRID-compatible ERA5 data.

---

## 12. Relevance to Causal Atlas

### Why ERA5 is essential

ERA5 is the **backbone climate dataset** for Causal Atlas. No other single dataset provides:
- Consistent, gap-free global coverage of key environmental variables
- Hourly temporal resolution (aggregable to any desired frequency)
- 80+ years of coverage (1940-present)
- Physical consistency across all variables
- Uncertainty estimates

### Priority variables for causal analysis

1. **Temperature (2m):** Heat stress → health, crop failure → food insecurity, energy demand
2. **Precipitation:** Drought/flood → agricultural disruption → displacement → conflict
3. **Soil moisture:** Agricultural drought detection, antecedent conditions for flooding
4. **Wind (10m):** Air pollution dispersion, tropical cyclone impacts
5. **Evaporation/potential evaporation:** Water stress indicators, drought severity
6. **Solar radiation:** Agricultural productivity, energy generation potential
7. **Snow depth:** Water resource availability, seasonal flood risk

### Recommended implementation approach

1. **Phase 1:** Download ERA5 monthly means for 10 key variables at 0.5° resolution (global, 1990-present) — ~20 GB
2. **Phase 2:** Compute derived indices (SPI drought index, heat wave days, anomalies)
3. **Phase 3:** Integrate with PRIO-GRID and align with other datasets
4. **Phase 4:** Use ERA5 daily/hourly for event-level analysis of specific causal chains

### Causal chains involving ERA5 variables

- Drought (low precipitation + high temperature) → crop failure → food price spikes → food insecurity → displacement → conflict
- Extreme heat → heat-related mortality → health system strain
- Wind patterns → air pollution transport → respiratory health
- Flooding (extreme precipitation) → displacement → humanitarian crisis
- Soil moisture depletion → agricultural drought → rural-urban migration
- Climate variability → pastoral livelihood disruption → resource competition → conflict

---

## Sources

- Hersbach, H., et al. (2020). The ERA5 global reanalysis. *QJRMS*, 146(730), 1999-2049. https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.3803
- CDS ERA5 single levels: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
- CDS ERA5 monthly means: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means
- ERA5 data documentation: https://confluence.ecmwf.int/display/CKB/ERA5:+data+documentation
- ERA5-Land documentation: https://confluence.ecmwf.int/display/CKB/ERA5-Land:+data+documentation
- CDS API setup: https://cds.climate.copernicus.eu/how-to-api
- cdsapi Python package: https://pypi.org/project/cdsapi/
- ERA5 in Google Earth Engine: https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_MONTHLY
- ERA5-Land in GEE: https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR
- WeatherBench 2: https://github.com/pangeo-data/WeatherBench
- ARCO-ERA5: https://github.com/google-research/arco-era5
- ERA5 on AWS: https://registry.opendata.aws/ecmwf-era5/
- Copernicus licence: https://www.copernicus.eu/en/access-data/copyright-and-licences
- CC-BY licence change: https://forum.ecmwf.int/t/cc-by-licence-to-replace-licence-to-use-copernicus-products-on-02-july-2025/13464
- Lavers et al. (2022). An evaluation of ERA5 precipitation for climate monitoring. *QJRMS*. https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/qj.4351
- Evaluation of ERA5 and CHIRPS in Ethiopia: https://link.springer.com/article/10.1007/s00703-024-01008-0
- ERA5 precipitation biases in West Africa: https://www.sciencedirect.com/science/article/abs/pii/S0169809522004136
- Climate Data Guide — ERA5: https://climatedataguide.ucar.edu/climate-data/era5-atmospheric-reanalysis
