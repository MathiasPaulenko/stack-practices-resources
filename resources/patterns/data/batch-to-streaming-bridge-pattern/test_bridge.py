"""Tests for bridge.py — batch-to-streaming bridge companion."""

import pytest
from datetime import datetime, timezone

from bridge import (
    CustomerRecord,
    BatchProducer,
    StreamingProducer,
    PartitionedLake,
    SpeedLayer,
    ServingLayer,
    UnifiedConsumer,
)

WHEN = datetime(2026, 8, 19, 14, tzinfo=timezone.utc)


def _row(**over):
    row = {"id": 1, "email": "  ANA@Shop.com ", "status": "active", "created_at": WHEN}
    row.update(over)
    return row


def _event(**over):
    after = {"id": 1, "email": "ana@shop.com", "status": "banned", "created_at": WHEN}
    after.update(over)
    return {"after": after}


def test_shared_schema_normalizes_both_paths():
    b = BatchProducer().produce(_row())
    s = StreamingProducer().produce(_event())
    assert b.email == s.email == "ana@shop.com"  # lowercase + strip on both
    assert b.source == "batch" and s.source == "streaming"
    assert s.is_active is False  # derived from status


def test_schema_rejects_invalid_status():
    with pytest.raises(ValueError):
        BatchProducer().produce(_row(status="ghost"))


def test_partition_path_includes_hour():
    lake = PartitionedLake()
    key = lake.write(BatchProducer().produce(_row()), WHEN)
    assert key == "customers/year=2026/month=08/day=19/hour=14"


def test_serving_layer_prefers_streaming_over_batch():
    lake = PartitionedLake()
    lake.write(BatchProducer().produce(_row()), WHEN)
    lake.write(StreamingProducer().produce(_event()), WHEN)
    winners = ServingLayer.latest(lake.read_all())
    assert len(winners) == 1
    assert winners[0].source == "streaming"


def test_serving_layer_keeps_batch_when_no_streaming():
    lake = PartitionedLake()
    lake.write(BatchProducer().produce(_row(id=2, email="bob@shop.com")), WHEN)
    winners = ServingLayer.latest(lake.read_all())
    assert [r.id for r in winners] == [2]


def test_unified_view_merges_streaming_over_batch_selectively():
    lake, speed = PartitionedLake(), SpeedLayer()
    lake.write(BatchProducer().produce(_row(email="old@shop.com")), WHEN)
    rec = StreamingProducer().produce(_event(email="new@shop.com"))
    speed.put(rec)

    view = UnifiedConsumer(lake, speed).get_unified_view(1)
    assert view["email"] == "new@shop.com"
    assert view["status"] == "banned"
    assert view["source"] == "merged"


def test_unified_view_returns_none_for_unknown_customer():
    consumer = UnifiedConsumer(PartitionedLake(), SpeedLayer())
    assert consumer.get_unified_view(999) is None
