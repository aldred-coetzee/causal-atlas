# FAO Data: FAOSTAT and FAO Data Services

*Last updated: March 2025*

## Overview

The Food and Agriculture Organization of the United Nations (FAO) maintains **FAOSTAT**, the world's most comprehensive statistical database on food, agriculture, fisheries, forestry, and natural resources. FAOSTAT provides free access to data for **over 245 countries and territories**, with many series extending back to **1961**.

FAOSTAT is the primary global source for:
- Crop and livestock production quantities, areas, and yields
- Food balance sheets (supply and utilisation accounts)
- Agricultural trade flows (bilateral and aggregate)
- Producer and consumer prices
- Fertiliser and pesticide use
- Land use and land cover
- Greenhouse gas emissions from agriculture
- Food security indicators

For the Causal Atlas project, FAOSTAT provides the **agricultural production backbone** needed to connect environmental variables (rainfall, NDVI) to food security outcomes (production shortfalls, price spikes, food insecurity). It is the authoritative source for country-level crop production, which can be cross-referenced with satellite-derived vegetation indices and climate data.

---

## Data Domains and Dataset Codes

FAOSTAT is organised into thematic domains, each with a unique dataset code used in API and bulk download access.

### Production

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `QCL` | Crops and livestock products | Production quantity, area harvested, yield for all crops and livestock products | 1961--present |
| `QI` | Production Indices | Gross and net production index numbers (base 2014-2016=100) | 1961--present |
| `QV` | Value of Agricultural Production | Gross production value in constant and current US$ and local currency | 1961--present |

### Trade

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `TCL` | Crops and livestock products (trade) | Import/export quantities and values for crops and livestock products | 1961--present |
| `TM` | Bilateral trade (detailed) | Bilateral trade flows by partner country | 1986--present |
| `TI` | Trade Indices | Import/export value and volume indices | 1961--present |

### Food Balance

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `FBS` | Food Balances (2010--) | Supply utilisation accounts: production, imports, exports, feed, food, losses, per capita supply | 2010--present |
| `FBSH` | Food Balances (--2013) | Old methodology food balance sheets | 1961--2013 |
| `SCL` | Supply Utilization Accounts | Detailed commodity-level supply and use data | 2010--present |

### Food Security

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `FS` | Suite of Food Security Indicators | Prevalence of undernourishment, food insecurity experience scale (FIES), dietary energy supply, protein supply, food affordability | 2000--present |

### Prices

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `PP` | Producer Prices | Annual producer prices for agricultural commodities (USD/tonne) | 1991--present |
| `PM` | Producer Prices (Monthly) | Monthly producer price data | Available for select countries |
| `CP` | Consumer Price Indices | Consumer price index for food | Various |
| `DP` | Deflators | GDP deflators for agricultural value calculations | Various |

### Land, Inputs, and Sustainability

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `RL` | Land Use | Agricultural land area, arable land, permanent crops, etc. | 1961--present |
| `LC` | Land Cover | FAO land cover classifications | 1992--present |
| `RFN` | Fertilizers by Nutrient | Nitrogen, phosphate, potash use (tonnes of nutrients) | 1961--present |
| `RFB` | Fertilizers by Product | Fertilizer use by specific product type | 2002--present |
| `RP` | Pesticides Use | Pesticide use by active ingredient type (tonnes) | 1990--present |
| `RT` | Pesticides Trade | Import/export of pesticides | 1961--present |
| `EF` | Fertilizers Indicators | Nutrient use per area, per output | Various |
| `EK` | Livestock Patterns | Livestock density and grazing indicators | Various |
| `EL` | Land Use Indicators | Land use intensity, change rates | Various |
| `EP` | Pesticides Indicators | Pesticide use per area | Various |
| `ESB` | Soil Nutrient Budget | Nitrogen, phosphorus, potassium budgets for cropland | 1961--2020 |
| `EMN` | Livestock Manure | Manure applied to soils, left on pasture | Various |

### Emissions

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `GT` | Emissions Totals | Total GHG emissions from agriculture, land use, forestry | 1961--present |
| `GN` | Emissions from Crops | CH4, N2O from rice, crop residues, etc. | 1961--present |
| `GR` | Emissions Intensities | Emissions per unit of production | Various |
| `EI` | Emissions Intensities | Carbon intensity indicators | Various |

