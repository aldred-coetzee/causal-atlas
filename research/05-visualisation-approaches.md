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
15. [Deep Dive: Kepler.gl v3 Architecture](#15-deep-dive-keplergl-v3-architecture)
16. [Deep Dive: DuckDB-WASM + Kepler.gl Under the Hood](#16-deep-dive-duckdb-wasm--keplergl-under-the-hood)
17. [Observable Framework](#17-observable-framework)
18. [Evidence.dev](#18-evidencedev)
19. [Apache Superset](#19-apache-superset)
20. [Streamlit + pydeck](#20-streamlit--pydeck)
21. [SQLRooms Framework](#21-sqlrooms-framework)
22. [Novel Visualisation Ideas for Causal Discovery](#22-novel-visualisation-ideas-for-causal-discovery)
23. [Accessibility Considerations](#23-accessibility-considerations)
24. [Performance Optimisation](#24-performance-optimisation)
25. [PMTiles and Protomaps](#25-pmtiles-and-protomaps)
26. [Causal Atlas-Specific UI/UX Design](#26-causal-atlas-specific-uiux-design)
27. [Interactive Causal Graph Visualisation](#27-interactive-causal-graph-visualisation)
28. [Time Series Visualisation for Causal Analysis](#28-time-series-visualisation-for-causal-analysis)
29. [Map-Based Anomaly Detection Visualisation](#29-map-based-anomaly-detection-visualisation)
30. [Print and Export](#30-print-and-export)

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

## 15. Deep Dive: Kepler.gl v3 Architecture

> **Checked:** March 2025

### 15.1 Redux Store Structure

Kepler.gl's entire state is managed through a centralised Redux store with four primary state domains, each handled by a dedicated subreducer. Understanding this structure is essential for programmatic control of the map.

```
keplerGlReducer
├── visState          -- All data and visualisation state
│   ├── datasets      -- Map of dataset ID -> { fields, allData, filteredIndex, ... }
│   ├── layers        -- Array of layer objects with config, visual channels, data accessors
│   ├── filters       -- Array of filter objects (time, range, select, polygon)
│   ├── interactionConfig  -- Tooltip, brush, coordinate, geocoder settings
│   ├── layerOrder    -- Z-ordering of layers
│   ├── splitMaps     -- Configuration for dual-map view
│   └── animationConfig    -- Playback speed, domain, current time
├── mapState          -- Viewport and base map behaviour
│   ├── latitude, longitude, zoom  -- Camera position
│   ├── bearing, pitch             -- 3D rotation
│   ├── dragRotate                 -- Whether perspective drag is enabled
│   └── isSplit                    -- Split map mode
├── mapStyle          -- Base map appearance
│   ├── styleType     -- Preset style name (dark, light, muted, satellite)
│   ├── mapStyles     -- Custom style definitions (MapLibre style JSON URLs)
│   ├── visibleLayerGroups  -- Toggle labels, roads, buildings, water, land, 3d buildings
│   └── threeDBuildingColor -- Colour for 3D building extrusions
└── uiState           -- UI panel state
    ├── activeSidePanel    -- null | 'layer' | 'filter' | 'interaction' | 'map'
    ├── currentModal       -- null | 'dataTable' | 'addData' | 'exportImage' | etc.
    ├── readOnly           -- Disable all editing UI
    └── mapControls        -- Toggle visibility of zoom, compass, split, fullscreen, etc.
```

Source: [Kepler.gl Reducers Documentation](https://docs.kepler.gl/docs/api-reference/reducers)

### 15.2 Action-Updater Pattern

Each subreducer is assembled from **updater functions**, each mapped to an action type. This pattern allows surgical overriding of any state transition:

```javascript
import { visStateUpdaters } from '@kepler.gl/reducers';
import { createAction } from '@reduxjs/toolkit';

// Override the default layer config change behaviour
const customVisStateReducer = (state, action) => {
  switch (action.type) {
    case 'LAYER_CONFIG_CHANGE':
      // Custom logic before standard update
      console.log('Layer changed:', action.payload);
      return visStateUpdaters.layerConfigChangeUpdater(state, action);
    default:
      return state;
  }
};
```

Key updater functions in `visState`:
- `updateVisDataUpdater` -- adds datasets and creates default layers
- `layerConfigChangeUpdater` -- modifies layer properties (colour, size, opacity)
- `layerVisConfigChangeUpdater` -- changes visual encoding channels
- `setFilterUpdater` -- adds/modifies data filters
- `interactionConfigChangeUpdater` -- configures tooltips, brushing
- `setFilterAnimationTimeUpdater` -- controls time playback position

Source: [Kepler.gl Reducers API](https://docs.kepler.gl/docs/api-reference/reducers), [Kepler.gl Actions API](https://docs.kepler.gl/docs/api-reference/actions/actions)

### 15.3 Programmatic Map Control

To control a Kepler.gl instance programmatically (critical for Causal Atlas), dispatch actions to the store:

```javascript
import { addDataToMap, forwardTo } from '@kepler.gl/actions';

// Add data and full configuration to a specific instance
store.dispatch(
  addDataToMap({
    datasets: {
      info: { id: 'conflict_data', label: 'ACLED Conflicts' },
      data: { fields, rows }  // Column-based format
    },
    config: {
      visState: {
        layers: [{ type: 'point', config: { dataId: 'conflict_data', columns: { lat: 'latitude', lng: 'longitude' } } }],
        filters: [{ dataId: ['conflict_data'], id: 'time_filter', name: ['event_date'], type: 'timeRange' }]
      },
      mapState: { latitude: 2.0, longitude: 40.0, zoom: 5 }  // Centre on East Africa
    },
    options: { centerMap: true, readOnly: false }
  })
);

// Forward actions to a specific kepler.gl instance
store.dispatch(forwardTo('my_map_id', updateMap({ latitude: 0, longitude: 38, zoom: 6 })));
```

**Multi-instance support:** When running multiple `KeplerGl` components (e.g., a comparison view), each has a unique `id` prop. Use `forwardTo(id, action)` to target a specific instance. Actions without forwarding go to the default instance.

Source: [Kepler.gl Get Started](https://docs.kepler.gl/docs/api-reference/get-started), [Kepler.gl All Actions](https://docs.kepler.gl/docs/api-reference/actions/actions)

### 15.4 Creating Custom Layers

Kepler.gl uses deck.gl under the hood, so custom layers must bridge both systems.

**Step 1: Create a deck.gl layer** by extending `CompositeLayer` or a primitive layer:

```javascript
import { CompositeLayer } from '@deck.gl/core';
import { ScatterplotLayer, TextLayer } from '@deck.gl/layers';

class CausalNodeLayer extends CompositeLayer {
  renderLayers() {
    const { data, getPosition, getRadius, getColor, getLabel } = this.props;
    return [
      new ScatterplotLayer(this.getSubLayerProps({
        id: 'nodes',
        data, getPosition, getRadius, getFillColor: getColor
      })),
      new TextLayer(this.getSubLayerProps({
        id: 'labels',
        data, getPosition, getText: getLabel,
        getSize: 12, getColor: [255, 255, 255]
      }))
    ];
  }
}
CausalNodeLayer.layerName = 'CausalNodeLayer';
```

**Step 2: Register in Kepler.gl** by defining a layer class that maps the custom deck.gl layer to Kepler.gl's UI system (specifying which fields/options appear in the side panel). This requires implementing `KeplerGlLayer` with methods like `formatLayerData()`, `renderLayer()`, and `getDefaultLayerConfig()`.

**Note:** Integrating custom deck.gl layers with Kepler.gl's UI is non-trivial. The layer must define its visual channels, column requirements, and interaction behaviour. For complex custom layers (like a causal arc layer with lag encoding), it may be more practical to render them as a separate deck.gl overlay on the same MapLibre base map, outside of Kepler.gl's Redux state.

Source: [deck.gl Custom Composite Layers](https://deck.gl/docs/developer-guide/custom-layers/composite-layers), [Kepler.gl GitHub Issue #370](https://github.com/keplergl/kepler.gl/issues/370)

### 15.5 Component Customisation via Factory Pattern

Kepler.gl provides an `injectComponents` function for replacing internal UI components:

```javascript
import { injectComponents, PanelHeaderFactory } from '@kepler.gl/components';

const CustomPanelHeader = () => <div>Causal Atlas Explorer</div>;
const CustomPanelHeaderFactory = () => CustomPanelHeader;

const KeplerGl = injectComponents([
  [PanelHeaderFactory, CustomPanelHeaderFactory]
]);
```

Replaceable factories include `PanelHeaderFactory`, `MapContainerFactory`, `SidePanelFactory`, `ModalContainerFactory`, and more. This enables Causal Atlas to maintain Kepler.gl's map engine while providing a custom UI shell for causal analysis controls.

---

## 16. Deep Dive: DuckDB-WASM + Kepler.gl Under the Hood

> **Checked:** March 2025

### 16.1 Architecture

The integration uses the `@kepler.gl/duckdb` npm package, which wraps DuckDB-WASM and provides a bridge between SQL query results and Kepler.gl's data model.

```
┌─────────────────────────────────────────────────────────────┐
│  Browser                                                     │
│                                                               │
│  ┌──────────────┐   SQL query    ┌────────────────────┐      │
│  │  SQL Editor   │──────────────>│  DuckDB-WASM        │      │
│  │  (CodeMirror) │               │  (Web Worker)        │      │
│  └──────────────┘               │  ┌──────────────┐   │      │
│                                  │  │ Spatial ext   │   │      │
│                                  │  └──────────────┘   │      │
│                                  └────────┬───────────┘      │
│                                           │ Apache Arrow     │
│                                           │ result table     │
│  ┌──────────────┐   deck.gl data  ┌──────┴───────────┐      │
│  │  Map Canvas   │<───────────────│  Data Converter    │      │
│  │  (WebGL2)     │                │  (Arrow->columns)  │      │
│  └──────────────┘                │  WKB->GeoArrow     │      │
│                                  └────────────────────┘      │
│                                                               │
│  ┌────────────────────────────────┐                          │
│  │  Remote Data (HTTP Range)      │                          │
│  │  S3/GCS GeoParquet files       │                          │
│  └────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### 16.2 How SQL Drives Map Updates

1. **Query execution:** DuckDB-WASM evaluates SQL queries asynchronously in a Web Worker, keeping the main thread (and map rendering) responsive.
2. **Result format:** Results are returned as Apache Arrow tables -- a zero-copy columnar format that avoids serialisation overhead.
3. **Geometry conversion:** For geospatial queries, WKB (Well-Known Binary) geometry output is converted to GeoArrow point/polygon vectors before being passed to deck.gl layers.
4. **Layer creation:** The converted Arrow table is registered as a Kepler.gl dataset, and a layer is automatically created based on detected geometry columns.
5. **Incremental updates:** When the user modifies a SQL query and re-executes, the old dataset is replaced and the layer re-renders.

**Any existing dataset in Kepler.gl is queryable.** If a file named `world-cities.csv` has been loaded, it is accessible as a table: `SELECT * FROM 'world-cities.csv' WHERE population > 1000000`.

### 16.3 Performance Characteristics

Based on the DuckDB-WASM academic paper (Kohn et al., VLDB 2022) and practical benchmarks:

| Operation | Approximate Performance | Notes |
|-----------|------------------------|-------|
| Load 100MB Parquet into DuckDB-WASM | ~2-4 seconds | Depends on browser and network |
| Simple SELECT with WHERE on 10M rows | ~200-500ms | Predicate pushdown on Parquet row groups |
| GROUP BY aggregation on 1M rows | ~100-300ms | Vectorised execution in WASM |
| Spatial join (ST_Within) on 100K polygons | ~1-3 seconds | Spatial extension + R-tree index |
| HTTP Range Request to remote Parquet | ~50-200ms per request | Only fetches needed byte ranges |
| TPC-H SF1 benchmark (1GB) | Competitive with native DuckDB | ~2-3x slower than native on average |

**Memory limits:** Modern browsers allocate up to 2-4 GB to a WASM module. For datasets exceeding ~500MB, use Parquet with HTTP range requests to avoid loading everything into memory. Spatially partitioned GeoParquet files are ideal -- DuckDB reads only the partitions matching the query's spatial predicate.

**Concurrency:** DuckDB-WASM runs in a dedicated Web Worker. Multiple queries are serialised but do not block the main thread. For Causal Atlas, this means the map remains interactive while a correlation query runs in the background.

Source: [DuckDB-WASM Paper (VLDB 2022)](https://dl.acm.org/doi/abs/10.14778/3554821.3554847), [DuckDB WASM Documentation](https://duckdb.org/docs/stable/clients/wasm/overview), [Kepler.gl SQL Data Explorer](https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/sql-data-explorer.md)

### 16.4 SQLRooms: The Framework Behind This Integration

Foursquare has extracted the DuckDB + Kepler.gl integration pattern into an open-source framework called **SQLRooms** (https://sqlrooms.org/). SQLRooms provides building blocks for React analytics applications powered by DuckDB-WASM:

- **DuckDB wrapper** that auto-detects file formats (CSV, Parquet, JSON, Arrow), infers schemas, and registers tables
- **State management** via Zustand stores connected to DuckDB instances
- **Kepler.gl integration** for geospatial rendering
- **Native GeoParquet, PMTiles support** for cloud-native geospatial workflows
- **LLM assistant integration** for natural language to SQL

Each "Room" is connected to a DuckDB instance (native on device or WASM in browser). This architecture enables complex spatial queries on multi-GB datasets without cloud compute dependence.

**Relevance to Causal Atlas:** SQLRooms could serve as the foundation for our frontend, providing the DuckDB-Kepler.gl integration out of the box. We would add our custom causal analysis layers, time-series panels, and AI interpretation components on top.

Source: [SQLRooms GitHub](https://github.com/sqlrooms/sqlrooms), [Foursquare SQLRooms Announcement](https://foursquare.com/resources/blog/products/foursquare-introduces-sqlrooms/), [SQLRooms Examples](https://sqlrooms.org/examples.html)

---

## 17. Observable Framework

> **Checked:** March 2025

**Repository:** https://github.com/observablehq/framework
**Documentation:** https://observablehq.com/framework/
**Licence:** ISC
**Current version:** 1.x (as of March 2025)

### 17.1 What It Is

Observable Framework is an open-source static site generator purpose-built for data apps, dashboards, and reports. Unlike a traditional SPA (Single Page Application), Framework produces static HTML with embedded reactive JavaScript -- data is precomputed at build time and the runtime is minimal.

### 17.2 Architecture

```
Build time (server / CI):
  data-loaders/
    rainfall.py    -- Python script that queries CHIRPS, outputs JSON
    conflicts.sql  -- SQL query against DuckDB, outputs CSV
    food_prices.R  -- R script that calls WFP API

  ↓  Executed at build time, outputs cached as static files

docs/
  index.md         -- Markdown + reactive JavaScript
  analysis.md      -- Uses Plot, D3, Mosaic for visualisations
  _data/           -- Cached loader outputs (JSON, CSV, Parquet)

  ↓  Compiled to static HTML + JS

dist/
  index.html       -- Instant-loading data dashboard
  analysis.html
  _data/           -- Bundled data snapshots
```

### 17.3 Key Features for Causal Atlas

| Feature | Description | Relevance |
|---------|-------------|-----------|
| **Data loaders in any language** | Python, R, SQL, shell scripts run at build time | Our Python adapters can serve as data loaders |
| **Reactive JavaScript** | Variables are reactive cells (like Observable notebooks) | Interactive controls update charts instantly |
| **Built-in libraries** | Observable Plot, D3, Mosaic, Vega-Lite, Leaflet, Mermaid | Rich visualisation without dependency management |
| **Static output** | No server required at runtime | Can host on GitHub Pages or any static host |
| **File-based routing** | Each `.md` file becomes a page | Natural mapping for per-region or per-analysis pages |
| **Data snapshots** | Loaders cache outputs; site loads instantly | Users see results without waiting for API calls |

### 17.4 Map Integration with Observable Framework

Brandon Liu (PMTiles creator) has demonstrated combining Observable Framework with Protomaps/PMTiles for static-site map applications (https://github.com/bdon/observable-framework-maps). The pattern:

1. Data loader produces PMTiles file from geospatial data at build time
2. MapLibre GL JS renders the tiles client-side
3. Reactive JavaScript handles user interaction (selection, filtering)
4. D3/Observable Plot renders linked charts

### 17.5 Assessment for Causal Atlas

**Strengths:**
- Perfect for publishing reproducible analyses ("Here's what we found about drought-conflict links in East Africa")
- Data loaders can run DuckDB queries against our Parquet files
- No backend infrastructure for read-only dashboards
- Excellent developer experience for data-literate researchers

**Limitations:**
- Not suitable for the interactive exploration app (no write operations, no authentication)
- Build-time data means analyses are snapshots, not live queries
- Limited to JavaScript for client-side interactivity (no Python in browser)

**Verdict:** Excellent complementary tool for publishing Causal Atlas findings as static reports and exploration guides. Not a replacement for the core interactive application.

Source: [Observable Framework](https://observablehq.com/framework/), [Observable Framework GitHub](https://github.com/observablehq/framework), [Observable Framework Maps Demo](https://github.com/bdon/observable-framework-maps)

---

## 18. Evidence.dev

> **Checked:** March 2025

**Website:** https://evidence.dev/
**Documentation:** https://docs.evidence.dev/
**Licence:** MIT
**Language:** JavaScript/Svelte

### 18.1 What It Is

Evidence is an open-source framework for building data products with SQL. You write Markdown interspersed with SQL queries and component tags, and Evidence renders interactive, responsive dashboards as static sites.

### 18.2 How It Works

```markdown
# Conflict Events by Region

```sql monthly_events
SELECT region, date_trunc('month', event_date) as month,
       COUNT(*) as events, SUM(fatalities) as fatalities
FROM acled_events
GROUP BY region, month
ORDER BY month
```

<LineChart data={monthly_events} x=month y=events series=region />

The events peaked in {monthly_events[0].region} during
{monthly_events[0].month} with {monthly_events[0].events} events.
```

### 18.3 Geospatial Capabilities

Evidence has built-in map components (as of 2025):

| Component | Description | Limitation |
|-----------|-------------|------------|
| `<USMap>` | Choropleth of US states | US-only |
| `<AreaMap>` | Choropleth for custom GeoJSON boundaries | Requires GeoJSON input |
| `<PointMap>` | Scatter points on a map | Basic, no deck.gl |
| `<BubbleMap>` | Sized circles on a map | Limited styling options |
| `<BaseMap>` | Custom Leaflet-based map | More flexibility but Leaflet performance limits |

### 18.4 Assessment for Causal Atlas

**Strengths:**
- SQL-first workflow aligns with our DuckDB backend
- Beautiful default styling, responsive out of the box
- Supports DuckDB as a data source (can query Parquet files directly)
- Markdown authoring is accessible to researchers

**Limitations:**
- Map components are basic -- no deck.gl, no WebGL, no time playback
- Cannot render 100K+ points (Leaflet-based, not WebGL)
- No custom visualisation components (no bivariate choropleth, no causal arcs)
- Svelte-based -- does not integrate with React/Kepler.gl ecosystem
- No DuckDB-WASM (queries run at build time or against a database connection)

**Verdict:** Not suitable as the primary Causal Atlas interface due to limited geospatial capabilities. Could be useful for generating simple SQL-driven reports from our data, but Observable Framework is a better fit for that use case given its richer visualisation library support.

Source: [Evidence.dev Documentation](https://docs.evidence.dev/), [Evidence.dev US Map Component](https://docs.evidence.dev/components/maps/us-map)

---

## 19. Apache Superset

> **Checked:** March 2025

**Repository:** https://github.com/apache/superset
**Licence:** Apache 2.0
**Language:** Python (backend) + React/TypeScript (frontend)

### 19.1 Overview

Apache Superset is an open-source data exploration and visualisation platform. It supports a wide range of chart types, SQL-based exploration, role-based access control, and dashboard composition. It connects to dozens of database backends including PostgreSQL/PostGIS, DuckDB, BigQuery, and ClickHouse.

### 19.2 Geospatial Capabilities

Superset includes several deck.gl-powered chart types:

| Chart Type | deck.gl Layer | Capabilities |
|------------|--------------|--------------|
| **deck.gl Scatter** | ScatterplotLayer | Point markers with size/colour encoding |
| **deck.gl Screen Grid** | ScreenGridLayer | Grid aggregation (like a heatmap) |
| **deck.gl Grid** | GridLayer | 3D extruded grid cells |
| **deck.gl Hex** | HexagonLayer | Hexagonal aggregation |
| **deck.gl Arc** | ArcLayer | Origin-destination arcs |
| **deck.gl Path** | PathLayer | Line/route rendering |
| **deck.gl Polygon** | PolygonLayer | Choropleth maps from GeoJSON |
| **deck.gl Heatmap** | HeatmapLayer | Continuous intensity surface |
| **deck.gl GeoJSON** | GeoJsonLayer | Points, lines, polygons from GeoJSON |
| **Mapbox Choropleth** | Country/region choropleths | ISO-based country mapping |

**Requirements:** All deck.gl charts in Superset require a Mapbox API key for the base map (as of March 2025). There is an open feature request for MapLibre support, but it has not been merged.

### 19.3 Assessment for Causal Atlas

**Strengths:**
- Comprehensive BI platform with dashboards, access control, caching
- deck.gl-based maps handle large datasets
- DuckDB connector available
- Rich SQL exploration (SQL Lab) with query history and saved queries
- Role-based access control for multi-user environments

**Limitations:**
- No time playback animation on maps
- No custom deck.gl layers (limited to the built-in chart types)
- Mapbox dependency for base maps (API cost)
- Heavy infrastructure requirements (PostgreSQL metadata DB, Redis, Celery)
- Complex deployment compared to our lightweight DuckDB + Parquet approach
- No causal-specific visualisations
- The polygon layer does not support text labels or annotations

**Verdict:** Superset is overkill for MVP and misaligned with our lightweight, file-based architecture. However, it could be relevant in a later phase if Causal Atlas needs a full BI layer for multi-user dashboards with access control. For now, the Kepler.gl + DuckDB-WASM approach is a better fit.

Source: [Apache Superset Spatial Analytics](https://medium.com/@saikrishna_17904/spatial-analytics-on-apache-superset-fdbfb1ebdeb1), [Superset Geospatial Guide](https://preset.io/blog/2021-02-11-superset-geodata/), [Superset GitHub](https://github.com/apache/superset)

---

## 20. Streamlit + pydeck

> **Checked:** March 2025

**Streamlit docs:** https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
**pydeck docs:** https://deckgl.readthedocs.io/

### 20.1 Overview

Streamlit is a Python framework for building data apps with minimal frontend code. `st.pydeck_chart` integrates deck.gl (via the pydeck Python wrapper) for 3D geospatial visualisation directly in Streamlit apps.

### 20.2 Capabilities

```python
import streamlit as st
import pydeck as pdk
import duckdb

# Query PRIO-GRID data from Parquet
con = duckdb.connect()
df = con.execute("""
    SELECT gid, lat, lon, value
    FROM read_parquet('data/domain=conflict/year=2023/*.parquet')
    WHERE variable_name = 'acled_fatalities'
""").fetchdf()

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(latitude=2.0, longitude=40.0, zoom=5, pitch=45),
    layers=[
        pdk.Layer(
            'GridCellLayer',
            data=df,
            get_position=['lon', 'lat'],
            get_elevation='value',
            elevation_scale=100,
            cell_size=55000,  # ~0.5 degrees at equator
            get_fill_color='[255, value * 2, 0, 180]',
            pickable=True
        )
    ]
))
```

### 20.3 Supported Layer Types

pydeck wraps all deck.gl layers: ScatterplotLayer, HexagonLayer, GridCellLayer, ArcLayer, PathLayer, PolygonLayer, HeatmapLayer, TextLayer, IconLayer, ColumnLayer, TripsLayer, and more. Custom layers can be loaded from external JavaScript bundles.

### 20.4 Assessment for Causal Atlas

**Strengths:**
- Pure Python -- lowest barrier to entry for researchers
- Rapid prototyping (a working map in 10 lines of code)
- Integrates with DuckDB, pandas, polars natively
- deck.gl rendering handles moderate data volumes (50K-500K points)
- 3D extrusion for showing variable magnitudes
- Community-contributed geospatial widgets (st-folium, streamlit-keplergl)

**Limitations:**
- No built-in time playback (must implement with st.slider + rerun loop)
- Re-renders entire app on each interaction (not reactive like Observable)
- Limited layout control compared to a custom React app
- Server-side Python required (not static, not client-side)
- Challenging to create complex linked-view layouts
- State management is session-based, not URL-shareable by default

**Verdict:** Excellent for the research/prototyping phase. Build Streamlit apps to validate data integration, test correlation calculations, and prototype map views before investing in the React application. Not suitable as the production frontend.

**Recommended prototyping workflow:**
1. Streamlit + pydeck for quick spatial exploration of individual datasets
2. Streamlit + plotly for time-series and correlation analysis
3. Port validated patterns to React + Kepler.gl for the production app

Source: [Streamlit pydeck_chart API](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart), [pydeck Documentation](https://deckgl.readthedocs.io/), [Streamlit Geospatial Multi-Layer Tutorial](https://quickstarts.snowflake.com/guide/building-geospatial-mult-layer-apps-with-snowflake-and-streamlit/)

---

## 21. SQLRooms Framework

> **Checked:** March 2025

(Covered in detail in Section 16.4. Summary here for completeness.)

**Repository:** https://github.com/sqlrooms/sqlrooms
**Licence:** MIT
**Maintained by:** Foursquare
**Stack:** React + Zustand + DuckDB-WASM + Kepler.gl

SQLRooms is the recommended starting point for the Causal Atlas frontend. It provides:

- Pre-built "rooms" (composable UI panels) for SQL editing, data tables, charts, and maps
- DuckDB-WASM integration with automatic schema detection
- Kepler.gl rendering for geospatial data
- Extensible architecture for adding custom rooms (our causal analysis panels)
- Example applications demonstrating spatial analytics workflows

The framework was presented at FOSDEM 2026 for scaling mobility flow visualisation with DuckDB, Flowmap.gl, and SQLRooms -- demonstrating its maturity for production spatial analytics.

Source: [SQLRooms GitHub](https://github.com/sqlrooms/sqlrooms), [SQLRooms Case Studies](https://sqlrooms.org/case-studies.html), [FOSDEM 2026 SQLRooms Talk](https://fosdem.org/2026/schedule/event/DC9M73-sqlrooms-flowmap/)

---

## 22. Novel Visualisation Ideas for Causal Discovery

> **Checked:** March 2025

These are original visualisation concepts designed for Causal Atlas, informed by academic research on causal visualisation and spatial data representation.

### 22.1 Causal Graph Overlaid on Map

**Concept:** A directed graph where nodes are grid cells (or admin regions) and edges are discovered causal links, rendered directly on a geographic map.

**Design:**
```
┌──────────────────────────────────────┐
│   Map (East Africa)                  │
│                                       │
│     [Turkana]──drought→──[Lodwar]    │
│        │                    │         │
│    food_price↗          conflict↑    │
│        │                    │         │
│     [Marsabit]──────────[Moyale]     │
│                                       │
│   Node size = number of causal links  │
│   Edge width = strength (F-stat)      │
│   Edge colour = positive/negative     │
│   Edge label = "var_a → var_b, lag=N" │
└──────────────────────────────────────┘
```

**Implementation strategy:**
- Nodes: deck.gl `ScatterplotLayer` with size encoding = degree centrality
- Edges: deck.gl `ArcLayer` with width = effect strength, colour = direction
- Labels: deck.gl `TextLayer` on hover/click
- Layout: Geographic positions (cell centroids) -- no force-directed layout needed
- Interactivity: Click node to see all causal relationships; click edge for detail panel

**Academic precedent:** Schottler et al. (2021) survey geospatial network visualisation techniques, identifying the "node-link on map" approach as most effective when geographic position is meaningful (which it is for spatially-embedded causal relationships). The key challenge is edge crossing -- mitigated by showing only edges above a significance threshold and using edge bundling.

Source: [Geospatial Network Visualisation Survey (Schottler 2021)](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.14198), [pywhy-graphs Causal Graph Visualization](https://www.pywhy.org/pywhy-graphs/stable/auto_examples/intro/intro_causal_graphs.html)

### 22.2 Causal Heatmap

**Concept:** A grid-cell choropleth where colour intensity represents the strength of the causal effect between two user-selected variables.

**Design:**
- User selects Variable A (e.g., rainfall deficit) and Variable B (e.g., conflict fatalities)
- For each grid cell, compute the time-lagged correlation (or Granger F-statistic)
- Render as a heatmap: hot colours = strong positive causal link, cool colours = strong negative, neutral = no significant link
- A second encoding (hatching, opacity) shows statistical significance (p < 0.05 vs. not significant)
- Slider controls the lag window (0 to 12 months)

**Interactive lag explorer extension:**
- The slider controls the lag parameter
- As the user drags the slider, the heatmap updates in real-time (precomputed for all lags)
- A linked line chart shows how the average correlation changes with lag
- The "optimal lag" is highlighted with a marker on the slider

**Implementation:**
- Precompute correlations for all cell-variable-lag combinations and store in Parquet
- Load into DuckDB-WASM; SQL query filters by variable pair and lag
- Render with deck.gl `GridCellLayer` or `SolidPolygonLayer` (for PRIO-GRID cells)
- Use Apache Arrow for zero-copy transfer between DuckDB-WASM and deck.gl

### 22.3 Animated Causal Propagation

**Concept:** An animation showing how a "shock" (e.g., drought onset, price spike, conflict outbreak) spreads spatially over time, following discovered causal pathways.

**Design:**
- Frame 0: The origin cell lights up (e.g., drought onset detected)
- Frame 1 (lag = 1 month): Adjacent cells with detected 1-month causal links light up (e.g., food prices rise)
- Frame 2 (lag = 2 months): Cells with 2-month lagged effects activate
- ... and so on, showing the "causal wavefront" spreading across the map
- Ripple animation emanating from the origin cell, with wavefront speed proportional to lag
- Cells that are NOT causally linked remain unchanged

**Academic precedent:** Elmqvist et al. introduced "Growing Squares" -- an animated visualisation technique for causal relations using the metaphor of colour pools spreading over time. Their user study found it significantly faster and more efficient than static Hasse diagram representations for understanding causal chains. A later extension, "Growing Polygons," used partitioned polygons with colour-coded segments showing dependencies. These techniques have been validated for both small and large causal system executions.

**Implementation:**
- deck.gl `TripsLayer` variant with custom trail rendering
- Each "trip" represents a causal pathway from origin to affected cell
- Trail length proportional to lag duration
- Colour encodes the type of causal link (climate->food, food->conflict, etc.)
- Alternatively: custom WebGL shader that animates a radial gradient expanding from each affected cell

A 2024 ACM paper on "Spatio-Causal Situation Awareness" proposes exactly this kind of visualisation for monitoring and forecasting causal cascades in geospatial settings.

Source: [Growing Squares (Elmqvist et al.)](http://users.umiacs.umd.edu/~elm/projects/causality/causalviz.pdf), [Spatio-Causal Situation Awareness (ACM 2024)](https://dl.acm.org/doi/10.1145/3672556)

### 22.4 Interactive Lag Explorer

**Concept:** A dedicated panel where the user selects two variables, and an interactive visualisation shows how their correlation changes as a function of temporal lag.

**Design:**
```
┌──────────────────────────────────────────────────┐
│  Variable A: [CHIRPS Rainfall ▼]                  │
│  Variable B: [ACLED Fatalities ▼]                 │
│  Region: [Selected on map / All East Africa ▼]    │
│                                                    │
│  ┌────────────────────────────────────────────┐   │
│  │  Correlation                                │   │
│  │   0.8│                                      │   │
│  │   0.4│    ╭──╮                              │   │
│  │   0.0│───╯    ╰──────────────────────      │   │
│  │  -0.4│                                      │   │
│  │  -0.8│                                      │   │
│  │      └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬   │   │
│  │         0  1  2  3  4  5  6  7  8  9 10    │   │
│  │                Lag (months)                 │   │
│  │  ★ Peak: r=0.71, lag=3 months, p<0.001     │   │
│  └────────────────────────────────────────────┘   │
│                                                    │
│  Lag: [====●==================] 3 months           │
│  (Drag slider to update causal heatmap on map)     │
└──────────────────────────────────────────────────┘
```

**Linked behaviour:**
- Dragging the lag slider updates the causal heatmap (Section 22.2) on the map
- Clicking the peak correlation point centres the map on the region with strongest effect
- The confidence interval widens at larger lags (fewer overlapping observations)

### 22.5 Counterfactual Map

**Concept:** A split-view or toggle-able map showing "what happened" vs. "what would have happened without X" -- visualising the estimated causal effect of an intervention or event.

**Design:**
- **Left panel:** Observed reality (actual food prices, actual conflict events)
- **Right panel:** Counterfactual scenario (estimated food prices if drought had not occurred)
- **Difference overlay:** Colour encodes the gap between observed and counterfactual (the estimated causal effect)
- **Swipe divider:** User drags a vertical line to reveal/hide the counterfactual

**Academic precedent:** Wang, Borland & Gotz (2024, 2025) developed a framework for counterfactual visualisation operators -- visual analytics methods that enhance causal inference by showing what would have happened under alternative conditions. Their empirical study found that counterfactual visualisation significantly improves users' ability to correctly identify causal relationships vs. mere correlations. Pearl's causal hierarchy (association -> intervention -> counterfactual) places counterfactual reasoning at the highest level of causal understanding.

**Implementation:**
- Requires a causal model (not just correlations) -- structural equation model or difference-in-differences estimator
- deck.gl `SolidPolygonLayer` with two data sources, rendered side-by-side using `MapView` with linked viewports
- The swipe divider is a CSS overlay controlling the clip path of the second map
- Computationally intensive (requires fitting causal model per grid cell) -- results should be precomputed server-side

**Use case example:** "What would food prices in Turkana have been in Q3 2023 if the March-May 2023 rainy season had been normal?" The counterfactual map shows estimated prices without the drought shock, while the actual map shows observed prices. The difference is the estimated causal effect of the drought on food prices.

Source: [Counterfactual Visualization Framework (Wang et al. 2025)](https://journals.sagepub.com/doi/full/10.1177/14738716241265120), [Counterfactual Visualization User Study (Wang et al. 2024)](https://arxiv.org/abs/2401.08822), [VACLab Counterfactual Project](https://vaclab.unc.edu/project/counterfactuals/)

### 22.6 Multi-Panel Synchronised Views

**Concept:** A dashboard layout with four linked panels that all respond to the same selection and time position:

```
┌─────────────────────────┬─────────────────────────┐
│                         │                          │
│    MAP VIEW             │    TIME-SERIES PANEL     │
│    (Kepler.gl)          │    (Plotly/Recharts)     │
│    - Causal heatmap     │    - All variables for   │
│    - Selected cell      │      selected cell       │
│      highlighted        │    - Lag markers shown   │
│                         │                          │
├─────────────────────────┼─────────────────────────┤
│                         │                          │
│    CAUSAL GRAPH         │    DATA TABLE            │
│    (D3.js force layout) │    (AG Grid/TanStack)    │
│    - Nodes = variables  │    - Raw data for        │
│    - Edges = causal     │      selected cell       │
│      links with lag     │    - Sortable, filterable │
│    - Click edge to      │    - Export to CSV       │
│      highlight on map   │                          │
│                         │                          │
└─────────────────────────┴─────────────────────────┘
```

**Synchronisation mechanism:**
- Zustand store holds `selectedCellId`, `selectedTimeRange`, `selectedVariables`
- All four panels subscribe to these values
- Any panel can update the shared state (map click, chart selection, table row click)
- URL encodes the state for shareability

This is the primary dashboard layout for the Causal Atlas production application.

---

## 23. Accessibility Considerations

> **Checked:** March 2025

### 23.1 WCAG Compliance for Maps

Interactive maps present significant accessibility challenges. A 2025 systematic evaluation of digital map tools against WCAG 2.1 found that only one tool achieved full compliance; most lacked adequate text alternatives, proper contrast, and keyboard operability. We must do better.

**Applicable WCAG 2.1 criteria for Causal Atlas:**

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| **1.1.1 Non-Text Content** | All non-text content has a text alternative | Provide `aria-label` on map container; generate text summary of visible data |
| **1.4.1 Use of Color** | Colour is not the sole means of conveying information | Add patterns, labels, or symbols alongside colour encoding |
| **1.4.3 Contrast (Minimum)** | Text: 4.5:1, large text: 3:1 contrast ratio | Use WCAG-compliant text colours; avoid light text on map backgrounds |
| **1.4.11 Non-text Contrast** | UI components and graphics: 3:1 contrast ratio | Ensure map markers, grid cell borders visible against all base maps |
| **2.1.1 Keyboard** | All functionality operable via keyboard | Tab through map controls, arrow keys for panning, +/- for zoom |
| **2.4.7 Focus Visible** | Keyboard focus indicator visible | Custom focus ring on map controls and interactive elements |
| **4.1.2 Name, Role, Value** | All UI components have accessible name and role | ARIA roles on custom components (slider, map controls) |

Source: [WCAG 2.1 Map Evaluation (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12094671/)

### 23.2 Colourblind-Safe Palettes

Approximately 8% of males and 0.5% of females have colour vision deficiency. Our palettes must work for all common types:

**Recommended palettes:**

| Use Case | Palette | Source |
|----------|---------|--------|
| **Sequential** (single variable, low to high) | Viridis, Magma, Cividis | Matplotlib; designed for perceptual uniformity and CVD safety |
| **Diverging** (positive/negative) | Blue-Red via white (Cividis-based) | Custom; avoid green-red |
| **Categorical** (event types) | Wong (2011) 8-colour palette | Nature Methods; safe for all CVD types |
| **Bivariate** (two variables) | Purple-Green (Stevens) or Blue-Orange | Joshua Stevens; tested for CVD |

**Design strategies:**
- Use [ColorBrewer](https://colorbrewer2.org/) with "colourblind safe" filter for choropleth palettes
- Add **double-border ("Oreo border")** technique on map features: outer line black, inner line white -- ensures 11:1+ contrast regardless of background
- Supplement colour with **icons, patterns, or hatching** for categorical data
- Provide a "High Contrast" mode toggle that switches to maximum-differentiation palettes
- Include a colourblind simulation preview (like Chrome DevTools) in developer testing

Source: [ColorBrewer](https://colorbrewer2.org/), [Esri Colourblind Readability Guide](https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/designing-maps-for-colorblind-readability/), [Salesforce Colourblind-Friendly Maps](https://www.salesforce.com/blog/how-we-designed-salesforce-maps-to-be-color-blind-friendly/)

### 23.3 Screen Reader Support

Maps are inherently visual, but we can provide non-visual access:

- **Text summary panel:** "This map shows 3,600 grid cells in East Africa. The highest conflict intensity (234 events) is in cell 18234 (Turkana, Kenya). Rainfall is 45% below average in 12% of cells."
- **Data table alternative:** Every map view has a corresponding data table with the same information, accessible by screen readers
- **Keyboard navigation:** Tab to map area -> arrow keys navigate between grid cells -> Enter selects a cell -> screen reader announces cell values
- **Live region updates:** When time playback is active, use `aria-live="polite"` to announce time step changes
- **Alt text on exported images:** AI-generated descriptions of map snapshots using Claude API

### 23.4 Motion and Animation

- Respect `prefers-reduced-motion` CSS media query
- Disable auto-playing animations by default
- Provide manual step-through as alternative to animated playback
- Ensure time scrubbing works without animation (jump between time steps)

---

## 24. Performance Optimisation

> **Checked:** March 2025

### 24.1 Vector Tiles and Data-Driven Styling

For rendering 259,200 PRIO-GRID cells globally, vector tiles are essential. Sending all cells as GeoJSON would be ~100MB; vector tiles reduce this to ~5-10MB of tiled data, loaded progressively.

**Pipeline for grid-to-vector-tiles:**

```
GeoParquet (PRIO-GRID cells + variable values)
    ↓  tippecanoe or ogr2ogr
MVT (Mapbox Vector Tiles) or PMTiles
    ↓  served via HTTP / CDN
MapLibre GL JS / deck.gl MVTLayer
    ↓  data-driven styling
Rendered map (colour = variable value)
```

**Tippecanoe** (by Felt/Mapbox) is the standard tool for creating vector tilesets from GeoJSON. It handles simplification, tile size budgets, and zoom-level management. For our 0.5-degree grid:

```bash
tippecanoe -z10 -Z3 -o grid.pmtiles \
  --no-feature-limit --no-tile-size-limit \
  --detect-shared-borders \
  grid_with_values.geojson
```

### 24.2 Progressive Loading Strategy

```
Zoom level 0-4:   Country-level aggregates (pre-computed, ~200 features)
Zoom level 5-7:   1-degree grid (quarter of PRIO-GRID, ~64,800 cells)
Zoom level 8-10:  0.5-degree PRIO-GRID (full resolution, ~259,200 cells)
Zoom level 11+:   Sub-grid data if available (0.05 degree, ~93M cells -- on demand only)
```

**Level-of-detail (LOD) transitions:**
- Use MapLibre GL JS `minzoom`/`maxzoom` on tile layers for smooth transitions
- Pre-aggregate to coarser grids at build time; store as separate tilesets
- DuckDB-WASM queries switch resolution based on current zoom level

### 24.3 WebGL2 Considerations

deck.gl v9+ uses WebGL2 as the primary rendering backend (with WebGPU experimental support):

- **Instanced rendering:** All point/grid layers use GPU instancing -- one draw call for thousands of grid cells
- **Texture-based data:** Large datasets can be encoded as textures (data textures) for GPU-side lookups
- **Shader-based styling:** Colour mapping happens on GPU, not in JavaScript -- critical for 200K+ cells
- **Frame budget:** Target 16.6ms per frame (60fps). Profile with browser DevTools Performance tab.

**Performance benchmarks (deck.gl v9, M2 MacBook Pro):**

| Layer Type | Feature Count | FPS (panning) | Notes |
|------------|--------------|---------------|-------|
| ScatterplotLayer | 1M points | 58-60 | GPU instanced |
| SolidPolygonLayer | 100K polygons | 45-55 | Depends on vertex count |
| GridCellLayer | 260K cells | 50-58 | Good fit for PRIO-GRID |
| ArcLayer | 50K arcs | 40-50 | CPU-bound arc calculation |
| HeatmapLayer | 500K points | 55-60 | GPU texture-based |

### 24.4 Data Transfer Optimisation

| Strategy | Reduction | Implementation |
|----------|-----------|----------------|
| **Parquet columnar reads** | Read only needed columns | DuckDB-WASM column projection |
| **HTTP Range Requests** | Read only needed byte ranges | DuckDB-WASM + remote Parquet |
| **Spatial partitioning** | Skip irrelevant partitions | GeoParquet with bbox metadata |
| **Arrow IPC** | Zero-copy data transfer | DuckDB-WASM -> deck.gl via Arrow |
| **Compression** | 5-10x size reduction | Parquet ZSTD compression |
| **CDN caching** | Eliminate repeat downloads | PMTiles on CloudFront/R2 |
| **Service Worker cache** | Offline support | Cache tiles and recent queries |

Source: [MapLibre Performance Optimisation](https://maplibre.org/maplibre-gl-js/docs/guides/large-data/), [MapLibre Performance Techniques](https://deepwiki.com/maplibre/maplibre-gl-js/5.2-performance-optimization-techniques)

---

## 25. PMTiles and Protomaps

> **Checked:** March 2025

**Repository:** https://github.com/protomaps/PMTiles
**Website:** https://protomaps.com/
**Specification:** https://docs.protomaps.com/pmtiles/
**Licence:** BSD 3-Clause

### 25.1 What PMTiles Is

PMTiles is a single-file archive format for tiled geospatial data addressed by Z/X/Y coordinates. Instead of storing millions of individual tile files on a file server, all tiles are packed into a single `.pmtiles` file. Clients fetch individual tiles using **HTTP Range Requests** -- reading only the bytes for the specific tile they need.

The archive uses a **Hilbert curve ordering** of tiles, which groups spatially nearby tiles together in the file. This means a single HTTP Range Request often fetches several useful tiles at once, improving cache efficiency.

### 25.2 How It Works

```
Traditional tile serving:
  Client requests /tiles/5/16/12.mvt
  → Server looks up file on disk
  → Returns tile data

PMTiles:
  Client requests Range: bytes=23456-23890 from grid.pmtiles
  → Static file server (S3, R2, CDN) returns those bytes
  → Client parses tile from the byte range
  → No tile server required
```

**Key advantages:**
- **Zero server infrastructure** -- host on any static file service (S3, Cloudflare R2, GitHub Pages)
- **Internal deduplication** -- reduces file size by 70%+ for global vector basemaps
- **Single file to upload** -- no managing millions of tile files
- **Supports raster and vector tiles** -- usable for both basemaps and data layers
- **MapLibre GL JS protocol** -- `pmtiles://` protocol handler integrates natively

### 25.3 Creating PMTiles for PRIO-GRID Data

```bash
# Step 1: Convert PRIO-GRID GeoParquet to GeoJSON (one-time)
duckdb -c "
  COPY (
    SELECT gid, value, ST_AsGeoJSON(geometry) as geometry
    FROM read_parquet('data/domain=conflict/year=2023/acled_fatalities.parquet')
  ) TO 'grid_conflict_2023.geojson' (FORMAT JSON);
"

# Step 2: Create PMTiles with tippecanoe
tippecanoe -z10 -Z2 -o grid_conflict_2023.pmtiles \
  --no-feature-limit \
  --no-tile-size-limit \
  --detect-shared-borders \
  --coalesce-densest-as-needed \
  grid_conflict_2023.geojson

# Step 3: Upload to static storage
aws s3 cp grid_conflict_2023.pmtiles s3://causal-atlas-tiles/

# Step 4: Use in MapLibre
# pmtiles://https://causal-atlas-tiles.s3.amazonaws.com/grid_conflict_2023.pmtiles
```

### 25.4 Integration with MapLibre GL JS

```javascript
import maplibregl from 'maplibre-gl';
import { Protocol } from 'pmtiles';

const protocol = new Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      'prio-grid': {
        type: 'vector',
        url: 'pmtiles://https://cdn.causal-atlas.org/grid_2023.pmtiles'
      }
    },
    layers: [{
      id: 'grid-fill',
      type: 'fill',
      source: 'prio-grid',
      'source-layer': 'default',
      paint: {
        'fill-color': ['interpolate', ['linear'], ['get', 'value'],
          0, '#f7fbff', 10, '#6baed6', 50, '#08306b'
        ],
        'fill-opacity': 0.7
      }
    }]
  }
});
```

### 25.5 Cost Comparison

| Approach | Monthly Cost (global PRIO-GRID, ~10K users) | Setup Complexity |
|----------|---------------------------------------------|------------------|
| Mapbox vector tiles | $200-500/month (tile API costs) | Low |
| Self-hosted tile server (Martin/Tegola) | $50-100/month (EC2/VPS) | Medium |
| PMTiles on S3 + CloudFront | $5-15/month (storage + bandwidth) | Low |
| PMTiles on Cloudflare R2 | $1-5/month (no egress fees) | Low |
| PMTiles on GitHub Pages | $0/month (public repos) | Very low |

**PMTiles is the clear winner for Causal Atlas:** near-zero cost, no server to maintain, and compatible with our MapLibre + deck.gl stack.

### 25.6 Limitations

- **No dynamic data:** PMTiles are static -- rebuilding tiles requires re-running tippecanoe
- **File size:** A full global PRIO-GRID tileset with 50 variables would be large (~500MB-2GB). Solution: separate PMTiles per variable or variable group.
- **No server-side filtering:** Unlike a tile server (Martin, PostGIS), PMTiles cannot filter data on the fly. Solution: use data-driven styling in MapLibre to filter client-side, or use DuckDB-WASM for complex queries.

Source: [PMTiles Concepts](https://docs.protomaps.com/pmtiles/), [PMTiles GitHub](https://github.com/protomaps/PMTiles), [Protomaps](https://protomaps.com/), [Simon Willison PMTiles Tutorial](https://til.simonwillison.net/gis/pmtiles)

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

### Additional Tools and Frameworks (Section 15-25)
- [Kepler.gl Reducers API](https://docs.kepler.gl/docs/api-reference/reducers)
- [Kepler.gl Actions API](https://docs.kepler.gl/docs/api-reference/actions/actions)
- [deck.gl Custom Composite Layers](https://deck.gl/docs/developer-guide/custom-layers/composite-layers)
- [deck.gl Layer Extensions](https://deck.gl/docs/developer-guide/custom-layers/layer-extensions)
- [Kepler.gl Custom Layer Integration (GitHub Issue #370)](https://github.com/keplergl/kepler.gl/issues/370)
- [DuckDB-WASM Paper (Kohn et al., VLDB 2022)](https://dl.acm.org/doi/abs/10.14778/3554821.3554847)
- [DuckDB WASM Documentation](https://duckdb.org/docs/stable/clients/wasm/overview)
- [SQLRooms GitHub](https://github.com/sqlrooms/sqlrooms)
- [SQLRooms Case Studies](https://sqlrooms.org/case-studies.html)
- [Foursquare SQLRooms Announcement](https://foursquare.com/resources/blog/products/foursquare-introduces-sqlrooms/)
- [Observable Framework](https://observablehq.com/framework/)
- [Observable Framework GitHub](https://github.com/observablehq/framework)
- [Observable Framework Maps Demo](https://github.com/bdon/observable-framework-maps)
- [Evidence.dev Documentation](https://docs.evidence.dev/)
- [Evidence.dev US Map Component](https://docs.evidence.dev/components/maps/us-map)
- [Apache Superset Spatial Analytics](https://medium.com/@saikrishna_17904/spatial-analytics-on-apache-superset-fdbfb1ebdeb1)
- [Apache Superset GeoJSON Guide](https://preset.io/blog/2021-02-11-superset-geodata/)
- [Streamlit pydeck_chart API](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart)
- [pydeck Custom Layers](https://deckgl.readthedocs.io/en/latest/custom_layers.html)
- [PMTiles Specification](https://docs.protomaps.com/pmtiles/)
- [PMTiles GitHub](https://github.com/protomaps/PMTiles)
- [Protomaps](https://protomaps.com/)
- [Simon Willison PMTiles Tutorial](https://til.simonwillison.net/gis/pmtiles)

### Causal Visualisation Research
- [Growing Squares: Animated Visualization of Causal Relations (Elmqvist et al.)](http://users.umiacs.umd.edu/~elm/projects/causality/causalviz.pdf)
- [Animated Visualization of Causal Relations Through Growing 2D Geometry](https://www.researchgate.net/publication/220586588)
- [Spatio-Causal Situation Awareness (ACM 2024)](https://dl.acm.org/doi/10.1145/3672556)
- [Counterfactual Visualization Framework (Wang et al. 2025)](https://journals.sagepub.com/doi/full/10.1177/14738716241265120)
- [Counterfactual Visualization User Study (Wang et al. 2024)](https://arxiv.org/abs/2401.08822)
- [VACLab Counterfactual Project](https://vaclab.unc.edu/project/counterfactuals/)
- [Geospatial Network Visualisation Survey (Schottler 2021)](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.14198)
- [pywhy-graphs Causal Graph Visualization](https://www.pywhy.org/pywhy-graphs/stable/auto_examples/intro/intro_causal_graphs.html)
- [Causal Graphs (Runge, Medium)](https://medium.com/causality-in-data-science/what-are-causal-graphs-abdb50354c8a)

### Accessibility
- [WCAG 2.1 Map Evaluation Study (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12094671/)
- [ColorBrewer 2.0](https://colorbrewer2.org/)
- [Section 508 Color Usage Guide](https://www.section508.gov/create/making-color-usage-accessible/)
- [Esri Colourblind Readability Guide](https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/designing-maps-for-colorblind-readability/)
- [Salesforce Colourblind-Friendly Maps](https://www.salesforce.com/blog/how-we-designed-salesforce-maps-to-be-color-blind-friendly/)
- [WCAG Color Contrast Guide](https://www.allaccessible.org/blog/color-contrast-accessibility-wcag-guide-2025)
- [Accessible Colors Palettes (Venngage)](https://venngage.com/blog/accessible-colors/)

### Performance
- [MapLibre Performance Optimisation](https://maplibre.org/maplibre-gl-js/docs/guides/large-data/)
- [MapLibre Performance Techniques (DeepWiki)](https://deepwiki.com/maplibre/maplibre-gl-js/5.2-performance-optimization-techniques)
- [WebGL Best Practices (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)
- [Heavy Map Visualizations Fundamentals](https://advena.hashnode.dev/heavy-map-visualizations-fundamentals-for-web-developers)

---

## 26. Causal Atlas-Specific UI/UX Design

> **Added:** March 2025

### 26.1 User Journey Mapping

A researcher using Causal Atlas follows a seven-step workflow. Each step implies specific UI components and interaction patterns.

**Step 1: Select Region of Interest (Map Interaction)**
- User lands on a full-screen map (Kepler.gl / MapLibre base) showing the global PRIO-GRID overlay at low zoom
- Interaction options: (a) click/drag to draw a bounding box, (b) click a country/admin polygon to auto-select all grid cells within it, (c) type a place name into a search box (geocoded via Nominatim or Mapbox Geocoding API)
- Selected grid cells highlight with a border/fill colour change
- A sidebar shows the count of selected cells and their aggregate area

**Step 2: Select Time Range (Temporal Controls)**
- A dual-handle range slider at the bottom of the screen (similar to Kepler.gl's time filter) lets the user drag start/end dates
- Preset buttons: "Last 12 months", "Last 5 years", "Full history (1989-present)"
- A histogram above the slider shows data density across time — gaps are visible immediately
- The slider snaps to monthly boundaries (our primary temporal unit)

**Step 3: Select Variables to Compare (Data Layer Picker)**
- A collapsible left panel lists available variables grouped by domain: Conflict, Climate, Food Security, Health, Economics, Pollution, Vegetation, Nightlights
- Each variable shows: name, source, temporal coverage bar, spatial coverage percentage for the selected region
- User checks 2+ variables to compare; a maximum of ~6 is recommended for readability
- Drag-and-drop reordering controls the layer stacking on the map and the order of time series panels

**Step 4: Run Correlation/Causal Analysis (Compute Trigger)**
- A prominent "Analyse" button becomes active once region + time + ≥2 variables are selected
- A dropdown beside it lets the user choose the method: Pearson correlation, Granger causality, PCMCI, transfer entropy
- An "Advanced" toggle exposes parameters: max lag (default 12 months), significance threshold (default p < 0.05), minimum data completeness (default 80%)
- Progress indicator shows computation status (server-side via FastAPI, results streamed back)

**Step 5: Explore Results (Causal Graph + Map + Time Series)**
- Results view splits into three synchronised panels (see wireframe below)
- Clicking any element in one panel highlights the corresponding elements in the others
- Claude AI interpretation panel (collapsible right drawer) provides a natural-language summary of findings

**Step 6: Drill Down into Specific Findings**
- Click an edge in the causal graph to see the full cross-correlation function for that variable pair
- Click a grid cell on the map to see its individual time series for all selected variables
- Click a time point in a time series to see the spatial pattern at that moment (map updates to show that month)
- Confidence intervals shown on hover; clicking locks the tooltip for comparison

**Step 7: Export Results / Generate Report**
- "Export" menu offers: PNG/SVG of current view, CSV of underlying data, PDF report (see Section 30), JSON of causal graph structure, shareable URL with encoded state
- "Cite" button generates a citation string including data sources, methods, and Causal Atlas version

### 26.2 Wireframe Descriptions

#### Main Analysis View (Desktop, ≥1280px)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [Logo] Causal Atlas    [Region: East Africa ▼]  [🔍 Search]   [⚙ Settings] │
├────────────┬─────────────────────────────────────┬───────────────────────┤
│            │                                     │                       │
│  VARIABLE  │           MAP VIEW                  │   CAUSAL GRAPH        │
│  PICKER    │                                     │                       │
│            │   ┌───────────────────────────┐     │   (A)──lag:3──►(B)   │
│  □ Conflict│   │  Choropleth / heatmap     │     │    │                  │
│  □ Rainfall│   │  of selected variable     │     │    lag:6              │
│  □ NDVI    │   │  on PRIO-GRID cells       │     │    │                  │
│  □ Food    │   │                           │     │    ▼                  │
│    prices  │   │                           │     │   (C)──lag:2──►(D)   │
│  □ Night-  │   └───────────────────────────┘     │                       │
│    lights  │                                     │  [Edge strength legend]│
│            │                                     │                       │
├────────────┴─────────────────────────────────────┴───────────────────────┤
│                        TIME SERIES PANEL                                 │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  Var A ─── (blue)     Var B ─── (orange, shifted by lag)          │  │
│  │  ╱╲    ╱╲                  ╱╲    ╱╲                               │  │
│  │ ╱  ╲  ╱  ╲                ╱  ╲  ╱  ╲                              │  │
│  │╱    ╲╱    ╲──────────────╱────╲╱    ╲─────                        │  │
│  │ 2018  2019  2020  2021  2022  2023  2024                          │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ◄ ════════════════╡▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╞═══════════════════════════ ►   │
│    Jan 2018                   Time Range Slider               Dec 2024  │
└──────────────────────────────────────────────────────────────────────────┘
```

#### Grid Cell Detail View (Modal or Drill-Down)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Grid Cell: 2.25°N, 37.75°E  │  Region: Turkana, Kenya             │
├─────────────────────────┬────────────────────────────────────────────┤
│  MINI MAP               │  ALL VARIABLES TIME SERIES                 │
│  ┌─────────────┐        │  ┌──────────────────────────────────────┐  │
│  │   ╔═══╗     │        │  │ Conflict events  ▁▁▃█▁▁▅▃▁▁        │  │
│  │   ║ ● ║     │        │  │ Rainfall (mm)    ▅▃▁▁▇█▃▁▅▃        │  │
│  │   ╚═══╝     │        │  │ NDVI             ▃▅▃▁▃▅▅▃▃▁        │  │
│  │  (selected  │        │  │ Food price index  ▁▃▅▇▅▃▅▇█▇        │  │
│  │   cell)     │        │  │ Nightlights      ▃▃▃▃▃▃▃▁▁▁        │  │
│  └─────────────┘        │  └──────────────────────────────────────┘  │
├─────────────────────────┼────────────────────────────────────────────┤
│  CROSS-CORRELATION      │  DATA QUALITY SUMMARY                     │
│  ┌─────────────┐        │                                            │
│  │   ▁▃▅█▅▃▁   │        │  Conflict:  98% complete  Source: ACLED   │
│  │  -6  0  +6  │        │  Rainfall: 100% complete  Source: CHIRPS  │
│  │  lag (months)│        │  NDVI:      95% complete  Source: MODIS   │
│  └─────────────┘        │  Food:      72% complete  Source: WFP     │
│  Peak: lag -3, r=0.67   │  Lights:    88% complete  Source: VIIRS   │
└─────────────────────────┴────────────────────────────────────────────┘
```

#### Report / Export View

```
┌──────────────────────────────────────────────────────────────────┐
│  CAUSAL ATLAS ANALYSIS REPORT                                    │
│  ────────────────────────────────────────────────────────────── │
│  Region: East Africa (Kenya, Somalia, Ethiopia)                  │
│  Period: Jan 2018 — Dec 2023                                     │
│  Variables: Rainfall, Conflict, Food Prices, NDVI                │
│  Method: PCMCI (max lag = 12, α = 0.05)                         │
│                                                                  │
│  [Static Map Image]    [Causal Graph Image]                      │
│                                                                  │
│  Key Findings:                                                   │
│  1. Rainfall anomaly → Food price increase (lag: 4 months)       │
│  2. Food price spike → Conflict increase (lag: 2 months)         │
│  3. Conflict → NDVI decrease (lag: 1 month)                      │
│                                                                  │
│  AI Interpretation:                                              │
│  "In the analysed region, rainfall deficits propagate through    │
│   food markets within 4 months, creating price pressure that     │
│   correlates with increased conflict 2 months later..."          │
│                                                                  │
│  [Download PDF]  [Download Data (CSV)]  [Copy Citation]          │
└──────────────────────────────────────────────────────────────────┘
```

### 26.3 Responsive Design Considerations

The multi-panel layout must adapt across four breakpoint tiers:

| Breakpoint | Width | Layout Strategy |
|---|---|---|
| **Large Desktop** | ≥1440px | Full three-column layout: variable picker (240px) + map (flex) + causal graph (320px); time series panel below |
| **Standard Desktop** | 1024–1439px | Two-column: variable picker collapses to icon rail (48px); map and causal graph share the main area with a draggable divider |
| **Tablet** | 768–1023px | Single column with tab switching: Map tab, Graph tab, Time Series tab. Variable picker becomes a bottom sheet |
| **Mobile** | <768px | Map-first view. Other panels accessible via bottom navigation tabs. Causal graph renders in simplified list view (A → B, lag 3, strength 0.67). Time series uses horizontal scroll |

**Key responsive patterns:**

- **Map always renders first** — it is the primary spatial context and should never be hidden by default on any screen size
- **Progressive disclosure** — on smaller screens, show summary statistics first; full detail views require explicit tap/click to expand
- **Touch-friendly targets** — all interactive elements (grid cells, graph nodes, slider handles) must be ≥44px touch targets on mobile (per Apple HIG / Material Design guidelines)
- **Swipe gestures** — on mobile, swipe left/right between panels; swipe up from time series to expand to full-screen
- **Collapsible panels** — every panel has a collapse/expand toggle; state persists across sessions via localStorage
- **Font scaling** — use `rem` units throughout; respect user's browser font-size preference for accessibility

**Implementation approach:** Use CSS Grid with `grid-template-areas` for the main layout, with media queries at each breakpoint to reassign areas. The causal graph and time series components should be lazy-loaded (React.lazy + Suspense) to keep initial load fast on mobile.

---

## 27. Interactive Causal Graph Visualisation

> **Added:** March 2025

### 27.1 The Challenge: DAGs Alongside Maps

Causal Atlas must display two fundamentally different spatial representations simultaneously: a geographic map (continuous 2D space) and a causal graph (abstract node-link diagram). The key design question is whether to overlay the graph on the map (nodes positioned at their geographic centroid) or display them side-by-side.

**Option A: Overlaid on map** — Nodes placed at grid-cell centroids, edges drawn as arcs. Works when the graph is sparse (≤20 nodes, ≤30 edges). Becomes unreadable with dense graphs due to edge crossings. Similar to ACLED's flow maps.

**Option B: Side-by-side (recommended)** — Map on the left, causal graph on the right, with cross-highlighting. Click a node in the graph and the corresponding grid cell(s) highlight on the map. Click a grid cell on the map and the corresponding node highlights in the graph. This preserves clarity in both views. The causal graph can use an optimised layout (Sugiyama/layered DAG) without geographic constraints.

**Option C: Hybrid** — Default side-by-side, but a toggle overlays graph nodes onto the map for quick spatial context checks. Edges become curved arcs with width proportional to effect strength and colour indicating lag duration.

### 27.2 Library Comparison for DAG Rendering

| Library | Rendering | Max Nodes (smooth) | React Integration | DAG Layout | Licence | Best For |
|---|---|---|---|---|---|---|
| **Cytoscape.js** | Canvas/WebGL | ~5,000 | Via `react-cytoscapejs` (Plotly wrapper) | Dagre, ELK, CoSE, Klay | MIT | Large networks, rich layout algorithms |
| **React Flow** | SVG/HTML | ~1,000 | Native React component | Dagre (via `@dagrejs/dagre`) | MIT (core) | Workflow editors, small-medium DAGs |
| **d3-dag** | SVG (via D3) | ~500 | Manual D3-React integration | Sugiyama, Zherebko, grid | Apache 2.0 | Publication-quality layered DAGs |
| **Sigma.js** | WebGL | ~50,000+ | `@react-sigma/core` | ForceAtlas2 (via graphology) | MIT | Massive networks, exploration |
| **vis.js (vis-network)** | Canvas | ~3,000 | Community wrappers | Hierarchical, force-directed | Apache 2.0 / MIT | Rapid prototyping, simple graphs |

Sources: [Cytoscape.js](https://js.cytoscape.org/), [React Flow](https://reactflow.dev/), [d3-dag GitHub](https://github.com/erikbrinkman/d3-dag), [Sigma.js](https://www.sigmajs.org/), [vis-network](https://visjs.github.io/vis-network/docs/network/)

**Recommendation for Causal Atlas:** Start with **Cytoscape.js** via `react-cytoscapejs` for its mature DAG layout support (Dagre for layered layouts, CoSE for force-directed), its ability to handle up to several thousand nodes, and extensive styling/interaction API. If we later need to render massive exploratory graphs (e.g., full PCMCI output across all grid cells), Sigma.js provides a WebGL fallback path. React Flow is tempting for its native React feel but lacks the layout algorithm depth needed for causal DAGs.

### 27.3 Tigramite Causal Graph Output and Integration

Tigramite (v5.2+) produces causal graphs via its `plotting` module with two main functions:

- **`plot_graph()`** — Renders a process graph (summary DAG) where nodes are variables and edges are labelled with lag and strength. Output is a matplotlib figure.
- **`plot_time_series_graph()`** — Renders the full time-unrolled graph where each variable at each time step is a separate node. More detailed but visually complex.

Both functions accept `val_matrix` (effect strengths), `graph` (adjacency structure with lag info encoded as string labels like `"-->"`, `"o->"`, `"x-x"`), and `var_names`.

**Integration strategy for Causal Atlas:**

1. **Backend (Python/FastAPI):** Run PCMCI via tigramite, extract the `graph` array and `val_matrix` as JSON-serialisable structures. The graph array is a NumPy array of shape `(N, N, tau_max+1)` with string entries encoding edge types.
2. **Convert to graph JSON:** Transform the tigramite output into a nodes-and-edges JSON format compatible with Cytoscape.js:
   ```json
   {
     "nodes": [
       {"data": {"id": "rainfall", "label": "Rainfall", "domain": "climate"}}
     ],
     "edges": [
       {"data": {"source": "rainfall", "target": "food_price", "lag": 4, "strength": 0.67, "type": "-->"}}
     ]
   }
   ```
3. **Frontend (React + Cytoscape.js):** Render the graph with edge width ∝ |strength|, edge colour mapped to lag (short lag = warm, long lag = cool), and edge style encoding certainty (`"-->"` solid, `"o->"` dashed).
4. **Fallback static rendering:** For PDF export, call tigramite's `plot_graph()` on the server side and return the matplotlib figure as a PNG/SVG.

Source: [Tigramite documentation](https://jakobrunge.github.io/tigramite/), [Tigramite GitHub](https://github.com/jakobrunge/tigramite), [Tigramite tutorial notebooks](https://github.com/jakobrunge/tigramite/tree/master/tutorials)

### 27.4 Interactive Features

The causal graph must support the following interactions:

| Feature | Implementation | Purpose |
|---|---|---|
| **Click node → highlight on map** | On node click, dispatch event to map component with variable ID; map highlights grid cells where that variable has data | Spatial context for abstract variables |
| **Click edge → show lag detail** | On edge click, open a popover showing: cross-correlation function plot, lag value, p-value, effect size, confidence interval | Evidence behind the causal claim |
| **Hover edge → show tooltip** | Lightweight tooltip: "Rainfall → Food Prices, lag 4 months, r = 0.67" | Quick scanning without full detail |
| **Drag nodes** | Allow repositioning for manual layout adjustment; positions saved to localStorage | User customisation |
| **Filter by strength** | Slider to hide edges below a threshold (e.g., |r| < 0.3) | Declutter dense graphs |
| **Filter by domain** | Toggle domain groups on/off (climate, conflict, economic, etc.) | Focus on specific causal pathways |
| **Zoom + pan** | Standard scroll-to-zoom, drag-to-pan | Navigate large graphs |
| **Animate temporal propagation** | Highlight cascade: if A → B (lag 3) → C (lag 2), animate a pulse along A → B → C with appropriate timing | Show how shocks propagate through the causal chain |

### 27.5 Causal Graph Styling Conventions

To ensure the graph is immediately readable, adopt consistent visual encoding:

- **Node colour:** By domain (conflict = red, climate = blue, food = orange, economic = green, health = purple, vegetation = olive, nightlights = yellow)
- **Node size:** Proportional to number of significant connections (degree centrality)
- **Edge width:** Proportional to |effect strength| (absolute value of partial correlation coefficient)
- **Edge colour:** Mapped to lag duration via a sequential colour scale (1 month = dark, 12 months = light)
- **Edge style:** Solid for definite causal direction (`"-->"`), dashed for ambiguous orientation (`"o->"`), dotted for uncertain (`"x-x"`)
- **Arrow heads:** Direction of causal influence; double-headed for bidirectional
- **Labels:** On edges, show "lag N" in a small chip; on hover, expand to full statistics

---

## 28. Time Series Visualisation for Causal Analysis

> **Added:** March 2025

### 28.1 Multi-Variable Time Series with Lag Alignment

The core time series view must show multiple variables simultaneously and allow the user to visually verify lag relationships discovered by the causal analysis.

**Key requirements:**
- Multiple y-axes (left and right) for variables with different units (mm rainfall vs. event counts vs. price index)
- Ability to shift one series by the detected lag: e.g., "shift Rainfall left by 4 months" to visually align the cause with the effect
- Confidence bands (shaded area) around each series, especially for modelled/interpolated values
- Annotation markers for significant events (e.g., "drought declared", "election", "COVID lockdown")
- Brushing: select a sub-range on the time series to zoom the map to that period

**Lag alignment visualisation** is critical and unusual. Most charting libraries don't natively support "shift this series by N time steps". Implementation approach:
1. Duplicate the data array for the shifted variable
2. Offset the timestamp by `lag * temporal_resolution`
3. Render both the original (faded) and shifted (solid) versions
4. A small label: "shifted by 4 months to align with Food Prices"

### 28.2 Cross-Correlation Function (CCF) Plots

The CCF plot shows correlation between two variables at each lag from -τ_max to +τ_max. This is the primary diagnostic for identifying lag structures.

**Visual design:**
```
  Correlation
  1.0 │
      │          ▓
  0.5 │        ▓ ▓ ▓
      │      ▓ ▓ ▓ ▓ ▓
  0.0 │──▓─▓─▓─▓─▓─▓─▓─▓─▓─▓──  ← significance threshold (dashed)
      │  ▓ ▓           ▓ ▓
 -0.5 │  ▓               ▓
      │
 -1.0 │
      └──────────────────────────
       -12  -6   0   +6  +12
              Lag (months)
```

- **Bar chart** format (like `statsmodels.graphics.tsaplots.plot_ccf`)
- Horizontal dashed lines at ±1.96/√N for 95% significance threshold
- Bars coloured by significance: significant = blue, non-significant = grey
- The peak lag is highlighted with a label: "Peak: lag -4, r = 0.67"
- Clicking a specific lag bar updates the time series view to show that alignment

### 28.3 Impulse Response Function (IRF) Visualisation

For VAR-based causal analysis, the IRF shows how a one-standard-deviation shock to variable A propagates to variable B over time.

**Visual design:**
- Line plot showing the response magnitude over time (0 to τ_max periods)
- Shaded confidence band (typically 90% or 95% from bootstrap)
- Horizontal line at zero for reference
- Multiple IRFs can be shown in a small-multiples grid (one panel per variable pair)
- Title format: "Response of Food Prices to a 1-σ Rainfall Shock"

**Implementation note:** IRFs are computed server-side (using `statsmodels.tsa.vector_ar.var_model.VARResults.irf()` or tigramite's causal effect estimation). The frontend receives arrays of (time_step, response_value, ci_lower, ci_upper) and renders them.

### 28.4 Library Comparison for Time Series Charts

| Library | Rendering | Large Data (>10k points) | React Native | Multi-Axis | Annotations | Brush/Zoom | Licence |
|---|---|---|---|---|---|---|---|
| **Recharts** | SVG | Moderate (sluggish >5k) | Yes | Yes (YAxis with yAxisId) | Limited | Yes (ReferenceArea) | MIT |
| **Nivo** | SVG/Canvas/HTML | Canvas mode handles well | Yes | Limited | Limited | Via ResponsiveLine | MIT |
| **Apache ECharts** | Canvas/WebGL | Excellent (millions via WebGL) | Via `echarts-for-react` | Yes (multiple yAxis) | Rich (markLine, markArea, markPoint) | Excellent (dataZoom) | Apache 2.0 |
| **Observable Plot** | SVG | Moderate | Not React-native | Yes (facets) | Declarative marks | Via D3-brush | ISC |
| **Plotly.js** | SVG/WebGL | WebGL mode handles millions | `react-plotly.js` | Yes | Yes (shapes, annotations) | Excellent (rangeslider) | MIT |

Sources: [Recharts](https://recharts.org/), [Nivo](https://nivo.rocks/), [Apache ECharts](https://echarts.apache.org/), [Observable Plot](https://observablehq.com/plot/), [Plotly.js](https://plotly.com/javascript/)

**Recommendation for Causal Atlas:** Use **Apache ECharts** (via `echarts-for-react`) as the primary time series library. Rationale:
- WebGL rendering handles the data volumes we need (years of monthly data across multiple variables)
- `dataZoom` component provides exactly the brush-and-zoom behaviour needed for temporal exploration
- `markLine` and `markArea` support the annotation requirements (significance thresholds, event markers)
- Multiple y-axes are first-class citizens
- Extensive tooltip customisation for showing lag/correlation information on hover
- Active community and regular updates (backed by Apache Foundation)
- Server-side rendering option for PDF export

For simpler views (single-variable sparklines in the variable picker), Recharts is a good lightweight choice.

---

## 29. Map-Based Anomaly Detection Visualisation

> **Added:** March 2025

### 29.1 Showing "This Grid Cell is Anomalous Right Now"

Anomaly detection is a natural output of having historical baselines for every variable in every grid cell. The map should be able to show, at a glance, where current conditions deviate significantly from the historical norm.

**What constitutes an anomaly:**
- Z-score: `z = (current_value - historical_mean) / historical_std`, computed per grid cell per variable per calendar month (to account for seasonality)
- A grid cell is flagged as anomalous if |z| > 2.0 (or a user-adjustable threshold)
- Multi-variable anomaly: a composite score combining z-scores across selected variables (e.g., "simultaneous rainfall deficit AND food price spike AND conflict increase")

### 29.2 Colour Scales for Z-Scores and Anomaly Magnitudes

**Diverging colour scale** centred at z = 0:

```
  z ≤ -3.0   -2.0   -1.0    0.0   +1.0   +2.0   z ≥ +3.0
    ████     ████   ████    ████   ████   ████    ████
  deep      medium  light   white  light  medium  deep
  blue      blue    blue    /grey  red    red     red
```

**Design principles (drawn from NOAA and ECMWF anomaly maps):**
- Use a **diverging** colour scale (blue-white-red or brown-white-green for precipitation) so the direction of anomaly is immediately clear
- NOAA's Global Temperature Anomalies Map Viewer uses anomalies based on a 1981-2010 mean, with blue for below-normal and red for above-normal — a proven and widely understood convention
- ECMWF's extended-range anomaly charts show statistical significance: regions where the Wilcoxon-Mann-Whitney test shows significance less than 90% are displayed as blank (grey), while regions exceeding 99% significance are delimited by solid contours
- **Saturate at the extremes** — z-scores beyond ±3 all get the deepest colour; the visual emphasis is on "extreme" vs "not extreme"
- **Use ColorBrewer diverging palettes** (RdBu, BrBG, PRGn) which are perceptually uniform and colourblind-safe
- **Opacity/hatching for low confidence** — if a cell has sparse data (e.g., <80% temporal coverage), reduce opacity or add diagonal hatching to indicate uncertainty
- **Variable-specific conventions:** precipitation anomaly uses brown (dry) to green (wet); temperature uses blue (cold) to red (hot); conflict uses white to red (more is always bad); NDVI uses brown (degraded) to green (healthy)

Sources: [NOAA Global Temperature Anomaly Map Viewer](https://www.climate.gov/maps-data/dataset/global-temperature-anomalies-map-viewer), [ECMWF Extended Range Forecast Products](https://www.ecmwf.int/en/forecasts/documentation-and-support/extended-range/extended-forecast-graphical-products), [Climate Reanalyzer (U. Maine)](https://climatereanalyzer.org/clim/t2_daily/), [ColorBrewer 2.0](https://colorbrewer2.org/)

### 29.3 Temporal Comparison (This Month vs. Historical Average)

The anomaly view needs a clear temporal reference. Two modes:

**Mode 1: Current anomaly map** — Shows z-scores for the most recent data month. The legend reads "March 2025 vs. 1989-2024 average for March". This is the default landing view for operational users.

**Mode 2: Anomaly time slider** — The user drags the time slider and the map updates to show the anomaly pattern for each month. This allows seeing anomalies evolve over time. Combined with animation (play button), this creates a powerful visual narrative of how crises develop.

**Mode 3: Anomaly duration** — Instead of showing the current z-score, show *how many consecutive months* a cell has been anomalous. Colour scale: 1 month = light, 6+ months = saturated. This highlights chronic vs. acute anomalies.

### 29.4 Inspiration from Operational Anomaly Maps

| Platform | What They Do Well | What We Can Adopt |
|---|---|---|
| **NOAA Climate Anomaly Maps** | Clear diverging colour scales, monthly updates, reference period clearly stated | Colour conventions, reference period labelling |
| **ECMWF Anomaly Charts** | Statistical significance overlays (blank = not significant, contours = highly significant) | Significance filtering on the anomaly map |
| **Climate Reanalyzer** | Daily updating, interactive hover showing exact values, time series on click | Click-to-drill-down from anomaly map to time series |
| **HungerMapLIVE** | Real-time composite index, traffic-light colour coding (green/yellow/orange/red) | Composite anomaly index combining multiple variables |
| **FEWS NET IPC Maps** | Widely understood 5-phase colour scale for food insecurity severity | Severity classification approach for multi-variable anomaly scores |

### 29.5 Multi-Variable Anomaly Composite

For Causal Atlas, the most powerful anomaly view will combine anomalies across domains. Implementation approach:

1. Compute z-scores independently for each selected variable per cell per month
2. A cell is flagged as "multi-domain anomalous" if z-scores exceed the threshold in ≥2 variables simultaneously
3. Visual encoding: use **bivariate colour mapping** — e.g., one axis for climate anomaly (blue-red), other axis for conflict anomaly (white-red), producing a 3×3 colour grid. See research on bivariate choropleth maps by Joshua Stevens.
4. Alternative: size-of-symbol encoding — show a circle in each cell, with size ∝ number of simultaneously anomalous variables and colour = the most extreme z-score direction

---

## 30. Print and Export

> **Added:** March 2025

### 30.1 Publication-Quality Static Maps with Matplotlib + Cartopy

For PDF reports and academic publications, interactive web maps are insufficient. We need a server-side rendering pipeline that produces high-resolution static images.

**Technology stack:**
- **Cartopy** (built on PROJ, shapely, matplotlib) — handles map projections, coastlines, borders, and gridlines
- **Matplotlib** — the rendering engine; supports vector output (PDF, SVG, EPS) and raster (PNG at any DPI)
- **GeoPandas** — for reading/plotting PRIO-GRID cells and admin boundaries

**Implementation pipeline:**
```python
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geopandas as gpd

fig, ax = plt.subplots(
    figsize=(12, 8),
    subplot_kw={'projection': ccrs.PlateCarree()}
)
ax.set_extent([32, 52, -5, 15])  # East Africa bounding box
ax.coastlines(resolution='50m')
ax.add_feature(cartopy.feature.BORDERS, linewidth=0.5)

# Plot PRIO-GRID cells with anomaly colours
grid_gdf.plot(
    column='z_score',
    ax=ax,
    cmap='RdBu_r',
    vmin=-3, vmax=3,
    legend=True,
    legend_kwds={'label': 'Rainfall Anomaly (z-score)', 'shrink': 0.6}
)

ax.set_title('Rainfall Anomaly — March 2025', fontsize=14)
fig.savefig('anomaly_map.pdf', dpi=300, bbox_inches='tight')
```

**Quality guidelines:**
- Minimum 300 DPI for print, 150 DPI for screen
- Use vector formats (PDF, SVG) where possible — they scale infinitely and have smaller file sizes for map-type graphics
- Include: title, legend with units, scale bar, north arrow, data source attribution, date of data, projection info
- Use journal-standard fonts (Helvetica, Arial, Times New Roman) to avoid rendering issues in LaTeX/Word

Sources: [Cartopy documentation](https://scitools.org.uk/cartopy/docs/latest/), [Matplotlib savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html), [Earth and Environmental Data Science — Maps in Scientific Python](https://earth-env-data-science.github.io/lectures/mapping_cartopy.html)

### 30.2 PDF Report Generation from Analysis Results

A "Generate Report" feature should produce a self-contained PDF summarising an analysis session.

**Report structure:**
1. **Header:** Causal Atlas logo, report title, generation date
2. **Analysis Parameters:** Region, time range, variables selected, method, significance threshold
3. **Static Map:** Matplotlib/Cartopy rendering of the study area with the primary variable displayed
4. **Causal Graph Image:** Tigramite `plot_graph()` output as a static figure (matplotlib → PNG/SVG)
5. **Key Findings Table:** Variable pair, lag, effect strength, p-value, direction
6. **Time Series Plots:** One figure per significant variable pair, with lag alignment shown
7. **AI Interpretation:** Claude-generated narrative summary of the findings
8. **Data Quality Summary:** Completeness metrics per variable per region
9. **Sources and Citations:** Auto-generated list of all data sources used (ACLED, CHIRPS, etc.) with standard citation formats
10. **Methodology Notes:** Brief description of the statistical method applied

**PDF generation libraries (Python):**

| Library | Approach | Pros | Cons |
|---|---|---|---|
| **WeasyPrint** | HTML/CSS → PDF | Use existing web templates, supports CSS flexbox/grid | Heavy dependency (Pango, Cairo); moderate rendering fidelity |
| **ReportLab** | Programmatic PDF construction | Full control, lightweight, no browser dependency | Verbose API, manual layout |
| **matplotlib.backends.backend_pdf.PdfPages** | Multi-page matplotlib figures → PDF | Perfect for figure-heavy reports; already in the stack | Not for rich text layout |
| **Typst** (via `typst-py`) | Modern typesetting language → PDF | Beautiful output, fast compilation, programmable | Newer ecosystem, less mature tooling |
| **Quarto** | Markdown + code → PDF/HTML | Reproducible reports, supports Python/R | Requires Quarto CLI installation; overkill for API-generated reports |

**Recommendation:** Use **WeasyPrint** for the main report layout (HTML template with Jinja2 for dynamic content) and embed matplotlib-generated figures as inline SVGs or base64-encoded PNGs. This approach lets us maintain a single HTML template that works for both web preview and PDF export.

### 30.3 Making Figures Reproducible

Every figure generated by Causal Atlas should be reproducible. This means:

- **Embed metadata in the figure file:** Use PNG `tEXt` chunks or PDF metadata fields to store: data query parameters, analysis method, software version, random seed (if applicable)
- **Provide a "Reproduce" button:** Generates a Python script (or Jupyter notebook) that recreates the figure from raw data using Causal Atlas's API
- **Pin data versions:** Each figure references a specific data snapshot (versioned via DuckDB table snapshots or Parquet file hashes)
- **Deterministic colour mapping:** Colours assigned to variables are consistent across sessions (defined in a central theme configuration, not randomly assigned)
- **Figure identifier:** Each exported figure gets a unique hash (SHA-256 of parameters + data version), printed in the figure caption for traceability
