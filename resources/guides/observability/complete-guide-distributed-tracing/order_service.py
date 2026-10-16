"""Manual span creation for business operations in an order service."""
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)


class OrderService:
    def __init__(self, auth_client, inventory_client, payment_client, order_repo):
        self.auth_client = auth_client
        self.inventory_client = inventory_client
        self.payment_client = payment_client
        self.order_repo = order_repo

    def create_order(self, user_id: int, items: list[dict]) -> dict:
        with tracer.start_as_current_span("create_order") as span:
            span.set_attribute("user.id", user_id)
            span.set_attribute("items.count", len(items))

            try:
                with tracer.start_as_current_span("validate_user") as child:
                    user = self.auth_client.get_user(user_id)
                    child.set_attribute("user.email", user["email"])
                    child.set_attribute("user.active", user["is_active"])

                with tracer.start_as_current_span("check_inventory") as child:
                    for item in items:
                        stock = self.inventory_client.get_stock(item["product_id"])
                        child.set_attribute(f"product.{item['product_id']}.stock", stock)
                        if stock < item["quantity"]:
                            raise ValueError(
                                f"Insufficient stock for product {item['product_id']}"
                            )

                with tracer.start_as_current_span("process_payment") as child:
                    payment = self.payment_client.charge(
                        user_id=user_id,
                        amount=sum(i["price"] * i["quantity"] for i in items),
                    )
                    child.set_attribute("payment.id", payment["id"])
                    child.set_attribute("payment.amount", payment["amount"])

                with tracer.start_as_current_span("save_order") as child:
                    order = self.order_repo.create(
                        user_id=user_id, items=items, payment_id=payment["id"]
                    )
                    child.set_attribute("order.id", order["id"])

                span.set_attribute("order.id", order["id"])
                span.set_status(Status(StatusCode.OK))
                return order

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
