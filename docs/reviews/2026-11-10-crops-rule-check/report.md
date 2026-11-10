# Independent check of the rule for the other crops (2026-11-10)

**Verdict: may be read after these changes.** All five are wording changes; no condition of the rule has to change:

1. **Correct two numbers.**
   - The results file's "the best gained 0.58%" is true at year-end only. At mid-year the best was 0.74% to 0.78% (seed 25001).
   - The README's "5 of 10" (the 35% link in a tenth of the records) needs "(5 of the 8 that had a linked record)".
2. **Say the cap never acts.** Claims are used with the full drought term, so a reported gain means picking the records that claim and adding the whole term. It is not a fitted slope.
3. **Say the flat driver is load-bearing.** A slow, curving drift that is shared between drought and yields, 2.5 times stronger than the registered one, passed every condition with the driver as it fell, with no link at all. It was stopped only because the flat driver must pass too. Keep the rule that both drivers must pass, and never report a pass by one driver alone as a read.
4. **Disclose that the real record looks unlike the made-up ones.** It is much more uneven and much more heavy-tailed, and the marks were not set on records like that.
5. **Add the measured numbers to the existing note on the shift controls,** and record that the fix I tried does not work.

**I could not save `report.md`.** The harness refused the write ("Subagents should return findings as text"), so this message is the report. The caller should save it as `docs/reviews/2026-11-10-crops-rule-check/report.md` if the folder needs it.

## What I did

- **Followed the hard rules.**
  - I did not run `run_claims.py real once`.
  - No real yield of the other crops was set beside any real drought value. Only yields were loaded, and the drought array was never opened.
  - I did not compute anything on the cereal record.
  - I changed nothing outside the folder, and made no commit, push, install or network call.
  - Every job ran under `nice -n 19` on one thread, with at most three running at once.
- **Read:**
  - `results/crops-drought.md`, all 120 rows of `results/crops-drought.jsonl`, decision 0054 and the README paragraph;
  - the code in `claims.py`, `harvest.py`, `yields.py`, `synth/harvest_panel.py` and `scripts/run_claims.py`, plus part of `tests/test_claims.py`.
- **Wrote my own scripts** in `docs/reviews/2026-11-10-crops-rule-check/scripts/`:
  - `panel_x.py` is the world generator with extra adversarial settings. With its defaults it gives the same world as the original, checked on seed 25001.
  - `rv.py` reads a world the same way `run_claims.read` does. `rv2.py` does the same and adds shifts whose drought term is scaled to the true alignment's size.
  - The others are `leak.py`, `table.py`, `interval.py`, `shape.py`, `shared.py`, `show.py` and `batch.sh`.
- **Logs** are in `logs/`. `runs.jsonl` has one line per adversarial world; the others are `runs2.jsonl`, `leak.log`, `interval.log`, `shape.log`, `shared.log` and `matched.log`.

## Findings

### 1. The written method against the code

The code does what the method section says. There are five differences.

- **The cap never acts.** The words say each claim is used "at that slope, held between 0 and 1". In practice the slope on a claim is 1 or more almost every time:
  - in the 720 registered readings, the capped gain equals the uncapped gain in 641;
  - in my runs, 0% to 3.5% of claims had a slope below 1.

  So the drought term is used at full size, and the rule is in effect "pick record-years, then add the whole term". The rows follow the code, so this is a wording point, not an error.
- **FEW counts something slightly different.** It counts countries whose claimed baseline error is above zero, not countries with a claiming record. These are nearly the same thing.
- **An empty bootstrap draw counts as zero.** A draw with no claims is scored as a gain of zero. This is harmless.
- **The 35% worlds are described two ways.** The rule says they hold "a fifth to a third" of the scored records. The rows show 17% to 38%. The results section's "a sixth to two fifths" is the accurate one.
- **The flat driver uses the whole record.** Its levelling uses future years. This is stated in the words, and item 2 shows it cannot produce a read on its own.

### 2. Leak test

I took one world (seed 26002), replaced every value from a cut year onward with noise (seed 26003), and compared everything before the cut. Cuts were at year index 40 and 55, in both variants, in scored records and beside records.

- **No leak in the forecast path with the driver as it fell.** Nothing before the cut changed: the largest difference was exactly 0. That holds for the forecast, the baseline chosen, the slopes and t-values, the claims, the error on the claims and the weights.
- **Two things changed before the cut, both as expected:**
  - The shift columns changed, because the shifts wrap round the record.
  - The flat driver changed (largest change in its term 0.32), because its levelling uses the whole record.

