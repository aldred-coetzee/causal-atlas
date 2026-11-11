# 0064: Ties between sets that a row may not name

Status: accepted, 2026-11-11. Made by this session under decision 0040; reported to the owner, his to overrule. Adds to decision 0063 before any placebo, planted run or real read.

## Context

Decision 0063 lets a row name only series outside its outcome's set, to keep out ties that come from how one set is made. Two such ties cross the sets. The World Bank passes on some of FAO's figures (cereal yield, land, the production indices), and the crops set is FAO's. The World Bank's series in current dollars are local values turned into dollars at the year's exchange rate, and its file holds the rate itself; the exchange-rate set is the same rate from FAO. The first was registered only as something to call a near copy after a pass. The second was not registered.

The steward sends forty rows under one bar. A series that is another's figure under a second name, or made with it, stands very high on a board, so such rows could take many of the forty and the read would spend its one bar on what is known by construction. The same holds for the planted runs, where they would crowd out the planted links and make a silence look like it rules out less.

## Decision

A row may not name, either way round:

- a World Bank series whose `Source` in the Bank's series file names the Food and Agriculture Organization, with any crops series (22 series);
- a World Bank series whose name in that file holds "current US$" or "LCU per US$", with either exchange-rate series (54 series).

Fixed from the Bank's own description of each series, with no series looked at beside another. 2,110 of 43,613 pairs between sets.

## What it gives up

Some of the 22 are not copies of anything in the crops set (fisheries, fresh water, fertiliser use), and a real lead between them and a crop cannot be heard in this read. A real effect of the exchange rate on a dollar value beyond the arithmetic cannot be heard either. Both are left for a read with a finer rule.

## What it does not catch

Series in constant dollars or as shares may still carry the rate faintly. Other organisations' figures may sit in two sets under names this rule does not read. Whatever passes is still looked at by hand for a near copy.

## Could it favour a result

Yes: it changes which rows reach the forty. It is made before any run, the placebos and planted runs use the same rule, and it removes rows, none of which could have been reported as a lead.

## Consequences

`scripts/run_stage_b.py` (`TIED`, `tied`); `results/stage-b-first-read.md`.
