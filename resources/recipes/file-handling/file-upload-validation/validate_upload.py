"""Layered file upload validation for Flask/Werkzeug.

Extension check -> size limit -> magic bytes via libmagic.
Requires: python-magic, werkzeug.

See https://stackpractices.com/recipes/file-upload-validation/
"""
import os

import magic
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

EXPECTED_MIMES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "pdf": "application/pdf",
}


def validate_upload(file_storage) -> str:
    """Return the sanitized filename or raise ValueError."""
    # 1. Extension
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension not allowed: {ext}")

    # 2. Size
    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")

    # 3. Magic bytes vs declared extension
    mime = magic.from_buffer(file_storage.read(2048), mime=True)
    file_storage.seek(0)
    if mime != EXPECTED_MIMES.get(ext):
        raise ValueError(f"MIME mismatch: got {mime}, expected {EXPECTED_MIMES.get(ext)}")

    return filename
