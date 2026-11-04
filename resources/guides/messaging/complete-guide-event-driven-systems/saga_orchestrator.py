"""Orchestration-based saga: central coordinator drives steps + compensation."""
from uuid import uuid4


class OrderSagaOrchestrator:
    def __init__(self, event_store, message_bus):
        self.event_store = event_store
        self.message_bus = message_bus

    def start_saga(self, order_id: str, total: float, items: list) -> str:
        saga_id = str(uuid4())
        self.event_store.append("SagaStarted", {
            "saga_id": saga_id, "order_id": order_id,
            "total": total, "items": items, "status": "processing_payment",
        })
        self.message_bus.send("ProcessPayment", {
            "saga_id": saga_id, "order_id": order_id, "amount": total,
        })
        return saga_id

    def on_payment_processed(self, event: dict) -> None:
        saga = self.load_saga(event["data"]["saga_id"])
        if saga["status"] != "processing_payment":
            return
        self.event_store.append("SagaStepCompleted", {
            "saga_id": saga["saga_id"], "step": "payment",
        })
        self.message_bus.send("ReserveInventory", {
            "saga_id": saga["saga_id"], "order_id": saga["order_id"],
            "items": saga["items"],
        })
        self.update_saga_status(saga["saga_id"], "reserving_inventory")

    def on_inventory_failed(self, event: dict) -> None:
        saga = self.load_saga(event["data"]["saga_id"])
        self.message_bus.send("RefundPayment", {
            "saga_id": saga["saga_id"], "order_id": saga["order_id"],
        })
        self.update_saga_status(saga["saga_id"], "failed")

    def load_saga(self, saga_id: str) -> dict:
        raise NotImplementedError

    def update_saga_status(self, saga_id: str, status: str) -> None:
        raise NotImplementedError
