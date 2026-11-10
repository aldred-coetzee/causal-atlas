# The referee counted again: is the shared-curve hole closed, what does it do with a shared slow path, and what did closing it cost?

Rule first, committed before any counted seed (rule 9). Stage A1 of `docs/plan-finders-and-referee.md`, a second count after decision 0060. Authority: decisions 0040, 0055 to 0057, 0059 and 0060. Code: `src/causal_atlas/referee.py`, `scripts/run_referee_b.py` (which uses `scripts/run_referee.py`), `synth/table_panel.py`, `synth/shared_paths.py`; tests in `tests/test_referee.py`, `tests/test_referee_b.py`, `tests/test_shared_paths.py`. Seeds: `results/seed-ledger.md`. Rows: `results/finders-stage-a1b.jsonl`, one a world.

Made-up tables only. No real series is read.

## Why

The first count (`results/finders-stage-a1.md`) held every mark and measured one hole: a curving drift shared by a series and an outcome passed as if it were a link, at twice its usual strength and, with four times the places, at its usual strength. Nothing real is to be read until that is closed. Decision 0060 changed the referee to close it: a baseline chosen for each place, a recent line among the baselines, and a check on what was new in the inputs. A changed referee is a new referee, so its tests of the test are counted again on fresh seeds, and three things are asked of it:

1. Does it still pass things where nothing predicts, now with the pairs that share the generator's curving drift sent to it directly, and with four times the places (which the first count did not have for no-link worlds)?
2. What does it do with a slow path shared by a series and an outcome, of shapes it was not shaped on?
3. What did closing the hole cost of what it can hear?

## What has been looked at

The referee was changed on smoke worlds from `synth/table_panel.py` and on shapes of this session's own, seeds 32001 to 32810 (decision 0060, with what they gave). Those seeds are never counted. No world with a seed from 33001 on has been made.

The shapes of question 2 are in `synth/shared_paths.py`. A helper that never saw the referee chose and wrote them, to a brief committed before it started (`docs/specs/2026-11-10-shared-paths.md`). This session read the helper's code against its brief and ran its tests. It has run the referee on three such worlds (smoke seeds) to learn the seconds a world takes, with nothing else printed, and on one more inside a test that checks only that forty proposals are sent and labelled. No pass or score on any of those shapes has been seen. The script refuses to print one before the count.

## The worlds

`synth/table_panel.py` as in the first count: forty series by 120 places by 60 years, places in groups of five, finders see years 0 to 34, the referee scores years 35 to 59. Wide worlds have 480 places.

**Where nothing predicts:**

| Panel | What | Worlds | Seeds |
|---|---|---|---|
| none | no link; drift, a step, shared shocks, near copies, a change part-way, at the usual strength | 100 | 33001 to 33100 |
| none_strong | the same at twice the strength | 100 | 33101 to 33200 |
| none_plain | no link, no nuisance | 50 | 33201 to 33250 |
| none_rough | twice the spikes | 50 | 33301 to 33350 |
| none_gaps | a tenth of the values missing | 50 | 33401 to 33450 |
| same_year | series move with outcomes in the same year, 35%; nothing leads | 50 | 33501 to 33550 |
| none_wide | as none, 480 places | 100 | 33601 to 33700 |
| none_strong_wide | as none_strong, 480 places | 100 | 33701 to 33800 |

**A shared slow path added to a no-link world** by `shared_paths.add`: two pairs, each an outcome and a series of the place's own, get one path in half the groups of places, the place's own draw of it, in the same years, about one and a half times each series' own spread in the middle place. Nothing leads. Seven kinds, numbered 0 to 6. The helper marks three as foreseeable (the path's next value could be told from its own past by someone who knew its formula): **waves** (two S-curves a few decades apart), **cycle** (a cycle of fixed period, 18 to 45 years, its strength changing steadily), **boom** (one smooth hump). Three keep fresh movement of their own: **wander** (a random walk, lightly smoothed), **regimes** (levels shifting about every dozen years), **quasi_cycle** (a cycle whose phase wanders). And **mixed**: each place draws its kind. For kind i:

| Panel | What | Worlds | Seeds |
|---|---|---|---|
| `path_<kind>` | 120 places | 40 | 34001 + 100i to 34040 + 100i |
| `path_<kind>_wide` | 480 places | 40 | 35001 + 100i to 35040 + 100i |

**Where a link is planted, 30 worlds (90 links) a panel**, the nine kinds of the first count in its order. For kind i:

| Panel | What | Seeds |
|---|---|---|
| `<kind>_35` | 35%, 120 places | 36001 + 100i to 36030 + 100i |
| `<kind>_20_wide` | 20%, 480 places | 37001 + 100i to 37030 + 100i |

1,700 worlds: 600 where nothing predicts, 560 with a shared path, 540 with links. Each is read once; the script will not read a world a second time.

