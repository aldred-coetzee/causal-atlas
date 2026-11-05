# Modelling in other fields worth repurposing

Date: 2026-11-05. Bounded reading: 25 distinct sources tried, in 30 fetches counting retries; 3 could not be read at all. Time and token costs are my estimates, scaled from one forecaster fit taking 7 to 9 seconds (`results/1b-known-answer.md`).

## For the owner

1. No field has a proven way to find unknown combinations on data like ours. Each has one useful piece, tested on data unlike ours.
2. The strongest lesson is a warning: earthquake and stock-market researchers both found gains that disappeared on later data.
3. Try first: finance's check for "best of many tries", about 9 machine hours. Nothing we discover can be trusted without it.
4. Then two finders: one from biology names combinations, and one from genetics adds up many weak signals.
5. Least sure: with only 48 held-out months, even a real pattern may not show, so a "nothing found" will be weak evidence.

## Shortlist, ranked

Run 1 to 3. Adopt the scoring from 4. Hold 5.

| # | Approach (field) | Answers | Code, licence | Machine, tokens | Drop it if |
|---|---|---|---|---|---|
| 1 | Reality Check (finance) | Is the best of many tries luck? | `arch`, NCSA-style, permissive [S1, S2] | 9 h, 50k | 3+ of 10 null seeds claim a find, or under 5 of 10 planted found |
| 2 | Iterative random forests (biology) | Which combination? | R GPL-3, off CRAN; dated Python port [S5–S7]. Write our own | Unmeasured, 80k | True pair ranks first in under 5 of 10, or a null pair scores over 0.5 in 2+ of 10 |
| 3 | Collective score (genetics) | Do many weak inputs add up? | None needed | 2 h, 60k | Gain under 0.02 in most seeds where 0.05 is possible, or a null gains over 0.005 in 2+ of 10 |
| 4 | Forward scoring (seismology) | Does a gain last? | pyCSEP, BSD-3 [S13b]. Copy the definitions only | 1 h, 25k | The score still shows gain after the link is switched off |
| 5 | Treed lag mixtures (environmental health) | Which inputs, over which lag windows? | R `dlmtree`, licence unconfirmed [S15] | Unknown, 50k | No window recovered, or more than a night on 500 cells |

**1. Reality Check.** *Problem:* thousands of trading rules tried on one record. *Model:* a bootstrap that judges the best rule against everything tried. *Shown:* nearly 8,000 rules on 100 years of daily Dow data beat the benchmark in 1897–1986 even after correction. In the next ten years, the chance that the best rule had no edge was nearly 12% [S3]. That is one dense, continuous series, from the method's own author; I opened no independent repeat. Finance still disputes the scale: one paper asks for a t-ratio above 3.0 [S4a], another says most factors replicate across 93 countries [S4b]. *Carries over:* it takes one loss per month per candidate, so our grid collapses to months. *Limits:* it says whether something won, not why; it cannot catch an effect that later dies; 48 months is short. *First test:* hide planted ratio 4 (17 of 20 detectable, per 1b) among 100 decoy inputs; run all three nulls with the same decoys; 10 seeds each.

**2. Iterative random forests.** *Problem:* which regulators act jointly. *Model:* reweight a forest towards useful inputs, then keep the rule combinations that recur across bootstraps. *Shown:* 7,809 fly sequences (about 10% positive), 23,823 human exons with 270 features, and planted Boolean rules up to order 8 at up to 5,000 rows and 2,500 features [S8]. Rows were treated as independent; there is no dependence handling and no null simulation. The 0.5 stability cut-off is informal, with no p-values. A separate group reports better networks than GENIE3 on DREAM benchmarks, but on its own variant, and I read the abstract only [S9]. *Carries over:* the search, and about 15,000 non-zero training rows (my arithmetic), though these cluster in few cells. *Limits:* the paper reports weaker results with many competing features and with inputs correlated at 0.75, and our lags are correlated. Bootstrapping by block of place and year would be our own unproven change. Our forecaster has not yet been scored on a combination in the refit [refit-marks]. *First test:* `planted_combo_8` (drought and ONI, neither working alone) plus 50 decoys; nulls `combo_null` and `shared_null`.

