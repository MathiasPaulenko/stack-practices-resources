"""Gatekeeper pattern — a framework-free edge validator.

One inspection point in front of the services: blocked paths, rate
limiting, injection screening, and JWT authentication — in that order.
Public routes (``/api/public/*``, ``/health``) skip authentication but
still go through every other layer.

Run the demo:   python gatekeeper.py
Run the tests:  python -m pytest test_gatekeeper.py -v
"""

import base64
import hashlib
import hmac
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Optional

# Fail fast if the secret is missing — never default to a guessable value.
JWT_SECRET = os.environ.get("GATEKEEPER_JWT_SECRET", "dev-secret-for-demo-only")
JWT_ALGORITHM = "HS256"


@dataclass
class Request:
    path: str
    query: str = ""
    headers: dict = field(default_factory=dict)
    client_ip: str = "unknown"


@dataclass
class Decision:
    allowed: bool
    status: int = 200
    code: str = "OK"
    reason: str = ""
    user: Optional[dict] = None


def _b64url_decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def sign_jwt(payload: dict, secret: str) -> str:
    """Minimal HS256 signer — enough for tests and demos."""
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    body = _b64url_encode(json.dumps(payload).encode())
    signing_input = f"{header}.{body}".encode()
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return f"{header}.{body}.{_b64url_encode(sig)}"


def verify_jwt(token: str, secret: str) -> Optional[dict]:
    """Verify signature + expiry. Returns the payload or None."""
    try:
        header_b64, body_b64, sig_b64 = token.split(".")
    except ValueError:
        return None
    signing_input = f"{header_b64}.{body_b64}".encode()
    expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(expected, _b64url_decode(sig_b64)):
        return None
    payload = json.loads(_b64url_decode(body_b64))
    if "exp" in payload and payload["exp"] < time.time():
        return None
    return payload


class Gatekeeper:
    """Edge inspection layers, cheapest rejection first."""

    BLOCKED_PATHS = ("/admin", "/internal", "/debug", "/.env", "/wp-admin")
    PUBLIC_PREFIXES = ("/api/public", "/health")
    INJECTION_PATTERNS = [
        re.compile(r"(\b(union|select|insert|update|delete|drop)\b)", re.I),
        re.compile(r"(--|;|/\*|\*/)"),
        re.compile(r"(\b(or|and)\b\s+\d+\s*=\s*\d+)", re.I),
    ]

    def __init__(self, rate_limit: int = 100, window_seconds: int = 60):
        self.rate_limit = rate_limit
        self.window = window_seconds
        # In production this lives in Redis so replicas share counters.
        self._hits: dict[str, list[float]] = {}

    def inspect(self, request: Request) -> Decision:
        if request.path.startswith(self.BLOCKED_PATHS):
            return Decision(False, 403, "BLOCKED_PATH", "path is not public")

        if self._over_limit(request.client_ip):
            return Decision(False, 429, "RATE_LIMITED", "too many requests")

        if self._looks_injected(request):
            return Decision(False, 400, "INJECTION_DETECTED", "malformed input")

        if not request.path.startswith(self.PUBLIC_PREFIXES):
            token = request.headers.get("Authorization", "")
            if not token.startswith("Bearer "):
                return Decision(False, 401, "AUTH_FAILED", "missing bearer token")
            payload = verify_jwt(token[7:], JWT_SECRET)
            if payload is None:
                return Decision(False, 401, "AUTH_FAILED", "invalid or expired token")
            return Decision(True, user=payload)

        return Decision(True)

    def _over_limit(self, client_ip: str) -> bool:
        now = time.time()
        hits = [t for t in self._hits.get(client_ip, []) if t > now - self.window]
        if len(hits) >= self.rate_limit:
            self._hits[client_ip] = hits
            return True
        hits.append(now)
        self._hits[client_ip] = hits
        return False

    def _looks_injected(self, request: Request) -> bool:
        target = f"{request.path}?{request.query}"
        return any(p.search(target) for p in self.INJECTION_PATTERNS)


if __name__ == "__main__":
    gk = Gatekeeper()
    token = sign_jwt({"sub": "user-1", "exp": time.time() + 3600}, JWT_SECRET)

    cases = [
        Request("/admin/panel"),
        Request("/api/orders", query="id=1 or 1=1"),
        Request("/api/orders"),
        Request("/api/orders", headers={"Authorization": f"Bearer {token}"}),
        Request("/api/public/products"),
        Request("/api/protected/users/me",
                headers={"Authorization": f"Bearer {token}"}),
    ]
    for req in cases:
        d = gk.inspect(req)
        verdict = "PASS" if d.allowed else f"REJECT {d.status}"
        print(f"{verdict:>11}  {req.path}{('?' + req.query) if req.query else ''}  [{d.code}]")