### Forestry

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `FO` | Forestry Production and Trade | Roundwood, sawnwood, panels, pulp, paper production and trade | 1961--present |

### Other

| Code | Domain | Description | Temporal Coverage |
|---|---|---|---|
| `IC` | Credit to Agriculture | Government and commercial credit flows to agriculture | Various |
| `SDGB` | SDG Indicators | FAO-custodian SDG indicator data | Various |
| `FA` | Food Aid Shipments (WFP) | Discontinued; historical food aid data | Historical |

---

## Schema and Data Structure

All FAOSTAT datasets share a common **long-format** (tidy) schema:

| Column | Description | Example |
|---|---|---|
| `Area Code` | FAO numeric country code | 114 (Kenya) |
| `Area Code (M49)` | UN M49 standard code | 404 |
| `Area` | Country or territory name | Kenya |
| `Item Code` | FAO item code | 56 (Maize) |
| `Item Code (CPC)` | Central Product Classification code | 0112 |
| `Item` | Commodity name | Maize (corn) |
| `Element Code` | FAO element code | 5510 (Production) |
| `Element` | Measurement type | Production |
| `Year Code` | Year identifier | 2023 |
| `Year` | Calendar year | 2023 |
| `Unit` | Unit of measurement | tonnes |
| `Value` | Data value | 4,200,000 |
| `Flag` | Data quality/source flag | A (Official figure) |

### Data Flags

| Flag | Meaning |
|---|---|
| `A` | Official figure |
| `X` | International reliable sources |
| `E` | FAO estimate |
| `F` | FAO data based on imputation methodology |
| `I` | Country data based on imputation methodology |
| `M` | Data not available (missing) |
| `T` | Unofficial figure (trend, calculated) |
| `R` | Estimated data using trading partners database |
| `S` | Standardised data |
| `Fc` | Calculated data |
| `N` | Data not significant |

### Key Item Codes (Crops)

| Item Code | Item Name |
|---|---|
| 15 | Wheat |
| 27 | Rice |
| 56 | Maize (corn) |
| 71 | Millet |
| 75 | Sorghum |
| 79 | Barley |
| 116 | Potatoes |
| 137 | Yams |
| 156 | Sugar cane |
| 176 | Beans, dry |
| 236 | Soybeans |
| 656 | Coffee, green |
| 661 | Cocoa beans |

### Key Element Codes

| Element Code | Element Name | Unit |
|---|---|---|
| 5312 | Area harvested | ha |
| 5510 | Production | tonnes |
| 5419 | Yield | hg/ha (hectograms per hectare) |
| 5611 | Import Quantity | tonnes |
| 5911 | Export Quantity | tonnes |
| 5622 | Import Value | 1000 US$ |
| 5922 | Export Value | 1000 US$ |

---

## Access Methods

### FAOSTAT Website (Interactive)

- **URL**: `https://www.fao.org/faostat/`
- **Features**: Interactive data explorer with filtering by domain, country, item, element, year
- **Download**: CSV, Excel, or API query from any data selection
- **Bulk download links**: Available on the right side menu of each domain page

### REST API

The FAOSTAT REST API allows programmatic data retrieval:

**Base URL**:
```
https://fenixservices.fao.org/faostat/api/v1/{language}/data/{domain_code}
```

**Query Parameters**:

| Parameter | Description | Example |
|---|---|---|
| `area` | Country codes (comma-separated) | `area=114,136` (Kenya, Uganda) |
| `area_cs` | Area coding system | `area_cs=ISO3` or `area_cs=FAO` |
| `element` | Element codes | `element=5510,5312` |
| `element_cs` | Element coding system | `element_cs=FAO` |
| `item` | Item codes | `item=56,27` (Maize, Rice) |
| `item_cs` | Item coding system | `item_cs=FAO` or `item_cs=CPC` |
| `year` | Years (comma-separated or ranges) | `year=2015,2016,2017,2018,2019,2020` |
| `show_codes` | Include code columns | `show_codes=true` |
| `show_unit` | Include unit column | `show_unit=true` |
| `show_flags` | Include quality flags | `show_flags=true` |
| `null_values` | Include null entries | `null_values=false` |
| `output_type` | Response format | `output_type=csv` |

