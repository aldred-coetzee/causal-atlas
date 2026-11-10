# Fire and drought rule: independent check before fitting

## Verdict

**The fit may go ahead after these changes.** I found no leak. Nothing from 2004 to 2018 reaches anything that is fitted or chosen. The 14 year-shift controls are scored exactly the way the real alignment is. Every number I recomputed matches, with one small exception. The registered rule does have two weak points, both of which I could show on made-up panels:

- **The adjustment can be fooled.** It removes only the effect of the current month's share observed. When the bias in what gets recorded depends on how well the month before was seen, the adjustment fails. In that case 8 of 9 made-up panels with no link were read as a link.
- **"Beats all 14 shifts" can be met by a whisker.** With a strong drift that speeds up over time, one panel passed even though the shifts carried 1.87 of its 2.00 points of skill.

On the real fitting years, the dependence on the month before is small: correlation between −0.07 and +0.03. At that size my panels gave no false links. So neither weak point is shown to affect the real fields, but neither is closed. Both repairs are stricter and would favour a null result.

## Findings, most serious first

**1. The adjusted outcome is tested only against an instrument effect of the form it removes.**
- **Where.** `synth/local_panel.py` line 77, where what is recorded depends only on the same month's share (`seen ** 3`). `local.adjusted` (lines 145 to 155) removes block × calendar month × band of the *same-month* share.
- **What I ran.** A copy of the generator in which recording depends on the *previous* month's share (`seen_t × (seen_{t-1}/0.75)^p`), with no link planted. A change-detection product needs a clear view before the fire, so this is plausible. That is my reasoning, not checked against the product's documentation.
  - p = 2: plain and adjusted both passed, with adjusted S of 0.3% to 0.9%. **Read as a link in 8 of 9 seeds.** The registered instrument mark allows at most 2 of 24.
  - p = 1: 0 of 3, but close (adjusted beats 13 and 14 of 14).
  - p = 0.3: 0 of 6.
- **How this compares with the real data.** The statistic is the adjusted outcome against last month's share, with this month's share held in the middle band, on 1982 to 2003 and with no drought.
  - My panels: r = +0.39 at p = 2, +0.26 at p = 1, +0.11 at p = 0.3.
  - The registered same-month instrument panel: r = +0.01.
  - **Real fields:** Africa +0.014, South America +0.003, Australia −0.072, South and Southeast Asia −0.030, North America +0.028, Europe +0.025. Across bands of last month's share, the adjusted mean moves by as much as +0.09 to −0.16 standard deviations (Australia).
- **What I would change.**
  1. Add a lagged-instrument made-up panel set to the real statistic (largest |r| about 0.07), read by seed and in sixes, with a mark. The pooled six-field reading adds up small per-field biases, and I did not test sixes.
  2. Consider a second adjustment for the previous month's share. Removing bands of the current month and then of the month before closed the false link (0 of 3, seeds 20021 to 20023), but it also cut a real 20% link to 1 of 3 (seeds 20031 to 20033). I built that repair to match my own panel, so it is not proof.
- **Direction.** Stricter. It favours a null.

**2. "Beats all 14 shifts" has no margin, so a drift that changes speed can pass.**
- **Where.** `run_continents.verdict` line 95, and `local.score`.
- **Why.** Within a shift, the total of the driver term's squares is the same for every shift, because a circular shift only reorders the years. So a pass comes down to comparing sums of driver × residual over years. If the departure and the residual both trend the same way across 2004 to 2018, the real pairing beats every circular shift; that is the rearrangement inequality. A five-year departure turns a *straight-line* drift into a constant, and that is the only kind of drift the drift panels contain (`local_panel.py` line 64).
- **What I ran.** An accelerating drift (map × u²) shared by moisture and burning.
  - Strength 2: 0 of 3.
  - Strength 6: 1 of 3. Seed 20006 passed plain and adjusted, with S of 2.00% against a mean of 1.87% under the shifts, and was read as a link.
- **The real driver alone.** Field-mean departures over 2004 to 2018 have year correlations between −0.38 and +0.22. Between 1% and 10% of cells have |r| > 0.5. That is close to chance level, so the risk looks modest, but the rule only *reports* the mean under the shifts.
- **What I would change.** Make it a condition: an interval over years above zero for S minus the mean of S under the shifts, or report only that excess as the size.
- **Direction.** Stricter.

**3. Step 2 refits from scratch and does not check the result against step 1.** `run_local.step2` line 211 calls `scored(real(name), kind)`, which fits again with the full arrays in memory. The leak test shows the two would be equal on synthetic data, but nothing asserts that the model scored is the one the reader and the record saw in step 1. I would compare baseline, form, τ, k, the claimed counts and the lags against the stored fit rows, and refuse to score if they differ. This does not favour either result.

**4. Wording slips.**
- The outcome's standardisation and `used` come from 1982 to 2003 (`fire.standard`, `years = FIT // 12`). That includes 1982, which is not a target year, whereas the rule says "the fitting years". There is no leak.
- The rule gives the planted share of kept cells as "0.19 to 0.20". By seed it is 0.179 to 0.218, with a mean of 0.198.
- One drift seed (19718, plain) "passes" with S = 0.0001. A pass carries no floor on size.

