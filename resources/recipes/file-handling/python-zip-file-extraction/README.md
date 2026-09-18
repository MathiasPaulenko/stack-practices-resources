# Safe Zip Extraction — Companion Code

Runnable version of the validation helpers from the
[Safely Extract Zip Files with Python](https://stackpractices.com/recipes/python-zip-file-extraction/)
recipe on StackPractices.

## Files

| File | Description |
|------|-------------|
| `safe_extract.py` | `validate_zip` (count + size + suspicious-path checks), `safe_extract` (path traversal guard via `relative_to`), `check_duplicates`, `quarantine_zip`, and a `unittest` suite covering normal, traversal, absolute-path, oversized and duplicate-entry archives |

## Requirements

- Python 3.10+ — no external dependencies.

## Usage

```python
from safe_extract import safe_extract, validate_zip

validate_zip("upload.zip", max_files=1000, max_total_size_mb=500)
count = safe_extract("upload.zip", "output_dir")
```

## Notes

- `is_safe_path` uses `Path.relative_to` (Python 3.9+) instead of a string
  `startswith` check, so it behaves correctly with Windows path separators
  and resolves symlinks before comparing.
- Validation happens before any byte is written to disk — a rejected
  archive leaves the target directory untouched.
- Quarantine rejected archives rather than deleting them if you need the
  evidence for incident response.
