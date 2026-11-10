# 0059: How the referee was shaped on smoke worlds, and where it departs from the plan

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The plan (`docs/plan-finders-and-referee.md`, "The referee") set out the referee in ten points before any of it was built. Building it and running it on made-up tables with smoke seeds (27001 to 27086, `results/seed-ledger.md`; development, never in a count) showed that some of those points were weak or silent. Every choice here was made on those smoke worlds. They could favour a result, so they are recorded before any counted seed is run.

## Decision

1. **What is held to the bar is the agreement, not the share removed.** For each place and scored year the referee has the baseline's error and what the proposal would add to the forecast. The plan held the share of squared error removed (twice their product, less the square of the addition) to the bar. The product alone, summed and taken as a share of the same squared error, is the agreement: it is above zero on average only if the term knows something, and on smoke worlds it stood about twice as many of its own spreads above zero as the share removed did. So the agreement is what must stand above the bar. **The share removed is still required to be above zero, with each form of the inputs, and without its best year**, so nothing passes that did not beat the baseline (rule 2); it is the size that is reported, with its own interval.
2. **Errors are counted in each place's usual error so far**, the middle of its absolute errors in earlier years, never taken as less than a quarter of the middle place's; **a departure of more than three of them counts as three.** So places count alike and one wild year does not decide a score. The share removed against the outcome as it fell, nothing capped, is reported beside.
3. **An input's comparable form is capped at three of its own past spreads.** A few wild values in an input otherwise set its slope. On smoke worlds, with the answer sent where the link is: steady links read 27% removed against 20% uncapped, pairs 16.5% against 10%, thresholds 40% against 22%.
4. **Groups of places and years are both drawn again**, as the plan says. Drawing years alone was tried: worlds with no link then gave statistics up to seven spreads above zero.
5. **A proposal must apply in at least five groups of places and ten scored years** (the first draft said eight groups; a quarter of the places is six).
6. **The bar is over every read, both forms of every proposal.** A pass needs both forms above it. That is stricter than the stated rate needs when neither form hears anything, so the real rate of false passes is expected well under 1 run in 20. A bar on the smaller of the two forms would be sharper and would not be valid where one form hears a shared drift, which is the case the second form is there for. Kept strict.
7. **Tried and dropped:** taking an input as its surprise against its own past (no gain; the ceiling for many weak series is in how little each carries, not in the form); a sturdier measure of an input's spread (little gain beside the cap).

The other constants are in `src/causal_atlas/referee.py` with their meanings; what was varied on the smoke worlds is listed above as far as this session's record of it goes.

## What the smoke worlds gave, for what development numbers are worth

Forty proposals a world, the answers among them, first scored year 35 of 60, a link planted in a quarter of the places. Seeds 27055 to 27084, links passed of 45, the answer sent for the link's own places:

| Kind | at 35% | at 20% |
|---|---|---|
| steady | 45 | 42 |
| sign differing by place | 45 | 42 |
| hidden mover | 38 to 41 | 23 |
| pair | 24 to 32 | 15 |
| many weak | 23 to 30 | 8 |
| from a series shared by all places | 25 to 27 | 13 |
| threshold | 21 to 22 | 12 |
| extremes | 19 to 28 | 10 |
| sign differing by the state of a third series | 9 to 10 | 3 |

(Two figures are two sets of fifteen worlds.) The same answers sent for all places passed in none of 45 for any kind. Sent by claim: steady 38 or 39 of 45 at 35% and 14 at 20%, hidden 11 or 12, the rest near none. With four times the places, at 20%: steady 45, threshold 45, many 45, extremes 41 in the link's places; steady 37 for all places.

No-link worlds, 150 of them over six kinds (seeds 27030 to 27054), forty keen proposals each: no pass. The largest statistic in the smaller of a proposal's two forms was 3.31 of its spreads, under a strong nuisance, against a bar near 3.6.

**A thing not looked for:** the keen proposer's second half, which names the quarter of the groups of places where a series went most its pooled way in the early years, named the link's own places and passed for 43 of 45 steady links at 35% and 29 of 45 at 20%. That is the first sign that where a link holds can be found from the early years by something very simple. It is a smoke number and no finder's test.

## What is given up, and said beside any result

- **The referee was shaped on worlds from the same generator as the counted ones.** The generator was written by a helper that never saw the referee, but the referee has seen forty or so of its worlds. Fresh seeds test the rule on new worlds of that family, not on a different family. The real record is rougher than made-up ones have been (decision 0058).
- **The caps cost something where a link lives only in the wildest values.** No such world is in the generator.
- **Strict means deaf.** With the bar over both forms, a real link that the level-and-line form weakens is lost. The sizes on smoke worlds are the smaller of the two forms and run at half to three quarters of what was planted.
- **Not knowing where costs more than anything else measured here.** A link in a quarter of the places, sent for all places, was not heard at all at this size of table.

## Consequences

- `src/causal_atlas/referee.py`, `tests/test_referee.py`, `scripts/run_referee.py`.
- The plan's referee section is amended at points 5, 7 and 8 and points here.
- The tests of the test, with their marks: `results/finders-stage-a1.md`, committed with this record and before any counted seed.
