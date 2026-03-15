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
11. [System Architecture Diagram](#11-system-architecture-diagram)
12. [Data Pipeline Orchestration](#12-data-pipeline-orchestration)
13. [Event-Driven Architecture](#13-event-driven-architecture)
14. [Caching Strategy](#14-caching-strategy)
15. [Authentication and Authorisation](#15-authentication-and-authorisation)
16. [API Versioning Strategy](#16-api-versioning-strategy)
17. [Testing Strategy](#17-testing-strategy)
18. [CI/CD Pipeline](#18-cicd-pipeline)
19. [Documentation Strategy](#19-documentation-strategy)
20. [Observability](#20-observability)
21. [Security Considerations](#21-security-considerations)
22. [Scaling Roadmap](#22-scaling-roadmap)
23. [Plugin/Extension Architecture](#23-pluginextension-architecture)
24. [Claude API Integration Design](#24-claude-api-integration-design)
25. [Novel Architecture Ideas](#25-novel-architecture-ideas)

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

## 11. System Architecture Diagram

> **Checked:** March 2025

### 11.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL DATA SOURCES                            │
│  ┌──────┐ ┌──────┐ ┌───────┐ ┌──────┐ ┌───────┐ ┌──────┐ ┌────────┐  │
│  │ACLED │ │CHIRPS│ │  WFP  │ │ USGS │ │MODIS/ │ │OpenAQ│ │World   │  │
│  │API   │ │HTTP  │ │HDX API│ │API   │ │VIIRS  │ │API   │ │Bank API│  │
│  └──┬───┘ └──┬───┘ └───┬───┘ └──┬───┘ └───┬───┘ └──┬───┘ └───┬────┘  │
│     │        │         │        │         │        │         │         │
└─────┼────────┼─────────┼────────┼─────────┼────────┼─────────┼────────┘
      │        │         │        │         │        │         │
      ▼        ▼         ▼        ▼         ▼        ▼         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          INGESTION LAYER                                │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Adapter Registry                                                │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │   │
│  │  │ ACLED   │ │ CHIRPS  │ │  WFP    │ │  USGS   │ │ OpenAQ  │  │   │
│  │  │Adapter  │ │Adapter  │ │Adapter  │ │Adapter  │ │Adapter  │  │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                           │                                             │
│                           ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Common Pipeline: fetch → parse → validate → transform → write   │   │
│  │  - Rate limiting (tenacity)                                      │   │
│  │  - Quality scoring (5-dimension taxonomy)                        │   │
│  │  - Spatial aggregation (exactextract / point-to-grid)            │   │
│  │  - Temporal alignment (monthly canonical)                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                           │                                             │
└───────────────────────────┼─────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          STORAGE LAYER                                  │
│                                                                         │
│  ┌───────────────────────────────────┐  ┌────────────────────────────┐  │
│  │  Partitioned Parquet Files        │  │  PRIO-GRID GeoParquet      │  │
│  │  data/                            │  │  (cell geometries, static  │  │
│  │    domain=conflict/year=2023/     │  │   variables, lookup tables)│  │
│  │    domain=climate/year=2023/      │  └────────────────────────────┘  │
│  │    domain=food_security/year=2023/│                                  │
│  └───────────────┬───────────────────┘  ┌────────────────────────────┐  │
│                  │                      │  PMTiles (vector tiles     │  │
│                  │                      │  for map rendering)        │  │
│                  │                      └────────────────────────────┘  │
│                  │                                                      │
│                  │  ┌────────────────────────────────────────────────┐  │
│                  └──│  DuckDB (analytical engine)                    │  │
│                     │  - Reads Parquet directly (no import)          │  │
│                     │  - Spatial extension for ST_* functions        │  │
│                     │  - Materialised views for hot queries          │  │
│                     └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          API LAYER                                      │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  FastAPI Application                                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │   │
│  │  │/grid     │ │/variables│ │/correlate│ │/interpret (Claude)│   │   │
│  │  │/tiles    │ │/causal   │ │/export   │ │/query (NL → SQL) │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │   │
│  │  - DuckDB connection pool                                       │   │
│  │  - Response caching (Redis or in-memory)                        │   │
│  │  - API key auth + rate limiting                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND LAYER                                 │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  React Application (Vite build)                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │   │
│  │  │ Kepler.gl    │  │ Time Series  │  │ Causal Graph Panel  │   │   │
│  │  │ Map Panel    │  │ Panel        │  │ (D3.js)             │   │   │
│  │  │ (deck.gl +   │  │ (Recharts)   │  │                     │   │   │
│  │  │  MapLibre)   │  │              │  │                     │   │   │
│  │  └──────────────┘  └──────────────┘  └─────────────────────┘   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │   │
│  │  │ DuckDB-WASM  │  │ Data Table   │  │ AI Interpretation   │   │   │
│  │  │ (client-side │  │ (TanStack)   │  │ Panel (Claude)      │   │   │
│  │  │  queries)    │  │              │  │                     │   │   │
│  │  └──────────────┘  └──────────────┘  └─────────────────────┘   │   │
│  │                                                                  │   │
│  │  State: Zustand store (selectedCell, timeRange, variables)       │   │
│  │  Data flow: DuckDB-WASM → Arrow → deck.gl (zero-copy)           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 11.2 Data Flow Summary

```
Raw data (API/HTTP/FTP)
  → Adapter (Python)
    → Canonical Parquet (long format, quality-scored)
      → DuckDB (server-side queries for API)
      → DuckDB-WASM (client-side queries for exploration)
      → PMTiles (pre-rendered map tiles for overview)
        → deck.gl/Kepler.gl (WebGL rendering)
          → User (browser)
```

---

## 12. Data Pipeline Orchestration

> **Checked:** March 2025

### 12.1 Options Comparison

| Tool | Architecture | Strengths | Weaknesses | Cost |
|------|-------------|-----------|------------|------|
| **Cron** | Time-based scheduler | Zero complexity, universal | No dependency tracking, no retry, no monitoring | Free |
| **Prefect** | Python-native, API-driven | Beautiful UI, dynamic flows, hybrid execution, simple setup | Cloud pricing for teams, smaller community than Airflow | Free (OSS), $300+/mo (Cloud) |
| **Dagster** | Asset-centric, declarative | Data lineage, asset materialisation, quality checks, partitions | Steeper learning curve, opinionated | Free (OSS), $100+/mo (Cloud) |
| **Airflow** | DAG-based, mature | Massive ecosystem (2000+ operators), proven at scale, many integrations | Complex setup (scheduler, webserver, workers, metadata DB), DAGs are code-heavy | Free (OSS), $300+/mo (MWAA) |

### 12.2 Recommendation: Phased Approach

**Phase 1 (MVP): Cron + Python scripts**

Keep it simple. Each adapter is a Python script callable from the command line. Cron schedules execution. A simple SQLite or JSON file tracks run status.

```bash
# crontab
0 2 * * 1   cd /opt/causal-atlas && python -m adapters.acled --mode incremental >> /var/log/ca/acled.log 2>&1
0 3 1 * *   cd /opt/causal-atlas && python -m adapters.chirps --month previous >> /var/log/ca/chirps.log 2>&1
```

**Phase 2 (5+ adapters): Dagster**

Dagster is the right choice when we outgrow cron. Rationale:

- **Asset-centric model** aligns with our data architecture. Each Parquet partition is a Dagster asset. Dagster tracks when each asset was last materialised, what it depends on, and whether it needs refreshing.
- **Partitions** support maps directly to our year/month/domain partitioning scheme.
- **Asset checks** (data quality assertions) are built-in -- we can define expectations on row counts, value ranges, and null percentages.
- **Sensors** can watch for file changes (new ACLED data uploaded) and trigger re-materialisation.
- **UI** provides a visual asset graph and run history without writing custom monitoring code.
- **Single-process mode** works without a scheduler daemon -- good for a single-developer deployment.

```python
# Dagster asset definition example
from dagster import asset, AssetIn, MonthlyPartitionsDefinition

monthly_partitions = MonthlyPartitionsDefinition(start_date="2015-01-01")

@asset(
    partitions_def=monthly_partitions,
    group_name="conflict",
    description="ACLED conflict events aggregated to PRIO-GRID cells"
)
def acled_grid_monthly(context):
    partition_key = context.partition_key  # "2023-06-01"
    year, month = int(partition_key[:4]), int(partition_key[5:7])

    adapter = ACLEDAdapter(config, output_dir)
    result = adapter.run(start_date=date(year, month, 1),
                         end_date=date(year, month, 28))

    context.log.info(f"Wrote {result} for {year}-{month:02d}")
    return result

@asset(
    ins={"acled": AssetIn("acled_grid_monthly"),
         "chirps": AssetIn("chirps_grid_monthly")},
    partitions_def=monthly_partitions,
    group_name="integrated"
)
def integrated_monthly(context, acled, chirps):
    """Join conflict and climate data for analysis."""
    ...
```

**Phase 3 (10+ adapters, team): Dagster Cloud or self-hosted Dagster with workers**

### 12.3 Why NOT Airflow

Airflow is the industry standard but is over-engineered for Causal Atlas at every foreseeable scale:
- Requires PostgreSQL metadata database + scheduler process + webserver process + worker processes
- DAG-based (task-centric), not asset-centric -- does not naturally model "this Parquet file depends on that API"
- Airflow 3.0 (April 2025) added Data Assets, narrowing the gap with Dagster, but the implementation is less mature
- We are a single developer, not a data engineering team

Source: [Dagster vs Prefect vs Airflow (ZenML)](https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow), [FreeAgent Orchestration Comparison](https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/), [Dagster Asset Guide](https://docs.dagster.io/concepts/assets/software-defined-assets)

---

## 13. Event-Driven Architecture

> **Checked:** March 2025

### 13.1 Triggers for Analysis

When new data arrives (a new ACLED weekly release, a new CHIRPS monthly raster), we want to automatically:
1. Ingest and integrate the new data
2. Re-run correlation analysis for affected grid cells and time periods
3. Generate narrative summaries for significant new findings
4. Update the "discoveries feed" on the frontend

### 13.2 Implementation for Causal Atlas

**Simple approach (MVP): File-based triggers**

```python
import watchdog  # Or use Dagster sensors

# Watch the raw data directory for new files
# When a new file appears, determine which adapter produced it
# Trigger downstream processing

class NewDataHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.parquet'):
            domain = extract_domain(event.src_path)
            year, month = extract_period(event.src_path)
            # Trigger integration for affected period
            integrate(domain, year, month)
            # Trigger correlation scan
            scan_correlations(year, month)
```

**Dagster approach (Phase 2): Sensors**

```python
from dagster import sensor, RunRequest

@sensor(target=integrated_monthly)
def new_acled_data_sensor(context):
    """Watch for new ACLED data and trigger integration."""
    last_run = context.cursor or "2024-01-01"
    new_files = find_new_parquet_files('data/domain=conflict/', since=last_run)

    if new_files:
        for f in new_files:
            year, month = extract_period(f)
            yield RunRequest(
                run_key=f"integrate_{year}_{month:02d}",
                partition_key=f"{year}-{month:02d}-01"
            )
        context.update_cursor(str(datetime.now()))
```

**Cloud approach (Phase 3): S3 event notifications**

```
S3 bucket (new Parquet file uploaded)
  → S3 Event Notification
    → SQS queue
      → Lambda function (lightweight)
        → Dagster API (trigger run)
```

### 13.3 Event Flow for Automated Discovery

```
New ACLED data arrives
  → ACLED adapter runs (fetch + aggregate + quality score)
    → New Parquet partition written
      → Integration step joins with existing climate/food data
        → Correlation scanner runs for updated cells/months
          → Claude API interprets significant new correlations
            → New findings posted to discoveries feed
              → Email/webhook notification to subscribed researchers
```

Source: [Prefect Event Triggers vs Sensors](https://www.prefect.io/blog/push-and-pull-architecture-event-triggers-vs-sensors-in-data-pipelines), [Dagster Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors)

---

## 14. Caching Strategy

> **Checked:** March 2025

### 14.1 What to Cache

| Cache Target | Why | Invalidation |
|-------------|-----|-------------|
| **API responses** (correlation results) | Expensive computation; same query by different users | When underlying data changes (new month ingested) |
| **AI interpretations** | Claude API costs money; same correlation = same interpretation | When correlation result changes |
| **DuckDB materialised views** | Avoid re-scanning Parquet for hot queries | On data ingestion |
| **PMTiles** (vector tiles) | Static between data updates | On data ingestion (rebuild tiles) |
| **Frontend assets** | Standard web caching | On deployment |
| **Parquet metadata** | DuckDB caches row group stats internally | Automatic (DuckDB handles this) |

### 14.2 Implementation

**MVP: DuckDB materialised views + in-memory Python cache**

```python
# Server-side: DuckDB materialised views for common queries
con = duckdb.connect('causal_atlas.duckdb')

con.execute("""
    CREATE OR REPLACE VIEW latest_month AS
    SELECT * FROM read_parquet('data/domain=*/year=*/**.parquet',
                               hive_partitioning=true)
    WHERE year = (SELECT MAX(year) FROM ...)
      AND month = (SELECT MAX(month) FROM ...);
""")

# Application-level: functools.lru_cache for API responses
from functools import lru_cache

@lru_cache(maxsize=1024)
def get_correlation(var_a: str, var_b: str, region: str, lag: int) -> dict:
    """Compute and cache correlation result."""
    ...
```

**Phase 2: Redis cache for multi-worker deployments**

```python
import redis
import json

r = redis.Redis()

def get_or_compute_correlation(key: str, compute_fn):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    result = compute_fn()
    r.setex(key, 3600, json.dumps(result))  # Cache for 1 hour
    return result
```

### 14.3 Cache Invalidation Strategy

```
On data ingestion (new month of data):
  1. Clear all correlation caches for affected variables/periods
  2. Rebuild DuckDB materialised views
  3. Rebuild PMTiles for affected variables
  4. Clear AI interpretation cache for affected correlations

On deployment (code change):
  1. Clear all caches (conservative)
  2. Frontend CDN purge
```

---

## 15. Authentication and Authorisation

> **Checked:** March 2025

### 15.1 Tiered Access Model

| Tier | Access | Auth Required | Rate Limit |
|------|--------|--------------|------------|
| **Public** | Pre-computed maps, global aggregations, published findings | None | 100 req/min |
| **Researcher** | Grid-level time series, correlation API, AI interpretation | API key | 1000 req/min |
| **Contributor** | Data upload, annotation, hypothesis marking | OAuth2 (GitHub/ORCID) | 5000 req/min |
| **Admin** | Pipeline management, user management, system config | OAuth2 + RBAC | Unlimited |

### 15.2 Implementation

**API key authentication (MVP):**

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key is None:
        return "public"  # Public tier
    if api_key in VALID_API_KEYS:
        return VALID_API_KEYS[api_key]  # Returns tier
    raise HTTPException(status_code=403, detail="Invalid API key")

@app.get("/api/v1/grid/{gid}/timeseries")
async def get_timeseries(gid: int, tier: str = Depends(verify_api_key)):
    if tier == "public":
        raise HTTPException(403, "API key required for grid-level data")
    ...
```

**OAuth2 (Phase 2):** Use GitHub OAuth for researcher login. ORCID OAuth for academic identity verification. Store user profiles in PostgreSQL (or SQLite for MVP).

### 15.3 Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.get("/api/v1/correlations")
@limiter.limit("100/minute")  # Per IP
async def get_correlations(request: Request, ...):
    ...
```

---

## 16. API Versioning Strategy

> **Checked:** March 2025

### 16.1 Approach: URL Path Versioning

```
/api/v1/grid/{gid}/timeseries     -- Current stable version
/api/v2/grid/{gid}/timeseries     -- Next version (when breaking changes needed)
```

**Why URL path (not header or query param):**
- Most explicit and discoverable
- Easy to document and test
- Standard in the geospatial API ecosystem (OGC APIs use path versioning)
- Clear in server logs and CDN configuration

### 16.2 Versioning Policy

- **v1** is the initial release. It remains supported for 12 months after v2 is released.
- Breaking changes (field renames, removed endpoints, changed response schemas) require a new major version.
- Non-breaking additions (new optional fields, new endpoints) are added to the current version.
- Deprecation warnings are returned as HTTP headers: `Deprecation: true`, `Sunset: 2026-12-31`

### 16.3 API Documentation

Every version has its own OpenAPI schema, auto-generated by FastAPI:

```
/api/v1/docs     -- Swagger UI for v1
/api/v1/openapi.json  -- OpenAPI spec for v1
```

---

## 17. Testing Strategy

> **Checked:** March 2025

### 17.1 Testing Pyramid

```
                    ┌──────────────┐
                    │  End-to-End  │  Playwright: full browser flow
                    │  (few)       │  "User selects cell, sees correlation"
                    ├──────────────┤
                    │ Integration  │  pytest: adapter -> Parquet -> DuckDB
                    │ (moderate)   │  "ACLED adapter produces valid Parquet"
                    ├──────────────┤
                    │  Data Quality│  Great Expectations: value ranges,
                    │  (per-ingest)│  null checks, temporal completeness
                    ├──────────────┤
                    │  Unit Tests  │  pytest: pure functions
                    │  (many)      │  "latlon_to_gid returns correct ID"
                    └──────────────┘
```

### 17.2 Unit Tests

```python
# tests/test_spatial.py
import pytest
from causal_atlas.spatial import latlon_to_gid, gid_to_latlon

def test_latlon_to_gid_equator():
    assert latlon_to_gid(0.25, 0.25) == 180 * 720 + 360 + 1

def test_gid_roundtrip():
    for gid in [1, 100, 129600, 259200]:
        lat, lon = gid_to_latlon(gid)
        assert latlon_to_gid(lat, lon) == gid

def test_quality_score():
    from causal_atlas.quality import compute_quality_score
    score = compute_quality_score(1.0, 1.0, 1.0, 1.0, 1.0)
    assert score == 1.0

    score = compute_quality_score(0.5, 0.5, 0.5, 0.5, 0.5)
    assert score == 0.5
```

### 17.3 Adapter Integration Tests

```python
# tests/test_acled_adapter.py
import pytest

@pytest.fixture
def acled_adapter():
    config = AdapterConfig(source_id="acled_test", domain="conflict", api_key="test")
    return ACLEDAdapter(config, output_dir=Path("/tmp/test"))

def test_acled_fetch_returns_data(acled_adapter):
    raw = acled_adapter.fetch(date(2023, 1, 1), date(2023, 1, 31))
    assert raw is not None
    assert len(raw) > 0

def test_acled_parse_produces_valid_table(acled_adapter):
    raw = acled_adapter.fetch(date(2023, 1, 1), date(2023, 1, 31))
    table = acled_adapter.parse(raw)
    assert 'latitude' in table.column_names
    assert 'event_date' in table.column_names
    assert table.num_rows > 0

def test_acled_full_pipeline_produces_valid_parquet(acled_adapter):
    path = acled_adapter.run(date(2023, 1, 1), date(2023, 1, 31))
    assert path.exists()
    assert path.suffix == '.parquet'
    # Verify with DuckDB
    import duckdb
    result = duckdb.query(f"SELECT COUNT(*) FROM read_parquet('{path}')").fetchone()
    assert result[0] > 0
```

### 17.4 Data Quality Tests (Great Expectations)

```python
# tests/test_data_quality.py
import great_expectations as gx

def test_acled_parquet_quality():
    context = gx.get_context()
    ds = context.sources.add_pandas("acled_test")
    asset = ds.add_parquet_asset("acled", filepath="data/domain=conflict/year=2023/acled.parquet")
    batch = asset.get_batch()

    # Define expectations
    batch.expect_column_to_exist("gid")
    batch.expect_column_to_exist("value")
    batch.expect_column_values_to_be_between("gid", min_value=1, max_value=259200)
    batch.expect_column_values_to_not_be_null("gid")
    batch.expect_column_values_to_not_be_null("year")
    batch.expect_column_values_to_be_between("month", min_value=1, max_value=12)
    batch.expect_column_values_to_be_between("value", min_value=0, max_value=100000)
    batch.expect_column_values_to_be_in_set(
        "source", ["acled_v24", "acled_v25"]
    )
    batch.expect_column_values_to_be_between(
        "quality_composite", min_value=0.0, max_value=1.0
    )

    results = batch.validate()
    assert results.success, f"Data quality check failed: {results}"
```

Source: [Great Expectations + GitHub Actions](https://greatexpectations.io/blog/github-actions/), [pytest + Great Expectations Pipeline Testing](https://github.com/greatexpectationslabs/put-data-pipeline-under-test-with-pytest-and-great-expectations), [pytest + GitHub Actions Tutorial](https://pytest-with-eric.com/integrations/pytest-github-actions/)

---

## 18. CI/CD Pipeline

> **Checked:** March 2025

### 18.1 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install ruff mypy
      - run: ruff check src/
      - run: mypy src/ --ignore-missing-imports

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
        with: { file: coverage.xml }

  data-quality:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -e ".[dev]"
      # Download sample data for testing
      - run: python scripts/download_test_data.py
      - run: pytest tests/test_data_quality.py -v

  build-frontend:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci && npm run build
      - run: cd frontend && npm run test
```

### 18.2 Deployment Pipeline

```
main branch push
  → CI (lint + test + data quality)
    → Build Docker image (Python API + frontend static files)
      → Push to GitHub Container Registry
        → Deploy to staging (auto)
          → Manual approval
            → Deploy to production
```

### 18.3 Data Pipeline CI

When adapter code changes, run the adapter against a small test dataset (not the full API):

```yaml
  test-adapters:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[dev]"
      # Use cached/mock API responses for deterministic testing
      - run: pytest tests/adapters/ -v --vcr-record=none
```

Use `vcrpy` or `responses` library to record and replay API responses, ensuring adapter tests are fast and deterministic.

---

## 19. Documentation Strategy

> **Checked:** March 2025

### 19.1 Tool Selection: MkDocs + Material Theme

**Decision: MkDocs with Material for MkDocs**

Rationale:
- Python-native -- aligns with our tech stack
- Material theme provides excellent search, navigation, dark mode out of the box
- Supports autodoc from Python docstrings (via mkdocstrings plugin)
- Simple Markdown authoring (same as our research docs)
- Used by major Python projects (FastAPI, Pydantic, Polars)
- Easy to deploy to GitHub Pages

**Why not Docusaurus:**
- JavaScript/React-based -- unnecessary complexity for a Python project
- Heavier build process
- Better suited for large multi-language documentation sites

### 19.2 Documentation Structure

```
docs/
├── index.md                   # Project overview, getting started
├── getting-started/
│   ├── installation.md        # pip install, Docker, development setup
│   ├── quickstart.md          # "Your first query in 5 minutes"
│   └── configuration.md       # Environment variables, config files
├── user-guide/
│   ├── data-sources.md        # Available datasets and variables
│   ├── api-reference.md       # REST API endpoints (auto-generated from OpenAPI)
│   ├── map-interface.md       # Using the web interface
│   ├── sql-queries.md         # Common DuckDB queries for analysis
│   └── interpreting-results.md # How to read correlation and causal results
├── developer-guide/
│   ├── architecture.md        # System architecture (this document, refined)
│   ├── adding-adapters.md     # How to write a new data source adapter
│   ├── adding-analysis.md     # How to add a new statistical method
│   ├── contributing.md        # Contribution guidelines, code standards
│   └── api-design.md          # API design decisions and patterns
├── research/                  # Our existing research/ folder, published as docs
│   ├── ...
└── changelog.md               # Release notes
```

### 19.3 API Documentation

FastAPI auto-generates OpenAPI specs. We embed these in MkDocs using the `mkdocs-swagger-ui` plugin or link to the hosted `/api/v1/docs` Swagger UI.

Source: [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), [MkDocs vs Docusaurus (Damavis)](https://blog.damavis.com/en/mkdocs-vs-docusaurus-for-technical-documentation/), [Documentation Generator Comparison 2025](https://okidoki.dev/documentation-generator-comparison)

---

## 20. Observability

> **Checked:** March 2025

### 20.1 The Three Pillars

| Pillar | What | Tool | Purpose |
|--------|------|------|---------|
| **Logs** | Structured event records | `structlog` (Python) | Debug adapter failures, audit data changes |
| **Metrics** | Numeric measurements over time | Prometheus (via `prometheus-client`) | Monitor ingestion rates, API latency, error rates |
| **Traces** | Request flow across components | OpenTelemetry | Track a correlation request from API to DuckDB to Claude to response |

### 20.2 Structured Logging

```python
import structlog

logger = structlog.get_logger()

# All log entries are structured JSON
logger.info("adapter_run_started",
    source="acled",
    mode="incremental",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

logger.info("adapter_run_completed",
    source="acled",
    rows_ingested=15234,
    duration_seconds=45.2,
    quality_mean=0.87,
    errors=0
)

logger.error("adapter_fetch_failed",
    source="acled",
    status_code=429,
    retry_attempt=3,
    error="Rate limited"
)
```

### 20.3 Key Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `ca_ingestion_rows_total` | Counter | source, variable | Total rows ingested |
| `ca_ingestion_duration_seconds` | Histogram | source | Time per ingestion run |
| `ca_ingestion_errors_total` | Counter | source, error_type | Ingestion failures |
| `ca_api_request_duration_seconds` | Histogram | endpoint, method | API latency |
| `ca_api_requests_total` | Counter | endpoint, status_code | API request count |
| `ca_correlation_computation_seconds` | Histogram | method | Time to compute correlations |
| `ca_claude_api_tokens_total` | Counter | model, direction | Token usage |
| `ca_claude_api_cost_usd` | Counter | model | Estimated API cost |
| `ca_duckdb_query_seconds` | Histogram | query_type | DuckDB query latency |
| `ca_data_quality_score` | Gauge | source, variable | Average quality score per source |

### 20.4 OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

# Setup (once at application start)
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("causal-atlas")

# Usage in API endpoint
@app.get("/api/v1/correlations")
async def get_correlations(var_a: str, var_b: str, lag: int):
    with tracer.start_as_current_span("compute_correlation") as span:
        span.set_attribute("var_a", var_a)
        span.set_attribute("var_b", var_b)
        span.set_attribute("lag", lag)

        with tracer.start_as_current_span("duckdb_query"):
            data = query_duckdb(var_a, var_b, lag)

        with tracer.start_as_current_span("compute_stats"):
            result = compute_correlation(data)

        with tracer.start_as_current_span("claude_interpret"):
            interpretation = await interpret_with_claude(result)

        return {**result, "interpretation": interpretation}
```

### 20.5 MVP Approach

For MVP, structured logging is sufficient. Add Prometheus metrics when we have a web service. Add OpenTelemetry tracing when debugging cross-component issues becomes a pain point.

Source: [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/), [OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/), [structlog Documentation](https://www.structlog.org/)

---

## 21. Security Considerations

> **Checked:** March 2025

### 21.1 Threat Model

| Threat | Risk | Mitigation |
|--------|------|------------|
| **API key exposure** in client-side code | API keys for ACLED, Claude, etc. leaked in browser | Server-side proxy for all external API calls; never embed keys in frontend |
| **Sensitive conflict data** misuse | Location data could identify individuals in conflict zones | Aggregate to 0.5-degree grid (anonymising); no individual event data in public API |
| **Claude API abuse** (prompt injection) | User manipulates AI interpretation to produce harmful content | Input validation; output filtering; rate limiting per user |
| **Data integrity** | Corrupted/malicious data ingested | Checksums on downloaded files; schema validation; value range checks |
| **DDoS on API** | Service unavailability | Rate limiting (slowapi); CDN for static assets; DuckDB is read-only (no injection) |
| **SQL injection** | Not applicable -- DuckDB queries are parameterised | Use parameterised queries; DuckDB-WASM is sandboxed in browser |

### 21.2 API Key Management

```python
# Use environment variables, never hardcode
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    acled_api_key: str
    claude_api_key: str
    maplibre_style_url: str
    database_path: str = "data/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# .env is in .gitignore -- never committed
# In CI/CD, use GitHub Secrets
# In production, use environment variables or secrets manager (AWS SSM, Vault)
```

### 21.3 HTTPS

- All API endpoints served over HTTPS (Let's Encrypt / Caddy auto-TLS)
- HSTS headers enforce HTTPS
- Secure cookies (if used) with `HttpOnly`, `Secure`, `SameSite` flags

### 21.4 Data Sensitivity

ACLED data includes geocoded conflict events. While we aggregate to 0.5-degree grid cells, we should:
- Not expose individual event coordinates through the public API
- Store raw event data in a separate, access-controlled partition
- Display only aggregate counts and derived statistics
- Follow ACLED's terms of use regarding redistribution
- Consider VIEWS' ethical framework for responsible handling of conflict prediction data

---

## 22. Scaling Roadmap

> **Checked:** March 2025

### 22.1 Stage 1: Single Developer Laptop

```
Hardware: MacBook / Linux laptop, 16-32GB RAM, 500GB SSD
Data volume: < 1 GB (MVP: East Africa, 3 sources, 10 years)
Users: 1 (developer)
Stack: Python scripts, DuckDB, local Parquet files, Jupyter notebooks

Scaling constraints: None. Everything runs locally in seconds.
```

### 22.2 Stage 2: Development Server

```
Hardware: VPS (4-8 cores, 32GB RAM, 500GB NVMe) or old desktop
Data volume: 10-50 GB (regional, 10+ sources, 30 years)
Users: 1-5 (research team)
Stack: FastAPI server, DuckDB, Parquet on local NVMe
       Frontend served by Caddy (reverse proxy + auto-TLS)
       Cron or Dagster for pipeline scheduling
       SQLite for API keys and user metadata

Estimated cost: $30-80/month (Hetzner, DigitalOcean, OVH)
```

### 22.3 Stage 3: Small Cloud Deployment

```
Hardware: Cloud VM or managed container (AWS ECS, Fly.io, Railway)
Data volume: 50-200 GB (global, 20+ sources, 30 years)
Users: 10-100 (researchers, analysts)
Stack: FastAPI in Docker container
       DuckDB reading from S3 (remote Parquet via httpfs extension)
       PMTiles on Cloudflare R2 (map tiles)
       Redis for API caching
       GitHub Actions for CI/CD
       Dagster Cloud for pipeline orchestration

Estimated cost: $100-300/month
```

### 22.4 Stage 4: Production Scale

```
Hardware: Managed cloud (AWS ECS/Fargate, GCP Cloud Run)
Data volume: 200GB+ (global, 50+ sources, sub-grid resolution)
Users: 100-1000+ (public research tool)
Stack: FastAPI behind ALB/CloudFront
       DuckDB + MotherDuck (managed DuckDB for shared access)
       PostGIS for concurrent writes and complex spatial operations
       Redis cluster for caching
       Dagster Cloud for orchestration
       Cloudflare R2 + CDN for tiles and static assets
       OpenTelemetry -> Grafana Cloud for observability

Estimated cost: $500-2000/month
```

### 22.5 Decision Points

| Trigger | Action |
|---------|--------|
| First user beyond developer | Deploy Stage 2 |
| > 5 concurrent users on API | Add Redis caching |
| > 50 GB data | Move data to S3, use DuckDB httpfs |
| Need concurrent writes | Add PostGIS alongside DuckDB |
| > 100 users | Add CDN, consider managed DuckDB (MotherDuck) |
| Need SLA/uptime guarantee | Move to managed cloud (Stage 4) |

---

## 23. Plugin/Extension Architecture

> **Checked:** March 2025

### 23.1 Design Goals

Third parties (researchers, institutions) should be able to:
1. Add new data source adapters without modifying core code
2. Add new statistical analysis methods
3. Add new visualisation components
4. Share these extensions as installable packages

### 23.2 Extension Points

**Data Source Adapters** (most common extension):

```python
# Third-party package: causal-atlas-era5
# pip install causal-atlas-era5

from causal_atlas.adapters import BaseAdapter, register_adapter

@register_adapter("era5")
class ERA5Adapter(BaseAdapter):
    """Ingest ERA5 climate reanalysis data from Copernicus CDS."""

    def fetch(self, start_date, end_date):
        import cdsapi
        client = cdsapi.Client()
        # ... fetch ERA5 data
        return raw_data

    def parse(self, raw_data):
        # ... parse NetCDF to Arrow table
        ...

    def validate(self, table):
        # ... validate temperature ranges, check for nulls
        ...

    def transform(self, table):
        # ... aggregate to PRIO-GRID, convert to canonical schema
        ...
```

**Statistical Methods:**

```python
# Third-party: causal-atlas-pcmci
from causal_atlas.methods import BaseMethod, register_method

@register_method("pcmci")
class PCMCIMethod(BaseMethod):
    """PCMCI causal discovery method (Runge 2020)."""

    def compute(self, data, target_var, predictor_vars, max_lag=12):
        from tigramite import data_processing as pp
        from tigramite.pcmci import PCMCI
        from tigramite.independence_tests import ParCorr

        # ... run PCMCI analysis
        return CausalResult(links=links, p_values=p_values, lags=lags)
```

### 23.3 Discovery Mechanism

Adapters and methods register themselves via entry points (Python packaging standard):

```toml
# pyproject.toml of causal-atlas-era5 package
[project.entry-points."causal_atlas.adapters"]
era5 = "causal_atlas_era5:ERA5Adapter"
```

```python
# Core discovery code
from importlib.metadata import entry_points

def discover_adapters():
    """Find all installed adapter plugins."""
    eps = entry_points(group="causal_atlas.adapters")
    for ep in eps:
        adapter_class = ep.load()
        ADAPTER_REGISTRY[ep.name] = adapter_class
```

### 23.4 Plugin Safety

- Plugins run in the same process (no sandboxing) -- trust model similar to pip packages
- All plugins must produce data in the canonical schema (validated by the core pipeline)
- Plugin metadata includes version, author, licence, required API keys
- A plugin catalogue (similar to QGIS or Jupyter extensions) could be hosted on GitHub

---

## 24. Claude API Integration Design

> **Checked:** March 2025

### 24.1 Integration Points

| Use Case | Trigger | Model | Input | Output |
|----------|---------|-------|-------|--------|
| **Correlation interpretation** | User views a correlation result | Sonnet 4.5 | Correlation stats + region + variables | 2-3 paragraph narrative |
| **Natural language query** | User types a question | Haiku 4.5 (parse) + Sonnet (respond) | User question + schema | SQL query + narrative answer |
| **Automated pattern scan** | New data ingested (batch) | Haiku 4.5 (Batch API) | Significant new correlations | Brief summary per finding |
| **Hypothesis generation** | Researcher requests | Opus 4.6 | Full causal graph for a region | Ranked hypotheses with literature references |

### 24.2 Prompt Templates

**Correlation Interpretation Prompt:**

```python
INTERPRET_CORRELATION_PROMPT = """You are a research analyst specialising in cross-domain
spatiotemporal analysis, with expertise in conflict, climate, food security, and development.

## Data Context
- Region: {region_name} ({country_iso3})
- Grid cells analysed: {n_cells}
- Time period: {start_date} to {end_date}
- Variable A: {var_a_name} ({var_a_description}, source: {var_a_source})
- Variable B: {var_b_name} ({var_b_description}, source: {var_b_source})

## Statistical Results
- Pearson correlation: {r_value:.3f}
- P-value: {p_value:.6f}
- Optimal lag: {lag_months} months (A leads B by {lag_months} months)
- 95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]
- N observations: {n_obs}
- Data quality (mean composite): {quality_mean:.2f}

## Instructions
1. Interpret this correlation in the specific context of {region_name}.
2. Describe plausible causal mechanisms that could explain this relationship.
3. Reference known academic research on this type of relationship (be specific).
4. Identify possible confounders that could produce a spurious correlation.
5. Assess whether the lag structure ({lag_months} months) is plausible.
6. Rate confidence: HIGH (strong evidence, known mechanism),
   MEDIUM (suggestive, plausible mechanism), or LOW (weak evidence, likely spurious).
7. Suggest follow-up analyses that could strengthen or weaken the causal claim.

Be concise (300-500 words). Use specific data from the results. Do not
over-claim causation from correlation alone."""
```

### 24.3 Structured Output Schema

```python
from pydantic import BaseModel
from typing import Literal

class CorrelationInterpretation(BaseModel):
    summary: str  # 1-2 sentence headline
    mechanism: str  # Plausible causal pathway
    academic_references: list[str]  # Known research
    confounders: list[str]  # Potential confounding variables
    lag_assessment: str  # Whether the lag makes sense
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    follow_up: list[str]  # Suggested next analyses

# Use with Claude structured outputs
response = client.messages.create(
    model="claude-sonnet-4-5-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "correlation_interpretation",
            "schema": CorrelationInterpretation.model_json_schema()
        }
    }
)
result = CorrelationInterpretation.model_validate_json(response.content[0].text)
```

### 24.4 Cost Estimates

Pricing as of March 2025 (source: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)):

| Model | Input ($/M tokens) | Output ($/M tokens) | Batch discount |
|-------|-------------------|---------------------|----------------|
| Claude Haiku 4.5 | $1.00 | $5.00 | 50% |
| Claude Sonnet 4.5 | $3.00 | $15.00 | 50% |
| Claude Opus 4.6 | $5.00 | $25.00 | 50% |

**Per-request cost estimates:**

| Use Case | Model | Input tokens | Output tokens | Cost per request | Monthly (1000 req) |
|----------|-------|-------------|---------------|-----------------|---------------------|
| Correlation interpretation | Sonnet 4.5 | ~800 | ~500 | $0.0099 | $9.90 |
| NL query (parse) | Haiku 4.5 | ~500 | ~200 | $0.0015 | $1.50 |
| NL query (respond) | Sonnet 4.5 | ~1000 | ~400 | $0.0090 | $9.00 |
| Pattern scan (batch) | Haiku 4.5 (batch) | ~600 | ~300 | $0.0011 | -- |
| Hypothesis generation | Opus 4.6 | ~5000 | ~2000 | $0.0750 | $75.00 (1K) |

**Cost optimisation strategies:**
- Use Batch API (50% discount) for automated pattern scanning -- results within 1 hour, not real-time
- Cache interpretations -- same correlation stats = same interpretation
- Prompt caching: if system prompt is > 1024 tokens, cache it (90% discount on cached portion)
- Use Haiku for parsing/routing, Sonnet for generation, Opus only for complex hypothesis generation
- Combined with prompt caching + batch: up to 95% cost reduction on repetitive workloads

### 24.5 Error Handling

```python
import anthropic

async def interpret_with_claude(correlation_data: dict) -> dict:
    """Call Claude API with retry and fallback."""
    try:
        response = await client.messages.create(
            model="claude-sonnet-4-5-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": format_prompt(correlation_data)}],
            timeout=30.0
        )
        return parse_interpretation(response)
    except anthropic.RateLimitError:
        # Queue for batch processing instead
        await queue_for_batch(correlation_data)
        return {"status": "queued", "message": "Interpretation will be available shortly"}
    except anthropic.APIError as e:
        logger.error("claude_api_error", error=str(e), correlation=correlation_data)
        return {"status": "error", "message": "AI interpretation unavailable"}
```

Source: [Claude Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Claude API Pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Claude Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [Claude Prompt Templates](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompt-templates-and-variables)

---

## 25. Novel Architecture Ideas

> **Checked:** March 2025

### 25.1 Causal Atlas as a Service (CAaaS)

**Concept:** Expose Causal Atlas's core capability -- querying causal relationships -- as a public API that other applications can consume.

```
POST /api/v1/causal/query
{
  "region": {"type": "bbox", "coordinates": [29, -5, 42, 12]},
  "variable_a": "rainfall_deficit",
  "variable_b": "conflict_events",
  "time_range": ["2020-01", "2024-12"],
  "method": "granger",
  "max_lag": 12,
  "include_interpretation": true
}

Response:
{
  "causal_links": [
    {
      "lag_months": 3,
      "f_statistic": 12.4,
      "p_value": 0.0001,
      "direction": "a_causes_b",
      "strength": "strong",
      "interpretation": "Rainfall deficits in this region precede increases in conflict events by approximately 3 months, consistent with the climate-food-conflict pathway documented by Raleigh et al. (2015)...",
      "confidence": "HIGH"
    }
  ],
  "metadata": {
    "n_cells": 620,
    "n_observations": 74400,
    "data_quality_mean": 0.87,
    "computation_time_ms": 1234
  }
}
```

**Use cases:**
- Humanitarian organisations querying "what are the causal risk factors for food insecurity in Region X?"
- Early warning systems consuming causal predictions as input features
- Journalists investigating causal claims about climate-conflict links
- Academic researchers accessing pre-computed causal networks for further analysis

### 25.2 Federated Analysis

**Concept:** Enable analysis on data that cannot be centralised -- privacy-sensitive data (health records, individual mobility data) or data with restrictive licences.

**Architecture:**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Provider A │     │  Data Provider B │     │  Data Provider C │
│  (National stats │     │  (Health data,   │     │  (Conflict data, │
│   office)        │     │   hospital)      │     │   classified)    │
│                  │     │                  │     │                  │
│  ┌────────────┐  │     │  ┌────────────┐  │     │  ┌────────────┐  │
│  │ Local      │  │     │  │ Local      │  │     │  │ Local      │  │
│  │ DuckDB     │  │     │  │ DuckDB     │  │     │  │ DuckDB     │  │
│  │ + Analysis │  │     │  │ + Analysis │  │     │  │ + Analysis │  │
│  │ Agent      │  │     │  │ Agent      │  │     │  │ Agent      │  │
│  └─────┬──────┘  │     │  └─────┬──────┘  │     │  └─────┬──────┘  │
│        │         │     │        │         │     │        │         │
└────────┼─────────┘     └────────┼─────────┘     └────────┼─────────┘
         │                        │                        │
         │  Aggregated stats      │  Aggregated stats      │
         │  (no individual data)  │  (no individual data)  │
         ▼                        ▼                        ▼
    ┌──────────────────────────────────────────────────────────┐
    │              Causal Atlas Central Server                   │
    │  Combines aggregate statistics from all providers          │
    │  Computes cross-domain correlations on aggregated data     │
    │  Never sees raw individual-level data                      │
    └──────────────────────────────────────────────────────────┘
```

**Privacy technologies:**
- **Differential privacy:** Add calibrated noise to aggregate statistics before sharing (local differential privacy)
- **Secure aggregation:** Use cryptographic protocols so the central server only sees the sum, not individual contributions
- **Federated learning:** Train correlation/causal models locally, share only model parameters

**Practical starting point:** Package a Docker container with DuckDB, our adapter code, and a "compute and share aggregates" script. Data providers run it on their own infrastructure and upload only the aggregated Parquet files.

Source: [Federated Analysis Primer (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10846631/), [Local Differential Privacy for Mobility (2025)](https://link.springer.com/article/10.1140/epjds/s13688-025-00611-4)

### 25.3 Collaborative Annotation

**Concept:** Researchers mark discovered causal links as "confirmed," "plausible," "spurious," or "needs investigation," building a curated knowledge base over time.

**Design:**

```python
class CausalAnnotation(BaseModel):
    link_id: str  # Hash of (var_a, var_b, region, lag)
    annotator_id: str  # ORCID or username
    label: Literal["confirmed", "plausible", "spurious", "needs_investigation"]
    confidence: float  # 0-1
    evidence: str  # Free text: why this label?
    references: list[str]  # DOIs or URLs of supporting literature
    timestamp: datetime

# API endpoint
@app.post("/api/v1/causal/annotate")
async def annotate_link(annotation: CausalAnnotation, user = Depends(verify_contributor)):
    ...
```

**Aggregation:** When multiple researchers annotate the same link, compute a consensus label (majority vote or confidence-weighted). Display the consensus prominently, with individual annotations accessible for transparency.

**Incentive:** Recognise top annotators on a leaderboard. Publish the curated causal knowledge base as a citable dataset (Zenodo DOI).

### 25.4 Automated Hypothesis Generation

**Concept:** When the system discovers a statistically significant correlation, automatically generate a structured hypothesis and suggest validation studies.

**Pipeline:**

```
New significant correlation detected
  ↓
Generate hypothesis (Claude Opus):
  - H1: "Rainfall deficits in Turkana cause increased conflict through
         food price increases, with a 3-month lag"
  - Mechanism: "Pastoral livelihoods depend on rainfall; drought reduces
               livestock productivity; competition for resources increases"
  - Required evidence: [
      "Granger causality test (done, p < 0.001)",
      "Mediation analysis through food prices (not yet done)",
      "Instrumental variable analysis using ENSO as instrument (not yet done)",
      "Qualitative case study validation (requires fieldwork)"
    ]
  - Confidence level: MEDIUM (correlation established, mechanism plausible,
                      but mediation not yet tested)
  ↓
Add to hypothesis registry
  ↓
Notify interested researchers (topic-based subscriptions)
  ↓
Track evidence accumulation over time
```

### 25.5 Real-Time Discovery Dashboard

**Concept:** A continuously updating dashboard that monitors all discovered causal relationships as new data arrives.

**Design:**
- **Discovery feed:** Chronological list of newly significant correlations, like a social media feed but for causal discoveries
- **Alert rules:** Researchers subscribe to specific variable pairs or regions. When a new significant finding matches their subscription, they receive an email/webhook.
- **Trend monitoring:** Track how the strength of known causal relationships changes over time. A weakening relationship (previously strong correlation becoming insignificant) is as newsworthy as a new one.
- **Anomaly detection:** Flag when a known causal relationship breaks down (e.g., drought usually predicts conflict in Region X, but this time it did not -- why?)

**Implementation:**

```python
# Run after each data ingestion
async def scan_for_new_discoveries(updated_cells: list[int], updated_months: list[tuple[int, int]]):
    """Scan for new significant correlations in updated data."""
    for gid in updated_cells:
        for var_a, var_b in variable_pairs:
            for lag in range(1, 13):
                r, p = compute_lagged_correlation(gid, var_a, var_b, lag)
                if p < 0.001 and abs(r) > 0.5:
                    # Check if this is a NEW finding (not previously discovered)
                    if not is_known_finding(var_a, var_b, gid, lag):
                        finding = Finding(var_a=var_a, var_b=var_b, gid=gid,
                                         lag=lag, r=r, p=p)
                        # Get AI interpretation
                        finding.interpretation = await interpret_with_claude(finding)
                        # Save and notify
                        save_finding(finding)
                        await notify_subscribers(finding)
```

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

### Pipeline Orchestration (Section 12)
- [Dagster vs Prefect vs Airflow (ZenML)](https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow) -- Comprehensive comparison
- [FreeAgent Orchestration Comparison](https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/) -- Practical evaluation
- [Airflow vs Dagster vs Prefect (RisingWave)](https://risingwave.com/blog/airflow-vs-dagster-vs-prefect-a-detailed-comparison/) -- Detailed feature comparison
- [Python Data Pipeline Tools 2026](https://ukdataservices.co.uk/blog/articles/python-data-pipeline-tools-2025) -- Current landscape

### Event-Driven Architecture (Section 13)
- [Prefect Event Triggers vs Sensors](https://www.prefect.io/blog/push-and-pull-architecture-event-triggers-vs-sensors-in-data-pipelines) -- Push vs pull patterns
- [Dagster Sensors Documentation](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) -- File and time-based sensors

### Testing and CI/CD (Sections 17-18)
- [Great Expectations](https://greatexpectations.io/) -- Data quality testing framework
- [Great Expectations + GitHub Actions](https://greatexpectations.io/blog/github-actions/) -- CI integration guide
- [pytest + Great Expectations Pipeline Testing](https://github.com/greatexpectationslabs/put-data-pipeline-under-test-with-pytest-and-great-expectations) -- Example repository
- [pytest + GitHub Actions Tutorial](https://pytest-with-eric.com/integrations/pytest-github-actions/) -- Setup guide

### Documentation (Section 19)
- [MkDocs Material Theme](https://squidfunk.github.io/mkdocs-material/) -- Material for MkDocs
- [MkDocs vs Docusaurus (Damavis)](https://blog.damavis.com/en/mkdocs-vs-docusaurus-for-technical-documentation/) -- Comparison
- [Documentation Generator Comparison 2025](https://okidoki.dev/documentation-generator-comparison) -- VitePress vs Docusaurus vs MkDocs

### Observability (Section 20)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) -- Python SDK
- [OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/) -- Core concepts
- [structlog Documentation](https://www.structlog.org/) -- Structured logging for Python

### Claude API Integration (Section 24)
- [Claude Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) -- Schema-guaranteed responses
- [Claude API Pricing](https://platform.claude.com/docs/en/about-claude/pricing) -- Per-token pricing
- [Claude Batch Processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) -- 50% discount for async
- [Claude Prompt Templates](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompt-templates-and-variables) -- Template guide

### Federated Analysis (Section 25.2)
- [Federated Analysis Primer (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10846631/) -- Technical and legal overview
- [Local Differential Privacy for Mobility (2025)](https://link.springer.com/article/10.1140/epjds/s13688-025-00611-4) -- Privacy-preserving spatial data
- [Privacy in Federated Learning (2025)](https://link.springer.com/article/10.1007/s10462-025-11170-5) -- Privacy mechanisms survey