**Example API call**:
```
https://fenixservices.fao.org/faostat/api/v1/en/data/QCL?area=114&area_cs=FAO&element=5510&item=56&year=2015,2016,2017,2018,2019,2020&show_codes=true&show_unit=true&show_flags=true&null_values=false&output_type=csv
```

This retrieves maize production for Kenya, 2015--2020.

**Metadata endpoints**:
```
https://fenixservices.fao.org/faostat/api/v1/en/definitions/types/area     # Country codes
https://fenixservices.fao.org/faostat/api/v1/en/definitions/types/item     # Item codes
https://fenixservices.fao.org/faostat/api/v1/en/definitions/types/element  # Element codes
```

### Bulk Download

Bulk download files are available as compressed CSV archives:

**Base URL**:
```
https://bulks-faostat.fao.org/production/
```

**Example**:
```
https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip
```

Each ZIP archive contains:
- Main CSV data file (normalised long format)
- Flags metadata file
- Symbols/notes file

**Dataset metadata index**:
- English: `https://bulks-faostat.fao.org/production/datasets_E.xml`
- Spanish: `https://bulks-faostat.fao.org/production/datasets_S.xml`

### Authentication

- **API**: No authentication required for the REST API
- **Bulk downloads**: No authentication required
- **Python library (v2.0+)**: Requires JWT bearer token from FAOSTAT Developer Portal or programmatic login with username/password for some functions

---

## Spatial Detail

### Primary Level: Country

FAOSTAT data is primarily at **national level**, covering:
- **245+ countries and territories** (using FAO country codes, mappable to ISO3 and M49)
- **Country groupings**: Regional aggregates (Africa, Asia, etc.), income groups, custom aggregates
- **Historical entities**: Data preserved for former countries (e.g., USSR, Yugoslavia) with appropriate flags

### Sub-national Data

Limited sub-national data is available in specific domains:
- **Sub-national crop statistics** exist for some countries through national statistical offices but are NOT systematically included in FAOSTAT
- **Land use/cover data** in FAOSTAT is country-level, but the underlying FAO datasets (e.g., Global Forest Resources Assessment) have sub-national components
- The **FAO Hand-in-Hand Geospatial Platform** (`https://data.apps.fao.org/`) provides some gridded agricultural data

### Country Code Systems

| System | Example (Kenya) | Notes |
|---|---|---|
| FAO code | 114 | FAO's own numeric system |
| M49 | 404 | UN standard |
| ISO3 | KEN | ISO 3166-1 alpha-3 |
| ISO2 | KE | ISO 3166-1 alpha-2 |

The `area_cs` parameter in the API allows querying by different coding systems.

---

## Temporal Detail

| Aspect | Detail |
|---|---|
| **Temporal resolution** | Annual (calendar year) for most domains; monthly for select price data |
| **Earliest data** | 1961 for core production and trade domains |
| **Latest data** | Typically 1-2 years behind current year (2022 or 2023 data available in 2025) |
| **Update frequency** | Varies by domain; typically 1-2 updates per year |
| **Calendar** | Calendar year (January--December); some crop data may refer to crop year |

### Latency by Domain

| Domain | Typical Latency | Notes |
|---|---|---|
| Crop production (QCL) | 1-2 years | Depends on country reporting |
| Trade (TCL) | 1-2 years | Mirror statistics used to fill gaps |
| Food Balance Sheets (FBS) | 2-3 years | Require reconciliation of multiple data sources |
| Food Security (FS) | 1 year | Some indicators updated more frequently |
| Prices (PP) | 6 months--1 year | Monthly prices have shorter lag |
| Land use (RL) | 1-2 years | |
| Emissions (GT) | 1-2 years | |

---

## Quality and Limitations

### Data Quality Framework

FAO applies the **Statistical Data and Quality Assurance Framework (SDQAF)** to guide quality assessments. Data quality flags (see Schema section above) indicate the source and reliability of each data point.

### Known Quality Issues

