# Dataset Synthesis: Master Integration Plan

> **Last updated:** March 2026
> **Status:** Pre-implementation reference document
> **Purpose:** Bridge between individual dataset deep-dives and data integration techniques — the operational blueprint for combining 16+ data sources into a unified spatiotemporal analysis platform

---

## Table of Contents

1. [Cross-Dataset Comparison Matrix](#1-cross-dataset-comparison-matrix)
2. [Temporal Alignment Strategy](#2-temporal-alignment-strategy)
3. [Spatial Overlap and Deduplication](#3-spatial-overlap-and-deduplication)
4. [Variable Naming Convention](#4-variable-naming-convention)
5. [Priority Integration Order](#5-priority-integration-order)
6. [Data Conflict Resolution](#6-data-conflict-resolution)
7. [Quality-Weighted Integration](#7-quality-weighted-integration)
8. [Derived Variables](#8-derived-variables)
9. [Known Data Gaps](#9-known-data-gaps)
10. [Data Update Pipeline Design](#10-data-update-pipeline-design)

---

## 1. Cross-Dataset Comparison Matrix

This table synthesises the key characteristics of every candidate data source, drawn from the individual deep-dives in `research/datasets/`. It is the single reference for deciding how each source maps onto the Causal Atlas spatial and temporal backbone.

### 1.1 Primary Datasets

| Dataset | Spatial Resolution | Spatial Coverage | Temporal Resolution | Temporal Range | Update Frequency | Access Method | Auth Required | Licence | Data Format | Approx. Volume | PRIO-GRID Compatibility |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **ACLED** | Point (lat/lon) | Global (250+ countries) | Daily (event-dated) | 1997--present (Africa); 2018--present (global) | Weekly (Friday) | REST API, bulk CSV | API key (free registration) | Free non-commercial; commercial requires agreement | CSV, JSON, Excel | ~1.4M events, ~500 MB | Moderate -- spatial join required |
| **UCDP-GED** | Point (lat/lon) | Global | Daily (event-dated) | 1989--present | Annual (monthly candidates) | REST API, bulk CSV | API token (email request) | CC BY 4.0 | CSV, JSON, Excel, Stata, R | ~350K events, ~200 MB | **Native** -- `priogrid_gid` included |
| **GDELT** | Point (geocoded) | Global | 15-minute intervals | 1979--present (v1); 2015--present (v2) | Every 15 minutes | Bulk CSV, BigQuery | None | Open (see terms) | Tab-delimited CSV | 500M+ events, multi-TB | Moderate -- spatial join required |
| **CHIRPS** | Raster (0.05 deg) | Quasi-global (50S--50N) | Daily / monthly | 1981--present | ~2-day lag (preliminary); ~3-week (final) | FTP, GEE, THREDDS | None | Public domain (USGS) | GeoTIFF, NetCDF, BIL | ~20 GB/year (daily global) | Easy -- aggregate 10x10 pixels per cell |
| **WFP Food Prices** | Point (market locations) | 98 countries (~3,000 markets) | Monthly (some weekly/daily) | ~1992--present (systematic from 2003) | Monthly | DataBridges API, HDX HAPI | API key (free) | CC BY 4.0 IGO | CSV, JSON | ~1M price observations, ~150 MB | Hard -- markets are points in admin regions |
| **EM-DAT** | Admin (country, sometimes sub-national) | Global | Event-dated (imprecise) | 1900--present (systematic from 1988) | Continuous (version releases) | Web download, API (limited) | Registration (free) | Free for non-commercial | CSV, Excel | ~27K disaster events, ~20 MB | Hard -- admin-level, imprecise locations |
| **USGS Earthquakes** | Point (lat/lon/depth) | Global | Millisecond precision | 1638--present (reliable from 1970s) | Real-time (every minute) | REST API, GeoJSON feeds | None | Public domain | GeoJSON, CSV, QuakeML | ~200K events/year (M2.5+), variable | Easy -- point-to-cell assignment |
| **OpenAQ** | Point (station locations) | Global (uneven) | Hourly / sub-hourly | ~2015--present | Near real-time | REST API v3, AWS S3 | API key (free) | Varies by provider (many open) | JSON, Parquet | Tens of millions of measurements | Hard -- sparse stations, many empty cells |
| **HDX HAPI** | Admin (country, admin1, admin2) | ~60+ countries | Monthly / annual | Varies by sub-dataset | Varies (days to months) | REST API | App identifier (free) | See upstream sources | JSON, CSV | Aggregator -- variable | Moderate -- admin-to-grid interpolation |
| **MODIS NDVI** | Raster (250m / 1km / 0.05 deg) | Global land | 16-day / monthly | Feb 2000--present | 16-day composites | NASA LAADS, AppEEARS, GEE | NASA Earthdata login (free) | NASA open data | HDF-EOS, GeoTIFF | ~500 GB/year (1km global) | Easy -- aggregate via zonal stats |
| **VIIRS NDVI** | Raster (500m) | Global land | 16-day (8-day cadence) | Jan 2012--present | 16-day composites | NASA LAADS, GEE | NASA Earthdata login (free) | NASA open data | HDF-EOS | ~300 GB/year | Easy -- aggregate via zonal stats |
| **VIIRS Nightlights (EOG)** | Raster (15 arc-sec, ~500m) | Global (65S--75N) | Monthly / annual | Apr 2012--present | Monthly (~2 month lag) | GEE, EOG direct download | EOG registration (free) for download; none for GEE | CC BY 4.0 | GeoTIFF | ~1 GB/month (global) | Easy -- ~3,600 pixels per cell |
| **DMSP Nightlights** | Raster (30 arc-sec, ~1km) | Global (65S--75N) | Annual | 1992--2013 | Historical archive | GEE, EOG download | None | Public domain | GeoTIFF | ~500 MB/year | Easy -- ~900 pixels per cell |
| **World Bank WDI** | Admin (country) | 217 economies | Annual (some quarterly) | 1960--present | Quarterly | REST API v2 | None | CC BY 4.0 | JSON, CSV, Excel | ~50 MB (full WDI CSV) | Hard -- country broadcast to all cells |
| **World Bank WGI** | Admin (country) | 214 economies | Annual (biennial before 2002) | 1996--present | Annual | REST API v2 (source=3) | None | CC BY 4.0 | JSON, CSV | ~5 MB | Hard -- country broadcast |
| **FAO (FAOSTAT)** | Admin (country) | 245+ countries | Annual | 1961--present | Continuous updates | REST API, bulk CSV/ZIP | None | CC BY-NC-SA 3.0 IGO | CSV, JSON | ~2 GB (full FAOSTAT) | Hard -- country broadcast |
| **WHO GHO** | Admin (country, some sub-national) | 194 WHO member states | Annual | Varies (some from 1950s) | Continuous | REST API (OData) | None | CC BY-NC-SA 3.0 IGO | JSON, CSV | Variable | Hard -- country broadcast |
| **PRIO-GRID** | Grid (0.5 deg) | Global land | Annual / static | Varies by variable (some from 1946) | Irregular (v2.0 in 2012; v3 in development) | Download, R package (v3) | None | CC BY 4.0 | CSV, R, Shapefile | ~200 MB | **Native** -- this IS the grid |

### 1.2 Supplementary Datasets (from `other-sources.md`)

| Dataset | Spatial Resolution | Temporal Resolution | Temporal Range | PRIO-GRID Compatibility | Notes |
|---|---|---|---|---|---|
| **IPC/CH** | Admin (admin2+) | ~quarterly | 2016--present | Moderate | Food security phase classification |
| **FEWS NET** | Admin (livelihood zones) | Dekadal / monthly | ~2000--present | Moderate | Food security outlook and NDVI products |
| **INFORM Risk** | Admin (country) | Annual | 2013--present | Hard | Composite risk index |
| **ERA5** | Raster (0.25 deg) | Hourly | 1940--present | Easy | Reanalysis -- precipitation, temperature, wind |
| **WorldPop** | Raster (100m / 1km) | Annual | 2000--2020 | Easy | Gridded population estimates |
| **GPW v4** | Raster (30 arc-sec) | 5-yearly | 2000, 2005, 2010, 2015, 2020 | Easy | UN-adjusted population counts |
| **V-Dem** | Admin (country) | Annual | 1789--present | Hard | Democracy and governance indicators |
| **FSI** | Admin (country) | Annual | 2006--present | Hard | Fragile States Index |
| **Natural Earth** | Vector (various scales) | Static / infrequent | N/A | Easy | Boundaries, basemaps |
| **geoBoundaries** | Vector (admin0--admin5) | Annual updates | Current | Easy | Open administrative boundaries |
| **GADM** | Vector (admin0--admin5) | Irregular | Current | Easy | Detailed admin boundaries |
| **van Donkelaar PM2.5** | Raster (0.01 deg) | Annual / monthly | 1998--2022 | Easy | Satellite-derived PM2.5 surfaces |
| **MERRA-2** | Raster (0.5 x 0.625 deg) | Hourly / monthly | 1980--present | Easy (near-native) | Aerosol reanalysis |
| **Hansen Forest Change** | Raster (30m) | Annual | 2000--present | Easy | Tree cover loss/gain |
| **JRC Surface Water** | Raster (30m) | Monthly | 1984--present | Easy | Surface water occurrence |

### 1.3 Key Observations from the Matrix

1. **Spatial resolution spans five orders of magnitude**: from 30m (Hansen, JRC) to country-level (World Bank, FAO, WHO). The PRIO-GRID 0.5-degree target (~55km) sits in the middle. Most raster sources are finer and require aggregation; most socioeconomic sources are coarser and require disaggregation or broadcasting.

2. **Temporal resolution varies by three orders of magnitude**: from 15-minute GDELT updates to annual World Bank releases. Monthly is the practical common denominator for causal analysis.

3. **Two datasets have native PRIO-GRID compatibility**: UCDP-GED (includes `priogrid_gid`) and PRIO-GRID itself. Every other dataset requires spatial transformation.

4. **Authentication ranges from none to token-required**: USGS, GDELT, and World Bank are fully open. ACLED, UCDP, and OpenAQ require free registration/tokens. No dataset requires paid access for research use, though ACLED's commercial licence is restrictive.

5. **Volume is dominated by raster datasets**: CHIRPS, NDVI, and nightlights together represent hundreds of GB per year. Point and tabular datasets are orders of magnitude smaller.

---

## 2. Temporal Alignment Strategy

### 2.1 The Canonical Temporal Unit

**Decision: The primary temporal unit for Causal Atlas is the calendar month, with the last day of the month (YYYY-MM-DD where DD is the last day) as the canonical timestamp.**

Rationale:
- Monthly is the highest resolution at which all priority datasets can meaningfully overlap.
- CHIRPS produces monthly composites. NDVI monthly composites (MOD13A3) are standard. WFP food prices are predominantly monthly. PRIO-GRID v2 uses yearly; VIEWS uses monthly for its PRIO-GRID cell predictions.
- Daily resolution is preserved in the underlying event data (ACLED, UCDP, USGS) for event-level analysis, but statistical causal methods (Granger causality, PCMCI, transfer entropy) operate on regular time series -- monthly is the practical choice.
- AfroGrid uses the same monthly-within-annual structure, validating this approach.

**Why month-end rather than mid-month:** Month-end aligns with how most monthly aggregation is naturally computed (sum/mean over the calendar month). Using mid-month (the 15th) would create ambiguity about whether a value represents the month to date or the full month. VIEWS uses month identifiers rather than specific dates. We adopt `YYYY-MM` as the period identifier, with the understanding that each row represents the full calendar month.

### 2.2 Source-Specific Temporal Alignment Rules

#### CHIRPS (daily/monthly precipitation)

- **Daily data**: Available from 1981 at 0.05-degree resolution. Sum daily values within each calendar month to produce monthly accumulated precipitation per PRIO-GRID cell.
- **Monthly composites**: CHIRPS provides pre-aggregated monthly totals. These are the primary ingestion target.
- **Preliminary vs. final**: CHIRPS publishes preliminary data with ~2-day lag, and final data with ~3-week lag. **Decision: Ingest preliminary for near-real-time monitoring; replace with final when available.** Flag the data status (`preliminary` / `final`) in a metadata column.
- **v2.0 to v3.0 transition**: CHIRPS v2.0 production continues through December 2026. v3.0 (released 2024) has 4x more station data and extends to 60N/S. **Decision: Begin ingesting v3.0 in parallel; when v2.0 ceases, switch. During overlap, compare and document any systematic differences.**

#### ACLED (weekly event releases)

- Events have specific dates (`event_date`). Aggregate to calendar month by assigning each event to its month.
- **Weekly release cycle**: ACLED releases data on Fridays, covering events approximately through the previous Saturday. Events from the last few days of a month may not appear until the first weekly release of the following month.
- **Decision**: For each monthly close, wait until at least the second weekly ACLED release of the following month before considering the previous month's data "complete". Flag month-data as `preliminary` until this point.
- **Historical revisions**: ACLED is a "living dataset" -- events can be added, revised, or removed in subsequent releases. Track the ACLED `timestamp` field to detect revisions.

#### WFP Food Prices (market prices)

- Prices are conventionally recorded with a date, often the 15th of the month for monthly observations.
- **Decision**: Treat each price observation as representing the calendar month indicated by its date, regardless of the specific day. For weekly or daily sub-monthly data, compute the monthly mean price per market per commodity.
- **Multiple commodities per market**: Store disaggregated (one row per market-commodity-month), then compute composite indices as derived variables.

#### EM-DAT (disaster events with imprecise dates)

- EM-DAT records `start_date` and `end_date` for each disaster, but many events have imprecise dates (month or even year only).
- **Decision for multi-month events**: Assign the event to all months it spans. For fatalities, deaths, and affected population counts (extensive variables), distribute evenly across months unless more specific information is available. Flag distributed values with an `estimated` quality indicator.
- **Decision for imprecise dates**: If only the year is known, distribute evenly across 12 months. If only month and year are known, assign to that month. Document the `date_prec` equivalent.

#### World Bank and FAO (annual data)

- Annual data cannot be meaningfully downscaled to monthly without strong assumptions.
- **Decision**: Store as annual values and broadcast to all 12 months of the year. In the data schema, mark `temporal_resolution = 'annual'` so that downstream analysis tools know not to interpret monthly variation. Alternatively, provide the value only for the month of December (year-end) and leave other months as NULL, with forward-fill available as an option.
- **For GDP and population**: Consider using nighttime lights as a monthly proxy for sub-annual economic variation, calibrated against annual World Bank GDP.
- **Temporal downscaling**: The data integration techniques document (Section 21) discusses model-based temporal downscaling. For GDP, a Chow-Lin procedure using monthly nightlights as an indicator series is well-established.

#### UCDP-GED (annual release with monthly candidates)

- GED has daily date precision (`date_start`, `date_end`). Aggregate to month using `date_start`.
- **Candidate vs. final**: Candidate events are released monthly with ~1-month lag. ~90% of candidates survive to final GED. **Decision**: Use candidate data for months not yet covered by the annual GED release. When a new GED version drops, replace candidate data with verified data and log any differences.
- **Multi-day events**: Assign to the month of `date_start`. If an event spans a month boundary, assign to the month containing the majority of days, or the start month if evenly split.

#### GDELT (15-minute updates)

- GDELT's 15-minute granularity is far higher than needed for monthly causal analysis.
- **Decision**: Pre-aggregate GDELT events to monthly cell counts by CAMEO root code. Compute: event count, mean GoldsteinScale, mean AvgTone, mention count.
- **Media volume as signal**: GDELT event counts reflect media attention, not ground truth. Monthly aggregation smooths daily noise. The absolute count is less meaningful than relative changes (month-over-month or anomaly from baseline).
- **Storage**: Given GDELT's massive volume (~500 MB/day uncompressed), pre-aggregate via BigQuery rather than ingesting raw 15-minute files.

#### Nightlights (VIIRS monthly composites)

- EOG monthly composites are released with ~2-month lag. **Decision**: Ingest when available; flag the month as pending until the composite arrives.
- **Negative radiance values**: Set to zero (these are noise in low-radiance areas).
- **Cloud-free coverage count**: Store `cf_cvg` alongside radiance. Cells with very low coverage (<5 observations in a month) should be flagged as unreliable.

#### NDVI (MODIS/VIIRS monthly)

- MOD13A3 monthly composites are derived from 16-day composites. Temporal alignment to calendar months is handled by the product itself.
- **Quality filtering**: Apply `SummaryQA` mask (retain values 0 and 1) before aggregation.
- **Decision**: Use MODIS MOD13A3 as primary (longest record, from Feb 2000). Plan for VIIRS VNP13A3 continuity post-MODIS.

### 2.3 Handling Reporting Lags

| Source | Typical Lag | Implication |
|---|---|---|
| GDELT | Minutes | Near-real-time; use for early signals |
| USGS earthquakes | Minutes (auto) to days (reviewed) | Near-real-time |
| ACLED | ~1 week | Monthly data is "complete" ~2 weeks after month-end |
| CHIRPS preliminary | ~2 days | Use for initial monthly estimate |
| CHIRPS final | ~3 weeks | Replace preliminary |
| OpenAQ | Hours to days | Depends on provider |
| UCDP candidates | ~1 month | Interim conflict data |
| VIIRS nightlights | ~2 months | Delayed economic proxy |
| MODIS NDVI monthly | ~1 month | Standard remote sensing lag |
| World Bank WDI | 1--2 years | Structural context, not real-time |
| FAO FAOSTAT | 1--2 years | Structural context |
| EM-DAT | Variable (days to months) | Impact data arrives in waves |
| UCDP GED (annual) | 6--12 months | Gold-standard conflict data, delayed |

**Decision**: Implement a two-stage pipeline:
1. **Near-real-time layer** (updated daily/weekly): GDELT, USGS, ACLED, CHIRPS preliminary, OpenAQ
2. **Analytical layer** (updated monthly): CHIRPS final, NDVI, nightlights, UCDP candidates, WFP prices, HDX HAPI
3. **Context layer** (updated annually): World Bank, FAO, WGI, FSI, PRIO-GRID static variables, UCDP GED (final)

---

## 3. Spatial Overlap and Deduplication

### 3.1 ACLED vs. UCDP-GED: Conflict Event Deduplication

These two datasets cover overlapping events but with fundamentally different coding methodologies. Based on the comparative literature (Eck 2012, "In data we trust?"; Oberg & Yilmaz 2025), the key differences are:

| Dimension | ACLED | UCDP-GED |
|---|---|---|
| **Inclusion threshold** | No minimum fatality threshold | 25 deaths/year per conflict dyad |
| **Event types** | Battles, protests, riots, strategic developments, violence against civilians | State-based, non-state, one-sided violence (armed only) |
| **Coding method** | Research assistants + AI assistance | Fully human-coded research team |
| **Fatality estimates** | Single best estimate (often 0 or unreported) | Low / best / high range |
| **Update cadence** | Weekly | Annual (monthly candidates) |
| **PRIO-GRID ID** | Not included | Included natively |

**Deduplication strategy:**

1. **Do not attempt event-level deduplication.** The coding methodologies are too different for reliable one-to-one matching. An ACLED "battle" may be coded as 1, 2, or 3 UCDP events (or none, if below the 25-death threshold). Conversely, UCDP may record a multi-day battle as a single event that ACLED splits into daily incidents.

2. **Aggregate to cell-month and treat as complementary signals:**
   - `conflict_events_count_acled`: total ACLED events per cell-month (all types)
   - `conflict_battles_count_acled`: ACLED battles only
   - `conflict_fatalities_sum_acled`: ACLED fatality sum
   - `conflict_events_count_ucdp`: UCDP events per cell-month
   - `conflict_fatalities_best_ucdp`: UCDP best-estimate fatalities
   - `conflict_fatalities_low_ucdp` / `conflict_fatalities_high_ucdp`: uncertainty range

3. **Cross-validation**: Where both datasets report conflict events in the same cell-month, compute a concordance score. High concordance increases confidence. Discordance flags cells for closer examination.

4. **Preference hierarchy**: For armed violence specifically, prefer UCDP-GED as the conservative, research-validated baseline. Use ACLED for broader event coverage (protests, riots) and for timeliness (weekly vs. annual). This matches the approach taken by VIEWS, which uses UCDP as its primary conflict data source.

### 3.2 GDELT vs. ACLED: Media Events vs. Researcher-Coded Events

GDELT and ACLED serve fundamentally different purposes and should not be treated as substitutes:

- **GDELT** measures media attention and discourse. It is machine-coded from news articles and captures what is *reported*, not necessarily what *happened*. Event counts are heavily influenced by media coverage density, language, and source availability.
- **ACLED** provides researcher-verified event records with controlled coding.

**Complementary use strategy:**
- Use GDELT as a **media attention index** alongside ACLED ground-truth events. A cell-month with high GDELT event counts but no ACLED events may indicate media concern without verified incidents (or early warning signals before ACLED captures events).
- Use GDELT GKG tone and emotion measures as **sentiment context** for ACLED-coded events.
- **Never sum or average GDELT and ACLED event counts.** They are measuring different things.

### 3.3 CHIRPS vs. ERA5 Precipitation

Both provide gridded precipitation, but from different methodologies:

| Aspect | CHIRPS | ERA5 |
|---|---|---|
| **Method** | Satellite IR + station blending | Atmospheric reanalysis model |
| **Resolution** | 0.05 deg (~5.5 km) | 0.25 deg (~28 km) |
| **Coverage** | 50S--50N (quasi-global) | Global |
| **Temporal** | Daily / monthly, 1981--present | Hourly, 1940--present |
| **Strengths** | Better in complex terrain (Africa, South Asia); higher spatial resolution | Global coverage including high latitudes; sub-daily resolution; includes temperature, wind, humidity |
| **Weaknesses** | No coverage poleward of 50 deg; station density affects quality | Underestimates extreme precipitation; drying bias in sub-Saharan Africa |

Research findings (evaluation studies over Ethiopia and West/Central Africa) indicate that **CHIRPS generally outperforms ERA5 for precipitation in Africa**, particularly in regions with complex topography and for detecting high-intensity rainfall events. ERA5 shows a drying bias in sub-Saharan Africa that contradicts station observations.

**Decision:**
- **Primary precipitation source: CHIRPS** for the 50S--50N belt where it is available.
- **Supplementary: ERA5** for (a) regions outside CHIRPS coverage (high latitudes), (b) temperature data (CHIRPS is precipitation only), (c) sub-daily temporal resolution when needed, and (d) pre-1981 historical context.
- **Discrepancy handling**: Where both sources are available, store both values. For derived drought indices (SPI), use CHIRPS-based calculations as primary. Flag cells where CHIRPS and ERA5 monthly totals differ by more than 50% for quality review.

### 3.4 MODIS NDVI vs. VIIRS NDVI

- **MODIS** (MOD13A3): February 2000--present. Longest continuous record. Sensor degradation post-2020 (Terra orbit decay).
- **VIIRS** (VNP13A1/A3): January 2012--present. Better calibration, higher spatial resolution (500m vs 1km), intended successor.
- **Systematic bias**: VIIRS NDVI is ~0.01--0.02 units higher than MODIS due to different spectral band widths.

**Decision:**
- Use MODIS as primary for the full 2000--present record.
- Do NOT naively concatenate MODIS and VIIRS series. Instead, compute anomalies relative to sensor-specific baselines:
  - MODIS anomalies: relative to 2001--2020 MODIS climatology
  - VIIRS anomalies: relative to 2012--2022 VIIRS climatology
- During the overlap period (2012--present), compute cross-calibration offsets for each PRIO-GRID cell.
- When MODIS ceases operation (expected ~2026--2027), transition to VIIRS with documented calibration adjustments.

### 3.5 DMSP vs. VIIRS Nightlights

- **DMSP-OLS** (1992--2013): Uncalibrated DN (0--63), saturates in bright areas, blooming effects. Annual only.
- **VIIRS EOG** (2012--present): Calibrated radiance (nW/cm2/sr), no saturation, monthly resolution.
- **Overlap period**: 2012--2013.

**Decision:**
- For 2014--present: use VIIRS EOG monthly composites (VCMSLCFG -- stray-light corrected).
- For 1992--2013: use the Li et al. (2020) harmonised DMSP-VIIRS dataset (available through 2024 in later versions), which applies sigmoid calibration to create a consistent time series at 30 arc-second resolution.
- For the 2012--2013 overlap: use the harmonised product rather than mixing raw DMSP and VIIRS.

### 3.6 WFP Food Prices vs. FAO Food Prices

| Aspect | WFP | FAO (FPMA/GIEWS) |
|---|---|---|
| **Resolution** | Market-level (point) | Country-level (national averages) |
| **Commodities** | Staple foods in crisis countries | Broader agricultural commodities |
| **Markets** | ~3,000 in 98 countries | National averages for 90+ countries |
| **Frequency** | Monthly (some weekly) | Monthly |
| **Focus** | Food security in vulnerable countries | Global agricultural trade |

**Decision:**
- Use WFP as primary for sub-national food price analysis (it has market-level granularity).
- Use FAO for country-level commodity price indices and for countries not covered by WFP.
- When both exist for the same country, WFP sub-national data takes precedence for cell-level analysis; FAO provides the national context.

### 3.7 HDX HAPI vs. Individual APIs

HDX HAPI is an aggregator that provides ACLED, WFP, IPC, INFORM, and other data through a single interface.

**Decision:**
- Use individual source APIs (ACLED, WFP DataBridges) as primary ingestion points for tier-1 datasets -- they provide richer data and more flexible queries.
- Use HDX HAPI for (a) datasets where it is the easiest access point (IPC, INFORM, operational presence), (b) rapid prototyping, and (c) cross-checking data consistency.
- HDX HAPI's standardised admin-region coding (P-codes) is valuable for spatial harmonisation.

### 3.8 WorldPop vs. GPW Population

| Aspect | WorldPop | GPW v4 |
|---|---|---|
| **Resolution** | 100m / 1km | 30 arc-sec (~1km) |
| **Method** | Random forest model using covariates (nightlights, land cover, roads) | Proportional allocation of census to grid |
| **Frequency** | Annual (2000--2020) | Every 5 years (2000, 2005, 2010, 2015, 2020) |
| **Adjustment** | UN WPP-adjusted versions available | UN-adjusted versions available |

**Decision:**
- Use **WorldPop UN-adjusted 1km** as primary (annual availability, dasymetric method accounts for settlement patterns).
- Use GPW for cross-validation and for analyses requiring strict census-consistency.
- For PRIO-GRID cells: aggregate using zonal sum (population is an extensive variable).

### 3.9 Multiple Governance Datasets (WGI, V-Dem, FSI)

| Dataset | Coverage | Dimensions | Scale | Temporal Depth |
|---|---|---|---|---|
| **WGI** | 214 countries | 6 governance dimensions | -2.5 to +2.5 (+ new 0--100) | 1996--present |
| **V-Dem** | 202 countries | 470+ indicators, 5 high-level indices | 0--1 (indices) | 1789--present |
| **FSI** | 179 countries | 12 fragility indicators | 0--120 (composite) | 2006--present |

**Decision:**
- All three provide country-year governance/fragility context. They are correlated but capture different aspects.
- **Primary**: WGI (broadest use in conflict research, available via World Bank API, used by VIEWS).
- **Supplementary**: V-Dem for deeper democracy analysis; FSI for fragility-specific analysis.
- Store all three. In causal models, use one at a time (to avoid collinearity) or extract principal components across all governance measures.

---

## 4. Variable Naming Convention

### 4.1 Schema

Every variable in the Causal Atlas unified dataset follows this pattern:

```
{domain}_{variable}_{aggregation}_{source}
```

| Component | Options | Examples |
|---|---|---|
| **Domain prefix** | `conflict`, `climate`, `food`, `health`, `econ`, `env`, `gov`, `pop`, `disaster` | `conflict_`, `climate_` |
| **Variable name** | Descriptive, snake_case | `fatalities`, `precip_mm`, `price_usd`, `ndvi`, `radiance_nw`, `pm25_ugm3`, `gdp_usd` |
| **Aggregation suffix** | `_count`, `_sum`, `_mean`, `_max`, `_min`, `_std`, `_median`, `_pct`, `_anomaly`, `_zscore` | `_sum`, `_mean` |
| **Source suffix** | `_acled`, `_ucdp`, `_chirps`, `_era5`, `_modis`, `_viirs`, `_wfp`, `_fao`, `_wb`, `_usgs`, `_gdelt`, `_emdat`, `_openaq`, `_who`, `_worldpop`, `_gpw` | `_chirps`, `_acled` |

### 4.2 Examples

| Variable Name | Description | Unit | Source |
|---|---|---|---|
| `conflict_events_count_acled` | Number of ACLED events in cell-month | count | ACLED |
| `conflict_battles_count_acled` | Number of ACLED battle events | count | ACLED |
| `conflict_fatalities_sum_acled` | Total ACLED fatalities in cell-month | persons | ACLED |
| `conflict_fatalities_best_ucdp` | UCDP best-estimate fatalities | persons | UCDP-GED |
| `conflict_fatalities_low_ucdp` | UCDP low-estimate fatalities | persons | UCDP-GED |
| `conflict_fatalities_high_ucdp` | UCDP high-estimate fatalities | persons | UCDP-GED |
| `conflict_events_count_ucdp` | UCDP event count | count | UCDP-GED |
| `conflict_onesided_count_ucdp` | UCDP one-sided violence events | count | UCDP-GED |
| `climate_precip_mm_sum_chirps` | Monthly precipitation total | mm | CHIRPS |
| `climate_precip_mm_mean_era5` | Monthly mean precipitation rate | mm/day | ERA5 |
| `climate_temp_c_mean_era5` | Monthly mean temperature | degrees C | ERA5 |
| `food_price_usd_mean_wfp` | Mean food price (local currency converted) | USD | WFP |
| `food_price_maize_usd_mean_wfp` | Mean maize price | USD/kg | WFP |
| `food_alps_alert_max_wfp` | Maximum ALPS alert level in cell-month | categorical | WFP |
| `env_ndvi_mean_modis` | Mean NDVI in cell-month | unitless (0--1) | MODIS MOD13A3 |
| `env_ndvi_anomaly_zscore_modis` | NDVI z-score anomaly vs 2001--2020 baseline | std deviations | MODIS MOD13A3 |
| `env_ndvi_mean_viirs` | Mean NDVI from VIIRS | unitless (0--1) | VIIRS VNP13A1 |
| `econ_ntl_radiance_mean_viirs` | Mean nighttime light radiance | nW/cm2/sr | VIIRS EOG |
| `econ_ntl_radiance_sum_viirs` | Sum of lights (total radiance) | nW/cm2/sr | VIIRS EOG |
| `econ_ntl_change_pct_viirs` | Month-over-month NTL change | percent | VIIRS EOG |
| `econ_gdp_usd_mean_wb` | GDP (current USD, country broadcast) | USD | World Bank |
| `econ_gdp_pcap_usd_mean_wb` | GDP per capita | USD | World Bank |
| `econ_inflation_pct_mean_wb` | Inflation rate | percent | World Bank |
| `gov_polstab_score_mean_wgi` | Political stability score | -2.5 to +2.5 | WGI |
| `gov_corruption_score_mean_wgi` | Control of corruption score | -2.5 to +2.5 | WGI |
| `pop_total_sum_worldpop` | Total population in cell | persons | WorldPop |
| `pop_density_mean_worldpop` | Population density | persons/km2 | WorldPop |
| `disaster_earthquake_count_usgs` | Earthquake events in cell-month | count | USGS |
| `disaster_earthquake_mag_max_usgs` | Maximum earthquake magnitude | Richter | USGS |
| `disaster_deaths_sum_emdat` | EM-DAT disaster deaths (distributed) | persons | EM-DAT |
| `health_pm25_ugm3_mean_openaq` | Mean PM2.5 from ground stations | ug/m3 | OpenAQ |
| `health_pm25_ugm3_mean_merra2` | Mean PM2.5 from reanalysis | ug/m3 | MERRA-2 |

### 4.3 Metadata Columns

Every cell-month record also carries:

| Column | Description |
|---|---|
| `pgid` | PRIO-GRID cell ID |
| `year` | Calendar year |
| `month` | Calendar month (1--12) |
| `period` | `YYYY-MM` string identifier |
| `lat` | Cell centroid latitude |
| `lon` | Cell centroid longitude |
| `country_iso3` | ISO 3166-1 alpha-3 country code |
| `country_gwno` | Gleditsch-Ward country number |
| `land_area_km2` | Land area of cell in km2 |

---

## 5. Priority Integration Order

### 5.1 Phase 1: MVP (Months 1--3)

**Datasets:** ACLED + CHIRPS + WFP Food Prices

**Justification:** These three datasets form the minimum viable platform for demonstrating cross-domain causal discovery. They cover the climate-food-conflict nexus, which is the most well-studied and policy-relevant causal chain.

**Causal chains enabled:**
- Rainfall anomaly (CHIRPS) -> food price spike (WFP) [1--3 month lag]
- Food price spike (WFP) -> protest/unrest (ACLED) [0--3 month lag]
- Rainfall deficit (CHIRPS) -> conflict escalation (ACLED) [3--12 month lag]

**Implementation tasks:**
1. Build PRIO-GRID cell geometry (global 0.5-deg grid with land mask, country assignments)
2. Ingest CHIRPS monthly precipitation, aggregate to grid cells
3. Ingest ACLED events, assign to grid cells, aggregate to monthly counts/fatalities
4. Ingest WFP food prices, assign to nearest grid cells or admin-to-grid mapping
5. Compute precipitation anomalies (SPI-1, SPI-3)
6. Run initial Granger causality tests on selected countries

**Expected data volume:** ~5 GB (compressed Parquet)

**Validation:** Compare results against published findings on the Sahel drought-conflict nexus and East Africa food price-conflict studies.

### 5.2 Phase 2: Cross-Validation and Economic Proxy (Months 4--6)

**Add:** UCDP-GED + MODIS NDVI + VIIRS Nightlights

**Justification:** UCDP-GED provides the research-validated conflict baseline for cross-validation against ACLED. NDVI is the critical intermediate variable between rainfall and crop production. Nightlights provide a sub-national, sub-annual economic activity proxy.

**New causal chains unlocked:**
- Rainfall (CHIRPS) -> vegetation response (NDVI) -> crop failure indicator [1--3 month lag]
- NDVI anomaly -> food price spike (WFP) [1--3 month lag]
- Conflict (ACLED/UCDP) -> economic decline (nightlights) [1--6 month lag]
- Drought (CHIRPS/NDVI) -> economic decline (nightlights) [3--12 month lag]
- Cross-validation: ACLED vs. UCDP event counts and fatalities

**Implementation tasks:**
1. Ingest UCDP-GED (bulk CSV, use native `priogrid_gid`)
2. Ingest MODIS NDVI monthly via GEE, aggregate to grid cells
3. Ingest VIIRS nightlights monthly via GEE, aggregate to grid cells
4. Compute NDVI anomalies (z-scores) and VCI
5. Compute nightlight change indicators
6. Implement ACLED-UCDP concordance scoring

**Expected data volume:** +15 GB (cumulative ~20 GB)

### 5.3 Phase 3: Disasters and Humanitarian Indicators (Months 7--9)

**Add:** EM-DAT + USGS Earthquakes + HDX HAPI

**Justification:** Extends coverage to natural disasters and humanitarian response indicators. Enables analysis of disaster-to-conflict and disaster-to-displacement causal chains.

**New causal chains unlocked:**
- Earthquake (USGS) -> displacement (HDX HAPI) [days to weeks]
- Earthquake (USGS) -> nightlight decline (VIIRS) -> economic recovery trajectory [weeks to months]
- Flood/drought disaster (EM-DAT) -> food price spike (WFP) [1--6 months]
- Disaster (EM-DAT) -> conflict (ACLED/UCDP) [contested; months to years]
- Displacement (HDX HAPI) -> food insecurity (WFP/IPC) [weeks to months]

**Implementation tasks:**
1. Ingest USGS earthquake catalog, assign to grid cells, aggregate monthly
2. Ingest EM-DAT with temporal distribution logic
3. Ingest HDX HAPI displacement and food security indicators (IPC phases)
4. Build disaster-triggered event analysis framework

**Expected data volume:** +5 GB (cumulative ~25 GB)

### 5.4 Phase 4: Context Variables (Months 10--14)

**Add:** World Bank (WDI + WGI) + FAO (FAOSTAT) + WorldPop + V-Dem/FSI

**Justification:** Country-level structural variables are essential control variables in causal models. Without economic context (GDP), governance quality (WGI), agricultural structure (FAO), and population (WorldPop), any detected causal relationships may be confounded.

**New causal chains unlocked (as moderators):**
- Low GDP (WB) amplifies drought -> conflict pathway
- Weak governance (WGI) amplifies food crisis -> unrest pathway
- High agricultural dependency (FAO) amplifies rainfall -> economic impact
- Population density (WorldPop) moderates conflict intensity per event

**Implementation tasks:**
1. Ingest World Bank WDI and WGI via `wbgapi`
2. Ingest FAO crop production and trade data via FAOSTAT API
3. Ingest WorldPop annual population grids, aggregate to PRIO-GRID
4. Build country-to-grid broadcast layer
5. Implement temporal downscaling for annual variables

**Expected data volume:** +10 GB (cumulative ~35 GB)

### 5.5 Phase 5: Full Platform (Months 15--18)

**Add:** GDELT + OpenAQ + Disease Outbreaks (WHO GHO, ProMED) + ERA5 + Remaining sources

**Justification:** Completes the full Causal Atlas vision with media signals, air quality, disease, and comprehensive climate data.

**New causal chains unlocked:**
- Air pollution (OpenAQ/MERRA-2) -> respiratory disease (WHO) [chronic; years]
- Conflict (ACLED) -> industrial destruction -> pollution spike (OpenAQ) [days]
- Agricultural burning -> PM2.5 spike (OpenAQ) -> health burden [days to weeks]
- Climate (ERA5 temperature) -> disease transmission (WHO) [weeks to months]
- Media attention (GDELT) as leading indicator of crisis escalation
- Cross-domain: forest loss (Hansen) -> rainfall change (CHIRPS) -> food security [years]

**Implementation tasks:**
1. Set up GDELT monthly aggregation pipeline (BigQuery)
2. Ingest OpenAQ reference-grade station data, supplement with MERRA-2 gridded PM2.5
3. Ingest WHO GHO indicators
4. Ingest ERA5 temperature and additional climate variables
5. Complete the full cross-domain analysis framework

**Expected data volume:** +50 GB (cumulative ~85 GB, dominated by ERA5 and GDELT aggregates)

---

## 6. Data Conflict Resolution

### 6.1 Decision Framework

When sources disagree on the same phenomenon, apply this hierarchy:

```
1. Is one source methodologically closer to ground truth?
   -> Prefer the more direct measurement.

2. Is one source more spatially/temporally precise?
   -> Prefer the higher-resolution source.

3. Is one source more conservative/validated?
   -> Prefer the peer-reviewed/researcher-coded source.

4. Can the sources be combined into an ensemble estimate?
   -> Use weighted averaging with quality scores.

5. None of the above?
   -> Present all sources transparently; let the analyst choose.
```

### 6.2 Specific Conflict Resolution Rules

#### Conflict event counts: ACLED says 50, UCDP says 30

This is expected and not an error. The difference is primarily driven by:
- ACLED's lower inclusion threshold (no minimum fatalities)
- ACLED's broader event type coverage (protests, riots)
- UCDP's 25-death annual threshold

**Resolution:**
- **Do not average.** Report both values in separate columns.
- For "armed violence" analysis: use UCDP (more conservative, validated).
- For "political instability" analysis: use ACLED (broader coverage).
- For forecasting models: test both; ensemble if both improve predictions.

#### Precipitation: CHIRPS vs. ERA5 differ for same cell-month

**Resolution:**
- **Default to CHIRPS** within its coverage area (50S--50N), based on validation studies showing superior performance in Africa and South Asia.
- **Use ERA5** outside CHIRPS coverage or when temperature/wind data is also needed.
- If both are stored, analysts can choose. Flag cases where discrepancy exceeds 50% of the CHIRPS value.
- For ensemble analysis: weighted average (CHIRPS weight 0.7, ERA5 weight 0.3 within CHIRPS domain).

#### Population: WorldPop vs. GPW vs. UN WPP

**Resolution:**
- **WorldPop UN-adjusted** is the primary gridded population source (dasymetric method, annual availability).
- GPW is used for validation and for analyses requiring strict census alignment.
- UN WPP provides the national totals to which both are adjusted.
- All three will agree at the national level (after adjustment); differences appear in sub-national distribution.

#### Admin boundaries: GADM vs. geoBoundaries vs. national sources

**Resolution:**
- **geoBoundaries** as primary (open licence, globally consistent, annual updates, DOI-versioned).
- GADM for higher detail where needed (but non-commercial licence restricts use).
- Natural Earth for cartographic display.
- **Boundary disputes**: Where sovereignty is contested (e.g., Kashmir, Western Sahara, Crimea), use the geoBoundaries "Comprehensive" layer which includes all claimed boundaries with metadata on dispute status. Do not take sides; present data for disputed areas with appropriate caveats.

### 6.3 The "Present All" Principle

For any cell-month where multiple sources measure the same underlying phenomenon, the default is to **store all values in separate columns** using the naming convention (Section 4). This allows:
- Analysts to choose the most appropriate source for their research question
- Ensemble methods to combine sources with appropriate weighting
- Transparency about measurement uncertainty

The Causal Atlas interface should offer source selection as a user-facing option, not hide disagreements.

---

## 7. Quality-Weighted Integration

### 7.1 Quality Scores by Dataset

Based on the individual deep-dives, each dataset receives a quality score (1--5) on four dimensions:

| Dataset | Spatial Precision | Temporal Precision | Completeness | Methodological Rigour | Overall |
|---|---|---|---|---|---|
| UCDP-GED | 4 (precision coded) | 5 (daily, coded) | 3 (25-death threshold) | 5 (human-coded, peer-reviewed) | 4.3 |
| ACLED | 4 (precision coded) | 5 (daily) | 4 (no threshold) | 4 (research assistants + AI) | 4.3 |
| CHIRPS | 5 (0.05 deg gridded) | 5 (daily available) | 4 (quasi-global, station-dependent) | 5 (published, validated) | 4.8 |
| WFP Food Prices | 3 (market points, sparse) | 4 (monthly) | 3 (98 countries, crisis-focused) | 4 (standardised collection) | 3.5 |
| MODIS NDVI | 5 (250m--1km) | 4 (16-day/monthly) | 5 (global land) | 5 (NASA standard product) | 4.8 |
| VIIRS Nightlights | 5 (500m) | 4 (monthly) | 4 (65S--75N, cloud issues) | 4 (calibrated radiance) | 4.3 |
| USGS Earthquakes | 5 (point + uncertainty) | 5 (millisecond) | 4 (complete above M4.5 globally) | 5 (seismological network) | 4.8 |
| World Bank WDI | 1 (country only) | 2 (annual) | 4 (217 economies) | 5 (harmonised methodology) | 3.0 |
| FAO FAOSTAT | 1 (country only) | 2 (annual) | 4 (245+ countries) | 4 (official statistics) | 2.8 |
| GDELT | 3 (geocoded from text) | 5 (15-minute) | 4 (global media) | 2 (machine-coded, noisy) | 3.5 |
| EM-DAT | 2 (country/sub-national) | 2 (imprecise dates) | 3 (threshold-based) | 4 (curated, peer-reviewed) | 2.8 |
| OpenAQ | 4 (station points) | 5 (hourly) | 2 (sparse in developing countries) | 3 (no QC by OpenAQ) | 3.5 |
| WHO GHO | 1 (country) | 2 (annual) | 4 (194 member states) | 4 (WHO methodology) | 2.8 |
| HDX HAPI | 2 (admin levels) | 3 (varies) | 3 (~60 countries) | 3 (aggregator quality) | 2.8 |

### 7.2 Spatial Precision Weighting

For point-event datasets (ACLED, UCDP), each event carries a precision code indicating location confidence. Weight events by precision in analysis:

| UCDP `where_prec` | ACLED `geo_precision` | Weight | Rationale |
|---|---|---|---|
| 1 (exact location) | 1 (exact) | 1.0 | High confidence in cell assignment |
| 2 (near location) | 1 (exact) | 0.9 | Likely correct cell |
| 3 (admin2 district) | 2 (within admin2) | 0.5 | May be in adjacent cell |
| 4 (admin1 province) | 3 (within admin1) | 0.2 | Low spatial confidence |
| 5+ (country/unknown) | -- | 0.0 | Exclude from cell-level analysis |

**Implementation**: Store both raw counts (all events) and precision-weighted counts as separate variables. Use precision-weighted counts for spatial analysis; use raw counts for national-level validation.

### 7.3 Temporal Recency Weighting

For slowly-updating datasets (World Bank, FAO), the most recent available value may be 1--2 years old. In causal models, this staleness introduces measurement error.

**Decision**: Apply a temporal decay weight when using annual data as covariates in monthly models:

```
weight = exp(-lambda * (current_year - data_year))
```

Where `lambda = 0.1` (weight drops to ~0.9 after 1 year, ~0.82 after 2 years, ~0.74 after 3 years). For structural variables that change slowly (governance, GDP per capita), this decay is mild. For volatile variables (inflation, conflict intensity), staleness is more problematic -- but these variables are not sourced from annual datasets.

### 7.4 Quality Propagation Through Causal Analysis

When computing cross-variable correlations or causal statistics:
- Report the **minimum quality score** across all input variables as the analysis quality indicator.
- If any input variable has a quality score below 2.5 for the specific cell-month, flag the result as `low_confidence`.
- In visualisations, use opacity or hatching to indicate quality: high-confidence results in full colour, low-confidence results faded.

---

## 8. Derived Variables

### 8.1 Climate-Derived (from CHIRPS)

| Variable | Formula | Description | Use |
|---|---|---|---|
| `climate_spi1_chirps` | Standardised Precipitation Index, 1-month window | Monthly rainfall anomaly relative to long-term distribution | Short-term drought detection |
| `climate_spi3_chirps` | SPI, 3-month window | Seasonal rainfall anomaly | Agricultural drought indicator |
| `climate_spi6_chirps` | SPI, 6-month window | Medium-term drought | Hydrological drought |
| `climate_spi12_chirps` | SPI, 12-month window | Long-term drought | Groundwater/reservoir drought |
| `climate_precip_anomaly_pct_chirps` | `(current - climatological_mean) / climatological_mean * 100` | Percent deviation from normal | Intuitive drought/excess measure |
| `climate_dry_months_count_chirps` | Count of months with SPI-1 < -1 in trailing 12 months | Drought persistence | Cumulative stress indicator |

**SPI computation**: Use the `climate_indices` Python package (NCAR) or `scipy.stats.gamma` for fitting the gamma distribution to the historical precipitation record (baseline: 1981--2020).

### 8.2 Vegetation-Derived (from NDVI)

| Variable | Formula | Description | Use |
|---|---|---|---|
| `env_vci_modis` | `100 * (NDVI - NDVI_min) / (NDVI_max - NDVI_min)` | Vegetation Condition Index (0--100) | Drought severity relative to historical range |
| `env_ndvi_anomaly_zscore_modis` | `(NDVI - clim_mean) / clim_std` (per month, per cell) | Z-score anomaly | Standardised vegetation stress |
| `env_ndvi_anomaly_pct_modis` | `(NDVI - clim_mean) / clim_mean * 100` | Percent anomaly | Crop condition estimate |
| `env_growing_season_onset_modis` | Threshold-based SOS detection | Month of growing season start | Phenology tracking |
| `env_growing_season_length_modis` | EOS - SOS | Growing season length in days | Crop calendar anomaly |
| `env_ndvi_integral_modis` | Area under NDVI curve during growing season | Cumulative greenness | Yield proxy |

**Baseline period**: 2001--2020 for MODIS; 2012--2022 for VIIRS.

### 8.3 Nightlight-Derived (from VIIRS)

| Variable | Formula | Description | Use |
|---|---|---|---|
| `econ_ntl_change_pct_viirs` | `(NTL_current - NTL_prev) / NTL_prev * 100` | Month-over-month change | Rapid economic shock detection |
| `econ_ntl_anomaly_zscore_viirs` | `(NTL - clim_mean) / clim_std` | Radiance anomaly | Economic deviation from normal |
| `econ_ntl_lit_area_pct_viirs` | Fraction of cell pixels with radiance > threshold | Lit area percentage | Electrification/urbanisation proxy |
| `econ_ntl_shock_flag_viirs` | Binary: 1 if NTL drops > 2 std below 12-month mean | Economic shock indicator | Conflict/disaster impact flag |

### 8.4 Conflict-Derived (from ACLED)

| Variable | Formula | Description | Use |
|---|---|---|---|
| `conflict_intensity_acled` | `fatalities / events` (cell-month) | Mean fatalities per event | Conflict severity indicator |
| `conflict_diffusion_acled` | Count of distinct events in cell + 8 neighbours | Spatial spread indicator | Conflict contagion measure |
| `conflict_trend_3m_acled` | 3-month moving average of event count | Smoothed conflict trend | Trend detection |
| `conflict_protest_ratio_acled` | `protest_events / total_events` | Protest share of all events | Unrest composition |

### 8.5 Food-Derived (from WFP)

| Variable | Formula | Description | Use |
|---|---|---|---|
| `food_alps_alert_wfp` | ALPS (Alert for Price Spikes) category | Pre-computed price anomaly indicator (normal/stress/alert/crisis) | Standardised food price alert |
| `food_price_anomaly_pct_wfp` | `(price - seasonal_mean) / seasonal_mean * 100` | Price deviation from seasonal norm | Food price spike detection |
| `food_tot_ratio_wfp` | Price of staple / price of alternative | Terms of trade between crops | Market stress indicator |
| `food_price_volatility_wfp` | Rolling 6-month standard deviation of prices | Price instability | Market uncertainty |

### 8.6 Cross-Domain Derived Variables

| Variable | Inputs | Description | Use |
|---|---|---|---|
| `cross_drought_conflict_cooccurrence` | `climate_spi3_chirps < -1` AND `conflict_events_count_acled > 0` | Co-occurrence of drought and conflict in same cell-month | Compound risk identification |
| `cross_food_conflict_lag3` | `food_price_anomaly_pct_wfp[t-3]` -> `conflict_events_count_acled[t]` | 3-month lagged correlation between food prices and conflict | Causal chain testing |
| `cross_ndvi_price_correlation` | Rolling 12-month correlation of NDVI and food prices | Vegetation-food price coupling strength | Market sensitivity to environment |
| `cross_disaster_displacement` | EM-DAT event + HDX HAPI displacement in same admin region within 3 months | Disaster-triggered displacement flag | Humanitarian response trigger |

---

## 9. Known Data Gaps

### 9.1 Geographic Gaps by Dataset

| Dataset | Well-Covered Regions | Poor Coverage | Systematic Gaps |
|---|---|---|---|
| **ACLED** | Africa (1997+), Middle East, South/Southeast Asia | Full global only from 2018 | Under-reporting in media blackout areas (e.g., North Korea, Eritrea, Xinjiang) |
| **UCDP-GED** | All regions with active conflict | Low-intensity violence below 25-death threshold | Remote/rural areas with limited media; non-state violence under-reported |
| **CHIRPS** | Tropics and subtropics (50S--50N) | No coverage above 50N or below 50S | Station density low in Central Africa, Central Asia; fewer stations in real-time |
| **WFP** | Crisis-affected countries (98 total) | No data in stable/wealthy countries | Markets in active conflict zones often cease reporting |
| **OpenAQ** | USA, Europe, China, India | Sub-Saharan Africa, Central Asia, Pacific Islands | Ground stations completely absent from many developing countries |
| **MODIS NDVI** | Global land | Persistent cloud cover (tropical wet season, monsoon) | Sensor degradation post-2020 (Terra) |
| **Nightlights** | Global (65S--75N) | Polar regions; cloud-persistent tropics | Gas flare contamination in oil-producing regions |
| **World Bank** | Well-covered for most indicators | Poverty/inequality data extremely sparse | Conflict states (Syria, Yemen, Somalia) often missing recent years |
| **EM-DAT** | Events meeting threshold (10 deaths or 100 affected) | Small-scale disasters below threshold | Systematic undercount in countries with poor reporting infrastructure |
| **USGS** | Dense networks in US, Japan, Europe | Sparse in Africa, Central Asia, deep oceans | Complete above M4.5 globally; below that, region-dependent |

### 9.2 Temporal Gaps

| Gap Type | Examples | Impact |
|---|---|---|
| **Dataset start dates** | ACLED global only from 2018; VIIRS from 2012; OpenAQ from 2015 | Long historical analyses limited to CHIRPS (1981), UCDP (1989), DMSP (1992), MODIS (2000) |
| **Conflict-induced reporting gaps** | WFP markets go silent during active fighting; ACLED coverage drops during internet shutdowns | Missing data precisely when it matters most |
| **Satellite data gaps** | VIIRS SNPP anomaly June--August 2022; persistent cloud cover in wet seasons | Monthly composites may have insufficient observations |
| **Annual data latency** | World Bank GDP available 1--2 years late; poverty data 3--5 years late | Context variables are always stale |
| **Sensor transitions** | DMSP to VIIRS (2012--2013); MODIS to VIIRS (ongoing) | Discontinuities in long time series |

### 9.3 The "Data Desert" Problem

The most analytically valuable regions for Causal Atlas -- active conflict zones, fragile states, disaster-affected areas -- are precisely where data quality is worst:

- **Conflict disrupts data collection**: Survey teams cannot operate; markets close; government statistics cease; satellite ground stations are abandoned.
- **Media blackouts reduce event data quality**: Internet shutdowns, journalist expulsion, and state censorship reduce ACLED/UCDP/GDELT coverage.
- **Infrastructure damage destroys ground stations**: Air quality monitors, weather stations, and seismographs are destroyed or unmaintained.
- **Population displacement invalidates gridded population**: WorldPop and GPW assume relatively stable populations. In conflict/disaster zones, millions may move.

**Strategies for data deserts:**

1. **Satellite-first approach**: Remote sensing (CHIRPS, NDVI, nightlights) works everywhere regardless of ground conditions. Prioritise satellite-derived indicators in data-sparse regions.
2. **Proxy indicators**: Use nightlights as GDP proxy where economic data is missing; use NDVI as food production proxy where FAO data is unavailable; use GDELT media volume as a signal even when ground-verified event data is missing.
3. **Acknowledge uncertainty**: In visualisations and statistical outputs, explicitly display data completeness. A cell with data from 10 sources has higher confidence than one with data from 2 sources.
4. **Nowcasting/imputation**: The HungerMapLIVE approach uses ML models trained on areas with good data to "nowcast" conditions in data-sparse areas. Causal Atlas can adopt a similar approach, with transparent uncertainty bounds.
5. **Never fabricate data**: Missing is better than wrong. Use NULL/NaN for missing values, not imputed values presented as real. Imputed values should always carry an `imputed` flag.

### 9.4 Systematic Biases to Document

| Bias | Source | Direction | Mitigation |
|---|---|---|---|
| Media reporting bias | ACLED, UCDP, GDELT | Under-reporting in media-dark areas; over-reporting in media-dense areas | Cross-validate with satellite indicators; weight by source density |
| Urban monitoring bias | OpenAQ, WFP | Cities over-represented; rural areas under-represented | Supplement with satellite-derived gridded products |
| Wealth bias | World Bank, OpenAQ | Rich countries have better data | Use satellite proxies for developing countries |
| Western source bias | GDELT | English-language and Western media over-represented | Use GDELT translingual data; weight by source diversity |
| Threshold bias | UCDP (25 deaths), EM-DAT (10 deaths / 100 affected) | Low-level events excluded | Complement with ACLED (no threshold) and micro-level data |
| Sensor saturation | DMSP nightlights (DN 0--63) | Bright urban cores cannot be distinguished | Use VIIRS calibrated radiance post-2012 |

---

## 10. Data Update Pipeline Design

### 10.1 Update Frequency Tiers

```
┌──────────────────────────────────────────────────────────────┐
│                    UPDATE FREQUENCY TIERS                      │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  REAL-TIME (minutes to hours)                                  │
│  ├── GDELT events       (every 15 min)                         │
│  ├── USGS earthquakes   (every minute)                         │
│  └── OpenAQ measurements (hourly)                              │
│                                                                │
│  NEAR-REAL-TIME (days)                                         │
│  ├── ACLED events       (weekly, Fridays)                      │
│  ├── CHIRPS preliminary  (2-day lag)                           │
│  └── HDX HAPI           (varies, days to weeks)                │
│                                                                │
│  MONTHLY                                                       │
│  ├── CHIRPS final        (~3-week lag)                         │
│  ├── MODIS NDVI monthly  (MOD13A3, ~1 month lag)               │
│  ├── VIIRS nightlights   (EOG monthly, ~2 month lag)           │
│  ├── WFP food prices     (monthly release)                     │
│  ├── UCDP candidates     (~1 month lag)                        │
│  └── IPC classifications (~quarterly)                          │
│                                                                │
│  ANNUAL                                                        │
│  ├── World Bank WDI      (quarterly updates, 1-2yr latency)    │
│  ├── World Bank WGI      (annual release)                      │
│  ├── FAO FAOSTAT         (continuous, 1-2yr latency)           │
│  ├── UCDP GED (final)    (annual release, ~6-12 month lag)     │
│  ├── EM-DAT updates      (continuous version releases)         │
│  ├── WorldPop            (annual gridded estimates)             │
│  ├── V-Dem               (annual release)                      │
│  ├── FSI                 (annual release)                      │
│  └── PRIO-GRID releases  (irregular)                           │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### 10.2 The Preliminary-to-Final Data Lifecycle

Several sources publish preliminary data that is later revised to final:

```
Time ──────────────────────────────────────────────────►

Month M ends
  │
  ├── +2 days:   CHIRPS preliminary available
  ├── +1 week:   ACLED weekly release covers most of month M
  ├── +2 weeks:  ACLED second release; month M considered "near-complete"
  ├── +3 weeks:  CHIRPS final replaces preliminary
  ├── +1 month:  UCDP candidate events for month M
  ├── +1 month:  MODIS NDVI monthly composite available
  ├── +2 months: VIIRS nightlight monthly composite available
  ├── +6-12 mo:  UCDP GED annual release incorporates verified M events
  ├── +12-24 mo: World Bank WDI updated with national statistics for year Y
  │
  └── Data for month M is "stable" after ~12 months
```

**Implementation**: Every cell-month record carries a `data_version` timestamp indicating when it was last updated. A `data_status` enum (`preliminary`, `near_final`, `final`) indicates maturity. The ingestion pipeline:

1. Creates new records when preliminary data arrives
2. Updates records as better data becomes available
3. Logs all changes in an audit trail (append-only changelog)
4. Maintains the current "best available" view as the default query target

### 10.3 Ingestion Pipeline Architecture

```
                         ┌──────────────────┐
                         │   Source APIs     │
                         │   & Downloads     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │     Source Adapters          │
                    │  (one per data source)       │
                    │  - Fetch/download            │
                    │  - Parse native format       │
                    │  - Validate schema           │
                    │  - Apply source-specific QA  │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Spatial Harmonisation      │
                    │  - Point → grid cell         │
                    │  - Raster → grid cell         │
                    │  - Admin → grid cell          │
                    │  - Assign pgid                │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Temporal Harmonisation     │
                    │  - Aggregate to month        │
                    │  - Handle multi-day events   │
                    │  - Apply naming convention   │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Derived Variable Engine    │
                    │  - SPI, VCI, anomalies       │
                    │  - NTL change indicators     │
                    │  - Cross-domain flags         │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Unified Store              │
                    │  (DuckDB / Parquet)          │
                    │  - Cell-month rows           │
                    │  - Versioned with changelog  │
                    │  - Quality metadata          │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Analysis & Visualisation   │
                    │  - Causal inference engine   │
                    │  - Kepler.gl map interface   │
                    │  - Claude API interpretation │
                    └──────────────────────────────┘
```

### 10.4 How Similar Projects Handle This

#### VIEWS (Uppsala/PRIO)

VIEWS ingests UCDP conflict data and PRIO-GRID environmental/socioeconomic variables into a unified database. Sub-national data is aggregated to PRIO-GRID cells; country data is matched via country identifiers. All data is aggregated to monthly or annual resolution. VIEWS operates on a monthly prediction cycle, producing 3-year rolling forecasts. Their pipeline uses a `views_pipeline` GitHub repository with MLOps and QA for all models and ensembles.

**Lesson for Causal Atlas**: VIEWS validates the PRIO-GRID monthly approach and demonstrates that a well-structured pipeline can operationally produce monthly analyses from heterogeneous sources.

#### AfroGrid (Linke et al. 2022, Scientific Data)

AfroGrid integrates conflict (UCDP-GED), environmental stress (CHIRPS precipitation, MODIS NDVI), and socioeconomic features (nightlights, population) into a single 0.5-degree grid-month dataset for Africa (1989--2020). It covers 10,674 grid cells with monthly data. The dataset includes PRIO-GRID IDs, COW country codes, and centroid coordinates to enable linkage with external data.

**Lesson for Causal Atlas**: AfroGrid is proof-of-concept for exactly what we are building, but limited to Africa and to a fixed set of variables. Causal Atlas extends this to global coverage and dynamic variable expansion. We should ensure our output format is compatible with AfroGrid for researchers who want to compare.

#### HungerMapLIVE (WFP)

HungerMapLIVE integrates population density (World Bank), nightlight intensity, rainfall, vegetation index (NASA), conflict data, market prices, and macroeconomic indicators into a unified data warehouse. ML models trained on 14 years of data across 63 countries produce "nowcasts" for food security where direct survey data is unavailable. The system uses call-centre-collected survey data as ground truth for model training.

**Lesson for Causal Atlas**: The "nowcast" approach -- using ML to fill spatial and temporal gaps -- is directly applicable. HungerMapLIVE demonstrates that multi-source integration with ML gap-filling is operationally viable at global scale. However, their focus is predictive (food security nowcasting), not causal. Causal Atlas adds the causal inference layer that HungerMapLIVE lacks.

### 10.5 Storage Format and Partitioning

**Primary format**: Apache Parquet, columnar, Snappy-compressed.

**Partitioning scheme**: By year, then by region (continent or VIEWS-style regional grouping).

```
data/
├── unified/
│   ├── year=2020/
│   │   ├── region=africa.parquet
│   │   ├── region=asia.parquet
│   │   ├── region=americas.parquet
│   │   ├── region=europe.parquet
│   │   └── region=oceania.parquet
│   ├── year=2021/
│   │   └── ...
│   └── ...
├── source_raw/
│   ├── acled/
│   ├── chirps/
│   └── ...
└── derived/
    ├── spi/
    ├── vci/
    └── ...
```

**Query engine**: DuckDB for local analysis (fast, columnar, SQL, Parquet-native). For larger deployments, consider Apache Arrow / DataFusion.

**Estimated total size**: ~85 GB for all sources through Phase 5 (compressed Parquet). The global grid has ~65,000 land cells; at monthly resolution from 2000--2025, that is ~19.5M cell-month rows. With ~200 variables per row, each row is ~2 KB, yielding ~39 GB for the unified table. Source-specific raw data and derived variables add the remainder.

---

## Sources

### Web References

- [VIEWS forecasting project](https://viewsforecasting.org/) -- methodology, data setup, pipeline architecture
- [VIEWS data setup notation](https://viewsforecasting.org/wp-content/uploads/2020/09/AppendixA.pdf)
- [VIEWS pipeline GitHub](https://github.com/prio-data/views_pipeline)
- [AfroGrid: Scientific Data publication](https://www.nature.com/articles/s41597-022-01198-5) -- Linke et al. 2022, "Introducing AfroGrid, a unified framework for environmental conflict research in Africa"
- [HungerMap LIVE](https://hungermap.wfp.org/) -- WFP near-real-time food security monitoring
- [HungerMap LIVE methodology](https://innovation.wfp.org/project/hungermap-live)
- [Eck 2012, "In data we trust?"](https://journals.sagepub.com/doi/10.1177/0010836711434463) -- UCDP GED vs ACLED comparison
- [Oberg & Yilmaz 2025](https://journals.sagepub.com/doi/10.1177/20531680251362440) -- measurement issues in conflict event data
- [ACLED comparison working paper](https://acleddata.com/report/working-paper-comparing-conflict-data)
- [CHIRPS vs ERA5 evaluation over Ethiopia](https://link.springer.com/article/10.1007/s00703-024-01008-0)
- [CHIRPS vs ERA5 for West/Central Africa](https://www.sciencedirect.com/science/article/pii/S2214581823000964)
- [Li et al. 2020, harmonised nighttime lights](https://doi.org/10.1038/s41597-020-0510-y)

### Internal Cross-References

All individual dataset deep-dives are in `research/datasets/`:
- `acled.md`, `ucdp-ged.md`, `gdelt.md` -- conflict and events
- `chirps.md` -- precipitation
- `wfp-food-prices.md` -- food prices
- `ndvi-vegetation.md` -- vegetation indices
- `nightlights.md` -- nighttime lights / economic proxy
- `usgs-earthquakes.md` -- seismic events
- `openaq.md` -- air quality
- `emdat.md` -- disaster database
- `hdx-hapi.md` -- humanitarian API
- `world-bank.md` -- development indicators and governance
- `fao-data.md` -- agriculture and food production
- `disease-outbreaks.md` -- health data sources
- `prio-grid.md` -- spatial framework
- `other-sources.md` -- supplementary sources (IPC, ERA5, WorldPop, GPW, V-Dem, FSI, boundaries)

Related research documents:
- `06-data-integration.md` -- spatial/temporal alignment techniques (the "how")
- `07-similar-projects.md` -- prior art and lessons learned
- `08-architecture-notes.md` -- emerging architecture decisions
