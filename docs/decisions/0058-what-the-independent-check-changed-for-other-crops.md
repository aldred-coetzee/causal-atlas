# 0058: What the independent check changed for the other-crops test: five things said more plainly, and no condition of the rule

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

`results/crops-drought.md` registered a test of whether the drought term of the harvest forecast is worth using in the records where it has gone with a crop's yield before, to be scored once on 47 crops not yet read (decision 0054). Its made-up marks held. Before the real record was read an independent reader, with no part in the work, was asked to find a way the rule could read something that is not there, or a place where the code and the words differ (`docs/reviews/2026-11-10-crops-rule-check/SPEC.md`, committed before it started). No real yield of these crops had been set beside any drought value, and the reader set none.

Its verdict: "May be read after these changes", the changes being five corrections to what is said. Its report is kept unchanged in that folder with its scripts and logs. This session checked its main numbers against the counted rows and its logs; all agreed.

## Decision

1. **The rule is not changed.** Every condition, level, mark and made-up row stands as registered. Nothing is re-run in the count.
2. **The five things are now said in the results file**, in a section placed before the real record's result and written before it was read:
   - the best no-link world gained 0.58% at year-end and 0.78% at mid-year, not 0.58% for both; the link in a tenth of the records was read in 5 of the 8 worlds that had a linked record;
   - the cap almost never shrinks the term: the rule in effect chooses record-years by the record's past and adds the term whole, and a size is to be read as that;
   - the driver with its level and line removed is what holds off a trend shared by drought and yields. The driver as it fell passed every condition alone in one of the reader's two strongest no-link worlds and in one of eight more run by this session with all 62 shifts. The rule already needs both drivers. **A pass by one driver is never reported as a read, in this test or in what is built from it**;
   - the real record is rougher than the made-up worlds: more uneven, far more very large yearly changes, records that end early, crops in a country moving together less;
   - the other-years controls are not a fair test alone (beaten outright 3 times in 45 and 3 in 20 where a fair control gives under one), for a reason now measured; the condition is kept and is said to carry little weight by itself.
3. **No further condition is added.** Considered: a third form of the driver with its curve removed as well, since a curving shared trend is what nearly passed. Not done, for three reasons. The flat driver stopped all ten such worlds, at zero and not by a whisker. The real drought series, measured alone, curves about as much as the registered worlds and well less than those ten. And a condition added after seeing which worlds came close, on the eve of the read, is a change whose effect on the real record nobody has measured; adding it would be the safer direction, but the registered rule was found sufficient by the check it was sent to.
4. **Carried into the next plan's referee** (`docs/plan-finders-and-referee.md`): the interval over places and years is the guard; shifted copies are a weak control when the fitted term is larger under the true alignment; every proposal is scored with the driver's level and line removed as well as as it fell; a cap that never binds is said to be so; series run beside to inform the fit cost power.

## What is given up, and said beside the result

- A read on the real record would be on records rougher than any the rule was tried on. The interval and the dropped best year are the protection there is.
- The reader ran one to three seeds a setting and 20 shifts; rare false reads are not ruled out. The eight follow-up worlds used 62.
- How much of the real drought series' slow curve is shared with yields is unknown, and cannot be known without the read.

## Consequences

- `results/crops-drought.md` gains the section "Independent check of the rule, and what it changed"; four sentences above it carry dated corrections; the README paragraph is corrected.
- The reader's folder is committed whole: its report, scripts and logs; a note on what this session checked and added; this session's two follow-up scripts and their logs.
- `results/seed-ledger.md` records the seeds used from 26001 to 26099.
- The real record is read next, once.
