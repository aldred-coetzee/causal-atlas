# Further fields in mathematics: what can we test?

Date: 2026-11-05. Numbers in brackets point to the sources at the end. "My reasoning" means no source says it. All costs and drop thresholds are my proposals, not benchmarks; thresholds should become editable settings.

## For the owner

1. Three of your seven fields give us a procedure to test now. None has been shown on data like ours.
2. Try first: random matrix theory's test of whether many inputs together move many outcomes months later. Its textbook noise line assumes things our data breaks, so we replace it with a noise line built from our own fake worlds.
3. Then transfer entropy, which is largely today's comparison in other units, and then persistent homology, which is the least proven.
4. Sheaves, categories and information geometry are worth your reading but add no useful test yet. Dynamical systems theory does not fit cell counts this sparse.
5. Least sure: whether the first test still finds anything once cells are averaged into regions, which it requires. I could not open Carlsson's paper.

## The three groups

- **Try on fake worlds now, ranked:** (1) random matrix theory, (2) transfer entropy, (3) persistent homology.
- **Study as a way of thinking, no useful test yet:** information geometry, applied sheaf theory, category theory.
- **Does not fit this data:** dynamical systems theory, as a method on cells.

Anything the first group finds must still pass the search-wide gate in `maths-for-combinations.md`.

| Field | Procedure or language? | Telling real from noise, and what that assumes | Shown on data like ours | Open code |
|---|---|---|---|---|
| Random matrix | Procedure | Theoretical edge: no link, large N, M, T; formal test for Gaussian data only [6] | Nothing. Nearest: 76 inputs, 34 outcomes, 265 months, dense, authors only [6] | Plain SVD; no package needed (my reasoning) |
| Transfer entropy | Procedure | Permutation, or chi-squared in large samples [8, 9]; shuffling ignores clustering (my reasoning) | Nearest: Nigeria, 37 units, binary, about 160 windows (my estimate), unvalidated [9] | JIDT, IDTxl: GPL-3 [10, 11] |
| Persistent homology | Procedure | Confidence sets assume independent draws [12]; "universal" null is a conjecture [13] | Nothing found. Nearest: California voting map, descriptive [14] | GUDHI: MIT, some parts effectively GPL [15] |
| Information geometry | Language, one procedure | Chi-squared at large N [16] | Nothing found | None opened |
| Sheaf theory | Procedure, given maps you supply | None given [17] | Nothing. 612 mostly simulated flight observations [17] | pysheaf: Apache-2.0 [18] |
| Category theory | Language | None | Nothing found | Not applicable |
| Dynamical systems | Language; methods need a trajectory | Surrogates; see the CCM page | No study found | Not opened |

## 1. Random matrix theory

**Your note:** right about dimension, overstated for us. Temporal correlation alone stretches the noise distribution into a longer tail [7, abstract], and heavy tails give "anomalously large eigenvalues with no information content" [19]. Our series have both.

**Procedure:** standardise and decorrelate inputs and outcomes, cross-correlate them at a lag, and compare the top singular values with noise [6]. Each singular value marks a mix of inputs tracking a mix of outcomes.

**What it adds:** one quick test of a collective link across many inputs and many outcomes, and a count of how many separate links exist. The short list's collective score and top-down testing work through a fitted forecaster, without that count (my reading).

**Shown:** using all variables, the lagged spectrum was "indistinguishable from pure noise". After dropping redundant factors, the top value was 0.81 against an edge of 0.642 [6]. I reproduced that edge from their formula. The result turned on a cleaning choice, which must be charged as a try (my reasoning). The authors call their comparison "eyeballing" and expect fat tails to blur the edge [6]. I found no independent repeat.

**Limits:** linear only, so it misses an either-both pair (my reasoning). The edge reaches 1, meaning no test, once inputs plus outcomes reach the number of months (my arithmetic), so thousands of cells must become regions. It says something exists, not what. Cost: minutes for 1,000 nulls.

**First test:** a hidden series moves 20 of 200 regional inputs, and three months later moves conflict in 10 of 40 regions, each link too weak alone. Nothing-planted world: same series, with input years paired to other outcome years. **Drop if** over 10% of 100 null worlds pass at nominal 5%, or the plant is found in under 7 of 10 seeds. Report the textbook edge's false alarms too, as the check on your note.