| Issue | Detail | Affected Domains |
|---|---|---|
| **Missing data** | Significant gaps for conflict-affected states and small island nations. Some country-years have no reports for any commodity. | All |
| **Estimation and imputation** | FAO estimates (flag `E` or `F`) fill many gaps, especially for countries that do not report. Estimation methodology varies and may introduce systematic biases. | Production, trade |
| **Inconsistencies across sources** | Known discrepancies between FAOSTAT livestock data and WOAH (World Organisation for Animal Health) data, sometimes due to differing data collection methodologies (surveys vs. administrative records). | Livestock production |
| **Yield calculation artefacts** | Yield = Production / Area Harvested. If area harvested is underreported (e.g., subsistence farming), yields may be overestimated. | QCL (yield element) |
| **Trade mirror statistics** | When a country does not report trade, FAO may use trading partner reports (mirror statistics). This can introduce inconsistencies. | TCL, TM |
| **Historical discontinuities** | Methodological changes (e.g., food balance sheet methodology changed in 2010; old FBS vs. new FBS not directly comparable) create time series breaks. | FBS, FBSH |
| **Coverage of subsistence agriculture** | Smallholder and subsistence agriculture is systematically underrepresented in many developing country statistics. | QCL |
| **Timeliness** | Data for recent years may be preliminary estimates, later revised. Always note which data version was used. | All |

### Data Quality Assessment for Key Domains

| Domain | Quality | Notes |
|---|---|---|
| Crop production (major crops) | Good for major crops in major producing countries | Wheat, rice, maize well-covered globally |
| Crop production (minor crops) | Moderate to poor | Roots, tubers, indigenous crops less well-covered |
| Livestock production | Moderate | Inconsistencies with other sources noted |
| Trade data | Good | Extensive use of mirror statistics |
| Food Balance Sheets | Good (post-2010) | New methodology is more transparent |
| Food Security Indicators | Good | Multiple indicators cross-validated |
| Pesticide use | Moderate to poor | Many countries do not report; estimates fill gaps |
| Fertiliser use | Moderate | Better coverage for N, P, K nutrients |

---

## Licence and Terms of Use

| Aspect | Detail |
|---|---|
| **Licence** | Open data; FAO Terms and Conditions apply |
| **Cost** | Free |
| **Registration** | Not required for website or API; Python library v2.0+ may require FAOSTAT account for some functions |
| **Attribution** | Required: "Source: FAO, FAOSTAT" |
| **Redistribution** | Permitted with attribution |
| **Commercial use** | Permitted under FAO terms |

### Citation

> FAO. (2025). FAOSTAT Statistical Database [Data set]. Food and Agriculture Organization of the United Nations. https://www.fao.org/faostat/

For specific domains:
> FAO. (2025). FAOSTAT Crops and Livestock Products [Data set]. Food and Agriculture Organization of the United Nations. License: CC BY-NC-SA 3.0 IGO.

---

## Interoperability with Other Causal Atlas Datasets

| Dataset | Relationship | Integration Notes |
|---|---|---|
| **NDVI (MODIS/VIIRS)** | NDVI during growing season is a leading indicator of crop production. FAO annual production data validates/calibrates NDVI-based yield models. | Country-level comparison: growing-season NDVI anomaly vs. FAO production anomaly. |
| **CHIRPS rainfall** | Rainfall drives crop production in rainfed agriculture. FAO production data provides ground truth for rainfall-yield relationships. | Country-year or admin-level join; seasonal rainfall vs. annual production. |
| **WFP food prices** | FAO provides production-side data; WFP provides market-side price data. Together they reveal the full food supply chain. | FAO production shortfall -> WFP price spike is a core causal chain. |
| **World Bank WDI** | Agriculture value added (% GDP) from WDI contextualises the economic importance of FAO crop data. GDP per capita indicates economic vulnerability to crop failures. | Country-year join via ISO3. |
| **ACLED / UCDP-GED** | Crop failure (FAO production decline) may contribute to food-related conflict. Conflict may disrupt agricultural production. Bidirectional causality. | Time-lagged analysis: production decline -> conflict onset; conflict -> production decline. |
| **EM-DAT** | Drought and flood disaster events (EM-DAT) should correlate with crop production losses (FAO). | Disaster year/country matching to production anomalies. |
| **PRIO-GRID** | FAO country-level data broadcast to grid cells within countries, or used as country-level context. | Country-to-grid mapping via ISO3. |
| **Nighttime lights** | Agricultural GDP (from FAO + WDI) is the component of GDP least captured by nighttime lights. Important for understanding NTL limitations. | Country-level: agricultural vs. non-agricultural GDP contribution to NTL. |

