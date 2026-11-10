# Seed ledger

A seed scored for a mark is spent for that purpose. A new method's fresh marks need a range not listed as spent here. Update this file in the same commit as the rule that reserves a range.

| Seeds | Rung and panels | State |
|---|---|---|
| 3001 to 3020 | Count: `planted_3.50`; nulls 3001 to 3005 | Spent. Development only |
| 5001 to 5020, 5101 and up | Count: reserved by R2 | Check before use; R2 stopped before its later steps |
| 6001 to 6060 | Count: decoy pool | Decoys only |
| 7001 to 7020; nulls 7001 to 7015 | Toy | Spent as a harness check. 7001 was also the smoke test (`results/framework-stage-1.md`) |
| 7101 to 7140; nulls 7101 to 7110 | Count | Reserved by `results/framework-stage-1.md`, never run. Now reserved for the method in `results/framework-shortlist.md`, scored once |
| 9001 to 9015; nulls 9001 to 9005 | Count: `planted_1.40`, `2.00`, `3.50`, `6.00`, `10.00` and each null panel | Reserved by `results/framework-curve.md`. A measurement, not marks on a method. Spent once it runs |
| 9901 | Count | Smoke test for the curve only, never scored |
| 7901 to 7999 | Toy | Smoke tests only, never in a count |
| 8001 to 8060 | Toy: decoy pool | Decoys only |
| 11001 to 11020 | Real field: decoy sets for the discovery marks | Spent (`results/real-enso-drought.md`, 2026-11-09) |
| 11101 to 11110 | Real field: ruler (planted link and its decoy set) | Spent, a measurement (`results/real-enso-drought.md`, 2026-11-09) |
| 11201 to 11220 | Real field: decoy sets for the marks of the two-gate search | Spent (`results/real-enso-drought-2.md`, 2026-11-09) |
| 11301 to 11310 | Real field: ruler of the two-gate search | Spent, a measurement and its instrument check (`results/real-enso-drought-2.md`, 2026-11-09) |
| 11901 to 11905 | Real field: development of the two-gate search, discovery years only | Development only, never in a count. Spent |
| 12101 to 12120, 12201 to 12220, 12301 to 12320, 12401 to 12420, 12501 to 12520 | Real fields never read before (South America, Australia, South and Southeast Asia, North America, Europe, in that order): decoy sets for naming | Spent (`results/real-enso-continents.md`, 2026-11-09) |
| 13101 to 13120, 13201 to 13220, 13301 to 13320, 13401 to 13420, 13501 to 13520 | Real fields (South America, Australia, South and Southeast Asia, North America, Europe, in that order): decoy sets for naming among 26 real series | Spent (`results/real-indices.md`, 2026-11-09) |
| 13601 to 13610, 13701 to 13710, 13801 to 13810, 13901 to 13910, 14001 to 14010 | The same five fields, in that order: ruler and instrument check among 26 real series (planted link and its decoy set) | Spent, a measurement and its instrument check, missed (`results/real-indices.md`, 2026-11-09) |
| 14901, 14999 | Real fields: smoke test of `scripts/run_indices.py` with decoys standing in for the real series | Smoke test only, never in a count. Spent |
| 15101 to 15120, 15201 to 15220, 15301 to 15320, 15401 to 15420, 15501 to 15520 | The same five fields, in that order: decoy sets for naming with the corrected controls | Spent (`results/real-indices-2.md`, 2026-11-10) |
| 15601 to 15610, 15701 to 15710, 15801 to 15810, 15901 to 15910, 16001 to 16010 | The same five fields, in that order: ruler and instrument check with the corrected controls | Spent (`results/real-indices-2.md`, 2026-11-10) |
| 17101 to 17120, 17201 to 17220, 17301 to 17320, 17401 to 17420, 17501 to 17520, 17601 to 17620 | Burned area, six fields (Africa, South America, Australia, South and Southeast Asia, North America, Europe, in that order): decoy sets for naming | Spent, missed (`results/fire-enso.md`, 2026-11-10) |
| 17701 to 17710, 17801 to 17810, 17901 to 17910, 18001 to 18010, 18101 to 18110, 18201 to 18210 | The same six fields, in that order: ruler (planted link and its decoy set) | Spent, a measurement (`results/fire-enso.md`, 2026-11-10) |
| 18901, 18999 | Burned area: smoke test of `scripts/run_fire.py` on noise shaped like the fields | Smoke test only, never in a count. Spent |
| 19801 to 19880 | Burned area, South and Southeast Asia fitting years: fresh decoy sets with nothing planted, the reader's `q4_sim.py real`, to spot-check its finding on the control set | Spent, a spot check (`results/fire-enso.md`, 2026-11-10) |
| 19101 to 19110, 19201 to 19210, 19301 to 19310, 19401 to 19460, 19501 to 19524, 19601 to 19610, 19701 to 19724 | Local drought and burned area, made-up panels (`synth/local_panel.py`), in that order: link at 20%, 10% and 5% of variance, nothing, instrument only, link and instrument, drift only | Spent, every mark held (`results/fire-drought.md`, 2026-11-10) |
| 20001 to 20006, 20011 to 20019, 20021 to 20023, 20031 to 20033, 20041, 20042, 20051 to 20057, 20061 to 20064 | The independent reader's own made-up panels for the drought rule (`docs/reviews/2026-11-10-fire-drought-rule-check/`); 20004 and 20006 run again by this session under the amended verdict | Spent, a check. Never in a count |
| 20101 to 20124, 20201 to 20212 | Local drought and burned area, panels added after the independent check, in that order: instrument only through the month before's view; a quickening drift (measured, no mark). The seeds of the row above the reader's are also run again under the amended verdict | Spent, every mark held (`results/fire-drought.md`, second result) |
| 20901, 20902 | The `before` panel: smoke runs and the measure it was set by | Smoke test only, never in a count. Spent |
| 21001 to 21004, 21101 to 21104, 21201 to 21204, 21301 to 21304 | Local drought and burned area after the scoring: a link planted in the real fields at 20%, 10%, 5% and 2% of variance, in that order (`scripts/explore_planted.py`) | An exploration on spent years, marks nothing (`results/fire-drought.md`, after the scoring) |
| 21401 to 21404, 21501 to 21504, 21601 to 21604, 21701 to 21704 | The same, with the planted squares on the detector's own blocks | An exploration on spent years, marks nothing (`results/fire-drought.md`, after the scoring) |
| 19901, 19902, 19903, 19999 | The same made-up panels: smoke runs on which the design was reached | Smoke test only, never in a count. Spent |
| 21801 to 21806 | Staple prices and drought, made-up panels (`synth/price_panel.py`): smoke runs on which the price test was tried and set aside (decision 0050) | Smoke test only, never in a count. Spent |
| 21901 to 21918 | National harvests and drought, made-up records (`synth/harvest_panel.py`): smoke runs on which the test was shaped (`results/harvest-drought.md`, changes after smoke) | Smoke test only, never in a count. Spent |
| 22001 to 22010, 22101 to 22110, 22201 to 22210, 22301 to 22330, 22401 to 22420, 22501 to 22520, 22601 to 22610 | National harvests and drought, made-up records, in that order: link at 20%, 10% and 5% of variance, nothing, drift, step, link at 20% in a fifth of the countries | Spent, every mark held (`results/harvest-drought.md`, 2026-11-10) |
| 23001, 23002, 23010 to 23013, 23020 to 23028, 23031 to 23038, 23041 to 23048, 23051 to 23054, 23061 to 23066, 23071 to 23078, 23081 to 23088 | The independent reader's own made-up records for the harvest rule (`docs/reviews/2026-11-10-harvest-rule-check/`); 23001 to 23099 were set aside for it | Spent, a check. Never in a count |
| 24001 to 24008, 24050 | The independent reader's sampling, noise and resampling for the check of the harvest result (`docs/reviews/2026-11-10-harvest-result-check/`), on the real record after its one scoring; 24050 is the project session's reproduction of its two-way interval. 24001 to 24099 were set aside for it | Spent, a check. Never in a count |
| 21940 to 21946, 21990 to 21999 | Other crops and drought, made-up records of many crops (`synth/harvest_panel.py`): smoke runs on which the rule of `results/crops-drought.md` was shaped (decision 0054) | Smoke test only, never in a count. Spent |
| 25001 to 25020, 25101 to 25110, 25201 to 25210, 25301 to 25310, 25401 to 25410, 25501 to 25510, 25601 to 25605, 25701 to 25705, 25801 to 25810 | Other crops and drought, made-up records, in that order: leak (the cereal-like crops linked, no other), leak with drift, leak with a step, nothing, link at 35%, link at 35% in few crops, leak at full size, link at full size, link at 20% | Registered (`results/crops-drought.md`, 2026-11-10); not yet run |
| 26001 to 26099 | Set aside for the independent reader of the other-crops rule | Set aside |
| 903000 to 903099, 910000 to 910099, 911000 to 911099, 950000 to 950059, 951000 to 951059, 952000 to 952059 | The independent reader's null runs on the control set (`docs/reviews/2026-11-10-fire-enso-independent-check/`, `q4_sim.py` and `q5_sim.py`). Its other null runs took their seeds as arguments and the values were not kept | Spent, the reader's, outside this project's counts |
