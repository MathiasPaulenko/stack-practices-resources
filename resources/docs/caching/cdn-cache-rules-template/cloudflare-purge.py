"""Cloudflare purge helpers: by URL, by tag, and full purge after deploy."""
import os

import requests

API = "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache"


def _post(zone_id: str, api_token: str, payload: dict) -> dict:
    return requests.post(
        API.format(zone_id=zone_id),
        headers={"Authorization": f"Bearer {api_token}",
                 "Content-Type": "application/json"},
        json=payload,
    ).json()


def purge_urls(zone_id: str, api_token: str, urls: list) -> dict:
    """Purge specific URLs (up to 30 per call)."""
    return _post(zone_id, api_token, {"files": urls})


def purge_by_tag(zone_id: str, api_token: str, tags: list) -> dict:
    """Purge by cache tag (Cloudflare Enterprise)."""
    return _post(zone_id, api_token, {"tags": tags})


def purge_after_deploy() -> None:
    """Purge everything — meant to run as a CI/CD post-deploy step."""
    resp = _post(os.environ["CLOUDFLARE_ZONE_ID"],
                 os.environ["CLOUDFLARE_API_TOKEN"],
                 {"purge_everything": True})
    if resp["success"]:
        print("CDN purged successfully after deployment")
    else:
        print(f"Purge failed: {resp['errors']}")


if __name__ == "__main__":
    print(purge_by_tag("zone123", "token456", ["products", "catalog"]))
