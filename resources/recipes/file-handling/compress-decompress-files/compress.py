"""Archive utilities for Python: streaming compression and safe extraction.

Requires Python 3.9+ (is_relative_to). Standard library only.
"""

import gzip
import tarfile
import zipfile
from pathlib import Path


def compress_directory_streaming(src_dir: str, dest_zip: str,
                                 level: int = 6) -> int:
    """Compress a directory to ZIP entry by entry. Returns file count."""
    src_path = Path(src_dir)
    file_count = 0
    with zipfile.ZipFile(dest_zip, 'w', zipfile.ZIP_DEFLATED,
                         compresslevel=level) as zf:
        for file_path in sorted(src_path.rglob('*')):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(src_path))
                file_count += 1
    return file_count


def decompress_zip_safe(zip_path: str, dest_dir: str,
                        max_size: int = 1 << 30) -> int:
    """Extract ZIP with zip-slip and zip-bomb protection."""
    dest_path = Path(dest_dir).resolve()
    dest_path.mkdir(parents=True, exist_ok=True)
    total = 0
    count = 0
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            member = info.filename
            member_path = (dest_path / member).resolve()
            if not member_path.is_relative_to(dest_path):
                raise ValueError(f"Unsafe path detected: {member}")
            total += info.file_size
            if total > max_size:
                raise ValueError(f"Archive exceeds {max_size} bytes")
            zf.extract(member, dest_path)
            count += 1
    return count


def gzip_file_streaming(src: str, dest: str, level: int = 6) -> None:
    """GZIP a single file in 64 KB chunks."""
    with open(src, 'rb') as f_in, gzip.open(dest, 'wb',
                                           compresslevel=level) as f_out:
        while chunk := f_in.read(65536):
            f_out.write(chunk)


def tar_directory(src_dir: str, dest: str, mode: str = 'w:gz') -> None:
    """Create a TAR.GZ archive of a directory."""
    with tarfile.open(dest, mode) as tar:
        tar.add(src_dir, arcname=Path(src_dir).name, recursive=True)


def list_archive_contents(archive_path: str) -> list[str]:
    """List contents of a ZIP or TAR archive."""
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            return zf.namelist()
    if archive_path.endswith(('.tar.gz', '.tgz', '.tar')):
        with tarfile.open(archive_path, 'r:*') as tar:
            return tar.getnames()
    raise ValueError(f"Unsupported archive format: {archive_path}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd, src, dest = sys.argv[1], sys.argv[2], sys.argv[3] if len(
        sys.argv) > 3 else 'out'
    if cmd == 'zip':
        print(f"Compressed {compress_directory_streaming(src, dest)} files")
    elif cmd == 'unzip':
        print(f"Extracted {decompress_zip_safe(src, dest)} files")
    elif cmd == 'gzip':
        gzip_file_streaming(src, dest)
    elif cmd == 'tar':
        tar_directory(src, dest)
    elif cmd == 'list':
        for name in list_archive_contents(src):
            print(name)
