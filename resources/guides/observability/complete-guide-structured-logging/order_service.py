# order_service.py — Structured logging in practice
import structlog

logger = structlog.get_logger()


class OrderService:
    def create_order(self, user_id: int, items: list[dict]) -> dict:
        logger.info(
            "order_creation_started",
            user_id=user_id,
            items_count=len(items),
            total_amount=sum(i["price"] * i["quantity"] for i in items),
        )

        try:
            payment = self.payment_client.charge(
                user_id=user_id,
                amount=sum(i["price"] * i["quantity"] for i in items),
            )
            logger.info(
                "payment_processed",
                user_id=user_id,
                payment_id=payment["id"],
                amount=payment["amount"],
            )

            order = self.order_repo.create(
                user_id=user_id, items=items, payment_id=payment["id"]
            )
            logger.info(
                "order_created",
                order_id=order["id"],
                user_id=user_id,
                total_amount=order["total"],
            )
            return order

        except Exception:
            logger.exception("order_creation_failed", user_id=user_id)
            raise
