# 08 — Architecture Notes: Emerging Decisions and Open Questions

> **Status:** In progress (first pass)
> **Last updated:** March 2025
> **Purpose:** Capture architecture decisions as they emerge from research, before any code is written. This is a living document.

---

## Table of Contents

1. [Canonical Data Format](#1-canonical-data-format)
2. [Adapter Architecture](#2-adapter-architecture)
3. [Spatial Aggregation](#3-spatial-aggregation)
4. [Storage Backend](#4-storage-backend)
5. [Real-time vs Historical](#5-real-time-vs-historical)
6. [API Design](#6-api-design)
7. [Frontend Architecture](#7-frontend-architecture)
8. [Minimum Viable Product](#8-minimum-viable-product)
9. [AI Integration](#9-ai-integration)
10. [Open Questions](#10-open-questions)

---

## 1. Canonical Data Format

### Why Parquet

Apache Parquet is the right storage format for Causal Atlas. The reasons are well-established and align with what similar projects are converging on:

- **Columnar storage** -- analytical queries (e.g., "give me all rainfall values for 2020") only read the columns they need, skipping irrelevant data entirely
- **Built-in compression** -- Parquet uses dictionary encoding, run-length encoding, and delta encoding, typically achieving 5-10x compression over CSV for this kind of data
- **Schema-embedded** -- the schema (column names, types, nullability) travels with the file, eliminating the "what are these columns?" problem
- **Predicate pushdown** -- DuckDB reads Parquet row group metadata and skips groups that cannot match a WHERE clause, dramatically reducing I/O ([DuckDB Parquet tips](https://duckdb.org/docs/stable/data/parquet/tips))
- **Ecosystem support** -- Python (pyarrow, pandas, polars), R (arrow), DuckDB, Spark, and browser-based tools (DuckDB-WASM) all read Parquet natively
- **GeoParquet** -- the OGC GeoParquet 1.1.0 specification extends Parquet with geometry columns and spatial metadata, enabling spatial filtering via bounding box columns ([geoparquet.org](https://geoparquet.org/))

PRIO-GRID v3 already distributes data in Parquet format alongside CSV and RDS, confirming that the geospatial research community has adopted this format ([PRIO-GRID downloads](https://grid.prio.org/)).

### Proposed Schema: Long (Narrow) Format

The primary storage format should be **long/narrow** -- one row per observation:

```
Column          Type        Description
------          ----        -----------
gid             INT32       PRIO-GRID cell ID (1 to 259,200)
year            INT16       Year of observation
month           INT8        Month (1-12), 0 for annual data
variable_name   VARCHAR     Canonical variable identifier (e.g., "acled_fatalities", "chirps_precip_mm")
value           FLOAT64     The observed/computed value
source          VARCHAR     Data source identifier (e.g., "acled_v24", "chirps_v2")
quality_flag    INT8        0 = observed, 1 = interpolated, 2 = modelled, 3 = missing/imputed
ingested_at     TIMESTAMP   When this record was ingested
```

**Advantages of long format:**
- Adding new variables requires no schema migration -- just new rows
- Uniform query pattern: `WHERE variable_name = 'X' AND year BETWEEN A AND B`
- Easy to track provenance per observation (source, quality)
- Natural fit for time-series analysis queries

### Alternative: Wide Format

For analysis, a **wide/pivoted** format is often more convenient -- one row per grid cell per time step, one column per variable:

```
gid | year | month | acled_fatalities | chirps_precip_mm | wfp_price_maize | ...
```

**Advantages of wide format:**
- Correlation analysis across variables is a single table scan (no joins/pivots)
- More compact when most cells have values for most variables
- Familiar to researchers (looks like a spreadsheet)

**Decision:** Store in long format as the canonical representation. Provide materialised wide views for specific analysis tasks. DuckDB's `PIVOT` function makes this transformation trivial at query time.

### Partitioning Strategy

Parquet files should be partitioned by **variable domain** and **year** using Hive-style partitioning:

```
data/
  domain=conflict/
    year=2020/
      acled_fatalities.parquet
      ucdp_ged_events.parquet
    year=2021/
      ...
  domain=climate/
    year=2020/
      chirps_precip_mm.parquet
      ndvi_mean.parquet
    ...
  domain=food_security/
    ...
```

This enables:
- **Partition pruning** -- queries scoped to a domain or year range skip irrelevant files entirely
- **Incremental updates** -- new data for a year can be rewritten without touching other partitions
- **Manageable file sizes** -- each file covers one variable, one year, globally (~259,200 rows for monthly data = ~3.1M rows/year), well within Parquet's sweet spot

A rule of thumb from DuckDB documentation: ensure the number of row groups per file is at least as large as the number of CPU threads used to query that file ([DuckDB Parquet tips](https://duckdb.org/docs/stable/data/parquet/tips)).

### DuckDB's Native Parquet Support

DuckDB can query Parquet files directly without importing them, using `read_parquet()` or `parquet_scan()`:

```sql
SELECT gid, year, month, value
FROM read_parquet('data/domain=climate/year=2020/chirps_precip_mm.parquet')
WHERE gid = 142567 AND month BETWEEN 6 AND 9;
```

DuckDB also supports:
- **Glob patterns** for querying across partitions: `read_parquet('data/domain=*/year=*/**.parquet')`
- **Hive partition auto-detection**: partition columns (domain, year) are automatically extracted
- **Parallel reading** of row groups within and across files
- **Parquet metadata caching** for repeated queries

As of DuckDB v1.1+, the spatial extension reads and writes GeoParquet natively, including bounding box columns for fast spatial filtering ([DuckDB GeoParquet tutorials](https://github.com/cholmes/duckdb-geoparquet-tutorials)).

---

## 2. Adapter Architecture

### Design Principles

Each data source gets a dedicated **adapter** -- a self-contained Python module responsible for fetching, parsing, validating, transforming, and writing data from that source into our canonical Parquet format.

This mirrors the approach taken by the VIEWS platform, where the pipeline processes raw geo-temporal data through deterministic data preparation stages with queryset and transformation replay ([VIEWS pipeline core](https://github.com/views-platform/views-pipeline-core)).

### Common Interface

Every adapter implements the same abstract interface:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from pathlib import Path

@dataclass
class AdapterConfig:
    source_id: str               # e.g., "acled_v24"
    domain: str                  # e.g., "conflict"
    api_key: str | None = None
    base_url: str | None = None
    rate_limit_rps: float = 1.0  # requests per second

class BaseAdapter(ABC):
    def __init__(self, config: AdapterConfig, output_dir: Path):
        self.config = config
        self.output_dir = output_dir

    @abstractmethod
    def fetch(self, start_date: date, end_date: date) -> bytes | Path:
        """Download raw data from the source. Returns raw bytes or path to temp file."""
        ...

    @abstractmethod
    def parse(self, raw_data: bytes | Path) -> "pa.Table":
        """Parse raw data into a PyArrow Table with source-native schema."""
        ...

    @abstractmethod
    def validate(self, table: "pa.Table") -> "pa.Table":
        """Validate data quality. Add quality_flag column. Raise on critical issues."""
        ...

    @abstractmethod
    def transform(self, table: "pa.Table") -> "pa.Table":
        """Transform to canonical schema: gid, year, month, variable_name, value, ..."""
        ...

    def write(self, table: "pa.Table") -> Path:
        """Write to partitioned Parquet. Common implementation, rarely overridden."""
        ...

    def run(self, start_date: date, end_date: date) -> Path:
        """Full pipeline: fetch -> parse -> validate -> transform -> write."""
        raw = self.fetch(start_date, end_date)
        parsed = self.parse(raw)
        validated = self.validate(parsed)
        transformed = self.transform(validated)
        return self.write(transformed)
```

### Error Handling and Retry Logic

- **Exponential backoff** with jitter for API failures (use `tenacity` library)
- **Checkpointing** -- adapters record the last successfully ingested time range, enabling resume after failure
- **Idempotent writes** -- rerunning an adapter for the same date range overwrites the same partition, producing identical results
- **Rate limiting** -- configurable per adapter, respecting source-specific limits (e.g., ACLED: ~1 req/s, GDELT: liberal, USGS: ~5 req/s)
- **Dead letter logging** -- records that fail validation are written to a separate file for manual review rather than silently dropped

### Incremental Updates

Adapters support two modes:
- **Full refresh**: re-ingest all data for a date range (used for initial load and periodic reconciliation)
- **Incremental**: fetch only data newer than the last checkpoint (used for regular updates)

The VIEWS platform uses a similar two-track approach: full retraining on annually vetted data (UCDP GED), plus monthly incremental updates for near-real-time forecasting ([VIEWS forecasting](https://viewsforecasting.org/early-warning-system/)).

### Registry Pattern for Adapter Discovery

Adapters register themselves via a simple registry, enabling dynamic discovery:

```python
ADAPTER_REGISTRY: dict[str, type[BaseAdapter]] = {}

def register_adapter(source_id: str):
    def decorator(cls: type[BaseAdapter]):
        ADAPTER_REGISTRY[source_id] = cls
        return cls
    return decorator

@register_adapter("acled")
class ACLEDAdapter(BaseAdapter):
    ...

@register_adapter("chirps")
class CHIRPSAdapter(BaseAdapter):
    ...
```

This allows a CLI tool or scheduler to discover and run adapters by name: `python -m causal_atlas.ingest --source acled --start 2020-01 --end 2024-12`

---

## 3. Spatial Aggregation

### Should We Use PRIO-GRID Cell IDs Directly?

**Decision: Yes, use PRIO-GRID cell IDs as our primary spatial identifier.**

Rationale:
- PRIO-GRID is the established standard in conflict and peace research, used by VIEWS, UCDP, and dozens of published studies
- PRIO-GRID v3 covers the full globe at 0.5 x 0.5 degree resolution (720 columns x 360 rows = 259,200 cells), with EPSG:4326 CRS ([PRIO-GRID](https://grid.prio.org/))
- It provides a stable cell ID that does not change between versions, enabling cross-study comparability
- It already includes pre-computed static variables (terrain, distance to borders, etc.) that we can use directly
- Creating our own grid would fragment compatibility with the research ecosystem for no clear benefit

### PRIO-GRID Cell ID Calculation

The cell ID can be computed deterministically from latitude/longitude:

```python
import numpy as np

def latlon_to_gid(lat: float, lon: float) -> int:
    """Convert lat/lon to PRIO-GRID cell ID (1-indexed).

    Grid: 720 columns (lon) x 360 rows (lat), 0.5 degree cells.
    Origin: bottom-left (-90, -180).
    Cell centres at -89.75, -89.25, ..., 89.75 (lat)
                    -179.75, -179.25, ..., 179.75 (lon)
    """
    col = int((lon + 180) / 0.5)  # 0 to 719
    row = int((lat + 90) / 0.5)   # 0 to 359
    return row * 720 + col + 1    # 1-indexed

def gid_to_latlon(gid: int) -> tuple[float, float]:
    """Convert PRIO-GRID cell ID to cell centre lat/lon."""
    gid_0 = gid - 1
    row = gid_0 // 720
    col = gid_0 % 720
    lat = -90 + row * 0.5 + 0.25  # cell centre
    lon = -180 + col * 0.5 + 0.25
    return lat, lon
```

### Pros and Cons of 0.5 Degree Resolution

| Aspect | Assessment |
|--------|-----------|
| Spatial precision | ~55 km at equator, ~28 km at 60 degrees latitude. Coarse for urban analysis but appropriate for regional/national patterns |
| Data volume | 259,200 cells globally. With 50 variables x 12 months x 30 years = manageable (~4.7 billion rows in long format, ~90 GB compressed Parquet) |
| Source compatibility | CHIRPS, MODIS NDVI, and ERA5 are available at finer resolution and aggregate well. ACLED/UCDP events geocode to points that map to cells. Country-level data (World Bank, FAO) must be disaggregated or linked via lookup |
| Computation | Correlation analysis across all cells and variable pairs is tractable on a single machine |
| Precedent | Used by PRIO-GRID, VIEWS, and the broader conflict research community |

### Multi-Resolution Support

Some analyses benefit from finer resolution (e.g., 0.05 degrees for urban areas, 0.25 degrees for climate data). We should support this as a secondary capability:

- **Primary grid**: 0.5 degree (PRIO-GRID compatible), used for all cross-domain analysis
- **Sub-grid**: finer resolution data stored separately, aggregated up to 0.5 degree for integration
- **Grid generation** via numpy:

```python
def generate_grid(resolution: float = 0.5):
    """Generate grid cell centres and IDs."""
    lats = np.arange(-90 + resolution/2, 90, resolution)
    lons = np.arange(-180 + resolution/2, 180, resolution)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    n_cols = len(lons)
    gids = np.arange(1, len(lats) * len(lons) + 1).reshape(len(lats), n_cols)
    return lat_grid, lon_grid, gids
```

PRIO-GRID v3 itself uses the R `terra` package for raster operations and switches to disk-based processing when estimated memory exceeds 4 GB -- a pattern worth noting for our Python implementation using `rasterio` or `xarray` ([PRIO-GRID GitHub](https://github.com/prio-data/priogrid)).

---

## 4. Storage Backend

### DuckDB vs PostGIS vs Both

This is a critical architectural decision. The three options:

| Criterion | DuckDB | PostGIS | Hybrid |
|-----------|--------|---------|--------|
| Analytical queries | Excellent -- columnar, vectorised, Parquet-native | Good but row-oriented, slower for large scans | Best of both |
| Spatial queries | Good -- spatial extension + GeoParquet | Excellent -- mature spatial indexing, ST_* functions | Best of both |
| Deployment complexity | Zero -- embedded, single file, no server | Moderate -- requires PostgreSQL server | Higher -- two systems to maintain |
| Client-side use | DuckDB-WASM runs in browser | Not possible | DuckDB-WASM for client |
| Concurrent writes | Limited (single writer) | Excellent (MVCC) | PostGIS for writes |
| Ecosystem | Growing fast, excellent Python/JS support | Mature, decades of tooling | Both ecosystems |

### Recommended: DuckDB-Primary with Optional PostGIS

**Decision: DuckDB as the primary analytical engine, reading directly from Parquet files. PostGIS as an optional layer for applications that need concurrent writes or complex spatial operations.**

Rationale:
- For a research-oriented platform, analytical query speed matters more than write concurrency
- DuckDB + Parquet requires no infrastructure -- anyone can clone the repo, download the data, and start querying
- This aligns with the project's open-source, accessible ethos
- PostGIS can be added later if needed for a production web service with concurrent users

DuckDB's in-process architecture means zero network overhead for queries, and its columnar engine is purpose-built for the aggregate/filter/group-by patterns that dominate spatiotemporal analysis ([DuckDB architecture](https://endjin.com/blog/2025/04/duckdb-in-depth-how-it-works-what-makes-it-fast)).

### Data Volume Estimates

```
Grid cells:              259,200 (global, 0.5 degree)
Time steps:              360 (30 years x 12 months)
Variables (initial):     ~20
Variables (full):        ~100

Long format rows:
  Initial:   259,200 x 360 x 20    = ~1.9 billion rows
  Full:      259,200 x 360 x 100   = ~9.3 billion rows

Estimated storage (Parquet, compressed):
  Initial:   ~15-30 GB
  Full:      ~80-150 GB

DuckDB query performance (estimated):
  Single cell time series:  < 100ms
  Regional aggregation:     < 1s
  Global correlation scan:  10-60s depending on variable count
```

These volumes are well within DuckDB's capabilities on a modern laptop (16-32 GB RAM). For the MVP (3-5 sources, one region, 10 years), we are looking at < 1 GB of data.

---

## 5. Real-time vs Historical

### Two-Track Approach

Data sources fall into two categories with very different update patterns:

**Near-real-time sources (hours to days):**

| Source | Update Frequency | Mechanism |
|--------|-----------------|-----------|
| GDELT | Every 15 minutes | HTTP file dumps |
| USGS Earthquakes | Real-time | REST API, streaming |
| OpenAQ | Hourly | REST API |
| ACLED | Weekly | API / CSV download |
| WFP food prices | Weekly to monthly | HDX API |

**Batch/historical sources (monthly to annual):**

| Source | Update Frequency | Mechanism |
|--------|-----------------|-----------|
| CHIRPS rainfall | Monthly (2-month lag) | FTP / HTTP download |
| MODIS/VIIRS NDVI | 16-day composites | NASA LAADS |
| PRIO-GRID | Annual | Download from grid.prio.org |
| UCDP GED | Annual (vetted) | API / download |
| World Bank / FAO | Annual | API |
| VIIRS nightlights | Monthly composites | NASA / EOG |

### Update Pipeline Design

```
Historical Pipeline (batch):
  Schedule: Monthly cron job
  Process: Full refresh for previous month
  Triggers: Calendar-based (1st of each month)

Live Pipeline (near-real-time):
  Schedule: Varies by source (hourly to weekly)
  Process: Incremental fetch from last checkpoint
  Triggers: Cron + optional webhook listeners

Reconciliation:
  Schedule: Quarterly
  Process: Re-ingest last 6 months from all sources
  Purpose: Catch retroactive corrections (ACLED, UCDP revise data)
```

The VIEWS platform follows a similar pattern: monthly near-real-time forecasts using the latest available data, coupled with rigorous annual evaluation against vetted UCDP GED releases ([VIEWS early warning system](https://viewsforecasting.org/early-warning-system/)).

### Scheduling

Use a simple cron-based scheduler initially (no Airflow/Dagster complexity for MVP):

```
# /etc/cron.d/causal-atlas
0 2 * * 1   causal-atlas ingest --source acled --mode incremental
0 3 1 * *   causal-atlas ingest --source chirps --mode full --month previous
0 4 * * *   causal-atlas ingest --source usgs --mode incremental
0 5 * * *   causal-atlas ingest --source openaq --mode incremental
```

Graduate to a proper workflow orchestrator (Prefect, Dagster) when the number of adapters and their dependencies warrant it.

---

## 6. API Design

### FastAPI Backend

FastAPI is the natural choice for the backend API:
- Async-first, high performance
- Automatic OpenAPI documentation
- Pydantic models for request/response validation
- Excellent geospatial ecosystem integration (GeoAlchemy2, Shapely) ([FastAPI + PostGIS](https://medium.com/@nunocarvalhodossantos/fastapi-postgis-and-geoalchemy-2-powerful-and-location-aware-web-applications-3b23f44c8fa5))

### Proposed Endpoints

```
GET /api/v1/grid/{gid}/timeseries
  Query params: variables, start_date, end_date
  Returns: time series for specified variables at a grid cell

GET /api/v1/grid/region
  Query params: bbox (or country_iso3), variables, date
  Returns: spatial snapshot of variables for a region at a point in time

GET /api/v1/variables
  Returns: catalogue of all available variables with metadata

GET /api/v1/correlations
  Query params: var_a, var_b, region, time_range, lag_months
  Returns: correlation results (Pearson, Granger, etc.) with significance

GET /api/v1/causal/search
  Query params: target_variable, region, time_range
  Returns: variables with significant lagged correlations to the target

POST /api/v1/interpret
  Body: { correlation_result, context }
  Returns: AI-generated interpretation of the correlation pattern

GET /api/v1/tiles/{z}/{x}/{y}.mvt
  Returns: Mapbox Vector Tiles for map visualisation layer
```

### Query Pattern Optimisation

The most common query pattern is: "give me all variables for grid cell X over time range Y." In long format, this is:

```sql
SELECT variable_name, year, month, value, quality_flag
FROM read_parquet('data/domain=*/year=*/**.parquet',
     hive_partitioning=true)
WHERE gid = :gid
  AND year BETWEEN :start_year AND :end_year
ORDER BY variable_name, year, month;
```

With Parquet partitioning by year and domain, DuckDB prunes irrelevant files and uses predicate pushdown on `gid` within each file. For the API layer, pre-materialised DuckDB views or cached results handle hot queries.

### Authentication and Rate Limiting

- Public read access for aggregated data (no API key needed)
- API key required for raw grid-level data and compute-intensive endpoints (correlation, causal search)
- Rate limiting via FastAPI middleware (e.g., `slowapi`)

---

## 7. Frontend Architecture

### React + Kepler.gl

Kepler.gl is the leading open-source library for large-scale geospatial visualisation, and it integrates directly with React via Redux state management ([Kepler.gl docs](https://docs.kepler.gl/)). Key capabilities:

- Renders millions of data points with WebGL
- Built-in support for heatmaps, hex bins, arcs, and grid layers
- Time playback animation (critical for our temporal dimension)
- As of 2025, Kepler.gl has native DuckDB integration for in-browser SQL queries on large datasets ([Kepler.gl release notes](https://docs.kepler.gl/release-notes))
- Vector tile support for serving large datasets without transferring all data to the client

### DuckDB-WASM for Client-Side Analytics

DuckDB-WASM enables running analytical SQL queries directly in the browser, eliminating round-trips to the server for exploratory analysis ([DuckDB-WASM paper](https://dl.acm.org/doi/abs/10.14778/3554821.3554847)):

- Can query remote Parquet files via HTTP range requests (only reads needed byte ranges)
- Handles datasets up to ~500 MB comfortably in a modern browser
- Apache Arrow integration enables zero-copy data transfer between DuckDB-WASM and JavaScript visualisation libraries
- Mosaic framework has demonstrated interactive visualisation of 18 million data points using DuckDB-WASM ([MotherDuck case study](https://motherduck.com/case-studies/dominik-moritz/))

### Handling Large Datasets in the Browser

Strategy for progressive data loading:

1. **Overview level**: Vector tiles served from the API (all grid cells, single variable, single time step) -- lightweight, cacheable
2. **Region zoom**: When user zooms to a region, load Parquet data for that bounding box via DuckDB-WASM HTTP range requests
3. **Detail/analysis mode**: When user selects specific cells, load full time series via API and run correlations client-side with DuckDB-WASM
4. **Pre-aggregated layers**: For global views, serve pre-computed aggregations (country-level, continental) rather than raw grid data

### Frontend Stack Summary

```
React                  -- UI framework
Redux                  -- State management (shared with Kepler.gl)
Kepler.gl              -- Map visualisation
DuckDB-WASM            -- Client-side analytical engine
Apache Arrow           -- Zero-copy data interchange
deck.gl                -- Additional custom visualisation layers
Vite                   -- Build tooling
```

HungerMapLIVE (WFP) uses a similar React-based architecture with backend ML models generating "nowcasts" that are served to the frontend for visualisation -- a pattern we should study for our real-time update flow ([HungerMap LIVE](https://hungermap.wfp.org/)).

---

## 8. Minimum Viable Product

### Philosophy

The smallest useful thing we can build is: **a tool that lets a researcher select a region on a map, pick two variables from different domains, and see their time-lagged correlation visualised as a time series chart with a significance indicator.**

### MVP Scope

**Data sources (3):**
| Source | Domain | Variable | Coverage |
|--------|--------|----------|----------|
| ACLED | Conflict | Event count, fatalities | East Africa, 2015-2024 |
| CHIRPS | Climate | Monthly precipitation (mm) | East Africa, 2015-2024 |
| WFP food prices | Food security | Maize price (USD/kg) | East Africa, 2015-2024 |

**Region:** East Africa (Kenya, Ethiopia, Somalia, South Sudan, Uganda, Tanzania) -- chosen because all three data sources have good coverage and there are well-documented causal chains (drought -> food prices -> conflict).

**Time range:** 2015-2024 (10 years, 120 monthly time steps).

**Grid cells:** ~3,600 cells covering East Africa.

**Data volume:** 3 variables x 3,600 cells x 120 months = ~1.3 million rows. Under 10 MB compressed Parquet.

### MVP Features

1. **Data pipeline**: Three adapters (ACLED, CHIRPS, WFP) producing canonical Parquet files
2. **Static map**: Kepler.gl showing East Africa with grid cells coloured by selected variable at selected time step
3. **Time series view**: Click a grid cell, see all three variables plotted over time
4. **Lag correlation**: For a selected cell or region, compute Pearson correlation at lags 0-12 months between any two variables
5. **Basic narrative**: Claude API generates a one-paragraph interpretation of the correlation result

### What the MVP Proves

- The adapter pattern works for heterogeneous data sources
- 0.5 degree grid resolution is useful for cross-domain analysis
- Parquet + DuckDB is fast enough for interactive exploration
- AI-generated interpretation adds value over raw statistics
- The platform is useful to a researcher even with minimal data

### MVP Non-Goals

- No user accounts or authentication
- No automated scheduling (manual adapter runs)
- No global coverage
- No advanced causal methods (Granger, PCMCI)
- No real-time data updates

---

## 9. AI Integration

### Claude API for Interpretation

The most valuable AI integration is **interpreting statistical results in domain context**. A correlation coefficient of 0.73 between rainfall deficit and conflict events with a 3-month lag is a number; Claude can explain what it means, what mechanisms might drive it, and what caveats apply.

### Proposed Integration Points

**1. Correlation Interpretation**

```python
prompt = f"""
You are an analyst examining cross-domain spatiotemporal correlations.

Region: {region_name}
Period: {start_date} to {end_date}
Variable A: {var_a_description}
Variable B: {var_b_description}
Correlation: {correlation_value} at lag {lag_months} months
P-value: {p_value}

Interpret this correlation. Consider:
- Plausible causal mechanisms
- Known research on this relationship
- Possible confounders
- Whether the lag structure makes sense
- Limitations of this analysis

Be specific to the region and time period.
"""
```

**2. Natural Language Queries**

Allow researchers to ask questions in natural language that get translated to SQL queries against the data:

```
User: "What was the relationship between drought and conflict in Somalia in 2022?"

System:
  1. Parse intent -> correlation query
  2. Identify variables -> CHIRPS precipitation, ACLED events
  3. Identify region -> Somalia grid cells
  4. Identify time range -> 2022
  5. Execute query
  6. Generate narrative from results
```

Claude's structured outputs capability (released November 2025) ensures that the query translation step returns valid, parseable query parameters rather than free-form text ([Claude structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)).

**3. Automated Pattern Scanning**

When new data is ingested, automatically scan for significant correlations and generate brief narrative summaries for a "discoveries feed":

```
"In the Turkana region of Kenya (grid cells 18234-18240), maize prices
increased 45% between March and June 2023, following a 3-month period
of below-average rainfall. Conflict events increased by 60% in the
subsequent 2 months. This pattern is consistent with published research
on climate-food-conflict linkages in pastoral regions (Raleigh et al., 2015)."
```

### Cost and Rate Considerations

- Claude API calls for interpretation are relatively inexpensive (a single correlation interpretation is ~500 input tokens + ~300 output tokens)
- Batch scanning of correlations should be done server-side and cached, not triggered per-user-request
- Natural language query translation can use a smaller/faster model for the parsing step, with Claude reserved for narrative generation

---

## 10. Open Questions

These are unresolved decisions that need more research, prototyping, or discussion before they can be settled.

### Data and Schema

| # | Question | Considerations | Resolution Path |
|---|----------|---------------|-----------------|
| Q1 | **How to handle country-level data (World Bank, FAO) on a grid?** | Options: (a) assign country value to all cells in that country, (b) store separately with ISO3 key and join at query time, (c) use population-weighted disaggregation. Option (b) is simplest; (c) is most accurate | Prototype with World Bank GDP data |
| Q2 | **Should we store raw event data (individual ACLED events) alongside aggregated grid data?** | Raw events enable custom aggregations but increase storage and complexity. Could store as separate GeoParquet with point geometries | Decide based on user feedback from MVP |
| Q3 | **What canonical variable naming convention?** | Options: `{source}_{variable}` (e.g., `acled_fatalities`), `{domain}_{variable}` (e.g., `conflict_fatalities`). Former is unambiguous; latter is more user-friendly when multiple sources measure the same thing | Adopt `{source}_{variable}` initially, add aliases later |

### Statistical Methods

| # | Question | Considerations | Resolution Path |
|---|----------|---------------|-----------------|
| Q4 | **Which causal inference method to implement first?** | Granger causality is simplest and most widely understood, but assumes linearity. PCMCI (Runge 2020) handles autocorrelation and multiple testing better. Transfer entropy is nonparametric but computationally expensive | Start with Granger for MVP, add PCMCI in v2 |
| Q5 | **How to handle the multiple testing problem?** | With 100 variables and 12 lags, there are ~60,000 potential correlations per grid cell. Need FDR correction (Benjamini-Hochberg) or similar | Research existing approaches in VIEWS and PCMCI literature |
| Q6 | **Spatial autocorrelation -- ignore, model, or exploit?** | Adjacent grid cells are not independent. Moran's I can detect spatial autocorrelation; spatial lag models can account for it | Needs deep dive in research/04-statistical-methods.md |

### Infrastructure

| # | Question | Considerations | Resolution Path |
|---|----------|---------------|-----------------|
| Q7 | **Single-machine vs distributed?** | MVP data volumes are tiny (< 1 GB). Even full global data (~100 GB) is manageable on one machine with DuckDB. Distributed only needed if we add high-frequency data (e.g., daily GDELT) | Single machine for foreseeable future |
| Q8 | **How to distribute the dataset?** | Options: Git LFS, Zenodo, S3 public bucket, DVC (Data Version Control). DVC integrates with Git and supports remote storage | Evaluate DVC for data versioning |
| Q9 | **CI/CD for data quality?** | Automated tests that run when new data is ingested: row counts, value ranges, null percentages, temporal completeness | Design data quality test framework |

### Frontend and UX

| # | Question | Considerations | Resolution Path |
|---|----------|---------------|-----------------|
| Q10 | **How much analysis should happen client-side vs server-side?** | DuckDB-WASM can handle simple correlations on a few thousand rows. Complex analyses (PCMCI, bootstrap significance) need server-side compute | Profile DuckDB-WASM performance with MVP data |
| Q11 | **How to present causal uncertainty to non-technical users?** | "Correlation does not imply causation" is essential but insufficient. Need visual language for strength of evidence, direction of effect, lag structure | Study how VIEWS and HungerMapLIVE present uncertainty |
| Q12 | **Mobile support?** | Kepler.gl is WebGL-heavy and may not perform well on mobile. Consider a simplified mobile view | Defer to post-MVP |

### Legal and Ethical

| # | Question | Considerations | Resolution Path |
|---|----------|---------------|-----------------|
| Q13 | **Data licence compatibility?** | ACLED has specific terms of use. Some World Bank data is CC-BY. Need to track and display attribution per source | Build licence metadata into the variable catalogue |
| Q14 | **Responsible disclosure of predictive patterns?** | If the system identifies a strong conflict predictor, how do we handle that responsibly? VIEWS has navigated this carefully | Study VIEWS ethical framework and consult with domain experts |

---

## References

- [PRIO-GRID](https://grid.prio.org/) -- Spatial grid framework, v3 with Parquet support
- [PRIO-GRID GitHub (prio-data/priogrid)](https://github.com/prio-data/priogrid) -- R package and replication scripts for PRIO-GRID v3.0
- [VIEWS Forecasting](https://viewsforecasting.org/) -- Conflict prediction system architecture
- [VIEWS Pipeline Core (GitHub)](https://github.com/views-platform/views-pipeline-core) -- ML pipeline for conflict forecasting
- [VIEWS Platform (GitHub)](https://github.com/views-platform) -- Full platform repository collection
- [HungerMap LIVE](https://hungermap.wfp.org/) -- WFP real-time food security monitoring
- [HungerMap LIVE Innovation Page](https://innovation.wfp.org/project/hungermap-live) -- Technical overview of WFP's monitoring platform
- [DuckDB Parquet Tips](https://duckdb.org/docs/stable/data/parquet/tips) -- Performance optimisation for Parquet queries
- [DuckDB Architecture Deep Dive](https://endjin.com/blog/2025/04/duckdb-in-depth-how-it-works-what-makes-it-fast) -- How DuckDB works internally
- [DuckDB-WASM Paper](https://dl.acm.org/doi/abs/10.14778/3554821.3554847) -- Academic paper on browser-based analytics
- [DuckDB-WASM Large Dataset Visualisation](https://motherduck.com/case-studies/dominik-moritz/) -- Mosaic: 18M rows in browser
- [GeoParquet Specification](https://geoparquet.org/) -- OGC standard for geospatial Parquet
- [DuckDB GeoParquet Tutorials](https://github.com/cholmes/duckdb-geoparquet-tutorials) -- Practical examples
- [Kepler.gl Documentation](https://docs.kepler.gl/) -- React geospatial visualisation library
- [Kepler.gl GitHub](https://github.com/keplergl/kepler.gl) -- Source code and examples
- [FastAPI + PostGIS Integration](https://medium.com/@nunocarvalhodossantos/fastapi-postgis-and-geoalchemy-2-powerful-and-location-aware-web-applications-3b23f44c8fa5) -- Geospatial API patterns
- [Claude Structured Outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs) -- Schema-guaranteed API responses
- [Building Analytics Stack with Python, Parquet, DuckDB](https://www.kdnuggets.com/building-your-modern-data-analytics-stack-with-python-parquet-and-duckdb) -- Modern data stack guide
- [Data Pipeline Design Patterns in Python](https://www.startdataengineering.com/post/code-patterns/) -- Adapter and pipeline patterns
