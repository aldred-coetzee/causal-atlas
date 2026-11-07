# 0039: Measure how strong a link must be before any further method

Status: accepted, 2026-11-07.

## Context

Framework Stage 1's third method missed its line on spent seeds, 2 of 20 against 8, and a perfect shortlist reached 3 of 20 (`results/framework-shortlist.md`). The proposal's check on changing direction was put to him with three options: measure the limit, try a fourth method now, or stop blind search on this design. I recommended the first at about 400k tokens and most of a day of machine time, and asked "Shall I go ahead with option 1?".

## Decision

The owner, 2026-11-07: "Yes".

It answers that question only. The ladder of test worlds, Stages 2 and 3, and new data for Stage 3 stay open with him.

## Consequences

- The measurement runs under its own rule, `results/framework-curve.md`, committed before any number from its code.
- It uses a new seed range, in `results/seed-ledger.md`. Seeds 7101 to 7140 stay unspent, kept for marks on a method.
- It passes no method. What each outcome means is fixed in the rule, and the result goes to him before any further method.
