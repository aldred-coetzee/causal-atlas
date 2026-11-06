# R2 ceiling: is the world too thin, or the instrument deaf?

Rule first, committed before any number from this code (rule 9). A diagnostic on spent seeds, not a mark, and no setting comes from it. Code: `scripts/run_r2_ceiling.py`.

## Why

`results/r2-check.md` left open whether any method could hear these worlds in 96 months. A fresh reader, asked whether we test the right things, scored the generator's own rate against its rate without the link, one month ahead, on months 195 to 290: S of at least 0.02 in 14 of 20 planted worlds. So it read the worlds as holding plenty and the instruments as deaf. Those figures are seen, so this is not blind to them. That comparison flatters the ceiling in two ways: its base knows the hidden episodes exactly, which makes the denominator small, and it is one month ahead where our methods work at three. This check scores the link's worth on the baseline we actually use, at three months.

## Worlds and months

`planted_3.50`, seeds 3001 to 3020; `pure_null`, `shared_null`, `combo_null`, seeds 3001 to 3005. Months 195 to 290, four spans, R at 25 trees, the same schedule as R2. No fresh seed, no decoys.

## Readings

**A. The reader's figure at the right lead.** S of `lead_rates` with the link against without it, lead 3. Planted only. Beside the others, not read by a bar.

**B. The ceiling on our ruler.** M = R × (with link / without link), both from `lead_rates` at lead 3, scored against R with `level_free`. This is the real baseline told the link's exact effect in each cell and month. The bar for a world is R2's pipeline bar without the screen: S at least 0.005, lower end above 0, raw above 0, S positive in at least 3 of 4 spans. Reported beside it: worlds at S of at least 0.02.

**C. The screen given the perfect column.** One column z = log(with link / without link), in the screen's own statistic, with the same 32 circular year shifts. A world hears if the unshifted T beats all 32. For a null world z is the planted world's of the same seed, so nothing in that world is linked to it.

Beside C, each scored the same way, to point at a cause:
- C-uncapped: no cap at 20 on the counts.
- C-oracle: the residual taken against the generator's rate without the link, one month ahead, rescaled, in place of R*. This asks whether R absorbs the link.

## How it is read, fixed now

| | At least 16 of 20 planted | At most 8 of 20 planted |
|---|---|---|
| **B** | The worlds hold enough for R2's bar on our baseline, so R2's miss is the instrument's | Too little to meet that bar, so R2's bar was out of reach for any method on this baseline and window |
| **C**, with at most 2 of 15 nulls | The statistic is sound and the fault lies in the columns or the search | The statistic cannot hear even the exact answer, and it should not be carried into the framework |

Between 9 and 15 is reported as mixed, with no verdict. C-uncapped and C-oracle only point at a cause; they prove none.

## Limits it carries

- The oracle is an upper limit and no method could reach it: it knows the link's form and cells, and inputs through the target month, while methods stop at the origin.
- `lead_rates` averages 6 simulated paths, so the ratio has some noise in linked cells, which lowers B slightly.
- 20 and 15 worlds, spent seeds, so counts are rough.

About 1 machine hour, about 30k tokens, estimates only. Two processes of 3 threads, nice 19.

## Result

Not yet run.
