"""Streaming Gzip compression with SHA256 integrity verification.

Usage:
    python gzip_streaming.py
"""
import gzip
import hashlib
import os
import tempfile


def gzip_streaming(src: str, dest: str, level: int = 6) -> str:
    """Compress a file with streaming. Returns SHA256 of the original."""
    hasher = hashlib.sha256()
    with open(src, "rb") as f_in, gzip.open(dest, "wb", compresslevel=level) as f_out:
        while chunk := f_in.read(65536):
            hasher.update(chunk)
            f_out.write(chunk)
    return hasher.hexdigest()


def gunzip_streaming(src: str, dest: str, expected_sha256: str | None = None) -> bool:
    """Decompress with optional integrity verification. Returns True if valid."""
    hasher = hashlib.sha256()
    with gzip.open(src, "rb") as f_in, open(dest, "wb") as f_out:
        while chunk := f_in.read(65536):
            hasher.update(chunk)
            f_out.write(chunk)
    return expected_sha256 is None or hasher.hexdigest() == expected_sha256


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "sample.log")
        gz = src + ".gz"
        restored = os.path.join(tmp, "restored.log")

        # repetitive log-like content compresses well
        with open(src, "wb") as f:
            f.write(b"2026-11-06 INFO request handled path=/api/users status=200\n" * 5000)

        sha = gzip_streaming(src, gz, level=6)
        original = os.path.getsize(src)
        compressed = os.path.getsize(gz)
        ok = gunzip_streaming(gz, restored, expected_sha256=sha)

        print(f"Original:   {original} bytes")
        print(f"Compressed: {compressed} bytes ({compressed / original * 100:.1f}%)")
        print(f"SHA256:     {sha[:16]}...")
        print(f"Integrity:  {'PASS' if ok else 'FAIL'}")
