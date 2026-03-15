# PRIO-GRID: Spatial Framework Deep Dive

> **Last updated:** March 2025
> **Relevance:** PRIO-GRID is the chosen spatial backbone for Causal Atlas. This document covers both PRIO-GRID v2.0 (the established, widely-used release) and PRIO-GRID v3.x (the in-development R-native successor).

---

## 1. Overview

### What Is PRIO-GRID?

PRIO-GRID is a standardised global spatiotemporal grid structure that divides all terrestrial land areas into uniform 0.5-degree by 0.5-degree grid cells (approximately 55 km x 55 km at the equator). Each cell is populated with socioeconomic, environmental, climate, conflict, and resource data, creating a unified spatial framework for cross-domain quantitative research.

The grid was designed to solve a fundamental problem in conflict research and related fields: different datasets use different spatial units (countries, provinces, districts, arbitrary polygons), making cross-dataset analysis difficult. PRIO-GRID provides a common spatial denominator that any point, polygon, or raster dataset can be mapped onto.

### Who Maintains It?

PRIO-GRID is developed and maintained by the **Peace Research Institute Oslo (PRIO)**, specifically by the PRIO Data team. Key personnel:

- **Andreas Forø Tollefsen** — Original creator, lead on v1 and v2
- **Jonas Vestby** — Lead developer on v3 (the `priogrid` R package)
- **Halvard Buhaug** and **Nils B. Weidmann** — Co-authors of the original 2012 paper

PRIO is a Norwegian independent research institute focused on peace and conflict studies, founded in 1959.

### Version History

| Version | Year | Key Characteristics |
|---------|------|---------------------|
| **v1.0** | 2012 | Original release alongside the Journal of Peace Research paper. CSV + shapefile. |
| **v2.0** | ~2015 | Major update with expanded variables, web interface at grid.prio.org, REST API, extended temporal coverage to 1946-2014. Still widely used. |
| **v3.0.0** | 2024 | Complete rewrite as an R package (`priogrid`). Shifted from "dataset" to "research tool." Temporal range extended to 1885-2024. Alpha release. |
| **v3.0.1** | 2025 | Current version. Still marked as "unstable Alpha." Available via GitHub and prio.org/data/40. |

### Key Publication

Tollefsen, A. F., Strand, H., & Buhaug, H. (2012). "PRIO-GRID: A Unified Spatial Data Structure." *Journal of Peace Research*, 49(2), 363-374. DOI: 10.1177/0022343311431287

This is the foundational paper and the primary citation for any use of PRIO-GRID.

---

## 2. Spatial Coverage and Structure

### Grid Specification

| Property | Value |
|----------|-------|
| **Cell size** | 0.5° x 0.5° (latitude x longitude) |
| **Projection** | WGS84 (EPSG:4326) |
| **Extent** | Global: -180° to 180° longitude, -90° to 90° latitude |
| **Grid dimensions** | 720 columns x 360 rows |
| **Total cells** | 259,200 |
| **Land cells** | ~64,818 (cells containing any land area) |
| **Cell area at equator** | ~3,080 km² (~55.6 km x 55.6 km) |
| **Cell area at 60° lat** | ~1,540 km² (~27.8 km x 55.6 km) |

The 0.5-degree resolution was chosen as a balance between spatial precision and data availability. At the equator, each cell is roughly 55.6 km on a side. Because PRIO-GRID uses an equirectangular (Plate Carrée) projection on WGS84, cells become narrower (in km) at higher latitudes, though they retain the same angular dimensions.

### Cell Numbering Convention (gid / pgid)

PRIO-GRID assigns a unique integer identifier to each cell. Understanding the numbering convention is critical for working with the data:

**v2 Convention:**
- The cell identifier is called `gid`
- Cells are numbered from 1 to 259,200
- `row` and `col` are also provided (1-indexed)
- `xcoord` and `ycoord` give the centroid longitude and latitude

**v3 Convention:**
- The cell identifier is called `pgid`
- Uses the same 720x360 grid but the indexing is generated programmatically

**How the v3 index is computed** (from the actual R source code in `R/utility.R`):

```r
create_pg_indices <- function(ncol = 720, nrow = 360) {
  # To create PRIO-GRID, swap ncol and nrow, load index in reverse order,
  # and rotate 90 degrees once.
  rotate <- function(x) t(apply(x, 2, rev))
  pg <- rotate(matrix(rev(1:(ncol*nrow)), nrow=ncol, ncol=nrow))
  return(pg)
}
```

This means:
1. A sequence from 259,200 down to 1 is created
2. It is placed into a matrix with ncol=720 rows and nrow=360 columns (note the swap)
3. The matrix is rotated 90 degrees (transpose + reverse columns)

