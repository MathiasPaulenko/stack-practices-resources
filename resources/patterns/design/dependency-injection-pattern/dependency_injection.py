"""Dependency Injection: manual constructor injection plus a tiny container.

Shows both ends of the pattern — plain constructor wiring (all you need
for small apps) and a minimal container that resolves a dependency graph
automatically (the shape of what Spring/tsyringe do at scale).

No dependencies; run directly: python dependency_injection.py
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Type


# --- The dependencies and the service that receives them ---

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        ...


class StripeProcessor(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f"Charging ${amount} via Stripe")
        return True


class Logger(ABC):
    @abstractmethod
    def log(self, msg: str) -> None:
        ...


class ConsoleLogger(Logger):
    def log(self, msg: str) -> None:
        print(f"[log] {msg}")


class OrderService:
    """Dependencies arrive through the constructor — nothing is created here."""

    def __init__(self, processor: PaymentProcessor, logger: Logger):
        self.processor = processor
        self.logger = logger

    def checkout(self, amount: float) -> bool:
        ok = self.processor.charge(amount)
        self.logger.log(f"checkout({amount}) -> {ok}")
        return ok


# --- Manual wiring at the composition root (the default choice) ---

def composition_root() -> OrderService:
    return OrderService(processor=StripeProcessor(), logger=ConsoleLogger())


# --- A minimal DI container: register a factory per type, resolve lazily ---

class Container:
    def __init__(self) -> None:
        self._factories: Dict[Type, Callable[["Container"], Any]] = {}
        self._singletons: Dict[Type, Any] = {}

    def register(self, iface: Type, factory: Callable[["Container"], Any], *, singleton: bool = False) -> None:
        self._factories[iface] = (lambda c, f=factory, s=singleton, t=iface: self._resolve_singleton(t, f, c) if s else f(c))

    def _resolve_singleton(self, t: Type, f: Callable[["Container"], Any], c: "Container") -> Any:
        if t not in self._singletons:
            self._singletons[t] = f(c)
        return self._singletons[t]

    def resolve(self, iface: Type) -> Any:
        if iface not in self._factories:
            raise KeyError(f"No registration for {iface.__name__}")
        return self._factories[iface](self)


def container_root() -> OrderService:
    c = Container()
    c.register(Logger, lambda _: ConsoleLogger(), singleton=True)
    c.register(PaymentProcessor, lambda _: StripeProcessor(), singleton=True)
    c.register(OrderService, lambda c: OrderService(c.resolve(PaymentProcessor), c.resolve(Logger)))
    return c.resolve(OrderService)


if __name__ == "__main__":
    composition_root().checkout(100.0)
    container_root().checkout(42.5)

    # Scope demo: singleton shares one instance, transient builds a new one.
    c = Container()
    c.register(Logger, lambda _: ConsoleLogger(), singleton=True)
    c.register(OrderService, lambda c: OrderService(StripeProcessor(), c.resolve(Logger)))
    assert c.resolve(Logger) is c.resolve(Logger)          # singleton
    assert c.resolve(OrderService) is not c.resolve(OrderService)  # transient

    # Testing is the point: inject a fake without touching OrderService.
    class FakeProcessor(PaymentProcessor):
        def charge(self, amount: float) -> bool:
            return amount < 50

    assert OrderService(FakeProcessor(), ConsoleLogger()).checkout(10.0)
    assert not OrderService(FakeProcessor(), ConsoleLogger()).checkout(99.0)
    print("All DI examples ran.")
