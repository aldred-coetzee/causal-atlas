# Brief: an independent reader of the first real monthly read's rule and code, before any run

Written by the project session before the reader is started (rule 7). One reader, a top model, no part in the work. Estimated cost: about 150k fresh tokens; counted from transcripts and reported beside the result.

## What it serves

`results/stage-d-monthly-read.md` is the rule for the first read of real monthly series from separate data sets beside each other. Its real read is made once and cannot be made again. The reader looks for faults in the rule and in `scripts/run_stage_d.py` before the first placebo run.

## Read

- `results/stage-d-monthly-read.md`, `docs/decisions/0069-the-first-real-monthly-read.md`
- `scripts/run_stage_d.py`, `tests/test_stage_d.py`
- as far as needed: `src/causal_atlas/months.py`, `src/causal_atlas/referee.py`, `src/causal_atlas/finders.py`, `results/monthly-lead-count.md`, `docs/tied-series.md`, `results/spent-ledger.md`, and the last reader's report `docs/reviews/2026-11-12-stage-c-rule-check/report.md`

## Questions

1. Can anything of 2020 to 2024 reach the finders or the referee in a placebo, a planted run or the real read? Check the code (`build`, `moved`, `plant`, `run`, the season step in `months.py`), not the rule's word. Note that the month's middle and the season step are computed where: does either carry later months back?
2. Do the two rearrangements break every link between sets, including a link from a common series to places and a month-wide part carried by the month's middle? Is moving by whole years within the months before 2020 sound for the referee's draw of whole years?
3. Is a planted link what the rule says (share of month-to-month movement, lag, places), on series that are mostly nought as well? Does the hearing test (`hit` in `run`) count the right thing?
4. The nought-filling of the conflict record from 1989, and the builder's order (fill, table values, transform, counts, middle): any fault? Any way a place or series is kept or dropped other than the rule says?
5. Sets: is there a tie in `docs/tied-series.md` between two monthly series that this rule puts in different sets? Is "a lead on drought, storms or earthquakes is false" sound for every allowed input?
6. The guards: the real read twice, a seed twice, an unregistered seed, the real read before the marks hold, `confirm` sending the same row with January 2020 as the first scored month.
7. Leaving out two members the counted read had: does anything in the rule claim more than the planted runs can support?
8. Does the rule say anything more firmly than what stands behind it? Anything else that would make the real read unsafe to make once.

## Bounds

- **Nothing is run on the real table and no real value is read.** Not `data/panel/`, `data/table/`, `data/raw/`, and no run of `run_stage_d.py` with any step (`panel`, `rehearse` included: `rehearse` loads the real panel for its shape).
- Made-up arrays and the tests may be run: `PYTHONPATH=src OMP_NUM_THREADS=1 nice -n 19 .venv/bin/python -m pytest -q -W ignore tests/test_stage_d.py`. Any seed used is 59001 to 59999 smoke only and listed. **Every Python run is started under `ulimit -v 4000000`**: a wide table can take many gigabytes and the box is shared.
- No file is edited but the report and, if needed, a check script beside it. No commit, no push. No web.
- No job is waited on for longer than four minutes.

## Back

`docs/reviews/2026-11-12-stage-d-rule-check/report.md`: at most one page. For each question: the finding, where in the code or rule, how sure, and what to change. Faults that must be fixed before any run first; then what the rule overstates; then what was checked and found sound. What was not checked is said. If the write is refused, return the report's text as the answer.
