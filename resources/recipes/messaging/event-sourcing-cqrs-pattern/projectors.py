from sqlalchemy import Column, DateTime, Float, String, text

from event_store import Base
from events import (
    AccountClosed,
    AccountCreated,
    DomainEvent,
    MoneyDeposited,
    MoneyWithdrawn,
)


class AccountProjection(Base):
    __tablename__ = "account_projection"
    id = Column(String, primary_key=True)
    owner_name = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=0)
    status = Column(String, nullable=False, default="active")
    last_updated = Column(DateTime)


class TransactionProjection(Base):
    __tablename__ = "transaction_projection"
    id = Column(String, primary_key=True)
    account_id = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # deposit, withdrawal
    amount = Column(Float, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, nullable=False)


def _mark_processed(session, event: DomainEvent) -> bool:
    """Insert dedup row. Returns True if the event is new."""
    result = session.execute(
        text(
            """INSERT INTO processed_events (event_id, processed_at)
               VALUES (:id, NOW()) ON CONFLICT DO NOTHING"""
        ),
        {"id": event.event_id},
    )
    return result.rowcount == 1


class AccountProjector:
    """Projects events into read-optimized tables."""

    def __init__(self, session_factory):
        self.Session = session_factory

    def handle(self, event: DomainEvent):
        session = self.Session()
        try:
            # Durable dedup — an in-memory set dies on restart, a table doesn't
            if not _mark_processed(session, event):
                return  # already processed

            if isinstance(event, AccountCreated):
                session.execute(
                    text(
                        """INSERT INTO account_projection (id, owner_name, balance, status, last_updated)
                           VALUES (:id, :name, :bal, 'active', :ts)"""
                    ),
                    {
                        "id": event.aggregate_id,
                        "name": event.owner_name,
                        "bal": event.initial_balance,
                        "ts": event.timestamp,
                    },
                )

            elif isinstance(event, MoneyDeposited):
                session.execute(
                    text(
                        """UPDATE account_projection SET balance = balance + :amt, last_updated = :ts
                           WHERE id = :id"""
                    ),
                    {
                        "amt": event.amount,
                        "ts": event.timestamp,
                        "id": event.aggregate_id,
                    },
                )
                session.execute(
                    text(
                        """INSERT INTO transaction_projection (id, account_id, type, amount, description, timestamp)
                           VALUES (:id, :aid, 'deposit', :amt, :desc, :ts)"""
                    ),
                    {
                        "id": event.event_id,
                        "aid": event.aggregate_id,
                        "amt": event.amount,
                        "desc": event.description,
                        "ts": event.timestamp,
                    },
                )

            elif isinstance(event, MoneyWithdrawn):
                session.execute(
                    text(
                        """UPDATE account_projection SET balance = balance - :amt, last_updated = :ts
                           WHERE id = :id"""
                    ),
                    {
                        "amt": event.amount,
                        "ts": event.timestamp,
                        "id": event.aggregate_id,
                    },
                )
                session.execute(
                    text(
                        """INSERT INTO transaction_projection (id, account_id, type, amount, description, timestamp)
                           VALUES (:id, :aid, 'withdrawal', :amt, :desc, :ts)"""
                    ),
                    {
                        "id": event.event_id,
                        "aid": event.aggregate_id,
                        "amt": event.amount,
                        "desc": event.description,
                        "ts": event.timestamp,
                    },
                )

            elif isinstance(event, AccountClosed):
                session.execute(
                    text(
                        """UPDATE account_projection SET status = 'closed', last_updated = :ts
                           WHERE id = :id"""
                    ),
                    {"ts": event.timestamp, "id": event.aggregate_id},
                )

            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class AccountStatsProjector:
    """Second projection counting per-account activity."""

    def __init__(self, session_factory):
        self.Session = session_factory

    def handle(self, event: DomainEvent):
        session = self.Session()
        try:
            if not _mark_processed(session, event):
                return
            session.execute(
                text(
                    """INSERT INTO account_stats (account_id, event_count, last_event_at)
                       VALUES (:aid, 1, :ts)
                       ON CONFLICT (account_id) DO UPDATE
                       SET event_count = account_stats.event_count + 1, last_event_at = :ts"""
                ),
                {"aid": event.aggregate_id, "ts": event.timestamp},
            )
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class ProjectorManager:
    """Fans out each event to every registered projector."""

    def __init__(self, projectors: list):
        self.projectors = projectors

    def handle(self, event: DomainEvent):
        for projector in self.projectors:
            projector.handle(event)
