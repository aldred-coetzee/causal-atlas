# A second set of finders: what would hear what the first set does not

Design notes, 2026-11-11, for the brief in `docs/specs/2026-11-11-parallel-helpers.md`, part C. **Every number here is a development number from smoke worlds** (made-up tables, 35% share, three links a world, seeds 59001 to 59999) and none is a count. Prototypes and harness: `scripts/lab_second_set.py`; outputs under `data/panel/second-set/`. The work was stopped early for a restart: what is half done and where to pick up is at the end.

## 1. Where each unheard kind is lost (run; finished)

**A link from a series common to all places** (`lost shared`, 6 worlds at 120 places and 6 at 240, 18 links each): told where, the answer passed 13 and 17 of 18. The planted term was first among the plain-line member's 39 terms for its outcome in 16 and 16 of 18, yet its lift reached 3 for only 7 and 9. Every row above the floor was sent (8 and 10); 6 and 6 were heard. So it is lost first **at the member's lift**: the deduction for the best of 39 terms (about 2.4 to 3.2) takes a first-ranked term under the floor. The steward loses nothing. Then about a quarter to a third of the rows sent fail at the referee in the scan's places. Inputs with long memory (0.74 to 0.95) are weak even for the answer.

**A sign that turns on a state** (`lost flip_state`, 6 worlds each size): a full row was above the floor and sent for 12 and 16 of 18 links; 2 and 5 were heard. The answer told where passes 1 and 4 of 18 as the referee is coded, 4 and 6 sent as a product, and **18 and 17 of 18 when the state's side is read by its own past mean in every read**. So it is lost **at the referee**: `referee.terms` builds the state's side from the series in the form of the read in hand (line, recent), where `referee.proposal` describes the side of its own past mean; under those reads the side agrees with the planted side in as little as 0.3 to 0.4 of scored years. At 120 places the member's lift is a second limit (at least 3 for 7 of 18 links; 16 of 18 at 240).

## 2. What would propose each (run; finished except the last block of worlds)

| Change | Worlds | Heard before | Heard after |
|---|---|---|---|
| Member `common lag 1` added | shared, 12 at 120 places (36 links) | 16 | 21 |
| | shared, 12 at 240 | 19 | 21 |
| State read by its past mean in every read | flip_state, 12 at 120 | 3 | 11 |
| | flip_state, 12 at 240 | 10 | 28 |

- **`common lag 1`** (`common_slope`): the plain line one year before, for the series common to all places only, as one member of the slope family. Same scan, same twenty other alignments, same lift rule; its deduction is the best of its own terms (8 here, about 1.8) and not of 39. Its lift is not raised by choosing or trying more: it tries fewer terms and pays for those. What it does add is one more member's worth of chance rows, and that is the cost to count: where nothing predicts (60 worlds) it put 5 rows above the floor, against 4 and 8 for the two plain-line members. To register it clean, take the common series out of the plain-line member's terms so no term is tried twice (not run that way: here both tried them and the higher lift stood).
- **The state's side by its past mean**: a change to the referee, not a member, and the project session's to make and count. Emulated here in one process only (`state_by_mean`); the file on disk is as it was.

## 3. Lags of three to five years (run; finished)

**`lags 3 to 5`** (`long_slope`): every series at lags 3, 4 and 5 as the terms of one slope member (120 terms here), other alignments kept five years and more away (18 of the 20).

| Planted lag, places | Links | First set | With `lags 3 to 5` | Rows sent, middle | Bar, middle |
|---|---|---|---|---|---|
| 3, 120 | 24 | 0 | 24 | 3 to 6 | 1.91 to 2.49 |
| 4, 120 | 24 | 0 | 24 | 2 to 6 | 1.76 to 2.46 |
| 5, 120 | 24 | 0 | 23 | 4 to 6 | 1.39 to 2.57 |
| 4, 240 | 18 | 0 | 18 | 4 to 8 | 2.27 to 2.61 |
| 1, 120 | 18 | 18 | 18 | 13 to 13 | 2.67 to 2.70 |

Its cost where nothing is at those lags: 2 rows above the floor in six lag-1 worlds; 6 in 60 worlds where nothing predicts; 5 in 27 slow-path worlds.

## False passes with both members and the by-mean reading (run)

