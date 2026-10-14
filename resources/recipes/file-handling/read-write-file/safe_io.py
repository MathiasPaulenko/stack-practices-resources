"""Safe file read/write utilities for Python.

Atomic writes (temp file + os.replace), graceful reads with defaults,
and JSON serialization helpers. Python 3.10+ (uses `X | None` unions).
"""

import os
import tempfile
from pathlib import Path
from typing import Any


def safe_write(path: str | Path, data: str, encoding: str = "utf-8") -> None:
    """Write text atomically: temp file + rename. Safe against crashes."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, suffix=".tmp", prefix=path.name
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def safe_read(
    path: str | Path, encoding: str = "utf-8", default: str | None = None
) -> str | None:
    """Read text with graceful fallback for missing files."""
    path = Path(path)
    if not path.exists():
        return default
    try:
        return path.read_text(encoding=encoding)
    except PermissionError:
        raise PermissionError(f"Cannot read {path}: permission denied")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"File {path} is not valid {encoding}",
        )


def read_lines_lazy(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """Read file lines, dropping blanks and trailing newlines."""
    path = Path(path)
    with path.open("r", encoding=encoding) as f:
        return [line.rstrip("\n\r") for line in f if line.strip()]


def write_json_atomic(path: str | Path, data: Any, indent: int = 2) -> None:
    """Serialize JSON and write atomically."""
    import json

    text = json.dumps(data, indent=indent, ensure_ascii=False, default=str)
    safe_write(path, text)


if __name__ == "__main__":
    demo = Path("demo.txt")
    safe_write(demo, "key: value\n")
    print(safe_read(demo, default="key: default\n"), end="")
    write_json_atomic("state.json", {"users": 42, "active": 10})
    print(read_lines_lazy(demo))
