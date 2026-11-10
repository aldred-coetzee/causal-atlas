# Independent check of the burned-area step 1 result, 2026-11-10

A fresh reader's check of "Result of step 1" in `results/fire-enso.md` as committed at 3d3d1de, with the rows in `results/fire-enso.jsonl`. The reader had no web access, made no edits to existing files, and kept to the sealed-data rule: no burned-area value from January 2004 on (month 264 and later on the fire clock) was set against anything, printed or summarised. The only use of those months was structural, replacing them with noise to show nothing fitted changes.

The scripts are in this folder. Each one takes the folders it reads and writes as arguments, and none of its outputs are kept. Run them from the repo root with `PYTHONPATH=src .venv/bin/python docs/reviews/2026-11-10-fire-enso-independent-check/<script> ...`. The usage line is at the top of each script.

## Verdict

**Holds with corrections.**

- The data step is right, there is no leak, and every number reported matches the rows except one claim count.
- The marks were missed, and not running step 2 was the right call.
- The **explanation** of the missed false-alarm mark is wrong. The result blames the length of the record. The real cause is the control set from decision 0044: dropping the copies one year either side of the real alignment pushes false alarms up, by an amount that depends on the data.
  - On the real South and Southeast Asia field with fresh decoys, this search gives a false alarm in about **15%** of runs.
  - With the full set of copies it gives about **7%**.
  - 18 of 120 (15%) is what this search does on this data. It is not a sign of anything beyond chance.
- The sentence stating a general floor of "two in (controls + 1)" is wrong for the control set actually used. So is the stated floor of about 4% for `results/real-indices-2.md`, which used the same cut.
- "Does not reopen" still holds for both earlier results, but for a different reason (question 5).

## 1. Rebuilding the standardised burned area (South and Southeast Asia, 1982-2003)

**What I did.**
- Read the raw 1982-2003 files only (`q1_rebuild.py`), checking each file's time stamp against its name.
- Summed quarter-degree cells four to one onto the half-degree grid.
- Standardised them with my own code (`q1_compare.py`), following the rule text, and compared the result with cache columns 0 to 263.

**What I found.**
- Same 4,367 kept cells, in the same order, with the same 24,983 cell-months in use.
- 113 values differed, by up to 1.06, all within 6 cell-calendar-months.
  - In each of those, the observed share is exactly 0.2, which is the "seen" threshold. Stored as float32 in the cache, the value lands on the other side of it.
  - Rebuilt with float32 inputs (`q1_threshold.py`), no value differs (largest gap 1.2e-7).
  - This edge case does not matter.
- The per-cent scaling is confirmed at source. In every January file from 1982 to 2003, both "fraction" variables reach 100 even though their units attribute says "1". Dividing by 100 is right.

**How sure:** high.

## 2. Leaks and alignment

**What I did.** In memory, I replaced every burned-area value from month 264 on with noise, two different draws, and pointed the cache at a temporary folder (`q2_leak.py`). Then I rebuilt the field and reran the step 1 real and sight rows for South and Southeast Asia.

**What I found.**
- Fitting-year values, kept cells, months in use and sight are identical for South and Southeast Asia and for Europe.
- The step 1 rows are identical to the committed ones under both draws.
- `fire.oni()` lines up with the fire clock: month 0 is January 1982 (−0.05), month 263 is December 2003, and it equals `oni.data` over 1982-2018.
- One thing to know: the surrogate decoys take their spectrum from the full-length El Niño index (444 months). That is the driver, not burned area, so it is not a leak.

**How sure:** high for the field and South and Southeast Asia. The other fields were checked for the field only.

## 3. The numbers in "Result of step 1"

**What I did.** Recomputed every count from the rows (`q3_rows.py`).

**What I found.**
- Everything matches, with one exception: the one mapping run below 90% has **105** claims, not 102 (0.505 on 105).
- Other counts match: El Niño 0 of 120 in every field, sight 3 of 20 in South and Southeast Asia, false alarms 18, 18 and 18, by gate 12/12/10 and 8/8/8.
- Kinds 1 and 2 give identical alarms in all 120 runs, so they are one measurement, as the text says.
- The sharp-gate bar of 0.85 to 0.95 is right for the 120 kind-1 runs. Across all 480 naming runs it is 0.847 to 0.953, which says the same thing.

**How sure:** high.

## 4. The false-alarm arithmetic

