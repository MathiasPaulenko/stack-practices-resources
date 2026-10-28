"""CDN health report: hit ratio, bandwidth and origin offload via Cloudflare analytics."""
import requests


def check_cdn_health(zone_id: str, api_token: str):
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/analytics/dashboard",
        headers={"Authorization": f"Bearer {api_token}"},
        params={"since": "-1440", "until": "now"},
    )
    data = response.json()["result"]["totals"]
    total = data["requests"]["all"]
    cached = data["requests"]["cached"]
    hit_ratio = (cached / total * 100) if total else 0
    print("CDN Health Report:")
    print(f"  Total requests: {total:,}")
    print(f"  Cached requests: {cached:,}")
    print(f"  Hit ratio: {hit_ratio:.1f}%")
    print(f"  Bandwidth: {data['bandwidth']['all'] / 1e9:.1f} GB")
    if hit_ratio < 90:
        print("ALERT: CDN hit ratio below 90%")
    return hit_ratio


if __name__ == "__main__":
    import os
    check_cdn_health(os.environ["CLOUDFLARE_ZONE_ID"], os.environ["CLOUDFLARE_API_TOKEN"])
