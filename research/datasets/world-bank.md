# World Bank Open Data / World Development Indicators

*Last updated: March 2025*

## Overview

The World Bank Open Data platform provides free and open access to global development data. The flagship database is the **World Development Indicators (WDI)**, which contains over 1,600 time series indicators for 217 economies and more than 40 country groups, with many series dating back over 50 years (from 1960).

Beyond WDI, the World Bank hosts over 45 databases accessible through a unified API, including:

- **Worldwide Governance Indicators (WGI)** -- six composite governance measures
- **International Debt Statistics (IDS)** -- external debt data
- **Doing Business** -- business regulation indicators (discontinued as of 2021)
- **Human Capital Index (HCI)** -- education and health productivity measures
- **Poverty and Inequality Platform (PIP)** -- poverty headcount ratios and inequality measures
- **Subnational Poverty** -- sub-national poverty estimates where available

For the Causal Atlas project, World Bank data provides essential **economic and governance context variables** at country level (and occasionally sub-national). While the spatial resolution (country-level) is coarser than our 0.5-degree PRIO-GRID target, these indicators are critical for understanding the socioeconomic context in which spatially-disaggregated environmental and conflict events occur.

---

## API Access: World Bank Indicators API v2

### Base URL and Structure

```
https://api.worldbank.org/v2/{endpoint}
```

**Authentication**: None required. The API is fully open with no API keys needed.

### Core Endpoints

| Endpoint Pattern | Description | Example |
|---|---|---|
| `/v2/country` | List countries with metadata | `https://api.worldbank.org/v2/country?format=json` |
| `/v2/country/{code}/indicator/{indicator}` | Data for specific country and indicator | `/v2/country/KEN/indicator/NY.GDP.MKTP.CD` |
| `/v2/country/all/indicator/{indicator}` | Data for all countries | `/v2/country/all/indicator/SP.POP.TOTL` |
| `/v2/indicator` | List all indicators | `/v2/indicator?format=json` |
| `/v2/indicator/{code}` | Indicator metadata | `/v2/indicator/NY.GDP.MKTP.CD` |
| `/v2/source` | List databases | `/v2/source?format=json` |
| `/v2/region` | Regional classifications | `/v2/region?format=json` |
| `/v2/incomelevel` | Income group classifications | `/v2/incomelevel?format=json` |
| `/v2/lendingtype` | Lending type classifications | `/v2/lendingtype?format=json` |
| `/v2/topic` | Subject area classifications | `/v2/topic?format=json` |

### Query Parameters

| Parameter | Description | Example |
|---|---|---|
| `format` | Response format: `json`, `xml`, `jsonstat` | `?format=json` |
| `date` | Year or range (colon-separated) | `?date=2010:2020` |
| `per_page` | Results per page (default 50, max 32500) | `?per_page=10000` |
| `page` | Page number | `?page=2` |
| `source` | Database ID (default: WDI=2) | `?source=3` (WGI) |
| `downloadformat` | Direct download: `csv`, `excel` | `?downloadformat=csv` |
| `language` | Response language (15+ supported) | `?language=fr` |
| `footnote` | Include footnotes: `y`/`n` | `?footnote=y` |
| `MRV` | Most Recent Values | `?MRV=5` |
| `gapfill` | Fill gaps with MRV: `y`/`n` | `?gapfill=y` |

### Date Range Formats

| Format | Example | Description |
|---|---|---|
| Single year | `?date=2020` | One year only |
| Year range | `?date=2000:2020` | Inclusive range |
| Monthly | `?date=2012M01:2012M08` | Monthly data (where available) |
| Quarterly | `?date=2013Q1:2013Q4` | Quarterly data (where available) |
| Most recent | `?MRV=5` | Last 5 available values |

### Multi-Indicator and Multi-Country Queries

Multiple indicators or countries can be requested using semicolons:

