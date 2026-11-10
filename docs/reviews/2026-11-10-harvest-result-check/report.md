# Independent check of the harvest and drought result (commit a1beda9)

## In short

**The result holds up, but the write-up says more than the numbers support.**
- **My own rebuild finds the same effect, a little smaller.** With my own forecasting code the gain is about 1.2% where the project reports 1.67%.
- **No leak.** Nothing from later years reaches an earlier year's forecast.
- **The gain comes from each country's own weather in the right year.** A distant country's weather gives nothing. Taking out each month's world-wide average leaves the gain at 2.1%.
- **The direction is mostly right.** Wetter usually goes with higher yields, in the expected season.

What needs changing is the wording:
- The 1.67% is a share of *squared* error.
- The interval is too narrow.
- One sentence turns the score into a link strength, which the evidence does not support.
- The write-up does not say that about a fifth of the countries carry the whole gain.

The scripts and their logs are in the review folder (`*.py`, `*.log`). Numbers are year-end unless marked mid-year. "S" is the share of the baseline forecast's squared error that the drought term removes. A "shift" is the same test run with the weather of a different year, as a control; the project runs 62 of them.

## 1. Rebuilding the score

**Data** (`check_data.py`, `check_data.log`):
- I checked 20 random panel yields (seed 24001) against the raw FAOSTAT file. All 20 matched, in value and in the "official" flag.
- I rebuilt the drought series for Australia, Hungary and Zimbabwe from `spei03.nc` with my own code. The cell counts and every value are identical to the panel's.

**My own forecast** (`own.py`, `own.log`) shares no forecast code with `harvest.py`.
- Baseline: a three-year mean, or as a second version a ten-year line.
- Errors are scaled by each record's past year-on-year changes and clipped at 4.
- The driver is the same six drought months, each standardised on earlier years only.
- It has four models:
  - A: one set of slopes per cereal.
  - B: one set per cereal and latitude band.
  - C: one set per record.
  - D: A, B and C combined, with weights fitted on earlier out-of-time forecasts.

