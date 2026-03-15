# Statistical Methods for Spatiotemporal Causal Analysis

> **Last updated:** March 2025
> **Status:** Deep research — comprehensive method review for Causal Atlas
> **Purpose:** Evaluate and compare statistical methods for detecting causal relationships across spatial and temporal dimensions in multi-domain datasets (conflict, climate, food security, health, economics, pollution)

---

## Table of Contents

1. [Overview and Framing](#1-overview-and-framing)
2. [Granger Causality](#2-granger-causality)
3. [Transfer Entropy](#3-transfer-entropy)
4. [PCMCI and Tigramite](#4-pcmci-and-tigramite)
5. [Convergent Cross-Mapping (CCM)](#5-convergent-cross-mapping-ccm)
6. [Spatial Lag and Spatial Error Models](#6-spatial-lag-and-spatial-error-models)
7. [Moran's I and Spatial Autocorrelation](#7-morans-i-and-spatial-autocorrelation)
8. [Vector Autoregression (VAR)](#8-vector-autoregression-var)
9. [Cross-Correlation with Lag Analysis](#9-cross-correlation-with-lag-analysis)
10. [Anomaly Co-occurrence Analysis](#10-anomaly-co-occurrence-analysis)
11. [Machine Learning Approaches](#11-machine-learning-approaches)
12. [Bayesian Network Methods](#12-bayesian-network-methods)
13. [Difference-in-Differences and Regression Discontinuity](#13-difference-in-differences-and-regression-discontinuity)
14. [Comparison Table](#14-comparison-table)
15. [Recommended Pipeline for Causal Atlas](#15-recommended-pipeline-for-causal-atlas)
16. [Sources](#16-sources)

---

## 1. Overview and Framing

### What Do We Mean by "Causality"?

No observational method can prove true causation in the interventionist sense. What these methods detect falls on a spectrum:

| Level | What It Means | Methods |
|-------|--------------|---------|
| **Association / Correlation** | Two variables co-vary | Cross-correlation, Moran's I |
| **Predictive Causality** | Past values of X improve prediction of Y beyond Y's own past | Granger causality, Transfer entropy, VAR |
| **Structural / Directed Causality** | A directed graph of conditional dependencies, potentially with latent confounders removed | PCMCI, Bayesian networks, PC/FCI algorithms |
| **Dynamical Coupling** | Variables share a common dynamical attractor | CCM |
| **Causal Effect Estimation** | Estimate the magnitude of a treatment effect under quasi-experimental assumptions | DiD, RDD, spatial matching |

For Causal Atlas, we need a **layered pipeline**: start with fast screening methods (cross-correlation, Moran's I), move to predictive causality (Granger, VAR), then to structural methods (PCMCI, Bayesian nets), with specialised tools (CCM, DiD) for specific questions.

### The Spatiotemporal Challenge

Standard time-series causality methods assume independent observations. Spatiotemporal data violates this because:

- **Spatial autocorrelation**: nearby grid cells are correlated (Tobler's first law)
- **Temporal autocorrelation**: consecutive time steps are correlated
- **Spatial spillovers**: a shock at location A affects outcomes at location B
- **Confounding**: unmeasured spatially or temporally varying confounders
- **Resolution mismatch**: different datasets have different spatial/temporal grains

Every method below must be evaluated for how well it handles these challenges.

---

## 2. Granger Causality

### What It Detects

**Predictive causality (not true causation).** Variable X "Granger-causes" Y if past values of X contain information that helps predict Y beyond what is contained in past values of Y alone. This is a necessary but not sufficient condition for true causation.

### The Method

Given two stationary time series $X_t$ and $Y_t$, fit two models:

1. **Restricted model:** $Y_t = \sum_{i=1}^{p} a_i Y_{t-i} + \epsilon_t$
2. **Unrestricted model:** $Y_t = \sum_{i=1}^{p} a_i Y_{t-i} + \sum_{i=1}^{p} b_i X_{t-i} + \eta_t$

If the unrestricted model significantly reduces residual variance (F-test or chi-squared test), X Granger-causes Y.

### Key Assumptions

1. **Stationarity** — Both series must be covariance-stationary (constant mean, variance, autocovariance). Non-stationary series must be differenced or detrended first. Use the Augmented Dickey-Fuller (ADF) or KPSS test to check. **This is critical**: applying Granger causality to integrated (non-stationary) series produces spurious results. See Toda-Yamamoto procedure for a test that does not require pre-testing for integration order.
2. **Linearity** — Standard Granger causality assumes a linear relationship. Nonlinear extensions exist but are computationally expensive.
3. **No instantaneous causation** — The test only detects lagged effects. Contemporaneous effects are not captured.
4. **No omitted variables** — If a common driver Z causes both X and Y with different lags, Granger causality may falsely detect X→Y. Multivariate extensions (conditional Granger causality) partially address this.
5. **Sufficient lag order** — Using too few lags misses the causal effect; too many wastes degrees of freedom. Select lag order using AIC/BIC on the VAR model.

### When Assumptions Are Violated

- **Non-stationary data**: Spurious Granger causality. Solution: difference the data or use the Toda-Yamamoto approach (fit VAR with p+d_max lags, test only on the first p).
- **Nonlinear relationships**: Standard test misses them. Solution: use nonlinear Granger causality or switch to transfer entropy.
- **Confounders**: False positives. Solution: use conditional (multivariate) Granger causality or PCMCI.
- **Short time series**: Low power. Solution: panel Granger causality (pool across spatial units).

### Spatial Variants

**Spatial Granger Causality**: Extends the standard test by incorporating spatial lags of both X and Y using a spatial weight matrix W:

$$Y_{it} = \sum_{j=1}^{p} a_j Y_{i,t-j} + \sum_{j=1}^{p} b_j X_{i,t-j} + \sum_{j=1}^{p} c_j (W \cdot Y)_{i,t-j} + \sum_{j=1}^{p} d_j (W \cdot X)_{i,t-j} + \epsilon_{it}$$

This tests whether X at neighbouring locations Granger-causes Y at location i.

**Panel Granger Causality (Dumitrescu-Hurlin test)**: For panel data with N spatial units and T time periods. Tests for Granger causality allowing heterogeneous coefficients across units. Uses the Z-bar statistic (for large T) or the Z-bar tilde statistic (for large N, small T). Not directly available in statsmodels but implementable manually or via R's `plm` package called from Python.

**Granger Cluster Sequence Mining**: Identifies pairs of spatial data clusters that exhibit causal relationships over time. Useful for discovering spatially aggregated causal patterns. See Luo et al. (2023) in *International Journal of Data Science and Analytics*.

### Python Implementation

**Primary package: `statsmodels`**

```python
# Bivariate Granger Causality Test
from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd

# data must be a DataFrame with 2 columns: [Y, X]
# Y is the effect variable (column 0), X is the cause variable (column 1)
data = pd.DataFrame({'Y': y_series, 'X': x_series})

# Test up to max_lag lags; returns dict of {lag: (test_results, ols_results)}
results = grangercausalitytests(data[['Y', 'X']], maxlag=12, verbose=True)

# Each lag entry contains 4 tests:
# - ssr_ftest: F-test on sum of squared residuals
# - ssr_chi2test: Chi-squared test
# - lrtest: Likelihood ratio test
# - params_ftest: F-test on parameters
# Access p-value for lag 3, F-test:
p_value = results[3][0]['ssr_ftest'][1]
```

**Via VAR model (multivariate):**

```python
from statsmodels.tsa.api import VAR

model = VAR(data[['Y', 'X1', 'X2']])
fitted = model.fit(maxlags=12, ic='aic')  # auto-select lag order

# Test if X1 Granger-causes Y
granger_result = fitted.test_causality('Y', ['X1'], kind='f')
print(granger_result.summary())
# Returns: test statistic, p-value, degrees of freedom
```

**Stationarity pre-check:**

```python
from statsmodels.tsa.stattools import adfuller, kpss

# ADF test (null = unit root / non-stationary)
adf_result = adfuller(series, autolag='AIC')
print(f'ADF Statistic: {adf_result[0]}, p-value: {adf_result[1]}')

# KPSS test (null = stationary) — use both for confirmation
kpss_result = kpss(series, regression='c', nlags='auto')
print(f'KPSS Statistic: {kpss_result[0]}, p-value: {kpss_result[1]}')
```

### Strengths

- Simple, well-understood, widely implemented
- Fast computation: O(T * p * N^2) for bivariate tests across N variable pairs
- Extensive theoretical foundation and known statistical properties
- Works well for linear systems with sufficient data
- Easy to interpret: clear directionality and lag structure

### Weaknesses

- Limited to linear relationships (standard version)
- Requires stationarity — pre-processing can distort causal signals
- Sensitive to lag order selection
- Bivariate version ignores confounders
- Cannot distinguish direct from indirect causation
- No spatial awareness in the standard version

### Computational Complexity / Scalability

- **Bivariate test**: O(T * p) per pair; O(N^2 * T * p) for all pairs of N variables
- **VAR-based (multivariate)**: O(T * N^2 * p) for fitting; O(N^2) tests
- Scales well to thousands of variable pairs at monthly resolution
- For a 0.5-degree grid with ~100 variables per cell, testing across ~64,000 land cells requires parallelisation but is feasible

### When to Use It

- **Best for**: Initial screening of pairwise lagged relationships; linear systems; when interpretability matters; panel data with spatial replication
- **Avoid when**: Relationships are strongly nonlinear; confounders are likely; time series are very short (< 30 observations)

### Published Examples in Climate-Conflict Domain

- Silva et al. (2021) used Granger causality to detect climate teleconnections, finding significant lagged relationships between ENSO indices and regional precipitation patterns at 3-12 month lags. Published in *Geophysical Research Letters*.
- Runge et al. (2018) noted that Granger causality can overreport relationships in autocorrelated climate data compared to PCMCI, which better controls for common drivers. Published in *Science Advances*.
- PMC article on drought-induced displacement (2024) used causal discovery (including Granger-type methods) to map drought→food insecurity→conflict→displacement chains in Somalia, finding that causal graphs varied across districts.

### How It Handles Spatial Structure

**Poorly in standard form.** Standard Granger causality treats each spatial unit independently or pools them without accounting for spatial dependence. Solutions:

- Use spatial weight matrices to create spatially lagged variables as additional predictors
- Apply panel Granger causality (Dumitrescu-Hurlin) across grid cells
- Combine with spatial econometric models (see Section 6)
- Pre-filter spatial autocorrelation using spatial differencing

---

## 3. Transfer Entropy

### What It Detects

**Predictive causality (information-theoretic version).** Transfer entropy measures the amount of information (in bits or nats) that the past of X provides about the future of Y, beyond what the past of Y itself provides. It is the information-theoretic analogue of Granger causality but is **model-free** and can detect **nonlinear** relationships.

### The Method

Transfer entropy from X to Y is defined as:

$$T_{X \to Y} = \sum p(y_{t+1}, y_t^{(k)}, x_t^{(l)}) \log \frac{p(y_{t+1} | y_t^{(k)}, x_t^{(l)})}{p(y_{t+1} | y_t^{(k)})}$$

where $y_t^{(k)}$ denotes k past values of Y and $x_t^{(l)}$ denotes l past values of X.

Equivalently, it can be expressed as a difference of conditional entropies:

$$T_{X \to Y} = H(Y_{t+1} | Y_t^{(k)}) - H(Y_{t+1} | Y_t^{(k)}, X_t^{(l)})$$

### Key Relationship to Granger Causality

For **multivariate Gaussian** variables, transfer entropy is equivalent (up to a factor of 2) to Granger causality:

$$T_{X \to Y} = \frac{1}{2} \ln \frac{\text{Var}(\epsilon_{\text{restricted}})}{\text{Var}(\epsilon_{\text{unrestricted}})}$$

This means transfer entropy is strictly more general: it reduces to Granger causality for linear Gaussian systems but also captures nonlinear dependencies.

### Key Assumptions

1. **Stationarity** — Like Granger causality, the process should be stationary for the estimates to be meaningful.
2. **Sufficient data** — Estimating probability distributions (especially in continuous spaces) requires substantially more data than parametric Granger tests. Rule of thumb: at least 500-1000 time points for reliable estimation with continuous data using KSG estimators.
3. **Correct embedding parameters** — The history lengths k and l, and any embedding delays, must be chosen carefully. Too short misses dependencies; too long increases estimation variance.
4. **No instantaneous effects** — Like Granger, standard TE only detects lagged information transfer.

### When Assumptions Are Violated

- **Insufficient data**: TE estimates become noisy and biased. Discrete TE is more robust with small samples but requires binning continuous data (information loss).
- **Non-stationarity**: Can produce spurious information transfer. Solution: use local/windowed TE or pre-process for stationarity.
- **Wrong embedding**: Misses or inflates true TE. Solution: use auto-embedding methods (e.g., Ragwitz criterion in IDTxl).

### Python Implementation

**Option 1: PyInform** (fast, C-backed, discrete data)

```python
from pyinform import transfer_entropy

# Data must be integer-valued (binned/discretised)
# xs = source time series (1D numpy array of ints)
# ys = target time series (1D numpy array of ints)
# k = target history length

te = transfer_entropy(xs, ys, k=2)
# Returns: average transfer entropy in bits

# Local (pointwise) transfer entropy
local_te = transfer_entropy(xs, ys, k=2, local=True)
# Returns: array of local TE values for each time step
```

**Option 2: JIDT** (Java library, Python bindings, continuous data)

```python
import jpype
import numpy as np

# Start JVM with JIDT jar
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea",
               "-Djava.class.path=/path/to/infodynamics.jar")

# Use Kraskov-Stoegbauer-Grassberger (KSG) estimator for continuous data
teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kraskov"
                             ).TransferEntropyCalculatorKraskov
teCalc = teCalcClass()
teCalc.setProperty("k", "1")          # target history length
teCalc.setProperty("k_HISTORY", "4")  # target embedding dimension
teCalc.setProperty("l_HISTORY", "4")  # source embedding dimension
teCalc.initialise()
teCalc.setObservations(
    jpype.JArray(jpype.JDouble, 1)(source.tolist()),
    jpype.JArray(jpype.JDouble, 1)(target.tolist())
)
te_result = teCalc.computeAverageLocalOfObservations()
# Statistical significance via surrogate testing
p_value = teCalc.computeSignificance(100).pValue  # 100 surrogates
```

**Option 3: IDTxl** (multivariate TE with automatic embedding, recommended for networks)

```python
from idtxl.multivariate_te import MultivariateTE
from idtxl.data import Data

# data_array: numpy array of shape (n_processes, n_samples)
data = Data(data_array, dim_order='ps')

network_analysis = MultivariateTE()
settings = {
    'cmi_estimator': 'JidtKraskovCMI',
    'max_lag_sources': 12,      # max lag for source variables
    'min_lag_sources': 1,       # min lag for source variables
    'max_lag_target': 12,       # max lag for target history
    'n_perm_max_stat': 200,     # surrogates for max statistic test
    'n_perm_min_stat': 200,     # surrogates for min statistic test
    'n_perm_omnibus': 500,      # surrogates for omnibus test
    'alpha_max_stat': 0.05,
    'alpha_min_stat': 0.05,
    'alpha_omnibus': 0.05,
}

results = network_analysis.analyse_network(settings, data, targets=[0, 1, 2])
# Returns: inferred network with significant source variables and lags
```

### Strengths

- **Model-free**: no linearity assumption; detects arbitrary nonlinear dependencies
- **Directional**: TE(X→Y) differs from TE(Y→X)
- **Information-theoretic interpretation**: measured in bits, giving a natural scale
- **Subsumes Granger causality**: equivalent for linear Gaussian systems, strictly more powerful otherwise
- **IDTxl provides multivariate TE**: conditions on other sources automatically, reducing false positives from confounders

### Weaknesses

- **Data-hungry**: continuous TE estimation requires substantially more data than Granger tests (500-1000+ observations minimum)
- **Computationally expensive**: KSG estimator is O(T * k * log(T)) per pair; multivariate TE is much slower
- **Sensitive to hyperparameters**: embedding dimension, lag, number of nearest neighbours (for KSG), bin sizes (for discrete)
- **Difficult to interpret magnitude**: "0.3 bits of transfer entropy" is less intuitive than a regression coefficient
- **Curse of dimensionality**: conditioning on many variables simultaneously degrades estimation quality

### Computational Complexity / Scalability

- **Bivariate, discrete (PyInform)**: Very fast, O(T) per pair. Suitable for large-scale screening.
- **Bivariate, continuous (KSG)**: O(T * log(T)) per pair due to nearest-neighbour search. Still tractable for moderate T.
- **Multivariate (IDTxl)**: Computationally intensive. Auto-embedding and surrogate testing multiply runtime. For 100 variables and T=500, expect hours of computation.
- **GPU acceleration**: IDTxl supports OpenCL-based GPU computation for significant speedups.

### When to Use It

- **Best for**: Detecting nonlinear causal couplings; systems where Granger causality assumptions fail; when you have abundant data (T > 500)
- **Avoid when**: Data is short (T < 100 for continuous); computational budget is tight; you need easily interpretable effect sizes; simple linear screening suffices

### Published Examples

- Barnett et al. (2009) proved the equivalence of TE and Granger causality for Gaussian variables in *Physical Review Letters*.
- Wollstadt et al. (2019) demonstrated IDTxl for multivariate network inference from neuroscience data, with methods directly applicable to spatiotemporal environmental data. Published in *Journal of Open Source Software*.
- Large-scale directed network inference using multivariate TE with hierarchical statistical testing has been applied to climate data (Novelli et al., 2019, *Network Neuroscience*).

### How It Handles Spatial Structure

**Not natively.** Standard TE operates on time series, not spatial fields. Approaches to incorporate space:

- Compute TE between spatially lagged variables (using spatial weight matrices)
- Use multivariate TE (IDTxl) where "sources" include neighbouring grid cells
- Apply TE independently per grid cell pair and then map the results spatially
- Use spatiotemporal embedding (include spatial neighbours in the embedding vector)

---

## 4. PCMCI and Tigramite

### What It Detects

**Structural causal relationships** in time series. PCMCI recovers a time-lagged causal graph: a set of directed links X(t-τ) → Y(t) that represent direct causal effects after conditioning out common causes, indirect paths, and autocorrelation effects. This is closer to "true" causal structure than Granger causality.

### The Method

PCMCI (Peter and Clark Momentary Conditional Independence) is a two-step algorithm:

**Step 1 — Condition Selection (PC-stable):** For each variable Y and each potential cause X(t-τ), iteratively test conditional independence X(t-τ) ⊥ Y(t) | S, where S is built up from the strongest associations. This efficiently removes spurious links without exhaustive conditioning.

**Step 2 — Momentary Conditional Independence (MCI):** For each remaining candidate link X(t-τ) → Y(t), test:

$$X(t-\tau) \perp Y(t) \mid \hat{P}(Y_t), \hat{P}(X_{t-\tau})$$

where $\hat{P}(Y_t)$ and $\hat{P}(X_{t-\tau})$ are the estimated parent sets of Y and X respectively. This controls for autocorrelation and common drivers simultaneously.

### Variants

| Variant | Key Feature | When to Use |
|---------|------------|-------------|
| **PCMCI** | Time-lagged links only; no contemporaneous effects | Default choice when temporal resolution is coarse relative to causal delays |
| **PCMCI+** | Also discovers contemporaneous (same-time-step) causal links | When causal delays are shorter than the sampling interval |
| **LPCMCI** | Allows for latent (unobserved) confounders | When you suspect important unmeasured variables; outputs partial ancestral graphs (PAGs) with uncertain edge marks |
| **CAnDOIT** | Extends LPCMCI with interventional data | When you have some experimental data alongside observational |
| **J-PCMCI+** | Accounts for regime-dependent causal relationships | When causal structure changes over time (e.g., wet vs dry seasons) |

### Key Assumptions

1. **Causal sufficiency** (PCMCI/PCMCI+): All common causes are observed. LPCMCI relaxes this.
2. **Causal Markov condition**: Each variable is independent of its non-descendants given its parents.
3. **Faithfulness**: All conditional independencies in the data arise from the causal structure (no exact cancellations).
4. **Stationarity**: The causal structure does not change over time (J-PCMCI+ relaxes this).
5. **No selection bias**: Data is not conditioned on a collider.

### When Assumptions Are Violated

- **Latent confounders** (with PCMCI/PCMCI+): May produce false positive links. Solution: use LPCMCI, which outputs uncertain edge marks (circles) for ambiguous orientations.
- **Non-stationarity**: Causal graph may change. Solution: use regime-dependent J-PCMCI+ or apply PCMCI on windows.
- **Strong contemporaneous effects**: PCMCI misses them. Solution: use PCMCI+.
- **Very high dimensionality**: Condition selection may fail. Solution: reduce dimensions first or increase significance threshold.

### Python Implementation (Tigramite)

```python
import numpy as np
import tigramite
from tigramite import data_processing as pp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

# Prepare data: numpy array of shape (T, N) where T=time steps, N=variables
dataframe = pp.DataFrame(
    data=data_array,
    datatime=np.arange(T),
    var_names=['rainfall', 'food_price', 'conflict_events', 'displacement']
)

# Choose conditional independence test
# ParCorr: linear partial correlation (fast, for linear relationships)
# GPDC: Gaussian process distance correlation (nonlinear, slower)
# CMIknn: Conditional mutual information with k-nearest neighbours (nonlinear)
parcorr = ParCorr(significance='analytic')

# Initialise PCMCI
pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)

# Run PCMCI with maximum lag of 12 months
results = pcmci.run_pcmci(tau_max=12, pc_alpha=0.05, alpha_level=0.05)

# Results contain:
# results['p_matrix']     — p-values for all links, shape (N, N, tau_max+1)
# results['val_matrix']   — test statistic values
# results['graph']        — causal graph as string array: '-->' (causal),
#                           'o-o' (uncertain), '' (no link)

# Visualise the causal graph
from tigramite import plotting as tp

tp.plot_graph(
    val_matrix=results['val_matrix'],
    graph=results['graph'],
    var_names=['rainfall', 'food_price', 'conflict', 'displacement'],
    link_colorbar_label='cross-MCI',
    node_colorbar_label='auto-MCI',
)

# Plot time series graph (shows lag structure)
tp.plot_time_series_graph(
    val_matrix=results['val_matrix'],
    graph=results['graph'],
    var_names=['rainfall', 'food_price', 'conflict', 'displacement'],
)
```

**Using PCMCI+ (with contemporaneous links):**

```python
results = pcmci.run_pcmciplus(tau_max=12, pc_alpha=0.05)
# graph entries can include: '-->', '<--', 'o->', '<-o', 'o-o', 'x-x'
```

**Using LPCMCI (latent confounders):**

```python
from tigramite.lpcmci import LPCMCI

lpcmci = LPCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)
results = lpcmci.run_lpcmci(tau_max=12, pc_alpha=0.05)
# graph entries include circle marks ('o') for uncertain orientations
```

**Using nonlinear independence tests:**

```python
from tigramite.independence_tests.gpdc import GPDC
from tigramite.independence_tests.cmiknn import CMIknn

# Gaussian process-based (moderate nonlinearity, moderate data)
gpdc = GPDC(significance='analytic', gp_params=None)

# KNN-based conditional mutual information (strong nonlinearity, needs more data)
cmiknn = CMIknn(significance='shuffle_test', knn=0.1,
                shuffle_neighbors=5, transform='ranks')

pcmci = PCMCI(dataframe=dataframe, cond_ind_test=cmiknn, verbosity=1)
```

### Strengths

- **Controls for autocorrelation**: The MCI step explicitly conditions on each variable's own parents, removing autocorrelation-driven false positives that plague Granger causality in climate data
- **Controls for common drivers**: Conditioning on parent sets removes indirect and confounded links
- **Handles high-dimensional data**: The PC condition-selection step has polynomial complexity in the number of variables (not exponential)
- **Multiple independence tests**: Choose linear (fast) or nonlinear (powerful) depending on the question
- **Rich output**: Full causal graph with time lags, effect sizes, and uncertainty indicators
- **Active development**: PCMCI+, LPCMCI, J-PCMCI+ continue to expand capabilities

### Weaknesses

- **Computational cost**: Slower than simple Granger causality, especially with nonlinear tests. For N=50 variables and tau_max=12, the PC step tests O(N^2 * tau_max) pairs with iterative conditioning.
- **Sensitivity to alpha**: The PC step's alpha parameter controls sparsity — too liberal includes false positives, too conservative removes true links.
- **Assumption of stationarity**: The causal graph is assumed constant (J-PCMCI+ partially addresses this).
- **Causal sufficiency**: Standard PCMCI/PCMCI+ assumes all common causes are observed. LPCMCI relaxes this at the cost of more ambiguous output.
- **Requires tuning**: tau_max, pc_alpha, choice of independence test, and test-specific hyperparameters all need careful selection.

### Computational Complexity / Scalability

- **PC step**: O(N^2 * tau_max * p_max^{d_max}) where p_max is the maximum number of conditions tested and d_max is the maximum conditioning set size. In practice, for sparse graphs this is roughly O(N^2 * tau_max).
- **MCI step**: O(N^2 * tau_max) independence tests, each with conditioning set size bounded by the parent set size.
- **With ParCorr (linear)**: Each test is O(T). Total: roughly O(N^2 * tau_max * T).
- **With CMIknn (nonlinear)**: Each test is O(T * log(T)). Significantly slower.
- **Benchmark**: For N=10 variables, T=500, tau_max=5 with ParCorr: seconds. With CMIknn: minutes. For N=100 with CMIknn: hours.

### When to Use It

- **Best for**: Discovering causal graph structure from multivariate time series; distinguishing direct from indirect effects; climate and environmental applications; when autocorrelation is a concern (almost always)
- **Avoid when**: You only need simple pairwise screening (overkill); time series are extremely short (< 50); you need real-time computation

### Published Examples in Climate-Conflict Domain

- **Runge et al. (2019)**: "Detecting and quantifying causal associations in large nonlinear time series datasets." Introduced PCMCI and demonstrated it on climate data, recovering the Walker circulation and ENSO teleconnection network. Published in *Science Advances*. This is the foundational paper.
- **Runge et al. (2020)**: "Causal networks for climate model evaluation and constrained projections." Used PCMCI to build causal networks from observational and model climate data. Published in *Nature Communications*.
- **Thalheimer et al. (2024)**: "Causal discovery reveals complex patterns of drought-induced displacement." Applied PCMCI to weekly time series in three Somali districts, mapping drought→water security→food insecurity→conflict→displacement chains. Found that causal graphs varied across districts, emphasising the need for disaggregated analysis. Published in *Nature Communications Earth & Environment*.

### How It Handles Spatial Structure

**Partially.** PCMCI operates on multivariate time series — spatial information can be included by treating values at neighbouring grid cells as additional variables. However:

- For a grid of 64,000 cells, N becomes enormous. In practice, PCMCI is applied to a curated set of regional aggregates or specific locations.
- Spatial dependencies can be handled by including spatially lagged variables as additional time series.
- The recent "CausalFlow" framework (Castri et al.) wraps PCMCI and other methods with a unified interface for spatiotemporal applications.
- For Causal Atlas: run PCMCI on spatially aggregated data (e.g., admin-1 regions) or on subsets of the grid, using domain knowledge to select relevant variables.

---

## 5. Convergent Cross-Mapping (CCM)

### What It Detects

**Dynamical coupling** — not predictive causality in the Granger sense, but evidence that two variables are part of the same dynamical system. If X causally influences Y, then the historical record of Y contains information about X (because Y's dynamics are partly driven by X). CCM tests for this "cross-map predictability."

### The Method

Rooted in Takens' embedding theorem for dynamical systems:

1. **Construct shadow manifolds**: For time series Y, create the delay-embedding manifold M_Y by forming vectors $(Y_t, Y_{t-\tau}, Y_{t-2\tau}, \ldots, Y_{t-(E-1)\tau})$ where E is the embedding dimension and τ is the delay.

2. **Cross-map**: For a point on M_Y, find its nearest neighbours on M_Y. Use the same time indices to identify corresponding points on M_X. If these corresponding points on M_X are close together (i.e., predict X well), then Y contains information about X, implying X→Y causation.

3. **Convergence test**: As the library size L (number of data points used) increases, cross-map skill should **converge** — improve and plateau. This distinguishes true coupling from coincidental correlation.

**Key insight**: If X causes Y (X→Y), then **Y cross-maps to X** (Y xmap X), not the other way around. This is counterintuitive but follows from the embedding theorem: Y's manifold contains the signature of its driver X.

### Key Assumptions

1. **Weak-to-moderate coupling**: CCM works best for weakly coupled systems. Strong forcing can make the driven variable a near-copy of the driver, causing both directions to appear causal.
2. **Deterministic dynamics**: The system should be at least partially deterministic (not purely stochastic). CCM is designed for dynamical systems, not noise-driven processes.
3. **Sufficient data for embedding**: Need enough time points to reconstruct the attractor. Minimum ~30-50 per embedded dimension, so E=3 needs ~100+ points.
4. **Stationarity of the attractor**: The underlying dynamical system should not change qualitatively over the observation period.
5. **No synchrony**: If X and Y are perfectly synchronised, CCM cannot determine direction.

### When Assumptions Are Violated

- **Purely stochastic systems**: CCM may give meaningless results. Use Granger causality instead.
- **Strong forcing**: Both directions show convergence. Solution: compare convergence rates or use extended CCM variants.
- **Short time series**: Poor manifold reconstruction. Solution: use **multispatial CCM** (Clark et al. 2015) which leverages spatial replication — this is key for Causal Atlas.

### Spatial CCM (Multispatial CCM)

Clark et al. (2015) in *Ecology* proposed **multispatial CCM**: instead of requiring long time series at a single location, it combines short time series from multiple spatial replicates to reconstruct the shadow manifold. This works with as few as 5 sequential observations per location, provided there are enough spatial replicates (locations).

This is directly relevant to Causal Atlas: many of our datasets have short time series (a few years of monthly data) but high spatial coverage (thousands of grid cells). Multispatial CCM can leverage this spatial replication.

### Python Implementation

**Option 1: causal_ccm** (simple, pure Python)

```python
# pip install causal-ccm
from causal_ccm import ccm

# x, y: 1D numpy arrays (time series)
# E: embedding dimension (typically 2-5, select via simplex projection)
# tau: time delay (typically 1 for monthly data)
# L: library size (number of points used; vary for convergence test)

ccm_xy = ccm(x, y, E=3, tau=1, L=len(x))
# Returns: cross-map correlation (Pearson r between predicted and actual)

# Convergence test: compute CCM for increasing L
import numpy as np
lib_sizes = np.arange(20, len(x), 10)
skills = [ccm(x, y, E=3, tau=1, L=L) for L in lib_sizes]
# Plot skills vs lib_sizes — should increase and plateau for true causation
```

**Option 2: pyEDM** (Sugihara Lab's official package, comprehensive)

```python
# pip install pyEDM
import pyEDM

# Create a DataFrame with columns for each variable
import pandas as pd
df = pd.DataFrame({'time': range(len(x)), 'X': x, 'Y': y})

# CCM: test if X causes Y (Y xmap X)
ccm_result = pyEDM.CCM(
    dataFrame=df,
    E=3,                    # embedding dimension
    columns='Y',            # variable to embed (the "effect")
    target='X',             # variable to predict (the "cause")
    libSizes='20 200 10',   # library sizes: start, stop, step
    sample=100,             # number of random library samples per size
    showPlot=True
)
# Returns: DataFrame with columns LibSize, X:Y (cross-map skill Y xmap X)

# Simplex projection to find optimal E
simplex_result = pyEDM.Simplex(
    dataFrame=df,
    lib='1 100',      # library (training) range
    pred='101 200',   # prediction range
    columns='Y',
    target='Y',
    E=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
)
# Choose E that maximises prediction skill (rho)
```

**Option 3: fastEDM-python** (newer, optimised)

```python
# pip install fastEDM
from fastEDM import easy_edm

# Automated CCM analysis with significance testing
result = easy_edm(
    cause=x_series,
    effect=y_series,
    time=time_index,
    verbosity=1
)
# Returns: causal direction, strength, and significance
```

### Strengths

- **Detects nonlinear dynamical coupling**: designed specifically for systems where variables interact through complex dynamics
- **Works when Granger fails**: Granger causality assumes separability; CCM does not
- **Convergence criterion**: provides a principled way to distinguish causation from correlation
- **Spatial variant**: multispatial CCM leverages spatial replication for short time series
- **No model specification needed**: non-parametric, based on nearest-neighbour prediction

### Weaknesses

- **Not suited for purely stochastic systems**: designed for deterministic or semi-deterministic dynamics
- **Struggles with strong forcing**: bidirectional convergence is hard to interpret
- **Sensitive to embedding parameters**: E, τ choice matters; incorrect embedding degrades results
- **Computational cost**: O(T^2 * E) per pair due to nearest-neighbour search; convergence test multiplies this by number of library sizes
- **Difficult to interpret for non-specialists**: the cross-mapping logic is counterintuitive
- **No direct lag estimation**: standard CCM doesn't directly tell you the causal lag (extensions exist but are more complex)

### Computational Complexity / Scalability

- **Per pair**: O(T^2) for nearest-neighbour search (or O(T * log(T)) with KD-trees) times number of library sizes for convergence test
- **All pairs of N variables**: O(N^2 * T^2 * n_lib_sizes)
- **Multispatial CCM**: scales with number of spatial replicates × time series length
- For monthly data (T~300) across thousands of grid cells: bivariate CCM is feasible; screening all pairs requires parallelisation

### When to Use It

- **Best for**: Nonlinear ecological/climate systems; short time series with spatial replication (multispatial CCM); distinguishing true coupling from shared forcing; dynamical systems questions
- **Avoid when**: System is purely stochastic; time series are very long and linear (Granger is simpler and sufficient); you need explicit lag identification

### Published Examples

- **Sugihara et al. (2012)**: "Detecting causality in complex ecosystems." The foundational CCM paper, applied to sardine-anchovy-temperature interactions. Published in *Science*.
- **Clark et al. (2015)**: "Spatial convergent cross mapping to detect causal relationships from short time series." Showed multispatial CCM works with as few as 5 observations per location. Published in *Ecology*.
- **Ye et al. (2015)**: "Distinguishing time-delayed causal interactions using convergent cross mapping." Extended CCM to identify causal lag structures. Published in *Scientific Reports*.

### How It Handles Spatial Structure

**Multispatial CCM directly leverages spatial structure.** This is a significant advantage for Causal Atlas:

- Short time series at each grid cell can be pooled across space
- Assumes the same underlying dynamical system operates across locations (at least approximately)
- Currently only implemented in R (`multispatialCCM` package); a Python port or wrapper would be needed for Causal Atlas

---

## 6. Spatial Lag and Spatial Error Models

### What They Detect

**Spatial dependence in regression relationships.** These models don't directly test for temporal causation but account for the spatial structure that confounds temporal causal analyses. They answer: "After accounting for spatial spillovers, does X predict Y?"

### The Models

**Spatial Lag Model (SLM):**

$$Y = \rho W Y + X\beta + \epsilon$$

The dependent variable Y at each location depends on the weighted average of Y at neighbouring locations (the spatial lag ρWY). W is the spatial weight matrix (e.g., contiguity, inverse distance, k-nearest neighbours).

**Spatial Error Model (SEM):**

$$Y = X\beta + u, \quad u = \lambda W u + \epsilon$$

The error term is spatially autocorrelated. This means that after accounting for X, the residuals at nearby locations are correlated, often due to unmeasured spatially varying confounders.

**Combined Model (SARAR / Kelejian-Prucha):**

$$Y = \rho W Y + X\beta + u, \quad u = \lambda W u + \epsilon$$

Both spatial lag in Y and spatial autocorrelation in errors.

**Spatial Durbin Model:**

$$Y = \rho W Y + X\beta + W X \gamma + \epsilon$$

Also includes spatial lags of the independent variables (WX), allowing neighbourhood characteristics of X to affect Y.

### Key Assumptions

1. **Correct spatial weight matrix**: The choice of W (contiguity, distance-based, k-NN) matters enormously and encodes assumptions about the spatial interaction structure.
2. **Exogeneity of W**: The spatial weight matrix should not be endogenous to the outcome.
3. **Correct model specification**: Spatial lag vs spatial error has different implications. LM tests (Lagrange Multiplier) help choose.
4. **Normality of errors** (for ML estimation): GMM/IV estimators relax this.
5. **Cross-sectional or panel data**: Extensions exist for space-time panels.

### When to Use Them

- When you observe clustering in OLS residuals (test with Moran's I on residuals)
- When a treatment/predictor at one location might affect outcomes at nearby locations (spatial spillovers)
- As a diagnostic step: if spatial lag is significant, your non-spatial regression estimates are biased

### Python Implementation (PySAL / spreg)

```python
import libpysal
from spreg import OLS, GM_Lag, ML_Lag, ML_Error, GM_Error_Het

# Build spatial weight matrix
w = libpysal.weights.Queen.from_dataframe(gdf)  # queen contiguity from GeoDataFrame
# Alternatives:
# w = libpysal.weights.KNN.from_dataframe(gdf, k=8)        # k-nearest neighbours
# w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=50)  # distance
w.transform = 'r'  # row-standardise

# OLS baseline
ols = OLS(y, X, w=w, spat_diag=True, name_y='conflict', name_x=['rainfall', 'food_price'])
print(ols.summary)
# Check: ols.lm_lag (LM test for spatial lag)
#        ols.lm_error (LM test for spatial error)
#        ols.moran_res (Moran's I on residuals)

# If LM-lag is significant: Spatial Lag Model
# GMM estimation (preferred for inference)
lag_model = GM_Lag(y, X, w=w, name_y='conflict', name_x=['rainfall', 'food_price'])
print(lag_model.summary)
# lag_model.betas: coefficients including rho (spatial lag parameter)

# ML estimation (for comparison / pedagogical)
ml_lag = ML_Lag(y, X, w=w, name_y='conflict', name_x=['rainfall', 'food_price'])

# If LM-error is significant: Spatial Error Model
error_model = GM_Error_Het(y, X, w=w, name_y='conflict', name_x=['rainfall', 'food_price'])
print(error_model.summary)
# error_model.betas: coefficients; lambda is the spatial error parameter

# Specification search (new in spreg 2024): automated model selection
from spreg import spsearch
# Follows Anselin, Serenini, Amaral (2024) methodology
```

### Strengths

- Explicitly models spatial dependence — critical for gridded data
- Well-developed theory and diagnostics (LM tests, Moran's I)
- PySAL/spreg is mature, well-documented, actively maintained
- Handles spatial spillovers that bias standard regression
- 2024 updates include automated specification search

### Weaknesses

- Primarily cross-sectional or panel; no built-in temporal dynamics
- Choice of W is often arbitrary and results can be sensitive to it
- ML estimation assumes normality; GMM is more robust but less efficient
- Cannot represent complex temporal lag structures
- Spatial lag model has simultaneity (Y depends on WY contemporaneously)

### Computational Complexity / Scalability

- **OLS with spatial diagnostics**: O(N^2) for weight matrix operations, O(N * K^2) for regression. Feasible for N up to ~50,000.
- **ML estimation**: Requires computing determinant of (I - ρW), which is O(N^3) naively. Sparse matrix methods reduce this substantially.
- **GMM estimation**: O(N^2) for instrument construction. More scalable than ML.
- For a global 0.5-degree grid (~64,000 land cells): feasible with sparse weight matrices.

### Published Examples

- Anselin et al. (2024) specification search strategies for spatial regression, implemented in spreg.
- Spatial regression approaches are widely used in conflict research: Buhaug & Rød (2006) used spatial lag models to show that conflict risk at one location is influenced by conflict in neighbouring areas.

### How It Handles Spatial Structure

**This is what these models are designed for.** They are the gold standard for accounting for spatial dependence in regression. For Causal Atlas, they serve as the spatial component of any regression-based causal analysis.

---

## 7. Moran's I and Spatial Autocorrelation

### What It Detects

**Spatial clustering and dispersion.** Moran's I tests whether values of a variable are spatially autocorrelated — whether nearby locations tend to have similar (clustering) or dissimilar (dispersion) values. This is a diagnostic and exploratory tool, not a causal test, but is essential for:

- Identifying spatial patterns that need to be accounted for in causal analysis
- Detecting hotspots and coldspots (local Moran's I / LISA)
- Testing whether regression residuals exhibit spatial dependence

### The Methods

**Global Moran's I:**

$$I = \frac{N}{\sum_{i}\sum_{j} w_{ij}} \cdot \frac{\sum_{i}\sum_{j} w_{ij}(x_i - \bar{x})(x_j - \bar{x})}{\sum_{i} (x_i - \bar{x})^2}$$

- Range: approximately -1 (perfect dispersion) to +1 (perfect clustering); 0 = random
- Statistical significance via permutation test or analytical approximation

**Local Moran's I (LISA — Local Indicators of Spatial Association):**

$$I_i = \frac{(x_i - \bar{x})}{\sum_{i}(x_i - \bar{x})^2 / N} \sum_{j} w_{ij}(x_j - \bar{x})$$

Computed for each location i, identifying:

- **HH (High-High)**: High values surrounded by high values (hot spots)
- **LL (Low-Low)**: Low values surrounded by low values (cold spots)
- **HL (High-Low)**: High values surrounded by low values (spatial outliers)
- **LH (Low-High)**: Low values surrounded by high values (spatial outliers)

### Key Assumptions

1. **Stationarity**: The mean and variance are constant across space (first-order stationarity)
2. **Correct weight matrix**: Like spatial regression, results depend on the choice of W
3. **Normality** (for analytical p-values): Permutation-based p-values are more robust

### Python Implementation (PySAL / esda)

```python
from esda.moran import Moran, Moran_Local
import libpysal

# Build spatial weight matrix
w = libpysal.weights.Queen.from_dataframe(gdf)
w.transform = 'r'  # row-standardise

# Global Moran's I
mi = Moran(gdf['conflict_count'], w)
print(f"Moran's I: {mi.I:.4f}")
print(f"Expected I: {mi.EI:.4f}")
print(f"p-value (permutation): {mi.p_sim:.4f}")
print(f"p-value (analytical): {mi.p_norm:.4f}")
print(f"z-score: {mi.z_sim:.4f}")

# Local Moran's I (LISA)
lisa = Moran_Local(gdf['conflict_count'], w, permutations=999)
# lisa.Is         — local I values for each location
# lisa.p_sim      — p-values from permutation test
# lisa.q          — quadrant (1=HH, 2=LH, 3=LL, 4=HL)

# Identify significant clusters (p < 0.05)
significant = lisa.p_sim < 0.05
hot_spots = significant & (lisa.q == 1)    # HH clusters
cold_spots = significant & (lisa.q == 3)   # LL clusters

# Moran's I on regression residuals (spatial diagnostics)
from spreg import OLS
ols = OLS(y, X, w=w, spat_diag=True)
print(f"Moran's I on residuals: {ols.moran_res[0]:.4f}, p={ols.moran_res[1]:.4f}")
```

**Visualisation:**

```python
from splot.esda import moran_scatterplot, lisa_cluster, plot_local_autocorrelation

# Moran scatterplot (variable vs spatial lag)
fig, ax = moran_scatterplot(mi)

# LISA cluster map
fig, ax = lisa_cluster(lisa, gdf)
```

**Bivariate Moran's I** (spatial correlation between two different variables):

```python
from esda.moran import Moran_BV

# Test if high rainfall in neighbours correlates with conflict at focal location
bv = Moran_BV(gdf['conflict'], gdf['rainfall'], w, permutations=999)
print(f"Bivariate Moran's I: {bv.I:.4f}, p={bv.p_sim:.4f}")
```

### Strengths

- Simple, widely understood, fast to compute
- LISA provides spatially explicit results (maps of clusters)
- Bivariate version explores spatial cross-variable relationships
- Essential diagnostic for any spatial analysis
- Well-implemented in PySAL with good visualisation support

### Weaknesses

- Not a causal test — only measures spatial association
- Sensitive to weight matrix choice and scale (MAUP — Modifiable Areal Unit Problem)
- Global Moran's I can miss localised patterns
- Does not account for temporal dynamics
- Significance testing assumes exchangeability under the null

### Computational Complexity / Scalability

- **Global Moran's I**: O(N^2) for dense W; O(N * k) for sparse W with average k neighbours. Very fast.
- **LISA**: O(N * k) for computation; O(N * k * P) for permutation test with P permutations.
- For 64,000 grid cells with P=999 permutations: seconds to minutes.

### When to Use It

- **Always** as a first step in spatial data analysis
- To check for spatial autocorrelation in regression residuals (if present, use spatial regression)
- To identify hotspots/coldspots for each variable (where is conflict clustered? where is food insecurity concentrated?)
- Bivariate Moran's I as a spatial screening tool before more expensive causal methods

### Published Examples

- Anselin (1995): "Local Indicators of Spatial Association — LISA" — the foundational paper.
- LISA has been widely used in conflict studies: mapping conflict hotspots in sub-Saharan Africa, identifying spatial clusters of food insecurity that move with climate patterns, etc.

### How It Handles Spatial Structure

**This IS a spatial method.** Moran's I is entirely about spatial structure. It is a prerequisite diagnostic rather than a causal method — telling us where we need to account for spatial dependence in our causal analyses.

---

## 8. Vector Autoregression (VAR)

### What It Detects

**Dynamic interdependencies among multiple time series.** VAR models the evolution of multiple variables simultaneously, allowing each variable to depend on its own past and the past of all other variables. It is the multivariate extension of autoregression and the foundation for multivariate Granger causality.

### The Method

A VAR(p) model for N variables:

$$Y_t = c + A_1 Y_{t-1} + A_2 Y_{t-2} + \ldots + A_p Y_{t-p} + u_t$$

where $Y_t$ is an N-dimensional vector, $A_i$ are N×N coefficient matrices, and $u_t$ is an N-dimensional error vector with covariance matrix Σ.

Key outputs:
- **Granger causality tests**: test whether lags of one variable are jointly significant in the equation for another
- **Impulse Response Functions (IRFs)**: trace the dynamic effect of a one-unit shock in one variable on all other variables over time
- **Forecast Error Variance Decomposition (FEVD)**: what fraction of the forecast error variance of each variable is attributable to shocks in each other variable

### Spatial Extensions (SpVAR)

Spatial Vector Autoregressions (SpVARs) incorporate spatial dynamics:

$$Y_{it} = c_i + \rho W Y_{it} + \sum_{j=1}^{p} A_j Y_{i,t-j} + \sum_{j=1}^{p} B_j (W \cdot Y)_{i,t-j} + u_{it}$$

This includes:
- **Contemporaneous spatial lag** (ρWY_t): Y at location i depends on Y at neighbouring locations at time t
- **Lagged spatial lags** (B_j(W·Y)_{t-j}): Y at location i depends on Y at neighbouring locations at past times

SpVAR is described theoretically (Beenstock & Felsenstein, 2007, *Spatial Economic Analysis*) but no standard Python implementation exists; it requires custom coding or specialised packages.

### Key Assumptions

1. **Stationarity**: All variables must be stationary (stable roots). For non-stationary data, use VECM (Vector Error Correction Model) if variables are cointegrated.
2. **Correct lag order**: Too few lags = omitted variable bias; too many = inefficiency. Use AIC/BIC/HQIC.
3. **No contemporaneous causation**: VAR captures only lagged effects (structural VAR uses identification restrictions for contemporaneous effects).
4. **Linearity**: Standard VAR is linear. Nonlinear extensions (threshold VAR, smooth-transition VAR) exist but are complex.
5. **Sufficient observations**: Rule of thumb: T > N * p + 50 at minimum.

### Python Implementation (statsmodels)

```python
from statsmodels.tsa.api import VAR
import pandas as pd

# data: DataFrame with columns for each variable, time-indexed
data = pd.DataFrame({
    'rainfall': rainfall_series,
    'food_price': food_price_series,
    'conflict': conflict_series,
    'displacement': displacement_series
}, index=time_index)

# Fit VAR model
model = VAR(data)
# Select lag order by information criteria
lag_order = model.select_order(maxlags=12)
print(lag_order.summary())  # shows AIC, BIC, HQIC, FPE for each lag

# Fit with selected lag order
fitted = model.fit(maxlags=12, ic='aic')
print(fitted.summary())

# Granger causality test
gc = fitted.test_causality('conflict', ['rainfall', 'food_price'], kind='f')
print(gc.summary())

# Impulse Response Functions
irf = fitted.irf(periods=24)  # 24 months ahead
irf.plot(orth=True)            # orthogonalised IRF
irf.plot_cum_effects(orth=True)  # cumulative effects

# Confidence intervals via bootstrap
irf = fitted.irf(periods=24)
irf.plot(orth=True, impulse='rainfall', response='conflict')

# Forecast Error Variance Decomposition
fevd = fitted.fevd(periods=24)
fevd.summary()
fevd.plot()

# Stability check (all roots inside unit circle)
fitted.is_stable(verbose=True)
```

**Structural VAR (identifying contemporaneous effects):**

```python
from statsmodels.tsa.vector_ar.svar_model import SVAR

# A-model: Ay_t = ... (specify contemporaneous restriction matrix)
# Use Cholesky ordering or theory-based restrictions
A = np.array([
    [1, 0, 0, 0],      # rainfall: exogenous
    ['E', 1, 0, 0],     # food_price: affected by rainfall
    ['E', 'E', 1, 0],   # conflict: affected by rainfall and food_price
    ['E', 'E', 'E', 1]  # displacement: affected by all
])
# 'E' = estimate, 0 = restricted to zero

svar = SVAR(data, svar_type='A', A=A)
svar_fit = svar.fit(maxlags=12)
```

### Strengths

- Captures multivariate dynamic relationships simultaneously
- IRFs provide intuitive visualisation of causal chains over time
- FEVD quantifies relative importance of each variable
- Well-established theoretical framework with known statistical properties
- Granger causality is a natural byproduct
- statsmodels implementation is mature and well-documented

### Weaknesses

- **Parameter proliferation**: N^2 * p parameters grow quickly. With N=10 and p=12, that's 1,200 parameters.
- **Stationarity requirement**: Most economic and environmental series are non-stationary
- **Linearity assumption**: Cannot capture nonlinear dynamics
- **No spatial awareness**: Standard VAR treats each time series independently of spatial location
- **Identification problem**: Contemporaneous effects require strong identifying assumptions (ordering, sign restrictions)
- **Sensitivity to variable ordering**: Cholesky decomposition for IRFs depends on the ordering of variables

### Computational Complexity / Scalability

- **Fitting**: O(T * N^2 * p) for OLS estimation per equation
- **IRFs**: O(N^3 * periods) for matrix operations
- **Bottleneck**: The number of variables N. With N > 20, VAR becomes unwieldy. With N > 50, estimation is unreliable without regularisation (LASSO-VAR).
- For Causal Atlas: VAR is suited for a moderate number of aggregated variables (5-15), not for cell-level analysis.

### When to Use It

- **Best for**: Understanding dynamic interactions among a moderate number of variables (5-15); generating IRFs for policy communication; baseline multivariate analysis
- **Avoid when**: Many variables (N > 20); strong nonlinearity; need to handle spatial structure explicitly; need to distinguish direct from indirect causal effects (use PCMCI instead)

### Published Examples

- VAR models are the workhorse of macroeconomic analysis and have been applied extensively in climate-economy studies.
- Hsiang et al. (2011) used panel VAR to study the relationship between ENSO, temperature, and civil conflict in tropical countries, finding that conflict risk doubles during El Nino years. Published in *Nature*.
- Burke et al. (2015) used VAR-like panel regression with climate variables predicting conflict, with lags up to 24 months.

### How It Handles Spatial Structure

**Not natively.** Options:
- **Panel VAR**: Estimate a VAR for each spatial unit (with or without pooled coefficients)
- **SpVAR**: Add spatial lags as additional regressors (custom implementation required)
- **Global VAR (GVAR)**: Separate VAR per country/region, linked through trade/distance weights. Implementation available in R (`GVAR` package); Python would require custom code.

---

## 9. Cross-Correlation with Lag Analysis

### What It Detects

**Linear association at different time lags.** This is the simplest and fastest method: compute the Pearson correlation between X(t) and Y(t+τ) for various lags τ. The lag with maximum absolute correlation suggests the temporal relationship.

**Important**: cross-correlation detects association, not causation. But it is invaluable as a fast screening step.

### The Method

The cross-correlation function (CCF) at lag τ:

$$r_{XY}(\tau) = \frac{\sum_{t} (X_t - \bar{X})(Y_{t+\tau} - \bar{Y})}{\sqrt{\sum_t (X_t - \bar{X})^2 \sum_t (Y_{t+\tau} - \bar{Y})^2}}$$

- If $r_{XY}(\tau) > 0$ for τ > 0: X leads Y (positive association)
- If $r_{XY}(\tau) < 0$ for τ > 0: X leads Y (negative association)
- If maximum |r| occurs at τ < 0: Y leads X

### Best Practices

1. **Detrend and deseasonalise first**: Shared trends and seasonality produce spurious cross-correlations. Use STL decomposition, differencing, or regression on seasonal dummies.
2. **Pre-whiten the series**: Fit an ARIMA model to X, apply the same filter to Y, then cross-correlate the residuals. This removes autocorrelation-driven false correlations.
3. **Use normalised cross-correlation**: Divide by the product of standard deviations so r ∈ [-1, 1].
4. **Compute confidence bounds**: Under the null of independence with pre-whitened series, the approximate 95% CI is ±1.96/√T.
5. **Test multiple variables systematically**: Correct for multiple comparisons (Bonferroni, FDR).

### Python Implementation

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Method 1: scipy.signal.correlate (raw cross-correlation)
x_norm = (x - np.mean(x)) / np.std(x)
y_norm = (y - np.mean(y)) / np.std(y)
ccf = signal.correlate(x_norm, y_norm, mode='full') / len(x)
lags = signal.correlation_lags(len(x), len(y), mode='full')

# Find lag with maximum absolute correlation
max_lag = lags[np.argmax(np.abs(ccf))]
max_corr = ccf[np.argmax(np.abs(ccf))]
print(f"Maximum correlation {max_corr:.3f} at lag {max_lag}")

# Method 2: statsmodels (with pre-whitening option)
from statsmodels.tsa.stattools import ccf as sm_ccf

# Cross-correlation function (unbiased estimate)
ccf_values = sm_ccf(x, y, adjusted=True)
# Returns: array of correlations for lags 0, 1, 2, ...

# Method 3: pandas rolling correlation (for time-varying association)
import pandas as pd
df = pd.DataFrame({'X': x, 'Y': y})
rolling_corr = df['X'].rolling(window=36).corr(df['Y'])  # 36-month window

# Proper pre-whitening pipeline
from statsmodels.tsa.arima.model import ARIMA

# 1. Fit ARIMA to source variable X
arima_x = ARIMA(x, order=(2, 0, 1)).fit()  # or auto-select order
residuals_x = arima_x.resid

# 2. Apply same filter to Y
# Extract the AR and MA polynomials from the fitted model and filter Y
from statsmodels.tsa.filters.filtertools import recursive_filter
filtered_y = arima_x.apply(y).resid  # approximate pre-whitening

# 3. Cross-correlate the pre-whitened series
ccf_pw = sm_ccf(residuals_x, filtered_y, adjusted=True)

# Plotting with confidence bounds
fig, ax = plt.subplots(figsize=(12, 4))
confidence = 1.96 / np.sqrt(len(x))
ax.bar(range(len(ccf_pw)), ccf_pw, width=0.3)
ax.axhline(confidence, color='red', linestyle='--', label='95% CI')
ax.axhline(-confidence, color='red', linestyle='--')
ax.set_xlabel('Lag (months)')
ax.set_ylabel('Cross-correlation')
ax.set_title('Cross-correlation function (pre-whitened)')
```

**Spatiotemporal cross-correlation (parallelised with Dask):**

```python
import dask.array as da
import xarray as xr

# For gridded data cubes: compute cross-correlation at each pixel
def compute_lag_correlation(x_cube, y_cube, max_lag=12):
    """Compute optimal lag and correlation for each grid cell."""
    results = xr.Dataset()
    correlations = []
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            corr = xr.corr(x_cube.isel(time=slice(None, -lag or None)),
                           y_cube.isel(time=slice(lag, None)),
                           dim='time')
        else:
            corr = xr.corr(x_cube.isel(time=slice(-lag, None)),
                           y_cube.isel(time=slice(None, lag or None)),
                           dim='time')
        correlations.append(corr)
    # Stack and find optimal lag per pixel
    corr_stack = xr.concat(correlations, dim='lag')
    corr_stack['lag'] = range(-max_lag, max_lag + 1)
    optimal_lag = corr_stack.idxmax(dim='lag')
    max_correlation = corr_stack.max(dim='lag')
    return optimal_lag, max_correlation
```

### Strengths

- Extremely fast and simple
- Intuitive interpretation
- Easily parallelised over spatial dimensions
- Good for initial screening across thousands of variable pairs and grid cells
- Lag identification is direct

### Weaknesses

- Only detects linear association
- Confounded by shared trends, seasonality, and autocorrelation (pre-whitening required)
- No causal interpretation — correlation ≠ causation
- Sensitive to outliers
- No control for confounders
- Multiple comparison problem when screening many pairs

### Computational Complexity / Scalability

- O(T * max_lag) per pair (or O(T * log(T)) via FFT)
- Trivially parallelisable across grid cells
- Can scan the entire Causal Atlas grid (64,000 cells × multiple variable pairs) in minutes
- **This is the fastest screening method available**

### When to Use It

- **Always** as the first step: identify candidate variable pairs and lag ranges for more expensive methods
- For building "lag maps" showing how the optimal correlation lag varies across space
- For seasonal cycle analysis (e.g., rainfall leads vegetation by 1-2 months)

### How It Handles Spatial Structure

Can be computed per grid cell independently and results mapped spatially. The spatial pattern of optimal lags itself is informative (e.g., a propagating wave of lagged correlations suggests a spatial causal process). No explicit spatial modelling, but spatially structured results.

---

## 10. Anomaly Co-occurrence Analysis

### What It Detects

**Temporal co-occurrence of anomalous events across domains.** Rather than testing continuous causal relationships, this approach asks: "When domain A experiences an anomaly (e.g., extreme drought), do anomalies in domain B (e.g., conflict spike) tend to follow within a specific time window?"

### The Method

1. **Define anomalies** in each variable: exceedances of a threshold (e.g., z-score > 2 or < -2, percentile-based, or domain-specific definitions)
2. **Create binary event series** for each variable at each location
3. **Measure co-occurrence** at various lags: count how often an anomaly in X at time t is followed by an anomaly in Y at time t+τ
4. **Test significance**: compare observed co-occurrence to a null model (e.g., random shuffling of event times)

### Anomaly Detection Methods

| Method | Formula | When to Use |
|--------|---------|-------------|
| **Z-score** | $z = (x - \mu) / \sigma$ | Normal-ish distributions; threshold at ±2 or ±3 |
| **Modified Z-score (MAD)** | $z = 0.6745(x - \text{median}) / \text{MAD}$ | Robust to outliers; threshold at ±3.5 |
| **Percentile-based** | Flag values above 95th or below 5th percentile | Distribution-free; intuitive |
| **Climatological anomaly** | Deviation from long-term monthly mean | Standard in climate science |
| **Rolling Z-score** | Z-score computed on a rolling window | Non-stationary series |

### Python Implementation

```python
import numpy as np
from scipy import stats

def detect_anomalies(series, method='zscore', threshold=2.0, window=None):
    """Detect anomalies in a time series."""
    if method == 'zscore':
        z = np.abs(stats.zscore(series))
        return z > threshold
    elif method == 'mad':
        median = np.median(series)
        mad = np.median(np.abs(series - median))
        modified_z = 0.6745 * (series - median) / mad
        return np.abs(modified_z) > threshold
    elif method == 'percentile':
        low = np.percentile(series, threshold)     # e.g., 5
        high = np.percentile(series, 100 - threshold)  # e.g., 95
        return (series < low) | (series > high)
    elif method == 'rolling':
        rolling_mean = pd.Series(series).rolling(window).mean()
        rolling_std = pd.Series(series).rolling(window).std()
        z = np.abs((series - rolling_mean) / rolling_std)
        return z > threshold

def lagged_cooccurrence(events_x, events_y, max_lag=12):
    """Count co-occurrences of binary events at various lags."""
    results = {}
    for lag in range(0, max_lag + 1):
        if lag == 0:
            co_occur = np.sum(events_x & events_y)
        else:
            co_occur = np.sum(events_x[:-lag] & events_y[lag:])
        # Expected under independence
        p_x = np.mean(events_x)
        p_y = np.mean(events_y)
        n = len(events_x) - lag
        expected = n * p_x * p_y
        # Chi-squared test
        if expected > 0:
            chi2 = (co_occur - expected) ** 2 / expected
            p_value = 1 - stats.chi2.cdf(chi2, df=1)
        else:
            p_value = 1.0
        results[lag] = {
            'observed': co_occur,
            'expected': expected,
            'ratio': co_occur / expected if expected > 0 else np.nan,
            'p_value': p_value
        }
    return results

# Example: drought events → conflict spikes
drought_events = detect_anomalies(rainfall_z, method='zscore', threshold=-2.0)
conflict_events = detect_anomalies(conflict_counts, method='percentile', threshold=95)

cooccurrence = lagged_cooccurrence(drought_events, conflict_events, max_lag=12)
for lag, stats_dict in cooccurrence.items():
    if stats_dict['p_value'] < 0.05:
        print(f"Lag {lag}: observed/expected ratio = {stats_dict['ratio']:.2f}, "
              f"p = {stats_dict['p_value']:.4f}")
```

**Significance testing via permutation:**

```python
def permutation_test_cooccurrence(events_x, events_y, lag, n_permutations=1000):
    """Permutation test for co-occurrence significance."""
    observed = np.sum(events_x[:-lag] & events_y[lag:]) if lag > 0 else np.sum(events_x & events_y)
    null_distribution = []
    for _ in range(n_permutations):
        shuffled_x = np.random.permutation(events_x)
        if lag > 0:
            null_count = np.sum(shuffled_x[:-lag] & events_y[lag:])
        else:
            null_count = np.sum(shuffled_x & events_y)
        null_distribution.append(null_count)
    p_value = np.mean(np.array(null_distribution) >= observed)
    return observed, p_value, null_distribution
```

### Strengths

- Intuitive: directly answers "do extreme events co-occur?"
- Handles non-Gaussian distributions naturally
- Works with sparse events (rare extremes)
- Easy to communicate to non-technical audiences
- Flexible anomaly definitions can incorporate domain knowledge

### Weaknesses

- Information loss from binarisation (continuous→binary)
- Threshold selection is subjective
- Cannot quantify the magnitude of causal effects
- Low statistical power for rare events
- Does not control for confounders
- Simple co-occurrence ≠ causation

### Computational Complexity / Scalability

- O(T * max_lag) per variable pair — very fast
- Permutation testing: O(T * max_lag * n_permutations) — still fast
- Easily parallelised over space

### When to Use It

- **Best for**: Event-based analysis (earthquakes, floods, conflict onsets); communicating findings to policy audiences; rare extreme events; initial exploration
- **Avoid when**: You need continuous effect sizes; confounders are important; you need statistical rigour beyond simple association

### Published Examples

- EM-DAT disaster co-occurrence analyses have mapped how natural disasters cluster temporally and spatially.
- FEWS NET early warning systems use threshold-based anomaly detection for food security monitoring, triggering alerts when multiple indicators simultaneously exceed thresholds.

### How It Handles Spatial Structure

Computed independently per grid cell. Spatial patterns in co-occurrence statistics (e.g., "co-occurrence of drought and conflict is strongest in the Sahel belt") emerge from mapping the results. Can be combined with spatial clustering (LISA) of co-occurrence ratios to identify spatial hotspots of cross-domain coupling.

---

## 11. Machine Learning Approaches

### What They Detect

ML methods can detect **complex nonlinear predictive relationships** and quantify **feature importance** — which variables are most predictive of an outcome. They do not directly infer causal direction but can complement causal methods through prediction, feature screening, and causal discovery algorithms.

### 11.1 Tree-Based Methods (Random Forest, XGBoost) for Feature Importance

**What**: Fit a predictive model (e.g., predict conflict events from climate, food price, economic indicators) and use feature importance scores to identify which variables and which lags matter most.

**Key tools for interpretation:**

- **SHAP (SHapley Additive exPlanations)**: Game-theoretic approach providing local and global feature importance with direction of effect. Exact SHAP values are efficiently computed for tree models.
- **Permutation importance**: Measure accuracy drop when a feature is permuted.
- **GeoShapley**: Extension of SHAP for spatial data that treats location as a player, enabling quantification of spatial effects (Hu et al. 2024, *Annals of the American Association of Geographers*).

```python
import xgboost as xgb
import shap
import numpy as np

# Create lagged features
def create_lagged_features(df, target_col, feature_cols, max_lag=12):
    """Create lagged versions of features for temporal prediction."""
    result = df[[target_col]].copy()
    for col in feature_cols:
        for lag in range(1, max_lag + 1):
            result[f'{col}_lag{lag}'] = df[col].shift(lag)
    return result.dropna()

# Prepare data
features_df = create_lagged_features(
    df, target_col='conflict',
    feature_cols=['rainfall', 'food_price', 'temperature', 'ndvi'],
    max_lag=12
)
X = features_df.drop('conflict', axis=1)
y = features_df['conflict']

# Fit XGBoost
model = xgb.XGBRegressor(n_estimators=500, max_depth=6, learning_rate=0.05)
model.fit(X, y)

# SHAP analysis
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# Summary plot: which features and lags matter most
shap.summary_plot(shap_values, X, plot_type='bar')  # global importance
shap.summary_plot(shap_values, X)                    # direction of effects

# Dependence plot: how a specific feature affects predictions
shap.dependence_plot('rainfall_lag3', shap_values, X)

# Which lags of rainfall are most important?
rainfall_features = [c for c in X.columns if c.startswith('rainfall_lag')]
rainfall_importance = {f: np.abs(shap_values[:, X.columns.get_loc(f)]).mean()
                       for f in rainfall_features}
# This tells you the optimal lag structure empirically
```

### 11.2 Causal Discovery with ML (NOTEARS, DAG-GNN)

**NOTEARS** (Zheng et al. 2018): Formulates structure learning as a continuous optimisation problem with a DAG constraint (no cycles). Instead of searching over discrete graph structures, it optimises a score function (least squares) subject to a smooth acyclicity constraint.

**Limitations**: NOTEARS has been shown to be problematic for causal discovery with dimensional quantities (Kaiser & Sipos, 2021) and sensitive to data scaling. It tends to find DAGs that explain variance rather than true causal structure.

**DAG-GNN** (Yu et al. 2019): Uses graph neural networks for structure learning. More robust to data scaling than NOTEARS but computationally heavier.

```python
# Using gCastle (Huawei's causal discovery toolbox)
# pip install gcastle
from castle.algorithms import Notears, DAG_GNN
from castle.datasets import DAG, IIDSimulation
from castle.metrics import MetricsDAG

# NOTEARS
notears = Notears()
notears.learn(data_array)  # data_array: (T, N) numpy array
causal_matrix = notears.causal_matrix  # (N, N) adjacency matrix
# causal_matrix[i, j] != 0 means variable i causes variable j

# DAG-GNN
dag_gnn = DAG_GNN()
dag_gnn.learn(data_array)
causal_matrix = dag_gnn.causal_matrix
```

```python
# Using causal-learn (py-why project, more algorithms)
# pip install causal-learn
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ScoreBased.GES import ges

# PC algorithm (constraint-based, assumes no latent confounders)
cg = pc(data_array, alpha=0.05, indep_test='fisherz')
cg.draw_pydot_graph()  # visualise

# FCI algorithm (handles latent confounders)
g, edges = fci(data_array, independence_test_method='fisherz', alpha=0.05)

# GES (score-based, Greedy Equivalence Search)
Record = ges(data_array, score_func='local_score_BIC')
```

### 11.3 C-XGBoost (Causal XGBoost)

A recent variant that integrates causal inference with tree boosting for heterogeneous treatment effect estimation (Huebbe et al. 2024). Estimates how the causal effect of a treatment varies across units.

### Strengths (ML Approaches)

- Handle nonlinear relationships and interactions naturally
- SHAP provides interpretable, directional feature importance
- High predictive accuracy for complex systems
- Feature importance analysis can guide causal analysis (screen which variables and lags to investigate)
- gCastle and causal-learn provide unified APIs for many algorithms

### Weaknesses (ML Approaches)

- **Feature importance ≠ causation**: XGBoost can identify the most predictive features but cannot establish causal direction
- **NOTEARS limitations**: sensitivity to scaling, may not recover true causal graph
- **DAG-GNN**: computationally expensive, black-box
- **Overfitting risk**: especially with many lagged features and limited temporal data
- **No spatial awareness**: standard implementations ignore spatial structure (GeoShapley partially addresses this)

### Computational Complexity / Scalability

- **XGBoost**: O(T * N * n_trees * max_depth) — fast, GPU-accelerated
- **SHAP**: O(T * N * 2^N) in theory, but TreeSHAP is polynomial: O(T * N * max_depth^2)
- **NOTEARS**: O(N^3) per iteration for the DAG constraint; can handle N up to ~100-200
- **DAG-GNN**: GPU-accelerated but heavy; N up to ~50-100

### When to Use Them

- **XGBoost + SHAP**: As a complement to causal analysis — identify the most important predictors and optimal lag structures; run before PCMCI to narrow down variables
- **NOTEARS / DAG-GNN**: For exploratory causal discovery when you have no prior graph structure; cross-validate against PCMCI results
- **Avoid**: relying on ML feature importance alone as evidence of causation

---

## 12. Bayesian Network Methods

### What They Detect

**Directed probabilistic dependencies (causal DAGs).** Bayesian networks represent the joint probability distribution as a directed acyclic graph where edges represent direct probabilistic dependencies. Structure learning from data aims to recover this graph, which under causal assumptions represents the causal structure.

### Methods

**Score-based learning**: Search over graph structures to optimise a score (BIC, BDeu, K2):
- Hill climbing: greedy local search
- Tabu search: hill climbing with memory to avoid revisiting
- Exhaustive search: tests all possible graphs (infeasible for > ~10 variables)

**Constraint-based learning**: Test conditional independence and build the graph:
- PC algorithm: assumes no latent confounders
- FCI algorithm: allows latent confounders

**Hybrid learning** (MMHC — Max-Min Hill Climbing): First uses constraint-based methods to restrict the search space, then score-based search within that space.

**Dynamic Bayesian Networks (DBNs)**: Extend Bayesian networks to temporal data by representing variables at multiple time slices. Edges between time slices represent temporal causal relations.

### Key Assumptions

1. **Causal Markov condition**: Each variable is independent of its non-descendants given its parents
2. **Faithfulness**: All conditional independencies come from the graph structure
3. **Causal sufficiency** (PC): All common causes are observed
4. **DAG structure**: No cycles (though DBNs can represent temporal cycles)
5. **Sufficient data**: Structure learning requires enough observations to reliably estimate conditional independencies

### Python Implementation

**pgmpy (recommended for flexibility and DBN support):**

```python
import pandas as pd
from pgmpy.estimators import HillClimbSearch, BicScore, PC
from pgmpy.models import BayesianNetwork, DynamicBayesianNetwork

# Score-based structure learning
data = pd.DataFrame(data_array, columns=var_names)
hc = HillClimbSearch(data)
best_model = hc.estimate(scoring_method=BicScore(data), max_indegree=4)
print(best_model.edges())  # list of (parent, child) tuples

# Constraint-based (PC algorithm)
pc_estimator = PC(data)
estimated_model = pc_estimator.estimate(
    variant='stable',
    max_cond_vars=4,
    significance_level=0.05
)

# Dynamic Bayesian Network (temporal structure)
dbn = DynamicBayesianNetwork()
# Add edges: (variable_name, time_slice)
dbn.add_edges_from([
    (('rainfall', 0), ('food_price', 1)),     # rainfall at t → food_price at t+1
    (('food_price', 0), ('conflict', 1)),      # food_price at t → conflict at t+1
    (('conflict', 0), ('conflict', 1)),        # conflict persistence
])

# Parameter learning
from pgmpy.estimators import MaximumLikelihoodEstimator
dbn.fit(data, estimator=MaximumLikelihoodEstimator)

# Inference
from pgmpy.inference import DBNInference
dbn_inf = DBNInference(dbn)
result = dbn_inf.query(
    variables=[('conflict', 1)],
    evidence={('rainfall', 0): 'low', ('food_price', 0): 'high'}
)
```

**bnlearn (simpler API, good visualisation):**

```python
import bnlearn as bn

# Structure learning
model = bn.structure_learning.fit(data, methodtype='hc', scoretype='bic')

# Plot the learned structure
bn.plot(model)

# Parameter learning
model = bn.parameter_learning.fit(model, data, methodtype='bayes')

# Inference
query = bn.inference.fit(model, variables=['conflict'],
                         evidence={'rainfall': 'low', 'food_price': 'high'})
```

**CausalNex (McKinsey's Bayesian causal inference library):**

```python
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork

# Structure learning using NOTEARS
sm = from_pandas(data, tabu_edges=[], w_threshold=0.1)

# Create Bayesian Network
bn = BayesianNetwork(sm)
bn = bn.fit_node_states(data)
bn = bn.fit_cpds(data, method='BayesianEstimator', bayes_prior='K2')

# Inference and intervention
from causalnex.inference import InferenceEngine
ie = InferenceEngine(bn)
ie.query({'conflict': 'high'})  # What is P(conflict=high)?

# Interventional query: what if we intervene on food_price?
ie.do_intervention('food_price', 'low')
ie.query({'conflict': 'high'})  # P(conflict=high | do(food_price=low))
ie.reset_do('food_price')
```

### Strengths

- Principled probabilistic framework
- Causal DAGs have clear interpretation
- Interventional queries possible (do-calculus)
- DBNs handle temporal structure
- Multiple learning algorithms available
- Can incorporate prior knowledge (required/forbidden edges)
- pgmpy is well-maintained and published in JMLR (2024)

### Weaknesses

- Score-based methods are NP-hard in general (exponential in number of variables)
- Constraint-based methods sensitive to significance threshold
- Requires discretisation for discrete BNs (information loss) or Gaussian assumptions for continuous
- DAG assumption: cannot represent cycles (which may exist in some systems)
- Causal interpretation requires strong assumptions (faithfulness, causal sufficiency)
- DBNs are limited to first-order Markov for tractability

### Computational Complexity / Scalability

- **Hill climbing with BIC**: O(N^2) per step, heuristic stopping; practical for N up to ~50-100
- **PC algorithm**: O(N^d) where d is the maximum conditioning set size; exponential worst case
- **DBN fitting**: O(T * N * |parents|^max); scales with time series length
- **Inference**: depends on tree-width of the graph; exact inference is NP-hard, approximate methods (variational, sampling) are more scalable

### When to Use Them

- **Best for**: Building interpretable causal models with domain knowledge; interventional reasoning; communicating causal structure; small to moderate numbers of variables (< 50)
- **Avoid when**: Many variables; no prior knowledge to constrain structure; need spatial analysis; purely exploratory (PCMCI may be better)

### Published Examples

- Dynamic Bayesian Networks have been used to model food security causal chains in East Africa (drought → crop failure → food insecurity → displacement → conflict).
- Bayesian networks are common in epidemiological causal analysis: modelling pollution → respiratory disease pathways.

### How It Handles Spatial Structure

**Poorly in standard form.** DBNs operate on multivariate time series without spatial awareness. Approaches:
- Include spatially lagged variables as additional nodes
- Build separate networks per region and compare structures
- Use network meta-analysis to identify common and region-specific causal paths

---

## 13. Difference-in-Differences and Regression Discontinuity

### What They Detect

**Causal effects under quasi-experimental conditions.** These are the closest to true causal identification from observational data, but they require specific data structures (treatment/control groups, sharp cutoffs).

### 13.1 Difference-in-Differences (DiD)

**Setting**: A treatment (e.g., a natural disaster, policy intervention) affects some units (locations) but not others, and we observe both before and after the event.

**Method**: Compare the change in outcomes for treated units to the change for control units:

$$\text{DiD} = (\bar{Y}_{\text{treated, after}} - \bar{Y}_{\text{treated, before}}) - (\bar{Y}_{\text{control, after}} - \bar{Y}_{\text{control, before}})$$

Regression form:

$$Y_{it} = \alpha + \beta_1 \text{Treated}_i + \beta_2 \text{Post}_t + \beta_3 (\text{Treated}_i \times \text{Post}_t) + \epsilon_{it}$$

The coefficient β₃ is the causal effect estimate.

**Key assumption — Parallel Trends**: In the absence of treatment, treated and control units would have followed the same trend. This is testable by checking pre-treatment trends.

**Staggered DiD**: When different units receive treatment at different times. Recent econometric advances (Callaway & Sant'Anna 2021, Sun & Abraham 2021) show that the standard two-way fixed effects (TWFE) estimator can be biased with staggered treatment timing. Use robust estimators.

### 13.2 Regression Discontinuity Design (RDD)

**Setting**: Treatment is assigned based on a continuous "running variable" crossing a threshold (e.g., regions above vs below a drought severity threshold receive aid).

**Method**: Compare outcomes for units just above and just below the threshold:

$$Y_i = \alpha + \beta_1 X_i + \beta_2 D_i + \beta_3 (X_i \times D_i) + \epsilon_i$$

where $D_i = 1$ if $X_i > c$ (the threshold). β₂ is the local average treatment effect at the cutoff.

**Types**: Sharp RDD (treatment deterministically assigned at cutoff) and Fuzzy RDD (treatment probability changes at cutoff).

### Python Implementation

**Difference-in-Differences:**

```python
import statsmodels.formula.api as smf
import pandas as pd

# Standard DiD regression
model = smf.ols('outcome ~ treated + post + treated:post + C(unit) + C(time)',
                data=panel_df).fit(cov_type='cluster', cov_kwds={'groups': panel_df['unit']})
# treated:post coefficient is the DiD estimate
print(model.summary())

# Using CausalPy (Bayesian DiD)
# pip install CausalPy
import causalpy as cp

result = cp.pymc_experiments.DifferenceInDifferences(
    panel_df,
    formula='outcome ~ 1 + treated:post',
    time_variable_name='time',
    group_variable_name='unit',
    treated=treated_units,
    model=cp.pymc_models.LinearRegression()
)
result.plot()
result.summary()
```

**Regression Discontinuity:**

```python
# Using rdrobust (R package via rpy2, or statsmodels for basic)
# Basic RDD
import statsmodels.formula.api as smf

# Restrict to bandwidth around cutoff
bandwidth = 10
rdd_df = df[(df['running_var'] > cutoff - bandwidth) &
            (df['running_var'] < cutoff + bandwidth)]
rdd_df['above'] = (rdd_df['running_var'] > cutoff).astype(int)
rdd_df['centered'] = rdd_df['running_var'] - cutoff

model = smf.ols('outcome ~ above * centered', data=rdd_df).fit()
print(f"RDD estimate: {model.params['above']:.3f}")

# Using CausalPy (Bayesian RDD)
result = cp.pymc_experiments.RegressionDiscontinuity(
    df,
    formula='outcome ~ 1 + running_var + above',
    running_variable_name='running_var',
    model=cp.pymc_models.LinearRegression(),
    treatment_threshold=cutoff
)
result.plot()
```

### Spatiotemporal Extensions

**Spatial DiD**: When treatment and control groups are defined spatially (e.g., locations affected vs not affected by an earthquake). Must account for:
- Spatial spillovers: treatment at location A affects nearby control locations (violates SUTVA)
- Spatial autocorrelation in errors: cluster standard errors spatially
- Solution: spatial matching frameworks (Kolak & Anselin 2020); buffer zones between treated and control areas

**Key paper**: Papadogeorgou et al. (2022), "Toward Causal Inference for Spatio-Temporal Data: Conflict and Forest Loss in Colombia," published in *Journal of the American Statistical Association*. Proposed a causal framework for spatiotemporal data with nonparametric hypothesis testing, finding heterogeneous effects of conflict on deforestation across Colombian provinces.

### Strengths

- **Strongest causal identification** among observational methods (under valid assumptions)
- Intuitive and easily communicated
- DiD is widely used and accepted in policy evaluation
- Bayesian implementations (CausalPy) provide full uncertainty quantification
- Can estimate causal effect magnitudes, not just direction

### Weaknesses

- **Requires quasi-experimental structure**: not always available
- **Parallel trends assumption** (DiD): strong and often untestable beyond pre-treatment period
- **Local estimates** (RDD): only valid at the cutoff, not globally
- **Spatial interference**: treatment at one location affects neighbours (standard DiD assumes no interference)
- **Staggered treatment**: standard TWFE is biased; need modern estimators
- **Limited to specific questions**: "did this event/policy cause this outcome?" — not for continuous causal network discovery

### Computational Complexity / Scalability

- **DiD**: Standard OLS regression — O(N * T) for basic model; O(N^2) for spatial clustering
- **RDD**: Local regression — fast; bandwidth selection requires cross-validation
- These are very computationally cheap

### When to Use Them

- **DiD**: When a discrete event (natural disaster, conflict onset, policy change) affects some locations but not others; for estimating the causal impact of specific events
- **RDD**: When treatment is assigned based on a threshold (aid eligibility, disaster classification)
- **For Causal Atlas**: Apply after cross-domain screening identifies candidate causal events; use to estimate the magnitude and significance of specific causal links identified by other methods

### Published Examples

- **Hsiang et al. (2013)**: "Quantifying the influence of climate on human conflict." Used panel regression (DiD-like framework) to estimate climate-conflict effects. Published in *Science*.
- **Papadogeorgou et al. (2022)**: "Toward Causal Inference for Spatio-Temporal Data: Conflict and Forest Loss in Colombia." Published in *JASA*.
- **Crost & Felter (2020)**: Used DiD with a rainfall threshold as an instrument for crop failure to estimate the effect of economic shocks on conflict in the Philippines.

### How It Handles Spatial Structure

DiD can be enhanced with spatial matching (match treated and control locations based on spatial characteristics), spatial clustering of standard errors, and buffer zones. RDD naturally handles spatial discontinuities (e.g., administrative borders, distance from an event). Both benefit from the spatial regression diagnostics discussed in Section 6.

---

## 14. Comparison Table

| Method | Type of Causality | Linearity | Handles Nonlinear | Min T | Max N (practical) | Spatial Awareness | Confounder Control | Python Package | Computational Cost |
|--------|------------------|-----------|-------------------|-------|-------------------|-------------------|--------------------|----------------|-------------------|
| **Granger Causality** | Predictive | Linear (standard) | Extensions exist | ~50 | ~20 (bivariate: unlimited) | No (extensions exist) | Conditional GC | `statsmodels` | Low |
| **Transfer Entropy** | Predictive (info-theoretic) | Model-free | Yes | ~500 (continuous) | ~20 (multivariate) | No | Multivariate TE (IDTxl) | `PyInform`, `JIDT`, `IDTxl` | Medium-High |
| **PCMCI** | Structural | Depends on test | Yes (CMIknn, GPDC) | ~100 | ~50-100 | Partial | Yes (parents) | `tigramite` | Medium-High |
| **CCM** | Dynamical coupling | Nonlinear | Yes (native) | ~100 (spatial: ~5) | Pairwise | Multispatial CCM | No | `pyEDM`, `causal_ccm` | Medium |
| **Spatial Lag/Error** | Association (spatial) | Linear | No | Cross-section | ~50,000+ | Yes (native) | Spatial structure | `spreg` (PySAL) | Medium |
| **Moran's I / LISA** | Spatial association | N/A | N/A | Cross-section | ~100,000+ | Yes (native) | No | `esda` (PySAL) | Low |
| **VAR** | Predictive (multivariate) | Linear | Threshold VAR | ~50 | ~15-20 | No (SpVAR custom) | Within-model | `statsmodels` | Low-Medium |
| **Cross-Correlation** | Association | Linear | No | ~30 | Unlimited pairs | Per-cell | No | `scipy.signal` | Very Low |
| **Anomaly Co-occurrence** | Event association | N/A | N/A | ~30 | Unlimited | Per-cell | No | Custom (numpy/scipy) | Very Low |
| **XGBoost + SHAP** | Predictive importance | Nonlinear | Yes | ~200 | ~100+ features | GeoShapley | Feature inclusion | `xgboost`, `shap` | Low-Medium |
| **NOTEARS / DAG-GNN** | Structural (DAG) | Depends | Some | ~200 | ~50-200 | No | Graph structure | `gcastle`, `causal-learn` | Medium-High |
| **Bayesian Networks** | Structural (DAG) | Depends | Discrete BN: nonlinear | ~200 | ~30-50 | DBN for temporal | Graph structure | `pgmpy`, `bnlearn` | Medium-High |
| **DiD** | Causal effect | Linear (standard) | Extensions | ~20+ per group | ~50,000+ | Spatial matching | Design-based | `statsmodels`, `CausalPy` | Very Low |
| **RDD** | Local causal effect | Local linear | Nonparametric | ~100 near cutoff | ~50,000+ | Natural spatial | Design-based | `CausalPy` | Very Low |

---

## 15. Recommended Pipeline for Causal Atlas

Given the Causal Atlas design (0.5° × 0.5° grid, monthly resolution, multi-domain data), here is a staged analysis pipeline from fast screening to rigorous causal inference.

### Stage 1: Exploratory Spatial Analysis (per variable, per time step)

**Goal**: Understand the spatial structure of each variable independently.

**Methods**:
- **Global Moran's I** on each variable at each time step → Is the variable spatially clustered?
- **LISA (Local Moran's I)** → Where are the hotspots and coldspots?
- **Bivariate Moran's I** between variable pairs → Are cross-domain spatial patterns correlated?

**Tools**: `esda` (PySAL), `splot` for visualisation

**Output**: Maps of spatial clusters; identification of variables with strong spatial structure; diagnostic information for later stages.

**Compute time**: Minutes for global grid.

### Stage 2: Temporal Screening (per grid cell, all variable pairs)

**Goal**: Identify candidate causal pairs and optimal lag structures across the entire grid.

**Methods**:
- **Cross-correlation with lag analysis** (pre-whitened) for all variable pairs at each grid cell
- Map the optimal lag and correlation strength spatially
- Apply **FDR correction** for multiple comparisons

**Tools**: `scipy.signal.correlate`, `statsmodels` for pre-whitening, `xarray`/`dask` for parallelisation

**Output**: For each variable pair, a spatial map of optimal lag and correlation strength. Candidate pairs for further analysis.

**Compute time**: Minutes to hours for global grid (embarrassingly parallel).

### Stage 3: Anomaly Co-occurrence (per grid cell)

**Goal**: Identify where extreme events in one domain are followed by extreme events in another.

**Methods**:
- Define anomalies using domain-appropriate thresholds (z-score, percentile, climatological)
- Compute lagged co-occurrence ratios with permutation-based significance testing
- Map co-occurrence hotspots

**Tools**: Custom code (numpy, scipy), `esda` for spatial clustering of results

**Output**: Maps of anomaly co-occurrence patterns; identification of event-driven causal links.

**Compute time**: Minutes.

### Stage 4: Pairwise Causal Testing (candidate pairs from Stage 2)

**Goal**: Test for predictive causality between the top candidate pairs identified in screening.

**Methods**:
- **Granger causality** (fast, linear) for all candidate pairs
- **Transfer entropy** (where nonlinearity is suspected and data is sufficient)
- **Panel Granger causality** (Dumitrescu-Hurlin) pooling across grid cells for each pair

**Tools**: `statsmodels` (Granger, VAR), `PyInform` or `IDTxl` (transfer entropy)

**Output**: Directed pairwise relationships with lag structures and effect sizes; separation of linear vs nonlinear effects.

**Compute time**: Hours.

### Stage 5: Causal Graph Discovery (regional, multi-variable)

**Goal**: Discover the causal graph structure among multiple variables, distinguishing direct from indirect effects.

**Methods**:
- **PCMCI with ParCorr** (linear, fast) on regional aggregates (admin-1 or admin-2 level)
- **PCMCI with CMIknn** (nonlinear) where Stage 4 suggests nonlinear relationships
- **LPCMCI** where latent confounders are suspected
- **Bayesian network structure learning** (pgmpy) as a cross-check

**Tools**: `tigramite`, `pgmpy`

**Output**: Causal graphs per region showing direct causal links with time lags; comparison of graph structures across regions.

**Compute time**: Hours to days depending on number of variables and regions.

### Stage 6: ML-Assisted Feature Importance and Validation

**Goal**: Validate causal findings using predictive modelling; discover complex nonlinear interactions missed by Stage 5.

**Methods**:
- **XGBoost with SHAP** to rank feature importance and optimal lags
- Compare SHAP-identified important features with PCMCI-identified causal links
- **CCM** for variable pairs where dynamical coupling is hypothesised
- Agreement across methods increases confidence in causal claims

**Tools**: `xgboost`, `shap`, `pyEDM`

**Output**: Ranked feature importance; validation of causal graph; identified nonlinear interactions.

**Compute time**: Hours.

### Stage 7: Causal Effect Estimation (specific events)

**Goal**: Estimate the magnitude of causal effects for specific events or interventions.

**Methods**:
- **DiD** for discrete events (major earthquakes, conflict onsets, policy changes) using pre-identified spatial control groups
- **Spatial lag models** to account for spillover effects in effect estimation
- **RDD** where natural thresholds exist

**Tools**: `CausalPy`, `statsmodels`, `spreg` (PySAL)

**Output**: Quantified causal effect sizes with confidence intervals for specific events.

**Compute time**: Minutes per event.

### Pipeline Summary Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: Spatial Exploration (Moran's I, LISA)                  │
│ → Understand spatial structure of each variable                 │
├─────────────────────────────────────────────────────────────────┤
│ Stage 2: Temporal Screening (Cross-correlation with lags)       │
│ → Identify candidate pairs and lag ranges                       │
├─────────────────────────────────────────────────────────────────┤
│ Stage 3: Anomaly Co-occurrence                                  │
│ → Event-based associations; extreme event pairing               │
├─────────────────────────────────────────────────────────────────┤
│ Stage 4: Pairwise Causal Testing (Granger, Transfer Entropy)    │
│ → Directed predictive causality; linear and nonlinear           │
├─────────────────────────────────────────────────────────────────┤
│ Stage 5: Causal Graph Discovery (PCMCI, Bayesian Networks)      │
│ → Full causal graph with confounders controlled                 │
├─────────────────────────────────────────────────────────────────┤
│ Stage 6: ML Validation (XGBoost+SHAP, CCM)                     │
│ → Cross-validate findings; discover nonlinear interactions      │
├─────────────────────────────────────────────────────────────────┤
│ Stage 7: Causal Effect Estimation (DiD, RDD, Spatial Regression)│
│ → Quantify specific causal effects with uncertainty             │
└─────────────────────────────────────────────────────────────────┘
```

### Key Python Dependencies

```
# Core statistical methods
statsmodels>=0.14       # Granger causality, VAR, OLS, ARIMA
scipy>=1.11             # Cross-correlation, signal processing
tigramite>=5.2          # PCMCI, PCMCI+, LPCMCI

# Spatial analysis
libpysal>=4.9           # Spatial weights
esda>=2.5               # Moran's I, LISA
spreg>=1.4              # Spatial regression

# Information theory
pyinform>=0.2           # Transfer entropy (discrete)
# JIDT via jpype        # Transfer entropy (continuous)
idtxl>=1.5              # Multivariate transfer entropy

# Causal discovery
pgmpy>=0.0.15           # Bayesian networks, DBNs
causal-learn>=0.1.3     # PC, FCI, GES algorithms
gcastle>=1.0.3          # NOTEARS, DAG-GNN

# Empirical dynamic modelling
pyEDM>=2.0              # CCM, simplex projection

# Machine learning
xgboost>=2.0            # Gradient boosting
shap>=0.44              # SHAP values

# Causal effect estimation
CausalPy>=0.4           # DiD, RDD (Bayesian)

# Data handling
xarray>=2024.01         # Gridded data operations
dask>=2024.01           # Parallel computation
```

---

## 16. Sources

### Foundational Papers

- Granger, C. W. J. (1969). "Investigating Causal Relations by Econometric Models and Cross-spectral Methods." *Econometrica*, 37(3), 424-438.
- Schreiber, T. (2000). "Measuring Information Transfer." *Physical Review Letters*, 85(2), 461.
- Barnett, L., Barrett, A. B., & Seth, A. K. (2009). "Granger Causality and Transfer Entropy Are Equivalent for Gaussian Variables." *Physical Review Letters*, 103(23), 238701.
- Sugihara, G., et al. (2012). "Detecting Causality in Complex Ecosystems." *Science*, 338(6106), 496-500.
- Runge, J., et al. (2019). "Detecting and quantifying causal associations in large nonlinear time series datasets." *Science Advances*, 5(11), eaau4996. https://www.science.org/doi/10.1126/sciadv.aau4996
- Clark, A. T., et al. (2015). "Spatial convergent cross mapping to detect causal relationships from short time series." *Ecology*, 96(5), 1174-1181. https://esajournals.onlinelibrary.wiley.com/doi/abs/10.1890/14-1479.1
- Anselin, L. (1995). "Local Indicators of Spatial Association — LISA." *Geographical Analysis*, 27(2), 93-115.

### Applied Papers (Climate-Conflict Domain)

- Runge, J., et al. (2020). "Causal networks for climate model evaluation and constrained projections." *Nature Communications*, 11, 1415. https://www.nature.com/articles/s41467-020-15195-y
- Thalheimer, L., et al. (2024). "Causal discovery reveals complex patterns of drought-induced displacement." *Nature Communications Earth & Environment*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11387590/
- Papadogeorgou, G., et al. (2022). "Toward Causal Inference for Spatio-Temporal Data: Conflict and Forest Loss in Colombia." *Journal of the American Statistical Association*, 117(538). https://www.tandfonline.com/doi/full/10.1080/01621459.2021.2013241
- Hsiang, S. M., et al. (2011). "Civil conflicts are associated with the global climate." *Nature*, 476, 438-441.
- Silva, V. B. R., et al. (2021). "Detecting Climate Teleconnections With Granger Causality." *Geophysical Research Letters*. https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021GL094707

### Software Documentation

- statsmodels VAR documentation: https://www.statsmodels.org/stable/vector_ar.html
- statsmodels Granger causality: https://www.statsmodels.org/stable/generated/statsmodels.tsa.vector_ar.var_model.VARResults.test_causality.html
- Tigramite documentation: https://jakobrunge.github.io/tigramite/
- Tigramite GitHub: https://github.com/jakobrunge/tigramite
- PySAL spreg documentation: https://pysal.org/spreg/
- PySAL esda documentation: https://pysal.org/esda/generated/esda.Moran.html
- PySAL esda Moran_Local: https://pysal.org/esda/generated/esda.Moran_Local.html
- PyInform documentation: https://elife-asu.github.io/PyInform/
- JIDT documentation: https://jlizier.github.io/jidt/
- JIDT Python examples: https://github.com/jlizier/jidt/wiki/PythonExamples
- IDTxl documentation: https://github.com/pwollstadt/IDTxl
- pyEDM GitHub: https://github.com/SugiharaLab/pyEDM
- fastEDM-python: https://github.com/EDM-Developers/fastEDM-python/
- causal_ccm GitHub: https://github.com/PrinceJavier/causal_ccm
- pgmpy documentation: https://pgmpy.org/
- pgmpy DBN: https://pgmpy.org/models/dbn.html
- bnlearn PyPI: https://pypi.org/project/bnlearn/
- bnlearn GitHub: https://github.com/erdogant/bnlearn
- CausalNex documentation: https://causalnex.readthedocs.io/en/latest/01_introduction/01_introduction.html
- causal-learn documentation: https://causal-learn.readthedocs.io/
- causal-learn GitHub: https://github.com/py-why/causal-learn
- gCastle GitHub/paper: https://arxiv.org/abs/2111.15155
- gCastle PyPI: https://pypi.org/project/gcastle/
- CausalPy (PyMC Labs): https://www.pymc-labs.com/blog-posts/causalpy-a-new-package-for-bayesian-causal-inference-for-quasi-experiments
- CausalFlow: https://github.com/lcastri/causalflow
- SciPy correlate: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html
- SciPy correlation_lags: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlation_lags.html
- GeoShapley: https://www.tandfonline.com/doi/full/10.1080/24694452.2024.2350982
- CausalST_Papers collection: https://github.com/yutong-xia/CausalST_Papers

### Methodological Reviews

- Runge, J., et al. (2023). "Causal inference for time series." *Nature Reviews Methods Primers*.
- Review of spatial causal inference methods: https://pmc.ncbi.nlm.nih.gov/articles/PMC10187770/
- Beenstock, M. & Felsenstein, D. (2007). "Spatial Vector Autoregressions." *Spatial Economic Analysis*, 2(2). https://www.tandfonline.com/doi/pdf/10.1080/17421770701346689
- Scalable causal structure learning review: https://pmc.ncbi.nlm.nih.gov/articles/PMC9890349/
- Kaiser & Sipos (2021). "Unsuitability of NOTEARS for Causal Graph Discovery when Dealing with Dimensional Quantities." *Neural Processing Letters*. https://link.springer.com/article/10.1007/s11063-021-10694-5
- Causal Discovery in Python (JMLR 2024): https://www.jmlr.org/papers/volume25/23-0970/23-0970.pdf
- Guide to Bayesian Networks software: https://pmc.ncbi.nlm.nih.gov/articles/PMC12415694/