---

## Python Access

### faostat Library (Official Python Package)

```bash
pip install faostat
```

**Version**: 2.0.1 (as of March 2025)

#### List Available Datasets

```python
import faostat

# List all available datasets
datasets = faostat.list_datasets_df()
print(datasets.head(20))
# Returns DataFrame with dataset codes and names
```

#### Explore Dataset Parameters

```python
# List available parameters for crop production
pars = faostat.list_pars_df('QCL')
print(pars)

# Get available areas (countries)
areas = faostat.get_par_df('QCL', 'area')
print(areas.head())

# Get available items (crops)
items = faostat.get_par_df('QCL', 'item')
print(items.head())

# Get available elements (production, area, yield)
elements = faostat.get_par_df('QCL', 'element')
print(elements)
```

#### Fetch Data

```python
import faostat

# Maize production for Kenya and Tanzania, 2015-2023
data = faostat.get_data_df(
    'QCL',
    pars={
        'area': [114, 215],      # Kenya=114, Tanzania=215
        'item': [56],             # Maize=56
        'element': [5510, 5312],  # Production, Area harvested
    }
)
print(data.head())

# Using ISO3 coding
data = faostat.get_data_df(
    'QCL',
    pars={
        'area': ['KEN', 'TZA'],
        'item': [56],
        'element': [5510],
    },
    coding={'area': 'ISO3'}
)
```

#### Food Security Indicators

```python
# Prevalence of undernourishment
fs_data = faostat.get_data_df(
    'FS',
    pars={
        'area': ['KEN', 'ETH', 'SOM', 'SDN', 'SSD'],
    },
    coding={'area': 'ISO3'}
)

# Filter to specific indicators
undernourishment = fs_data[fs_data['Item'].str.contains('undernourishment', case=False)]
```

### Direct API Access with requests

```python
import requests
import pandas as pd
import io

def fetch_faostat(domain, areas, items, elements, years, area_cs='FAO'):
    """Fetch FAOSTAT data via REST API."""
    base_url = f"https://fenixservices.fao.org/faostat/api/v1/en/data/{domain}"

    params = {
        'area': ','.join(str(a) for a in areas),
        'area_cs': area_cs,
        'item': ','.join(str(i) for i in items),
        'item_cs': 'FAO',
        'element': ','.join(str(e) for e in elements),
        'element_cs': 'FAO',
        'year': ','.join(str(y) for y in years),
        'show_codes': 'true',
        'show_unit': 'true',
        'show_flags': 'true',
        'null_values': 'false',
        'output_type': 'csv',
    }

    resp = requests.get(base_url, params=params)
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text))
    return df

# Maize production for East African countries, 2015-2023
df = fetch_faostat(
    domain='QCL',
    areas=[114, 215, 226, 238],  # Kenya, Tanzania, Uganda, Ethiopia
    items=[56],                    # Maize
    elements=[5510, 5312, 5419],  # Production, Area, Yield
    years=range(2015, 2024)
)
print(df.head())
```

### Bulk Download

```python
import requests
import zipfile
import io
import pandas as pd

def download_faostat_bulk(domain_code):
    """Download and extract bulk FAOSTAT data for a domain."""
    # Bulk download URL pattern
    url = f"https://bulks-faostat.fao.org/production/{domain_code}_E_All_Data_(Normalized).zip"

    resp = requests.get(url)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        # Find the main data CSV
        csv_files = [f for f in z.namelist() if f.endswith('.csv') and 'Flag' not in f]
        if csv_files:
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f, encoding='latin-1')
                return df

    return None

# Download all crop production data
crops = download_faostat_bulk('Production_Crops_Livestock')
print(f"Shape: {crops.shape}")
print(crops.head())
```

### Our World in Data ETL (Alternative)

Our World in Data maintains a well-documented ETL pipeline for FAOSTAT data with cleaning, harmonisation, and country name standardisation:

- **Documentation**: `https://docs.owid.io/projects/etl/data/faostat/`
- **GitHub**: `https://github.com/owid/etl`

This can serve as a reference implementation for our own ingestion pipeline.

---

