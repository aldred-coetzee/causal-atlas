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

---

## 13. CHIRPS-GEFS: Forecast Extension

> **Last checked:** March 2025

### 13.1 Overview

CHIRPS-GEFS is a bias-corrected and downscaled version of the NCEP Global Ensemble Forecast System (GEFS) v12 precipitation forecasts. It provides 5-day to 15-day precipitation forecasts that are directly compatible with CHIRPS historical data, enabling seamless blending of observed and forecast rainfall for early warning applications.

**Key publication:** Funk, C., et al. (2022). "Advancing early warning capabilities with CHIRPS-compatible NCEP GEFS precipitation forecasts." *Scientific Data*, 9, 295. DOI: [10.1038/s41597-022-01468-2](https://doi.org/10.1038/s41597-022-01468-2)

### 13.2 How It Works

1. **Raw GEFS forecasts** (0.25° resolution, ensemble of 31 members) are obtained from NCEP
2. **Bias correction:** GEFS climatological biases are removed using the CHPclim2 climatology, the same used in CHIRPS — this ensures compatibility between forecast and observed products
3. **Downscaling:** The bias-corrected forecasts are downscaled from 0.25° to 0.05° using the CHPclim2 high-resolution climatology as a guide
4. **Output:** Daily precipitation forecasts at 0.05° resolution for the next ~15 days, aggregated to 5-day, 10-day, and 15-day totals and anomalies

### 13.3 Data Products

| Product | Description | Update frequency |
|---------|-------------|-----------------|
| 5-day forecast totals | Cumulative precipitation for next 5 days | ~Every 5 days |
| 10-day forecast totals | Cumulative precipitation for next 10 days | ~Every 5 days |
| 15-day forecast totals | Cumulative precipitation for next 15 days | ~Every 5 days |
| 5/10/15-day anomalies | Departure from climatological average | ~Every 5 days |
| Reforecasts (Phase 2) | Historical reforecasts 2000–2019 | Static archive |

### 13.4 Access

| Resource | URL |
|----------|-----|
| CHC CHIRPS-GEFS page | <https://chc.ucsb.edu/data/chirps-gefs> |
| Data repository (DOI) | <https://doi.org/10.15780/G2PH2M> |
| Operational data server | <https://data.chc.ucsb.edu/products/EWX/data/forecasts/CHIRPS-GEFS_precip/> |
| Reforecasts (2000–2019) | <https://data.chc.ucsb.edu/products/EWX/data/forecasts/CHIRPS-GEFS_precip_reforecast/> |
| Early Warning eXplorer (EWX) | <https://ewx3.chc.ucsb.edu/> |
| ClimateSERV | <https://climateserv.servirglobal.net/> |
| FAO Catalog entry | <https://data.apps.fao.org/catalog/dataset/fd93b304-c926-491e-af67-d31649fbcf78> |

- **Format:** GeoTIFF
- **Resolution:** 0.05° × 0.05° (same as CHIRPS)
- **Extent:** 50°S to 50°N (matching CHIRPS v2.0)
- **No authentication required**

### 13.5 Operational Use at FEWS NET

CHIRPS-GEFS maps and time series graphics are updated every ~5 days and show:
- Recent CHIRPS-observed precipitation
- 15-day outlook using GEFS forecasts
- Combined observed + forecast rainfall anomalies for the current season

This enables FEWS NET analysts to assess whether current rainfall deficits are likely to persist or improve, directly informing food security outlooks.

### 13.6 Relevance to Causal Atlas

CHIRPS-GEFS extends Causal Atlas from purely retrospective analysis into **near-future forecasting**. By combining CHIRPS historical data with CHIRPS-GEFS forecasts:
- We can project SPI/SPEI values 2–3 weeks into the future
- This enables early warning of emerging drought conditions before they appear in monthly CHIRPS data
- Forecast accuracy degrades with lead time, so CHIRPS-GEFS is most useful for 5–10 day outlooks

---

## 14. CHIRTS: Temperature Companion Datasets

> **Last checked:** March 2025

### 14.1 Overview

The Climate Hazards Center InfraRed Temperature with Stations (CHIRTS) datasets are companion products to CHIRPS, providing high-resolution temperature data using a similar methodology of combining satellite infrared observations with station data.

**Key publication:** Verdin, A., et al. (2020). "Development and validation of the CHIRTS-daily quasi-global high-resolution daily temperature data set." *Scientific Data*, 7, 303. DOI: [10.1038/s41597-020-00643-7](https://doi.org/10.1038/s41597-020-00643-7)

### 14.2 Products

| Product | Variable | Resolution | Temporal range | Temporal resolution |
|---------|----------|------------|----------------|---------------------|
| **CHIRTSmax** (monthly) | Maximum 2m temperature | 0.05° × 0.05° | 1983–2016 | Monthly |
| **CHIRTSmin** (monthly) | Minimum 2m temperature | 0.05° × 0.05° | 1983–2016 | Monthly |
| **CHIRTS-daily** (v1) | Tmax, Tmin, SVP, VPD, RH, Heat Index | 0.05° × 0.05° | 1983–2016 | Daily |
| **CHIRTS-ERA5** | Tmax, Tmin, Heat Index, WBGT | 0.05° × 0.05° | 1980–near present | Daily |

### 14.3 Methodology

1. **CHIRTSmax/min (monthly):** Combines thermal infrared satellite data (providing land surface temperature proxies) with station-based maximum/minimum air temperatures, using a climatology (CHTclim) similar in concept to CHPclim for CHIRPS
2. **CHIRTS-daily:** Merges monthly CHIRTSmax data with daily temperature variations from ERA5 reanalysis to produce daily Tmax and Tmin at 0.05° resolution
3. **CHIRTS-ERA5:** An updated version that extends to near-present by continuously incorporating ERA5 reanalysis updates

### 14.4 Derived Variables (CHIRTS-daily)

| Variable | Abbreviation | Description |
|----------|-------------|-------------|
| Maximum temperature | Tmax | Maximum daily 2m air temperature (°C) |
| Minimum temperature | Tmin | Minimum daily 2m air temperature (°C) |
| Saturation Vapour Pressure | SVP | Computed from Tmax/Tmin (kPa) |
| Vapour Pressure Deficit | VPD | SVP minus actual vapour pressure (kPa) |
| Relative Humidity | RH | Percentage relative humidity |
| Heat Index | HI | Perceived temperature under shade (°C) |
| Wet Bulb Globe Temperature | WBGT | Heat stress metric (CHIRTS-ERA5 only) |

### 14.5 Access

| Resource | URL |
|----------|-----|
| CHC CHIRTS-daily page | <https://www.chc.ucsb.edu/data/chirtsdaily> |
| CHC CHIRTSmonthly page | <https://www.chc.ucsb.edu/data/chirtsmonthly> |
| Data server (CHIRTS-daily) | <https://data.chc.ucsb.edu/products/CHIRTSdaily/> |
| Data server (CHIRTSmax monthly) | <https://data.chc.ucsb.edu/products/CHIRTSmax/> |
| Data server (CHIRTSmin monthly) | <https://data.chc.ucsb.edu/products/CHIRTSmin/> |
| Google Earth Engine | `UCSB-CHG/CHIRTS/DAILY` |

- **Licence:** Public domain (CC0)
- **No authentication required**

### 14.6 Google Earth Engine Access

```javascript
// Load CHIRTS-daily
var chirts = ee.ImageCollection('UCSB-CHG/CHIRTS/DAILY');

// Get maximum temperature for a date range
var tmax = chirts.filterDate('2015-06-01', '2015-06-30')
    .select('tmax')
    .mean();

// Compute monthly mean maximum temperature for East Africa
var region = ee.Geometry.Rectangle([28, -12, 52, 15]);
var stats = tmax.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: region,
  scale: 5566,
  maxPixels: 1e9
});
print(stats);
```

### 14.7 Relevance to Causal Atlas

CHIRTS is essential for Causal Atlas because:

1. **SPEI computation:** SPEI requires potential evapotranspiration (PET) in addition to precipitation. PET can be computed from CHIRTS Tmax/Tmin using the Hargreaves equation — meaning CHIRPS + CHIRTS together provide all inputs needed for SPEI
2. **Heat stress → health:** Extreme Tmax and Heat Index values can be correlated with health outcomes (heatstroke, mortality)
3. **Heat stress → agriculture:** High temperatures during critical crop growth stages cause yield loss; CHIRTS enables grid-cell level analysis
4. **VPD → wildfire risk:** Vapour pressure deficit is a key driver of fire weather conditions
5. **Temperature → disease vectors:** Mosquito-borne disease transmission rates depend on temperature; CHIRTS provides the resolution needed for sub-national analysis

---

## 15. Comparison with Other Precipitation Products

> **Last checked:** March 2025

### 15.1 Product Summary

| Product | Resolution | Coverage | Period | Source type | Open access |
|---------|-----------|----------|--------|-------------|-------------|
| **CHIRPS v2.0** | 0.05° | 50°S–50°N, land | 1981–present | Satellite IR + gauges | Yes |
| **CHIRPS v3.0** | 0.05° | 60°S–60°N, land | 1981–present | Satellite IR + gauges (4x more) | Yes |
| **GPM IMERG** | 0.1° | 60°S–60°N | 2000–present (v7) | Multi-satellite (PMW+IR) + gauges | Yes |
| **TAMSAT v3.1** | 0.0375° | Africa only | 1983–present | Satellite IR + gauges (Africa focused) | Yes |
| **ARC2** | 0.1° | Africa, 40°S–40°N | 1983–present | Satellite IR + GTS gauges | Yes |
| **MSWEP v2.8** | 0.1° | Global | 1979–present | Multi-source (satellite, reanalysis, gauges) | Conditional |
| **ERA5** | 0.25° (~31 km) | Global | 1940–present | Reanalysis | Yes |
| **PERSIANN-CDR** | 0.25° | 60°S–60°N | 1983–present | Satellite IR + neural network | Yes |

### 15.2 Quantified Accuracy Differences (Africa)

Based on multi-scale validation studies over Africa (Satgé et al., 2023; Ageet et al., 2022; Dinku et al., 2018):

#### Monthly Scale Performance (KGE — Kling-Gupta Efficiency, higher is better)

| Product | Northern Africa | Western Africa | Eastern Africa | Southern Africa | Central Africa |
|---------|----------------|----------------|----------------|-----------------|----------------|
| CHIRPS v2.0 | Moderate | Good | **Best** | Good | Good |
| MSWEP v2.8 | **Best** | Good | Good | Good | Good |
| RFE v2.0 | Good | **Best** | Good | Good | Good |
| ARC v2.0 | Good | Good | Good | Good | **Best** |
| IMERG-F v6B | Moderate | Moderate | Good | Good | Good |
| ERA5 | Poor–Moderate | Moderate | Poor–Moderate | Moderate | Moderate |
| TAMSAT v3.1 | N/A (Africa only) | Poor–Moderate | Moderate | Moderate | Moderate |

#### Daily Scale Performance

At the daily timescale, performance patterns shift:
- **RFE, ARC2, CPC** yield the highest KGE scores at the daily timestep
- **TAMSAT** performs better than CHIRPS at the daily timescale in some West African basins
- **CHIRPS** daily performance is moderate — it is optimised for monthly/pentadal use
- **IMERG-F** is most reliable for detecting heavy and high-intensity rainfall events at all spatial scales

#### Drought Detection Capability

- **CHIRPS v2.0** and **ARC v2.0** are the most reliable products for detecting dry conditions (< 1 mm/day) across all 19 spatial scales tested — indicating **high confidence for drought studies**, which is Causal Atlas's primary use case
- **IMERG-F v6B** excels at detecting extreme rainfall events

#### Key Regional Findings

**East Africa (Dinku et al., 2018):**
- CHIRPS validation against ENACTS (national enhanced observations) showed strong correlations at monthly scale (r > 0.85)
- CHIRPS significantly outperforms ARC2, with higher skill and low or no bias
- Performance degrades in complex terrain (Ethiopian Highlands) and coastal areas

**Ethiopia (Evaluation, 2024):**
- CHIRPS outperforms ERA5 in high-altitude areas
- CHIRPS has better capability detecting high-intensity rainfall events than ERA5
- Validated against 167 rain gauges

**West Africa (Tarek et al., 2022):**
- CHIRPS is the most effective product for hydrological modelling at monthly timestep
- Performance weakens in coastal and mountainous regions

**Trans-African (Ageet et al., 2022):**
- Validation using 6 years of rain gauge data from 596 TAHMO stations
- CHIRPS daily mean rainfall bias over Africa: 15.5% (0.5 mm)
- CHIRPS correlations stratified across East, Southern, and West Africa at daily, pentadal, and monthly scales — improving substantially at longer aggregation periods

### 15.3 When to Prefer Each Product

| Use case | Recommended product | Rationale |
|----------|-------------------|-----------|
| Monthly drought monitoring, Africa | **CHIRPS** | Best drought detection, long record (1981+), 0.05° resolution |
| Daily flood analysis, Africa | **IMERG** or **RFE** | Better daily accuracy, better extreme event detection |
| Global analysis | **MSWEP** | Consistently high accuracy globally, multi-source fusion |
| Africa-specific at highest resolution | **TAMSAT** | 0.0375° resolution, tailored for Africa; but lower accuracy than CHIRPS |
| Reanalysis / model forcing | **ERA5** | Full global coverage, hourly data, but large wet bias in tropics |
| Longest possible record | **CHIRPS** or **PERSIANN-CDR** | Both start 1983; CHIRPS from 1981 |

### 15.4 Key References

- Satgé, F., et al. (2023). "Accuracy of satellite and reanalysis rainfall estimates over Africa: A multi-scale assessment of eight products for continental applications." *Journal of Hydrology: Regional Studies*. <https://www.sciencedirect.com/science/article/pii/S221458182300201X>
- Ageet, S., et al. (2022). "Validation and Intercomparison of Satellite-Based Rainfall Products over Africa with TAHMO In Situ Rainfall Observations." *Journal of Hydrometeorology*, 23(7). <https://journals.ametsoc.org/view/journals/hydr/23/7/JHM-D-21-0161.1.xml>
- Dinku, T., et al. (2018). "Validation of the CHIRPS satellite rainfall estimates over eastern Africa." *Quarterly Journal of the Royal Meteorological Society*, 144(S1), 292–312. DOI: [10.1002/qj.3244](https://doi.org/10.1002/qj.3244)
- Beck, H.E., et al. (2024). "Global-scale evaluation of precipitation datasets for hydrological modelling." *Hydrology and Earth System Sciences*, 28, 3099–3118. <https://hess.copernicus.org/articles/28/3099/2024/>

---

## 16. SPI at Multiple Timescales — Full Python Code

> **Last checked:** March 2025

### 16.1 Using the `climate-indices` Package (Recommended for Production)

The `climate-indices` package (maintained by NIDIS / Drought.gov) is the most robust open-source implementation, supporting SPI with gamma and Pearson Type III distributions, plus SPEI and Palmer drought indices.

```bash
pip install climate-indices
```

#### Command-Line: Compute SPI at 1, 3, 6, 12 Month Scales

```bash
process_climate_indices \
  --index spi \
  --periodicity monthly \
  --netcdf_precip chirps-v2.0.monthly.nc \
  --var_name_precip precip \
  --output_file_base chirps_spi \
  --scales 1 3 6 12 \
  --calibration_start_year 1981 \
  --calibration_end_year 2010 \
  --multiprocessing all
```

This produces four output NetCDF files:
- `chirps_spi_gamma_01.nc` (SPI-1)
- `chirps_spi_gamma_03.nc` (SPI-3)
- `chirps_spi_gamma_06.nc` (SPI-6)
- `chirps_spi_gamma_12.nc` (SPI-12)

#### Programmatic: Compute SPI for a Single Grid Cell

```python
from climate_indices import indices, compute

import numpy as np

# Monthly precipitation for a single grid cell, starting January 1981
precip_monthly = np.array([...])  # shape: (n_months,)

# Compute SPI-3 using gamma distribution
spi3 = indices.spi(
    values=precip_monthly,
    scale=3,
    distribution=indices.Distribution.gamma,
    data_start_year=1981,
    calibration_year_initial=1981,
    calibration_year_final=2010,
    periodicity=compute.Periodicity.monthly,
)
```

### 16.2 Using the `spei` Package (Lightweight Alternative)

```bash
pip install spei
```

```python
import pandas as pd
from spei import spi

# Load CHIRPS monthly data for a single grid cell as a pandas Series
precip = pd.Series(
    data=[...],  # monthly precipitation values in mm
    index=pd.date_range('1981-01', periods=528, freq='ME'),
    name='precip_mm'
)

# Compute SPI at multiple scales
spi_1 = spi(precip, dist='gamma', timescale=1, cal_start='1981-01', cal_end='2010-12')
spi_3 = spi(precip, dist='gamma', timescale=3, cal_start='1981-01', cal_end='2010-12')
spi_6 = spi(precip, dist='gamma', timescale=6, cal_start='1981-01', cal_end='2010-12')
spi_12 = spi(precip, dist='gamma', timescale=12, cal_start='1981-01', cal_end='2010-12')
```

### 16.3 Grid-Scale SPI Computation with xarray + Dask

For computing SPI across the full CHIRPS grid (millions of cells), parallelisation with Dask is essential:

```python
import xarray as xr
import numpy as np
from scipy.stats import gamma, norm
import dask

def compute_spi_gridcell(precip_series, scale, cal_start_idx, cal_end_idx):
    """Compute SPI for a single grid cell time series."""
    n = len(precip_series)
    if np.all(np.isnan(precip_series)):
        return np.full(n, np.nan)

    # Rolling sum
    accumulated = np.convolve(precip_series, np.ones(scale), mode='full')[:n]
    accumulated[:scale - 1] = np.nan

    # Calibration period
    cal_data = accumulated[cal_start_idx:cal_end_idx]
    cal_data = cal_data[~np.isnan(cal_data)]
    cal_positive = cal_data[cal_data > 0]

    if len(cal_positive) < 30:
        return np.full(n, np.nan)

    # Probability of zero
    q = np.sum(cal_data == 0) / len(cal_data) if len(cal_data) > 0 else 0

    # Fit gamma
    try:
        alpha, _, beta = gamma.fit(cal_positive, floc=0)
    except Exception:
        return np.full(n, np.nan)

    spi = np.full(n, np.nan)
    valid = ~np.isnan(accumulated)

    prob = np.where(
        accumulated[valid] == 0,
        q,
        q + (1 - q) * gamma.cdf(accumulated[valid], alpha, loc=0, scale=beta)
    )
    # Clamp probabilities to avoid infinities
    prob = np.clip(prob, 1e-6, 1 - 1e-6)
    spi[valid] = norm.ppf(prob)
    spi = np.clip(spi, -3.5, 3.5)

    return spi

def compute_spi_grid(ds, var_name='precip', scale=3,
                     cal_start='1981-01', cal_end='2010-12'):
    """
    Compute SPI across the full CHIRPS grid using xarray.apply_ufunc.
    """
    precip = ds[var_name]
    times = pd.DatetimeIndex(precip.time.values)

    cal_start_idx = np.searchsorted(times, pd.Timestamp(cal_start))
    cal_end_idx = np.searchsorted(times, pd.Timestamp(cal_end)) + 1

    spi_da = xr.apply_ufunc(
        compute_spi_gridcell,
        precip,
        input_core_dims=[['time']],
        output_core_dims=[['time']],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float],
        kwargs={'scale': scale,
                'cal_start_idx': cal_start_idx,
                'cal_end_idx': cal_end_idx},
    )

    spi_da.name = f'spi_{scale}'
    spi_da.attrs['long_name'] = f'Standardized Precipitation Index ({scale}-month)'
    spi_da.attrs['calibration_period'] = f'{cal_start} to {cal_end}'

    return spi_da

# Usage
ds = xr.open_dataset('chirps-v2.0.monthly.nc', chunks={'time': -1, 'latitude': 50, 'longitude': 50})
spi3 = compute_spi_grid(ds, scale=3)
spi3.to_netcdf('chirps_spi3.nc')
```

---

## 17. SPEI Computation

> **Last checked:** March 2025

### 17.1 What SPEI Adds Over SPI

The **Standardized Precipitation Evapotranspiration Index (SPEI)** extends SPI by incorporating temperature effects on drought through potential evapotranspiration (PET). While SPI only considers precipitation, SPEI accounts for how rising temperatures increase evaporative demand, making it a better indicator of agricultural drought under climate change.

**SPEI = SPI methodology applied to (Precipitation − PET) instead of Precipitation alone**

### 17.2 Computing PET from CHIRTS Temperature Data

The Hargreaves equation is the simplest PET method requiring only Tmax and Tmin (available from CHIRTS):

```python
import numpy as np

def hargreaves_pet(tmax, tmin, lat, doy):
    """
    Compute daily potential evapotranspiration using Hargreaves equation.

    Parameters
    ----------
    tmax : float or array
        Daily maximum temperature (°C)
    tmin : float or array
        Daily minimum temperature (°C)
    lat : float
        Latitude in degrees
    doy : int
        Day of year (1-366)

    Returns
    -------
    float or array
        PET in mm/day
    """
    # Mean temperature
    tmean = (tmax + tmin) / 2.0

    # Temperature range
    trange = np.maximum(tmax - tmin, 0)

    # Extraterrestrial radiation (Ra) approximation
    lat_rad = np.radians(lat)
    dr = 1 + 0.033 * np.cos(2 * np.pi * doy / 365)
    delta = 0.409 * np.sin(2 * np.pi * doy / 365 - 1.39)
    ws = np.arccos(-np.tan(lat_rad) * np.tan(delta))
    ws = np.clip(ws, 0, np.pi)

    Ra = (24 * 60 / np.pi) * 0.0820 * dr * (
        ws * np.sin(lat_rad) * np.sin(delta) +
        np.cos(lat_rad) * np.cos(delta) * np.sin(ws)
    )

    # Hargreaves equation
    pet = 0.0023 * Ra * (tmean + 17.8) * np.sqrt(trange)
    pet = np.maximum(pet, 0)

    return pet
```

### 17.3 Full SPEI Computation

```python
from climate_indices import indices, compute

# Monthly precipitation from CHIRPS (mm)
precip_monthly = np.array([...])

# Monthly PET computed from CHIRTS using Hargreaves (mm)
pet_monthly = np.array([...])

# Compute SPEI-3 using Pearson Type III distribution
spei3 = indices.spei(
    values_precip=precip_monthly,
    values_pet=pet_monthly,
    scale=3,
    distribution=indices.Distribution.pearson,
    data_start_year=1983,  # CHIRTS starts 1983
    calibration_year_initial=1983,
    calibration_year_final=2010,
    periodicity=compute.Periodicity.monthly,
)
```

### 17.4 When to Use SPEI vs SPI

| Scenario | Recommended | Rationale |
|----------|-------------|-----------|
| Precipitation-only drought monitoring | SPI | Simpler, longer record (CHIRPS starts 1981) |
| Agricultural drought under warming | **SPEI** | Captures temperature-driven evaporative stress |
| Health impact analysis (heat + drought) | **SPEI** | Integrates both climate stressors |
| Comparison with historical baselines | SPI | Fewer assumptions, more comparable across studies |
| Climate change projections | **SPEI** | Temperature trend is a first-order driver |

### 17.5 References

- Vicente-Serrano, S.M., Beguería, S., & López-Moreno, J.I. (2010). "A Multiscalar Drought Index Sensitive to Global Warming: The Standardized Precipitation Evapotranspiration Index." *Journal of Climate*, 23(7), 1696–1718.
- Global SPEI Database: <https://spei.csic.es/>
- Drought.gov Python tools: <https://www.drought.gov/data-maps-tools/climate-and-drought-indices-python-spi-spei-pet>
- `climate-indices` documentation: <https://climate-indices.readthedocs.io/>
- `spei` PyPI package: <https://pypi.org/project/spei/>
- `standard_precip` GitHub: <https://github.com/e-baumer/standard_precip>

---

## 18. Data Quality Flags and Handling

> **Last checked:** March 2025

### 18.1 CHIRPS Quality Control Pipeline

CHIRPS does not use traditional data quality flags in its output files (the raster values are simply precipitation in mm, or -9999 for NoData/ocean). However, the production pipeline applies extensive QC to station inputs before blending.

#### False Zero Detection

The most significant QC challenge in CHIRPS is **"false zeros"** — missing station values incorrectly coded as zero precipitation in GTS and GSOD automated networks. CHIRPS v3.0 addresses this with explicit screening:

- **Daily level:** If a GTS/GSOD station reports 0 on a day when the satellite-only CHIRP3 estimate exceeds the long-term (1991–2020) average daily rainfall intensity at that pixel, the station value is treated as **missing** rather than zero
- **Pentadal level:** If a station reports 0 for a pentad but CHIRP indicates ≥ 7 mm, the station is treated as missing
- **Monthly level:** If a station reports 0 for a month but CHIRP indicates ≥ 20 mm, the station is treated as missing

#### Extreme Value Screening

Automatic QC routines screen station data for:
- **Standardised anomalies exceeding ±4σ** — flagged and excluded
- **Very large absolute values** — flagged and excluded
- **Ratios > 5× the CHIRP satellite estimate** — flagged and excluded

These extreme values are not used in the CHIRPS blending process.

#### Station Anchor Selection

- A new station is added to the processing set only if there is not already an "anchor station" within 5 km
- If an anchor station already exists within 5 km, the new station is flagged for use only as a gap-filler at the anchor station location

#### Reality Checks (R-Checks)

The "Reality Checks" process is a hands-on quality assessment where:
1. CHIRPS fields are examined visually via the Early Warning Explorer (EWX)
2. Station values are overlaid on CHIRPS fields to check for spatial consistency
3. Ancillary information (FEWS NET datasets, news reports, national meteorological reports) is used to validate results
4. Statistics are calculated to identify suspect areas

### 18.2 Diagnostics Resources

CHC publishes extensive QC diagnostics that users should consult when working with CHIRPS data in specific regions:

| Resource | Location | Purpose |
|----------|----------|---------|
| Station density maps | `diagnostics/global_monthly_station_density/` | Assess gauge coverage for your region/period |
| Station count by country | `diagnostics/chirps-n-stations_byCountry/` | Track station availability trends |
| Monthly QC imagery | `diagnostics/global_monthly_qc_pngs/` | Visual anomaly detection |
| Reality Checks | `diagnostics/rchecks/` | Station vs. CHIRPS field comparisons |
| Station list | `diagnostics/list_of_stations_used/` | Identify which stations contribute to your area |
| Raw station data | `diagnostics/monthly_station_data/` | Independent validation source |

**CHIRPS v2 diagnostics:** <https://data.chc.ucsb.edu/products/CHIRPS-2.0/diagnostics/>
**CHIRPS v3 diagnostics:** <https://www.chc.ucsb.edu/data/chirps3/diagnostics>

### 18.3 Best Practices for Handling CHIRPS Data Quality

1. **Always check station density** for your study region and period before drawing conclusions. Regions with <5 stations per PRIO-GRID cell may have substantially more uncertainty.
2. **Use final products** (not preliminary) for any research analysis — preliminary products use only GTS stations and can miss significant local precipitation.
3. **Distinguish NoData from zero** — -9999 means no data (ocean, outside coverage); 0.0 means the model estimated zero precipitation.
4. **Compare preliminary and final** for recent months to assess the value of additional station data in your region.
5. **Cross-validate with IMERG or ARC2** in regions where CHIRPS station density is poor (Central Africa, Pacific islands, Central Asia).

---

## 19. Detailed File Size and Storage Planning

> **Last checked:** March 2025

### 19.1 File Sizes by Product

| Product | Single file (compressed .tif.gz) | Single file (uncompressed .tif) | Note |
|---------|----------------------------------|--------------------------------|------|
| Daily 0.05° global | 4–6 MB | ~55 MB (Float32, 7200×2000) | Size varies with land precipitation coverage |
| Daily 0.25° global | ~0.5 MB | ~2.3 MB (Float32, 1440×400) | |
| Pentadal 0.05° global | ~6–8 MB | ~55 MB | Higher values → less compressible |
| Dekadal 0.05° global | ~8–10 MB | ~55 MB | |
| Monthly 0.05° global | ~13–14 MB | ~55 MB | |
| Annual 0.05° global | ~20 MB (uncompressed) | ~55 MB | Not always gzipped |
| Monthly NetCDF (all years) | N/A | ~7.1 GB | Single file covering 1981–present |

### 19.2 Full Archive Storage Estimates

| Archive | Files | Compressed size | Uncompressed size |
|---------|-------|----------------|-------------------|
| Daily 0.05° global (1981–2025, 44 years) | ~16,060 | **~80 GB** | **~880 GB** |
| Daily 0.25° global (1981–2025) | ~16,060 | **~8 GB** | **~37 GB** |
| Monthly 0.05° global (1981–2025) | ~528 | **~7.4 GB** | **~29 GB** |
| Monthly 0.05° Africa only (1981–2025) | ~528 | **~2 GB** | **~8 GB** |
| Pentadal 0.05° global (1981–2025) | ~3,168 | **~25 GB** | **~174 GB** |
| CHIRPS v3.0 monthly (1981–2025) | ~528 | **~9 GB** (est.) | **~35 GB** (est., larger rows for 60°S–60°N) |

### 19.3 Causal Atlas Storage Recommendation

For Causal Atlas, the recommended data pipeline is:

1. **Download monthly 0.05° global** (compressed): ~7.4 GB — very manageable
2. **Aggregate to PRIO-GRID (0.5°)** resolution: reduces data volume by 100× to ~74 MB for entire 44-year archive
3. **Store as Parquet**: Further compressed, entire monthly PRIO-GRID precipitation archive fits in **<50 MB**
4. **Keep daily 0.25°** for Africa only if daily analysis is needed: ~3 GB compressed
5. **Use Google Earth Engine** for ad-hoc analysis at full 0.05° resolution to avoid local storage

---

## 20. Google Earth Engine: PRIO-GRID Aggregation

> **Last checked:** March 2025

### 20.1 Server-Side Aggregation to 0.5° Grid Cells

```javascript
// ==========================================
// CHIRPS Monthly Aggregation to PRIO-GRID
// Google Earth Engine JavaScript API
// ==========================================

// 1. Define the PRIO-GRID as a regular 0.5° grid
// Create a grid image where each pixel represents a PRIO-GRID cell
var gridImage = ee.Image.pixelLonLat()
  .multiply(2).floor().divide(2);  // Snap to 0.5° grid

var gridId = gridImage.select('longitude')
  .multiply(1000)
  .add(gridImage.select('latitude'));

// 2. Load CHIRPS daily data
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY');

// 3. Compute monthly totals for a given year
var year = 2023;
var months = ee.List.sequence(1, 12);

var monthlyTotals = ee.ImageCollection(months.map(function(month) {
  var start = ee.Date.fromYMD(year, month, 1);
  var end = start.advance(1, 'month');

  var monthlySum = chirps.filterDate(start, end)
    .sum()
    .rename('precip_mm');

  return monthlySum
    .set('year', year)
    .set('month', month)
    .set('system:time_start', start.millis());
}));

// 4. Aggregate a single month to PRIO-GRID resolution
var juneTotal = monthlyTotals.filter(ee.Filter.eq('month', 6)).first();

// Resample to 0.5° using mean aggregation
var priogridPrecip = juneTotal
  .reduceResolution({
    reducer: ee.Reducer.mean(),
    maxPixels: 100,        // 10x10 CHIRPS cells per PRIO-GRID cell
    bestEffort: true
  })
  .reproject({
    crs: 'EPSG:4326',
    scale: 55660           // ~0.5° in metres
  });

// 5. Export PRIO-GRID aggregated data
// Option A: Export as GeoTIFF
Export.image.toDrive({
  image: priogridPrecip,
  description: 'chirps_priogrid_2023_06',
  scale: 55660,
  region: ee.Geometry.Rectangle([-180, -50, 180, 50]),
  fileFormat: 'GeoTIFF',
  maxPixels: 1e9
});

// Option B: Export as table (CSV with grid cell values)
// First create a FeatureCollection from the grid
var region = ee.Geometry.Rectangle([28, -12, 52, 15]); // East Africa

var priogridFC = priogridPrecip.sample({
  region: region,
  scale: 55660,
  geometries: true
});

Export.table.toDrive({
  collection: priogridFC,
  description: 'chirps_priogrid_eastafrica_2023_06',
  fileFormat: 'CSV'
});
```

### 20.2 Python API: Batch Processing Multiple Months

```python
import ee
import pandas as pd

ee.Initialize()

def get_chirps_priogrid_monthly(year, month, region_bounds):
    """
    Aggregate CHIRPS monthly precipitation to PRIO-GRID resolution
    using Google Earth Engine server-side computation.

    Parameters
    ----------
    year : int
    month : int
    region_bounds : list [lon_min, lat_min, lon_max, lat_max]

    Returns
    -------
    pd.DataFrame with columns: longitude, latitude, precip_mm
    """
    chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')

    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')

    monthly_total = chirps.filterDate(start, end).sum().rename('precip_mm')

    # Aggregate to 0.5°
    priogrid = monthly_total.reduceResolution(
        reducer=ee.Reducer.mean(),
        maxPixels=100,
        bestEffort=True
    ).reproject(crs='EPSG:4326', scale=55660)

    # Sample values
    region = ee.Geometry.Rectangle(region_bounds)
    samples = priogrid.sample(
        region=region,
        scale=55660,
        geometries=True
    )

    # Extract to pandas
    data = samples.getInfo()
    rows = []
    for f in data['features']:
        coords = f['geometry']['coordinates']
        rows.append({
            'longitude': coords[0],
            'latitude': coords[1],
            'precip_mm': f['properties']['precip_mm']
        })

    return pd.DataFrame(rows)

# Example: East Africa, all months of 2023
east_africa = [28, -12, 52, 15]
all_months = []
for month in range(1, 13):
    df = get_chirps_priogrid_monthly(2023, month, east_africa)
    df['year'] = 2023
    df['month'] = month
    all_months.append(df)

result = pd.concat(all_months, ignore_index=True)
result.to_parquet('chirps_priogrid_eastafrica_2023.parquet')
```

---

## 21. FEWS NET Operational Use of CHIRPS

> **Last checked:** March 2025

### 21.1 FEWS NET Overview

The **Famine Early Warning Systems Network (FEWS NET)** is a USAID-funded early warning system that provides evidence-based analysis on food insecurity in over 30 countries. CHIRPS was developed specifically to serve FEWS NET's operational needs, and remains a core data input to FEWS NET's monitoring pipeline.

### 21.2 How CHIRPS Fits in the FEWS NET Pipeline

```
Satellite IR observations (Meteosat, GOES)
    ↓
CCD (Cold Cloud Duration) estimates
    ↓
CHPclim bias correction
    ↓
CHIRP (satellite-only product, ~2 day latency)
    ↓ + Station data (GTS, GSOD, national networks)
CHIRPS (blended product, ~3 week latency)
    ↓
Derived products:
├── Rainfall anomalies (% of normal)
├── SPI at multiple timescales
├── Onset/cessation of rainy season
├── Cumulative seasonal rainfall
└── CHIRPS-GEFS forecast extension (15-day outlook)
    ↓
Combined with NDVI, LST, crop models, market data
    ↓
FEWS NET Food Security Outlook (3-month projection)
    ↓
IPC-compatible food security classification
```

### 21.3 FEWS NET Data Products Using CHIRPS

| Product | Description | Platform |
|---------|-------------|----------|
| Rainfall estimate maps | Dekadal, monthly, seasonal CHIRPS totals and anomalies | EWX, FEWS NET |
| Agroclimatology data | CHIRPS rainfall combined with NDVI and LST | <https://fews.net/data/agroclimatology-data> |
| USGS EROS CHIRPS downloads | Regional subsets formatted for FEWS NET analysts | <https://earlywarning.usgs.gov/fews/datadownloads/Global/CHIRPS%202.0> |
| Seasonal rainfall accumulation | Oct–May and other season-specific accumulations | <https://earlywarning.usgs.gov/fews/product/600/> |
| ClimateSERV | Polygon-based CHIRPS extraction for specific admin areas | <https://climateserv.servirglobal.net/> |

### 21.4 Key Insight for Causal Atlas

FEWS NET's operational pipeline demonstrates that CHIRPS, combined with NDVI and food price data, has **proven predictive value for food insecurity** at lead times of 2–6 months. This validates the core Causal Atlas hypothesis that climate data (via rainfall anomalies) can be causally linked to food security outcomes through crop production and market price transmission mechanisms. The specific lag structures used by FEWS NET (dekadal monitoring → seasonal projection → 3-month food security outlook) provide empirical calibration points for our own time-lagged correlation analysis.
