# Independent reading of the national-harvest and drought rule (commit d08fa65)

## Verdict

**The real scoring may go ahead after these changes.** None of the changes makes a pass easier. One (change 1, option b) makes a pass harder. The rest only correct what a pass or a silence is said to mean.

1. **Guard the size against shared drift, not only the pass.** In my tries, a slow shared drift in drought and yields, with no seasonal link, met every condition on the model side, beat all 62 shifted controls, and reached a size of up to 1.56%. Only the flat-driver condition stopped it. The pass is protected; the size read off the real record is not.
   - (a) Report the flat driver's S and interval beside the model's S as a headline number, not only as a pass/fail line. Neutral for a pass.
   - (b) Better: take the smaller of model S and flat S as the size that is reported and tested against 0.2%. Harder for a pass.
   - Also change "not through a shared drift" to say "not through a drift that a straight line per country and calendar month removes". That is what the code does.
2. **Say plainly that the ruler is optimistic.** In the made-up records, the drought series the detector sees is exactly the moisture that acts on yields. Real national SPEI-3 at fixed months is at best a proxy. With a proxy correlated 0.71 with the acting moisture, the 20% link was read 5 times in 8 instead of 9 in 10, and S roughly halved. The sentence "a silence would rule out only a link about that large" should say that a silence rules out a link of that size *in the index as measured*, and that a true effect that the national SPEI-3 at these six months only partly captures could be larger and still missed. Wording only, no effect on a pass.
3. **A common cause is read as a link, every time.** A shared year-to-year swing in both moisture and yields, with no drought-to-yield path, passed 4 of 4 with S 1.5% to 2.7%, and the flat control passed too. That is right for the forecasting question. The result text must still not read as "drought lowers yields". The rule hints at this; it should say it outright beside any pass: heat, ENSO-linked rain and other weather that moves with drought are not separated. Wording only.
4. **Minor rule-against-code mismatches** (detail under Findings). Correct the rule's text to match the code before the real run, so the record is exact. None changes a number.

## Findings, most serious first

### 1. Shifted controls do not protect against drift; only the flat control does

- **Where:** `src/causal_atlas/harvest.py`. Shifts in `run` (`range(2, years)`, about line 185 onward); the flat driver in `level()` (lines 205–209). Pass conditions in `reading` (233–248).
- **What I ran:** a modified copy of the generator (`panel_mod.py` in the review folder) with no seasonal link, plus a shared slow drift in moisture and yields of three shapes. Year-end, 62 shifts each.
  - Square drift ×2, seeds 23021–23028: 0 of 8 passed. In 3 of 8 the model side met every condition, with S 0.23% to 0.29% and beating all 62 shifts. Each was stopped only by the flat condition (flat S ≤ 0.02%).
  - Square drift ×3, seeds 23071–23074: 0 of 4 passed. In 2 of 4 the model side met every condition, with S 1.1% to 1.4%, beating 62. Flat S ≤ 0.
  - Hockey-stick drift ×1, seeds 23031–23038: 0 of 8, model side never fully met.
  - Hockey-stick drift ×2, seeds 23075–23078: 0 of 4; model side met in 1, with S 1.56%. Flat caught it.
  - U-shaped drift ×1 and ×2, seeds 23020 and 23041–23048: 0 of 9, model side never met.
  - Also on the counted drift panels already in `results/harvest-drought.jsonl`: the real alignment beat all 62 shifts in 4 of 20 at year-end (about 0.3 expected by chance) and 3 of 20 mid-year. Seed 22403 at year-end met every model condition except the 0.2% size (S 0.12%).
- **What it means:** a circular shift keeps a slow trend's overall level, so a shared drift lines up again in most shifts. The "beats the shifts" condition therefore gives little protection against drift. The flat driver, which removes a straight line per country and calendar month over the whole record, is the only guard, and it caught every drift I tried. Real drought looks drift-like: 80% of countries dry over the record, and the curvature left after the line (median share 0.032 of detrended yearly variance, 90th percentile 0.203) is at the level of the made-up drift panels (0.026–0.028 and 0.12–0.19), well above the no-link panels (0.007–0.010 and 0.03). So on the real record, a drift-made S can sit beside a flat S that settles the pass. The size the result reports could be drift.
- **Change:** as in verdict item 1.

### 2. The made-up records make the test easier than the real one will be

- **Driver is the acting moisture.** In `synth/harvest_panel.py` the yields respond to exactly the series given to the detector as `x`, and every linked season falls inside the detector's window (July of the year before to December of the harvest year). With a blurred driver (blur=1, correlation 0.71 with the acting moisture), link_20, seeds 23081–23088: 5 of 8 passed (against 9 of 10 counted). S was 0.15% to 0.51%. The three misses failed the interval or the size on the model side, while flat passed. Flat S was larger than model S in all eight.
- **Tails.** On real yields, 0.54% of blend errors hit the clip at 4, against 0.11% to 0.18% on made-up records. The top 5% of records carry 14% of squared error, against 10%. A heavy-tailed made-up record (t with 3 degrees of freedom, no link, seeds 23061–23066) did not fool the test, 0 of 6. So this costs power, not false links.
- **Baselines.** On made-up records (23012, 23013) the linear baseline is relatively stronger (relative error 0.97 and 1.01) than on real ones (0.986, with blend 0.889 and mean3 0.955 the best). The baseline mix differs, but the stacking re-chooses each year. I found no sign this favours a pass.
- **Driver behaviour.** Real seasonal drought is less persistent from one season to the next (lag-1 correlation 0.08, against 0.12–0.25 made-up), and its spread changes more over the record (10th percentile of late-to-early spread ratio 0.69, against 0.82–0.91).
- **Meaning:** the stated reading power (a 20% link read 9 in 10) is an upper bound. Wording change as in verdict item 2.

