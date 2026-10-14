# Read and Write Files in Python, Node.js & Bash — Companion Resources

Companion files for [Read and Write Files in Python, Node.js & Bash](https://stackpractices.com/recipes/read-write-file/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `safe_io.py` | `safe_write` (temp + `os.replace` + `fsync`), `safe_read` with default, `read_lines_lazy`, `write_json_atomic` |
| `stream-file.js` | Line-by-line Transform pipeline writing through a temp file, plus `readLines`/`appendLine` helpers |
| `FileOps.java` | NIO `atomicWrite` (`ATOMIC_MOVE`), `safeRead`, `readLines`, `appendLine`, `processLines` |
| `safe-file-ops.sh` | Bash `safe_write`, `safe_read`, `log_append`, `read_lines`, `create_secret_file` (`chmod 600`) |

## How to use

1. `python safe_io.py` — writes `demo.txt`, `state.json` and prints the read-back.
2. `node stream-file.js` — streams `input.log` → `output.log` uppercased, appends a timestamped line to `app.log`.
3. `javac FileOps.java && java FileOps` — atomic write + safe read + line processing demo.
4. `bash safe-file-ops.sh` — exercises every helper and prints results.

No dependencies — Python 3.10+, Node.js 18+, any modern JDK, Bash 4+.
