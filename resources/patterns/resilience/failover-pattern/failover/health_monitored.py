# failover/health_monitored.py — Active-passive failover with health checks
import time
import threading
import requests
from enum import Enum

class NodeStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class FailoverManager:
    """Monitors primary and standby nodes.
    Automatically fails over when primary becomes unhealthy."""

    def __init__(self, primary_url, standby_url, health_path="/health",
                 check_interval=5, failure_threshold=3, recovery_threshold=3):
        self.primary_url = primary_url
        self.standby_url = standby_url
        self.health_path = health_path
        self.check_interval = check_interval
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold

        self._active_url = primary_url
        self._primary_failures = 0
        self._primary_successes = 0
        self._standby_failures = 0
        self._is_failover = False
        self._lock = threading.Lock()
        self._running = True

    @property
    def active_url(self):
        with self._lock:
            return self._active_url

    @property
    def is_failover(self):
        with self._lock:
            return self._is_failover

    def _check_health(self, url):
        """Check if a node is healthy."""
        try:
            resp = requests.get(f"{url}{self.health_path}", timeout=3)
            if resp.status_code == 200:
                return NodeStatus.HEALTHY
            return NodeStatus.UNHEALTHY
        except Exception:
            return NodeStatus.UNHEALTHY

    def _monitor_loop(self):
        """Continuously monitor the primary and fail over if needed."""
        while self._running:
            primary_status = self._check_health(self.primary_url)

            with self._lock:
                if not self._is_failover:
                    # Monitoring primary
                    if primary_status == NodeStatus.HEALTHY:
                        self._primary_failures = 0
                    else:
                        self._primary_failures += 1
                        if self._primary_failures >= self.failure_threshold:
                            print(f"Primary failed {self._primary_failures} times, "
                                  f"failing over to standby")
                            self._initiate_failover()
                else:
                    # In failover mode — check if primary recovered
                    if primary_status == NodeStatus.HEALTHY:
                        self._primary_successes += 1
                        if self._primary_successes >= self.recovery_threshold:
                            print(f"Primary recovered {self._primary_successes} times, "
                                  f"failing back")
                            self._initiate_failback()
                    else:
                        self._primary_successes = 0

            time.sleep(self.check_interval)

    def _initiate_failover(self):
        """Switch traffic from primary to standby."""
        standby_status = self._check_health(self.standby_url)
        if standby_status == NodeStatus.HEALTHY:
            self._active_url = self.standby_url
            self._is_failover = True
            self._primary_successes = 0
            print(f"Failover complete: now serving from {self.standby_url}")
        else:
            print(f"CRITICAL: Standby is also unhealthy! Cannot fail over.")

    def _initiate_failback(self):
        """Switch traffic back to primary."""
        self._active_url = self.primary_url
        self._is_failover = False
        self._primary_failures = 0
        print(f"Failback complete: now serving from {self.primary_url}")

    def start(self):
        """Start the monitoring thread."""
        t = threading.Thread(target=self._monitor_loop, daemon=True)
        t.start()

    def stop(self):
        self._running = False

    def request(self, method, path, **kwargs):
        """Make a request to the currently active node."""
        url = f"{self.active_url}{path}"
        return requests.request(method, url, **kwargs)

    def get_status(self):
        with self._lock:
            return {
                "active_url": self._active_url,
                "is_failover": self._is_failover,
                "primary_failures": self._primary_failures,
                "primary_successes": self._primary_successes,
            }


if __name__ == "__main__":
    failover = FailoverManager(
        primary_url="https://api-primary.example.com",
        standby_url="https://api-standby.example.com",
        health_path="/health",
        check_interval=5,
        failure_threshold=3,
        recovery_threshold=3
    )
    failover.start()

    # All requests go to the active node (primary or standby)
    response = failover.request("GET", "/api/products")
    print(response.status_code)
