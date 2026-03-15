# CHIRPS — Climate Hazards Group InfraRed Precipitation with Station Data

> **Last updated:** March 2025
> **Version reviewed:** CHIRPS v2.0 (primary), CHIRPS v3.0 (noted)
> **Relevance:** Core precipitation dataset for Causal Atlas drought/rainfall analysis

---

## 1. Overview

CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data) is a quasi-global, high-resolution gridded rainfall time series combining satellite imagery with in-situ station observations. It is designed specifically for drought early warning and environmental monitoring in data-sparse regions.

### Who maintains it

- **Primary developer:** Climate Hazards Center (CHC) at the University of California, Santa Barbara (UCSB)
- **Funding:** USGS (via FEWS NET — Famine Early Warning Systems Network), NASA, NOAA
- **Key personnel:** Chris Funk (PI), Pete Peterson (data engineer, pete@geog.ucsb.edu)
- **Institutional collaboration:** USGS Earth Resources Observation and Science (EROS) Center

### History and versioning

| Version | Year | Key changes |
|---------|------|-------------|
| CHIRP (no S) | 2014 | Satellite-only product (no station blending) |
| CHIRPS v1.8 | 2014 | Initial station-blended release |
| CHIRPS v2.0 | 2015 | Expanded station network, improved algorithms; current production version |
| CHIRPS v3.0 | 2024 | New precipitation algorithm, 4x station data, extended to 60°N/S; see section 1.1 |

CHIRPS v2.0 production continues through **December 2026**, after which users should migrate to v3.0.

### Methodology (CHIRPS v2.0)

CHIRPS combines five data inputs:

1. **CHPclim** — a high-resolution monthly climatology (1980-2009 baseline for v2.0) incorporating station normals, satellite averages, and physiographic predictors (elevation, latitude, longitude)
2. **CCD (Cold Cloud Duration)** — thermal infrared satellite imagery from geostationary satellites (GOES, Meteosat, GMS/MTSAT) measuring the duration of cold cloud tops as a proxy for precipitation
3. **TRMM 3B42** — used to calibrate the CCD-precipitation relationship
4. **CHPclim-adjusted CCD estimates (CHIRP)** — the satellite-only product before station blending
5. **Station observations** — from GTS (Global Telecommunication System), GSOD (Global Summary of the Day), national networks, and other sources; blended using a modified inverse distance weighting algorithm

The key innovation is using CHPclim to remove systematic bias from satellite estimates before station blending, which addresses two known problems: (a) satellite data alone underestimates extreme precipitation events, and (b) station-only grids lack coverage in rural and conflict-affected areas.

### 1.1 CHIRPS v3.0 changes

CHIRPS v3.0 (released 2024) introduces significant improvements:

- **Improved precipitation algorithm:** `CHIRP3 ~ b2 * CCD` where `b2 = (CHPclim2 + 6) / (MeanCCD + 2)`, replacing the linear approach in v2. This better captures precipitation variability, especially for high-impact storms.
- **CHPclim2:** Updated climatology baseline (1991-2020), incorporating IMERG v6 Final inputs and corrected station normals.
- **Nearly 4x more gauge data** than v2.0, with Legates-Willmott gauge-undercatch corrections.
- **Extended spatial coverage:** 60°N to 60°S (vs. 50°N to 50°S in v2).
- **COG (Cloud Optimized GeoTIFF)** format added.
- v3.0 data: <https://data.chc.ucsb.edu/products/CHIRPS/v3.0/>

---

## 2. Coverage

### Spatial extent

| Parameter | CHIRPS v2.0 | CHIRPS v3.0 |
|-----------|-------------|-------------|
| Latitude | 50°S to 50°N | 60°S to 60°N |
| Longitude | 180°W to 180°E | 180°W to 180°E |
| Land only | Yes (ocean cells are NoData) | Yes |
| Coordinate system | WGS84 (EPSG:4326) | WGS84 (EPSG:4326) |

Regional subsets are available pre-cut for:

- **Africa** — daily, pentadal, dekadal, monthly, 2-monthly, 3-monthly, 6-hourly
- **Central America & Caribbean** — dekadal, monthly, pentadal
- **Western Hemisphere** — daily
- **Indonesia** — dekadal, monthly
- **Eastern Africa** — monthly

### Temporal range

- **Start:** 1 January 1981
- **End:** Near-present (updated continuously)
- **Record length:** 44+ years as of 2025

