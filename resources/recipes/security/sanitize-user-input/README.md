# Sanitize User Input — Companion Resources

Companion files for [Sanitize User Input](https://stackpractices.com/recipes/sanitize-user-input/) on StackPractices.

## Files

| File | What it demonstrates |
|------|----------------------|
| `path_traversal_guard.js` | Resolving a user path under an allowed base and rejecting `../` escapes and null bytes |
| `nosql_sanitize.js` | Stripping `$`-prefixed operators from user-supplied query objects |
| `validate_upload.py` | Magic-byte file type detection and size limits (stdlib only — no `magic` dependency needed for the demo) |

## How to use

```bash
node path_traversal_guard.js
node nosql_sanitize.js
python validate_upload.py
```

No dependencies beyond Node.js ≥ 18 and Python ≥ 3.10.
