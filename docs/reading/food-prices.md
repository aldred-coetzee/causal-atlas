# Reading: can local staple food prices be fetched, and on what terms

Bounded reading, 2026-11-10. One question, pulled by one decision (0049): which
place-by-place monthly food price data can be fetched by script with no account,
on what licence and coverage, and are its prices observed or modelled? One helper
read (178,152 fresh tokens, counted from its transcript). It was
asked to download no more than 5 MB and took about 14 MB, which it disclosed: two
files came down whole because the server ignored a request for part of them. It
sent no address anywhere and made no account. This session then checked at source
what the choice rests on, and fetched and counted the chosen file. The helper's
page follows as written; "I" in it is the helper.

## Checked at source by this session, 2026-11-10

- The file's address answers with 133,148,482 bytes and the name
  `WLD_RTFP_mkt_2026-11-02.zip`; the site has no robots file (404).
- The study record (`https://microdata.worldbank.org/index.php/api/catalog/4483?id_format=id`)
  gives access as "open" and "Public use", and says: "The estimates presented in
  this dataset are all based on publicly-available data. The dataset of price
  estimates is published as open data." Its citation is the one in
  `docs/data-sources.md`.
- The same record says "Predicted data for missing entries are based on exchange
  rates, and price data available either at other market locations or from
  related price items" and "To produce smooth price series, outliers in the data
  are often adjusted using non-parametric density estimation and other
  techniques." It does not mention weather, rainfall, drought or vegetation.
- **Not re-checked by this session:** the "Creative Commons Attribution 4.0"
  wording, which the helper read on a country entry of the World Bank's Data
  Catalog, and the three papers' figures in section 3.
- **Counted on the whole file, prices alone:** 762,728 rows, 37 countries, 3,229
  markets (3,192 with coordinates), 2007-01 to 2026-11. 571 markets in 33
  countries have one cereal with 120 or more observed months, 272 with 180 or
  more. Where an observed price exists the model's closing estimate equals it in
  about 90% of months. Detail in decision 0049.

---

## The helper's page

### 1. Answer

Two sources are usable with no account: the World Bank's **Real Time Food Prices** (RTFP) market file and FAO's **GIEWS FPMA** price API. I would start with **RTFP, using only its raw-price columns**. It has latitude and longitude for every market, an explicit CC BY 4.0 licence, and dated, frozen releases in a single file. Its weakness is length. It starts in 2007, so no series can be longer than about 19 years. Many markets have only a few years of raw prices, and the rest of each series is model-filled. In the Afghanistan rows I read, 13 of 20 provincial wheat series have raw prices only from 2020; Kabul, Hirat, Jalalabad and Kandahar have them from 2007. Whether enough markets have 15 or more years of raw cereal prices is **not yet counted**; that takes the full 133 MB file. FPMA has longer and wider records: 714 cereal series in 95 countries span at least 15 years. But it has no coordinates, so markets would have to be geocoded by name. Many of its series come from third parties (WFP, FEWS NET, national bodies), and FAO's licence excludes third-party data from its blanket CC BY. FEWS NET and WFP DataBridges are closed to us.

### 2. Sources

