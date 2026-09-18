"""flask.py — Flask before/after request hooks that emit Deprecation /
Sunset / Link headers on responses from deprecated endpoints.
Register on your app: app.before_request(add_deprecation_headers),
app.after_request(set_deprecation_headers)."""

from datetime import datetime
from flask import Flask, request, g

app = Flask(__name__)

DEPRECATED_PATHS = {
    "/v1/orders": {"sunset": "2026-10-01", "replacement": "/v2/orders"},
    "/v1/products": {"sunset": "2026-10-01", "replacement": "/v2/products"},
}


@app.before_request
def add_deprecation_headers():
    for path, info in DEPRECATED_PATHS.items():
        if request.path.startswith(path):
            g.deprecation_sunset = info["sunset"]
            g.deprecation_replacement = info["replacement"]
            break


@app.after_request
def set_deprecation_headers(response):
    if hasattr(g, "deprecation_sunset"):
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = datetime.strptime(
            g.deprecation_sunset, "%Y-%m-%d"
        ).strftime("%a, %d %b %Y 00:00:00 GMT")
        response.headers["Link"] = (
            '<https://docs.example.com/api-migration>; rel="deprecation"'
        )
    return response
