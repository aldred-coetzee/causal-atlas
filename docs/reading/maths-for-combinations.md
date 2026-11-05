# What mathematics could find combinations that predict together?

Date: 2026-11-05. Numbers in brackets point to the sources at the end. "My reasoning" means no source says it.

## For the owner

1. I found no method proven to find joint predictors, with error control, on data like ours. The evidence comes from genetics, finance and disease surveillance.
2. Try three first: **(A)** a strict gate that charges for every combination tried; **(B)** an exhaustive search for rare "this and not that and this" conditions; **(C)** top-down testing: do all inputs help, then which family, then which member.
3. Why those: A keeps the other two honest. B handles combinations of any size. C is the smallest step from today's method and can catch many weak things together, which B cannot.
4. Set aside for now: reading interactions from forests, knockoffs, synergy measures, tensor factorisation and early-warning signals. Each has a specific problem, listed below.
5. Least sure: whether any of this stays honest on our data. Millions of rows may be worth only a few decades of independent months. Run A first; if it fails, stop.

## Candidates, ranked

| # | Method | What it finds | Best evidence, and on what shape | Repeated independently? |
|---|---|---|---|---|
| 1 (A) | Search-wide gate: Reality Check/SPA logic plus a null made by rerunning the whole search | Whether the best of everything tried beats the baseline | Finance forecasts; heavy-tail failure is simulated [1]. White and Hansen themselves not opened | Not established here |
| 2 (B) | Exhaustive pattern search, stratified: FACS, LAMP, Westfall-Young Light | Yes/no conditions of any size, with family-wise error control | 84–95 plants, about 1,400–2,700 features; 12,773 genes by 397 motifs [2]. Benchmarks up to 515,597 rows [3] | Partly: a different group measured LAMP's error rate [3]. FACS: none found |
| 3 (C) | Hierarchical group testing | Smallest group that helps, with family-wise error control | Linear models, Gaussian errors, simulated and real [4] | Mandozzi and Bühlmann extend Meinshausen [4]. None on counts found |
| 4 | FAST exhaustive pair ranking | Pairs, including uncorrelated ones | Dense regression and classification; synthetic functions [5] | None found in what I read |
| 5 | Multivariate subset scan | Which places and which series are unusually high together | Counts: 97 zip codes, 16 streams, two years of real data with simulated outbreaks [6] | None found |

**1. Search-wide gate.** This test asks whether a benchmark is beaten by any of m competitors, so it prices the search itself [1]. I would resample whole months or years, which keeps the map's spatial pattern intact (my reasoning, untested).
- *Limits:* standard tests assume finite variance. With infinite-variance loss differentials, a nominal 5% Diebold-Mariano test rejected true nulls up to 70% of the time [1]. Subsampling may fix this, but that is one 2026 preprint on finance, and for SPA it only "lays the groundwork" [1]. Conflict bursts could behave this way (my reasoning). No test is free of assumptions: conditional independence tests cannot be both uniformly valid and powerful [7]. Shuffling years also fails if an input trends (my reasoning).
- *Tells us:* something beat the baseline, not why.
- *Cost:* the score table is small; rerunning the search 100+ times is the real bill (my estimate, not benchmarked).
- *First test:* 100 worlds with nothing planted, realistic clustering and heavy bursts, running the full search. **Drop or rebuild if** over 10% report a discovery at a nominal 5%.

**2. Exhaustive pattern search.** Each input becomes yes/no conditions. Pruning uses how often a condition occurs, not how well its members predict alone [2]. So a combination with no useful member stays in the search by construction (my reading; I found no published test of that pure case). FACS conditions on a category, which could be a baseline-risk band, so a hit must add to history. In the gene data, 1,214 unconditioned hits fell to 26 once conditioned; the plant data fell from 100,883 to 433 [2]. LAMP reaching eight motifs comes from a search snippet; its paper was not opened.
- *Limits:* conjunctions of binary features only; the authors call continuous data an open problem [2]. It cannot see 100 weak things. Permutation shuffles labels, and neither paper I read discusses dependent samples [2, 3]. Independent-row p-values could flood on clustered data (my reasoning), so A must confirm every hit. LAMP's real error rate ran from α/2 to α/100, so it wastes power [3].
- *Cost:* unknown at 4 million rows; benchmark first. About 1,200 items (100 series, two sides, six lags) is my estimate.
- *First test:* plant an either-both pattern: A and B together, or neither, raises risk threefold, while A alone and B alone predict nothing. Add a regional episode as a decoy. **Drop if** it misses the pattern at 1,000 affected cell-months, or reports the decoy.

**3. Hierarchical testing.** Test everything together, descending only where a group passes [4]. Each test can be today's comparison of baseline against baseline plus inputs. The tree can come from domain knowledge [4], such as weather, prices, crime. Economic forecasting also hints that many inputs often matter at once [8] (abstract only; dense data).
- *Limits:* the theory needs valid p-values for each group and a linear model; the guarantee is asymptotic [4]. I read pages 1–3 only; Meinshausen 2008 was not opened. If partners sit in different branches, descent may lose them (my reasoning). It may stop at "something in prices".
- *Cost:* up to about 200 refits for 100 series, usually fewer (my estimate).
- *First test:* plant 50 weak inputs together, none detectable alone, then a separate cross-family pair. **Drop if** the root test misses the 50, or the nothing-planted worlds fail A's limit.

**4. FAST pairs.** It scans every pair on residuals after single effects, at O(b²+N) per pair [5]. That avoids relying on greedy splits (my reasoning).
- *Limits:* pairs only; no error control in pages 3–7. With 100 features it needed about 10⁶ samples for average precision above 0.7 [5]. Correlated features produced a false pair [5].
- *Cost:* about 180,000 pairs for 600 lagged inputs; minutes to hours (my estimate).
- *First test:* the same either-both pair, by rank. **Drop if** it ranks below the top 100.

