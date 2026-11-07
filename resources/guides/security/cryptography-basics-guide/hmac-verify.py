"""HMAC-SHA256 signing and verification — webhook payloads, signed URLs.

Never build a keyed hash as SHA-256(secret + msg): it is vulnerable to
length-extension. HMAC is designed for this.

Run: python hmac-verify.py  (stdlib only)
"""
import hashlib
import hmac
import os


def sign(secret: bytes, message: bytes) -> str:
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def verify(secret: bytes, message: bytes, signature_hex: str) -> bool:
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()
    # Constant-time compare — == leaks via timing on some platforms
    return hmac.compare_digest(expected, signature_hex)


if __name__ == "__main__":
    secret = os.urandom(32)
    payload = b'{"event": "payment.completed", "id": "evt_123"}'
    sig = sign(secret, payload)
    print("signature:", sig[:32], "...")
    print("valid:", verify(secret, payload, sig))
    print("tampered:", verify(secret, payload + b"!", sig))
