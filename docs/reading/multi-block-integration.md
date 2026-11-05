# Shared and block-specific structure across domains: the method without the biology

Date: 2026-11-05. Numbers in brackets point to the sources at the end. "My reasoning" means no source says it. Thresholds are my proposals, to become editable settings. Reading stopped early at the token limit, so several gaps are marked.

## For the owner

1. The family is real and its core is simple: summarise each domain separately, then measure how far the summaries point the same way. Economists built the same idea for time series.
2. Your note is half right. Code exists, but "mature" is overstated, and random matrix results decide the number of shared dimensions only in part (corrected; see the spot-check).
3. Try first: the plain two-step version (below), judged against a noise line from our own fake worlds, not the published ones.
4. I found no test on data like ours. Every noise rule I read assumes independent noise, and sparse counts are the worst fit.
5. Least sure: whether shared dimensions predict anything out of time. I could open no evidence that they do, so this stays a way to build inputs for today's test.

## The note, claim by claim

- **"Closest analogue": partly.** The algebra fits if months are the samples and each block's features are cells: 430 samples, thousands of features (my reasoning). But AJIVE treats samples as unlinked data objects and never models time, even on mortality by year [1]. Group factor models are closer, because they are built on time-indexed panels [4].
- **"Mature": overstated.** AJIVE picks each block's starting rank from scree plots and judgement, and calls one Wedin case "useless" [1]. DIVAS's authors criticise JIVE and AJIVE on these basics [3]. In one comparison, JIVE's permutation rule found the right rank in only 42–58% of runs in one case, and its BIC rule in 0–14% at n=100, rank 5 [6]. That comparison promotes a rival method.
- **"Working code": yes**, with limits in the table.
- **"Already uses random matrix techniques to decide how many shared dimensions": partly right (corrected from "mostly wrong"; see the spot-check).** AJIVE uses a perturbation bound and random subspaces [1]. DIVAS uses Marchenko-Pastur and Gavish-Donoho only for each block's signal; shared rank comes from angles and a rotational bootstrap [3]. Only BIDIFAC comes close: the bound √m+√n sets a penalty on the stacked matrices, and rank follows from it [2].
- **"No target variable": true of the method, not of us.** See Connection below.

## Candidates, ranked

| # | Method, other names | Shared count decided by | Evidence and shape | Code, licence |
|---|---|---|---|---|
| 1 | Two-step angles: AJIVE [1]; group factor model [4] | Angles against two bounds [1]; test on unit canonical correlations, large T and N [4] | 616 samples by up to 24,174 features; 95 years of mortality rates [1]; 117 monthly sectors plus annual data [4] | mvlearn, MIT [7, 8]. Upkeep not visible |
| 2 | Convex linked factorisation: BIDIFAC [2] | Penalty √m+√n after noise scaling [2] | 100×100 simulations; tumour data 660 vs 86 samples [2] | R, github.com/lockEF/bidifac; licence not opened |
| 3 | Bayesian factors with smooth time: MOFA, MEFISTO | Unchecked: both papers refused | Unchecked; search excerpt only | mofapy2, LGPL-3.0 [9] |

**1. Two-step angles.** *Model:* Xₖ = Jₖ + Iₖ + Eₖ, low-rank joint and individual signal plus noise, with joint scores shared across blocks [1]. The time-series form is y_{j,t} = Λᶜⱼfᶜₜ + Λˢⱼfˢⱼₜ + εⱼₜ for two groups [4]. *Estimated:* principal components per block, then canonical correlations; those equal to 1 mark common factors [4]. Canonical correlations between orthonormal components are cosines of AJIVE's angles, so this is one calculation under two names (my reasoning). Pooling all blocks into one PCA is inconsistent, and common factors may not even lead the pooled data [4, footnote 3].
- *Assumptions:* AJIVE: isotropic noise, smaller than the weakest signal [1]. Group factors: approximate factor models, per-block factor count treated as known first [4]; I read pp. 1–8, not the dependence conditions or Monte Carlo.
- *Limits:* the random-subspace bound ignores smoothness, so autocorrelated blocks should look shared too often (my reasoning, untested). The Wedin bound was 100% conservative on a 10,000×100 block [1], so size imbalance costs power. Over-specified ranks can create false joint components [1]. It finds linear co-movement, not "this and that" combinations (my reasoning).
- *Cost:* 298 s for two steps at 616 samples and four blocks [1], machine unstated. One dense 430×10,000 block is 34 MB (my arithmetic). Nulls are the bill; not benchmarked.
- *First test:* below.

