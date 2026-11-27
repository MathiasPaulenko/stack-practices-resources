# strangler_router.py — route requests based on feature flags
from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

LEGACY_URL = os.environ["LEGACY_URL"]
NEW_SERVICE_URL = os.environ["NEW_SERVICE_URL"]

# Routes that have been migrated to the new service
MIGRATED_ROUTES = {
    ("GET", "/api/customers"),
    ("GET", "/api/customers/<id>"),
    ("POST", "/api/customers"),
    ("PUT", "/api/customers/<id>"),
    ("DELETE", "/api/customers/<id>"),
    ("GET", "/api/orders"),
    ("POST", "/api/orders"),
}

# Percentage of traffic to route to new service (for canary testing)
CANARY_PERCENTAGE = 10

def is_migrated(method, path):
    """Check if a route has been fully migrated."""
    # Normalize path (remove trailing slashes, extract pattern)
    normalized = path.rstrip("/")
    for m, p in MIGRATED_ROUTES:
        if method == m and normalized.startswith(p.replace("<id>", "")):
            return True
    return False

def is_canary_eligible():
    """Determine if this request should go to the new service for canary."""
    import random
    return random.randint(1, 100) <= CANARY_PERCENTAGE

@app.route("/api/<path:route>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def strangler_route(route):
    method = request.method
    path = f"/api/{route}"

    target_url = None

    if is_migrated(method, path):
        target_url = NEW_SERVICE_URL
    elif is_canary_eligible():
        target_url = NEW_SERVICE_URL
    else:
        target_url = LEGACY_URL

    # Forward the request
    resp = requests.request(
        method=method,
        url=f"{target_url}{path}",
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        params=request.args,
        allow_redirects=False
    )

    # Add strangler header for observability
    response = Response(resp.content, resp.status_code, resp.headers.items())
    response.headers["X-Strangler-Target"] = "new" if target_url == NEW_SERVICE_URL else "legacy"
    return response