The result is that **cell 1 is in the bottom-left corner** (SW corner: -180° lon, -90° lat) and numbering proceeds **eastward along rows, then northward**. Cell 720 is at the end of the first (southernmost) row. Cell 721 starts the second row. Cell 259,200 is in the top-right corner (NE corner: 180° lon, 90° lat).

### Converting Between Cell ID and Coordinates

For the standard 720x360 grid:

```
col = ((gid - 1) mod 720) + 1         # 1 to 720, west to east
row = floor((gid - 1) / 720) + 1      # 1 to 360, south to north

longitude = -180.0 + (col - 1) * 0.5 + 0.25   # centroid longitude
latitude  = -90.0  + (row - 1) * 0.5 + 0.25   # centroid latitude
```

To go from coordinates to cell ID:

```
col = floor((longitude + 180.0) / 0.5) + 1
row = floor((latitude + 90.0) / 0.5) + 1
gid = (row - 1) * 720 + col
```

---

## 3. Temporal Coverage

### v2 Temporal Range

- **Static variables:** No time dimension (terrain, land cover snapshots, resource deposits)
- **Time-varying variables:** Yearly, covering **1946-2014** (varies by variable)
- **Temporal unit:** Year (no sub-annual resolution in v2)

### v3 Temporal Range

- **Default range:** 1850-present (configurable)
- **Default resolution:** 1 year (configurable to month, quarter, week)
- **Actual data availability:** 1885-2024 for the pre-built release; individual source coverage varies
- **Key improvement:** v3 supports monthly temporal resolution for sources like CRU climate data

---

## 4. Variables: v2 (PRIO-GRID 2.0)

PRIO-GRID v2 contains **98 variables** across multiple domains. The complete variable list from the v2 API:

### Core Identifiers (5 variables)

| Variable | Description |
|----------|-------------|
| `gid` | Unique grid cell identifier (integer, 1-259200) |
| `row` | Row number (1-360, south to north) |
| `col` | Column number (1-720, west to east) |
| `xcoord` | Centroid longitude (decimal degrees) |
| `ycoord` | Centroid latitude (decimal degrees) |

### Static Variables (36 non-core static variables)

**Land Cover (Globcover 2009):**
`agri_gc`, `aquaveg_gc`, `barren_gc`, `forest_gc`, `herb_gc`, `shrub_gc`, `urban_gc`, `water_gc` — Proportion of cell covered by each land type.

**Agriculture:**
`growstart`, `growend` — Main crop growing season start/end months.
`harvarea` — Main crop harvest area (hectares).
`maincrop` — Main crop type (categorical).

**Resources:**
`diamsec_s`, `diamprim_s`, `gem_s`, `goldplacer_s`, `goldvein_s`, `goldsurface_s`, `petroleum_s` — Binary/presence indicators for mineral deposits.

**Socioeconomics:**
`cmr_mean/max/min/sd` — Child malnutrition rate.
`imr_mean/max/min/sd` — Infant mortality rate.

**Terrain & Accessibility:**
`mountains_mean` — Proportion of cell covered by mountains.
`ttime_mean/max/min/sd` — Travel time to nearest urban centre (minutes).

**Climate:**
`rainseas` — Rain season start month.

**Political:**
`gwno` (static version) — Gleditsch & Ward country code.

### Time-Varying (Yearly) Variables (57 variables)

**Conflict & Politics:**
`excluded` — Count of politically excluded ethnic groups (source: GeoEPR, 1946-2013).
`gwno` (yearly) — Country code assignment per year (source: cShapes, 1946-2014).
`gwarea` — Land area belonging to allocated country (km², 1946-2014).

**Border & Capital Distance:**
`bdist1` — Distance to nearest land-contiguous neighbouring country border (km, 1946-2014).
`bdist2` — Distance to nearest country border regardless of water (km, 1946-2014).
`bdist3` — Distance from cell to its own country's border (km, 1946-2014).
`capdist` — Distance to national capital (km, 1946-2014).

**Climate:**
`prec_gpcc` — Annual precipitation (mm, GPCC, 1946-2013).
`prec_gpcp` — Annual precipitation (mm, GPCP, 1979-2014).
`temp` — Annual mean temperature (°C, 1948-2014).

**Drought (multiple indicators):**
`droughtcrop_speibase/speigdm/spi` — Proportion of crop season under drought.
`droughtstart_speibase/speigdm/spi` — Drought severity at rainy season start.
`droughtend_speibase/speigdm/spi` — Drought severity at rainy season end.
`droughtyr_speibase/speigdm/spi` — Annual proportion experiencing drought.

**Population:**
`pop_gpw_sum/max/min/sd` — Population from Gridded Population of the World (1990-2010).
`pop_hyd_sum/max/min/sd` — Population from HYDE dataset (1950-2005).

**Economics:**
`gcp_mer` — Gross cell product, market exchange rate USD (1990-2005).
`gcp_ppp` — Gross cell product, purchasing power parity USD (1990-2005).
`gcp_qual` — GCP data quality indicator (1990-2005).