### Update frequency

CHIRPS produces two operational products with different latencies:

| Product | Latency | Station data used |
|---------|---------|-------------------|
| **Preliminary** | ~2 days after pentad end | GTS and Conagua (Mexico) only |
| **Final** | Third week of the following month | Full station network (GTS, GSOD, national networks) |

The preliminary product is available first and is useful for near-real-time monitoring. The final product incorporates substantially more station data and should be preferred for analysis.

---

## 3. Access Methods

### 3.1 CHC Data Server (primary)

**Base URL:** <https://data.chc.ucsb.edu/products/CHIRPS-2.0/>

Supports direct HTTP download, `wget`, `curl`, and browser access. No authentication required.

#### Directory structure

```
CHIRPS-2.0/
├── README-CHIRPS.txt
├── docs/
│   ├── README-CHIRPS.txt
│   └── USGS-DS832.CHIRPS.pdf
├── diagnostics/                    # QC imagery, station density maps
├── global_daily/
│   ├── tifs/p05/YYYY/             # 0.05° daily GeoTIFF
│   ├── tifs/p25/YYYY/             # 0.25° daily GeoTIFF
│   └── netcdf/p05/               # NetCDF daily
├── global_pentad/
│   └── tifs/                      # 0.05° pentadal GeoTIFF
├── global_dekad/
│   └── tifs/                      # 0.05° dekadal GeoTIFF
├── global_monthly/
│   ├── tifs/                      # 0.05° monthly GeoTIFF
│   └── netcdf/                    # Single multi-year NetCDF (~7.1 GB)
│       ├── chirps-v2.0.monthly.nc
│       └── byYear/
├── global_annual/
│   └── tifs/                      # 0.05° annual GeoTIFF
├── africa_daily/                  # Africa subset (0.05° and 0.25°)
├── africa_dekad/
├── africa_monthly/
├── camer_daily/
└── ...
```

#### wget example — download all monthly GeoTIFFs

```bash
wget -r -np -nH --cut-dirs=3 -A '*.tif.gz' \
  https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/
```

#### wget example — download a single year of daily data

```bash
wget -r -np -nH --cut-dirs=5 -A '*.tif.gz' \
  https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/2023/
```

### 3.2 Google Earth Engine

CHIRPS is available as managed datasets in Google Earth Engine (GEE):

| Dataset | Asset ID | Temporal resolution |
|---------|----------|-------------------|
| CHIRPS Daily | `UCSB-CHG/CHIRPS/DAILY` | Daily |
| CHIRPS Pentad | `UCSB-CHG/CHIRPS/PENTAD` | 5-day |

- **Band name:** `precipitation`
- **Units:** mm/day (daily) or mm/pentad (pentad)
- **Pixel size:** 5,566 m (~0.05°)
- **Temporal extent:** 1981-01-01 to near-present

GEE is the most practical way to do server-side computation (zonal statistics, anomaly calculations) without downloading terabytes of data.

### 3.3 IRI Data Library

**URL:** <https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/>

The IRI/LDEO Climate Data Library provides subsetting, visualization, and OPeNDAP access to CHIRPS. Requires free registration. Useful for programmatic access to spatial/temporal subsets.

### 3.4 ClimateSERV

**URL:** <https://climateserv.servirglobal.net/>

Provides a web interface and API for requesting CHIRPS data for arbitrary polygons (country, admin boundaries). Useful for users who do not want to handle raw raster files.

### 3.5 CHIRPS v3.0 data server

**Base URL:** <https://data.chc.ucsb.edu/products/CHIRPS/v3.0/>

```
v3.0/
├── README-CHIRPSv3.0.txt
├── daily/
├── pentads/
├── dekads/
├── monthly/
├── annual/
├── 2-monthly/
├── 3-monthly/
├── 4-monthly/
├── 5-monthly/
├── 6-monthly/
├── diagnostics/
└── prelim/
```

---

## 4. Schema and Data Values

### Data encoding

| Property | Value |
|----------|-------|
| Data type | Float32 (GeoTIFF); Float32 or Int16 (BIL) |
| Units | Millimetres (mm) of precipitation for the time period |
| NoData / missing value | **-9999** |
| Minimum valid value | 0 |
| Maximum observed | ~1,444 mm/day (extreme events) |
| Compression | gzip for .tif.gz files; internal compression for NetCDF |

