# causal-atlas

A spatiotemporal observatory, at the very start. The aim is to bring event and
indicator data from different domains (conflict, climate, food, prices and
others) onto one grid of place and month, find time-lagged relationships between
domains, and use them to predict trends.

**Nothing is built and nothing has been found yet.** The repo holds its rules,
its decisions and, shortly, a pre-registered design for one experiment.
`STATUS.md` says where things stand.

## The question

Do lagged signals from other domains improve the prediction of an outcome in a
place beyond what that place's own history and seasonality already give? This is
a working hypothesis, to be tested and not assumed. It may well be false; a
clean "no" is an acceptable result and would be published the same way.

## How it is run

The first deliverable is a test, not a survey. A baseline comes first, and
nothing counts as a finding unless it beats that baseline out of time. A method
must recover planted links in synthetic data, and find none in null data, before
it is pointed at real data. Metric, split and threshold are committed before any
number is computed, and the held-out set is scored once. The rules, and the
failure in an earlier project that produced them, are in
`docs/decisions/0004-working-rules.md`.

The analysis is at the level of grid cells and months. There is no person-level
inference, and limitations are published beside every finding. Pipeline code
makes no model calls: it is deterministic at runtime.

## Layout

- `CLAUDE.md`: the standing brief for the working session.
- `STATUS.md`: the honest current state.
- `docs/decisions/`: decision records, immutable once written.

Later, `docs/plan-phase-1.md` for the design and `results/` for one file per
experiment, each with its rule committed before its numbers.

## Licence

Code is MIT (`LICENSE`). Text is CC BY 4.0 (`LICENSE-CC-BY-4.0`). Third-party
material keeps its owner's licence. No dataset is held in this repo: only fetch
scripts, checksums and a manifest recording each source's own terms.
