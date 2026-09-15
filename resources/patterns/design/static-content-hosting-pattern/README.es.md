# Patrón de Hosting de Contenido Estático — Recursos Companion

Scripts para subir y gestionar assets estáticos en almacenamiento de objetos con integración CDN.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `upload_assets.py` | Sube archivos a S3 con cache headers y versionado por hash de contenido |
| `invalidate_cache.py` | Crea invalidaciones de caché en CloudFront para rutas actualizadas |
| `generate_signed_urls.py` | Genera URLs firmadas con tiempo limitado para contenido privado |
| `resize_images.py` | Genera variantes de imagen responsivas y atributos srcset |

## Requisitos

```bash
pip install boto3 pillow cryptography
```

Configura las credenciales de AWS con `aws configure` o variables de entorno:

```bash
export AWS_ACCESS_KEY_ID=tu-access-key
export AWS_SECRET_ACCESS_KEY=tu-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

## Uso

### Subir un asset individual

```python
from upload_assets import upload_asset

url = upload_asset("dist/app.js", "myapp-assets", "js/app.js", "cdn.myapp.com")
print(url)  # https://cdn.myapp.com/js/app.js
```

### Subir con versionado por hash de contenido

```python
from upload_assets import upload_with_versioning

url = upload_with_versioning("dist/app.js", "myapp-assets", "js/app", "cdn.myapp.com")
print(url)  # https://cdn.myapp.com/js/app.abc12345.js
```

### Invalidar caché CDN

```python
from invalidate_cache import create_invalidation

inv_id = create_invalidation("E1ABC23DEF4GHI", ["/js/app.js", "/css/*"])
print(f"Invalidación: {inv_id}")
```

### Generar URL firmada para contenido privado

```python
from generate_signed_urls import generate_signed_url

url = generate_signed_url("myapp-private", "reports/q3-2026.pdf", expiration_seconds=3600)
print(url)  # Acceso con tiempo limitado a un PDF privado
```

### Generar variantes de imagen responsivas

```python
from resize_images import resize_image, generate_srcset

outputs = resize_image("source.jpg", "dist/images")
srcset = generate_srcset("source.jpg", "https://cdn.example.com/images")
print(srcset)  # https://cdn.example.com/images/source_thumbnail.jpg 150w, ...
```

## Fuente

- [Patrón de Hosting de Contenido Estático](https://stackpractices.com/es/patterns/static-content-hosting-pattern/)
