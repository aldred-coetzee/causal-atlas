# Brief for a helper: the made-up tables for Stage A

Written by the project session before the helper was started. Estimated cost stated beforehand: about 150,000 fresh tokens; the helper stops and reports at about 250,000 by its own estimate, finished or not. Plan: `docs/plan-finders-and-referee.md`, section "The made-up tables". Read that section and this brief; nothing else in the repo is needed.

## Why you and not the project session

Rule 3 of this project: the generator of made-up records shares no code and no assumptions with whatever is tested on them. The referee and the finders do not exist yet and you will never see them. Do not import anything from `src/causal_atlas`. Do not read `synth/harvest_panel.py` or the other generators for ideas: write this one from this brief.

## What to write

`synth/table_panel.py`, numpy only, and `tests/test_table_panel.py` (pytest; it adds `synth/` to `sys.path` as `tests/test_synth_isolated.py` does, which you may read for that one line).

    make(seed, kind, share=0.35, places=120, years=60, outcomes=8, local=24, shared=8,
         links=3, frac=0.25, source="local", flip="place", rough=1.0, nuisance=1.0, gaps=0.0)

returns a dict:

- `values`: float array (series, places, years). Series order: outcomes, then local inputs, then shared inputs. A shared series has the same value in every place.
- `role`: array of strings, one a series: `outcome`, `local`, `shared`.
- `group`: int array (places,): which group a place is in. Groups of 5 places (24 groups at the default size); they stand for regions or countries.
- `truth`: a list, one entry a planted link: `outcome` (series index), `inputs` (list of (series index, years ahead)), `places` (bool array), `kind`, and what the kind needs to be stated exactly (the level, the sign by place, the state series, the weights, the members of a mode). `predicts` (bool): whether knowing the inputs before the year helps predict the outcome. `changes` (bool): whether changing the inputs would change the outcome.

Nothing else, and no year split: that is the harness's business.

Same arguments, same world, byte for byte. Use `numpy.random.SeedSequence(seed).spawn` so that each part (base series, nuisances, links, roughness, gaps) has its own stream and adding an option later does not change the others.

## The base world, in every kind

- Every series in every place: its own mean and spread, and memory from one year to the next (a coefficient drawn per series between 0.2 and 0.7), run in for 50 years before the first kept year.
- Year-to-year shocks are part shared within a group (about 30% of their variance) and, for outcomes, a little shared by all places (about 5%).
- **Rough, as real records are** (scaled by `rough`; 0 turns it off): shocks from a heavy-tailed law (Student t, 4 degrees of freedom, scaled to unit variance); each place-and-series spread drawn log-normally so a few places are three or four times rougher than the middle; about 1% of values hit by a one-year spike of several spreads.
- **Nuisances** (scaled by `nuisance`; 0 turns them off), none of which is a link:
  - a slow drift in about a third of the series: a line plus a curve, by place, and **for two outcome series the same curving drift is shared with two local input series** in the same places (their year-to-year departures unrelated);
  - a step in level part-way, in about a tenth of the place-series;
  - two local series that are near copies of two others (the other plus a tenth of its spread in noise);
  - a change of behaviour part-way in about a fifth of the places: memory and spread both change at a year between 25 and 45.
- Shared inputs: one series each, the same everywhere; two of them with long memory (0.85 to 0.95), as an ocean index has.
- `gaps`: that share of local and outcome values set to NaN at random, never in shared series. Default none.

## The planted links

`links` links of the one `kind`, each on a different outcome series, each in the same set of places: `frac` of the groups, whole groups. The input is a local series unless `source="shared"`. Never use a drifting or near-copy series as a planted input or outcome.

How strong: in a linked place the outcome's year-to-year shock is `sqrt(1 - share) * its own shock + sqrt(share) * signal`, both in units of that place's shock spread, where `signal` has mean zero and unit variance over the linked place-years. So the outcome's shock variance is unchanged and `share` of it comes from the link. The signal by kind (z means: the series as its departure from its own mean in its own spreads, in that place):

| `kind` | signal for year t | `predicts` | `changes` |
|---|---|---|---|
| `steady` | z of the input at t-1 | yes | yes |
| `threshold` | the part of z(t-1) above its 80th percentile, zero below; centred and scaled | yes | yes |
| `extremes` | 1 when z(t-1) is above its 90th percentile, else 0; centred and scaled | yes | yes |
| `pair` | z of input A at t-1 times z of input B at t-1; centred and scaled. A and B unrelated | yes | yes |
| `flip` | z(t-1) times a sign: by place, half the linked places each way (`flip="place"`), or the sign of a shared series at t-1 (`flip="state"`) | yes | yes |
| `many` | a hidden series h for each place (unit variance, memory 0.3), seen by nobody; twenty local series each have a tenth of their variance from h in the same year; signal is h at t-1 | yes | no |
| `hidden` | a hidden h as above; one local series has half its variance from h in the same year; signal is h at t-1 | yes | no |
| `same_year` | the input's own shock at t (the part of it at t that nothing before t predicts) | no | no |
| `none` | no link; `truth` is empty | | |

For `many` the truth's inputs are the twenty series, with equal weights. Percentiles are taken over that place's whole made-up record: this is the generator, it may know the future.

## Tests to write

- Same seed twice gives identical arrays; a different seed differs.
- For each kind except `none` and `same_year`, over several seeds: in linked places, the share of the outcome's shock variance that the stated signal accounts for is within a tolerance of `share`; in unlinked places and for unlinked outcomes it is near zero. (Return the shocks under a key `_shocks` for the tests only, and say so in the docstring.)
- `same_year`: the input at t-1 has no relation to the outcome's shock at t beyond chance.
- `none`: `truth` is empty; shared series are identical across places; groups have five places.
- `rough=0, nuisance=0` gives shocks with no heavy tail (kurtosis near 3) and no drift.
- `gaps=0.05` gives about 5% NaN in local and outcome series and none in shared ones.

Keep the tests under about 20 seconds in total.

## Rules

- Write only `synth/table_panel.py` and `tests/test_table_panel.py`. Change no other file. Do not commit, push, install anything, or use the network.
- Python: `.venv/bin/python` from the repo root. Run your tests with `PYTHONPATH=src OMP_NUM_THREADS=2 nice -n 19 .venv/bin/python -m pytest -q tests/test_table_panel.py`.
- Match the house style of the repo's code: short functions, a one-line docstring that says what and why, comments only where a choice is not obvious, no classes unless needed.
- No job you wait on runs longer than about four minutes.

## What to send back

A short report as your final message: what the file does, every place where you had to choose something this brief did not settle (and what you chose), the test results, and anything in this brief that turned out to be wrong or impossible as written.