## Relevance to Causal Atlas

### Primary Use Cases

1. **Agricultural production as outcome variable**: Crop production quantity and area harvested are the key outcome variables for testing whether rainfall anomalies, NDVI declines, or conflict events cause agricultural losses.

2. **Food balance and supply chains**: Food balance sheets reveal how countries depend on imports vs. domestic production. Countries heavily dependent on imports may be more vulnerable to global food price shocks; countries dependent on domestic production may be more vulnerable to local climate events.

3. **Food security indicators**: The FAO Suite of Food Security Indicators (FS domain) provides validated measures of undernourishment, dietary energy supply, and food insecurity prevalence. These are the ultimate outcome variables in many of our causal chains.

4. **Price data complementing WFP**: FAO producer prices capture the farm-gate price level, while WFP monitors retail/market prices. Together they reveal the full price transmission chain from producer to consumer.

5. **Land use and environmental inputs**: Fertiliser use, pesticide use, and land use change provide context for understanding agricultural productivity trends and environmental sustainability.

6. **Emissions from agriculture**: Agricultural GHG emissions data enables analysis of the environmental footprint of food production, linking to climate change and pollution domains.

### Core Causal Chains Using FAO Data

```
Rainfall anomaly (CHIRPS)
  -> Vegetation stress (NDVI anomaly)
    -> Crop production decline (FAO QCL)
      -> Food price spike (WFP + FAO prices)
        -> Food insecurity (FAO FS indicators)
          -> Social unrest / conflict (ACLED)
```

```
Conflict event (ACLED/UCDP)
  -> Agricultural disruption
    -> Crop production decline (FAO QCL)
      -> Food supply shortfall (FAO FBS)
        -> Food insecurity (FAO FS)
```

### Limitations for Causal Atlas

- **Country-level only**: Cannot resolve within-country variation. A drought affecting one region may not show up in national crop production figures if other regions compensate.
- **Annual resolution**: Cannot capture sub-annual dynamics. Monthly market prices (WFP), monthly NDVI, and monthly rainfall operate at much finer temporal resolution.
- **1-2 year lag**: By the time FAO data is published, the events being studied are old. Near-real-time analysis must rely on satellite proxies.
- **Estimation for many countries**: Data for conflict-affected states (precisely where Causal Atlas is most needed) is often estimated by FAO rather than reported by countries.

### Integration Strategy

1. **Ingest QCL (crop production)** for all countries and major crops, 1990--present, via bulk download.
2. **Ingest FS (food security indicators)** for all countries via API.
3. **Ingest FBS (food balance sheets)** for food import dependency analysis.
4. **Store as country-year Parquet** with FAO, M49, and ISO3 codes.
5. **Compute production anomalies** (z-scores against long-term mean) for each crop-country combination.
6. **Join to PRIO-GRID** by broadcasting country values, similar to World Bank data.
7. **Cross-validate** FAO production data with satellite-derived NDVI during growing seasons.
8. **Use as annual calibration** for higher-frequency satellite-based estimates.

---

## Sources

- FAOSTAT main portal: https://www.fao.org/faostat/
- FAO Statistics division: https://www.fao.org/statistics/en
- FAOSTAT API (GitHub): https://github.com/FAOSTAT/faostat-api
- FAOSTAT Python package: https://pypi.org/project/faostat/
- Bulk download base: https://bulks-faostat.fao.org/production/
- Dataset metadata: https://bulks-faostat.fao.org/production/datasets_E.xml
- OWID FAOSTAT documentation: https://docs.owid.io/projects/etl/data/faostat/
- FAO SDQAF: https://www.fao.org/statistics/quality-assurance/en/
- FAO Hand-in-Hand Platform: https://data.apps.fao.org/
- FAOSTAT User Guide (Spring 2025): https://opendatasets1.github.io/UMD-OpenDataset/Current%20User%20Guides/FAOSTAT_May2025.pdf
- FAOSTAT data quality analysis: https://datascience.codata.org/articles/10.5334/dsj-2024-044
- Cropland nutrient budgets (ESSD): https://essd.copernicus.org/articles/16/525/2024/
- Wikipedia FAOSTAT overview: https://en.wikipedia.org/wiki/Food_and_Agriculture_Organization_Corporate_Statistical_Database