## 2. Transfer entropy

**Your note:** "without linearity" holds. "Without stationarity" does not: Schreiber's setup is "a stationary Markov process" [1]. The ensemble fix assumes "independent repetitions" [5], which neighbouring cells are not (my reasoning). "Directed information flow" is disputed: James and colleagues accept it as reduced uncertainty and call the flow reading incorrect [3]. For Gaussian data it equals Granger causality [4].

**What it adds:** little. For many predictive models, the log-likelihood ratio estimates transfer entropy [8, abstract], so a log-loss comparison of our forecaster is close to one (my reading). Its value is a cross-check that needs no fitted forecaster.

**Shown:** nearest shape is ACLED Nigeria, with no validation or false-positive rates, and there the corrected measure gave the densest graph of the three built [9]. No independent repeat found. The corrected measure's null is uniform and uncorrelated, unlike ours [9].

**Limits:** pairwise it reads 0 bits for two inputs that jointly determine an outcome [3], which is exactly your combination case. Bias scales as C^(k+l+1)/N [9]: about 0.02 in one binary cell over 430 months, against roughly 0.06 nats of total uncertainty at 1% event months (my arithmetic). So cells must be pooled. Cost: hours with nulls, 4 million rows by 600 lagged inputs.

**First test:** pooled and discretised, conditional on own past and neighbours. Plant one lag-3 input tripling risk in 5% of cells, plus an either-both pair. Nothing-planted world: same inputs, years re-paired. **Drop if** over 10% of null worlds pass, or the single link fails to outrank 100 decoys in 7 of 10 seeds, or it finds nothing the forecaster's log-loss missed.

## 3. Persistent homology

**Your note:** overstated. Feng and Porter call building the topological object "a crucial step", and their constructions see features distance-based ones miss. They also call "persistent means signal" conventional wisdom, and note short-lived features can carry signal [14]. So there is a modelling choice, and persistence is not proof. "Surfaces correlations linear methods miss": nothing I opened shows it; Carlsson not opened (403).

**What it adds:** map shape, such as rings around a core or how hot spots join as the threshold falls. No short-list method looks at that (my reasoning).

**Limits:** Fasy's sets assume independent draws [12]. Bobrowski and Skraba's null fails on perturbed lattices [13], and a grid resembles one (my reasoning), so we need our own null. Mostly zero maps tie heavily (my reasoning). Cost not benchmarked.

**First test:** plant conflict forming an expanding ring around a drought core. Nothing-planted world: same monthly counts and cluster sizes, rearranged. **Drop if** shape features add no skill beyond counts of active cells and neighbour averages, or over 10% of null worlds pass.

## Study: no useful test yet

- **Information geometry.** Your description is accurate. One real procedure separates a pure interaction from each input's own rate, with a chi-squared test at large N, shown on simulated data for two and three neurons, with experimental results cited but not shown in the pages read [16]. Terms grow as 2ⁿ−1 [16]. It teaches what "a combination" means. Its test would duplicate the either-both world already planned for pattern search. The survey I opened names no time-series use in the part read [20].
- **Sheaf theory.** Your note says local data asks what global structure it is compatible with. Only after the modeller fixes how the domains relate [17], which is the reverse of structure-first. No statistical test [17]. Possible test, for data checking only: plant a regional disagreement between two resolutions, against a matching world where they agree. **Drop if** it does no better than comparing totals.
- **Category theory.** A language. The book's abstract names no data analysis [21, abstract only]. Your "functorial claim" has a plain test without it: fit in one region, score in another. That finds nothing new, and the categorical wording adds no check.

## Does not fit

**Dynamical systems theory.** It is a fine language for regimes. Its methods need a trajectory, and a cell with five events in 430 months has none (my reasoning). Schreiber's demonstrations used 10⁴ to 10⁵ iterates [1]. The CCM and early-warning results are on file and not repeated. I opened no source on attractor or bifurcation recovery from sparse counts, so this rests on those pages and my reasoning. Cheap check: thin a low-noise coupled map to our event rate, against a shuffled copy as the nothing-planted world. **Close it if** forecast skill from embedding no longer beats the shuffled copy, as I expect.

## Looked at and set aside

