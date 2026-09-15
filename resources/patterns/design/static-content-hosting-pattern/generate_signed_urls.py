"""Generate signed URLs for private static content."""

import boto3
from datetime import datetime, timedelta, timezone


def generate_signed_url(bucket, key, expiration_seconds=3600):
    """Generate a time-limited signed URL for a private S3 object.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        expiration_seconds: URL validity in seconds (default 1 hour).

    Returns:
        Signed URL string valid until expiration.
    """
    s3 = boto3.client("s3")
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration_seconds,
    )


def generate_signed_cookie(distribution_id, key_pair_id, private_key_path, resource_path, expiration_hours=1):
    """Generate a CloudFront signed cookie for protected content.

    Args:
        distribution_id: CloudFront distribution domain.
        key_pair_id: CloudFront key pair ID.
        private_key_path: path to the RSA private key PEM file.
        resource_path: URL pattern the cookie grants access to (e.g. "https://cdn.example.com/private/*").
        expiration_hours: cookie validity in hours.

    Returns:
        Dict with cookie name-value pairs to set in the response.
    """
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    import base64
    import time

    expiry = int(time.time()) + expiration_hours * 3600
    policy = (
        '{"Statement":[{"Resource":"' + resource_path + '",'
        '"Condition":{"DateLessThan":{"AWS:EpochTime":' + str(expiry) + '}}}]}'
    )

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    signature = private_key.sign(
        policy.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA1(),
    )
    signed_policy = base64.b64encode(policy.encode("utf-8")).decode("utf-8")
    signed_signature = base64.b64encode(signature).decode("utf-8")

    return {
        "CloudFront-Policy": signed_policy,
        "CloudFront-Signature": signed_signature,
        "CloudFront-Key-Pair-Id": key_pair_id,
    }


if __name__ == "__main__":
    url = generate_signed_url("myapp-private", "reports/q3-2026.pdf", 3600)
    print(f"Signed URL (valid 1h): {url}")
