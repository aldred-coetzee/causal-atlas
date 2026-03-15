# Cross-Domain Causal Chains: Published Research Review

> **Last updated:** March 2026
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
10. [Water Scarcity to Conflict](#10-water-scarcity--conflict)
11. [Night Lights to Economic Activity to Political Stability](#11-night-lights--economic-activity--political-stability)
12. [Land Degradation to Food Insecurity to Migration to Urban Stress to Conflict](#12-land-degradation--food-insecurity--migration--urban-stress--conflict)
13. [Mining/Resource Extraction to Pollution to Health to Social Unrest](#13-miningresource-extraction--pollution--health--social-unrest)
14. [Temperature to Labor Productivity to Economic Output to Social Stress](#14-temperature--labor-productivity--economic-output--social-stress)
15. [Sea Level Rise to Saltwater Intrusion to Agricultural Loss to Displacement](#15-sea-level-rise--saltwater-intrusion--agricultural-loss--displacement)
16. [Pandemic to Supply Chain Disruption to Food Price Shock to Unrest](#16-pandemic--supply-chain-disruption--food-price-shock--unrest)
17. [Social Media / Information Cascades to Protest Mobilization](#17-social-media--information-cascades--protest-mobilization)
18. [El Nino/La Nina to Multi-Domain Cascading Effects](#18-el-ninola-nina--multi-domain-cascading-effects)
19. [Volcanic Eruptions to Climate Forcing to Agricultural Disruption](#19-volcanic-eruptions--climate-forcing--agricultural-disruption)
20. [Causal Chain Atlas: Master Reference Table](#20-causal-chain-atlas-master-reference-table)
21. [Novel and Emerging Pathways](#21-novel-and-emerging-pathways)
22. [Cross-Cutting Methodological Insights](#22-cross-cutting-methodological-insights)
23. [Implications for Causal Atlas](#23-implications-for-causal-atlas)

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

### 1.8 IPCC AR6 WGII Chapter 16 — Key Risks Assessment (2022)

The IPCC Sixth Assessment Report, Working Group II (2022), Chapter 16: "Key Risks across Sectors and Regions" provides the most authoritative assessment of climate-conflict linkages to date.

- **URL:** https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-16/
- **Key findings with confidence levels:**
  - Climate increases conflict risk by undermining food and water security, income and livelihoods in situations where there are large populations, weather-sensitive economic activities, weak institutions and high levels of poverty and inequality (**high confidence**)
  - In urban areas, food and water insecurity and inequitable access to services has been associated with civil unrest where there are weak institutions (**medium confidence**)
  - Climate hazards are associated with increased violence against women, girls and vulnerable groups, and the experience of armed conflict is gendered (**medium confidence**)
  - Adaptation and mitigation projects implemented without consideration of local social dynamics have exacerbated non-violent conflict (**medium confidence**)
- **Advancement over AR5:** AR6 is considerably more confident than the Fifth Assessment Report (2014), reflecting the growth of the empirical literature. AR5 found "low confidence" in direct climate-conflict links; AR6 elevated this to "high confidence" for the indirect pathways through food/water/livelihoods
- **Significance for Causal Atlas:** The IPCC's distinction between direct and indirect pathways, and between different confidence levels for different mechanisms, provides a roadmap for which causal chains have the strongest evidence base

### 1.9 Mach et al. (2019) — Expert Elicitation Deep Dive

#### Methodology
- **Journal:** Nature, Vol. 571, pp. 193-197
- **DOI:** 10.1038/s41586-019-1300-6
- **Approach:** Structured expert elicitation — a formal methodology used when evidence is contested or incomplete. Individual day-long interviews were conducted with each of 11 experts from diverse disciplines (political science, economics, environmental science, peace/conflict studies), followed by a two-day group deliberation
- **Experts included:** Leading scholars from both "climate matters" and "climate is overstated" camps, ensuring balanced representation
- **Process:** Produced 950 pages of transcripts analyzed for convergence and divergence of expert opinion. Each expert provided quantitative estimates of climate's contribution to conflict risk with uncertainty ranges
- **Innovation:** The method does not aim for "definitive answers" but rather to quantify uncertainty and highlight areas of expert agreement and disagreement

#### Detailed Findings
- **Historical attribution:** Experts agreed that **3-20% of organized armed conflict risk** over the past century has been influenced by climate variability and change (interquartile range across experts)
- **Ranking of drivers:** Other drivers were judged substantially more influential:
  - Low socioeconomic development: **most influential**
  - Low state capacity: **very influential**
  - Intergroup inequality: **very influential**
  - Recent history of violent conflict: **very influential**
  - Climate variability/change: **modest but real influence**, particularly when interacting with other drivers
- **Future projections:** Under 2degC warming, experts estimated climate's influence on conflict risk would approximately double. Under 4degC warming, the increase could be five-fold or more
- **Mechanisms:** The experts identified food insecurity, economic shocks, and livelihood disruption as the most plausible causal mechanisms linking climate to conflict, with less agreement on migration as a pathway
- **Significance:** This study is widely cited as providing the most careful, uncertainty-aware assessment that avoids both alarmism and dismissal. It established the "3-20%" range as a consensus benchmark

### 1.10 Koubi (2019) — Annual Review of Political Science

- **Reference:** Koubi, V. (2019). "Climate Change and Conflict." *Annual Review of Political Science*, 22, 343-360
- **DOI:** 10.1146/annurev-polisci-050317-070830
- **Scope:** Comprehensive review of the quantitative and qualitative literatures on climate change and conflict
- **Key conclusions:**
  - The literature has **not detected a robust and general effect** linking climate to conflict onset
  - Substantial agreement exists that climatic changes contribute to conflict **under some conditions and through certain pathways**
  - The strongest evidence is for regions dependent on agriculture, in combination and interaction with socioeconomic and political factors such as low economic development, political marginalization, and ethnic fractionalization
  - Future research must investigate how climatic changes interact with and/or are conditioned by socioeconomic, political, and demographic settings
- **Important distinction:** Koubi differentiates between (a) temperature/precipitation effects on interpersonal violence (relatively strong evidence) and (b) effects on organized armed conflict (weaker, more contested evidence)
- **Relevance:** This review established the "conditional effects" framework as the dominant paradigm — climate affects conflict primarily through interaction with pre-existing vulnerabilities, not as a direct cause

### 1.11 Recent Key Papers (2020-2025)

#### Von Uexkull & Buhaug (2021) — "Security Implications of Climate Change: A Decade of Scientific Progress"
- **Journal:** Journal of Peace Research, Vol. 58(1), pp. 21-32
- **DOI:** 10.1177/0022343320984210
- **Key contribution:** Decade-in-review assessment noting that the research community has made important strides in specifying and evaluating plausible indirect causal pathways between climatic conditions and conflict outcomes
- **Finding:** Identifies remaining research gaps including the long-term implications of gradual climate change and the conflict potential of climate policy responses (e.g., renewable energy transitions creating new resource conflicts)

#### Von Uexkull & Buhaug (2021) — "Vicious Circles: Violence, Vulnerability, and Climate Change"
- **Journal:** Annual Review of Environment and Resources, Vol. 46, pp. 169-192
- **Key innovation:** Develops a unified conceptual model showing how conditions that shape vulnerability to climate change (poverty, inequality, weak governance) also increase the likelihood of climate-conflict interactions, and armed conflict impacts aggravate these conditions, creating a "vicious circle" trapping societies in cycles of violence, vulnerability, and climate impacts
- **Significance for Causal Atlas:** Suggests we need to model **feedback loops**, not just unidirectional causal chains

#### Ide (2023) — Climate-Conflict Pathways Review
- **Finding:** Growing research consensus that climate change and environmental stress factors increase the risk of violent conflict along **complex causal pathways**, but the relationship is **highly context-dependent**
- **Six main pathways identified:** (1) resource competition, (2) livelihood deterioration, (3) migration/displacement, (4) elite exploitation of grievances, (5) tactical considerations (e.g., fighting during dry season), (6) food price transmission

#### Nature Reviews Earth & Environment (2022) — "Climate Change and Conflict"
- **DOI:** 10.1038/s43017-022-00382-w
- **Key finding:** Distinguishes between four categories of climate-conflict relationships: (1) direct impacts of climate inaction (e.g., resource wars), (2) direct impacts of climate action (e.g., resistance against fossil fuel subsidy cuts), (3) indirect impacts of climate inaction (e.g., communal tensions over water), (4) indirect impacts of climate action (e.g., opposition to mining for renewable energy materials)

#### Adams et al. (2018) — Sampling Bias in Climate-Conflict Research
- **Journal:** Nature Climate Change, Vol. 8(3), pp. 200-203
- **Key finding:** Documented systematic sampling bias — scholars have disproportionately studied places already experiencing violence instead of studying non-violent adaptation to climate stress. Africa, Asia, and the Middle East receive disproportionate attention, particularly Kenya, Sudan, Israel/Palestine, and Colombia
- **Implication:** Effect sizes in the literature may be inflated due to selection on the dependent variable

#### Journal of Peace Research Special Issue (2021) — "Security Implications of Climate Change"
- **Guest editors:** Von Uexkull & Buhaug
- **Content:** 12 original research articles and viewpoint essays
- **Key contributions:**
  - Significant climate impacts on social unrest in urban settings
  - Complexity of the climate-migration-unrest link
  - Agricultural production patterns shape conflict risk
  - Understudied outcomes: interstate claims, individual trust
  - Gender dimensions of climate-conflict interactions

#### IMF Staff Climate Note (2023) — "Climate Challenges in Fragile and Conflict-Affected States"
- **Key finding:** Fragile and conflict-affected states suffer **more severe and persistent GDP losses** from climate shocks than other countries, and climate vulnerability and underlying fragilities exacerbate each other

### 1.12 Regional Meta-Analyses

#### Sub-Saharan Africa
- **Evidence strength:** Strongest of any region, partly due to research attention bias (Adams et al. 2018)
- **Key findings:**
  - Farmer-herder violence has increased substantially over the past decade due to growing land pressure (documented in Nigeria, Mali, Burkina Faso, Central African Republic)
  - Growing-season drought effects are strongest for agriculturally dependent, politically excluded ethnic groups (von Uexkull et al. 2016)
  - In the Sahel, the shrinking of Lake Chad has created resource competition exploited by extremist groups including Boko Haram
  - Vulnerability to climate change has both direct and indirect negative effects on internal conflict, with migration as a key transmission channel (Ofosu et al. 2023)
- **Effect sizes:** Climate shocks associated with approximately 10-14% increase in conflict incidence in agricultural regions (from multiple panel studies)
- **Caveat:** Political exclusion and governance quality are consistently stronger predictors than climate variables alone

#### South Asia
- **Key findings:**
  - Agricultural dependence makes the region highly vulnerable to climate-conflict pathways (monsoon disruption is critical)
  - Intra-regional geopolitical tensions over shared water resources (India-Pakistan over the Indus, India-Bangladesh over the Ganges) amplify climate stress
  - Myanmar's conflict has been exacerbated by climate impacts on agriculture, creating a compounding crisis (East Asia Forum, 2023)
  - Evidence is somewhat weaker than Sub-Saharan Africa, partly due to fewer cell-level studies using PRIO-GRID methodology
- **Effect sizes:** Less precisely quantified than Africa; most studies use national-level panel data

#### MENA (Middle East and North Africa)
- **Key findings:**
  - Temperatures have risen **twice as fast as the global average**, and rainfall has become scarcer and more unpredictable (IMF 2023)
  - Agriculture, fisheries, and livestock account for ~15% of livelihoods, making the region highly vulnerable to drought impacts
  - Shared transboundary water resources (Nile, Tigris-Euphrates, Jordan River) are significant sources of tension
  - Water-related conflicts quadrupled between 2012-2022 compared to 2000-2011, with the MENA region seeing the highest concentration of incidents (Ide et al. 2021)
  - The 2007-2010 Syrian drought case (Kelley et al. 2015) remains the most studied single-country example, though its interpretation remains contested (Selby et al. 2017)
- **Effect sizes:** Conflict risk is higher in areas where population depends on agriculture for livelihoods; the worsening livelihood mechanism shows consistent results across multiple studies

### 1.13 Growing Season vs. Harvest Season Distinction

A critical methodological insight from recent research is that the **timing** of climate shocks relative to agricultural calendars matters enormously:

- **Growing season shocks** (drought/heat during planting-to-harvest period):
  - Directly reduce crop yields
  - The strongest and most consistently documented pathway to conflict
  - Effects manifest in the same year or the following year
  - Harari & La Ferrara (2018) found that only growing-season shocks increase conflict; off-season weather anomalies have no effect
  - Von Uexkull et al. (2016) found drought during the growing season significantly increases conflict, but only for agriculturally dependent and politically excluded groups

- **Harvest season shocks** (disruptions during harvest period):
  - Can destroy crops already in the field, causing acute food loss
  - May affect post-harvest storage and food availability
  - Different transmission mechanism: reduces stored food rather than crop potential
  - Less studied in the climate-conflict literature

- **Off-season weather anomalies:**
  - Generally show no effect on conflict (Harari & La Ferrara 2018)
  - Important negative finding: suggests the agricultural productivity channel is critical, not a general "heat makes people aggressive" mechanism

- **Implications for Causal Atlas:** The system must incorporate **crop calendar data** at the grid-cell level (available from Sacks et al. 2010 crop calendar dataset and MIRCA2000) to correctly specify growing-season windows. Testing climate-conflict links without accounting for agricultural timing will produce attenuated or null results.

### 1.14 Quantified Effect Sizes and Confidence Intervals

| Study | Climate Variable | Conflict Measure | Effect Size | Notes |
|-------|-----------------|-----------------|-------------|-------|
| Hsiang et al. 2013 (meta-analysis) | +1sigma temperature | Intergroup conflict | +14% [+8%, +21%] | Pooled across 60 studies |
| Burke, Hsiang & Miguel 2015 (meta-analysis) | +1sigma temperature | Intergroup conflict | +11.3% [+5%, +18%] | Refined methodology |
| Burke, Hsiang & Miguel 2024 (updated meta) | +1sigma temperature | Intergroup conflict | Smaller than earlier estimates but significant | NBER WP 33040 |
| Harari & La Ferrara 2018 | Growing-season drought | UCDP-GED events in cell | +3-5 percentage points conflict incidence | PRIO-GRID cells, Africa |
| Von Uexkull et al. 2016 | SPEI drought index | Civil conflict | Significant for agri-dependent, politically excluded groups only | Interaction effects critical |
| Mach et al. 2019 (expert elicitation) | Climate overall | Organized armed conflict | 3-20% of risk attributable | Interquartile range across 11 experts |
| Recent meta-analysis (via Ide 2023) | Average expected change by 2050 | Group conflict | +4.9% to +9.8% | Pooled across 80 studies |
| Recent meta-analysis (via Ide 2023) | Average expected change by 2050 | Interpersonal conflict | +3.8% to +7.6% | Pooled across 80 studies |

### 1.15 The "Direct" vs. "Indirect" Pathways Debate

A central controversy in the climate-conflict literature concerns whether climate affects conflict through direct or indirect pathways:

#### Direct Pathway Hypothesis
- **Claim:** Higher temperatures directly increase aggression, violence, and intergroup conflict through physiological and psychological mechanisms
- **Evidence:** Laboratory studies show heat increases aggressive cognition; crime data shows higher assault rates on hot days
- **Proponents:** Anderson & DeLisi (2011); some interpretations of Hsiang et al. (2013)
- **Weakness:** Difficult to extrapolate from individual aggression to organized armed conflict; does not explain why some hot regions are peaceful

#### Indirect Pathway Hypothesis
- **Claim:** Climate affects conflict through intermediate steps — primarily through agricultural productivity, food prices, economic shocks, migration, and resource competition
- **Evidence:** Much stronger empirical support; growing-season effects (Harari & La Ferrara 2018), food price thresholds (Lagi et al. 2011), livelihood disruption (von Uexkull et al. 2016)
- **Proponents:** Koubi (2019), Mach et al. (2019), Buhaug (2015), most PRIO researchers
- **Key insight:** Indirect pathways are **conditional** on context — they operate primarily in poor, agricultural, politically marginalized settings

#### IPCC AR6 Position
- The IPCC AR6 WGII effectively endorsed the indirect pathway framework, stating that climate increases conflict risk through undermining food security, water security, and livelihoods (**high confidence**), while not attributing direct causal effects
- The report describes climate as a "threat multiplier" and "risk factor" rather than a direct cause

#### Current Consensus (2024-2025)
- Most researchers now accept that both direct and indirect pathways operate simultaneously, but indirect pathways are more important for organized armed conflict
- The field has shifted from debating "whether" to "when, where, and through what mechanisms"
- Emphasis on **interaction effects**: climate shocks are dangerous primarily when they interact with pre-existing vulnerabilities (poverty, political exclusion, weak institutions, agricultural dependence)

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

### 2.5 Cattaneo & Peri (2016) — Trapped Populations Deep Dive

The "trapped populations" finding is one of the most important and counterintuitive results in climate-migration research. It warrants detailed treatment:

#### Mechanism
- Migration requires **liquidity** — financial resources to pay for travel, initial settlement, finding employment
- In middle-income countries, when temperatures rise and agricultural productivity declines, households have enough resources to finance emigration (both to cities and internationally)
- In the **poorest countries**, the same temperature increase reduces income so severely that households cannot afford to migrate, even though their incentive to leave is stronger
- The result: the most climate-vulnerable populations become **trapped in place**, unable to escape worsening conditions

#### Data and Methodology
- Panel data from 116 countries over 1960-2000
- Bilateral migration data from World Bank
- Temperature and precipitation data
- Decadal analysis of emigration rates as a function of temperature trends

#### Quantified Effects
- In middle-income countries: a 1degC temperature increase raises emigration rates by ~0.5 percentage points
- In poor countries: a 1degC temperature increase **reduces** emigration probability
- The threshold between "mobile" and "trapped" roughly corresponds to per-capita income levels that distinguish lower-middle-income from low-income countries

#### Policy Implications
- Aid programs and adaptation financing may be critical for enabling voluntary migration from climate-stressed areas
- Without intervention, the poorest populations face the worst of climate impacts with the least ability to respond
- This finding undermines simplistic "climate refugee" narratives that assume mass movement from the Global South

### 2.6 Rigaud et al. (2018) — World Bank Groundswell Report Deep Dive

#### Methodology
- **URL:** https://openknowledge.worldbank.org/handle/10986/29461
- **Modeling approach:** Modified gravity model (not agent-based), isolating projected climate-driven deviations from baseline population distributions
- **Climate scenarios:** Three scenarios — pessimistic (high emissions, unequal development), more inclusive development, and more climate-friendly
- **Climate factors modeled:** Water availability, crop productivity, sea level rise and storm surges
- **Temporal scope:** Projections from 2020 to 2050
- **Spatial scope:** Sub-Saharan Africa, South Asia, and Latin America (three regions chosen for data availability and vulnerability)

#### Projection: 143 Million Internal Climate Migrants by 2050
- **Sub-Saharan Africa:** 86 million (60% of total) — largest share due to combination of high climate vulnerability, agricultural dependence, and population growth
- **South Asia:** 40 million (28%) — primarily driven by water stress and crop productivity decline
- **Latin America:** 17 million (12%) — primarily driven by water stress
- The 143 million figure represents ~2.8% of the combined population of the three regions
- **Critical caveat:** This represents the *pessimistic scenario*; concerted climate and development action could reduce internal climate migration by up to 80% (to ~30 million)

#### Groundswell Part 2 (2021)
- Extended analysis to three additional regions: East Asia and Pacific, North Africa, Eastern Europe and Central Asia
- Revised total: up to 216 million internal climate migrants across six regions by 2050 under pessimistic scenario

### 2.7 Abel et al. (2019) — Climate, Conflict, and Forced Migration

- **Journal:** Global Environmental Change, Vol. 54, pp. 239-249
- **DOI:** 10.1016/j.gloenvcha.2018.12.003
- **Method:** Gravity model with bilateral asylum application data for 157 countries (2006-2015)
- **Causal chain tested:** Climate anomaly -> drought severity -> increased conflict likelihood -> asylum seeking
- **Key findings:**
  - Climatic conditions, by affecting drought severity and the likelihood of armed conflict, played a significant role in explaining asylum seeker flows in 2011-2015
  - The climate -> conflict -> asylum chain was particularly relevant in Western Asia during 2010-2012, coinciding with the Arab Spring
  - Climate's impact on asylum flows is **limited to specific time periods and contexts** — it is not a universal, time-invariant relationship
  - Policies to improve adaptive capacity in developing countries may reduce both conflict and refugee outflows
- **Significance:** One of the few studies to empirically test the **full chain** from climate -> agriculture -> conflict -> forced migration using quantitative data

### 2.8 Internal vs. International Migration Responses

The literature increasingly recognizes that climate events produce fundamentally different migration patterns depending on whether they are internal or international:

| Dimension | Internal Migration | International Migration |
|-----------|-------------------|------------------------|
| **Scale** | Much larger (accounts for ~90% of climate-related movement) | Smaller but politically more salient |
| **Typical trigger** | Both sudden and slow-onset events | Primarily slow-onset or compound events |
| **Duration** | Often temporary (especially for sudden events) | Usually permanent or long-term |
| **Distance** | Rural-to-urban within same country | Cross-border, often to neighboring countries |
| **Data availability** | Poor (no systematic tracking in most countries) | Better (asylum/refugee databases) |
| **IDMC 2023 data** | 26.4 million new internal displacements from weather events alone | Much smaller flows recorded |

- The **Internal Displacement Monitoring Centre (IDMC)** recorded 46.9 million new internal displacements in 2023, of which 26.4 million (~56%) were attributable to climate extreme events
- Most disaster-related displacement is short-term, but slow-onset climate change may produce more permanent, potentially large-scale migration

### 2.9 Slow-Onset vs. Sudden-Onset Events and Migration

| Event Type | Examples | Migration Pattern | Duration | Key Studies |
|-----------|---------|-------------------|----------|-------------|
| **Sudden-onset** | Floods, cyclones, wildfires | Immediate mass displacement, predominantly internal, often to nearby areas | Usually temporary (weeks-months); some become permanent | IDMC annual reports; Pakistan 2022 floods |
| **Slow-onset** | Sea level rise, desertification, land degradation, temperature trends | Progressive departure, can be international, often preceded by livelihood diversification | Usually permanent | Cattaneo & Peri 2016; Rigaud et al. 2018 |
| **Compound** | Slow-onset + sudden-onset combined | Most complex response; can convert temporary to permanent displacement | Variable; tends toward permanent | Pakistan 2022 (floods on top of existing economic collapse) |

- **Pakistan 2022 example:** 8+ million people displaced by floods (sudden-onset), but the country was already experiencing economic collapse and inflation (compound vulnerability). Initial movement was internal, but thousands subsequently migrated irregularly to Europe within months
- **Key insight:** The slow-onset/sudden-onset binary is dissolving as compound events become more frequent

### 2.10 The Role of Remittances in Mediating Climate Impacts

Remittances — financial transfers from migrants to their communities of origin — play a critical but underexplored role in the climate-migration-adaptation nexus:

- **Scale:** Remittances to developing countries were more than **twice as large as all official development assistance (ODA)**, making them the largest financial flow from rich to poor countries
- **Self-insurance function:** Migrants tend to send **more** remittances following natural disasters, economic crises, and conflicts — acting as a form of self-insurance for climate-vulnerable households
- **Adaptation financing:** The 2009 commitment of $100 billion/year in climate finance was only met in 2022, two years late, with only $32.4 billion (28%) for adaptation. Remittances could fill this gap
- **Limitations:** Unregulated remittances have limited impact on household climate hazard exposure and adaptive actions (research from SE Nigeria)
- **Policy relevance:** High-income countries could create labor migration programs targeting climate-vulnerable countries, with resulting remittances classified as mobilized private climate finance for adaptation
- **Implications for Causal Atlas:** Remittance flows may **weaken** the climate->poverty->conflict chain by providing income buffers in climate-stressed regions. This represents a negative (dampening) link in the causal network that should be modeled

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

## 10. Water Scarcity -> Conflict

### 10.1 The "Water Wars" Hypothesis

The claim that water scarcity will lead to armed conflict — the "water wars" hypothesis — is one of the most debated propositions in environmental security. The evidence is nuanced: outright interstate wars over water are extremely rare, but sub-national water-related violence is surging.

### 10.2 Gleick's Water Conflict Chronology

- **Database:** The Water Conflict Chronology, maintained by the Pacific Institute, is the world's most comprehensive open-source database on water-related violence
- **URL:** https://pacinst.org/water-conflict-chronology/
- **Coverage:** Over 2,750 documented incidents spanning 4,500+ years
- **Categories:** Three types of water-conflict relationships:
  1. **Trigger:** Water access or scarcity triggers or is associated with violence
  2. **Weapon:** Water systems are used as weapons or tools of conflict
  3. **Casualty:** Water systems are targets or casualties of violence
- **Recent surge:**
  - **420 events** reported in 2024 — nearly 20% increase over 2023 and 78% increase over 2022
  - In 2024: 61% of incidents involved attacks on water infrastructure, 34% stemmed from disputes over water access, 5% involved deliberate use of water as a weapon
  - Geographic concentration: Middle East, South Asia, and Sub-Saharan Africa saw the highest concentration
  - ~12% of 2024 incidents connected to the Israeli-Palestinian conflict; ~16% connected to the Russia-Ukraine war
- **Critical finding:** Subnational conflicts (farmers vs. pastoralists, urban vs. rural water users, religious/clan disputes) **far outnumber** transboundary interstate events

### 10.3 Petersen-Perlman, Veilleux & Wolf (2017) — Transboundary Water Cooperation vs. Conflict

- **Journal:** Water International, Vol. 42(2), pp. 105-120
- **DOI:** 10.1080/02508060.2017.1276041
- **Key findings:**
  - Historically, transboundary water basins have produced **more cooperation than conflict** — the "water wars" prediction has not materialized at the interstate level
  - However, as populations grow and climate change manifests, the likelihood of water conflicts could increase
  - Institutional capacity and third-party involvement are critical for resolving disputes and promoting cooperation
  - Basins undergoing rapid physical and economic change require re-examination of existing water-sharing frameworks
- **Oregon State University database:** The Transboundary Freshwater Dispute Database catalogs over 400 international water agreements and tracks both cooperative and conflictual events

### 10.4 Ide et al. (2021) — Pathways to Water Conflict During Drought in MENA

- **Journal:** Journal of Peace Research, Vol. 58(3)
- **DOI:** 10.1177/0022343320910777
- **Method:** Qualitative Comparative Analysis (QCA) of 34 cases (17 with conflict onset)
- **Key findings:**
  - **No direct causal link** between water scarcity and conflict
  - Escalation depends on pre-existing negative socio-political relationships and political system types
  - Water-related conflicts quadrupled between 2012-2022 compared to 2000-2011, mainly in MENA
- **Significance:** Demonstrates that mediating variables (governance quality, group relations) are essential

### 10.5 GRACE Satellite Data for Groundwater Monitoring

The Gravity Recovery and Climate Experiment (GRACE) satellites and their successor GRACE-FO provide a unique capability for monitoring groundwater depletion — a key precursor to water-related conflict:

- **GRACE (2002-2017), GRACE-FO (2018-present):** Measure changes in Earth's gravitational field caused by mass redistribution, primarily water
- **Key applications:** Detecting aquifer depletion in water-scarce regions where traditional borehole monitoring is sparse
- **Regional findings:** Severe depletion trends documented in Saudi Arabia, Iran (linked to agricultural abstraction), and the Murray-Darling Basin in Australia
- **Relevance to conflict:** GRACE data can serve as an **early warning indicator** for water stress before surface-level scarcity becomes apparent
- **Limitation:** Spatial resolution (~300km) is coarse; must be combined with higher-resolution data for local analysis

### 10.6 Lag Structures

| Pathway | Lag | Evidence |
|---------|-----|---------|
| Groundwater depletion -> water scarcity | Years to decades | Slow onset, cumulative |
| Water scarcity -> farmer-herder violence | Months (seasonal) | Especially during dry season |
| Transboundary river flow reduction -> interstate tension | Months to years | Dependent on institutional frameworks |
| Dam construction -> downstream water reduction -> tension | 1-5 years | Documented for Nile (GERD), Mekong |

---

## 11. Night Lights -> Economic Activity -> Political Stability

### 11.1 Henderson, Storeygard & Weil (2012) — "Measuring Economic Growth from Outer Space"

- **Journal:** American Economic Review, Vol. 102(2), pp. 994-1028
- **DOI:** 10.1257/aer.102.2.994
- **Method:** Statistical framework using satellite nighttime light data as a proxy for GDP, with panel data from 188 countries (1992-2008)
- **Key findings:**
  - A **1% increase in nighttime light intensity** corresponds, on average, to a **0.3% increase in measured GDP**
  - For countries with good national accounts, lights data adds marginal value
  - For countries with the **worst national accounts**, the optimal estimate of true income growth assigns roughly equal weight to official GDP data and lights data
  - Among poor-data countries, the lights-based estimate of average annual growth differs by as much as **3 percentage points** from official data
  - Enables sub-national analysis: researchers can measure growth for regions, cities, or grid cells rather than entire countries
- **Innovation:** Demonstrated that coastal areas in sub-Saharan Africa were growing slower than the hinterland — a finding invisible in national statistics

### 11.2 Nightlight-GDP Elasticity Estimates

| Country Group | Elasticity (% change in lights per % change in GDP) | Source |
|--------------|-----------------------------------------------------|--------|
| Advanced economies | ~1.0 | Henderson et al. 2012 |
| Emerging markets and developing economies | **1.55** (range 1.36-1.81) | IMF 2022 |
| Poor-data countries | ~1.0 (lights provide independent signal) | Henderson et al. 2012 |

- A 10% decline in nighttime light intensity suggests an economic impact of approximately **6.5% of GDP** in emerging markets
- This elasticity is higher in developing economies because light use is more closely tied to economic fundamentals (less saturation)

### 11.3 Conflict-Driven Economic Decline Visible in Nightlights

Nightlight data has proven particularly valuable in conflict-affected economies where statistical agencies may have stopped functioning:

- **Afghanistan example (World Bank 2024):** Civilian lights showed the country was **10.5% brighter in 2023 than in 2020**, while national accounts pointed to an economy **one-quarter smaller**. The discrepancy reveals limitations of official GDP in conflict states
- **Syria:** Night lights documented the dramatic economic collapse during the civil war, with total luminosity declining by over 80% between 2011-2015 in conflict-affected areas
- **Yemen, Libya, Iraq:** Similar patterns of rapid light decline during active conflict, sometimes followed by partial recovery

### 11.4 VIIRS vs. DMSP Data Quality

- **VIIRS Day/Night Band (2012-present):** Higher spatial resolution (~750m), better radiometric calibration, wider dynamic range
- **DMSP-OLS (1992-2013):** Lower resolution (~2.7km), saturation in bright urban areas, inter-annual calibration challenges
- VIIRS provides a better proxy for local economic activity, but neither data source works well in **low-density rural areas** due to insufficient baseline luminosity
- **Cloud cover limitation:** Tropical low-income countries often have <39 clear nightly observations per quarter

### 11.5 Causal Chain: Night Lights -> Stability

```
Nighttime light change (observable from space)
    |
    v
Proxy for economic activity change
    |
    ├── Rapid decline -> Economic contraction
    │   ├── Job losses -> Grievance
    │   ├── Revenue decline -> Reduced state capacity
    │   └── Service delivery collapse -> Legitimacy crisis
    |
    └── Uneven distribution -> Spatial inequality
        ├── Urban-rural gap -> Rural grievance
        └── Inter-regional disparity -> Secessionist pressure
```

### 11.6 Datasets and Implementation

- **Key datasets:** VIIRS DNB monthly composites (2012-present), DMSP-OLS annual (1992-2013)
- **Sources:** NOAA/NCEI, Colorado School of Mines Earth Observation Group
- **Grid compatibility:** VIIRS can be aggregated to PRIO-GRID 0.5deg cells; DMSP is natively close to this resolution
- **Recommended approach for Causal Atlas:** Use nightlights as a real-time economic proxy in grid cells, particularly in Sub-Saharan Africa and conflict-affected regions where official economic data is unreliable

---

## 12. Land Degradation -> Food Insecurity -> Migration -> Urban Stress -> Conflict

This is the longest documented causal chain, with 5+ links, each of which has been independently studied and quantified.

### 12.1 The Full Chain

```
Land degradation (soil erosion, desertification, salinization)
    |
    v (Lag: years to decades)
Reduced agricultural productivity
    |
    v (Lag: 1-2 growing seasons)
Food insecurity (household and regional)
    |
    v (Lag: months to years)
Rural-to-urban migration
    |
    v (Lag: years)
Urban stress (overcrowding, unemployment, service strain)
    |
    v (Lag: months to years)
Social unrest / conflict
```

### 12.2 UNCCD Global Land Outlook Findings

- **Source:** UN Convention to Combat Desertification, Global Land Outlook 2 (2022)
- **URL:** https://www.unccd.int/resources/global-land-outlook/overview
- **Key findings:**
  - Land degradation is a growing threat to global security
  - If current trends continue, crop yields could decline by **up to 50% in some regions by 2050**, driving food prices up by **30%**
  - Land degradation may lead to the **migration of 135 million people by 2045** (UK Ministry of Defence estimate)
  - Agriculture, livestock, and forestry provide income and employment for **more than 80% of the Sahel population**
  - Overexploitation of natural resources has direct and persistent impacts on food, water, and energy security, amplifying social inequalities, conflicts over land, and forced migration

### 12.3 Sahel Case Studies

The Sahel provides the most extensively documented example of this long-chain pathway:

- **Lake Chad Basin:** The lake has shrunk by ~90% since the 1960s, devastating fishing and farming livelihoods for 30+ million people, creating conditions exploited by Boko Haram
- **Mali and Burkina Faso:** Desertification has pushed pastoralists southward into farming zones, triggering escalating farmer-herder violence and providing recruitment opportunities for armed groups
- **Nigeria's Middle Belt:** Land degradation and southward pastoralist migration have produced some of the deadliest communal violence in recent years
- **Radicalization link:** The UNCCD notes that radicalization of youth in areas with severely degraded land is "not a coincidence" — degraded livelihoods create vulnerable populations for recruitment by armed groups

### 12.4 How Each Link Has Been Quantified

| Link | Quantified Effect | Source |
|------|------------------|--------|
| Land degradation -> crop yield loss | Up to 50% decline in degraded areas by 2050 | UNCCD GLO2 (2022) |
| Crop failure -> food insecurity | 3-12 month lag; IPC Phase 3+ increases | FEWS NET, IPC reports |
| Food insecurity -> migration | 135 million by 2045 (land degradation alone) | UNCCD citing UK MoD |
| Rural-urban migration -> urban stress | Population density increases, service strain | UN-Habitat |
| Urban stress -> conflict | Significant association in cities with weak institutions | IPCC AR6 (medium confidence) |

---

## 13. Mining/Resource Extraction -> Pollution -> Health -> Social Unrest

### 13.1 Berman et al. (2017) — "This Mine Is Mine! How Minerals Fuel Conflicts in Africa"

- **Journal:** American Economic Review, Vol. 107(6), pp. 1564-1610
- **DOI:** 10.1257/aer.20150774
- **Method:** Combined georeferenced data on mining extraction of 14 minerals with conflict events at **0.5deg x 0.5deg** resolution for all of Africa (1997-2010)
- **Key findings:**
  - Positive impact of mining on conflict at the local level
  - The historical rise in mineral prices (commodity super-cycle) might explain up to **one-fourth of the average level of violence** across African countries
  - Price spikes for minerals extracted in ethnic homelands of rebel groups tend to expand fighting operations beyond the homeland
  - Capturing a mine empowers the successful group to expand fighting activity across larger territory in following years
- **Lag structure:** Price changes affect conflict with 0-12 month lag; territorial expansion follows mine capture with 1-2 year lag
- **Significance for Causal Atlas:** Uses the same 0.5deg grid resolution as PRIO-GRID, making direct integration feasible

### 13.2 The "Resource Curse" at Sub-National Level

The resource curse — the paradox that resource-rich countries often have worse development outcomes — operates at sub-national scales:

- **Local-level mechanisms:**
  - Revenue from extraction funds armed groups
  - Grievances over unequal distribution of mining benefits
  - Environmental degradation of farmland and water sources
  - In-migration of workers creates social tensions
  - State forces may protect mining operations at the expense of local populations
- **Cobalt in the DRC:** The energy transition has created new "critical mineral" conflicts, with cobalt reserves associated with conflict in Africa (recent analysis, 2024)
- **Gold mining in West Africa:** Chinese companies have moved into artisanal gold mining sites in DRC and Ghana, replacing small-scale mining with environmentally destructive semi-industrial operations

### 13.3 Artisanal Mining Regions as Hotspots

- **Scale:** An estimated 40 million people worldwide depend on artisanal and small-scale mining (ASM)
- **DRC:** ~40,000 children work in artisanal cobalt mines, exposed to toxic dust causing respiratory diseases
- **Ghana:** Artisanal mining ("galamsey") linked to mercury contamination of water, crops, and miners themselves
- **Health impacts:** Mercury poisoning, lead contamination, respiratory disease from dust, waterborne illness
- **Conflict dynamics:** Armed groups finance operations through illicit mineral trade; communities protest environmental destruction; government forces clash with illegal miners

### 13.4 The Full Causal Chain

```
Mining/resource extraction
    |
    ├── Environmental contamination
    │   ├── Water pollution (mercury, arsenic, heavy metals)
    │   ├── Soil contamination -> crop contamination
    │   └── Deforestation and land degradation
    |
    ├── Health impacts (lag: months to decades)
    │   ├── Respiratory disease (dust, particulates)
    │   ├── Neurological damage (mercury, lead)
    │   ├── Cancer clusters
    │   └── Reduced labor productivity
    |
    └── Social/political impacts
        ├── Community grievance over environmental destruction
        ├── Unequal benefit distribution -> social tension
        ├── Armed group financing through mineral trade
        └── Displacement of agricultural livelihoods
```

---

## 14. Temperature -> Labor Productivity -> Economic Output -> Social Stress

### 14.1 Burke, Hsiang & Miguel (2015) — Global Non-Linear Temperature-Economy Relationship

- **Journal:** Nature, Vol. 527, pp. 235-239
- **DOI:** 10.1038/nature15725
- **Method:** Economic data from 166 countries (1960-2010), identifying a universal nonlinear relationship
- **Key findings:**
  - Overall economic productivity is **non-linear in temperature** for all countries
  - Productivity peaks at an annual average temperature of **13degC** and declines strongly at higher temperatures
  - The relationship is globally generalizable, unchanged since 1960, and apparent for **both agricultural and non-agricultural** activity in both rich and poor countries
  - Climate change is projected to lower global incomes by **more than 20% by 2100** relative to a no-warming scenario
  - Warming will widen the gap between rich (temperate, ~13degC average) and poor (tropical, already above optimal) countries

### 14.2 Dell, Jones & Olken (2012) — Temperature Shocks and Economic Growth

- **Journal:** American Economic Journal: Macroeconomics, Vol. 4(3), pp. 66-95
- **DOI:** 10.1257/mac.4.3.66
- **Key findings:**
  - A 1degC increase in average temperature reduces growth by **~1.3 percentage points** in poor countries
  - Higher temperatures may reduce **growth rates** (not just output levels), implying persistent, compounding effects
  - Wide-ranging effects: reduces agricultural output, industrial output, *and* political stability

### 14.3 Sector-Specific Effects

| Sector | Temperature Sensitivity | Mechanism | Key Finding |
|--------|------------------------|-----------|-------------|
| **Agriculture** | Very high | Direct crop damage + worker heat stress | Accounts for 60% of projected heat-related labor losses by 2030 (ILO) |
| **Construction** | Very high | Outdoor work, physical labor | 19% of projected heat-related labor losses by 2030 |
| **Manufacturing** | Moderate | Indoor work, but poorly climate-controlled in developing countries | Significant losses in low-exposure sectors including manufacturing and utilities |
| **Services** | Lower but non-zero | Cognitive performance declines at high temperatures | Office productivity declines documented above 25degC |

### 14.4 Heat Stress and Labor Productivity — Recent Evidence (2020-2025)

- **US Federal Reserve (2024):** In 2021, more than **2.5 billion hours of labor** in US agriculture, construction, manufacturing, and service sectors were lost to heat exposure
- **Economic cost:** $100 billion in lost productivity in 2020, expected to grow to **$500 billion/year by 2050** (US alone)
- **Productivity thresholds:**
  - At 90degF (32degC): productivity drops by ~25%
  - At 100degF (38degC): productivity drops by ~70%
  - Heavy work becomes unsafe at WBGT >33degC (91degF)
- **Global projections:** Under worst-case warming, heat stress could reduce global labor productivity by **30-40% by 2100** (ILO)
- **ILO (2019):** Agriculture and construction sectors will account for **60% and 19%** respectively of working hours lost to heat stress in 2030

### 14.5 Regional Disparities

- Africa, Asia, and Oceania face the greatest projected declines in effective labor: **~33%, ~25%, and ~18%** respectively under 3degC warming
- This disproportionate impact on already-poor tropical regions amplifies global inequality and creates conditions for social stress
- The temperature-productivity relationship implies a **positive feedback loop**: warming reduces output -> reduces adaptive capacity -> increases vulnerability to further warming impacts

### 14.6 The Complete Chain

```
Temperature increase
    |
    v
Labor productivity decline
├── Direct: heat stress (outdoor workers)
├── Indirect: cognitive performance decline
└── Compound: combined heat + humidity (wet-bulb temperature)
    |
    v
Economic output reduction
├── Agricultural: crop losses + farmer productivity decline
├── Industrial: manufacturing output decline
└── Services: reduced efficiency
    |
    v
Social stress
├── Unemployment / underemployment
├── Income decline -> poverty
├── Government revenue decline -> service cuts
└── Inequality (within and between countries)
    |
    v
Potential for instability
```

---

## 15. Sea Level Rise -> Saltwater Intrusion -> Agricultural Loss -> Displacement

### 15.1 The Pathway

Sea level rise represents a slow-onset climate impact with cascading consequences through multiple linked systems:

```
Sea level rise
    |
    v
Saltwater intrusion into coastal aquifers and deltas
    |
    v
Agricultural soil salinization + freshwater contamination
    |
    v
Crop failure and loss of arable land
    |
    v
Livelihood loss -> food insecurity
    |
    v
Displacement (initially internal, potentially international)
```

### 15.2 Bangladesh Case Study

Bangladesh is the most extensively documented case of this pathway:

- **Sea level rise rate:** Bay of Bengal sea levels rising at a rate **60% faster** than the global average
- **Displacement projection:** 0.9-2.1 million people displaced by 2050 from sea level rise alone
- **Agricultural impact:** Each year, thousands of hectares of arable land are lost to sea encroachment; salinization renders agricultural soil infertile, destroying crops and increasing food insecurity
- **Salinity intrusion:** Affects both drinking water and irrigation water in coastal districts (Khulna, Satkhira, Bagerhat)
- **Social impacts:** Forced rural families to abandon homes; women and girls disproportionately affected; seasonal and permanent migration to Dhaka and Chittagong
- **Causal chain in action:** Shoreline retreat and erosion documented to cascade into livelihood disruption, settlement abandonment, and migration to urban areas

### 15.3 Pacific Island Case Studies

- **Kiribati:** Projected to lose between **9.7% and 19.8%** of total land area to permanent submersion
- **Tuvalu, Micronesia, Maldives:** Among the most vulnerable globally
- **Atoll vulnerability:** Atolls are the most susceptible to coastal erosion, flooding, and salt intrusion into soils and freshwater
- **Existential threat:** For low-lying atoll nations, sea level rise threatens not just displacement but the potential loss of sovereign territory entirely

### 15.4 IPCC AR6 Sea Level Projections Linked to Displacement

- **IPCC SROCC Chapter 4:** Sea level rise and implications for low-lying islands, coasts, and communities
- **Projections:** 0.43-0.84m rise by 2100 (SSP2-4.5 to SSP5-8.5 scenarios)
- **Economic cost:** Loss of land estimated to carry annual costs of **$34.1-$88.0 billion** by end of century (South Asia, East Asia, Central and West Asia)
- **Cascading effects:** Sea level rise produces compounding impacts: coastal ecosystem loss, groundwater salinization, flooding, infrastructure damage -> risks to livelihoods, settlements, health, food and water security (IPCC AR6 WGII)

### 15.5 Timeline of Expected Impacts

| Timeframe | Expected Impact | Affected Populations |
|-----------|----------------|---------------------|
| 2030-2040 | Increased saltwater intrusion in major deltas (Bangladesh, Mekong, Nile) | Hundreds of millions |
| 2040-2060 | Loss of significant arable land in coastal zones | Tens of millions of farmers |
| 2050-2080 | Partial or complete submersion of low-lying atolls | Small island nations (~1 million) |
| 2100+ | Major coastal city flooding (without adaptation) | Hundreds of millions in megacities |

---

## 16. Pandemic -> Supply Chain Disruption -> Food Price Shock -> Unrest

### 16.1 COVID-19 as the Definitive Case Study

The COVID-19 pandemic provided an unprecedented natural experiment in how health crises cascade through supply chains to food security and social stability:

```
Pandemic (COVID-19)
    |
    ├── Lockdowns and movement restrictions
    │   ├── Labor shortages in agriculture (seasonal workers stranded)
    │   ├── Processing plant shutdowns (especially meat processing)
    │   ├── Transport disruption (air freight for perishables)
    │   └── Border closures -> trade disruption
    |
    ├── Demand shocks
    │   ├── Restaurant/food service collapse -> demand redistribution
    │   ├── Panic buying -> short-term hoarding
    │   └── Income loss -> reduced purchasing power
    |
    └── Supply chain cascading effects
        ├── Food price spikes (retail prices up 11% in US, 2021-2022)
        ├── Global food price index hit record in March 2022 (+13% in single month)
        └── Doubled number of severely food-insecure people (to 276 million)
```

### 16.2 Quantified Impacts of the 2020-2022 Food Price Crisis

- **Global GDP:** Declined approximately 3.1% in 2020 (IMF estimate)
- **US food prices:** Spiked **11%** between 2021-2022
- **World food prices:** March 2022 saw the **fastest price surge ever**, jumping nearly 13% to a new record high (driven by both pandemic aftereffects and the Russia-Ukraine war)
- **Food insecurity:** The number of severely food-insecure people **doubled** from pre-pandemic levels to 276 million
- **Supply chain disruption:** Subtracted 0.5-1.2% from global value added during 2021 recovery; added ~1% to global core inflation

### 16.3 How Pandemic Restrictions Amplified Existing Vulnerabilities

- Countries with **higher food import dependence** were more severely affected (paralleling the Arab Spring food price dynamics)
- **Low-income countries** experienced more severe food security impacts due to weaker social safety nets
- **Informal economy workers** (dominant in developing countries) lost income immediately with no fallback
- Pre-existing inequalities were **amplified**: women, minority groups, and rural populations faced disproportionate impacts
- The pandemic demonstrated how a single shock can cascade across domains (health -> economy -> food -> social stability) within months

### 16.4 Lag Structures

| Phase | Timing from Pandemic Onset | Key Effects |
|-------|---------------------------|-------------|
| Immediate (0-3 months) | Demand shock, panic buying, price spikes | Initial food price volatility |
| Short-term (3-12 months) | Supply chain disruption, labor shortages | Sustained high prices, localized shortages |
| Medium-term (1-2 years) | Inflation, input cost increases, fertilizer shortages | Structural food price increase |
| Longer-term (2-4 years) | Combined with Ukraine war, energy crisis | Record food prices, increased food insecurity |

---

## 17. Social Media / Information Cascades -> Protest Mobilization

### 17.1 Digital Communication and Protest Dynamics

The role of social media and digital communication in protest mobilization has fundamentally transformed collective action dynamics:

- **Key mechanism:** Social media reduces the cost of coordination, information sharing, and collective action, enabling rapid mobilization that was previously impossible
- **Research finding:** Studies using both ARIMA and Granger Causality models find a **significant impact of social media activity on physical turnout** at protests across days
- **Amplification:** TV and social media have different but complementary effects on protest mobilization — social media provides horizontal coordination while traditional media provides legitimacy and broader awareness

### 17.2 GDELT as Early Warning Signal

- **GDELT (Global Database of Events, Language, and Tone)** monitors print, broadcast, and web news media in over 100 languages, coding events and measuring media tone
- **Media tone as predictor:** Changes in media tone (increasingly negative sentiment) about government, food prices, or economic conditions can serve as leading indicators of protest events
- **Limitations:** GDELT data is notoriously noisy with large volumes of superfluous information from automated collection and analysis
- **Lag structure:** Media coverage typically leads protest events by **days to weeks**; sustained negative tone over months may predict larger-scale unrest

### 17.3 Early Warning Systems

- **Anomaly detection approaches:** Identify sudden and unexpected changes in behavioral patterns (social media activity, media coverage, search queries) that may indicate potential for unrest
- **Digital connectivity effects:** Higher mobile ownership and network coverage facilitate protest mobilization, but free speech limitations attenuate this effect
- **Dual role:** Social media can both mobilize protests AND enable government surveillance and repression — the net effect depends on context

### 17.4 Lag Structures and Causal Chain

| Signal | Lag to Protest | Mechanism |
|--------|---------------|-----------|
| Media tone shift (negative) | Days to weeks | Framing and grievance amplification |
| Social media viral content | Hours to days | Rapid coordination and mobilization |
| Food price spike news | Days to weeks | Grievance activation |
| Government policy announcement | Days to months | Response to perceived injustice |

---

## 18. El Nino/La Nina -> Multi-Domain Cascading Effects

### 18.1 Hsiang, Meng & Cane (2011) — ENSO and Civil Conflict

- **Journal:** Nature, Vol. 476, pp. 438-441
- **DOI:** 10.1038/nature10311
- **Method:** Quasi-experiment comparing conflict rates in ENSO-affected (teleconnected) tropical countries vs. weakly affected countries, 1950-2004
- **Key findings:**
  - The risk of civil conflict in teleconnected tropical countries **doubles** during El Nino years: from **3% annual conflict risk** (La Nina) to **6%** (El Nino)
  - ENSO may have played a part in initiating **21% of all civil conflicts since 1950**
  - The effect is concentrated in tropical countries (South America, Africa, Asia-Pacific, including parts of Australia) that are strongly affected by ENSO teleconnections
  - Countries weakly affected by ENSO show no such pattern
- **Significance:** One of the strongest pieces of evidence for a climate-conflict link, because ENSO is exogenous (not caused by conflict) and has well-documented regional effects

### 18.2 ENSO Teleconnections and Regional Impacts

| Region | El Nino Effect | La Nina Effect | Primary Impact Pathway |
|--------|---------------|----------------|----------------------|
| **Australia/SE Asia** | Drought, reduced rainfall | Increased rainfall, flooding | Crop failure, wildfire |
| **South America (Pacific coast)** | Flooding, heavy rainfall | Drought | Infrastructure damage, fishery collapse |
| **East Africa** | Increased rainfall | Drought | Crop impact varies; malaria increase |
| **Southern Africa** | Drought | Increased rainfall | Crop failure (maize) |
| **India** | Weakened monsoon | Strengthened monsoon | Crop failure when monsoon fails |
| **Peru** | Anchovy fishery collapse | Recovery | Fishmeal price spike, economic loss |

### 18.3 Crop Failure and Food Price Impacts

- Significant negative El Nino impacts on yields evident in **22-24% of harvested areas worldwide**
- Affected crops include: maize (SE US, China, E/W Africa, Mexico, Indonesia), soybean (India, China), rice (S China, Myanmar, Tanzania), wheat (China, US, Australia)
- In past El Nino years, **Zimbabwe and South Africa maize production** saw average deficits of **10-15%** relative to expected yields, with some years exceeding 50% deficit, leading to sharp regional food price spikes

### 18.4 Using ONI (Oceanic Nino Index) as a Predictor

- **Definition:** The ONI tracks 3-month running mean SST anomalies in the Nino 3.4 region (5degN-5degS, 120degW-170degW)
- **Thresholds:** El Nino declared when ONI >= +0.5degC for 5 consecutive overlapping 3-month periods; La Nina when ONI <= -0.5degC
- **Predictive value:** ONI transitions are detectable months before regional climate impacts manifest
- **Lag structure:** Typically **2-8 months** between ENSO phase transition and regional climate/agricultural impacts
- **Source:** NOAA Climate Prediction Center (https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php)
- **Relevance for Causal Atlas:** ONI can serve as a **leading indicator** for multi-domain risk assessment in teleconnected regions. When ONI exceeds thresholds, the system should flag increased risk of crop failure, food price spikes, and conflict in affected regions

### 18.5 The Multi-Domain Cascade

```
ENSO phase transition (El Nino onset)
    |
    v (2-4 months lag)
Regional weather anomalies
├── Drought (Australia, SE Asia, S Africa, India)
├── Flooding (South America, East Africa)
└── Temperature anomalies
    |
    v (1-6 months lag)
Multi-domain impacts
├── Agriculture: Crop failure -> food price spikes (3-6 months)
├── Fisheries: Anchovy collapse (Peru) -> fishmeal prices (1-3 months)
├── Disease: Malaria/dengue/cholera increase (2-6 months)
├── Water: Reservoir depletion/flooding -> water stress
└── Energy: Hydropower disruption (drought-affected regions)
    |
    v (months to years)
Social/political consequences
├── Food price unrest (weeks-months from price spike)
├── Increased conflict risk (doubled in tropics, Hsiang et al.)
├── Migration from agricultural areas
└── Government fiscal stress (disaster response)
```

---

## 19. Volcanic Eruptions -> Climate Forcing -> Agricultural Disruption

### 19.1 Historical Evidence: Tambora 1815 and the "Year Without a Summer"

- **Event:** Mount Tambora (Indonesia) erupted in April 1815 with VEI 7, the largest eruption in recorded history
- **Magnitude:** Ejected 37-45 km3 of material and massive quantities of SO2 into the stratosphere
- **Climate impact:** Global temperature drop of ~0.4-0.7degC in 1816, producing the "Year Without a Summer"
- **Agricultural devastation:**
  - Snow and frozen soil persisted into summer across New England, devastating crops
  - European harvest failures across multiple countries
  - Indian monsoon disruption caused three failed harvests
  - Rice crop failure in China and Southeast Asia
- **Cascading social effects:**
  - Food prices rose dramatically across Europe and North America
  - Famine across multiple continents
  - Contributed to spread of a new strain of cholera
  - Triggered westward migration in the US (to Indiana, Illinois)
  - Social unrest and political instability in Europe

### 19.2 Pinatubo 1991 as a Modern Natural Experiment

- **Event:** Mount Pinatubo (Philippines) erupted June 1991 with VEI 6
- **SO2 injection:** ~20 Mt into the stratosphere (Tambora was ~3.5x larger)
- **Climate impact:** Global cooling of ~0.5degC for 2-3 years
- **Agricultural effects:** Measurable reductions in global crop yields
- **Scientific value:** Provided the most detailed observations of volcanic climate forcing, used to validate climate models
- **Comparison:** Pinatubo was at least 10x smaller than Tambora but still produced significant global effects — demonstrating vulnerability of modern food systems to volcanic forcing

### 19.3 Quantified Climate Impacts of Large Eruptions

| Eruption | VEI | SO2 Injection | Global Cooling | Duration |
|----------|-----|--------------|----------------|----------|
| Tambora 1815 | 7 | ~70 Mt | 0.4-0.7degC | 2-3 years |
| Krakatoa 1883 | 6 | ~15 Mt | ~0.3degC | 1-2 years |
| Pinatubo 1991 | 6 | ~20 Mt | ~0.5degC | 2-3 years |
| Hunga Tonga 2022 | 5-6 | Low SO2, high H2O | Complex (net warming possible from water vapor) | Under study |

### 19.4 Relevance for Causal Atlas

- Large volcanic eruptions represent **exogenous shocks** to the climate-food-conflict system
- The Tambora case demonstrates the full chain: volcanic eruption -> climate forcing -> agricultural disruption -> food price spike -> famine -> social unrest
- **Lag structure:** Climate effects begin 1-3 months after eruption; agricultural effects in the following growing season(s); social effects 6-24 months after the eruption
- **Data source:** Smithsonian Institution Global Volcanism Program (https://volcano.si.edu/); NOAA volcanic SO2 data
- Modern eruptions could be detected in real-time via satellite (SO2 plumes) and their agricultural impacts predicted using existing climate models

---

## 20. Causal Chain Atlas: Master Reference Table

This table provides a comprehensive mapping of all documented causal chains relevant to the Causal Atlas project.

### 20.1 Master Table

| # | Source Domain | Intermediate Steps | Target Domain | Typical Lag | Effect Size (Standardized) | Confidence | Key Datasets Needed | Best Statistical Method | # Published Studies |
|---|-------------|-------------------|---------------|-------------|---------------------------|------------|--------------------|-----------------------|-------------------|
| 1 | Climate (drought/heat) | Crop failure -> food prices | Conflict/unrest | 0-12 months (growing season) | +11-14% intergroup conflict per 1sigma temp increase | **Strong** | CHIRPS, SPEI, ACLED, UCDP-GED, WFP prices | PCMCI, panel FE | 100+ |
| 2 | Climate extremes | Direct displacement / livelihood loss | Migration | Days (sudden) to years (slow) | 0.5pp emigration per 1degC (middle-income) | **Moderate** | ERA5, CHIRPS, IDMC, census data | Gravity models, panel FE | 50+ |
| 3 | PM2.5 / air pollution | Cumulative exposure | Respiratory/cardiovascular mortality | Days (acute) to years (chronic) | +7-10% mortality per 10ug/m3 | **Very strong** | OpenAQ, Sentinel-5P, MODIS AOD, WHO GHO | Cox PH, spatiotemporal models | 200+ |
| 4 | Earthquake | Infrastructure destruction -> displacement -> economic disruption | Social effects | Immediate to years | Variable; GDP effects often small due to reconstruction | **Strong** | USGS, VIIRS nightlights, World Bank | DiD, event studies | 80+ |
| 5 | Food price spike | Affordability crisis -> grievance | Political instability/unrest | Weeks to months | Significant above FAO FPI threshold ~210 | **Strong** | FAO FPI, WFP, ACLED | Threshold models, panel FE | 30+ |
| 6 | Disease outbreak | Health system strain -> behavioral response -> economic collapse | Social/economic disruption | Days to years | Behavioral effects = 80-90% of total economic impact | **Strong** | WHO, IHME, World Bank, ACLED | Event studies, DiD | 50+ |
| 7 | Deforestation | GHG emissions + local climate change -> crop yield reduction | Food insecurity | Years to decades | 0.3-0.8degC local warming from deforestation | **Moderate** | GFW, ERA5, FAO, FEWS NET | Spatial panel, time series | 40+ |
| 8 | Urbanization | Industrial/transport emissions -> pollution exposure | Health outcomes | 1-5 years | +0.54 ug/m3 PM2.5 per 1% urbanization | **Strong** | UN WUP, OpenAQ, Sentinel-5P, WHO GHO | Panel IV, spatial econometrics | 60+ |
| 9 | Water scarcity | Resource competition -> farmer-herder violence | Conflict | Months (seasonal) | Quadrupled incidents 2012-2022 vs 2000-2011 | **Moderate** | GRACE-FO, CHIRPS, Pacific Institute DB, ACLED | QCA, panel FE | 30+ |
| 10 | Night light decline | GDP proxy decline -> job loss -> service collapse | Political instability | Months to years | 1% lights change ~ 0.3% GDP (0.65% in developing) | **Moderate** | VIIRS DNB, DMSP-OLS, Polity | Panel FE, event studies | 20+ |
| 11 | Land degradation | Food insecurity -> migration -> urban stress | Conflict | Years to decades | Crop yields down up to 50% in degraded areas | **Moderate** | UNCCD, MODIS NDVI, FAO, IDMC | Long-panel, spatial models | 25+ |
| 12 | Mining activity | Pollution + revenue competition | Health + conflict | Months to years | Mine price increase explains ~25% of African violence | **Moderate** | Mining databases, ACLED, OpenAQ, WHO | Spatial panel, IV with commodity prices | 20+ |
| 13 | Temperature increase | Labor productivity decline -> economic output reduction | Social stress | Contemporaneous to years | Productivity peaks at 13degC; -1.3pp growth per 1degC in poor countries | **Strong** | ERA5, Penn World Tables, ILO labor stats | Panel FE, nonlinear models | 40+ |
| 14 | Sea level rise | Saltwater intrusion -> agricultural loss -> livelihood disruption | Displacement | Years to decades | 0.9-2.1 million displaced in Bangladesh by 2050 | **Moderate** | Satellite altimetry, GRACE, FAO, IDMC | Scenario modeling, gravity models | 30+ |
| 15 | Pandemic | Supply chain disruption -> food price shock | Unrest | Weeks to months | Food prices +11-13% (COVID); food insecurity doubled | **Strong** (COVID as natural experiment) | WHO, FAO FPI, WFP, ACLED | Event studies, DiD | 30+ |
| 16 | Social media / information cascade | Coordination cost reduction -> rapid mobilization | Protest events | Hours to days | Significant Granger-causal relationship | **Moderate** | GDELT, Twitter/X API, ACLED | Granger causality, ARIMA, NLP | 20+ |
| 17 | ENSO (El Nino) | Regional weather -> crop failure -> food prices | Conflict | 2-8 months | Conflict risk doubles in tropics (3% -> 6%) | **Strong** | ONI, CHIRPS, FAO, ACLED | Panel FE, quasi-experimental | 15+ |
| 18 | Volcanic eruption | Stratospheric SO2 -> global cooling -> crop failure | Social disruption | Months to years | 0.4-0.7degC cooling (VEI 7) | **Strong** (historical) | GVP, satellite SO2, crop models | Event studies, natural experiment | 10+ |
| 19 | Lead exposure (childhood) | Neurological damage -> impulsivity/aggression | Violent crime | 18-23 years | ~56% of US crime decline attributable | **Very strong** | NHANES, FBI UCR, environmental monitoring | Distributed lag, IV | 15+ |
| 20 | ENSO -> disease | Regional flooding/drought -> vector breeding | Malaria/dengue/cholera increase | 2-6 months | Documented increases in affected regions | **Moderate** | ONI, WHO, DHS | Time series, spatial models | 15+ |

### 20.2 How to Read This Table

- **Effect Size:** Standardized where possible; expressed as percentage change per unit of the climate/environmental variable. Confidence intervals are generally wide — see individual sections for details.
- **Confidence levels:**
  - **Very strong:** Multiple meta-analyses, consistent results across contexts, biological mechanism well understood
  - **Strong:** Multiple rigorous studies, consistent results, plausible mechanisms identified
  - **Moderate:** Evidence exists but results are context-dependent, some conflicting findings, or limited geographic coverage
  - **Weak:** Preliminary evidence, few studies, highly contested
- **# Published Studies:** Approximate count of peer-reviewed quantitative studies, not including qualitative/case study work

---

## 21. Novel and Emerging Pathways

### 21.1 Compound Events (Multiple Hazards Simultaneously)

The IPCC AR6 highlights that compound events — multiple climate hazards occurring simultaneously or in rapid succession — pose risks that exceed the sum of individual hazards:

- **Definition:** Events where multiple drivers and/or hazards contribute to societal or environmental risk, where the combination leads to impacts that are qualitatively different or larger than those from any individual driver/hazard
- **Examples:**
  - Heat + drought: Combined effects trigger sudden, significant losses in agricultural yields beyond what either hazard alone would produce
  - Heat + labor productivity loss: Workers cannot compensate for drought losses because they are simultaneously less productive
  - Sea level rise + storm surge + river flooding: Cascading coastal impacts
  - Pakistan 2022: Unprecedented rainfall hit a country already experiencing economic collapse and inflation, displacing **30+ million people** and causing **$30 billion+ in damages**
- **IPCC AR6 language:** "Multiple climate hazards will occur simultaneously, and multiple climatic and non-climatic risks will interact, resulting in compounding overall risk and risks cascading across sectors and regions"
- **Implication for Causal Atlas:** The system must model **interaction effects** between hazards, not just individual causal chains. A grid cell experiencing both drought AND high temperatures should flag compound risk

### 21.2 Cascading Tipping Points

#### Lenton et al. (2019) — "Climate Tipping Points — Too Risky to Bet Against"
- **Journal:** Nature (commentary), Vol. 575, pp. 592-595
- **DOI:** 10.1038/d41586-019-03595-0
- **Key argument:** Climate tipping points are interconnected — crossing one threshold makes crossing others more likely, creating a potential "tipping cascade"
- **Identified tipping elements:**
  - Arctic sea ice loss
  - Greenland ice sheet disintegration
  - West Antarctic ice sheet collapse
  - Boreal permafrost thaw
  - Amazon rainforest dieback
  - Atlantic Meridional Overturning Circulation (AMOC) weakening
  - Coral reef die-off

#### Armstrong McKay et al. (2022) — "Exceeding 1.5degC Could Trigger Multiple Climate Tipping Points"
- **Journal:** Science, Vol. 377(6611)
- **DOI:** 10.1126/science.abn7950
- **Key findings:**
  - Even at 1.5degC warming, **five tipping points** become possible
  - Tipping elements interact: Arctic sea ice retreat -> Greenland melt -> AMOC weakening -> Amazon dieback
  - The probability of triggering cascading tipping points increases non-linearly with warming

#### Wunderling et al. (2024) — "Climate Tipping Point Interactions and Cascades: A Review"
- **Journal:** Earth System Dynamics, Vol. 15, pp. 41-66
- **Key contribution:** Interactions between tipping elements could lower thresholds compared to individual tipping points, and cascades could emit additional CO2, creating a self-reinforcing feedback
- **Relevance for Causal Atlas:** While tipping points operate on longer timescales than monthly monitoring, early indicators (ice sheet mass balance from GRACE, AMOC strength, Amazon vegetation indices from NDVI) could be tracked as background risk factors

### 21.3 Climate -> Mental Health -> Social Cohesion

An emerging research area connecting climate impacts to mental health and, through that, to social stability:

- **Direct pathways:**
  - Extreme weather events -> PTSD, anxiety, depression (53% of climate event-affected survey respondents reported impacts; 22.8% reported negative mental health effects)
  - Heat waves -> increased aggression, violence, and self-harm
  - Chronic climate change -> eco-anxiety, solastalgia (grief over environmental loss)
- **Indirect pathways:**
  - Climate -> job loss, displacement -> anxiety, depression -> reduced social cohesion
  - Climate -> forced migration -> loss of community, cultural identity -> social fragmentation
- **Eco-anxiety:** A growing concern, particularly among children and young people, associated with age, gender, media exposure, socioeconomic context, and government inaction
- **Social cohesion impacts:** WHO (2022) policy brief notes that climate change can harm social cohesion and community resources, with cascading mental health consequences
- **Vulnerable populations:** Indigenous communities, low-income populations, and those with pre-existing mental health conditions face heightened psychological impacts
- **Research gaps:** The pathway from climate-induced mental health deterioration to collective social action (protest, conflict) remains largely unquantified. This is a frontier for Causal Atlas research

### 21.4 AI/Automation -> Job Displacement -> Inequality -> Instability

An emerging non-climate causal chain with significant implications for social stability:

- **Scale of displacement:** Goldman Sachs (2023) projected that roughly two-thirds of current jobs are exposed to some degree of AI automation, with up to **300 million jobs worldwide** potentially displaced or significantly altered
- **Inequality amplification:**
  - Knowledge-based industries (finance, legal, customer support) already shedding entry-level jobs
  - 79% of employed women in the US work in jobs at high risk of automation vs. 58% of men
  - Automation disproportionately impacts routine tasks held by minority workers
  - Tech sector: over 95,000 workers lost jobs in 2024
- **Public anxiety:** 2023 survey across 31 countries found over half of respondents "nervous" about AI's impact on daily lives
- **Instability pathway:**
  ```
  AI/Automation advancement
      |
      v
  Job displacement (especially routine tasks)
      |
      v
  Income inequality (within and between countries)
      |
      v
  Social stress (loss of purpose, economic anxiety)
      |
      v
  Political polarization + populism
      |
      v
  Potential for social instability
  ```
- **Relevance for Causal Atlas:** While not a "climate" chain, AI-driven economic disruption could interact with climate vulnerabilities — e.g., automation displacing agricultural labor in already climate-stressed regions

### 21.5 Biodiversity Loss -> Ecosystem Services -> Food Security

- **The paradox:** The global food system is the primary driver of biodiversity loss (agriculture accounts for 80% of global land-use change), yet biodiversity is essential for sustaining food systems
- **Ecosystem service degradation:** Pollinator decline, soil microbiome loss, pest control disruption, fishery collapse
- **IPBES assessment:** Reducing one ecosystem service tends to reduce the productivity of others (cascading degradation)
- **Supply chain vulnerability:** 80% of recent global land-use change impacts were associated with increased agri-food exports from Latin America, Africa, and SE Asia + Pacific
- **Collapse risk:** "Realistic possibility some ecosystems start to collapse by 2030 or sooner" due to combined pressures of land use change, pollution, climate change, and other drivers (UK government assessment, 2024)
- **Kunming-Montreal GBF (2022):** Target 18 requires signatories to identify and phase out subsidies harmful to biodiversity by 2025
- **Causal chain:**
  ```
  Agricultural intensification + deforestation
      |
      v
  Biodiversity loss (pollinators, soil biota, pest predators)
      |
      v
  Ecosystem service degradation
      |
      v
  Reduced crop resilience and productivity
      |
      v
  Food insecurity (especially in biodiversity-dependent systems)
      |
      v
  Livelihood stress and potential conflict
  ```

---

## 22. Cross-Cutting Methodological Insights

### 22.1 Statistical Methods Used Across Studies

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

### 22.2 PCMCI: Most Relevant Method for Causal Atlas

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

### 22.3 Common Pitfalls in Cross-Domain Causal Analysis

1. **Ecological fallacy:** Relationships observed at aggregate level may not hold at individual level
2. **Omitted variable bias:** Cross-domain chains almost always have confounders
3. **Endogeneity:** Many relationships are bidirectional (conflict -> food insecurity -> conflict)
4. **Publication bias:** Positive findings (significant effects) are more likely to be published
5. **Spatial and temporal scale sensitivity:** Results can change dramatically with different aggregation choices
6. **Simpson's paradox:** Aggregated trends can reverse at disaggregated levels

---

## 23. Implications for Causal Atlas

### 23.1 Which Causal Chains to Prioritize

Based on the evidence strength, data availability, and relevance to our spatiotemporal grid approach:

| Chain | Evidence Strength | Data Availability | Grid Compatibility | Priority |
|-------|------------------|-------------------|-------------------|----------|
| Climate -> Food prices -> Conflict | Strong | Excellent (CHIRPS, ACLED, WFP) | High (PRIO-GRID proven) | **Highest** |
| ENSO -> Multi-domain cascade | Strong | Excellent (ONI, CHIRPS, FAO, ACLED) | High | **Highest** |
| PM2.5 -> Respiratory mortality | Very strong | Good (OpenAQ, satellite, WHO) | High | **High** |
| Food price spikes -> Unrest | Strong | Good (FAO, ACLED) | Medium (national prices) | **High** |
| Temperature -> Labor productivity -> Economic output | Strong | Good (ERA5, ILO, nightlights) | High | **High** |
| Mining -> Conflict (Africa) | Moderate | Good (mining DB, ACLED, commodity prices) | High (0.5deg proven) | **High** |
| Climate -> Migration | Moderate | Fair (limited spatial migration data) | Medium | Medium |
| Earthquake -> Economic disruption | Strong | Good (USGS, nightlights) | High | Medium |
| Night lights -> Economic activity -> Stability | Moderate | Excellent (VIIRS, DMSP) | High | Medium |
| Water scarcity -> Conflict | Moderate | Good (GRACE-FO, CHIRPS, Pacific Institute) | Medium | Medium |
| Land degradation -> Long chain -> Conflict | Moderate | Fair (NDVI, FAO, IDMC) | Medium | Medium |
| Disease -> Economic cascade | Strong | Fair (WHO, World Bank) | Medium | Medium |
| Sea level rise -> Agricultural loss -> Displacement | Moderate | Good (satellite, GRACE, FAO) | Medium | Medium |
| Pandemic -> Supply chain -> Food prices | Strong (COVID data) | Good (FAO, WFP, WHO) | Low (global chains) | Medium |
| Social media -> Protest mobilization | Moderate | Fair (GDELT, social media APIs) | Low | Lower |
| Volcanic eruption -> Climate -> Agriculture | Strong (historical) | Good (GVP, satellite) | Medium | Lower |
| Lead -> Crime | Very strong but historical | Limited ongoing data | Low | Low |

### 23.2 Recommended Lag Windows to Test

Based on the literature review, the Causal Atlas system should test the following lag windows:

- **Short (0-3 months):** Acute climate events -> conflict, price shocks -> unrest, pollution -> acute health
- **Medium (3-12 months):** Growing season drought -> conflict, food production -> prices, disease -> economic
- **Long (1-5 years):** Climate trends -> migration, urbanization -> pollution -> health, economic disruption -> recovery
- **Very long (5-25 years):** Lead exposure -> crime, deforestation -> climate feedback, tipping point cascades

### 23.3 Key Variables to Include in Grid Cells

From the literature, the following variables at grid-cell level are most frequently used and most informative:

- **Climate:** Temperature anomaly, precipitation anomaly, SPEI drought index, growing season conditions
- **Vegetation:** NDVI (vegetation health proxy for agricultural production)
- **Conflict:** Event count (ACLED/UCDP-GED), fatalities, event type
- **Economic:** Nighttime light intensity (proxy for economic activity), food prices (nearest market)
- **Pollution:** PM2.5 (satellite-derived or ground station), NO2
- **Health:** Disease incidence where available
- **Population:** Population density, urbanization level
- **Context:** Agricultural dependence, political exclusion, governance quality (typically at admin-1 or national level)

### 23.4 Methodological Recommendations

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

### Chain 9: Water Scarcity -> Conflict
- Gleick, P.H. Water Conflict Chronology. Pacific Institute. https://pacinst.org/water-conflict-chronology/
- Petersen-Perlman, J.D., Veilleux, J.C., & Wolf, A.T. (2017). International water conflict and cooperation: challenges and opportunities. *Water International*, 42(2), 105-120.
- Ide, T. et al. (2021). Pathways to water conflict during drought in the MENA region. *Journal of Peace Research*, 58(3).

### Chain 10: Night Lights -> Economy -> Stability
- Henderson, J.V., Storeygard, A., & Weil, D.N. (2012). Measuring economic growth from outer space. *American Economic Review*, 102(2), 994-1028.
- IMF (2022). Measuring quarterly economic growth from outer space. *IMF Working Papers*, 2022/109.

### Chain 11: Land Degradation -> Conflict (long chain)
- UNCCD (2022). Global Land Outlook 2. https://www.unccd.int/resources/global-land-outlook/overview

### Chain 12: Mining -> Conflict
- Berman, N., Couttenier, M., Rohner, D., & Thoenig, M. (2017). This mine is mine! How minerals fuel conflicts in Africa. *American Economic Review*, 107(6), 1564-1610.

### Chain 13: Temperature -> Labor Productivity -> Economy
- Burke, M., Hsiang, S.M., & Miguel, E. (2015). Global non-linear effect of temperature on economic production. *Nature*, 527, 235-239.
- Dell, M., Jones, B.F., & Olken, B.A. (2012). Temperature shocks and economic growth. *American Economic Journal: Macroeconomics*, 4(3), 66-95.
- ILO (2019). Working on a warmer planet: The impact of heat stress on labour productivity and decent work.

### Chain 14: Sea Level Rise -> Displacement
- IPCC (2019). Special Report on the Ocean and Cryosphere in a Changing Climate, Chapter 4.

### Chain 15: Pandemic -> Food Prices -> Unrest
- Various COVID-19 supply chain studies (2020-2023). See Section 16.

### Chain 16: ENSO -> Multi-Domain Cascade
- Hsiang, S., Meng, K., & Cane, M. (2011). Civil conflicts are associated with the global climate. *Nature*, 476, 438-441.

### Chain 17: Volcanic Eruptions -> Climate -> Agriculture
- Kandlbauer, J. & Sparks, R. (2013). Climate and carbon cycle response to the 1815 Tambora volcanic eruption. *JGR Atmospheres*.

### Novel and Emerging Pathways
- Lenton, T.M. et al. (2019). Climate tipping points — too risky to bet against. *Nature*, 575, 592-595.
- Armstrong McKay, D.I. et al. (2022). Exceeding 1.5degC global warming could trigger multiple climate tipping points. *Science*, 377(6611).
- Wunderling, N. et al. (2024). Climate tipping point interactions and cascades: a review. *Earth System Dynamics*, 15, 41-66.
- IPBES (2019). Global Assessment Report on Biodiversity and Ecosystem Services.

### IPCC AR6 and Major Reviews
- IPCC (2022). Climate Change 2022: Impacts, Adaptation and Vulnerability. Working Group II, Chapter 16.
- Koubi, V. (2019). Climate change and conflict. *Annual Review of Political Science*, 22, 343-360.
- Von Uexkull, N. & Buhaug, H. (2021). Security implications of climate change: A decade of scientific progress. *Journal of Peace Research*, 58(1), 21-32.
- Von Uexkull, N. & Buhaug, H. (2021). Vicious circles: Violence, vulnerability, and climate change. *Annual Review of Environment and Resources*, 46, 169-192.
- Adams, C. et al. (2018). Sampling bias in climate-conflict research. *Nature Climate Change*, 8(3), 200-203.

### Cross-Domain Methods
- Runge, J. et al. (2019). Detecting and quantifying causal associations in large nonlinear time series datasets. *Science Advances*, 5(11), eaau4996.
- Dell, M., Jones, B.F., & Olken, B.A. (2012). Temperature shocks and economic growth. *American Economic Journal: Macroeconomics*, 4(3), 66-95.
- Burke, M., Hsiang, S.M., & Miguel, E. (2015). Global non-linear effect of temperature on economic production. *Nature*, 527, 235-239.
