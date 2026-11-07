"""Compression-ratio benchmark across payload types and levels.

Shows why thresholds and already-compressed formats matter:
JSON/HTML compress to ~15-30%, random bytes grow slightly.

Usage:
    python ratio_benchmark.py
"""
import gzip
import os
import zlib

try:
    import brotli  # pip install brotli
    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False


def ratio(original: bytes, compressed: bytes) -> str:
    return f"{len(compressed)} B ({len(compressed) / len(original) * 100:.1f}%)"


def benchmark(name: str, data: bytes) -> None:
    gz = gzip.compress(data, compresslevel=6)
    row = f"{name:<28} {len(data):>8} B -> gzip-6 {ratio(data, gz):>18}"
    if HAS_BROTLI:
        br = brotli.compress(data, quality=6)
        row += f" | brotli-6 {ratio(data, br):>18}"
    print(row)


if __name__ == "__main__":
    benchmark(
        "JSON (repetitive)",
        (b'{"user":"alice","role":"admin","active":true},' * 2000),
    )
    benchmark(
        "HTML document",
        (b"<html><body><div class='card'><p>text</p></div>" * 3000),
    )
    benchmark(
        "Log lines",
        (b"2026-11-06 10:00:00 INFO handler ok\n" * 4000),
    )
    benchmark(
        "Random bytes (incompressible)",
        os.urandom(100_000),
    )
    benchmark(
        "Tiny payload (<1KB threshold)",
        b'{"ok":true}' * 10,
    )
    if not HAS_BROTLI:
        print("(install `brotli` to include Brotli numbers)")
