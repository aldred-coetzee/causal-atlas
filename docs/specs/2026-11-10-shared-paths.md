# Brief for a helper: shared slow paths for the made-up tables

Written by the project session before the helper was started. Estimated cost stated beforehand: about 80,000 fresh tokens; the helper stops and reports at about 150,000 by its own estimate, finished or not.

## Why you and not the project session

Rule 3 of this project: the generator of made-up records shares no code and no assumptions with whatever is tested on them. A referee now exists and was shaped by the project session, which has also tried a few shapes of shared path of its own on it. So that the counted test holds shapes the referee was not shaped on, you choose them, and you never see the referee.

Do not open anything under `src/`, `scripts/`, `results/`, `docs/decisions/`, `docs/plan-finders-and-referee.md` or `STATUS.md`. You may read `synth/table_panel.py` and `tests/test_table_panel.py`, and `docs/specs/2026-11-10-made-up-tables.md` (the brief the table generator was written from). Nothing else in the repo is needed.

## The matter

A real yearly record of a place often carries something slow that nobody recorded (an economy growing, a technology spreading, a climate regime) and that moves two of the place's series together over the decades. One series then seems to tell about the other although neither moves the other. `table_panel.make` already plants one such thing: a line plus a curve shared by two outcome series and two local series (see its nuisances). You add others, of other shapes.

## What to write

`synth/shared_paths.py`, numpy only, and `tests/test_shared_paths.py` (pytest; it adds `synth/` to `sys.path` as `tests/test_table_panel.py` does).

    KINDS            a tuple of the names of your kinds of path
    FORESEEABLE      a dict, kind -> bool (see below)
    add(world, seed, kind, strength=1.0, pairs=2, frac=0.5)

- `world`: what `table_panel.make` returns, of any kind and size. It is not modified. `add` returns a new dict with the same keys (arrays copied where changed) and one more, `paths`: a list, one entry a pair, each with `outcome` (series index), `series` (series index of a local input), `places` (bool array), `kind`, and `sign` (+1 or -1: whether the series carries the path the same way up as the outcome).
- For each of `pairs` pairs: one outcome series and one local series, no series used twice, none that is an outcome or an input in `world["truth"]`. Places: `frac` of the groups, whole groups, drawn for each pair.
- In each of those places draw a path over the years, the place's own (its own parameters or its own draws), and add it to both series in that place in the same years: to each, the path times that series' own spread in that place (as the series stood before) times `strength` times a size that differs by place. With `strength=1` the path's own spread over the record should be, in the middle place, about one and a half times the series' spread about it; some places well under, some two or three times.
- Nothing leads: the path's value for year t goes into both series at year t. Nothing else is shared between the two series; their year-to-year departures from the path stay as they were.
- `kind`: one of `KINDS`, or `"mixed"`, where each place draws its kind.
- **The kinds are yours to choose: at least six.** What a country's yearly record could plausibly carry over sixty years. None may be a straight line or a line plus a single bend alone: `table_panel` has that. Among them there must be at least two whose next value could be told closely from the path's own earlier values by someone who knew the formula (a path with no fresh movement of its own), and at least two that keep some fresh movement of their own every year or every few years (so that the path's own past never quite gives its next value), while still being slow against the year-to-year roughness of the series. `FORESEEABLE[kind]` says which is which. Say in the docstring of each what real thing it stands for.
- NaN stays NaN. `strength=0` returns values equal to the input's.
- Same arguments, same output, byte for byte. Use `numpy.random.SeedSequence([seed, <a number of your own>]).spawn` with a stream each for the choice of pairs, the places and the paths, so that it shares no stream with `table_panel`.
- Under a key `_paths`, for the tests only: the path added to the outcome of each pair, as (places, years), zero outside its places. Say so in the docstring.

## Tests to write

- Same arguments twice give identical arrays; another seed differs; the input world's arrays are unchanged.
- Only the named series in the named places differ from the input, and whole groups are in or out.
- For each kind: what was added to the outcome and what was added to the series are the same path up to scale and the stated sign (correlation over the years of plus or minus one in each place).
- For each kind: the path is slow (you choose a fair measure, for instance its year-to-year change against its range over the record, and state it), and its size in the middle place is as asked.
- For each kind: `FORESEEABLE` is true to the path. One way: fit the path's own formula, or a smooth curve of a few terms, to its first forty years and see how far it stands from the next ten; a foreseeable kind should stand close, the other kind not.
- `mixed` uses several kinds; `strength=0` changes nothing; NaN is kept; no series of `truth` is used.

Keep the tests under about 20 seconds in total.

## Rules

- Write only `synth/shared_paths.py` and `tests/test_shared_paths.py`. Change no other file. Do not commit, push, install anything, or use the network.
- Python: `.venv/bin/python` from the repo root. Run your tests with `PYTHONPATH=src OMP_NUM_THREADS=2 nice -n 19 .venv/bin/python -m pytest -q tests/test_shared_paths.py tests/test_synth_isolated.py`. Do not run the rest of the suite: another change is in progress in the working tree and some other tests fail for now.
- Match the house style of `synth/table_panel.py`: short functions, a one-line docstring that says what and why, comments only where a choice is not obvious, no classes unless needed.
- No job you wait on runs longer than about four minutes.

## What to send back

A short report as your final message: the kinds you chose, one line each on what it stands for and whether it is foreseeable; every place where you had to choose something this brief did not settle (and what you chose); the test results; and anything in this brief that turned out to be wrong or impossible as written.
