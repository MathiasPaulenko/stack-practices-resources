"""Upload validation skeleton — run: python validate_upload.py

Demonstrates magic-byte MIME detection without third-party dependencies
(the recipe uses the `magic` package; this demo reads the signatures inline).
"""

ALLOWED_SIGNATURES = {
    b"\xff\xd8\xff": ".jpg",
    b"\x89PNG": ".png",
    b"GIF8": ".gif",
    b"%PDF": ".pdf",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def detect_mime(file_bytes: bytes) -> str | None:
    for signature, ext in ALLOWED_SIGNATURES.items():
        if file_bytes.startswith(signature):
            return ext
    return None


def validate_upload(file_bytes: bytes) -> str:
    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File exceeds 5MB limit")
    ext = detect_mime(file_bytes)
    if ext is None:
        raise ValueError("File type not allowed")
    return ext


# Demo
samples = {
    "png header": b"\x89PNG\r\n\x1a\n" + b"0" * 100,
    "pdf header": b"%PDF-1.7" + b"0" * 100,
    "fake png": b"MZ\x90\x00" + b"0" * 100,  # actually an EXE header
}
for name, data in samples.items():
    try:
        print(f"OK    {name}: accepted as {validate_upload(data)}")
    except ValueError as err:
        print(f"BLOCK {name}: {err}")