```
/v2/country/KEN;TZA;UGA/indicator/NY.GDP.MKTP.CD;SP.POP.TOTL?date=2010:2020&format=json
```

**Constraints**:
- Maximum 60 indicators per request
- Maximum 1,500 characters between forward slashes
- Maximum 4,000 characters total URL length

### JSON Response Structure

```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 11,
    "sourceid": "2",
    "lastupdated": "2024-12-19"
  },
  [
    {
      "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
      "country": {"id": "KE", "value": "Kenya"},
      "countryiso3code": "KEN",
      "date": "2023",
      "value": 113140000000,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    }
  ]
]
```

### Rate Limits

The World Bank API does not impose strict rate limits, but best practice is to use `per_page=10000` to minimise the number of requests. There is no documented rate limit, but excessive automated requests may be throttled.

---

## Key Indicator Codes for Causal Atlas

### Economic Indicators

| Code | Name | Unit | Coverage |
|---|---|---|---|
| `NY.GDP.MKTP.CD` | GDP (current US$) | US$ | 1960--2023 |
| `NY.GDP.MKTP.KD` | GDP (constant 2015 US$) | US$ | 1960--2023 |
| `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) | % | 1961--2023 |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) | US$ | 1960--2023 |
| `NY.GDP.PCAP.KD` | GDP per capita (constant 2015 US$) | US$ | 1960--2023 |
| `NY.GDP.PCAP.PP.KD` | GDP per capita, PPP (constant 2021 intl $) | Intl $ | 1990--2023 |
| `NV.AGR.TOTL.ZS` | Agriculture, value added (% of GDP) | % | 1960--2023 |
| `NE.TRD.GNFS.ZS` | Trade (% of GDP) | % | 1960--2023 |
| `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) | % | 1960--2023 |
| `SL.UEM.TOTL.ZS` | Unemployment, total (% of labor force) | % | 1991--2023 |
| `BX.TRF.PWKR.CD.DT` | Personal remittances, received (current US$) | US$ | 1970--2023 |

### Poverty and Inequality

| Code | Name | Unit | Coverage |
|---|---|---|---|
| `SI.POV.DDAY` | Poverty headcount ratio at $2.15/day (2017 PPP) | % | Various |
| `SI.POV.LMIC` | Poverty headcount ratio at $3.65/day (2017 PPP) | % | Various |
| `SI.POV.UMIC` | Poverty headcount ratio at $6.85/day (2017 PPP) | % | Various |
| `SI.POV.NAHC` | Poverty headcount ratio at national poverty lines | % | Various |
| `SI.POV.GINI` | Gini index (World Bank estimate) | 0--100 | Various |
| `SI.DST.10TH.10` | Income share held by highest 10% | % | Various |
| `SI.DST.FRST.10` | Income share held by lowest 10% | % | Various |

**Note**: Poverty and inequality data are irregularly available -- they depend on household surveys which are conducted at irregular intervals (typically every 3-5 years). Many country-years have no data.

### Governance (Worldwide Governance Indicators -- source=3)

| Code | Name | Scale | Coverage |
|---|---|---|---|
| `CC.EST` | Control of Corruption: Estimate | -2.5 to 2.5 | 1996--2023 |
| `GE.EST` | Government Effectiveness: Estimate | -2.5 to 2.5 | 1996--2023 |
| `PV.EST` | Political Stability and Absence of Violence/Terrorism: Estimate | -2.5 to 2.5 | 1996--2023 |
| `RQ.EST` | Regulatory Quality: Estimate | -2.5 to 2.5 | 1996--2023 |
| `RL.EST` | Rule of Law: Estimate | -2.5 to 2.5 | 1996--2023 |
| `VA.EST` | Voice and Accountability: Estimate | -2.5 to 2.5 | 1996--2023 |
| `CC.PER.RNK` | Control of Corruption: Percentile Rank | 0--100 | 1996--2023 |

