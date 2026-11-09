# 0041: After the confirmation missed, the forecast step is changed and confirmed on fields never read, not rescored on Africa

Status: accepted, 2026-11-09. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The one-time confirmation of El Niño against the baseline on Africa's 2000 to 2024 missed (`results/real-enso-drought.md`). Looking at why, on that now-spent period, showed two faults in the forecast step: slopes about three times too large, and a baseline that could not follow a shift in the field's level. Both are fixable. Any fix is now informed by the years that were meant to judge it.

## Decision

- Africa's result stands as a miss. Nothing scored on Africa after it counts as confirmation, whatever it shows.
- The forecast step is changed (`src/causal_atlas/forecast.py`): one slope multiplier chosen on held-out blocks of discovery years; the baseline chosen among three on held-out blocks; region averages as the unit. The first rule's gradient-boosting baseline is dropped, with the numbers that showed it was the weakest written into the new rule.
- The changed method is confirmed once on five continental boxes of the same drought file that this project had never read (`results/real-enso-continents.md`), pooled over the fields where the frozen search names the ONI, with a third pass condition added: the model must also beat each baseline alone.
- False-alarm marks for naming are pooled over the five fields (8 of 100) instead of 2 of 20 per field.

## Why these could favour a result, and what guards against it

- Changing the baseline after a miss could make the driver look better against a weaker one. Guard: the new candidates are stronger than the old on Africa's later years, and the model must beat every one of them alone on the scoring years.
- Pooling fields and choosing which enter could select the favourable ones. Guard: entry is decided by the naming step alone, on discovery years, before any confirmation year is read; all five fields are reported.
- Pooled false-alarm marks are easier to pass than fifteen separate ones. The rate allowed is tighter (8% against 10%).

## Consequences

- If the pooled check passes, the claim is about those fields and years, with the limits in the rule file. Africa is not part of it.
- If it misses, those years are spent as well, and the next step is a judgement about the forecast step itself, not another resizing.
