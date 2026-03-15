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
26. [Detailed Data Model](#26-detailed-data-model)
27. [Adapter Specification (Detailed)](#27-adapter-specification-detailed)
28. [Deployment Architecture](#28-deployment-architecture)
29. [Data Pipeline Scheduling](#29-data-pipeline-scheduling)
30. [Claude API Integration -- Detailed Design](#30-claude-api-integration----detailed-design)

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

## 26. Detailed Data Model

> **Checked:** March 2025

### 26.1 Entity-Relationship Diagram

```
┌─────────────────────────┐         ┌─────────────────────────────┐
│       grid_cells        │         │          variables          │
├─────────────────────────┤         ├─────────────────────────────┤
│ gid         INT32   PK  │    ┌───>│ name        VARCHAR    PK   │
│ row         INT16       │    │    │ domain      VARCHAR         │
│ col         INT16       │    │    │ unit        VARCHAR         │
│ lat_centre  FLOAT64     │    │    │ description VARCHAR         │
│ lon_centre  FLOAT64     │    │    │ aggregation VARCHAR         │
│ geometry    GEOMETRY    │    │    │   (sum|mean|max|min|mode)    │
│ country_iso3 VARCHAR    │    │    │ temporal_res VARCHAR         │
│ is_land     BOOLEAN     │    │    │   (daily|monthly|annual)     │
│ area_km2    FLOAT64     │    │    │ source_id   VARCHAR    FK──>│──┐
│ elevation_m FLOAT64     │    │    │ created_at  TIMESTAMP       │  │
│ pop_2020    FLOAT64     │    │    └─────────────────────────────┘  │
└────────┬────────────────┘    │                                     │
         │                     │    ┌─────────────────────────────┐  │
         │  1:N                │    │          sources            │  │
         │                     │    ├─────────────────────────────┤  │
         ▼                     │    │ source_id   VARCHAR    PK   │<─┘
┌─────────────────────────┐    │    │ name        VARCHAR         │
│      observations       │    │    │ version     VARCHAR         │
├─────────────────────────┤    │    │ url         VARCHAR         │
│ gid         INT32   FK──│───>│    │ licence     VARCHAR         │
│ year        INT16       │    │    │ licence_url VARCHAR         │
│ month       INT8        │    │    │ update_freq VARCHAR         │
│ variable    VARCHAR FK──│────┘    │   (daily|weekly|monthly|    │
│ value       FLOAT64     │         │    annual|irregular)        │
│ source_id   VARCHAR FK──│────────>│ api_base_url VARCHAR        │
│ quality_flag INT8       │         │ requires_key BOOLEAN        │
│   (0=observed,          │         │ citation    VARCHAR         │
│    1=interpolated,      │         │ notes       VARCHAR         │
│    2=modelled,          │         │ last_checked DATE           │
│    3=imputed)           │         └─────────────────────────────┘
│ quality_composite FLOAT │
│ ingested_at TIMESTAMP   │
└────────┬────────────────┘
         │
         │  N:N (via analysis)
         │
         ▼
┌──────────────────────────────────┐    ┌──────────────────────────┐
│      causal_relationships        │    │      analysis_runs       │
├──────────────────────────────────┤    ├──────────────────────────┤
│ id            UUID          PK   │    │ id          UUID     PK  │
│ source_var    VARCHAR       FK   │    │ started_at  TIMESTAMP    │
│ target_var    VARCHAR       FK   │    │ completed_at TIMESTAMP   │
│ lag_months    INT8               │    │ method      VARCHAR      │
│ strength      FLOAT64            │    │   (granger|pcmci|       │
│   (correlation coefficient)      │    │    transfer_entropy|     │
│ p_value       FLOAT64            │    │    pearson|ccm)          │
│ ci_lower      FLOAT64            │    │ parameters  JSON         │
│ ci_upper      FLOAT64            │    │   {"tau_max": 12,        │
│ method        VARCHAR            │    │    "alpha": 0.05,        │
│ analysis_run_id UUID        FK──>│───>│    "ci_test": "ParCorr"} │
│ spatial_extent VARCHAR           │    │ status      VARCHAR      │
│   (global|continent|country|     │    │   (pending|running|      │
│    region|single_cell)           │    │    completed|failed)     │
│ region_name   VARCHAR            │    │ n_cells     INT32        │
│ n_cells       INT32              │    │ n_variables INT16        │
│ n_observations INT32             │    │ error_msg   VARCHAR      │
│ discovered_at TIMESTAMP          │    │ triggered_by VARCHAR     │
│ confidence    VARCHAR            │    │   (manual|schedule|      │
│   (HIGH|MEDIUM|LOW)              │    │    sensor|api)           │
│ interpretation TEXT              │    └──────────────────────────┘
│ interpretation_model VARCHAR     │
└──────────────────────────────────┘
```

### 26.2 Parquet File Organization

The complete directory structure on disk, using Hive-style partitioning for DuckDB auto-discovery:

```
data/
├── raw/                                    # Downloaded files, original format
│   ├── acled/
│   │   ├── acled_2024-01_2024-06.csv
│   │   └── checksums.sha256
│   ├── chirps/
│   │   ├── chirps-v2.0.2024.01.01.tif
│   │   ├── chirps-v2.0.2024.01.02.tif
│   │   └── ...
│   ├── usgs/
│   │   └── earthquakes_2024-01.geojson
│   └── ...
│
├── processed/                              # Canonical Parquet, long format
│   ├── domain=conflict/
│   │   ├── year=2020/
│   │   │   ├── acled_events.parquet        # ~259,200 rows (12 months x 21,600 land cells)
│   │   │   ├── acled_fatalities.parquet
│   │   │   └── ucdp_ged_events.parquet
│   │   ├── year=2021/
│   │   │   └── ...
│   │   └── year=2024/
│   │       └── ...
│   ├── domain=climate/
│   │   ├── year=2020/
│   │   │   ├── chirps_precip_mm.parquet
│   │   │   ├── ndvi_mean.parquet
│   │   │   └── temperature_mean.parquet
│   │   └── ...
│   ├── domain=food_security/
│   │   ├── year=2020/
│   │   │   ├── wfp_price_maize.parquet
│   │   │   ├── wfp_price_rice.parquet
│   │   │   └── fao_crop_production.parquet
│   │   └── ...
│   ├── domain=natural_hazards/
│   │   ├── year=2020/
│   │   │   ├── usgs_earthquake_count.parquet
│   │   │   ├── usgs_earthquake_max_mag.parquet
│   │   │   └── emdat_disaster_count.parquet
│   │   └── ...
│   ├── domain=environment/
│   │   ├── year=2020/
│   │   │   ├── openaq_pm25_mean.parquet
│   │   │   └── nightlights_mean.parquet
│   │   └── ...
│   └── domain=socioeconomic/
│       ├── year=2020/
│       │   ├── wb_gdp_per_capita.parquet
│       │   └── wb_population.parquet
│       └── ...
│
├── grid/                                   # Static reference data
│   ├── prio_grid_cells.geoparquet          # 259,200 cells with geometries
│   ├── prio_grid_land_mask.parquet         # Boolean land mask
│   ├── country_grid_lookup.parquet         # gid -> ISO3 mapping
│   └── grid_static_variables.parquet       # Elevation, terrain, distance to border
│
├── analysis/                               # Analysis outputs
│   ├── correlations/
│   │   ├── run=20250315_143022/
│   │   │   ├── metadata.json              # Run parameters, status, timing
│   │   │   ├── results.parquet            # Causal relationship table
│   │   │   └── diagnostics.parquet        # Per-cell diagnostics
│   │   └── run=20250401_091500/
│   │       └── ...
│   ├── pcmci/
│   │   ├── run=20250320_060000/
│   │   │   ├── metadata.json
│   │   │   ├── causal_graph.parquet       # Full causal graph
│   │   │   └── link_strengths.parquet     # Pairwise link strengths
│   │   └── ...
│   └── interpretations/
│       └── cache.parquet                  # Cached Claude interpretations
│
├── tiles/                                  # Pre-rendered map tiles
│   ├── grid_overview.pmtiles              # All cells, single layer
│   └── variable_layers/
│       ├── acled_fatalities_2024.pmtiles
│       └── chirps_precip_2024.pmtiles
│
└── exports/                                # User-requested data exports
    └── ...
```

### 26.3 DuckDB Views and Materialized Tables

DuckDB reads Parquet files directly but benefits from pre-defined views for common query patterns:

```sql
-- View: All processed data across all domains and years
CREATE OR REPLACE VIEW observations AS
SELECT *
FROM read_parquet(
    'data/processed/domain=*/year=*/**.parquet',
    hive_partitioning = true,
    union_by_name = true
);

-- View: Grid cell reference with geometries
CREATE OR REPLACE VIEW grid_cells AS
SELECT * FROM read_parquet('data/grid/prio_grid_cells.geoparquet');

-- View: Land cells only (skip ocean)
CREATE OR REPLACE VIEW land_cells AS
SELECT * FROM read_parquet('data/grid/prio_grid_land_mask.parquet')
WHERE is_land = true;

-- View: Latest available data per variable
CREATE OR REPLACE VIEW latest_observations AS
SELECT o.*
FROM observations o
INNER JOIN (
    SELECT variable, MAX(year * 100 + month) AS max_period
    FROM observations
    GROUP BY variable
) latest ON o.variable = latest.variable
    AND (o.year * 100 + o.month) = latest.max_period;

-- View: Wide-format pivot for analysis (example: East Africa, 3 variables)
CREATE OR REPLACE VIEW east_africa_wide AS
PIVOT (
    SELECT gid, year, month, variable, value
    FROM observations
    WHERE gid IN (SELECT gid FROM read_parquet('data/grid/country_grid_lookup.parquet')
                  WHERE country_iso3 IN ('KEN', 'ETH', 'SOM', 'SSD', 'UGA', 'TZA'))
)
ON variable
USING FIRST(value)
GROUP BY gid, year, month;

-- Materialized table: Pre-computed monthly aggregates by country
CREATE TABLE IF NOT EXISTS country_monthly_agg AS
SELECT
    l.country_iso3,
    o.year,
    o.month,
    o.variable,
    AVG(o.value) AS mean_value,
    MIN(o.value) AS min_value,
    MAX(o.value) AS max_value,
    STDDEV(o.value) AS stddev_value,
    COUNT(*) AS n_cells,
    AVG(o.quality_composite) AS mean_quality
FROM observations o
JOIN read_parquet('data/grid/country_grid_lookup.parquet') l
    ON o.gid = l.gid
GROUP BY l.country_iso3, o.year, o.month, o.variable;

-- Materialized table: Causal relationship catalogue
CREATE TABLE IF NOT EXISTS causal_catalogue AS
SELECT * FROM read_parquet('data/analysis/correlations/run=*/results.parquet',
                           hive_partitioning = true,
                           union_by_name = true);

-- View: Variable catalogue with metadata
CREATE OR REPLACE VIEW variable_catalogue AS
SELECT
    variable,
    domain,
    COUNT(DISTINCT gid) AS n_cells,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(*) AS n_observations,
    AVG(quality_composite) AS mean_quality
FROM observations
GROUP BY variable, domain;
```

These views are defined in a `setup_views.sql` file that runs on application startup. DuckDB's lazy evaluation means views do not materialise data until queried.

---

## 27. Adapter Specification (Detailed)

> **Checked:** March 2025

### 27.1 Abstract Base Class (Full Definition)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import pyarrow as pa
import pyarrow.parquet as pq
import structlog

logger = structlog.get_logger()


class AdapterState(Enum):
    IDLE = "idle"
    DISCOVERING = "discovering"
    FETCHING = "fetching"
    PARSING = "parsing"
    VALIDATING = "validating"
    TRANSFORMING = "transforming"
    STORING = "storing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AdapterConfig:
    source_id: str                          # e.g., "acled_v24"
    domain: str                             # e.g., "conflict"
    variables: list[str] = field(           # Variables this adapter produces
        default_factory=list)
    api_key: str | None = None
    api_key_env_var: str | None = None      # e.g., "ACLED_API_KEY"
    base_url: str | None = None
    rate_limit_rps: float = 1.0             # Requests per second
    max_retries: int = 3
    retry_backoff_base: float = 2.0         # Exponential backoff base (seconds)
    retry_backoff_max: float = 300.0        # Max backoff (5 minutes)
    timeout_seconds: float = 60.0           # Per-request timeout
    chunk_size_days: int = 30               # How many days to fetch per request
    user_agent: str = "CausalAtlas/0.1 (https://github.com/aldred-coetzee/causal-atlas)"


@dataclass
class AdapterCheckpoint:
    source_id: str
    last_successful_date: date | None = None
    last_run_at: datetime | None = None
    last_content_hash: str | None = None    # SHA-256 of last fetched data
    last_etag: str | None = None            # HTTP ETag for change detection
    last_modified: str | None = None        # HTTP Last-Modified header
    rows_ingested: int = 0
    status: str = "never_run"


@dataclass
class ValidationReport:
    total_rows: int
    valid_rows: int
    invalid_rows: int
    null_counts: dict[str, int]             # Column -> null count
    out_of_range: dict[str, int]            # Column -> out-of-range count
    warnings: list[str]
    errors: list[str]
    quality_mean: float


class BaseAdapter(ABC):
    """Abstract base class for all data source adapters.

    Lifecycle: discover -> fetch -> parse -> validate -> transform -> store -> verify

    Each method can be called independently for debugging, or chained via run().
    """

    def __init__(self, config: AdapterConfig, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.state = AdapterState.IDLE
        self._checkpoint: AdapterCheckpoint | None = None
        self._log = logger.bind(source=config.source_id)

    # ── Lifecycle Methods ──────────────────────────────────────────────

    @abstractmethod
    def discover(self) -> dict[str, Any]:
        """Discover what data is available from the source.

        Returns metadata about available date ranges, variables, and coverage.
        Used to determine what needs to be fetched.

        Returns:
            {"available_range": (date, date), "variables": [...],
             "last_updated": date, "estimated_size_mb": float}
        """
        ...

    @abstractmethod
    def fetch(self, start_date: date, end_date: date) -> bytes | Path:
        """Download raw data from the source.

        Handles pagination, rate limiting, and authentication.
        Returns raw bytes (for small responses) or a Path to a temp file.

        Raises:
            FetchError: Network errors, auth failures, rate limiting
        """
        ...

    @abstractmethod
    def parse(self, raw_data: bytes | Path) -> pa.Table:
        """Parse raw data into a PyArrow Table with source-native schema.

        Preserves all original fields -- no transformation yet.
        Handles CSV, JSON, GeoJSON, NetCDF, GeoTIFF, etc.

        Raises:
            ParseError: Malformed data, unexpected schema
        """
        ...

    @abstractmethod
    def validate(self, table: pa.Table) -> tuple[pa.Table, ValidationReport]:
        """Validate data quality.

        Checks: null counts, value ranges, temporal completeness,
        spatial coverage, duplicate detection.
        Adds quality_flag and quality_composite columns.
        Returns the table with quality columns and a validation report.

        Raises:
            ValidationError: Critical data quality issues (>50% invalid)
        """
        ...

    @abstractmethod
    def transform(self, table: pa.Table) -> pa.Table:
        """Transform to canonical schema.

        Operations:
        - Point-to-grid aggregation (lat/lon -> PRIO-GRID gid)
        - Raster resampling (fine grid -> 0.5-degree cells)
        - Temporal alignment (daily -> monthly, annual -> monthly)
        - Column renaming to canonical names
        - Unit conversion if needed

        Output schema: gid, year, month, variable, value, source_id,
                       quality_flag, quality_composite, ingested_at
        """
        ...

    def store(self, table: pa.Table) -> Path:
        """Write to partitioned Parquet files.

        Common implementation -- rarely needs overriding.
        Partitions by domain and year (Hive-style).
        Uses Snappy compression, row groups of 100K rows.
        """
        self.state = AdapterState.STORING

        # Group by year for partitioned output
        years = table.column("year").to_pylist()
        unique_years = sorted(set(years))

        output_paths = []
        for year in unique_years:
            year_mask = pa.compute.equal(table.column("year"), year)
            year_table = table.filter(year_mask)

            partition_dir = (
                self.output_dir
                / f"domain={self.config.domain}"
                / f"year={year}"
            )
            partition_dir.mkdir(parents=True, exist_ok=True)

            # One file per variable per year
            variables = year_table.column("variable").to_pylist()
            for var in sorted(set(variables)):
                var_mask = pa.compute.equal(year_table.column("variable"), var)
                var_table = year_table.filter(var_mask)

                output_path = partition_dir / f"{var}.parquet"
                pq.write_table(
                    var_table,
                    output_path,
                    compression="snappy",
                    row_group_size=100_000,
                    write_statistics=True,
                    # Sort by gid for optimal predicate pushdown
                    use_dictionary=["variable", "source_id", "quality_flag"],
                )
                output_paths.append(output_path)

        self._log.info("store_completed", n_files=len(output_paths),
                       years=unique_years)
        return output_paths[0].parent.parent  # Return base partition dir

    def verify(self, output_dir: Path) -> bool:
        """Verify written Parquet files are readable and internally consistent.

        Checks:
        - Files are valid Parquet (readable by DuckDB)
        - Row counts match expected
        - Schema matches canonical schema
        - No corruption (Parquet footer is valid)
        """
        self.state = AdapterState.VERIFYING
        import duckdb

        con = duckdb.connect()
        try:
            result = con.execute(f"""
                SELECT COUNT(*) AS n_rows,
                       COUNT(DISTINCT gid) AS n_cells,
                       MIN(year) AS min_year,
                       MAX(year) AS max_year
                FROM read_parquet('{output_dir}/domain=*/year=*/**.parquet',
                                  hive_partitioning=true)
                WHERE source_id = ?
            """, [self.config.source_id]).fetchone()

            self._log.info("verify_completed",
                           n_rows=result[0], n_cells=result[1],
                           year_range=f"{result[2]}-{result[3]}")
            return result[0] > 0
        except Exception as e:
            self._log.error("verify_failed", error=str(e))
            return False
        finally:
            con.close()

    def run(self, start_date: date, end_date: date) -> Path:
        """Full pipeline: discover -> fetch -> parse -> validate ->
           transform -> store -> verify.

        This is the primary entry point for adapter execution.
        """
        run_start = datetime.utcnow()
        self._log.info("run_started", start_date=str(start_date),
                       end_date=str(end_date))
        try:
            self.state = AdapterState.DISCOVERING
            metadata = self.discover()
            self._log.info("discover_completed", metadata=metadata)

            self.state = AdapterState.FETCHING
            raw = self.fetch(start_date, end_date)

            self.state = AdapterState.PARSING
            parsed = self.parse(raw)
            self._log.info("parse_completed", n_rows=parsed.num_rows)

            self.state = AdapterState.VALIDATING
            validated, report = self.validate(parsed)
            self._log.info("validate_completed",
                           valid=report.valid_rows,
                           invalid=report.invalid_rows,
                           quality_mean=report.quality_mean)
            if report.errors:
                for err in report.errors:
                    self._log.error("validation_error", error=err)

            self.state = AdapterState.TRANSFORMING
            transformed = self.transform(validated)
            self._log.info("transform_completed", n_rows=transformed.num_rows)

            output = self.store(transformed)
            verified = self.verify(self.output_dir)

            self.state = AdapterState.COMPLETED
            duration = (datetime.utcnow() - run_start).total_seconds()
            self._log.info("run_completed",
                           duration_seconds=duration,
                           n_rows=transformed.num_rows,
                           verified=verified)

            # Update checkpoint
            self._save_checkpoint(end_date, transformed.num_rows)
            return output

        except Exception as e:
            self.state = AdapterState.FAILED
            self._log.error("run_failed", error=str(e),
                            state=self.state.value)
            raise

    # ── Checkpoint Management ──────────────────────────────────────────

    def _load_checkpoint(self) -> AdapterCheckpoint:
        """Load checkpoint from JSON file."""
        checkpoint_path = self.output_dir / ".checkpoints" / f"{self.config.source_id}.json"
        if checkpoint_path.exists():
            import json
            data = json.loads(checkpoint_path.read_text())
            return AdapterCheckpoint(**data)
        return AdapterCheckpoint(source_id=self.config.source_id)

    def _save_checkpoint(self, last_date: date, rows: int):
        """Save checkpoint after successful run."""
        import json
        checkpoint_dir = self.output_dir / ".checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        checkpoint = AdapterCheckpoint(
            source_id=self.config.source_id,
            last_successful_date=last_date,
            last_run_at=datetime.utcnow(),
            rows_ingested=rows,
            status="completed"
        )
        path = checkpoint_dir / f"{self.config.source_id}.json"
        path.write_text(json.dumps(
            {k: str(v) if isinstance(v, (date, datetime)) else v
             for k, v in checkpoint.__dict__.items()},
            indent=2
        ))
```

### 27.2 Error Taxonomy

```python
class AdapterError(Exception):
    """Base exception for all adapter errors."""
    def __init__(self, message: str, source_id: str, recoverable: bool = False):
        self.source_id = source_id
        self.recoverable = recoverable
        super().__init__(f"[{source_id}] {message}")


class FetchError(AdapterError):
    """Errors during data download."""
    pass

class NetworkError(FetchError):
    """Connection timeout, DNS failure, SSL error."""
    def __init__(self, source_id: str, url: str, status_code: int | None = None):
        self.url = url
        self.status_code = status_code
        super().__init__(f"Network error fetching {url} (status={status_code})",
                         source_id, recoverable=True)

class RateLimitError(FetchError):
    """HTTP 429 or equivalent rate limiting."""
    def __init__(self, source_id: str, retry_after: float | None = None):
        self.retry_after = retry_after
        super().__init__(f"Rate limited, retry after {retry_after}s",
                         source_id, recoverable=True)

class AuthenticationError(FetchError):
    """HTTP 401/403, invalid API key."""
    def __init__(self, source_id: str):
        super().__init__("Authentication failed -- check API key",
                         source_id, recoverable=False)

class ParseError(AdapterError):
    """Errors during data parsing."""
    pass

class SchemaError(ParseError):
    """Unexpected columns, missing required fields."""
    def __init__(self, source_id: str, expected: list[str], actual: list[str]):
        missing = set(expected) - set(actual)
        super().__init__(f"Schema mismatch: missing columns {missing}",
                         source_id, recoverable=False)

class FormatError(ParseError):
    """Cannot parse file format (corrupt CSV, invalid JSON, etc.)."""
    pass

class ValidationError(AdapterError):
    """Data quality below acceptable threshold."""
    def __init__(self, source_id: str, report: "ValidationReport"):
        self.report = report
        pct_invalid = report.invalid_rows / max(report.total_rows, 1) * 100
        super().__init__(f"Validation failed: {pct_invalid:.1f}% invalid rows",
                         source_id, recoverable=False)

class SpatialError(AdapterError):
    """Errors in spatial operations (projection, aggregation)."""
    pass

class GridMappingError(SpatialError):
    """Cannot map coordinates to PRIO-GRID cells."""
    def __init__(self, source_id: str, lat: float, lon: float):
        super().__init__(f"Cannot map ({lat}, {lon}) to grid cell",
                         source_id, recoverable=False)
```

### 27.3 Retry and Backoff Strategy

```python
import tenacity
import httpx

def create_retry_policy(config: AdapterConfig) -> tenacity.Retrying:
    """Create a tenacity retry policy from adapter config.

    Strategy:
    - Exponential backoff with full jitter: wait = random(0, base^attempt)
    - Max retries: config.max_retries (default 3)
    - Max wait: config.retry_backoff_max (default 300s)
    - Retry on: NetworkError, RateLimitError, HTTP 5xx, HTTP 429
    - Do NOT retry on: AuthenticationError, ParseError, ValidationError
    """
    return tenacity.Retrying(
        retry=tenacity.retry_if_exception_type((
            NetworkError,
            RateLimitError,
            httpx.TimeoutException,
            httpx.ConnectError,
        )),
        wait=tenacity.wait_exponential_jitter(
            initial=1,
            exp_base=config.retry_backoff_base,
            max=config.retry_backoff_max,
            jitter=5,
        ),
        stop=tenacity.stop_after_attempt(config.max_retries),
        before_sleep=tenacity.before_sleep_log(logger, log_level=20),
        reraise=True,
    )
```

### 27.4 Incremental Update Detection

Adapters detect whether remote data has changed before downloading, using three mechanisms:

```python
import hashlib
import httpx

async def check_for_updates(config: AdapterConfig,
                            checkpoint: AdapterCheckpoint,
                            url: str) -> bool:
    """Check if remote data has changed since last fetch.

    Methods (in order of preference):
    1. HTTP ETag comparison (cheapest -- single HEAD request)
    2. HTTP Last-Modified comparison
    3. Content hash comparison (most expensive -- must download)
    """
    async with httpx.AsyncClient() as client:
        # Method 1: ETag
        head = await client.head(url, headers={
            "If-None-Match": checkpoint.last_etag or ""
        })
        if head.status_code == 304:
            logger.info("no_update_detected", method="etag", source=config.source_id)
            return False

        new_etag = head.headers.get("ETag")
        if new_etag and new_etag == checkpoint.last_etag:
            return False

        # Method 2: Last-Modified
        last_modified = head.headers.get("Last-Modified")
        if last_modified and last_modified == checkpoint.last_modified:
            logger.info("no_update_detected", method="last-modified",
                        source=config.source_id)
            return False

        # If we reach here, data may have changed
        return True


def compute_content_hash(data: bytes) -> str:
    """SHA-256 hash for content comparison."""
    return hashlib.sha256(data).hexdigest()
```

### 27.5 Adapter Registry with Plugin Discovery

```python
from importlib.metadata import entry_points
from typing import Type

ADAPTER_REGISTRY: dict[str, Type[BaseAdapter]] = {}


def register_adapter(source_id: str):
    """Decorator to register an adapter class."""
    def decorator(cls: Type[BaseAdapter]):
        if source_id in ADAPTER_REGISTRY:
            logger.warning("adapter_overwritten", source_id=source_id,
                           old=ADAPTER_REGISTRY[source_id].__name__,
                           new=cls.__name__)
        ADAPTER_REGISTRY[source_id] = cls
        return cls
    return decorator


def discover_plugins():
    """Discover adapter plugins installed via entry_points.

    Third-party packages register adapters in pyproject.toml:

        [project.entry-points."causal_atlas.adapters"]
        era5 = "causal_atlas_era5:ERA5Adapter"
    """
    eps = entry_points(group="causal_atlas.adapters")
    for ep in eps:
        try:
            adapter_class = ep.load()
            ADAPTER_REGISTRY[ep.name] = adapter_class
            logger.info("plugin_loaded", source_id=ep.name,
                        class_name=adapter_class.__name__)
        except Exception as e:
            logger.error("plugin_load_failed", source_id=ep.name, error=str(e))


def get_adapter(source_id: str, output_dir: Path,
                **config_kwargs) -> BaseAdapter:
    """Get an adapter instance by source ID."""
    if source_id not in ADAPTER_REGISTRY:
        discover_plugins()
    if source_id not in ADAPTER_REGISTRY:
        raise ValueError(f"No adapter registered for '{source_id}'. "
                         f"Available: {list(ADAPTER_REGISTRY.keys())}")
    cls = ADAPTER_REGISTRY[source_id]
    config = AdapterConfig(source_id=source_id, **config_kwargs)
    return cls(config, output_dir)
```

### 27.6 Complete Example Adapter: ACLED

```python
"""ACLED adapter -- complete pseudocode showing the full ingestion flow.

ACLED (Armed Conflict Location & Event Data) provides geocoded conflict
event data via a REST API. Events are points with lat/lon, event type,
fatality count, and other attributes.

API docs: https://apidocs.acleddata.com/
"""

import io
from datetime import date
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc

from causal_atlas.adapters.base import (
    BaseAdapter, AdapterConfig, ValidationReport,
    register_adapter, create_retry_policy
)
from causal_atlas.spatial import latlon_to_gid


@register_adapter("acled")
class ACLEDAdapter(BaseAdapter):
    """Ingest ACLED conflict events into PRIO-GRID monthly aggregates.

    Produces variables:
    - acled_event_count: Number of conflict events per cell per month
    - acled_fatalities: Total fatalities per cell per month
    - acled_battle_count: Battle events only
    - acled_protest_count: Protest events only
    """

    ACLED_API_URL = "https://api.acleddata.com/acled/read"
    PAGE_SIZE = 5000  # ACLED max per request

    def discover(self) -> dict:
        """Check ACLED API for available date range."""
        # ACLED API supports a metadata endpoint
        response = httpx.get(
            self.ACLED_API_URL,
            params={
                "key": self.config.api_key,
                "email": "user@example.com",
                "limit": 1,
                "fields": "event_date",
                "order": "desc",
            },
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        latest_date = data["data"][0]["event_date"]

        return {
            "available_range": (date(1997, 1, 1), date.fromisoformat(latest_date)),
            "variables": ["acled_event_count", "acled_fatalities",
                          "acled_battle_count", "acled_protest_count"],
            "last_updated": date.fromisoformat(latest_date),
            "estimated_size_mb": 1.5,  # Per month, approximate
        }

    def fetch(self, start_date: date, end_date: date) -> bytes:
        """Fetch ACLED events with pagination and retry.

        ACLED API returns JSON with max 5000 records per request.
        We paginate through the full date range.
        """
        retry = create_retry_policy(self.config)
        all_records = []
        page = 1

        while True:
            @retry
            def _fetch_page(page_num):
                response = httpx.get(
                    self.ACLED_API_URL,
                    params={
                        "key": self.config.api_key,
                        "email": "user@example.com",
                        "event_date": f"{start_date}|{end_date}",
                        "event_date_where": "BETWEEN",
                        "limit": self.PAGE_SIZE,
                        "page": page_num,
                        "fields": "event_id_cnty|event_date|year|"
                                  "event_type|sub_event_type|"
                                  "country|iso3|latitude|longitude|"
                                  "fatalities|source",
                    },
                    timeout=self.config.timeout_seconds,
                )
                response.raise_for_status()
                return response.json()

            result = _fetch_page(page)
            records = result.get("data", [])
            all_records.extend(records)

            self._log.info("fetch_page", page=page, records=len(records),
                           total_so_far=len(all_records))

            if len(records) < self.PAGE_SIZE:
                break  # Last page
            page += 1

        # Serialize to bytes for the parse step
        import json
        return json.dumps(all_records).encode("utf-8")

    def parse(self, raw_data: bytes) -> pa.Table:
        """Parse ACLED JSON into a PyArrow Table."""
        import json
        records = json.loads(raw_data)

        df = pd.DataFrame(records)
        # Type conversions
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
        df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").fillna(0).astype(int)
        df["event_date"] = pd.to_datetime(df["event_date"])
        df["year"] = df["event_date"].dt.year.astype("int16")
        df["month"] = df["event_date"].dt.month.astype("int8")

        return pa.Table.from_pandas(df)

    def validate(self, table: pa.Table) -> tuple[pa.Table, ValidationReport]:
        """Validate ACLED data quality."""
        df = table.to_pandas()
        warnings = []
        errors = []

        # Check for null coordinates
        null_lat = df["latitude"].isna().sum()
        null_lon = df["longitude"].isna().sum()
        if null_lat > 0:
            warnings.append(f"{null_lat} events with null latitude")

        # Check coordinate ranges
        out_of_range_lat = ((df["latitude"] < -90) | (df["latitude"] > 90)).sum()
        out_of_range_lon = ((df["longitude"] < -180) | (df["longitude"] > 180)).sum()
        if out_of_range_lat > 0:
            errors.append(f"{out_of_range_lat} events with latitude out of range")

        # Check fatalities are non-negative
        negative_fat = (df["fatalities"] < 0).sum()
        if negative_fat > 0:
            errors.append(f"{negative_fat} events with negative fatalities")

        # Remove invalid rows
        valid_mask = (
            df["latitude"].notna() &
            df["longitude"].notna() &
            df["latitude"].between(-90, 90) &
            df["longitude"].between(-180, 180) &
            (df["fatalities"] >= 0)
        )
        valid_df = df[valid_mask].copy()

        # Assign quality flags
        # 0 = observed (precise coordinates), 1 = interpolated (centroid-coded)
        # ACLED uses "GEO_PRECISION" but we approximate: if coordinates are
        # exact integers, likely centroid-coded
        valid_df["quality_flag"] = np.where(
            (valid_df["latitude"] % 1 == 0) & (valid_df["longitude"] % 1 == 0),
            1,  # Likely admin-unit centroid
            0   # Precise coordinate
        )
        valid_df["quality_composite"] = np.where(
            valid_df["quality_flag"] == 0, 0.9, 0.6
        )

        report = ValidationReport(
            total_rows=len(df),
            valid_rows=len(valid_df),
            invalid_rows=len(df) - len(valid_df),
            null_counts={"latitude": int(null_lat), "longitude": int(null_lon)},
            out_of_range={"latitude": int(out_of_range_lat),
                          "longitude": int(out_of_range_lon)},
            warnings=warnings,
            errors=errors,
            quality_mean=float(valid_df["quality_composite"].mean()),
        )

        return pa.Table.from_pandas(valid_df), report

    def transform(self, table: pa.Table) -> pa.Table:
        """Transform ACLED events to PRIO-GRID monthly aggregates.

        Point events -> grid cell aggregation:
        - Map each event to a PRIO-GRID cell ID via latlon_to_gid()
        - Aggregate by (gid, year, month) with SUM for counts and fatalities
        - Produce one row per (gid, year, month, variable) in long format
        """
        df = table.to_pandas()

        # Map events to grid cells
        df["gid"] = df.apply(
            lambda r: latlon_to_gid(r["latitude"], r["longitude"]),
            axis=1
        ).astype("int32")

        # Aggregate by grid cell and month
        agg = df.groupby(["gid", "year", "month"]).agg(
            event_count=("event_id_cnty", "count"),
            fatalities=("fatalities", "sum"),
            battle_count=("event_type", lambda x: (x == "Battles").sum()),
            protest_count=("event_type", lambda x: (x == "Protests").sum()),
            quality_composite=("quality_composite", "mean"),
        ).reset_index()

        # Pivot to long format
        records = []
        variable_map = {
            "acled_event_count": "event_count",
            "acled_fatalities": "fatalities",
            "acled_battle_count": "battle_count",
            "acled_protest_count": "protest_count",
        }
        for var_name, col_name in variable_map.items():
            var_df = agg[["gid", "year", "month", col_name, "quality_composite"]].copy()
            var_df = var_df.rename(columns={col_name: "value"})
            var_df["variable"] = var_name
            var_df["source_id"] = self.config.source_id
            var_df["quality_flag"] = 0  # Direct observation
            var_df["ingested_at"] = pd.Timestamp.utcnow()
            records.append(var_df)

        result = pd.concat(records, ignore_index=True)
        result = result[["gid", "year", "month", "variable", "value",
                         "source_id", "quality_flag", "quality_composite",
                         "ingested_at"]]

        return pa.Table.from_pandas(result)
```

---

## 28. Deployment Architecture

> **Checked:** March 2025

### 28.1 Development Environment

Local machine with DuckDB and Parquet files. No services to manage.

```
Developer laptop/desktop
├── Python venv with all dependencies
├── DuckDB (embedded, in-process)
├── data/processed/ (Parquet files on NVMe)
├── data/raw/ (downloaded source files)
├── Jupyter notebooks for exploration
└── FastAPI dev server (uvicorn --reload)
```

No Docker required for development. `python -m causal_atlas.ingest --source acled` runs adapters directly.

### 28.2 Staging: Single Hetzner Server with Docker Compose

**Target:** Hetzner AX102 (Ryzen 9 7950X3D, 128 GB DDR5 ECC, 2x 1.92 TB NVMe, ~$130/month).

```yaml
# docker-compose.yml
# Causal Atlas -- staging deployment

version: "3.9"

services:
  # ── Reverse Proxy ──────────────────────────────────────────
  nginx:
    image: nginx:1.27-alpine
    container_name: ca-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/www:/var/www/certbot:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - frontend_build:/usr/share/nginx/html:ro
    depends_on:
      - api
      - frontend
    restart: unless-stopped
    networks:
      - ca-network

  # ── SSL Certificate Management ─────────────────────────────
  certbot:
    image: certbot/certbot:latest
    container_name: ca-certbot
    volumes:
      - ./certbot/www:/var/www/certbot
      - ./certbot/conf:/etc/letsencrypt
    # Renew certificates every 12 hours
    entrypoint: >
      sh -c "trap exit TERM;
      while :; do
        certbot renew --webroot -w /var/www/certbot --quiet;
        sleep 43200;
      done"
    restart: unless-stopped

  # ── FastAPI Backend ────────────────────────────────────────
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: ca-api
    environment:
      - ACLED_API_KEY=${ACLED_API_KEY}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - DATA_DIR=/data
      - DUCKDB_MEMORY_LIMIT=32GB
      - DUCKDB_THREADS=8
      - LOG_LEVEL=info
    volumes:
      - parquet_data:/data:ro        # Read-only access to Parquet files
      - analysis_output:/data/analysis
    expose:
      - "8000"
    command: >
      uvicorn causal_atlas.api.main:app
        --host 0.0.0.0
        --port 8000
        --workers 4
        --loop uvloop
        --access-log
    restart: unless-stopped
    networks:
      - ca-network
    deploy:
      resources:
        limits:
          memory: 48G
        reservations:
          memory: 16G

  # ── React Frontend (build stage) ───────────────────────────
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: ca-frontend
    volumes:
      - frontend_build:/app/dist
    # Frontend is a build-only container; nginx serves the static files
    command: ["npm", "run", "build"]
    profiles:
      - build

  # ── Data Pipeline Scheduler ────────────────────────────────
  scheduler:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: ca-scheduler
    environment:
      - ACLED_API_KEY=${ACLED_API_KEY}
      - DATA_DIR=/data
      - LOG_LEVEL=info
    volumes:
      - parquet_data:/data            # Read-write access for ingestion
      - raw_data:/data/raw
    # Run as Dagster daemon or simple cron scheduler
    command: >
      python -m causal_atlas.scheduler
    restart: unless-stopped
    networks:
      - ca-network
    deploy:
      resources:
        limits:
          memory: 32G

  # ── Monitoring: Prometheus ─────────────────────────────────
  prometheus:
    image: prom/prometheus:v2.53.0
    container_name: ca-prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/alert_rules.yml:/etc/prometheus/alert_rules.yml:ro
      - prometheus_data:/prometheus
    expose:
      - "9090"
    restart: unless-stopped
    networks:
      - ca-network

  # ── Monitoring: Grafana ────────────────────────────────────
  grafana:
    image: grafana/grafana:11.4.0
    container_name: ca-grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-changeme}
      - GF_SERVER_ROOT_URL=https://atlas.example.com/grafana/
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
      - grafana_data:/var/lib/grafana
    expose:
      - "3000"
    restart: unless-stopped
    networks:
      - ca-network

  # ── Monitoring: Loki (log aggregation) ─────────────────────
  loki:
    image: grafana/loki:3.3.0
    container_name: ca-loki
    volumes:
      - ./monitoring/loki-config.yml:/etc/loki/local-config.yaml:ro
      - loki_data:/loki
    expose:
      - "3100"
    restart: unless-stopped
    networks:
      - ca-network

  # ── Node Exporter (system metrics) ─────────────────────────
  node-exporter:
    image: prom/node-exporter:v1.8.2
    container_name: ca-node-exporter
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
    expose:
      - "9100"
    restart: unless-stopped
    networks:
      - ca-network

volumes:
  parquet_data:
    driver: local
    driver_opts:
      type: none
      device: /data/processed
      o: bind
  raw_data:
    driver: local
    driver_opts:
      type: none
      device: /data/raw
      o: bind
  analysis_output:
    driver: local
    driver_opts:
      type: none
      device: /data/analysis
      o: bind
  frontend_build:
  prometheus_data:
  grafana_data:
  loki_data:

networks:
  ca-network:
    driver: bridge
```

### 28.3 Nginx Configuration

```nginx
# nginx/conf.d/causal-atlas.conf

upstream api_backend {
    server api:8000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name atlas.example.com;

    # ACME challenge for Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name atlas.example.com;

    # SSL certificates (managed by certbot)
    ssl_certificate /etc/letsencrypt/live/atlas.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/atlas.example.com/privkey.pem;

    # SSL hardening
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Frontend (React SPA)
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;

        # Cache static assets aggressively (hashed filenames)
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API proxy
    location /api/ {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for long-running queries
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;

        # Response caching for common queries
        proxy_cache_valid 200 5m;
    }

    # Grafana (monitoring dashboard)
    location /grafana/ {
        proxy_pass http://grafana:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    location /api/v1/interpret {
        limit_req zone=api_limit burst=5 nodelay;
        proxy_pass http://api_backend;
    }
}
```

### 28.4 Production: Hetzner Dedicated + Optional Cloud Burst

**Primary:** Hetzner AX162-S (EPYC 9454P 48C/96T, 128 GB DDR5 ECC, 2x NVMe, ~$200/month).

Production deployment uses the same Docker Compose structure as staging with these additions:

**Systemd service for Docker Compose:**

```ini
# /etc/systemd/system/causal-atlas.service
[Unit]
Description=Causal Atlas Application Stack
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/causal-atlas
EnvironmentFile=/opt/causal-atlas/.env
ExecStart=/usr/bin/docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker compose -f docker-compose.yml -f docker-compose.prod.yml down
ExecReload=/usr/bin/docker compose -f docker-compose.yml -f docker-compose.prod.yml restart
TimeoutStartSec=120

[Install]
WantedBy=multi-user.target
```

**Let's Encrypt initial setup:**

```bash
#!/bin/bash
# scripts/init-letsencrypt.sh
# Run once to obtain initial SSL certificates

DOMAIN="atlas.example.com"
EMAIL="admin@example.com"

# Start nginx with self-signed dummy cert
docker compose up -d nginx

# Obtain real certificate
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN"

# Reload nginx to use real cert
docker compose exec nginx nginx -s reload
```

### 28.5 Monitoring Stack: Prometheus + Grafana + Loki

**Prometheus scrape configuration:**

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]

  - job_name: "fastapi"
    static_configs:
      - targets: ["api:8000"]
    metrics_path: /metrics

  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

**Alert rules:**

```yaml
# monitoring/alert_rules.yml
groups:
  - name: causal_atlas
    rules:
      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/data"} / node_filesystem_size_bytes{mountpoint="/data"}) < 0.10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space below 10% on /data"

      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 0.90
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Memory usage above 90%"

      - alert: APIHighLatency
        expr: histogram_quantile(0.95, rate(ca_api_request_duration_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API P95 latency above 10 seconds"

      - alert: IngestionFailure
        expr: increase(ca_ingestion_errors_total[1h]) > 0
        labels:
          severity: warning
        annotations:
          summary: "Data ingestion errors detected"
```

### 28.6 Backup: Automated Parquet Snapshots to Backblaze B2

```bash
#!/bin/bash
# scripts/backup-to-b2.sh
# Automated daily backup of processed data to Backblaze B2
# Called by cron: 0 2 * * * /opt/causal-atlas/scripts/backup-to-b2.sh

set -euo pipefail

B2_REMOTE="b2-causal-atlas"       # rclone remote name
BUCKET="causal-atlas-backups"
DATA_DIR="/data/processed"
ANALYSIS_DIR="/data/analysis"
LOG_FILE="/var/log/causal-atlas/backup.log"

log() {
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') $*" >> "$LOG_FILE"
}

log "Backup started"

# Sync processed Parquet files (incremental -- only changed files)
rclone sync "$DATA_DIR" "${B2_REMOTE}:${BUCKET}/processed/" \
    --fast-list \
    --transfers 8 \
    --checkers 16 \
    --log-file "$LOG_FILE" \
    --log-level INFO \
    --stats 60s \
    --stats-one-line

# Sync analysis results (these are irreplaceable)
rclone sync "$ANALYSIS_DIR" "${B2_REMOTE}:${BUCKET}/analysis/" \
    --fast-list \
    --transfers 4 \
    --log-file "$LOG_FILE" \
    --log-level INFO

# Verify backup integrity (spot-check 5 random files)
rclone check "$DATA_DIR" "${B2_REMOTE}:${BUCKET}/processed/" \
    --one-way \
    --size-only \
    --log-file "$LOG_FILE" \
    2>&1 | tail -1 >> "$LOG_FILE"

log "Backup completed"

# Alert on failure
if [ $? -ne 0 ]; then
    curl -X POST "$SLACK_WEBHOOK_URL" \
        -H 'Content-type: application/json' \
        -d '{"text":"Causal Atlas backup FAILED. Check /var/log/causal-atlas/backup.log"}'
fi
```

---

## 29. Data Pipeline Scheduling

> **Checked:** March 2025

### 29.1 Adapter Schedule

| Adapter | Schedule | Mode | Dependencies | Typical Duration | Data Volume |
|---------|----------|------|-------------|-----------------|-------------|
| ACLED | Weekly (Monday 02:00 UTC) | Incremental | None | 5-15 min | 5-50 MB |
| CHIRPS | Monthly (1st, 03:00 UTC) | Full month | None | 30-60 min | 500 MB - 2 GB |
| WFP food prices | Weekly (Monday 04:00 UTC) | Incremental | None | 2-5 min | 1-10 MB |
| USGS earthquakes | Daily (05:00 UTC) | Incremental | None | 1-3 min | 1-5 MB |
| OpenAQ | Daily (06:00 UTC) | Incremental | None | 10-30 min | 50-200 MB |
| MODIS/VIIRS NDVI | Monthly (5th, 04:00 UTC) | Full composite | None | 60-120 min | 1-3 GB |
| VIIRS nightlights | Monthly (10th, 04:00 UTC) | Full composite | None | 30-60 min | 500 MB - 1 GB |
| UCDP GED | Annual (February) | Full refresh | None | 5-10 min | 100-300 MB |
| World Bank | Annual (April) | Full refresh | None | 10-30 min | 50-200 MB |
| FAO | Annual (March) | Full refresh | None | 10-30 min | 100-500 MB |
| EM-DAT | Monthly (1st, 05:00 UTC) | Full refresh | None | 2-5 min | 10-50 MB |
| HDX HAPI | Weekly (Wednesday 03:00 UTC) | Incremental | None | 5-15 min | 10-50 MB |
| **Integration** | After any adapter | Merge | Upstream adapter | 5-15 min | -- |
| **Correlation scan** | After integration | Analysis | Integration | 10-60 min | -- |
| **Interpretation** | After correlation | Claude API | Correlation scan | 1-5 min | -- |

### 29.2 Dependency Graph

```
                    ┌─────────┐
                    │  ACLED   │──┐
                    └─────────┘  │
                    ┌─────────┐  │
                    │  CHIRPS  │──┤
                    └─────────┘  │
                    ┌─────────┐  │     ┌──────────────┐     ┌────────────────┐
                    │   WFP   │──┼────>│  Integration │────>│  Correlation   │
                    └─────────┘  │     │  (merge all  │     │  Scan          │
                    ┌─────────┐  │     │   domains)   │     │  (updated      │
                    │  USGS   │──┤     └──────────────┘     │   cells only)  │
                    └─────────┘  │                          └───────┬────────┘
                    ┌─────────┐  │                                  │
                    │ OpenAQ  │──┤                                  ▼
                    └─────────┘  │                          ┌────────────────┐
                    ┌─────────┐  │                          │  Claude API    │
                    │  NDVI   │──┤                          │  Interpretation│
                    └─────────┘  │                          └───────┬────────┘
                    ┌─────────┐  │                                  │
                    │Nightlts │──┘                                  ▼
                    └─────────┘                             ┌────────────────┐
                                                            │  Notify        │
                                                            │  (email/Slack) │
                                                            └────────────────┘
```

**Key design decisions:**

- Each source adapter is independent -- no adapter depends on another adapter's output
- The integration step depends on ALL adapters having current data, but runs after any single adapter updates
- Correlation scans are incremental -- they only re-analyse grid cells and time periods affected by the new data
- Claude interpretation is triggered only for NEW significant findings (not previously seen correlations)

### 29.3 Failure Handling and Retries

| Failure Type | Behaviour | Retry Policy | Alert |
|-------------|-----------|-------------|-------|
| Network timeout | Retry with exponential backoff | 3 retries, max 5 min wait | Alert after all retries exhausted |
| HTTP 429 (rate limit) | Wait for Retry-After header, then retry | Honour server directive | Alert if blocked > 1 hour |
| HTTP 5xx (server error) | Retry with backoff | 3 retries | Alert after all retries exhausted |
| HTTP 401/403 (auth) | Do NOT retry | Immediate failure | Alert immediately -- API key issue |
| Parse error | Do NOT retry | Immediate failure | Alert with sample of malformed data |
| Validation > 50% invalid | Do NOT retry | Immediate failure | Alert with validation report |
| Disk full | Do NOT retry | Immediate failure | Critical alert -- requires human intervention |
| Integration failure | Retry once | 1 retry after 5 min | Alert with error details |
| Claude API error | Queue for batch | Retry via Batch API | No alert (graceful degradation) |

**Dead letter queue:** Records that fail validation are written to `data/dead_letter/{source_id}/{date}/` as Parquet files with the original data plus the failure reason. These are reviewed manually and either fixed and re-ingested or permanently discarded.

### 29.4 Alert Routing

```yaml
# monitoring/alertmanager.yml (for Prometheus Alertmanager integration)
# Alternatively, implement in Python with structlog + webhook

route:
  receiver: "default"
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: "critical-alerts"
    - match:
        severity: warning
      receiver: "warning-alerts"

receivers:
  - name: "default"
    email_configs:
      - to: "admin@example.com"
        from: "alerts@causal-atlas.org"

  - name: "critical-alerts"
    email_configs:
      - to: "admin@example.com"
    slack_configs:
      - api_url: "${SLACK_WEBHOOK_URL}"
        channel: "#causal-atlas-alerts"
        title: "CRITICAL: {{ .CommonAnnotations.summary }}"
        text: "{{ .CommonAnnotations.description }}"

  - name: "warning-alerts"
    slack_configs:
      - api_url: "${SLACK_WEBHOOK_URL}"
        channel: "#causal-atlas-alerts"
        title: "WARNING: {{ .CommonAnnotations.summary }}"
```

### 29.5 Dagster Asset Dependency Graph

When graduating from cron to Dagster (Phase 2, 5+ adapters):

```python
from dagster import (
    asset, AssetIn, MonthlyPartitionsDefinition,
    WeeklyPartitionsDefinition, DailyPartitionsDefinition,
    AutoMaterializePolicy, FreshnessPolicy,
    define_asset_job, ScheduleDefinition, Definitions
)
from datetime import datetime

# ── Partition Definitions ────────────────────────────────────

monthly = MonthlyPartitionsDefinition(start_date="2015-01-01")
weekly = WeeklyPartitionsDefinition(start_date="2020-01-06")
daily = DailyPartitionsDefinition(start_date="2020-01-01")


# ── Source Assets (independent) ──────────────────────────────

@asset(
    partitions_def=weekly,
    group_name="conflict",
    description="ACLED conflict events aggregated to PRIO-GRID cells",
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=7 * 24 * 60),  # 1 week
)
def acled_grid(context):
    """Fetch and process ACLED data for the given week."""
    partition_key = context.partition_key
    adapter = get_adapter("acled", output_dir=Path("/data/processed"),
                          domain="conflict")
    start, end = week_bounds(partition_key)
    return adapter.run(start, end)


@asset(
    partitions_def=monthly,
    group_name="climate",
    description="CHIRPS monthly precipitation aggregated to PRIO-GRID",
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=60 * 24 * 60),  # 60 days
)
def chirps_grid(context):
    partition_key = context.partition_key
    adapter = get_adapter("chirps", output_dir=Path("/data/processed"),
                          domain="climate")
    start, end = month_bounds(partition_key)
    return adapter.run(start, end)


@asset(
    partitions_def=weekly,
    group_name="food_security",
    description="WFP food prices aggregated to PRIO-GRID cells",
)
def wfp_prices_grid(context):
    partition_key = context.partition_key
    adapter = get_adapter("wfp", output_dir=Path("/data/processed"),
                          domain="food_security")
    start, end = week_bounds(partition_key)
    return adapter.run(start, end)


@asset(
    partitions_def=daily,
    group_name="natural_hazards",
    description="USGS earthquake data aggregated to PRIO-GRID cells",
)
def usgs_earthquakes_grid(context):
    partition_key = context.partition_key
    adapter = get_adapter("usgs", output_dir=Path("/data/processed"),
                          domain="natural_hazards")
    return adapter.run(
        date.fromisoformat(partition_key),
        date.fromisoformat(partition_key),
    )


# ── Derived Assets (depend on sources) ───────────────────────

@asset(
    ins={
        "acled": AssetIn("acled_grid"),
        "chirps": AssetIn("chirps_grid"),
        "wfp": AssetIn("wfp_prices_grid"),
    },
    partitions_def=monthly,
    group_name="integrated",
    description="Integrated multi-domain dataset for analysis",
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def integrated_monthly(context, acled, chirps, wfp):
    """Join conflict, climate, and food security data for a given month."""
    import duckdb
    con = duckdb.connect()
    month = context.partition_key
    result = con.execute(f"""
        SELECT * FROM read_parquet('data/processed/domain=*/year={month[:4]}/*.parquet',
                                    hive_partitioning=true)
        WHERE month = {int(month[5:7])}
    """).arrow()
    return result


@asset(
    ins={"integrated": AssetIn("integrated_monthly")},
    partitions_def=monthly,
    group_name="analysis",
    description="Correlation scan on updated data",
)
def correlation_scan(context, integrated):
    """Run lag correlation analysis on newly integrated data."""
    from causal_atlas.analysis import scan_correlations
    month = context.partition_key
    results = scan_correlations(month, max_lag=12)
    context.log.info(f"Found {len(results)} significant correlations")
    return results


@asset(
    ins={"correlations": AssetIn("correlation_scan")},
    partitions_def=monthly,
    group_name="analysis",
    description="AI interpretation of significant new correlations",
)
def interpreted_findings(context, correlations):
    """Generate Claude interpretations for new significant findings."""
    from causal_atlas.ai import batch_interpret
    new_findings = filter_new_findings(correlations)
    if new_findings:
        interpretations = batch_interpret(new_findings)
        context.log.info(f"Interpreted {len(interpretations)} new findings")
        return interpretations
    return []


# ── Schedules ────────────────────────────────────────────────

acled_schedule = ScheduleDefinition(
    name="weekly_acled",
    target=define_asset_job("acled_job", selection=[acled_grid]),
    cron_schedule="0 2 * * 1",  # Monday 02:00 UTC
)

chirps_schedule = ScheduleDefinition(
    name="monthly_chirps",
    target=define_asset_job("chirps_job", selection=[chirps_grid]),
    cron_schedule="0 3 1 * *",  # 1st of month, 03:00 UTC
)

# ── Definitions (entry point) ────────────────────────────────

defs = Definitions(
    assets=[acled_grid, chirps_grid, wfp_prices_grid, usgs_earthquakes_grid,
            integrated_monthly, correlation_scan, interpreted_findings],
    schedules=[acled_schedule, chirps_schedule],
)
```

---

## 30. Claude API Integration -- Detailed Design

> **Checked:** March 2025

### 30.1 Prompt Engineering for Causal Interpretation

**System prompt template (cached -- reused across all interpretation requests):**

```python
SYSTEM_PROMPT = """You are a research analyst for the Causal Atlas platform,
specialising in cross-domain spatiotemporal analysis. Your expertise covers
conflict dynamics, climate science, food security, public health, economics,
and environmental monitoring.

## Your Role
You interpret statistical correlation and causal analysis results in the
context of specific geographic regions and time periods. You provide
scientifically grounded explanations that are useful to humanitarian
researchers and policy analysts.

## Guidelines
1. ALWAYS ground your interpretation in the specific data provided. Do not
   invent statistics or fabricate details not present in the input.
2. Reference established academic research where relevant. Cite specific
   authors and years (e.g., "Raleigh et al., 2015" or "Burke et al., 2009").
   Only cite research you are confident exists.
3. Distinguish clearly between correlation and causation. Use language like
   "this correlation is consistent with..." rather than "X causes Y."
4. Assess whether the observed lag structure is mechanistically plausible.
   A 3-month lag between rainfall deficit and conflict is plausible via
   food price transmission; a 1-day lag is not.
5. Identify at least one plausible confounder that could produce the
   observed correlation without a direct causal link.
6. Rate your confidence as HIGH, MEDIUM, or LOW based on:
   - HIGH: Strong statistical evidence (p < 0.001, |r| > 0.5), well-documented
     mechanism in literature, plausible lag structure
   - MEDIUM: Moderate evidence (p < 0.01, |r| > 0.3), plausible mechanism
     but less documented, or possible confounders
   - LOW: Weak evidence (p > 0.01 or |r| < 0.3), speculative mechanism,
     or likely confounders
7. Be concise. 300-500 words maximum per interpretation.
8. If the data quality score is below 0.5, prominently note that the
   results should be treated with additional caution.
"""
```

**Few-shot examples for interpreting correlation results:**

```python
FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": """## Data Context
- Region: Turkana County, Kenya (KEN)
- Grid cells analysed: 12
- Time period: 2015-01 to 2023-12
- Variable A: chirps_precip_mm (Monthly precipitation in mm, CHIRPS v2.0)
- Variable B: acled_fatalities (Monthly conflict fatalities, ACLED v24)

## Statistical Results
- Pearson correlation: -0.42
- P-value: 0.000003
- Optimal lag: 3 months (A leads B by 3 months)
- 95% CI: [-0.56, -0.27]
- N observations: 108
- Data quality (mean composite): 0.82"""
    },
    {
        "role": "assistant",
        "content": """{
  "summary": "Rainfall deficits in Turkana County precede increases in conflict fatalities by approximately 3 months, a pattern consistent with the well-documented climate-food-conflict pathway in pastoral regions of East Africa.",
  "mechanism": "Turkana is a predominantly pastoral region where livelihoods depend directly on rainfall for livestock grazing. Below-average rainfall reduces pasture and water availability, intensifying competition between pastoral groups for remaining resources. This resource competition, combined with livelihood stress and potential food price increases, can escalate into violent conflict. The 3-month lag is mechanistically plausible: it takes approximately one season for drought conditions to deplete available resources and for inter-group tensions to escalate.",
  "academic_references": [
    "Raleigh, C. & Kniveton, D. (2012). Come rain or shine: An analysis of conflict and climate variability in East Africa. Journal of Peace Research.",
    "Schilling, J. et al. (2012). Raiding pastoral livelihoods: motives and effects of violent conflict in north-western Kenya. Pastoralism: Research, Policy and Practice.",
    "Theisen, O.M. (2012). Climate clashes? Weather variability, land pressure, and organized violence in Kenya. Journal of Peace Research."
  ],
  "confounders": [
    "Seasonal patterns: Both rainfall and conflict may follow seasonal cycles without direct causal connection",
    "Market dynamics: Food price changes driven by regional/global supply may co-occur with local rainfall deficits",
    "Political events: Elections or policy changes may independently drive both livestock movements and conflict"
  ],
  "lag_assessment": "The 3-month lag is highly plausible for this region and mechanism. It aligns with the typical timescale for drought impacts to propagate through pastoral livelihoods to resource competition. Shorter lags (0-1 months) would be implausible for this mechanism; longer lags (6+ months) would be less consistent with direct resource competition but might reflect food price transmission.",
  "confidence": "MEDIUM",
  "follow_up": [
    "Mediation analysis: test whether WFP food prices mediate the rainfall-conflict relationship",
    "Granger causality test to assess temporal precedence more rigorously",
    "Compare with adjacent counties (Marsabit, Samburu) to assess spatial consistency",
    "Check if the relationship weakens or disappears during periods of humanitarian food aid"
  ]
}"""
    }
]
```

**Structured output schema (Pydantic):**

```python
from pydantic import BaseModel, Field
from typing import Literal


class CorrelationInterpretation(BaseModel):
    """Schema for Claude's interpretation of a correlation result.

    Used with Claude's structured output mode to guarantee parseable JSON.
    """
    summary: str = Field(
        ...,
        description="1-2 sentence headline summarising the finding",
        max_length=500
    )
    mechanism: str = Field(
        ...,
        description="Plausible causal pathway explaining the correlation",
        max_length=2000
    )
    academic_references: list[str] = Field(
        ...,
        description="Published research supporting the interpretation (author, year, journal)",
        min_length=1,
        max_length=5
    )
    confounders: list[str] = Field(
        ...,
        description="Variables that could produce a spurious correlation",
        min_length=1,
        max_length=5
    )
    lag_assessment: str = Field(
        ...,
        description="Whether the lag structure is mechanistically plausible",
        max_length=1000
    )
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(
        ...,
        description="Confidence level based on evidence strength"
    )
    follow_up: list[str] = Field(
        ...,
        description="Suggested next analyses to strengthen or weaken the claim",
        min_length=1,
        max_length=5
    )


class NaturalLanguageQuery(BaseModel):
    """Schema for parsing a natural language question into a structured query."""
    intent: Literal["correlation", "timeseries", "comparison", "explanation", "prediction"]
    variables: list[str] = Field(
        ..., description="Variable names referenced (e.g., ['chirps_precip_mm', 'acled_fatalities'])"
    )
    region: str | None = Field(
        None, description="Geographic region (country name, ISO3 code, or 'global')"
    )
    time_range: tuple[str, str] | None = Field(
        None, description="Start and end dates as YYYY-MM strings"
    )
    lag_months: int | None = Field(
        None, description="Specific lag to test, if mentioned"
    )
    sql_query: str = Field(
        ..., description="DuckDB SQL query to retrieve the needed data"
    )


class HypothesisGeneration(BaseModel):
    """Schema for automated hypothesis generation from significant findings."""
    hypothesis: str = Field(..., description="Formal hypothesis statement")
    mechanism: str = Field(..., description="Proposed causal mechanism")
    required_evidence: list[str] = Field(
        ..., description="What additional evidence would confirm or reject this hypothesis"
    )
    confidence_level: Literal["HIGH", "MEDIUM", "LOW"]
    related_literature: list[str]
    suggested_methods: list[str] = Field(
        ..., description="Statistical methods to test the hypothesis"
    )
```

### 30.2 Handling Hallucination: Grounding in Data

Claude's interpretations must be grounded in the actual data. Strategies:

1. **Data-first prompting:** Always include the exact statistical results in the prompt. Never ask Claude to "estimate" or "guess" values.

2. **Citation verification:** After receiving Claude's response, cross-reference cited papers against a known bibliography database. Flag citations that do not appear in the database as "unverified."

3. **Confidence calibration:** Automatically downgrade confidence if:
   - p-value > 0.01 and Claude says HIGH
   - Sample size < 50 and Claude says HIGH
   - Data quality < 0.5

4. **Output validation:**

```python
def validate_interpretation(result: CorrelationInterpretation,
                           stats: dict) -> CorrelationInterpretation:
    """Post-process Claude's interpretation to ensure grounding."""
    # Force confidence downgrade if statistics are weak
    if stats["p_value"] > 0.01 and result.confidence == "HIGH":
        result.confidence = "MEDIUM"
    if stats["p_value"] > 0.05:
        result.confidence = "LOW"
    if abs(stats["r_value"]) < 0.3 and result.confidence == "HIGH":
        result.confidence = "MEDIUM"

    # Prepend data quality warning if needed
    if stats["quality_mean"] < 0.5:
        result.summary = (
            "[DATA QUALITY WARNING: Mean quality score is below 0.5. "
            "Interpret with caution.] " + result.summary
        )

    return result
```

### 30.3 Natural Language Query Interface

The full query pipeline: user question -> Claude parsing -> SQL generation -> DuckDB execution -> Claude narrative response.

```python
async def handle_natural_language_query(question: str, user_tier: str) -> dict:
    """Process a natural language question about causal relationships.

    Example: "What caused the spike in food prices in South Sudan in March 2023?"

    Pipeline:
    1. Parse question with Haiku (fast, cheap) -> structured query
    2. Generate DuckDB SQL from structured query
    3. Execute SQL against Parquet data
    4. Generate narrative answer with Sonnet (higher quality)
    """
    # Step 1: Parse with Haiku
    parse_response = await client.messages.create(
        model="claude-haiku-4-5-20241022",
        max_tokens=512,
        system=NL_QUERY_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"""Parse this question into a structured query.

Available variables: {VARIABLE_CATALOGUE}
Available regions: {REGION_LIST}

Question: {question}"""}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "query",
                "schema": NaturalLanguageQuery.model_json_schema()
            }
        }
    )
    query = NaturalLanguageQuery.model_validate_json(
        parse_response.content[0].text
    )

    # Step 2: Validate and sanitise SQL (prevent injection)
    safe_sql = sanitise_duckdb_query(query.sql_query)

    # Step 3: Execute against DuckDB
    import duckdb
    con = duckdb.connect(read_only=True)
    try:
        result = con.execute(safe_sql).fetchdf()
    except Exception as e:
        return {"error": f"Query failed: {e}", "sql": safe_sql}
    finally:
        con.close()

    # Step 4: Generate narrative with Sonnet
    narrative_response = await client.messages.create(
        model="claude-sonnet-4-5-20241022",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            *FEW_SHOT_EXAMPLES,
            {"role": "user", "content": f"""The user asked: "{question}"

Here is the data retrieved from our database:

{result.to_markdown()}

Provide a clear, data-grounded answer to the user's question.
Reference the specific numbers from the data.
If the data is insufficient to answer the question, say so clearly."""}
        ]
    )

    return {
        "question": question,
        "parsed_query": query.model_dump(),
        "sql": safe_sql,
        "data_summary": result.describe().to_dict(),
        "answer": narrative_response.content[0].text,
        "model": "claude-sonnet-4-5",
    }
```

### 30.4 Cost Optimisation

| Strategy | Savings | Implementation |
|----------|---------|---------------|
| **Prompt caching** (system prompt > 1024 tokens) | 90% on cached portion | System prompt is ~800 tokens; add variable catalogue to push over 1024 |
| **Batch API** for pattern scanning | 50% off per-token rates | Queue scan results, submit as batch, retrieve within 1 hour |
| **Model tiering** | 60-80% vs using Opus for everything | Haiku for parsing/routing, Sonnet for narrative, Opus only for hypothesis |
| **Result caching** | Eliminates repeat API calls | Cache interpretation by hash(var_a, var_b, region, lag, r_value rounded to 2dp) |
| **Deduplication** | Variable | Skip interpretation if a near-identical finding already exists |

**Monthly cost projection (1,000 correlation interpretations/month):**

```
Correlation interpretation (Sonnet):
  Input:  1000 req x 1300 tokens x $3.00/M  = $3.90
  Output: 1000 req x 500 tokens  x $15.00/M = $7.50
  With prompt caching (90% of 800 system tokens):
    Cached input savings: 1000 x 800 x $3.00/M x 0.9 = -$2.16
  Subtotal: ~$9.24

NL queries (Haiku parse + Sonnet respond):
  Parse:  500 req x 700 tokens x $1.00/M + 500 x 300 x $5.00/M = $1.10
  Respond: 500 req x 1500 tokens x $3.00/M + 500 x 600 x $15.00/M = $6.75
  Subtotal: ~$7.85

Pattern scanning (Haiku batch, monthly):
  5000 findings x 600 tokens x $0.50/M + 5000 x 300 x $2.50/M = $5.25

Total estimated monthly: ~$22/month
```

### 30.5 Prompt Versioning and A/B Testing

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PromptVersion:
    id: str                    # e.g., "interpret_v3"
    version: int               # Incremental version number
    system_prompt: str
    few_shot_examples: list
    model: str
    temperature: float
    created_at: datetime
    description: str           # What changed in this version
    active: bool = True


# Prompt registry (stored in DuckDB or JSON)
PROMPT_VERSIONS = {
    "interpret_v1": PromptVersion(
        id="interpret_v1", version=1,
        system_prompt=SYSTEM_PROMPT_V1,
        few_shot_examples=[],
        model="claude-sonnet-4-5-20241022",
        temperature=0.3,
        created_at=datetime(2025, 3, 1),
        description="Initial prompt, no few-shot examples",
        active=False,
    ),
    "interpret_v2": PromptVersion(
        id="interpret_v2", version=2,
        system_prompt=SYSTEM_PROMPT_V2,
        few_shot_examples=FEW_SHOT_EXAMPLES,
        model="claude-sonnet-4-5-20241022",
        temperature=0.2,
        created_at=datetime(2025, 3, 15),
        description="Added few-shot examples and structured output",
        active=True,
    ),
}


async def interpret_with_ab_test(correlation_data: dict) -> dict:
    """Run interpretation with A/B testing between prompt versions.

    10% of requests go to the challenger version for evaluation.
    Results are logged for offline comparison.
    """
    import random
    active_versions = [v for v in PROMPT_VERSIONS.values() if v.active]
    if len(active_versions) > 1 and random.random() < 0.10:
        version = active_versions[1]  # Challenger
    else:
        version = active_versions[0]  # Champion

    result = await interpret_correlation(correlation_data, version)
    result["prompt_version"] = version.id

    # Log for offline evaluation
    logger.info("interpretation_generated",
                prompt_version=version.id,
                confidence=result.get("confidence"),
                model=version.model)

    return result
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

### Deployment Architecture (Sections 26-30)
- [Hetzner AX102 Dedicated Server](https://www.hetzner.com/dedicated-rootserver/ax102) -- AMD Ryzen 9 7950X3D, 128 GB DDR5 ECC
- [Hetzner Docker CE](https://docs.hetzner.com/cloud/apps/list/docker-ce/) -- Docker installation on Hetzner servers
- [nginx-certbot Docker Compose (GitHub)](https://github.com/wmnnd/nginx-certbot) -- Boilerplate nginx + Let's Encrypt setup
- [Let's Encrypt Docker Compose (GitHub)](https://github.com/eugene-khyst/letsencrypt-docker-compose) -- Automated SSL with Docker
- [Grafana Loki Docker Compose](https://grafana.com/docs/loki/latest/setup/install/docker/) -- Log aggregation setup
- [Prometheus + Grafana + Loki Stack](https://github.com/maiobarbero/grafana-prometheus-loki) -- Production-ready monitoring
- [Backblaze B2 + rclone Integration](https://rclone.org/b2/) -- Cloud backup with rclone
- [Backblaze B2 rclone Quickstart](https://help.backblaze.com/hc/en-us/articles/1260804565710-Quickstart-Guide-for-Rclone-and-B2-Cloud-Storage) -- Setup guide
- [Dagster Declarative Scheduling](https://medium.com/@dagster-io/declarative-scheduling-for-data-assets-a-breakthrough-in-data-orchestration-85bd5fa6d707) -- Asset-based scheduling
- [Dagster Automations in Practice (FreeAgent)](https://engineering.freeagent.com/2025/12/10/how-we-use-dagster-automations-in-our-data-pipeline/) -- Real-world Dagster usage
- [Dagster Asset Documentation](https://docs.dagster.io/examples/full-pipelines/etl-pipeline/automate-your-pipeline) -- Pipeline automation guide
- [ACLED API Documentation](https://apidocs.acleddata.com/) -- REST API for conflict data
- [Tigramite (GitHub)](https://github.com/jakobrunge/tigramite) -- PCMCI causal discovery library
- [Cloudflare Free Plan](https://www.cloudflare.com/plans/free/) -- CDN and DDoS protection
- [Cloudflare DDoS Best Practices](https://developers.cloudflare.com/ddos-protection/best-practices/) -- Protection configuration
