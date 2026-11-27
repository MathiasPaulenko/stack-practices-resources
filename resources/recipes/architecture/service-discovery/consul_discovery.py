"""Client-side service discovery against Consul with a local cache.

Queries the catalog once per `cache_ttl` seconds instead of on every
request — the registry stays quiet and per-request latency drops by a
millisecond or two. If the registry is unreachable, the last known
instance list keeps working (stale-but-working beats fresh-and-dead).

Requires: pip install python-consul requests
"""
import random
import time
from typing import List, Optional

import consul
import requests


class ConsulServiceDiscovery:
    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500,
                 cache_ttl: float = 30.0):
        self.client = consul.Consul(host=consul_host, port=consul_port)
        self.cache_ttl = cache_ttl
        self._cache: dict = {}          # service_name -> (timestamp, instances)
        self._last_good: dict = {}      # service_name -> instances (no expiry)

    def get_instances(self, service_name: str) -> List[dict]:
        now = time.monotonic()
        cached = self._cache.get(service_name)
        if cached and now - cached[0] < self.cache_ttl:
            return cached[1]

        try:
            _, services = self.client.catalog.service(service_name)
            healthy = []
            for service in services:
                _, checks = self.client.health.checks(service_name)
                passing = [c for c in checks if c["Status"] == "passing"]
                if passing:
                    healthy.append({
                        "id": service["ServiceID"],
                        "address": service["ServiceAddress"] or service["Address"],
                        "port": service["ServicePort"],
                    })
            self._cache[service_name] = (now, healthy)
            self._last_good[service_name] = healthy
            return healthy
        except Exception:
            # Registry unreachable — keep serving the last known list.
            return self._last_good.get(service_name, [])

    def get_instance(self, service_name: str) -> dict:
        instances = self.get_instances(service_name)
        if not instances:
            raise RuntimeError(f"No healthy instances for {service_name}")
        return random.choice(instances)

    def call_service(self, service_name: str, path: str, method: str = "GET") -> dict:
        instance = self.get_instance(service_name)
        url = f'http://{instance["address"]}:{instance["port"]}{path}'
        response = requests.request(method, url, timeout=5)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    discovery = ConsulServiceDiscovery(consul_host="consul-server")
    result = discovery.call_service("payment-service", "/payments/123")
    print(result)
