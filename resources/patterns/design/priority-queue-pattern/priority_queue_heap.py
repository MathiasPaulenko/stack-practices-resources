"""Priority Queue Pattern: heap-based priority queue with worker threads.

Run: python priority_queue_heap.py
Tests: python -m pytest test_priority_queue.py
"""
import heapq
import time
from dataclasses import dataclass, field
from typing import Callable
from enum import Enum
import threading


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


@dataclass(order=True)
class Task:
    priority: int
    timestamp: float = field(compare=True)
    task_id: str = field(compare=False)
    payload: dict = field(compare=False)
    handler: Callable = field(compare=False, default=None)


class PriorityQueueProcessor:
    """Process tasks by priority with fairness within priority levels."""

    def __init__(self, num_workers=4):
        self.heap = []
        self.lock = threading.Lock()
        self.workers = []
        self.running = False
        self.num_workers = num_workers
        self.completed = []
        self.failed = []

    def submit(self, task_id, payload, priority=Priority.NORMAL, handler=None):
        task = Task(
            priority=priority.value,
            timestamp=time.time(),
            task_id=task_id,
            payload=payload,
            handler=handler,
        )
        with self.lock:
            heapq.heappush(self.heap, task)

    def _process_next(self):
        with self.lock:
            if not self.heap:
                return None
            task = heapq.heappop(self.heap)

        try:
            if task.handler:
                task.handler(task.payload)
            else:
                self._default_handler(task)
            self.completed.append(task.task_id)
        except Exception as exc:
            self.failed.append((task.task_id, str(exc)))

    def _default_handler(self, task):
        time.sleep(0.01)

    def _worker_loop(self):
        while self.running:
            self._process_next()
            time.sleep(0.001)

    def start(self):
        self.running = True
        for _ in range(self.num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self.workers.append(t)

    def stop(self):
        self.running = False
        for w in self.workers:
            w.join(timeout=2)

    def size(self):
        with self.lock:
            return len(self.heap)


if __name__ == "__main__":
    processor = PriorityQueueProcessor(num_workers=2)
    processor.start()

    processor.submit("email-batch", {"type": "newsletter"}, Priority.LOW)
    processor.submit("fraud-alert", {"user_id": 12345}, Priority.CRITICAL)
    processor.submit("report-gen", {"format": "pdf"}, Priority.NORMAL)
    processor.submit("vip-onboarding", {"customer_id": "VIP-001"}, Priority.HIGH)

    time.sleep(1)
    processor.stop()
    print(f"Completed: {processor.completed}")
    print(f"Failed: {processor.failed}")