### Grid structure (0.05° resolution)

| Property | Value |
|----------|-------|
| Columns (nx) | 7,200 |
| Rows (ny) | 2,000 (v2.0, 50°S-50°N); 2,400 (v3.0, 60°S-60°N) |
| Cell size | 0.05° x 0.05° (~5.56 km at equator) |
| Registration | Grid-registered (cell centres at 0.025°, 0.075°, ...) |
| Origin | Upper-left corner at (-180.0, 50.0) for v2.0 |
| Total cells | 14,400,000 (v2.0); 17,280,000 (v3.0) |

### Grid structure (0.25° resolution)

Available for daily data only:

| Property | Value |
|----------|-------|
| Columns (nx) | 1,440 |
| Rows (ny) | 400 (v2.0) |
| Cell size | 0.25° x 0.25° (~27.8 km at equator) |

### File size estimates

| Product | Compressed (.tif.gz) | Uncompressed (.tif) |
|---------|----------------------|---------------------|
| Daily 0.05° global | ~4-6 MB | ~55 MB |
| Monthly 0.05° global | ~13.8 MB | ~55 MB |
| Annual 0.05° global | N/A | ~55 MB |
| Monthly NetCDF (all years) | N/A | ~7.1 GB |

### Storage estimate for full archive

- Daily 0.05° global, 1981-2024 (44 years x 365 days): ~16,000 files x ~5 MB = **~80 GB compressed**
- Monthly 0.05° global, 1981-2024: 528 files x ~14 MB = **~7.4 GB compressed**
- Monthly is far more manageable and sufficient for most Causal Atlas use cases

---

## 5. File Naming Conventions

### GeoTIFF files (.tif.gz)

| Aggregation | Pattern | Example |
|-------------|---------|---------|
| Daily | `chirps-v2.0.YYYY.MM.DD.tif.gz` | `chirps-v2.0.2023.06.15.tif.gz` |
| Pentadal | `chirps-v2.0.YYYY.MM.P.tif.gz` (P=1-6) | `chirps-v2.0.2023.06.3.tif.gz` |
| Dekadal | `chirps-v2.0.YYYY.MM.D.tif.gz` (D=1-3) | `chirps-v2.0.2023.06.2.tif.gz` |
| Monthly | `chirps-v2.0.YYYY.MM.tif.gz` | `chirps-v2.0.2023.06.tif.gz` |
| Annual | `chirps-v2.0.YYYY.tif` | `chirps-v2.0.2023.tif` |

### NetCDF files

- Monthly (single file): `chirps-v2.0.monthly.nc` (all years, ~7.1 GB)
- Monthly (by year): available in `netcdf/byYear/` subdirectory

### Pentad numbering convention

Each month has exactly 6 pentads:

| Pentad | Days |
|--------|------|
| 1 | 1-5 |
| 2 | 6-10 |
| 3 | 11-15 |
| 4 | 16-20 |
| 5 | 21-25 |
| 6 | 26-end of month (3-6 days) |

### Dekad numbering convention

Each month has exactly 3 dekads:

| Dekad | Days |
|-------|------|
| 1 | 1-10 |
| 2 | 11-20 |
| 3 | 21-end of month (8-11 days) |

---

## 6. Temporal Detail

### Available aggregation levels

| Level | Period | Files per year | Primary use case |
|-------|--------|---------------|------------------|
| Daily | 1 day | 365-366 | Event-level rainfall, flood analysis |
| Pentadal | 5 days | 72 | Crop monitoring, short-term drought |
| Dekadal | 10 days | 36 | Agricultural monitoring (standard for FEWS NET) |
| Monthly | 1 month | 12 | Seasonal drought analysis, climatological comparison |
| 2-monthly | 2 months | 6 | Seasonal patterns |
| 3-monthly | 3 months | 4 | Seasonal totals (e.g., MAM, OND) |
| Annual | 1 year | 1 | Long-term trends |

### Preliminary vs. final product timeline

For a given month (e.g., January 2025):

1. **Pentad 1 preliminary** available ~Feb 7 (2 days after pentad end)
2. **Pentad 2 preliminary** available ~Feb 12
3. ... (continues for each pentad)
4. **Monthly final product** available ~Feb 20 (third week of following month)

### Relationship between CHIRP and CHIRPS

- **CHIRP** (no S) = satellite-only estimates, no station blending. Available with shorter latency.
- **CHIRPS** = CHIRP + station data blending. Higher accuracy but longer latency.

