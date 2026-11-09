# 0043: Many real series at once, and what each adds beyond El Niño

Status: accepted, 2026-11-09. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The chain (finder, map, predictor) passed once on a link that is already known: El Niño to drought on four continents (`results/real-enso-continents.md`). In that test the author chose the one real candidate. The owner's aim is the opposite: "find relationships without hypothesiseing", from many data sets.

The coordinating session audited that result (its second and last audit; its report is kept outside this repo). Its reading of the gate was to extend: a further driver whose answer is not known, registered the same way, with the ruler run on the new fields. It set five conditions on the first result's records and asked that they be closed in one commit before the forecast step here runs.

## Decision

1. The next test gives the search many real series at once, chosen by a rule and not by the author. The list is every series on NOAA PSL's page of monthly time series. A file is in when it is complete for 1950 to 2024, is not rainfall, is not El Niño by another name (correlation with the ONI below 0.6 at every lag within a year), is not mostly a trend (a straight line explains less than 0.25 of its variance), and is not a series already kept (correlation below 0.9). Twenty-five are in. The rule, its measurements and how it was arrived at are in `results/real-indices.md`; the code is `scripts/index_candidates.py`.
2. The instrument check and the ruler are run again on each of the five fields with the new candidate set (26 real, 18 decoys), because more candidates raise the bar and the earlier ruler was measured on Africa with 32.
3. A named series must add to the forecast **beyond own history and the El Niño model as tested**, on 2000 to 2024, scored once. The interval is widened for the number of pairs named.
4. The search and the forecast step are the frozen ones. What changes is stated in the rule before any number: 44 candidates in place of 32, the cap of five leads per gate lifted to the number of real candidates, and a second forecast stage fitted to what the first leaves (`forecast.residual`, `forecast.after`).
5. All 96 files on the page are fetched together. Decision 0040's reading said "one at a time, each named with its reason". The reason here is one reason for all of them: the test is about not choosing, and a rule can only be applied to the whole list. Each of the 25 kept has its own manifest entry and checksum; the others are read only to apply the rule. This is this session's reading and the owner's to correct.
6. Africa stays out: its years after 1999 are spent, the forecast step was shaped on them, and its forecast missed. Europe stays in: El Niño made no claim there, so anything named there stands on its own.
7. The audit's five conditions are closed in a separate commit that names the audit, before `scripts/run_indices.py confirm once` is run. The rule, the instrument check and the naming do not wait for that; the scoring does.

## What is and is not untouched

The five fields' years after 1999 have been scored once for the ONI. Their drought values have therefore been read by the scoring code, and the author knows the baseline's and the El Niño model's error by year. No series other than the ONI has been set against any drought value in any year. The forecast step was fixed before these fields were read and is not changed by what was seen. This is weaker than fields never read and is said beside the result.

## Consequences

- `data/manifest.toml`, `docs/data-sources.md` and `results/seed-ledger.md` carry the new entries. One kept series, the sunspot number, is under a non-commercial licence (CC BY-NC 4.0); the others are public domain, open licences, or carry no stated licence and a request for credit. None is redistributed.
- Whatever comes out is about climate series and drought. No claim about conflict, prices or any link between domains follows from it, and the project's own question stays open. That sentence goes wherever the result is summarised.
- After step 2 these fields' later years are spent for these series as well. A further test of the same kind needs outcome fields or years not yet read.
