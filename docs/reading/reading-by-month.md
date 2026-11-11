# Reading by month: what the finders and the referee need first

Design notes for brief E of `docs/specs/2026-11-11-parallel-helpers-second-wave.md`, finished under E2 of the fifth wave. Made-up tables only; nothing real was read or set beside anything. **Every number here is a development number** on smoke seeds 60001 to 60999, never a count.

Code: `scripts/lab_monthly_worlds.py` (world maker, numpy only) and `scripts/lab_monthly.py` (prototypes and harness; `finders.py` and `referee.py` imported, not edited, settings changed in the lab's process and put back). Rows: `data/panel/monthly/asis.jsonl`, `ways.jsonl`, `base.jsonl`, `passed-over.jsonl`; run lists `queue1.sh` to `queue5.sh`. Worlds: 60 places in groups of five, 4 outcomes, 12 series by place, 4 common; a yearly and half-yearly cycle in every series; months near each other; drifts, steps, spikes; two links a world in half the places.

## Faults found in the harness on review

- Way a2 made `MIN_PAST`, `WARM`, `SPAN`, `OWN` and the finders' `QUIET` months but left `YEARS` at 10, so "holds in 10 scored years" became 10 months. Way **a3** is a2 with `YEARS` 120. It gave the same passes as a2 in every world it was run on (24 nulls, 21 linked), so no a2 number below is changed by the fault.
- `RIDGE` (in place-years) and the baselines' least of three earlier steps were left unscaled. Not tested; listed under not known.
- Two run lines named seeds already used (`asis wander 60101`, `ways none 60501` and `60541`); they were run on fresh seeds instead.
- The season step, the whole-year draw, the calendar-month indexing of way c and the tally were read and found right.

## 1. As they are, where nothing predicts (finished)

360 months, scored from month 216.

| Cell | Worlds with any pass | Floor away, 20 rows: rows passing (single months / whole years) |
|---|---|---|
| season, near (first run) | 7 of 20 | 68 / 66 of 100 |
| **season, near (rerun, 60801–60820)** | **7 of 20** | **55 / 55 of 100** |
| season, no memory | 3 of 20 | 70 / 76 of 100 |
| season changing size by year (0.3; 60881–60892) | 2 of 12 | 37 / 33 of 60 |
| no season (two memories) | 0 of 20 each | 0 of 100 each |
| season, near, a same-month tie | 6 of 18 | 67 of 100 |

**Holds on rerun.** The season makes false passes, whichever bar; every pass names nothing planted (modes rows, t 5 to 14). The floor hides the fault, it does not cure it.

## 2. Ways to read by month (finished)

480 months, scored from 288, lag 1 to 6 by seed. a0 season out only; a1 season out plus month members (lines at 1 to 6 months, three windows, tails at 3 and 6); a2 a1 plus month settings and the whole-year bar; a3 a2 plus `YEARS` 120; a9 a2 with the floor away and 20 rows; by, bh yearly features; c one table a calendar month.

| Links heard (of planted) | a1 | a2 (= a3) | by | bh | c |
|---|---|---|---|---|---|
| steady, share 0.35 | 6 of 6 | 6 of 6 | 5 of 6 | 5 of 6 | 5 of 6 |
| steady, share 0.10 (first 10; **rerun 60851–56: 12 of 12**) | 10 of 10 | 22 of 22 | 2 of 10 | 3 of 10 | 3 of 10 |
| steady, share 0.04 (first 14; **rerun 60861–68: 16 of 16**) | 11–12 of 14 | 29 of 30 | | | |
| steady, share 0.015 (60231–60238) | | 9 of 14 | | | |
| bursts (60601–60606) | 10 of 10 | 10 of 10 | 5 of 10 | 3 of 10 | 9 of 10 |
| three-month windows (60651–60656) | 3–4 of 10 | 9 of 10 | 1 of 10 | 0 of 10 | 10 of 10 |

| Worlds with any pass where nothing predicts | a2 | a3 | a9 (floor away) | by | bh | c |
|---|---|---|---|---|---|---|
| nothing planted | **0 of 54** (30 + rerun 24) | 0 of 24 | **0 of 5** | 0 of 30 | 0 of 30 | 0 of 30 |
| season changing size (0.3) | 0 of 10 | | **0 of 5** | 0 of 12 | 0 of 12 | 0 of 12 |
| same-month tie | 0 of 6 | | | 0 of 6 | 0 of 6 | 0 of 6 |

- **a2 holds on rerun**: no false pass in 24 fresh nulls; every planted link heard at 0.10 and 0.04.
- **a9**: with the floor away and 20 rows sent, the referee alone passed nothing on 10 season-out null worlds (bar 3.3 to 3.5 under either bar). So a2's zero does not rest only on the floor sending little. Ten worlds is few.
- No pass named nothing planted in any linked world, any way. c hears windows best but sends 40 rows every world (bar about 3.4) and is weak on steady links; by and bh are weak on all but share 0.35.
- Seconds a world, one thread, 60 by 480: a2 9 (null) to 17 (linked); c 10 to 13; by, bh 2.

## 3. The baseline to register (finished, unchanged)

Each value less the mean of the same calendar month in all earlier years (at least two), then the referee's six baselines on what is left. Error on the scored months, 4 cells of 6 worlds: 0.59 to 0.96 of each place's spread, against 0.86 to 1.54 for the six as they are and 0.62 to 1.19 for the best plain seasonal rule. The gap of the six as they are is what a seasonal driver falsely "beats".

## 4. Recommendation and the package change

**Way a2 with `YEARS` made months**: settings `MIN_PAST` 24, `WARM` 24, `SPAN` 36, `OWN` 120, `YEARS` 120, finders' `QUIET` 12; the floor and steward as counted; bar by whole years.

The change is `data/panel/monthly/monthly-read.patch`, **not applied**:
- `referee.py`: a list of the settings and `using(settings, level)`, which sets them for a block and puts them back even on failure (an unknown name is refused); `judge` and `label` take `draw`, `settings` and `level_fn`, all `None` by default, and with none given the code path is the counted one.
- `finders.py`: `view` takes `settings` and `quiet` and records the settings on the view; `swarm` runs its members under them.
- New `months.py`: `season_out`, `whole_years`, the month members and `read` (season step, finders, steward, referee with month settings and the whole-year draw).
- New `tests/test_months.py`: yearly boards, rows and judgements (with and without the floor, with shifts) equal, field for field, to those of the counted code read from git at `269b5d8`; settings put back after a read and after a failure; the season step uses earlier dates only; the whole-year draw; a monthly read hears a four-month link and passes nothing on a null. With `CA_COUNTED` set, registered worlds of the finders' count are read again and must give their stored rows. On a scratch copy with the patch applied: 7 passed in 25 s; 4 registered worlds read again, identical.

## 5. The registered count (proposal)

- **Worlds** at the places and months of the real monthly table: where nothing predicts, four panels of 60 (plain, same-month tie, season changing size, gaps and late starts); mark at most 19 of 240 worlds with any pass. Linked: steady at each lag 1 to 6 at shares 0.10 and 0.04, bursts, three-month windows, 60 worlds each (about 360); marks set from the smoke numbers above, less a margin: at least 90% heard at 0.10, 75% at 0.04, 80% for bursts, 70% for windows; passes naming nothing planted in at most 5% of linked worlds. The marks are a proposal and must be committed before any count.
- **Seeds**: a fresh block set aside in the ledger, outside 59001 to 61999.
- **Runtime on this box**, a2 at 120 places by 600 months, one thread: 33 s a null world, 47 to 145 s a linked one (measured, 60701–60703, 60711–60712). About 600 worlds: about 12 hours on one core, 2 hours on six.
- **Memory**: one linked 120-by-600 world peaked at **5.3 GB**, over the 2 GB a process is allowed here (`size.out`). A count at that size needs the memory found and cut first, or at most two processes at once. Not yet located.

## Tried and dropped

Months read as they are (the season passes); ways by and bh (deaf below share 0.35); way c (40 rows always, weak on steady links; worth keeping in mind for windows only); the referee's own past level over hundreds of steps (too slow; the finders' function gives the same numbers to 4e-16).

## Seeds used

First work: 60001–60002, 60101–60120, 60141–60148, 60201–60203, 60211–60216, 60221–60228, 60301–60306, 60351–60356, 60401–60406, 60501–60524, 60541–60551. This work: 60231–60238, 60561–60565, 60571–60575, 60601–60606, 60651–60656, 60701–60703, 60711–60712, 60801–60820, 60821–60844, 60851–60856, 60861–60868, 60881–60892, 60901–60924, 60931–60942. No world for 60106, 60109, 60142, 60144, 60216, 60224, 60231, 60602, 60653 (too few series free of drift).

## Not known

- Whether scaling `RIDGE` and the baselines' least past matters.
- Memory at the real size and where it goes; runtime at the real table's size.
- Shares under 0.015; lags beyond six months; a9 on more than 10 worlds or on linked worlds.
- Gaps, late starts, many zeros, a season that shifts its timing: the maker has none.
- One family of made-up worlds; a real table differs in ways none of this measures.
