# 0017: A one million ceiling for 1b, and a second run on a corrected design

**Date:** 2026-11-05. **Status:** accepted. Changes 1b's token stop at the owner's word and adds to 0016's step 1.

## Context

1b reached 508k against a 450k estimate. Its pass mark had proved unreachable in the 48-month scored window. The
owner, typed to next-pattern and relayed by it here: *"I think it'll be okay if we let it go higher than that. I don't
really have a problem with us capping this at 1 million tokens. I'd rather get a proper outcome than one that we
truncated early because of an arbitrary limit."* next-pattern reads "this" as step 1b, and has told him so that he can
correct it. The Phase 1 cap stays 3M and covers both sessions. 1M is a ceiling, not a target.

## Decision

1. The first run closes as agreed in `results/1b-known-answer.md`. Tokens did not stop it from passing; the scoring
   window did.
2. Inside 1b, a second run on a corrected design: a longer or rolling scored window, still scored once on real data; the
   detection mark stated in that window at the three-month lead from generator truth; the rule committed first; fresh
   seeds shared with no earlier run, nulls included. It is labelled a second run, with the first run's miss left beside it.
3. next-pattern checks the rule before the first fit, as part of the plan audit, not a third audit.
4. The 25% stop applies against the estimate given for this run.

## Consequences

The window chosen carries into the real test, so this is a design decision and not only a test setting.
