"""Queue-Based Load Leveling Pattern - Producer implementation.

Simple in-memory queue with depth limits, dead-letter queue, and rate limiting.
This is a teaching implementation, not production-ready.
"""

import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class Task:
    id: str
    type: str
    payload: Any
    attempts: int = 0
    max_retries: int = 3
    created_at: float = field(default_factory=time.time)


class DeadLetterQueue:
    """Holds messages that failed processing after max retries."""

    def __init__(self):
        self._messages = deque()

    def push(self, task: Task, error: str):
        self._messages.append({"task": task, "error": error, "failed_at": time.time()})

    def drain(self):
        items = list(self._messages)
        self._messages.clear()
        return items

    def __len__(self):
        return len(self._messages)


class LoadLevelingQueue:
    """Bounded queue with depth limit, TTL, and dead-letter overflow."""

    def __init__(self, max_length=1000, message_ttl=3600, rate_limit_per_min=100):
        self._queue = deque()
        self._max_length = max_length
        self._message_ttl = message_ttl
        self._rate_limit = rate_limit_per_min
        self._processed_count = 0
        self._rejected_count = 0
        self._dlq = DeadLetterQueue()
        self._lock = threading.Lock()
        self._last_process_time = 0.0

    def enqueue(self, task: Task) -> bool:
        with self._lock:
            if len(self._queue) >= self._max_length:
                self._rejected_count += 1
                return False
            self._queue.append(task)
            return True

    def dequeue(self) -> Optional[Task]:
        with self._lock:
            if not self._queue:
                return None
            task = self._queue.popleft()
            if time.time() - task.created_at > self._message_ttl:
                self._dlq.push(task, "TTL expired")
                return None
            return task

    def fail(self, task: Task, error: str):
        task.attempts += 1
        if task.attempts >= task.max_retries:
            self._dlq.push(task, error)
        else:
            with self._lock:
                self._queue.append(task)

    def depth(self) -> int:
        return len(self._queue)

    def rejected(self) -> int:
        return self._rejected_count

    def dlq_depth(self) -> int:
        return len(self._dlq)

    def drain_dlq(self):
        return self._dlq.drain()


class TaskProducer:
    """Enqueues tasks into the load-leveling queue."""

    def __init__(self, queue: LoadLevelingQueue):
        self._queue = queue

    def send(self, task: Task) -> bool:
        return self._queue.enqueue(task)

    def send_batch(self, tasks):
        results = []
        for task in tasks:
            results.append(self._queue.enqueue(task))
        return results


class TaskConsumer:
    """Pulls tasks from the queue and processes them at a steady rate."""

    def __init__(self, queue: LoadLevelingQueue, handler: Callable[[Task], Any], interval=0.1):
        self._queue = queue
        self._handler = handler
        self._interval = interval
        self._running = False
        self._thread = None
        self._processed = 0

    def _loop(self):
        while self._running:
            task = self._queue.dequeue()
            if task is None:
                time.sleep(self._interval)
                continue
            try:
                self._handler(task)
                self._processed += 1
            except Exception as exc:
                self._queue.fail(task, str(exc))
            time.sleep(self._interval)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def processed_count(self) -> int:
        return self._processed