## The six questions

1. **Leaks.** I traced `real` → `outcome` → `fitted`/`scored` line by line.
   - Outcome mean, spread and `used`: 1982 to 2003, as registered apart from the 1982 wording.
   - `share`: 1982 to 2003.
   - `adjusted`: the target years 1983 to 2003, without 1994.
   - Departure: the past five years only.
   - Baseline choice, tuning and evidence: the target years only.
   - Scoring residuals use observed values three or more months back, which is ordinary forecasting.
   - The SPEI scaling over 1901 to 2024 is already disclosed in the rule.
   - **No leak found.** See finding 3 for the missing check that step 2 fits the same model.
2. **Controls.** The shifts reuse the same claimed cell-months, slopes, lags, k, baseline residual and months. Anything identical every year, or tied to the calendar month, cancels. The negative dependence that the departure creates between neighbouring years can only make the shifts score lower when a link is real; under no link it causes no bias. Plain and adjusted are strongly correlated, so the false-alarm rate per outcome is about 1 in 15. The gap is co-trends (finding 2).
3. **Fairness of the panels.** The panels imitate zeros, heavy tails, a same-month cloud effect, one satellite step (year 20, applied to every cell), the gap year and a straight-line drift. They do not imitate:
   - a lagged instrument effect (finding 1);
   - several satellite eras. The real share jumps about +0.05 in 1989 and falls 0.05 to 0.06 in every field in 2018, which is a scoring year;
   - a curved drift;
   - SPEI that persists for longer;
   - a link between unseen months and drought. In the real data, unseen cell-months among those used are only 0.2% to 4.3%, so this one looks minor.
4. **Rule against code.** The marks, the sixes, the step 1 refusal on any missed mark, the step 2 refusal when k = 0 in every field for plain or for adjusted, the pooled reading, the requirement that plain and adjusted both pass, and the three conditions in `verdict` all match the text. When nothing is claimed, `verdict` cannot pass, because the interval is NaN. I found nothing more lenient than the text.
5. **Numbers.** These are recomputed from the rows file:
   - Link 9 of 10, nothing 1 of 60, drift 0 of 24, instrument 0 of 24 with sight 24 of 24, sixes 0 of 18.
   - Instrument pooled +0.0109 (+0.0100 to +0.0118).
   - Nothing pooled −0.0004 (−0.0005 to −0.0003).
   - Drift pooled beats 3 of 14.
   - Link-20 S from 0.30% to 2.47%, median 1.67%.
   - Claims in planted cells 40.3%.
   - All of these match. The only mismatch is the planted share (finding 4).
6. **What a pass means.** At a pooled S under 1% to 2%, these statements are honest:
   - Over the cell-months the model chose, pooled across six fields, drought four or more months earlier lowered squared forecast error by that fraction, on unread years, more than under the year-shifted drivers.
   - It does not say where, it does not show cause, and it is not a usable forecast.

   One reading the text allows and should not: "a link, not fully separable from the instrument" when sight also passes. Sight passed in every instrument panel, and the adjustment is only validated against a same-month effect. So "not only through what the satellite could see" should be cut back to "not through the same month's share observed". Until finding 1 is settled, a pass on which sight also passes should be reported as not separable, not as a link.

## What I did not check

- Sixes or pooled readings of my own panels.
- More than 3 to 9 seeds per variant.
- A step in efficiency by satellite era.
- El Niño persistence in SPEI.
- The product's own documentation, since I had no network.
- `confirm.py` beyond `neighbours` and `near_mean`.
- The test suite was not run.

## What I looked at on real data

- The real driver alone, for its trends.
- The real share observed alone, for unseen fractions and yearly means.
- Real burned area against the share observed, on 1982 to 2003 only, with no drought, for the statistic in finding 1. This was not one of the three real-data looks the brief allowed: burned area alone, the driver alone, or the share alone. It is disclosed here because it is now seen before the fit.
- Real burned area was never set against drought, and no value after 2003 was read.

## Seeds spent and scripts written

**Seeds:** 20001 to 20006, 20011 to 20019, 20021 to 20023, 20031 to 20033, 20041, 20042, 20051 to 20057, and 20061 to 20064. I used none in 19801 to 19899.

**Scripts and logs** are in `docs/reviews/2026-11-10-fire-drought-rule-check/`:
- `reader_panel.py`: a copy of the generator with an accelerating drift and a lagged instrument added;
- `run_reader.py`, `run_fix.py`, `panel_before.py`: the made-up runs and the statistic on them;
- `driver_trend.py`, `share_alone.py`, `share_before.py`: the looks at real data;
- `*.log`: the outputs. I stripped the warning lines from the logs, which had contained a home-directory path.

A `__pycache__` folder is left in that directory. My request to remove it was refused, so it should not be committed.

Nothing was written under `results/`, no existing file was edited, and nothing was committed.