**3. Collective score.** *Problem:* traits driven by thousands of tiny effects. *Model:* rank variants in one sample, sum them into one score, test it in another. *Shown:* 3,322 cases and 3,587 controls; thousands of small-effect variants, carrying over to bipolar disorder but not to several non-psychiatric diseases [S10]. Across 245 traits, accuracy shows "systematic and dramatic" loss outside the training group [S11]. In macro, micro and finance data the evidence does not settle on a few predictors [S12]; I did not read a forecast gain there. These are independent people, not linked cells. *Carries over:* the recipe, applied to place data only, and closest to his "something collectively". Screening inputs against the baseline's errors is our design. *Limits:* it is additive, so it shows that the group helps, not how inputs combine, and it may not travel between regions or decades. *First test:* a new panel with 40 inputs, each too weak alone, among 200 decoys.

**4. Forward scoring.** The closest data shape I found: rare, clustered events scored as rates on a grid. *Model:* a baseline map multiplied by a three-parameter factor from other maps. *Shown:* 16 hybrids, 40 earthquakes, 2011–2020. None of the models was "significantly more informative than the HKJ benchmark" prospectively, with "temporal instabilities in the fit" given as a reason. The original reader also reported earlier retrospective gains that did not last, few events and inputs losing skill; the spot-check, which read the abstract only, did not confirm those [S13a, S13b]. A shared co-author makes this a self-check, and 40 events is few. *Carries over:* frozen forward tests, gain per event, a negative-binomial count check. *Limits:* it finds nothing itself; pyCSEP assumes independent bins [S14] and is built around earthquake catalogues. *First test:* a planted link that switches off before the held-out block.

**5. Treed lag mixtures.** *Model:* tree pairs over time-resolved exposures, including interactions. *Shown:* five weekly exposures in a Denver birth cohort, authors' own simulations [S15]. No independent repeat opened. *Carries over:* his "over a period of time"; the method only, with no individual data here. *Limits:* five inputs, not hundreds; no scale statement found; adds R and Bayesian sampling. *First test:* `planted_combo_8`, 500 cells.

## Looked at and set aside

- **Retail forecasting (M5):** boosted trees on 42,840 intermittent series [S16, S17]. We already use boosted trees.
- **Knockoffs (genetics):** the time-series version gives only asymptotic control, under conditions, via subsampling [S18, abstract]. I found no version for panels.
- **Exhaustive interaction scans (genetics):** not opened; iRF reports lower cost than incremental searches [S8, SI not read].
- **Gene network inference:** "moderate" accuracy, and no method reached twice random on the hardest synthetic network [S19, search excerpt].
- **Climate precursors (RGCPD):** groups correlated cells, then rests on tigramite, whose grid limits are on file [S20, search excerpt]. The remote-region idea may be worth revisiting. Analogue forecasting: not opened.
- **Dengue early warning:** unchecked figures of 81% of 54 regions alerted with 25% false alarms; the excerpts show covariates in a regression and no combination search [S21, search excerpt, paper not confirmed]. The sprint comparison could not be opened (403).
- **Neuroscience:** not opened; the mathematics of joint signals is his separate reading request.
- **Predictive maintenance:** the popular benchmark is engine-sensor prognostics [S22, search excerpt]. No transfer seen, on that thin reading.

## Not verified

Pages came through a tool that summarises them, except S3 pp. 1647–49, which I read directly, so check any wording before relying on it. Not opened: Hansen's test paper, White's original, McLean and Pontiff, Stock and Watson, DREAM5, Lowe's full text, `dlmtree`'s licence, licence of the Python iRF port. S5–S7: whether either iRF codebase is maintained could not be seen. Using GPL code needs the owner's licence decision (`anything-similar.md`).

## Sources

