import json
from typing import List

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    text,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

from events import EVENT_REGISTRY, DomainEvent

Base = declarative_base()


class EventRecord(Base):
    __tablename__ = "event_store"
    __table_args__ = (
        # The real concurrency guard: two writers can't commit the same
        # (aggregate_id, version) pair even if both pass a SELECT check.
        UniqueConstraint("aggregate_id", "version", name="uq_aggregate_version"),
    )
    id = Column(String, primary_key=True)
    aggregate_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    data = Column(Text, nullable=False)
    # 'metadata' is a reserved attribute name in Declarative — map it explicitly
    event_metadata = Column("metadata", Text, nullable=False, default="{}")


class SnapshotRecord(Base):
    __tablename__ = "snapshots"
    aggregate_id = Column(String, primary_key=True)
    version = Column(Integer, nullable=False)
    state = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class ProcessedEvent(Base):
    __tablename__ = "processed_events"
    event_id = Column(String, primary_key=True)
    processed_at = Column(DateTime(timezone=True), nullable=False)


class ConcurrencyError(Exception):
    pass


class EventStore:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def append(self, aggregate_id: str, events: List[DomainEvent], expected_version: int):
        session = self.Session()
        try:
            # Fast-path check; the UNIQUE constraint above is the actual guarantee
            current = session.execute(
                text("SELECT MAX(version) FROM event_store WHERE aggregate_id = :aid"),
                {"aid": aggregate_id},
            ).scalar()
            current = current if current is not None else -1

            if current != expected_version:
                raise ConcurrencyError(
                    f"Expected version {expected_version}, got {current}"
                )

            for event in events:
                session.execute(
                    text(
                        """INSERT INTO event_store (id, aggregate_id, event_type, version, timestamp, data, metadata)
                           VALUES (:id, :aid, :etype, :ver, :ts, :data, :meta)"""
                    ),
                    {
                        "id": event.event_id,
                        "aid": aggregate_id,
                        "etype": event.event_type,
                        "ver": event.version,
                        "ts": event.timestamp,
                        "data": event.model_dump_json(),
                        "meta": json.dumps(event.metadata),
                    },
                )

            session.commit()
        except IntegrityError:
            session.rollback()
            # A concurrent writer committed the same version first
            raise ConcurrencyError(f"Version conflict on aggregate {aggregate_id}")
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        session = self.Session()
        try:
            records = session.execute(
                text(
                    """SELECT data FROM event_store
                       WHERE aggregate_id = :aid AND version > :ver
                       ORDER BY version ASC"""
                ),
                {"aid": aggregate_id, "ver": from_version},
            ).fetchall()

            events = []
            for record in records:
                data = json.loads(record[0])
                event_class = EVENT_REGISTRY.get(data["event_type"], DomainEvent)
                events.append(event_class(**data))
            return events
        finally:
            session.close()
