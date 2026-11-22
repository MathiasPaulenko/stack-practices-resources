"""Synchronous REST call with timeout and exponential-backoff retries.

Companion to https://stackpractices.com/recipes/microservices-communication/
Requires: httpx, tenacity (see requirements.txt).
"""

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_order(order_id: str) -> dict:
    with httpx.Client(timeout=5.0) as client:
        r = client.get(f"http://orders-service/orders/{order_id}")
        r.raise_for_status()
        return r.json()


if __name__ == "__main__":
    import json
    import sys

    order_id = sys.argv[1] if len(sys.argv) > 1 else "ord_123"
    try:
        print(json.dumps(get_order(order_id), indent=2))
    except httpx.HTTPError as exc:
        print(f"orders-service unreachable: {exc}")
        sys.exit(1)
