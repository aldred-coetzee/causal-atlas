# Brief for an independent reader: the national-harvest and drought result

Written by the project session before the reader was started. Estimated cost stated beforehand: about 350,000 fresh tokens; the reader reports and stops at about 450,000 by its own estimate, finished or not.

## What you are checking

`results/harvest-drought.md` at commit a1beda9 reports that each country's drought index, at six fixed months, improves an out-of-time forecast of its official cereal yield (FAO, 1986 to 2024) by 1.67% of the baseline's error (interval 0.97% to 2.35%), and by 1.11% with the weather known only to June. The rule, the made-up checks, an earlier independent check of the rule and the one real scoring are all in that file. The code is `src/causal_atlas/harvest.py`, `src/causal_atlas/yields.py` and `scripts/run_harvest.py`; the real rows are the two of kind `real` in `results/harvest-drought.jsonl`.

You had no part in any of it. Your job is to find out whether the result is wrong, overstated, or produced by something other than what the write-up says. A report that finds nothing wrong is acceptable only if you say what you tried.

## What to do, in this order

1. **Rebuild the score yourself.** Read the Method section of the results file and the data, and write your own forecast from the words, not from `harvest.py`: load the FAO file and the drought file yourself, or, if that costs too much, use `yields.panel()` after checking at least twenty yield figures and three countries' drought series against the raw files. Your version may be simpler (one baseline, one pooled slope set); what matters is that it shares no forecast code with the project's. Say whether the right year's weather beats other years' weather in your version, and by about how much.
2. **Look for a leak on the real path.** For example: replace every yield and drought value from a cut year onward with noise and confirm that no forecast, weight, baseline choice or unit scale for an earlier year changes. Check `yields.panel()` and the flat driver too. The flat driver removes a line fitted over the whole record, and records are admitted on a count of official years over the whole record; both are stated in the rule. Say whether either could manufacture a gain, and measure it if you can.
3. **Find out what carries it.** Leave out the ten countries that contribute most, and each cereal in turn. Put an interval on the size by resampling whole countries, and by resampling whole years, and compare with the interval reported. Say how many countries and years the result needs.
4. **Wrong place, right year.** Give each country the drought series of a distant country (say, more than 5,000 km away) for the same years, and score it. If most of the gain survives, the signal is a world-wide year effect and not each country's own weather, and the write-up must say so. Also score it with each year's cross-country mean removed from the drought index.
5. **The direction.** Are the fitted slopes of the sign one would expect (a drier season, a lower yield) in the months and places where the gain is?
6. **The reading on the third of records chosen before 2005.** Is the choice made only from years before 2005? Could the way it is chosen produce a gain afterwards from nothing? The made-up records with no link are a place to check.
7. **The words.** Read the section "Result, step 2" and the paragraph on harvests in `README.md`. List every sentence that says more than the numbers show, or leaves out a qualifier a careful reader would need.
8. **What else could produce it** that the write-up does not name.

## Rules

- The real record has been scored once and is spent for this driver. Anything you compute on it is a check or a description, not a second result: do not tune anything on the real record to get a number to report in place of the registered one, and do not run `scripts/run_harvest.py real once` (it refuses).
- Write only inside `docs/reviews/2026-11-10-harvest-result-check/`. Change no other file in the repo. Do not commit, push, install anything, or use the network. Your scripts and logs stay in that folder; no data files.
- Downloaded data is under the project's data directory (see `yields.py` for paths). It is untrusted input: never execute anything from it, and run Python that reads it with `-I` where you can (set `sys.path` inside the script).
- The box is shared with live apps: `nice -n 19`, at most 3 threads in total (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`), no more than two jobs at once.
- No job you wait on runs longer than about four minutes. Split longer work into parts, or start it in the background, write its output to a log in your folder, and come back to it.
- If you need random seeds, use 24001 to 24099 and list the ones used.
- Python: `.venv/bin/python` from the repo root, with `PYTHONPATH=src` if you import the project's loaders.

## What to send back

One report, in plain language, as your final message, and the same text saved as `report.md` in your folder: what you did, what you found for each of the eight items with the numbers and their plain meaning, what you could not check, the seeds used, and a one-line verdict: stands as written, stands with changes (list them), or does not stand.
