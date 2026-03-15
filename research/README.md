# Causal Atlas — Research

This folder contains the deep research that underpins the Causal Atlas project. Each file is a thorough investigation of a specific topic, intended to inform architecture and implementation decisions.

**Total research:** ~49,000 lines across 29 files (as of March 2025)

## Research Index

| # | File | Topic | Lines | Status |
|---|---|---|---|---|
| 01 | [landscape-analysis.md](01-landscape-analysis.md) | Existing platforms, tools, and projects we can leverage | 2,199 | 🟢 Deep (second pass) |
| 02 | [dataset-synthesis.md](02-dataset-synthesis.md) | Cross-dataset integration decisions, overlap handling, variable naming | 984 | 🟢 Complete (first pass) |
| — | [datasets/](datasets/) | Deep dives into 20 candidate data sources (see [index](datasets/README.md)) | ~20,000 | 🟢 Deep (second pass) |
| 03 | [causal-chains.md](03-causal-chains.md) | Published research on cross-domain causal relationships | 2,585 | 🟢 Deep (second pass) |
| 04 | [statistical-methods.md](04-statistical-methods.md) | Methods for spatiotemporal causal analysis | 4,989 | 🟢 Deep (second pass) |
| 05 | [visualisation-approaches.md](05-visualisation-approaches.md) | How others present multi-layer temporal data | 2,631 | 🟢 Deep (second pass) |
| 06 | [data-integration.md](06-data-integration.md) | Spatial/temporal alignment techniques | 3,337 | 🟢 Deep (second pass) |
| 07 | [similar-projects.md](07-similar-projects.md) | Prior art, GitHub repos, academic papers | 2,065 | 🟢 Deep (second pass) |
| 08 | [architecture-notes.md](08-architecture-notes.md) | Emerging architecture decisions from research | 4,350 | 🟢 Deep (second pass) |
| 09 | [machine-specifications.md](09-machine-specifications.md) | Linux hardware specs, cloud vs self-hosted, software stack | 2,380 | 🟢 Deep (second pass) |
| 10 | [validation-strategy.md](10-validation-strategy.md) | Validating discovered causal relationships | 1,150 | 🟢 Complete (first pass) |

## Status Key

- 🔴 Not started
- 🟡 In progress
- 🟢 Complete (first pass) — initial thorough research
- 🟢 Deep (second pass) — significantly expanded with additional depth
- 🔵 Reviewed and validated

## How to Contribute Research

See [CLAUDE.md](../CLAUDE.md) for writing standards. Key points:

- Be thorough — we need implementation-level detail, not summaries
- Include sources with URLs
- Note access requirements, rate limits, and licence terms
- Flag quality issues and known limitations
- Date your findings (APIs change)
