import httpx
import uuid

def charge_payment(order_id: str, amount: int, idempotency_key: str | None = None):
    key = idempotency_key or str(uuid.uuid4())
    response = httpx.post(
        "http://payment-service:8000/payments",
        json={"order_id": order_id, "amount": amount},
        headers={"Idempotency-Key": key},
        timeout=httpx.Timeout(5.0, connect=2.0),
    )
    response.raise_for_status()
    return response.json()
