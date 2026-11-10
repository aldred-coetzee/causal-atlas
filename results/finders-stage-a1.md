# The referee on made-up tables: does it pass what is not there, and what can it hear when handed the answer?

Rule first, committed before any counted seed (rule 9). Stage A1 of `docs/plan-finders-and-referee.md`: tests of the test. Authority: decisions 0040, 0055 to 0057 and 0059. Code: `src/causal_atlas/referee.py`, `scripts/run_referee.py`, `synth/table_panel.py`, tests in `tests/test_referee.py` and `tests/test_table_panel.py`. Seeds: `results/seed-ledger.md`. Rows: `results/finders-stage-a1.jsonl`, one a world.

Made-up tables only. No real series is read.

## Why

Every later stage rests on the referee: finders of any kind propose, and it alone decides what counts as found. So before any finder is built, two things are measured about it. Does it pass things in worlds where nothing predicts, when it is sent the forty proposals that fitted the early years best? And when it is handed the planted link itself, how often does it hear it? The second sets the ceiling: a finder cannot be blamed for a link the referee would not pass even when told.

## What has been looked at

The referee was shaped on smoke worlds from the same generator, seeds 27001 to 27086 (decision 0059, with what they gave). Those seeds are never counted. No world with a seed from 28001 on has been made.

## The worlds

`synth/table_panel.py`, written by a helper that never saw the referee. Forty series by 120 places by 60 years: 8 outcomes, 24 series of each place's own, 8 shared by all places. Places come in groups of five. A linked world plants three links of one kind, a year ahead, in the same quarter of the groups, at a stated share of what the outcome's own history leaves unexplained. Finders see years 0 to 34; the referee scores years 35 to 59.

**Where nothing predicts, 100 worlds each:**

| Panel | What | Seeds |
|---|---|---|
| none_plain | no link, no nuisance | 28001 to 28100 |
| none | no link; drift, a step, shared shocks, near copies, a change part-way, at the usual strength | 28101 to 28200 |
| none_strong | the same at twice the strength | 28201 to 28300 |
| none_rough | the same, with twice the spikes | 28301 to 28400 |
| none_gaps | the same, a tenth of the values missing | 28401 to 28500 |
| same_year | series move with outcomes in the same year, 35%; nothing leads | 28501 to 28600 |

**Where a link is planted, 30 worlds (90 links) a panel**, nine kinds, numbered 0 to 8: steady; threshold; extremes; pair; sign differing by place; sign differing by the state of a third series; many weak; hidden mover; steady from a series shared by all places. For kind i:

| Panel | What | Seeds |
|---|---|---|
| `<kind>_35` | 35%, 120 places | 29001 + 100i to 29030 + 100i |
| `<kind>_20` | 20%, 120 places | 30001 + 100i to 30030 + 100i |
| `<kind>_20_wide` | 20%, 480 places | 31001 + 100i to 31030 + 100i |

1,410 worlds. Each is read once; the script will not read a world a second time.

## What is sent

Forty proposals a world, under one bar.

- **The answer**, in linked and same-year worlds: each planted link in the form its kind calls for, sent three ways: for the places it is in; for all places; and by claim (each place's own past decides whether it applies). Up to nine of the forty.
- **A keen proposer** fills the rest, from the early years alone and knowing nothing of what was planted: half are the single-series slopes that fitted best over all places; half are the slopes that fitted best in the quarter of the groups where the series went most its pooled way, sent for those groups. It stands in for the worst a finder could do by choosing. Each of its proposals is tagged afterwards by the script, which knows the truth: it names a planted input of its outcome, its series is a near copy of one, or neither.

## Marks

1. **False passes.** On each panel where nothing predicts, at most 9 of 100 worlds have any pass at all; over the six, at most 40 of 600. On same_year the answers count: a same-year link passed a year ahead is a false pass. (At a true rate of 1 world in 20, ten or more of 100 comes about 3 times in 100, and more than 40 of 600 about 3 times in 100.)
2. **False passes beside real links.** Over the 810 linked worlds, at most 55 have a keen proposal pass that names neither a planted input nor a near copy of one.
3. **The ceiling.** For each of the nine kinds at 35%, the answer sent for the link's own places passes for at least 72 of the 90 links. A kind that does not is recorded as "could not be heard at this size of table", and no finder in a later stage is blamed for missing that kind at that size.
4. **No leak.** `tests/test_referee.py::test_no_later_year_reaches_an_earlier_score` holds for all twelve of its proposals on the commit that is counted.

If mark 1, 2 or 4 fails, the referee is not valid: nothing is built on it, the fault is found on smoke seeds, and the stage is run again on fresh seeds with this file saying so. Mark 3 is a measurement and cannot fail the referee; it says what can be asked of finders.

## Measured beside, no mark

- The same ceiling at 20%, and at 20% with four times the places.
- The answer sent for all places, and by claim: what not knowing where costs.
- The keen proposer's set proposals that name a planted input: how many pass, and how much of each passed set lies in the link's places. A first look at whether where a link holds can be found from the early years. It is one simple proposer, not a finder's test.
- The size reported for passed answers against the share planted. A passed size is the smaller of two forms and is of the squared error in each place's usual-error units, so it is not the planted share and is expected below it.
- The bar, and seconds a world.

## What it could change, said beforehand

- Kinds under the ceiling at 120 places and over it at 480: the yearly country table is too narrow for those kinds, and the data work that follows favours more places (sub-national series) for them.
- Kinds under it at both: finders for that kind are not built until the referee or the table changes.
- If the answer for all places stays unheard where the answer in its places passes, Stage A2's first finder is one that proposes where, not only what.

## Departures from the plan

- The plan named nuisance kinds one at a time (drift, step, near copies, a change part-way). The generator gives them together at a strength, so the panels vary strength, roughness and gaps.
- The plan sent one answer among thirty-nine other proposals. Here up to nine answers (three links, three ways) are among forty. The bar is over all forty either way.
- The keen proposer names sets of places as well as all places. It is not kept from the planted pairs: it may find them, and that is counted apart.
- Two kinds and one size are additions: the sign differing by the state of a third series, a link from a shared series, and the wide worlds.
- The referee itself: decision 0059.

## Limits, whatever the counts

- The referee has seen worlds from this generator, though not these. A pass here is on new worlds of one family. Real records have been rougher than made-up ones each time they were compared.
- Links of one world share their places and the bar, so 90 links are not 90 independent trials; intervals are taken over worlds.
- One length of record (60 years, 25 scored), one number of series (40), links one year ahead, in a quarter of the places.
- The ceiling is for the form the generator planted. A real link need not have one of these forms.

## Result

Not yet run.
