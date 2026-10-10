"""Ambassador proxy for outbound API calls.

Adds retry with exponential backoff, circuit breaking, and per-endpoint
metrics without modifying the client. Run `client_example.py` for a demo
against a local stub or any HTTP endpoint.
"""

import logging
import time
from collections import defaultdict

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AmbassadorProxy:
    """Proxy that adds retry, circuit breaking, and monitoring
    to outbound calls without modifying the client."""

    def __init__(self, target_url):
        self.target_url = target_url
        self.failure_count = 0
        self.failure_threshold = 5
        self.recovery_timeout = 30
        self.last_failure_time = None
        self.circuit_open = False
        self.request_stats = defaultdict(
            lambda: {"count": 0, "errors": 0, "latency_ms": []}
        )

    def _check_circuit(self):
        if self.circuit_open:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                logger.info("Circuit breaker recovery attempt")
                self.circuit_open = False
                self.failure_count = 0
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")

    def _record_success(self, endpoint, latency_ms):
        self.failure_count = 0
        self.circuit_open = False
        stats = self.request_stats[endpoint]
        stats["count"] += 1
        stats["latency_ms"].append(latency_ms)

    def _record_failure(self, endpoint, latency_ms):
        self.failure_count += 1
        self.last_failure_time = time.time()
        stats = self.request_stats[endpoint]
        stats["count"] += 1
        stats["errors"] += 1
        stats["latency_ms"].append(latency_ms)

        if self.failure_count >= self.failure_threshold:
            self.circuit_open = True
            logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures"
            )

    def request(self, method, path, max_retries=3, **kwargs):
        endpoint = f"{method} {path}"
        self._check_circuit()

        last_error = None
        for attempt in range(max_retries):
            start = time.time()
            try:
                url = f"{self.target_url}{path}"
                resp = requests.request(method, url, timeout=10, **kwargs)
                latency_ms = (time.time() - start) * 1000

                if resp.status_code < 500:
                    self._record_success(endpoint, latency_ms)
                    return resp

                last_error = f"HTTP {resp.status_code}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
            except requests.RequestException as e:
                latency_ms = (time.time() - start) * 1000
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

        self._record_failure(endpoint, 0)
        raise AmbassadorError(f"All retries exhausted: {last_error}")

    def get_stats(self):
        return {
            endpoint: {
                "count": s["count"],
                "errors": s["errors"],
                "avg_latency_ms": (
                    sum(s["latency_ms"]) / len(s["latency_ms"])
                    if s["latency_ms"]
                    else 0
                ),
                "circuit_open": self.circuit_open,
            }
            for endpoint, s in self.request_stats.items()
        }


class CircuitBreakerOpenError(Exception):
    pass


class AmbassadorError(Exception):
    pass