**Nighttime Lights:**
`nlights_mean/max/min/sd` — DMSP-OLS nighttime light emission (1992-2013).
`nlights_calib_mean` — Calibrated nighttime lights (1992-2012).

**Land Use (ISAM-HYDE, 1950-2010):**
`agri_ih`, `barren_ih`, `forest_ih`, `grass_ih`, `pasture_ih`, `savanna_ih`, `shrub_ih`, `urban_ih`, `water_ih` — Land use percentages over time.

**Irrigation:**
`irrig_sum/max/min/sd` — Area equipped for irrigation (hectares, 1950-2005).

**Resources (time-varying):**
`diamsec_y`, `diamprim_y`, `gem_y`, `goldplacer_y`, `goldvein_y`, `goldsurface_y`, `petroleum_y`, `drug_y` — Presence indicators with known discovery/production dates.

---

## 5. Variables: v3 (PRIOGRID R Package)

PRIO-GRID v3 takes a fundamentally different approach. Instead of distributing a fixed dataset, it provides **generator functions** that build variables on demand from original source data. The v3.0.1 package includes generators for:

### Static Variables

| Generator Function | Variable | Source |
|--------------------|----------|--------|
| `gen_ne_disputed_area_share()` | Disputed territory share | Natural Earth |
| `gen_ruggedterrain()` | Terrain ruggedness | SRTM elevation data |
| `gen_cshapes_gwcode()` | Country codes (static) | cShapes |

### Time-Varying Variables

| Generator Function | Variable | Source | Temporal Resolution |
|--------------------|----------|--------|---------------------|
| `gen_ucdp_ged()` | Battle-related deaths | UCDP GED | Yearly (configurable) |
| `gen_ghsl_population_grid()` | Population | GHSL GHS-POP R2023A | 5-year intervals, 1975-2030 |
| `gen_cru_tmp()` | Temperature | CRU TS v4.09 | Monthly (configurable) |
| `gen_cru_pre()` | Precipitation | CRU TS v4.09 | Monthly (configurable) |
| `gen_cru_pet()` | Potential evapotranspiration | CRU TS v4.09 | Monthly (configurable) |
| `gen_spei6()` | SPEI-6 drought index | SPEIbase | Monthly (configurable) |
| `gen_hilda_*()` | Land use (cropland, forest, pasture, urban, water) | HILDA+ | Yearly |
| `gen_linight()` | Nighttime lights | VIIRS (likely) | Yearly |
| `gen_geoEPR_*()` | Ethnic group exclusion | GeoEPR | Yearly |
| `gen_geopko_*()` | Peacekeeping operations | GeoPKO | Yearly |
| `calc_traveltime()` | Travel time to cities | Accessibility datasets | Static/periodic |
| `gen_bdist1/2/3()` | Border distances | cShapes | Yearly |

### Key Differences: v2 vs v3 Variable Sets

| Aspect | v2 | v3 |
|--------|-----|-----|
| **Number of variables** | ~98 fixed | ~20+ generator functions, growing |
| **Population source** | GPW, HYDE | GHSL GHS-POP (higher res, more recent) |
| **Climate source** | GPCC, misc | CRU TS v4.09 (unified) |
| **Conflict data** | Not included in base grid | UCDP GED integrated |
| **Land use source** | ISAM-HYDE, Globcover | HILDA+ |
| **Nighttime lights** | DMSP-OLS (1992-2013) | VIIRS (more recent) |
| **Temporal flexibility** | Yearly only | Configurable (monthly/quarterly/yearly) |
| **Spatial flexibility** | 0.5° only | Configurable (any resolution/projection) |
| **Extensibility** | Fixed | Users can write custom generators |

---

## 6. Access Methods

### v2: Web Interface and Downloads

**Website:** https://grid.prio.org

**Download formats:** CSV and Shapefile

The v2 website provides:
- Interactive map viewer
- Variable selection and download
- API (REST endpoints at `grid.prio.org/api/`)
- Codebook documentation

**v2 API (grid.prio.org):**

The v2 API provides JSON access to variable metadata:
- `GET /api/variables` — List all 98 variables with metadata
- `GET /api/variables?type=static` — Static variables only
- `GET /api/variables?type=yearly` — Time-varying variables only

Note: The v2 web interface is a Single Page Application that may not render in simple web scrapers. The API endpoints return JSON directly.

### v3: R Package

**Repository:** https://github.com/prio-data/priogrid

**Documentation site:** https://prio-data.github.io/priogrid/

**Pre-built data download:** https://www.prio.org/data/40

**Installation:**

```r
install.packages("renv")
renv::install("prio-data/priogrid")
```

**System dependencies required:**
- `terra` (raster processing) — requires GDAL, PROJ, GEOS
- `sf` (vector spatial data) — requires GDAL, PROJ, GEOS
- `exactextractr` (spatial extraction) — requires GEOS

