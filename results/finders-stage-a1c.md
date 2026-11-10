# The label counted: does "may be moving together" mark the shared slow paths, and leave the planted leads alone?

Rule first, committed before any counted seed (rule 9). Stage A1 of `docs/plan-finders-and-referee.md`, a third count, of the label only. Authority: decisions 0040, 0055 to 0057, 0059, 0060 and 0061. Code: `src/causal_atlas/referee.py`, `scripts/run_referee_c.py` (which uses `scripts/run_referee.py` and `scripts/run_referee_b.py`), `synth/table_panel.py`, `synth/shared_paths.py`; tests in `tests/test_referee.py`. Seeds: `results/seed-ledger.md`. Rows: `results/finders-stage-a1c.jsonl`, one a world.

Made-up tables only. No real series is read.

## Why

The second count (`results/finders-stage-a1b.md`) found that the referee passes a series and an outcome that only move slowly together, and its rule says no real table is read until a pass carries a label that tells the two apart, registered and counted on fresh worlds. Decision 0061 is that label. A pass is labelled "may be moving together" when the same proposal turned round (the outcome a year before, for the series) stands by a lower mark, or when it is at least as strong read in the same year. The label is not charged in the bar and cannot make or unmake a pass, so nothing the first two counts said of passes changes.

Two questions, each with a mark:

1. Of the passes that are only a shared slow path, how many go unlabelled? Those are the ones a reader would take for a lead.
2. Of the passes that are a planted lead, how many are labelled? Those are real leads marked down.

And it is counted at three sizes of table, the middle one (240 places) near the real yearly table's 218, which no count has had.

## What has been looked at

The label was shaped on 257 smoke worlds, seeds 32041 to 32099, 32121 to 32201, 32213 to 32300 and 32521 to 32552 (decision 0061, with what they gave). Those seeds are never counted. The second count's worlds (33001 to 37830) were looked at after their count, which is where the lower mark was first seen; they are spent and are not read here. No world with a seed from 38001 on has been made.

The path shapes are the helper's seven of the second count. They are no longer unseen: this session has now seen passes on all of them, and the label was shaped on five of the seven at 120 and 480 places and on all seven at 240.

## The worlds

`synth/table_panel.py` as before: forty series by 60 years, places in groups of five, finders see years 0 to 34, the referee scores years 35 to 59. Three sizes, numbered j = 0, 1, 2: **120 places** with links at 35%; **240 places** with links at 35%; **480 places** with links at 20%.

**A shared slow path added to a no-link world** by `shared_paths.add`, as in the second count: two pairs, each an outcome and a series of the place's own, on one path in half the groups; nothing leads. Seven kinds numbered i = 0 to 6 in the order waves, cycle, boom, wander, regimes, quasi_cycle, mixed.

| Panel | Worlds | Seeds |
|---|---|---|
| `path_<kind>_<places>` | 30 | 38001 + 1000j + 100i to 38030 + 1000j + 100i |

**Where a link is planted,** three links a world, nine kinds numbered i = 0 to 8 in the order steady, threshold, extremes, pair, flip (sign differing by place), flip_state (sign by a third series' state), many (many weak), hidden (hidden mover), shared (from a series common to all places).

| Panel | Worlds | Seeds |
|---|---|---|
| `<kind>_<places>` | 20 | 41001 + 1000j + 100i to 41020 + 1000j + 100i |

**A lead and a path in one pair.** A linked world, and the first link's own outcome and first series are also given one slow path, in that link's places, by `beside` in the harness (this session's composition, from the helper's path makers). Three kinds numbered i = 0 to 2: steady with a cycle, steady with a wander, hidden mover with a wander.

| Panel | Worlds | Seeds |
|---|---|---|
| `<kind>+<shape>_<places>` | 15 | 44001 + 1000j + 100i to 44015 + 1000j + 100i |

1,305 worlds: 630 with a shared path, 540 with links, 135 with both in one pair. Each is read once; the script will not read a world a second time.

## What is sent

Forty proposals a world, under one bar, as in the second count but with no turned-round proposal sent (the referee now reads that itself, outside the bar):

- **With a shared path:** each of the two pairs on a path sent five ways (all places, by claim, the quarter and the half of the groups where the series went most with the outcome in the early years, and the places the path is truly in). The keen proposer fills the rest.
- **With links, and with a lead and a path:** each answer three ways (the link's own places, all places, by claim). The keen proposer fills the rest.

Every pass carries the referee's label. A keen pass is tagged afterwards as naming a path's pair, the pair with both a lead and a path, a planted input, a near copy of one, or none of these.

## Marks

Counted in worlds, at each size of table apart. Each limit is the count a true rate of 1 world in 20 would exceed less than 3 times in 100.

1. **A shared path is not left looking like a lead.** Of the 210 path worlds at each size, those in which any pass of a path's pair (sent directly in any of its five ways, or by the keen proposer) carries no label: **at most 17**.
2. **A planted lead is not marked down.** Of the 180 linked worlds at each size, those in which any pass of a planted link (its answer in any of its three ways, or a keen proposal that names a planted input) carries the label: **at most 15**.

**If mark 1 fails at a size,** the label misses shared movement at that size and this file says how often and for which shapes. A pass without the label is then not to be called a lead at that size of table; Stage B's rule would have to carry the weight, by putting the table's main shared movements in the baseline, and whether the label is changed again is decided on smoke seeds.

**If mark 2 fails at a size,** the label is too keen there: it would mark down real leads, and this file says for which kinds. The label is then reported as "cannot be told apart at this size" for those kinds, not as "moves together".

**Whatever the marks,** the words stay as the second count left them: a pass means the forecast improves; an unlabelled pass means the series comes first in time, never that it causes.

## Expected, said beforehand

- Mark 2 is expected to hold at every size. On smoke worlds one pass of a lead in 343 was labelled, and none of 95 through the harness.
- Mark 1 is expected to hold at 120 and at 480 places (no smoke world of 81 with a path pass left unlabelled). **At 240 places it is not known:** 2 of 35 smoke worlds had one, both on cycles, and 2 in 35 is about the rate the mark allows.
- Path worlds with any pass at all: few at 120 places, most at 480, as the second count found. Mark 1 counts worlds of all 210, so at 120 places it is held mostly by the referee refusing the path, and the label's own share is in the table beside.

## Measured beside, no mark

- Of path passes, the share labelled, by kind of path and size, and by which reading (turned round, same year).
- Of lead passes, the share labelled by kind of link and size. Passes whose inputs are all one series common to all places cannot be turned round; they are counted apart.
- **A lead and a path in one pair:** how often the link's pass is labelled. Both are true there, so there is no right answer and no mark. It says how often a label sits on a pair that also holds a lead.
- **The ceiling at 240 places:** the answer sent for the link's own places, how many of 60 links a kind pass. The first measure at the size of the real table. (Twenty worlds a kind, so it is rougher than the first two counts' 90 links.)
- Keen passes that name neither a path's pair nor a planted input nor a near copy; the bar; seconds a world.

## Limits, whatever the counts

- One family of worlds, and the referee and its label were shaped on it, three times now.
- Seven shapes of path, all seen before this count. A real table's slow movements are not bound to be like any.
- The made-up links act a year later and not within the year. A real link that acts in both will be labelled by the same-year reading (decision 0061, point 4); nothing here measures how often.
- Every lag here is one year.
- The directly sent pairs and the answers are handed over by a script that knows the layout. They measure the referee and its label, not any finder.
- The label cannot see an unrecorded thing that moves the series first and the outcome later: that is unlabelled, and is a lead in time and not a cause.