- Nothing predicts, six variants (36 worlds at 120 places, 24 at 240): **no pass under any arrangement.** Rows sent in all: 174 for the first set, 182 with both members.
- Shared slow paths, seven shapes at 240 places (27 worlds): 2 worlds with a pass, both regimes, both carrying the path label, **the same two under every arrangement**; no pass named nothing planted. Rows sent 115 against 122.
- Linked worlds (24 shared, 24 flip_state, 36 lagged): no pass named nothing planted.

## Recommended for the second set

1. `common lag 1`, settings as above, common series removed from the plain-line member.
2. `lags 3 to 5`, one member, settings as above.
3. In the referee, a by_state proposal's state read by its past mean in every read; counted as a referee change, with nothing-predicts and path worlds first.

## Tried and dropped

- **What was new in a common series** (lag 1 less its memory times lag 2, as a mode): 19 and 20 of 36 against 21 and 21 for the plain member, and its row stands in for the plain one.
- **Product of a local and a common series** (`state_pairs`): adds nothing as coded (4 to 4, 7 to 8) and with the by-mean reading costs hearing (12 to 10, 29 to 19), its rows standing in for sign-by-state rows of the same names.
- **A window over lags 3 to 5** (sum of the three): heard 13, 20 and 4 of 24 at lags 3, 4 and 5, and 18 rows above the floor where nothing predicts against 6.
- **Other alignments from three years** for the long member: same hearing in 36 lag worlds; not run where nothing predicts.

## 4. Two further kinds of mathematics (reasoning only; nothing run)

**a. Gathering within blocks that share coverage, going down only where a block stands** (hierarchical testing, `maths-for-combinations.md` candidate 3). Reason: the first read's rule says a gathered term speaks only where every series has a value, so on a table a third missing the modes family says little; series of one source share places and years. Blocks are fixed by source before any outcome is seen, so they cost no lift; one term a block keeps the deduction small. Test: made-up tables with gaps laid by block; twenty weak series planted inside one block and, apart, across blocks; nothing-planted tables with the same blocks. Drop if it hears no more than the gathered member does on a table with gaps. Needs gaps by block in the generator (it has gaps at random only).

**b. The lagged cross-correlation spectrum between blocks** (`further-maths.md` field 1; set aside in decision 0062, point 7). Reason: the only candidate that pools over outcomes as well as inputs, and the table has far more series than years. No textbook edge: the top singular value at the true alignment against the same at the other alignments, the whole decomposition done again at each. It posts one mode row an outcome, so the referee needs no new form. Test: a hidden mover planted through several inputs and, a year later, several outcomes, each link too weak for a row alone; nothing-planted worlds with a mover on each side and no link between. Drop if it hears only what the gathered member hears. Needs a planted kind with several outcomes a link.

Set aside: pattern search on conditions (two tails together leave about forty early place-years), transfer entropy, persistent homology.

## Not known; where to pick up

- **Not run (stopped):** whether the additions cost hearing of the seven kinds the first set hears. Next: `try all <kind> 120` for steady, threshold, extremes, pair, flip, many, hidden, then flip_state and shared at 120 and 240, on unused seeds. `try-all-steady-120.jsonl` holds one world and is not used above.
- `common lag 1` with the common series out of the plain-line member; a common member at lag 2; the long member's rows on a table with gaps.
- The by-mean reading where the state series trends: every late year is then on one side.
- Common series here number 8 and series 40; the real table has 26 and 461, and its series are read as departures from the year's middle.
- Section 4 is untested.

**Seeds used:** 59001–59006, 59011–59016, 59021–59026, 59031–59036 (`lost`); 59041–59052, 59061–59072 (`try shared`); 59081–59092, 59101–59112 (`try state`); 59121–59128, 59131–59138, 59141–59148, 59151–59156, 59161–59166 (lags); 59201–59206, 59211–59216, 59221–59226, 59231–59236, 59241–59246, 59251–59256, 59301–59304, 59311–59314, 59321–59324, 59331–59334, 59341–59344, 59351–59354 (nothing predicts); 59401–59403, 59411–59413, 59421–59423, 59431–59433, 59441–59443, 59451–59453, 59461–59463, 59471–59476 (paths); 59501 and 59502 (started, stopped). 59001 was made twice.
