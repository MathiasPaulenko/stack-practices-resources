"""Batch-to-Streaming Bridge — companion example.

Simulates the Lambda-architecture bridge without infrastructure:
two producers (batch + streaming) write records into a partitioned
"lake", a speed layer holds the freshest state per key, and a serving
layer deduplicates by id preferring streaming over batch.

Run: python bridge.py
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

VALID_STATUSES = {"active", "inactive", "banned", "suspended"}


@dataclass
class CustomerRecord:
    """Shared schema both paths must produce (schema alignment)."""

    id: int
    email: str
    status: str
    is_active: bool
    created_at: datetime
    source: Literal["batch", "streaming"]
    ingested_at: datetime

    def __post_init__(self):
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if self.source not in ("batch", "streaming"):
            raise ValueError(f"invalid source: {self.source}")


def _now() -> datetime:
    return datetime.now(timezone.utc)


class BatchProducer:
    """Normalizes a raw DB row into the shared record."""

    def produce(self, row: dict) -> CustomerRecord:
        return CustomerRecord(
            id=row["id"],
            email=row["email"].lower().strip(),
            status=row["status"],
            is_active=row["status"] == "active",
            created_at=row["created_at"],
            source="batch",
            ingested_at=_now(),
        )


class StreamingProducer:
    """Normalizes a CDC envelope ('after' payload) into the shared record."""

    def produce(self, event: dict) -> CustomerRecord:
        after = event["after"]
        return CustomerRecord(
            id=after["id"],
            email=after["email"].lower().strip(),
            status=after["status"],
            is_active=after["status"] == "active",
            created_at=after["created_at"],
            source="streaming",
            ingested_at=_now(),
        )


class PartitionedLake:
    """A stand-in for the S3 lake: files keyed by partition path.

    Every record lands under year=/month=/day=/hour= — the same layout
    both writers must match, hour included.
    """

    def __init__(self, table: str = "customers"):
        self.table = table
        self.files: dict[str, list[CustomerRecord]] = {}

    @staticmethod
    def partition_key(table: str, when: datetime) -> str:
        return (
            f"{table}"
            f"/year={when:%Y}/month={when:%m}/day={when:%d}/hour={when:%H}"
        )

    def write(self, record: CustomerRecord, when: datetime | None = None) -> str:
        when = when or _now()
        key = self.partition_key(self.table, when)
        self.files.setdefault(key, []).append(record)
        return key

    def read_all(self) -> list[CustomerRecord]:
        return [r for rows in self.files.values() for r in rows]


class SpeedLayer:
    """Redis stand-in: latest streaming state per key."""

    def __init__(self):
        self._state: dict[int, dict] = {}

    def put(self, record: CustomerRecord) -> None:
        self._state[record.id] = {
            "id": record.id,
            "email": record.email,
            "status": record.status,
            "is_active": record.is_active,
        }

    def get(self, customer_id: int) -> dict | None:
        return self._state.get(customer_id)


class ServingLayer:
    """Trino stand-in: ROW_NUMBER() dedup preferring streaming, then freshest."""

    @staticmethod
    def latest(records: list[CustomerRecord]) -> list[CustomerRecord]:
        rank = {"streaming": 0, "batch": 1}
        best: dict[int, CustomerRecord] = {}
        for r in records:
            cur = best.get(r.id)
            key = (rank[r.source], -r.ingested_at.timestamp())
            if cur is None or key < (
                rank[cur.source],
                -cur.ingested_at.timestamp(),
            ):
                best[r.id] = r
        return list(best.values())


class UnifiedConsumer:
    """History from the serving layer + fresh state from the speed layer."""

    def __init__(self, lake: PartitionedLake, speed: SpeedLayer):
        self.lake = lake
        self.speed = speed

    def get_unified_view(self, customer_id: int) -> dict | None:
        historical = next(
            (
                r
                for r in ServingLayer.latest(self.lake.read_all())
                if r.id == customer_id
            ),
            None,
        )
        result = vars(historical).copy() if historical else {}

        latest = self.speed.get(customer_id)
        if latest:
            # Streaming overrides only the fields it actually carries
            for f in ("email", "status", "is_active"):
                if f in latest:
                    result[f] = latest[f]
            result["source"] = "merged"

        return result or None


def _demo() -> None:
    lake, speed = PartitionedLake(), SpeedLayer()
    batch, stream = BatchProducer(), StreamingProducer()
    when = datetime(2026, 8, 19, 14, tzinfo=timezone.utc)

    lake.write(batch.produce({
        "id": 1, "email": "  ANA@Shop.com ", "status": "active",
        "created_at": when,
    }), when)

    event = {"after": {
        "id": 1, "email": "ana@shop.com", "status": "banned",
        "created_at": when,
    }}
    rec = stream.produce(event)
    lake.write(rec, when)
    speed.put(rec)

    print("partitions:", list(lake.files))
    print("serving dedup:", [r.source for r in ServingLayer.latest(lake.read_all())])
    print("unified view:", UnifiedConsumer(lake, speed).get_unified_view(1))


if __name__ == "__main__":
    _demo()
