# Cross-Domain Causal Chains: Published Research Review

> **Last updated:** March 2025
> **Purpose:** Comprehensive review of published academic research on cross-domain causal relationships relevant to the Causal Atlas project. Documents key papers, datasets used, lag structures found, statistical methods, effect sizes, and controversies for each major causal pathway.

---

## Table of Contents

1. [Drought to Crop Failure to Food Price to Conflict/Unrest](#1-drought--crop-failure--food-price--conflictunrest)
2. [Climate Extremes to Migration/Displacement](#2-climate-extremes--migrationdisplacement)
3. [Pollution/Air Quality to Health Outcomes](#3-pollutionair-quality--health-outcomes)
4. [Earthquake to Economic Disruption to Social Effects](#4-earthquake--economic-disruption--social-effects)
5. [Commodity Price Shocks to Political Instability](#5-commodity-price-shocks--political-instability)
6. [Disease Outbreaks to Economic and Social Impacts](#6-disease-outbreaks--economic-and-social-impacts)
7. [Deforestation to Climate to Food Security](#7-deforestation--climate--food-security)
8. [Urbanization to Pollution to Health](#8-urbanization--pollution--health)
9. [Other Documented Multi-Domain Causal Chains](#9-other-documented-multi-domain-causal-chains)
10. [Cross-Cutting Methodological Insights](#10-cross-cutting-methodological-insights)
11. [Implications for Causal Atlas](#11-implications-for-causal-atlas)

---

## 1. Drought -> Crop Failure -> Food Price -> Conflict/Unrest

This is the most extensively studied cross-domain causal chain in the literature. The pathway runs: climate anomaly (drought/heat) -> reduced agricultural output -> rising food prices -> economic grievance -> social unrest or armed conflict.

### 1.1 Seminal Meta-Analyses

#### Hsiang, Burke & Miguel (2013) — "Quantifying the Influence of Climate on Human Conflict"
- **Journal:** Science, Vol. 341, Issue 6151
- **DOI:** 10.1126/science.1235367
- **Method:** Hierarchical meta-analysis of 60 rigorous quantitative studies
- **Key findings:**
  - Each 1 standard deviation (1sigma) change toward warmer temperatures or more extreme rainfall increases interpersonal violence by 4% and intergroup conflict by 14%
  - Effects are consistent across spatial scales (individual, local, national, global) and temporal scales (hourly to multi-decadal)
  - Effects documented across all major world regions
- **Datasets used across studies:** UCDP/PRIO Armed Conflict Dataset, ACLED, police records, archaeological data, agricultural output records
- **Controversies:** Some scholars (e.g., Buhaug 2010) argued the climate-conflict link is overstated and confounded by socioeconomic factors

#### Burke, Hsiang & Miguel (2015) — "Climate and Conflict"
- **Journal:** Annual Review of Economics, Vol. 7, pp. 577-617
- **DOI:** 10.1146/annurev-economics-080614-115430
- **Method:** Updated meta-analysis with refined methodology
- **Key findings:**
  - Contemporaneous temperature has the largest average impact
  - Each 1sigma increase in temperature increases interpersonal conflict by 2.4% and intergroup conflict by 11.3%
  - The approach emphasizes natural experiments using climate variation over time rather than cross-sectional geographic comparisons
- **Regions:** Global coverage with strongest evidence from Sub-Saharan Africa, Latin America, and South/Southeast Asia

#### Burke, Hsiang & Miguel (2024) — Updated Meta-Analysis
- **Source:** NBER Working Paper No. 33040
- **URL:** https://www.nber.org/system/files/working_papers/w33040/w33040.pdf
- **Key findings:**
  - Updated with far larger sample of studies
  - Confirms extreme climate is associated with elevated risk of inter-group conflict, interpersonal violence, and self-harm
  - Average effects are smaller than earlier estimates but remain statistically significant and meaningful in magnitude

### 1.2 Disaggregated and Cell-Level Studies

#### Harari & La Ferrara (2018) — "Conflict, Climate, and Cells: A Disaggregated Analysis"
- **Journal:** The Review of Economics and Statistics, Vol. 100(4), pp. 594-608
- **DOI:** 10.1162/rest_a_00730
- **Method:** Spatial econometric analysis at PRIO-GRID cell level (0.5deg x 0.5deg)
- **Datasets:** UCDP-GED georeferenced conflict events, PRIO-GRID, crop calendar data, weather station data
- **Key findings:**
  - Negative weather shocks occurring during the growing season of local crops increase conflict incidence
  - Effects are persistent (multiple subsequent periods)
  - Spatial spillover: conflict in one cell increases conflict risk in neighboring cells
- **Lag structure:** Growing-season shocks affect conflict in the same year and subsequent years
- **Region:** Africa, 1997-2011
- **Significance for Causal Atlas:** Demonstrates the value of cell-level gridded analysis (exactly our approach) for identifying climate-conflict links

#### von Uexkull, Croicu, Fjelde & Buhaug (2016) — "Civil Conflict Sensitivity to Growing-Season Drought"
- **Journal:** PNAS, Vol. 113(44), pp. 12391-12396
- **DOI:** 10.1073/pnas.1607542113
- **Method:** Actor-oriented analysis using georeferenced ethnicity and conflict data
- **Datasets:** UCDP-GED, Ethnic Power Relations (EPR), PRIO-GRID, SPEI drought index
- **Key findings:**
  - Naive models suggest drought has little general impact on conflict
  - Context-sensitive models reveal drought can sustain conflict, especially for:
    - Agriculturally dependent ethnic groups
    - Politically excluded groups in very poor countries
  - The interaction between drought and agricultural dependence is critical
- **Lag structure:** Growing-season effects with lags of 0-12 months
- **Region:** Asia and Africa, 1989-2014
- **Significance:** Shows that context (agricultural dependence, political exclusion, poverty) mediates the climate-conflict pathway

#### Hendrix & Salehyan (2012) — "Climate Change, Rainfall, and Social Conflict in Africa"
- **Journal:** Journal of Peace Research, Vol. 49(1), pp. 35-50
- **DOI:** 10.1177/0022343311426165
- **Datasets:** Social Conflict in Africa Database (SCAD, 6,000+ events over 20 years), ACLED, GPCP rainfall data
- **Key findings:**
  - Rainfall variability significantly affects both large-scale and smaller-scale instances of political conflict
  - Both extreme wet and extreme dry anomalies increase conflict risk
  - Broader definition of conflict (demonstrations, riots, strikes, communal violence) beyond just organized rebellion
- **Region:** Africa, 1990-2009

### 1.3 Case Studies

#### Kelley, Mohtadi, Cane, Seager & Kushnir (2015) — "Climate Change in the Fertile Crescent and Implications of the Recent Syrian Drought"
- **Journal:** PNAS, Vol. 112(11), pp. 3241-3246
- **DOI:** 10.1073/pnas.1421533112
- **Key findings:**
  - The 2007-2010 Syrian drought (worst in instrumental record) caused widespread crop failure
  - Mass migration of ~1.5 million people from rural farming areas to urban peripheries
  - Anthropogenic forcing made such a 3-year drought 2-3 times more likely
  - Drought contributed to conditions leading to the 2011 Syrian conflict
- **Lag structure:** 3-4 year chain: drought (2007-2010) -> crop failure and migration (2008-2010) -> urban stress -> conflict onset (2011)
- **Datasets:** CRU temperature/precipitation records, GPCC precipitation, climate model ensembles (CMIP5)
- **Controversies:** Selby et al. (2017, Political Geography) challenged this narrative, arguing the drought-conflict link in Syria has been overstated and the causal chain oversimplified. They note pre-existing agricultural policy failures and political factors were more important drivers.

### 1.4 Expert Assessment

#### Mach, Kraan et al. (2019) — "Climate as a Risk Factor for Armed Conflict"
- **Journal:** Nature, Vol. 571, pp. 193-197
- **DOI:** 10.1038/s41586-019-1300-6
- **Method:** Structured expert elicitation with 11 experts from diverse disciplines; 950 pages of transcripts
- **Key findings:**
  - Expert consensus: 3-20% of organized armed conflict risk over the last century has been influenced by climate
  - Other drivers (low socioeconomic development, low state capacity) judged substantially more influential
  - Mechanisms of climate-conflict linkages remain a key uncertainty
  - Intensifying climate change estimated to increase future conflict risk
- **Significance:** Provides a calibrated, uncertainty-aware assessment that avoids both alarmism and dismissal

### 1.5 Historical Evidence

#### Zhang, Brecke, Lee, He & Zhang (2007) — "Global Climate Change, War, and Population Decline in Recent Human History"
- **Journal:** PNAS, Vol. 104(49), pp. 19214-19219
- **DOI:** 10.1073/pnas.0703073104
- **Datasets:** European temperature reconstructions, historical conflict databases, population records
- **Key findings:**
  - Grain price was the Granger-cause of social disturbance, war, migration, epidemics, and famine
  - Temperature change was the Granger-cause of grain price (agricultural production was climate-dependent)
  - Causal chain: cooling -> poor harvests -> high grain prices -> social disturbance -> war -> famine/epidemics -> population decline
- **Lag structure:** Multi-decadal analysis with lags of years to decades
- **Statistical method:** Granger causality analysis on long time series

### 1.6 Summary of Lag Structures Found

| Study | Lag (Climate to Conflict) | Spatial Resolution | Mechanism |
|-------|--------------------------|-------------------|-----------|
| Hsiang et al. 2013 | Contemporaneous to 1 year | National | Temperature direct effects |
| Harari & La Ferrara 2018 | 0-12 months (growing season) | 0.5deg grid cell | Agricultural shock |
| von Uexkull et al. 2016 | 0-12 months | Grid cell/ethnic group | Drought in growing season |
| Kelley et al. 2015 | 3-4 years (full chain) | Regional | Drought -> migration -> urban stress |
| Zhang et al. 2007 | Years to decades | Continental | Cooling -> grain price -> war |
| Hendrix & Salehyan 2012 | 0-12 months | National | Rainfall anomaly |

### 1.7 Controversies and Conflicting Findings

- **Buhaug (2010, PNAS)** challenged the Burke et al. (2009) findings, arguing that civil war in Africa is better predicted by structural/institutional factors than climate variables. This sparked a productive debate that led to more nuanced, context-sensitive research.
- **Selby et al. (2017, Political Geography)** challenged the Syria drought-conflict narrative, noting pre-existing agricultural mismanagement and political repression as more important drivers.
- **Adams et al. (2018, Journal of Peace Research)** found that the effect sizes in climate-conflict studies vary considerably depending on the conflict measure used, the climate variable examined, and the time period studied.
- **Theisen, Holtermann & Buhaug (2012)** found no robust statistical relationship between drought and civil conflict onset in Africa when using more granular conflict data.
- The field has largely moved from debating *whether* climate affects conflict to understanding *when, where, and through what mechanisms* it does.

---

## 2. Climate Extremes -> Migration/Displacement

### 2.1 Key Frameworks and Reviews

#### Cattaneo & Peri (2016) — "The Migration Response to Increasing Temperatures"
- **Journal:** Journal of Development Economics, Vol. 122, pp. 127-146
- **DOI:** 10.1016/j.jdeveco.2016.05.004
- **Datasets:** Bilateral migration data (World Bank), temperature and precipitation data, panel of 116 countries (1960-2000)
- **Key findings:**
  - Heterogeneous effects by income level:
    - **Middle-income countries:** Higher temperatures increased emigration (both urban and international)
    - **Poor countries:** Higher temperatures *reduced* emigration probability, consistent with liquidity constraints (too poor to move)
  - This "trapped populations" finding is critical: the most climate-vulnerable populations may be least able to migrate
- **Effect size:** A 1degC temperature increase raises emigration rates by ~0.5 percentage points in middle-income countries
- **Lag structure:** Decadal trends rather than short-term shocks

#### Rigaud, de Sherbinin et al. (2018) — "Groundswell: Preparing for Internal Climate Migration" (World Bank)
- **URL:** https://openknowledge.worldbank.org/handle/10986/29461
- **Method:** Agent-based and gravity models under three climate scenarios
- **Key findings:**
  - By 2050, 143 million people (~3% of population) in Sub-Saharan Africa, Latin America, and South Asia could be forced to move within their own countries
  - Main drivers: water availability, crop productivity, sea level rise
  - Concerted climate and development action could reduce internal climate migration by up to 80%
- **Regions:** Sub-Saharan Africa (86 million), South Asia (40 million), Latin America (17 million)
- **Datasets:** Climate projections (CMIP5), crop models, population projections, DEM for sea level rise

#### Hoffmann, Dimitrova, Muttarak et al. (2020) — Methodological Review
- **Journal:** Global Environmental Change, Vol. 71, 102367
- **DOI:** 10.1016/j.gloenvcha.2021.102367 (published 2021)
- **Method:** Systematic review of 127 quantitative studies
- **Key challenges identified:**
  1. Measurement of migration and climatic events
  2. Integration and aggregation of data across scales
  3. Identification of causal relationships
  4. Exploration of contextual influences and mechanisms
  5. Different definitions of migration (internal vs. international, permanent vs. temporary)
- **Key insight:** Climate change is at most an *indirect* driver of migration, operating through pre-existing economic, demographic, social, political, and environmental conditions

#### Daoust (2024) — "Climate Change and Migration: A Review and New Framework"
- **Journal:** WIREs Climate Change
- **DOI:** 10.1002/wcc.886
- **Key contribution:** Presents five different pathways through which climate change might affect migration, emphasizing that slow-onset events (drought) produce different migration patterns than rapid-onset events (storms/floods)

### 2.2 Lag Structures and Temporal Dynamics

The literature reveals important distinctions in temporal dynamics:

| Event Type | Typical Lag | Migration Type | Duration |
|-----------|-------------|----------------|----------|
| Rapid-onset (flood, cyclone) | Days to weeks | Sudden displacement, predominantly internal | Often temporary (return within months) |
| Slow-onset (drought, sea level rise) | Months to years | Progressive departure, can be international | Often permanent |
| Temperature trends | Decades | Gradual rural-urban shift | Permanent structural change |
| Crop failure | 3-12 months | Seasonal/permanent rural-urban | Variable |

### 2.3 Datasets Commonly Used

- **Migration:** World Bank bilateral migration matrices, census microdata (IPUMS), Internal Displacement Monitoring Centre (IDMC), UNHCR refugee data
- **Climate:** CRU TS, ERA5, CHIRPS, GPCC precipitation, Berkeley Earth temperature
- **Intermediary variables:** FAO crop production, NDVI (vegetation health), soil moisture (SMAP/SMOS)

### 2.4 Controversies

- **Immobility paradox:** The poorest and most vulnerable populations are often *unable* to migrate (Cattaneo & Peri 2016; Black & Collyer 2014), challenging the narrative of mass climate migration
- **Attribution difficulty:** Isolating climate from other migration drivers (economic opportunity, political instability, social networks) remains extremely challenging
- **Projections vary enormously:** Estimates of future climate migrants range from tens of millions to over a billion, depending on assumptions and definitions
- **Internal vs. international:** Most climate-related migration is internal, but policy attention focuses disproportionately on international movement

---

## 3. Pollution/Air Quality -> Health Outcomes

### 3.1 PM2.5 and Respiratory/Cardiovascular Mortality

#### WHO Systematic Review and Meta-Analysis (2024 update)
- **Journal:** International Journal of Environmental Research and Public Health
- **PMC:** PMC11466858
- **Method:** Systematic review and meta-analysis updating WHO Global Air Quality Guidelines
- **Key findings:**
  - Each 10 ug/m3 increment in PM2.5 increases risk of respiratory disease mortality by ~10%
  - Each 10 ug/m3 increment in PM10 increases respiratory mortality risk by ~12%
  - Approximately 3.2 million worldwide deaths in 2010 attributed to ambient PM2.5 (sixth largest overall global risk factor)
- **Lag structure:** Both short-term (days, for acute events) and long-term (years of cumulative exposure)
- **Statistical methods:** Cox proportional hazards models, marginal structural models, spatiotemporal exposure models

#### Long-term PM2.5 Exposure and Mortality (Di et al., 2017)
- **Journal:** New England Journal of Medicine, Vol. 376, pp. 2513-2522
- **Datasets:** Medicare beneficiary data (61 million), satellite-derived PM2.5 estimates, NASA MODIS AOD
- **Key findings:**
  - Significant mortality effects even below EPA standards (12 ug/m3)
  - Each 10 ug/m3 increase in PM2.5 associated with 7.3% increase in all-cause mortality
  - Effects larger in low-income communities and among racial minorities

#### Cohort Evidence from China (JMIR, 2024)
- **DOI:** 10.2196/56059
- **Key findings:**
  - 6.6% increase in respiratory mortality per 1 ug/m3 increase in PM1
  - 4.2% increase per 1 ug/m3 for PM2.5
  - 4.0% increase per 1 ug/m3 for PM10
- **Method:** Validated spatiotemporal models estimating annual average concentrations at residential addresses

### 3.2 Lead Exposure -> Cognitive Impairment -> Crime

This is one of the most striking cross-domain causal chains discovered, with a remarkably long lag.

#### Reyes (2007) — "Environmental Policy as Social Policy? The Impact of Childhood Lead Exposure on Crime"
- **Journal:** B.E. Journal of Economic Analysis & Policy, Vol. 7(1)
- **NBER Working Paper:** 13097
- **Datasets:** State-level gasoline lead content, blood lead levels in children (NHANES), FBI Uniform Crime Reports
- **Key findings:**
  - Phase-out of lead from gasoline was responsible for approximately 56% of the decline in violent crime in the US between 1992 and 2002
  - Strong correlation (r = 0.54) between average lead in gasoline and blood lead levels in children
  - **Lag structure: 20-year time lag** between childhood exposure and adult criminal behavior
  - Largest crime declines occurred in states with largest lead exposure declines
- **Mechanism:** "Childhood lead exposure increases the likelihood of behavioral and cognitive traits such as impulsivity, aggressivity, and low IQ that are strongly associated with criminal behavior"
- **Region:** United States

#### Nevin (2000, 2007) — International Lead-Crime Evidence
- **Journal:** Environmental Research, Vol. 83(1), pp. 1-22 (2000); Vol. 104(3), pp. 315-336 (2007)
- **Key findings:**
  - Found lead-crime relationship for all types of crime (violence, sexual assault, murder, property crime) — broader than Reyes who found it primarily for violent offences
  - Replicated across nine countries (US, Canada, UK, France, Finland, Italy, West Germany, Australia, New Zealand)
  - **Lag structure:** 18-23 years depending on crime type and country
- **Significance:** Cross-national replication strengthens the causal claim considerably

#### Meta-Analysis (Higney et al., 2022)
- **Journal:** Journal of Environmental Economics and Management
- **DOI:** 10.1016/j.jeem.2022.102665 (approximate)
- **Published in:** Journal of Housing Economics, 2022
- **Key finding:** Meta-analysis of lead-crime studies confirms a significant but heterogeneous relationship; spatial distribution of lead exposure is uneven, with urban areas disproportionately affected

### 3.3 Spatial Patterns and Environmental Justice

- Pollution exposure is systematically unequal: lower-income communities and racial minorities bear disproportionate burden
- This creates spatial clustering of health outcomes that can be detected in gridded analysis
- PM2.5 concentration is a strong predictor of respiratory hospital admissions at fine spatial scales (zip code or grid cell level)

### 3.4 Lag Structures Summary

| Exposure | Health Outcome | Lag | Effect Size |
|----------|---------------|-----|-------------|
| PM2.5 (acute) | Respiratory ER visits | 0-3 days | ~1-3% per 10 ug/m3 |
| PM2.5 (chronic) | All-cause mortality | Years (cumulative) | 7.3% per 10 ug/m3 |
| PM2.5 (chronic) | Respiratory mortality | Years | 10% per 10 ug/m3 |
| Lead (childhood) | Violent crime | 18-23 years | ~56% of crime decline attributable |
| Ozone (acute) | Respiratory admissions | 0-5 days | ~1-2% per 10 ppb |

---

## 4. Earthquake -> Economic Disruption -> Social Effects

### 4.1 Comprehensive Reviews

#### Aksoy, Chupilkin, Koczan & Plekhanov (2024) — "Unearthing the Impact of Earthquakes"
- **Journal:** Journal of Policy Analysis and Management
- **DOI:** 10.1002/pam.22642
- **Also:** EBRD Working Paper 293; IZA Discussion Paper 17108
- **Method:** Comprehensive review synthesizing ~80 large earthquakes across 30+ countries
- **Key findings on cascading effects:**
  - **GDP:** Overall effect on GDP per capita is generally small due to reconstruction stimulus
  - **Fiscal accounts:** Impact can be substantial, varying significantly between economies
  - **Trade:** External trade balances weaken; considerable decrease in exports, ambiguous effect on imports
  - **Supply chains:** Shocks propagate and amplify through supply chains, affecting direct and indirect suppliers/customers
  - **Social capital:** Critical for post-disaster resilience; seismically active areas benefit disproportionately from high social capital
  - **Relocation:** Forced relocation separates families and disrupts social structure
- **Moderating factors:** Wealthier, more open economies with well-developed financial markets and strong institutions show greater ability to absorb impacts

#### Botzen, Deschenes & Sanders (2019) — "The Economic Impacts of Natural Disasters: A Review"
- **Journal:** Review of Environmental Economics and Policy, Vol. 13(2)
- **DOI:** 10.1093/reep/rez004
- **Key contribution:** Distinguishes between asset destruction (immediate) and flow losses (ongoing disruption to economic activity). The latter are much harder to measure but often larger.

### 4.2 Cascading Pathways

The research identifies several cascading pathways from earthquakes:

```
Earthquake
├── Infrastructure destruction
│   ├── Housing loss -> Displacement -> Social disruption
│   ├── Transportation damage -> Supply chain disruption -> Economic contraction
│   └── Hospital/school damage -> Health/education service gaps
├── Economic disruption
│   ├── Business destruction -> Unemployment -> Poverty
│   ├── Agricultural land damage -> Food insecurity
│   └── Insurance payouts / fiscal strain -> Government budget reallocation
├── Psychological trauma
│   ├── PTSD -> Reduced productivity
│   └── Community cohesion breakdown
└── Secondary hazards
    ├── Tsunamis, landslides, fires
    └── Nuclear incidents (Fukushima 2011)
```

### 4.3 Lag Structures

| Phase | Timing | Key Effects |
|-------|--------|-------------|
| Immediate (acute) | 0-30 days | Mortality, injury, displacement, infrastructure damage |
| Short-term | 1-6 months | Economic contraction, supply chain disruption, disease risk |
| Medium-term | 6 months - 2 years | Reconstruction stimulus, migration decisions, fiscal strain |
| Long-term | 2-10 years | GDP recovery (or not), institutional change, demographic shifts |

### 4.4 Nighttime Lights as Proxy for Recovery

- Satellite nighttime lights (VIIRS/DMSP) provide a spatially granular proxy for economic activity post-disaster
- Night-light-based GDP estimates often show faster economic deterioration during crisis than official data, but also stronger bounce-back
- In emerging markets, a 1% change in quarterly GDP is associated with ~1.55% change in nightlight intensity
- DMSP data can overestimate negative impacts by >50% compared to VIIRS due to lower resolution and saturation issues
- **Relevant datasets:** VIIRS Day/Night Band (2012-present), DMSP-OLS (1992-2013)

---

## 5. Commodity Price Shocks -> Political Instability

### 5.1 Food Prices and Social Unrest

#### Lagi, Bertrand & Bar-Yam (2011) — "The Food Crises and Political Instability in North Africa and the Middle East"
- **Institution:** New England Complex Systems Institute (NECSI)
- **arXiv:** 1108.2455
- **Datasets:** FAO Food Price Index, global food riot event data
- **Key findings:**
  - Identified a specific food price threshold: when the FAO Food Price Index rises above 210, riots become significantly more likely
  - Timing of violent protests in MENA in 2011 and earlier riots in 2008 coincides precisely with global food price peaks
  - The paper was sent to the US government four days before the Arab Spring began in Tunisia
- **Mechanism:** In 2010, droughts in Russia, Ukraine, China, and Argentina plus storms in Canada, Australia, and Brazil reduced global crop output, bumping the food price index up 32% in the second half of 2010
- **Lag structure:** Near-simultaneous (weeks to months) once threshold is crossed

#### Lagi, Bar-Yam et al. (2015) — Food Price Model
- **Journal:** PNAS, Vol. 112(20)
- **DOI:** 10.1073/pnas.1413108112
- **Key contribution:** Developed an accurate market price formation model incorporating both supply-demand fundamentals and trend-following (speculation), showing that ethanol conversion mandates and financial speculation amplified food price spikes

#### Bellemare (2015) — "Rising Food Prices, Food Price Volatility, and Social Unrest"
- **Journal:** American Journal of Agricultural Economics, Vol. 97(1), pp. 1-21
- **Key findings:**
  - Higher food price levels (not just volatility) are associated with increased social unrest
  - Uses instrumental variable approach to address endogeneity
  - Effect is stronger in countries with higher food expenditure shares

### 5.2 The Arab Spring Case

- **Preconditions:** MENA countries highly dependent on wheat imports (Egypt imported ~60% of wheat)
- **Trigger:** Global food price spike in 2010-2011 (FAO index exceeded 230)
- **Climate drivers:** Russian heat wave and drought (2010), Australian floods, Chinese drought
- **Causal chain:** Climate extremes in exporting countries -> crop failure -> export restrictions (Russia banned wheat exports) -> global price spike -> import-dependent countries face sudden food cost increase -> protests -> regime change
- **Lag:** Climate event to protest: approximately 3-6 months
- **Caveat:** The protests were triggered by food prices but evolved due to deeper political, socioeconomic, and diplomatic failures built up over decades. Only 2 of 8 affected countries experienced civil war.

### 5.3 Oil Price Shocks and Petrostates

#### Oil Price Drops and Instability
- **Key finding (multiple studies):** Prolonged low oil price periods correlate with increased instability in petrostates and risk of becoming fragile states
- **Mechanism:** Petrostates maintain domestic stability using petrodollars to fund social programs and security apparatus; when revenue drops, this social contract breaks down

#### Colgan (2013) — "Petro-Aggression"
- **Key finding:** States that are "petro-revolutionary" (both oil income and revolutionary leaders) instigate international conflicts at 3.5x the rate of comparable "typical" states
- **Dataset:** MID (Militarized Interstate Disputes)

#### Bruckner & Ciccone (2010) — "International Commodity Prices, Growth, and Civil War in Sub-Saharan Africa"
- **Journal:** Economic Journal, Vol. 120(544)
- **Key finding:** A 2018 study in the Economic Journal found that oil price shocks promote coups in onshore-intensive oil countries while preventing them in offshore-intensive oil countries (different distributional effects)

### 5.4 Lag Structures

| Price Shock Type | Lag to Instability | Mechanism |
|-----------------|-------------------|-----------|
| Food price spike | Weeks to months | Direct affordability crisis |
| Sustained high food prices | 3-12 months | Erosion of purchasing power |
| Oil price crash (petrostate) | 6-24 months | Fiscal contraction, reduced social spending |
| Oil price spike (importers) | 3-12 months | Current account deterioration, inflation |

---

## 6. Disease Outbreaks -> Economic and Social Impacts

### 6.1 The West African Ebola Outbreak (2014-2016)

#### Huber, Finelli & Stevens (2018) — "The Economic and Social Burden of the 2014 Ebola Outbreak"
- **Journal:** Journal of Infectious Diseases, Vol. 218(Suppl. 5), pp. S698-S704
- **Key findings:**
  - Economic burden estimates range from $2.8 to $32.6 billion in lost GDP
  - Knocked more than $2 billion off the GDPs of Guinea, Liberia, and Sierra Leone combined
  - **Behavioral effects were 80-90% of total economic impact** — fear of contagion, not direct illness, drove most economic losses
  - Mechanisms: loss of worker income, movement restrictions, reduced agricultural production, cross-border trade collapse
  - Rice prices jumped 30% in affected regions of Sierra Leone

#### Health System Collapse and Indirect Mortality
- **PMC:** PMC9759305 (Impacts of Ebola disease outbreak review, 2022)
- **Key findings:**
  - Health service delivery for non-Ebola conditions reduced by ~50%
  - In Sierra Leone: ~3,600 additional maternal, neonatal, and stillbirth deaths in 2014-15 attributable to health system disruption
  - Estimated 3.5 million untreated cases of malaria due to diverted health resources
  - Additional deaths from HIV/AIDS and tuberculosis due to interrupted treatment
- **Critical insight:** Indirect mortality effects were comparable in magnitude to direct Ebola mortality
- **Lag structure:** Health system effects immediate; economic recovery took 2-4 years; some institutional effects persist

### 6.2 COVID-19 Cascading Effects

#### GDP and Economic Impact
- Global GDP declined by approximately 3.1% in 2020 (IMF estimate)
- Individual country studies found GDP declines ranging from 2.3% to 8%+ depending on lockdown severity
- Supply disruptions subtracted 0.5-1.2% from global value added during 2021 recovery
- Supply disruptions added ~1% to global core inflation

#### Supply Chain Cascading Effects
- **Systematic review (PLOS ONE, 2021):** Analyzed 95 studies on COVID-19 supply chain impacts
  - Identified supply risks, demand risks, and financial risks as interconnected cascading categories
  - Government interventions (travel restrictions, factory shutdowns, mandatory confinement) led to labor shortages, raw material shortages, and logistics system failures
  - Key finding: Liberal Market Economies (LMEs) were more responsive to disease outbreak impacts than Coordinated Market Economies (CMEs), where government involvement moderated effects

#### Cascading Pathway
```
Disease outbreak
├── Direct health impact
│   ├── Illness and death -> Labor supply reduction
│   └── Healthcare system strain -> Non-COVID excess mortality
├── Behavioral response (fear)
│   ├── Reduced consumption -> Demand shock
│   ├── Reduced mobility -> Service sector collapse
│   └── Stockpiling -> Supply distortions
├── Policy response (lockdowns)
│   ├── Business closures -> Unemployment spike
│   ├── Travel restrictions -> Tourism collapse
│   ├── School closures -> Human capital loss
│   └── Border closures -> Trade disruption
└── Macro-financial
    ├── Fiscal stimulus -> Government debt
    ├── Supply chain disruption -> Inflation
    └── Uncertainty -> Investment decline
```

### 6.3 Cholera, Measles, and Endemic Disease Cascades

- Cholera outbreaks are strongly linked to water quality and sanitation infrastructure, which are in turn linked to urbanization patterns and climate (flooding/drought)
- Measles outbreaks following health system disruption (Ebola, conflict) demonstrate how one crisis creates vulnerability to another
- These cascading chains are particularly relevant for Causal Atlas because they connect climate, infrastructure, disease, and economic domains

### 6.4 Lag Structures

| Disease Impact | Lag | Effect Size |
|---------------|-----|-------------|
| Direct mortality | Days to weeks | Immediate |
| Health system disruption | Weeks to months | 50% reduction in non-outbreak services |
| Behavioral economic impact | Days to months | 80-90% of total economic cost |
| GDP recovery | 1-3 years | Variable by country income/institutions |
| Educational disruption | Years to decades | Difficult to quantify |
| Institutional change | Years | Can be positive (improved preparedness) or negative |

---

## 7. Deforestation -> Climate -> Food Security

### 7.1 The Cyclical Chain

This pathway is notable because it is reciprocal and cyclical:

```
Deforestation -> Greenhouse gas emissions (~20% of global CO2)
                    |
                    v
            Climate change (temperature rise, altered precipitation)
                    |
                    v
        Reduced agricultural productivity
                    |
                    v
    Pressure to expand agricultural land -> MORE deforestation
```

### 7.2 Key Research

#### IPCC Special Report on Climate Change and Land (2019) — Chapter 5: Food Security
- **URL:** https://www.ipcc.ch/srccl/chapter/chapter-5/
- **Key findings:**
  - Climate change has already affected food security through weather events (drought, flooding, heat waves)
  - Effects include reduced soil fertility, disrupted rain patterns, pollinator decline
  - Over time: higher food prices, reduced food availability, increased hunger, particularly in agriculture-dependent areas
  - The report documents both slow-onset and acute pathways

#### Curtis et al. (2018) — "Classifying Drivers of Global Forest Loss"
- **Journal:** Science, Vol. 361(6407)
- **Key finding:** ~73% of tropical forest loss is driven by agriculture (both commercial and subsistence)
- **Significance:** Establishes agriculture as the dominant deforestation driver, completing one side of the cycle

#### Scientific Reports (2024) — "Analysis of Food System Drivers of Deforestation"
- **DOI:** 10.1038/s41598-024-65397-3
- **Key finding:** ~90% of global forest cover changes between 2000-2018 were attributable to agricultural expansion
- **Additional drivers:** Foreign direct investment and urbanization identified as threats to tropical forests

#### Alkama & Cescatti (2016) — "Biophysical Climate Impacts of Recent Changes in Global Forest Cover"
- **Journal:** Science
- **Key finding:** Deforestation causes local warming of 0.3-0.8degC through changes in albedo, evapotranspiration, and surface roughness, beyond the greenhouse gas effect

### 7.3 Key Datasets for This Chain

- **Deforestation:** Global Forest Watch / Hansen et al. tree cover loss, PRODES (Brazil), JRC Tropical Moist Forest
- **Climate:** ERA5, CHIRPS, CRU TS
- **Food security:** FAO crop production, IPC food security classifications, FEWS NET
- **Carbon emissions:** Global Carbon Project, EDGAR

### 7.4 Lag Structures

| Link in Chain | Lag | Notes |
|--------------|-----|-------|
| Deforestation -> Local climate effect | 1-5 years | Biophysical effects (temperature, rainfall) |
| Deforestation -> Global CO2 contribution | Decades | Carbon cycle timescale |
| Climate change -> Crop yield reduction | Variable | Acute events: same season; Trends: years to decades |
| Crop failure -> Food insecurity | 3-12 months | Market transmission |
| Food insecurity -> Agricultural expansion | 1-10 years | Policy and economic response |

---

## 8. Urbanization -> Pollution -> Health

### 8.1 Key Reviews

#### Neiderud (2015) — "How Urbanization Affects the Epidemiology of Emerging Infectious Diseases"
- **Journal:** Infection Ecology & Epidemiology, Vol. 5
- **Key finding:** Rapid urbanization creates conditions for disease emergence through crowding, poor sanitation, and proximity to animal reservoirs

#### Rathore & Agrawal (2022) — Systematic Review of Urbanization and Health in Developing Countries
- **PubMed:** 24702762 (Vlahov et al., 2007 review also relevant)
- **Key findings:**
  - Urbanization is associated with lower undernutrition risk but higher overweight risk
  - Lower total fertility rates in urban areas
  - Common risk factors for chronic diseases more prevalent in urban areas
  - Association with life expectancy is positive but insignificant

#### Chen et al. (2023) — "How Does Urbanization Affect Public Health?"
- **Journal:** PMC, 175 countries worldwide
- **Key findings:**
  - Each percentage point increase in urbanization rate associated with 0.54 ug/m3 rise in PM2.5
  - Each 1 ug/m3 increase in PM2.5 leads to approximately 2.5 additional respiratory disease cases per 1,000 population
  - Air pollution undermines the positive impacts of urbanization on health
- **Statistical method:** Panel data analysis with instrumental variables

#### Landrigan et al. (2018) — The Lancet Commission on Pollution and Health
- **Journal:** The Lancet, Vol. 391(10119)
- **Key findings:**
  - Pollution responsible for 9 million premature deaths per year (16% of all deaths worldwide)
  - The largest pollution-related disease burdens are in low- and middle-income countries undergoing rapid industrialization
  - Pollution disproportionately affects the poor and marginalized

### 8.2 Causal Pathway

```
Urbanization (population growth + rural-urban migration)
├── Industrial development -> Industrial emissions
├── Vehicle density increase -> Transport emissions
├── Construction activity -> Particulate matter
├── Energy demand increase -> Power plant emissions
├── Waste generation increase -> Waste burning, landfill emissions
└── Infrastructure gap -> Unsafe water, poor sanitation
         |
         v
Pollution exposure (air, water, soil)
         |
         v
Health outcomes
├── Respiratory disease (COPD, asthma, lung cancer)
├── Cardiovascular disease
├── Waterborne disease (cholera, typhoid)
├── Cognitive impairment (lead, mercury)
├── Cancer clusters
└── Mental health effects
```

### 8.3 Effect Sizes and Spatial Patterns

| Urbanization Metric | Pollution Outcome | Health Effect | Lag |
|-------------------|-------------------|---------------|-----|
| +1% urbanization rate | +0.54 ug/m3 PM2.5 | +2.5 respiratory cases per 1,000 | 1-5 years |
| Industrial zone proximity | PM2.5 10-50 ug/m3 above background | 7-15% increase in all-cause mortality | Chronic (years) |
| Traffic density | NO2, PM2.5 near roads | Asthma prevalence 1.5-2x in adjacent blocks | 1-5 years |
| Unsafe water access | Waterborne pathogens | Diarrheal disease, cholera outbreaks | Days to weeks |

### 8.4 Key Datasets

- **Urbanization:** UN World Urbanization Prospects, Landscan population, GHS-SMOD settlement classification
- **Pollution:** OpenAQ (ground stations), Sentinel-5P (satellite NO2/SO2), NASA MODIS/VIIRS AOD for PM2.5
- **Health:** WHO Global Health Observatory, GBD (Global Burden of Disease), DHS surveys

---

## 9. Other Documented Multi-Domain Causal Chains

### 9.1 Water Scarcity -> Conflict

#### Ide, Rodriguez Lopez, Frohlich & Scheffran (2021) — "Pathways to Water Conflict During Drought in the MENA Region"
- **Journal:** Journal of Peace Research, Vol. 58(3)
- **DOI:** 10.1177/0022343320910777
- **Method:** Qualitative Comparative Analysis (QCA) integrating quantitative and qualitative data; 34 cases (17 with conflict onset)
- **Key findings:**
  - No direct causal link established between water scarcity and conflict
  - Escalation depends on pre-existing negative socio-political relationships and political system types
  - Water-related conflicts quadrupled between 2012-2022 compared to 2000-2011, mainly in MENA
- **Significance for Causal Atlas:** Demonstrates that mediating variables (governance quality, group relations) are essential to include in causal models

#### Nkiaka et al. (2024) — Water Footprint and Conflict in the Sahel
- **Journal:** Earth's Future (AGU)
- **DOI:** 10.1029/2023EF004013
- **Innovation:** Uses water footprint concept to link water scarcity to violent conflicts in the Sahel and Lake Chad Basin

### 9.2 Climate Tipping Points and Cascading Risks

#### Armstrong McKay et al. (2022) — "Exceeding 1.5degC Could Trigger Multiple Climate Tipping Points"
- **Journal:** Science, Vol. 377(6611)
- **DOI:** 10.1126/science.abn7950
- **Key findings:**
  - Even at 1.5degC warming, five tipping points are possible (including West Antarctic ice sheet collapse, Greenland ice sheet loss, boreal permafrost thaw)
  - Tipping elements interact: passing one makes triggering others more likely
  - Arctic sea ice retreat -> Greenland ice sheet melt -> AMOC weakening -> Amazon rainforest dieback (potential cascade)
- **Lag structure:** Decades to centuries for physical climate tipping points; years to decades for socioecological tipping points

#### Wunderling et al. (2024) — "Climate Tipping Point Interactions and Cascades: A Review"
- **Journal:** Earth System Dynamics, Vol. 15, pp. 41-
- **Key contribution:** Systematic review of tipping point interactions, including both catastrophic and potentially positive cascades (e.g., rapid decarbonization triggering cascading technology adoption)

### 9.3 Conflict -> Environmental Degradation

The reverse pathway is also documented:

- Armed conflict causes deforestation (e.g., DRC, Colombia), water contamination, and wildlife destruction
- Post-conflict reconstruction often prioritizes economic recovery over environmental protection
- Landmines and unexploded ordnance contaminate agricultural land for decades
- Key study: Hanson et al. (2009), "Warfare in Biodiversity Hotspots" (Conservation Biology)

### 9.4 Temperature -> Labor Productivity -> Economic Output

#### Dell, Jones & Olken (2012) — "Temperature Shocks and Economic Growth"
- **Journal:** American Economic Journal: Macroeconomics, Vol. 4(3), pp. 66-95
- **DOI:** 10.1257/mac.4.3.66
- **Method:** Panel data with country fixed effects, using historical temperature fluctuations within countries
- **Key findings:**
  - Higher temperatures substantially reduce economic growth in poor countries
  - Higher temperatures may reduce growth *rates* (not just output levels), implying persistent effects
  - Wide-ranging effects: reduces agricultural output, industrial output, *and* political stability
- **Lag structure:** Lagged effects examined over 1-3, 1-5, and 1-7 year windows
- **Datasets:** CRU temperature, Penn World Tables GDP, Polity IV political stability
- **Effect size:** A 1degC increase in average temperature reduces growth by ~1.3 percentage points in poor countries

#### Burke, Hsiang & Miguel (2015) — "Global Non-linear Effect of Temperature on Economic Production"
- **Journal:** Nature, Vol. 527, pp. 235-239
- **Key finding:** Global economic production peaks at an annual average temperature of 13degC; both hotter and colder temperatures reduce output. This implies that warming will widen the gap between rich (temperate) and poor (tropical) countries.

### 9.5 El Nino/La Nina -> Multi-Domain Cascades

El Nino events create cascading impacts across multiple domains simultaneously:

- **Agriculture:** Drought in Australia/Southeast Asia, floods in South America -> crop failures
- **Fisheries:** Collapse of Peruvian anchovy catch -> fishmeal price spike
- **Disease:** Increased malaria, dengue, cholera in affected regions (documented lag of 2-6 months)
- **Conflict:** Some evidence of increased conflict in El Nino years (Hsiang et al. 2011, Nature)
- **Key study:** Hsiang, Meng & Cane (2011), "Civil Conflicts Are Associated with the Global Climate" (Nature, Vol. 476)
  - Found the risk of civil conflict across tropics doubles during El Nino years compared to La Nina years
  - Effect size: 3% annual conflict risk in La Nina vs. 6% in El Nino
  - **Lag:** Contemporaneous to 1-year lag

### 9.6 Mining/Extraction -> Environmental Contamination -> Health -> Economic Loss

- Heavy metal contamination from mining (mercury from artisanal gold mining, arsenic from copper mining)
- Water contamination pathways documented in Peru, Ghana, DRC
- Health effects include neurological damage, kidney disease, cancer
- Economic effects through reduced labor productivity and healthcare costs
- Lag structures: years to decades for chronic health effects

---

## 10. Cross-Cutting Methodological Insights

### 10.1 Statistical Methods Used Across Studies

| Method | Strengths | Weaknesses | Best Used For |
|--------|-----------|------------|---------------|
| **Granger causality** | Simple, well-understood; handles autocorrelation well | Assumes linearity; only detects predictive, not true causality; pairwise | Time series with clear temporal precedence |
| **Panel fixed effects** | Controls for time-invariant unobservables; large-N | Cannot identify non-linear relationships; relies on within-unit variation | Cross-country/cross-cell studies |
| **Instrumental variables** | Addresses endogeneity | Requires valid instruments (hard to find) | When confounding is severe |
| **PCMCI** (Runge et al. 2019) | Handles high-dimensional time series; controls for autocorrelation; nonlinear variants available | Computationally intensive; requires stationarity assumption | Multivariate causal discovery in spatiotemporal data |
| **Convergent Cross-Mapping** | Captures nonlinear coupling; works for weakly coupled systems | Requires long time series; sensitive to noise | Nonlinear dynamical systems |
| **Transfer entropy** | Information-theoretic; no linearity assumption | Computationally expensive; requires large samples | Directed information flow |
| **Spatial lag/error models** | Accounts for spatial dependence | Assumes specific spatial weight matrix | Spatially correlated data |
| **Difference-in-differences** | Clean causal identification with natural experiments | Requires parallel trends assumption | Before/after policy or event studies |
| **Qualitative Comparative Analysis (QCA)** | Identifies necessary/sufficient conditions; handles complex causality | Sensitive to case selection and calibration | When multiple pathways lead to outcome |

### 10.2 PCMCI: Most Relevant Method for Causal Atlas

PCMCI (Peter and Clark Momentary Conditional Independence) is particularly relevant for the Causal Atlas project:

- **Reference:** Runge, Nowack, Kretschmer, Flaxman & Sejnoweth (2019), "Detecting and quantifying causal associations in large nonlinear time series datasets," Science Advances, Vol. 5(11), eaau4996
- **Implementation:** Tigramite Python package (https://github.com/jakobrunge/tigramite)
- **How it works:**
  1. PC1 condition selection to identify relevant conditions
  2. Momentary Conditional Independence (MCI) test to establish causal links
- **Spatial extension:** Mapped-PCMCI reconstructs a lower-dimensional spatial representation, conducts causal discovery, then maps relations back to grid level
- **Advantages for our use case:**
  - Designed for high-dimensional time series (multiple variables per grid cell)
  - Handles autocorrelation (critical for climate data)
  - Can detect time-lagged causal dependencies
  - Nonlinear variants available (GPDC, CMIknn)
  - Already widely used in climate research

### 10.3 Common Pitfalls in Cross-Domain Causal Analysis

1. **Ecological fallacy:** Relationships observed at aggregate level may not hold at individual level
2. **Omitted variable bias:** Cross-domain chains almost always have confounders
3. **Endogeneity:** Many relationships are bidirectional (conflict -> food insecurity -> conflict)
4. **Publication bias:** Positive findings (significant effects) are more likely to be published
5. **Spatial and temporal scale sensitivity:** Results can change dramatically with different aggregation choices
6. **Simpson's paradox:** Aggregated trends can reverse at disaggregated levels

---

## 11. Implications for Causal Atlas

### 11.1 Which Causal Chains to Prioritize

Based on the evidence strength, data availability, and relevance to our spatiotemporal grid approach:

| Chain | Evidence Strength | Data Availability | Grid Compatibility | Priority |
|-------|------------------|-------------------|-------------------|----------|
| Climate -> Food prices -> Conflict | Strong | Excellent (CHIRPS, ACLED, WFP) | High (PRIO-GRID proven) | **Highest** |
| PM2.5 -> Respiratory mortality | Very strong | Good (OpenAQ, satellite, WHO) | High | **High** |
| Food price spikes -> Unrest | Strong | Good (FAO, ACLED) | Medium (national prices) | **High** |
| Climate -> Migration | Moderate | Fair (limited spatial migration data) | Medium | Medium |
| Earthquake -> Economic disruption | Strong | Good (USGS, nightlights) | High | Medium |
| Disease -> Economic cascade | Strong | Fair (WHO, World Bank) | Medium | Medium |
| Lead -> Crime | Very strong but historical | Limited ongoing data | Low | Low |

### 11.2 Recommended Lag Windows to Test

Based on the literature review, the Causal Atlas system should test the following lag windows:

- **Short (0-3 months):** Acute climate events -> conflict, price shocks -> unrest, pollution -> acute health
- **Medium (3-12 months):** Growing season drought -> conflict, food production -> prices, disease -> economic
- **Long (1-5 years):** Climate trends -> migration, urbanization -> pollution -> health, economic disruption -> recovery
- **Very long (5-25 years):** Lead exposure -> crime, deforestation -> climate feedback, tipping point cascades

### 11.3 Key Variables to Include in Grid Cells

From the literature, the following variables at grid-cell level are most frequently used and most informative:

- **Climate:** Temperature anomaly, precipitation anomaly, SPEI drought index, growing season conditions
- **Vegetation:** NDVI (vegetation health proxy for agricultural production)
- **Conflict:** Event count (ACLED/UCDP-GED), fatalities, event type
- **Economic:** Nighttime light intensity (proxy for economic activity), food prices (nearest market)
- **Pollution:** PM2.5 (satellite-derived or ground station), NO2
- **Health:** Disease incidence where available
- **Population:** Population density, urbanization level
- **Context:** Agricultural dependence, political exclusion, governance quality (typically at admin-1 or national level)

### 11.4 Methodological Recommendations

1. **Start with PCMCI** on monthly time series at the PRIO-GRID level for the climate-conflict chain, as this has the most validation in the literature
2. **Use Granger causality** as a simpler baseline for comparison
3. **Always test multiple lag windows** (the literature shows results are highly sensitive to lag choice)
4. **Include contextual moderators** (agricultural dependence, income level, governance) as the von Uexkull et al. (2016) and Cattaneo & Peri (2016) studies show these dramatically change results
5. **Validate against known findings** (e.g., El Nino -> conflict doubling in tropics) before exploring novel chains
6. **Account for spatial spillovers** (Harari & La Ferrara 2018 show conflict spreads to neighboring cells)

---

## References (Selected Key Papers by Chain)

### Chain 1: Climate -> Food -> Conflict
- Burke, M., Hsiang, S.M., & Miguel, E. (2015). Climate and Conflict. *Annual Review of Economics*, 7, 577-617.
- Hsiang, S.M., Burke, M., & Miguel, E. (2013). Quantifying the influence of climate on human conflict. *Science*, 341(6151), 1235367.
- Harari, M. & La Ferrara, E. (2018). Conflict, Climate, and Cells: A Disaggregated Analysis. *Review of Economics and Statistics*, 100(4), 594-608.
- von Uexkull, N., Croicu, M., Fjelde, H., & Buhaug, H. (2016). Civil conflict sensitivity to growing-season drought. *PNAS*, 113(44), 12391-12396.
- Hendrix, C.S. & Salehyan, I. (2012). Climate change, rainfall, and social conflict in Africa. *Journal of Peace Research*, 49(1), 35-50.
- Kelley, C.P. et al. (2015). Climate change in the Fertile Crescent and implications of the recent Syrian drought. *PNAS*, 112(11), 3241-3246.
- Mach, K.J. et al. (2019). Climate as a risk factor for armed conflict. *Nature*, 571, 193-197.
- Zhang, D.D. et al. (2007). Global climate change, war, and population decline in recent human history. *PNAS*, 104(49), 19214-19219.

### Chain 2: Climate -> Migration
- Cattaneo, C. & Peri, G. (2016). The migration response to increasing temperatures. *Journal of Development Economics*, 122, 127-146.
- Rigaud, K.K. et al. (2018). *Groundswell: Preparing for Internal Climate Migration*. World Bank.
- Hoffmann, R. et al. (2020). A meta-analysis of country-level studies on environmental change and migration. *Nature Climate Change*, 10, 904-912.

### Chain 3: Pollution -> Health
- Di, Q. et al. (2017). Air quality and mortality in the Medicare population. *New England Journal of Medicine*, 376, 2513-2522.
- Reyes, J.W. (2007). Environmental policy as social policy? The impact of childhood lead exposure on crime. *B.E. Journal of Economic Analysis & Policy*, 7(1).
- Nevin, R. (2007). Understanding international crime trends: the legacy of preschool lead exposure. *Environmental Research*, 104(3), 315-336.
- Landrigan, P.J. et al. (2018). The Lancet Commission on pollution and health. *The Lancet*, 391(10119).

### Chain 4: Earthquake -> Economic/Social
- Aksoy, C.G. et al. (2024). Unearthing the impact of earthquakes: A review of economic and social consequences. *Journal of Policy Analysis and Management*.
- Botzen, W.J.W., Deschenes, O., & Sanders, M. (2019). The economic impacts of natural disasters: A review. *Review of Environmental Economics and Policy*, 13(2).

### Chain 5: Commodity Prices -> Instability
- Lagi, M., Bertrand, K.Z., & Bar-Yam, Y. (2011). The food crises and political instability in North Africa and the Middle East. *arXiv:1108.2455*.
- Bellemare, M.F. (2015). Rising food prices, food price volatility, and social unrest. *American Journal of Agricultural Economics*, 97(1), 1-21.

### Chain 6: Disease -> Economic/Social
- Huber, C., Finelli, L., & Stevens, W. (2018). The economic and social burden of the 2014 Ebola outbreak in West Africa. *Journal of Infectious Diseases*, 218(Suppl. 5), S698-S704.

### Chain 7: Deforestation -> Climate -> Food
- IPCC (2019). Special Report on Climate Change and Land, Chapter 5: Food Security.
- Curtis, P.G. et al. (2018). Classifying drivers of global forest loss. *Science*, 361(6407).

### Chain 8: Urbanization -> Pollution -> Health
- Chen et al. (2023). How does urbanization affect public health? *PMC*.
- Landrigan, P.J. et al. (2018). The Lancet Commission on pollution and health. *The Lancet*, 391(10119).

### Cross-Domain Methods
- Runge, J. et al. (2019). Detecting and quantifying causal associations in large nonlinear time series datasets. *Science Advances*, 5(11), eaau4996.
- Dell, M., Jones, B.F., & Olken, B.A. (2012). Temperature shocks and economic growth. *American Economic Journal: Macroeconomics*, 4(3), 66-95.
- Burke, M., Hsiang, S.M., & Miguel, E. (2015). Global non-linear effect of temperature on economic production. *Nature*, 527, 235-239.
