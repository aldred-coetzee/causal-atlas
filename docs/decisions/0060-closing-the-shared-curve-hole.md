# 0060: Closing the shared-curve hole: a baseline for each place, a recent line, and a check on what was new

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

Stage A1 (`results/finders-stage-a1.md`) measured one hole in the referee. Where a series and an outcome of a place share a curving drift and nothing else, the series a year before does go with the outcome out of time, and the referee passed it: at twice the usual strength of the drift, and at the usual strength once there were 480 places. Removing an input's past level and line does not remove a curve. The result said the hole must be closed before any real table is read.

Every choice below was made on smoke worlds from `synth/table_panel.py` (seeds 32001 to 32810, `results/seed-ledger.md`; never in a count). Each could favour a result, so all are recorded before any counted seed is run.

## Decision

1. **Each place's baseline is chosen for that place.** Stage A1's referee chose one baseline an outcome for all places, by the pooled error of earlier years. A place on a slow path of its own then got whatever served the many, and its path stayed in the baseline's error for any series on the same path to explain. Now each place's choice is by its own earlier error, with ten years of every place's usual error set beside it (`OWN = 10.0`), so a place with little to go on gets what serves all places.
2. **A sixth baseline: the line through the place's last fifteen years, carried forward** (`PATH`, `SPAN = 15`). It follows a slow path of any smooth shape; a line over the whole record does not.
3. **A check on what was new, not charged in the bar.** Beside the two reads held to the bar (each input as it fell; with its past level and line removed), a proposal is read a third time with each input as its departure from its own recent line. It must stand two of its own spreads above zero there and take something off the baseline's error (`CHECKS = ("recent",)`, `LEAST = 2.0`). It is a check and not a third charged read: charged, it raised the bar for every proposal and cost more of what can be heard than it kept out.
4. **A shared path with fresh movement of its own is counted as a link of the hidden-mover kind, not as a false pass.** This is a choice about what the test of the test counts, and it could favour a result, so the reasoning is given. When something unrecorded moves a series and an outcome together and keeps moving in ways its own past does not give, the series a year before is a second reading of where that thing now stands, and it does help forecast the outcome beyond anything the outcome's own history can. In the referee's own terms ("helps predict", never "moves") that is what it is asked to find; the made-up tables already plant it under the name hidden mover. What should be refused is a path whose next value the place's own history gives. Even there, a series on the path helps against any baseline that follows the path imperfectly, so what separates the two is how good the baseline is, not a line in nature.
5. **What follows from 4, owed before any real table is read:** the commonest pass on real tables will be "these two move together", not "this leads that". So a pass is labelled when the same pair, turned round (the outcome a year before for the series), passes as well; and Stage B's own rule considers putting the table's main shared movements in the baseline. The second count measures what the label separates.

`OWN = None`, `PATH = False` and `CHECKS = ()` give the referee as Stage A1 counted it; `scripts/referee_look.py` sets them so, and still reproduces the counted bars.

## What the smoke worlds gave, for what development numbers are worth

**What it costs.** Twelve worlds a kind (36 links), 35%, 120 places, the answer sent for the link's own places, as now against as Stage A1 counted it:

| Kind | now | as counted in A1 |
|---|---|---|
| steady | 36 | 36 |
| sign differing by place | 36 | 36 |
| hidden mover | 31 | 33 |
| threshold | 24 | 25 |
| extremes | 20 | 25 |
| pair | 19 | 21 |
| many weak | 19 | 20 |
| from a series shared by all places | 14 | 19 |
| sign differing by the state of a third series | 3 | 6 |

**What it keeps out.** The generator's two drift pairs sent directly, four ways each (all places, by claim, the best quarter and the best half of the groups by the early years), with keen proposals to forty. At 120 places and twice the strength (40 worlds) and at 480 places and the usual strength (20 worlds): no pass. At 480 places and twice the strength, one proposal of 96 in one world of twelve passed. A check at 2.5 spreads would have refused it and cost too much (pairs 19 to 10, extremes 20 to 13 of 36), so 2.0 stays and the one world is a stated remainder.

**Shapes of this session's own**, added to no-link worlds, a series and an outcome on one path in half the groups. A cubic and an S-curve: refused. A wave of period 40 to 90 years: no pass at 120 places, none at 480 places at the usual size, one world of eight at twice the size. A random walk smoothed over five years: passes, one world of 20 at 120 places, three of eight at 480 places, eight of eight at twice the size. That is point 4, seen before it was reasoned.

**Tried and dropped.** A recent line over ten or twelve years instead of fifteen: no gain on the generator's curve, a sharper check on waves, and more of the ceiling lost (shared 10 and 13 of 36 against 14, pairs 13 and 15 against 19, extremes 12 against 20 at ten years). A line plus one bend, fitted on earlier years, as a third form of the inputs: tried in the first rounds and set aside for the recent line, which assumes no shape. A line plus one bend is the very shape this generator plants, so no count on this generator could have said what that form was worth elsewhere. The check charged in the bar: see 3.

## What is not known

- The shapes the second count holds (`synth/shared_paths.py`) were written by a helper that never saw the referee, and no pass on them has been looked at by this session; only the seconds a world takes. Reading the helper's code against its brief showed that one foreseeable kind is a cycle with a period as short as 18 years, shorter than any wave tried here. A line through fifteen years cannot follow that, and it may pass.
- One family of worlds, one size of table, and the referee was shaped on it.
- Whether the turned-round label separates a shared path from a link as cleanly as point 5 hopes.

## Consequences

`src/causal_atlas/referee.py`, `tests/test_referee.py`; the plan's referee section says "as built"; `results/finders-stage-a1b.md` registers the second count. Stage A1's counted numbers stand as the record of the referee as it then was.
