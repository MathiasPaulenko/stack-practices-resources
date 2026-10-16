# metrics.py — Prometheus instrumentation for Python
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Define metrics
ORDERS_TOTAL = Counter(
    "orders_total",
    "Total number of orders created",
    ["status", "payment_method"],
)

ORDER_DURATION = Histogram(
    "order_creation_duration_seconds",
    "Time spent creating orders",
    ["endpoint"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

ACTIVE_USERS = Gauge(
    "active_users",
    "Number of currently active users",
)

QUEUE_DEPTH = Gauge(
    "message_queue_depth",
    "Number of messages in the queue",
    ["queue_name"],
)


# Usage in service code
class OrderService:
    def create_order(self, user_id: int, items: list[dict]) -> dict:
        start = time.time()
        try:
            order = self._process_order(user_id, items)
            ORDERS_TOTAL.labels(status="success", payment_method=order["payment_method"]).inc()
            return order
        except PaymentError:
            ORDERS_TOTAL.labels(status="payment_failed", payment_method="unknown").inc()
            raise
        except Exception:
            ORDERS_TOTAL.labels(status="error", payment_method="unknown").inc()
            raise
        finally:
            ORDER_DURATION.labels(endpoint="/api/orders").observe(time.time() - start)


# Metrics endpoint
from flask import Flask, Response

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