---

## 7. Quality and Validation

### Known strengths

- **Long record:** 44+ years (1981-present) enables robust climatological analysis and trend detection.
- **High resolution:** 0.05° (~5.5 km) is fine enough for sub-national analysis, capturing terrain-driven rainfall gradients.
- **Station blending:** Significantly improves accuracy compared to satellite-only products, especially for capturing extreme events.
- **Designed for drought monitoring:** Optimised to detect rainfall deficits rather than capturing the full precipitation distribution.
- **Well-validated in Africa:** The primary design target for FEWS NET; extensive validation across sub-Saharan Africa.

### Known limitations and issues

1. **Station density variation:** Performance degrades in regions with sparse station networks. The diagnostics directory (`diagnostics/global_monthly_station_density/`) provides maps of station density by month/year. Station counts can vary dramatically — some regions in Central Asia, Southeast Asia, and the Pacific islands have minimal gauge input.

2. **Underestimation of extreme precipitation:** While station blending helps, CHIRPS can still underestimate extreme rainfall events, particularly convective storms. This is improved in v3.0.

3. **Temporal precipitation variance:** CHIRPS v2.0 has a known tendency to underestimate temporal precipitation variance (acknowledged in v3.0 documentation). The linear CCD-precipitation relationship in v2.0 compresses the range of estimates.

4. **Orographic precipitation:** In mountainous regions, the CHPclim climatology helps, but there can be significant errors in areas with complex terrain where gauges are sparse (e.g., Ethiopian Highlands, Himalayas, Andes).

5. **Gauge-undercatch:** Precipitation gauges systematically undercount rainfall (wind effects, wetting losses, evaporation). CHIRPS v2.0 does not correct for this; CHIRPS v3.0 applies Legates-Willmott corrections.

6. **Snowfall:** CHIRPS is designed for rainfall, not snowfall. In regions where precipitation falls as snow, CHIRPS estimates are unreliable. The 50°S-50°N extent of v2.0 partially mitigates this by excluding high latitudes.

7. **Early period data quality:** Pre-1985 data may have lower quality due to fewer satellite inputs and station observations.

8. **Island and coastal regions:** Can have artefacts due to land-sea boundaries and limited gauge data.

### Validation studies

Key published validation studies include:

