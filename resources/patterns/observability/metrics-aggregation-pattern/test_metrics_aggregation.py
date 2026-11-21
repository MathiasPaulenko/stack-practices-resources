"""Tests for the metrics-aggregation companion examples.

Run: pip install prometheus-client pytest && pytest test_metrics_aggregation.py
"""
from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram


def test_counter_increments():
    registry = CollectorRegistry()
    c = Counter("orders_total", "Total orders", registry=registry)
    c.inc()
    c.inc(3)
    assert registry.get_sample_value("orders_total") == 4


def test_counter_with_labels():
    registry = CollectorRegistry()
    c = Counter(
        "requests_total", "Requests", ["method", "status"], registry=registry
    )
    c.labels(method="GET", status="200").inc()
    c.labels(method="GET", status="200").inc()
    c.labels(method="POST", status="500").inc()
    assert (
        registry.get_sample_value(
            "requests_total", {"method": "GET", "status": "200"}
        )
        == 2
    )
    assert (
        registry.get_sample_value(
            "requests_total", {"method": "POST", "status": "500"}
        )
        == 1
    )


def test_gauge_goes_up_and_down():
    registry = CollectorRegistry()
    g = Gauge("active_connections", "Active", registry=registry)
    g.set(10)
    g.inc(5)
    g.dec(3)
    assert registry.get_sample_value("active_connections") == 12


def test_histogram_buckets():
    registry = CollectorRegistry()
    h = Histogram(
        "latency_seconds",
        "Latency",
        buckets=[0.1, 0.5, 1.0],
        registry=registry,
    )
    h.observe(0.05)
    h.observe(0.3)
    h.observe(0.8)

    assert registry.get_sample_value("latency_seconds_count") == 3
    assert registry.get_sample_value(
        "latency_seconds_bucket", {"le": "0.1"}
    ) == 1
    assert registry.get_sample_value(
        "latency_seconds_bucket", {"le": "0.5"}
    ) == 2
    assert registry.get_sample_value(
        "latency_seconds_bucket", {"le": "+Inf"}
    ) == 3


def test_business_metrics_labels_bounded():
    """The label set stays bounded: no per-user or per-request labels."""
    import business_metrics

    label_names = set(business_metrics.ORDERS_PROCESSED._labelnames)
    forbidden = {"user_id", "request_id", "order_id", "session_id"}
    assert not (label_names & forbidden), f"unbounded labels: {label_names}"