- **Event coincidence analysis:** made for sparse event pairs, but multivariate is future work and seasons create false links [22]. pyunicorn (BSD-3) shuffles events, which destroys clustering [23]. Schleussner's climate-conflict use: refused, no claim.
- **Unchecked, no claim:** Marchenko-Pastur, Bouchaud and Potters' book, SINDy, Mapper, Turkeš on persistent homology (search snippet only).

## Sources

Pages were read through a summarising fetch tool, so check wording before relying on it, except 14 and 16, whose pages I read directly.

1. Schreiber 2000, full text: https://ar5iv.labs.arxiv.org/html/nlin/0001042
2. Wrong arXiv ID (unrelated paper), no claim: https://arxiv.org/abs/1112.1041
3. James, Barnett, Crutchfield, full text: https://ar5iv.labs.arxiv.org/html/1512.06479
4. Barnett, Barrett, Seth, abstract: https://arxiv.org/abs/0910.4514
5. Gomez-Herrero et al., abstract: https://arxiv.org/abs/1008.0539
6. Bouchaud, Laloux, Miceli, Potters, full text: https://ar5iv.labs.arxiv.org/html/physics/0512090
7. Hisakado, Kaneko, abstract: https://arxiv.org/abs/2305.12632
8. Barnett, Bossomaier, abstract; conditions not read: https://arxiv.org/abs/1205.6339
9. Kirkley v1, with supplement: https://arxiv.org/html/2506.16215v1
10. JIDT repo: https://github.com/jlizier/jidt
11. IDTxl repo: https://github.com/pwollstadt/IDTxl
12. Fasy et al., first 100,000 of 128,000 characters: https://ar5iv.labs.arxiv.org/html/1303.7117
13. Bobrowski, Skraba, full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC10382541/
14. Feng, Porter, pp. 1–2 only: https://arxiv.org/pdf/1902.05911
15. GUDHI licensing page; cubical module's licence not stated there: https://gudhi.inria.fr/licensing/
16. Nakahara, Amari 2001, pp. 1–4: https://papers.neurips.cc/paper_files/paper/2001/file/ea5a486c712a91e48443cd802642223d-Paper.pdf
17. Robinson, first 100,000 of 128,000 characters: https://ar5iv.labs.arxiv.org/html/1603.01446
18. pysheaf repo: https://github.com/kb1dds/pysheaf
19. Biroli, Bouchaud, Potters, full text: https://ar5iv.labs.arxiv.org/html/cond-mat/0609070
20. Nielsen, first 100,000 of 157,000 characters: https://ar5iv.labs.arxiv.org/html/1808.08271
21. Fong, Spivak, abstract only: https://arxiv.org/abs/1803.05316
22. Donges et al., full text: https://ar5iv.labs.arxiv.org/html/1508.03534
23. pyunicorn source: https://pyunicorn.readthedocs.io/en/latest/_modules/pyunicorn/eventseries/event_series.html

**Not opened:** Carlsson 2009, 403: https://www.ams.org/journals/bull/2009-46-02/S0273-0979-09-01249-X/S0273-0979-09-01249-X.pdf. Schleussner et al. 2016, browser check: https://pmc.ncbi.nlm.nih.gov/articles/PMC4995947

**Count:** 25 sources tried, 23 returned the page and 2 refused. Of the 23, source 2 was irrelevant.

## Spot-check and origin

Question, in the owner's words: "Think we need to look at further fields in mathematics", naming topological data analysis, applied sheaf theory, category theory, transfer entropy, dynamical systems, random matrix theory and information geometry. Written by a separate session outside this repo; cost outside the Phase 1 cap (decision 0025). "Your note" above means a private note of the owner's, which is not in this repo; only its claims about the mathematics are quoted. Input to the plan revision: nothing here runs before the revision and the owner's yes.

One helper opened eleven claims on four pages at source (sources 6, 3, 1 and 10), all supported. Two nuances:
- Source 6: "indistinguishable from pure noise" is for the one-month lagged case with all variables. The simultaneous case showed one value, 0.87 against 0.806.
- Source 1: Schreiber's abstract says "minimal assumptions about the dynamics", while the definition is for a process "approximated by a stationary Markov process of order k".

Everything else on this page rests on its original reader alone.
