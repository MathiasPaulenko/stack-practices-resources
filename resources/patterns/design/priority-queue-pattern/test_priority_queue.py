import heapq
import time
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from priority_queue_heap import PriorityQueueProcessor, Priority


def test_submit_and_size():
    proc = PriorityQueueProcessor(num_workers=1)
    proc.submit("t1", {"x": 1}, Priority.LOW)
    proc.submit("t2", {"x": 2}, Priority.CRITICAL)
    assert proc.size() == 2


def test_priority_order():
    proc = PriorityQueueProcessor(num_workers=1)
    proc.submit("low", {}, Priority.LOW)
    proc.submit("critical", {}, Priority.CRITICAL)
    proc.submit("normal", {}, Priority.NORMAL)
    # Pop manually to verify order
    order = []
    while proc.heap:
        order.append(heapq.heappop(proc.heap).task_id)
    assert order == ["critical", "normal", "low"]


def test_processing_completes():
    proc = PriorityQueueProcessor(num_workers=2)
    proc.start()
    proc.submit("a", {}, Priority.NORMAL)
    proc.submit("b", {}, Priority.HIGH)
    time.sleep(0.5)
    proc.stop()
    assert "a" in proc.completed
    assert "b" in proc.completed


def test_failed_handler_records_error():
    proc = PriorityQueueProcessor(num_workers=1)
    proc.start()

    def bad_handler(payload):
        raise ValueError("boom")

    proc.submit("bad", {}, Priority.NORMAL, handler=bad_handler)
    time.sleep(0.3)
    proc.stop()
    assert len(proc.failed) == 1
    assert proc.failed[0][0] == "bad"


def test_empty_queue_safe():
    proc = PriorityQueueProcessor(num_workers=1)
    proc.start()
    time.sleep(0.1)
    proc.stop()
    assert proc.completed == []
    assert proc.failed == []


def test_priority_enum_values():
    assert Priority.CRITICAL.value < Priority.HIGH.value
    assert Priority.HIGH.value < Priority.NORMAL.value
    assert Priority.NORMAL.value < Priority.LOW.value
    assert Priority.LOW.value < Priority.BACKGROUND.value
