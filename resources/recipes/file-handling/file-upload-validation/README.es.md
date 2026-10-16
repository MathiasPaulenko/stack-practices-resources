# Validación de Subida de Archivos — Recursos complementarios

Código ejecutable referenciado en
[Validación de Subida de Archivos](https://stackpractices.com/es/recipes/file-upload-validation/).

| Archivo | Propósito |
| --- | --- |
| `validate_upload.py` | Validador por capas para Flask/Werkzeug: extensión, tamaño, magic bytes |
| `upload.js` | Setup de multer + verificación de magic bytes con `file-type` (ESM-safe) |
| `UploadValidator.java` | Allow-list de tamaño + content-type para Spring Boot |
| `upload_quota.py` | Cuotas con Redis, extracción ZIP segura (bombas de descompresión), logging de seguridad |
| `nginx-uploads.conf` | `Content-Disposition: attachment` + headers de hardening para `/uploads/` |

La validación corre por capas — extensión y MIME primero (barato), luego
magic bytes, después AV/re-codificación. Nunca confíes en una sola verificación.
