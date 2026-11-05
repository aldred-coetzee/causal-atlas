# 0019: The 1b second run does not go ahead; a proposal to fix the comparison instead

**Date:** 2026-11-05. **Status:** accepted. Supersedes the second run of decisions 0017 and 0018 before any fit.

## Context

The first run missed replicates clearly worth finding, and showed gaps between two fitted models far larger than the margin. The checks after it found the baseline's level far
off in some scored months and the inputs model gaining 3% to 6% in training, more than most effects are worth. A longer scoring window does not fix that.

next-pattern put two things to the owner: (1) "does your 1M for step 1b cover the project session's work only (about 320k left, my recommendation), or both sessions (essentially
spent)?", and (2) "the long second run should not go ahead as designed, because a longer scoring window does not fix a baseline that is off-level. The next step should be a short,
written proposal for fixing the comparison itself, tried on fresh made-up panels." His answer, typed in next-pattern and relayed: *"I will go with your recommendation"*.

## Decision

1. The 1M ceiling for 1b covers this session's work only. next-pattern's coordination counts against the 3M phase cap as before.
2. The second run as designed is not run. The window criterion and its numbers stay on record and may still be used.
3. The next step is a written proposal, rule first, checked by next-pattern in one reply before anything runs. If the learner cannot be made quiet at reasonable cost, that is reported as the result.

## Consequences

`scripts/run_1b_second.py` stays in the repo unused unless the proposal reuses it. Seeds 3001 to 3020 have never been fitted and are still fresh.
