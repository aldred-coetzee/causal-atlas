# 0015: Finish the machinery, then add sources, with the held-out set unscored

**Date:** 2026-11-05. **Status:** accepted. Changes the order of Phase 1 at the owner's word.

## Context

Step 1b stopped because the planted effects were worth far less than the 2% margin (see
`results/1b-known-answer.md`). The owner then said: *"what we need to do initially is just collect more
data and get more data sets put together, and then start studying different kinds of mathematics or
biological systems"*. Rule 6 was quoted back with three options. His answer: *"1, go with your
recommendation"*.

## Decision

In this order:

1. **Fix the generator and re-measure,** about 30k tokens, by its original author, to keep it independent
   of the detector. next-pattern pointed out that the first table may partly reflect the generator's
   faults, so those numbers set nothing.
2. **Finish 1b,** with the changes in the results file's amendment. Each planted panel reports its rate
   ratio, the share of cells it affects and the best possible skill it is worth, so that a "no" can say
   what size of effect it excludes.
3. **Do not run 1c or 1d now.** The held-out set can be scored once, so it waits for the richer test.
4. **Add about 10 sources to `docs/data-sources.md`, capped at 150k tokens.** This is his yes for "more
   domains" and a list of checked sources from the "Not now" list, up to that cap.
5. **Then stop for the owner:** set the margin, knowing what 1b says it can detect, and pre-register a
   multi-input test before any real input meets a real outcome.

New methods come in one at a time, after that, with one question each and the known-answer test first
(rules 3 and 5). No open reading survey: he did not choose that option.

## Consequences

The plan's 1c and 1d are deferred, not dropped. The 3M cap stands. The plan's amendments section is the
place to look for the current order. Any "no" from Phase 1 can no longer come from two inputs alone
unless he chooses that later.
