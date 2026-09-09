# Copy and Move Files — Companion Examples

Companion code for the [Copy and Move Files recipe](https://stackpractices.com/recipes/copy-move-files/).

## Files

| File | Description |
| ---- | ----------- |
| `safe_copy.py` | Python safe copy/move with shutil, pathlib, and SHA-256 verification |
| `copy_move.js` | JavaScript copy/move with fs.promises, checksums, and EXDEV fallback |
| `FileCopier.java` | Java NIO copy/move with ATOMIC_MOVE and cross-device fallback |
| `safe_copy.sh` | Bash safe copy with sha256sum verification and batch copy |
| `test_copy_move.py` | Unit tests (run without external dependencies) |

## Quick start (Python)

```bash
python safe_copy.py
```

## Quick start (JavaScript)

```bash
node copy_move.js
```

## Run tests

```bash
pip install pytest
pytest test_copy_move.py -v
```

## Author

Mathias Paulenko — [StackPractices.com](https://stackpractices.com)
