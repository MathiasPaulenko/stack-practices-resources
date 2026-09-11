"""Tests for the Queue-Based Load Leveling Pattern."""

import time
import threading
from queue_producer import LoadLevelingQueue, Task, TaskProducer, TaskConsumer
from queue_consumer import route_task


def make_task(tid="t1", ttype="send-email", payload=None):
    return Task(id=tid, type=ttype, payload=payload or {"to": "a@b.com", "body": "hello world this is a test email"})


def test_enqueue_and_dequeue():
    q = LoadLevelingQueue(max_length=10)
    t = make_task()
    assert q.enqueue(t) is True
    got = q.dequeue()
    assert got is not None
    assert got.id == "t1"


def test_depth_limit_rejects():
    q = LoadLevelingQueue(max_length=3)
    for i in range(3):
        assert q.enqueue(make_task(f"t{i}")) is True
    assert q.enqueue(make_task("overflow")) is False
    assert q.rejected() == 1
    assert q.depth() == 3


def test_ttl_expires_to_dlq():
    q = LoadLevelingQueue(max_length=10, message_ttl=0.05)
    q.enqueue(make_task())
    time.sleep(0.1)
    result = q.dequeue()
    assert result is None
    assert q.dlq_depth() == 1


def test_fail_moves_to_dlq_after_max_retries():
    q = LoadLevelingQueue(max_length=10)
    t = make_task()
    t.max_retries = 2
    q.enqueue(t)
    got = q.dequeue()
    q.fail(got, "error 1")
    got2 = q.dequeue()
    q.fail(got2, "error 2")
    assert q.dlq_depth() == 1


def test_fail_requeues_before_max_retries():
    q = LoadLevelingQueue(max_length=10)
    t = make_task()
    t.max_retries = 3
    q.enqueue(t)
    got = q.dequeue()
    q.fail(got, "error 1")
    assert q.depth() == 1


def test_producer_batch():
    q = LoadLevelingQueue(max_length=100)
    p = TaskProducer(q)
    tasks = [make_task(f"batch-{i}") for i in range(10)]
    results = p.send_batch(tasks)
    assert all(results)
    assert q.depth() == 10


def test_consumer_processes_tasks():
    q = LoadLevelingQueue(max_length=100)
    processed = []

    def handler(task):
        processed.append(task.id)

    c = TaskConsumer(q, handler, interval=0.01)
    for i in range(5):
        q.enqueue(make_task(f"c-{i}"))
    c.start()
    time.sleep(0.5)
    c.stop()
    assert len(processed) == 5
    assert c.processed_count() == 5


def test_consumer_handles_failures():
    q = LoadLevelingQueue(max_length=100)

    def handler(task):
        if task.id == "fail-me":
            raise RuntimeError("boom")

    c = TaskConsumer(q, handler, interval=0.01)
    t = make_task("fail-me")
    t.max_retries = 1
    q.enqueue(t)
    c.start()
    time.sleep(0.5)
    c.stop()
    assert q.dlq_depth() == 1


def test_route_task_email():
    t = make_task("e1", "send-email", {"to": "a@b.com", "body": "hello"})
    result = route_task(t)
    assert result["status"] == "sent"


def test_route_task_report():
    t = make_task("r1", "generate-report", {"type": "monthly"})
    result = route_task(t)
    assert result["status"] == "completed"


def test_route_task_unknown_type():
    t = make_task("x1", "unknown-type")
    try:
        route_task(t)
        assert False, "Should have raised"
    except ValueError as e:
        assert "Unknown task type" in str(e)


def test_dlq_drain():
    q = LoadLevelingQueue(max_length=10, message_ttl=0.05)
    q.enqueue(make_task())
    q.enqueue(make_task("t2"))
    time.sleep(0.1)
    q.dequeue()
    q.dequeue()
    assert q.dlq_depth() == 2
    drained = q.drain_dlq()
    assert len(drained) == 2
    assert q.dlq_depth() == 0


def test_queue_depth_after_partial_consume():
    q = LoadLevelingQueue(max_length=100)
    for i in range(10):
        q.enqueue(make_task(f"d-{i}"))
    for _ in range(3):
        q.dequeue()
    assert q.depth() == 7


def test_rejected_count_tracks_overflows():
    q = LoadLevelingQueue(max_length=2)
    q.enqueue(make_task("a"))
    q.enqueue(make_task("b"))
    q.enqueue(make_task("c"))
    q.enqueue(make_task("d"))
    assert q.rejected() == 2


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f"PASS: {test.__name__}")
        except Exception as exc:
            failed += 1
            print(f"FAIL: {test.__name__} — {exc}")
    print()
    if failed == 0:
        print(f"=== All {passed} tests passed ===")
    else:
        print(f"=== {passed} passed, {failed} failed ===")
