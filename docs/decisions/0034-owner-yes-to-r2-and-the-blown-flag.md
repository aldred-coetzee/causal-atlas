# 0034: The owner says yes to R2 and to changing the blown flag; the hearing test waits

**Date:** 2026-11-06. **Status:** accepted. The owner's word, typed directly in this session. The flag change is a rule change that could favour a result.

## Context

R1 passed its gate on spent seeds. Its `blown` flag fired on 4 of 20 planted rows, against 1 in 20 allowed at R3, and a post hoc look showed all four are real surges where the events themselves exceed the limit (`results/r1-twin.md`). This session asked him three things, recommending yes to R2, yes to the flag change, and the hearing test only if the screen hears at 3.50 in R2.

## Decision

His words: "Happy to go at your recommendations. So yes on the first two and waiting on the third. I just want to be sure that we believe we're making progress there and not wasting time."

1. R2 goes ahead.
2. A span is now flagged `blown` when its forecast total is over 5 times the **larger of** the observed total of the previous 24 months and the observed total of the span itself. It is scored after the fact, so using the span's observed total is allowed. A forecast 143 times observed is still caught.
3. The hearing test waits, and is not built unless the screen hears at 3.50 and he then says yes.

## Consequences

The change was made after seeing four flags on spent seeds, and it is looser. The protection: the fresh seeds are unseen, the 5 times is unchanged, and the count of "no more than 1 row in 20" stands. R3 also reports the count under the old flag.

His last sentence is treated as an instruction. R2 gets an early stop on spent seeds, before the expensive calibration, set at R3's own counts (`results/r2-screen.md`). It can only stop work, so it cannot favour a result.

**A plan error found while writing R2.** Section 4 of the revision says each world has 8 input series (4 gridded, 4 global). The generator returns 2 series, drought and ONI; the 8 were the columns `input_features` builds from them. So 3 other worlds would give 8 series and 320 columns, not the 1,280 the plan states and the many-input null is meant to test. The figure is kept, since it is the harder test and the plan's rule on real data rests on it: each world gets its own 2 series plus 30 decoys from 15 other worlds, 32 series and 1,280 columns. The section's correction is marked in the plan.
