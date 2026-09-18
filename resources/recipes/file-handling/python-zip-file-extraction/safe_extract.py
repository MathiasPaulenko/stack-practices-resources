"""Safe zip extraction — runnable companion code.

Companion to https://stackpractices.com/recipes/python-zip-file-extraction/

Validates a zip archive before extracting: file count cap, total
uncompressed size cap, and a path traversal check that resolves every
member path and rejects anything outside the extraction directory.

Run the tests:

    python -m unittest safe_extract -v
"""

from __future__ import annotations

import logging
import shutil
import unittest
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_zip(
    zip_path: str | Path,
    max_files: int = 1000,
    max_total_size_mb: int = 500,
) -> bool:
    """Validate a zip archive. Raises ValueError on any failed check."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        files = zf.namelist()
        if len(files) > max_files:
            raise ValueError(f"Too many files: {len(files)} (max {max_files})")

        total_size = sum(info.file_size for info in zf.infolist())
        if total_size > max_total_size_mb * 1024 * 1024:
            raise ValueError(
                f"Archive too large: {total_size / 1024 / 1024:.1f}MB"
            )

        for member in files:
            if member.startswith("/") or ".." in member:
                raise ValueError(f"Unsafe path in archive: {member}")
    return True


def is_safe_path(extract_dir: Path, member_name: str) -> bool:
    """Check that a zip member resolves inside the extraction directory."""
    target = (extract_dir / member_name).resolve()
    try:
        target.relative_to(extract_dir.resolve())
        return True
    except ValueError:
        return False


def safe_extract(zip_path: str | Path, extract_to: str | Path) -> int:
    """Extract a zip after validating every member path. Returns count."""
    dest = Path(extract_to)
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            if not is_safe_path(dest, member):
                raise ValueError(f"Path traversal detected: {member}")
        zf.extractall(dest)
        return len(zf.namelist())


def check_duplicates(zip_path: str | Path) -> list[str]:
    """Find filenames that appear more than once in the archive."""
    from collections import Counter

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = [m for m in zf.namelist() if not m.endswith("/")]
    counts = Counter(names)
    return [name for name, count in counts.items() if count > 1]


def quarantine_zip(zip_path: str | Path, reason: str,
                   quarantine_dir: Path) -> Path:
    """Move a suspicious zip to quarantine. Returns the new path."""
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    dest = quarantine_dir / Path(zip_path).name
    shutil.move(str(zip_path), str(dest))
    logger.warning("Quarantined %s: %s", zip_path, reason)
    return dest


class TestSafeExtract(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self.tmp = Path(tempfile.mkdtemp())

    def _make_zip(self, members: dict[str, bytes]) -> Path:
        z = self.tmp / "test.zip"
        with zipfile.ZipFile(z, "w") as zf:
            for name, data in members.items():
                zf.writestr(name, data)
        return z

    def test_normal_zip_extracts(self) -> None:
        z = self._make_zip({"a.txt": b"hello", "sub/b.txt": b"world"})
        out = self.tmp / "out"
        self.assertEqual(safe_extract(z, out), 2)
        self.assertEqual((out / "a.txt").read_bytes(), b"hello")
        self.assertEqual((out / "sub" / "b.txt").read_bytes(), b"world")

    def test_path_traversal_rejected(self) -> None:
        z = self._make_zip({"../evil.txt": b"bad"})
        with self.assertRaises(ValueError):
            safe_extract(z, self.tmp / "out")

    def test_absolute_path_rejected(self) -> None:
        z = self._make_zip({"/etc/passwd": b"bad"})
        with self.assertRaises(ValueError):
            validate_zip(z)

    def test_too_many_files_rejected(self) -> None:
        z = self._make_zip({f"f{i}.txt": b"x" for i in range(5)})
        with self.assertRaises(ValueError):
            validate_zip(z, max_files=3)

    def test_oversized_archive_rejected(self) -> None:
        z = self._make_zip({"big.bin": b"x" * 1024})
        with self.assertRaises(ValueError):
            validate_zip(z, max_total_size_mb=0)

    def test_duplicates_detected(self) -> None:
        z = self._make_zip({"dup.txt": b"1"})
        with zipfile.ZipFile(z, "a") as zf:
            zf.writestr("dup.txt", b"2")
        self.assertEqual(check_duplicates(z), ["dup.txt"])


if __name__ == "__main__":
    unittest.main()
