# failover/cascading.py — Multi-tier failover: primary -> standby -> tertiary
import requests

class CascadingFailover:
    """Tries endpoints in order: primary, then standby, then tertiary.
    Each tier is tried only if the previous one fails."""

    def __init__(self, tiers):
        """tiers: [{"name": "primary", "url": "...", "timeout": 5}, ...]"""
        self.tiers = tiers
        self._active_tier = 0

    @property
    def active_url(self):
        return self.tiers[self._active_tier]["url"]

    def request(self, method, path, **kwargs):
        for i, tier in enumerate(self.tiers):
            try:
                url = f"{tier['url']}{path}"
                resp = requests.request(method, url, timeout=tier["timeout"], **kwargs)
                if resp.status_code < 500:
                    if i != self._active_tier:
                        print(f"Failover: tier {self._active_tier} -> {i} ({tier['name']})")
                        self._active_tier = i
                    return resp
            except Exception:
                continue

        raise Exception("All tiers exhausted")


if __name__ == "__main__":
    fo = CascadingFailover([
        {"name": "primary", "url": "https://api-primary.example.com", "timeout": 5},
        {"name": "standby", "url": "https://api-standby.example.com", "timeout": 5},
        {"name": "tertiary", "url": "https://api-tertiary.example.com", "timeout": 10},
    ])
    resp = fo.request("GET", "/api/products")
    print(resp.status_code)
