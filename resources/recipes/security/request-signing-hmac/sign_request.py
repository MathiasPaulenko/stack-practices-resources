"""HMAC-SHA256 request signing — client and server sides."""
import hashlib
import hmac
from datetime import datetime, timezone

SIGNATURE_HEADER = "X-Request-Signature"
TIMESTAMP_HEADER = "X-Request-Timestamp"


def sign_request(secret: str, method: str, path: str, body: str = "") -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    message = f"{method}\n{path}\n{timestamp}\n{body}"
    signature = hmac.new(
        secret.encode(), message.encode(), hashlib.sha256
    ).hexdigest()
    return {TIMESTAMP_HEADER: timestamp, SIGNATURE_HEADER: signature}


def verify_request(
    secret: str, headers: dict, method: str, path: str, body: str = ""
) -> bool:
    signature = headers.get(SIGNATURE_HEADER) or headers.get(
        SIGNATURE_HEADER.lower()
    )
    timestamp = headers.get(TIMESTAMP_HEADER) or headers.get(
        TIMESTAMP_HEADER.lower()
    )
    if not signature or not timestamp:
        return False

    message = f"{method}\n{path}\n{timestamp}\n{body}"
    expected = hmac.new(
        secret.encode(), message.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


if __name__ == "__main__":
    # Round-trip demo: sign then verify
    headers = sign_request("my-secret-key", "POST", "/api/orders", '{"item": "book"}')
    ok = verify_request(
        "my-secret-key", headers, "POST", "/api/orders", '{"item": "book"}'
    )
    print("signature verifies:", ok)
