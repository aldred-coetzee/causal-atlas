# WFP Food Price Data — Deep Dive

> **Last reviewed:** March 2025
> **Author:** Causal Atlas research phase

---

## 1. Overview

The **World Food Programme (WFP) Food Price Database** is the largest publicly available collection of sub-national food commodity prices in developing and crisis-affected countries. Maintained by the WFP's **Vulnerability Analysis and Mapping (VAM)** unit, the database records retail, wholesale, and farm-gate prices for staple food commodities (cereals, pulses, oils, sugar, tubers, meat, fish, dairy, and non-food items such as fuel) collected from individual market locations.

### Key facts

| Attribute | Value |
|---|---|
| Maintainer | WFP Vulnerability Analysis and Mapping (VAM) |
| Operational since | Early 1990s (some series back to 1992); systematic global coverage from ~2003 |
| Countries | **98** (as of 2025) |
| Markets monitored | **~3,000** (up from ~1,500 in earlier years) |
| Records | Over **1 million** price observations |
| Primary temporal resolution | Monthly (daily/weekly preserved where collected) |
| Primary access points | WFP DataBridges API, HDX (Humanitarian Data Exchange), HDX HAPI, VAM DataViz portal |
| Licence | CC BY 4.0 IGO (Intergovernmental Organisations) |

WFP is the world's largest humanitarian agency fighting hunger, and its price monitoring underpins operational decisions about cash-based transfers, food procurement, early warning, and response planning. The data is a cornerstone of the global food security early-warning architecture alongside FAO GIEWS/FPMA, FEWS NET, and IPC/CH.

### Relationship to other WFP analytical products

- **ALPS (Alert for Price Spikes):** An automated anomaly-detection indicator computed from the price database (see Section 7).
- **PEWI (Price Early Warning Index):** Composite index combining ALPS signals across commodities and markets.
- **Market Monitor:** Quarterly global report summarising price trends, published by VAM.
- **HungerMapLIVE:** Near-real-time dashboard that ingests price data alongside food consumption, conflict, and weather indicators.
- **Economic Explorer:** Interactive visualisation tool on the VAM DataViz platform.

---

## 2. Coverage

### Spatial extent

The database covers **98 countries** across:

- **Sub-Saharan Africa:** Dominant coverage — nearly all countries with WFP operations. Particularly dense market networks in West Africa (Sahel), East Africa (Horn), and Great Lakes regions.
- **Middle East & North Africa:** Syria, Yemen, Iraq, Libya, Lebanon, Palestine, etc.
- **South & Southeast Asia:** Afghanistan, Pakistan, Bangladesh, Myanmar, Nepal, Cambodia, etc.
- **Latin America & Caribbean:** Haiti, Honduras, Guatemala, El Salvador, Venezuela, Colombia, etc.
- **Central Asia:** Tajikistan, Kyrgyzstan.

Coverage is concentrated in countries where WFP has operational presence. High-income OECD countries are **not** covered. The spatial unit is the **individual market** (a named trading location within an administrative subdivision), not an administrative area or grid cell.

### Temporal range

- **Earliest data:** January 1990 (limited countries — e.g., some African markets)
- **Systematic coverage:** From approximately 2003 onward for most countries
- **Ongoing:** Continuously updated; HDX datasets refreshed weekly, DataBridges API near-real-time
- **HDX time range label:** "15 January 1990 – 15 March 2026" (as seen on HDX in March 2025)

### Update frequency

| Channel | Update frequency |
|---|---|
| WFP corporate database | Continuous (as country offices submit) |
| DataBridges API | Near-real-time after ingestion |
| HDX bulk CSV | Weekly automated updates |
| HDX HAPI | Aligned with HDX updates |
| VAM Economic Explorer | Weekly |

The underlying data is **predominantly monthly** — prices are typically collected once per month per market per commodity. However, some country offices collect weekly or even daily prices, and the DataBridges API exposes daily, weekly, and monthly endpoints separately.

---

## 3. Access

There are **four** main access channels, ranging from bulk download to programmatic API access.

### 3.1 HDX Bulk Download (simplest for research)

