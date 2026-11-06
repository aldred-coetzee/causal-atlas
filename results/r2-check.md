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

Not yet run.
