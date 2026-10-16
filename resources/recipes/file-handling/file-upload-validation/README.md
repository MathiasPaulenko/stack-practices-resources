# File Upload Validation — Companion Resources

Runnable code referenced by
[File Upload Validation: Secure File Handling Guide](https://stackpractices.com/recipes/file-upload-validation/).

| File | Purpose |
| --- | --- |
| `validate_upload.py` | Layered Flask/Werkzeug validator: extension, size, magic bytes |
| `upload.js` | multer setup + `file-type` magic-byte verification (ESM-safe) |
| `UploadValidator.java` | Spring Boot size + content-type allow-list |
| `upload_quota.py` | Redis quotas, safe ZIP extraction (decompression bombs), security logging |
| `nginx-uploads.conf` | `Content-Disposition: attachment` + hardening headers for `/uploads/` |

Validation runs in layers — extension and MIME first (cheap), then magic
bytes, then AV/re-encoding. Never trust a single check.
