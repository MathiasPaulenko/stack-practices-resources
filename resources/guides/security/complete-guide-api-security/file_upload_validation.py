import magic

ALLOWED_MIME_TYPES = {
    "image/jpeg": {"jpg", "jpeg"},
    "image/png": {"png"},
    "image/webp": {"webp"},
    "application/pdf": {"pdf"},
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_file_upload(file_bytes: bytes, filename: str) -> str:
    # Check file size
    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError(f"File exceeds {MAX_FILE_SIZE // 1024 // 1024}MB limit")
    
    # Check file extension
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    
    # Detect actual MIME type from content (not from extension)
    mime = magic.from_buffer(file_bytes, mime=True)
    
    if mime not in ALLOWED_MIME_TYPES:
        raise ValueError(f"File type {mime} not allowed")
    
    if ext not in ALLOWED_MIME_TYPES[mime]:
        raise ValueError(f"Extension .{ext} does not match MIME type {mime}")
    
    # Check for embedded scripts in images
    if mime.startswith("image/"):
        if b"<script" in file_bytes.lower() or b"<?php" in file_bytes.lower():
            raise ValueError("File contains embedded scripts")
    
    return mime

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    mime_type = validate_file_upload(content, file.filename)
    
    # Never trust the user-supplied name — generate your own
    import secrets, os
    ext = os.path.splitext(file.filename)[1].lower()
    safe_filename = f"{secrets.token_hex(8)}{ext}"
    filepath = f"/uploads/{safe_filename}"
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    return {"filename": safe_filename, "mime_type": mime_type}
