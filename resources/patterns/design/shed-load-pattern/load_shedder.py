# pip install psutil
from dataclasses import dataclass
from typing import Callable
from enum import Enum
import threading
import time
import concurrent.futures

import psutil

class LoadStatus(Enum):
    ACCEPTED = "accepted"
    SHED = "shed"

@dataclass
class LoadMetrics:
    active_requests: int = 0
    queue_depth: int = 0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0

class LoadShedder:
    def __init__(self, max_concurrent: int = 100,
                 cpu_threshold: float = 0.85,
                 memory_threshold: float = 0.90,
                 queue_threshold: int = 500):
        self.max_concurrent = max_concurrent
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.queue_threshold = queue_threshold
        self._active = 0
        self._lock = threading.Lock()
        self._shed_count = 0
        self._accept_count = 0

    def _get_metrics(self) -> LoadMetrics:
        cpu = psutil.cpu_percent(interval=0.05) / 100.0
        mem = psutil.virtual_memory().percent / 100.0
        return LoadMetrics(
            active_requests=self._active,
            queue_depth=self._active * 10,
            cpu_usage=cpu,
            memory_usage=mem,
        )

    def should_shed(self) -> bool:
        metrics = self._get_metrics()
        if self._active >= self.max_concurrent:
            return True
        if metrics.cpu_usage >= self.cpu_threshold:
            return True
        if metrics.memory_usage >= self.memory_threshold:
            return True
        return metrics.queue_depth >= self.queue_threshold

    def execute(self, request_id: str, handler: Callable) -> dict:
        with self._lock:
            if self.should_shed():
                self._shed_count += 1
                return {
                    "request_id": request_id,
                    "status": LoadStatus.SHED.value,
                    "message": "Service overloaded, retry later",
                    "http_status": 503,
                }
            self._active += 1
            self._accept_count += 1

        try:
            result = handler(request_id)
            return {
                "request_id": request_id,
                "status": LoadStatus.ACCEPTED.value,
                "result": result,
                "http_status": 200,
            }
        finally:
            with self._lock:
                self._active -= 1

    def stats(self) -> dict:
        total = self._accept_count + self._shed_count
        return {
            "accepted": self._accept_count,
            "shed": self._shed_count,
            "active": self._active,
            "shed_rate": self._shed_count / max(total, 1),
        }

# Usage
shedder = LoadShedder(
    max_concurrent=3, cpu_threshold=0.95,
    memory_threshold=0.95, queue_threshold=10000,
)

def mock_handler(req_id: str) -> str:
    time.sleep(0.1)
    return f"processed-{req_id}"

def send_request(i: int) -> dict:
    return shedder.execute(f"req-{i}", mock_handler)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(send_request, range(10)))

for r in results:
    print(f"  {r['request_id']}: {r['status']} (HTTP {r['http_status']})")

print(f"\nStats: {shedder.stats()}")