**Derivation.**
- Under the usual assumption, a candidate's real alignment is no more likely to come out on top than any of its year-moved copies. With 19 copies, a gate then alarms about 1 time in 20.
- Two independent gates give 9.75%, so the result's figure is the right figure for that assumption.
- But that assumption only holds if every alignment has the same kind of comparison set. With the full set of copies (1 to 21 years) it does, by symmetry: every alignment has neighbours on both sides.
- Decision 0044 removed only the real alignment's two neighbours (1 and 21 years). Every copy still keeps its own neighbours. Values one year apart are correlated (about +0.24 for the broad value; two years apart it is −0.01). So the real alignment loses exactly the rivals most likely to beat it. Its standardising row also changes.
- The floor is therefore above 1 in 20 per gate, and by how much depends on how persistent the field and decoys are.

**Test.** I simulated the null hypothesis directly (`q4_sim.py`). Each run built a field and 32 decoys with no El Niño, computed every statistic once for all 22 alignments, and then applied the two gates twice: with the cut control set and with the full one. I checked my gate code against a committed row (`q4_validate.py`: Africa, seed 17111, exact match). Tally in `q4_tally.py` and `q4_extra.py`.

| Null runs | Runs | Any alarm, cut set (as built) | Any alarm, full set |
|---|---|---|---|
| Smooth synthetic noise, South and Southeast Asia | 300 | 10.7% | 8.0% |
| Smooth synthetic noise, Africa | 150 | 13.3% | 6.7% |
| Real South and Southeast Asia field, fresh decoys | 150 | **15.3%** (10-22%) | 7.3% |
| Same, each cell-month detrended | 87 | 17.2% | 5.7% |
| Real North America field, fresh decoys | 150 | 6.7% | 6.7% |
| White-noise decoys, South and Southeast Asia | 150 | 8.7% | 7.3% |
| Synthetic field with a strong trend | 86 | 44% | 17% |

- Paired across all 1,055 runs, there were 54 broad-gate alarms with the cut set only and 8 with the full set only. For the sharp gate it was 14 and 0. The difference is not chance.
- With the full set, the overall largest value fell on the real alignment about 1 time in 22 everywhere, as it should.
- **Reading.** 18 of 120 is what this search gives on this data: about 15% on the real South and Southeast Asia field, and 15% pooled over kinds 1 and 3 (36 of 240).
  - Detrending did not remove the excess, so the cause is the control set and not the falling trend in burned area.
  - Strong trends would add more on top.
  - The field-to-field spread (North America shows no excess) is why the text's "may be something more, or may be chance" was the right instinct. The something is the procedure.

**How sure.** High that the cut set inflates false alarms, mainly in the broad gate. Moderate on the exact size per field: about 150 runs each, intervals in the table.

## 5. The earlier results

- `results/real-enso-continents.md` used copies 1 to 49 on 50 years, the full set. Its floor of about 4% is right, and it is unaffected.
- `results/real-indices-2.md` used copies 2 to 48, the same cut, so its stated floor of about 4% is too low.
  - A 50-year version of my null test (`q5_sim.py`, 81 runs) gave 4.9% with the cut set against 2.5% with the full one. That is the same direction, but too few runs to size it.
  - Its measured 3 and 5 of 100 still held marks of 8. A higher floor would only have made holding them harder, so its pass stands.
  - Its named pairs were all rejected at step 2, so no claim rests on them.
- So "does not reopen" is right in outcome, but the reason given for real-indices-2 is wrong.

**How sure:** high for continents; moderate on the size for real-indices-2.

## 6. "El Niño named in 0 of 120"

**What I did** (`q6_oni.py`, `q6_1997.py`).
- Rebuilt my own region tiles and recomputed the strongest correlation with El Niño.
- Looked at the 1997 Indonesian fire season in the plain, unstandardised km².

**What I found.**
- The +0.81 is confirmed: +0.805 in March, lag 2, in the tile centred near 5°N 125°E.
- The silence is fair, and it is not a processing fault. Alignment is right, clipping touches 0.13% of values, and lags 0 to 12 cover the season.
- **The product itself does not show 1997 as a big fire year in equatorial Asia.**
  - August to October km² in 1997 ranks 13th of 21 years for Borneo, 12th for Sumatra and 13th for the two together.
  - February to April 1998 ranks at or near the bottom.
  - Correlations with El Niño over those boxes, August to October, run from about +0.2 to −0.4.
  - The best-known El Niño fire event is absent from this record, so a known-answer test built on it could not pass here whatever the search did.
- The +0.81 tile is a weak place to look for a missed signal. In March only 15 of its 66 cells are in use, and there its burned area correlates 0.66 with the raw observed share.

**How sure.** High on the numbers. I could not check against the product's own validation why 1997 is missing; cloud and smoke over peat fires are the likely reason, but that is a guess.

## 7. "What the satellite saw"

**What I did** (`q7_sight.py`, `q4_trend.py`). Checked whether the observed share is near-constant, which would be the plainer explanation of its strong correlations.

