# About this folder

An independent reader checked the drought and burned-area rule, its code and its made-up results before any real field was fitted. It read the repo at commit 829e432 with no part in the design.

- `report.md` is the reader's report. It came back as a message and was saved here unchanged by the project session.
- The scripts and logs are the reader's own. They ran against commit 829e432. `run_reader.py` and `run_fix.py` call the verdict with four parts; the amended code passes six, so they need that commit to run as they are.
- What was changed in response is `docs/decisions/0048-what-the-independent-check-changed.md` and the amendment in `results/fire-drought.md`.
- The project session ran `share_before.py` again and got the report's numbers for the six real fields, and ran the reader's drift seeds 20004 and 20006 through its own copy of the panel.