**2. BIDIFAC.** *Model:* Xᵢⱼ = global + row-shared + column-shared + individual + noise, each penalised by nuclear norm; the objective is convex [2]. *Assumes:* unit-variance Gaussian noise, independent within and across matrices [2]. *Limits:* authors say discrete data fit poorly, outliers hurt, and identifiability needs study [2]. It over-penalises at high signal [2]. Its one result worth having is that the bound follows matrix size, which addresses unequal blocks (my reading). *First test:* same worlds, conflict block first through count scaling. **Drop if** it fails any of the limits in the first test below, or if over 10% of nothing-shared worlds report a shared dimension at its published penalty, since replacing that penalty removes its one advantage.

**3. MEFISTO.** Factor analysis with Gaussian-process priors on factors, aimed at samples that are not independent (search excerpt only; paper refused). It is the only family member I saw that models time directly. Count likelihood and rank rule are unchecked, as is cost at thousands of features. **Do not build** until someone reads it. *First test if read:* same worlds. **Drop if** a night's run on 500 cells does not finish.

## What breaks the noise rule

- **Time and space:** no opened source tests any of these methods on dependent units. BIDIFAC and DIVAS assume independent noise [2, 3]. Factorless nonstationary data can show a few components taking nearly all variance, with scree plots and criteria agreeing (Onatski-Wang, search excerpt, not opened); they advise comparing levels with differences. Seasons and trends shared by every domain will look like the top shared dimension unless removed first (my reasoning).
- **Sparse counts:** biwhitening rescales a Poisson matrix so noise follows Marchenko-Pastur [5]. Entries must be independent, with theory needing means that grow; zeros are supported by simulation only [5]. At low rates "the signal eigenvalues are not large enough to be detected" and rank stays at 1 [5]. Our cell counts are low and clustered, so expect a miss at cell level (my reasoning). Regions may help; untested.
- **Block sizes:** see rank 1 limits.

## Independent comparisons and shape

Cantini et al. benchmarked nine methods including JIVE, MOFA and RGCCA [10]. The paper was refused; a search excerpt says intNMF led on clustering. The truth there appears to be sample clusters, not shared rank, which is a different question (my reading of the excerpt, unchecked). I found no independent test of shared-rank selection. On our shape (linked units, about 430 months, thousands of places, sparse counts): nothing found.

## Connection to the forecast test

Fit blocks on training months only, freeze loadings, project later months, and add scores to the forecaster. Today's comparison and the search-wide gate then judge them. Fitting on the whole record leaks the future (my reasoning). Shared does not mean useful: conflict history already in the baseline may be what is shared, so score only what the non-conflict blocks supply (my reasoning).

**Evidence of out-of-time gain: none opened.** Excerpts only: Moench, Ng and Potter find block-level movement often matters more, and that PCA treats it as common; Koop and Korobilis warn that all-block models over-parameterise [11]. Stock and Watson not opened.

## First test on fake worlds

Three blocks, cell level, 430 months, seasonal, conflict as clustered counts.
- **Planted:** one hidden persistent driver moves 10% of weather cells and prices, and conflict rates three months later; a second driver moves weather only.
- **Nothing shared:** each block has its own driver, same seasons, bursts and margins. Also pair blocks by shuffled years on real inputs.
- **Noise line:** the shared count across 100 nothing-shared worlds, reported beside the published bounds.

**Drop if** any of these holds:
- over 10% of nothing-shared worlds report a shared dimension against our line;
- the planted driver is missed in over 3 of 10 seeds;
- the weather-only driver is called shared in over 10% of runs;
- frozen scores add no forecast gain in the planted world.

