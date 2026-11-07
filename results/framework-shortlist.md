# Framework Stage 1, third method: shortlist on earlier months, test on later months

Rule first, committed before any number from this code (rule 9). The owner's yes: decision 0038. Code: `src/causal_atlas/bench.py`, `scripts/run_shortlist.py`. Seeds: `results/seed-ledger.md`.

## Seen before this rule, so nothing is blind to it

`results/framework-stage-1.md`, on the same spent seeds and the whole 96 months: uncapped `pooled` has a true input first in 10 of 20 and 0 of 15 nulls, and in the top 5 in 15 of 20 and 2 of 15. With only the true inputs searched it names one first in 12 of 20. This method was chosen knowing that. Those numbers are why step 2 cannot decide anything, and only step 3 can.

## The method

No cap. Months 195 to 290, the same four spans of 24.

1. **Shortlist, months 195 to 242.** The screen's table on all 1,280 columns, for one form. Rank columns by the gate's own scale at the unshifted value. Walk down the ranking and keep the first column of each new input, until 5 inputs are held. Taking inputs and not columns is because columns of one input are close copies, so 5 columns would often be one claim.
2. **Test, months 243 to 290.** The same form's table on those 5 columns only, with the same gap and width, 32 year shifts, and the same stepping gate with K = 5.

A lead is a named column from step 2. The rescaled baseline is the same as Stage 1. Nothing else changes. Forms are `all`, `largest` and `pooled`, one form used in both steps.

Why it may fail: each half has half the months, so the test can hear less than the 12 of 20 above.

## Plug-ins beside it, on every world

- **Floor:** 5 inputs and columns drawn at random (generator seeded by world and form), then the same test. A method must clearly beat it. Random columns can include a true input, so the floor is not zero.
- **Oracle shortlist:** handed the 2 true inputs, keeps each one's best column on the earlier months, then the same test. This is what the split costs when the shortlist is perfect.
- **Truth:** hands back the true input as a lead. The scorer must score it true in every world. A miss means the scorer is broken.
- **Exact column on the later months:** reading C of `results/r2-ceiling.md` on months 243 to 290, no cap. This is the instrument limit for the test half.

## Scoring

As Stage 1: found means the first lead is truly linked; any lead is beside. Also reported: the shortlist held a true input. The scorecard still cannot credit a second true input in one world; that is owed to Stage 2. The toy's global input is reported as how often it was claimed.

## Tests of the test

Noise: the gate on 5 columns of pure noise names a lead at about 1 in 33 (standing unit test). Truth, as above. Baseline: R's total over observed on nulls, as Stage 1, unchanged since it reuses the saved R. Smoke tests use seed 7901 and write to a scratch file.

## Order and marks, fixed now

**Step 1, toy,** seeds as in the ledger. For each form: first lead true in at least 18 of 20, a lead named in at most 2 of 15 nulls. This checks the plumbing and could hardly be missed by working code, so passing it says little. A miss means stop and find out why.

**Step 2, development on spent seeds** (3001 to 3020; nulls 3001 to 3005), saved R. The form is chosen by the rule of `results/framework-stage-1.md`: most planted worlds with the first lead true, among forms naming a lead in at most 2 of 15 nulls; ties to fewer named on nulls, then the order `all`, `largest`, `pooled`.

- **At least 8 of 20 first lead true, nulls at most 2 of 15, and above the floor for that form:** go on to step 3 on that form. The line is the same 8 the last method missed.
- **Fewer:** no fresh seed is used. Stop and report to the owner, with the oracle and the floor beside.

**Step 3, marks on fresh seeds, scored once.** `planted_3.50` seeds 7101 to 7140; each null panel seeds 7101 to 7110. Chosen form only. Its code is committed before it runs. Computed first:

- **E, worlds with something to find:** the real baseline told the exact link, over months 195 to 290, has S at least 0.02 and lower end above 0. **E must hold at least 20 worlds, or there is no verdict** and the rule goes back to him.
- **Instrument mark:** the exact column on the later months hears in at least 80% of E. A miss means the test half is too short for this statistic, and recovery below is not read as a verdict on search.
- **Recovery mark:** first lead true in at least half of E, Wilson 95% interval reported.
- **Quiet mark:** a lead named in at most 3 of 30 null worlds, Wilson interval reported.

All three met: Stage 1 passes for this method, and it goes to him before any Stage 2 rule. Any missed: stop for his guidance, including the proposal's check on changing direction. A later method needs its own rule and its own fresh seeds. Half and the 8 are judgements, as in Stage 1.

## Limits it carries

- One signal strength, one link shape, independent decoys. A pass says nothing about related inputs, combinations or other outcomes.
- One split, in time order. The months are not exchangeable if a world's link drifts; here it does not by construction, and real data may.
- The exact link is a strong reference and not a strict upper limit. E inherits that.
- Rule 2 is untouched: nothing here is a finding about real data.

## Estimates

About 300k tokens to the end of step 2. Machine: toy under 20 minutes, step 2 about 40 minutes, step 3 about 4 hours, two processes of 3 threads, nice 19. Overruns are reported beside the result.
