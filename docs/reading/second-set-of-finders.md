# A second set of finders: what would hear what the first set does not

Design notes for the brief in `docs/specs/2026-11-11-parallel-helpers.md`, part C, finished under `docs/specs/2026-11-11-parallel-helpers-fifth-wave.md`, C2. **Every number here is a development number from smoke worlds** (made-up tables, 35% share, three links a world, seeds 59001 to 59999) and none is a count. Code: `scripts/lab_second_set.py`; outputs under `data/panel/second-set/` (the fifth wave's are `try-count-*.jsonl`). Nothing real was read.

## The harness, read for faults (fifth wave)

No fault that changes a number below was found. Three things to know. (a) The steward keys a row on outcome, series named, family and tag; every new member is in the slope family with no tag, so a `common lag 1` or `lags 3 to 5` row and a `lag 1` or `lag 2` row naming the same series count as one, the higher lift standing for all. A long-lag row can therefore stand in for a lag-1 row; hearing is reported at the planted lag as well, and in every run below the two agree. (b) `stands` in `scripts/run_finders.py` labels a row against the first planted link on its outcome only, so a row naming a second link on the same outcome would read as naming nothing planted; no world used here has two links on one outcome (0 of 54 checked), so it is latent. (c) The by-mean emulation replaces, inside one process, the state series' form by its past-mean form in the referee's `terms` for `by_state` proposals only; it reaches every read and the shifted scores, and nothing else. `referee.py` is as it was.

## 1. Where each unheard kind is lost (earlier helper; not rerun)

**From a series common to all places**: lost first at the plain-line member's lift. The planted term ranked first among its 39 terms for 16 of 18 links at each size, yet the deduction for the best of 39 (about 2.4 to 3.2) left only 7 and 9 of 18 above the floor of 3. The steward lost nothing; a quarter to a third of rows sent then failed at the referee.

**A sign that turns on a state**: lost at the referee. A row was sent for 12 and 16 of 18 links; 2 and 5 heard. The referee builds the state's side in each read's own form (line, recent) where the proposal means the side of its own past mean; read by the past mean in every read, the answer told where passed 18 and 17 of 18, against 1 and 4 as coded.

## 2 and 3. Members tried, rerun on unused seeds (fifth wave)

Arrangements read on every world, each under its own bar: the first set; the first set with the state read by its past mean; `common lag 1` added; `common lag 1` and `lags 3 to 5` added; the same by mean; and **the second set as it would be registered**: its own board built with `lag 1` split into series that differ by place and series common to all (`local_slope`, `common_slope`), `lags 3 to 5` run last after the second round, with and without the by-mean reading.

| Worlds (fifth wave) | Links | First set | `common lag 1` added | Registered set | Registered, by mean |
|---|---|---|---|---|---|
| shared, 6 at 120 | 18 | 6 | 11 | 11 | 11 |
| shared, 6 at 240 | 18 | 4 | 5 | 5 | 5 |
| flip_state, 6 at 120 | 18 | 1 | 1 | 1 | 8 |
| flip_state, 6 at 240 | 18 | 5 | 5 | 5 | 14 |

**Does it hold?** The direction holds for both: `common lag 1` hears more links from a common series at 120 places (earlier 16 to 21 of 36; now 6 to 11 of 18), little at 240 (earlier 19 to 21; now 4 to 5); the by-mean reading hears more state links at both sizes (earlier 3 to 11 and 10 to 28 of 36; now 1 to 8 and 5 to 14 of 18). The size of the gain at 240 for the common member is small on both sets of seeds. Taking the common series out of the plain-line member changes nothing heard here (registered equals added on every world). **Lags 3 to 5** (earlier helper, not rerun): heard 24, 24 and 23 of 24 at lags 3, 4 and 5 at 120 places, 18 of 18 at lag 4 at 240, against none for the first set.

**What the additions cost the seven kinds the first set hears**: nothing, on 6 worlds each at 120 places. Links heard, of 18, the same number in all seven arrangements: steady 18, threshold 8, extremes 7, two together 10, sign by place 16, many weak 10, hidden mover 15. Every heard link was heard at its lag. Rows sent rose by 0 to 5 a kind over six worlds; the bar's middle moved by at most 0.06.

## False passes (fifth wave, unused seeds)

- **Nothing predicts**, six variants: 24 worlds at 120 places, 12 at 240: **no pass in any arrangement**, the by-mean reading included. Rows sent: 58 for the first set and 60 registered at 120; 40 and 44 at 240.
- **Shared slow paths**, seven shapes, 14 worlds at 240: **no pass in any arrangement**. Rows sent 55 against 60. (Earlier: 2 of 27 worlds passed, the same two in every arrangement, both a path.)
- **Linked worlds** (90 above): no pass named nothing planted, in any arrangement.

## Recommended for the second set

1. `common lag 1`: the plain line a year before for the series common to all places, its deduction from its own terms; the common series taken out of `lag 1` (`local_slope`). Expect its gain at 120 places; at 240 it is small.
2. `lags 3 to 5`: one slope member, every series at lags 3, 4 and 5, other alignments from five years.
3. In the referee, a `by_state` proposal's state read by its past mean in every read: a referee change, the project session's to make, registered and counted apart from the finders.

**Dropped** (earlier helper): what was new in a common series (19 and 20 of 36 against 21 and 21); the product of a local and a common series (adds nothing; with the by-mean reading costs hearing, 12 to 10 and 29 to 19); a window summing lags 3 to 5 (hears less at lag 5 and puts 18 rows above the floor where nothing predicts, against 6).

## 4. Two further kinds of mathematics (reasoning only; untested)

**a. Gathering within blocks that share coverage**, going down only where a block stands (hierarchical testing). Blocks fixed by source before any outcome is seen; one term a block keeps the deduction small. Test: gaps laid by block, weak series planted inside one block and across blocks, nothing-planted tables with the same blocks; drop if it hears no more than `gathered` on a table with gaps. Needs gaps by block in the generator.
**b. The lagged cross-correlation spectrum between blocks**: the top singular value at the true alignment against the other alignments, pooling outcomes as well as inputs; posts a mode row. Test: a hidden mover planted through several inputs and, a year later, several outcomes; drop if it hears only what `gathered` hears. Needs a planted kind with several outcomes a link.

## What a registered count needs

- **Two counts, apart.** (A) The second set of finders under the referee as it is. (B) The by-mean reading, as a referee change, on the referee's own nothing-predicts and path panels first, then on state worlds, with worlds where the state series trends added.
- **Worlds for A**: the first set's count panels (`results/finders-stage-a2.md`: nothing predicts 30, 30, 15 a variant at 120, 240, 480 places; seven path shapes 15, 15, 8; nine linked kinds 20, 20, 10), plus steady links at lags 3, 4 and 5 (20, 20, 10 each): about 1,316 worlds. Each read twice, the first set's board and the registered board, each under its own bar, so that what is lost and gained is paired on the same world.
- **Marks (proposed)**: marks 1, 2 and 4 of the first set's count, with its limits, for the registered set. Mark 3 at the first set's limits for the seven kinds, and paired: links heard by the first set and not by the second at most 2 of 60 (of 30 at 480) a kind. Common series: more heard than the first set at 120 places, paired; at 240 and 480 reported, no mark. Lags 3 to 5: at least 45 of 60 (25 of 30) a lag. Flip_state: no mark in A.
- **Seeds**: a fresh range, outside 47001 to 47999, the first set's counted seeds and 59001 to 59999.
- **Runtime on this box**: per world, the swarm 3 s at 120 places and 6 s at 240; the registered board 1.5 and 3 s more; one reading 2 to 6 s (from seven readings in 10 to 63 s a world, box shared). The first set's count, 1,166 worlds with three readings each, took 2 h 18 min on six processes; this is about the same work, so about 2.5 hours on six processes or 7 on two. 480 places was not timed here.

## Not known

480 places (nothing run there); the by-mean reading where the state series trends; why the common member gains little at 240; the long member's rows on a table with gaps; tables with 26 common series of 461, as the real table has, against 8 of 40 here; section 4.

**Seeds used.** Earlier helper: 59001–59006, 59011–59016, 59021–59026, 59031–59036; 59041–59052, 59061–59072; 59081–59092, 59101–59112; 59121–59128, 59131–59138, 59141–59148, 59151–59156, 59161–59166; 59201–59206, 59211–59216, 59221–59226, 59231–59236, 59241–59246, 59251–59256, 59301–59304, 59311–59314, 59321–59324, 59331–59334, 59341–59344, 59351–59354; 59401–59403, 59411–59413, 59421–59423, 59431–59433, 59441–59443, 59451–59453, 59461–59463, 59471–59476; 59501, 59502. Fifth wave: 59511–59516, 59521–59526, 59531–59536, 59541–59546, 59551–59556, 59561–59566, 59571–59576, 59581–59586, 59591–59596, 59601–59606, 59611–59616, 59621–59624, 59631–59634, 59641–59644, 59651–59654, 59661–59664, 59671–59674, 59681–59682, 59691–59692, 59701–59702, 59711–59712, 59721–59722, 59731–59732, 59741–59742, 59751–59752, 59761–59762, 59771–59772, 59781–59782, 59791–59792, 59801–59802; and 59999 (one check that the new member runs).