**Global dataset (country-level CSVs):**
- URL: [https://data.humdata.org/dataset/global-wfp-food-prices](https://data.humdata.org/dataset/global-wfp-food-prices)
- Dataset ID: `31579af5-3895-4002-9ee3-c50857480785`
- Format: CSV files, one per year (1990–2026), plus supporting reference files
- Resources: ~40 files including:
  - `wfp_food_prices_global_<YEAR>.csv` — annual price files
  - `Global WFP commodities` — commodity reference table
  - `Global WFP markets` — market reference table with coordinates
  - `Global WFP currencies` — currency reference table

**Legacy single-file dataset:**
- URL: [https://data.humdata.org/dataset/wfp-food-prices](https://data.humdata.org/dataset/wfp-food-prices)
- Resource: `wfpvam_foodprices.csv` (~100+ MB single file)
- Download URL: `https://data.humdata.org/dataset/4fdcd4dc-5c2f-43af-a1e4-93c9b6539a27/resource/12d7c8e3-eff9-4db0-93b7-726825c4fe9a/download/wfpvam_foodprices.csv`

**Per-country datasets:**
- WFP also publishes individual country-level datasets on HDX (e.g., "WFP - Food Prices for Afghanistan")
- These are linked from the global dataset page
- Each has HXL (Humanitarian Exchange Language) tags for interoperability

**No authentication required** for HDX downloads.

### 3.2 WFP DataBridges API (most powerful)

The DataBridges API is WFP's official programmatic gateway to VAM data.

| Property | Value |
|---|---|
| Base URL | `https://api.wfp.org/vam-data-bridges/7.0.0` |
| Documentation portal | [https://databridges.vam.wfp.org/](https://databridges.vam.wfp.org/) |
| Authentication | OAuth 2.0 (client credentials flow) |
| Authorization URL | `https://api.wfp.org/authorize` |
| Registration | Register at [https://databridges.vam.wfp.org/](https://databridges.vam.wfp.org/) to obtain API key and secret |
| Rate limits | Not publicly documented; access scoped by application profile |

#### Market Prices Endpoints

| Endpoint | Description | Required scope |
|---|---|---|
| `GET /MarketPrices/PriceMonthly` | Monthly aggregated time series | `vamdatabridges_marketprices-pricemonthly_get` |
| `GET /MarketPrices/PriceWeekly` | Weekly aggregated time series | `vamdatabridges_marketprices-priceweekly_get` |
| `GET /MarketPrices/PriceDaily` | Daily time series | `vamdatabridges_marketprices-pricedaily_get` |
| `GET /MarketPrices/PriceRaw` | Original unprocessed prices | `vamdatabridges_marketprices-priceraw_get` |
| `GET /MarketPrices/Alps` | ALPS and PEWI indicator values | `vamdatabridges_marketprices-alps_get` |

#### Supporting Endpoints

| Endpoint | Description |
|---|---|
| `GET /Commodities/List` | Full commodity catalogue |
| `GET /Commodities/Categories/List` | Commodity category taxonomy |
| `GET /CommodityUnits/List` | Units of measure |
| `GET /CommodityUnits/Conversion/List` | Conversion factors to kg/litres |
| `GET /Markets/List` | Market list by country |
| `GET /Markets/GeoJSONList` | Geo-referenced markets (GeoJSON) |
| `GET /Markets/NearbyMarkets` | Markets within 15 km radius |

#### Common Query Parameters (price endpoints)

| Parameter | Type | Description |
|---|---|---|
| `countryCode` | string | ISO 3166-1 alpha-3 country code |
| `marketId` | integer | Specific market identifier |
| `commodityId` | integer | Specific commodity identifier |
| `priceTypeName` | string | "Retail", "Wholesale", or "Farm Gate" |
| `currencyId` | integer | Currency identifier |
| `startDate` | string (date) | Start of date range (RFC 3339) |
| `endDate` | string (date) | End of date range |
| `latestValueOnly` | boolean | Return only the most recent observation |
| `page` | integer | Page number for pagination |
| `format` | string | "json" or "csv" |

### 3.3 HDX HAPI (Humanitarian API)

HDX HAPI provides a standardised, simplified API layer over HDX datasets including WFP food prices.

| Property | Value |
|---|---|
| Base URL | `https://hapi.humdata.org` |
| Endpoint (v2) | `/api/v2/food-security-nutrition-poverty/food-prices-market-monitor` |
| OpenAPI spec | `https://hapi.humdata.org/openapi.json` |
| Docs | [https://hdx-hapi.readthedocs.io/](https://hdx-hapi.readthedocs.io/) |
| Authentication | `app_identifier` parameter: base64-encoded `"app_name:email"` |
| Rate limits | 10,000 records per request (paginate with `offset`) |
| Output formats | JSON, CSV |

#### HAPI Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `app_identifier` | string (required) | Base64 of `"app_name:email"` |
| `market_code` | string | Unique market identifier |
| `market_name` | string | Market name filter |
| `commodity_code` | string | Unique commodity identifier |
| `commodity_category` | enum | Food group (see Section 4) |
| `commodity_name` | string | Commodity name filter |
| `price_flag` | enum | "actual", "aggregate", "actual,aggregate" |
| `price_type` | enum | "Retail", "Wholesale", "Farm Gate" |
| `price_min` / `price_max` | number | Price range filter |
| `start_date` / `end_date` | string | Reference period filter |
| `has_hrp` | boolean | Filter by Humanitarian Response Plan status |
| `in_gho` | boolean | Filter by Global Humanitarian Overview inclusion |
| `output_format` | enum | "json" or "csv" |
| `limit` | integer | Max 10,000 |
| `offset` | integer | Pagination offset |

### 3.4 VAM DataViz Economic Explorer

- URL: [https://dataviz.vam.wfp.org/economic/prices](https://dataviz.vam.wfp.org/economic/prices)
- Interactive web tool for visual exploration and manual CSV export
- Supports filtering by country, market, commodity, date range
- No authentication required
- Best for ad-hoc exploration, not bulk research

---

## 4. Schema

### 4.1 HDX CSV Schema (per-country and global files)

The HDX CSV files use the following column structure (with HXL tags in row 2):

| Column name | HXL tag | Type | Description |
|---|---|---|---|
| `date` | `#date` | string (YYYY-MM-DD) | Price observation date (typically 15th of month for monthly data) |
| `admin1` | `#adm1+name` | string | First-level administrative division name |
| `admin2` | `#adm2+name` | string | Second-level administrative division name |
| `market` | `#name+market` | string | Market name |
| `latitude` | `#geo+lat` | float | Market latitude (WGS84) |
| `longitude` | `#geo+lon` | float | Market longitude (WGS84) |
| `category` | `#item+type` | string | Commodity category / food group |
| `commodity` | `#item+name` | string | Commodity name |
| `unit` | `#item+unit` | string | Unit of measure (e.g., "KG", "15 KG", "50 LB") |
| `priceflag` | `#indicator+type` | string | "actual" or "aggregate" |
| `pricetype` | `#indicator+name` | string | "Retail", "Wholesale", or "Farm Gate" |
| `currency` | `#currency` | string | ISO 4217 currency code |
| `price` | `#value` | float | Price in local currency |
| `usdprice` | `#value+usd` | float | Price converted to USD |

### 4.2 Commodity Categories

The following commodity categories (food groups) are used consistently across HDX and HAPI:

| Category | Example commodities |
|---|---|
| **cereals and tubers** | Maize, rice, wheat, sorghum, millet, cassava, potatoes |
| **pulses and nuts** | Beans, lentils, peas, groundnuts, cowpeas |
| **oil and fats** | Vegetable oil, palm oil, sunflower oil, ghee |
| **meat, fish and eggs** | Beef, goat, chicken, fish (various species), eggs |
| **milk and dairy** | Fresh milk, powdered milk, cheese |
| **vegetables and fruits** | Tomatoes, onions, bananas, oranges |
| **miscellaneous food** | Sugar, salt, tea, bread, pasta |
| **non-food** | Fuel (diesel, petrol, kerosene), charcoal, firewood, transport costs |

### 4.3 Price Types

| Price type | Description |
|---|---|
| **Retail** | Price paid by consumers at the market (most common) |
| **Wholesale** | Price at which traders buy in bulk for resale |
| **Farm Gate** | Price at which farmers sell at or near the farm |

Retail prices dominate the database. Wholesale and farm-gate prices are available for a subset of markets and commodities.

### 4.4 Price Flags

| Flag | Meaning |
|---|---|
| `actual` | Collected at monthly frequency — one observation per month |
| `aggregate` | Collected at higher frequency (daily or weekly), then aggregated to monthly via weighted mean |
| `actual,aggregate` | Mixed — some observations are direct monthly, others are aggregated |

### 4.5 Sample Record

```csv
date,admin1,admin2,market,latitude,longitude,category,commodity,unit,priceflag,pricetype,currency,price,usdprice
2024-01-15,Mogadishu,Banadir,Mogadishu/Bakaaraha,2.0469,45.3182,cereals and tubers,Sorghum,KG,actual,Retail,SOS,8500,0.51
```

### 4.6 DataBridges API Response Model

The API returns data using a `PagedCommodityPriceListDTO` (or similar DTO variant depending on the endpoint). Key response fields include:

- `CommodityID`, `CommodityName`
- `MarketID`, `MarketName`
- `CountryCode`, `CountryName`
- `CommodityUnitID`, `CommodityUnitName`
- `CurrencyID`, `CurrencyName`
- `PriceTypeID`, `PriceTypeName`
- `CommodityCategoryID`, `CommodityCategoryName`
- `Price`, `PriceDate`
- `AnalysisValueEstimatedPrice` (for ALPS endpoints)
- Pagination metadata (`TotalItems`, `Page`, `PageSize`)

The exact model schema can be inspected in the auto-generated client at [github.com/WFP-VAM/DataBridgesAPI](https://github.com/WFP-VAM/DataBridgesAPI) under `data_bridges_client/models/`.

---

## 5. Spatial Detail

### Market-level geocoding

WFP food price data is fundamentally **market-level** — each observation is tied to a named market in a named location. Markets are geocoded with latitude/longitude coordinates (WGS84 datum).

| Spatial attribute | Details |
|---|---|
| **Market coordinates** | Latitude and longitude included in both HDX CSV and API responses |
| **Coordinate precision** | Typically 4-6 decimal places; accuracy varies by country |
| **Admin hierarchy** | `admin1` (region/province), `admin2` (district/county) — text names, not standardised P-codes |
| **GeoJSON endpoint** | `GET /Markets/GeoJSONList` returns all markets as a GeoJSON feature collection |
| **Nearby markets** | `GET /Markets/NearbyMarkets` returns markets within 15 km radius of a given point |

### P-coding status

The source data from WFP is **not P-coded** (i.e., does not use the Common Operational Dataset administrative boundary codes). The HDX HAPI team has retrospectively P-coded most markets using admin1 and admin2 name matching, but some remain un-coded. HAPI responses include both `admin1_code`/`admin2_code` (P-codes where available) and `provider_admin1_name`/`provider_admin2_name` (original WFP names).

### Mapping to PRIO-GRID

WFP markets can be mapped to PRIO-GRID cells using the latitude/longitude coordinates:

1. Each market point falls within exactly one 0.5 x 0.5 degree PRIO-GRID cell
2. Multiple markets may fall within the same cell (especially in urban areas)
3. Many PRIO-GRID cells will have **no** market coverage (rural/uninhabited areas)
4. Aggregation strategy needed: average, median, or nearest-market interpolation

The Economic Explorer uses a **5 km radius** around each market's coordinates to estimate the population served, which suggests WFP considers market influence areas to be relatively local.

---

## 6. Temporal Detail

### Timestamp resolution

| Aspect | Detail |
|---|---|
| **Date format** | `YYYY-MM-DD` in CSVs; ISO 8601 in API |
| **Monthly convention** | Monthly observations are typically dated to the **15th** of the month |
| **Daily/weekly data** | Available via separate API endpoints (`PriceDaily`, `PriceWeekly`) |
| **Aggregation method** | When daily/weekly data is aggregated to monthly, a **weighted mean** is used |
| **Reporting lag** | Country offices typically submit data 2-4 weeks after collection |

### Historical depth

- Some African markets: continuous monthly series from **1992–present** (30+ years)
- Most countries: from **2003–2005** onward
- Conflict-affected countries: frequent gaps during periods of active fighting (see Section 7)

---

## 7. Quality — Known Biases, Gaps, and Limitations

### Data collection methodology

Prices are collected by WFP staff, partner organisations, and local enumerators who physically visit markets and record prices for a standardised basket of commodities using structured forms (increasingly digital — tablets and mobile phones).

**Collection process:**
1. Country VAM officers define the market basket (locally relevant staple commodities)
2. Enumerators visit selected markets (typically monthly, sometimes weekly)
3. Prices are recorded for standard units (usually per kilogram)
4. Data is entered into standardised templates and uploaded to WFP's corporate database
5. Automated quality checks flag outliers and anomalies
6. Data flows to the public database via API/HDX

### Known quality issues

| Issue | Description |
|---|---|
| **Market selection bias** | Markets are selected based on WFP operational needs, not statistical sampling. Urban and peri-urban markets, and those near WFP distribution points, are over-represented. Remote rural markets are under-covered. |
| **Temporal gaps** | Data collection stops during active conflict, insecurity, or natural disasters — precisely when prices may be most volatile and informative. |
| **Commodity inconsistency** | The specific commodities tracked vary by country, reflecting local diets. Cross-country comparisons require careful commodity matching. |
| **Unit inconsistency** | Although KG is the standard, some markets report in local units (bowls, tins, sacks). Conversion factors are available via the `CommodityUnits/Conversion/List` API endpoint but add uncertainty. |
| **Currency conversion** | USD prices use exchange rates that may not reflect black-market or parallel rates prevalent in crisis countries (e.g., Venezuela, Sudan, Myanmar). |
| **Reporting lag** | Data may be 2-6 weeks old by the time it appears in the public database. |
| **Seasonality in coverage** | Some markets are seasonal (e.g., flood-prone areas accessible only in dry season). This creates systematic seasonal gaps. |
| **Quality varies by country** | Well-resourced country offices (e.g., in the Sahel) produce very reliable, continuous series. Others have sporadic, lower-quality data. |
| **Non-standardised admin names** | Admin1/admin2 names use local spelling conventions, making joins to other datasets error-prone. |
| **No production/supply data** | Prices are observed outcomes — the database does not include trade volumes, supply quantities, or stock levels. |

### ALPS (Alert for Price Spikes) indicator

The ALPS indicator, developed in partnership with CERDI (Centre d'Etudes et de Recherches sur le Developpement International, France) since 2012, provides automated price anomaly detection:

- **Method:** Compares observed prices to a seasonal trend estimated from historical data. Conceptually similar to Bollinger Bands — a price is "abnormal" when it deviates significantly from its seasonal expected range.
- **Alert levels:**
  - **Normal:** Price within expected seasonal range
  - **Stress:** Price above expected range but within 1 standard deviation
  - **Alert:** Price exceeds 1 standard deviation above seasonal trend
  - **Crisis:** Price exceeds 2 standard deviations above seasonal trend
- **Assumption:** Abnormally rising prices typically precede price crises by several months, enabling early warning.
- **Coverage:** Applied across 1,800+ markets in 60+ countries.
- **Access:** Available via `GET /MarketPrices/Alps` API endpoint and on the Economic Explorer.

**Technical guidance:** [WFP Technical Guidance Note on ALPS (April 2014)](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)

---

## 8. Licence and Attribution

| Aspect | Detail |
|---|---|
| **Licence** | Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO) — on HDX listed as CC BY 4.0 IGO; on Kaggle mirrors as CC BY 3.0 IGO |
| **Attribution** | "Source: WFP Vulnerability Analysis and Mapping (VAM)" |
| **Commercial use** | Permitted under CC BY terms |
| **Redistribution** | Permitted with attribution |
| **API terms** | DataBridges API access is subject to WFP's API terms; data access scoped to application profile permissions |
| **Citation** | "World Food Programme, Vulnerability Analysis and Mapping (VAM). Food Prices Database. Available at: https://dataviz.vam.wfp.org/" |

---

## 9. Interoperability — Shared Identifiers with Other Datasets

### Direct connections

| Dataset | Shared identifier | Notes |
|---|---|---|
| **HDX HAPI** | P-codes (`admin1_code`, `admin2_code`) | HAPI has retrospectively P-coded most WFP markets, enabling joins to all other HAPI datasets (conflict, population, humanitarian needs) |
| **FEWS NET** | Market names, admin names | FEWS NET uses many of the same markets; names need fuzzy matching |
| **FAO GIEWS/FPMA** | Commodity names, country codes | FAO tracks similar commodities but with different market selections; useful for cross-validation |
| **ACLED** | Admin names, geocoordinates | Conflict events can be spatially joined to nearby markets using lat/lon proximity |
| **IPC/CH** | Admin1/admin2 | IPC food insecurity classifications can be linked via admin boundary codes |

### For Causal Atlas PRIO-GRID integration

To map WFP prices to PRIO-GRID cells:

1. **Spatial join:** Use market lat/lon to assign each market to a PRIO-GRID cell ID (floor of lat/lon to 0.5-degree grid)
2. **Temporal alignment:** Standardise dates to month (already the case for most data)
3. **Aggregation:** When multiple markets fall in one cell, aggregate prices (e.g., population-weighted mean)
4. **Gap filling:** Interpolate for cells without markets using nearest-market values or spatial kriging
5. **Currency standardisation:** Use the `usdprice` column for cross-country comparisons, or compute real prices deflated by a national CPI

### ISO codes

- Country codes: ISO 3166-1 alpha-3 (e.g., "SOM", "AFG", "YEM")
- Currency codes: ISO 4217 (e.g., "SOS", "AFN", "YER")
- Admin codes: OCHA P-codes where available (via HAPI)

---

## 10. Python Access — Libraries, Wrappers, and Code Examples

### 10.1 Official: DataBridges Python Client

```bash
pip install git+https://github.com/WFP-VAM/DataBridgesAPI.git
```

Requires Python 3.7+. Auto-generated via OpenAPI Generator.

```python
import os
import data_bridges_client
from data_bridges_client.rest import ApiException

# Configure OAuth 2.0
configuration = data_bridges_client.Configuration(
    host="https://api.wfp.org/vam-data-bridges/7.0.0"
)
configuration.access_token = os.environ["WFP_ACCESS_TOKEN"]

with data_bridges_client.ApiClient(configuration) as api_client:
    # List commodities
    commodities_api = data_bridges_client.CommoditiesApi(api_client)
    commodities = commodities_api.commodities_list_get()

    # Get monthly prices for Somalia
    prices_api = data_bridges_client.MarketPricesApi(api_client)
    prices = prices_api.market_prices_price_monthly_get(
        country_code="SOM",
        start_date="2023-01-01",
        end_date="2024-01-01",
        page=1,
        format="json"
    )

    # Get geo-referenced markets
    markets_api = data_bridges_client.MarketsApi(api_client)
    markets_geojson = markets_api.markets_geo_json_list_get(
        country_code="SOM"
    )
```

**GitHub:** [https://github.com/WFP-VAM/DataBridgesAPI](https://github.com/WFP-VAM/DataBridgesAPI)

### 10.2 Official: DataBridgesKnots (simplified wrapper)

```bash
pip install git+https://github.com/WFP-VAM/DataBridgesKnots.git
```

Supports Python, R (via reticulate), and Stata. Configuration via YAML file or environment variables.

```python
from data_bridges_knots import DataBridgesShapes

# Config via YAML file with KEY, SECRET, VERSION, SCOPES
client = DataBridgesShapes("data_bridges_api_config.yaml")

# Get commodity units for Tanzania
units = client.get_commodity_units_list(
    country_code="TZA",
    commodity_unit_name="Kg",
    page=1,
    format='json'
)
```

**Configuration YAML example:**
```yaml
KEY: "your-client-key"
SECRET: "your-client-secret"
VERSION: "7.0.0"
SCOPES:
  - "vamdatabridges_marketprices-pricemonthly_get"
  - "vamdatabridges_commodities-list_get"
  - "vamdatabridges_markets-list_get"
```

**GitHub:** [https://github.com/WFP-VAM/DataBridgesKnots](https://github.com/WFP-VAM/DataBridgesKnots)

### 10.3 HDX HAPI (no authentication key needed)

```python
import requests
import base64
import pandas as pd

APP_IDENTIFIER = base64.b64encode(b"causal-atlas:user@example.com").decode()
BASE_URL = "https://hapi.humdata.org/api/v2"

def get_food_prices(country_code, start_date, end_date):
    """Fetch WFP food prices via HDX HAPI."""
    all_data = []
    offset = 0
    limit = 10000

    while True:
        params = {
            "app_identifier": APP_IDENTIFIER,
            "location_code": country_code,
            "start_date": start_date,
            "end_date": end_date,
            "output_format": "json",
            "limit": limit,
            "offset": offset,
        }
        resp = requests.get(
            f"{BASE_URL}/food-security-nutrition-poverty/food-prices-market-monitor",
            params=params,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        if not data:
            break
        all_data.extend(data)
        offset += limit

    return pd.DataFrame(all_data)

# Example: Get all food prices for Yemen in 2024
df = get_food_prices("YEM", "2024-01-01", "2024-12-31")
print(df.columns.tolist())
print(df.head())
```

### 10.4 Direct HDX CSV Download with pandas

```python
import pandas as pd

# Download a single year of global data
url = "https://data.humdata.org/dataset/31579af5-3895-4002-9ee3-c50857480785/resource/{resource_id}/download/wfp_food_prices_global_2024.csv"

# Or use the legacy single-file download (large — ~100MB+)
url_legacy = "https://data.humdata.org/dataset/4fdcd4dc-5c2f-43af-a1e4-93c9b6539a27/resource/12d7c8e3-eff9-4db0-93b7-726825c4fe9a/download/wfpvam_foodprices.csv"

df = pd.read_csv(url_legacy)
# Skip HXL tag row if present (row 2 in some files)
# df = pd.read_csv(url, header=[0], skiprows=[1])

print(f"Shape: {df.shape}")
print(f"Countries: {df['admin1'].nunique()}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
```

### 10.5 HDX Scraper (for understanding the data pipeline)

The OCHA-DAP team maintains an automated scraper that pulls WFP data and publishes it to HDX:

- **GitHub:** [https://github.com/OCHA-DAP/hdx-scraper-wfp-foodprices](https://github.com/OCHA-DAP/hdx-scraper-wfp-foodprices)
- Processes ~2,000 reads from the WFP API per run
- Creates ~2 files per country (each < 2 MB) plus a consolidated ~100 MB file
- Runs on a monthly schedule

---

## 11. Relevance to Causal Atlas

### Domain coverage

WFP food price data is central to the **food security** domain and intersects directly with:

- **Conflict** (food price shocks as triggers for unrest; conflict disrupting markets and raising prices)
- **Climate** (drought/flood impacts on crop production and prices)
- **Economics** (inflation, exchange rate depreciation, trade disruptions)
- **Migration** (food insecurity as a push factor)
- **Health/nutrition** (food affordability affecting dietary diversity and malnutrition)

### Key causal chains for Causal Atlas

#### 1. Food prices <-> Conflict (bidirectional)

This is one of the most well-studied causal chains in the food security literature and is directly relevant to Causal Atlas:

- **Price -> Conflict:** A 100% increase in food prices is associated with a ~13% increase in expected conflict events in Africa ([Raleigh et al., 2015, PLOS ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC5268344/)). The effect is strongest in urban areas where people depend on food markets. In low-income countries, increases in international food prices lead to significant increases in anti-government demonstrations, riots, and civil conflict ([Arezki & Bruckner, 2011, IMF WP/11/62](https://www.imf.org/external/pubs/ft/wp/2011/wp1162.pdf)).

- **Conflict -> Price:** Conflict disrupts supply chains, destroys infrastructure, displaces farmers, and limits market access, causing prices to spike. This creates a **positive feedback loop**.

- **Regime type moderator:** Democracies are more prone to urban unrest during high food prices than autocracies ([Hendrix & Haggard, 2015](https://journals.sagepub.com/doi/abs/10.1177/0022343314561599)).

- **Temporal lag:** Conflict responses to price changes appear relatively immediate (same month), while climate effects on prices operate with a 2-4 month lag ([Raleigh et al., 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC5268344/)).

#### 2. Climate -> Food prices

- Decreased rainfall increases food prices after a **2-4 month lag**
- One standard deviation decrease in rainfall increases prices by approximately **9.1%**
- Climate effects on conflict are **mediated through food prices** rather than being direct

#### 3. Food prices -> Migration

- Sustained food price increases (beyond household coping capacity) drive displacement
- WFP data can be paired with UNHCR/IOM displacement data for lag analysis

#### 4. Food prices -> Nutrition/health outcomes

- Food price increases reduce dietary diversity, particularly affecting protein and micronutrient consumption
- Causal Atlas can correlate WFP price spikes with malnutrition survey data (e.g., DHS, SMART surveys)

### Statistical methods applicable

The food price literature uses methods directly aligned with Causal Atlas's methodology:

| Method | Application | Key references |
|---|---|---|
| **Granger causality** | Testing whether food prices Granger-cause conflict events (and vice versa) | Common in food-conflict literature; criticised for assuming linear time-lag structure |
| **Simultaneous equations** | Modelling the bidirectional food price <-> conflict relationship | Raleigh et al. (2015) |
| **ARDL (Autoregressive Distributed Lag)** | Estimating short-run and long-run effects of climate on food security via prices | Used in Somalia food security studies |
| **Time-varying Granger causality** | Allowing the causal relationship to evolve over time | Applied to climate-conflict-food nexus |
| **Panel data models** | Cross-country analysis with fixed effects for markets | Arezki & Bruckner (2011) — 120+ countries, 1970-2007 |
| **Instrumental variables** | Using global commodity prices as instruments for local price variation | Addresses endogeneity between local prices and local conflict |

### Integration approach for Causal Atlas

1. **Ingest** monthly HDX CSV data or use HAPI API for automated updates
2. **Geocode** markets to PRIO-GRID cells using lat/lon
3. **Compute** derived indicators: month-over-month % change, year-over-year % change, ALPS-like anomaly scores
4. **Align** temporally with conflict data (ACLED/UCDP), climate data (CHIRPS), and displacement data
5. **Test** lagged correlations and Granger causality at the grid-cell level
6. **Visualise** spatial patterns of price anomalies alongside conflict hotspots

---

## 12. Sources

### Primary documentation

- WFP VAM DataViz — Economic Explorer: [https://dataviz.vam.wfp.org/economic/prices](https://dataviz.vam.wfp.org/economic/prices)
- WFP Market Analysis overview: [https://www.wfp.org/market-analysis](https://www.wfp.org/market-analysis)
- DataBridges API documentation: [https://databridges.vam.wfp.org/](https://databridges.vam.wfp.org/)
- DataBridges API Python client: [https://github.com/WFP-VAM/DataBridgesAPI](https://github.com/WFP-VAM/DataBridgesAPI)
- DataBridgesKnots wrapper: [https://github.com/WFP-VAM/DataBridgesKnots](https://github.com/WFP-VAM/DataBridgesKnots)
- WFP-VAM GitHub organisation: [https://github.com/WFP-VAM](https://github.com/WFP-VAM)

### HDX datasets

- Global Food Prices (country-level CSVs): [https://data.humdata.org/dataset/global-wfp-food-prices](https://data.humdata.org/dataset/global-wfp-food-prices)
- Global Food Prices Database (legacy single file): [https://data.humdata.org/dataset/wfp-food-prices](https://data.humdata.org/dataset/wfp-food-prices)
- WFP datasets on HDX (all): [https://data.humdata.org/organization/wfp](https://data.humdata.org/organization/wfp)
- HDX scraper source code: [https://github.com/OCHA-DAP/hdx-scraper-wfp-foodprices](https://github.com/OCHA-DAP/hdx-scraper-wfp-foodprices)
- Getting up to Speed: WFP Food Data on HDX: [https://centre.humdata.org/getting-up-to-speed-wfp-food-data-on-hdx/](https://centre.humdata.org/getting-up-to-speed-wfp-food-data-on-hdx/)

### HDX HAPI

- HDX HAPI documentation: [https://hdx-hapi.readthedocs.io/](https://hdx-hapi.readthedocs.io/)
- HDX HAPI OpenAPI docs: [https://hapi.humdata.org/docs](https://hapi.humdata.org/docs)
- HDX HAPI enums: [https://hdx-hapi.readthedocs.io/en/latest/data_usage_guides/enums/](https://hdx-hapi.readthedocs.io/en/latest/data_usage_guides/enums/)

### ALPS methodology

- WFP Technical Guidance Note — ALPS (April 2014): [https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)
- ReliefWeb summary: [https://reliefweb.int/report/world/technical-guidance-note-calculation-and-use-alert-price-spikes-alps-indicator-april](https://reliefweb.int/report/world/technical-guidance-note-calculation-and-use-alert-price-spikes-alps-indicator-april)

### WFP price collection methodology

- Collecting Prices for Food Security Programming (WFP guidance): [https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp291385.pdf](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp291385.pdf)
- WFP VAM overview (Tufts/INDDEX): [https://inddex.nutrition.tufts.edu/data4diets/data-source/world-food-programme-wfp-vulnerability-analysis-and-mapping-vam](https://inddex.nutrition.tufts.edu/data4diets/data-source/world-food-programme-wfp-vulnerability-analysis-and-mapping-vam)

### Academic papers — food prices, conflict, and causality

- Raleigh, C. et al. (2015). "The devil is in the details: An investigation of the relationships between conflict, food price and climate across Africa." *PLOS ONE*. [https://pmc.ncbi.nlm.nih.gov/articles/PMC5268344/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5268344/)
- Arezki, R. & Bruckner, M. (2011). "Food Prices and Political Instability." *IMF Working Paper WP/11/62*. [https://www.imf.org/external/pubs/ft/wp/2011/wp1162.pdf](https://www.imf.org/external/pubs/ft/wp/2011/wp1162.pdf)
- Hendrix, C.S. & Haggard, S. (2015). "Global food prices, regime type, and urban unrest in the developing world." *Journal of Peace Research*. [https://journals.sagepub.com/doi/abs/10.1177/0022343314561599](https://journals.sagepub.com/doi/abs/10.1177/0022343314561599)
- Martin-Shields, C.P. & Stojetz, W. (2019). "Food security and conflict: Empirical challenges and future opportunities." *World Development*, 119, 150-164. [https://www.sciencedirect.com/science/article/abs/pii/S0305750X18302407](https://www.sciencedirect.com/science/article/abs/pii/S0305750X18302407)
- Martini, G. et al. (2023). "On the forecastability of food insecurity." *Scientific Reports*. [https://www.nature.com/articles/s41598-023-29700-y](https://www.nature.com/articles/s41598-023-29700-y)
- Baquedano, F. et al. (2024). "Improving the accuracy of food security predictions by integrating conflict data." *arXiv*. [https://arxiv.org/html/2410.22342](https://arxiv.org/html/2410.22342)
- Foini, P. et al. (2024). "Forecasting trends in food security with real time data." *Communications Earth & Environment*. [https://www.nature.com/articles/s43247-024-01698-9](https://www.nature.com/articles/s43247-024-01698-9)

### Kaggle mirrors (for exploration)

- [https://www.kaggle.com/datasets/alhamomarhotaki/global-food-prices-database-wfp](https://www.kaggle.com/datasets/alhamomarhotaki/global-food-prices-database-wfp)
- [https://www.kaggle.com/jboysen/global-food-prices](https://www.kaggle.com/jboysen/global-food-prices)

### Review of global food price databases

- [https://reliefweb.int/report/world/review-global-food-price-databases-overlaps-gaps-and-opportunities-improve](https://reliefweb.int/report/world/review-global-food-price-databases-overlaps-gaps-and-opportunities-improve)

---

## 13. DataBridges API v2 — Detailed Documentation

> **Last checked:** March 2025

### 13.1 OAuth 2.0 Authentication Flow

The DataBridges API uses the **OAuth 2.0 Client Credentials** flow. There is no user-interactive login — you authenticate your application directly.

#### Step 1: Register an Application

1. Go to <https://databridges.vam.wfp.org/>
2. Create an account and log in
3. Navigate to the application registration section
4. Register a new application, specifying the API scopes you need
5. You will receive a **Client Key** (API Key) and **Client Secret**

#### Step 2: Obtain an Access Token

```python
import requests
import base64

CLIENT_KEY = "your-client-key"
CLIENT_SECRET = "your-client-secret"

# Encode credentials
credentials = base64.b64encode(f"{CLIENT_KEY}:{CLIENT_SECRET}".encode()).decode()

# Request token
token_response = requests.post(
    "https://api.wfp.org/token",
    headers={
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    },
    data={
        "grant_type": "client_credentials",
        "scope": "vamdatabridges_marketprices-pricemonthly_get vamdatabridges_commodities-list_get vamdatabridges_markets-list_get vamdatabridges_marketprices-alps_get"
    }
)

token = token_response.json()["access_token"]
```

#### Step 3: Make Authenticated API Requests

```python
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Example: Get monthly prices for Kenya
response = requests.get(
    "https://api.wfp.org/vam-data-bridges/7.0.0/MarketPrices/PriceMonthly",
    headers=headers,
    params={
        "countryCode": "KEN",
        "startDate": "2023-01-01",
        "endDate": "2024-01-01",
        "page": 1,
        "format": "json"
    }
)

data = response.json()
```

### 13.2 Complete Endpoint Reference

#### Market Prices Endpoints

| Endpoint | Method | Description | Key scopes required |
|---|---|---|---|
| `/MarketPrices/PriceMonthly` | GET | Monthly aggregated price time series | `vamdatabridges_marketprices-pricemonthly_get` |
| `/MarketPrices/PriceWeekly` | GET | Weekly aggregated price time series | `vamdatabridges_marketprices-priceweekly_get` |
| `/MarketPrices/PriceDaily` | GET | Daily price time series | `vamdatabridges_marketprices-pricedaily_get` |
| `/MarketPrices/PriceRaw` | GET | Original unprocessed price observations | `vamdatabridges_marketprices-priceraw_get` |
| `/MarketPrices/Alps` | GET | ALPS anomaly indicator values | `vamdatabridges_marketprices-alps_get` |

#### Reference Data Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/Commodities/List` | GET | Full commodity catalogue with IDs, names, categories |
| `/Commodities/Categories/List` | GET | Commodity category taxonomy |
| `/CommodityUnits/List` | GET | Units of measure per country |
| `/CommodityUnits/Conversion/List` | GET | Conversion factors to standard units (kg/litres) |
| `/Markets/List` | GET | Market directory by country |
| `/Markets/GeoJSONList` | GET | Geo-referenced market locations (GeoJSON) |
| `/Markets/NearbyMarkets` | GET | Markets within 15 km radius of a point |

#### Additional Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/Currency/List` | GET | Available currencies and exchange rates |
| `/Currency/UsdIndirectQuotation` | GET | USD exchange rates |
| `/Rpme/XLSForms` | GET | Remote price monitoring survey forms |
| `/Surveys/List` | GET | Available surveys by country |
| `/IncubationLab/HungerSnapshots` | GET | HungerMap snapshot data |

#### Pagination

All list endpoints support pagination:
- `page` (integer): Page number (1-based)
- `pageSize` (integer): Results per page (default varies, max 1000 for most endpoints)
- Response includes `totalItems`, `page`, `pageSize` metadata

### 13.3 Rate Limits and Quotas

Rate limits are **not publicly documented** but are controlled per application profile:
- Typical rate: ~100 requests per minute (estimated from community usage)
- Data volume limits: scoped by the permissions granted during app registration
- If rate-limited, the API returns HTTP 429 with a `Retry-After` header

**Recommendation for Causal Atlas:** Use HDX bulk downloads for initial historical data loading, then use the DataBridges API for incremental monthly updates.

---

## 14. ALPS Methodology — Detailed Algorithm

> **Last checked:** March 2025

### 14.1 Mathematical Formulation

The ALPS (Alert for Price Spikes) indicator quantifies how far the current price of a commodity deviates from its expected seasonal trend. It is computed for each market-commodity pair individually.

#### Step 1: Seasonal Trend Estimation

For a time series of monthly prices {P_t}, estimate the seasonal component using a **Hodrick-Prescott (HP) filter** or polynomial trend + seasonal dummies:

```
Trend_t = HP_filter(P_t, lambda=14400)  # lambda=14400 for monthly data
```

Or equivalently, fit a model:
```
P_t = α + β·t + Σ(γ_m · D_m) + ε_t
```

Where D_m are monthly dummy variables capturing regular seasonal patterns.

#### Step 2: Compute the ALPS Score

```
ALPS_t = (P_t - Trend_t) / σ(ε)
```

Where:
- P_t is the observed price at time t
- Trend_t is the estimated seasonal trend at time t
- σ(ε) is the standard deviation of the residuals from the trend model

#### Step 3: Classify Alert Levels

| ALPS Score | Alert Level | Interpretation |
|---|---|---|
| ALPS < 0.25 | **Normal** | Price within expected seasonal range |
| 0.25 ≤ ALPS < 1.0 | **Stress** | Price above expected range but within 1σ |
| 1.0 ≤ ALPS < 2.0 | **Alert** | Price exceeds 1σ above seasonal trend |
| ALPS ≥ 2.0 | **Crisis** | Price exceeds 2σ above seasonal trend |

### 14.2 Computing ALPS Yourself

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.filters.hp_filter import hpfilter

def compute_alps(prices, lambda_hp=14400):
    """
    Compute the ALPS (Alert for Price Spikes) indicator.

    Parameters
    ----------
    prices : pd.Series
        Monthly price series with DatetimeIndex.
        Must have at least 36 months of data.
    lambda_hp : int
        HP filter smoothing parameter. 14400 for monthly data (WFP convention).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: price, trend, alps_score, alert_level
    """
    if len(prices) < 36:
        raise ValueError("ALPS requires at least 36 months of data")

    # Remove missing values for trend estimation
    prices_clean = prices.dropna()

    # Step 1: HP filter to extract trend + cycle
    cycle, trend = hpfilter(prices_clean, lamb=lambda_hp)

    # Step 2: Compute standard deviation of residuals
    sigma = cycle.std()

    # Step 3: ALPS score
    alps_score = cycle / sigma if sigma > 0 else pd.Series(0, index=cycle.index)

    # Step 4: Alert classification
    def classify_alert(score):
        if score < 0.25:
            return 'Normal'
        elif score < 1.0:
            return 'Stress'
        elif score < 2.0:
            return 'Alert'
        else:
            return 'Crisis'

    result = pd.DataFrame({
        'price': prices_clean,
        'trend': trend,
        'alps_score': alps_score,
        'alert_level': alps_score.apply(classify_alert)
    })

    return result

# Example usage
# prices = pd.Series([...], index=pd.date_range('2015-01', periods=96, freq='ME'))
# alps = compute_alps(prices)
# print(alps.tail(12))
```

### 14.3 ALPS Limitations

- Requires at least 36 months (3 years) of continuous data to estimate a meaningful seasonal trend — many conflict-affected markets have gaps that prevent ALPS computation
- The HP filter can produce boundary effects at the start and end of the series
- ALPS does not distinguish between demand-driven price increases (genuine scarcity) and supply-driven increases (market manipulation, transport disruption)
- The same ALPS score means different things for different commodities — a 2σ deviation for rice may represent a smaller absolute price change than for imported cooking oil

### 14.4 PEWI: Price Early Warning Index

The **PEWI** (Price Early Warning Index) is a composite index that aggregates ALPS signals:

- Computed at the **country level** by combining ALPS scores across all monitored markets and commodities
- Provides a single summary indicator of national food price stress
- Available via the DataBridges API and on the VAM Economic Explorer
- Useful for country-level dashboards and comparison, though it masks within-country variation

**Technical reference:** [WFP Technical Guidance Note — ALPS (April 2014)](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)

---

## 15. Market-Level Metadata

> **Last checked:** March 2025

### 15.1 Market Coverage by Region

| Region | Approximate markets | Countries | Key coverage areas |
|---|---|---|---|
| West Africa (Sahel) | ~800 | 15+ | Dense coverage; FEWS NET priority region |
| East Africa (Horn) | ~600 | 8+ | Somalia, Ethiopia, Kenya, South Sudan, Sudan |
| Great Lakes / Central Africa | ~300 | 6+ | DRC, Burundi, Rwanda |
| Southern Africa | ~200 | 8+ | Mozambique, Malawi, Madagascar, Zimbabwe |
| Middle East & North Africa | ~400 | 10+ | Yemen, Syria, Iraq, Lebanon, Palestine |
| South/Southeast Asia | ~400 | 8+ | Afghanistan, Myanmar, Bangladesh, Nepal |
| Latin America & Caribbean | ~300 | 8+ | Haiti, Honduras, Guatemala, Venezuela, Colombia |
| **Total** | **~3,000** | **98** | |

### 15.2 Market Selection Criteria

WFP distinguishes between two types of markets for monitoring:

| Market type | Selection approach | Coverage target |
|---|---|---|
| **Local markets** | Markets directly used by the population of interest (beneficiaries, vulnerable households) | 25–50% of local markets in the area |
| **Market hubs** | Markets with regional or transnational importance that set prices for surrounding areas | Include all key hub markets |

Selection criteria include:
- **Operational relevance:** Markets near WFP distribution points, transit corridors, or planned cash-transfer areas are prioritised
- **Population served:** Markets serving larger populations are preferred
- **Accessibility:** Markets that can be safely and regularly accessed by enumerators
- **Supply chain importance:** Markets that function as wholesale/aggregation points for the region
- **Cross-border relevance:** Markets near borders where trade flows affect food availability

### 15.3 Data Collection Process

1. **Country VAM officers** define the "market basket" of commodities — typically 10–20 locally relevant staple foods plus fuel
2. **Enumerators** (WFP staff, partner organisations, or contracted data collectors) physically visit each market, typically monthly
3. **Prices are recorded** for standardised units, with at least 3 price quotes per commodity per market visit to establish a representative price
4. **Digital data collection** is increasingly standard (tablets/mobile phones with ODK or similar platforms)
5. **Automated quality checks** flag outliers (>2σ from market historical median, negative values, duplicates)
6. **Data flows** to WFP corporate database → DataBridges API → HDX
7. **Typical reporting lag:** 2–4 weeks from market visit to public availability

### 15.4 Market Functionality Index (MFI)

WFP's Market Functionality Index assesses nine dimensions of market health:
1. Assortment of essential goods
2. Availability of goods
3. Price levels
4. Resilience of supply chains
5. Market competition
6. Physical infrastructure
7. Market services
8. Food quality
9. Access and protection (including safety)

The MFI is relevant because it provides context for interpreting price data — a market with low functionality may show price spikes not because of commodity scarcity but because of structural market failure.

---

## 16. Commodity Classification System

> **Last checked:** March 2025

### 16.1 WFP Standard Commodity List

WFP maintains an internal commodity taxonomy with hierarchical categories. The commodities tracked vary by country to reflect local diets, but the classification framework is standardised:

#### Category → Commodity Examples

| Category ID | Category Name | Example commodities | Typical count per country |
|---|---|---|---|
| 1 | cereals and tubers | Maize, rice (local/imported), wheat flour, sorghum, millet, cassava, potatoes, yams | 4–8 |
| 2 | pulses and nuts | Beans (red/white), lentils, cowpeas, chickpeas, groundnuts, peas | 2–4 |
| 3 | oil and fats | Vegetable oil, palm oil, sunflower oil, ghee, butter | 1–3 |
| 4 | meat, fish and eggs | Beef, goat meat, chicken, fish (dried/fresh/smoked), eggs | 2–4 |
| 5 | milk and dairy | Fresh milk, powdered milk, cheese, yoghurt | 1–2 |
| 6 | vegetables and fruits | Tomatoes, onions, bananas, oranges, cabbage | 2–4 |
| 7 | miscellaneous food | Sugar, salt, tea, bread, pasta, cooking banana | 2–3 |
| 8 | non-food | Diesel, petrol, kerosene, charcoal, firewood, transport | 1–3 |

### 16.2 Mapping to FAO Commodity Codes

There is no official one-to-one mapping between WFP commodity codes and FAO Item Codes, but the following approximate correspondences can be established:

| WFP Commodity | WFP Category | FAO Item Code | FAO Item Name | Notes |
|---|---|---|---|---|
| Maize | cereals and tubers | 56 | Maize (corn) | Direct match |
| Rice (imported) | cereals and tubers | 27 | Rice | WFP distinguishes imported/local; FAO does not |
| Wheat flour | cereals and tubers | 16 | Wheat flour | FAO code for flour specifically |
| Sorghum | cereals and tubers | 75 | Sorghum | Direct match |
| Millet | cereals and tubers | 71 | Millet | Direct match |
| Beans (dry) | pulses and nuts | 176 | Beans, dry | WFP may specify colour; FAO is generic |
| Groundnuts | pulses and nuts | 242 | Groundnuts (shelled) | Direct match |
| Vegetable oil | oil and fats | — | — | FAO has specific oils (palm 257, soybean 236); WFP often uses generic "vegetable oil" |
| Sugar | miscellaneous food | 162 | Sugar (raw centrifugal) | Approximate |
| Cassava | cereals and tubers | 125 | Cassava | May appear as fresh or flour in WFP |

**Key interoperability challenges:**
- WFP distinguishes local vs. imported varieties (especially rice); FAO does not
- WFP records retail prices per kg; FAO records producer prices per tonne
- WFP may track processed forms (flour, oil) while FAO focuses on primary commodities
- Currency and unit conversions introduce additional discrepancies

---

## 17. Real-World Data Quality Issues — Detailed Examples

> **Last checked:** March 2025

### 17.1 Currency Conversion Errors

| Issue | Example | Impact |
|---|---|---|
| **Black market exchange rates** | In Venezuela, Sudan, and Myanmar, official exchange rates diverge massively from parallel market rates. WFP USD conversions use official rates, so `usdprice` may understate the true cost to consumers by 2–10×. | USD price comparisons across countries become unreliable. Use local currency prices for within-country time series analysis. |
| **Multiple currencies** | In South Sudan, both SSP (South Sudanese Pound) and USD are used in markets. Some observations are in SSP, others in USD, creating apparent price discontinuities. | Filter by `currency` field before analysis. |
| **Exchange rate timing** | Exchange rate used for conversion may differ from the rate prevailing on the price collection date by days or weeks. | In rapidly depreciating currencies (Lebanon, Argentina), this introduces 5–15% noise. |
| **Dollarisation** | In Zimbabwe, markets transitioned from ZWL to USD and back. Currency column may not always reflect the actual transaction currency. | Cross-reference with market-specific notes. |

### 17.2 Unit Inconsistencies

| Issue | Example | Mitigation |
|---|---|---|
| Local units | "Bowl" (Nigeria), "Tin" (East Africa), "Sack" (multiple countries) — conversion factors to kg are approximations | Use the `CommodityUnits/Conversion/List` API endpoint; verify conversions with country office |
| Changing units | A market may switch from reporting per 50kg sack to per kg without annotation, causing an apparent 50× price drop | Detect using price-to-previous-month ratio checks |
| Weight vs volume | Some liquids (oil, milk) reported in litres, others in kg; density assumptions needed | Flag litres vs kg in processing pipeline |

### 17.3 Market Closures and Conflict Gaps

- **Somalia (2007–2012):** Multiple markets in south-central Somalia have complete data gaps during Al-Shabaab control periods
- **Yemen (2015–present):** Intermittent market reporting from Houthi-controlled areas; some markets disappear for months then reappear
- **Syria:** Dramatic reduction in monitored markets from ~60 pre-conflict to <30 during peak fighting; markets in opposition-held areas are systematically underrepresented
- **South Sudan:** Data collection completely ceased in some counties during the 2013–2014 and 2016–2017 fighting seasons

**Key insight for Causal Atlas:** Data gaps correlate with conflict events — precisely when price data would be most informative. This creates a **selection bias** that must be accounted for in any food-price-to-conflict causal analysis.

### 17.4 Seasonal Coverage Gaps

Some markets are physically inaccessible during certain seasons:
- Flood-prone markets in Bangladesh, South Sudan, and Mozambique are unreachable during rainy season
- Mountain markets in Afghanistan and Nepal are inaccessible during winter
- This creates **systematic seasonal gaps** that can confound seasonal adjustment

---

## 18. Seasonal Adjustment Techniques for Food Price Data

> **Last checked:** March 2025

### 18.1 Why Seasonal Adjustment Matters

Food prices exhibit strong seasonal patterns driven by agricultural cycles:
- **Lean season** (pre-harvest): prices rise as stocks diminish
- **Harvest season**: prices fall as new supply enters the market
- **Dry season**: prices for fresh vegetables and dairy may spike
- Ignoring seasonality will produce spurious "anomalies" that are actually normal seasonal variation

### 18.2 Methods Used in the Literature

| Method | Description | Suitability for WFP data |
|---|---|---|
| **Hodrick-Prescott (HP) filter** | Separates trend from cycle; used by ALPS | Good; standard in WFP/CERDI framework |
| **STL decomposition** | Seasonal-Trend decomposition using LOESS | Good; handles changing seasonal patterns |
| **X-13 ARIMA-SEATS** | US Census Bureau's standard seasonal adjustment | Overkill for most food price series; requires continuous data |
| **Month-of-year dummies** | OLS regression with 12 monthly dummy variables | Simple; works well for stable seasonal patterns |
| **Moving average ratio** | Observed / 12-month centered moving average | Robust to short gaps; easy to implement |
| **Seasonal-and-Trend decomposition (MSTL)** | Multi-seasonal STL for complex seasonal patterns | Useful if both annual and intra-annual patterns exist |

### 18.3 STL Decomposition Example

```python
import pandas as pd
from statsmodels.tsa.seasonal import STL

def seasonal_adjust_price(prices, period=12, seasonal_window=13):
    """
    Seasonally adjust a food price series using STL decomposition.

    Parameters
    ----------
    prices : pd.Series
        Monthly price time series with DatetimeIndex.
    period : int
        Seasonal period (12 for monthly data).
    seasonal_window : int
        Width of the LOESS window for seasonal extraction (must be odd, >= 7).

    Returns
    -------
    pd.DataFrame
        With columns: observed, trend, seasonal, residual, seasonally_adjusted
    """
    stl = STL(prices.dropna(), period=period, seasonal=seasonal_window, robust=True)
    result = stl.fit()

    df = pd.DataFrame({
        'observed': result.observed,
        'trend': result.trend,
        'seasonal': result.seasonal,
        'residual': result.resid,
        'seasonally_adjusted': result.observed - result.seasonal,
    })

    return df
```

---

## 19. The WFP–FEWS NET–IPC Data Ecosystem

> **Last checked:** March 2025

### 19.1 How the Three Systems Relate

The global food security early warning architecture rests on three interconnected systems:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    WFP VAM       │     │   FEWS NET       │     │     IPC/CH       │
│  (data provider) │────▶│  (analyst)       │────▶│  (classifier)    │
│                  │     │                  │     │                  │
│ • Market prices  │     │ • Scenario-based │     │ • Consensus-     │
│ • Food consump.  │     │   food security  │     │   based phase    │
│ • Remote sensing │     │   analysis       │     │   classification │
│ • HungerMapLIVE  │     │ • 3-month food   │     │ • Phases 1-5     │
│                  │     │   security       │     │   (Minimal to    │
│                  │     │   outlook        │     │   Famine)        │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  Harmonized Food Insecurity Dataset (HFID)                      │
│  Consolidates: IPC/CH phases, FEWS NET IPC-compatible phases,   │
│  WFP FCS (Food Consumption Score), WFP rCSI (Coping Strategy)   │
│  Monthly, sub-national, common admin reference system            │
└──────────────────────────────────────────────────────────────────┘
```

### 19.2 IPC Phase Classification

| Phase | Name | Description | Typical price signal |
|---|---|---|---|
| 1 | Minimal | Adequate food access | Prices within seasonal norms |
| 2 | Stressed | Marginally adequate food access | ALPS Stress or above |
| 3 | Crisis | Acute food insecurity | ALPS Alert; >25% price above seasonal |
| 4 | Emergency | Severe food gaps | ALPS Crisis; markets may be failing |
| 5 | Famine | Death, destitution, starvation | Markets non-functional or prices hyperinflationary |

### 19.3 Harmonized Food Insecurity Dataset (HFID)

A new consolidated dataset published in 2025 (Pokhariyal et al., *Scientific Data*) that combines:
- **IPC/Cadre Harmonisé phase classifications**
- **FEWS NET IPC-compatible phase estimates**
- **WFP Food Consumption Score (FCS)**
- **WFP reduced Coping Strategy Index (rCSI)**

Updated monthly with a common reference system for administrative units, this is the most comprehensive harmonised food insecurity dataset available.

**Reference:** Pokhariyal, G.P., et al. (2025). "A monthly sub-national Harmonized Food Insecurity Dataset for comprehensive analysis and predictive modeling." *Scientific Data*. <https://www.nature.com/articles/s41597-025-05034-4>

### 19.4 Relevance to Causal Atlas

For Causal Atlas, the WFP–FEWS NET–IPC ecosystem means:
1. WFP food prices are **input data** that drive food security classifications
2. IPC phases are the **outcome variable** for food security prediction models
3. The HFID provides a standardised outcome variable for training prediction models
4. Combining WFP prices with CHIRPS rainfall and ACLED conflict data replicates (and could improve upon) the manual analytical process that FEWS NET analysts perform

---

## 20. Food Price Data in Academic Early Warning Models

> **Last checked:** March 2025

### 20.1 Key Machine Learning Studies Using Food Price Data

| Study | Method | Food price role | Accuracy | Lead time |
|---|---|---|---|---|
| Busker et al. (2024), *Earth's Future* | XGBoost | Food prices as one of 56 input features | IPC phase prediction accuracy varies by region | Up to 12 months |
| Foini et al. (2024), *Comms. Earth & Environment* | Reservoir Computing, ARIMA, XGBoost, LSTM, CNN | WFP FCS, rCSI, and food prices as input | 83% accuracy for food consumption forecasts | Up to 4 months |
| Martini et al. (2023), *Scientific Reports* | Various ML models | WFP HungerMap real-time data including prices | Forecastability varies by country stability | 1–3 months |
| Baquedano et al. (2024), *arXiv* | Integrated model | Conflict + price data integration | Improved accuracy over price-only models | 3–6 months |
| Lentz et al. (2019), *World Development* | Logistic regression with lagged features | Food prices as predictive features alongside conflict and climate | Improvements over baseline | 6 months |

### 20.2 Key Findings

1. **Food prices are consistently among the top predictive features** for food insecurity forecasting, typically ranking alongside conflict intensity and rainfall anomalies
2. **Food price volatility and conflict interact synergistically** — the combination is more predictive than either alone
3. **Lead time vs accuracy trade-off:** Models achieve ~83% accuracy at 1 month lead time, degrading to ~60–70% at 6 months
4. **WFP's HungerMapLIVE** data (which includes prices) has been used directly for real-time forecasting, with daily updates providing near-real-time predictive capability
5. **Spatial granularity matters:** Sub-national (admin1/admin2) price data significantly outperforms national-level data for crisis prediction

### 20.3 References

- Busker, T., et al. (2024). "Predicting Food-Security Crises in the Horn of Africa Using Machine Learning." *Earth's Future*, 12, e2023EF004211. <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023EF004211>
- Foini, P., et al. (2024). "Forecasting trends in food security with real time data." *Communications Earth & Environment*, 5, 698. <https://www.nature.com/articles/s43247-024-01698-9>
- Lentz, E.C., et al. (2019). "A data-driven approach improves food insecurity crisis prediction." *World Development*, 122, 399–409. <https://www.sciencedirect.com/science/article/abs/pii/S0305750X19301603>

---

## 21. Worked Example: East Africa Maize Prices → ALPS → PRIO-GRID

> **Last checked:** March 2025

### 21.1 End-to-End Pipeline

This example downloads all maize prices for East Africa (Kenya, Uganda, Tanzania, Ethiopia, Somalia, South Sudan), cleans the data, computes ALPS scores, and maps to PRIO-GRID cells.

```python
import pandas as pd
import numpy as np
import requests
import base64
from statsmodels.tsa.filters.hp_filter import hpfilter

# ============================================================
# Step 1: Download data from HDX
# ============================================================

# Using the legacy single-file download for simplicity
url = ("https://data.humdata.org/dataset/4fdcd4dc-5c2f-43af-a1e4-93c9b6539a27"
       "/resource/12d7c8e3-eff9-4db0-93b7-726825c4fe9a/download/wfpvam_foodprices.csv")

print("Downloading WFP food price data...")
df_all = pd.read_csv(url)

# Skip HXL tag row if present
if df_all.iloc[0].apply(lambda x: str(x).startswith('#')).any():
    df_all = pd.read_csv(url, skiprows=[1])

print(f"Total records: {len(df_all):,}")

# ============================================================
# Step 2: Filter to East Africa maize
# ============================================================

east_africa_countries = ['Kenya', 'Uganda', 'Tanzania', 'Ethiopia', 'Somalia', 'South Sudan']
# Note: admin1 contains country in some file versions; adjust field as needed

# Filter for maize commodities (various names)
maize_terms = ['maize', 'Maize', 'corn', 'Corn']
df_maize = df_all[
    df_all['commodity'].str.contains('|'.join(maize_terms), case=False, na=False)
].copy()

# Further filter by region if country column is available
# (field names may vary; adapt to your download)

print(f"Maize records: {len(df_maize):,}")

# ============================================================
# Step 3: Clean the data
# ============================================================

# Parse dates
df_maize['date'] = pd.to_datetime(df_maize['date'], errors='coerce')
df_maize = df_maize.dropna(subset=['date', 'price'])

# Remove obviously invalid prices
df_maize = df_maize[df_maize['price'] > 0]

# Remove unit inconsistencies: keep only KG
df_maize_kg = df_maize[df_maize['unit'].str.upper().str.contains('KG', na=False)].copy()

# Flag potential outliers (price > 5× market median)
market_medians = df_maize_kg.groupby(['market'])['price'].transform('median')
df_maize_kg['outlier_flag'] = df_maize_kg['price'] > 5 * market_medians
print(f"Outliers flagged: {df_maize_kg['outlier_flag'].sum()}")

# Remove outliers
df_clean = df_maize_kg[~df_maize_kg['outlier_flag']].copy()

# ============================================================
# Step 4: Compute ALPS for each market
# ============================================================

def compute_alps_for_market(market_prices, min_months=36, lambda_hp=14400):
    """Compute ALPS for a single market's monthly price series."""
    # Resample to monthly (use mean if multiple obs per month)
    monthly = market_prices.set_index('date')['price'].resample('ME').mean()

    # Need at least 36 months
    if monthly.dropna().shape[0] < min_months:
        return None

    # Interpolate short gaps (up to 3 months)
    monthly = monthly.interpolate(method='linear', limit=3)

    if monthly.dropna().shape[0] < min_months:
        return None

    try:
        cycle, trend = hpfilter(monthly.dropna(), lamb=lambda_hp)
        sigma = cycle.std()

        if sigma == 0 or np.isnan(sigma):
            return None

        alps_score = cycle / sigma

        result = pd.DataFrame({
            'price': monthly,
            'trend': trend,
            'alps_score': alps_score,
        })

        result['alert_level'] = pd.cut(
            result['alps_score'],
            bins=[-np.inf, 0.25, 1.0, 2.0, np.inf],
            labels=['Normal', 'Stress', 'Alert', 'Crisis']
        )

        return result
    except Exception:
        return None

# Apply per market
alps_results = []
for market_name, group in df_clean.groupby('market'):
    alps_df = compute_alps_for_market(group)
    if alps_df is not None:
        alps_df['market'] = market_name
        # Get market coordinates (take first non-null)
        lat = group['latitude'].dropna().iloc[0] if 'latitude' in group else np.nan
        lon = group['longitude'].dropna().iloc[0] if 'longitude' in group else np.nan
        alps_df['latitude'] = lat
        alps_df['longitude'] = lon
        alps_results.append(alps_df)

df_alps = pd.concat(alps_results).reset_index()
print(f"Markets with ALPS: {df_alps['market'].nunique()}")

# ============================================================
# Step 5: Map to PRIO-GRID cells
# ============================================================

def assign_priogrid(lat, lon):
    """Assign a PRIO-GRID cell ID from lat/lon coordinates."""
    if pd.isna(lat) or pd.isna(lon):
        return np.nan

    # PRIO-GRID row and column
    row = int(np.floor((lat + 90) / 0.5))
    col = int(np.floor((lon + 180) / 0.5))

    # PRIO-GRID cell ID (simplified encoding)
    gid = row * 720 + col + 1
    return gid

df_alps['prio_gid'] = df_alps.apply(
    lambda r: assign_priogrid(r['latitude'], r['longitude']), axis=1
)

# ============================================================
# Step 6: Aggregate to PRIO-GRID level
# ============================================================

# When multiple markets fall in the same cell, take the mean
priogrid_monthly = df_alps.groupby(['prio_gid', 'date']).agg({
    'price': 'mean',
    'alps_score': 'mean',
    'alert_level': lambda x: x.mode().iloc[0] if len(x) > 0 else np.nan,
    'latitude': 'first',
    'longitude': 'first',
}).reset_index()

priogrid_monthly['year'] = priogrid_monthly['date'].dt.year
priogrid_monthly['month'] = priogrid_monthly['date'].dt.month

# Save as Parquet
priogrid_monthly.to_parquet('wfp_maize_alps_priogrid_eastafrica.parquet', index=False)
print(f"PRIO-GRID cells with data: {priogrid_monthly['prio_gid'].nunique()}")
print(f"Output shape: {priogrid_monthly.shape}")
```

### 21.2 Expected Output Schema

| Column | Type | Description |
|---|---|---|
| `prio_gid` | int | PRIO-GRID cell identifier |
| `date` | datetime | Month (last day of month) |
| `price` | float | Mean maize price in local currency (per kg) |
| `alps_score` | float | ALPS anomaly score (z-score) |
| `alert_level` | string | Normal / Stress / Alert / Crisis |
| `latitude` | float | Representative latitude |
| `longitude` | float | Representative longitude |
| `year` | int | Calendar year |
| `month` | int | Calendar month |

This output can be directly joined with CHIRPS precipitation data (by `prio_gid` + `year` + `month`) for lag correlation analysis.
