# Independent reading of the second real read's rule and runner, before any run

**What was read (2026-11-12):** `results/stage-c-second-read.md`, decision 0067, `scripts/run_stage_c.py`, `tests/test_stage_c.py`, `scripts/run_stage_b.py`, the referee's past-only arithmetic, `docs/tied-series.md`, the seed ledger, and the made-up table maker the count used. One check script on made-up arrays was run: `PYTHONPATH=src:scripts .venv/bin/python docs/reviews/2026-11-12-stage-c-rule-check/check.py`.

## To settle before step 1

1. **Taking the year's middle off and then changing puts one place's yearly move into every place.** The code is `run_stage_b.py` lines 86-87, then `run_stage_c.py` line 30.
   - The change of (value less the year's median) is the change less the change of the median. So whichever place sits at the median, and whichever places enter or leave, shifts every place's change that year.
   - On made-up arrays, the year's median of the changes is about 0.28 of the spread of changes across places (0.48 at the 90th percentile of series). A made-up kind with places far apart in level and late entries gives 0.30. If the middle is not taken off at all, it is 0.07.
   - The count on made-up tables used the same arithmetic, so its marks were met with this present. The places placebo leaves the component untouched, because reordering places does not change a year's median. So a pass it carries would also show in the placebos.
   - Two of the rule's claims do not hold for this component. The rule says the places placebo breaks the links between sets; only the years placebo breaks this one. It also says the change is "one line of arithmetic with no setting".
   - A real pass carried by this component would be a year-wide relation over nineteen points, not a lead "in the places named".
   - Choose before any number. Either keep the arithmetic, say so in the rule's limits, and report beside every pass its score with the year's median of the changes taken off. Or take the year's middle off again after the change, and say the count did not measure that arithmetic.
   - I am sure of the arithmetic. Its size on the real series is unknown.
2. **The once-guards check and then write, with nothing in between to stop a second process.**
   - Real read: `run_stage_c.py` lines 79-84. Confirm: lines 87-102.
   - If two `real once` commands start together, both pass the check and both keep a real read. `confirm` then refuses for good ("no real read to confirm"), and the file needs repair by hand.
   - Two placebo processes finishing the same seed together (lines 72-76) do the same. `once()` then refuses every later command.
   - This fails safe: there is no hidden second read. But the real read cannot be made again.
   - Cheap fix: before the real read and before confirm, create a marker file with an exclusive create (`os.O_CREAT | os.O_EXCL`), and refuse if it already exists.

## What the rule overstates

- **The "Silence" paragraph** says that, together with the first read's silence, it would show that neither kind of steady link of the planted sizes stood out. The first read heard none of its 54 planted links, even when handed over, so its silence covers no kind of link. Only this read's planted runs can give a silence any weight, and only for a change leading a change.
- **Ties.**
  - It is mechanically right that a change makes no new tie.
  - As changes, these series are mostly inflation, which persists:
    - the two exchange-rate series (`faostat_pe:lcu:year`, `faostat_pe:slc:year`);
    - the World Bank's current-LCU series (23 named in the first read's rows);
    - its price series (`FP.CPI.TOTL*`, `NY.GDP.DEFL*`).
  - A rate's change leading a nominal series' change a year later is therefore a known answer, likely larger in high-inflation countries. The rule should name it as a known answer beforehand, not leave it to the hand check.
  - `lcu:year` also jumps at each redenomination (tied-series 5.5). As a change, that is one huge value. The referee clips it, but it widens that place's past spread for every later year.
- **What a confirmed pass is worth.** Confirmation uses the first read's rule on ten years, and the change of 2015 uses the 2014 value, which has now been read twice. That is acceptable, but the rule should state the chance of a false pass being confirmed, or say it is not known.

## Minor

- **Planted links where the input is missing.** `plant` writes zero there (`run_stage_b.py` lines 181 and 184).
  - As a change, that zero is a jump about three times a typical planted move. It affects about 19% of outcome-years when 10% of input values are missing (check 2).
  - The scored row drops out, because its input change is missing, but the outcome's own past and its neighbours carry the jump.
  - The count did the same. It makes hearing look lower, so a silence is undersold, not oversold.
- **Memory split.** The planted table splits links by the input's memory in levels (`run_stage_b.py` lines 183 and 286). For this read, what matters is the memory of the change.
- **Labels at confirmation.** `confirm` keeps each row's label, but `sb.table()` does not print it (line 297). A labelled row, which may be two series moving together, could be read as a confirmed lead.

## Checked and found sound

- **Q1, the last ten years.** No value of 2015 to 2024 reaches the finders or the referee in any step.
  - `run()` cuts at index 54 (2015) before the swarm, the steward, the reading and the handed-over links. The change at index 54 uses 53, never the other way round.
  - `plant` takes its scales from the years before 54 and adds the input of the year before.
  - Rolls stay within the years before 54 and happen after the change, so no change crosses a seam.
  - The referee's forms and baselines use earlier years only.
  - The test perturbs 2015 to 2024 and finds the read years unchanged in all three arrangements.
- **Q2, the rearrangements.**
  - The years placebo breaks every link between sets: shifts are at least ten years apart, the World Bank set stays fixed, and common series move with climate.
  - The places placebo breaks every place-level link between crops, exchange rates, drought and the World Bank, and breaks links to common series by the roll. It does not break the year-wide part (item 1).
  - After the change, a planted link is a change leading a change by one year, at the stated share of the outcome's year-to-year movement.
- **Q3, the bookkeeping.**
  - The names the first read's bookkeeping reads (`OUT`, `SEEDS`, `MOST`) are looked up when called. They are set at import, before any call, and no default argument holds the old values.
  - No path writes the first read's file. The test restores the names for other tests.
  - Unregistered seeds and seeds kept twice are refused. The real read waits for both marks and all twelve planted runs.
  - Seeds 64001 to 64999 are fresh in the ledger.
- **Q4, `confirm once`.** It sends the same row (form, places, thresholds in change units) to the referee on the changed table, with 2015 as the first scored year and labels off, under the first read's rule for confirmed.

## Not checked

- The real series' transforms (logged or not), their gaps, and how big item 1 is on them.
- Whether any tied pair beyond the first read's list is in the panel.
- How the finders behave on changes beyond what the count showed.
- Run time.