**What I found.**
- It is not near-constant: median spread 0.10 on a median of 0.40. That plainer explanation is ruled out.
- Sight's strong El Niño correlation is robust. The best is +0.88 over the Philippines in February, lag 1, and leaving out any one year gives 0.85 to 0.92.
- The likely physical reading is that El Niño brings clearer, drier skies over the Philippines and the Maritime Continent.
- **But the comparison is not like for like.**
  - Sight has a value in every cell-month, while burned area is 56% zero.
  - Sight rises with the year in every field (field-mean correlation with year +0.40 to +0.68): the instrument sees more in later years.
  - Burned area falls in the four tropical fields (about −0.37).
- So "the search hears sight but not fire" says as much about how dense and smooth each series is as about the search.
- The text's reading is fair as a caution. It should add that sight trends upward and is dense.

**How sure:** moderate.

## 8. Does "needs more years" follow?

Only in part.

- The bar near 0.9 in the sharp gate comes from how wide the search is as much as from 20 years. It is taken over about 97 tiles × 13 lags × 12 months × 32 candidates, beaten against 19 copies.
- The false-alarm excess is the control set, not the length (question 4).
- The known answer may simply be absent from this product (question 6).
- More years would help, but "needs more years than a satellite record has" is not shown.

What would most likely fool a local-drought test:
- **Cloud.** Drought means clear skies, which means more of the ground is seen. The 0.2 seen-threshold already selects on cloud, so drought could "predict" burned area through what the satellite saw.
- **Shared trends.** Both the instrument and the drought indices drift over these years.
- **Few true samples.** Neighbouring cells are correlated, and the real unit is the year: about 20 of them.
- **Shared seasons.** Drought and fire share a season, and a 3-month drought index includes the concurrent month's rain.
- **El Niño behind both.** It drives drought, so a drought link may just be El Niño again.
- **Unseen months.** Setting them to "average" treats wet and dry seasons unevenly.
- **Breaks in the record.** The missing 1994 and satellite changes.
- **Many places tested at once.**

## Corrections the result file needs

1. "(51%, on 102 claims)" should be "(51%, on 105 claims)".
2. The paragraph beginning "A candidate is named when its real alignment beats every year-moved copy of every candidate. With 19 moved copies, the strongest of the candidates does that by luck once in 20 in each gate, however many candidates there are."
   - That holds only when every alignment has the same kind of comparison set.
   - Under decision 0044 the real alignment alone loses its one-year neighbours. That raises the chance of a false alarm, by an amount that depends on the data.
   - Measured on the real South and Southeast Asia field with fresh decoys, it is about 15% per run, against about 7% with the full set of copies.
   - The text's "about 1 run in 10" and "about 12 of 120" are the figures for a symmetric control set, not the one used.
3. "What was measured, 18 of 120, is above even that floor; a sound search would give 18 or more about 1 time in 25." should say that 18 of 120 is what this control set gives on this field, and is not above its floor.
4. "**the false-alarm rate cannot go below about two in (controls + 1), and the number of whole-year controls is set by the length of the record.**" holds only for a symmetric set of copies, such as 1 to 21 or 1 to 49. With decision 0044's set the rate is higher and depends on the data.
5. "**This does not reopen the earlier results.** With 49 controls the floor is about 4 in 100 and those runs measured 3, 3 and 5; with 47 it is about 4 and they measured 3 and 5" needs a qualifier for `results/real-indices-2.md`:
   - its 2-to-48 set has the same lopsidedness, so 4 in 100 understates its floor;
   - its pass stands because a higher floor only makes passing harder, and its named pairs all failed step 2.
6. "Two reasons, both arithmetic: with 19 controls its false-alarm floor is about 1 in 10, and on 20 years the bar it sets is a correlation near 0.9. Naming one driver for a whole continent, blind among 32, needs more years than a satellite record has."
   - The first reason should be the control set from decision 0044, not the count of controls.
   - "Needs more years than a satellite record has" is not shown: the breadth of the search, and the known answer's absence from this product (1997 ranks 12th to 13th of 21 years in Borneo and Sumatra), are at least as likely.
7. Minor: "A sound search would have held these marks about one time in four" is right per mark (0.26). For the two separate measurements together (kinds 1 and 2 as one, kind 3) it is about 7%.
8. Suggested addition to "what the satellite saw": sight rises with the year in every field and has a value in every cell-month, while burned area is mostly zero. The two are not heard on equal terms.

## What I could not check

- Why 1997 is missing from the product. That needs the product's own documentation or validation, and I had no web access.
- The machine times stated in the result.
- The exact size of the inflation in `results/real-indices-2.md`: 81 runs is too few.
- The physical explanations above (cloud over the Philippines, smoke over peat) are plausible readings, not tested.
