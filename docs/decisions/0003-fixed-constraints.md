# 0003: Fixed constraints

**Date:** 2026-11-05. **Status:** accepted.

## Context

The owner's brief sets constraints that hold for every phase.

## Decision

- No person-level inference. Limitations are published beside every finding.
- European, non-US-controlled infrastructure where practical.
- Deterministic at runtime: LLMs are used only inside sessions at design time,
  with no model calls in pipeline code.
- Everything runs on one box (8 cores, 16 GB RAM, 512 GB NVMe), in Python under
  a uv-managed environment, with DuckDB and Parquet.
- Provisional, to be confirmed by test and not by reading: PRIO-GRID-compatible
  0.5 degree cells at monthly resolution; PCMCI (tigramite) and empirical dynamic
  modelling (pyEDM, convergent cross mapping) as candidate methods.

## Consequences

A method too heavy for the box is out, whatever its merits, and its runtime is a
result to report. The provisional items are not commitments: a method that fails
the known-answer test is dropped. Where a data source has no European equivalent,
the source is used and the fact recorded.
