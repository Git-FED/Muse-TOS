#!/usr/bin/env python3
"""Validate verdict shape; never re-judges whether a verdict is correct."""
import argparse, json, sys
from pathlib import Path
VERDICTS = {"CLEAR", "CONFLICT", "CONTRADICTION", "UNCHECKED"}
LABELS = {"VERIFIED", "UNVERIFIED"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("verdict_json", type=Path); args = ap.parse_args()
    data = json.loads(args.verdict_json.read_text(encoding="utf-8")); missing = []
    if data.get("verdict") not in VERDICTS: missing.append("verdict (CLEAR, CONFLICT, CONTRADICTION, or UNCHECKED)")
    for field in ("action", "platform"):
        if not data.get(field): missing.append(field)
    if data.get("label") not in LABELS: missing.append("label (VERIFIED or UNVERIFIED)")
    if data.get("verdict") == "UNCHECKED":
        if not data.get("reason"): missing.append("reason for UNCHECKED")
    elif data.get("verdict") in {"CLEAR", "CONFLICT", "CONTRADICTION"}:
        rules = data.get("rules_cited") or []
        if not rules: missing.append("at least one rules_cited entry")
        for i, rule in enumerate(rules, 1):
            for field in ("exact_text", "source", "snapshot_date"):
                if not rule.get(field): missing.append(f"rules_cited[{i}].{field}")
    if missing:
        print("FAIL"); print("Missing or invalid fields:"); print("- " + "\n- ".join(missing)); return 1
    print("PASS"); return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except (OSError, json.JSONDecodeError, TypeError) as e:
        print(f"FAIL\n- invalid JSON or unreadable file: {e}", file=sys.stderr); raise SystemExit(1)
