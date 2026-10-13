# per_tenant.py — Isolate resources per tenant.
import threading
from collections import defaultdict
from contextlib import contextmanager

from exceptions import BulkheadFullError


class PerTenantBulkhead:
    """Each tenant gets its own concurrency limit.
    One tenant can't exhaust resources for all others."""

    def __init__(self, max_per_tenant=10):
        self._max_per_tenant = max_per_tenant
        self._semaphores = defaultdict(lambda: threading.Semaphore(max_per_tenant))
        self._active = defaultdict(int)
        self._lock = threading.Lock()

    @contextmanager
    def acquire(self, tenant_id):
        sem = self._semaphores[tenant_id]
        if not sem.acquire(timeout=5):
            raise BulkheadFullError(
                f"Tenant {tenant_id} exceeded {self._max_per_tenant} concurrent requests"
            )
        with self._lock:
            self._active[tenant_id] += 1
        try:
            yield
        finally:
            with self._lock:
                self._active[tenant_id] -= 1
            sem.release()

    def get_stats(self):
        return dict(self._active)


if __name__ == "__main__":
    bulkhead = PerTenantBulkhead(max_per_tenant=2)

    def job():
        import time
        time.sleep(0.1)

    for tenant in ("acme", "globex", "initech"):
        for _ in range(2):
            with bulkhead.acquire(tenant):
                job()

    print(bulkhead.get_stats())
