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

---

## FAOSTAT API — Detailed Reference

> **Last checked:** March 2025

### Domain Codes — Complete Reference

The FAOSTAT REST API uses domain codes to specify which dataset to query. Here is the complete set organised by theme:

#### API Endpoint Pattern

```
GET https://fenixservices.fao.org/faostat/api/v1/{lang}/data/{domain_code}
```

Where `{lang}` is `en`, `es`, `fr`, `ar`, `zh`, or `ru`.

#### Metadata Discovery Endpoints

```python
import requests

# List all available datasets (domain codes)
datasets = requests.get(
    "https://fenixservices.fao.org/faostat/api/v1/en/definitions/domain"
).json()

# List all countries/areas for a domain
areas = requests.get(
    "https://fenixservices.fao.org/faostat/api/v1/en/definitions/domain/QCL/area"
).json()

# List all items (commodities) for a domain
items = requests.get(
    "https://fenixservices.fao.org/faostat/api/v1/en/definitions/domain/QCL/item"
).json()

# List all elements (measurement types) for a domain
elements = requests.get(
    "https://fenixservices.fao.org/faostat/api/v1/en/definitions/domain/QCL/element"
).json()

# List all years available for a domain
years = requests.get(
    "https://fenixservices.fao.org/faostat/api/v1/en/definitions/domain/QCL/year"
).json()
```

#### Complete API Example with All Parameters

```python
import requests
import pandas as pd
import io

def faostat_query(domain, areas, items, elements, years,
                  area_cs='FAO', item_cs='FAO', element_cs='FAO',
                  output_type='csv', show_codes=True, show_flags=True,
                  show_unit=True, null_values=False):
    """
    Full-featured FAOSTAT API query.

    Parameters
    ----------
    domain : str
        FAOSTAT domain code (e.g., 'QCL', 'FBS', 'FS', 'PP')
    areas : list
        Area codes (depends on area_cs: FAO numeric, ISO3, M49)
    items : list
        Item codes (FAO numeric or CPC)
    elements : list
        Element codes
    years : list or range
        Year values
    area_cs : str
        Area coding system: 'FAO', 'ISO3', or 'M49'
    item_cs : str
        Item coding system: 'FAO' or 'CPC'
    element_cs : str
        Element coding system: 'FAO'
    output_type : str
        'csv' or 'objects'

    Returns
    -------
    pd.DataFrame
    """
    base_url = f"https://fenixservices.fao.org/faostat/api/v1/en/data/{domain}"

    params = {
        'area': ','.join(str(a) for a in areas),
        'area_cs': area_cs,
        'item': ','.join(str(i) for i in items),
        'item_cs': item_cs,
        'element': ','.join(str(e) for e in elements),
        'element_cs': element_cs,
        'year': ','.join(str(y) for y in years),
        'show_codes': str(show_codes).lower(),
        'show_flags': str(show_flags).lower(),
        'show_unit': str(show_unit).lower(),
        'null_values': str(null_values).lower(),
        'output_type': output_type,
    }

    resp = requests.get(base_url, params=params, timeout=120)
    resp.raise_for_status()

    if output_type == 'csv':
        return pd.read_csv(io.StringIO(resp.text))
    else:
        return pd.DataFrame(resp.json()['data'])

# Example 1: Maize production for all East African countries, 2015-2023
df_maize = faostat_query(
    domain='QCL',
    areas=['KEN', 'TZA', 'UGA', 'ETH', 'RWA', 'BDI', 'SSD', 'SOM'],
    items=[56],                     # Maize
    elements=[5510, 5312, 5419],   # Production, Area harvested, Yield
    years=range(2015, 2024),
    area_cs='ISO3',
)

# Example 2: Food security indicators for the Sahel
df_fs = faostat_query(
    domain='FS',
    areas=['NER', 'MLI', 'BFA', 'TCD', 'MRT', 'SEN'],
    items=[210041],  # Prevalence of undernourishment
    elements=[6120],
    years=range(2000, 2024),
    area_cs='ISO3',
)

# Example 3: Fertiliser use (nitrogen) for sub-Saharan Africa
df_fert = faostat_query(
    domain='RFN',
    areas=[5501],  # FAO code for sub-Saharan Africa aggregate
    items=[3102],  # Nitrogen fertilisers (N total)
    elements=[5157, 5159],  # Use per area of cropland, Total
    years=range(2000, 2024),
)
```

#### API Limitations

