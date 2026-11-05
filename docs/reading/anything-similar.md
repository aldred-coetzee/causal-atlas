# Is anything similar already out there? (bounded reading check)

Date: 2026-11-05. Budget used: 8 searches, 12 pages opened.

Question (owner's words): "let's also check if there is anything kind of similar out there already, which looks at a wide range of data sets and then has a look at how those different systems might potentially interact to cause, to have an influence on each other."

Precisely: does a system put many unrelated domains on one grid of place and time and search for unhypothesised lagged combinations that predict an outcome?

Method note: pages were read through a fetch tool that returns a summary of the page, so short phrases below came through it. Those the verdict rests on were checked against the raw text; see the spot-check below.

## Answer

Not found in this bounded search, as a single system. The pieces exist separately: gridded multi-variable datasets (AfroGrid), operational conflict forecasting on the same grid we intend (VIEWS), and lagged causal-discovery software (tigramite/PCMCI). I found nothing that joins them as "many unrelated domains, screened for unhypothesised lagged combinations, scored out of sample". This does not prove nothing exists; I looked at 8 searches. Reading for the owner: borrow the data and grid conventions (AfroGrid, PRIO-GRID, VIEWS benchmarks) and the software (tigramite); build the cross-domain search; joining VIEWS is possible as a benchmark, not as a team (not checked).

## Closest systems

| System | Domains | Grid, step | Search or named variables | Reported finding | Could not do | Open? |
|---|---|---|---|---|---|---|
| VIEWS / 2023-24 prediction challenge (opened: arXiv 2407.11045; prio.org/projects/2002) | Shared data "about 100 features" at country-month and grid-month; one model uses "15 topics" from news. Themes not fully listed (not stated) | PRIO-GRID cell, month; Africa and Middle East at grid level | Fixed feature sets and submitted models; no discovery search stated | Test windows 2018-2023 and a true-future year; the paper says a separate article will give model performance, so no model scores seen | Page does not say what features add beyond conflict history | Evaluation code on GitHub (opened); data "can be found at" the challenge site; data and model licence not stated |
| AfroGrid (opened: PMC8964753) | 74 conflict indicators plus 10 environment, development, population indicators | 0.5 degree, 10,674 African cells; mostly monthly, night light and population annual extrapolated; 1989-2020, most variables 2000-2020 | A dataset; demonstration regressions only, "not presented as clear conclusions about any specific relationships" | None claimed | No lagged search, no prediction; no prices, crime, health | Data and R scripts on Harvard Dataverse; article CC BY 4.0, dataset licence not stated |
| EMBERS, IARPA OSI performer (opened: arXiv 1604.00033 via ar5iv) | News, blogs, tweets, machine-coded events, currency rates, food prices (abstract) | City-level, daily | "several different models" fused; the paper describes no automated search over combinations (my reading, not its words) | Scored by MITRE against a gold standard; actual versus IARPA targets reported (e.g. month 36 recall 0.79, precision 0.87); the paper says forecasts are "communicated in real-time before the event to MITRE/IARPA and scored independently of the authors", so this is a true forward test | Civil unrest in Latin America only; its section on uncertainties treats spontaneous protests as a limit (gist, not quoted) | Code and data release not stated |
| Tigramite / PCMCI (opened: GitHub; arXiv 1702.07007 abstract) | Any time series; not a data system | Not applicable | Searches lagged causal links among many variables | Validated on one climate teleconnection (tropical Pacific to extra-tropical temperature) and "large-scale synthetic datasets"; no out-of-sample prediction claimed | Variable count not stated in the abstract | GPL v3 (opened) |
| FEWS NET (opened: fews.net/about/projections) | Food security; rainfall, prices and others used by analysts | "Areas of concern", no grid named; 8-month outlook refreshed every 4 months | Analyst-built "if-then" scenarios, not a statistical search | No out-of-sample score seen | Not a data-mining system | Data Explorer exists; terms not stated |

## Closest in spirit, and how it differs

EMBERS is the closest in ambition: many unlike data streams (including food prices and currency rates) feeding one forecast, scored against an external record. It differs in four ways: city and day not cell and month, several built models rather than a search, one event class in one region, and no combination search. The delta-MAPS method (snippet only) screens lagged cross-correlations between regions of a single climate field with multiple-testing correction; it is a method on one domain, not a cross-domain system.

## What could be reused

- AfroGrid data and R scripts: Harvard Dataverse, doi 10.7910/DVN/LDI5TK (opened). Dataset licence not stated at source; check before relying on it.
- VIEWS evaluation code: github.com/prio-data/prediction_competition_2023 (opened, licence not seen). Useful as a benchmark for our "baseline first" rule.
- tigramite: GPL v3. Our repo is MIT; using it as a dependency needs a licence check by the owner (not resolved here).
- Snippet only: PRIO-GRID codebook at grid.prio.org; CEDAR, M-CaStLe and TraCE-ST preprints for screening on gridded data, not opened.

## Not verified, not checked

- Snippet only, not opened: the full Sandia/OSTI report (a binary file the tool could not read). Its abstract was opened and quoted in `lagged-methods.md`. A 2022 Lisbon thesis on Sahel random-forest conflict prediction using 10-fold cross-validation (random folds, so not a time-forward test). The SeasFire Earth data cube. A 2025 hydrometeorology comparison. Teleconnection patents. A food-price machine-learning study on 105 variables.
- Not looked at: Google Data Commons, ACLED CAST, Earth System Data Lab internals, GDELT-based work, crime or pollen or house-price systems, commercial products, any 2026 work after the search snippets.
- VIEWS model scores and licence terms: not found. EMBERS full ablation table: only the tool's summary seen.
- I did not test whether any system searches unhypothesised combinations internally; the sources opened did not say.

## Spot-check by the session that commissioned this

Raw text of the VIEWS, EMBERS and AfroGrid papers. Held: VIEWS grid coverage, "about 100 features", "15 topics", the separate article on performance; AfroGrid's 10,674 cells, 74 conflict indicators, Dataverse DOI, the article's CC BY 4.0; EMBERS's city and day, Latin America, month 36 recall 0.79 and precision 0.87. Four corrections: "in-sample or not is not stated" was wrong, since EMBERS scored live forecasts, and that makes it stronger; "five" models does not appear in its text; one AfroGrid phrase was the tool's wording; and the Sandia note contradicted `lagged-methods.md`. Not re-checked: AfroGrid's 10 other indicators and its dates, tigramite, PCMCI, FEWS NET, and everything marked snippet only. Using tigramite would also reopen the owner's PCMCI deferral.

## Sources

- https://arxiv.org/html/2407.11045v1 (VIEWS challenge)
- https://www.prio.org/projects/2002 (VIEWS challenge page)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8964753/ (AfroGrid)
- https://arxiv.org/abs/1604.00033 and https://ar5iv.labs.arxiv.org/html/1604.00033 (EMBERS at four years)
- https://arxiv.org/abs/1702.07007 (PCMCI)
- https://github.com/jakobrunge/tigramite (tigramite)
- https://fews.net/about/projections (FEWS NET)
- Snippet only: https://arxiv.org/pdf/1602.07249 (delta-MAPS); https://www.osti.gov/servlets/purl/1991387 (Sandia); https://run.unl.pt/handle/10362/134614 (Sahel thesis)
