# Terms of Service Scanner Skill

## Purpose

Run a pre-action check against the Terms of Service Tracker's saved rule snapshots. The scanner advises; it never performs the action.

## Standing rules

- Check **BEFORE** the action, never after. A scan after the fact is a report, not a scanner.
- Written rules are the **ONLY** authority. A person saying “go ahead” — a mod, support, a cop — does **NOT** override the written rules. One person letting you do it does not make it allowed for the next person. A verbal okay is never proof; only the written rule counts.
- Verdicts are exactly four: **CLEAR** (action matches the written rules), **CONFLICT** (action breaks a written rule — quote it), **CONTRADICTION** (a human instruction conflicts with the written rules — quote both), and **UNCHECKED** (the rules could not be fetched or verified — never a silent pass).
- Cite the exact rule text + its source + its snapshot date for every verdict. A verdict with no citation is an opinion, not a scan.
- User-named platforms and actions only. Never guess a platform, a rule, or what the user is about to do.
- “Couldn't check” is a result, never a silent pass. Login wall, moved page, blocked fetch, or unreadable rules = UNCHECKED with the reason.
- Every verdict is labeled **VERIFIED** (checked by hand, with live evidence and a stated time) or **UNVERIFIED** (worker-reported or unchecked). No unlabeled verdicts.
- No action without an order. Advise only. Never post, email, or contact a platform on the user's behalf without a separate explicit order.

## Routine

1. Load the action the user described, including its named platform and `involves` flags.
2. Load that platform's rule text from the tracker's snapshots. Fetch live only if no snapshot exists, and say so; a failed fetch is UNCHECKED.
3. Compare the action against each applicable rule without guessing.
4. Issue exactly one verdict: CLEAR, CONFLICT, CONTRADICTION, or UNCHECKED.
5. Cite every rule used with exact text, source, and snapshot date. Quote the human instruction too when the result is CONTRADICTION.
6. Save the verdict under `checks/` and log the run with counts for clear, conflict, contradiction, and unchecked.

## Storage layout

- `prompts/` — copy-paste prompts for consistent scans.
- `scripts/` — local command-line scanner and verdict-shape checker.
- `templates/` — action and rendered-verdict shapes.
- `examples/` — fictional dry-run examples plus the recorded contradiction reference.
- `checks/` — saved verdict history; contents are private and gitignored by default.
- `logs/` — run logs; gitignored by default.

## What this is not

This is not a grader of current terms (ToS;DR's job), not a vendor-compliance tool, not the AI compliance skill, and not a posting tool. Fed Poster posts; the scanner only checks first.
