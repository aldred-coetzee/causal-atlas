# Framework Stage 1: how strong must a link be for blind search to find it

Rule first, committed before any number from this code (rule 9). The owner's yes: decision 0039. Code: `scripts/run_curve.py`. Seeds: `results/seed-ledger.md`.

This is a measurement, not a test of a method. It passes nothing and spends none of the seeds kept for marks.

## Seen before this rule

At strength 3.50 and 96 months on spent seeds: search on all months names a true input first in at most 4 of 20, the shortlist in 2 of 20, a perfect shortlist in 3 of 20, the true inputs alone in 12 of 20, and the exact link hears in 16 of 20 on the later half. `pooled` was the best form there. No other strength or length has been run under this statistic.

## The grid

- **Strength:** rate ratio per standard deviation of input past its threshold, 1.40, 2, 3.50, 6 and 10. The plan's original panels stopped at 1.40. 10 is far past anything expected and is there so the curve has a top. The generator's own cap lets the rate rise by up to the cube of the ratio, so high rows are extreme worlds.
- **Length:** 96 months (195 to 290) and 240 months (195 to 434). 240 is everything this record has after the baseline's first fit, so no real run at this design can have more.
- **Worlds:** `planted_<strength>` seeds 9001 to 9015, the same seeds at every strength, so only the link's size changes between rows. Nulls `pure_null`, `shared_null`, `combo_null`, seeds 9001 to 9005 each, 15 worlds, read at each length. Own 2 series plus 30 decoys from the existing pool, 1,280 columns. No count cap. Real baseline at 25 trees, spans of 24, rescaled as before. The later months of the synthetic worlds are not the real held-out record, so using them spends nothing.

A world that crashes is counted as not found, and reported.

## What is read at each strength and length

For all three forms. **`pooled` is the headline, fixed now**; it was seen to be the best on spent seeds, so this favours it and the others are always beside it.

- **Search:** the stepping gate on all 1,280 columns over all months.
- **Shortlist:** the method of `results/framework-shortlist.md`, split at the middle (months 48 and 48, or 120 and 120).
- **True inputs only:** the gate on the 80 columns of the 2 true inputs over all months. Blind search cannot beat this by more than chance.
- **Oracle shortlist and floor:** as in that file. The floor's draw now also depends on the panel, so null rows are independent draws; the last run's were not.
- **Exact link:** told the exact effect, over all months, does the unshifted value beat all 32 shifts. On nulls, the 3.50 link of the same seed, so a false alarm rate.
- **Truth plug-in:** the scorer must score it true on every world.
- **Size of the link in plain terms:** the share of all events in those months the link accounts for, 1 less the no-link rate's total over the rate's. A later step can set this beside real links.

Found means the first lead is truly linked. All counts carry a 95% Wilson interval. With 15 worlds these are wide, about plus or minus 25 points at the middle, so this locates a limit roughly and no finer.

**A cell works** when `pooled` search has the first lead true in at least 8 of 15, and a lead named in at most 2 of 15 nulls at that length. Half is a judgement, as before.

## What each outcome means, fixed now

Checks first. **If the exact link hears in fewer than 13 of 15 at strength 10 at both lengths, or the truth plug-in misses,** the instrument is broken and nothing below is read.

Then, taking the first that is true:

1. **Search works at strength 2 or below, at either length.** Blind search is workable at modest strength. Next would be its own rule and marks on seeds 7101 to 7140, at a strength this curve names.
2. **Search works only at 3.50 or above.** Blind search hears only large links. The next question is how large real links are: one reading, one page, pulled by this decision, set against the size column.
3. **Search works nowhere and true inputs alone work somewhere.** The width of the search is the barrier, not the data. That points at narrowing the search and away from longer data.
4. **Neither works anywhere though the exact link hears.** The grid's columns are the barrier, or the statistic.

Whichever it is, the result goes to the owner before any further method. It is his call, including stopping blind search on this design.

## Tests of the test

On seed 3001 at 3.50, a spent seed: the first 96 months of R must match the saved R, and the 96-month table must match Stage 1's saved table to within 0.1%. A miss stops the run. Smoke uses seed 9901 at 3.50 and 10, for timing and crashes only, writing to a scratch file; no score from it is read. If the smoke projects past 36 hours, seeds drop from 15 to 10 and nulls from 5 to 3 per panel, before any world is run, and the intervals widen. Nothing is read until every world has finished.

## Limits it carries

- One link shape, one input pair, independent decoys. A limit here is for this shape.
- The generator's strength is not a real effect size. The size column is the bridge, and it is only a rough one.
- Decoys are independent of each other. Real inputs are related, which should make search harder, so this curve is more likely to flatter than to harm.
- Rule 2 is untouched: nothing here is a finding about real data.

## Estimates

About 400k tokens to the report. Machine: about 20 to 30 minutes a world, 90 worlds, two processes of 3 threads, nice 19, most of a day. The nightly restart can stop the run; the launcher skips finished rows.
