# Brief: an independent reader of the second real read's rule and code, before any run

Written by the project session before the reader is started (rule 7). One reader, a top model, no part in the work. Estimated cost: about 150k fresh tokens; reported from transcripts beside the result.

## What it serves

`results/stage-c-second-read.md` is the rule for reading the real yearly panel a second time, every series as its change from the year before. Its real read is made once and cannot be made again. The reader looks for faults in the rule and in `scripts/run_stage_c.py` before the first placebo run.

## Read

- `results/stage-c-second-read.md`, `docs/decisions/0067-a-second-real-read-as-changes.md`
- `scripts/run_stage_c.py`, `tests/test_stage_c.py`
- `scripts/run_stage_b.py` (what it wraps), and as far as needed `results/stage-b-first-read.md`, `results/change-count.md`, `docs/reading/series-that-keep-their-level.md`, `src/causal_atlas/referee.py`, `src/causal_atlas/finders.py`

## Questions

1. Can anything of 2015 to 2024 reach the finders or the referee in a placebo, a planted run or the real read? Check the code, not the rule's word.
2. Do the two rearrangements still break every link between sets on the changed table? Is the order (reorder places, plant in levels, change, move the common series; or change, then move years) sound, and is a planted link after it what the rule says it is?
3. The runner points the first read's bookkeeping at its own file, seeds and marks by setting names in that module. Can any path write to the first read's file, read its rows as this read's, or get round a once-guard (the real read twice, a seed twice, an unregistered seed, the real read before the marks hold)?
4. Is `confirm once` right: the same row, the changed table, 2015 as the first scored year, the first read's rule for confirmed?
5. Does a tie arise or matter differently when series are read as changes, among the series this panel holds? Answer from the sources' own descriptions and the rule's list, not from values.
6. Does the rule say anything more firmly than what stands behind it? In particular what a pass, a confirmed pass and a silence would each be worth after two reads of the same years.
7. Anything else that would make the real read unsafe to make once.

## Bounds

- **Nothing is run on the real table and no real value is read.** Not `data/panel/`, `data/table/`, `data/raw/`, and not any run of `run_stage_c.py` or `run_stage_b.py` with a step. `results/*.jsonl` of the first read may be read (published).
- Made-up arrays and the tests may be run: `PYTHONPATH=src OMP_NUM_THREADS=1 nice -n 19 .venv/bin/python -m pytest -q -W ignore tests/test_stage_c.py`. Any seed used is 59001 to 59999 smoke only and listed.
- No file is edited but the report and, if needed, a check script beside it. No commit, no push. No web.
- No job is waited on for longer than four minutes.

## Back

`docs/reviews/2026-11-12-stage-c-rule-check/report.md`: at most one page. For each question: the finding, where in the code or rule, how sure, and what to change. Faults that must be fixed before any run first; then what the rule overstates; then what was checked and found sound. What was not checked is said.
