# 0046: The corrected controls are lopsided; the blind search is set aside until that is put right and measured

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule. Corrects what decision 0044 said about its own effect; 0044 itself is not edited.

## Context

The search names a candidate when its real alignment beats every copy of every candidate moved by whole years. Decision 0044 took out the copies a year either side of the real alignment, because on a record of N years the copy moved N − 1 years is the series one year earlier. It said the result was a sound comparison, and `results/fire-enso.md` then gave the search a false-alarm floor of about two in (controls + 1).

An independent reader of the burned-area result (`docs/reviews/2026-11-10-fire-enso-independent-check/`, its section 4) found that this is wrong. Taking out only the real alignment's neighbours leaves every copy with its own neighbours among the copies, and neighbours a year apart resemble each other (about +0.24). The real alignment alone loses the rivals most likely to beat it. On fields with nothing in them the reader measured, for any alarm, 15% with that set against 7% with every copy on the real South and Southeast Asia burned-area field (150 runs), 17% against 6% on the same field detrended, 7% against 7% on North America, 44% against 17% on a made-up field with a strong trend, and 4.9% against 2.5% on a 50-year record (81 runs). This session spot-checked it on 80 fresh sets: 14 against 9.

## Decision

1. **The floor of about two in (controls + 1) is withdrawn for the control set of decision 0044.** It holds only when every alignment is judged against the same kind of set. With 0044's set the false-alarm rate is higher and depends on the data, most where a field has a trend.
2. **The blind two-gate search with 0044's control set is not run on any field again** until every alignment is given the same kind of comparison set (the real one and each copy alike), and its false-alarm rate is then measured on nulls built from the field in question, before any mark is set. That work is not started now.
3. **What stands, and what does not, among the results that used the search:**
   - `results/real-enso-continents.md` judged against all 49 copies, on equal terms. Untouched. It was, as 0044 found, too strict if anything.
   - `results/real-indices-2.md` used 0044's set. Its step 1 stands as measured, since its marks were counts on nulls and a higher floor only makes them harder to hold (3 and 5 of 100 against 8). What `STATUS.md` drew from it, that the corrected search "is the one to use with many real candidates", does not stand. Every pair it named failed the forecast step, so no claim rests on its naming.
   - `results/fire-enso.md`: the miss stands. Its false alarms (18 of 120) are what this set gives on those fields with nothing there; they are not a sign of anything in the fields. Corrected in place.
4. **Nothing is rerun.** The burned-area fitting years are not searched again with a repaired set: the known answer that search was looking for is not clearly in the product (1997 in equatorial Asia ranks 12th to 13th of 21 years), so a repaired search would have nothing to be checked against there.

## Considered and not done

- **Repairing the control set now** (for instance, judging each copy against the copies at least two years from it). It would need its own rule, nulls and ruler, and the next test (local drought against burned area, with its own rule and decision to follow) does not use this search at all: its controls are whole-year shifts of the driver field on the scoring years, each scored the same way as the real one, and its false alarms are measured on made-up panels before any real field is touched.
- **Rerunning the fire naming with all 21 copies.** That set contains the two copies 0044 showed to be the series itself, so it is too strict in a different way; and a rerun on fitting years already read, with a known answer the product does not hold, would decide nothing.
- **Rerunning `results/real-indices-2.md`.** Its 2000 to 2024 are spent for the pairs it named and none passed.

## Consequences

- `results/fire-enso.md`, `results/real-indices-2.md`, `STATUS.md` and `README.md` are corrected in the commit that carries this decision.
- A lesson for every later control: a control must be made the same way as the thing it is compared with, and the false-alarm rate is measured on nulls shaped like the data, not derived.
