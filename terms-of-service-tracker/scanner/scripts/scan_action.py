#!/usr/bin/env python3
"""Run a conservative, local pre-action scan against a tracker snapshot."""
from __future__ import annotations
import argparse, datetime as dt, json, re, sys
from pathlib import Path

VERDICTS = {"CLEAR", "CONFLICT", "CONTRADICTION", "UNCHECKED"}

def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def normalize(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()

def snapshot_candidates(snapshot_dir: Path, platform: str):
    key = normalize(platform).replace(" ", "-")
    candidates = []
    for p in snapshot_dir.rglob("*"):
        if not p.is_file() or p.name.startswith('.'):
            continue
        hay = normalize(p.stem).replace(" ", "-")
        if key and (key in hay or normalize(platform) in normalize(p.name)):
            candidates.append(p)
    return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)

def parse_snapshot(path: Path):
    raw = path.read_text(encoding="utf-8")
    data = None
    if path.suffix.lower() == ".json":
        try: data = json.loads(raw)
        except json.JSONDecodeError: data = None
    if isinstance(data, dict):
        rules = data.get("rules") or data.get("rule_text") or data.get("text")
        source = data.get("source") or str(path)
        date = data.get("snapshot_date") or data.get("date") or "unavailable"
        if isinstance(rules, list):
            rules = "\n".join(map(str, rules))
        if rules:
            return str(rules), str(source), str(date)
    return raw, str(path), dt.datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()

def make_verdict(action, snapshot_dir):
    platform = action.get("platform", "")
    if not action.get("action") or not platform:
        return {"verdict":"UNCHECKED", "action":action.get("action", ""), "platform":platform,
                "reason":"action and platform are required", "rules_cited":[], "label":"UNVERIFIED"}
    candidates = snapshot_candidates(snapshot_dir, platform)
    if not candidates:
        return {"verdict":"UNCHECKED", "action":action["action"], "platform":platform,
                "reason":"no snapshot — run the tracker check first", "rules_cited":[], "label":"UNVERIFIED"}
    text, source, date = parse_snapshot(candidates[0])
    flags = action.get("involves", {})
    terms = []
    if flags.get("link"): terms += ["link", "url", "paid", "waitlist"]
    if flags.get("payment"): terms += ["payment", "paid", "purchase", "fee"]
    if flags.get("account"): terms += ["account", "login", "sign up"]
    if flags.get("personal_data"): terms += ["personal data", "personal information", "privacy"]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cited = []
    conflict = False
    for line in lines:
        low = line.lower()
        if terms and any(t in low for t in terms) and any(w in low for w in ["prohibit", "not allowed", "remove", "ban", "forbidden", "do not", "can't", "cannot"]):
            cited.append({"exact_text":line, "source":source, "snapshot_date":date})
            conflict = True
    if not cited and lines:
        cited = [{"exact_text":lines[0], "source":source, "snapshot_date":date}]
    return {"verdict":"CONFLICT" if conflict else "CLEAR", "action":action["action"], "platform":platform,
            "rules_cited":cited, "what_it_means":"The action was compared with the available written snapshot.",
            "what_to_do_next":"Change the action or do not do it." if conflict else "Go ahead, subject to the cited written rules.",
            "label":"UNVERIFIED"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action_json", type=Path)
    ap.add_argument("snapshot_dir", type=Path)
    ap.add_argument("--checks-dir", type=Path, default=Path(__file__).parents[1]/"checks")
    args = ap.parse_args()
    action = load_json(args.action_json)
    result = make_verdict(action, args.snapshot_dir)
    args.checks_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    safe = re.sub(r"[^a-z0-9]+", "-", f"{result.get('platform','unknown')}-{result.get('action','action')}".lower()).strip('-')
    out = args.checks_dir / f"{safe}-{stamp}.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"script error: {e}", file=sys.stderr); raise SystemExit(1)
