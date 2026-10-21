"""State Pattern — runnable Python example.

An order lifecycle (pending -> paid -> shipped, or -> cancelled) where each
state is a class that owns its behavior and its outbound transitions.
"""
from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def pay(self, order):
        pass

    @abstractmethod
    def ship(self, order):
        pass

    @abstractmethod
    def cancel(self, order):
        pass


class PendingState(OrderState):
    def pay(self, order):
        print("Processing payment...")
        order.transition_to(PaidState())

    def ship(self, order):
        print("Cannot ship: payment pending")

    def cancel(self, order):
        print("Order cancelled")
        order.transition_to(CancelledState())


class PaidState(OrderState):
    def pay(self, order):
        print("Already paid")

    def ship(self, order):
        print("Shipping order...")
        order.transition_to(ShippedState())

    def cancel(self, order):
        print("Issuing refund...")
        order.transition_to(CancelledState())


class ShippedState(OrderState):
    def pay(self, order):
        print("Already paid")

    def ship(self, order):
        print("Already shipped")

    def cancel(self, order):
        print("Cannot cancel: already shipped")


class CancelledState(OrderState):
    def pay(self, order):
        print("Cannot pay: order cancelled")

    def ship(self, order):
        print("Cannot ship: order cancelled")

    def cancel(self, order):
        print("Already cancelled")


class Order:
    def __init__(self):
        self._state = PendingState()

    def transition_to(self, state):
        self._state = state

    def pay(self):
        self._state.pay(self)

    def ship(self):
        self._state.ship(self)

    def cancel(self):
        self._state.cancel(self)


# ---- Table-driven variant (for many states with thin per-state logic) ----

TRANSITIONS = {
    ("pending", "pay"): "paid",
    ("paid", "ship"): "shipped",
    ("pending", "cancel"): "cancelled",
    ("paid", "cancel"): "cancelled",
}


class InvalidTransition(Exception):
    pass


class TableDrivenOrder:
    def __init__(self):
        self.state = "pending"

    def handle(self, event):
        next_state = TRANSITIONS.get((self.state, event))
        if next_state is None:
            raise InvalidTransition(f"{event} not allowed in {self.state}")
        self.state = next_state


if __name__ == "__main__":
    order = Order()
    order.pay()
    order.ship()
    order.cancel()  # Cannot cancel: already shipped

    table_order = TableDrivenOrder()
    table_order.handle("pay")
    table_order.handle("ship")
    try:
        table_order.handle("cancel")
    except InvalidTransition as exc:
        print("Rejected:", exc)