On Ubuntu/Debian:
```bash
sudo apt install libgdal-dev libproj-dev libgeos-dev
```

**Pre-built data files:**

Two ZIP files available from https://www.prio.org/data/40:
- `priogrid_300_05deg_yearly.zip` (v3.0.0)
- `priogrid_3_0_1_05deg_yearly.zip` (v3.0.1)

These contain pre-computed variables in CSV, Parquet, and RDS formats.

### v3: Basic R Usage

```r
library(priogrid)

# Configure data storage location
pgoptions$set_rawfolder("/path/to/data")
pgoptions$set_start_date(as.Date("1990-12-31"))
pgoptions$set_end_date(as.Date("2023-12-31"))

# Download the official pre-built release
download_priogrid()

# Load static data as a data.table
pg_static <- read_pg_static()
# Returns: data.table with pgid as rows, variables as columns

# Load time-varying data as a data.table
pg_tv <- read_pg_timevarying()
# Returns: data.table with pgid + measurement_date as rows, variables as columns

# Load a single variable as a SpatRaster
r <- load_pgvariable("cshapes_gwcode")

# Generate a blank grid with PRIO-GRID IDs
pg <- prio_blank_grid()

# Build a custom variable from source data
r_temp <- gen_cru_tmp()

# Change temporal resolution to monthly
pgoptions$set_temporal_resolution("1 month")
r_monthly <- gen_cru_tmp()

# Get citations for variables you use
pgcitations("ucdp_ged")
pgcitations("ucdp_ged", as_biblatex = TRUE)
```

---

## 7. Python Access

PRIO-GRID does not provide an official Python package. However, working with PRIO-GRID data in Python is straightforward because the pre-built releases are available in Parquet and CSV formats.

### Reading Pre-Built v3 Data in Python

```python
import pandas as pd
import pyarrow.parquet as pq

# After downloading and extracting priogrid_3_0_1_05deg_yearly.zip:
pg_static = pd.read_parquet("priogrid/releases/3.0.1/05deg_yearly/pg_static.parquet")
pg_tv = pd.read_parquet("priogrid/releases/3.0.1/05deg_yearly/pg_timevarying.parquet")

# Static data: one row per pgid
print(pg_static.head())
# pgid, variable1, variable2, ...

# Time-varying data: one row per (pgid, measurement_date)
print(pg_tv.head())
# pgid, measurement_date, variable1, variable2, ...
```

### Reading v2 CSV Data in Python

```python
import pandas as pd

# Static data (one row per cell)
pg_static = pd.read_csv("PRIO-GRID Static Variables - 2023-09-26.csv")

# Yearly data (one row per cell-year)
pg_yearly = pd.read_csv("PRIO-GRID Yearly Variables for 1946-2014 - 2023-09-26.csv")

# Key columns: gid, row, col, xcoord, ycoord, year (for yearly)
```

### Generating the PRIO-GRID from Scratch in Python

This is essential for Causal Atlas, since we need to create the grid programmatically without depending on R:

```python
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

def create_priogrid(resolution=0.5):
    """
    Generate the standard PRIO-GRID as a GeoDataFrame.

    Replicates the R create_pg_indices() logic:
    - 720 columns x 360 rows
    - Cell 1 at bottom-left (-180, -90)
    - Numbering goes east along rows, then north
    """
    ncol = int(360 / resolution)  # 720
    nrow = int(180 / resolution)  # 360

    records = []
    pgid = 1

    for row in range(nrow):  # 0 to 359, south to north
        lat_south = -90.0 + row * resolution
        lat_north = lat_south + resolution
        lat_centroid = lat_south + resolution / 2

        for col in range(ncol):  # 0 to 719, west to east
            lon_west = -180.0 + col * resolution
            lon_east = lon_west + resolution
            lon_centroid = lon_west + resolution / 2

            records.append({
                'pgid': pgid,
                'row': row + 1,
                'col': col + 1,
                'xcoord': lon_centroid,
                'ycoord': lat_centroid,
                'geometry': box(lon_west, lat_south, lon_east, lat_north)
            })
            pgid += 1

    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    return gdf

# Generate the grid
pg = create_priogrid()
print(f"Total cells: {len(pg)}")  # 259200
print(f"Cell 1: lon={pg.loc[0, 'xcoord']}, lat={pg.loc[0, 'ycoord']}")
# Cell 1: lon=-179.75, lat=-89.75
```

### Mapping Point Data to PRIO-GRID Cells in Python

