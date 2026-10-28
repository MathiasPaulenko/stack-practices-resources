"""Business Delegate: lookup, cached reference, and retry with backoff."""
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class OrderServiceInterface(ABC):
    @abstractmethod
    def create_order(self, customer_id: str, items: list) -> dict:
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> dict:
        pass


class RemoteOrderService(OrderServiceInterface):
    """Simulated remote EJB or API service"""
    def create_order(self, customer_id: str, items: list) -> dict:
        return {"order_id": "ORD-123", "status": "created", "items": items}

    def get_order(self, order_id: str) -> dict:
        return {"order_id": order_id, "status": "shipped"}


class ServiceLocator:
    """Central registry for service lookup"""
    _services: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, service: Any):
        cls._services[name] = service

    @classmethod
    def lookup(cls, name: str) -> Any:
        return cls._services.get(name)


class OrderBusinessDelegate:
    """Delegate that simplifies access to OrderService"""
    def __init__(self):
        self._service: Optional[OrderServiceInterface] = None

    def _get_service(self) -> OrderServiceInterface:
        if self._service is None:
            self._service = ServiceLocator.lookup("OrderService")
            if self._service is None:
                self._service = RemoteOrderService()
        return self._service

    def create_order(self, customer_id: str, items: list) -> dict:
        try:
            return self._get_service().create_order(customer_id, items)
        except Exception as e:
            raise RuntimeError(f"Failed to create order: {e}")

    def get_order(self, order_id: str) -> dict:
        return self._get_service().get_order(order_id)


class ResilientOrderDelegate:
    """Caches the service reference and retries remote calls."""
    def __init__(self, max_retries: int = 3):
        self._service = None
        self._max_retries = max_retries

    def _get_service(self):
        if self._service is None:
            self._service = ServiceLocator.lookup("OrderService") or RemoteOrderService()
        return self._service

    def create_order(self, customer_id: str, items: list) -> dict:
        delay = 0.05
        for attempt in range(1, self._max_retries + 1):
            try:
                return self._get_service().create_order(customer_id, items)
            except Exception as exc:
                if attempt == self._max_retries:
                    raise RuntimeError("Order service unavailable after %d attempts" % attempt) from exc
                time.sleep(delay)
                delay *= 2


# Presentation layer (servlet/controller equivalent)
class OrderController:
    def __init__(self):
        self.delegate = OrderBusinessDelegate()

    def handle_create_order(self, customer_id: str, items: list):
        result = self.delegate.create_order(customer_id, items)
        return f"Order created: {result['order_id']}"


if __name__ == "__main__":
    ServiceLocator.register("OrderService", RemoteOrderService())
    controller = OrderController()
    print(controller.handle_create_order("CUST-001", ["item1", "item2"]))
    resilient = ResilientOrderDelegate()
    print(resilient.create_order("CUST-002", ["item3"]))
