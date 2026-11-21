"""Business metrics with dimensional tags.

Counters and histograms tagged by product category, payment method
and region — the labels that make per-segment dashboards possible.
Keep every tag bounded: no user IDs, no request IDs.
"""
import random
import time

from prometheus_client import Counter, Gauge, Histogram, start_http_server

ORDERS_PROCESSED = Counter(
    "orders_processed_total",
    "Total orders processed",
    ["product_category", "payment_method", "region", "status"],
)

ORDER_VALUE = Histogram(
    "order_value_usd",
    "Order value in USD",
    ["product_category", "region"],
    buckets=[1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000],
)

ACTIVE_SUBSCRIPTIONS = Gauge(
    "active_subscriptions",
    "Currently active subscriptions",
    ["plan", "region"],
)

CATEGORIES = ["electronics", "books", "clothing"]
PAYMENT_METHODS = ["card", "paypal", "transfer"]
REGIONS = ["us-east", "eu-west", "sa-east"]


class Order:
    def __init__(self) -> None:
        self.category = random.choice(CATEGORIES)
        self.payment_method = random.choice(PAYMENT_METHODS)
        self.region = random.choice(REGIONS)
        self.total = round(random.uniform(5, 900), 2)
        self.success = random.random() > 0.05


def process_order(order: Order) -> None:
    ORDER_VALUE.labels(
        product_category=order.category,
        region=order.region,
    ).observe(order.total)

    ORDERS_PROCESSED.labels(
        product_category=order.category,
        payment_method=order.payment_method,
        region=order.region,
        status="success" if order.success else "failed",
    ).inc()


def main() -> None:
    start_http_server(9091)
    print("Business metrics at http://localhost:9091/metrics — Ctrl+C to stop")

    ACTIVE_SUBSCRIPTIONS.labels(plan="pro", region="us-east").set(1200)
    ACTIVE_SUBSCRIPTIONS.labels(plan="free", region="eu-west").set(5400)

    try:
        while True:
            process_order(Order())
            time.sleep(random.uniform(0.02, 0.15))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