```python
import numpy as np

def point_to_pgid(lon, lat, resolution=0.5):
    """Convert a longitude/latitude pair to a PRIO-GRID cell ID."""
    col = int((lon + 180.0) / resolution) + 1
    row = int((lat + 90.0) / resolution) + 1

    # Clamp to valid range
    col = max(1, min(col, 720))
    row = max(1, min(row, 360))

    pgid = (row - 1) * 720 + col
    return pgid

def pgid_to_centroid(pgid, resolution=0.5):
    """Convert a PRIO-GRID cell ID to centroid coordinates."""
    col = ((pgid - 1) % 720) + 1
    row = ((pgid - 1) // 720) + 1

    lon = -180.0 + (col - 1) * resolution + resolution / 2
    lat = -90.0 + (row - 1) * resolution + resolution / 2

    return lon, lat

# Example: Map an ACLED event in Mogadishu to its PRIO-GRID cell
pgid = point_to_pgid(45.3418, 2.0469)
print(f"Mogadishu PGID: {pgid}")
lon, lat = pgid_to_centroid(pgid)
print(f"Cell centroid: {lon}, {lat}")
```

### Mapping Raster Data to PRIO-GRID in Python

```python
import rasterio
import numpy as np
from rasterio.transform import from_bounds

def aggregate_raster_to_priogrid(raster_path, method='mean'):
    """
    Aggregate a raster dataset to PRIO-GRID 0.5-degree cells.

    Args:
        raster_path: Path to input raster (GeoTIFF, NetCDF, etc.)
        method: Aggregation method ('mean', 'sum', 'max', 'min')

    Returns:
        dict mapping pgid -> aggregated value
    """
    from rasterstats import zonal_stats
    import geopandas as gpd

    # Create PRIO-GRID polygons (or load from cache)
    pg = create_priogrid()

    # Compute zonal statistics
    stats = zonal_stats(
        pg.geometry,
        raster_path,
        stats=[method],
        all_touched=True
    )

    result = {}
    for i, stat in enumerate(stats):
        pgid = pg.iloc[i]['pgid']
        result[pgid] = stat[method]

    return result
```

### Working with PRIO-GRID in DuckDB (Parquet-Native)

```python
import duckdb

con = duckdb.connect()

# Load the pre-built Parquet data
con.execute("""
    CREATE TABLE pg_static AS
    SELECT * FROM read_parquet('priogrid/releases/3.0.1/05deg_yearly/pg_static.parquet')
""")

con.execute("""
    CREATE TABLE pg_timevarying AS
    SELECT * FROM read_parquet('priogrid/releases/3.0.1/05deg_yearly/pg_timevarying.parquet')
""")

# Join with your own data using pgid
con.execute("""
    SELECT t.pgid, t.measurement_date, t.ucdp_ged, t.cru_tmp
    FROM pg_timevarying t
    WHERE t.measurement_date >= '2010-01-01'
    AND t.ucdp_ged > 0
    ORDER BY t.ucdp_ged DESC
    LIMIT 20
""")
```

---

## 8. Quality and Limitations

### Spatial Resolution Limitations

- **0.5 degrees is coarse** for many applications. At the equator, each cell is ~3,080 km². Urban-level analysis is not possible. Events occurring at different locations within the same cell are treated as co-located.
- **Area distortion:** Because the grid uses an equirectangular projection (WGS84), cells at higher latitudes cover less actual area than cells at the equator. This must be accounted for in any area-weighted analysis. The cell at 60°N covers roughly half the area of a cell at the equator.
- **Coastal cells:** Cells along coastlines contain a mix of land and water. The `landarea` variable accounts for this, but some variables may not be properly weighted by land area.
- **Ocean cells:** PRIO-GRID is designed for terrestrial analysis. Ocean cells are generally empty/NA, though some variables (nighttime lights, for instance) may have values over water.

### Temporal Limitations (v2)

- **Yearly resolution only** in v2, which means sub-annual dynamics (seasonal patterns, monthly shocks) cannot be captured.
- **Variable temporal coverage is uneven:** Some variables cover 1946-2014, others only 1990-2005 or 1992-2013. Any panel analysis must handle this.
- **Data ends at 2014** in v2, making it increasingly outdated.

### Known Data Quality Issues

- **Population data:** GPW and HYDE population estimates involve significant interpolation and downscaling. Actual sub-national population distribution is uncertain, especially in conflict-affected or data-sparse regions.
- **GCP (Gross Cell Product):** Only available 1990-2005 with quality issues. The GCP estimates involve disaggregating national GDP to grid cells using nighttime lights as a proxy, which introduces circular reasoning if used alongside nighttime lights.
- **Nighttime lights:** DMSP-OLS data (v2) has saturation issues in urban centres and inter-calibration challenges across satellites. v3 should address this with VIIRS data.
- **Resource variables:** Mineral deposit data is based on known deposits, which biases toward regions with more geological surveys. Absence of a deposit marker does not mean absence of the resource.
- **Country assignment:** Border regions and disputed territories can be assigned to different countries depending on the cShapes version used. This affects all country-level variables.

### v3 Stability Warning

