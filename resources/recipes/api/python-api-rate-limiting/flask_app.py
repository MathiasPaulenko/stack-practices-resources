"""Runnable Flask example: per-IP token bucket with Retry-After header."""
import time
from collections import defaultdict
from functools import wraps

from flask import Flask, jsonify, request

from token_bucket import TokenBucket

app = Flask(__name__)

buckets: dict[str, TokenBucket] = defaultdict(lambda: TokenBucket(capacity=10, refill_rate=1.0))


def rate_limit(capacity: int = 10, refill_rate: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            bucket = buckets[request.remote_addr]
            if not bucket.consume():
                response = jsonify({"error": "Rate limit exceeded"})
                response.status_code = 429
                response.headers["Retry-After"] = str(max(1, round(1 / refill_rate)))
                return response
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/api/data")
@rate_limit(capacity=10, refill_rate=1.0)
def get_data():
    return jsonify({"data": "success"})


if __name__ == "__main__":
    app.run(debug=True)
