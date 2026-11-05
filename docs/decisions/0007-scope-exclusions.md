# 0007: What is out of scope

**Date:** 2026-11-05. **Status:** accepted.

## Context

The earlier failure described in decision 0004 was one of breadth, so the brief
names what is not to be built.

## Decision

causal-finance is out of scope for this repo. Also not now: web UI, maps, API, more
domains, global coverage, a generic adapter framework, a dataset catalogue, a
literature survey. Each needs a Phase 1 result and the owner's yes.

## Consequences

Phase 1 code fetches its few sources with plain one-off scripts, with no abstraction
over them. A second domain or region is new work to be argued for, not a
configuration change to be anticipated.