- S1 https://bashtage.github.io/arch/multiple-comparison/multiple-comparison_examples.html (documentation)
- S2 https://github.com/bashtage/arch (repo page) and https://raw.githubusercontent.com/bashtage/arch/main/LICENSE.md (licence)
- S3 https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf (pp. 1647–49 only)
- S4a https://www.nber.org/papers/w20592 (abstract); S4b https://www.nber.org/papers/w28432 (abstract)
- S5 https://cran.r-project.org/package=iRF (status page); S6 https://github.com/sumbose/iRF (repo page); S7 https://github.com/Yu-Group/iterative-Random-Forest (repo page)
- S8 https://ar5iv.labs.arxiv.org/html/1706.08457 (first 100,000 characters of about 137,000)
- S9 Europe PMC records: `https://www.ebi.ac.uk/europepmc/webservices/rest/search` for the Cliff 2019 and Walker 2022 titles (abstracts)
- S10 same service, DOI 10.1038/nature08185 (abstract; the Nature page redirected to login)
- S11 same service, DOI 10.1016/j.ajhg.2021.11.008 (abstract)
- S12 https://econometricsociety.org/publications/econometrica/2021/09/01/economic-predictions-big-data-illusion-sparsity (abstract, supplement list)
- S13a https://academic.oup.com/gji/article/229/3/1736/6507712 (first 100,000 of about 171,000 characters); S13b https://github.com/SCECcode/pycsep (repo page)
- S14 https://docs.cseptesting.org/concepts/forecasts.html (documentation)
- S15 same Europe PMC service (Mork and Wilson abstract); https://mirror.uned.ac.cr/cran/web/packages/dlmtree/readme/README.html (readme)
- S16 https://econpapers.repec.org/RePEc:eee:intfor:v:38:y:2022:i:4:p:1346-1364 (abstract); S17 https://ar5iv.labs.arxiv.org/html/2103.08250 (second-place method paper)
- S18 https://arxiv.org/abs/2112.09851 (abstract)
- S19 https://www.biorxiv.org/content/10.1101/642926.full.pdf (search excerpt, not opened)
- S20 https://github.com/semvijverberg/RGCPD/commit/0dd397f6101573544f10a55a4205e037e69acdfe (search excerpt, not opened)
- S21 Search listing for Lowe et al., including https://ore.exeter.ac.uk/repository/handle/10871/8302 (excerpts, not opened); which listed page holds the figures is not confirmed
- S22 https://www.phmsociety.org/node/1405 (search excerpt, not opened)
- Could not be read: https://core.ac.uk/download/492594653.pdf and https://www.medrxiv.org/content/10.1101/2025.05.12.25327419.full.pdf (403), https://zendy.io/title/10.1002/sim.5549 (empty page). Retried elsewhere: the PMC copy of S8 (browser check), arXiv PDFs of S8 and S17 (tool returned binary), the Nature page of S10 (login)
- Project files read: `docs/plan-phase-1.md`, `synth/SPEC.md`, `synth/README.md`, `results/1b-known-answer.md`, `results/refit-marks.md` (search hits only)

## Spot-check and origin

Question, in the owner's words: "what modeling has been done in other systems, which we could perhaps repurpose or reuse". Written by a separate session outside this repo; cost outside the Phase 1 cap (decision 0024). Input to the plan revision, not acted on yet.

One helper opened six claims across this page and `maths-for-combinations.md` at source, in 11 fetches. Those for this page:
- S3 Sullivan, Timmermann, White: confirmed from full text (7,846 rules, 1897 to 1986 beat the benchmark after adjustment, "nearly 12 percent" for the following ten years).
- S1/S2 `arch`: SPA/Reality Check, StepM and MCS confirmed from the documentation. Licence: the file names no licence; its wording ("Developed by", "deal with the Software") is University of Illinois/NCSA style, permissive but not MIT. Corrected above from "MIT-like".
- S13a Bayona et al. 2022: abstract only. "None beat the baseline" was stronger than its wording and is corrected above. "Few events", "inputs losing skill" and the earlier retrospective gains are unconfirmed, not contradicted, since the original reader read more of the text.

Two cautions added when this was committed, not checked at source:
- "Gains that disappeared on later data", under "For the owner", rests for earthquakes on the unconfirmed part of S13a.
- If the "nearly 12%" under Reality Check is the test's p-value, as the method implies, it is the chance of a result this good if no rule had an edge, not the chance that the best rule had none.
