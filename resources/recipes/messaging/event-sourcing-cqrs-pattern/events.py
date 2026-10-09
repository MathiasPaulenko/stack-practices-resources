import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    # default_factory runs per instance — a plain default would be
    # evaluated once at class definition and shared by every event.
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    aggregate_id: str
    version: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = Field(default_factory=dict)


class AccountCreated(DomainEvent):
    event_type: str = "AccountCreated"
    owner_name: str
    initial_balance: float


class MoneyDeposited(DomainEvent):
    event_type: str = "MoneyDeposited"
    amount: float
    description: str


class MoneyWithdrawn(DomainEvent):
    event_type: str = "MoneyWithdrawn"
    amount: float
    description: str


class AccountClosed(DomainEvent):
    event_type: str = "AccountClosed"
    reason: str


EVENT_REGISTRY = {
    "AccountCreated": AccountCreated,
    "MoneyDeposited": MoneyDeposited,
    "MoneyWithdrawn": MoneyWithdrawn,
    "AccountClosed": AccountClosed,
}
