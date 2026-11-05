# 0018: Stop the 1b first run after ratio 3.00, and check the null deficit first

**Date:** 2026-11-05. **Status:** accepted. Changes the order in 0016 and 0017, agreed by this session and next-pattern under the owner's
*"Happy to go with your collective recommendations."*

## Context

The first run's only mark is already recorded as missed, and its nulls belong to a 48 month scoring design that is being replaced. At 18
of 140 replicates it held the machine for most of a day before the second run could start. A smoke test then showed the inputs costing
about 0.03 on one null seed at 159 training months, which a day-long second run would only restate.

## Decision

1. The first run stops when ratio 3.00 has its 20 replicates. No first-run nulls or other planted panels are run. This cannot favour a
   result, since the only mark is already missed. The nulls' false-discovery and shuffle evidence comes from the second run, on its window.
2. The null deficit is checked before the second run, by the rule in `results/1b-known-answer.md`.

## Consequences

The first run's closing rule cannot report nulls and shuffles against their marks; the write-up says they were not run, and why. Its
description of detection by worth stands, on ratio 3.00 alone, as does the stop if replicates clearly worth 0.05 are missed. The per-panel worth
for the other first-run panels stays the generator table on seeds 101 to 120.