PRIO-GRID v3 (the `priogrid` R package) is explicitly marked as an **"unstable Alpha release"** as of March 2025. The PRIO team warns that breaking changes may occur before the beta release. The variable set is also smaller than v2 (the team is progressively adding generators).

---

## 9. Licence and Citation

### v2 Licence

PRIO-GRID v2 data is freely available for academic and non-commercial use. Individual variables carry their own source data licences (e.g., GPCC precipitation data has its own terms). Users must cite both PRIO-GRID and the original data sources.

### v3 Licence

The `priogrid` R package uses a triple licence: **MIT + ODC-By + file LICENSE**. This covers the code and the derived data, respectively. The MIT licence applies to the R package code. The ODC-By licence applies to the database/data compilation. Individual source datasets retain their original licences (typically CC-BY).

### Citation Requirements

**Always cite:**

1. The PRIO-GRID system itself:
   > Tollefsen, A. F., Strand, H., & Buhaug, H. (2012). PRIO-GRID: A Unified Spatial Data Structure. *Journal of Peace Research*, 49(2), 363-374.

2. For v3 R package:
   > Vestby, J. & Tollefsen, A. F. (2025). PRIOGRID: An R-package for collecting and standardizing open spatial data.

3. **All original data sources used.** The v3 package provides `pgcitations()` to automatically generate citations for the variables you use. This is not optional — most source data licences (CC-BY) legally require attribution.

The `pgcitations()` function in v3:
```r
# Print citations for all time-varying variables
pgcitations(names(pg_timevarying))

# Get BibLaTeX format for a specific variable
pgcitations("ucdp_ged", as_biblatex = TRUE)
```

---

## 10. Interoperability: Mapping Other Datasets to PRIO-GRID

### Point Data (ACLED, UCDP GED, GDELT)

Event datasets with latitude/longitude coordinates are the easiest to map:

```python
# For any event with (lon, lat):
col = int((lon + 180.0) / 0.5) + 1
row = int((lat + 90.0) / 0.5) + 1
pgid = (row - 1) * 720 + col
```

UCDP GED explicitly includes PRIO-GRID cell assignments in its data. ACLED does not, but can be mapped using the above formula.

**Spatial precision caveat:** UCDP GED assigns spatial precision codes (1-6). The v3 `gen_ucdp_ged()` function only uses events with precision codes 1-5 (sub-national or better), excluding national-level-only events (code 6). This prevents incorrectly gridding events whose locations are only known at the country level.

### Administrative Region Data (World Bank, FAO, DHS)

For data reported at admin-1 or admin-2 level:

1. **Area-weighted overlay:** Intersect admin polygons with PRIO-GRID cells. For each cell, weight the admin-region value by the proportion of the cell covered by that admin region.
2. **Population-weighted overlay:** Similar to area-weighted, but use population as the weight (requires a population raster).
3. **Centroid assignment:** Assign each cell the value of the admin region containing its centroid. Simpler but less accurate for cells straddling borders.

The `exactextractr` R package (a dependency of v3 priogrid) is optimised for this type of operation.

### Raster Data (CHIRPS, MODIS NDVI, VIIRS nightlights)

Raster datasets at higher resolution than 0.5° must be aggregated:

1. **Mean:** For continuous variables like temperature, NDVI, precipitation rate.
2. **Sum:** For count variables like population, total precipitation.
3. **Max/Min:** For extreme values.
4. **Exact extraction:** The `exactextractr` (R) or `rasterstats` (Python) approach handles sub-cell weighting properly, accounting for cells that partially overlap.

### Country-Level Crosswalk

PRIO-GRID uses the **Gleditsch & Ward (GW) country coding system** via cShapes. This differs from ISO country codes. Key mappings:

- GW codes are time-varying (countries are born, die, merge, split)
- cShapes provides the historical country boundaries used to assign `gwno` to each cell each year
- To link PRIO-GRID cells to ISO-coded datasets, a GW-to-ISO crosswalk is needed (available from the Correlates of War project and others)

### Compatibility with Other Grid Systems

| System | Resolution | Compatible? | Notes |
|--------|-----------|-------------|-------|
| **CRU TS** | 0.5° x 0.5° | Direct match | Same grid resolution; v3 uses CRU TS natively |
| **GPCC** | 0.5° (and others) | Direct match at 0.5° | v2 uses GPCC precipitation |
| **CHIRPS** | 0.05° | Aggregate 10x10 | 100 CHIRPS cells per PRIO-GRID cell |
| **MODIS** | 250m-1km | Aggregate heavily | Thousands of pixels per cell |
| **GPW** | 2.5 arc-min (~5km) | Aggregate ~6x6 | 36 GPW cells per PRIO-GRID cell |
| **GHSL** | 100m-1km | Aggregate heavily | v3 uses GHSL natively |
| **WorldPop** | 100m-1km | Aggregate heavily | |
| **ERA5** | 0.25° | Aggregate 2x2 | 4 ERA5 cells per PRIO-GRID cell |
| **AfroGrid** | 0.5° x 0.5° | Aligned | AfroGrid uses PRIO-GRID compatible resolution |

