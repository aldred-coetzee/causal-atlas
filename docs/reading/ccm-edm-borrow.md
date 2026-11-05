# Can we borrow CCM and EDM from ecology for our data?

2026-11-05. Bounded reading check; it checks the assertion and does not recommend a plan change.
Question: what do convergent cross mapping (CCM) and empirical dynamic modelling (EDM) need, how do they fail, and have they been used on social or sparse count data?

## Verdict: only if

Only if the series behave like a low-noise deterministic system settled on an attractor, which monthly conflict counts do not obviously do. Conditions the sources point to:
1. Seasonality is handled by an explicit seasonal-surrogate null, and synchrony between regions is treated as a warning, not a result. The surrogate remedy is known here only from snippets; it could not be opened.
2. The method first recovers planted links, and rejects planted nulls, on a synthetic panel that looks like ours (sparse, noisy, seasonal).
3. Zero-heavy counts are shown to work in that test. I found no study that does this.

## What the methods need, against our data

- Needs: Cobey and Baskerville (preprint, tested on simulations and infection records) say CCM "is optimized for dynamics that have converged to a deterministic attractor" and "remains sensitive to high levels of process noise". Enough length for cross-map skill to converge as more data is used.
- Length: a search summary says CCM is "typically used with about 30 or more observations" (snippet only). Ours is 432 months per cell, so length is not the issue.
- Multispatial CCM (Clark et al. 2015) pools many short replicate series and reports detection "with as few as five sequential observations" despite process noise and observation error. Its tests were on "simulated and real-world ecological data"; the page I opened does not name them. Our 10,000 cells are the replicate case, but they are not independent: neighbours share regional episodes.
- Our data: sparse counts, mostly zeros, strong persistence, shared seasonality, multi-year regional episodes, inputs SPEI and ONI that are themselves seasonal or slow. Each of these cuts against the stated requirements.

## Published criticisms that apply

- Cobey and Baskerville: the original criterion "is extremely sensitive to periodic fluctuations" and reports links between independent strains with similar cycles. A stricter lag criterion cuts false positives but misses weak links and links in noisy systems. Transient or drifting dynamics gave false positives and negatives; with weak driving the right link was found in 19 of 100 runs that included transients, against always once they had passed, and a reverse link was wrongly found in 21 of 100. They also say the original criterion's sensitivity to periodic fluctuations "vanishes with alternative criteria". Different state-space reconstruction choices gave different answers. Their tests were on infection models and records, not conflict.
- Seasonal forcing and synchrony (snippet only): the Sugihara group concedes synchrony can make a one-way effect look two-way, and defends a seasonal-surrogate test (Deyle et al. 2016 on influenza). A recent reviewed preprint says the choice of which variable to surrogate can swing false-positive rates a lot. I could not open these texts.
- McCracken and Weigel: in simple linear and nonlinear systems the CCM "driver" changed with parameters (for example source frequency). They say CCM did not reliably match intuitive driving.

## Uses outside ecology

- Epidemics: influenza and humidity (Deyle et al. 2016), contested by Baskerville and Cobey (snippet only).
- Climate and conflict: Guo, Sun and Wilson (COMPLEXIS 2023, an exploratory conference paper) compared Predictability Improvement, CCM and conditional mutual information on ERA5 rainfall and temperature (0.5 degree, monthly) against Global Terrorism Database attack counts for 12 world regions, 1970-2018. They report rainfall as a fairly general indicator, strongest in parts of Africa and South Asia, with lags near 1 and 3 years, read from one method's figures (CMI). They say the methods disagree in some regions and that social-science knowledge is needed to filter spurious causality. This is region-level, with terrorism as a proxy. It is not cell-level and not UCDP.
- Crime: a geographical-CCM paper uses simulated Chicago data (snippet only).
- Sparse or zero-heavy counts: I found no CCM or EDM study on them.

## Not verified, not checked

- Sugihara 2012 full text and the EDM FAQ (Munch et al. 2020): PDFs would not extract, so the original data requirements are second-hand.
- Deyle 2016, the Sugihara reply and PMC pages refused automated access; claims on them are snippet only.
- I did not check EDM forecasting results on counts, Granger or transfer-entropy alternatives, or any run of the code.

## Spot-check by the session that commissioned this

Opened at source: Clark et al., Cobey and Baskerville, Guo et al. Clark held. On Cobey and Baskerville, "stationary" does not appear in the paper and was removed, and the 19 of 100 and the criterion's qualifier were completed. Deyle et al. 2016 was tried again and refused (reCAPTCHA, then 403), so condition 1's remedy stays snippet only. Not re-checked: McCracken and Weigel, and everything marked snippet only.

## Sources

- Sugihara et al. 2012, Science 338:496, doi:10.1126/science.1227079 (snippet only) https://api.crossref.org/works/10.1126%2FSCIENCE.1227079
- Clark et al. 2015, Ecology 96(5):1174, doi:10.1890/14-1479.1 https://experts.umn.edu/en/publications/spatial-convergent-cross-mapping-to-detect-causal-relationships-f/
- Cobey and Baskerville, arXiv 1601.00716 https://ar5iv.labs.arxiv.org/html/1601.00716
- McCracken and Weigel, arXiv 1407.5696 https://ar5iv.labs.arxiv.org/html/1407.5696v1
- Climate-society-conflict, SCITEPRESS 2023 https://scitepress.org/publishedPapers/2023/119684/pdf/index.html
- Deyle et al. 2016, PNAS, doi:10.1073/pnas.1607747113 (snippet only) https://pmc.ncbi.nlm.nih.gov/articles/PMC5135385
- Baskerville and Cobey comment and reply (snippet only) https://pmc.ncbi.nlm.nih.gov/articles/PMC5373349
- Munch et al. 2020 FAQ, doi:10.1093/icesjms/fsz209 (not read) https://par.nsf.gov/servlets/purl/10230196
