# 06 — Data Integration Techniques for Heterogeneous Spatiotemporal Data

> **Last updated:** March 2025
> **Status:** Deep research — pre-implementation
> **Relevance:** Core to Causal Atlas ingestion pipeline design

---

## Table of Contents

1. [Spatial Resolution Mismatch](#1-spatial-resolution-mismatch)
2. [Area-Weighted Interpolation](#2-area-weighted-interpolation)
3. [Point-to-Grid Aggregation](#3-point-to-grid-aggregation)
4. [Raster-to-Grid Resampling](#4-raster-to-grid-resampling)
5. [Temporal Alignment](#5-temporal-alignment)
6. [Missing Data Handling](#6-missing-data-handling)
7. [The PRIO-GRID Approach](#7-the-prio-grid-approach)
8. [The AfroGrid Approach](#8-the-afrogrid-approach)
9. [How HungerMapLIVE Integrates Sources](#9-how-hungermaplive-integrates-sources)
10. [Admin-to-Grid Mapping](#10-admin-to-grid-mapping)
11. [Coordinate Reference Systems](#11-coordinate-reference-systems)
12. [Data Versioning and Provenance](#12-data-versioning-and-provenance)
13. [Recommended Pipeline for Causal Atlas](#13-recommended-pipeline-for-causal-atlas)

---

## 1. Spatial Resolution Mismatch

The fundamental challenge in cross-domain spatiotemporal analysis is that data sources use incompatible spatial representations. Our target is a PRIO-GRID-compatible 0.5 x 0.5 degree grid (roughly 55 km x 55 km at the equator), but incoming data arrives in at least four distinct spatial forms.

### 1.1 The Four Spatial Data Types

| Type | Examples | Native format | Challenge |
|------|----------|---------------|-----------|
| **Point events** | ACLED conflicts, USGS earthquakes, WFP market prices | Lat/lon coordinates | Must aggregate into grid cells; event density varies wildly |
| **Raster grids** | CHIRPS rainfall (0.05 deg), MODIS NDVI (250m-1km), VIIRS nightlights (500m) | Regular grid, various resolutions | Must resample to 0.5 deg; some finer, some coarser than target |
| **Admin regions** | World Bank GDP, WHO disease data, FAO crop statistics | Irregular polygons (country, province, district) | Must disaggregate or apportion to grid cells; boundaries change over time |
| **Irregular polygons** | Land cover classes, conflict zones, flood extents | Vector polygons of varying size | Must compute overlay with grid cells |

### 1.2 Resolution Hierarchy

```
Source resolution          Target
─────────────────────────  ──────────────
MODIS NDVI (250m)          ─┐
VIIRS nightlights (500m)   ─┤
CHIRPS rainfall (0.05°)    ─┼─ Aggregate ──► 0.5° × 0.5° grid cell
CRU climate (0.5°)         ─┤              (PRIO-GRID compatible)
WorldPop (1km)             ─┘

Country-level GDP          ─┐
Province-level health      ─┼─ Disaggregate ──► 0.5° × 0.5° grid cell
District food prices       ─┘

Conflict events (points)   ─── Bin/count ──► 0.5° × 0.5° grid cell
```

### 1.3 Key Principle: Distinguish Extensive vs. Intensive Variables

This distinction is critical and affects every spatial operation:

- **Extensive (count-like) variables:** Population, number of conflict events, total rainfall (mm accumulated), GDP. When a spatial unit is split, the value must be **divided proportionally** (e.g., half the area gets half the population).
- **Intensive (rate-like) variables:** Temperature, rainfall rate (mm/hr), NDVI, population density, prevalence rate. When a spatial unit is split, the value **stays the same** in each part (or is averaged).

Getting this wrong produces systematic errors. A grid cell that overlaps two admin regions should receive the area-weighted **sum** of population from each region, but the area-weighted **average** of temperature.

---

## 2. Area-Weighted Interpolation

Area-weighted interpolation (also called areal interpolation) is the method for transferring attribute values from one set of polygons (source zones) to another (target zones). This is the workhorse technique for admin-to-grid conversion.

### 2.1 Mathematical Foundation

Given source polygons $S_1, S_2, \ldots, S_n$ and a target polygon $T$:

**For extensive variables** (e.g., population):

$$\hat{V}_T = \sum_{i=1}^{n} V_{S_i} \cdot \frac{|S_i \cap T|}{|S_i|}$$

Where $|S_i \cap T|$ is the area of intersection between source polygon $S_i$ and target $T$, and $|S_i|$ is the total area of source polygon $S_i$.

Interpretation: each source polygon contributes a share of its value proportional to the fraction of its area that falls within the target.

**For intensive variables** (e.g., temperature, density):

$$\hat{V}_T = \sum_{i=1}^{n} V_{S_i} \cdot \frac{|S_i \cap T|}{|T|}$$

Where $|T|$ is the total area of the target polygon. This computes the area-weighted average.

### 2.2 Dasymetric Refinement

Pure area-weighted interpolation assumes uniform distribution within source zones, which is often unrealistic (e.g., population is concentrated in cities, not evenly spread across a province). Dasymetric interpolation incorporates ancillary data to improve estimates:

- **Binary dasymetric:** Use a mask (e.g., land cover) to exclude uninhabitable areas. Population is apportioned only across the habitable fraction.
- **Intelligent dasymetric:** Use continuous ancillary data (e.g., nighttime lights as a proxy for population density) to weight the allocation.

For population disaggregation, nighttime lights or WorldPop gridded estimates are excellent ancillary layers.

### 2.3 Python Implementation with Tobler

[Tobler](https://github.com/pysal/tobler) is the PySAL package specifically designed for areal interpolation. It provides three families of methods: simple area-weighted, dasymetric (binary and multi-class), and model-based interpolation.

```python
import geopandas as gpd
from tobler.area_weighted import area_interpolate

# Load source polygons (e.g., admin regions with population data)
source = gpd.read_file("admin_regions.gpkg")

# Load target polygons (our PRIO-GRID cells)
target = gpd.read_file("priogrid_cells.gpkg")

# Ensure both are in the same CRS (important!)
source = source.to_crs("EPSG:4326")
target = target.to_crs("EPSG:4326")

# Extensive variable (population counts — will be summed proportionally)
result = area_interpolate(
    source_df=source,
    target_df=target,
    extensive_variables=["population"],
    intensive_variables=["temperature_avg"]
)
# result is a GeoDataFrame with target geometries and interpolated values
```

**Dasymetric interpolation with Tobler:**

```python
from tobler.dasymetric import masked_area_interpolate

# Binary mask: only interpolate into areas classified as inhabited
result = masked_area_interpolate(
    source_df=source,
    target_df=target,
    extensive_variables=["population"],
    raster="land_cover.tif",       # ancillary raster
    codes=[1, 2, 3],               # land cover classes considered habitable
    nan_value=0                    # value for uninhabited target cells
)
```

### 2.4 When to Use

- **Best for:** Admin-region data (GDP, health stats, food prices) to grid cells
- **Requires:** Both source and target as polygon geometries
- **Limitation:** Assumes uniform distribution within source zones (mitigated by dasymetric approach)
- **Performance consideration:** Tobler leverages shapely for multicore architecture, but intersection computation can be expensive for many polygons. Pre-compute the source-target intersection weights once and cache them.

### 2.5 Pitfalls

- **CRS mismatch:** Source and target must be in the same CRS before computing intersections. Use EPSG:4326 for our grid, but be aware that area calculations in geographic coordinates are approximate. For precise area ratios, project to an equal-area CRS (e.g., Mollweide EPSG:54009) for the intersection calculation, then apply weights to geographic geometries.
- **Slivers and topology errors:** Polygon intersections can produce tiny sliver polygons due to floating-point imprecision. Use `buffer(0)` on geometries before intersection to fix invalid geometries.
- **Boundary changes:** Admin boundaries change over time. A province that splits in 2015 will have different polygons before and after. Must use the correct vintage of boundaries for each time period.
- **Coastlines and water bodies:** Grid cells along coastlines include ocean area. When apportioning, only the land area should count. Clip source polygons to a land mask first.

---

## 3. Point-to-Grid Aggregation

Point events (conflict incidents, earthquake epicentres, market price observations) must be assigned to grid cells. There are several approaches with different trade-offs.

### 3.1 Simple Binning (Point-in-Polygon)

The most common approach: assign each point to the grid cell it falls within, then count events per cell per time period.

```python
import geopandas as gpd
import pandas as pd

# Load point events
events = gpd.read_file("acled_events.csv")
events = gpd.GeoDataFrame(
    events,
    geometry=gpd.points_from_xy(events.longitude, events.latitude),
    crs="EPSG:4326"
)

# Load PRIO-GRID cells
grid = gpd.read_file("priogrid_cells.gpkg")

# Spatial join: assign each event to a grid cell
joined = gpd.sjoin(events, grid, how="left", predicate="within")

# Aggregate: count events per grid cell per month
monthly_counts = (
    joined.groupby(["grid_cell_id", "year_month"])
    .agg(
        event_count=("event_id", "count"),
        fatalities=("fatalities", "sum"),
        fatalities_mean=("fatalities", "mean")
    )
    .reset_index()
)
```

**Performance optimisation with spatial indexing:**

For large event datasets (ACLED has >1 million events), the naive spatial join is slow. Use a spatial index:

```python
# H3 hexagonal indexing for fast point-to-cell assignment
import h3

def latlon_to_priogrid_cell(lat, lon, resolution=0.5):
    """Convert lat/lon to PRIO-GRID cell ID.

    PRIO-GRID cells are indexed by their southwest corner.
    Cell (i, j) covers: lon in [i*0.5 - 180, (i+1)*0.5 - 180)
                         lat in [j*0.5 - 90,  (j+1)*0.5 - 90)
    """
    col = int((lon + 180) / resolution)
    row = int((lat + 90) / resolution)
    return row * 720 + col  # 720 columns in a 0.5-degree global grid

# Vectorized assignment (much faster than spatial join for regular grids)
events["grid_cell_id"] = events.apply(
    lambda r: latlon_to_priogrid_cell(r.latitude, r.longitude), axis=1
)
```

### 3.2 Kernel Density Estimation (KDE)

Instead of hard assignment to a single cell, KDE spreads each event's influence across neighbouring cells using a kernel function. This produces smoother surfaces and handles positional uncertainty.

$$\hat{f}(x) = \frac{1}{nh} \sum_{i=1}^{n} K\left(\frac{x - x_i}{h}\right)$$

Where $K$ is a kernel function (typically Gaussian), $h$ is the bandwidth, and $x_i$ are event locations.

```python
from scipy.stats import gaussian_kde
import numpy as np

# Create KDE from event coordinates
coords = np.vstack([events.longitude, events.latitude])
kde = gaussian_kde(coords, bw_method=0.5)  # bandwidth in degrees

# Evaluate on grid cell centres
grid_lons = np.arange(-179.75, 180, 0.5)
grid_lats = np.arange(-89.75, 90, 0.5)
lon_grid, lat_grid = np.meshgrid(grid_lons, grid_lats)
positions = np.vstack([lon_grid.ravel(), lat_grid.ravel()])

density = kde(positions).reshape(lon_grid.shape)
```

**When to use KDE vs. simple binning:**

| Criterion | Simple binning | KDE |
|-----------|---------------|-----|
| Interpretability | Easy: "X events in this cell" | Harder: "density estimate" |
| Positional uncertainty | Ignores it | Naturally handles it |
| Sparse data | Many empty cells | Smoother surface |
| Computation | Fast | Slower for large N |
| Appropriate for | Precise event data (ACLED) | Imprecise or sparse data |

### 3.3 Distance-Weighted Aggregation

A middle ground: assign events to cells but weight by distance from cell centre. Useful for market price data where price influence decays with distance.

```python
from scipy.spatial import cKDTree

# Build KD-tree from grid cell centres
grid_centres = np.column_stack([grid.centroid.x, grid.centroid.y])
tree = cKDTree(grid_centres)

# For each event, find k nearest grid cells and compute distance weights
k = 4  # number of cells to distribute to
distances, indices = tree.query(
    np.column_stack([events.longitude, events.latitude]),
    k=k
)

# Inverse distance weights (avoid division by zero)
weights = 1.0 / np.maximum(distances, 1e-10)
weights = weights / weights.sum(axis=1, keepdims=True)  # normalize to sum to 1

# Distribute each event's value across neighbouring cells
for event_idx in range(len(events)):
    for j in range(k):
        cell_idx = indices[event_idx, j]
        w = weights[event_idx, j]
        grid.loc[cell_idx, "weighted_value"] += events.iloc[event_idx]["value"] * w
```

### 3.4 Handling Geocoding Precision

Many conflict and humanitarian datasets report events at varying levels of geographic precision. ACLED and UCDP-GED both include a `geo_precision` field:

| Precision level | Meaning | Recommended handling |
|-----------------|---------|---------------------|
| 1 | Exact location | Assign to cell directly |
| 2 | Nearest named location | Assign to cell, flag uncertainty |
| 3 | Admin-2 centroid | Spread across admin-2 area or exclude |
| 4 | Admin-1 centroid | Spread across admin-1 area or exclude |

AfroGrid excludes events with precision worse than district level (precision > 2), which is a defensible choice. Alternatively, low-precision events can be area-weighted across the relevant admin unit.

---

## 4. Raster-to-Grid Resampling

Much of our data (satellite imagery, climate reanalyses, gridded population) arrives as raster grids at various resolutions. We need to resample everything to our 0.5-degree target grid.

### 4.1 Downsampling (Higher Resolution to 0.5 Degrees)

Most satellite-derived data is finer than 0.5 degrees and must be aggregated. The correct method depends on the variable type.

**Area-weighted mean (for intensive variables):**

Each target cell's value is the weighted mean of all source pixels that overlap it, weighted by the fraction of the source pixel within the target cell. This is the most accurate method for continuous fields like temperature or NDVI.

$$\hat{V}_T = \frac{\sum_{i} w_i \cdot V_i}{\sum_{i} w_i}$$

where $w_i$ is the area of overlap between source pixel $i$ and target cell $T$.

**Area-weighted sum (for extensive variables):**

For count data like population:

$$\hat{V}_T = \sum_{i} V_i \cdot \frac{|P_i \cap T|}{|P_i|}$$

**Implementation with exactextract (recommended):**

[exactextract](https://github.com/isciences/exactextract) is the gold standard for raster zonal statistics. Unlike simpler implementations, it correctly handles pixels that are partially covered by polygon boundaries, computing exact fractional coverage rather than using pixel centroids.

```python
from exactextract import exact_extract
import rasterio
import geopandas as gpd

# Load high-resolution raster
raster_path = "chirps_rainfall_0.05deg.tif"

# Load target PRIO-GRID cells as polygons
grid = gpd.read_file("priogrid_cells.gpkg")

# Compute area-weighted mean for intensive variable (rainfall rate)
result = exact_extract(
    raster_path,
    grid,
    ["mean", "min", "max", "stdev", "count"],
    include_cols=["grid_cell_id"],
    output="pandas"
)

# For extensive variable (population sum)
pop_result = exact_extract(
    "worldpop_1km.tif",
    grid,
    ["sum"],
    include_cols=["grid_cell_id"],
    output="pandas"
)
```

**Why exactextract over rasterio zonal_stats:**

exactextract computes the exact fraction of each pixel covered by each polygon using computational geometry, giving 10-100x better performance and more accurate results than approaches that use pixel centroid containment tests. This matters most for small or irregular polygons where many pixels are partially covered.

### 4.2 Upsampling (Coarser Resolution to 0.5 Degrees)

Some data (e.g., certain climate reanalysis products at 1 or 2.5 degrees) is coarser than our target. We must interpolate to finer resolution, acknowledging that no new information is created.

**Bilinear interpolation:**

Uses the four nearest source pixels. The value at target point $(x, y)$ is:

$$f(x, y) = (1-s)(1-t) f_{00} + s(1-t) f_{10} + (1-s)t f_{01} + st f_{11}$$

where $s$ and $t$ are the fractional positions within the source pixel, and $f_{00}, f_{10}, f_{01}, f_{11}$ are the four surrounding source values.

**Cubic convolution:**

Uses a 4x4 neighbourhood of source pixels. Smoother than bilinear but can introduce ringing artifacts near sharp transitions. Generally preferred for continuous fields.

**Nearest neighbour:**

Simply assigns the value of the closest source pixel. Preserves original values (no blending). Use for categorical data (land cover class) or when maintaining exact values matters more than smoothness.

**Implementation with rioxarray:**

```python
import xarray as xr
import rioxarray
from rasterio.enums import Resampling

# Open coarse-resolution dataset
ds = xr.open_dataset("era5_temperature_1deg.nc")
ds = ds.rio.set_crs("EPSG:4326")
ds = ds.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude")

# Create a reference grid at 0.5-degree resolution
# (or load one from an existing file)
target = xr.open_dataarray("priogrid_reference.tif")

# Reproject to match target grid
resampled = ds.rio.reproject_match(
    target,
    resampling=Resampling.bilinear  # or .cubic, .nearest
)
```

**Implementation with rasterio directly:**

```python
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject, calculate_default_transform
import numpy as np

src_path = "coarse_data_1deg.tif"
dst_path = "resampled_0.5deg.tif"

with rasterio.open(src_path) as src:
    # Calculate transform for 0.5-degree target
    dst_transform, dst_width, dst_height = calculate_default_transform(
        src.crs, src.crs,
        720, 360,  # 720 cols x 360 rows for 0.5-degree global grid
        left=-180, bottom=-90, right=180, top=90
    )

    dst_meta = src.meta.copy()
    dst_meta.update({
        "transform": dst_transform,
        "width": 720,
        "height": 360
    })

    with rasterio.open(dst_path, "w", **dst_meta) as dst:
        for band in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, band),
                destination=rasterio.band(dst, band),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs=src.crs,
                resampling=Resampling.bilinear
            )
```

### 4.3 Resampling Method Selection Guide

| Variable type | Downsampling (fine to coarse) | Upsampling (coarse to fine) |
|--------------|-------------------------------|----------------------------|
| Continuous, intensive (temperature, NDVI) | Area-weighted mean | Bilinear or cubic |
| Continuous, extensive (population) | Area-weighted sum | Bilinear (with caution) |
| Categorical (land cover class) | Majority (mode) | Nearest neighbour |
| Binary (presence/absence) | Fraction (proportion of 1s) | Nearest neighbour |
| Extremes matter (max rainfall) | Area-weighted max | Nearest neighbour |

### 4.4 Pitfalls

- **Edge alignment:** Ensure source and target grids share cell boundaries where possible. A 0.05-degree grid divides evenly into 0.5-degree cells (10x10 source pixels per target cell), making aggregation clean. A 0.042-degree grid does not divide evenly, creating partial-pixel issues at cell boundaries.
- **NoData handling:** When aggregating, decide how to treat NoData pixels. For mean calculations, exclude them (don't treat as zero). Track the fraction of valid pixels per target cell as a quality indicator.
- **Reprojection before resampling:** If the source raster is in a different CRS, reproject first, then resample. Combining both operations in a single `reproject()` call is cleaner than doing them separately.
- **Antimeridian (dateline) wrapping:** Global rasters may have the antimeridian at the left edge (0-360 longitude) or in the middle (-180 to 180). Standardize to -180 to 180 before processing.

---

## 5. Temporal Alignment

### 5.1 The Temporal Mismatch Problem

| Data source | Native temporal resolution | Update frequency |
|-------------|---------------------------|------------------|
| ACLED conflict events | Daily (event date) | Weekly |
| CHIRPS rainfall | Daily or pentadal (5-day) | Monthly release |
| MODIS NDVI | 16-day composites | Continuous |
| CRU climate | Monthly | Annual release |
| World Bank indicators | Annual | Annual |
| USGS earthquakes | Instantaneous (origin time) | Near-real-time |
| WFP food prices | Monthly or irregular | Varies by market |
| VIIRS nightlights | Daily or monthly composites | Monthly |

Our target temporal unit is **monthly** (following PRIO-GRID convention), with daily data preserved where available for lag analysis.

### 5.2 Aggregation Strategies

**Daily to monthly:**

```python
import pandas as pd
import xarray as xr

# For tabular event data (e.g., ACLED)
events["event_date"] = pd.to_datetime(events["event_date"])
events["year_month"] = events["event_date"].dt.to_period("M")

monthly = events.groupby(["grid_cell_id", "year_month"]).agg(
    event_count=("event_id", "count"),
    fatalities_sum=("fatalities", "sum"),
    fatalities_max=("fatalities", "max"),
    first_event=("event_date", "min"),
    last_event=("event_date", "max")
).reset_index()

# For xarray gridded data (e.g., daily rainfall)
ds = xr.open_dataset("chirps_daily.nc")

# Sum for accumulated rainfall, mean for average temperature
monthly_precip = ds["precip"].resample(time="1MS").sum(skipna=True)
monthly_temp = ds["temp"].resample(time="1MS").mean(skipna=True)
monthly_temp_max = ds["temp"].resample(time="1MS").max(skipna=True)
```

**16-day composite to monthly (MODIS NDVI):**

MODIS produces 23 composites per year, with start dates that don't align with calendar months. Options:

```python
# Option 1: Assign each composite to the month containing its midpoint
ndvi = xr.open_dataset("modis_ndvi_16day.nc")
# Each composite's time stamp is already the start of the 16-day window
# Resample by taking the mean of composites that fall within each month
monthly_ndvi = ndvi.resample(time="1MS").mean()

# Option 2: Time-weighted average
# Weight each composite by how many of its 16 days fall in each month
# More accurate but more complex
import numpy as np

def weighted_monthly_mean(ds, var_name):
    """Compute monthly means weighted by temporal overlap."""
    monthly = []
    for year in range(ds.time.dt.year.min().item(),
                      ds.time.dt.year.max().item() + 1):
        for month in range(1, 13):
            month_start = pd.Timestamp(year, month, 1)
            month_end = month_start + pd.offsets.MonthEnd(1)

            weights = []
            values = []
            for t in ds.time.values:
                comp_start = pd.Timestamp(t)
                comp_end = comp_start + pd.Timedelta(days=15)

                overlap_start = max(comp_start, month_start)
                overlap_end = min(comp_end, month_end)
                overlap_days = max(0, (overlap_end - overlap_start).days + 1)

                if overlap_days > 0:
                    weights.append(overlap_days)
                    values.append(ds[var_name].sel(time=t))

            if weights:
                w = np.array(weights) / sum(weights)
                weighted_val = sum(v * wi for v, wi in zip(values, w))
                weighted_val = weighted_val.assign_coords(time=month_start)
                monthly.append(weighted_val)

    return xr.concat(monthly, dim="time")
```

**Annual to monthly (constant fill):**

For annual data (World Bank GDP, annual population estimates), the standard approach is to assign the annual value to all 12 months of that year. This is what PRIO-GRID and AfroGrid do.

```python
# Repeat annual value across all months
annual_data = pd.DataFrame({
    "grid_cell_id": [1, 1],
    "year": [2020, 2021],
    "gdp_per_capita": [1500, 1600]
})

# Expand to monthly
months = pd.date_range("2020-01", "2021-12", freq="MS")
monthly_index = pd.MultiIndex.from_product(
    [annual_data["grid_cell_id"].unique(), months],
    names=["grid_cell_id", "month"]
)
monthly_gdp = (
    annual_data.set_index(["grid_cell_id", "year"])
    .reindex(monthly_index, method=None)
)
# Forward-fill within each cell
monthly_gdp = monthly_gdp.groupby(level=0).ffill()
```

### 5.3 Handling Irregular Observations

Some data (e.g., WFP market prices) arrives at irregular intervals. Markets may report monthly, quarterly, or with gaps.

**Strategies:**
1. **Forward fill (last observation carried forward):** Assume the price remains unchanged until the next observation. Simple and conservative.
2. **Linear interpolation:** Assume smooth change between observations. Better for slowly-varying quantities.
3. **Mark as missing:** If the gap exceeds a threshold (e.g., 3 months), mark as NaN rather than interpolating.

```python
# Forward-fill with a maximum gap
prices = prices.sort_values(["market_id", "date"])
prices = prices.set_index("date")
prices_monthly = prices.groupby("market_id").resample("MS").first()
prices_monthly["price"] = prices_monthly.groupby("market_id")["price"].ffill(limit=3)
# Gaps > 3 months remain NaN
```

### 5.4 Lag Preservation

For causal analysis, preserving sub-monthly timing can be important. If drought onset occurred on March 5 and conflict spiked on March 28, a monthly aggregation loses this within-month lag structure.

**Recommendation:** Store daily event data alongside monthly aggregates. Use daily data for lag discovery (via cross-correlation or Granger causality) and monthly data for spatial panel analysis.

### 5.5 Calendar and Time Zone Considerations

- **UTC standardization:** All timestamps should be converted to UTC. ACLED event dates are local dates; earthquake origin times are UTC.
- **Month boundary alignment:** Use the first day of the month (`freq="MS"` in pandas) rather than the last day. Be consistent.
- **Islamic/Ethiopian calendars:** Some data sources from specific regions use non-Gregorian calendars. Convert to Gregorian on ingestion.

---

## 6. Missing Data Handling

Missing data is ubiquitous in spatiotemporal datasets. Satellite imagery has cloud gaps. Conflict data is absent where monitoring is impossible. Economic data is missing for failed states. Each type of missingness requires different treatment.

### 6.1 Types of Missingness in Spatiotemporal Context

| Type | Meaning | Example | Treatment |
|------|---------|---------|-----------|
| **MCAR** (Missing Completely at Random) | Missingness unrelated to any variable | Random cloud cover | Safe to interpolate or impute |
| **MAR** (Missing at Random) | Missingness related to observed variables | More cloud cover in tropics | Conditional interpolation works |
| **MNAR** (Missing Not at Random) | Missingness related to the unobserved value itself | No conflict data from areas controlled by armed groups; no economic data from failed states | **Dangerous to interpolate** — missingness is informative |

**Critical insight:** In conflict and humanitarian research, missingness is often informative (MNAR). The absence of data from a region may itself indicate crisis. Imputing values in these cases can introduce systematic bias. Better to model the missingness explicitly or use it as a feature.

### 6.2 Spatial Interpolation: Inverse Distance Weighting (IDW)

IDW estimates the value at an unknown location as a weighted average of values at known nearby locations, with weights inversely proportional to distance.

$$\hat{z}(x_0) = \frac{\sum_{i=1}^{n} w_i \cdot z(x_i)}{\sum_{i=1}^{n} w_i}, \quad w_i = \frac{1}{d(x_0, x_i)^p}$$

Where $p$ is the power parameter (typically 2). Higher $p$ gives more weight to nearby points.

```python
from scipy.spatial import cKDTree
import numpy as np

def idw_interpolate(known_coords, known_values, target_coords, power=2, k=8):
    """
    Inverse distance weighting interpolation.

    Parameters:
        known_coords: (n, 2) array of known point coordinates
        known_values: (n,) array of known values
        target_coords: (m, 2) array of target point coordinates
        power: distance weighting exponent
        k: number of nearest neighbours to use

    Returns:
        (m,) array of interpolated values
    """
    tree = cKDTree(known_coords)
    distances, indices = tree.query(target_coords, k=k)

    # Handle case where target coincides with known point
    distances = np.maximum(distances, 1e-10)

    weights = 1.0 / distances ** power
    weighted_values = np.sum(weights * known_values[indices], axis=1)
    weight_sums = np.sum(weights, axis=1)

    return weighted_values / weight_sums
```

**Strengths:** Simple, fast, deterministic, easy to understand.

**Weaknesses:** Does not account for spatial autocorrelation structure. Cannot extrapolate beyond the convex hull of known points. Sensitive to power parameter choice. No uncertainty estimate.

### 6.3 Spatial Interpolation: Kriging

Kriging is a geostatistical method that uses the spatial autocorrelation structure (modelled via a variogram) to provide optimal unbiased predictions with uncertainty estimates.

**The variogram** describes how spatial similarity decays with distance:

$$\gamma(h) = \frac{1}{2} \text{Var}[Z(x) - Z(x+h)]$$

Common variogram models:
- **Spherical:** Reaches a sill (maximum variance) at a finite range
- **Exponential:** Approaches the sill asymptotically
- **Gaussian:** Very smooth near the origin, good for highly continuous fields

```python
from pykrige.ok import OrdinaryKriging
import numpy as np

# Known observation locations and values
lons = np.array([30.5, 31.2, 29.8, 30.1, 31.5])
lats = np.array([-1.5, -1.2, -2.0, -0.8, -1.8])
values = np.array([120.5, 130.2, 115.0, 125.3, 110.8])

# Create kriging model
ok = OrdinaryKriging(
    lons, lats, values,
    variogram_model="spherical",
    verbose=False,
    enable_plotting=False,
    nlags=10
)

# Interpolate to grid
grid_lon = np.arange(29.0, 32.0, 0.5)
grid_lat = np.arange(-3.0, 0.0, 0.5)

z_pred, z_var = ok.execute("grid", grid_lon, grid_lat)
# z_pred: interpolated values
# z_var: kriging variance (uncertainty estimate)
```

**Strengths:** Provides uncertainty estimates. Uses spatial structure (variogram). Optimal in a statistical sense (BLUE — Best Linear Unbiased Estimator). Can incorporate trend (Universal Kriging).

**Weaknesses:** Computationally expensive for large datasets ($O(n^3)$ for $n$ observations). Assumes stationarity. Variogram fitting can be sensitive.

**When to use kriging vs. IDW:**

| Criterion | IDW | Kriging |
|-----------|-----|---------|
| Need uncertainty estimates | No | Yes |
| Large number of observations | Better (faster) | Expensive; use local kriging |
| Data has clear spatial structure | Less effective | Much better |
| Quick-and-dirty gap filling | Good choice | Overkill |
| Publication-quality interpolation | Insufficient | Preferred |

### 6.4 Temporal Interpolation

For time series gaps in grid cells:

```python
import pandas as pd

# Linear interpolation for continuous variables
df["value_interp"] = df.groupby("grid_cell_id")["value"].transform(
    lambda x: x.interpolate(method="linear", limit=3)  # max 3-month gap
)

# Seasonal decomposition + interpolation for seasonal data
from statsmodels.tsa.seasonal import STL

def seasonal_interpolate(series, period=12):
    """Fill gaps using seasonal decomposition."""
    # First do linear interpolation to get a complete series for decomposition
    filled = series.interpolate(method="linear")

    stl = STL(filled, period=period, robust=True)
    result = stl.fit()

    # Replace only originally-missing values with the reconstructed signal
    reconstructed = result.trend + result.seasonal
    output = series.copy()
    output[series.isna()] = reconstructed[series.isna()]
    return output
```

### 6.5 Multiple Imputation for Spatial Panel Data

For systematic analysis where uncertainty from imputation must be propagated:

```python
from sklearn.impute import IterativeImputer
import numpy as np

def multiple_imputation_spatial(data, n_imputations=5, random_state=42):
    """
    Perform multiple imputation on spatial panel data.

    data: DataFrame with columns [grid_cell_id, time, var1, var2, ...]
    Returns: list of n_imputations completed datasets
    """
    feature_cols = [c for c in data.columns
                    if c not in ["grid_cell_id", "time"]]
    X = data[feature_cols].values

    imputed_datasets = []
    for i in range(n_imputations):
        imputer = IterativeImputer(
            max_iter=50,
            random_state=random_state + i,
            sample_posterior=True,  # crucial for multiple imputation
            n_nearest_features=10
        )
        X_imputed = imputer.fit_transform(X)

        result = data.copy()
        result[feature_cols] = X_imputed
        imputed_datasets.append(result)

    return imputed_datasets

# Run analysis on each imputed dataset, then pool results
# using Rubin's rules for combining multiply-imputed estimates
```

### 6.6 Practical Recommendations for Causal Atlas

1. **Record missingness explicitly.** For every variable in every grid-cell-month, store a flag: observed, interpolated, imputed, or missing.
2. **Do not impute conflict data.** Zero observed events is different from "we do not know." Store event counts and a separate data-availability indicator.
3. **Interpolate satellite gaps cautiously.** Cloud gaps in NDVI or nightlights are MCAR/MAR and can be spatiotemporally interpolated. But prolonged gaps (e.g., months of cloud cover) should be flagged.
4. **Use multiple imputation for economic data.** GDP, trade statistics, etc. from fragile states have informative gaps. If imputing, use multiple imputation and propagate uncertainty.
5. **Set maximum interpolation distances.** Do not spatially interpolate across more than 2-3 cell widths (100-150 km). Do not temporally interpolate across more than 3 months.

---

## 7. The PRIO-GRID Approach

[PRIO-GRID](https://grid.prio.org/) is the foundational spatial framework for quantitative conflict research. Understanding its methodology is essential since Causal Atlas adopts a PRIO-GRID-compatible grid structure.

### 7.1 Grid Structure

- **Resolution:** 0.5 x 0.5 decimal degrees (approximately 55 x 55 km at the equator)
- **Extent:** Global, covering all terrestrial areas (-180 to 180 longitude, -90 to 90 latitude)
- **Grid size:** 720 columns x 360 rows = 259,200 cells (many are ocean)
- **CRS:** EPSG:4326 (WGS84 geographic coordinates)
- **Cell indexing:** Each cell identified by (column, row) or a sequential ID
- **Temporal resolution:** Configurable; default is annual, but supports monthly and quarterly

Source: [Tollefsen et al., 2012, Journal of Peace Research](https://journals.sagepub.com/doi/10.1177/0022343311431287)

### 7.2 Version 3 Architecture

PRIO-GRID v3 (available via [GitHub](https://github.com/prio-data/priogrid)) is implemented as an R package rather than a static dataset. Key design decisions:

**Core technology stack (R):**
- **terra:** Memory-efficient raster operations with automatic disk-based processing when estimated memory exceeds 4GB
- **sf:** Vector/simple features data handling
- **exactextractr:** Area-weighted extraction from rasters to polygons with exact fractional pixel coverage

**Flexible configuration via `pgoptions`:**
```r
# Default configuration (matches classic PRIO-GRID)
# Resolution: 0.5 x 0.5 degrees (720 x 360 cells)
# CRS: EPSG:4326
# Extent: global
# Temporal resolution: 1 year

# Custom configuration for finer analysis
pgoptions$set_ncol(1440)        # 0.25-degree resolution
pgoptions$set_nrow(720)
pgoptions$set_crs("ESRI:54009") # Mollweide equal-area
pgoptions$set_temporal_resolution("1 month")
pgoptions$set_start_date("2010-01-31")
pgoptions$set_end_date("2023-12-31")
```

**Key functions:**
- `prio_blank_grid()` — Generates the base spatial grid as an sf object
- `load_pgvariable()` — Loads individual variables as raster objects
- `read_pg_static()` — Reads time-invariant variables (terrain, distance to coast)
- `read_pg_timevarying()` — Reads time-varying variables (population, conflict)
- `download_priogrid()` — Downloads raw data from original sources

**Reproducibility:** Custom builds use 6-character MD5 hashes to identify unique spatial configurations (resolution, extent, CRS) and temporal configurations (resolution, date range), ensuring exact replication.

### 7.3 Data Ingestion Methods in PRIO-GRID

PRIO-GRID v3 handles three types of source data:

1. **Raster data** (climate, land cover, nightlights): Uses `exactextractr::exact_extract()` to compute area-weighted statistics (mean, sum, min, max) for each grid cell. Temporary files stored in `{rawfolder}/tmp/` and auto-cleaned after processing.

2. **Point data** (conflict events): Assigns events to grid cells via spatial join, then counts/aggregates per cell-period.

3. **Polygon data** (admin regions): Area-weighted interpolation using geometry intersection, with weights based on the overlap area fraction.

### 7.4 Variables Included

PRIO-GRID v3 includes variables across these domains:

| Domain | Variables | Source |
|--------|-----------|--------|
| Conflict | Event counts, fatalities | UCDP-GED |
| Climate | Temperature, precipitation | CRU TS |
| Population | Total population, density | WorldPop, GPW |
| Land cover | Forest cover, cropland, urban | ESA CCI |
| Terrain | Elevation, slope, ruggedness | SRTM, ETOPO |
| Nightlights | Mean luminosity | DMSP-OLS, VIIRS |
| Water | Distance to coast/river, lake area | Natural Earth |
| Economy | Nightlights-derived proxies | Derived |

### 7.5 Lessons for Causal Atlas

- Adopt the same grid structure (0.5 x 0.5 degree, EPSG:4326) for compatibility with existing PRIO-GRID datasets.
- Use `exactextract` (Python version) for raster-to-grid operations.
- The R package approach (code-as-dataset) is superior to distributing static files because it enables reproducibility and customisation.
- PRIO-GRID v3's configuration system (`pgoptions`) is a good model for allowing users to customize resolution.

---

## 8. The AfroGrid Approach

[AfroGrid](https://www.nature.com/articles/s41597-022-01198-5) (published in *Nature Scientific Data*, 2022) is an integrated, disaggregated 0.5-degree grid-month dataset on conflict, environmental stress, and socioeconomic features covering Africa from 1989 to 2020.

### 8.1 Spatial and Temporal Scope

- **Grid:** 0.5-degree cells covering Africa (10,674 terrestrial grid cells)
- **Time:** Monthly, 1989-2020 (384 months)
- **Total observations:** ~4.1 million cell-months

### 8.2 Data Harmonization Methodology

AfroGrid's processing pipeline handles each data type differently:

**Conflict event aggregation:**
- Sources: ACLED, UCDP-GED, PITF, SCAD (four distinct conflict datasets)
- Events without at least district-level geographic precision are excluded
- For SCAD campaigns (multi-day events): expanded to campaign-month format; campaigns exceeding one year are excluded (136 of ~900 campaigns removed, retaining 86%)
- Result: 74 distinct conflict indicators organized by perpetrator type, violence type, and fatality estimates, all standardized to grid-month resolution

**NDVI processing:**
- Source: MODIS Terra satellite data at 0.08-degree resolution
- Extracted using the `MODIStsp` R package
- Three indicators per cell-month: NDVI mean (average of all pixels within cell), NDVI max, NDVI min
- Captures both central tendency and within-cell vegetation variability

**Climate data:**
- Source: CRU TS monthly gridded climate dataset (already at 0.5-degree resolution, so no resampling needed)
- Innovation: Computes 30-year rolling Z-scores for anomaly detection
  $$Z_{it} = \frac{X_{it} - \bar{X}_{im}}{\sigma_{im}}$$
  where $\bar{X}_{im}$ and $\sigma_{im}$ are the 30-year mean and standard deviation for cell $i$ in calendar month $m$
- This captures how unusual current conditions are relative to the long-term local pattern

**Nighttime lights harmonization (key innovation):**
- Problem: DMSP-OLS data (1992-2013) and VIIRS (2012+) use different sensors with different characteristics
- Three-step harmonization:
  1. Quantify monthly VIIRS radiance across the continent during the overlap period
  2. Calculate calibration relationships between VIIRS and DMSP-OLS
  3. Generate consistent time series by integrating temporally calibrated DMSP data with DMSP-like data derived from VIIRS
- Result: A harmonized nighttime lights series covering 1992-2018 with improved sensitivity to low-emission rural areas

**Population:**
- Source: WorldPop annual census-derived estimates at 1 km resolution
- Aggregation: Sum all 1 km pixels within each grid cell per year
- Coverage: 2000-2020

### 8.3 Quality Assurance

- Two-stage least squares estimation with precipitation as an instrument to address NDVI endogeneity to conflict
- Fixed effects for grid cells, months, and years to control for unobserved heterogeneity
- Explicit handling of temporal overlap between data sources

### 8.4 Lessons for Causal Atlas

- **Z-score anomalies** are more useful than raw values for cross-domain analysis. A raw rainfall value of 50mm means different things in the Sahel vs. Congo basin. The Z-score tells you "this is 2 standard deviations below normal for this place at this time of year."
- **Sensor harmonization** is a major challenge. When satellite instruments change, creating consistent time series requires careful calibration. This affects nightlights (DMSP to VIIRS), NDVI (MODIS to VIIRS), and potentially future data sources.
- **Multiple conflict datasets** provide cross-validation. Where ACLED and UCDP-GED agree, we have high confidence. Where they disagree, we can flag uncertainty.
- The data is available on [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LDI5TK).

---

## 9. How HungerMapLIVE Integrates Sources

[HungerMapLIVE](https://hungermap.wfp.org/) is WFP's near-real-time global food security monitoring platform. It integrates multiple data streams using machine learning to produce sub-national food security estimates.

### 9.1 Data Sources and Fusion

HungerMapLIVE brings together the following data streams:

| Data stream | Source | Temporal resolution | Role |
|-------------|--------|-------------------|------|
| Food security surveys | WFP mVAM (mobile surveys) | Near-real-time (daily calls) | Ground truth for training |
| Conflict | ACLED | Daily | Predictor variable |
| Rainfall / vegetation | NASA (CHIRPS, MODIS NDVI) | Dekadal / 16-day | Environmental stress indicator |
| Market prices | WFP VAM | Monthly (varies by market) | Economic stress indicator |
| Population | World Bank / WorldPop | Annual | Denominator for prevalence |
| Nighttime lights | VIIRS | Monthly composites | Economic proxy |
| Hazards data | Pacific Disaster Centre | Near-real-time | Shock indicator |
| Macro-economic indicators | Various | Quarterly/annual | Structural vulnerability |

Source: [WFP Innovation](https://innovation.wfp.org/project/hungermap-live), [WFPUSA](https://wfpusa.org/news/leveraging-big-data-and-machine-learning-to-monitor-global-food-security-in-real-time/)

### 9.2 Machine Learning Pipeline

The platform uses a two-track approach:

1. **Direct monitoring:** Continuous near-real-time data collection through call centres that remotely collect thousands of data points daily, producing direct food security estimates for ~90 countries.

2. **Nowcasting via ML:** Where direct survey data is limited or unavailable, machine learning models trained on 14 years of data from 63 countries produce "nowcasts" — near-real-time estimates using the predictor variables above.

The ML models predict the prevalence of insufficient food consumption (the share of the population not meeting minimum dietary needs) at sub-national levels.

### 9.3 Data Fusion Architecture

HungerMapLIVE uses a unified data warehouse that brings all information streams into one place. The key integration steps (as far as publicly documented) are:

1. All data is aligned to a common spatial framework (sub-national admin regions, typically admin-1 or admin-2)
2. Temporal alignment to a common update cycle
3. Feature engineering: raw data is transformed into predictor features (e.g., rainfall anomalies rather than raw rainfall)
4. The ML model combines all features to produce food security predictions
5. Results are displayed on an interactive map with ability to overlay and compare different data layers

### 9.4 Lessons for Causal Atlas

- **ML-based nowcasting** can fill spatial and temporal gaps when direct observations are unavailable.
- **Feature engineering** (anomalies, trends, lags) matters more than raw values for prediction.
- **Multiple update frequencies** are managed by having the system pull each data stream at its native frequency and re-run models when any input updates.
- The platform demonstrates that near-real-time data fusion across heterogeneous sources is feasible and operationally useful.
- **Transparency limitation:** HungerMapLIVE's exact ML architecture and preprocessing pipeline are not fully published, making replication difficult. Causal Atlas should document every transformation.

---

## 10. Admin-to-Grid Mapping

### 10.1 The Crosswalk Problem

Many important datasets (economic indicators, health statistics, food prices) are reported at administrative region level. To integrate with our grid, we need a mapping from admin regions to grid cells.

**Key challenges:**
- Admin boundaries change over time (redistricting, country splits)
- Multiple admin boundary datasets exist with inconsistent boundaries
- Grid cells may overlap multiple admin regions
- Coastal cells partially cover ocean

### 10.2 Boundary Datasets

| Dataset | Coverage | Levels | License | Best for |
|---------|----------|--------|---------|----------|
| [GADM](https://gadm.org/) | Global | Up to 5 (country to local) | Academic use only (non-commercial) | Research, high detail |
| [geoBoundaries](https://www.geoboundaries.org/) | Global, 200+ entities | Up to 5 (ADM0-ADM5) | CC BY 4.0 / ODbL (open) | Open-source projects, quality-assured |
| [Natural Earth](https://www.naturalearthdata.com/) | Global | 2 (country, province) | Public domain | Cartography, lower detail |
| [OCHA CODs](https://data.humdata.org/) | Humanitarian contexts | Varies by country | Open | Humanitarian response, P-coded |

**Recommendation for Causal Atlas:** Use **geoBoundaries** as the primary boundary dataset because:
- Fully open license (compatible with MIT-licensed project)
- Quality-assured with manual revisions
- API access: `https://www.geoboundaries.org/api/current/gbOpen/{ISO3}/{ADM_LEVEL}/`
- Frequently updated
- Community-maintained

Use GADM as a fallback where geoBoundaries lacks coverage or detail.

### 10.3 P-Codes (Place Codes)

P-codes are unique alphanumeric identifiers assigned by OCHA to administrative units in humanitarian contexts. They are the primary key for linking humanitarian datasets.

- Format: Typically ISO 2-letter country code + numeric identifier (e.g., `AF0101` for a district in Afghanistan)
- Available as a [Global P-Code List on HDX](https://data.humdata.org/dataset/global-pcodes)
- Essential for linking to HDX HAPI, WFP data, OCHA situation reports

```python
# Download P-code crosswalk
import pandas as pd

pcodes = pd.read_csv(
    "https://data.humdata.org/dataset/.../global_pcodes.csv"
)
# Columns: iso3, adm0_pcode, adm0_name, adm1_pcode, adm1_name,
#           adm2_pcode, adm2_name, ...
```

### 10.4 Building the Admin-to-Grid Crosswalk

A pre-computed crosswalk table maps each admin region to the grid cells it overlaps, with area weights:

```python
import geopandas as gpd
import numpy as np

def build_admin_grid_crosswalk(admin_gdf, grid_gdf):
    """
    Build crosswalk table between admin regions and grid cells.

    Returns DataFrame with columns:
        admin_id, grid_cell_id, weight_extensive, weight_intensive

    weight_extensive = area_overlap / area_admin
        (fraction of admin region in this cell)
    weight_intensive = area_overlap / area_cell
        (fraction of cell covered by this admin region)
    """
    # Ensure same CRS
    admin_gdf = admin_gdf.to_crs("EPSG:4326")
    grid_gdf = grid_gdf.to_crs("EPSG:4326")

    # For accurate area calculations, project to equal-area
    admin_ea = admin_gdf.to_crs("ESRI:54009")  # Mollweide
    grid_ea = grid_gdf.to_crs("ESRI:54009")

    # Compute intersections
    overlay = gpd.overlay(admin_ea, grid_ea, how="intersection")
    overlay["overlap_area"] = overlay.geometry.area

    # Get original areas
    admin_ea["admin_area"] = admin_ea.geometry.area
    grid_ea["cell_area"] = grid_ea.geometry.area

    # Merge areas
    overlay = overlay.merge(
        admin_ea[["admin_id", "admin_area"]], on="admin_id"
    )
    overlay = overlay.merge(
        grid_ea[["grid_cell_id", "cell_area"]], on="grid_cell_id"
    )

    # Compute weights
    overlay["weight_extensive"] = overlay["overlap_area"] / overlay["admin_area"]
    overlay["weight_intensive"] = overlay["overlap_area"] / overlay["cell_area"]

    return overlay[["admin_id", "grid_cell_id",
                     "weight_extensive", "weight_intensive",
                     "overlap_area"]].copy()


def apply_crosswalk(crosswalk, admin_data, variable, var_type="extensive"):
    """
    Apply crosswalk to transfer admin-level data to grid cells.

    var_type: "extensive" (population, GDP) or "intensive" (temperature, rate)
    """
    weight_col = f"weight_{var_type}"

    merged = crosswalk.merge(admin_data[["admin_id", variable]], on="admin_id")

    if var_type == "extensive":
        # Sum weighted values per grid cell
        merged["weighted_value"] = merged[variable] * merged[weight_col]
        result = merged.groupby("grid_cell_id")["weighted_value"].sum()
    else:
        # Area-weighted average per grid cell
        merged["weighted_value"] = merged[variable] * merged[weight_col]
        result = merged.groupby("grid_cell_id").agg(
            value=("weighted_value", "sum"),
            weight_sum=(weight_col, "sum")
        )
        result = result["value"] / result["weight_sum"]

    return result.reset_index()
```

### 10.5 Handling Boundary Changes Over Time

Admin boundaries change frequently in developing countries. Strategies:

1. **Use time-stamped boundary files.** geoBoundaries and GADM provide vintaged boundary datasets.
2. **Build crosswalks for each time period.** If a province splits in 2015, have separate crosswalks for pre-2015 and post-2015 boundaries.
3. **Harmonize to the finest common geography.** If you need a consistent time series, identify the smallest units that are consistent across the entire period and aggregate up.
4. **The grid itself is time-invariant.** This is a key advantage of grid-based analysis over admin-based analysis. Grid cells never change boundaries, so temporal comparisons are straightforward. The challenge is only in the admin-to-grid mapping step.

---

## 11. Coordinate Reference Systems

### 11.1 Our CRS: EPSG:4326 (WGS84)

Causal Atlas uses WGS84 geographic coordinates (EPSG:4326) as its primary CRS, matching PRIO-GRID and most global datasets.

**Properties:**
- Coordinates are in degrees (longitude, latitude)
- Not projected (no distortion from projection, but distances and areas are not constant)
- Cell sizes vary: a 0.5-degree cell is ~55 x 55 km at the equator but ~55 x 28 km at 60 degrees latitude
- Suitable for global analysis but area calculations need care

### 11.2 CRS Handling in Python

Modern best practice (as of March 2025):

```python
import geopandas as gpd
from pyproj import CRS

# Setting CRS on a GeoDataFrame
gdf = gdf.set_crs("EPSG:4326")  # preferred format

# Reprojecting
gdf_projected = gdf.to_crs("EPSG:4326")

# DO NOT use the old init format
# gdf.set_crs({"init": "epsg:4326"})  # DEPRECATED, DO NOT USE

# Checking CRS
print(gdf.crs)             # pyproj CRS object
print(gdf.crs.to_epsg())   # 4326
print(gdf.crs.is_geographic)  # True

# For raster data with rioxarray
import rioxarray
ds = ds.rio.set_crs("EPSG:4326")
ds = ds.rio.reproject("EPSG:4326")

# CRS comparison (pyproj handles this correctly)
crs1 = CRS.from_epsg(4326)
crs2 = CRS.from_wkt(some_wkt_string)
assert crs1 == crs2  # pyproj compares semantically, not string equality
```

Source: [GeoPandas Projections docs](https://geopandas.org/en/latest/docs/user_guide/projections.html)

### 11.3 When to Use Projected CRS

For certain operations, geographic coordinates (degrees) are insufficient:

| Operation | Use geographic (EPSG:4326)? | Use projected CRS? |
|-----------|---------------------------|---------------------|
| Storing data | Yes | No |
| Displaying on web map | Yes (standard for web) | No |
| Computing areas | No (degrees are not area units) | Yes (e.g., Mollweide ESRI:54009) |
| Computing distances | Approximate only | Yes (e.g., UTM for local, Mollweide for global) |
| Spatial joins | Yes (if both layers match) | Either |
| Buffer operations | No (buffer in degrees is distorted) | Yes |

**Practical approach for Causal Atlas:**
- Store everything in EPSG:4326
- Project to equal-area (Mollweide ESRI:54009) for area calculations in the crosswalk
- Use `geopy` or Haversine formula for distance calculations rather than projecting

```python
from geopy.distance import geodesic

# Accurate distance without projecting
dist_km = geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Haversine for vectorized computation
import numpy as np

def haversine_km(lat1, lon1, lat2, lon2):
    """Vectorized haversine distance in kilometres."""
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))
```

### 11.4 Axis Order

GeoPandas always stores coordinates as (x, y) = (longitude, latitude), regardless of the CRS's native axis order. When reprojecting, pyproj handles axis order differences automatically. This means you do not need to swap axes manually.

### 11.5 Datum Transformations

Most modern global datasets use WGS84. However, some older or regional datasets may use different datums (e.g., NAD27, ED50, local African datums). The transformation errors can be significant (tens to hundreds of metres).

```python
# pyproj handles datum transformations automatically when reprojecting
from pyproj import Transformer

# Transform from a local datum to WGS84
transformer = Transformer.from_crs(
    "EPSG:4267",  # NAD27
    "EPSG:4326",  # WGS84
    always_xy=True  # ensures (lon, lat) order
)
lon_wgs84, lat_wgs84 = transformer.transform(lon_nad27, lat_nad27)
```

### 11.6 Pitfalls

- **Longitude wrapping:** Some datasets use 0-360 longitude, others -180 to 180. Standardize to -180 to 180 on ingestion.
- **Antimeridian crossing:** Grid cells and polygons that cross the 180/-180 boundary need special handling. Split geometries at the antimeridian before processing.
- **Coordinate precision:** For 0.5-degree grid cells, coordinate precision beyond 4 decimal places is unnecessary. But store source event coordinates at full precision.

---

## 12. Data Versioning and Provenance

### 12.1 Why Provenance Matters

Every grid cell value in Causal Atlas has a story: which source dataset it came from, what version, when it was downloaded, what transformations were applied, and what quality flags it carries. Without tracking this, results are not reproducible and errors cannot be traced.

### 12.2 Cell-Level Metadata

For each variable in each grid-cell-month, track:

```python
# Schema for provenance tracking
cell_metadata = {
    "grid_cell_id": 12345,
    "variable": "conflict_events",
    "year_month": "2023-06",
    "value": 3,

    # Provenance fields
    "source_dataset": "ACLED",
    "source_version": "2023-07-14",        # version/release date of source
    "source_download_date": "2023-08-01",   # when we downloaded it
    "spatial_method": "point_binning",       # how spatial integration was done
    "temporal_method": "monthly_sum",        # how temporal aggregation was done
    "quality_flag": "observed",             # observed | interpolated | imputed | missing
    "coverage_fraction": 1.0,               # fraction of cell with valid data
    "pipeline_version": "0.3.2",            # version of our processing code
    "pipeline_commit": "abc123f"             # git commit of processing code
}
```

### 12.3 Storage Approach: Parquet with Metadata

Apache Parquet is well-suited for this because it supports:
- Column-level metadata (store provenance as column metadata)
- Efficient columnar storage (quality flags and provenance columns compress well)
- Partitioning by time period for efficient queries

```python
import pyarrow as pa
import pyarrow.parquet as pq

# Define schema with metadata
schema = pa.schema([
    ("grid_cell_id", pa.int32()),
    ("year_month", pa.string()),
    ("conflict_events", pa.float32()),
    ("conflict_source", pa.string()),
    ("conflict_quality", pa.string()),
    ("rainfall_mm", pa.float32()),
    ("rainfall_source", pa.string()),
    ("rainfall_quality", pa.string()),
    # ... more variables and their provenance columns
])

# Add dataset-level metadata
schema = schema.with_metadata({
    b"pipeline_version": b"0.3.2",
    b"pipeline_commit": b"abc123f",
    b"created_at": b"2025-03-15T10:00:00Z",
    b"grid_specification": b"PRIO-GRID compatible, 0.5 deg, EPSG:4326"
})

# Write partitioned by year
table = pa.Table.from_pandas(df, schema=schema)
pq.write_to_dataset(
    table,
    root_path="data/processed/grid_monthly/",
    partition_cols=["year"]
)
```

### 12.4 DVC for Data Versioning

[DVC (Data Version Control)](https://dvc.org/) tracks large data files alongside code in Git, storing the actual data in remote storage (S3, GCS, etc.) and keeping lightweight pointer files in the repo.

```bash
# Initialize DVC in the repo
dvc init

# Track a large data file
dvc add data/raw/acled_2023.csv
# Creates data/raw/acled_2023.csv.dvc (pointer file, tracked by Git)
# Actual data stored in .dvc/cache/

# Track processed output
dvc add data/processed/grid_monthly/

# Define a processing pipeline
# dvc.yaml:
# stages:
#   ingest_acled:
#     cmd: python scripts/ingest_acled.py
#     deps:
#       - data/raw/acled_2023.csv
#       - scripts/ingest_acled.py
#     outs:
#       - data/processed/acled_gridded.parquet
#
#   build_grid:
#     cmd: python scripts/build_grid.py
#     deps:
#       - data/processed/acled_gridded.parquet
#       - data/processed/chirps_gridded.parquet
#     outs:
#       - data/processed/grid_monthly/

# Reproduce the pipeline
dvc repro
```

**Key DVC features relevant to Causal Atlas:**
- Pipeline stages with explicit dependencies model the data flow
- `dvc repro` only re-runs stages whose inputs have changed
- `dvc diff` shows what data changed between versions
- Remote storage (S3, GCS, Azure) for sharing large datasets

### 12.5 Source Dataset Version Tracking

Each source dataset should be tracked with:

```python
# source_registry.yaml
sources:
  acled:
    name: "Armed Conflict Location & Event Data"
    url: "https://acleddata.com/data-export-tool/"
    license: "Attribution required, non-commercial research"
    last_download: "2025-03-01"
    version: "2025-03-01 export"
    citation: "Raleigh et al., 2010"
    update_frequency: "weekly"
    spatial_coverage: "global"
    temporal_coverage: "1997-present"
    api_endpoint: "https://api.acleddata.com/acled/read"
    raw_file: "data/raw/acled/acled_20250301.csv"
    checksum: "sha256:abc123..."

  chirps:
    name: "Climate Hazards Group InfraRed Precipitation with Station data"
    url: "https://www.chc.ucsb.edu/data/chirps"
    license: "Public domain"
    last_download: "2025-02-15"
    version: "v2.0"
    citation: "Funk et al., 2015"
    # ...
```

### 12.6 Recommended Provenance Strategy for Causal Atlas

1. **Code versioning:** Git for all processing code. Every pipeline run tagged with the git commit.
2. **Data versioning:** DVC for raw and processed data files. DVC pointer files committed to Git.
3. **Pipeline definition:** DVC pipeline (`dvc.yaml`) or similar (Prefect, Dagster) defining the DAG of processing steps.
4. **Cell-level provenance:** Stored as additional columns in the Parquet output files.
5. **Source registry:** YAML file tracking all upstream data sources, their versions, and download dates.
6. **Immutable raw data:** Never modify raw downloaded files. All transformations produce new files.

---

## 13. Recommended Pipeline for Causal Atlas

Based on the techniques reviewed above, here is the recommended data standardization pipeline for Causal Atlas.

### 13.1 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAW DATA SOURCES                           │
│  ACLED  CHIRPS  MODIS  WFP  WorldBank  USGS  OpenAQ  ...      │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: INGESTION                           │
│  - Download from APIs/bulk sources                              │
│  - Validate schema and data types                               │
│  - Standardize CRS to EPSG:4326                                │
│  - Standardize timestamps to UTC                                │
│  - Store raw files immutably (DVC tracked)                      │
│  - Record source version and download date                      │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 2: SPATIAL ALIGNMENT                   │
│                                                                 │
│  Point data ──► Point-in-grid assignment (vectorized)           │
│                 - Use arithmetic cell ID calculation             │
│                 - Exclude low-precision events (configurable)   │
│                                                                 │
│  Raster data ──► exactextract zonal statistics                  │
│                  - mean/sum/min/max/stdev per cell               │
│                  - Track coverage fraction                       │
│                                                                 │
│  Admin data ──► Pre-computed crosswalk (Tobler/manual)          │
│                 - Extensive: area-weighted sum                   │
│                 - Intensive: area-weighted mean                  │
│                 - Dasymetric where ancillary data available      │
│                                                                 │
│  Output: per-source grid-aligned datasets                       │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 3: TEMPORAL ALIGNMENT                  │
│                                                                 │
│  - Aggregate all data to monthly (primary unit)                 │
│    - Events: count, sum fatalities, etc.                        │
│    - Rasters: monthly mean/sum as appropriate                   │
│    - 16-day composites: time-weighted monthly mean              │
│    - Annual data: constant fill across 12 months                │
│  - Preserve daily data in separate tables for lag analysis      │
│  - Compute derived indicators:                                  │
│    - Rolling Z-scores (AfroGrid approach)                       │
│    - Month-over-month changes                                   │
│    - Seasonal anomalies                                         │
│                                                                 │
│  Output: grid-cell-month datasets per source                    │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 4: INTEGRATION & QC                    │
│                                                                 │
│  - Join all source datasets on (grid_cell_id, year_month)       │
│  - Apply quality flags:                                         │
│    - "observed": direct measurement/observation                 │
│    - "interpolated": gap-filled via spatial/temporal interp     │
│    - "imputed": estimated via model                             │
│    - "missing": no data, not imputed                            │
│  - Track coverage fraction per variable per cell-month          │
│  - Validate: no duplicate cell-months, reasonable value ranges  │
│  - Handle missing data (per strategy in Section 6.6):           │
│    - Satellite gaps: spatiotemporal interpolation (flagged)     │
│    - Conflict: zero ≠ missing, store both                       │
│    - Economic: multiple imputation if needed                    │
│                                                                 │
│  Output: integrated grid-cell-month Parquet files               │
│          partitioned by year                                    │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 5: OUTPUT & PROVENANCE                 │
│                                                                 │
│  - Write final dataset as partitioned Parquet                   │
│  - Embed provenance metadata in Parquet schema                  │
│  - Update source registry YAML                                 │
│  - DVC commit data files                                        │
│  - Git commit code and DVC pointer files                        │
│                                                                 │
│  Output format:                                                 │
│  data/processed/grid_monthly/                                   │
│    year=2023/                                                   │
│      part-00000.parquet                                         │
│    year=2024/                                                   │
│      part-00000.parquet                                         │
└─────────────────────────────────────────────────────────────────┘
```

### 13.2 Core Grid Specification

```python
# grid_spec.py — Causal Atlas grid specification

GRID_CONFIG = {
    "crs": "EPSG:4326",
    "resolution_deg": 0.5,
    "n_cols": 720,          # 360 / 0.5
    "n_rows": 360,          # 180 / 0.5
    "extent": {
        "west": -180.0,
        "east": 180.0,
        "south": -90.0,
        "north": 90.0
    },
    "cell_id_formula": "row * 720 + col",
    "col_from_lon": "int((lon + 180) / 0.5)",
    "row_from_lat": "int((lat + 90) / 0.5)",
    "total_cells": 259200,
    "land_cells": "~65000 (approximate, depends on land mask)",
    "temporal_unit": "month",
    "temporal_format": "YYYY-MM"
}
```

### 13.3 Technology Stack for the Pipeline

| Component | Tool | Rationale |
|-----------|------|-----------|
| Grid creation | geopandas + shapely | Generate PRIO-GRID-compatible cell polygons |
| Raster zonal stats | exactextract (Python) | Best accuracy and performance for raster-to-grid |
| Raster resampling | rioxarray + rasterio | xarray integration, supports all resampling methods |
| Areal interpolation | tobler (PySAL) | Handles extensive/intensive variables, dasymetric |
| Spatial joins | geopandas | Point-in-polygon, overlay operations |
| Temporal resampling | xarray resample, pandas | Flexible temporal aggregation |
| Missing data | PyKrige, scipy, sklearn | Kriging, IDW, multiple imputation |
| Storage | Apache Parquet (pyarrow) | Columnar, compressed, metadata support |
| Data versioning | DVC | Track large files alongside Git |
| Pipeline orchestration | DVC pipelines or Prefect | DAG of processing stages |
| CRS operations | pyproj | Datum transforms, CRS definitions |
| Boundary data | geoBoundaries API | Open license, quality-assured |

### 13.4 Pre-Computed Assets

These should be built once and cached:

1. **Land mask:** Boolean grid indicating which cells contain land (from Natural Earth or GADM coastline)
2. **Admin-to-grid crosswalks:** One per admin boundary vintage per boundary source (geoBoundaries ADM1, ADM2; GADM levels 1-3)
3. **Grid cell polygons:** GeoPackage of all 0.5-degree cell polygons with cell IDs
4. **Reference raster:** A single-band GeoTIFF at 0.5-degree resolution for use as a `reproject_match` target
5. **Cell area lookup:** Area in km2 for each grid cell (varies with latitude)

```python
import numpy as np

def cell_area_km2(lat_south, resolution=0.5):
    """
    Approximate area of a grid cell at given latitude.
    Uses the formula for the area of a latitude-longitude rectangle
    on a sphere with radius R.

    A = R^2 * |sin(lat2) - sin(lat1)| * |lon2 - lon1|
    where angles are in radians.
    """
    R = 6371.0  # Earth radius in km
    lat1 = np.radians(lat_south)
    lat2 = np.radians(lat_south + resolution)
    dlon = np.radians(resolution)

    return R**2 * abs(np.sin(lat2) - np.sin(lat1)) * dlon

# Example: cell at equator
print(f"Equator: {cell_area_km2(0):.0f} km2")     # ~3078 km2
# Example: cell at 60 degrees
print(f"60°N: {cell_area_km2(60):.0f} km2")        # ~1538 km2
```

### 13.5 Incremental Update Strategy

The pipeline should support incremental updates when new data arrives:

1. **New time period:** When ACLED releases a new week of data, re-run only the ACLED ingestion and the integration stage for affected months.
2. **Source dataset revision:** When a source releases a corrected version, re-ingest that source and flag the affected cell-months as "revised."
3. **New data source:** Adding a new variable (e.g., air quality from OpenAQ) requires running stages 1-4 for that source only, then re-running stage 4 (integration) to join it with the existing dataset.

DVC pipelines handle this automatically via dependency tracking: `dvc repro` will only re-run stages whose inputs have changed.

---

## References

### Spatial Data Frameworks
- Tollefsen, A.F., Strand, H., & Buhaug, H. (2012). [PRIO-GRID: A unified spatial data structure](https://journals.sagepub.com/doi/10.1177/0022343311431287). *Journal of Peace Research*, 49(2), 363-374.
- PRIO-GRID v3 R Package: [github.com/prio-data/priogrid](https://github.com/prio-data/priogrid)
- PRIO-GRID website: [grid.prio.org](https://grid.prio.org/)

### AfroGrid
- Harari, M.F., et al. (2022). [Introducing AfroGrid, a unified framework for environmental conflict research in Africa](https://www.nature.com/articles/s41597-022-01198-5). *Nature Scientific Data*, 9, 103.
- AfroGrid data: [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LDI5TK)

### HungerMapLIVE
- WFP HungerMap LIVE: [hungermap.wfp.org](https://hungermap.wfp.org/)
- [WFP Innovation — HungerMap LIVE](https://innovation.wfp.org/project/hungermap-live)
- [Using Big Data and Machine Learning to Monitor Food Security](https://wfpusa.org/news/leveraging-big-data-and-machine-learning-to-monitor-global-food-security-in-real-time/)

### Areal Interpolation
- Tobler (PySAL): [github.com/pysal/tobler](https://github.com/pysal/tobler)
- [Areal Interpolation in Python Using Tobler](https://dges.carleton.ca/CUOSGwiki/index.php/Areal_Interpolation_in_Python_Using_Tobler)

### Zonal Statistics
- exactextract: [github.com/isciences/exactextract](https://github.com/isciences/exactextract)
- gdptools: [gdptools.readthedocs.io](https://gdptools.readthedocs.io/en/main/)

### Boundary Datasets
- GADM: [gadm.org](https://gadm.org/)
- geoBoundaries: [geoboundaries.org](https://www.geoboundaries.org/)
- [geoBoundaries: A global database of political administrative boundaries](https://pmc.ncbi.nlm.nih.gov/articles/PMC7182183/)
- OCHA P-codes: [Global P-Code List on HDX](https://data.humdata.org/dataset/global-pcodes)

### Spatial Interpolation
- PyKrige: [geostat-framework.readthedocs.io/projects/pykrige](https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/)
- [Spatial Interpolation with Python (pygis.io)](https://pygis.io/docs/e_interpolation.html)

### Raster Processing
- rasterio: [rasterio.readthedocs.io](https://rasterio.readthedocs.io/en/stable/topics/resampling.html)
- rioxarray: [corteva.github.io/rioxarray](https://corteva.github.io/rioxarray/stable/examples/reproject_match.html)

### Temporal Processing
- [xarray time series documentation](https://docs.xarray.dev/en/stable/user-guide/time-series.html)
- [xarray resample](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.resample.html)

### CRS and Projections
- [GeoPandas projections documentation](https://geopandas.org/en/latest/docs/user_guide/projections.html)
- pyproj: [pyproj4.github.io/pyproj](https://pyproj4.github.io/pyproj/stable/)

### Data Versioning
- DVC: [dvc.org](https://dvc.org/)
- [Versioning, Provenance, and Reproducibility (CMU)](https://mlip-cmu.github.io/book/24-versioning-provenance-and-reproducibility.html)

### Missing Data
- [scikit-learn IterativeImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html)
- [Casper: Causality-Aware Spatiotemporal Imputation](https://arxiv.org/html/2403.11960v1)

### Point Pattern Analysis
- [Geographic Data Science with Python — Point Pattern Analysis](https://geographicdata.science/book/notebooks/08_point_pattern_analysis.html)
- [Point Density Measures (pygis.io)](https://pygis.io/docs/e_summarize_vector.html)