| Limitation | Detail |
|---|---|
| **No authentication** | Public API; no keys needed |
| **Rate limits** | Not formally documented; ~100 requests/minute appears safe |
| **Max response size** | Large queries may time out (>60 seconds); split by year ranges |
| **Data latency** | 1–2 years behind current year for most domains |
| **Concurrent requests** | Be conservative (2–3 concurrent) to avoid throttling |

---

## GIEWS — Global Information and Early Warning System

> **Last checked:** March 2025

### Overview

GIEWS is FAO's operational food security monitoring system, continuously monitoring food supply, demand, and prices in all countries. It is one of the oldest food security early warning systems, established in 1975.

**URL:** <https://www.fao.org/giews/en/>

### Key Data Products

| Product | Description | URL |
|---|---|---|
| **Country Briefs** | Country-specific food security updates (irregularly updated) | <https://www.fao.org/giews/country-analysis/en/> |
| **FPMA (Food Price Monitoring & Analysis)** | Monthly domestic retail/wholesale price series for 2,900+ price series across 126 countries (since 2009) | <https://www.fao.org/giews/food-prices/en/> |
| **Country Cereal Balance Sheets (CCBS)** | Annual supply-utilisation balances for major cereals, 220+ countries, since 1980 | <https://www.fao.org/giews/data-tools/en/> |
| **Crop Calendar** | Planting and harvesting dates by crop and country | Available via GIEWS tools |
| **Agricultural Stress Index (ASI)** | Satellite-derived drought indicator for agricultural areas | Near-real-time |
| **Earth Observation data** | NDVI, rainfall anomalies, LST for crop monitoring | Via GIEWS data tools |

### FPMA Tool

The Food Price Monitoring and Analysis Tool is particularly relevant to Causal Atlas:

- **Coverage:** 2,900+ monthly domestic price series for major foods across 126 countries
- **Data since:** January 2009 (some series earlier)
- **Prices tracked:** Retail and wholesale for locally consumed staples
- **Complements WFP data:** FPMA covers some countries and markets not monitored by WFP
- **Anomaly detection:** FPMA includes automated alerts for unusual price movements

**Access:** <https://fpma.fao.org/giews/fpmat4/#/dashboard/home>

### Relevance to Causal Atlas

GIEWS provides:
1. **Country cereal balance sheets** — essential for understanding import dependency and vulnerability to global price shocks
2. **Crop calendars** — needed to define growing season windows for correlating rainfall with production
3. **Agricultural Stress Index** — an alternative/complement to SPI/SPEI for agricultural drought monitoring
4. **FPMA price data** — complements WFP price data with additional country/market coverage
5. **Country briefs** — qualitative context for interpreting quantitative signals

---

## FAO Hand-in-Hand Geospatial Platform

> **Last checked:** March 2025

### Overview

The Hand-in-Hand (HiH) Geospatial Platform is FAO's flagship open-access geospatial data platform, providing agricultural and food security data layers at multiple resolutions.

| Attribute | Detail |
|---|---|
| **URL** | <https://data.apps.fao.org/> |
| **Landing page** | <https://www.fao.org/hih-geospatial-platform/en> |
| **Data layers** | >2 million layers across 5,400+ datasets |
| **Users** | 90+ organisations worldwide |
| **Licence** | Open access |

### Key Data Layers

| Category | Examples | Resolution |
|---|---|---|
| **Crop production** | Crop suitability (GAEZ), crop area maps | Various (30m to 10km) |
| **Climate** | Rainfall, temperature, drought indices | 0.05° to 0.25° |
| **Soil** | Soil type, fertility, carbon content | 250m (SoilGrids) |
| **Water** | Irrigation areas, water stress, WaPOR ET | 100m to 5km |
| **Land cover** | ESA WorldCover, GlobeLand30 | 10m to 30m |
| **Socioeconomic** | Population density, poverty, market access | Various |
| **Food security** | IPC phases, food prices, nutrition | Admin level |

### API Architecture

The platform uses standard geospatial web service protocols:

| Protocol | Purpose | Example |
|---|---|---|
| **WMS** (Web Map Service) | Map image tiles | `GetMap` requests |
| **WMTS** (Web Map Tile Service) | Cached tile access (Google Earth Engine integration) | Tile-based access |
| **WFS** (Web Feature Service) | Vector data download | GeoJSON/shapefile |
| **WCS** (Web Coverage Service) | Raster data download | GeoTIFF extraction |
| **OGC API** | Modern REST-based geospatial access | JSON-based queries |

### Programmatic Access

