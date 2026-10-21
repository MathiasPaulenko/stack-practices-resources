"""Compensating Transaction — runnable saga demo.

A successful order saga (charge → reserve → ship) and a failing one
(insufficient stock) that triggers reverse-order compensation.

Run: python compensating_transaction.py  (stdlib only)
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class StepResult:
    success: bool
    step_name: str
    compensation_needed: bool = False
    compensation_error: Optional[str] = None


class SagaOrchestrator:
    """Coordinates a saga with compensating transactions."""

    def __init__(self):
        self.completed_steps: List[dict] = []
        self.compensation_log: List[dict] = []

    def execute(self, steps: List[dict]) -> StepResult:
        for i, step in enumerate(steps):
            print(f"Executing step {i + 1}: {step['name']}")
            success = step["action"]()
            if success:
                self.completed_steps.append(
                    {"index": i, "name": step["name"], "compensate": step["compensate"]}
                )
            else:
                print(f"Step {step['name']} failed! Running compensating transactions...")
                self._compensate()
                return StepResult(success=False, step_name=step["name"])
        return StepResult(success=True, step_name="all_steps")

    def _compensate(self):
        """Run compensating transactions in reverse order."""
        for step in reversed(self.completed_steps):
            print(f"Compensating: {step['name']}")
            try:
                step["compensate"]()
                self.compensation_log.append(
                    {"step": step["name"], "status": "success",
                     "timestamp": datetime.now().isoformat()}
                )
            except Exception as e:
                self.compensation_log.append(
                    {"step": step["name"], "status": "failed",
                     "error": str(e), "timestamp": datetime.now().isoformat()}
                )
                print(f"WARNING: Compensation failed for {step['name']}: {e}")


class PaymentService:
    def __init__(self):
        self.charges = {}

    def charge(self, order_id: str, amount: float) -> bool:
        txn_id = str(uuid.uuid4())
        self.charges[order_id] = {"txn_id": txn_id, "amount": amount, "status": "charged"}
        print(f"  [Payment] Charged ${amount} for order {order_id}, txn={txn_id}")
        return True

    def refund(self, order_id: str) -> bool:
        charge = self.charges.get(order_id)
        if charge:
            charge["status"] = "refunded"
            print(f"  [Payment] Refunded ${charge['amount']} for order {order_id}")
            return True
        print(f"  [Payment] No charge found for order {order_id}")
        return False


class InventoryService:
    def __init__(self):
        self.stock = {"SKU-001": 100, "SKU-002": 50}
        self.reservations = {}

    def reserve(self, order_id: str, sku: str, qty: int) -> bool:
        if self.stock.get(sku, 0) >= qty:
            self.stock[sku] -= qty
            self.reservations[order_id] = {"sku": sku, "qty": qty}
            print(f"  [Inventory] Reserved {qty}x {sku} for order {order_id}")
            return True
        print(f"  [Inventory] Insufficient stock for {sku}")
        return False

    def release(self, order_id: str) -> bool:
        reservation = self.reservations.pop(order_id, None)
        if reservation:
            self.stock[reservation["sku"]] += reservation["qty"]
            print(f"  [Inventory] Released {reservation['qty']}x {reservation['sku']}")
            return True
        return False


class ShippingService:
    def __init__(self):
        self.shipments = {}

    def create_label(self, order_id: str, address: str) -> bool:
        self.shipments[order_id] = {"address": address, "status": "label_created"}
        print(f"  [Shipping] Label created for order {order_id}")
        return True

    def cancel_label(self, order_id: str) -> bool:
        shipment = self.shipments.pop(order_id, None)
        if shipment:
            print(f"  [Shipping] Label cancelled for order {order_id}")
            return True
        return False


class OrderSaga:
    def __init__(self, payments: PaymentService, inventory: InventoryService,
                 shipping: ShippingService):
        self.payments = payments
        self.inventory = inventory
        self.shipping = shipping

    def create_order(self, order_id: str, amount: float, sku: str, qty: int,
                     address: str) -> StepResult:
        saga = SagaOrchestrator()
        steps = [
            {"name": "charge_payment",
             "action": lambda: self.payments.charge(order_id, amount),
             "compensate": lambda: self.payments.refund(order_id)},
            {"name": "reserve_inventory",
             "action": lambda: self.inventory.reserve(order_id, sku, qty),
             "compensate": lambda: self.inventory.release(order_id)},
            {"name": "create_shipping_label",
             "action": lambda: self.shipping.create_label(order_id, address),
             "compensate": lambda: self.shipping.cancel_label(order_id)},
        ]
        return saga.execute(steps)


if __name__ == "__main__":
    payments = PaymentService()
    inventory = InventoryService()
    shipping = ShippingService()
    saga = OrderSaga(payments, inventory, shipping)

    print("=== ORDER 1 (Success) ===")
    result = saga.create_order("ORD-001", 99.99, "SKU-001", 2, "123 Main St")
    print(f"Result: {'SUCCESS' if result.success else 'FAILED'}")

    print("\n=== ORDER 2 (Failure -> Compensation) ===")
    result = saga.create_order("ORD-002", 999.99, "SKU-999", 500, "456 Oak Ave")
    print(f"Result: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Payment refunded: {payments.charges.get('ORD-002', {}).get('status')}")