Results (in the "Beats shifts" column, the shifts' average S is in brackets):

| Model and baseline | S | Interval | Beats shifts |
|---|---|---|---|
| D, three-year mean | 1.21% | 0.62% to 1.78% | 62 of 62 (−0.01%) |
| D, ten-year line | 1.12% | 0.38% to 1.78% | 62 of 62 (−0.03%) |
| A | 0.53% | | 62 of 62 (−0.46%) |
| B | 0.47% | | 62 of 62 (−1.15%) |
| C | −10.0% (overfits) | | 62 of 62 (−14.9%) |

**What it means:** in every version I built, the right year's weather beats every other year's weather by about 1 to 1.6 points. How much of that becomes a net gain over the baseline depends on how strongly the slopes are held back. The project's 1.67% is the same effect, a little larger.

## 2. Leaks

**The real-data path** (`leak.py`, `leak.log`, seed 24003):
- I replaced everything from a cut year onward with noise and random flags. I did this at three cut years (1995, 2005, 2015), in three ways: yields only, drought only, and both.
- Nothing computed for the years before the cut changed, down to the last digit. That covers the model errors, the baseline errors and weights, the baseline chosen, which figures were scored, the seven baselines and the record scales.
- Only the shift columns and the flat driver changed. That is by design, and neither enters S.

**The flat driver** (`leak2.py`, `leak2.log`):
- I rebuilt it from the past only, so each year has removed the line through earlier years only.
- S is then 2.29% (interval 1.58% to 3.01%) and still beats all 62 shifts.
- So using later drought did not inflate the project's flat figure of 2.24%.

**The admission rule:**

| Admission rule | Records | S |
|---|---|---|
| 30 official years (as run) | 503 | 1.67% |
| 20 official years | 590 | 1.51% |
| 40 official years | 394 | 1.48% |
| 15 official years before 1986 only | 391 | 1.39% |
| 10 official years | 645 | 1.35% |

- Every rule beats all 62 shifts, and the flat S is 1.93% to 2.24% under all of them.
- Admission looks only at yield flags, never at drought, so it cannot manufacture the gain.
- The registered rule happens to give the highest S. It was fixed before any real number was seen, so this is not tuning. But 1.67% sits at the top of the range that other reasonable rules give (1.35% to 1.67%).

## 3. What carries it

Source: `carry.py`, `carry.log`.

**By country.**
- The ten largest contributors give 55% of the gain, and the top 20 give 85%. The ten are Zimbabwe, Hungary, Romania, Australia, Bulgaria, Morocco, Chad, the USA, Spain and Moldova.
- Year-end S with countries left out (first figure: gains summed without them; second: forecast run again without them):
  - Without the top 10: 0.86% / 0.87%.
  - Without the top 20: 0.32% / 0.46%.
  - Without the top 30: −0.14% / 0.18%.
- Removing the largest 28 of 141 countries brings the summed gain to zero (19 countries mid-year). Mid-year, the top 20 give 104% of the gain, so the rest lose a little on net.
- Removing the largest contributors always lowers a pooled score, so this shows concentration, not a fault. But a reader needs to know that the gain sits in about a fifth of the countries, mostly dry rain-fed producers.

**By cereal.** Leaving out each cereal in turn and refitting gives S of 1.48% to 1.89%. No single cereal carries it, and leaving out rice raises S.

**By year.**
- The best years are 1992 and 2003 (13% of the gain each), then 2012, 2022 and 2000.
- S is 1.22% without the best 3 years and 1.07% without the best 5.
- S reaches zero only after the best 19 of 39 years are removed (13 years mid-year).

**Intervals:**

| What is resampled | Year-end | Mid-year |
|---|---|---|
| Years (as reported) | 0.95% to 2.39% | 0.48% to 1.77% |
| Countries | 1.02% to 2.34% | 0.54% to 1.71% |
| Countries and years together | **0.60% to 2.79%** | **0.17% to 2.04%** |

The honest interval is about half again as wide as the one reported. It stays above zero in both variants.

## 4. Wrong place, right year

Source: `place.py`, `place.log`, `world.py`, `world.log`.

**A distant country's weather.** Each country was given the drought of a random partner more than 5,000 km away (median about 8,700 km), in five draws with seed 24007.
- The project's S is −0.13%, −0.04%, −0.04%, −0.02% and +0.01%. These beat 0, 29, 38, 18 and 59 of the 62 shifts.
- My own forecast D gives −0.05% to 0.22%.
- The gain disappears, so it is not a world-wide year effect.

**Each month's cross-country average taken out of the drought index:**
- S is 2.11% (1.33% to 2.96%) and beats all 62 shifts. The flat S is 2.19%.
- Mid-year, S is 1.31% (0.67% to 1.96%) and beats all 62 shifts.
- My own D gives 1.84% year-end. The mid-year D line in `place.log` repeats the year-end figure, because my code ignores the mid-year setting.

**The world average alone, given to every country:**
- The project's S is 0.06%.
- My own D gave 1.09%, but that is drift. With a straight line removed it is −0.01%, and shifted world averages score up to 1.36%.

**What it means:** the gain belongs to each country's own weather. The write-up does not claim otherwise, but it can now say so as something that was tested.

## 5. Direction

Source: `direction.py`, `direction.log`, `seasons.py`, `seasons.log`. A positive correlation means wetter goes with a higher yield than expected.

**The 25 records with the largest gains.** In 21 of them the strongest correlation is positive and falls in a plausible season:
- Australia wheat and barley: September and December, about +0.5 to +0.6.
- Argentina maize and sorghum: the previous December and March, about +0.6.
- Zimbabwe maize and millet: March, about +0.7.
- Syria and Moldova wheat and barley: June, about +0.6 to +0.7.
- Bulgaria and North Macedonia maize: September, about +0.5 to +0.6.

The exceptions:
- Korea rice is −0.60 at September. Plausibly, wet or stormy seasons cut rice.
- Greece wheat and barley, and Georgia maize, are negative at the previous September.

**All 491 records with 20 or more years:**
- The strongest correlation is positive in 324 records and negative in 167.
- Counting only correlations above 0.3 in size, 189 are positive and 80 negative.
- The average correlation is +0.07 in March, +0.09 in June and +0.07 in September.

**Which months carry it:**
- The harvest year's four months alone give S of 1.31% (0.63% to 2.02%).
- March and June alone give 0.85% (0.14% to 1.59%).
- The previous year's two months alone give 0.15% (−0.09% to 0.39%).

So a "rebound" route, where last year's weather helps only by explaining last year's dip, is small.

## 6. The third of records chosen before 2005

Source: `kept_check.py`, `kept.log`, and the existing made-up rows in `results/harvest-drought.jsonl`.

**How the third was chosen.**
- I rebuilt the choice from the 1986 to 2004 errors alone and got exactly the stored 136 records, in 76 countries.
- Those early errors are themselves out of time (item 2).

**Whether the choice can create a gain from nothing.** On the evidence, it cannot:
- On the 30 made-up records with no link, the chosen third's later S runs from −0.11% to +0.14% (−0.16% to +0.09% mid-year).
- Drift records reach at most 0.26%, and step records at most 0.14%.

**The size of the later gain, 2005 to 2024:**
- The chosen third gets S of 5.32%. Resampling countries gives 3.79% to 6.86%.
- **The other two-thirds of ranked records get −0.21%.**
- Records too short to rank get 2.31%.
- A record's early gain and later gain correlate only 0.27 by rank.
- Ten countries give 61% of the chosen third's later gain.

"About three times the whole panel" is arithmetically true. The reader also needs the other half: outside that third and the short records, the term gains nothing after 2005.

## 7. The words

| # | Sentence | What is wrong | Change |
|---|---|---|---|
| 1 | "takes 1.67% off the forecast error" and "one part in sixty" (results and README) | It is a share of squared error, scaled per record and clipped at 4. In the size of a typical error it is about 0.8%, about one part in 120. | Say "squared error" and give the plain size. |
| 2 | "The honest range is one part in a hundred to one part in forty", and the reported interval | It resamples years only. | Report 0.60% to 2.79% (mid-year 0.17% to 2.04%) beside it. |
| 3 | "the real link in the index is at least that strong" | The made-up ruler covers one shape of link. The score depends on how a link is spread as much as on how strong it is. A shared cause with no link at all gave S of 1.5% to 2.7% in the earlier check. | Withdraw it. Say only that the real S exceeds the ruler's strongest case. |
| 4 | "It does not rest on one year, or on one half" | True, but about 28 of 141 countries (19 mid-year) carry all the net gain and ten carry half. | Add that. |
| 5 | "went on helping, about three times as much" | The other ranked two-thirds gained −0.21% after 2005. | Add that. |
| 6 | "harvested in autumn lose most of it" | Sorghum, largely an autumn crop, keeps most of its gain (1.48% to 1.20%), and leaving out any one cereal moves S by under 0.25 points. | Narrow it to maize and millet. |
| 7 | README: "no false link in 140 no-link readings" | It is 70 made-up records, each read twice, and drift is stopped only by the flat driver. | Say so. |
| 8 | "Knowing how dry each country was in the months to its harvest" | The year-end figure includes September to December, after most northern harvests, and the index also carries heat. | Add a few words. |

These parts are not overstated, and are now independently supported: that the wrong-year weather does nothing; that the gain does not rest on a trend (the past-only flat driver gives 2.29%); and that the third was chosen before 2005.

## 8. What else could produce it

**Checked, and ruled out or small:**
- A world-wide year effect.
- Straight-line drift, including a line fitted on the past only.
- The admission rule.
- A leak.
- The rebound through last year's weather.

**Not named in the write-up:**
- **Errors shared within a country.** The cereals of one country share one drought series and one statistics office. The reported interval ignores this.
- **Which years have official figures.** Offices may fail to report in bad years. This would more likely weaken the link than create one. Not measured.
- **Fields abandoned in drought.** These drop out of yield per harvested hectare, which would hide some of the effect, not create it.

**Already named and still open:** yields estimated with weather data, El Niño and heat as shared causes, FAO revisions, and the drought file's known error. Nothing I ran separates these.

## Could not check

- Whether official yields are estimated using weather.
- Published effect sizes, crop calendars, FAO revisions, and the drought file's error.
- My own model's mid-year variant.
- Item 4 with my own model beyond these five draws.

## Seeds used

- 24001: data sample.
- 24002 and 24004 to 24006: bootstraps.
- 24003: leak noise.
- 24007: distant partners.
- 24008: bootstrap of the chosen third.

No made-up records were generated. Item 6 used the 70 existing made-up rows.

## Token use

About 140,000 fresh tokens by my own estimate. This was not counted from the transcript.

## Verdict

**Stands with changes**:
1. Say "squared error" and give the plain size (about 0.8%).
2. Report the interval with countries and years both resampled: 0.60% to 2.79%, and 0.17% to 2.04% mid-year.
3. Withdraw "the real link in the index is at least that strong".
4. Say that about a fifth of the countries carry the gain, and that the other ranked two-thirds gained nothing after 2005.
5. Correct the cereal-timing sentence and the README's "140 readings".
6. Optional: add that a distant country's weather gives nothing, and that S stays at 2.1% with the world-wide average removed.
