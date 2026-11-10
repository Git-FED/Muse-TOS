# Scanner Usage

## Manual scan

```bash
python scanner/scripts/scan_action.py path/to/action.json path/to/terms-of-service-tracker/snapshots
```

The command reads only the named action and the tracker's snapshot files. It does not post, email, or contact a platform.

## Verdicts

- **CLEAR** — the action matches the cited written rules. Next: go ahead, while respecting the cited rules.
- **CONFLICT** — the action breaks a written rule. Next: change the action or do not do it.
- **CONTRADICTION** — a human instruction conflicts with the written rules. Quote both; the written rule wins. Only written permission from the same authority makes it safe.
- **UNCHECKED** — the rules were not verified. Next: run the tracker check first and scan again. UNCHECKED is not CLEAR.

## Verdict anatomy

Every completed verdict contains: action, platform, verdict, rules cited, what it means, what to do next, and a VERIFIED or UNVERIFIED label. A citation includes exact rule text, source, and snapshot date.

**Advise only:** no platform contact or action on the user's behalf without a separate explicit order.
