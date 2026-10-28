"""S3 presigned-URL upload flow: sign server-side, PUT client-side.

Usage:
    python s3_upload.py --bucket my-bucket --key uploads/report.pdf --file report.pdf
Requires AWS credentials in environment (IAM role, aws configure, or env vars).
"""

import argparse

import boto3
import requests


def create_upload_url(bucket: str, key: str, content_type: str, expires: int = 900) -> str:
    """Generate a presigned PUT URL with a 15-minute default expiry."""
    s3 = boto3.client("s3")
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key, "ContentType": content_type},
        ExpiresIn=expires,
    )


def create_download_url(bucket: str, key: str, expires: int = 3600) -> str:
    """Generate a presigned GET URL."""
    s3 = boto3.client("s3")
    return s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires
    )


def upload_file(url: str, path: str, content_type: str) -> int:
    with open(path, "rb") as f:
        r = requests.put(url, data=f, headers={"Content-Type": content_type})
    r.raise_for_status()
    return r.status_code


def multipart_upload(bucket: str, key: str, path: str) -> None:
    """Upload a large file with automatic multipart above 50 MB."""
    from boto3.s3.transfer import TransferConfig

    config = TransferConfig(
        multipart_threshold=50 * 1024 * 1024,
        multipart_chunksize=25 * 1024 * 1024,
        max_concurrency=10,
    )
    boto3.client("s3").upload_file(path, bucket, key, Config=config)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--bucket", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--file")
    p.add_argument("--type", default="application/octet-stream")
    args = p.parse_args()

    url = create_upload_url(args.bucket, args.key, args.type)
    print(f"Presigned PUT URL (15 min): {url[:120]}...")
    if args.file:
        status = upload_file(url, args.file, args.type)
        print(f"Upload finished: HTTP {status}")