**Note**: WGI data uses `source=3` in API queries. The 2025 methodology revision introduces an absolute 0--100 scale anchored to fixed benchmark countries, alongside the traditional estimate scale.

WGI covers **214 economies** and aggregates information from **35 different data sources** including expert assessments and survey respondents.

### Population and Demographics

| Code | Name | Unit | Coverage |
|---|---|---|---|
| `SP.POP.TOTL` | Population, total | People | 1960--2023 |
| `SP.POP.GROW` | Population growth (annual %) | % | 1961--2023 |
| `SP.URB.TOTL.IN.ZS` | Urban population (% of total) | % | 1960--2023 |
| `SP.DYN.LE00.IN` | Life expectancy at birth, total | Years | 1960--2023 |
| `SP.DYN.IMRT.IN` | Infant mortality rate (per 1,000 live births) | Per 1000 | 1960--2023 |
| `SM.POP.REFG` | Refugee population by country of asylum | People | 1960--2023 |
| `SM.POP.REFG.OR` | Refugee population by country of origin | People | 1960--2023 |

### Health

| Code | Name | Unit | Coverage |
|---|---|---|---|
| `SH.DYN.MORT` | Under-5 mortality rate (per 1,000 live births) | Per 1000 | 1960--2023 |
| `SH.STA.STNT.ZS` | Stunting prevalence (% of children under 5) | % | Various |
| `SH.STA.MALN.ZS` | Malnutrition prevalence, weight for age (% of children under 5) | % | Various |
| `SH.XPD.CHEX.GD.ZS` | Current health expenditure (% of GDP) | % | 2000--2021 |
| `SN.ITK.DEFC.ZS` | Prevalence of undernourishment (% of population) | % | 2001--2022 |

### Education

| Code | Name | Unit | Coverage |
|---|---|---|---|
| `SE.ADT.LITR.ZS` | Literacy rate, adult total (% ages 15+) | % | Various |
| `SE.PRM.ENRR` | School enrollment, primary (% gross) | % | 1970--2023 |
| `SE.SEC.ENRR` | School enrollment, secondary (% gross) | % | 1970--2023 |

### Infrastructure and Environment

| Code | Name | Unit | Coverage |
|---|---|---|---|
| `EG.ELC.ACCS.ZS` | Access to electricity (% of population) | % | 1990--2022 |
| `IT.NET.USER.ZS` | Internet users (% of population) | % | 1990--2023 |
| `AG.LND.FRST.ZS` | Forest area (% of land area) | % | 1990--2021 |
| `EN.ATM.CO2E.PC` | CO2 emissions (metric tons per capita) | t/capita | 1960--2021 |

---

## Spatial Detail

### Coverage Level

World Bank data is primarily at **country level** (ISO 3166-1 alpha-3 codes). The API uses its own 3-character codes which mostly align with ISO3:

```
KEN = Kenya, TZA = Tanzania, UGA = Uganda, NGA = Nigeria, etc.
```

The API also provides data for:
- **Regional aggregates**: Sub-Saharan Africa (SSA), South Asia (SAS), etc.
- **Income groups**: Low income (LIC), Lower middle income (LMC), etc.
- **Lending groups**: IDA, IBRD, Blend
- **World total**: WLD

### Sub-national Data

Limited sub-national data is available through:
- **Subnational Poverty Database**: Poverty estimates at admin-1 level for ~100 countries
- **Poverty and Inequality Platform (PIP)**: Some sub-national estimates
- **World Bank Microdata Library**: Household survey microdata (requires separate access)

For Causal Atlas, country-level WDI data will be **broadcast to all PRIO-GRID cells within each country**, providing a uniform contextual layer.

---

## Temporal Detail

| Aspect | Detail |
|---|---|
| **Temporal resolution** | Primarily annual; some indicators available quarterly or monthly |
| **Earliest data** | 1960 for core indicators (GDP, population) |
| **Latest data** | Typically 1-2 years behind current year (2023 data available in 2025) |
| **Update frequency** | WDI updated quarterly (April, July, October, December) |
| **Historical revisions** | Past values may be revised in each update as source agencies revise data |

