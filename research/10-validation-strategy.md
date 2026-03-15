# Validation Strategy: How to Validate Discovered Causal Relationships

> **Last updated:** March 2026
> **Status:** Deep research — validation framework design for Causal Atlas
> **Purpose:** Define a rigorous, multi-layered validation strategy for causal relationships discovered by the Causal Atlas platform, ensuring that novel findings are credible before being presented as discoveries. This document addresses false positive control, robustness checking, cross-validation, simulation-based testing, ethical reporting, and automated pipeline design.

---

## Table of Contents

1. [The Validation Problem](#1-the-validation-problem)
2. [Known Ground Truth Benchmarks](#2-known-ground-truth-benchmarks)
3. [Negative Controls](#3-negative-controls)
4. [Multiple Testing Correction](#4-multiple-testing-correction)
5. [Cross-Validation Approaches](#5-cross-validation-approaches)
6. [Robustness Checks](#6-robustness-checks)
7. [Comparison with Published Findings](#7-comparison-with-published-findings)
8. [Simulation-Based Validation](#8-simulation-based-validation)
9. [Expert Review and Community Validation](#9-expert-review-and-community-validation)
10. [Automated Validation Pipeline](#10-automated-validation-pipeline)
11. [Reporting Standards](#11-reporting-standards)
12. [Ethical Considerations](#12-ethical-considerations)
13. [Sources](#13-sources)

---

## 1. The Validation Problem

### 1.1 Why Validation Is Essential

Causal Atlas will test hundreds of variable pairs across 259,200 PRIO-GRID cells at multiple lag orders. At this scale, the false positive problem is not an edge case — it is the central challenge. Without rigorous validation, the platform will generate a flood of spurious "discoveries" that are artefacts of multiple testing, spatial autocorrelation, shared confounders, or temporal trends.

The key threats to validity in spatiotemporal causal discovery are:

| Threat | Description | Example |
|--------|-------------|---------|
| **Multiple testing** | Testing millions of hypotheses guarantees false positives at any conventional significance level | 259,200 cells x 100 variable pairs x 12 lags = 311 million tests |
| **Spatial autocorrelation** | Nearby grid cells are not independent observations, inflating effective sample sizes and producing clustered false positives | Rainfall in adjacent 0.5 degree cells is highly correlated |
| **Temporal autocorrelation** | Time series in adjacent months are correlated, violating independence assumptions of many tests | GDP does not change independently month to month |
| **Shared confounders** | Two variables may correlate because they share a common driver, not because one causes the other | Rainfall drives both crop yield and disease, making crop yield and disease appear causally linked |
| **Temporal trends** | Shared upward or downward trends create spurious correlation | Population growth drives both urbanisation and CO2, creating a spurious urbanisation-CO2 link |
| **Selection bias** | Reporting only significant results from many tests overstates the evidence | The "file drawer" problem |

### 1.2 The Base Rate Problem

Most correlations in a high-dimensional spatiotemporal dataset are spurious. If the true base rate of genuine causal relationships among all tested pairs is 0.1%, then even a test with 95% specificity will produce far more false positives than true positives:

- 311 million tests x 0.1% true causal = ~311,000 true relationships
- 311 million tests x 99.9% non-causal x 5% false positive rate = ~15.5 million false positives
- **Precision (positive predictive value) = 311,000 / (311,000 + 15,500,000) = 2%**

This means 98% of "significant" findings would be false positives at p < 0.05 without correction. This is not hypothetical — it is the reality of large-scale observational analysis.

### 1.3 Philosophical Framing

Observational data can suggest but cannot prove causation in the interventionist sense. The causal hierarchy, as laid out in the existing `04-statistical-methods.md`, ranges from association through predictive causality to structural causality to interventionist causality. Causal Atlas operates primarily at the predictive and structural levels. We must be transparent about this limitation.

The appropriate epistemic stance is: "We have found a statistically robust, temporally ordered, spatially coherent association between X and Y that is consistent with X causing Y, that replicates out of sample, and that is consistent with published domain knowledge. We have not proven causation."

### 1.4 The "Garden of Forking Paths"

Gelman and Loken (2013) demonstrated that researchers can inadvertently inflate false positive rates through a "garden of forking paths" — the many implicit decisions made during data analysis that are contingent on the data itself. In spatiotemporal analysis, these researcher degrees of freedom are particularly numerous:

- **Spatial resolution:** 0.25 degree, 0.5 degree, 1 degree, country level?
- **Temporal resolution:** Daily, monthly, quarterly, annual?
- **Lag structure:** 1 month, 3 months, 6 months, 12 months? Test all?
- **Variable transformation:** Raw values, anomalies, z-scores, first differences, log-transform?
- **Detrending:** Linear detrend, polynomial, seasonal decomposition?
- **Spatial aggregation:** Grid cell, admin-1, admin-2, country?
- **Time window:** Full period, or subset? Include COVID years or not?
- **Conditional independence test:** Partial correlation, GPDC, CMI-knn?
- **Significance threshold:** 0.05, 0.01, 0.001?

Each choice is defensible in isolation, but the combination of choices creates an enormous space of possible analyses. If any combination produces a significant result, reporting only that combination constitutes implicit p-hacking even without conscious intent.

**Mitigation for Causal Atlas:** Pre-specify the primary analysis pipeline (spatial resolution, temporal resolution, lag range, variable transformations, significance threshold) before running analyses. Document all choices. Treat deviations from the pre-specified pipeline as exploratory analyses requiring additional validation.

**Key reference:** Gelman, A. and Loken, E. (2013). "The garden of forking paths: Why multiple comparisons can be a problem, even when there is no 'fishing expedition' or 'p-hacking' and the research hypothesis was posited ahead of time." Columbia University Department of Statistics. ([PDF](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf))

---

## 2. Known Ground Truth Benchmarks

Before trusting Causal Atlas to discover novel relationships, we must demonstrate that it correctly recovers relationships that are already well-established in the literature. These serve as positive controls — if the system cannot find these, something is wrong with the methodology.

### 2.1 Rainfall to Crop Yield

| Attribute | Detail |
|-----------|--------|
| **Datasets** | CHIRPS rainfall x FAO crop production statistics (or MODIS NDVI as proxy for yield) |
| **Expected direction** | Positive (more rainfall = higher yield), with non-linearity at extremes (flooding reduces yield) |
| **Expected lag** | 0-3 months (within growing season) |
| **Expected magnitude** | Strong (R-squared 0.3-0.6 in rainfed agriculture zones) |
| **Spatial extent** | Strongest in Sub-Saharan Africa, South Asia, and other rainfed agriculture regions |
| **Key papers** | Lobell et al. (2011), "Climate Trends and Global Crop Production Since 1980," Science; Ray et al. (2015), "Climate variation explains a third of global crop yield variability," Nature Communications |
| **Notes** | Weakest in irrigated areas. Must control for irrigation. Non-linear: beneficial up to optimum, harmful beyond. |
| **Validation criterion** | System should detect a significant positive association at 0-3 month lag in rainfed zones, with declining or absent signal in irrigated zones |

### 2.2 Earthquake to Building Damage and Losses

| Attribute | Detail |
|-----------|--------|
| **Datasets** | USGS ShakeMap (peak ground acceleration) x EM-DAT disaster losses |
| **Expected direction** | Positive (stronger shaking = more damage) |
| **Expected lag** | 0 months (near-instantaneous) |
| **Expected magnitude** | Very strong, nearly deterministic for large events |
| **Spatial extent** | Global, along tectonic plate boundaries |
| **Key papers** | Jaiswal and Wald (2010), "An Empirical Model for Global Earthquake Fatality Estimation," Earthquake Spectra |
| **Notes** | Confounded by building quality, population density, time of day. But the physical relationship is direct. |
| **Validation criterion** | System should detect a strong, zero-lag positive association. If it does not, the spatial or temporal alignment is likely wrong. |

### 2.3 Drought (SPI) to Food Prices

| Attribute | Detail |
|-----------|--------|
| **Datasets** | CHIRPS-derived Standardised Precipitation Index (SPI-3 or SPI-6) x WFP food price monitoring data |
| **Expected direction** | Negative SPI (drought) leads to higher food prices |
| **Expected lag** | 3-6 months (time for harvest failure to propagate through markets) |
| **Expected magnitude** | Moderate (effect mediated by market integration, trade, reserves) |
| **Spatial extent** | Strongest in food-deficit, market-isolated regions (e.g. Sahel, Horn of Africa) |
| **Key papers** | Bren d'Amour et al. (2016), "Teleconnected food supply shocks," Environmental Research Letters; WFP uses SPI-6 with CHIRPS for drought insurance triggers |
| **Notes** | WFP's Sahel Climate Catastrophe Layer uses SPI-6 from CHIRPS as its backup index for insurance products, confirming the operational validity of this relationship |
| **Validation criterion** | System should detect a significant association at 3-6 month lag, stronger in isolated markets than well-connected urban centres |

### 2.4 ENSO to Regional Rainfall Anomalies

| Attribute | Detail |
|-----------|--------|
| **Datasets** | Oceanic Nino Index (ONI) x CHIRPS regional rainfall |
| **Expected direction** | El Nino (positive ONI) = drought in Eastern Africa, Indonesia, Australia; excess rainfall in Horn of Africa (short rains), western South America |
| **Expected lag** | 1-3 months (atmospheric teleconnection propagation) |
| **Expected magnitude** | Strong for established teleconnection regions |
| **Spatial extent** | Well-mapped teleconnection patterns, strongest in tropics |
| **Key papers** | Ropelewski and Halpert (1987), "Global and Regional Scale Precipitation Patterns Associated with the El Nino/Southern Oscillation," Monthly Weather Review |
| **Notes** | Teleconnections are region-specific. The system should recover the correct sign for each region. ENSO teleconnections are robust and have been validated using hypergeometric tests on empirical probabilities. |
| **Validation criterion** | System should detect ENSO associations in known teleconnection regions with correct sign and 1-3 month lag. Should NOT detect associations in regions without known teleconnections. |

### 2.5 Conflict to Nightlight Decline

| Attribute | Detail |
|-----------|--------|
| **Datasets** | ACLED conflict events x VIIRS nighttime lights monthly composites |
| **Expected direction** | Conflict onset leads to reduced nightlight radiance |
| **Expected lag** | 0-2 months |
| **Expected magnitude** | Moderate to strong in zones of active conflict |
| **Spatial extent** | Documented in Syria, Iraq, Ukraine, Yemen, Nigeria, and elsewhere |
| **Key papers** | Li et al. (2013), "Detecting changes in night-time light associated with geopolitical disturbances using DMSP-OLS"; research on Ukraine conflict using VIIRS with territorial control maps, visual damage reports; recent work on VIIRS + anthropogenic CO2 monitoring during geopolitical conflicts (2025) |
| **Notes** | Cloud interference is a significant confound in tropical regions. Monthly composites mitigate but do not eliminate this. Difference-in-difference approaches are best for causal inference here. |
| **Validation criterion** | System should detect conflict-associated nightlight decline at 0-2 month lag in known conflict zones |

### 2.6 Conflict to Displacement

| Attribute | Detail |
|-----------|--------|
| **Datasets** | ACLED (or UCDP-GED) conflict events x IDMC/UNHCR displacement data |
| **Expected direction** | Increased conflict leads to increased displacement |
| **Expected lag** | 0-3 months (immediate displacement during active conflict, with reporting delays) |
| **Expected magnitude** | Strong, but with significant threshold effects (low-level conflict may not trigger displacement) |
| **Spatial extent** | Global, strongest in regions with active armed conflict |
| **Key papers** | IDMC analysis (2023), "Can we predict conflict displacement?"; logistic models using ACLED data to predict large-scale displacement over 3-month windows |
| **Notes** | IDMC data shows many months where conflict was recorded but no displacement was reported, suggesting threshold effects and lag. Models using UCDP and ACLED variables measure total or civilian deaths for the last 1, 3, 6, and 9 months alongside displacement counts. |
| **Validation criterion** | System should detect a positive association, strongest at 0-3 month lag, with evidence of threshold effects |

### 2.7 Temperature to Agricultural Productivity

| Attribute | Detail |
|-----------|--------|
| **Datasets** | ERA5 or CPC temperature data x FAO crop yields or MODIS NDVI |
| **Expected direction** | Non-linear: beneficial up to crop-specific optimum, then sharply harmful |
| **Expected lag** | Within growing season (0-3 months) |
| **Expected magnitude** | Strong non-linear effect. Yields increase up to 29 degrees C for corn, 30 degrees C for soybeans, 32 degrees C for cotton, then decline steeply. |
| **Spatial extent** | Global, but strongest in already-warm regions |
| **Key papers** | Schlenker and Roberts (2009), "Nonlinear temperature effects indicate severe damages to U.S. crop yields under climate change," PNAS, 106, 15594-15598 |
| **Notes** | The asymmetry is crucial: the slope of decline above the optimum is significantly steeper than the incline below it. Linear methods will miss or underestimate this relationship. This benchmark specifically tests whether the system can detect non-linear causal effects. |
| **Validation criterion** | System should detect a temperature-yield association. If using linear methods only, the non-linearity will be missed, which is itself informative. |

### 2.8 Summary: Benchmark Validation Matrix

| Benchmark | Datasets | Direction | Lag | Magnitude | Key Test |
|-----------|----------|-----------|-----|-----------|----------|
| Rainfall to yield | CHIRPS x FAO/NDVI | + | 0-3 mo | Strong | Rainfed vs irrigated |
| Earthquake to damage | USGS x EM-DAT | + | 0 mo | Very strong | Near-deterministic |
| Drought to food prices | SPI x WFP | - SPI to + price | 3-6 mo | Moderate | Isolated vs connected markets |
| ENSO to rainfall | ONI x CHIRPS | Region-specific | 1-3 mo | Strong | Correct sign by region |
| Conflict to nightlights | ACLED x VIIRS | - | 0-2 mo | Moderate-strong | Known conflict zones |
| Conflict to displacement | ACLED x IDMC | + | 0-3 mo | Strong | Threshold effects |
| Temperature to ag productivity | Temp x yield | Non-linear | 0-3 mo | Strong | Non-linearity detection |

**Minimum viability criterion:** Causal Atlas must correctly recover at least 5 of 7 benchmark relationships with the correct direction and approximate lag structure before any novel findings are reported.

---

## 3. Negative Controls

Negative controls are relationships that should NOT be detected. If the system finds them, it indicates a methodological problem (spatial leakage, temporal confounding, or insufficient correction for multiple testing).

### 3.1 Geographic Independence Tests

- **Earthquakes in East Africa should not correlate with rainfall in South America** (unless mediated through ENSO, which should be controlled for)
- **Conflict in the Democratic Republic of Congo should not predict wheat prices in Canada** (no plausible causal pathway)
- **Air quality in Beijing should not predict displacement in Central America** (no pathway)

If any of these associations appear significant, it suggests:
- Shared global trends have not been adequately removed
- Multiple testing correction is insufficient
- There is a global confounder (e.g. COVID-19 pandemic) creating spurious links

### 3.2 Temporal Permutation Tests

Randomly shuffling the temporal order of one variable while preserving the other should destroy any genuine causal signal. This is the most basic negative control:

```python
# Pseudocode for temporal permutation test
import numpy as np

def permutation_test(x, y, n_permutations=1000, causal_method=pcmci_test):
    """
    Test whether the causal association between x and y
    is stronger than expected by chance.
    """
    observed_statistic = causal_method(x, y)

    null_distribution = []
    for _ in range(n_permutations):
        # Shuffle time indices of x, breaking temporal alignment
        x_permuted = np.random.permutation(x)
        null_stat = causal_method(x_permuted, y)
        null_distribution.append(null_stat)

    # p-value: fraction of null statistics >= observed
    p_value = np.mean(np.array(null_distribution) >= observed_statistic)
    return p_value, null_distribution
```

**Important caveat:** Simple permutation of autocorrelated time series does not preserve the autocorrelation structure. This can lead to conservative tests (genuine signals may also appear in permuted data if autocorrelation creates pseudo-structure). Better approaches include:

- **Block permutation:** Shuffle blocks of consecutive time steps rather than individual observations, preserving short-range autocorrelation
- **Phase randomisation:** Randomise the phase spectrum of the time series while preserving the amplitude spectrum (and hence the autocorrelation structure)
- **Floating Grid Permutation Technique (FGPT):** Randomise observations with known geographical locations while preserving spatial autocorrelation structure (Radersma and Sheldon, 2015)

### 3.3 Spatial Permutation Tests

Randomly reassign grid cell identities while preserving temporal structure. If a causal signal persists after spatial permutation, it indicates a global (non-spatial) trend rather than a spatially specific causal relationship.

### 3.4 Constructing Proper Negative Controls

For spatiotemporal data, negative controls must account for the correlation structure. A rigorous negative control strategy:

1. **Identify variable pairs with no plausible causal pathway** based on domain knowledge
2. **Test these pairs using the same pipeline** as candidate causal relationships
3. **The rate of significant findings among negative controls** estimates the false positive rate of the pipeline
4. **If the false positive rate exceeds the nominal alpha level**, the pipeline needs recalibration

**Target:** False positive rate among negative controls should be at or below 5% (or whatever the nominal alpha level is). If testing at FDR = 0.05, no more than 5% of negative control pairs should be flagged.

### 3.5 Placebo Tests

Following the framework of Eggers et al. (2024), "Placebo Tests for Causal Inference" (American Journal of Political Science):

- **Placebo outcome:** Replace the outcome variable with a variable that should not be affected by the treatment. If the treatment "affects" the placebo outcome, confounding is likely.
- **Placebo treatment:** Replace the treatment with a variable that should not cause the outcome. If the placebo treatment appears to cause the outcome, the model is misspecified.
- **Placebo population:** Apply the analysis to a population where the causal mechanism should not operate. If the effect persists, it is likely artefactual.

**Caution:** Eggers et al. note that placebo tests are subject to the "difference between significant and non-significant is not itself statistically significant" problem. A non-significant placebo result does not prove the absence of confounding — it only fails to detect it.

---

## 4. Multiple Testing Correction

### 4.1 The Scale of the Problem

Causal Atlas operates at a scale that makes multiple testing correction essential and non-trivial:

| Component | Count |
|-----------|-------|
| Grid cells (0.5 degree global) | ~259,200 |
| Variable pairs (conservative) | ~100 |
| Lag orders (1-12 months) | 12 |
| **Total potential tests** | **~311 million** |

Even at p < 0.001, we would expect ~311,000 false positives by chance alone.

### 4.2 Bonferroni Correction

The simplest approach: divide the significance threshold by the number of tests.

- Adjusted threshold: 0.05 / 311,000,000 = 1.6 x 10^-10
- **Problem:** Bonferroni assumes independent tests. Spatially autocorrelated data violates this assumption severely. Adjacent grid cells are correlated, so the effective number of independent tests is much smaller than 311 million.
- **Consequence:** Bonferroni is far too conservative for spatially correlated data, leading to unacceptably high false negative rates. True clusters will be largely missed.

**When to use:** Only when a quick, conservative bound is needed and false negatives are acceptable. Not suitable as the primary correction method for Causal Atlas.

### 4.3 False Discovery Rate (FDR) — Benjamini-Hochberg Procedure

FDR controls the expected proportion of false positives among all rejected hypotheses, rather than the probability of any single false positive:

```python
from statsmodels.stats.multitest import multipletests

# p_values: array of p-values from all tests
rejected, p_adjusted, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
```

**Advantages for spatial data:**
- Much more powerful than Bonferroni
- Controls a more relevant quantity (proportion of false discoveries, not probability of any false discovery)
- Caldas de Castro and Singer (2006) demonstrated that FDR gives a significantly better picture of meaningful spatial clusters than either no adjustment or Bonferroni

**Limitation:** The standard Benjamini-Hochberg procedure assumes independence or positive regression dependency among test statistics. Spatial autocorrelation creates complex dependency structures that may not satisfy this assumption.

**Reference:** Caldas de Castro, M. and Singer, B.H. (2006). "Controlling the False Discovery Rate: A New Application to Account for Multiple and Dependent Tests in Local Statistics of Spatial Association." Geographical Analysis, 38(2), 180-208.

### 4.4 Spatial FDR Corrections

Several approaches extend FDR to account for spatial correlation:

1. **Benjamini-Yekutieli (BY) procedure:** Controls FDR under arbitrary dependency structure. More conservative than BH but valid for any correlation pattern.
   ```python
   rejected, p_adjusted, _, _ = multipletests(p_values, alpha=0.05, method='fdr_by')
   ```

2. **Effective number of independent tests:** Estimate the effective number of independent spatial units using Moran's I or semivariogram range, then apply BH with the reduced count.

3. **Cluster-based thresholding:** Rather than correcting each grid cell individually, identify spatial clusters of significant cells and test whether the cluster extent exceeds what would be expected by chance. This is standard in neuroimaging (random field theory) and applicable to geospatial data.

4. **Anselin's approach for LISA:** For local indicators of spatial association (Moran's I), Anselin (2019) recommends combining FDR adjustments with more stringent significance cutoffs (0.001, 0.005, 0.01 rather than the conventional 0.01, 0.05, 0.1), preferring the term "interesting" over "significant."

### 4.5 Permutation-Based Significance Testing

Instead of relying on parametric p-values, generate the null distribution empirically:

1. Permute the data (using block permutation or phase randomisation to preserve autocorrelation structure)
2. Run the full analysis pipeline on permuted data
3. Repeat 1000+ times
4. The p-value is the fraction of permuted datasets that produce a test statistic as extreme as observed

**Advantages:**
- Makes no distributional assumptions
- Naturally accounts for the correlation structure if permutation preserves it
- Accounts for the full pipeline, not just individual tests

**Disadvantages:**
- Computationally expensive at scale (1000 permutations x 311 million tests)
- Autocorrelated data is not exchangeable, so naive permutation is not exact

**Practical approach for Causal Atlas:** Use permutation testing for candidate relationships that survive FDR correction, not as the primary screening step.

### 4.6 How PCMCI/Tigramite Handles Multiple Testing

PCMCI (the primary causal discovery method recommended in `04-statistical-methods.md`) has built-in multiple testing control:

1. **Condition-selection phase (PC1):** The iterative PC algorithm selects a superset of parents for each variable, dramatically reducing the number of subsequent tests.
2. **MCI test:** The Momentary Conditional Independence test conditions on estimated parents, which empirically controls false positives well even for highly autocorrelated variables.
3. **FDR correction:** MCI p-values can be corrected using Benjamini-Hochberg within Tigramite.

This two-step design is a significant advantage: by first identifying relevant conditioning variables and then testing causal links conditional on parents, PCMCI achieves much better false positive control than methods that test all variable pairs unconditionally.

**Reference:** Runge, J. et al. (2019). "Detecting and quantifying causal associations in large nonlinear time series datasets." Science Advances, 5(11), eaau4996.

### 4.7 Practical Guidance: How Many Tests Are We Actually Running?

The 311 million figure is an upper bound. In practice, the number of effective tests is much smaller:

- **PCMCI reduces tests:** The PC condition-selection step eliminates most candidate links before the MCI test is applied
- **Spatial clustering:** Treating spatial clusters as single units reduces the number of spatial tests
- **Variable grouping:** Testing domain-level associations (e.g. "drought to food prices" rather than cell-by-cell) reduces the dimensionality
- **Focus regions:** Initial analyses may focus on specific regions (e.g. Sahel, Horn of Africa) rather than global coverage

**Recommended approach:** Report both the raw number of tests and the effective number of tests (after accounting for spatial autocorrelation and the PCMCI filtering step). Use FDR correction on the effective number.

---

## 5. Cross-Validation Approaches

### 5.1 Temporal Holdout

Split the time series into training and test periods:

| Split | Training Period | Test Period | Purpose |
|-------|----------------|-------------|---------|
| Primary | 2000-2017 | 2018-2024 | Do discovered relationships hold out of sample? |
| Sensitivity | 2000-2012 | 2013-2024 | Does the split point matter? |
| Recent focus | 2005-2019 | 2020-2024 | Robustness through COVID-era disruptions? |

**Key question:** If a causal relationship is discovered in the training period, does it replicate in the test period with the same direction, similar lag, and similar magnitude?

**What to report:**
- Effect size in training vs test period (with confidence intervals)
- Whether the relationship remains statistically significant in the test period
- Whether the lag structure is consistent
- If the relationship weakens or reverses, this is informative (the causal structure may be non-stationary)

### 5.2 Spatial Holdout

Train on one region, test on another where the same causal mechanism should operate:

| Training Region | Test Region | Mechanism Being Tested |
|----------------|-------------|----------------------|
| East Africa | West Africa | Drought to food prices |
| Syria/Iraq | Ukraine | Conflict to nightlight decline |
| South Asia | Southeast Asia | Temperature to crop yield |
| Global tropics (50% cells) | Remaining 50% | ENSO teleconnections |

**Important caveat:** Not all causal relationships are expected to generalise across regions. Drought-to-food-prices should generalise across food-deficit regions but may fail in regions with robust trade networks. This is informative, not a failure.

### 5.3 Leave-One-Country-Out Cross-Validation

For country-level analyses:

1. Fit the model on all countries except one
2. Predict the held-out country
3. Repeat for each country
4. Report the distribution of prediction accuracy across countries

This tests whether relationships are driven by a few influential countries or are truly general.

### 5.4 Rolling Window Validation

Apply causal discovery to rolling temporal windows (e.g. 10-year windows, sliding by 1 year):

```
Window 1: 2000-2009 → Discover causal structure
Window 2: 2001-2010 → Discover causal structure
...
Window N: 2015-2024 → Discover causal structure
```

**Purpose:** Detect whether the causal structure is stationary or evolving. For example:
- Climate-conflict links may strengthen as climate change intensifies
- Trade liberalisation may weaken local drought-to-food-price links
- New infrastructure (irrigation) may decouple rainfall from yield

Rolling windows that show a consistent causal structure are more trustworthy than those showing intermittent significance. Non-stationarity is itself a finding worth reporting.

### 5.5 k-Fold Spatiotemporal Cross-Validation with Blocking

Standard k-fold cross-validation is invalid for spatiotemporal data because it assumes independence. If training data includes observations that are spatially or temporally adjacent to test observations, information leaks from train to test, and performance is overestimated.

**Solution: Spatial and temporal blocking.**

The key principle (from the blockCV package and the spacv Python library):

1. **Spatial blocking:** Divide the study area into spatially contiguous blocks. All observations within a block go into the same fold. Block size should exceed the range of spatial autocorrelation (estimated from a semivariogram).

2. **Temporal blocking:** All observations within a temporal block go into the same fold. Block size should exceed the range of temporal autocorrelation.

3. **Spatiotemporal blocking:** Combine spatial and temporal blocks, ensuring that no fold shares both spatial and temporal proximity with another fold.

**Python implementation:**

- **spacv** ([github.com/SamComber/spacv](https://github.com/SamComber/spacv)): Provides spatial cross-validation in Python, including spatial blocking, spatial buffering, and spatial clustering approaches.
- **scikit-learn GroupKFold:** Can be used with spatial block assignments as group labels.

**Key reference:** Valavi, R. et al. (2019). "blockCV: An R package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models." Methods in Ecology and Evolution, 10, 225-232.

**Adapting for Causal Atlas:**

```python
# Pseudocode for spatiotemporal blocked cross-validation
from sklearn.model_selection import GroupKFold
import numpy as np

def create_spatiotemporal_blocks(grid_cells, timestamps,
                                  spatial_block_size_deg=5.0,
                                  temporal_block_size_months=24):
    """
    Assign each observation to a spatiotemporal block.
    Block size should exceed autocorrelation range.
    """
    spatial_block = (grid_cells.lat // spatial_block_size_deg).astype(int) * 1000 + \
                    (grid_cells.lon // spatial_block_size_deg).astype(int)
    temporal_block = timestamps // temporal_block_size_months
    # Combine into unique block IDs
    block_id = spatial_block * 10000 + temporal_block
    return block_id

# Use GroupKFold with block assignments
block_ids = create_spatiotemporal_blocks(grid_cells, timestamps)
gkf = GroupKFold(n_splits=5)
for train_idx, test_idx in gkf.split(X, y, groups=block_ids):
    # Train and evaluate causal discovery on each fold
    pass
```

---

## 6. Robustness Checks

These are the standard academic robustness checks that any credible causal claim should survive. A finding that is significant under one specification but not under reasonable alternatives is fragile and should be downgraded.

### 6.1 Alternative Lag Specifications

Does the result hold with different lag orders?

- Test at lags 1, 2, 3, 6, 9, 12 months
- The primary lag should be the strongest, with a gradual decay at longer and shorter lags
- If the result appears only at an unusual lag (e.g. exactly 7 months) with no signal at adjacent lags, it is likely spurious
- **Pattern to expect:** A smooth lag-response curve peaking at the true causal lag

### 6.2 Alternative Spatial Scales

Does the result hold at different spatial resolutions?

| Scale | Resolution | Purpose |
|-------|-----------|---------|
| Fine | 0.25 degree | More spatial detail, smaller sample per cell |
| Primary | 0.5 degree (PRIO-GRID) | Standard analysis resolution |
| Coarse | 1.0 degree | Aggregated, less noise |
| Admin-1 | Province/state | Policy-relevant units |
| Country | National | Maximum aggregation |

A robust causal relationship should be detectable across spatial scales, though effect size may vary. Relationships that appear only at one specific scale deserve scepticism.

### 6.3 Alternative Datasets

Does the result replicate with different data sources measuring the same construct?

| Construct | Primary Dataset | Alternative Dataset |
|-----------|----------------|-------------------|
| Conflict events | ACLED | UCDP-GED |
| Rainfall | CHIRPS | ERA5 precipitation |
| Temperature | ERA5 | CPC Global Temperature |
| Food prices | WFP VAM | FAO FPMA |
| Vegetation health | MODIS NDVI | VIIRS NDVI |
| Economic activity | World Bank indicators | VIIRS nighttime lights |
| Displacement | IDMC | UNHCR |

If a result holds with ACLED but not UCDP-GED, the finding may be an artefact of dataset-specific coding decisions rather than a genuine causal relationship.

### 6.4 Placebo Tests

Following Eggers et al. (2024):

- **Fake treatment timing:** Shift the hypothesised cause backward or forward in time. If the "causal" effect appears at fake timings too, the result is likely confounded by a shared trend.
  ```
  True timing: Drought in month T → Price increase in month T+4
  Placebo:     Drought in month T-12 → Price increase in month T+4?  (Should be null)
  ```

- **Fake treatment location:** Apply the analysis using the treatment variable from a random, distant grid cell. If the effect persists, it is driven by global trends rather than local causation.

- **Dose-response check:** Is there a monotonic relationship between shock magnitude and outcome magnitude? A true causal effect should show a dose-response pattern. Severe drought should cause larger price increases than mild drought.

### 6.5 Pre-Trend Analysis

Before the hypothesised cause occurs, were the outcomes already diverging? This is critical for difference-in-differences designs:

- Plot the outcome variable for treated and control units in the pre-treatment period
- If the trends are not parallel before treatment, the difference-in-differences estimate is biased
- For spatiotemporal causal discovery, this translates to: was Y already changing before X changed?

### 6.6 Sensitivity to Unobserved Confounders

#### E-Values

The E-value quantifies how strong an unmeasured confounder would need to be to fully explain away an observed association (VanderWeele and Ding, 2017):

- A large E-value means the result is robust to plausible confounding
- A small E-value means even weak confounding could explain the result
- **Rule of thumb:** E-values above 2.0 indicate moderate robustness; above 3.0 indicates strong robustness

**Implementation:** The `evalue` package in R, and the E-value calculator at [evalue-calculator.com](https://evalue-calculator.com/).

**Reference:** VanderWeele, T.J. and Ding, P. (2017). "Sensitivity Analysis in Observational Research: Introducing the E-Value." Annals of Internal Medicine, 167(4), 268-274.

#### Rosenbaum Bounds

For matched observational designs, Rosenbaum bounds determine the threshold of unobserved confounding strength (ORxu and ORyu) that would render the observed association insignificant. If even modest confounding (Gamma = 1.5) could overturn the result, the finding is fragile.

#### Cinelli and Hazlett Sensitivity Analysis

The sensemakr framework (Cinelli and Hazlett, 2020, Journal of the Royal Statistical Society, Series B) extends omitted variable bias analysis for regression models:

- Answers: "How strong would an unobserved confounder need to be — relative to observed covariates — to change the conclusion?"
- Available in R (sensemakr), Stata, and Python
- Produces contour plots showing the combinations of confounder-treatment and confounder-outcome associations that would change inference

**Reference:** Cinelli, C. and Hazlett, C. (2020). "Making Sense of Sensitivity: Extending Omitted Variable Bias." Journal of the Royal Statistical Society, Series B, 82(1), 39-67. ([PDF](https://carloscinelli.com/files/Cinelli%20and%20Hazlett%20(2020)%20-%20Making%20Sense%20of%20Sensitivity.pdf))

### 6.7 Instrumental Variables and Natural Experiments

Where available, instrumental variables provide stronger causal evidence than observational association alone:

- **Rainfall as an instrument for agricultural income** (commonly used in development economics)
- **Distance from fault line as an instrument for earthquake exposure** (geographic instrument)
- **ENSO as a natural experiment for climate shocks** (exogenous climate variation)

Not always available, but when they are, they substantially strengthen causal claims.

---

## 7. Comparison with Published Findings

### 7.1 Systematic Literature Comparison

For each discovered causal chain, the following comparison protocol should be applied:

1. **Search for published studies** on the same X-to-Y relationship (using Google Scholar, Web of Science, Scopus)
2. **Compare direction:** Does our finding agree with published results on the sign of the effect?
3. **Compare magnitude:** Is our effect size in the range of published estimates?
4. **Compare lag structure:** Is the temporal lag consistent with published findings?
5. **Compare spatial variation:** Do we find the relationship in the same regions as published studies?
6. **Flag contradictions:** If our finding contradicts established literature, treat this as requiring additional validation, not as a novel discovery. It could be an error OR a genuine new finding, but the former is more likely a priori.

### 7.2 The Replication Crisis in Climate-Conflict Research: Hsiang vs Buhaug

This debate is directly relevant to Causal Atlas and illustrates the risks of over-claiming from observational data.

**Hsiang, Burke, and Miguel (2013)** published a meta-analysis in Science finding a "remarkable convergence" across 60 studies: each 1-sigma climate deviation increases intergroup conflict by 14%.

**Buhaug et al. (2014)** challenged this meta-analysis, arguing it:
- Selected the strongest climate indicator from each study (when many studies tested multiple indicators with mixed results)
- Used fixed-effect meta-analysis inappropriately given study heterogeneity
- Misrepresented the degree of consensus in the literature

**Hsiang et al.'s response** accused Buhaug et al. of misclassifying studies, making coding errors, and suppressing inconvenient results.

**Buhaug's rejoinder** assessed these claims and found they "largely missed the target," concluding that concerns about the meta-analysis methodology remain valid.

**Lessons for Causal Atlas:**
- The same data can support opposite conclusions depending on analytical choices
- Meta-analytic claims of consensus may overstate agreement
- The climate-conflict link is real but much more heterogeneous and context-dependent than headline findings suggest
- Causal Atlas should present uncertainty and heterogeneity, not just average effects
- Reporting only the strongest specification from multiple alternatives is a form of the garden of forking paths

**Key references:**
- Hsiang, S.M., Burke, M. and Miguel, E. (2013). "Quantifying the Influence of Climate on Human Conflict." Science, 341(6151).
- Buhaug, H. et al. (2014). "One effect to rule them all? A comment on climate and conflict." Climatic Change, 127, 391-397. ([Springer](https://link.springer.com/article/10.1007/s10584-014-1266-1))
- PRIO comment: "Climate and conflict: A Comment on Hsiang et al.'s Reply to Buhaug et al." ([PRIO](https://www.prio.org/publications/7521))

### 7.3 How to Present Findings Responsibly

Causal Atlas should adopt a confidence tier system:

| Confidence Level | Criteria | Presentation |
|-----------------|----------|--------------|
| **Confirmed** | Replicates a well-established finding with correct direction, lag, and approximate magnitude | "Consistent with published literature" |
| **Supported** | Novel finding that passes all robustness checks, survives out-of-sample validation, and has a plausible mechanism | "Novel finding with strong statistical support — domain review recommended" |
| **Suggestive** | Significant after FDR correction, but fails one or more robustness checks, or has no published precedent | "Suggestive association requiring further investigation" |
| **Exploratory** | Significant before but not after FDR correction, or fails multiple robustness checks | "Exploratory finding — likely spurious but potentially interesting" |
| **Not supported** | Fails FDR correction and robustness checks | Not reported (but logged internally for completeness) |

---

## 8. Simulation-Based Validation

### 8.1 Purpose

Before applying the full Causal Atlas pipeline to real data, test it on synthetic data with known ground truth. This allows precise measurement of:

- **False positive rate (Type I error):** Does the system find causal links that do not exist?
- **False negative rate (Type II error):** Does the system miss causal links that do exist?
- **Effect size bias:** Does the system over- or under-estimate the true effect size?
- **Lag recovery accuracy:** Does the system correctly identify the true causal lag?
- **Spatial pattern recovery:** Does the system correctly localise the causal relationship to the right grid cells?

### 8.2 Generating Synthetic PRIO-GRID Data

Create synthetic data on a 0.5 degree grid with planted causal relationships:

```python
import numpy as np
from scipy.ndimage import gaussian_filter

def generate_synthetic_causal_data(
    n_lat=360, n_lon=720,  # 0.5 degree global grid
    n_timesteps=240,        # 20 years monthly
    causal_lag=4,            # 4-month lag
    effect_size=0.3,         # correlation coefficient
    spatial_extent=50,       # number of grid cells with causal link
    noise_spatial_autocorr=2.0,  # sigma for Gaussian spatial smoothing
    seed=42
):
    """
    Generate synthetic spatiotemporal data with a planted causal relationship.

    X causes Y in a specific spatial region, at a specific lag,
    with a specific effect size. Everything else is noise
    (but spatially and temporally autocorrelated noise).
    """
    rng = np.random.RandomState(seed)

    # Generate cause variable X (spatially autocorrelated noise)
    X = np.zeros((n_timesteps, n_lat, n_lon))
    for t in range(n_timesteps):
        raw = rng.randn(n_lat, n_lon)
        X[t] = gaussian_filter(raw, sigma=noise_spatial_autocorr)

    # Add temporal autocorrelation to X
    for t in range(1, n_timesteps):
        X[t] = 0.6 * X[t-1] + 0.4 * X[t]  # AR(1) process

    # Generate effect variable Y (independent noise + causal signal)
    Y = np.zeros((n_timesteps, n_lat, n_lon))
    for t in range(n_timesteps):
        raw = rng.randn(n_lat, n_lon)
        Y[t] = gaussian_filter(raw, sigma=noise_spatial_autocorr)

    # Add temporal autocorrelation to Y
    for t in range(1, n_timesteps):
        Y[t] = 0.6 * Y[t-1] + 0.4 * Y[t]

    # Define causal region (random subset of grid cells)
    causal_mask = np.zeros((n_lat, n_lon), dtype=bool)
    # Pick a contiguous region
    center_lat = rng.randint(50, n_lat - 50)
    center_lon = rng.randint(50, n_lon - 50)
    radius = int(np.sqrt(spatial_extent / np.pi))
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i**2 + j**2 <= radius**2:
                causal_mask[center_lat + i, center_lon + j] = True

    # Plant causal relationship: Y[t] += effect_size * X[t - causal_lag]
    for t in range(causal_lag, n_timesteps):
        Y[t][causal_mask] += effect_size * X[t - causal_lag][causal_mask]

    return X, Y, causal_mask, {
        'lag': causal_lag,
        'effect_size': effect_size,
        'n_causal_cells': causal_mask.sum()
    }
```

### 8.3 Evaluation Metrics for Synthetic Data

| Metric | Definition | Target |
|--------|-----------|--------|
| **True Positive Rate (Sensitivity)** | Fraction of planted causal links correctly detected | > 0.8 |
| **False Positive Rate** | Fraction of non-causal links incorrectly flagged | < 0.05 |
| **Lag Recovery MAE** | Mean absolute error in estimated lag vs true lag | < 1 month |
| **Effect Size Bias** | (Estimated effect - True effect) / True effect | < 20% |
| **Spatial Precision** | Fraction of detected causal cells that are truly causal | > 0.7 |
| **Spatial Recall** | Fraction of truly causal cells that are detected | > 0.7 |

### 8.4 Systematic Simulation Experiments

Run the pipeline across a grid of simulation parameters:

| Parameter | Values to Test |
|-----------|---------------|
| Effect size | 0.05, 0.1, 0.2, 0.3, 0.5 |
| Causal lag | 1, 3, 6, 12 months |
| Spatial autocorrelation | Low, medium, high |
| Temporal autocorrelation | Low (AR coefficient 0.2), medium (0.5), high (0.8) |
| Missing data | 0%, 10%, 30% random missingness |
| Non-linearity | Linear, quadratic, threshold |
| Number of variables | 5, 10, 20, 50 |
| Confounders | 0, 1, 3 unobserved confounders |

This produces a comprehensive performance profile showing where the pipeline is reliable and where it breaks down.

### 8.5 Existing Benchmark Platforms

#### CauseMe Platform

The CauseMe platform ([causeme.uv.es](https://causeme.uv.es/)) provides ground truth benchmark datasets for causal discovery methods, featuring different real data challenges. Developed by Runge, Munoz-Mari, Mateo, and Camps-Valls. Datasets are either generated from synthetic models mimicking real challenges or are real-world data with known causal structure.

**Relevance to Causal Atlas:** CauseMe benchmarks can be used to evaluate PCMCI and other methods before deploying them on real PRIO-GRID data.

#### CausalDiscoveryToolbox (cdt)

The Python package `cdt` ([fentechsolutions.github.io/CausalDiscoveryToolbox](https://fentechsolutions.github.io/CausalDiscoveryToolbox/html/data.html)) provides synthetic data generators with configurable causal mechanisms:

- Causal mechanisms: linear, polynomial, sigmoid, Gaussian process, neural network
- Noise types: additive, multiplicative, mixed
- Graph structures: acyclic graphs of arbitrary complexity

```python
from cdt.data import AcyclicGraphGenerator

generator = AcyclicGraphGenerator(causal_mechanism='linear', noise='gaussian',
                                   npoints=1000, nodes=10, parents_max=3)
data, graph = generator.generate()
# graph contains the true causal adjacency matrix
```

**Limitation:** cdt does not natively support spatiotemporal structure. We would need to extend it with spatial autocorrelation and temporal dynamics.

#### Microsoft CSuite

CSuite ([github.com/microsoft/csuite](https://github.com/microsoft/csuite)) is a collection of synthetic benchmark datasets specifically designed for benchmarking causal ML algorithms. It provides standardised evaluation protocols.

#### tsBNgen

tsBNgen is a Python library for generating synthetic time series data based on arbitrary dynamic Bayesian network structures. Useful for testing temporal causal discovery methods with known ground truth.

#### CausalTime

CausalTime (ICLR 2024) provides realistically generated time-series benchmarks for causal discovery, addressing the criticism that synthetic evaluations often lack realism by generating data with realistic noise patterns and non-linear dynamics.

---

## 9. Expert Review and Community Validation

### 9.1 Domain Expert Review

Statistical significance is necessary but not sufficient for a credible causal claim. Domain expertise is essential for:

- **Mechanism plausibility:** Is there a scientifically plausible mechanism connecting X and Y?
- **Effect size reasonableness:** Is the estimated magnitude in a plausible range?
- **Lag plausibility:** Does the estimated lag make sense given the hypothesised mechanism?
- **Regional variation:** Are the spatial patterns consistent with domain knowledge?
- **Confounders:** What unobserved confounders might domain experts identify?

### 9.2 Collaborative Annotation Framework

Design a system where domain experts can review and annotate discovered relationships:

| Annotation | Meaning |
|-----------|---------|
| **Confirmed** | Expert agrees this is a known, well-established relationship |
| **Plausible** | Expert considers the mechanism plausible and the statistical evidence convincing |
| **Needs investigation** | Expert finds the result interesting but wants additional evidence |
| **Implausible** | Expert considers the mechanism implausible despite statistical significance |
| **Known artefact** | Expert identifies a known confound or data quality issue that explains the association |

### 9.3 The Causal Atlas Confidence Score

Combine multiple evidence streams into a single confidence score:

| Component | Weight | Score Range | How Assessed |
|-----------|--------|-------------|-------------|
| Statistical significance (FDR-corrected) | 15% | 0-1 | Automated |
| Effect size magnitude | 10% | 0-1 | Automated |
| Temporal holdout replication | 15% | 0-1 | Automated |
| Spatial holdout replication | 15% | 0-1 | Automated |
| Robustness checks (lag, scale, dataset) | 15% | 0-1 | Automated |
| Literature support | 15% | 0-1 | Semi-automated |
| Expert review | 15% | 0-1 | Manual |

**Composite score interpretation:**
- 0.8-1.0: High confidence — report as validated finding
- 0.6-0.8: Moderate confidence — report with caveats
- 0.4-0.6: Low confidence — report as suggestive only
- 0.0-0.4: Very low confidence — do not report externally

### 9.4 Pre-Registration of Analyses

To combat the garden of forking paths, Causal Atlas analyses should be pre-registered:

- **Pre-registration platform:** Open Science Framework (OSF) Registries ([osf.io](https://osf.io))
- **What to pre-register:**
  - Specific hypotheses to be tested
  - Data sources and versions
  - Spatial and temporal resolution
  - Variable transformations
  - Statistical methods and parameter choices
  - Significance thresholds and multiple testing corrections
  - Planned robustness checks
- **When to pre-register:** Before accessing the outcome data (or before analysing a new data vintage)
- **Deviations from pre-registration:** Document and label as exploratory

Pre-registration is especially important for novel findings that were not anticipated. If a novel finding is discovered during exploratory analysis, it should be validated on a separate holdout dataset before being reported.

**Reference:** Center for Open Science. "Preregistration." ([cos.io/initiatives/prereg](https://www.cos.io/initiatives/prereg))

---

## 10. Automated Validation Pipeline

### 10.1 Pipeline Overview

Design an automated system that subjects every discovered relationship to a standardised validation protocol before it reaches users:

```
[Raw Discovery]
    → Step 1: Statistical significance filter
    → Step 2: Multiple testing correction (FDR)
    → Step 3: Temporal holdout test
    → Step 4: Spatial holdout test
    → Step 5: Robustness checks
    → Step 6: Literature comparison
    → Step 7: Confidence score assignment
    → Step 8: Human review (for high-confidence novel findings)
    → [Validated Output]
```

### 10.2 Step-by-Step Design

#### Step 1: Statistical Significance Filter

- **Input:** Raw causal discovery results (e.g. PCMCI output)
- **Test:** Is the MCI test statistic significant at p < 0.05?
- **Output:** Candidate causal links with uncorrected p-values
- **Expected attrition:** ~50-80% of candidate links eliminated

#### Step 2: Multiple Testing Correction (FDR)

- **Method:** Benjamini-Hochberg FDR at q = 0.05
- **Scope:** Apply across all tests within each analysis run
- **Output:** FDR-corrected p-values; retain only links with q < 0.05
- **Expected attrition:** ~50-90% of Step 1 survivors eliminated

#### Step 3: Temporal Holdout Test

- **Method:** Re-run causal discovery on the holdout period (last 30% of data)
- **Criterion:** Link must be significant (uncorrected p < 0.05) in holdout period, with same direction
- **Output:** Links that replicate temporally
- **Expected attrition:** ~30-50% eliminated (non-stationary relationships)

#### Step 4: Spatial Holdout Test

- **Method:** Re-run causal discovery on held-out spatial region
- **Criterion:** Link must be significant in at least one other region where the mechanism is expected to operate
- **Output:** Links that generalise spatially
- **Expected attrition:** ~20-40% eliminated (region-specific artefacts)
- **Note:** Not all relationships are expected to generalise — this step should be applied judiciously

#### Step 5: Robustness Checks

Run automatically for all surviving links:

- [ ] Alternative lag order (+/- 2 months): effect persists?
- [ ] Alternative spatial scale (1 degree resolution): effect persists?
- [ ] First-differences specification: effect persists?
- [ ] Placebo timing test (shift treatment by 12 months): effect disappears?
- [ ] Dose-response check: monotonic relationship between magnitude of X and magnitude of Y?

**Criterion:** Pass at least 3 of 5 checks
**Expected attrition:** ~20-40% eliminated

#### Step 6: Literature Comparison

- **Method:** Automated search using the relationship description (X variable, Y variable, direction, lag) against a curated database of published findings (drawn from `03-causal-chains.md` and expanded)
- **Classification:**
  - **Match:** Published study confirms the relationship → boost confidence
  - **No match:** No published study found → flag as potentially novel, requires extra scrutiny
  - **Contradiction:** Published study finds the opposite → flag for review, likely an error

#### Step 7: Confidence Score Assignment

Calculate the composite confidence score as described in Section 9.3. Assign the confidence tier (Confirmed / Supported / Suggestive / Exploratory / Not Supported).

#### Step 8: Human Review

- **Trigger:** Any finding classified as "Supported" or higher that has no literature match (i.e. potentially novel)
- **Review process:** Domain expert evaluates mechanism plausibility, examines visualisations, checks for known confounders
- **Output:** Final confidence tier, with expert annotation

### 10.3 Pipeline Performance Targets

| Metric | Target |
|--------|--------|
| False positive rate (among all reported findings) | < 5% |
| False negative rate (among known ground truth benchmarks) | < 20% |
| Lag recovery accuracy (within +/- 1 month) | > 80% |
| Direction accuracy | > 95% |
| Processing time per analysis run | < 24 hours |

---

## 11. Reporting Standards

### 11.1 Minimum Reporting Requirements

Every causal relationship reported by Causal Atlas should include:

1. **Effect size with confidence interval** — Not just "significant" but how large is the effect and how precisely is it estimated?
2. **Uncorrected p-value and FDR-corrected p-value** — Both are informative
3. **Lag structure** — At what temporal offset is the association strongest? Visualise the lag-response curve.
4. **Spatial extent** — Map showing where the relationship holds and where it does not
5. **Direction** — Clear statement of which variable leads and which follows
6. **Robustness check results** — Table showing which checks passed and which failed
7. **Temporal stability** — Does the relationship hold across different time periods?
8. **Comparison with published literature** — Concordance or discordance with prior work
9. **Explicit assumptions** — What assumptions does the analysis make (stationarity, linearity, no unobserved confounders)?
10. **Limitations** — What could invalidate this finding?

### 11.2 Visualisation Standards

Each reported relationship should be accompanied by:

- **Lag-response curve:** Effect size (y-axis) vs lag in months (x-axis), with confidence band
- **Spatial map:** Grid cells where the relationship is significant, colour-coded by effect size
- **Time series overlay:** Cause variable and effect variable plotted together for representative grid cells
- **Robustness summary:** Forest plot or table showing effect sizes under alternative specifications
- **Negative control results:** What does the same analysis show for known non-relationships?

### 11.3 Applicable Reporting Guidelines

#### STROBE (Strengthening the Reporting of Observational Studies in Epidemiology)

STROBE provides a 22-item checklist for reporting observational studies, covering title, abstract, introduction, methods, results, and discussion. While designed for epidemiological studies (cohort, case-control, cross-sectional), the principles apply directly to Causal Atlas:

- Describe the setting, locations, and relevant dates
- State the eligibility criteria and sources of data
- Describe all statistical methods, including how confounders were addressed
- Report the number of individuals at each stage of study and reasons for non-participation
- Give unadjusted and adjusted estimates with confidence intervals

**Reference:** von Elm, E. et al. (2007). "Strengthening the Reporting of Observational Studies in Epidemiology (STROBE)." The Lancet, 370(9596), 1453-1457. ([strobe-statement.org](https://www.strobe-statement.org/))

**Note:** There is no established "STROBE-Space" extension specifically for spatiotemporal studies. Causal Atlas could contribute to developing such a standard. Elements that would need to be added include: spatial resolution, temporal resolution, spatial autocorrelation handling, temporal stationarity assessment, and cross-validation design.

### 11.4 DOI-Mintable Research Outputs

Discovered causal relationships and the underlying analyses should be published as citable research objects:

- **Platform:** Zenodo ([about.zenodo.org](https://about.zenodo.org/principles/))
- **What to deposit:**
  - Analysis specification (pre-registration document)
  - Complete results dataset (all tested relationships, not just significant ones)
  - Code used for analysis
  - Validation results
- **DOI assignment:** Zenodo automatically assigns a DOI to every published record via Datacite
- **FAIR principles:** Deposits should be Findable, Accessible, Interoperable, and Reusable
- **Licence:** CC-BY 4.0 for results; MIT for code (consistent with project licence)

This ensures that Causal Atlas findings are citeable, reproducible, and verifiable by external researchers.

---

## 12. Ethical Considerations

### 12.1 Responsible Disclosure of Conflict-Predictive Findings

If Causal Atlas discovers predictive relationships for conflict onset (e.g. drought in region X predicts conflict 6 months later), this information could be:

- **Beneficial:** Early warning systems, humanitarian pre-positioning, preventive diplomacy
- **Harmful:** Justification for pre-emptive military action, targeting of vulnerable populations, insurance redlining, speculative market manipulation

**Principles for responsible disclosure:**

1. **Do not publish conflict prediction models with sufficient spatial and temporal specificity to identify specific communities at risk** without engagement with affected communities and humanitarian partners
2. **Engage with established early warning systems** (FEWS NET, IPC, INFORM) rather than creating independent predictions
3. **Present probabilities, not deterministic predictions** — avoid language that implies certainty
4. **Consider the information environment** — how will this be interpreted by different actors?
5. **Implement delayed release for high-sensitivity findings** — allow time for responsible engagement before public release

### 12.2 Self-Fulfilling Prophecies

Prediction models can create harmful self-fulfilling prophecies:

- If a region is labelled as "high conflict risk," investors may withdraw, aid agencies may prepare for the worst, and the resulting economic decline or militarisation may increase the actual risk of conflict
- A prediction of food price spikes could trigger hoarding behaviour that causes the price spike
- Labelling a community as "at risk" can lead to stigmatisation and discrimination

**Mitigation:**
- Present causal relationships, not predictions (emphasise "X is associated with Y" rather than "conflict will occur in region Z")
- Avoid publishing predictive scores for specific locations and timeframes
- Frame findings as informing structural interventions (addressing root causes) rather than predictive targeting

**Reference:** PMC (2025). "When accurate prediction models yield harmful self-fulfilling prophecies." ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12010445/))

### 12.3 Data Sovereignty and Who Benefits

Causal Atlas analyses global data, much of it collected from or about communities in the Global South. Key questions:

- **Who benefits from this analysis?** If the primary users are researchers and policymakers in the Global North, while the data subjects are in the Global South, there is an extractive dynamic
- **Indigenous data sovereignty:** Indigenous peoples have the right to control data about their communities, lands, and cultures. The CARE Principles (Collective Benefit, Authority to Control, Responsibility, Ethics) complement the FAIR principles. ([GIDA](https://www.gida-global.org/care))
- **Local capacity:** Does Causal Atlas build local analytical capacity, or does it centralise expertise?
- **Accessibility:** Is the platform genuinely usable by analysts in data-subject countries, or only by well-resourced institutions?

**Commitments:**
- Open source and free to use (MIT licence) — non-negotiable
- Documentation in multiple languages where feasible
- Active engagement with researchers and institutions in data-subject regions
- Credit and co-authorship for local data contributors and analysts
- Respect data access restrictions imposed by data-sovereign communities

### 12.4 The "Do No Harm" Principle

OCHA's Data Responsibility Guidelines (2021, updated 2025) define data responsibility as "the safe, ethical and effective management of personal and non-personal data for operational response." Key principles:

1. **Do no harm:** Data management should not cause or exacerbate risk for affected people and communities
2. **Both personal and non-personal data can be sensitive** in humanitarian contexts. Aggregated conflict data, even at 0.5-degree resolution, could identify vulnerable communities.
3. **Data sensitivity assessment:** Before publishing analysis results, assess whether the findings could be used to target or harm affected populations
4. **Proportionality:** Collect and analyse only the data necessary for the stated purpose

**Reference:** OCHA Centre for Humanitarian Data. "Data Responsibility Guidelines" (2025). ([PDF](https://data.humdata.org/dataset/2048a947-5714-4220-905b-e662cbcd14c8/resource/8bc5b848-8ece-4f1f-a78b-18dd972bb21a/download/data-responsibility-guidelines-2025.pdf))

**IASC Operational Guidance:** The Inter-Agency Standing Committee (IASC) published "Operational Guidance on Data Responsibility in Humanitarian Action" (2021), providing an operational framework for data management across the humanitarian system. ([IASC](https://interagencystandingcommittee.org/operational-response/iasc-operational-guidance-data-responsibility-humanitarian-action))

### 12.5 Causal Atlas Ethical Review Process

For findings that involve vulnerable populations, conflict prediction, or potentially sensitive causal chains:

1. **Sensitivity classification** of all analysis outputs before publication
2. **Ethical review board** (even informal) for high-sensitivity findings
3. **Engagement with affected communities** where feasible
4. **Right to object:** Communities should be able to request that specific analyses about them not be published
5. **Transparency about limitations:** Never present observational associations as proven causal effects to policymakers

---

## 13. Sources

### Validation and False Positive Control
- Runge, J. et al. (2019). "Detecting and quantifying causal associations in large nonlinear time series datasets." Science Advances, 5(11). [Link](https://www.science.org/doi/10.1126/sciadv.aau4996)
- Gelman, A. and Loken, E. (2013). "The garden of forking paths." Columbia University. [PDF](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)
- Gelman, A. (2014). "The Statistical Crisis in Science." American Scientist. [Link](https://www.americanscientist.org/article/the-statistical-crisis-in-science)

### Multiple Testing and Spatial Statistics
- Caldas de Castro, M. and Singer, B.H. (2006). "Controlling the False Discovery Rate." Geographical Analysis, 38(2). [Link](https://onlinelibrary.wiley.com/doi/10.1111/j.0016-7363.2006.00682.x)
- Accounting for multiple testing in spatiotemporal environmental data. Environmental and Ecological Statistics (2020). [Link](https://link.springer.com/article/10.1007/s10651-020-00446-4)

### Robustness and Sensitivity Analysis
- Eggers, A. et al. (2024). "Placebo Tests for Causal Inference." American Journal of Political Science. [Link](https://onlinelibrary.wiley.com/doi/10.1111/ajps.12818)
- Cinelli, C. and Hazlett, C. (2020). "Making Sense of Sensitivity." JRSS-B. [PDF](https://carloscinelli.com/files/Cinelli%20and%20Hazlett%20(2020)%20-%20Making%20Sense%20of%20Sensitivity.pdf)
- VanderWeele, T.J. and Ding, P. (2017). "Sensitivity Analysis: Introducing the E-Value." Annals of Internal Medicine, 167(4). [Link](https://pubmed.ncbi.nlm.nih.gov/28693043/)
- Lu, X., White, H. (2014). "Robustness checks and robustness tests in applied economics." Journal of Econometrics. [Link](https://www.sciencedirect.com/science/article/abs/pii/S0304407613001668)
- Harvard Kasy lecture notes on robustness, sensitivity, and falsification. [PDF](https://scholar.harvard.edu/files/kasy/files/4-robustness_sensitivity_falsification.pdf)

### Climate-Conflict Debate
- Hsiang, S.M., Burke, M. and Miguel, E. (2013). "Quantifying the Influence of Climate on Human Conflict." Science, 341(6151).
- Burke, M., Hsiang, S.M. and Miguel, E. (2015). "Climate and Conflict." Annual Review of Economics, 7. [Link](https://www.annualreviews.org/content/journals/10.1146/annurev-economics-080614-115430)
- Buhaug, H. et al. (2014). "One effect to rule them all?" Climatic Change. [Link](https://link.springer.com/article/10.1007/s10584-014-1266-1)
- PRIO (2014). "Climate and conflict: A Comment on Hsiang et al.'s Reply to Buhaug et al." [Link](https://www.prio.org/publications/7521)

### Benchmarks and Simulation
- CauseMe platform. [Link](https://causeme.uv.es/)
- CausalDiscoveryToolbox documentation. [Link](https://fentechsolutions.github.io/CausalDiscoveryToolbox/html/data.html)
- Microsoft CSuite. [GitHub](https://github.com/microsoft/csuite)
- CausalTime (ICLR 2024). [PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/0c79d6ed1788653643a1ac67b6ea32a7-Paper-Conference.pdf)
- CausalProfiler (2025). [arXiv](https://arxiv.org/abs/2511.22842)

### Cross-Validation and Spatial Blocking
- blockCV R package. [GitHub](https://github.com/rvalavi/blockCV)
- spacv Python package. [GitHub](https://github.com/SamComber/spacv)
- Radersma, R. and Sheldon, B.C. (2015). "A new permutation technique to explore and control for spatial autocorrelation." Methods in Ecology and Evolution. [Link](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210x.12390)
- Choosing blocks for spatial cross-validation (2025). Frontiers in Remote Sensing. [Link](https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/full)

### Ground Truth Benchmarks
- Schlenker, W. and Roberts, M.J. (2009). "Nonlinear temperature effects." PNAS, 106, 15594-15598. [Link](https://www.pnas.org/doi/10.1073/pnas.0906865106)
- IDMC (2023). "Can we predict conflict displacement?" [Link](https://www.internal-displacement.org/expert-analysis/can-we-predict-conflict-displacement/)
- Nature (2022). "Anticipating drought-related food security changes." Nature Sustainability. [Link](https://www.nature.com/articles/s41893-022-00962-0)
- Nature (2024). "Forecasting trends in food security with real time data." Communications Earth & Environment. [Link](https://www.nature.com/articles/s43247-024-01698-9)
- Nature (2025). "Monitoring changes in nighttime lights during geopolitical conflicts." Humanities and Social Sciences Communications. [Link](https://www.nature.com/articles/s41599-025-05151-w)

### Ethical Frameworks
- OCHA Data Responsibility Guidelines (2025). [PDF](https://data.humdata.org/dataset/2048a947-5714-4220-905b-e662cbcd14c8/resource/8bc5b848-8ece-4f1f-a78b-18dd972bb21a/download/data-responsibility-guidelines-2025.pdf)
- IASC Operational Guidance on Data Responsibility (2021). [Link](https://interagencystandingcommittee.org/operational-response/iasc-operational-guidance-data-responsibility-humanitarian-action)
- OCHA Guidance Note on Humanitarian Data Ethics. [Link](https://www.unocha.org/publications/report/world/centre-humanitarian-data-guidance-note-series-data-responsibility-humanitarian-action-1)
- GIDA CARE Principles for Indigenous Data Governance. [Link](https://www.gida-global.org/care)
- PMC (2025). "When accurate prediction models yield harmful self-fulfilling prophecies." [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC12010445/)
- Martin, A. (2025). "Why sovereignty matters for humanitarian data." [Link](https://journals.sagepub.com/doi/10.1177/20539517251361109)

### Reporting Standards
- STROBE Statement. [Link](https://www.strobe-statement.org/)
- Zenodo principles. [Link](https://about.zenodo.org/principles/)
- Center for Open Science preregistration. [Link](https://www.cos.io/initiatives/prereg)

### Spatiotemporal Causal Discovery
- Tigramite documentation. [Link](https://jakobrunge.github.io/tigramite/)
- Tigramite GitHub. [Link](https://github.com/jakobrunge/tigramite)
- STCausal 2024 workshop, UMBC. [Link](https://bdal.umbc.edu/stcausal-2024/)
- CausalST Papers collection. [GitHub](https://github.com/yutong-xia/CausalST_Papers)
- Causal Discovery from Temporal Data: Overview (ACM Computing Surveys, 2024). [Link](https://dl.acm.org/doi/10.1145/3705297)
