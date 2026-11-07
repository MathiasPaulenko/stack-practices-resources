"""Python implementation with event sourcing.

Source: https://stackpractices.com/recipes/cqrs-pattern-recipe/
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Any
from abc import ABC, abstractmethod


@dataclass
class Event:
    type: str
    aggregate_id: str
    payload: Any
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class EventStore(ABC):
    @abstractmethod
    async def append(self, events: List[Event]) -> None:
        ...

    @abstractmethod
    async def get_events(self, aggregate_id: str) -> List[Event]:
        ...


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: float


class OrderWriteModel:
    def __init__(self, order_id: str, customer_id: str, items: List[OrderItem]):
        self.id = order_id
        self.customer_id = customer_id
        self.items = items
        self.status = 'pending'

    def pay(self, payment_method: str) -> List[Event]:
        if self.status != 'pending':
            raise ValueError('Order already paid')
        self.status = 'paid'
        return [Event(
            type='OrderPaid',
            aggregate_id=self.id,
            payload={'payment_method': payment_method, 'total': self.total()}
        )]

    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)


class PayOrderHandler:
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    async def handle(self, order_id: str, payment_method: str) -> None:
        events = await self._event_store.get_events(order_id)
        order = self._rehydrate(events)
        new_events = order.pay(payment_method)
        await self._event_store.append(new_events)

    def _rehydrate(self, events: List[Event]) -> OrderWriteModel:
        if not events:
            raise ValueError('No events found for order')
        order = OrderWriteModel(events[0].aggregate_id, '', [])
        for event in events:
            if event.type == 'OrderCreated':
                order.customer_id = event.payload['customer_id']
                order.items = [OrderItem(**i) for i in event.payload['items']]
            elif event.type == 'OrderPaid':
                order.status = 'paid'
        return order