| | RTFP (World Bank) | FAO GIEWS FPMA | FEWS NET FDW | WFP DataBridges |
|---|---|---|---|---|
| Open route, tested | `https://microdata.worldbank.org/catalog/4483/download/361260/WLD_RTFP_mkt_2026-11-02.zip`: **200**, `application/octet-stream`, 133,148,482 bytes; a range request gave the CSV header. Listing: `.../index.php/api/catalog/WLD_2021_RTFP_v02_M/resources` | `https://fpma.fao.org/giews/v4/global/price_module/api/v1/FpmaSerie/` (catalogue, **200** JSON, 4.1 MB) and `.../FpmaSeriePrice/<uuid>/?periodicity=monthly` (**200** JSON; the endpoint was found by reading the web app's code) | None: `fdw.fews.net/robots.txt` is `Disallow: /` for every agent | None: credentials only by email to WFP. The old gateway gives **401** |
| Scripted fetching | No robots.txt (404). Terms say nothing on automated access | No robots.txt on fpma.fao.org (it redirects to the app). FAO database terms say nothing on it | `/llms.txt`: "Please do not crawl this site … If you want the data, ask" | n/a |
| Licence | Chad entry: "License: Creative Commons Attribution 4.0" ([datacatalog](https://datacatalog.worldbank.org/search/dataset/0060174/chad-monthly-food-price-estimates-by-product-and-market)). Global entry: "published as open data"; citation to Andrée (2021), DOI 10.48529/2ZH0-JF55 | "licensed under the Creative Commons Attribution-4.0 International licence", but third-party data "may not be redistributed or reused without the consent of the original data provider" ([FAO](https://www.fao.org/contact-us/terms/db-terms-of-use/en/)) | n/a | n/a |
| Coverage | 37 countries, 3,192 markets, 2007-01 to 2026-11 (study page). Mostly fragile states in Africa, Asia, Haiti and Guatemala | 4,938 series, 690 markets, 139 countries, 1987-01 to 2026-10. 714 cereal series in 292 markets and 95 countries span at least 15 years and run past 2024 | n/a | n/a |
| Observed or modelled | Both (see below) | Observed, with the source named per series | n/a | n/a |
| Coordinates | Yes: `lat`, `lon`, `geo_id` | No: names and admin units only | n/a | n/a |
| Versioning, host | Dated releases, old ones still listed. World Bank, US | Live API, not versioned. FAO, Rome (Italy) | | |

**RTFP, raw versus modelled.** Every item has a bare column (e.g. `maize`) and estimated columns `o_/h_/l_/c_`, plus `inflation_` and `trust_`. In the rows I opened, the bare column is filled only in some months, and where it is filled `c_` equals it. Elsewhere `c_` is imputed, and `trust_` rises from about 6.6 to 10 where there is an observation. That the bare column is the raw observation is **my inference from the file**; I did not find it stated in the documentation. The study page also says "outliers in the data are often adjusted", so even the bare values may be cleaned.

**RTFP, is weather an input?** In the documentation I read, no. The study page says: "Predicted data for missing entries are based on exchange rates, and price data available either at other market locations or from related price items" ([study page](https://microdata.worldbank.org/index.php/catalog/4483/study-description)). The method paper ([WPS 9886](https://doi.org/10.1596/1813-9450-9886), pp. 12–13) lists the inputs as other items' prices, "logarithmic coordinates", "market-level fixed effects and administrative-level fixed effects", "seasonal dummies" and country price-trend features. So weather does not enter. But imputed values borrow from neighbouring markets and from seasonality, which would blur a local drought signal. Use bare columns only.

### 3. Published sizes for the link

1. **Ethiopia, 82 markets, 1996–2012** (Hill & Fuje, World Bank WPS 9389, 2020, [pdf](https://documents1.worldbank.org/curated/en/840771599657255297/pdf/What-is-the-Impact-of-Weather-Shocks-on-Prices-Evidence-from-Ethiopia.pdf)): "On average a 1 in 5-year moderate drought caused grain prices from January to May to increase by 9 percent", falling to "3 percent" by the lean season. Separately: "a 12 percent increase in prices in March before 2004 in comparison to a 4 percent increase post 2004". The main rainy season runs May to November, so the effect peaks about 2 to 5 months after the season ends, roughly 8 to 11 months after it starts.
2. **554 markets, 51 countries, 2008–2012** (Brown & Kshirsagar, Global Environmental Change 35, 2015, doi 10.1016/j.gloenvcha.2015.08.003, [open copy](https://gala.gre.ac.uk/id/eprint/28384/)): "almost 20% of local market prices were affected by domestic weather disturbances in the short run". The body text gives 23.2%, and says that for "a fifth of our sample" lagged weather fits better than a seasonal random walk. In Eldoret, Kenya: "an NDVI anomaly of 10% is associated with a 9% decrease in price of maize". **The lag is one month**, shorter than ours.
3. **Ethiopia, Kenya, Somalia, Malawi, Mozambique, about 1995–2018** (Davenport et al., Environmental Research Letters 2021, doi 10.1088/1748-9326/ac15cc): a start-of-season indicator "leads to increased predictive power when examining prices over a 6 months window". It is strongest in central Ethiopia, southern Kenya and southern Somalia, with less support in Malawi and Mozambique. Results are reported as MAPE rankings, with no effect size. This one is out of sample, which is closest to our rule 2.

### 4. Not checked, or resting on documentation

- **Not counted:** the RTFP markets with 15 or more years of raw cereal prices. Only the first 1 MB was decompressed, which covers Afghanistan only.
- **Gaps in FPMA not checked:** its 15-year count uses each series' first and last dates, not gaps. One sample (Tombouctou millet) had 221 of 226 months.
- **RTFP figures from documentation:** the country, market and date coverage and the weather-free imputation come from the study page and the 2021 paper. The current model may have changed. I also did not check whether RTFP appears on the World Bank's restricted-data list.
- **FPMA licences per source not checked:** I did not check the terms of each third-party source behind the FPMA series.
- **Not checked:** WFP VAM's dataviz site, whose robots.txt allows all, beyond its robots file.
- **Paywalled:** none of the three papers. Paper 3 was read through a fetch summary of its page, not the full PDF.
- **Download limit exceeded:** about 14 MB in total against the 5 MB asked. The FPMA web app's code (4.3 MB) and the series catalogue (4.1 MB) came down whole; the API ignored a range request.
