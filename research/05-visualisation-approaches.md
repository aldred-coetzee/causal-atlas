# 05 — Visualisation Approaches for Multi-Layer Spatiotemporal Data

> **Last updated:** March 2025
> **Status:** Deep research — comprehensive review of tools, techniques, and recommendations for Causal Atlas

---

## Table of Contents

1. [Kepler.gl](#1-keplergl)
2. [deck.gl](#2-deckgl)
3. [HungerMapLIVE](#3-hungermaplive)
4. [ACLED Dashboard](#4-acled-dashboard)
5. [GDELT Analysis Tools](#5-gdelt-analysis-tools)
6. [Mapbox GL JS and MapLibre GL JS](#6-mapbox-gl-js-and-maplibre-gl-js)
7. [Leaflet / Folium](#7-leaflet--folium)
8. [Plotly / Dash](#8-plotly--dash)
9. [Felt](#9-felt)
10. [Observable / D3.js](#10-observable--d3js)
11. [DuckDB + Kepler.gl v3.1 Integration](#11-duckdb--keplergl-v31-integration)
12. [Visualisation Techniques for Causal Discovery](#12-visualisation-techniques-for-causal-discovery)
13. [Tool Comparison Table](#13-tool-comparison-table)
14. [Recommended Approach for Causal Atlas](#14-recommended-approach-for-causal-atlas)

---

## 1. Kepler.gl

**Repository:** https://github.com/keplergl/kepler.gl
**Docs:** https://docs.kepler.gl/
**Licence:** MIT
**Maintained by:** Foursquare (formerly Uber Visualization)
**Current version:** v3.1.x (as of March 2025)

### 1.1 Overview

Kepler.gl is a high-performance, open-source geospatial analysis tool for large-scale datasets. Originally developed by Uber's visualization team, it is now maintained by Foursquare. It is built on top of deck.gl and MapLibre GL JS, rendering layers via WebGL2 for GPU-accelerated performance.

### 1.2 Supported Layer Types

Kepler.gl v3.x supports the following layer types:

| Layer Type | Description | Relevance to Causal Atlas |
|---|---|---|
| **Point** | Individual point markers with size/colour encoding | Event data (conflicts, earthquakes, disease outbreaks) |
| **Arc** | Curved lines connecting two locations | Causal connections between regions, migration flows |
| **Line** | Straight lines between two points | Simpler origin-destination connections |
| **Hexbin** | Hexagonal spatial aggregation with metrics (count, avg, sum, median, min, max) | Spatial density of events, aligns with H3 indexing |
| **Grid** | Rectangular grid aggregation | PRIO-GRID compatible density views |
| **Heatmap** | Continuous intensity surface from point data | Showing hotspots of activity |
| **Cluster** | Dynamic point clustering by geospatial radius | Overview of event concentrations |
| **H3** | Uber's hexagonal hierarchical spatial index | High-performance spatial aggregation at multiple resolutions |
| **S2** | Google's S2 spherical geometry cells | Alternative spatial indexing |
| **Trip** | Animated trajectories along paths with timestamps | Temporal movement patterns |
| **Polygon** | GeoJSON polygon rendering with fill/stroke | Administrative boundaries, choropleth maps |
| **Icon** | Custom icon markers | Categorical event types |
| **Vector Tile** | Tiled vector data for large polygon datasets | Efficient rendering of boundary layers |
| **Raster Tile** | Satellite/aerial imagery tiles | Contextual base layers (NDVI, nightlights) |
| **WMS** | Web Map Service layer integration | Connecting to OGC-compatible data services |

Source: https://docs.kepler.gl/docs/user-guides/c-types-of-layers

### 1.3 Temporal Capabilities

Kepler.gl has built-in time playback for any dataset with a timestamp column:

- **Time filter:** Add a filter on a datetime field to get a playback control at the bottom of the map. A distribution histogram shows data density across the time range.
- **Playback controls:** Play/pause, adjustable speed (1x, 2x, 4x), draggable time window.
- **Rolling time window:** A white slider controls the span of time visible on the map. Dates in the active window are highlighted; others are greyed out.
- **Y-axis selection:** The distribution graph can be switched from default (point count) to a timeseries of any numeric column.
- **Trip layer animation:** The Trip layer animates paths with configurable trail length (fade-out duration in seconds) and animation speed.

**Limitation:** The time filter operates on a single time field per filter. Synchronising multiple layers with different temporal resolutions (e.g., daily conflict events + monthly food prices) requires workarounds. There is an open issue (GitHub #743) requesting better multi-layer temporal synchronisation.

Source: https://docs.kepler.gl/docs/user-guides/h-playback

### 1.4 Embedding in React Applications

Kepler.gl is a React component that uses Redux for state management:

```bash
npm install kepler.gl @kepler.gl/components @kepler.gl/reducers
```

**Requirements:**
- Node 18.18.2+
- Redux store with kepler.gl reducer mounted
- react-palm middleware for side effects
- Mapbox/MapLibre access token for base map tiles

**Key integration points:**
- `KeplerGl` component accepts props for `id`, `mapboxApiAccessToken`, `width`, `height`
- `addDataToMap` action dispatches dataset(s) and full configuration (mapState, mapStyle, visState)
- Multiple KeplerGl instances can coexist with unique IDs
- Configuration is serialisable as JSON — maps can be saved and restored

**Customisation:** The component is modular. Individual sub-components (map container, side panel, modal) can be replaced or extended via a factory pattern. Custom reducers can be injected to extend state management.

Source: https://docs.kepler.gl/docs/api-reference/get-started

### 1.5 Performance with Large Datasets

**Strengths:**
- GPU-accelerated rendering via deck.gl/WebGL2 — can render millions of points
- Spatial aggregation layers (hexbin, grid, H3) handle large point clouds efficiently
- DuckDB integration (v3.1) offloads data processing from main thread

**Limitations:**
- **Browser memory cap:** Chrome enforces ~250MB upload limit for direct file loading. Datasets larger than 250MB must be loaded from a remote URL or via DuckDB/GeoParquet.
- **CPU filtering bottleneck:** Time playback and filtering on large datasets still rely on CPU processing for domain calculations, causing lag during scrubbing. This is the most significant performance issue for temporal analysis.
- **Layer stacking:** No hard limit on layers, but rendering performance degrades with many simultaneous layers.
- **No server-side rendering:** All processing happens in-browser. For datasets exceeding browser memory, pre-aggregation or tiling is required.

Source: https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/i-FAQ.md

### 1.6 Relevance to Causal Atlas

Kepler.gl is a strong candidate for the primary map visualisation component. Its layer variety, temporal playback, DuckDB integration, and React embedding make it the most feature-complete option for our use case. The main gaps are: (a) no built-in brushing-and-linking with external charts, (b) limited multi-variable temporal synchronisation, and (c) CPU filtering performance on large time-filtered datasets.

---

## 2. deck.gl

**Repository:** https://github.com/visgl/deck.gl
**Docs:** https://deck.gl/docs
**Licence:** MIT
**Current version:** v9.2.x (as of March 2025)

### 2.1 Overview

deck.gl is the rendering engine underlying Kepler.gl. It is a WebGL2/WebGPU-powered framework for large-scale data visualisation, designed for high-performance rendering of millions of data points. Where Kepler.gl is a turnkey application, deck.gl is the library you would use if you need full programmatic control.

### 2.2 Architecture

- **Layer-based compositing:** Layers are declarative — you describe what to render, and deck.gl handles the GPU pipeline.
- **Immutable data model:** Data updates trigger efficient diff-based re-renders.
- **WebGPU support:** v9.x added experimental WebGPU support via luma.gl v9, future-proofing for next-gen browser graphics.
- **View system:** Supports multiple synchronised views (MapView, OrthographicView, FirstPersonView).

### 2.3 Relevant Layer Catalog

deck.gl organises layers into categories:

**Core Layers:**

| Layer | Use Case for Causal Atlas |
|---|---|
| `ScatterplotLayer` | Point events (conflict, earthquakes, disease outbreaks) |
| `ArcLayer` | Causal connections between regions, migration arcs |
| `LineLayer` | Direct connections, simple flow lines |
| `PathLayer` | Routes, trajectories |
| `PolygonLayer` | Administrative boundaries, PRIO-GRID cells |
| `SolidPolygonLayer` | Filled polygons for choropleth |
| `TextLayer` | Labels, annotations |
| `IconLayer` | Categorical markers |
| `ColumnLayer` | 3D bar charts on map (e.g., event count per grid cell) |

**Aggregation Layers:**

| Layer | Use Case |
|---|---|
| `HexagonLayer` | Spatial binning of events |
| `GridLayer` | PRIO-GRID-compatible rectangular aggregation |
| `HeatmapLayer` | Continuous density surface |
| `ContourLayer` | Isolines/isobands for density |
| `ScreenGridLayer` | Screen-space grid (viewport-dependent) |
| `GPUGridLayer` | GPU-accelerated grid aggregation |
| `CPUGridLayer` | CPU-based grid with more flexibility |

**Geo Layers:**

| Layer | Use Case |
|---|---|
| `TripsLayer` | Animated temporal trajectories |
| `H3HexagonLayer` | H3 spatial index visualisation |
| `H3ClusterLayer` | H3 cluster boundaries |
| `S2Layer` | S2 cell visualisation |
| `TileLayer` | Tile-based data loading |
| `MVTLayer` | Mapbox Vector Tiles |
| `TerrainLayer` | 3D terrain rendering |
| `Tile3DLayer` | 3D tiles (buildings, terrain) |
| `GeoJsonLayer` | GeoJSON rendering (auto-detects geometry type) |

Source: https://deck.gl/docs/api-reference/layers

### 2.4 Custom Layer Development

deck.gl supports custom layers by extending the `Layer` base class:

```javascript
import { Layer } from '@deck.gl/core';

class CausalLinkLayer extends Layer {
  // Custom vertex/fragment shaders
  // Custom attribute definitions
  // Custom rendering pipeline
}
```

This is how we would implement specialised visualisations like:
- **Lag-annotated arcs** — arcs with variable thickness or animation speed representing time lag
- **Bivariate grid cells** — custom colour mixing for two variables per cell
- **Sparkline overlays** — small time-series charts rendered at grid cell positions

### 2.5 Python Integration: pydeck

pydeck is the Python binding for deck.gl, enabling use in Jupyter notebooks:

```python
import pydeck as pdk

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_fill_color=[255, 0, 0, 140],
    get_radius=1000,
)
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html("map.html")
```

**Key features:**
- Full deck.gl layer catalog available in Python
- Two-way communication with Jupyter kernel (selected data can be passed back)
- Handles hundreds of thousands of points
- JSON-based serialisation under the hood

This is valuable for the research/exploration phase of Causal Atlas, where analysts work in notebooks before features are promoted to the web application.

Source: https://deckgl.readthedocs.io/

### 2.6 Integration Approaches

| Approach | Pros | Cons |
|---|---|---|
| **Use Kepler.gl** (wraps deck.gl) | Turnkey UI, built-in filters, time playback | Less control, harder to customise |
| **Use deck.gl directly in React** | Full control, custom layers, better perf tuning | More development effort |
| **Use pydeck in Jupyter** | Rapid prototyping, Python ecosystem | Not suitable for production web app |
| **Hybrid: Kepler.gl + custom deck.gl layers** | Best of both — UI from Kepler, custom layers for causal | Integration complexity |

---

## 3. HungerMapLIVE

**URL:** https://hungermap.wfp.org/
**Operator:** UN World Food Programme (WFP)

### 3.1 Visualisation Approach

HungerMapLIVE is one of the most relevant reference implementations for Causal Atlas. It visualises multiple food security and contextual indicators on a single interactive map.

**Layer architecture:**
- **Base layer:** Choropleth map showing Insufficient Food Consumption (IFC) prevalence at sub-national level, colour-coded from green (low) to red (high)
- **Point overlays:** Conflict events, natural hazard alerts, weather anomalies rendered as point markers with icons
- **Toggle overlays:** Users can layer metrics including: food consumption, livelihood coping, rainfall anomalies, vegetation anomalies (NDVI), conflict density, economic shocks, hazard alerts
- **Country drilldown:** Clicking a country zooms in and shows sub-national detail with additional charts

**UX patterns worth noting:**
- **Progressive disclosure:** Global overview shows country-level aggregates; clicking reveals sub-national granularity, then district-level detail
- **Overlay toggling:** Simple checkboxes to add/remove layers. Each layer has its own legend that appears/disappears with the toggle
- **Side panel charts:** Clicking a region opens a side panel with time-series charts (food consumption trends, price trends) — a form of brushing-and-linking
- **Nowcasting indicators:** Where real-time data is unavailable, ML-generated nowcasts fill gaps with visual differentiation (different shading or pattern)
- **Minimal clutter:** Despite many data layers, the interface remains clean by defaulting to a single choropleth and requiring explicit user action to add complexity

### 3.2 Temporal Animation

HungerMapLIVE focuses on near-real-time snapshots rather than historical time-series animation. It shows "the current situation" with recent trends in side-panel charts. This is a design choice — it prioritises actionable current state over temporal exploration. For Causal Atlas, we need both: a current-state view AND the ability to scrub through time.

### 3.3 What We Can Learn

- The overlay toggle pattern is effective for multi-domain data
- Progressive disclosure (country -> sub-national -> district) manages complexity well
- Side-panel time-series charts linked to map selection is the right pattern for causal exploration
- Clean defaults with opt-in complexity is essential for usability

Source: https://hungermap.wfp.org/, https://innovation.wfp.org/project/hungermap-live

---

## 4. ACLED Dashboard

**URL:** https://acleddata.com/
**Platforms:** ACLED Explorer, Trendfinder, Conflict Index Dashboard, Early Warning Dashboard

### 4.1 Visualisation Architecture

ACLED provides several interconnected visualisation platforms:

**ACLED Explorer:**
- Interactive map showing conflict events as points, colour-coded by event type (battles, protests, violence against civilians, riots, explosions/remote violence, strategic developments)
- Click events to see details (date, actors, fatalities, description)
- Temporal bar chart below the map showing weekly event counts
- Trendline overlay showing 4-week or 52-week moving average

**Trendfinder:**
- Interconnected analytical modules sharing a common filter header
- Shared header lets you set date range, geography, and actor/event filters once — these carry across all modules
- Trend visualisation shows event counts over time with statistical anomaly detection
- Country-level heatmap for comparative analysis

**Conflict Index Dashboard:**
- Four composite indicators: deadliness, danger to civilians, geographic diffusion, number of armed groups
- Ranked country list with small-multiple sparklines
- Map with colour-coded countries by overall conflict severity

### 4.2 Filtering and Temporal Controls

- **Date range selector:** Start/end date pickers with preset ranges (last month, last year, custom)
- **Event type filter:** Checkboxes for ACLED event taxonomy
- **Actor filter:** Search and select specific armed groups or actor types
- **Geographic filter:** Country, region, or custom polygon selection
- **Temporal resolution:** Weekly bars (based on ACLED coding weeks: Saturday-Friday), with 4-week and 52-week moving average options

### 4.3 Technology

ACLED's dashboards use a combination of custom web components and, for some views, ArcGIS integration. The Conflict Index data is also available as an ArcGIS Living Atlas feature layer with time configuration.

### 4.4 What We Can Learn

- The shared filter header pattern (set once, applies everywhere) is excellent for multi-view dashboards
- Weekly temporal bars with moving average trendlines are an effective way to show conflict dynamics
- Event-type colour coding with consistent symbology across all views aids interpretation
- The Conflict Index approach of decomposing conflict into named sub-dimensions (deadliness, diffusion, etc.) is a good model for our multi-domain causal indicators

Source: https://acleddata.com/conflict-data/data-platforms, https://acleddata.com/platform/conflict-index-dashboard

---

## 5. GDELT Analysis Tools

**URL:** https://analysis.gdeltproject.org/
**Data source:** Global Database of Events, Language, and Tone

### 5.1 Visualisation Suite

GDELT provides several browser-based analysis and visualisation tools:

**GKG Tone Timeline Visualizer:**
- Plots average "tone" from the Global Knowledge Graph over time
- Tone scale: -100 (extremely negative) to +100 (extremely positive)
- Generates publication-ready time-series plots
- Outputs downloadable CSV data
- Useful for tracking sentiment shifts around events

**GKG Heatmap Visualizer:**
- Geographic heatmap from GKG search results
- Shows spatial distribution of media coverage and tone
- Rapid construction from keyword search

**GKG Network Visualizer:**
- Interactive browser-based network diagrams from GKG
- "Centrality" and "influencer" rankings for entities
- Shows relationships between actors, themes, and locations

**GKG Geographic Network Visualizer:**
- Georeferenced network diagrams
- Shows spatial connectivity between locations mentioned together
- Arc-based flow visualisation on a map

### 5.2 BigQuery Integration

GDELT's primary analytical pathway is through Google BigQuery, where the full dataset is freely queryable. Visualisation is typically done downstream:
- BigQuery SQL -> export -> Kepler.gl / deck.gl
- BigQuery SQL -> Google Data Studio / Looker dashboards
- BigQuery SQL -> Python (pandas/geopandas) -> pydeck / matplotlib

### 5.3 What We Can Learn

- Tone/sentiment as a continuous variable mapped to colour is an effective encoding
- Geographic network visualisation (location co-occurrence as arcs) is directly applicable to showing causal connections between regions
- The GKG approach of extracting themes, entities, and tone from unstructured text could complement our structured data sources
- GDELT's approach to massive-scale data (BigQuery + downstream viz) validates our DuckDB strategy at a different scale

Source: https://analysis.gdeltproject.org/, https://analysis.gdeltproject.org/module-gkg-tonetimeline.html

---

## 6. Mapbox GL JS and MapLibre GL JS

### 6.1 Mapbox GL JS

**URL:** https://docs.mapbox.com/mapbox-gl-js/
**Licence:** Proprietary (BSL 1.1 since v2.0, December 2020)
**Current version:** v3.x

**Capabilities:**
- Vector tile rendering with custom styling via Mapbox Style Specification (JSON-based)
- 3D terrain, building extrusion, sky/atmosphere rendering
- Data-driven styling: colour, size, opacity can be bound to data properties with expressions
- Camera animations (fly-to, ease-to, custom easing functions)
- Dynamic style images for animated icons/patterns
- Cluster aggregation for point data
- Runtime style modification (change colours, add/remove layers programmatically)
- Geocoding, directions, and other Mapbox services integration

**Pricing (as of March 2025):**

| Tier | Map Loads/Month | Price |
|---|---|---|
| Free | Up to 50,000 | $0 |
| Pay-as-you-go | 50,001 - 100,000 | ~$5/1,000 loads |
| Volume | 100,001 - 1,000,000 | Tiered discounts |
| Enterprise | 1,000,000+ | Custom pricing |

A "map load" is counted each time a Map object is initialised.

**Temporal animation:** Mapbox GL JS does not have built-in temporal animation controls. Temporal scrubbing requires custom implementation: external slider + programmatic filter updates via `map.setFilter()` or `map.setPaintProperty()`. This works but requires significant custom code. Heat map intensity transitions can be smoothed using opacity and colour gradient interpolation.

Source: https://docs.mapbox.com/mapbox-gl-js/guides/pricing/

### 6.2 MapLibre GL JS

**URL:** https://maplibre.org/
**Repository:** https://github.com/maplibre/maplibre-gl-js
**Licence:** BSD 3-Clause (fully open source)

MapLibre GL JS is the community fork of Mapbox GL JS v1.x, created after Mapbox switched to a proprietary licence. It is now the recommended open-source alternative.

**Key differences from Mapbox GL JS:**
- Fully open source — no API key required for the rendering library itself (only for tile services)
- Provider-independent — works with any vector tile source (MapTiler, Stadia Maps, self-hosted, etc.)
- Active community development with regular releases
- TypeScript rewrite
- WebGL2 support
- Drop-in replacement for Mapbox GL JS v1.x (replace `mapbox-gl` with `maplibre-gl` in package.json)

**For Causal Atlas:** MapLibre GL JS is the preferred base map renderer. Kepler.gl v3.x already uses MapLibre internally. If we build custom visualisation components beyond Kepler.gl, MapLibre is the right choice — open source, no per-load pricing, and compatible with our tech stack.

Source: https://maplibre.org/, https://github.com/maplibre/maplibre-gl-js

---

## 7. Leaflet / Folium

### 7.1 Leaflet

**URL:** https://leafletjs.com/
**Licence:** BSD 2-Clause
**Current version:** 1.9.x

Leaflet is the most widely used open-source JavaScript mapping library. It is simpler and lighter than Mapbox GL / deck.gl, using DOM-based rendering (SVG/Canvas) rather than WebGL.

**Strengths:**
- Extremely simple API — quick to prototype
- Massive plugin ecosystem (400+ plugins)
- Works everywhere (no WebGL requirement)
- Tiny footprint (~42KB gzipped)

**Limitations for Causal Atlas:**
- No WebGL — poor performance with >10,000 points
- No built-in 3D support
- No deck.gl-style aggregation layers
- Raster tile only (no native vector tile support without plugins)

### 7.2 Leaflet.TimeDimension

**Repository:** https://github.com/socib/Leaflet.TimeDimension
**Purpose:** Adds temporal controls to Leaflet maps

**Features:**
- Play/pause, next/back, speed controls, time slider
- Supports WMS layers with TIME parameter (OGC standard)
- Supports GeoJSON with timestamped features (looks for `coordTimes`, `times`, or `linestringTimestamps` in feature properties)
- TimeDimension object can be shared among different layers for synchronisation
- Duration option for showing features active within a time window

**Good for:** Quick prototypes, embedding in research notebooks, OGC-compatible data sources (THREDDS/ncWMS for climate data).

**Not suitable for:** Production application with millions of points — performance will not scale.

### 7.3 Folium (Python)

Folium wraps Leaflet for Python, generating interactive HTML maps from pandas DataFrames:

```python
import folium
m = folium.Map(location=[0, 30], zoom_start=4)
folium.CircleMarker([1.2, 32.3], radius=5, color='red').add_to(m)
m.save("map.html")
```

Plugins include `folium.plugins.TimestampedGeoJson` for temporal animation and `folium.plugins.HeatMapWithTime` for animated heatmaps.

**Role in Causal Atlas:** Useful for quick exploratory visualisation in Jupyter notebooks during the research phase. Not suitable for the production application.

Source: https://github.com/socib/Leaflet.TimeDimension, https://leafletjs.com/plugins.html

---

## 8. Plotly / Dash

### 8.1 Plotly Express

**URL:** https://plotly.com/python/
**Licence:** MIT

Plotly Express provides high-level functions for geospatial visualisation:

```python
import plotly.express as px

fig = px.choropleth(
    df, locations="iso_alpha", color="value",
    hover_name="country", animation_frame="year",
    color_continuous_scale="RdYlGn_r"
)
fig.show()
```

**Key geospatial chart types:**
- `px.choropleth` — country/region fill maps using Natural Earth or custom GeoJSON
- `px.choropleth_mapbox` — choropleth on Mapbox base map (deprecated in newer versions, use `px.choropleth_map`)
- `px.scatter_mapbox` / `px.scatter_map` — point data on Mapbox/MapLibre base map
- `px.density_mapbox` / `px.density_map` — heatmap on base map
- `px.line_mapbox` / `px.line_map` — paths/routes on base map

**Built-in animation:** The `animation_frame` parameter creates a play button and slider, stepping through time periods. This is the simplest way to create temporal choropleth animations in Python.

### 8.2 Dash

**URL:** https://dash.plotly.com/
**Licence:** MIT (open source), Enterprise version available

Dash is a Python framework for building analytical web applications. It wraps Plotly charts in a reactive callback system.

**Temporal data pattern:**

```python
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Slider(id='year-slider', min=2010, max=2024, value=2020, step=1),
    dcc.Graph(id='map'),
    dcc.Graph(id='timeseries')
])

@app.callback(
    Output('map', 'figure'),
    Output('timeseries', 'figure'),
    Input('year-slider', 'value')
)
def update(year):
    filtered = df[df.year == year]
    map_fig = px.choropleth(filtered, ...)
    ts_fig = px.line(df, x='year', y='value', ...)
    return map_fig, ts_fig
```

This callback pattern naturally supports brushing-and-linking: selecting a region on the map can trigger updates in linked time-series charts.

**Geospatial Dash components:**
- `dash-leaflet` — Leaflet integration for Dash
- `dash-deck` — deck.gl integration for Dash
- `dcc.Graph` with Plotly mapbox figures

### 8.3 Performance Considerations

- Plotly figures with >50,000 points become sluggish in the browser
- For large polygon datasets, use GeoJSON (not Shapefiles) and simplify geometries
- `dash-deck` provides access to deck.gl's GPU-accelerated rendering within a Dash app, bypassing Plotly's SVG/Canvas limitations
- Server-side callbacks can handle heavy data processing, sending only the visible subset to the client

### 8.4 Role in Causal Atlas

Dash is well-suited for the **analytical dashboard** layer of Causal Atlas — statistical results, correlation matrices, lag analysis charts, time-series comparisons. It complements a Kepler.gl/deck.gl map rather than replacing it. The callback pattern is ideal for linked views between a map and analytical charts.

Source: https://plotly.com/python/choropleth-maps/, https://dash.plotly.com/

---

## 9. Felt

**URL:** https://felt.com/
**Type:** Commercial SaaS platform

### 9.1 Capabilities

Felt is a modern collaborative mapping platform focused on ease of use:

- **Real-time collaboration:** Multiple users can view, edit, and annotate maps simultaneously (Google Docs model for maps)
- **Data upload:** Supports most geospatial formats (GeoJSON, Shapefile, GeoTIFF, CSV, KML, GeoPackage), up to 5GB per upload, up to 50 layers per upload
- **Drawing and annotation:** Freehand drawing, markers, polygons, text annotations directly on the map
- **Sharing:** Simple link-based sharing with granular permissions (view, edit, admin)
- **API:** REST API for programmatic data upload, layer management, webhook notifications
- **JavaScript SDK:** For embedding maps in applications
- **Database connections (Enterprise):** Postgres, Snowflake, AWS, Databricks

### 9.2 Limitations

| Limitation | Impact on Causal Atlas |
|---|---|
| **No temporal animation** | Cannot scrub through time — a dealbreaker for our use case |
| **Commercial pricing** | Enterprise features (API, DB connections, SDK) require paid plans |
| **No custom rendering** | Cannot implement specialised causal visualisation layers |
| **No analytical capabilities** | No built-in statistical analysis or correlation tools |
| **Closed source** | Cannot extend or self-host |
| **No bivariate choropleth** | Cannot show two variables simultaneously on a single map layer |

### 9.3 Role in Causal Atlas

Felt is **not suitable** as a core visualisation component for Causal Atlas. Its strengths (collaboration, simplicity) do not align with our needs (temporal animation, custom layers, statistical integration, open source). However, it could be useful for sharing research findings with non-technical stakeholders — create a Felt map as a communication tool, not as the analysis platform.

Source: https://felt.com/, https://felt.com/pricing

---

## 10. Observable / D3.js

### 10.1 D3.js

**URL:** https://d3js.org/
**Licence:** ISC
**Current version:** v7.x
**Maintained by:** Observable (Mike Bostock)

D3.js is the foundational library for custom data visualisation on the web. It provides low-level primitives for bindings data to DOM elements with transitions, interactions, and geographic projections.

**Geospatial capabilities (d3-geo):**
- 30+ map projections (Mercator, Albers, Orthographic, etc.) with arbitrary aspects
- Adaptive sampling, antimeridian cutting, and configurable clipping
- GeoJSON path generation
- Spherical area, centroid, distance calculations
- Extended projections via `d3-geo-projection` and `d3-geo-polygon`

**Interaction primitives:**
- Brushing: `d3.brush()` for rectangular selection, `d3.brushX()` / `d3.brushY()` for single-axis
- Zooming: `d3.zoom()` with configurable extent and transitions
- Dragging: `d3.drag()` for interactive element repositioning
- Transitions: `d3.transition()` for animated changes with easing

### 10.2 Observable Notebooks

**URL:** https://observablehq.com/
**Licence:** Platform is free for public notebooks; private notebooks require subscription

Observable notebooks provide a reactive JavaScript environment for data exploration:

- **Reactive cells:** When a cell's value changes, dependent cells automatically re-evaluate
- **Built-in data loading:** Fetch APIs, file attachments, database connections
- **D3 integration:** D3 is available by default in all notebooks
- **Observable Plot:** Higher-level charting library built on D3, with first-class projection support for maps
- **Import system:** Import cells from other notebooks to reuse visualisation components
- **Embedding:** Notebooks can be embedded in external websites

### 10.3 Observable Framework

Observable Framework (2024+) is a static site generator for data apps:
- Builds data-driven dashboards as static HTML
- Data loaders run at build time (Python, R, SQL, JavaScript)
- Embeds Observable Plot and D3 visualisations
- Markdown-based authoring

### 10.4 Linked Brushing in Observable

Observable provides excellent linked brushing capabilities:

> "Linked brushing with geospatial data can help viewers focus on events and patterns within and across regions of interest, and see how those patterns change across dimensions like time."

The reactive cell model makes linked brushing natural: select a region on a map -> that selection is a reactive variable -> a time-series chart in another cell automatically updates to show data for the selected region.

Source: https://observablehq.com/blog/linked-brushing

### 10.5 Role in Causal Atlas

D3.js/Observable is ideal for **custom one-off visualisations** that cannot be achieved with Kepler.gl or Plotly — bivariate choropleths, sparkline maps, custom lag visualisations, network diagrams of causal chains. Observable notebooks are excellent for prototyping these visualisations during research. Selected visualisations can then be ported to the React application using D3 directly or Observable Plot.

Source: https://d3js.org/, https://observablehq.com/

---

## 11. DuckDB + Kepler.gl v3.1 Integration

### 11.1 The New Architecture

Kepler.gl v3.1 (released 2024) introduced a fundamental shift by embedding DuckDB as an in-browser analytical engine. This is the most significant development for our use case.

**How it works:**
1. DuckDB-WASM runs in the browser — no server, no database connection required
2. Users can drag-and-drop files (CSV, Parquet, GeoParquet) to create DuckDB tables
3. A SQL Data Explorer panel provides a full SQL editor within Kepler.gl
4. SQL query results are rendered as map layers
5. DuckDB's spatial extension enables complex spatial queries

### 11.2 GeoParquet Integration

The killer feature is direct GeoParquet support:
- **Spatially partitioned GeoParquet** files can be read from cloud storage (S3, GCS)
- DuckDB's spatial extension reads only relevant data partitions, not the entire file
- This eliminates the need to download entire datasets into browser memory
- Enables working with datasets far larger than browser memory limits

```sql
-- Example: Query spatially partitioned GeoParquet from S3
SELECT * FROM read_parquet('s3://bucket/events/*.parquet', hive_partitioning=true)
WHERE ST_Within(geometry, ST_MakeEnvelope(29, -5, 36, 5))
AND date >= '2023-01-01'
```

### 11.3 SQL-Driven Visualisation

The SQL explorer enables analytical workflows directly in the visualisation tool:

```sql
-- Aggregate monthly conflict events per PRIO-GRID cell
SELECT grid_id, date_trunc('month', event_date) as month,
       COUNT(*) as event_count,
       SUM(fatalities) as total_fatalities,
       AVG(ST_X(geometry)) as lon, AVG(ST_Y(geometry)) as lat
FROM conflict_events
GROUP BY grid_id, month
ORDER BY month
```

The query result becomes a layer that can use time playback to animate through months.

### 11.4 Performance Benefits

| Scenario | Without DuckDB | With DuckDB |
|---|---|---|
| Load 500MB CSV | Fails (browser memory) | Loads into DuckDB table, queries subset |
| Filter 10M points by time | CPU-bound, laggy | SQL WHERE clause, fast |
| Spatial aggregation | Client-side, slow | `GROUP BY grid_id`, GPU-efficient |
| Join two datasets | Manual in Python/JS | SQL JOIN in browser |
| Cloud data access | Download entire file | Read relevant partitions only |

### 11.5 Relevance to Causal Atlas

This integration is transformative for our project:
- **PRIO-GRID aggregation** can be done in SQL directly in the visualisation tool
- **Temporal filtering** is handled by DuckDB rather than CPU-bound JavaScript
- **Multi-dataset joins** (e.g., conflict events + food prices + rainfall) can be done in SQL
- **GeoParquet** is our planned storage format — native support eliminates format conversion
- **No server required** for exploratory analysis — analysts can work with cloud-hosted Parquet files directly

**npm package:** `@kepler.gl/duckdb`

Source: https://foursquare.com/resources/blog/products/foursquare-brings-enterprise-grade-spatial-analytics-to-your-browser-with-kepler-gl-3-1/, https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/sql-data-explorer.md

---

## 12. Visualisation Techniques for Causal Discovery

This section covers specialised techniques for visualising causal relationships — the core differentiator of Causal Atlas.

### 12.1 Brushing and Linking

**What it is:** Selecting a subset of data in one view (e.g., a region on a map) and having linked views (e.g., time-series charts, scatter plots) update automatically to reflect the selection.

**Implementation approaches:**

| Approach | Pros | Cons |
|---|---|---|
| **Observable reactive cells** | Natural reactivity, rapid prototyping | Not a production framework |
| **Dash callbacks** | Python-native, server-side processing | Round-trip latency for large data |
| **Vega-Lite selections** | Declarative, concise | Limited geospatial support |
| **Custom React state** | Full control, client-side | Significant development effort |
| **Crossfilter.js** | Purpose-built for fast cross-filtering | Older library, not maintained |

**Recommended for Causal Atlas:** React state management (Zustand or Redux) coordinating between a Kepler.gl/deck.gl map component and Plotly/Recharts time-series panels. Selection on the map dispatches an action; linked charts subscribe to the selection state.

**UX pattern:**
1. User clicks a PRIO-GRID cell (or draws a selection polygon)
2. Side panel populates with time-series charts for all available indicators in that cell
3. Charts show: conflict events, food price index, rainfall, NDVI, etc. on aligned time axes
4. Highlighted lags are annotated (e.g., "rainfall drop precedes food price spike by 2 months")

Source: https://observablehq.com/blog/linked-brushing, https://geodacenter.github.io/workbook/2a_eda/lab2a.html

### 12.2 Temporal Scrubbing

**What it is:** A slider or playback control that steps through time, updating the map to show spatial patterns at each time step.

**Design considerations for Causal Atlas:**

- **Dual-mode scrubbing:** (a) Manual slider for precise time selection, (b) Auto-play with adjustable speed for watching patterns evolve
- **Time window vs. time point:** Show data for a single month (point) or a rolling window (e.g., trailing 3 months). Rolling window is better for sparse data.
- **Linked timeline:** A timeline bar below the map shows the distribution of events, with the current position highlighted. Users can click anywhere on the timeline to jump.
- **Event markers on timeline:** Significant events (major conflicts, disasters, policy changes) are marked on the timeline for context.
- **Multi-layer synchronisation:** When showing conflict + rainfall + food prices, all layers must update in sync as the time slider moves. This is non-trivial when layers have different temporal resolutions (daily vs. monthly).

**Implementation:**
- Kepler.gl's built-in time playback handles single-layer scrubbing well
- For multi-layer synchronisation, custom implementation is needed: a master time controller dispatches the current time to each layer, which maps it to the nearest available time step in its resolution

### 12.3 Small Multiples

**What it is:** A grid of small maps, each showing the same geographic area at a different time step. The viewer compares spatial patterns across time by scanning across the grid.

**Strengths:**
- Enables direct visual comparison without relying on animation memory
- Works well in print and static reports
- Shows subtle spatial pattern changes that might be missed in animation

**Implementation:**
- D3.js: Create a grid of SVG/Canvas maps, each with the same projection and data filtered to a time step
- deck.gl: Multiple `Deck` instances or a single instance with `MultiViewport`
- Plotly: `px.choropleth` with `facet_col` parameter (limited to ~12 panels)
- Observable Plot: Faceted geo marks

**Design for Causal Atlas:**
- Show a 4x3 grid of monthly maps for a selected indicator
- Or show 2 rows: one for cause variable, one for effect variable, aligned temporally
- Highlight the time lag visually (e.g., if cause leads effect by 2 months, offset the rows)

### 12.4 Bivariate Choropleth

**What it is:** A choropleth map that encodes two variables simultaneously using a 2D colour scheme. Each cell's colour represents the intersection of two variable values.

**The colour legend** is a square grid (typically 3x3 or 2x2):
- X-axis: Variable A (e.g., drought severity), low to high
- Y-axis: Variable B (e.g., conflict intensity), low to high
- Cells are coloured by blending two colour ramps
- Corner colours: low-low (neutral), high A only, high B only, high-high (the combination of interest)

**Common colour schemes:**
- Purple-green (Stevens): A = green, B = purple, overlap = dark
- Blue-red: A = blue, B = red, overlap = purple
- Custom: Any two diverging ramps that produce readable blends

**Design considerations:**
- Use 3x3 (9 classes) for most purposes — 4x4 and above are too hard to read
- Always show the 2D legend prominently
- Consider adding a univariate toggle so users can see each variable individually
- The bivariate encoding is most effective when the relationship between variables IS the story (which is exactly our use case)

**Implementation:**
- D3.js: Custom implementation with `d3.scaleQuantile` for each variable + colour mixing
- Python: GeoPandas + matplotlib with custom colormap
- Plotly: Requires manual colour assignment (no built-in bivariate choropleth)
- deck.gl: Custom layer with two-variable colour accessor

**Relevance to Causal Atlas:** This is a priority technique. Showing drought severity AND conflict intensity on the same map immediately reveals spatial correlation. A bivariate choropleth of "cause" and "effect" variables, with the effect lagged by the detected optimal lag, would directly visualise the causal hypothesis.

Source: https://www.joshuastevens.net/cartography/make-a-bivariate-choropleth-map/, https://giscarta.com/blog/bivariate-choropleth-maps-a-comprehensive-guide

### 12.5 Flow Maps / Arc Layers

**What it is:** Curved arcs connecting locations on a map, representing directed relationships (flows, connections, causal links).

**Application to causal discovery:**
- **Cross-regional causal arcs:** An arc from Region A to Region B with label "drought -> food price spike, lag: 3 months, p < 0.01"
- **Arc encoding:** Width = strength of correlation, colour = type of relationship (positive/negative), animation direction = causal direction
- **Radial flow maps:** Multiple arcs converging on a single destination (e.g., all regions causally linked to a conflict hotspot)

**Implementation:**
- deck.gl `ArcLayer`: Source/target positions, source/target colours, width, height (arc curvature)
- Kepler.gl Arc layer: Built-in, supports colour/width encoding from data fields
- D3.js: Custom path generator with great circle arcs (`d3.geoPath` with `d3.geoGreatArc`)

**Design for Causal Atlas:**
- Discovered causal links rendered as arcs between PRIO-GRID cells or admin regions
- Arc thickness = Granger causality F-statistic or transfer entropy value
- Arc colour = positive (warm) or negative (cool) relationship
- Arc animation = flows from cause to effect location
- Clicking an arc shows detailed statistics: lag, p-value, effect size, confidence interval

### 12.6 Lag Visualisation

**What it is:** Techniques for showing time-lagged relationships on a map — the core of Causal Atlas.

**Approach 1: Offset Small Multiples**
- Two rows of small multiples: cause variable (top) and effect variable (bottom)
- The rows are offset by the detected lag (e.g., if lag = 2 months, the effect row starts 2 months later)
- Vertical alignment shows the temporal relationship

**Approach 2: Cross-Correlation Maps (Spatial)**
- For each grid cell, compute cross-correlation between cause and effect at multiple lags
- Render a map where colour = optimal lag (e.g., blue = 1 month, green = 3 months, red = 6 months)
- A second map shows colour = correlation strength at optimal lag
- ArcGIS Pro's Time Series Cross Correlation tool outputs exactly this: feature classes showing strongest correlations and associated lags, with pop-up charts

**Approach 3: Animated Causal Cascade**
- Animation shows the cause variable activating (e.g., drought onset) in certain cells
- After the detected lag, the effect variable activates in the same or nearby cells
- Visual "ripple" effect showing causality propagating through space and time

**Approach 4: Lag Heatmap Matrix**
- Grid: X-axis = geographic units, Y-axis = lag (0 to 12 months)
- Cell colour = correlation strength at that lag for that location
- Highlights which regions have the strongest time-lagged relationships and at what delay

**Implementation reference:** The ArcGIS Space Time Pattern Mining toolbox includes a Time Series Cross Correlation tool that computes and visualises lagged correlations. Its output format (map layers with correlation at optimal lag + the lag value itself) is a good model for our own implementation.

Source: https://pro.arcgis.com/en/pro-app/latest/tool-reference/space-time-pattern-mining/time-series-correlation.htm, https://pubmed.ncbi.nlm.nih.gov/16187896/

### 12.7 Sparkline Maps

**What it is:** Small time-series line charts embedded directly into map cells (or positioned at geographic locations). Each sparkline shows the temporal trend for that location.

**Design:**
- Each PRIO-GRID cell (or admin region) contains a tiny line chart
- The sparkline shows the trend of a selected indicator (e.g., conflict events per month)
- Zooming in reveals more detail; zooming out shows overall pattern
- Optional: dual sparklines per cell (cause + effect) to show temporal relationship

**Implementation:**
- deck.gl: Custom layer rendering sparklines as textures or using `TextLayer` + `PathLayer` combination
- D3.js: SVG sparklines positioned at centroid coordinates
- Tableau: Built-in sparkline-on-map capability (commercial)
- Custom WebGL: Most performant but highest development effort

**Challenges:**
- Visual clutter at wide zoom levels — need level-of-detail (LOD) strategy
- Rendering thousands of sparklines requires GPU acceleration or canvas-based drawing
- Interaction (hover/click for detail) adds complexity

**Relevance to Causal Atlas:** Sparkline maps are highly effective for showing "at a glance" which regions have increasing vs. decreasing trends. Combined with colour-coding (red = worsening, green = improving), they provide both trend and current-state information in a single view.

---

## 13. Tool Comparison Table

| Tool | Licence | Layer Types | Temporal Animation | Large Data Performance | React Integration | Custom Layers | Python Support | Causal Viz Support |
|---|---|---|---|---|---|---|---|---|
| **Kepler.gl v3.1** | MIT | 15+ (point, arc, hex, grid, H3, S2, trip, heatmap, polygon, tile, raster, WMS, cluster, icon, line) | Built-in time playback | Good (DuckDB, but CPU filtering lag) | Yes (Redux) | Limited (factory pattern) | KeplerGl Jupyter widget | Basic (arc layer for flows) |
| **deck.gl v9.2** | MIT | 30+ (all kepler layers + more) | Via TripsLayer + custom | Excellent (WebGL2/WebGPU) | Yes (native) | Full custom layer API | pydeck | Excellent (build anything) |
| **Mapbox GL JS** | Proprietary (BSL) | Vector tiles, raster, GeoJSON, image | Custom implementation | Good (vector tiles) | Yes | Via style spec | No | None built-in |
| **MapLibre GL JS** | BSD 3-Clause | Same as Mapbox GL v1 | Custom implementation | Good | Yes | Via style spec | No | None built-in |
| **Leaflet** | BSD 2-Clause | Marker, circle, polygon, GeoJSON | Via TimeDimension plugin | Poor (>10K points) | Via react-leaflet | Plugins | Folium | None |
| **Plotly/Dash** | MIT | Choropleth, scatter, density, line (map variants) | Slider + callbacks | Moderate (50K points) | Dash (React-like) | No custom layers | Native Python | Good (linked callbacks) |
| **Felt** | Commercial | Points, lines, polygons, rasters | None | Good (5GB upload) | JS SDK (embed) | None | API only | None |
| **D3.js** | ISC | Unlimited (custom SVG/Canvas) | Custom implementation | Moderate (DOM-limited) | Yes (manual) | Everything is custom | No (JS only) | Excellent (build anything) |
| **Observable** | Free (public) / Paid (private) | D3 + Observable Plot | Custom implementation | Moderate | Embed via iframe | Everything is custom | No | Excellent |
| **GDELT Tools** | Free (data) | Heatmap, network, timeline, geo-network | Timeline visualizer | Good (BigQuery backend) | No (standalone) | No | BigQuery + Python | Limited (tone/network) |

### Decision Matrix: Weighted Scoring for Causal Atlas

| Criterion (Weight) | Kepler.gl | deck.gl | Plotly/Dash | D3/Observable | MapLibre |
|---|---|---|---|---|---|
| Open source (10) | 10 | 10 | 10 | 10 | 10 |
| Temporal animation (9) | 8 | 6 | 7 | 5 | 3 |
| Large data handling (9) | 8 | 10 | 5 | 4 | 7 |
| React integration (8) | 8 | 10 | 6 | 5 | 9 |
| Multi-layer support (8) | 9 | 10 | 6 | 8 | 7 |
| Custom causal viz (8) | 4 | 10 | 5 | 10 | 3 |
| Python/notebook use (6) | 6 | 8 | 10 | 6 | 2 |
| Ease of development (6) | 9 | 5 | 8 | 3 | 6 |
| DuckDB/Parquet support (7) | 10 | 3 | 2 | 2 | 2 |
| Community/ecosystem (5) | 7 | 8 | 9 | 9 | 8 |
| **Weighted Total** | **604** | **608** | **510** | **486** | **440** |

---

## 14. Recommended Approach for Causal Atlas

### 14.1 Architecture: Layered Visualisation Stack

We recommend a **three-tier visualisation architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                    TIER 3: Custom Causal Viz              │
│  D3.js custom components: bivariate choropleth,          │
│  sparkline maps, lag heatmaps, causal cascade animation  │
│  Built as React components using deck.gl custom layers   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────┐
│                    TIER 2: Analytical Dashboard           │
│  Plotly/Recharts: time-series charts, correlation         │
│  matrices, lag analysis, statistical result panels        │
│  Connected via React state (Zustand/Redux)               │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────┐
│                    TIER 1: Map Engine                     │
│  Kepler.gl (embedded React component) with DuckDB        │
│  OR deck.gl direct (for more control)                    │
│  Base map: MapLibre GL JS (open source, no API fees)     │
│  Data layer: GeoParquet via DuckDB                       │
└─────────────────────────────────────────────────────────┘
```

### 14.2 Phase 1: Research and Prototyping (Current)

**Tools:** pydeck + Jupyter notebooks, Folium for quick maps, Observable notebooks for custom visualisation experiments

**Goals:**
- Validate data integration workflows with real datasets
- Prototype bivariate choropleth with drought + conflict data
- Test Kepler.gl DuckDB integration with PRIO-GRID-aggregated GeoParquet files
- Prototype brushing-and-linking with Observable (fastest iteration)

### 14.3 Phase 2: Core Map Application

**Primary map engine:** Kepler.gl v3.1+ embedded in React with DuckDB

**Rationale:**
- Built-in time playback for temporal scrubbing
- 15+ layer types cover most of our needs without custom code
- DuckDB/GeoParquet integration aligns with our data architecture
- SQL explorer enables power-user analysis without custom UI
- Redux-based state management integrates with our React app
- MIT licence, actively maintained by Foursquare

**Base map:** MapLibre GL JS (already used by Kepler.gl internally) with OpenStreetMap or MapTiler tiles (no Mapbox API costs)

**Alternative if Kepler.gl proves too constraining:** Drop to deck.gl directly with MapLibre. More development effort but total control over rendering and interaction.

### 14.4 Phase 3: Causal Visualisation Layer

Build custom visualisation components for causal discovery, implemented as deck.gl custom layers or React components using D3.js:

| Component | Implementation | Priority |
|---|---|---|
| **Brushing-and-linking** (map selection -> time-series panel) | React state + Recharts/Plotly | P0 (essential) |
| **Temporal scrubbing** (multi-layer synchronised playback) | Custom time controller wrapping Kepler.gl filter | P0 (essential) |
| **Bivariate choropleth** (two variables on one map) | D3.js custom colour scale + deck.gl PolygonLayer | P1 (high) |
| **Causal arc layer** (connections between regions with lag/strength encoding) | deck.gl ArcLayer with custom accessors | P1 (high) |
| **Cross-correlation lag map** (optimal lag + strength per cell) | deck.gl GridLayer with custom colour accessor | P1 (high) |
| **Small multiples** (grid of maps at different time steps) | Multiple deck.gl viewports or D3.js SVG | P2 (medium) |
| **Lag heatmap matrix** (location x lag correlation matrix) | Plotly heatmap or D3.js | P2 (medium) |
| **Sparkline maps** (embedded time-series per grid cell) | deck.gl custom layer (texture-based) | P3 (future) |
| **Causal cascade animation** (propagation through space-time) | deck.gl TripsLayer variant with custom shaders | P3 (future) |

### 14.5 Phase 4: Analytical Dashboard

**Tool:** Plotly Dash or a custom React dashboard with Recharts

**Components:**
- Correlation matrix (all indicator pairs for selected region)
- Lag analysis chart (correlation vs. lag for selected variable pair)
- Granger causality results table with interactive filtering
- Time-series comparison panel (overlay multiple indicators with adjustable lag offset)
- Statistical significance indicators (p-values, confidence intervals)

### 14.6 Key Design Principles

1. **Progressive disclosure:** Start with a clean single-layer map. Users opt in to complexity.
2. **Linked views:** Every selection on the map updates linked analytical panels. Every chart interaction can highlight map regions.
3. **URL-encoded state:** Map position, selected layers, time position, selected region — all encoded in URL for shareability and reproducibility.
4. **Mobile-responsive:** Map fills screen on mobile; analytical panels stack below or slide in.
5. **Accessibility:** Colour schemes must be colourblind-safe. All information conveyed by colour must also be available via labels, patterns, or interaction.
6. **Performance budget:** Target 60fps map interaction with up to 1M points. Use DuckDB for filtering, deck.gl for rendering, and server-side pre-aggregation for anything beyond browser capacity.

### 14.7 Data Flow

```
Cloud Storage (S3/GCS)
  └── Spatially partitioned GeoParquet files
        └── DuckDB-WASM (in browser)
              ├── SQL filtering by space, time, indicators
              ├── Aggregation to PRIO-GRID resolution
              └── Results -> deck.gl/Kepler.gl layers
                              ├── Map rendering (WebGL2)
                              ├── Selection events -> React state
                              └── Linked charts (Plotly/Recharts)
```

### 14.8 What We Do NOT Need

- **ArcGIS/QGIS:** Desktop GIS tools. Our target is web-first.
- **Google Maps API:** Proprietary, expensive, less flexible than MapLibre.
- **Tableau/Power BI:** Commercial BI tools. We are open source.
- **Felt:** No temporal animation, commercial, closed source.
- **Leaflet:** Performance insufficient for our data scale.

---

## Sources

### Tools and Libraries
- [Kepler.gl Documentation](https://docs.kepler.gl/)
- [Kepler.gl GitHub Releases](https://github.com/keplergl/kepler.gl/releases)
- [Kepler.gl Layer Types](https://docs.kepler.gl/docs/user-guides/c-types-of-layers)
- [Kepler.gl Time Playback](https://docs.kepler.gl/docs/user-guides/h-playback)
- [Kepler.gl SQL Data Explorer](https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/sql-data-explorer.md)
- [Kepler.gl 3.1 Announcement (Foursquare)](https://foursquare.com/resources/blog/products/foursquare-brings-enterprise-grade-spatial-analytics-to-your-browser-with-kepler-gl-3-1/)
- [@kepler.gl/duckdb npm package](https://www.npmjs.com/package/@kepler.gl/duckdb)
- [deck.gl Documentation](https://deck.gl/docs)
- [deck.gl Layer Catalog](https://deck.gl/docs/api-reference/layers)
- [deck.gl What's New](https://deck.gl/docs/whats-new)
- [pydeck Documentation](https://deckgl.readthedocs.io/)
- [MapLibre GL JS](https://maplibre.org/)
- [MapLibre GL JS GitHub](https://github.com/maplibre/maplibre-gl-js)
- [Mapbox GL JS Pricing](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/)
- [Leaflet.TimeDimension](https://github.com/socib/Leaflet.TimeDimension)
- [Plotly Choropleth Maps](https://plotly.com/python/choropleth-maps/)
- [Dash Documentation](https://dash.plotly.com/)
- [Felt Platform](https://felt.com/)
- [D3.js](https://d3js.org/)
- [D3-geo Module](https://d3js.org/d3-geo)
- [Observable](https://observablehq.com/)
- [Observable Linked Brushing](https://observablehq.com/blog/linked-brushing)

### Reference Platforms
- [HungerMapLIVE](https://hungermap.wfp.org/)
- [WFP Innovation - HungerMapLIVE](https://innovation.wfp.org/project/hungermap-live)
- [ACLED Data Platforms](https://acleddata.com/conflict-data/data-platforms)
- [ACLED Conflict Index Dashboard](https://acleddata.com/platform/conflict-index-dashboard)
- [ACLED Trendfinder](https://acleddata.com/trendfinder/)
- [GDELT Analysis Service](https://analysis.gdeltproject.org/)
- [GDELT GKG Tone Timeline](https://analysis.gdeltproject.org/module-gkg-tonetimeline.html)
- [GDELT GKG Heatmap Visualizer](https://analysis.gdeltproject.org/module-gkg-heatmapper.html)
- [GDELT GKG Geographic Network](https://analysis.gdeltproject.org/module-gkg-geonet.html)

### Techniques and Methods
- [Bivariate Choropleth Guide (Joshua Stevens)](https://www.joshuastevens.net/cartography/make-a-bivariate-choropleth-map/)
- [Bivariate Choropleth Comprehensive Guide (GISCarta)](https://giscarta.com/blog/bivariate-choropleth-maps-a-comprehensive-guide)
- [ArcGIS Time Series Cross Correlation](https://pro.arcgis.com/en/pro-app/latest/tool-reference/space-time-pattern-mining/time-series-correlation.htm)
- [Cross Correlation Maps (PubMed)](https://pubmed.ncbi.nlm.nih.gov/16187896/)
- [Sparklines on Maps (Tableau)](https://www.tableau.com/blog/sparklines-maps)
- [Space-Time Visualization Techniques (BioMedware)](https://biomedware.com/four-space-time-data-visualization-techniques-to-consider/)
- [Temporal Data Visualization Techniques (Map Library)](https://www.maplibrary.org/1582/data-visualization-techniques-for-temporal-mapping/)
- [GeoParquet Performance with DuckDB (Radiant Earth)](https://medium.com/radiant-earth-insights/performance-explorations-of-geoparquet-and-duckdb-84c0185ed399)
- [NYC Taxi Data with DuckDB + KeplerGL](https://medium.com/@tibeggs/exploring-nyc-taxi-geospatial-data-with-duckdb-h3-and-keplergl-68da908f7397)
