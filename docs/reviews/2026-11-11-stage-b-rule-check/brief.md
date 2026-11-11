# Brief for an independent reader: the first read across the real table, before any run

Written by the project session before the reader was started. Estimated cost stated beforehand: about 200,000 fresh tokens; the reader stops and reports at about 300,000 by its own estimate. The reader has had no part in the work. It is started only after the change to the finders named below is committed, and before any placebo, planted run or real read, because a flaw found after a run would cost registered seeds.

## What is to be checked

`results/stage-b-first-read.md` registers the first read that sets real series from separate data sets beside each other: country and year, 461 series in 166 places, the finders on 1961 to 1995, the referee on 1996 to 2014, and 2015 to 2024 unopened until one last reading of whatever passes. Nothing has been run. Read it, decisions 0063 and 0064 (`docs/decisions/`), `scripts/run_stage_b.py`, `src/causal_atlas/finders.py` with the commit that added `allowed` and the choice of members (`git log -3 -- src/causal_atlas/finders.py`), and as much of `src/causal_atlas/referee.py` and `scripts/run_finders.py` as the questions need. Then answer, each with the evidence:

1. **Can anything of 1996 on reach the board, or anything of 2015 on reach the board, the referee's read or the choice of rows?** Follow the values from `build` (the count rule, the transform, months made years, the departure from the year's middle) through `moved`, `plant`, `run`, `reading` and into `fd.view`, and through `confirm`. A use of later years that only decides which series and places are in the panel, or how large a planted link is, is to be named and judged apart from one that reaches a row.
2. **Are the placebos fair, and could they be easier to pass than the real read?** They should break every link between sets and keep what else the real table carries: each series' own memory, the links inside a set, the pattern of gaps, the shared shocks of a year or a region. Say what each rearrangement keeps and loses. Look for anything that makes a placebo pass less often than a real table with no true link would: fewer places where two series both have values, gaps moved with the values, the bar. Are the marks (at most 2 of 20, at most 1 of 8) ones that could fail, and what false-pass rate does holding them leave room for?
3. **Is the change to the finders what it says?** With `allowed` left out and every member run, is every board the same as before the change (a test claims so; check the diff as well as the test)? With `allowed`, is each member's lift still honest: the other alignments cut the same way as the true one, the number of terms tried the same, nothing disallowed counted or carried in through a gathered term, a component or a second-round pair?
4. **Ties between sets (decision 0064).** Does `tied` do what the registration says, and by the Bank's own description of its series (`data/raw/wdi/WDISeries.csv`, descriptions only) what ties by construction between the sets does it leave? Name the series; do not look at any values.
5. **Do the marks, the refusals, the seeds and the confirmation match the registration?** Can the real read run before both placebo marks hold, or twice? Can a placebo or planted seed be read twice or a failed run be quietly run again? Does `confirm` give each passed row one reading on 2015 to 2024 under the mark the registration states, and is that mark one a chance row would rarely meet? Does `table` count what the registration's "What counts as what" says?
6. **The planted links.** Are they sized and scored as stated, in places the referee can pass? Does a link planted on a table with places moved say what a silence on the real table would rule out, or is it easier or harder to hear there, and why?

And anything else you find that would make the read's result, a lead or a silence, mean less than the file says. Do not propose a better method: the question is whether this read, as registered, is honest and whether anything must change before the first run.

## Rules

- Run none of `run_stage_b.py places`, `years`, `planted`, `real`, `confirm`, and make nothing with a seed from 58001 on. Read no values of the real table or the panel: nothing under `data/` except the text columns of `data/raw/wdi/WDISeries.csv`, and do not load `data/panel/stage-b/panel.npz`. No number that sets one real series beside another may be computed, by you or by a script of yours.
- To try something, use made-up tables: `run_stage_b.py rehearse <kind> <seeds>` or a script of your own on worlds from `scripts/run_finders.py`, with seeds 47990 to 47999 only; list the ones you used. Seeds from 48001 on are spent or reserved.
- Write only inside `docs/reviews/2026-11-11-stage-b-rule-check/`: your report as `report.md` and any script you ran. Change no other file. Do not commit or push.
- Start every shell command with `cd` to the repo root. Python is `.venv/bin/python` with `PYTHONPATH=src`. The box is shared: `nice -n 19`, one thread (`OMP_NUM_THREADS=1`), at most two processes, and no job you wait on runs longer than about four minutes.
- The repo is public: no email address, no absolute home path, no model or tool name in anything you write.

## What to send back

`report.md`, at most two pages: for each question a verdict (holds, does not hold, could not tell), the evidence with file and line, and what would have to change before the first run. Then the same in ten lines as your final message.