---

## 11. v2 vs v3: Detailed Comparison

| Aspect | v2 (PRIO-GRID 2.0) | v3 (priogrid R package) |
|--------|---------------------|-------------------------|
| **Philosophy** | Fixed dataset | Research tool / data factory |
| **Distribution** | CSV + Shapefile download | R package + Parquet/CSV/RDS releases |
| **Grid flexibility** | Fixed 720x360 only | Configurable resolution, extent, CRS |
| **Temporal resolution** | Yearly only | Configurable (month/quarter/year) |
| **Temporal range** | 1946-2014 | 1885-2024+ |
| **Variable count** | ~98 | ~20+ generators (growing) |
| **Data sources** | GPCC, GPW, HYDE, DMSP-OLS, etc. | CRU TS, GHSL, UCDP GED, HILDA+, etc. |
| **Web interface** | grid.prio.org (interactive map) | None (R/CLI only) |
| **API** | REST API at grid.prio.org | R function calls |
| **Cell ID field** | `gid` | `pgid` |
| **Status** | Stable, widely cited | Alpha, unstable |
| **Python support** | CSV import | Parquet import |
| **Extensibility** | None | Write custom `gen_*()` functions |
| **Citation support** | Manual | `pgcitations()` auto-generates |
| **Memory management** | N/A | Auto disk-based above 4GB |
| **Reproducibility** | Download exact version | Spatial/temporal hash system |

### When to Use Which

- **Use v2** if you need a stable, well-established dataset with comprehensive variable coverage, especially for historical analysis (1946-2014).
- **Use v3** if you need monthly temporal resolution, more recent data (post-2014), custom grid configurations, or integration with UCDP GED conflict data directly.
- **For Causal Atlas:** We should use both. The v2 data provides valuable historical coverage. The v3 Parquet releases provide a modern data format. The v3 grid construction logic should be replicated in Python for our core spatial engine.

---

## 12. The VIEWS Connection

The **VIEWS (Violence Early-Warning System)** forecasting project, also based at PRIO and Uppsala University, uses PRIO-GRID as its spatial unit of analysis at the sub-national level. VIEWS produces monthly conflict forecasts at the PRIO-GRID cell-month level, making it a direct validation case for spatiotemporal analysis on this grid.

VIEWS demonstrates that PRIO-GRID can support:
- Monthly temporal resolution (not just yearly)
- Machine learning models at the cell-month level
- Multi-domain feature integration (conflict, climate, socioeconomic data)
- Operational forecasting, not just historical analysis

This is directly relevant to Causal Atlas: if VIEWS can do monthly forecasting on PRIO-GRID cells, we can do monthly causal analysis on the same grid.

---

## 13. Relevance to Causal Atlas

PRIO-GRID is the spatial backbone of Causal Atlas. Here is how we should use it:

### What We Adopt

1. **The 0.5° x 0.5° grid** as our primary spatial unit. All datasets will be mapped to these cells.
2. **The pgid numbering convention** (cell 1 at SW corner, numbering east then north) for consistent cell identification.
3. **WGS84 (EPSG:4326) projection** as the coordinate reference system.
4. **The v3 Parquet data** as a starting point for pre-computed variables (climate, population, terrain, conflict).

### What We Build Ourselves

1. **Python grid generation** — We replicate `create_pg_indices()` in Python (see Section 7 above) rather than depending on R.
2. **Ingestion adapters** — Each data source gets a Python adapter that maps its data to pgid cells.
3. **Monthly temporal resolution** — We follow v3's lead and use monthly as our primary temporal unit, with daily preserved where available.
4. **Extended variable coverage** — We ingest many more data sources than PRIO-GRID includes (food prices, air quality, disease outbreaks, earthquakes, etc.).

### Implementation Strategy

1. **Phase 1:** Download v3 pre-built Parquet files. Load into DuckDB. This gives us immediate access to terrain, climate, population, and conflict data on the grid.
2. **Phase 2:** Build Python utilities for pgid computation, point-to-cell mapping, raster aggregation, and admin-region overlay.
3. **Phase 3:** Build ingestion adapters for each additional data source, all outputting `(pgid, date, variable, value)` tuples.
4. **Phase 4:** Store everything in DuckDB/Parquet with pgid and date as the join keys.

### Key Design Decisions Informed by PRIO-GRID

- **Cell area correction:** Any density or rate calculation must account for the latitude-dependent cell area. Use `cos(latitude_radians)` as a correction factor.
- **Land masking:** Ocean cells should be masked out. Use a land area variable or Natural Earth land polygons.
- **Country assignment:** Use the time-varying `gwno`/`cshapes_gwcode` to correctly assign cells to countries for each time period.
- **Border effects:** Cells at country borders may be split between countries. Some analyses should use border distance variables to control for this.

