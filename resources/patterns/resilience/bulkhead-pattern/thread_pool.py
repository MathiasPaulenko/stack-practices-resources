# thread_pool.py — Thread pool isolation per service.
import concurrent.futures
from collections import defaultdict
import time
import logging

from exceptions import BulkheadFullError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BulkheadManager:
    """Manages separate thread pools for different services.
    Each service gets its own pool — one service can't exhaust another's threads."""

    def __init__(self):
        self._pools = {}
        self._configs = {}
        self._active = defaultdict(int)

    def configure(self, service_name, max_workers, queue_capacity=100):
        """Configure a bulkhead for a specific service."""
        self._pools[service_name] = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=f"bulkhead-{service_name}"
        )
        self._configs[service_name] = {
            "max_workers": max_workers,
            "queue_capacity": queue_capacity
        }
        logger.info(f"Bulkhead configured for {service_name}: "
                    f"max_workers={max_workers}, queue={queue_capacity}")

    def submit(self, service_name, fn, *args, **kwargs):
        """Submit a task to a service's bulkhead.
        Raises BulkheadFullError if the pool and queue are exhausted."""
        if service_name not in self._pools:
            raise ValueError(f"No bulkhead configured for {service_name}")

        config = self._configs[service_name]
        if self._active[service_name] >= config["max_workers"] + config["queue_capacity"]:
            raise BulkheadFullError(
                f"Bulkhead '{service_name}' is full: "
                f"{self._active[service_name]} active tasks"
            )

        self._active[service_name] += 1

        def wrapped_fn(*a, **kw):
            try:
                return fn(*a, **kw)
            finally:
                self._active[service_name] -= 1

        return self._pools[service_name].submit(wrapped_fn, *args, **kwargs)

    def get_stats(self):
        return {
            service: {
                "active": self._active[service],
                "max_workers": self._configs[service]["max_workers"],
                "queue_capacity": self._configs[service]["queue_capacity"],
                "utilization": self._active[service] / self._configs[service]["max_workers"]
            }
            for service in self._pools
        }

    def shutdown(self):
        for pool in self._pools.values():
            pool.shutdown(wait=True)


if __name__ == "__main__":
    bulkhead = BulkheadManager()
    bulkhead.configure("payment", max_workers=10, queue_capacity=20)
    bulkhead.configure("inventory", max_workers=5, queue_capacity=10)
    bulkhead.configure("notifications", max_workers=3, queue_capacity=5)

    def call_payment_api(amount):
        time.sleep(0.5)
        return {"status": "charged", "amount": amount}

    future = bulkhead.submit("payment", call_payment_api, 99.99)
    print(future.result(timeout=5))
    print(bulkhead.get_stats())
    bulkhead.shutdown()
