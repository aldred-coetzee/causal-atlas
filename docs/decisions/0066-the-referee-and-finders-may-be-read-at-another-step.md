# 0066: The referee and the finders may be held to settings in another step than a year, off unless asked for

Status: accepted, 2026-11-11. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

Every count so far reads a table by year. Many of the sources are monthly, and notes on made-up monthly tables (`docs/reading/reading-by-month.md`) found that the method reads them without false passes only when the season is taken out first and the referee's settings are counted in months. A linked monthly table also took about 5 GB, because the referee kept, for every scored step of every outcome, a places-by-steps array. A helper wrote the change in a separate working copy (brief: `docs/specs/2026-11-11-parallel-helpers-sixth-wave.md`). The rule of this project is that the counted path of the referee and of the finders is never changed.

## Decision

The change is taken into the package. What it adds to the two counted files:

1. `referee.using(settings, level)`: the referee's settings changed for the length of a block and put back after it. With nothing given, nothing changes.
2. `referee.LAZY`, off by default: an outcome's errors at each scored step made again when asked for, by the same arithmetic, in place of being kept.
3. `referee.judge` and `referee.label` take `draw`, `settings` and `level_fn`, each `None` by default; `finders.view` takes `settings` and `quiet`, each `None` by default, and `finders.swarm` runs under the view's settings.

The monthly read itself (season step, month members, month settings, whole years drawn together) is a new file, `months.py`, and has been counted on nothing. A count of it is registered on its own, rule first, on seeds no run has used; the draft in `docs/drafts/` is a draft.

## Checked before taking it in

- The diff to the two counted files read line by line by this session: every new argument and setting defaults to the path as counted.
- The whole suite run by this session on the branch: 293 passed, 1 skipped.
- Stored made-up tables read again under the new code and compared with their stored rows (board, first round, answers told, ranks, rows posted): the helper reports the first seed of each of the 66 registered panels the same; this session chose five others itself (the last seed of a sign that turns, a shared cycle, a hidden link at 240 places, gaps with nothing to predict, a steady link at 480 places) and all five are the same. These are checks of spent seeds against their stored rows, not counts.

## Could it favour a result

Not a yearly one: with nothing asked for, the code that runs is the code that was counted, and the checks above say the numbers are the same. A monthly read is a new thing with settings of its own, and anything it finds has to be earned by its own registered count before it is used on the real table.

## Limits

- `using` changes the module's settings in place for the length of a block. Two reads with different settings must not run in one process at the same time. Runs here are one process a table.
- `LAZY` trades memory for time; how much time has not been measured beyond the helper's development runs.
- The helper's memory figure (about 0.5 GB where it was about 5 GB) is its report and was not measured again by this session.
