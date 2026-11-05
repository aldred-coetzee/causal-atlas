# 1b: known-answer test

**Rule, committed before any number, from `docs/plan-phase-1.md` as amended by decision 0013.**

**Question.** Can the 1d machinery find a planted link, and stay quiet where there is none?

**Shape.** The real outcome panel is built from UCDP GED 26.1, `where_prec` 1 to 3, by month of
`date_start`, on 10,228 cells over the 399 target months and the 36 months of warm-up before them.
These statistics come from training months (1992-01 to 2017-03) only: size, share of zeros, lag-1
and lag-12 autocorrelation, seasonal amplitude, spatial clustering, share of events in the top 1%
of cell-months, regional episode length. No validation or held-out month is used.

**Generator.** In `synth/`, imports nothing from `src/` (a test enforces this), committed before any
detector code. Written by one Sonnet subagent, about 100k fresh tokens, from a written spec holding
the shape statistics and the panel list, forbidden from opening the plan or `src/`. The mechanism is
a self-exciting negative binomial count process over a latent spatial rate, with threshold input
effects over distributed lags the author chooses, in only some cells.

**Panels,** with synthetic inputs shaped like the real ones, with multi-year persistence:
planted at rate ratios per standard deviation of input of 1.05, 1.15 and 1.40; a pure null with large
multi-year regional episodes unrelated to the inputs; and a shared-driver null, as the pure null plus
a seasonal driver and slow regional trend shared by input and outcome, with no link.

**Detector.** Exactly 1d's: baseline B and M1 as the plan defines them, with the same split, metric,
interval and verdict. M1's settings are frozen at B's during shuffles. The verdict for a replicate
needs all three: (1) skill at least 0.02 and the lower end of its 95% block-bootstrap interval above 0;
(2) under circular shift, skill above all 32 shifts; under year permutation, above all but at most 0
of 19 draws, which tests criterion 2 only coarsely, at 1 in 20; (3) the median shuffled skill under
0.01 in size. Bootstrap draws: 10,000.

Deviations already named: the 19 draws above; the sub-panel below; and the tuning grid, fixed at B's
default settings for the synthetic runs if runtime requires it, which would then be stated here.

**Replicates.** 20 per panel, each through the full pipeline with both schemes, with the oracle's
skill (the generator's own true rate) reported. One replicate per panel runs at full size, the other
19 on a contiguous sub-panel of 2,000 cells. Disclosed departure from the brief's "same size".

**Pass, or stop, for each scheme.** Detection at least 80% at ratio 1.40 (16 of 20). False positives
at most 1 of 20 on each null, with the exact binomial upper bound printed beside the count. Criterion
1's false-positive rate is reported alone, as the check on the interval. The 1.15 result is reported
and shows what 2% means. If both schemes qualify, the circular shift is used for 1d; if one, that one;
if neither, 1b fails.

**Runtime.** Ceiling 24 hours in total, `nice -n 19`, at most 6 threads. One fit of each size is
timed first; if the projection exceeds the ceiling, this stops and reports at a gate rather than
cutting replicates unasked.

**Scope.** No real input is joined to any real outcome in this step. PCMCI and CCM do not run.

## Shape statistics

Not yet computed.

## Result

Not yet computed.
