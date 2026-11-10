# Checks

Store one file per scan: a verdict JSON plus its rendered verdict, named like `checks/<platform>-<action>-YYYY-MM-DD-HHMM.json`.

Keep every verdict — the verdict history is the proof of what was checked before it was done. `checks/` is gitignored by default because verdicts can name platforms and actions the user may not want public. Choosing to track verdicts is a deliberate decision, not the default.

A verdict without citations or without a label is not a verdict. Run `scripts/verdict_check.py` before showing it to anyone.
