# 0044: The control copies a year either side of the real alignment are left out

Status: accepted, 2026-11-09. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The fourth iteration (decision 0043, `results/real-indices.md`) stopped at its first step. Among 44 candidates, 26 of them real, the search missed its instrument check (a planted link found in 42 of 50 runs against 45, and in 4 of 10 in South and Southeast Asia) and lost El Niño in one region. By its rule the forecast step was not run and the years after 1999 stay unread for the 25 series.

A look at the fitting years (same file, last section) found the cause. The search judges a candidate against copies of every candidate moved by 1 to 49 whole years, circularly, on a 50-year record, at lags of 0 to 12 months. The copy moved 49 years is the series one year earlier: at lag 12 it is the series itself at lag 0, and at shorter lags it is the series' own near future. The copy moved 1 year, at lag 0, is the series itself at lag 12. A decoy is tied to nothing at any lag, so with one real candidate among decoys this cost little. With many real candidates, each one's real ties at lag 0, and the ties of series that follow the field's driver, were counted as chance and set the bar for all.

## Decision

1. **The controls are the copies moved by 2 to 48 whole years.** The rule behind the numbers: a control's window of lags must not touch the real window, and must leave a year between them, on either side. With lags 0 to 12 that leaves out exactly the moves of 1 and 49. Forty-seven controls per candidate.
2. **Nothing else in the search changes:** the two gates, the lags, the tiles, the stepping down that stops at the first candidate that fails, the cap on leads, the candidates and the fields.
3. **The corrected search is tested as the last one was, on fresh seeds, with the same marks** (`results/real-indices-2.md`): the instrument check on planted links, El Niño kept, decoys and mixed years quiet. Only if all hold is the forecast step run, once, as written in `results/real-indices.md`.
4. **The forecast step is not changed.** Its own control gives each year another year's driver values, 24 moves on 25 years, and the moves next to zero have the same weakness: for a real series they are not pure chance. Left in, they can only make a pass harder. Changing a mark on the scoring side after a miss is the kind of change that could favour a result, so it stays as it was and the weakness is stated as a limit.

## Considered and not done

- **A wider gap** (also leaving out 2 and 48, or 3 and 47). Looked at on seven runs of the fitting years: the bars move little. The narrowest change that the reasoning supports was taken.
- **Judging each candidate against its own copies only.** With 47 copies the smallest chance a candidate can show is about 1 in 48, which cannot be corrected for 44 candidates. The shared bar is what makes the correction possible.
- **Not stopping at the first candidate that fails.** The stop is what holds the false-alarm rate across candidates. With the controls corrected the bar is no longer set by real ties, and the stop is left alone.

## Consequences

- The choice of controls could favour a result: fewer and weaker controls mean a lower bar. The guards are the false-alarm marks on fresh seeds, and the forecast step on years no series but the ONI has been set against.
- The second naming is not blind. The real series are the same and the author has seen, on seven runs, what clears the bar with the two moves left out. Stated in both results files.
- Earlier results used all 49 moves. Their namings passed a test at least as strict in the sharp gate, and stricter in the broad gate in six of the seven runs looked at, and stand; their false-alarm counts belong to the stricter controls.
- A series that repeats itself at a period of whole years (the stratospheric wind does, nearly) still meets copies of itself among its controls. If such a series really drove a field it would not be named, and it would raise the bar for others. Known, and not addressed here.
