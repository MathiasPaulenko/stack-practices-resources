"""Surrogate-key purge clients for Fastly and Cloudflare.

Source: https://stackpractices.com/guides/complete-guide-cdn-caching-strategy/
"""
import os
import requests

FASTLY_KEY = os.environ.get("FASTLY_API_KEY", "")
CF_TOKEN = os.environ.get("CF_API_TOKEN", "")


def fastly_purge_surrogate(service_id: str, key: str):
    """Purge every response tagged `key` in one call."""
    return requests.post(
        f"https://api.fastly.com/purge/{service_id}",
        headers={"Fastly-Key": FASTLY_KEY, "Surrogate-Key": key},
        timeout=5,
    )


def cloudflare_purge_urls(zone_id: str, urls: list[str]):
    """Cloudflare doesn't do surrogate keys — purge explicit URLs."""
    return requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
        headers={"Authorization": f"Bearer {CF_TOKEN}",
                 "Content-Type": "application/json"},
        json={"files": urls},
        timeout=5,
    )
