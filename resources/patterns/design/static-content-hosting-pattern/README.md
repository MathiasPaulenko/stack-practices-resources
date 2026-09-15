# Static Content Hosting Pattern — Companion Resources

Scripts for uploading and managing static assets on object storage with CDN integration.

## Files

| File | Purpose |
|------|---------|
| `upload_assets.py` | Upload files to S3 with cache headers and content hash versioning |
| `invalidate_cache.py` | Create CloudFront cache invalidations for updated paths |
| `generate_signed_urls.py` | Generate time-limited signed URLs for private content |
| `resize_images.py` | Generate responsive image variants and srcset attributes |

## Requirements

```bash
pip install boto3 pillow cryptography
```

Configure AWS credentials via `aws configure` or environment variables:

```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

## Usage

### Upload a single asset

```python
from upload_assets import upload_asset

url = upload_asset("dist/app.js", "myapp-assets", "js/app.js", "cdn.myapp.com")
print(url)  # https://cdn.myapp.com/js/app.js
```

### Upload with content hash versioning

```python
from upload_assets import upload_with_versioning

url = upload_with_versioning("dist/app.js", "myapp-assets", "js/app", "cdn.myapp.com")
print(url)  # https://cdn.myapp.com/js/app.abc12345.js
```

### Invalidate CDN cache

```python
from invalidate_cache import create_invalidation

inv_id = create_invalidation("E1ABC23DEF4GHI", ["/js/app.js", "/css/*"])
print(f"Invalidation: {inv_id}")
```

### Generate a signed URL for private content

```python
from generate_signed_urls import generate_signed_url

url = generate_signed_url("myapp-private", "reports/q3-2026.pdf", expiration_seconds=3600)
print(url)  # Time-limited access to a private PDF
```

### Generate responsive image variants

```python
from resize_images import resize_image, generate_srcset

outputs = resize_image("source.jpg", "dist/images")
srcset = generate_srcset("source.jpg", "https://cdn.example.com/images")
print(srcset)  # https://cdn.example.com/images/source_thumbnail.jpg 150w, ...
```

## Source

- [Static Content Hosting Pattern](https://stackpractices.com/patterns/static-content-hosting-pattern/)
