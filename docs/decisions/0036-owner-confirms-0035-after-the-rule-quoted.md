# 0036: The owner confirms the 20M and no asking on overruns, after rule 6 was quoted back

**Date:** 2026-11-06. **Status:** accepted. The owner's word, typed directly in this session. Corrects 0035, which stands otherwise.

## Context

Decision 0035 said rule 6's quote-back was not needed, because the figure and the instruction were explicit. That was wrong. The brief says: "If I tell you to go broader or to stop pausing, quote this rule back to me and ask me to confirm." This repo's `CLAUDE.md` had dropped "or to stop pausing" from its summary, and next-pattern caught the missed step. The rule was then quoted to him and he was asked.

## Decision

His words: "Yes on both cap raise and stop asking on overruns".

The cap is 20M. Step overruns are reported with the result, and are not put to him and do not stop work. Direction still goes to him.

## Consequences

The summary in `CLAUDE.md` now carries the full sentence. A summary of a rule that loses a clause loses the clause in practice, which is why the brief wins over the summary.
