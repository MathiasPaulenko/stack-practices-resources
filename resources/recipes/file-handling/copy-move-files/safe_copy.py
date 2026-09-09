"""Safe copy and move with shutil, pathlib, and SHA-256 verification."""
import hashlib
import shutil
from pathlib import Path


def safe_copy(src, dest, *, overwrite=False, verify=True, follow_symlinks=False):
    """Copy a file, preserving metadata and optionally verifying integrity."""
    src, dest = Path(src), Path(dest)
    if not src.exists():
        raise FileNotFoundError(f"Source not found: {src}")
    if dest.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)

    if src.is_symlink() and not follow_symlinks:
        dest.symlink_to(Path(src).readlink())
    else:
        shutil.copy2(src, dest)

    if verify and not src.is_symlink():
        src_hash = hashlib.sha256(src.read_bytes()).hexdigest()
        dest_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
        if src_hash != dest_hash:
            dest.unlink()
            raise IOError(f"Checksum mismatch: {src} -> {dest}")
    return dest


def safe_move(src, dest, *, overwrite=False):
    """Move a file, falling back to copy+delete across filesystems."""
    src, dest = Path(src), Path(dest)
    if not src.exists():
        raise FileNotFoundError(f"Source not found: {src}")
    if dest.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dest))
    except shutil.Error:
        safe_copy(src, dest, overwrite=overwrite, verify=True)
        src.unlink()
    return dest


def batch_copy(src_dir, dest_dir, pattern="*", *, overwrite=False):
    """Copy all files matching a pattern from src_dir to dest_dir."""
    src_dir, dest_dir = Path(src_dir), Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for file in src_dir.glob(pattern):
        if file.is_file():
            copied.append(safe_copy(file, dest_dir / file.name, overwrite=overwrite))
    return copied


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "test.txt"
        src.write_text("hello world")
        dest = Path(tmp) / "out" / "test.txt"
        safe_copy(src, dest)
        print(f"Copied {src} -> {dest}")
        safe_move(dest, Path(tmp) / "moved.txt")
        print(f"Moved to {Path(tmp) / 'moved.txt'}")