## What is sent

Forty proposals a world, under one bar.

- **Where nothing predicts:** the two pairs to which the generator gives one curving drift, each sent four ways: for all places; by claim; and for the quarter and the half of the groups where the series went most with the outcome in the early years, which is what a finder of where would name. (On none_plain there is no drift and the same two pairs are sent all the same.) On same_year also the answers, as in the first count, and each turned round. A keen proposer fills the rest as in the first count.
- **With a shared path:** each of the two pairs on a path sent those four ways and for the places the path is truly in; and turned round (the outcome a year before, for the series) in those places. Twelve of the forty. The keen proposer fills the rest; its proposals are tagged afterwards as naming a path's pair, one of the generator's drift pairs, or neither.
- **With links:** each answer three ways as in the first count; and turned round in the link's places where its first input is a series of the place's own. The keen proposer fills the rest.

## Marks

1. **False passes where nothing predicts.** On each of the eight panels, the worlds with any pass at all are at most 9 of 100, or 6 of 50; over the eight, at most 40 of 600. On same_year the answers and their turned-round forms count. (Each limit is the count a true rate of 1 world in 20 would exceed less than 3 times in 100.)
2. **A foreseeable shared path is refused.** Over the three foreseeable kinds, the worlds in which a path's pair passes forwards (sent directly in any of its five ways, or by the keen proposer) are at most 11 of 120 at 120 places, and at most 11 of 120 at 480 places.
3. **Nothing else passes beside a path or a link.** Worlds with a keen pass that names neither a path's pair, nor a planted input, nor a near copy of one: at most 38 of the 560 with a path, and at most 37 of the 540 with links.
4. **The three kinds the first count heard are still heard.** At 35% and 120 places, the answer sent for the link's own places passes for at least 72 of 90 links, for each of: steady, sign differing by place, hidden mover.
5. **No leak.** `tests/test_referee.py::test_no_later_year_reaches_an_earlier_score` holds for all its proposals on the commit that is counted; it covers the check as well as the two reads held to the bar.

**If mark 1, 3 or 5 fails, the referee is not valid:** nothing is built on it, the fault is found on smoke seeds, and it is counted again on fresh seeds with this file saying so.

**If mark 2 fails, the hole is not closed for that shape of path and this file says so.** The referee is then published as one that passes shared slow movement it should refuse; no real table is read until a pass carries the label of mark 2's remedy, the turned-round read measured below, and Stage B's own rule puts the table's main shared movements in the baseline. Whether to change the referee again is decided then, on smoke seeds, with the knowledge that these shapes are no longer unseen.

**If mark 4 fails for a kind,** closing the hole cost that kind at this size of table, and it is recorded with the others that cannot be heard.

## Expected, said beforehand

- Marks 1, 3, 4 and 5 are expected to hold, from the smoke worlds of decision 0060.
- Mark 2 is not known. Waves and boom are like shapes the referee refused on smoke seeds. The cycle can be as short as 18 years, shorter than any wave tried, and a line through a place's last fifteen years cannot follow that; it may pass, and more so with 480 places.
- The three kinds with fresh movement of their own are **expected to pass often**, and decision 0060 (point 4) says why that is counted as hearing a hidden mover and not as a false pass: the series a year before is a second reading of where the unrecorded thing now stands, which the outcome's own past cannot give. They are measured, with no mark.

## Measured beside, no mark

- **The turned-round read.** For each pair on a path, and each link whose first input is a series of the place's own: of those that pass forwards in their true places, how many pass turned round as well. If a shared path passes both ways and a link passes one way, a both-ways pass can be labelled "these move together" and kept apart from "this leads that". This is the measure of that label, on worlds where the answer is known.
- The six kinds not under mark 4, at 35%; and all nine at 20% with four times the places, beside the first count's figures (at 35%: shared-series 64, pairs 63, thresholds 55, extremes 52, many weak 48, sign by a third series' state 21, of 90).
- What the check on what was new removed: proposals that passed the two reads held to the bar and failed the check, for path pairs, drift pairs and answers.
- The generator's drift pairs sent directly: passes by way, by panel.
- The answer sent for all places and by claim; the keen proposer's passes that name a planted input; the bar; seconds a world.

## Limits, whatever the counts

- One family of worlds (`synth/table_panel.py`), and the referee was shaped on it, twice now.
- The path shapes are a helper's and unseen, and there are seven of them. A real table's slow movements are not bound to be like any.
- The paths are added to no-link worlds only: nothing here says how a link is heard beside a shared path in the same series.
- The directly sent pairs and the answers are handed over by a script that knows the layout. They measure the referee, not any finder.
- At twice the generator's drift and four times the places, one smoke world of twelve had a drift pair pass (decision 0060). Mark 1's panel none_strong_wide counts that case.

## Result

Not yet counted.
