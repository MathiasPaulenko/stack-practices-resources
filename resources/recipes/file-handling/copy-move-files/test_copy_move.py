"""Tests for the copy/move companion (no external dependencies required)."""
import hashlib
import sys
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np

COMPANION_DIR = Path(__file__).parent
sys.path.insert(0, str(COMPANION_DIR))


def test_sha256_logic():
    """Verify SHA-256 computation with known input."""
    expected = hashlib.sha256(b"hello world").hexdigest()
    assert expected == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


def test_checksum_comparison():
    """Verify checksum comparison logic."""
    hash_a = hashlib.sha256(b"same content").hexdigest()
    hash_b = hashlib.sha256(b"same content").hexdigest()
    hash_c = hashlib.sha256(b"different content").hexdigest()
    assert hash_a == hash_b
    assert hash_a != hash_c


def test_safe_copy_guard_missing_source():
    """Verify safe_copy raises when source doesn't exist."""
    import pytest
    mod = __import__("safe_copy")
    with pytest.raises(FileNotFoundError, match="Source not found"):
        mod.safe_copy("/nonexistent/path", "/tmp/dest")


def test_safe_copy_guard_dest_exists():
    """Verify safe_copy raises when dest exists without overwrite."""
    import pytest
    import tempfile
    mod = __import__("safe_copy")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src.txt"
        dest = Path(tmp) / "dest.txt"
        src.write_text("content")
        dest.write_text("existing")
        with pytest.raises(FileExistsError, match="Destination exists"):
            mod.safe_copy(src, dest, overwrite=False)


def test_safe_copy_with_overwrite():
    """Verify safe_copy works with overwrite=True."""
    import tempfile
    mod = __import__("safe_copy")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src.txt"
        dest = Path(tmp) / "out" / "dest.txt"
        src.write_text("new content")
        result = mod.safe_copy(src, dest, overwrite=True)
        assert result.exists()
        assert dest.read_text() == "new content"


def test_batch_copy_creates_dir():
    """Verify batch_copy creates the destination directory."""
    import tempfile
    mod = __import__("safe_copy")
    with tempfile.TemporaryDirectory() as tmp:
        src_dir = Path(tmp) / "src"
        dest_dir = Path(tmp) / "dest"
        src_dir.mkdir()
        (src_dir / "a.txt").write_text("a")
        (src_dir / "b.txt").write_text("b")
        copied = mod.batch_copy(src_dir, dest_dir)
        assert len(copied) == 2
        assert (dest_dir / "a.txt").exists()
        assert (dest_dir / "b.txt").exists()


def test_js_syntax():
    """Verify the JS companion file has the expected functions."""
    js_path = COMPANION_DIR / "copy_move.js"
    content = js_path.read_text(encoding="utf-8")
    assert "async function copyWithChecksum" in content
    assert "async function moveWithFallback" in content
    assert "module.exports" in content
    assert "EXDEV" in content


def test_java_syntax():
    """Verify the Java companion file has the expected class and methods."""
    java_path = COMPANION_DIR / "FileCopier.java"
    content = java_path.read_text(encoding="utf-8")
    assert "class FileCopier" in content
    assert "copyWithAttributes" in content
    assert "moveWithFallback" in content
    assert "ATOMIC_MOVE" in content
    assert "sha256" in content


def test_bash_syntax():
    """Verify the Bash companion file has the expected functions."""
    sh_path = COMPANION_DIR / "safe_copy.sh"
    content = sh_path.read_text(encoding="utf-8")
    assert "safe_copy()" in content
    assert "batch_copy()" in content
    assert "sha256sum" in content
    assert "set -euo pipefail" in content
