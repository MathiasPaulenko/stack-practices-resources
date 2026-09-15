"""Invalidate CDN cache for specific paths."""

import boto3


def create_invalidation(distribution_id, paths):
    """Create a CloudFront invalidation for the given paths.

    Args:
        distribution_id: CloudFront distribution ID (e.g. E1ABC23DEF4GHI)
        paths: list of paths to invalidate (e.g. ["/js/app.js", "/css/*"])

    Returns:
        Invalidation ID string.
    """
    cloudfront = boto3.client("cloudfront")
    response = cloudfront.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {
                "Quantity": len(paths),
                "Items": paths,
            },
            "CallerReference": f"invalidation-{__import__('time').time()}",
        },
    )
    return response["Invalidation"]["Id"]


def list_invalidations(distribution_id, max_items=10):
    """List recent invalidations for a distribution."""
    cloudfront = boto3.client("cloudfront")
    response = cloudfront.list_invalidations(
        DistributionId=distribution_id,
        MaxItems=str(max_items),
    )
    return response["InvalidationList"]["Items"]


if __name__ == "__main__":
    inv_id = create_invalidation("E1ABC23DEF4GHI", ["/js/app.js", "/css/*"])
    print(f"Created invalidation: {inv_id}")
