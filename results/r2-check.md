# R2 check: does the screen hear with a fair gate and a smaller search?

Rule first, committed before any number (rule 9). The owner's yes: decision 0035. A diagnostic on spent seeds, not a mark. Code: `scripts/run_r2_check.py`, `screen.gate`.

## Question

R2 part A stopped with too many false alarms and too few true inputs (`results/r2-screen.md`). With the gate's scaling corrected, is the screen quiet, and does it hear, at 1,280, 320 or 80 columns?

## Same as part A

The same 35 worlds: `planted_3.50` seeds 3001 to 3020; `pure_null`, `shared_null`, `combo_null` seeds 3001 to 3005. The same decoys, months 195 to 290, columns, shifts, K = 5, three forms, 25 trees. No tier 2. No fresh seed.

## What changes

- **The gate:** Z is scaled by the mean and SD over all 33 values, the unshifted included.
- **Search size:** each world's table is read at three sizes, always with the world's own 2 series first: 1,280 columns (32 series), 320 (own 2 and the first 6 decoy series), 80 (own 2 alone).
- **T tables are saved** per world under `data/panel/r2-tables/`, not committed, so later questions need no rerun.

A correct gate should name a lead in about 1 world in 33 where nothing is linked, so 15 null worlds should give 0 or 1.

## How it is read, fixed now

For each form and size: null worlds naming a lead, at most 2 of 15, and planted worlds naming a true column among the leads, at least 16 of 20.

- **At 80 columns every column is true**, so hearing there only means the gate fired. It is the easiest case, and it says nothing about picking the right input.
- **If no form and size reaches both bars**, this screen is closed. That means this statistic at this signal strength over 96 months. It does not mean discovery as a whole.
- **If some form and size reaches both,** that is the largest search the screen supports on this evidence, on seen seeds, with no margin. No setting changes and calibration does not start: what follows goes in the framework proposal.
- **If the gate is still noisy** at the corrected scaling, above 2 of 15, the shifts themselves are not a fair comparison on these worlds. That is reported as its own finding.

Beside them: a true column in the top 5, and the same at each size on nulls, by chance.

## Limits

About 1.5 machine hours, about 40k tokens, estimates only (decision 0035). Two processes of 3 threads, nice 19.

## Result

Run 2026-11-06, 15:40 to 17:15 UTC, from e325e01, as a unit started by next-pattern. All 35 worlds, no failures. Rows `results/r2-check.jsonl`, log `results/r2-check.log`. Spent seeds, no margin, 15 null worlds, so counts are rough.

**The rule's answer: the gate is now quiet, the screen does not hear at any size, and this screen is closed.** That means this statistic at this signal strength over 96 months, not discovery as a whole.

| Columns | Null worlds naming a lead, of 15 (`all`, `largest`, `pooled`) | Planted worlds naming a true column, of 20; 16 needed |
|---|---|---|
| 1,280 | 0, 0, 0 | 1, 1, 1 |
| 320 | 1, 0, 1 | 2, 2, 2 |
| 80 | 1, 0, 0 | 4, 4, 5 |

The correction worked as a test of false alarms: 9 to 11 of 15 became 0 or 1. It also cost the few hits part A had, which were partly the flaw firing. At 80 every column is true, so 4 or 5 of 20 means the gate fired at all. So removing decoys does not rescue it, and search size is not the main cause.

**Beside the marks: a post hoc look at the saved tables, on spent seeds, after the verdict; no setting comes from it.** Three plainer readings give the same picture at 80 columns:

- The largest unscaled T beats every shift in 3, 3 and 4 planted worlds of 20 by form, and 1, 0 and 0 null worlds of 15.
- The mean T of all 80 true columns beats all 32 shifts in 5 of 20 planted worlds and 0 of 15 null worlds.
- The best true column stands 2.1 times above its own shift mean on planted worlds, against 1.63 on nulls, with `all`.

A planted world differs from a null one, but in most worlds not by enough to tell inside 96 months. The planted signal, named as the strongest in the plan, has never been shown to be easy. R1's 16 of 20 had the right inputs handed over, with 240 months.

**Unanswered:** whether any method could hear these worlds in 96 months, or whether the worlds themselves hold too little in that window. Nothing here measures an upper limit, such as a test given the true link. That gap is a question for the framework.

**Tokens.** Stated at the report beside this file.
