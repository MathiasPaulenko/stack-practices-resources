from prometheus_client import CollectorRegistry, Gauge, generate_latest
import requests


class DatabaseCollector:
    """Custom collector that scrapes database stats."""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.registry = CollectorRegistry()

        self.active_queries = Gauge(
            "db_active_queries",
            "Number of active database queries",
            registry=self.registry
        )
        self.connection_pool = Gauge(
            "db_connection_pool_size",
            "Database connection pool size",
            ["state"],
            registry=self.registry
        )

    def collect(self):
        stats = requests.get(f"{self.db_url}/stats").json()

        self.active_queries.set(stats["active_queries"])
        self.connection_pool.labels(state="idle").set(stats["pool"]["idle"])
        self.connection_pool.labels(state="active").set(stats["pool"]["active"])
        self.connection_pool.labels(state="waiting").set(stats["pool"]["waiting"])

        yield from self.registry.collect()


if __name__ == "__main__":
    from flask import Flask, Response

    app = Flask(__name__)
    collector = DatabaseCollector("http://localhost:8080")

    @app.route("/metrics")
    def metrics():
        collector.collect()
        return Response(
            generate_latest(collector.registry),
            mimetype="text/plain; version=0.0.4; charset=utf-8"
        )

    app.run(host="0.0.0.0", port=5000)