### 3. A shared year-to-year cause passes as a link

- **What I ran:** `panel_mod.py` with a common AR(1) swing (0.6 persistence, 0.5 SD) in both moisture and yields, no seasonal link, seeds 23051–23054.
- **What I saw:** 4 of 4 passed, S 1.5% to 2.7%, beating 62. Flat S was 2.2% to 2.9%, so flat passed as well.
- **Meaning:** a pass means "drought at these months helps forecast the harvest", not "drought causes the change". Wording as in verdict item 3.

### 4. Small mismatches between the rule's words and the code

None changes a pass. Each should be corrected in the rule's text.

- The rule says each term is clipped at 4. In `harvest.py` the per-scale forecast is clipped at line 177, but the combined term at line 181 (`term = weights @ per`) is not clipped. Weight sums were at most 0.892 on every counted panel, so the term stays near the clip. Harmless, but the text is wrong.
- "Ten known earlier years" is in the code: 9 finite consecutive changes for the scale, with trend10 needing at least 6 of 10 years and trend20 at least 8 of 20.
- "Last year's figure" falls back to mean3 when last year is missing.
- Figures flagged X (international organisations) are left out of the targets along with E. This is conservative, but the rule should say so.
- In `scripts/run_harvest.py`, `real()` (lines 85–102) writes year-end and mid-year as separate rows. A crash between the two would leave the year-end row on file and block the mid-year one. Write down what happens then.

## What I checked and found sound

- **No leak.**
  - Changing yields and flags (noise, removed values, random flags) from years 27, 33 and 45 onward (seed 23001) left every earlier year's scale, baselines, choice, weights, pick and model error identical, in every shift column and in flat.
  - Changing the driver from those years onward left earlier "as fell" years identical. Shift and flat columns change by design: the roll and the whole-record line use later drought. That is a property of the controls, not a leak into the model.
  - Same-year check (seed 23002, years 30, 44, 63): changing a year's own yield or flag leaves its scale, every baseline, the choice and the term unchanged.
  - The shifted controls go through the same `errors()` with the same pick, chosen and now as the real alignment.
- **Counted results reproduce.** I recomputed the whole step-1 table from the jsonl file, and it matches the rule:
  - link_20 year-end 9/10 (S 0.37%, 0.79%, 1.14%); mid-year 8/10.
  - link_10 3/10; link_05 0/10; few_20 2/10.
  - none 0/30; drift 0/20; step 0/20.
  - Gains: 2.26% linked, −0.66% unlinked.
  - kept: 73% of kept records are linked; kept S median 1.59% against 0.79%.
  - Mid-year misses: 22002 (interval −0.20%) and 22010 (−0.01%).
  - Re-runs from scratch of none 22301, link_20 22002 and drift 22403 at year-end matched their rows exactly.
- **Real data path.**
  - Driver starts January 1960. Years run 1961 to 2024, and index 20 is 1981.
  - Only flag A is used for targets. The country index uses `searchsorted` on sorted codes. China's total (159) is excluded.
  - The drought file ends December 2024, as asserted.
- **Real yields alone** match the rule: 503 records, 141 countries, scored count 16,763, 320 to 480 per year. Element 5412 flags are A 31,432, E 8,494 and X 1,097. Official figures equal to the previous year are 0.93% (165 in scored years).
- **Real drought alone:** 141 countries, 780 finite months; 9 countries have fewer than 5 cells.
- **`harvest.kept`:** no leak. Ranking uses only the early half, each shift ranked on its own errors; the top third is round(1/3 × able). It matches the rule.

## What I did not check

- The mid-year variant on my own modified panels (year-end only).
- How large real drought-to-yield effects are in published work, and so whether 20% is a fair target.
- FAOSTAT's revision practice, and whether flag A figures are later revised.
- Known errors in SPEIbase.
- Crop calendars by country, and whether the six fixed months fit them.
- Runtime on the real record.

## Seeds used

- New records: 23001, 23002, 23010–23013, 23020–23028, 23031–23038, 23041–23048, 23051–23054, 23061–23066, 23071–23078, 23081–23088.
- Re-runs of counted seeds: 22301 (none), 22002 (link_20), 22403 (drift), year-end.

## Files

- Everything I wrote is in `docs/reviews/2026-11-10-harvest-rule-check/` (scripts, logs, `runs.jsonl`); nothing else was changed, committed or pushed.
- That folder also holds a `__pycache__` directory; my attempt to delete it was refused. Delete it before committing the folder.
- A sweep of the folder for home paths, email addresses and model or tool names found none.
- No real yield was set beside any real drought value. `scripts/run_harvest.py real` was not run, and `results/harvest-drought.jsonl` was not written.

## Token use

About 200k fresh tokens. This is my estimate, not a count from the transcript.
