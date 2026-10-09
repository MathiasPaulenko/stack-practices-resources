from abc import ABC, abstractmethod
from typing import List

from events import (
    AccountClosed,
    AccountCreated,
    DomainEvent,
    MoneyDeposited,
    MoneyWithdrawn,
)


class AggregateRoot(ABC):
    def __init__(self, aggregate_id: str):
        self.id = aggregate_id
        self.version = -1
        self._pending_events: List[DomainEvent] = []

    @abstractmethod
    def apply(self, event: DomainEvent):
        pass

    def raise_event(self, event: DomainEvent):
        event.version = self.version + 1
        self.apply(event)
        self.version = event.version
        self._pending_events.append(event)

    def get_pending_events(self) -> List[DomainEvent]:
        return self._pending_events

    def clear_pending_events(self):
        self._pending_events.clear()

    @classmethod
    def from_events(cls, aggregate_id: str, events: List[DomainEvent]):
        aggregate = cls(aggregate_id)
        for event in events:
            aggregate.apply(event)
            aggregate.version = event.version
        return aggregate


class BankAccount(AggregateRoot):
    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.owner_name: str = ""
        self.balance: float = 0
        self.status: str = "nonexistent"

    def apply(self, event: DomainEvent):
        if isinstance(event, AccountCreated):
            self.owner_name = event.owner_name
            self.balance = event.initial_balance
            self.status = "active"
        elif isinstance(event, MoneyDeposited):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount
        elif isinstance(event, AccountClosed):
            self.status = "closed"

    # Command methods — validate and raise events
    def create(self, owner_name: str, initial_balance: float):
        if self.status != "nonexistent":
            raise ValueError("Account already exists")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.raise_event(AccountCreated(
            aggregate_id=self.id,
            version=0,
            owner_name=owner_name,
            initial_balance=initial_balance,
        ))

    def deposit(self, amount: float, description: str = ""):
        if self.status != "active":
            raise ValueError("Account is not active")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.raise_event(MoneyDeposited(
            aggregate_id=self.id,
            version=self.version + 1,
            amount=amount,
            description=description,
        ))

    def withdraw(self, amount: float, description: str = ""):
        if self.status != "active":
            raise ValueError("Account is not active")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")

        self.raise_event(MoneyWithdrawn(
            aggregate_id=self.id,
            version=self.version + 1,
            amount=amount,
            description=description,
        ))

    def close(self, reason: str):
        if self.status != "active":
            raise ValueError("Account is not active")
        if self.balance != 0:
            raise ValueError("Balance must be zero to close")

        self.raise_event(AccountClosed(
            aggregate_id=self.id,
            version=self.version + 1,
            reason=reason,
        ))
