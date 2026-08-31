from prometheus_client import Counter, Histogram, generate_latest
from flask import Flask, request
import time

app = Flask(__name__)

http_requests = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'route', 'status_code']
)

http_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'route'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

@app.before_request
def before():
    request.start_time = time.time()

@app.after_request
def after(response):
    route = request.endpoint or 'unknown'
    http_requests.labels(request.method, route, response.status_code).inc()
    http_duration.labels(request.method, route).observe(time.time() - request.start_time)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200

@app.route('/')
def hello():
    return 'Hello, Prometheus!'

if __name__ == '__main__':
    app.run(port=8080)
