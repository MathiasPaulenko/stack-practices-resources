"""Upload static assets to S3 with CDN integration."""

import boto3
import hashlib
import mimetypes
from pathlib import Path


def upload_asset(local_path, bucket, s3_key, cdn_domain=None, cache_control="public, max-age=31536000, immutable"):
    """Upload a single file to S3 and return the CDN URL."""
    s3 = boto3.client("s3")
    content_type, _ = mimetypes.guess_type(local_path)
    content_type = content_type or "application/octet-stream"

    s3.upload_file(
        str(local_path),
        bucket,
        s3_key,
        ExtraArgs={
            "ContentType": content_type,
            "CacheControl": cache_control,
            "ACL": "public-read",
        },
    )

    domain = cdn_domain or f"{bucket}.s3.amazonaws.com"
    return f"https://{domain}/{s3_key}"


def upload_with_versioning(local_path, bucket, base_key, cdn_domain=None):
    """Upload with content hash in filename for cache busting."""
    content = Path(local_path).read_bytes()
    file_hash = hashlib.md5(content).hexdigest()[:8]
    ext = Path(local_path).suffix
    versioned_key = f"{base_key}.{file_hash}{ext}"
    return upload_asset(local_path, bucket, versioned_key, cdn_domain)


def upload_directory(local_dir, bucket, prefix="", cdn_domain=None):
    """Upload all files in a directory to S3."""
    base = Path(local_dir)
    urls = []
    for path in base.rglob("*"):
        if path.is_file():
            s3_key = f"{prefix}/{path.relative_to(base)}".replace("\\", "/")
            url = upload_asset(str(path), bucket, s3_key, cdn_domain)
            urls.append(url)
    return urls


if __name__ == "__main__":
    url = upload_asset("dist/app.js", "myapp-assets", "js/app.js", "cdn.myapp.com")
    print(f"Uploaded: {url}")