**5. Subset scan.** It fits our counts and space: Poisson, irregular regions, all subsets of streams [6].
- *Limits:* it detects current excess rather than predicting. Naming streams is unreliable: unaffected streams were reported 26–63% of the time in one experiment [6]. Those counts averaged 0.5–44 a day, far denser than ours (my reasoning, not measured).
- *Cost:* the authors claim fast search; not benchmarked here.
- *First test:* plant a three-input excess in one region, leading outcomes by three months. **Drop if** scan hits add nothing to the baseline forecast.

The drop thresholds are my proposals, to be set as editable settings.

## Looked at and set aside

- **Interaction readouts from forests:** pure interactions were mostly not detected better than no interaction, and main effects were read as interactions [9].
- **Iterative random forests:** stability rule, with no formal error rate in the abstract [10]. Full text refused.
- **Knockoffs for interactions:** assumes independent samples and needs a model of the inputs; tested at p=30 [11]. The time-series version is asymptotic, with one inflation study named [12]. No panel use found.
- **Synergy measures (O-information):** a snippet reports independent triplets biased towards synergy when samples are few (paper refused, unchecked).
- **Tensor factorisation:** the sparsity matches ours (0.54% non-zero), but held-out months were interleaved and no significance testing was reported [13]. Maybe later, as a way to compress inputs.
- **Early-warning signals:** variance caught 25% of crashes at 5% false alarms, under a best-case mechanism [14].
- **e-values:** FDR holds under any dependence, but calibrated p-values typically give no more power than BH [15]. Revisit once series arrive over time.
- **FDR across grid cells:** only modestly sensitive to spatial correlation [16], but disputed: results can shift with the chosen domain [17] (preprint under review). A concern for mapping, not selection.
- **ViEWS competition:** abstract only; ensembles beat the average model [18]. Not a discovery method.
- **Not opened, no claim made:** stability selection, RuleFit, partial information decomposition, Chen and Neill on civil unrest.

## Sources

Abstract/page = read through a fetch tool's extract. Pages = read directly.

1. Frederiksen, Matsui, Pedersen 2026 preprint, pp. 1–3: https://arxiv.org/abs/2605.16866
2. Papaxanthos et al. 2016 (FACS), pp. 5–8: https://proceedings.neurips.cc/paper_files/paper/2016/file/0a0a0c8aaa00ade50f74a3f0ca981ed7-Paper.pdf
3. Llinares-López et al. 2015, full-text extract: https://ar5iv.arxiv.org/html/1502.04315
4. Mandozzi and Bühlmann, pp. 1–3: https://arxiv.org/pdf/1312.5556
5. Lou et al. 2013, pp. 3–7: https://microsoft.com/en-us/research/wp-content/uploads/2017/06/kdd13.pdf
6. Neill, McFowland, Zheng 2013, pp. 1–3, 14–17: https://www.cs.nyu.edu/~neill/papers/StatMed2013.pdf
7. Shah and Peters, abstract: https://arxiv.org/abs/1804.07203
8. Giannone, Lenza, Primiceri 2021, abstract: https://econometricsociety.org/publications/econometrica/2021/09/01/economic-predictions-big-data-illusion-sparsity
9. Wright, Ziegler, König 2016, full-text extract (it notes its summaries are not fully consistent): https://pmc.ncbi.nlm.nih.gov/articles/PMC4815164
10. Basu et al., abstract: https://arxiv.org/abs/1706.08457
11. Diamond, full-text extract: https://arxiv.org/html/2408.17016v2
12. Chi et al., abstract: https://arxiv.org/abs/2112.09851
13. Schein et al. 2015, full-text extract: https://ar5iv.labs.arxiv.org/html/1506.03493
14. Boettiger and Hastings 2012, full-text extract: https://ar5iv.labs.arxiv.org/html/1204.6231
15. Wang and Ramdas, extract of first 100,000 characters: https://ar5iv.labs.arxiv.org/html/2009.02824
16. Wilks, conference abstract only; the 2016 article not opened: https://ams.confex.com/ams/96Annual/webprogram/Paper276937.html
17. Schutte et al. 2026, abstract and review page: https://egusphere.copernicus.org/preprints/2026/egusphere-2026-2203/
18. Vesco et al. 2022, abstract: https://www.prio.org/publications/13337

**Not opened:** Terada et al. 2013 (LAMP), refused three ways; Hansen 2005, empty or abstract-less copies; White 2000; Meinshausen 2008; Gehlen et al. 2024, refused twice.

**Count:** 30 fetches. 21 returned a page: the 18 above, one abstract-less Hansen record, and two irrelevant papers from arXiv IDs I guessed wrongly. No claim rests on those three.

## Spot-check and origin

Question, in the owner's words: "ideas on what mathematics we could use to try and find emergent correlations". Written by a separate session outside this repo; cost outside the Phase 1 cap (decision 0024). Input to the plan revision, not acted on yet.

One helper opened six claims across this page and `other-fields.md` at source, in 11 fetches. Those for this page:
- [1] Frederiksen et al. 2026: confirmed from abstract and full text ("may reject a true null as often as 70% of the time"; SPA "lays the groundwork").
- [2] FACS: confirmed, with a precision: 100,883 against 433 is the LY plant dataset only; the avrB dataset is 546 against 43; 84 and 95 are the two datasets' sample counts. Binary features and continuous data as "a key open problem" confirmed.
- [9] Wright, Ziegler, König 2016: **not re-checked**; the checker could not open it (captcha, then 403). Setting aside forest interaction readouts rests on the original reader alone.

Everything else on this page is unchecked beyond its author's reading.