### Data Latency by Indicator Type

| Indicator Type | Typical Latency | Example |
|---|---|---|
| National accounts (GDP) | 1-2 years | 2023 GDP available mid-2025 |
| Population | 1 year | 2024 estimates available in 2025 |
| Poverty/inequality | 2-5 years | Survey-dependent |
| Governance (WGI) | 1 year | 2023 WGI available in 2024 |
| Health | 1-2 years | Varies by indicator |

---

## Quality and Limitations

### Data Quality Strengths

- **Standardised methodology**: WDI harmonises data from international sources (UN, IMF, WHO, ILO, etc.) using consistent definitions and methodologies
- **Metadata rich**: Each indicator has detailed source notes, definitions, methodology descriptions
- **Transparent revisions**: Historical data are updated when source agencies revise figures
- **Peer-reviewed compilation**: Backed by World Bank statistical standards

### Known Limitations

| Issue | Detail |
|---|---|
| **Missing data** | Many indicators have sparse coverage for low-income and conflict-affected states -- precisely the countries where Causal Atlas is most needed. Poverty data is especially patchy. |
| **Country-level only** | No sub-national breakdown for most indicators. Intra-country variation (urban vs. rural, conflict vs. non-conflict areas) is invisible. |
| **Annual granularity** | Monthly dynamics are not captured. Economic shocks, conflict impacts, and seasonal patterns require higher-frequency data (nighttime lights fill this gap). |
| **Latency** | 1-2 year publication lag means data is not useful for near-real-time monitoring. |
| **Revisions** | Historical values change across WDI editions. Analysis should note which WDI release was used. |
| **Aggregation artefacts** | Regional and income-group aggregates use specific weighting methodologies that may not suit all analytical purposes. |
| **Small states and territories** | Some micro-states and territories have very limited data coverage. |
| **Governance indicators (WGI)** | Perception-based, derived from 35 sources with varying methodology. Confidence intervals are wide for many countries. Not suitable as precise measurements. |

### Data Completeness Assessment (Key Indicators for Sub-Saharan Africa)

| Indicator | Completeness (SSA, 2000-2023) | Notes |
|---|---|---|
| GDP (current US$) | ~95% | Well-covered |
| GDP per capita | ~95% | Well-covered |
| Population | ~100% | UN estimates fill gaps |
| Gini index | ~20-30% | Very sparse, survey-dependent |
| Poverty headcount | ~20-30% | Very sparse, survey-dependent |
| Life expectancy | ~95% | Well-covered via UN estimates |
| Inflation | ~80% | Some gaps in conflict states |
| WGI indicators | ~95% (since 1996) | Good coverage since inception |

---

## Licence and Terms of Use

| Aspect | Detail |
|---|---|
| **Licence** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **Cost** | Free |
| **Registration** | Not required for API access |
| **Attribution** | Required: "Source: World Bank, [Database Name]" |
| **Redistribution** | Permitted with attribution |
| **Commercial use** | Permitted |

### Third-Party Data Restrictions

Some WDI indicators are sourced from third parties with their own terms. The World Bank notes that "certain data series may have additional terms and conditions." Always check the source notes for specific indicators.

### Citation

> World Bank. (2025). World Development Indicators [Data set]. The World Bank. https://data.worldbank.org/

> Kaufmann, D., Kraay, A. & Mastruzzi, M. (2011). "The Worldwide Governance Indicators: Methodology and Analytical Issues." Hague Journal on the Rule of Law, 3(2), 220-246.

---

## Interoperability with Other Causal Atlas Datasets

