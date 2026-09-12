from flask import Flask, request
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "flask_requests_total",
    "Total Flask requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "flask_request_duration_seconds",
    "Flask request latency",
    ["endpoint"]
)


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    endpoint = request.path
    method = request.method
    status = response.status_code

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - request.start_time)

    return response


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/api/users")
def get_users():
    return {"users": []}, 200


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
