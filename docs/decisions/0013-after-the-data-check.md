# 0013: Rule changes after the data check, and a data sources file

**Date:** 2026-11-05. **Status:** accepted.

## Context

Step 1a (`results/1a-data-check.md`) put two questions to the owner, with a recommendation on each.
His answer: *"Proceed and I will go with your recommendations going forwards. So don't ask me again.
Also be sure though that we are maintaining a file somewhere in the repo which lists our data
sources, how to access them, the links, that kind of thing, the licensing requirements, etc., etc.
Because I think this will be part of the real value of this as we build it up over time."*

All of this was decided before any outcome was computed by place or period.

## Decision

1. **Events to the district centre count.** `where_prec` 1 to 3, 85.6% of African events, on the 0.5
   degree grid. Some level 3 events land in a neighbouring cell; this is disclosed.
2. **H2 is dropped from Phase 1.** No price data is fetched, because HDX's `robots.txt` disallows it.
   H1 alone is tested, with a 95% interval. This removes an input the brief names.
3. **SPEI is the drought input.** Its European host broke the tie, as the plan said.
4. **E is the last target month with its inputs,** 2025-03 at the primary lead, the same target months
   for every lead. Held-out 2021-04 to 2025-03, validation 2017-04 to 2021-03, train from 1992-01.
5. **ONI is used to t-1.** PSL describes a 3-month running mean; read as centred, its value at t
   holds t+1. If it turns out not to be centred, this costs one month of freshness and nothing else.
6. **Events go in the month of `date_start`.**
7. **`docs/data-sources.md` is kept up to date,** as the owner asked. It lists every source checked,
   including those not used, with its access route, links and what the licence requires of us.
   `data/manifest.toml` still holds versions and checksums. Decision 0007 left "a dataset catalogue"
   out of scope pending a Phase 1 result: this file is the owner's narrower yes, covering sources this
   project has actually checked. It does not start a survey of other datasets, and rule 5 still
   applies.

**The owner's "don't ask me again" is not yet read as dropping the gates.** Rule 6 requires this to
be quoted back and confirmed, and that was done the same day. Until he confirms, recommendations on
design choices are taken and reported, and each gate still stops for his yes.

## Consequences

The plan's amendments section records the effect on each rule. With one comparison, a circular shift
of 32 steps has a smallest p of 1/33, about 0.030, which meets the 0.05 that a single comparison
allows. The plan's limit on that criterion no longer applies. A 1b replicate is about 53 fits.

Dropping H2 means this phase can say nothing about food prices. A "no" for H1 must not be reported
as a "no" for cross-domain signals in general.
