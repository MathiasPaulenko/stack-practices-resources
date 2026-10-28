"""Tests for BatchProcessor: idempotency, retries and checkpoint resume.

Run: pytest test_batch_processor.py
"""

import os

from batch_processor import BatchProcessor


def _items(n=250):
    return iter({"id": i} for i in range(n))


def test_processes_all_items(tmp_path):
    processor = BatchProcessor(batch_size=100)
    result = processor.process(_items(250), lambda batch: None)
    assert result == {"processed": 250, "failed": 0}
    assert processor.processed == 250


def test_retries_then_succeeds():
    attempts = {"count": 0}

    def flaky(batch):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ConnectionError("transient")

    processor = BatchProcessor(batch_size=50, max_retries=3)
    result = processor.process(_items(50), flaky)
    assert result["failed"] == 0
    assert attempts["count"] == 3


def test_dead_letters_after_exhausted_retries():
    def always_fails(batch):
        raise ValueError("permanent")

    processor = BatchProcessor(batch_size=50, max_retries=2)
    result = processor.process(_items(100), always_fails)
    assert result == {"processed": 0, "failed": 100}
    assert len(processor.failed) == 100


def test_checkpoint_resume(tmp_path):
    checkpoint = str(tmp_path / "checkpoint.json")

    p1 = BatchProcessor(batch_size=100, checkpoint_path=checkpoint)
    p1.process(_items(200), lambda batch: None)
    assert os.path.exists(checkpoint)

    p2 = BatchProcessor(batch_size=100, checkpoint_path=checkpoint)
    assert p2._batch_number == 2  # resumed from batch 2