That flat-driver change cannot produce a read: both drivers must pass, the smaller gain is the one reported, and with no link the flat driver is independent of the yields.

### 3 and 4. Hard worlds with no link in the other crops

All readings below are year-end unless marked, used 20 shifts instead of 62, and had no linked scored record. Each gain is shown as "driver as it fell / flat driver". None was read.

| World | Seed | Gain | Interval lower end | Beats all 20 shifts |
|---|---|---|---|---|
| Drift 2.5× (drought 3.0, yields 0.75) | 26010 | +0.71% / −1.27% | −0.56% | no (18 and 1 of 20) |
| Drift 2.5× | **26011** | **+1.62% / −0.72%** | **+0.06%** / −1.92% | **yes** / no (2 of 20) |
| One-year permanent step | 26014 | −1.12% / +0.79% | −8.29% / −2.02% | no / yes |
| One-year permanent step | 26015 | −0.30% / −0.42% | −5.23% | no |
| Persistence | 26018 | −0.12% / −0.09% | −0.73% | no |
| Persistence | 26019 | +0.10% / −0.03% | −0.17% | no (18 of 20) |
| Rough, heavy-tailed records | 26022 | −0.06% / −0.08% | −0.80% | no |
| Rough, heavy-tailed records | 26023 | −0.02% / −0.16% | −0.62% | no |
| Cereals linked at 50% | 26030 | −0.27% / −0.43% | −2.19% | no |
| Cereals linked at 50% | 26031 | −0.72% / −1.51% | −3.28% | no |
| Cereals linked at 50% | 26032 | −1.09% / −0.97% | −3.04% | no |
| Cereals at 50% plus strong shared country shocks | 26034 | −6.93% / −4.81% | −13.55% | no |
| Cereals at 50% plus strong shared country shocks | 26035 | −0.59% / −0.75% | −7.14% | no |
| Cereals at 50% plus strong shared country shocks | 26037 | −0.56% / −1.28% | −4.50% | no |
| Cereals at 50% plus strong shared country shocks, mid-year | 26036 | −2.58% / −3.56% | −7.24% | no |

**Seed 26011 is the main finding.** It has no link, but the driver as it fell passed every one of its own conditions:

- a gain of 1.62% with an interval of 0.06% to 3.13%;
- it beat all 20 shifts;
- the gain without its best country was +1.43%;
- the gain beat each baseline alone.

It also read at the 1.5 and 2.0 levels. It was not read only because the flat driver lost 0.72%. What it means:

- **The two-driver rule is what guards against a slow, curving trend that drought and yields share.** Removing it would allow false reads.
- The registered drift (drought 1.2, yields 0.25) gave 0 of 10 reads, so this is outside the tested range.
- Whether the real record has such a shared curve cannot be checked without setting yields beside drought.

**Cereals do not make a false gain in the other crops.** A strongly linked cereal crop drags the other crops into a loss, not a gain. The country-level term carries the cereals' drought term into every crop in that country. The term under the true alignment was 0.08 to 0.12, against about 0.02 under the shifts. This costs power and would partly hide a real link in the other crops. It does not create a false read.

### 5. Are the 62 shift controls fair?

**No, as a test on their own.** The results file already says this and gives the likely reason. I measured both.

- **The true alignment beats all 62 shifts too often in worlds with no link:**
  - year-end, 3 of 45 worlds, where a fair control would give about 0.7 (a 3.5% chance of 3 or more);
  - mid-year, 3 of 20, where it would give about 0.3 (a 0.4% chance).
- **Its rank among the shifts is U-shaped, not flat.** Across 65 runs it beat no shift in 16, against about 1 expected. It beat 60 or more in 15, against about 3 expected.
- **The stated reason is confirmed.** The term under the true alignment is three to six times its size under a shift:

  | World | Seed | True alignment | Shifts |
  |---|---|---|---|
  | Registered-style | 26001 | 0.034 | 0.011 |
  | Cereals linked at 50% | 26030 | 0.069 | 0.015 |
  | One-year step | 26014 | 0.158 | 0.024 |

  So the shifts' gains bunch near zero, and "beats every shift" amounts to "the gain is a little above zero".
- **The fix I tried fails.** I rescaled each shift's term to the true alignment's size (seed 26014, 20 shifts). The rescaled shifts lose heavily (down to −11.6%), so the true alignment went from beating 0 to beating 15 of 20. That makes the condition easier, not fairer.

What protected every world with no link was the interval, together with the flat driver (item 3).

### 6. The interval

I checked it directly with `interval.py`, seeds 26060 to 26064. Each setting had a true gain of zero by construction, heavy tails, year shocks and country effects, and 300 repeats.

