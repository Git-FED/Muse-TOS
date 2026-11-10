# Scanner Setup

## Requirements

- Build the `terms-of-service-tracker` repo first, with at least one platform snapshotted.
- Python 3.
- Install the shared tracker dependencies with `pip install -r scripts/requirements.txt` from the tracker repo. This scanner's scripts use the Python standard library; the shared requirements file remains the tracker's source of truth.

## First dry run

Start with the worked examples in `examples/`. A dry run is documentation-only: do not use a real action and do not save a verdict under `checks/`.

## First real scan

1. Name the first real platform and the one action to check.
2. Verify that the platform's rules are already snapshotted by the tracker.
3. Put the action in the `templates/action-template.json` shape.
4. Run the scanner:

```bash
python scanner/scripts/scan_action.py path/to/action.json path/to/tracker/snapshots
```

5. Read the verdict fields: verdict, rules cited, what it means, what to do next, and label.
6. Validate a saved verdict before showing it:

```bash
python scanner/scripts/verdict_check.py scanner/checks/<verdict>.json
```

Never scan a real action before its platform's rules are snapshotted. That scan reports UNCHECKED, not CLEAR.
