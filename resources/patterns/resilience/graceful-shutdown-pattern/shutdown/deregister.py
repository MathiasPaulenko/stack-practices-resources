# shutdown/deregister.py — Deregister from load balancer before draining
import requests
import time
import signal
import sys

class GracefulService:
    """Deregisters from load balancer, then drains requests."""

    def __init__(self, lb_registry_url, health_port=8080):
        self.lb_url = lb_registry_url
        self.health_port = health_port
        self._healthy = True
        self._active_requests = 0

    def deregister(self):
        """Tell the load balancer to stop sending traffic."""
        try:
            resp = requests.post(
                f"{self.lb_url}/deregister",
                json={"port": self.health_port},
                timeout=5
            )
            print(f"Deregistered from load balancer: {resp.status_code}")
        except Exception as e:
            print(f"Deregistration failed: {e}")

        # Wait for LB to propagate
        time.sleep(5)

    def health_check(self):
        """Return 200 if healthy, 503 if shutting down."""
        if not self._healthy:
            return 503
        return 200

    def shutdown(self, timeout=30):
        # Step 1: Mark as unhealthy (LB stops sending new traffic)
        self._healthy = False
        print("Marked as unhealthy")

        # Step 2: Deregister from load balancer
        self.deregister()

        # Step 3: Wait for active requests
        start = time.time()
        while self._active_requests > 0:
            if time.time() - start > timeout:
                print(f"Timeout with {self._active_requests} requests active")
                break
            time.sleep(0.5)

        # Step 4: Cleanup and exit
        print("Shutting down")
        sys.exit(0)
