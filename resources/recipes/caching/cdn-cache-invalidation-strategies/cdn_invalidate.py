"""CDN cache invalidation helpers for Cloudflare, Fastly and AWS CloudFront.

Companion code for:
https://stackpractices.com/recipes/cdn-cache-invalidation-strategies/

Environment variables expected:
    CLOUDFLARE_ZONE_ID, CLOUDFLARE_API_TOKEN
    FASTLY_SERVICE_ID, FASTLY_API_KEY
    AWS credentials configured for boto3 (for CloudFront)

Requires: httpx (Cloudflare/Fastly), boto3 (CloudFront).
"""

import asyncio
import os
import time

import boto3
import httpx

CLOUDFLARE_API = "https://api.cloudflare.com/client/v4"
FASTLY_API = "https://api.fastly.com"


async def purge_cloudflare_urls(zone_id: str, api_token: str, urls: list[str]) -> dict:
    """Purge specific URLs from Cloudflare's cache."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CLOUDFLARE_API}/zones/{zone_id}/purge_cache",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            json={"files": urls},
        )
        response.raise_for_status()
        return response.json()


async def purge_cloudflare_tags(zone_id: str, api_token: str, tags: list[str]) -> dict:
    """Purge all URLs with matching Cache-Tag headers (Enterprise plan)."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CLOUDFLARE_API}/zones/{zone_id}/purge_cache",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            json={"tags": tags},
        )
        response.raise_for_status()
        return response.json()


async def purge_cloudflare_everything(zone_id: str, api_token: str) -> dict:
    """Purge the entire Cloudflare zone cache."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CLOUDFLARE_API}/zones/{zone_id}/purge_cache",
            headers={"Authorization": f"Bearer {api_token}"},
            json={"purge_everything": True},
        )
        response.raise_for_status()
        return response.json()


async def purge_fastly_urls(service_id: str, api_key: str, urls: list[str]) -> list[dict]:
    """Purge specific URLs from Fastly's cache."""
    results = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.post(
                f"{FASTLY_API}/purge/{url}",
                headers={"Fastly-Key": api_key},
            )
            results.append(response.json())
    return results


async def purge_fastly_key(service_id: str, api_key: str, surrogate_key: str) -> dict:
    """Purge all URLs tagged with a Fastly surrogate key."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTLY_API}/service/{service_id}/purge/{surrogate_key}",
            headers={"Fastly-Key": api_key},
        )
        response.raise_for_status()
        return response.json()


async def soft_purge_fastly(service_id: str, api_key: str, surrogate_key: str) -> dict:
    """Soft purge: mark objects stale so edges serve stale while revalidating."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTLY_API}/service/{service_id}/purge/{surrogate_key}",
            headers={
                "Fastly-Key": api_key,
                "Fastly-Soft-Purge": "1",
            },
        )
        response.raise_for_status()
        return response.json()


def invalidate_cloudfront(distribution_id: str, paths: list[str]) -> dict:
    """Create a CloudFront invalidation for path patterns like /products/*."""
    client = boto3.client("cloudfront")
    return client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {
                "Quantity": len(paths),
                "Items": paths,
            },
            "CallerReference": str(int(time.time())),
        },
    )


async def invalidate_product(
    product_id: str,
    category_id: str,
    zone_id: str,
    api_token: str,
) -> dict:
    """Invalidate every cache entry related to a product via Cloudflare tags."""
    tags = [
        f"product-{product_id}",
        f"category-{category_id}",
        "search-results",
        "product-feed",
    ]
    return await purge_cloudflare_tags(zone_id, api_token, tags)


async def invalidate_on_deploy() -> None:
    """Purge the whole edge cache after a deployment, based on CDN_PROVIDER."""
    cdn = os.getenv("CDN_PROVIDER")
    if cdn == "fastly":
        await purge_fastly_key(
            os.environ["FASTLY_SERVICE_ID"],
            os.environ["FASTLY_API_KEY"],
            "all",
        )
    elif cdn == "cloudflare":
        await purge_cloudflare_everything(
            os.environ["CLOUDFLARE_ZONE_ID"],
            os.environ["CLOUDFLARE_API_TOKEN"],
        )
    elif cdn == "cloudfront":
        invalidate_cloudfront(
            os.environ["CLOUDFRONT_DISTRIBUTION_ID"],
            ["/*"],
        )
    print("CDN cache invalidated after deploy")


if __name__ == "__main__":
    asyncio.run(invalidate_on_deploy())
