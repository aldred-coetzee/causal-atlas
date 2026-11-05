# 0008: Roles and records

**Date:** 2026-11-05. **Status:** accepted.

## Context

House rule is one project, one session, with next-pattern coordinating. This repo
being public changes where some things can live.

## Decision

The project session does the project's work and reports at each gate. next-pattern
sets up, relays the owner's decisions in his words, and audits exactly twice, the
Phase 1 plan and the Phase 1 result. Gate approval is the owner's alone.

Records are `CLAUDE.md` (under 150 lines), `STATUS.md`, immutable
`docs/decisions/NNNN-title.md` and `results/` with one file per experiment, rule
first. The verbatim brief, the Remote Control unit and the nightly work log are held
in the owner's private configuration repo, not here.

## Consequences

No automated commit appears in this repo: every commit here is one this session made.
A cold session starts from `CLAUDE.md` and `STATUS.md`.
