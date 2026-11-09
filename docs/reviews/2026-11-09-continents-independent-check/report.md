# Independent check of the forecast result on four continents, 2026-11-09

The report of one fresh reader with no part in the work, asked to break "Results, step 2" of `results/real-enso-continents.md` as it stood at commit ed95c77. It is the reader's text, unedited, except that 1 absolute path(s) to the reader's scratch folder and 1 to the project's checkout are replaced by paths in this repo. The reader had no web access.

Beside it, as the reader left them: `reimpl.py` (its own implementation from the rule text), `pool.py` (pooling, shifts and intervals), `leak.py` (compares a clean fit with one where every value from 2000-01 is noise) and `noise.out` (that run's printed output). In each script one line, the path of the folder its outputs are written to and read from, is changed to the script's own folder; nothing else. To rerun, from `scripts/`: `PYTHONPATH=../src uv run python ../docs/reviews/2026-11-09-continents-independent-check/reimpl.py`, then the same with a second argument for the noise run (see the script), then `pool.py` and `leak.py`. The two JSON files they write are outputs and are not committed.

What was done with it: `results/real-enso-continents.md`, "Independent check". Cost: 131,314 fresh tokens by the counter.

---

Independent review of "Results, step 2" in results/real-enso-continents.md

1. RE-IMPLEMENTATION
- My script, written from the rule text with plain loops: docs/reviews/2026-11-09-continents-independent-check/reimpl.py. Pooling, shifts and bootstrap are in pool.py in the same folder. From the repo it uses only field.box, field.oni and links.tiles. Correlations, the Benjamini-Hochberg step, baselines, folds, slopes, k, shifts and scoring are all my own code.
- My numbers match the rows exactly, field by field:
  - South America: S +0.1610, model error 4991.01, linear baseline, k 0.764, 353 claims.
  - Australia: +0.1286, 1807.76, linear, k 0.467, 113 claims.
  - South and Southeast Asia: +0.2242, 2874.10, linear, k 0.772, 260 claims.
  - North America: +0.1172, 770.59, linear, k 0.675, 57 claims.
  - Europe: zero baseline, 0 claims.
- Also identical: the fold errors for all three baselines, the lag counts, and each baseline's error on its own (for example South America: zero 6952.12, level 6924.2, linear 5949.0).
- Pooled: S +0.17122. Interval +0.1199 to +0.2196 with seed 0; seeds 1 to 3 give +0.119 to +0.223. Shifted controls run from -0.2766 to -0.0374, and the real score beats all 24.
- The repo's helpers do what the rule says. links.correlations matches a plain np.corrcoef on every entry (largest difference 7e-16). links.significant is Benjamini-Hochberg at 5% over every unit, month and lag. links.tiles gives 10-degree squares, stepped 5 degrees, with at least 40 cells.

2. LEAKS
- (a) Baseline prediction for month t uses only months up to t-3.
  - In the code: own values at t-3, t-4, t-5, t-6 and t-12; the mean of all units at t-3; trailing means over months t-14..t-3 and t-62..t-3.
  - Tested on the repo's own baseline(): raising every value from t-2 onward by 5 changed nothing for any baseline at t = 603, 700 and 899. Changing t-3 did change the level and linear predictions.
- (b) and (c): the linear fit, and the choice of baseline, use months 12 to 599 only. Each of the five blocks of years is predicted from a fit on the others.
- (d) Claims, lags, slopes and k use the discovery years 1951 to 1999 only. The latest driver value they read is month 595.
- (e) The ONI file (PSL oni.data) is laid out year by month. The value in the January column is the December-January-February mean (for example 1998 January = 2.22), so the value at index m is the mean of months m-1, m and m+1.
  - At lag 4, the predictor for target month t therefore holds real-world data from months t-5 to t-3.
  - SPEI-3 at t covers months t-2 to t. There is no overlap, even at the most common lag (494 of the 783 claims are at lag 4).
- Noise test: I replaced every SPEI cell value and every ONI value from 2000-01 onward with noise and refitted, both in my code and in the repo's forecast.fit. Everything fitted stayed identical in all four fields: the chosen baseline, the fold errors, the coefficients, k, the lags, the claim mask, the slopes and the discovery residuals.
- Shifted controls: the shift is circular over whole years within 2000 to 2024, and shift 0 is the real score.
- Two things are not strictly out of time:
  - The disclosed one: the SPEI is standardised over its whole record.
  - One not disclosed: CPC's ONI uses centred 30-year base periods and is the 2026 ERSST v6 version, so values from the discovery years carry some later sea-surface data. This is from my own knowledge of how CPC computes the ONI; I did not check it at source (no web). Like the SPEI scaling, it cannot tell the model which way a given month went.

3. ORDER OF EVENTS
- The rule and all the code (forecast.py, run_continents.py, the field.py boxes, the tests) were committed together in 4c25ec2 at 22:26:10.
- The naming rows were committed at 22:41:54 (f48ee26), and the confirmation rows plus the step 2 text at 22:45:44 (ed95c77).
- No commit after 4c25ec2 touches src/, scripts/ or tests/. links.py, confirm.py and run_enso.py were last changed at 21:53 or earlier.
- The 305 naming rows in the current jsonl are byte-identical to f48ee26. The 12 scoring rows were appended once, and the file was last modified at 22:43.
- The script refuses a second scoring only if confirmation or pooled rows are already in the jsonl. That is a guard, not a lock: deleting rows, or calling forecast.* directly, gets round it.
- What git cannot show:
  - That nothing was run without being recorded.
  - That the naming began after the rule commit. The text says about 35 minutes of machine time, but only 15.5 minutes separate the rule commit and the naming commit. That fits the five fields running in parallel, but git cannot settle it.
  - The cached data files for the five boxes were built at 22:16, ten minutes before the rule. That fits the "shapes only" counts the rule reports.

4. TEXT AGAINST ROWS
- Checked and correct:
  - The pooled S, interval and shifted range, and the three "below each baseline" figures (17%, 26%, 27%).
  - Every value in the per-field table: S, intervals, shifted ranges, claims of 1,140 / 588 / 1,200 / 1,260 / 768, k and baseline.
  - The single-cell pooled and per-field figures, and Europe's 56,520 cell-months with no claim.
  - 494 of 783 claims at lag 4; 19% claimed and 81% not; how good each baseline is against zero (0.104, 0.025, 0.031, 0.043).
  - 22 of 25 years better. The worse years are 2001, 2013 and 2014, at -4.8%, -3.8% and -1.2%. The top years are 2015 +0.39, 2011 +0.35, 2010 and 2022 +0.32.
- One mismatch: "no year carries more than 7% of the error being explained" is wrong. 2015 carries 13.3% of the reduction in error and 2010 carries 11.2%. The 7% matches each year's largest share of the baseline's error (6.6%), not of the error explained.
- The point it supports still holds. A new analysis, not a check: dropping 2015 gives S +0.158; dropping 2015-16 and 2010-11 together gives +0.124 or more.
- Not in the rows, so not checkable: "on all region-months the gain is much smaller". It is true by construction, since unclaimed months get no ONI term.

5. OTHER POINTS
- Few El Niño events. The year bootstrap treats calendar years as independent, but an event spans two years.
  - New analysis: a bootstrap that draws 3-year blocks gives +0.112 to +0.219, close to the reported interval.
  - Dropping the three largest El Niño pairs (2010-11, 2015-16, 2023-24) leaves S +0.124. The lower end does not rest on one event.
- The shifted control adds little beyond S > 0. A slope fed the wrong years only adds error, so every shifted value comes out negative, as expected. Beating all 24 says little once the interval is above 0.
- "Below each baseline alone" is computed on the same claimed region-months, the same years and the same fit for all three baselines. It holds.
- Overlapping regions: a cell counts in up to four units, so the 783 claims are not independent. The bootstrap draws whole years across all units, so the interval is not made narrower by this. Overlap only re-weights the central cells.
- A route from 2000 to 2024 into the design: the forecast step (how k is chosen, the three baselines, region units) was tuned on Africa's 2000 to 2024. Those years share the same El Niño time series as the new fields. The design was therefore shaped by these years' events, though not by these places, and Africa itself scored only +0.033 under it. The file's "new places, not new years" names this, but it does not say the design's tuning saw these same events.
- The boxes were drawn knowing where El Niño acts (disclosed). Entry is decided only by naming on the discovery years, and North America entered on that rule, not by choice.

VERDICT: holds with these corrections.
- (1) Replace the "no year carries more than 7% of the error being explained" sentence. 2015 carries 13%, and S is still +0.158 without it.
- (2) Add to the limits that the ONI, like the SPEI, is not strictly out of time: centred base periods and the 2026 version of ERSST v6.
- (3) Optionally note that the forecast design was tuned on the same 2000 to 2024 El Niño events, though in Africa, and that the shifted control mostly repeats S > 0.

Could not check: that nothing was run without being recorded, or that naming started after the rule commit; CPC's and SPEI's standardisation at source (no web).
