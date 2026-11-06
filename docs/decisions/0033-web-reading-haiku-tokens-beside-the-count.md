# 0033: Haiku tokens from web reading are reported beside the count, outside the cap

**Date:** 2026-11-06. **Status:** accepted. The owner's word, typed in the next-pattern session at 11:04 UTC, relayed, and checked in that transcript. Adds to decision 0006.

## Context

Next-pattern found that the web tools hand each page to Haiku inside the tool. That use is in no transcript, so the count never saw it. Its figure for this project's four research runs is 3,053,170 such tokens, from each run's `run.json`, beside 620,514 counted for the main model. Web reading inside an ordinary session is recorded nowhere it has found, so the figure is a lower bound.

## Decision

His words: "on the Haiku thing, report it beside the count, but don't include it in the caps."

## Consequences

Each gate report gives this figure beside the count, as it gives cache reads. Phase 1's 7M does not change.

Separately, a compaction's summary call is also in no transcript and does count. Next-pattern measured one at about 20k. This project's transcripts show 9 compactions so far, so the count is low by roughly 180k on that one measurement.
