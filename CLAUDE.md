# CLAUDE.md — Causal Atlas Project Intelligence

## Project Overview

Causal Atlas is an open-source platform for discovering cross-domain causal relationships through spatiotemporal data analysis and visualisation. It ingests global event and indicator data from multiple domains (conflict, climate, food security, health, economics, pollution, etc.), aligns them on a common spatiotemporal grid, and surfaces statistically significant time-lagged correlations.

**Repository:** https://github.com/aldred-coetzee/causal-atlas
**Owner:** Aldred Coetzee (aldred-coetzee)
**Licence:** MIT
**Status:** Research phase — no code yet, building the evidence base first

## Current Phase: Deep Research

We are NOT writing application code yet. The current goal is to build a comprehensive research base in the `research/` folder before any architecture or implementation decisions are finalised. Research must be deep, thorough, and well-sourced.

## Key Decisions Made

- **Spatial backbone:** PRIO-GRID compatible (0.5° × 0.5° grid cells, WGS84)
- **Temporal resolution:** Monthly as primary unit, daily preserved where available
- **Tech stack direction:** Python, DuckDB/Parquet, Kepler.gl, FastAPI+React, Claude API for interpretation
- **Open source and accessible to all — non-negotiable**
- **Leverage existing work — do not reinvent the wheel**
- **AI-assisted development workflow (Claude Code)**

## Research Priorities

### What we need to investigate deeply:

1. **Existing platforms and tools** — What open-source projects already do pieces of what we want? Can we build on them rather than from scratch? Look at PRIO-GRID v3, VIEWS, AfroGrid, ClimateSERV, HDX HAPI, xSub, etc.

2. **Dataset deep dives** — For each candidate data source: exact API endpoints, authentication requirements, rate limits, data formats, field schemas, update frequency, spatial/temporal coverage, known quality issues, licence terms, citation requirements. Not surface-level — we need the detail you'd need to write an ingestion adapter.

3. **Academic research on cross-domain causal chains** — What has been published on drought→conflict, climate→migration, pollution→health, food prices→unrest, earthquakes→economic disruption, etc.? What lag structures have been found? What statistical methods work best?

4. **Statistical methods for spatiotemporal causality** — Granger causality, transfer entropy, convergent cross-mapping, PCMCI, spatial lag models, Moran's I, etc. What are their strengths, weaknesses, and when to use each?

5. **Visualisation approaches** — How do the best existing platforms (HungerMapLIVE, ACLED dashboard, Kepler.gl demos, GDELT analysis tools) present multi-layer temporal data? What works, what doesn't?

6. **Data integration challenges** — How have others solved the spatial resolution mismatch problem? Temporal alignment? Missing data? How does AfroGrid handle it? How does PRIO-GRID v3 handle it?

7. **Similar projects and prior art** — Any GitHub repos, academic papers, or tools that attempted cross-domain spatiotemporal correlation discovery? What can we learn from their approach and limitations?

## Research Folder Structure

All research goes in `research/`. Each topic gets its own markdown file. Files should be thorough, well-structured, and include sources/URLs.

```
research/
├── README.md                          # Index of all research files
├── 01-landscape-analysis.md           # Existing platforms, tools, projects
├── 02-datasets/
│   ├── README.md                      # Dataset catalogue overview
│   ├── acled.md                       # Deep dive: ACLED
│   ├── gdelt.md                       # Deep dive: GDELT
│   ├── emdat.md                       # Deep dive: EM-DAT
│   ├── wfp-food-prices.md             # Deep dive: WFP food price data
│   ├── chirps.md                      # Deep dive: CHIRPS rainfall
│   ├── usgs-earthquakes.md            # Deep dive: USGS earthquake API
│   ├── openaq.md                      # Deep dive: OpenAQ air quality
│   ├── hdx-hapi.md                    # Deep dive: HDX Humanitarian API
│   ├── prio-grid.md                   # Deep dive: PRIO-GRID framework
│   ├── nightlights.md                 # Deep dive: VIIRS nighttime lights
│   ├── ndvi-vegetation.md             # Deep dive: MODIS/VIIRS NDVI
│   ├── ucdp-ged.md                    # Deep dive: UCDP-GED conflict data
│   ├── world-bank.md                  # Deep dive: World Bank indicators
│   ├── fao-data.md                    # Deep dive: FAO (pesticides, crops, etc.)
│   ├── disease-outbreaks.md           # Deep dive: WHO, ProMED, IHME
│   └── other-sources.md               # Additional sources discovered
├── 03-causal-chains.md                # Published research on cross-domain causality
├── 04-statistical-methods.md          # Methods for spatiotemporal causal analysis
├── 05-visualisation-approaches.md     # How others present multi-layer temporal data
├── 06-data-integration.md             # Spatial/temporal alignment techniques
├── 07-similar-projects.md             # Prior art and lessons learned
└── 08-architecture-notes.md           # Emerging architecture decisions from research
```

## Writing Standards for Research Files

- **Be thorough.** Surface-level summaries are not useful. We need the detail that would let someone write code against an API or replicate a methodology.
- **Include sources.** Every claim should have a URL or citation.
- **Note access requirements.** Registration needed? API keys? Rate limits? Commercial restrictions?
- **Flag quality issues.** Known biases, gaps, limitations.
- **Include schema details.** What fields does the data have? What are the column names? What formats?
- **Note interoperability.** How does this data relate to other sources? Shared identifiers? Compatible grids?
- **Date your findings.** APIs change. Note when you checked something.

## Commands and Conventions

- All research files are Markdown
- Use `##` for major sections, `###` for subsections
- Use tables for structured comparisons
- Use code blocks for API examples, schema definitions, etc.
- Commit frequently with descriptive messages
- Branch naming: `research/topic-name` for focused research branches

## What NOT to Do Yet

- Do not write application code
- Do not create Python packages or modules
- Do not set up CI/CD
- Do not create Docker files
- Do not build the web frontend
- Focus entirely on research depth and breadth
