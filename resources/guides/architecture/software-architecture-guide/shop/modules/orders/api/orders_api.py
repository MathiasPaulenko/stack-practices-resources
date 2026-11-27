class OrdersApi:
    """Public interface of the orders module. Payments consumes this; nothing
    else may reach into orders' internals."""

    def get_order_total_cents(self, order_id: str) -> int:
        raise NotImplementedError

    def mark_paid(self, order_id: str) -> None:
        raise NotImplementedError
