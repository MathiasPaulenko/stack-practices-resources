# Snapshot Testing Pattern — Companion Resources

Companion code for the [Snapshot Testing Pattern](https://stackpractices.com/patterns/snapshot-testing-pattern/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `package.json` | JSON | Minimal Jest project (`test`, `test:ci`, `test:update` scripts) |
| `user_card.test.jsx` | JavaScript + Jest 29 | External snapshot, inline snapshot, and property matchers for dynamic values |
| `test_snapshots.py` | Python 3.12+ | pytest-snapshot and syrupy examples, including a normalized-order snapshot |
| `normalize_response.py` | Python 3.12+ | Replaces UUIDs and timestamps with stable placeholders before snapshotting |
| `generate_nginx_config.py` | Python 3.12+ | Generated-file example: deterministic nginx config to snapshot |
| `.github/workflows/test.yml` | YAML | CI guard: `jest --ci` fails when a baseline is missing or outdated |
| `README.es.md` | Markdown | Spanish version of this file |

## Quick start

### Jest

```bash
npm install
npm test            # first run writes __snapshots__/ baselines
npm test            # subsequent runs compare against them
npm run test:update # regenerate baselines after an intentional change
npm run test:ci     # CI mode: fails instead of writing missing snapshots
```

### pytest

```bash
pip install pytest pytest-snapshot syrupy

pytest --snapshot-create   # pytest-snapshot: write baselines
pytest --snapshot-update   # syrupy / update baselines
pytest                     # compare against stored snapshots
```

### Generated config

```bash
python generate_nginx_config.py
# Prints the deterministic nginx server block used in the snapshot example
```
