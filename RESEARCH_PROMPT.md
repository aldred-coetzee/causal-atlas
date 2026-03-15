# Claude Code Research Prompt for Causal Atlas

Copy and paste the section below (between the --- markers) into Claude Code as your research prompt.

---

## Prompt

I need you to conduct deep, thorough research for the Causal Atlas project. Read CLAUDE.md first — it contains the project context, research priorities, folder structure, and writing standards.

The goal is to populate the `research/` folder with comprehensive findings across all topics. This is the foundation the entire project will be built on, so depth matters more than speed.

### Research Tasks

Use web search extensively. For each task, create or update the specified file(s), commit with a descriptive message, and push.

**Work through these in priority order:**

#### Task 1: Dataset Deep Dives (research/datasets/)
For EACH dataset listed in research/datasets/README.md, create a dedicated markdown file following the template in that README. This means investigating:
- Exact API endpoints and authentication flows
- Rate limits and bulk download alternatives
- Full field schemas with column names and data types
- Sample API calls and response formats
- Spatial encoding (lat/lon, admin codes, grid cells)
- Temporal resolution and update frequency
- Known quality issues, biases, and validation studies
- Licence terms and citation requirements
- Existing Python libraries or wrappers
- How it relates to other datasets in our catalogue

Start with the Tier 1 datasets (ACLED, GDELT, EM-DAT, WFP, CHIRPS, PRIO-GRID, HDX HAPI), then move to Tier 2. Search for each dataset's official documentation, API docs, GitHub repos, and academic papers about data quality.

#### Task 2: Landscape Analysis (research/01-landscape-analysis.md)
Deep investigation of existing platforms and tools we could leverage or learn from:
- PRIO-GRID v3 (R package) — architecture, how it handles data ingestion, what we can reuse
- VIEWS conflict forecasting system — their pipeline, methods, what's open source
- AfroGrid — their integration methodology, published in Nature Scientific Data
- WFP HungerMapLIVE — their architecture (what's publicly known), data layers, ML approach
- ClimateSERV — NASA's tool for climate data, API capabilities
- xSub — cross-national subnational violence portal
- HDX platform — CKAN-based, what their Python libraries offer
- Kepler.gl — latest capabilities (v3.1 with DuckDB), embedding approach
- Any other open-source projects doing multi-domain spatiotemporal analysis

For each: what does it do well, what are its limitations, what can we directly reuse vs. what do we need to build?

#### Task 3: Published Causal Chains (research/03-causal-chains.md)
Search academic literature for published research on cross-domain causal relationships that are geospatially and temporally grounded. Focus on:
- Drought → crop failure → food price → conflict/unrest
- Climate extremes → migration/displacement
- Pollution/air quality → health outcomes
- Earthquake → economic disruption → social effects
- Commodity price shocks → political instability
- Disease outbreaks → economic and social impacts
- Any other documented multi-domain causal chains

For each: what datasets were used, what lag structures were found, what statistical methods worked, what regions were studied, key paper references.

#### Task 4: Statistical Methods (research/04-statistical-methods.md)
Investigate methods for detecting causality in spatiotemporal data:
- Granger causality (standard and spatial variants)
- Transfer entropy
- PCMCI (Peter and Clark Momentary Conditional Independence)
- Convergent cross-mapping
- Spatial lag and spatial error models
- Moran's I and spatial autocorrelation
- Vector autoregression (VAR) with spatial dimensions
- Cross-correlation with lag analysis
- Anomaly co-occurrence analysis
- Machine learning approaches (random forests for feature importance, etc.)

For each: what it detects, assumptions, Python implementation (statsmodels, tigramite, etc.), strengths, weaknesses, when to use it, published examples in our domain.

#### Task 5: Similar Projects (research/07-similar-projects.md)
Search GitHub, academic papers, and project websites for anyone who has attempted something similar:
- Cross-domain event correlation platforms
- Multi-layer temporal map tools
- Humanitarian data integration frameworks
- Open-source OSINT geospatial platforms
- Climate-conflict analysis tools
- Any "atlas of causality" type projects

For each: what they built, what stack they used, how far they got, what we can learn, links.

#### Task 6: Data Integration Techniques (research/06-data-integration.md)
How do others solve the hard problems of combining heterogeneous spatiotemporal data:
- Spatial resolution mismatch (point data vs raster vs admin regions vs grid cells)
- Temporal alignment (daily vs monthly vs irregular)
- Missing data handling in spatial grids
- The PRIO-GRID approach to data standardisation
- The AfroGrid approach
- How HungerMapLIVE integrates its sources
- Area-weighted interpolation techniques
- Admin-to-grid mapping strategies

#### Task 7: Visualisation Approaches (research/05-visualisation-approaches.md)
How do the best existing platforms present this kind of data:
- Kepler.gl capabilities and limitations for our use case
- deck.gl ecosystem and relevant layers
- How HungerMapLIVE does overlay + temporal
- ACLED's dashboard approach
- GDELT's analysis and visualisation tools
- DuckDB integration with Kepler.gl v3.1
- Alternatives: Felt, Mapbox, Leaflet, Plotly/Dash
- What interaction patterns work for causal discovery (brushing, linking, temporal scrubbing)

#### Task 8: Architecture Notes (research/08-architecture-notes.md)
As research progresses, capture emerging architecture decisions and open questions:
- What should the canonical data format be (Parquet schema)?
- How should adapters be structured?
- What's the right level of spatial aggregation?
- Should we use PRIO-GRID cell IDs directly or create our own?
- DuckDB vs PostGIS vs both?
- How to handle real-time vs historical data?
- What's the minimum viable product?

### Working Approach

- Use multiple sub-agents to research different topics in parallel where possible
- Search the web extensively — official docs, GitHub repos, academic papers, blog posts
- When you find a particularly important source, fetch the full page content
- Be specific: API endpoints, field names, code examples, not just descriptions
- Update research/README.md status indicators as files are completed
- Commit and push after completing each major file
- If a research file gets very long, that's fine — thoroughness over brevity

---