Also report how often published bounds raise false alarms, as the check on your note.

## Looked at and set aside

- **DIVAS:** finds partly shared structure, which suits many domains, and bounds beat true angles in its simulation [3]. MATLAB, licence not seen, heavier than AJIVE. Revisit if rank 1 survives.
- **JIVE:** no inferential basis for the split, per DIVAS's authors [3]; AJIVE reports 121 s against 10.8 s [1].
- **Hallin-Liška block dynamic factors, COBE, SLIDE, multi-set CCA, tensor forms:** not opened, no claim.
- **Lagged cross-correlation:** already on file in `further-maths.md`; it is the targeted two-block cousin.

## Sources

Read through a summarising fetch tool, so check wording, except [4] and [11b], read directly.

1. AJIVE, Feng et al., first 100,000 of 135,733 characters: https://ar5iv.labs.arxiv.org/html/1704.02060
2. BIDIFAC, Park and Lock, first 100,000 of 106,562: https://ar5iv.labs.arxiv.org/html/1906.03722
3. DIVAS, Prothero et al., first 100,000 of 174,409; case studies unread: https://arxiv.org/html/2212.00703v2
4. Andreou, Gagliardini, Ghysels, Rubin 2019, pp. 1–8 only: https://people.lu.usi.ch/gagliarp/AGGR_2019.pdf
5. Landa, Zhang, Kluger, first 100,000 of 180,299; sparsity-filter appendix unread: https://ar5iv.labs.arxiv.org/html/2103.13840
6. Joint LCA, Xiao and Xiao (fetch shows names only; independence from JIVE's authors unknown), simulation results: https://ar5iv.labs.arxiv.org/html/2406.11761
7. mvlearn documentation: https://mvlearn.github.io/references/decomposition.html
8. mvlearn repo: https://github.com/mvlearn/mvlearn
9. mofapy2 repo: https://github.com/bioFAM/mofapy2
10. momix benchmark repo (GPL-3.0, no results stated): https://github.com/ComputationalSystemsBiology/momix-notebook
11. Search excerpts: https://econpapers.repec.org/RePEc:fip:fednsr:412 and https://nep.repec.org/nep-for/2009-10-10. 11b: title page only: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr412.html

**Not opened:** Cantini 2021 (https://pmc.ncbi.nlm.nih.gov/articles/PMC7785750 browser check; Nature login; bioRxiv 429). MEFISTO (https://pmc.ncbi.nlm.nih.gov/articles/PMC8828471/ browser check). Onatski-Wang (https://econometricsociety.org/publications/econometrica/2021/03/01/spurious-factor-analysis, search excerpt). Stock and Watson 2002.

**Count:** 15 sources tried, 11 returned usable pages.

## Spot-check and origin

Question: methods that split structure shared across domain blocks from structure in one block, with the biology removed; the owner said yes, in his words "Yes on multi-omics" (decision 0026). Written by a separate session outside this repo, 131k fresh, outside the Phase 1 cap. "Your note" above means a private note of the owner's, which is not in this repo; it is quoted only where it is about the mathematics. Input to the plan revision: under decision 0026 this method's output is a lead until it beats the baseline out of time.

One helper opened eight claims on sources 1, 3 and 2: seven supported, one not as worded.
- **Not as worded:** "random matrix results mostly do not decide the number of shared dimensions" was too strong, and is corrected above. In DIVAS the Marchenko-Pastur noise estimate feeds the rotational bootstrap that sets the angle bounds for the shared search, so random matrix theory enters that decision indirectly there, and directly in BIDIFAC's penalty. The DIVAS sentence in "The note, claim by claim" is the original reader's and should be read with this.
- **Supported, but on a summary:** AJIVE's Wedin bound being "too conservative to be useful", DIVAS's rotational bootstrap and BIDIFAC's stated limitations rest on the fetch tool's summary of the later part of each page, not verbatim text.

Everything else on this page rests on its original reader alone.