| Dataset | Relationship | Integration Notes |
|---|---|---|
| **PRIO-GRID** | Country-level WDI values broadcast to all grid cells within a country. PRIO-GRID includes country identifiers (gwno, ISO codes). | Join via ISO3 country code or GW number. |
| **ACLED / UCDP-GED** | Governance indicators (WGI), GDP, inequality as context variables for conflict analysis. | Country-year join; WGI political stability as predictor. |
| **Nighttime lights** | NTL sum-of-lights at country level can be compared with/substitute for GDP. NTL provides sub-annual and sub-national resolution that WDI lacks. | Country-level NTL aggregation for validation against GDP. |
| **WFP food prices** | Inflation (CPI), GDP per capita as economic context for food price analysis. | Country-year context layer. |
| **FAO data** | Agriculture value added (% GDP) provides sector importance context for FAO crop production data. | Country-year join. |
| **CHIRPS / NDVI** | Economic vulnerability (GDP per capita, poverty) as moderating variable in climate-impact causal chains. | Country-level economic context for interpreting grid-level climate impacts. |
| **EM-DAT** | GDP as denominator for disaster economic impact normalisation (damage as % of GDP). | Country-year join for impact assessment. |
| **HDX HAPI** | ISO3 country codes shared. WDI supplements HDX humanitarian data with development context. | Direct ISO3 join. |

---

## Python Access

### wbgapi (Official World Bank Python Library)

The `wbgapi` library is the most modern and comprehensive Python interface to the World Bank API.

```bash
pip install wbgapi
```

#### Basic Usage

```python
import wbgapi as wb

# Explore available databases
wb.source.info()
# Default database is WDI (db=2)

# Search for indicators by keyword
wb.series.info(q='GDP per capita')

# Get indicator metadata
wb.series.get('NY.GDP.PCAP.CD')

# Fetch data as DataFrame
import pandas as pd

# GDP per capita for all countries, 2010-2023
df = wb.data.DataFrame(
    'NY.GDP.PCAP.CD',
    economy=wb.region.members('SSA'),  # Sub-Saharan Africa
    time=range(2010, 2024)
)
print(df.head())
```

#### Multiple Indicators

```python
# Fetch multiple indicators simultaneously
indicators = [
    'NY.GDP.PCAP.CD',      # GDP per capita
    'SP.POP.TOTL',          # Population
    'SI.POV.DDAY',          # Poverty headcount
    'FP.CPI.TOTL.ZG',      # Inflation
]

df = wb.data.DataFrame(
    indicators,
    economy=['KEN', 'TZA', 'UGA', 'ETH', 'SOM', 'SDN', 'SSD'],
    time=range(2000, 2024)
)
```

#### Governance Indicators (WGI)

```python
# Switch to WGI database (source=3)
wb.db = 3

# List available WGI indicators
wb.series.info()

# Fetch political stability for all countries
df_wgi = wb.data.DataFrame(
    'PV.EST',  # Political Stability
    time=range(2000, 2024)
)

# Reset to WDI
wb.db = 2
```

#### Country Metadata

```python
# Get all country information as DataFrame
countries = wb.economy.DataFrame()
# Includes: region, incomeLevel, lendingType, capitalCity, longitude, latitude

# Filter to specific income group
lic = wb.economy.info(wb.income.members('LIC'))  # Low-income countries
```

#### Most Recent Values

```python
# Get most recent 5 available values (useful for sparse indicators like poverty)
df = wb.data.DataFrame(
    'SI.POV.GINI',
    economy='all',
    mrv=5
)
```

### Direct API Access with requests

```python
import requests
import pandas as pd

def fetch_wb_indicator(indicator, countries='all', date_range='2000:2023'):
    """Fetch World Bank indicator data via API v2."""
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
    params = {
        'format': 'json',
        'date': date_range,
        'per_page': 10000
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    if len(data) < 2:
        return pd.DataFrame()

    records = data[1]
    df = pd.DataFrame([{
        'country_code': r['countryiso3code'],
        'country': r['country']['value'],
        'year': int(r['date']),
        'value': r['value'],
        'indicator': r['indicator']['id']
    } for r in records if r['value'] is not None])

    return df

# Usage
gdp = fetch_wb_indicator('NY.GDP.MKTP.CD', 'KEN;TZA;UGA')
print(gdp.head())
```

