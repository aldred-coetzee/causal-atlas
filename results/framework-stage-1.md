# Framework Stage 1: can a blind search find a real input, once the instrument hears?

Rule first, committed before any number from this code (rule 9). The owner's yes: decision 0037. Proposal: `docs/framework-proposal.md`. Code: `src/causal_atlas/bench.py`, `synth/toy.py`, `scripts/run_stage1.py`.

## Seen before this rule, so nothing is blind to it

`results/r2-check.md` and `results/r2-ceiling.md` on the spent seeds: the capped screen names a true column in 1 to 5 of 20 at every size, and given the exact column it hears 6, 6, 3 of 20 capped and 14, 12, 19 uncapped. No number exists for the uncapped screen on real candidate columns.

## The harness

- **A world** holds the outcome, its named input series, which of them are truly linked, and the link's exact effect. A null world holds the same parts and no link.
- **A method** takes a world and months, and returns ranked claims: input, gap, width, strength, and whether its own gate named each as a lead.
- **The scorecard** reads every method the same way, with its floor and its ceiling beside it.

The floor is a method ranking at random: first claim true in 2 of 32 series, 6.25%, about 1 world in 20. The ceiling is a method handed the truth: it must score every world, which tests the scorecard. Both run as plug-ins.

**A relationship counts as found when the first lead the gate names comes from a truly linked series**, so a world naming a decoy first and a true input later is a miss. This is stricter than R2's "any lead". R2's reading is reported beside it. Whether the lag falls within the true lags is reported beside too, not marked.

## Methods

The screen as built, and the screen with no cap on counts. Same columns, 32 year shifts, K = 5, three forms, corrected gate. No other change. A third method needs its own rule committed first.

## Rungs

**Toy** (`synth/toy.py`, sharing nothing with the detector): every fifth cell of the grid, an outcome of seasonality, AR(1) and unit noise. Planted: 0.25 × a cell input at lag 6 in the northern half of cells, plus 0.25 × a global input at lag 8. Null: no link. Own 2 series and 30 decoys, 1,280 columns. The baseline is plain code: month means and the AR term, fitted before month 195, at three months ahead. Months 195 to 290. Seeds 7001 to 7020 planted, 7001 to 7015 null.

**Count**, as in R2: `planted_3.50`; `pure_null`, `shared_null`, `combo_null`. Months 195 to 290, 25 trees, own 2 series and 30 decoys, 1,280 columns.

## Tests of the test, before any score counts

1. **Noise:** the gate on tables of pure noise names a lead at about 1 in 33 (standing unit test).
2. **Exact answer:** the method's statistic given the exact column beats all 32 shifts. Reading C of `results/r2-ceiling.md`.
3. **Baseline sanity:** on null worlds, R's total per span within 0.2 to 5 times observed; the count outside is reported.
4. **Floor and ceiling plug-ins** score as stated above.

## Order and marks, fixed now

**Step 1, toy.** For each method and form: first lead true in at least 18 of 20 planted, a lead named in at most 2 of 15 nulls. A miss means the harness or the method is broken on the easiest case: stop, find out why, report.

**Step 2, development on spent seeds** (3001 to 3020; nulls 3001 to 3005). The saved R is reused, so nothing is refitted. The form is chosen here: most planted worlds with the first lead true, among forms naming a lead in at most 2 of 15 nulls; ties go to fewer named on nulls, then the order `all`, `largest`, `pooled`.

- **At least 8 of 20 first lead true, nulls at most 2 of 15:** go on to step 3, on the method and form chosen.
- **Fewer:** no fresh seed is used. Stop and report to the owner, with the search sizes 320 and 80 read from the same table beside. That would mean a blind search of this kind does not reach what the exact column can.

8 is a chosen line, not a calculation. It is 40%, above the capped screen's best of 5 at 80 columns, and it asks for clearly more than the floor. It was set knowing those seen numbers and not knowing the uncapped table's.

**Step 3, marks on fresh seeds, scored once.** `planted_3.50` seeds 7101 to 7140; each null panel seeds 7101 to 7110. Chosen method and form only. The denominator is set by the ceiling, computed first:

- **E, worlds with something to find:** the real baseline told the exact link has S at least 0.02 and lower end above 0.
- **Instrument mark:** given the exact column, the method hears in at least 80% of E. A miss here means it is still deaf, and recovery below is not read as a verdict on search.
- **Recovery mark:** first lead true in at least half of E, Wilson 95% interval reported.
- **Quiet mark:** a lead named in at most 3 of 30 null worlds, Wilson interval reported. The gate's design rate is 1 in 33, so about 1 of 30.

Half is a judgement: a tool that finds half of what can be found, at about one false alarm in thirty worlds, is worth taking to the harder rungs, and one finding less is not yet. Worlds outside E are reported on their own line and count neither way.

- **All three met:** Stage 1 passes for this method, reported, and Stage 2's rule is written.
- **Any missed:** stop for the owner's guidance, with the option of a third method under its own rule.

## Limits it carries

- One signal strength, one link shape, independent decoys. A pass says nothing yet about related inputs, combinations or other outcomes: those are Stage 2.
- The exact link is a strong reference and not a strict upper limit (`results/r2-ceiling.md`). E inherits that.
- Step 2 is on seen seeds, so it only decides whether to go on.
- Rule 2 is untouched: nothing here is a finding about real data.

## Estimates

Tokens, 1M to 2M for the stage. Machine: toy about 30 minutes, step 2 about 2 hours, step 3 about 10 hours, two processes of 3 threads, nice 19. Overruns are reported beside the result.

## Results

**Step 1, toy: passed** (35 worlds, 9.5 minutes). Mark: first lead true in at least 18 of 20, a lead named in at most 2 of 15 nulls. At 1,280 columns:

| Form | First lead true | Any lead true | Lead named on nulls |
|---|---|---|---|
| all | 20 of 20 (Wilson 95%: 84% to 100%) | 20 | 1 of 15 (1% to 30%) |
| largest | 20 of 20 (84% to 100%) | 20 | 1 of 15 (1% to 30%) |
| pooled | 20 of 20 (84% to 100%) | 20 | 0 of 15 (0% to 20%) |

- Tests of the test: given the exact column, all three forms beat all 32 shifts in 20 of 20 planted worlds and in 0 of 15 nulls, where the column does not enter the outcome. The exact link's median gain is 0.08 of the residual variance.
- Beside the mark, not marked: `all` and `largest` named the cell input at gap 3, width 1 in all 20, which is its true lag of 6 (gap plus the lead of 3). `pooled` did so in 12 and scattered around it in 8. The global input at lag 8 has no matching gap (5 is not in the grid) and was never the first claim.
- What this says: the harness and the screen work on smooth numbers with a plain baseline and a link this strong, and nothing more. The link here is 0.08 of the residual variance in every world, which is far easier than the count world's.
