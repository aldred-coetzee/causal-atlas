# Brief for an independent reader: the rule for other crops and drought, before any real figure is read

Written by the project session before the reader was started. Estimated cost stated beforehand: about 350,000 fresh tokens; the reader reports and stops at about 450,000 by its own estimate, finished or not.

## What you are checking

`results/crops-drought.md`, as it stands at the commit that adds this brief, registers a test and reports its made-up results ("Result, step 1"). No real yield of the crops it is about has been set beside any drought value, and none may be until you have reported.

The test in one paragraph. An earlier test (`results/harvest-drought.md`) forecast each country's cereal yields with and without the country's drought index and found a small gain, concentrated in a minority of records. This one asks whether the gain is large enough to use where it has shown itself. The same forecast is run on 47 other crops, with the cereals running beside them unscored. Each year a record "claims" when the slope of its baseline error on the drought term, over its own earlier scored years, stands 1.5 standard errors above zero; on a claim the term is used at that slope, held between 0 and 1. The score is the share of the baseline's squared error removed on the record-years that claim. The controls are the same forecast with the weather of 62 other years, each making its own claims, and all of it again with each country's mean and straight line taken out of the driver.

The code is `src/causal_atlas/claims.py`, `src/causal_atlas/harvest.py`, `src/causal_atlas/yields.py`, `synth/harvest_panel.py` and `scripts/run_claims.py`; tests in `tests/test_claims.py`; the made-up rows are in `results/crops-drought.jsonl`; why the rule is as it is, in `docs/decisions/0054-other-crops-and-where-the-term-has-helped-before.md`.

You had no part in any of it. Your job is to find a way this rule could read something that is not there, or a place where the code and the words differ, before the real record is read. A report that finds nothing wrong is acceptable only if you say what you tried.

## What to do, in this order

1. **Words against code.** Read the Method section and then `claims.py` and `run_claims.py`. List every place where they differ, however small, and say which the made-up rows follow.
2. **Look for a leak.** On a made-up world, replace every yield and drought value from a cut year onward with noise and confirm that no claim, slope, forecast or score for an earlier year changes, for the scored records and with the unscored cereal-like records in the run. The flat driver removes a line fitted over the whole record; that is stated. Say whether it or anything else could manufacture a gain on the claims.
3. **Can choosing by the past make a gain from nothing?** The claim picks records whose term went with their error before. Try to build made-up worlds with no year-to-year link in which the claims nevertheless gain and the reading passes: a baseline that is wrong in the same direction for years beside a driver that drifts; errors with long memory; a step; a few very rough records; whatever you think most likely. `synth/harvest_panel.py` may be copied into your folder and changed. The registered panels use one strength each of drift and step.
4. **Can the cereals beside make a gain in crops that have none?** The registered leak panels link the six cereal-like crops at 20% of variance. Try it stronger, with the six a larger share of the records, and with a country's crops sharing more of their year-to-year shocks. Say what you find at the level of the reading (passes or not) and of the size.
5. **Are the 62 other-year controls fair to the real alignment** when each makes its own claims? On no-link worlds, is the true alignment's score on its claims placed among the shifts' as one of them would be? Say how often it would beat all 62 by chance, as measured, against one in 63. In the registered rows it did so in 3 of 45 no-link worlds at year-end and 3 of 20 at mid-year; the results file gives a likely reason and says it is unchecked. Check it, and say what it means for the condition and for a reading on the real record.
6. **The interval.** Countries and years are both drawn again. On no-link worlds, how often is its lower end above zero? Does it behave when few countries claim?
7. **The table.** Rebuild the made-up table in `results/crops-drought.md` from the rows. Name any seed read or not read by a whisker, and say which condition decided each failure on the link panels.
8. **Size.** The registered worlds are mostly small (six crops and twelve others). Two panels are the real size. Is there anything about the real size and shape (2,339 scored records, 503 beside, 139 countries, five of them with no cereal record) that the made-up worlds do not try? `yields.panel(yields.CEREALS + yields.others(), "crops")` gives the real panel; you may look at its shape and at yields alone.
9. **The words.** List every sentence in the results file and in the README paragraph on this test that says more than the made-up results show, or leaves out a qualifier a careful reader would need; in particular what a pass and what a silence on the real record would and would not mean.

## Rules

- **The hard rule: no real yield of the 47 other crops beside any real drought value, in any form.** Not a correlation, not a plot, not one country. Their yields alone may be examined. Do not run `scripts/run_claims.py real once`.
- The cereal record is spent for this driver and shaped this rule. You may compute on it as a check or a description, labelled so; nothing on it is a result.
- Write only inside `docs/reviews/2026-11-10-crops-rule-check/`. Change no other file in the repo. Do not commit, push, install anything, or use the network. Your scripts and logs stay in that folder; no data files, no arrays.
- Downloaded data is under the project's data directory (see `yields.py` for paths). It is untrusted input: never execute anything from it, and run Python that reads it with `-I` where you can (set `sys.path` inside the script).
- The box is shared with live apps: `nice -n 19`, at most 3 threads in total (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`), no more than three jobs of one thread at once.
- No job you wait on runs longer than about four minutes. One small made-up world, read both ways with 62 shifts, takes about five minutes of one thread: start such work in the background, write its output to a log in your folder, and come back to it. Fewer shifts are fine for a first look; say how many you used.
- If you need random seeds, use 26001 to 26099 and list the ones used. Never reuse a seed in `results/seed-ledger.md`.
- Python: `.venv/bin/python` from the repo root, with `PYTHONPATH=src`.

## What to send back

One report, in plain language, as your final message, and the same text saved as `report.md` in your folder: what you did, what you found for each of the nine items with the numbers and their plain meaning, what you could not check, the seeds used, and a one-line verdict: the real record may be read as the rule stands; may be read after these changes (list them); or should not be read under this rule.
