# Example: Python application metrics with the Prometheus client library.
# Companion to https://stackpractices.com/guides/metrics-and-dashboards-guide/
# pip install prometheus-client flask

from prometheus_client import Counter, Histogram, Gauge, start_http_server
from flask import Flask, jsonify
import time

app = Flask(__name__)

# Choose buckets around the latency thresholds you alert on.
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'status', 'path']
)

request_duration_seconds = Histogram(
    'request_duration_seconds',
    'HTTP request duration',
    ['method', 'path'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# Business metrics alongside technical ones.
orders_total = Counter(
    'orders_total',
    'Orders processed',
    ['result']
)


class OrderNotFound(Exception):
    pass


def fetch_order(order_id):
    raise OrderNotFound()


@app.route("/api/orders/<order_id>")
def get_order(order_id):
    start = time.time()
    active_connections.inc()

    try:
        order = fetch_order(order_id)
        http_requests_total.labels(method='GET', status='200', path='/api/orders').inc()
        orders_total.labels(result='success').inc()
        return jsonify(order)
    except OrderNotFound:
        http_requests_total.labels(method='GET', status='404', path='/api/orders').inc()
        return jsonify({"error": "Not found"}), 404
    finally:
        request_duration_seconds.labels(method='GET', path='/api/orders').observe(time.time() - start)
        active_connections.dec()


if __name__ == "__main__":
    # Serve /metrics on a dedicated port bound to the internal interface.
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000)