```python
import requests

# Example: Query WCS for a data layer
wcs_url = "https://data.apps.fao.org/geoserver/ows"
params = {
    'service': 'WCS',
    'version': '2.0.1',
    'request': 'GetCoverage',
    'coverageId': 'layer_name',  # Specific layer identifier
    'format': 'image/geotiff',
    'subset': 'Lat(0,10)',
    'subset': 'Long(30,42)',
}

# Note: Layer identifiers must be looked up in the platform catalogue
```

**Quick-Start Guide:** <https://openknowledge.fao.org/server/api/core/bitstreams/acb53145-6aa2-4d3a-9f1b-86ab99303034/content>

---

## AQUASTAT — Water Resources Data

> **Last checked:** March 2025

### Overview

AQUASTAT is FAO's global water information system and the most cited source on global water statistics. It provides data on water resources, water use, and agricultural water management for 200+ countries.

**URL:** <https://www.fao.org/aquastat/en/>

### Key Variables Relevant to Causal Atlas

| Variable | Unit | Relevance |
|---|---|---|
| **Total renewable water resources** | km³/year | Baseline water availability per country |
| **Total water withdrawal** | km³/year | Water stress indicator |
| **Agricultural water withdrawal** | km³/year | Irrigation dependency |
| **Water stress (SDG 6.4.2)** | % | Water scarcity indicator for drought-agriculture chains |
| **Irrigated cropland area** | 1000 ha | Which areas buffer against rainfall variability |
| **Irrigation water use efficiency** | — | Agricultural water productivity |
| **Dam capacity** | km³ | Water storage and flood management capacity |
| **Flood occurrence** | events/year | Hydrological hazard data |

### Database Structure

| Database | Content | Coverage |
|---|---|---|
| **Core database** | 180+ variables on water resources and use | 200+ countries, 1960–2017 |
| **Irrigated crop calendars** | Planting/harvesting dates for irrigated crops | Country-specific |
| **Sub-national irrigation** | Irrigation area at sub-national level | Select countries |
| **Dams and reservoirs** | Location, capacity, year built for major dams | Global |

### Access

- **Interactive database:** <https://www.fao.org/aquastat/en/databases/maindatabase/>
- **Bulk download:** CSV exports from the interactive interface
- **No formal API** — data must be queried through the web interface or downloaded in bulk
- **World Bank Data360 mirror:** <https://data360.worldbank.org/en/dataset/FAO_AS>

### Relevance to Drought-Agriculture Causal Chains

AQUASTAT is critical for understanding the **mediating role of irrigation** in climate-food security pathways:

```
Rainfall deficit (CHIRPS) → Water stress (AQUASTAT) → Crop production loss (FAOSTAT)
                                    ↓
                          Irrigated areas (AQUASTAT) → Buffer against drought
```

Countries with high irrigation coverage (Egypt, Pakistan) may show weak rainfall-production correlations because irrigation decouples crops from direct rainfall dependency. AQUASTAT data enables Causal Atlas to identify and control for this mediating factor.

---

## FAO-GAEZ — Global Agro-Ecological Zones

> **Last checked:** March 2025

### Overview

GAEZ (Global Agro-Ecological Zones) is a collaborative model between FAO and IIASA that assesses agricultural production potential and crop suitability worldwide, considering climate, soil, terrain, and management conditions.

| Attribute | Detail |
|---|---|
| **Current version** | GAEZ v4 (2021); GAEZ v5 (2025) |
| **Portal (v4)** | <https://gaez.fao.org/> |
| **Portal (v5)** | <https://www.fao.org/gaez/en> |
| **Resolution** | 30 arc-seconds (~1 km) to 5 arc-minutes (~10 km) |
| **Data layers** | 226,225 layers (v4), several terabytes |
| **Climate scenarios** | Historical + CMIP5/CMIP6 future projections |
| **Crops modeled** | 49+ major and minor crops |

### Six Major Themes (GAEZ v4)

| Theme | Content | Key variables |
|---|---|---|
| **1. Land and Water Resources** | Soil, terrain, land cover | Soil suitability classes, terrain slope, land use |
| **2. Agro-climatic Resources** | Climate characterisation | Growing period, temperature regime, moisture regime |
| **3. Agro-climatic Potential Yield** | Maximum attainable yield under climate constraints | Potential yield for 49 crops under rain-fed and irrigated conditions |
| **4. Suitability and Attainable Yield** | Yield accounting for soil and terrain limitations | Crop suitability index (0–100), attainable yield (kg/ha) |
| **5. Actual Yields and Production** | Current production levels | Estimated current yield vs potential |
| **6. Yield and Production Gaps** | Gap between actual and potential | Exploitable yield gap (kg/ha) |

