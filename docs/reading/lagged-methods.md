# Lagged-relationship methods for a sparse-count climate-conflict panel

Date: 2026-11-05

**Question.** For an Africa cell-month panel (about 10,000 cells, 432 months, sparse UCDP counts, strong persistence and seasonality; SPEI and ONI as inputs), which lagged-relationship methods have published evidence of working, on what assumptions, with what failure modes, and has any been applied to climate and conflict?

## Answer

I found no published evidence that PCMCI, convergent cross mapping (CCM) or Granger-type tests work on sparse zero-inflated counts at this scale. What exists is for continuous series, small systems or simulations. The one benchmark on gridded data reports poor PCMCI performance. Most climate-conflict work found uses lagged panel regressions and forests. One exploratory conference paper uses CCM, at region level, and its methods disagree (see `ccm-edm-borrow.md`). A recent annual forecasting result is that weather impacts add nothing beyond conflict history, governance and socio-economic variables. This is thin evidence, from a bounded search; it is not a survey.

## Methods

| Method | Assumptions | Evidence found, and on what data | Failure modes that bear on this panel |
|---|---|---|---|
| PCMCI / PCMCI+ | Stationary, time-lagged links, causal sufficiency (survey description, snippet only) | Original paper: climate and heart-physiology series plus synthetic data; abstract only, snippet only. | Runge (2020): autocorrelation makes the plain PC algorithm "much less reliable"; PCMCI+ is said to fix this. All tests on continuous data. Nothing found on zero-inflated counts. |
| PCMCI on grids | As above | Sandia benchmark on simulated 1-D and 2-D spatial autoregressions: direct application "is not suitable" for gridded systems "without significant preprocessing and downscaling"; "requires unrealistic sample sizes"; "a notable curse of dimensionality". The findings are hedged ("Our findings suggest"). Simulated, not conflict. | Direct warning for 10,000 spatially linked cells. |
| CCM (state-space) | Deterministic-ish dynamics on an attractor | Cobey and Baskerville (infectious disease): the original criterion is "extremely sensitive to periodic fluctuations", a sensitivity they say "vanishes with alternative criteria", which have other weaknesses; conclusions varied with reconstruction choices. A reply (Sugihara et al., snippet only) says periodic drivers defeat the lag test. | Seasonality is the central problem here. Noise and drifting conditions also hurt. No cell-level or sparse-count use found; one region-level use on terrorism counts, below. |
| Granger-type, panel forms | Linear, stationary; the past of X improves prediction of Y | I found no study applying a formal Granger test to gridded climate and conflict. Definition from a search summary only. | Not verified for zero-inflated counts; no sources opened. |
| Count-aware causal discovery (ZiG-DAG, Choi and Ni, JMLR 2023) | Zero-inflated counts, no time ordering | Synthetic data and gene-expression data. | Handles zeros but not lags or time series, as far as the abstract says. |

## Applied to climate and conflict

- Harari and La Ferrara (snippet only): cell-year panel of Africa with lagged SPEI and spatial and temporal lags of conflict; growing-season shocks raise conflict. A dynamic regression, not a Granger test.
- Michelini et al. 2023 (abstract opened): random-forest forecasts of African conflict, 1994 to 2012. Adding weather impacts to models with conflict history and socioeconomic variables does not improve them; such impacts "do not contain any unique information for forecasting annual conflict incidence". Annual data, not monthly; drought, floods, crop shocks and cyclones, not SPEI or ONI. Spatial unit not stated on the abstract page.
- Michelini 2025 (snippet only): title says drought effects are "primarily explained by pre-existing conflict risk"; uses a zero-inflated negative binomial with cell and year effects.
- Guo, Sun and Wilson 2023 (conference paper, opened in the spot-check): PI, CCM and CMI on ERA5 against Global Terrorism Database monthly counts, 12 world regions, 1970 to 2018. Exploratory; results from different methods are inconsistent.
- Method dispute: Burke et al. versus Buhaug (PNAS 2010). Buhaug says the link vanishes with other climate datasets and a different war definition; Burke says fixed effects are essential and Buhaug cherry-picked. Both from search excerpts.

## Not verified, not checked

- I could not open the PCMCI papers (Science Advances: 403; Nature Communications: redirect to login). PCMCI claims come from the Runge 2020 arXiv abstract, a search summary and the Sandia abstract. I did not confirm the 2019 Nature Communications paper's text on Granger or CCM.
- Not checked: tigramite's own docs on discrete data, spatial-panel Granger tests, hurdle or Poisson Granger variants, conflict-forecasting competitions, whether the Sandia result holds on real data.

## Spot-check by the session that commissioned this

Opened at source: Sandia, Cobey and Baskerville, Michelini et al. 2023, Guo et al. Three things were corrected: two quotations that were not verbatim, a qualifier dropped from the CCM claim, and the statement that no CCM use on conflict existed. Not re-checked: Runge 2020, Choi and Ni, and everything marked snippet only.

## Sources

- Runge et al. 2019, Sci. Adv., doi 10.1126/sciadv.aau4996 (search result only): https://centaur.reading.ac.uk/89762
- Runge et al. 2019, Nat. Commun., doi 10.1038/s41467-019-10105-3 (snippet only): https://rsc4earth.de/publication/runge-inferring-2019/
- Runge 2020, PCMCI+: https://arxiv.org/abs/2003.03685v1
- Nichol et al. 2023, Sandia, doi 10.2172/1991387: https://www.sandia.gov/ccr/publications/details/benchmarking-the-pcmci-causal-discovery-algorithm-for-spatiotemporal-system-2023-06-01/
- Cobey and Baskerville 2016: https://ar5iv.labs.arxiv.org/html/1601.00716
- Choi and Ni 2023: https://jmlr.org/papers/v24/21-1476.html
- Michelini et al. 2023, doi 10.1057/s41599-023-01996-1: https://ideas.repec.org/a/pal/palcom/v10y2023i1d10.1057_s41599-023-01996-1.html
- Michelini 2025, doi 10.1088/1748-9326/ae16c0 (snippet only): https://publications.pik-potsdam.de/pubman/item/item_33533
- Harari and La Ferrara (snippet only): https://faculty.wharton.upenn.edu/wp-content/uploads/2017/09/HarariLaFerrara_Dec2017.pdf
- Guo, Sun and Wilson 2023, COMPLEXIS, doi 10.5220/0011968400003485: https://scitepress.org/publishedPapers/2023/119684/pdf/index.html
- Buhaug 2010 reply (snippet only): https://pmc.ncbi.nlm.nih.gov/articles/PMC3009780
- CCM follow-ups (snippet only): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9126924/