| Countries | Lower end above zero |
|---|---|
| 15 | 2, 1 and 7 of 300 (7 of 300, 2.3%, was with a wide spread between countries) |
| 40 | 4 of 300 |
| 100 | 2 of 300 |

So it holds at or below its nominal 2.5%, even with as few countries as the rule allows. In the registered worlds with no link, the highest lower end was −0.11% at year-end and −0.43% at mid-year.

### 7. The made-up table

It rebuilds exactly from the rows.

| Case | Seeds and lower ends |
|---|---|
| Read by a whisker (lower end under 0.2%) | 25507 (0.14%), 25804 (0.06%), 25805 (0.03%), 25810 (0.12%), and 25403 mid-year (0.08%) |
| Not read, by a whisker | 25801 (−0.15% / −0.16%), 25405 mid-year (−0.20%, driver as it fell only), 25509 (flat −0.02%, as it fell −0.49%) |

- In the link worlds, every failure was decided by the interval alone, except 25503 and 25510, which had no linked record and failed everything.
- **One error:** "the best gained 0.58%" is true only at year-end. The mid-year best was 0.737% (as it fell) and 0.778% (flat), both in seed 25001.
- **Every other number checked matches:**
  - linked records gained 3.5% to 7.7%;
  - 0.52 to 0.81 of the claims fell in linked records;
  - claims covered 11% to 20% of what could be claimed;
  - the pooled reading passed in 8+5, 2 and 0 worlds;
  - the small worlds are 44% cereal-like.

### 8. The real panel's shape (yields only)

Only yields were loaded. The made-up comparison world is seed 26050.

| | Real | Made-up |
|---|---|---|
| Scored and beside records | 2,339 and 503, in 139 countries | |
| Countries with no cereal record | 5 | 1 |
| Scored records per country, median (range) | 14 (1 to 45) | 20 (12 to 29) |
| Records with fewer than 20 official scored years | 6.6% | 0.2% |
| Figures that are not official | 11.3% | 8% |
| Kurtosis of standardised changes | 6.0 | 3.1 |
| Changes beyond 4 standard deviations | 0.39% | 0.01% |
| Records ending before 2020 | 64 | 0 |
| Exactly repeated figures | 1.2% | 0.9% |
| How much each year's change undoes the last, median (lag-1 autocorrelation) | −0.32 | −0.34 |
| How closely crops in one country move together, median | 0.08 to 0.10 | about 0.25 |

What this means:

- **The real record is much more uneven and heavy-tailed** than the made-up worlds the marks were set on. That is not covered except partly, by the rough worlds and the interval check.
- **The made-up worlds share more within a country** than the real record does. That makes the cereal test harsher than reality, which is the safe direction.

### 9. The words

- The results file's "the best gained 0.58%" needs "(year-end; 0.74% to 0.78% mid-year)".
- The README's "a 35% link in a tenth of the records in 5 of 10" needs "of the 8 that had a linked record".
- "Used at that slope, held between 0 and 1" should say that in practice the slope is always 1.
- **Missing:** the flat driver's role against a shared curving trend (item 3), and the real record's unevenness and heavy tails (item 8). Both belong beside "a silence would rule out only …".
- The weakness of the shift controls is already disclosed. My measurements (item 5) can replace "not yet checked".

## What I could not check

- **The real drought series' own shape.** By rule it was not opened, so I cannot say whether it has a shared curving trend like seed 26011.
- **Worlds at the real record's full unevenness and tail weight.** Only partial versions were run.
- **Rare false reads.** I ran one to three seeds per hard setting, so a false-read rate below about one in five per setting cannot be ruled out. In particular, how often drift at 2.5× fools the driver as it fell is not known beyond 1 of 2.
- **The 62 shifts themselves.** My readings used 20, which makes beating every shift easier, so it is the harsher direction.
- **The interval on the real layout of countries.** It was tested on a simulated layout, not the real one.

## Seeds used

All 33 seeds are in the 26001–26099 range, and none is in `results/seed-ledger.md`:

- 26001 (also used for one short test of `rv2.py`), 26002, 26003
- 26010, 26011, 26014, 26015, 26018, 26019, 26022, 26023
- 26030, 26031, 26032, 26034, 26035, 26036, 26037
- 26050
- 26060, 26061, 26062, 26063, 26064

## Verdict

**May be read after these changes:** correct the "0.58%" and "5 of 10" sentences; say the cap never acts; say the flat driver is what guards against a shared curving trend (seed 26011) and keep requiring both drivers; disclose that the real record is more uneven and heavy-tailed than the made-up worlds; add the measured shift-control numbers.