### Relevance to Causal Atlas

GAEZ provides essential context for interpreting climate-food security relationships:

1. **Crop suitability maps** identify which areas *should* be productive given climate/soil — deviations from potential may indicate human factors (conflict, policy, investment)
2. **Yield gaps** quantify how much additional production is theoretically possible — areas with large gaps are potentially more resilient to climate shocks
3. **Climate change scenarios** project how suitability will shift — important for long-term trend analysis
4. **Growing period length** defines the temporal window for correlating rainfall with crop outcomes

### Data Access

```python
# GAEZ v4 data can be downloaded via the data viewer
# Export CSV with download URLs, then batch download:

import subprocess

# Example: download crop suitability rasters
urls = [
    "https://s3.eu-west-1.amazonaws.com/data.gaezdev.aws.fao.org/res05/CRUTS32/Hist/8110L/suHr_mze.tif",
    # ... more URLs from the data viewer export
]

for url in urls:
    subprocess.run(['curl', '-O', url])
```

**Documentation:** <https://openknowledge.fao.org/server/api/core/bitstreams/73f77f36-4976-41b9-823c-a82f1f14f87f/content>

---

## CountrySTAT — National Food and Agriculture Statistics

> **Last checked:** March 2025

### Overview

CountrySTAT is an FAO system that provides **sub-national food and agriculture statistics** — filling a critical gap in FAOSTAT, which is primarily national-level.

| Attribute | Detail |
|---|---|
| **URL** | <https://www.fao.org/in-action/countrystat/background/en/> |
| **Coverage** | 31 countries (26 in Africa) |
| **Spatial resolution** | Sub-national (uses GAUL administrative units) |
| **Standards** | FAOSTAT data standards + GAUL spatial framework |
| **Data types** | Crop production, livestock, food balance, prices — at admin-1 and admin-2 level |

### Country Coverage (as of 2025)

| Region | Countries |
|---|---|
| **West Africa** | Benin, Burkina Faso, Cabo Verde, Côte d'Ivoire, Gambia, Ghana, Guinea, Guinea-Bissau, Liberia, Mali, Mauritania, Niger, Nigeria, Senegal, Sierra Leone, Togo |
| **East Africa** | Burundi, Ethiopia, Kenya, Rwanda, Tanzania, Uganda |
| **Central Africa** | Cameroon, Congo |
| **Southern Africa** | Malawi, Mozambique |
| **Other** | Armenia, Georgia, Kyrgyzstan, Tajikistan, Turkey |

### Relevance to Causal Atlas

CountrySTAT is **extremely valuable** for Causal Atlas because it provides the sub-national agricultural production data that FAOSTAT lacks:

- **Sub-national crop production** enables correlating CHIRPS rainfall at PRIO-GRID resolution with production outcomes at the admin-1/2 level instead of national level
- **This dramatically improves causal inference** — national-level averaging masks within-country variation that drives local food security outcomes
- **However**, coverage is limited to 31 countries and data quality/completeness varies significantly by country

---

## FAOSTAT vs USDA PSD — Known Discrepancies

> **Last checked:** March 2025

### Overview

Both FAOSTAT and the USDA Production, Supply and Distribution (PSD) database are major global sources for agricultural production and trade data. They often disagree.

### Key Differences

| Aspect | FAOSTAT | USDA PSD |
|---|---|---|
| **Maintainer** | FAO (Rome) | USDA Foreign Agricultural Service (Washington) |
| **Country coverage** | 245+ countries | ~190 countries (focused on commercially important) |
| **Temporal coverage** | 1961–present | Varies; many series from 1960 |
| **Update frequency** | Annual (1–2 year lag) | Monthly updates for current crop year |
| **Primary purpose** | Statistical reference for all FAO members | US trade policy, market intelligence |
| **Methodology** | Countries self-report; FAO fills gaps with estimates | USDA attachés and analysts produce independent estimates |
| **Timeliness** | 1–2 year lag typical | **Near real-time** for current crop year |
| **Livestock** | Official country data + FAO estimates | Based on USDA FAS assessments |

### Sources of Discrepancy

| Source | Explanation | Impact |
|---|---|---|
| **Independent estimation** | USDA produces its own crop estimates using satellite imagery, ground intelligence, and economic modeling — these may differ from country self-reports used by FAOSTAT | 5–20% differences for key crops in some countries |
| **Marketing year vs calendar year** | FAOSTAT uses calendar year; USDA PSD uses marketing/crop year (varies by country and commodity) | Same production may be attributed to different years |
| **Definition differences** | "Production" may include or exclude certain categories (e.g., green maize vs grain maize) | Systematic level differences |
| **Update timing** | USDA revises estimates monthly; FAOSTAT revises annually | At any point, they may reflect different vintages of information |
| **Mirror statistics** | When a country doesn't report trade, FAOSTAT uses partner reports; USDA may use different gap-filling | Trade data can diverge substantially |

