"""Per-user upload quotas with Redis.

Check quota before the expensive checks; consume only after the file
passes validation — otherwise rejected uploads still eat quota.

See https://stackpractices.com/recipes/file-upload-validation/
"""
import logging
import zipfile

import redis

r = redis.Redis()
logger = logging.getLogger("upload_security")

MAX_DECOMPRESSED_SIZE = 100 * 1024 * 1024  # 100 MB


def has_quota(user_id: str, file_size: int, max_quota: int = 100 * 1024 * 1024) -> bool:
    key = f"upload_quota:{user_id}"
    used = int(r.get(key) or 0)
    return used + file_size <= max_quota


def consume_quota(user_id: str, file_size: int) -> None:
    r.incrby(f"upload_quota:{user_id}", file_size)


def safe_extract_zip(zip_path: str, dest_dir: str) -> int:
    """Extract a ZIP with decompression-bomb protection."""
    total_size = 0
    count = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            total_size += info.file_size
            if total_size > MAX_DECOMPRESSED_SIZE:
                raise ValueError(f"Decompression bomb: {total_size} bytes")
            zf.extract(info, dest_dir)
            count += 1
    return count


def validate_upload_with_logging(file_storage, user_id: str, validate_upload):
    """Wrap the validator with security-event logging."""
    try:
        filename = validate_upload(file_storage)
        logger.info(f"Upload accepted: user={user_id} file={filename}")
        return filename
    except ValueError as e:
        logger.warning(
            f"Upload rejected: user={user_id} reason={e} filename={file_storage.filename}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Upload error: user={user_id} error={e} filename={file_storage.filename}",
            exc_info=True,
        )
        raise