---

## 14. Data Storage Architecture (v3)

The v3 package organises data on disk as follows:

```
{rawfolder}/
├── {source_name}/{version}/{id}/          # Raw downloaded source files
│   └── (original files from data providers)
├── priogrid/
│   ├── releases/
│   │   ├── 3.0.0/
│   │   │   └── 05deg_yearly/
│   │   │       ├── pg_static.parquet
│   │   │       ├── pg_timevarying.parquet
│   │   │       ├── pg_timevarying.csv.gz
│   │   │       └── {variable_name}.rds     # Individual SpatRaster files
│   │   └── 3.0.1/
│   │       └── 05deg_yearly/
│   │           └── (same structure)
│   ├── custom/
│   │   └── {pkg_version}/
│   │       └── {spatial_hash}/             # 6-char MD5 of spatial config
│   │           └── {temporal_hash}/        # 6-char MD5 of temporal config
│   │               ├── pg_static.parquet
│   │               ├── pg_timevarying.parquet
│   │               └── {variable_name}.rds
│   ├── priogrid_3_0_0_05deg_yearly.zip
│   └── priogrid_3_0_1_05deg_yearly.zip
└── tmp/                                    # Temporary files, auto-cleaned
```

The hash-based custom directory system ensures that different spatial/temporal configurations do not overwrite each other. This is relevant for Causal Atlas if we ever experiment with different grid resolutions.

### Pre-Built Release Download URLs

| Release | URL |
|---------|-----|
| v3.0.0 | `https://cdn.cloud.prio.org/files/379b7254-b47c-48f3-a650-783348d0ff7e` |
| v3.0.1 | `https://cdn.cloud.prio.org/files/1c76a606-8efa-4dc0-a938-301c4e9331e6` |

These are direct download links to ZIP files containing Parquet, CSV, and RDS data.

---

## 15. Sources and References

### Primary Resources

| Resource | URL |
|----------|-----|
| PRIO-GRID v2 website | https://grid.prio.org |
| PRIO-GRID data page (v3 downloads) | https://www.prio.org/data/40 |
| priogrid R package (GitHub) | https://github.com/prio-data/priogrid |
| priogrid R package documentation | https://prio-data.github.io/priogrid/ |
| priogrid citation guide | https://prio-data.github.io/priogrid/articles/citation.html |
| priogrid function reference | https://prio-data.github.io/priogrid/reference/index.html |

### Academic Papers

- Tollefsen, A. F., Strand, H., & Buhaug, H. (2012). PRIO-GRID: A Unified Spatial Data Structure. *Journal of Peace Research*, 49(2), 363-374. https://doi.org/10.1177/0022343311431287
- Vestby, J. & Tollefsen, A. F. (2025). PRIOGRID: An R-package for collecting and standardizing open spatial data. (Package documentation / forthcoming paper)
- Harris, I., Osborn, T. J., Jones, P., & Lister, D. (2020). Version 4 of the CRU TS monthly high-resolution gridded multivariate climate dataset. *Scientific Data*, 7(1), 109. (CRU TS, used by v3 for climate data)
- Schiavina, M., Freire, S., Carioli, A., & MacManus, K. (2023). GHS-POP R2023A - GHS population grid multitemporal (1975-2030). European Commission, Joint Research Centre. (GHSL, used by v3 for population data)

### Related Projects Using PRIO-GRID

- **VIEWS (Violence Early-Warning System):** https://viewsforecasting.org — Monthly conflict forecasts at PRIO-GRID cell level
- **UCDP GED:** https://ucdp.uu.se — Conflict event data with PRIO-GRID cell assignments
- **cShapes:** https://icr.ethz.ch/data/cshapes/ — Historical country boundaries used for country assignment
- **GeoEPR:** https://icr.ethz.ch/data/epr/geoepr/ — Ethnic group settlement areas mapped to grid
- **AfroGrid:** Uses PRIO-GRID compatible 0.5° resolution for Africa

### Source Data Used by PRIO-GRID (37 sources catalogued in v3)

The v3 `pgsources` data frame catalogues 37 data sources relevant to quantitative conflict research. Key sources include:
- UCDP GED (conflict events)
- GHSL GHS-POP (population)
- CRU TS v4.09 (temperature, precipitation, evapotranspiration)
- SPEIbase (drought index)
- HILDA+ (land use change)
- Natural Earth (administrative boundaries, disputed areas)
- cShapes (historical country boundaries)
- GeoEPR (ethnic group geography)
- GeoPKO (peacekeeping operations)
- SRTM (terrain elevation/ruggedness)
- Li et al. nighttime lights

New sources can be proposed via GitHub issues: https://github.com/prio-data/priogrid/issues/new/choose
