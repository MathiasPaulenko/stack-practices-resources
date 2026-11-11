"""Temporary file and directory patterns from the Generate Temporary Files recipe.

Run: python temp_files.py
"""

import os
import shutil
import tempfile


def auto_cleanup_file() -> None:
    """NamedTemporaryFile deletes itself when the context manager exits."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=True) as f:
        f.write('{"key": "value"}')
        f.flush()
        path = f.name
        print(f"temp file inside context: {path} (exists={os.path.exists(path)})")
    print(f"after context: exists={os.path.exists(path)}")


def auto_cleanup_dir() -> None:
    """TemporaryDirectory removes the tree on context exit."""
    with tempfile.TemporaryDirectory(prefix="myapp-") as tmpdir:
        with open(os.path.join(tmpdir, "report.txt"), "w") as f:
            f.write("temporary report data")
        print(f"temp dir inside context: {tmpdir}")
    print(f"after context: exists={os.path.exists(tmpdir)}")


def manual_cleanup_for_external_process() -> None:
    """delete=False when an external tool needs the path; clean up yourself."""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    try:
        tmp.write("id,name\n1,Alice\n")
        tmp.close()  # close before handing the path out (Windows-safe)
        print(f"hand to external tool: {tmp.name}")
    finally:
        os.unlink(tmp.name)
        print("manual cleanup done")


def atomic_update(target: str, data: bytes) -> None:
    """Write-temp-then-rename in the SAME directory: atomic on one filesystem."""
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(target) or ".",
        prefix=".tmp-",
        suffix=".partial",
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())  # durable before the rename
        os.replace(tmp_path, target)  # atomic; works on Windows too
    except BaseException:
        os.unlink(tmp_path)  # never leave the partial file behind
        raise


def recursive_cleanup() -> None:
    """os.rmdir only removes empty dirs; shutil.rmtree handles nesting."""
    tmpdir = tempfile.mkdtemp(prefix="nested-")
    try:
        nested = os.path.join(tmpdir, "a", "b", "c")
        os.makedirs(nested)
        with open(os.path.join(nested, "file.txt"), "w") as f:
            f.write("data")
        shutil.rmtree(tmpdir)
    finally:
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"nested temp dir removed: exists={os.path.exists(tmpdir)}")


if __name__ == "__main__":
    auto_cleanup_file()
    auto_cleanup_dir()
    manual_cleanup_for_external_process()
    recursive_cleanup()

    target = os.path.join(tempfile.gettempdir(), "atomic-demo.json")
    atomic_update(target, b'{"version": 2}')
    print(f"atomic update wrote: {target}")
    os.unlink(target)
