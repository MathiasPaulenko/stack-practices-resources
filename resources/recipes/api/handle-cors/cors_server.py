"""Runnable CORS middleware example for the "Handle CORS" recipe.

Usage:
    pip install -r requirements.txt
    python cors_server.py            # starts a Flask API on :5000

Then verify the headers from another terminal:

    bash verify-cors.sh http://localhost:5000

or manually:

    curl -i -X OPTIONS http://localhost:5000/api/users \\
        -H "Origin: https://app.example.com" \\
        -H "Access-Control-Request-Method: PUT"
"""

from flask import Flask, request, make_response

app = Flask(__name__)

ALLOWED_ORIGINS = {
    "https://app.example.com",
    "https://admin.example.com",
    "http://localhost:3000",
}
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
ALLOWED_HEADERS = ["Content-Type", "Authorization", "X-Request-ID"]
ALLOW_CREDENTIALS = True


@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")

    # Only reflect allowed origins; never use "*" with credentials
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"

    if ALLOW_CREDENTIALS:
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response


@app.route("/api/<path:path>", methods=["OPTIONS"])
def handle_preflight(path):
    origin = request.headers.get("Origin")
    if origin not in ALLOWED_ORIGINS:
        return make_response(("", 204))  # No CORS headers for disallowed origins

    response = make_response(("", 204))
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = ", ".join(ALLOWED_METHODS)
    response.headers["Access-Control-Allow-Headers"] = ", ".join(ALLOWED_HEADERS)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response


@app.route("/api/users", methods=["GET", "PUT"])
def users():
    return {"users": [{"id": 1, "name": "Alice"}]}


if __name__ == "__main__":
    app.run(port=5000)
