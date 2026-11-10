"""Repository + Unit of Work + application service.

The domain defines `OrderRepository` as an interface; infrastructure
provides the real implementation (an in-memory one here so it runs without
a database). Ordering: mutate -> save -> commit -> publish.
"""
from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional
from uuid import UUID, uuid4

from order_aggregate import Order, OrderPlaced


class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]: ...

    @abstractmethod
    async def save(self, order: Order) -> None: ...

    @abstractmethod
    async def delete(self, order: Order) -> None: ...


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._store: Dict[UUID, Order] = {}

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return self._store.get(order_id)

    async def save(self, order: Order) -> None:
        self._store[order.id] = order

    async def delete(self, order: Order) -> None:
        self._store.pop(order.id, None)


class UnitOfWork(ABC):
    order_repository: OrderRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.order_repository = InMemoryOrderRepository()

    async def commit(self):
        pass  # in-memory store needs no commit

    async def rollback(self):
        pass


class PrintEventBus:
    async def publish(self, event):
        print(f"published {type(event).__name__}")


class OrderApplicationService:
    """Orchestrates the use case; holds no business rules."""

    def __init__(self, uow_factory: Callable[[], UnitOfWork], event_bus):
        self._uow_factory = uow_factory
        self._event_bus = event_bus

    async def submit_order(self, order_id: UUID) -> None:
        async with self._uow_factory() as uow:
            order = await uow.order_repository.get_by_id(order_id)
            if order is None:
                raise ValueError(f"Order {order_id} not found")
            order.submit()
            await uow.order_repository.save(order)
            # Commit happens in __aexit__; publish only after it succeeds
            for event in order.domain_events:
                await self._event_bus.publish(event)
            order.clear_events()


if __name__ == "__main__":
    import asyncio

    async def main():
        uow = InMemoryUnitOfWork()
        order = Order(customer_id=uuid4())
        order.add_item(product_id=uuid4(), quantity=1, unit_price=99.0)
        await uow.order_repository.save(order)

        service = OrderApplicationService(
            uow_factory=lambda: uow, event_bus=PrintEventBus()
        )
        await service.submit_order(order.id)
        print("status:", order.status)

    asyncio.run(main())
