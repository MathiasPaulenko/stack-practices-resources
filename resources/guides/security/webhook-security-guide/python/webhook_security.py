"""Webhook signing, verification, and replay protection — runnable demo.

Simulates a producer signing deliveries and a consumer verifying them,
including the attack cases: forged signature, stale timestamp, and replay.

Run: python webhook_security.py  (stdlib only)
"""
import hmac
import hashlib
import json
import time
import uuid

WEBHOOK_SECRET = "whsec_demo_secret"
MAX_AGE_SECONDS = 300  # 5 minutes


# ---------- Producer side ----------

def sign_delivery(payload: dict) -> tuple[bytes, dict]:
    """Serialize the payload and return (body, headers) for delivery."""
    body = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(
        WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    headers = {
        "X-Webhook-Signature": f"v1={signature}",
        "X-Webhook-ID": str(uuid.uuid4()),
        "X-Webhook-Timestamp": str(int(time.time())),
    }
    return body, headers


# ---------- Consumer side ----------

# In production this is Redis (SET key 1 NX EX ttl) or a DB unique index.
_processed_ids: set[str] = set()


def already_processed(webhook_id: str) -> bool:
    if webhook_id in _processed_ids:
        return True
    _processed_ids.add(webhook_id)
    return False


def verify_webhook(body: bytes, signature_header: str,
                   timestamp_header: str, webhook_id: str) -> bool:
    """True only if the webhook is authentic, fresh, and unseen."""
    if not signature_header.startswith("v1="):
        return False
    expected_sig = signature_header[3:]

    computed = hmac.new(
        WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(computed, expected_sig):
        return False

    if abs(time.time() - int(timestamp_header)) > MAX_AGE_SECONDS:
        return False

    return not already_processed(webhook_id)


# ---------- Demo ----------

if __name__ == "__main__":
    payload = {"type": "invoice.paid", "amount": 4900, "currency": "usd"}
    body, headers = sign_delivery(payload)

    # 1. Legitimate delivery → accepted
    ok = verify_webhook(body, headers["X-Webhook-Signature"],
                        headers["X-Webhook-Timestamp"], headers["X-Webhook-ID"])
    print("legitimate delivery:", "ACCEPTED" if ok else "REJECTED")

    # 2. Replay the exact same delivery → deduplicated
    ok = verify_webhook(body, headers["X-Webhook-Signature"],
                        headers["X-Webhook-Timestamp"], headers["X-Webhook-ID"])
    print("replayed delivery:  ", "ACCEPTED" if ok else "REJECTED (duplicate)")

    # 3. Forged signature → rejected
    ok = verify_webhook(body, "v1=" + "0" * 64,
                        headers["X-Webhook-Timestamp"], headers["X-Webhook-ID"])
    print("forged signature:   ", "ACCEPTED" if ok else "REJECTED")

    # 4. Stale timestamp → rejected (replay outside the window)
    ok = verify_webhook(body, headers["X-Webhook-Signature"],
                        str(int(time.time()) - 3600), headers["X-Webhook-ID"])
    print("stale timestamp:    ", "ACCEPTED" if ok else "REJECTED")
