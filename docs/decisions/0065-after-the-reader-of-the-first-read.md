# 0065: After the independent reader of the first read's rule: seven more tied series, a guard on gathered rows, refusals that hold

Status: accepted, 2026-11-11. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

An independent reader, with no part in the work, read the first read's rule and code before any run on the real table (`docs/reviews/2026-11-11-stage-b-rule-check/report.md`). It ran nothing on the real table and read no real values. It found three things to fix before the first placebo and several things the rule said more firmly than it should. Each of its three faults was checked in the code by this session before anything was changed. Nothing had been run on the real table when these changes were made.

## Decision

1. **Seven more World Bank series may not be named with a crops series.** The Bank's greenhouse gas figures for agriculture are worked out from FAO's crop and animal figures (the reader's reading of the Bank's own descriptions). Barred with crops: methane, nitrous oxide and carbon dioxide from agriculture; total methane and total nitrous oxide, of which agriculture is a large part; and the two all-gas totals, where agriculture is the larger part in many farming countries. Left in: the carbon dioxide totals, of which agriculture is a small part, and the gases by other sectors. The tied series are now 29 with crops and 54 with exchange rates; 2,747 of 43,613 pairs between sets (2,110 before).

2. **The exchange-rate ties the reader named are not in the panel** (price level indices, the real effective rate, the trade value and unit value indices, terms of trade): checked by id against the panel's list of series. Nothing is added for them. If a later panel holds them, they are tied.

3. **A gathered row cannot name what it may not.** Where a series that may be named has no standing for an outcome (no overlap in the early years), it sorted behind the barred series and a gathered row could reach into them, the outcome itself included. With a cut on names, such a series now sorts with the barred, and no more series are gathered than may be named and have a standing at every alignment. Without a cut nothing changes: twelve counted worlds, one of each kind, read again as a check give the stored rows exactly. A test holds the guard and fails on the code as it was.

4. **The script's refusals are exits, not asserts**, so they cannot be switched off. The placebo marks count registered seeds, each kept once, and refuse a seed kept twice; a run that finds its seed already kept by another process does not keep a second row. The real read is refused until the six planted runs are in as well as both marks.

5. **What the marks and the planted runs do not say is written into the rule**: holding both marks is compatible with a false-pass rate of one in ten or a little more; the runs are rearrangements of one table; a planted link's size is not the made-up tables' measure; an input that keeps its level makes the same share a larger effect, so heard counts are given by the input's memory; no link is planted from a common series; planted tables are easier than the real one; a gap-filled or revised series can carry later years into earlier ones; the sorting of what passes is by hand.

## Considered and not done

- **More placebo runs, to tighten the marks.** At about 25 minutes a run, forty more would add most of a day for a mark that still could not show one in twenty. The last ten years, untouched, are the second guard, and the reader's own check found the confirmation rule passed by chance in 0 of 80 tries on made-up tables.
- **Planting a link from a common series.** The registered plan plants between series that differ by place, and its sizing is place by place. Said as a limit.
- **Changing how a planted link is sized.** Stated as it is made.

## Could it favour a result

Barring more pairs removes rows that would have passed for a reason that is not a lead; it could also remove a real lead from farm emissions to crops, which is given up. The guard removes rows that should never have been built. The refusals and the marks' counting can only stop a read, never allow one. All of it was fixed before any run.

## Consequences

`scripts/run_stage_b.py`, `src/causal_atlas/finders.py`, `tests/test_finders.py`, `results/stage-b-first-read.md`. The reader's smoke seeds 47990 to 47999 are spent.
