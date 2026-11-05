# 0009: Commits use a GitHub noreply address

**Date:** 2026-11-05. **Status:** accepted, made by the project session, reported at
the Phase 0 gate.

## Context

Rule 10 says no email address goes into the repo. A commit's author and committer
fields are in the repo, and the box's global git identity is a personal address that
the owner's other repos carry. Left alone, the root commit would have published it
permanently, and this could not be undone without the force-push the brief forbids.

## Decision

This repo's local git config sets `user.email` to the owner's GitHub noreply address,
which still attributes commits to his account. The global identity is untouched,
because box configuration is not this session's to change.

## Consequences

Local config does not survive a fresh clone: a new clone must set it before
committing, and the pre-push sweep checks authorship with
`git log --format='%ae %ce' origin/main..`.
