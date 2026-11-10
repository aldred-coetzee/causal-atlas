# About this folder

An independent reader checked the national-harvest and drought rule, its code and its made-up results before any real yield was set against drought. It read the repo at commit d08fa65 with no part in the design, under a written brief with one hard rule: no real yield beside any real drought value.

- `report.md` is the reader's report. It came back as a message and was saved here unchanged by the project session.
- The scripts and logs are the reader's own and ran against commit d08fa65. `panel_mod.py` is its modified copy of the made-up record generator; `runs.jsonl` holds its runs. Its seeds, 23001 to 23088, are in `results/seed-ledger.md`.
- What was changed in response is `docs/decisions/0052-what-the-independent-check-changed-for-harvests.md` and the amendment in `results/harvest-drought.md`.
- The project session checked three of its claims against the code and the counted rows before acting: where the clip is applied, that only figures flagged A are targets, and that on the counted drift records the true years beat all 62 shifts in 4 of 20 year-end and 3 of 20 mid-year.
