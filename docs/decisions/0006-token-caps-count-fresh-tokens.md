# 0006: Token caps, and what they count

**Date:** 2026-11-05. **Status:** accepted.

## Context

The brief caps Phase 0 at 300k tokens and Phase 1 at 3M, covering both this session
and next-pattern's audits. The subscription limit is shared with every other
session on the box, so spend here can lock the owner out of the others. Asked
whether to change the caps, and what counts as a token, the owner answered *"(a) yes
(b) count fresh tokens"*.

## Decision

The numbers are unchanged. A cap counts fresh tokens: input + output + cache writes.
Cache reads are not counted against the cap but are reported beside it at every gate.

## Consequences

Fresh tokens measure new work and are the honest thing to cap, but cache reads can
be many times larger, so they stay visible. Figures are taken from the session
transcripts, not estimated. A step heading 25% over its estimate stops and says so.
