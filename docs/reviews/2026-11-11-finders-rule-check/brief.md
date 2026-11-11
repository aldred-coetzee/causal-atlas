# Brief for an independent reader: the finders' rule, before its count

Written by the project session before the reader was started. Estimated cost stated beforehand: about 150,000 fresh tokens; the reader stops and reports at about 250,000 by its own estimate. The reader has had no part in the work.

## What is to be checked

`results/finders-stage-a2.md` registers a count of 1,166 made-up worlds, committed at 70c426a, none yet run. Read it, decision 0062 (`docs/decisions/0062-the-finders-and-the-steward.md`), `src/causal_atlas/finders.py`, `scripts/run_finders.py`, and as much of `src/causal_atlas/referee.py` as the questions need. Then answer, each with the evidence:

1. **Can anything from the scored years, or anything of the planted truth, reach a row the steward sends?** The finders must see years before 35 only and nothing the generator knows. Look for a leak in `view`, in the lift, in the scan for where, in the second round, and in how the harness hands rows to the referee.
2. **Does the bar still cover what is sent?** The steward sends only rows with a lift of at least three, chosen on the early years. The referee's bar is the largest chance departure among the rows sent. Is there a way the choosing on early years makes a chance row likelier to pass on the scored years than the bar allows (the outcome's own slow movement, a series' memory across year 35, the same places chosen by a scan and then scored)? If you can show it on a made-up world, do; if you can only argue it, say so.
3. **Do the marks as written match what `table()` in `scripts/run_finders.py` computes,** and is each mark something that could fail? Say which wording and which code line disagree, if any. Is any pass that should count as false counted as a copy, a part or a path instead?

And anything else you find that would make the count's result mean less than the file says. Do not propose improvements to the finders: the question is whether this count, as registered, is honest.

## Rules

- Do not run `scripts/run_finders.py count` and do not make any world with a seed from 48001 on: those are the counted seeds. For worlds of your own use seeds 47900 to 47999 only, through `run_finders.py smoke` or your own script, and list the ones you used.
- Write only inside `docs/reviews/2026-11-11-finders-rule-check/`: your report as `report.md` and any script you ran. Change no other file. Do not commit or push. Read no real data: nothing under `data/`.
- Start every shell command with `cd` to the repo root. Python is `.venv/bin/python` with `PYTHONPATH=src`. The box is shared: `nice -n 19`, one thread (`OMP_NUM_THREADS=1`), at most two processes, and no job you wait on runs longer than about four minutes (a world at 120 places takes 5 to 20 seconds, at 480 places up to two minutes).
- The repo is public: no email address, no absolute home path, no model or tool name in anything you write.

## What to send back

`report.md`, one page: for each question a verdict (holds, does not hold, could not tell), the evidence, and what would have to change in the registration before the count. Then the same in ten lines as your final message.