### pandas-datareader (Alternative)

```python
from pandas_datareader import wb

# Fetch GDP per capita for Sub-Saharan African countries
df = wb.download(
    indicator='NY.GDP.PCAP.CD',
    country=['KEN', 'TZA', 'UGA', 'ETH'],
    start=2000,
    end=2023
)
```

**Note**: `pandas-datareader` uses the older API and may have compatibility issues. `wbgapi` is recommended.

### Bulk Download

```python
import requests
import zipfile
import io

# Download entire WDI dataset as CSV
url = "https://databank.worldbank.org/data/download/WDI_csv.zip"
resp = requests.get(url)
with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
    z.extractall("./wdi_data/")

# Files include:
# WDIData.csv - Main data file (large: ~700MB uncompressed)
# WDISeries.csv - Indicator metadata
# WDICountry.csv - Country metadata
# WDICountry-Series.csv - Country-indicator notes
```

---

## Relevance to Causal Atlas

### Primary Use Cases

1. **Economic context layer**: GDP, GDP per capita, and growth rates provide essential economic context for interpreting conflict, food security, and environmental events at the country level.

2. **Governance and institutional quality**: WGI indicators (especially Political Stability and Rule of Law) are critical control variables in conflict analysis. Poor governance may moderate or amplify the impact of environmental stressors on conflict.

3. **Vulnerability assessment**: Poverty headcount, inequality (Gini), and human development indicators identify populations vulnerable to climate shocks, food crises, and conflict.

4. **Causal chain moderators**: Economic variables serve as moderating factors in cross-domain causal chains. For example, the impact of drought on conflict may be stronger in countries with lower GDP per capita, higher inequality, or weaker governance.

5. **Normalisation denominators**: GDP, population, and other macro indicators serve as denominators for normalising conflict events, disaster impacts, and other outcomes.

### Limitations for Causal Atlas

- **Country-level resolution is too coarse** for grid-cell-level causal analysis. WDI data must be treated as a contextual layer rather than a spatially varying predictor within countries.
- **Annual temporal resolution** is too slow for detecting monthly causal lags. Nighttime lights provide a sub-annual, sub-national economic proxy that complements WDI.
- **Sparse poverty/inequality data** limits time-series analysis for these critical variables. Consider using nighttime lights or survey-based estimates as alternatives.

### Integration Strategy

1. **Ingest key indicators** via `wbgapi` for all countries, 1990--present.
2. **Store as country-year Parquet** with ISO3 codes as identifiers.
3. **Join to PRIO-GRID** by broadcasting country values to all grid cells within each country boundary (using a country-to-grid mapping layer).
4. **Use as control variables** in statistical models, not as primary spatially-varying predictors.
5. **Complement with nighttime lights** for sub-national, sub-annual economic variation.

---

## Sources

- World Bank Open Data: https://data.worldbank.org/
- World Development Indicators: https://datatopics.worldbank.org/world-development-indicators/
- API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- API basic call structure: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures
- V2 API features: https://datahelpdesk.worldbank.org/knowledgebase/articles/1886674-new-features-and-enhancements-in-the-v2-api
- Indicator API queries: https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries
- Country API queries: https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-country-api-queries
- Worldwide Governance Indicators: https://www.worldbank.org/en/publication/worldwide-governance-indicators
- WGI methodology: https://www.worldbank.org/en/publication/worldwide-governance-indicators/documentation
- wbgapi on PyPI: https://pypi.org/project/wbgapi/
- wbgapi on GitHub: https://github.com/tgherzog/wbgapi
- Poverty and Inequality Platform: https://pip.worldbank.org/
- WDI quarterly updates: https://datatopics.worldbank.org/world-development-indicators/
