from dataclasses import dataclass


@dataclass
class CartItem:
    id: str
    price: float
    qty: int


@dataclass
class Address:
    email: str
    country: str


@dataclass
class OrderResult:
    order_id: str
    total: float
    tracking_number: str


class InventoryService:
    def check_stock(self, item_id: str) -> bool:
        return True

    def reserve(self, item_id: str, qty: int) -> None:
        print(f"  reserved {qty}x {item_id}")


class PricingService:
    def calculate_total(self, items: list[CartItem]) -> float:
        return sum(i.price * i.qty for i in items)

    def apply_coupon(self, total: float, coupon: str) -> float:
        return total * 0.9 if coupon else total


class PaymentService:
    def charge(self, amount: float, token: str) -> dict:
        print(f"  charged {amount:.2f} with {token}")
        return {"success": True, "tx_id": "tx_123"}


class ShippingService:
    def create_label(self, address: Address) -> str:
        return "TRK_456"

    def calculate_cost(self, address: Address) -> float:
        return 9.99


class NotificationService:
    def send_confirmation(self, email: str, order_id: str) -> None:
        print(f"  confirmation sent to {email} for {order_id}")


class CheckoutFacade:
    """Facade: one entry point for the whole checkout flow.

    Services are injected, so each one stays mockable in tests and
    remains directly reachable for callers that need it.
    """

    def __init__(self, inventory, pricing, payment, shipping, notification):
        self.inventory = inventory
        self.pricing = pricing
        self.payment = payment
        self.shipping = shipping
        self.notification = notification

    def checkout(self, cart: list[CartItem], coupon: str,
                 payment_token: str, address: Address) -> OrderResult:
        # 1. Check stock and reserve
        for item in cart:
            if not self.inventory.check_stock(item.id):
                raise ValueError(f"Item {item.id} out of stock")
            self.inventory.reserve(item.id, item.qty)

        # 2. Calculate price
        total = self.pricing.calculate_total(cart)
        if coupon:
            total = self.pricing.apply_coupon(total, coupon)
        total += self.shipping.calculate_cost(address)

        # 3. Charge
        result = self.payment.charge(total, payment_token)
        if not result["success"]:
            raise ValueError("Payment failed")

        # 4. Create shipment
        tracking = self.shipping.create_label(address)

        # 5. Notify
        self.notification.send_confirmation(address.email, result["tx_id"])

        return OrderResult(order_id=result["tx_id"], total=total,
                           tracking_number=tracking)


if __name__ == "__main__":
    facade = CheckoutFacade(
        InventoryService(), PricingService(), PaymentService(),
        ShippingService(), NotificationService(),
    )
    cart = [CartItem("sku-1", 25.0, 2), CartItem("sku-2", 10.0, 1)]
    addr = Address(email="ana@example.com", country="ES")
    order = facade.checkout(cart, "SAVE10", "tok_abc", addr)
    print(order)