- **Funk et al., 2015** — The definitive CHIRPS paper. Validation against GPCC and CPC gauge analyses showed strong correlations (r > 0.85) in most tropical and subtropical regions. Published in *Scientific Data*, 2, 150066. DOI: [10.1038/sdata.2015.66](https://doi.org/10.1038/sdata.2015.66)

- **Funk et al., 2014** — Original USGS Data Series publication (DS 832). DOI: [10.3133/ds832](https://doi.org/10.3133/ds832)

- Multiple regional validation studies exist for East Africa, West Africa, South America, and Southeast Asia, generally finding CHIRPS outperforms satellite-only products (TRMM, CMORPH) and performs comparably to or better than other blended products.

### Quality control resources

CHC provides extensive QC diagnostics at: <https://data.chc.ucsb.edu/products/CHIRPS-2.0/diagnostics/>

| Resource | Description |
|----------|-------------|
| `global_monthly_qc_pngs/` | Monthly QC imagery showing anomalies |
| `global_pentad_qc_pngs/` | Pentad-level QC imagery |
| `global_monthly_station_density/` | Maps of gauge density per month |
| `global_pentad_station_density/` | Maps of gauge density per pentad |
| `rchecks/` | "Reality checks" — station values overlaid on CHIRPS fields |
| `chirps-n-stations_byCountry/` | Station count by country over time |
| `list_of_stations_used/` | Station metadata and inventory |
| `monthly_station_data/` | Raw station observations |

---

## 8. Licence and Terms of Use

**CHIRPS is in the public domain.**

- The dataset is released under **Creative Commons CC0 / Public Domain** terms.
- No restrictions on commercial or non-commercial use.
- No authentication or API keys required for data access.
- Citation is requested but not legally required.

### Recommended citation

> Funk, C.C., Peterson, P.J., Landsfeld, M.F., Pedreros, D.H., Verdin, J.P., Rowland, J.D., Romero, B.E., Husak, G.J., Michaelsen, J.C., and Verdin, A.P., 2014, A quasi-global precipitation time series for drought monitoring: U.S. Geological Survey Data Series 832, 4 p., <https://dx.doi.org/10.3133/ds832>

And/or:

> Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A. and Michaelsen, J., 2015. The climate hazards infrared precipitation with stations — a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066. <https://doi.org/10.1038/sdata.2015.66>

---

## 9. Interoperability

### Mapping to PRIO-GRID cells

PRIO-GRID uses a 0.5° x 0.5° grid (approximately 55 km at the equator). CHIRPS native resolution is 0.05°, meaning:

- **Each PRIO-GRID cell contains exactly 100 CHIRPS cells** (10 x 10 at 0.05° resolution)
- **Each PRIO-GRID cell contains exactly 4 CHIRPS cells at 0.25° resolution** (2 x 2)
- CHIRPS grid cells align perfectly with PRIO-GRID boundaries (both are regular lat-lon grids on WGS84)
- Aggregation from CHIRPS to PRIO-GRID requires simple spatial averaging (area-weighted mean or simple mean, since at 0.5° scale the cell area difference within a PRIO-GRID cell is negligible)

#### Aggregation approach

```
PRIO-GRID cell (gid) at (row, col) maps to:
  lat_min = -90 + (row * 0.5)
  lat_max = lat_min + 0.5
  lon_min = -180 + (col * 0.5)
  lon_max = lon_min + 0.5

CHIRPS cells to average: all 0.05° cells where
  lat_min <= cell_centre_lat < lat_max
  lon_min <= cell_centre_lon < lon_max
```

### Compatibility with other datasets

| Dataset | Grid compatibility | Notes |
|---------|-------------------|-------|
| PRIO-GRID | Perfect alignment (10x10 cells per PRIO-GRID cell) | Both WGS84 regular grids |
| MODIS NDVI (250m) | Requires reprojection (MODIS uses sinusoidal) | CHIRPS is coarser; aggregate NDVI to CHIRPS grid |
| ERA5 (0.25°) | Good alignment (CHIRPS 0.25° matches directly, or 5x5 at 0.05°) | Both regular lat-lon |
| VIIRS Nightlights (500m) | Requires aggregation | Nightlights much finer resolution |
| ACLED events | Point-in-raster lookup | Assign ACLED lat/lon to containing CHIRPS cell |
| WFP food prices | Market locations → raster extraction | Extract CHIRPS value at market coordinates |
| UCDP-GED | Point-in-raster lookup | Same approach as ACLED |
| GPM IMERG (0.1°) | 2x2 CHIRPS cells per IMERG cell at 0.05° | Both regular lat-lon grids |

### Shared identifiers

CHIRPS does not use country or admin codes — it is purely gridded. Linkage to administrative boundaries requires spatial join (point-in-polygon or zonal statistics).

---

## 10. Python Access

### 10.1 Reading CHIRPS GeoTIFF with rasterio

```python
import rasterio
import numpy as np

# Read a single monthly CHIRPS GeoTIFF
with rasterio.open('chirps-v2.0.2023.06.tif') as src:
    precip = src.read(1)  # Band 1
    transform = src.transform
    crs = src.crs

    # Mask NoData values
    precip = np.where(precip == -9999, np.nan, precip)

    print(f"Shape: {precip.shape}")        # (2000, 7200) for 0.05° global
    print(f"CRS: {crs}")                   # EPSG:4326
    print(f"Resolution: {transform.a}°")   # 0.05
    print(f"Mean precip: {np.nanmean(precip):.1f} mm")
```

### 10.2 Reading CHIRPS with xarray (NetCDF)

```python
import xarray as xr

# Open the consolidated monthly NetCDF file
ds = xr.open_dataset(
    'chirps-v2.0.monthly.nc',
    chunks={'time': 12}  # Dask chunking for lazy loading
)

# Select a region and time period (e.g., East Africa, 2015-2023)
east_africa = ds['precip'].sel(
    latitude=slice(15, -12),
    longitude=slice(28, 52),
    time=slice('2015-01', '2023-12')
)

# Compute monthly climatology (1981-2010 baseline)
climatology = ds['precip'].sel(
    time=slice('1981-01', '2010-12')
).groupby('time.month').mean('time')

# Compute anomalies
anomalies = east_africa.groupby('time.month') - climatology
```

### 10.3 Reading CHIRPS GeoTIFF with xarray + rioxarray

```python
import xarray as xr
import rioxarray

# Read a single GeoTIFF as xarray
da = xr.open_dataarray('chirps-v2.0.2023.06.tif', engine='rasterio')

# Or read multiple files as a time series
import glob
files = sorted(glob.glob('chirps-v2.0.2023.*.tif'))
ds = xr.open_mfdataset(
    files,
    engine='rasterio',
    concat_dim='time',
    combine='nested'
)
```

### 10.4 Google Earth Engine Python API

```python
import ee
ee.Initialize()

# Load CHIRPS daily collection
chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')

# Monthly total for June 2023
june_2023 = chirps.filterDate('2023-06-01', '2023-07-01').sum()

# Compute long-term June average (1981-2010)
june_clim = (chirps
    .filter(ee.Filter.calendarRange(6, 6, 'month'))
    .filterDate('1981-01-01', '2011-01-01')
    .mean()
    .multiply(30)  # daily mean → monthly total
)

# Anomaly
anomaly = june_2023.subtract(june_clim)

# Extract mean precipitation for a region
region = ee.Geometry.Rectangle([28, -12, 52, 15])  # East Africa
stats = june_2023.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=region,
    scale=5566,  # CHIRPS native resolution in metres
    maxPixels=1e9
)
print(stats.getInfo())  # {'precipitation': <value>}

# Export to Google Drive as GeoTIFF
task = ee.batch.Export.image.toDrive(
    image=anomaly,
    description='chirps_anomaly_june2023',
    scale=5566,
    region=region,
    fileFormat='GeoTIFF'
)
task.start()
```

### 10.5 Downloading CHIRPS programmatically

```python
import requests
import gzip
import rasterio
from io import BytesIO

def download_chirps_monthly(year, month):
    """Download a single CHIRPS monthly GeoTIFF."""
    url = (
        f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/"
        f"global_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"
    )
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Decompress gzip
    decompressed = gzip.decompress(response.content)

    # Read with rasterio from memory
    with rasterio.open(BytesIO(decompressed)) as src:
        data = src.read(1)
        profile = src.profile

    return data, profile

# Example: download June 2023
precip, profile = download_chirps_monthly(2023, 6)
```

### 10.6 Aggregating CHIRPS to PRIO-GRID resolution

```python
import xarray as xr
import numpy as np

def aggregate_chirps_to_priogrid(chirps_da):
    """
    Aggregate 0.05° CHIRPS data to 0.5° PRIO-GRID resolution.
    Uses xarray coarsen to average 10x10 blocks of cells.

    Parameters
    ----------
    chirps_da : xr.DataArray
        CHIRPS precipitation data at 0.05° resolution.
        Expected dimensions: (time, latitude, longitude) or (latitude, longitude).

    Returns
    -------
    xr.DataArray
        Precipitation data aggregated to 0.5° resolution.
    """
    # Replace NoData with NaN
    chirps_clean = chirps_da.where(chirps_da != -9999)

    # Coarsen by factor of 10 in both spatial dimensions
    # boundary='trim' handles edge cases where grid doesn't divide evenly
    priogrid = chirps_clean.coarsen(
        latitude=10,
        longitude=10,
        boundary='trim'
    ).mean()

    return priogrid

# Usage
ds = xr.open_dataset('chirps-v2.0.monthly.nc', chunks={'time': 12})
precip_05 = ds['precip']
precip_priogrid = aggregate_chirps_to_priogrid(precip_05)

# Verify resolution
print(f"Original resolution: {precip_05.latitude.diff('latitude').values[0]:.2f}°")
print(f"Aggregated resolution: {precip_priogrid.latitude.diff('latitude').values[0]:.2f}°")
```

### 10.7 Computing Standardized Precipitation Index (SPI)

The SPI is the standard metric for classifying drought severity from precipitation data. It compares observed precipitation for a given accumulation period against a probability distribution fitted to the historical record.

#### SPI interpretation

| SPI Value | Category |
|-----------|----------|
| >= 2.0 | Extremely wet |
| 1.5 to 1.99 | Very wet |
| 1.0 to 1.49 | Moderately wet |
| -0.99 to 0.99 | Near normal |
| -1.0 to -1.49 | Moderately dry |
| -1.5 to -1.99 | Severely dry |
| <= -2.0 | Extremely dry |

Common accumulation periods: SPI-1 (1 month), SPI-3 (3 months), SPI-6 (6 months), SPI-12 (12 months).

#### Using the climate-indices Python package

```bash
pip install climate-indices
```

```python
# Command-line usage for computing SPI from CHIRPS NetCDF
# process_climate_indices \
#   --index spi \
#   --periodicity monthly \
#   --netcdf_precip chirps-v2.0.monthly.nc \
#   --var_name_precip precip \
#   --output_file_base chirps_spi \
#   --scales 1 3 6 12 \
#   --calibration_start_year 1981 \
#   --calibration_end_year 2010 \
#   --multiprocessing all
```

#### Manual SPI computation with scipy

```python
import numpy as np
from scipy.stats import gamma, norm

def compute_spi(precip_series, scale=3, calibration_period=None):
    """
    Compute Standardized Precipitation Index (SPI) for a single pixel.

    Parameters
    ----------
    precip_series : np.ndarray
        Monthly precipitation time series (mm).
    scale : int
        Accumulation period in months (e.g., 1, 3, 6, 12).
    calibration_period : tuple of int, optional
        (start_index, end_index) for fitting the gamma distribution.
        If None, uses the full series.

    Returns
    -------
    np.ndarray
        SPI values (same length as input, first scale-1 values are NaN).
    """
    # Rolling sum over the accumulation period
    accumulated = np.convolve(precip_series, np.ones(scale), mode='full')[:len(precip_series)]
    accumulated[:scale - 1] = np.nan

    # Select calibration period
    if calibration_period:
        cal = accumulated[calibration_period[0]:calibration_period[1]]
    else:
        cal = accumulated[~np.isnan(accumulated)]

    cal = cal[cal > 0]  # Gamma requires positive values

    # Fit gamma distribution to calibration data
    alpha, loc, beta = gamma.fit(cal, floc=0)

    # Compute probability of zero precipitation
    q = np.sum(precip_series == 0) / len(precip_series)

    # Transform to SPI
    spi = np.full_like(accumulated, np.nan)
    valid = ~np.isnan(accumulated)

    # For zero values: use q probability
    # For non-zero: use gamma CDF
    prob = np.where(
        accumulated[valid] == 0,
        q,
        q + (1 - q) * gamma.cdf(accumulated[valid], alpha, loc=0, scale=beta)
    )

    # Convert to standard normal
    spi[valid] = norm.ppf(prob)

    # Clip extreme values
    spi = np.clip(spi, -3.5, 3.5)

    return spi
```

### 10.8 Extracting CHIRPS values at point locations

```python
import rasterio
import pandas as pd

def extract_chirps_at_points(tif_path, points_df, lat_col='latitude', lon_col='longitude'):
    """
    Extract CHIRPS precipitation values at a set of point locations
    (e.g., ACLED events, WFP market locations).

    Parameters
    ----------
    tif_path : str
        Path to CHIRPS GeoTIFF file.
    points_df : pd.DataFrame
        DataFrame with latitude and longitude columns.

    Returns
    -------
    np.ndarray
        Precipitation values at each point location.
    """
    with rasterio.open(tif_path) as src:
        coords = list(zip(points_df[lon_col], points_df[lat_col]))
        values = np.array([val[0] for val in src.sample(coords)])
        values = np.where(values == -9999, np.nan, values)
    return values

# Example: extract CHIRPS for ACLED event locations
# acled = pd.read_csv('acled_events.csv')
# acled['precip_mm'] = extract_chirps_at_points(
#     'chirps-v2.0.2023.06.tif', acled
# )
```

---

## 11. Relevance to Causal Atlas

CHIRPS is one of the most important datasets for Causal Atlas due to precipitation's central role in multiple causal chains:

### Causal pathways where CHIRPS is critical

1. **Rainfall deficit → drought → crop failure → food insecurity → conflict**
   - This is the most-studied causal chain in the climate-conflict literature.
   - SPI computed from CHIRPS is the standard drought indicator used by FEWS NET.
   - Lag structures: rainfall deficit → crop failure (1-3 months), food insecurity (3-6 months), conflict (6-12 months). These vary by region and livelihood system.

2. **Rainfall excess → flooding → displacement → disease outbreaks**
   - Extreme positive precipitation anomalies can be detected from CHIRPS.
   - Links to EM-DAT flood events and disease outbreak data.

3. **Rainfall variability → pastoral migration → resource competition → conflict**
   - In the Sahel and Horn of Africa, pastoralist movement patterns follow rainfall.
   - CHIRPS anomalies correlate with changes in NDVI (vegetation), which drives migration.

4. **Rainfall → NDVI / vegetation → agricultural output → economic indicators**
   - CHIRPS + MODIS NDVI together provide a powerful picture of agricultural conditions.
   - Can be linked to FAO crop production data and WFP food price monitoring.

5. **Long-term precipitation trends → climate adaptation stress → governance pressure**
   - The 44-year CHIRPS record enables trend analysis (Mann-Kendall, Sen's slope).
   - Declining rainfall trends can be correlated with governance indicators.

### Recommended integration approach for Causal Atlas

1. **Primary temporal resolution:** Monthly (sufficient for most causal analyses, manageable data volume)
2. **Primary spatial resolution:** Aggregate to 0.5° PRIO-GRID cells
3. **Derived variables to compute:**
   - Monthly precipitation totals (raw CHIRPS)
   - SPI-1, SPI-3, SPI-6, SPI-12 (drought severity at multiple time scales)
   - Precipitation anomalies relative to 1981-2010 climatology
   - Number of dry days per month (from daily data, if available)
   - Onset/cessation of rainy season (from pentadal data)
4. **Storage format:** Parquet or DuckDB table with columns: `(year, month, prio_gid, precip_mm, spi1, spi3, spi6, spi12, precip_anomaly_pct)`
5. **Update cadence:** Monthly, using final CHIRPS product (~3 weeks after month end)

### Version recommendation

- **For analysis starting in 2025:** Use CHIRPS v2.0, which has the longest validation track record and widest tool support.
- **Plan migration to v3.0** before December 2026 (v2.0 end of production). v3.0 offers meaningful improvements in precipitation variability estimation and station density.
- The 50°S-50°N extent of v2.0 covers all regions of primary interest for Causal Atlas (tropics and subtropics where climate-conflict nexus is most studied).

---

## 12. Sources and References

### Primary publications

1. Funk, C.C., Peterson, P.J., Landsfeld, M.F., et al., 2014. A quasi-global precipitation time series for drought monitoring. *USGS Data Series 832*, 4 p. <https://dx.doi.org/10.3133/ds832>

2. Funk, C., Peterson, P., Landsfeld, M., et al., 2015. The climate hazards infrared precipitation with stations — a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066. <https://doi.org/10.1038/sdata.2015.66>

### Data access URLs

| Resource | URL |
|----------|-----|
| CHC CHIRPS landing page | <https://www.chc.ucsb.edu/data/chirps> |
| CHIRPS v2.0 data server | <https://data.chc.ucsb.edu/products/CHIRPS-2.0/> |
| CHIRPS v3.0 data server | <https://data.chc.ucsb.edu/products/CHIRPS/v3.0/> |
| CHIRPS FAQ | <https://wiki.chc.ucsb.edu/CHIRPS_FAQ> |
| GEE CHIRPS Daily | <https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY> |
| GEE CHIRPS Pentad | <https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_PENTAD> |
| ClimateSERV | <https://climateserv.servirglobal.net/> |
| IRI Data Library | <https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/> |
| CHIRPS v2.0 README | <https://data.chc.ucsb.edu/products/CHIRPS-2.0/README-CHIRPS.txt> |
| CHIRPS v2.0 diagnostics | <https://data.chc.ucsb.edu/products/CHIRPS-2.0/diagnostics/> |
| CHC Early Warning Explorer (EWX) | <https://ewx3.chc.ucsb.edu/> |
| USGS DS 832 publication | <https://pubs.usgs.gov/ds/832/> |

### Python packages

| Package | Purpose | Install |
|---------|---------|---------|
| `rasterio` | Read GeoTIFF files | `pip install rasterio` |
| `xarray` | NetCDF and multi-dimensional array operations | `pip install xarray` |
| `rioxarray` | xarray extension for rasterio/GeoTIFF | `pip install rioxarray` |
| `earthengine-api` | Google Earth Engine Python API | `pip install earthengine-api` |
| `climate-indices` | SPI, SPEI, Palmer indices | `pip install climate-indices` |
| `dask` | Parallel/lazy computation for large arrays | `pip install dask` |

### Contact

- **Pete Peterson** (CHIRPS data engineer): pete@geog.ucsb.edu
- **Climate Hazards Center:** <https://www.chc.ucsb.edu/>
