# metrics_sidecar.py — scrape app metrics and push to Prometheus
import os
import time

import requests
from prometheus_client import (
    CollectorRegistry, Gauge, push_to_gateway,
)

PUSHGATEWAY = os.environ.get(
    "PROMETHEUS_PUSHGATEWAY", "http://prometheus:9091")
APP_URL = os.environ.get("APP_URL", "http://localhost:8080")
SCRAPE_INTERVAL = int(os.environ.get("SCRAPE_INTERVAL", "15"))

class MetricsSidecar:
    """Sidecar that scrapes app metrics and pushes them."""

    def __init__(self, app_url, pushgateway_url):
        self.app_url = app_url
        self.pushgateway_url = pushgateway_url
        self.registry = CollectorRegistry()
        self.request_count = Gauge(
            "app_request_count", "Total requests",
            ["method", "endpoint"], registry=self.registry)
        self.response_time = Gauge(
            "app_response_time_ms", "Response time in ms",
            ["endpoint"], registry=self.registry)

    def scrape(self):
        """Pull metrics from the main app's /metrics endpoint."""
        try:
            resp = requests.get(f"{self.app_url}/metrics", timeout=5)
            if resp.status_code != 200:
                return
            data = resp.json()
            for m in data.get("counters", []):
                self.request_count.labels(
                    method=m["method"],
                    endpoint=m["endpoint"],
                ).set(m["value"])
            for m in data.get("timers", []):
                self.response_time.labels(
                    endpoint=m["endpoint"],
                ).set(m["p99"])
            self.push()
        except Exception as e:
            print(f"Scrape failed: {e}")

    def push(self):
        """Push the registry to Prometheus pushgateway."""
        try:
            push_to_gateway(
                self.pushgateway_url,
                job="api-server",
                registry=self.registry,
            )
        except Exception as e:
            print(f"Push failed: {e}")

    def run(self):
        """Run the scrape-push loop forever."""
        print(f"Metrics sidecar for {self.app_url}")
        while True:
            self.scrape()
            time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    MetricsSidecar(APP_URL, PUSHGATEWAY).run()
