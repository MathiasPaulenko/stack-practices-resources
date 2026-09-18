# failover/active_active.py — Both nodes serve traffic simultaneously
import random
import requests

class ActiveActiveManager:
    """Both primary and standby serve traffic.
    If one fails, the other absorbs all traffic."""

    def __init__(self, endpoints, health_path="/health"):
        self.endpoints = {url: {"healthy": True, "failures": 0}
                          for url in endpoints}
        self.health_path = health_path

    def get_healthy_endpoints(self):
        return [url for url, info in self.endpoints.items()
                if info["healthy"]]

    def request(self, method, path, **kwargs):
        healthy = self.get_healthy_endpoints()
        if not healthy:
            raise Exception("All endpoints are unhealthy")

        # Random load balancing among healthy endpoints
        url = random.choice(healthy)
        try:
            resp = requests.request(method, f"{url}{path}", timeout=10, **kwargs)
            return resp
        except Exception:
            self.endpoints[url]["failures"] += 1
            if self.endpoints[url]["failures"] >= 3:
                self.endpoints[url]["healthy"] = False
                print(f"Marked {url} as unhealthy")
            # Retry on another healthy endpoint
            return self.request(method, path, **kwargs)


if __name__ == "__main__":
    manager = ActiveActiveManager([
        "https://api-1.example.com",
        "https://api-2.example.com",
    ])
    resp = manager.request("GET", "/api/products")
    print(resp.status_code)
