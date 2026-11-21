"""Push-based metrics with StatsD — the variant for batch jobs
and short-lived processes that won't be alive at scrape time.

Run:
    pip install statsd
    # requires a StatsD-compatible collector on localhost:8125
    python statsd_metrics.py
"""
import time

import statsd

client = statsd.StatsClient("localhost", 8125, prefix="order-service")


def process_order() -> None:
    time.sleep(0.05)


if __name__ == "__main__":
    client.incr("orders.created")
    client.incr("orders.failed", count=1)

    with client.timer("order_processing_duration"):
        process_order()

    client.gauge("active_connections", 42)
    client.set("unique_users", 12345)

    print("Metrics pushed to StatsD on localhost:8125")
