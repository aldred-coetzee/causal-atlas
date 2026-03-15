# Dataset Deep Dives

Each file in this folder is a thorough investigation of a candidate data source for Causal Atlas.

## Template

Every dataset deep dive should cover:

1. **Overview** — What is it, who maintains it, how long has it existed
2. **Coverage** — Spatial extent, temporal range, update frequency
3. **Access** — API endpoints, authentication, rate limits, bulk download options
4. **Schema** — Field names, data types, key columns, sample records
5. **Spatial detail** — How is location encoded? Lat/lon points? Admin regions? Grid cells?
6. **Temporal detail** — What timestamp resolution? Continuous or periodic?
7. **Quality** — Known biases, gaps, limitations, validation studies
8. **Licence** — Terms of use, attribution requirements, commercial restrictions
9. **Interoperability** — Shared identifiers with other datasets, grid compatibility
10. **Python access** — Existing libraries, API wrappers, code examples
11. **Relevance to Causal Atlas** — Which domain(s) does it serve, what causal chains could it illuminate
12. **Sources** — URLs, papers, documentation links

## Dataset Index

| File | Dataset | Domain | Priority |
|---|---|---|---|
| [acled.md](acled.md) | ACLED (Armed Conflict Location & Event Data) | Conflict & protest | Tier 1 |
| [gdelt.md](gdelt.md) | GDELT (Global Database of Events, Language, and Tone) | Global events & media | Tier 1 |
| [emdat.md](emdat.md) | EM-DAT (International Disaster Database) | Natural disasters | Tier 1 |
| [wfp-food-prices.md](wfp-food-prices.md) | WFP Food Price Data | Food commodity prices | Tier 1 |
| [chirps.md](chirps.md) | CHIRPS (Climate Hazards Group InfraRed Precipitation) | Rainfall/precipitation | Tier 1 |
| [prio-grid.md](prio-grid.md) | PRIO-GRID | Spatial framework | Tier 1 |
| [hdx-hapi.md](hdx-hapi.md) | HDX HAPI (Humanitarian API) | Humanitarian indicators | Tier 1 |
| [usgs-earthquakes.md](usgs-earthquakes.md) | USGS Earthquake Hazards | Seismic events | Tier 2 |
| [openaq.md](openaq.md) | OpenAQ | Air quality / pollution | Tier 2 |
| [ucdp-ged.md](ucdp-ged.md) | UCDP-GED | Armed conflict (researcher-coded) | Tier 2 |
| [nightlights.md](nightlights.md) | VIIRS Nighttime Lights | Economic activity proxy | Tier 2 |
| [ndvi-vegetation.md](ndvi-vegetation.md) | MODIS/VIIRS NDVI | Vegetation health | Tier 2 |
| [world-bank.md](world-bank.md) | World Bank Open Data | Development indicators | Tier 2 |
| [fao-data.md](fao-data.md) | FAO (FAOSTAT, pesticides, crops) | Agriculture | Tier 2 |
| [disease-outbreaks.md](disease-outbreaks.md) | WHO GHO, ProMED, IHME GBD | Health & disease | Tier 2 |
| [other-sources.md](other-sources.md) | Additional sources discovered during research | Various | Tier 3 |
