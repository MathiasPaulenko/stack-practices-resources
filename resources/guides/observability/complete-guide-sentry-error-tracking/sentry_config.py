"""Sentry SDK configuration for Python (Flask/Django).

This module shows how to initialize the Sentry SDK with sensitive data
filtering, user context, breadcrumbs, and manual error capture.

Usage:
    from sentry_config import init_sentry
    init_sentry()
"""

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


def init_sentry() -> None:
    """Initialize Sentry SDK with integrations and PII filtering."""
    sentry_sdk.init(
        dsn="https://your-dsn@sentry.io/123",
        environment="production",
        release="order-service@1.2.3",
        traces_sample_rate=0.1,
        sample_rate=1.0,
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration(),
            RedisIntegration(),
            CeleryIntegration(),
        ],
        send_default_pii=True,
        before_send=filter_sensitive_data,
    )


def filter_sensitive_data(event: dict, hint: dict) -> dict:
    """Remove sensitive data before sending to Sentry."""
    if "request" in event:
        headers = event["request"].get("headers", {})
        for key in list(headers.keys()):
            if key.lower() in ("authorization", "cookie", "x-api-key"):
                headers[key] = "[REDACTED]"
        body = event["request"].get("data", {})
        if isinstance(body, dict):
            for key in ("password", "credit_card", "ssn"):
                if key in body:
                    body[key] = "[REDACTED]"
    return event


class PaymentError(Exception):
    """Raised when a payment fails."""


class OrderService:
    """Example service with manual error capture."""

    def create_order(self, user_id: int, items: list[dict]) -> dict:
        from sentry_sdk import capture_exception, set_user, add_breadcrumb

        set_user({"id": str(user_id), "email": "user@example.com"})
        add_breadcrumb(
            category="order",
            message=f"Creating order for user {user_id} with {len(items)} items",
            level="info",
        )

        try:
            order = self._process_order(user_id, items)
            add_breadcrumb(category="order", message="Order created successfully", level="info")
            return order
        except PaymentError as e:
            capture_exception(e, {
                "extra": {
                    "user_id": user_id,
                    "items_count": len(items),
                    "total_amount": sum(i["price"] * i["quantity"] for i in items),
                },
                "tags": {"error_type": "payment", "severity": "high"},
            })
            raise
        except Exception as e:
            capture_exception(e)
            raise

    def _process_order(self, user_id: int, items: list[dict]) -> dict:
        return {"user_id": user_id, "items": items, "status": "created"}
