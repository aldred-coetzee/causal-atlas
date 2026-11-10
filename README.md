# causal-atlas

A spatiotemporal observatory, at an early stage. The aim is to bring event and
indicator data from different domains (conflict, climate, food, prices and
others) onto one grid of place and month, find time-lagged relationships between
domains, and use them to predict trends.

The owner's aim, refined on 2026-11-05, is broader than any one link: from many
factors, not known in advance, find combinations that help to predict or infer a
direction, including combinations nobody would have thought of. How to do that is
still an open question. His words are in
`docs/decisions/0021-owner-refines-the-aim.md`. The first experiment below tests
the narrower question.

**Where it stands (2026-11-10).** Nothing new about the world has been found.
What has been shown is that the chain works end to end on a link that is already
known. Among 31 decoys, the search named El Niño blind as a driver of drought on
four continents and stayed silent in Europe. A forecast built from that, fitted
on 1950 to 1999 and scored once on 2000 to 2024, had about a sixth less error
(17%, between 12% and 22%) than a forecast from each region's own history, on the
region-months where it made a claim. Each of the four passes by itself, North
America narrowly (its own interval starts just above zero). A side check
afterwards, which is not a test, measured El Niño on a fixed base instead of
NOAA's moving one: the four together still pass, at 13% to 14%, and North America
by itself does not. An earlier attempt on
Africa missed and is published as a miss. The result, its limits, an independent
check and an audit are in `results/real-enso-continents.md`; the independent
reader's report and code are in `docs/reviews/`.

This is a climate-to-climate link. No claim about conflict, or about any link
between domains, follows from it, and the question below is still open. One limit
touches every number here: the drought file used carries an error its makers have
acknowledged (small, they say, and largest in dry regions), and a corrected file
is not yet out.

From that tested model there is a dated outlook for November 2026 to September
2027, with the rule for scoring it fixed in advance: `results/outlook-2026-27.md`.
It is a test of the method that can fail in public, not a warning service.

The step after that handed the search 25 more real climate series at once, chosen
by a rule and not by hand. The first attempt stopped at its own check: among that
many real candidates the search could no longer reliably hear a link planted on
purpose, and nothing was scored (`results/real-indices.md`). The cause was a defect
in the search's controls. With it corrected, and the same pass marks on fresh
seeds, the search passed every check and named 16 series-and-region pairs beyond
El Niño. Scored once on 2000 to 2024, none of them improves the forecast four or
more months ahead once each region's own history and El Niño are in it
(`results/real-indices-2.md`). So among these climate series El Niño is the only
usable lead found, and the search can now be trusted with many real candidates,
for large links only.

The step now under way is the first outside climate: burned area from satellites,
1982 to 2018, with a link others have published (El Niño leading fire) to
rediscover first. Its rule is committed (`results/fire-enso.md`); nothing has been
run on it yet.

`STATUS.md` says where things stand in more detail.

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
- `docs/data-sources.md`: every source checked, how to get it and what its
  licence requires.
- `docs/plan-phase-1.md`: the first design, on synthetic data.
- `docs/decisions/`: decision records, immutable once written.
- `docs/reviews/`: reports of independent checks, as written, with their code.
- `results/`: one file per experiment, its rule committed before its numbers.
- `data/manifest.toml`: versions and checksums. `scripts/`: fetch scripts.

## Licence

Code is MIT (`LICENSE`). Text is CC BY 4.0 (`LICENSE-CC-BY-4.0`). Third-party
material keeps its owner's licence. No dataset is held in this repo: only fetch
scripts, checksums and a manifest recording each source's own terms.

Burned-area data: this project acknowledges the ESA Climate Change Initiative and
the Fire CCI project. Chuvieco, E.; Pettinari, M.L.; Otón, G. (2020): ESA Fire
Climate Change Initiative (Fire_cci): AVHRR-LTDR Fire_cci Burned Area Grid
product, version 1.1. Centre for Environmental Data Analysis.
doi:10.5285/62866635ab074e07b93f17fbf87a2c1a. Every source's terms and citation
are in `docs/data-sources.md`.