### Complementary Use

- **Use FAOSTAT** for historical analyses (longer, more consistent time series) and for countries not covered by USDA
- **Use USDA PSD** for current-year production estimates (more timely) and for major commodity-producing countries
- For livestock, some products are missing from USDA PSD; FAOSTAT can fill these gaps
- **Cross-validate:** When FAOSTAT and PSD disagree significantly for a country-year, this itself may signal data quality issues worth investigating

---

## WaPOR — Water Productivity Open Access Data

> **Last checked:** March 2025

### Overview

WaPOR (Water Productivity through Open access of Remotely sensed derived data) is FAO's portal for monitoring water productivity through remote sensing, covering **Africa and the Near East**.

| Attribute | Detail |
|---|---|
| **URL** | <https://wapor.apps.fao.org/> |
| **Coverage** | Africa and Near East (Level 1), 26 countries (Level 2), 12 pilot areas (Level 3) |
| **Temporal range** | January 2009 – near present |
| **Update frequency** | Near real-time |
| **Licence** | Open access |

### Resolution Levels

| Level | Resolution | Coverage | Use case |
|---|---|---|---|
| **Level 1** | 250m | Continental (Africa + Near East) | Regional assessment |
| **Level 2** | 100m | 26 countries and 6 river basins | Country-level analysis |
| **Level 3** | 30m | 12 pilot irrigation schemes | Field-level water management |

### Key Variables

| Variable | Abbreviation | Temporal resolution | Description |
|---|---|---|---|
| Actual evapotranspiration & interception | **ETIa** | Annual, monthly, dekadal | Total water consumed by vegetation |
| Reference evapotranspiration | **RET** | Daily, monthly | Atmospheric evaporative demand (Penman-Monteith) |
| Precipitation | **PCP** | Annual, monthly, dekadal | From CHIRPS |
| Net primary production | **NPP** | Annual, dekadal | Biomass production |
| Total biomass production | **TBP** | Annual | Total above-ground dry matter |
| Land cover classification | **LCC** | Annual | 23-class land cover |
| Phenology | **PHE** | Annual | Start/end of growing season |

### API Access

WaPOR provides REST APIs for programmatic data access:

```python
import requests

# WaPOR API base URL
WAPOR_BASE = "https://io.apps.fao.org/gismgr/api/v1"

# List available datasets
response = requests.get(f"{WAPOR_BASE}/catalog/workspaces/WAPOR_2/mapsets")
datasets = response.json()

# Get raster data for a specific area
# (specific endpoints depend on the layer)

# For Python users, the pywapor package provides higher-level access:
# pip install pywapor
```

### `pywapor` Python Package

```bash
pip install pywapor
```

```python
# pywapor provides tools for:
# - Downloading WaPOR data
# - Computing water productivity indicators
# - Gap-filling and quality assessment
# Documentation: https://github.com/FAO-SID/pywapor
```

### Relevance to Causal Atlas

WaPOR is critical for the **rainfall → evapotranspiration → crop water stress → production** causal chain:

1. **ETIa (actual evapotranspiration)** is a direct measure of crop water use — more informative than rainfall alone because it accounts for soil moisture, vegetation type, and atmospheric demand
2. **RET (reference ET)** combined with CHIRPS precipitation enables computation of **water balance** and **SPEI** at high resolution across Africa
3. **NPP/TBP (biomass production)** provides a remote-sensing proxy for crop production that is more timely than FAO production statistics
4. **Dekadal resolution** enables sub-monthly monitoring of water stress — useful for early warning
5. **Africa and Near East focus** aligns well with Causal Atlas's primary study regions

### Integration with Other Datasets

```
CHIRPS precipitation → WaPOR precipitation (same source)
                    ↕
WaPOR ETIa ←→ CHIRTS temperature (for PET computation)
    ↓
WaPOR NPP/TBP ←→ MODIS NDVI (complementary vegetation indices)
    ↓
FAOSTAT crop production (annual calibration/validation)
    ↓
WFP food prices (outcome variable)
```

WaPOR bridges the gap between climate inputs (CHIRPS, CHIRTS) and agricultural outcomes (FAOSTAT) by providing **real-time, spatially explicit measures of crop water use and biomass production**.
