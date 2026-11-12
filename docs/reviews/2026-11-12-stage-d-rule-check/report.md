# Stage D rule check: independent reader, 2026-11-12

Scope: `results/stage-d-monthly-read.md`, decision 0069, `scripts/run_stage_d.py`, `tests/test_stage_d.py`, `src/causal_atlas/{months,finders,referee}.py`, `docs/tied-series.md`, `data/manifest.toml`. Nothing under `data/panel/`, `data/table/` or `data/raw/` was opened, and no step of `run_stage_d.py` was run on the real table. Checks were run on made-up arrays only: `check.py` beside this file, with seeds 59001 to 59006, under `ulimit -v 4000000`. The 14 tests pass.

## Faults to fix before any run

1. **False leads are neither counted nor reported** (`run_stage_d.py` `table()` 293-322, `reading()` 204-222; sure). The rule (line 31) says a lead on drought, storms or earthquakes "is counted as a false lead and reported as such, in the real read as in the placebos". No code checks what kind of outcome a lead has. A real lead on SPEI would print as `LEAD` like any other. In the placebos it only counts as "any lead", which already fails the mark. To fix: tag each board row by whether its outcome comes from the drought, storms or earthquakes sources. Print a separate count of false leads for the real read and for each placebo step. Add a test.
2. **The panel is not pinned between the steps** (`__main__` 338-339, `build()` 128; fairly sure). `panel` can be run again at any time and silently overwrites `panel.npz`. No row records which panel it read. The placebos, the planted runs, `real` and `confirm` could therefore each read a different table, and the table is still growing. To fix: store the sha256 of `panel.npz` in every kept row. Make `real`, `confirm` and `table` refuse when the hashes differ. Make `panel` refuse once any row exists.

## What the rule overstates

- **The hearing rates on planted links will flatter count outcomes.** About five of the 14 outcomes are mostly nought (conflict, storms, earthquakes). For these, the plant is close to all of the outcome's movement in its quiet months. Check 3: a share of 0.038 overall, but 1.000 in months that are quiet before and after. So "heard at share 0.04" says less about real links into count series. To fix: report planted results by outcome kind.
- **The stated share is of raw month-to-month movement, season included**, while the read takes the season out first. For seasonal outcomes (births, storms) the true size of a plant differs from its label.
- **The places placebo and the planted runs scramble neighbours** in every set except prices and money. That weakens the neighbour baseline there compared with the real read. The rule keeps the month-wide parts, but it does not say this.
- **"A quarter of places in five groups" has an exception the rule leaves out.** When the groups run out, a plant can cover fewer places (docstring line 182; births have about 40 places).
- **"Nothing outside climate can lead drought" is true of causes, not of prediction.** Markets price El Niño forecasts, and oil prices can come before induced earthquakes. A flagged false lead may be a real forecasting signal, not a fault in the method. Word it as "implausible", and read each one by hand.
- **A true lead can be labelled "moving together" and so not count.** In check 2, a strong planted link from conflict to climate passed and was confirmed, but was labelled "moving together", not a lead. What a silence is worth therefore depends on how often the label throws away true leads. The planted runs measure this, so the rule should say so.
- **Confirmation scores only 5 whole years** (the bar is about 1.98; it uses its own `(5, 36)` rather than `YEARS`). It is weak evidence either way. How often a false pass would be confirmed is unmeasured; the rule admits this, but should put it next to any confirmation.
- **The 97 to 98% hearing figure** was measured on the 16-series made-up table, not one of the panel's shape.

## Checked and sound

- **Q1:** nothing of 2020 to 2024 reaches the finders or the referee. `run` cuts the table to before 2020 before taking out the season. `moved` rolls only within that span. `plant` sizes over that span and uses the input from earlier months. Each month's middle is computed from that month alone. In `confirm`, the values before 2020 match the real read's. Check 1: adding noise of size 50 to 2020 to 2024 left the board and the handed-over reading identical.
- **Q2:** shifts are whole years, at least 4 years apart and at least 4 from none. The years placebo moves each set's month-wide parts as a whole.
- **Q3:** `hit` (line 235) is right. It compares the set of names with `{input}` on the planted outcome, requires a lead, and accepts any lag. In check 1, 3 of 6 plants were heard on the board, and the same 3 when handed over directly.
- **Q4:** UCDP zero-fill: log1p of nought is nought, and GED 26.1 covers 1989 to 2025.
- **Q5:** every tie in `docs/tied-series.md` lies inside one set.
- **Q6:** check 2 ran a copy of the script on smoke seeds. `real once` ran, `confirm once` ran, and a second `real once` was refused. `marks` refuses unregistered and repeated seeds.
- Minor and safe: if the run crashes after `only_once`, the read stays blocked rather than reopening.

## Not checked

- Runtime and memory at the real panel's size.
- `build()` against real files: its order, the 30-place NaN months, and the fact that `keep_p` uses the series set before `keep_s` (choices among places and series do look at whether 2020 to 2024 data are present, but not at their values).
- **Q7**, the cost of the two left-out members: not measured on a table of the panel's shape.
- How often a false pass would be confirmed.
- Whether the six planted links per table interact with each other.
