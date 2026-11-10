# 0061: The label a pass carries: it may be two series moving together

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The referee's second count (`results/finders-stage-a1b.md`) showed what a pass means: knowing the series a year before improves the forecast beyond the place's own history. It does not show that the series leads. A series and an outcome that share a slow path and nothing else pass as well: a regular cycle in 10 of 40 worlds at 120 places and 40 of 40 at 480, paths with fresh movement of their own nearly always at 480 places. Decision 0060 (point 5) owed a label before any real table is read, and the count's rule made it a condition.

The count also measured the first form of that label, the same pair turned round and held to the full bar. It never passed for a planted link (0 of 1,440) and passed for 293 of 343 path passes at 480 places, but only 10 of 36 at 120. A check after the count suggested a lower mark would do better. That was seen on spent worlds, so it is not a result, and the label is shaped here on smoke worlds and counted on fresh ones.

Every choice below was made on smoke worlds (seeds listed at the end; never in a count). Each could favour a result: a label that is too slow lets "moves together" be read as "leads", and one that is too keen marks real leads down.

## Decision

1. **Each pass carries a label, "may be moving together", when either of two readings beside it says so.**
   - **Turned round.** Each input of the proposal that differs by place is made the outcome, with the outcome that many years before as its input, in the same places; the form is kept where the proposal has one input, a plain slope otherwise. If any of these stands more than two of its own spreads above zero and takes something off its baseline's error, in both reads the referee holds to the bar, the pass is labelled (`BACK = 2.0`). A proposal whose inputs are all one series common to all places cannot be turned round, and that is recorded as such.
   - **The same year.** The proposal is read again with each input as it stood in the outcome's own year. If it stands at least as far above zero there as it does with the inputs beforehand (the lesser of the two reads, each way), the pass is labelled.
2. **Neither reading is charged in the bar, and neither can make or unmake a pass.** They are read after the bar is set, on passes only. The bar and every pass are what they were under decision 0060; a test holds this.
3. **What the label says and does not say.** Labelled: the pass still improves the forecast, and that stands; what is not shown is that the series comes first. Unlabelled: the series a year before tells something the outcome a year before does not tell of the series, and more than the same year tells. That is a lead in time. It is not a cause, and an unrecorded thing that moves the series first and the outcome a year later is unlabelled too (the made-up tables plant it as the hidden mover).
4. **A real link that also acts within the year will be labelled** by the same-year reading. That is intended: where a series moves an outcome in the same year and the series lasts from year to year, last year's value helps only as a stand-in for this year's, and "leads" would be the wrong word. The made-up tables do not plant that case; a test in `tests/test_referee.py` does.

## What the smoke worlds gave, for what development numbers are worth

229 worlds, forty proposals each: a shared path added to a no-link world (116), links of the nine kinds (81), and a path put beside a link's own outcome and series (32).

Passes of a path's pair (sent directly or by the keen proposer), and how many each reading labels:

| Places | Worlds | with a pass | Passes | turned round above 1.5 | above 2 | above 2.5 | above 3 | same year | either (at 2) | Worlds with a pass left unlabelled |
|---|---|---|---|---|---|---|---|---|---|---|
| 120 | 56 | 10 | 17 | 17 | 17 | 15 | 14 | 8 | 17 | 0 |
| 240 | 35 | 20 | 72 | 62 | 62 | 58 | 49 | 66 | 70 | 2 |
| 480 | 25 | 24 | 179 | 172 | 170 | 164 | 155 | 171 | 179 | 0 |

The two left at 240 places were one pass on the regular cycle and one on the cycle whose phase wanders.

Passes of a planted link's answer (for its own places or by claim), in worlds with no path:

| Places | Passes | cannot be turned round | turned round above 1.5 | above 2 | same year | either (at 2) |
|---|---|---|---|---|---|---|
| 120 | 124 | 5 | 0 | 0 | 1 | 1 |
| 240 | 133 | 8 | 2 | 0 | 0 | 0 |
| 480 | 86 | 4 | 1 | 0 | 0 | 0 |

So of 343 passes of a real lead one was labelled (a hidden mover at 120 places, 4.7 in the same year against 4.4 beforehand). The keen proposer's passes that name a planted input, in worlds of steady links and hidden movers with no path: 1 of 56 labelled.

Then, through the count's own harness (`scripts/run_referee_c.py smoke`, 28 more worlds): 23 of 23 path passes labelled in four worlds; 0 of 95 passes of a lead labelled in nineteen linked worlds, two of each kind and three of the shared kind, at 240 places.

**A lead and a path in one pair** (a path given to a link's own outcome and series, in the link's places): the link's answer was labelled in 3 of 6 passes at 120 places, 8 of 15 at 240, 7 of 8 at 480; through the harness 2 of 5. Both things are true of such a pair, so neither answer is wrong, and it is measured with no mark. What it shows is that a label does not mean there is no lead.

**Tried and not chosen.** The turned-round mark at 1.5 (no gain on paths, 3 of 343 leads labelled against 0), at 2.5 and at 3.0 (paths lost: 15 and 14 of 17 at 120 places). The turned-round reading alone at 2: 6 and 5 worlds with an unlabelled path pass at 240 and 480 places, against 2 and 0 with the same-year reading beside it. The same year counted when it reaches eight tenths of the forward strength: it labels the two path passes left at 240 places (72 of 72) and 11 of 343 leads against 1; a label that marks down one lead in thirty to gain two passes in 268 was not taken.

## What is not known

- How many shared-path passes go unlabelled at each size of table, on worlds not used for shaping. That is the count's first mark. At 240 places, the size nearest the real yearly table, the two cycles are where a miss was seen.
- Whether a real table's slow shared movement resembles any of the seven shapes.
- Links whose input is a series common to all places cannot be turned round; only the same-year reading speaks for them.
- A lag other than one year: the turned-round form uses the proposal's own lag, and nothing longer than a year has been tried.

## Consequences

`src/causal_atlas/referee.py` (`turned`, `label`, `BACK`; `judge` attaches a label to each pass), five tests in `tests/test_referee.py`, `scripts/run_referee_c.py`, and `results/finders-stage-a1c.md`, which registers the count. Decision 0060's other debt stands: Stage B's own rule puts the real table's main shared movements in the baseline.

Smoke seeds: 32041 to 32099, 32121 to 32201, 32213 to 32300, 32521 to 32552 (32201 a second time). In `results/seed-ledger.md`.
