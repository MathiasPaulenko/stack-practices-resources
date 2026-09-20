"""Tests for the Gatekeeper edge validator.

Run:  python -m pytest test_gatekeeper.py -v
"""
import time

from gatekeeper import Gatekeeper, Request, sign_jwt, JWT_SECRET


def valid_token():
    return sign_jwt({"sub": "user-1", "exp": time.time() + 3600}, JWT_SECRET)


def authed(path="/api/orders"):
    return Request(path, headers={"Authorization": f"Bearer {valid_token()}"})


def test_blocked_path_rejected_before_auth():
    # /admin is blocked even with a valid token — path check runs first.
    d = Gatekeeper().inspect(authed("/admin/panel"))
    assert not d.allowed
    assert d.status == 403
    assert d.code == "BLOCKED_PATH"


def test_injection_in_query_rejected():
    d = Gatekeeper().inspect(Request("/api/orders", query="id=1 or 1=1"))
    assert not d.allowed
    assert d.status == 400
    assert d.code == "INJECTION_DETECTED"


def test_rate_limit_kicks_in():
    gk = Gatekeeper(rate_limit=3)
    req = Request("/api/public/products", client_ip="10.0.0.9")
    assert all(gk.inspect(req).allowed for _ in range(3))
    d = gk.inspect(req)
    assert not d.allowed
    assert d.status == 429


def test_missing_token_rejected_on_protected_route():
    d = Gatekeeper().inspect(Request("/api/orders"))
    assert not d.allowed
    assert d.status == 401
    assert d.code == "AUTH_FAILED"


def test_expired_token_rejected():
    token = sign_jwt({"sub": "user-1", "exp": time.time() - 10}, JWT_SECRET)
    d = Gatekeeper().inspect(
        Request("/api/orders", headers={"Authorization": f"Bearer {token}"})
    )
    assert not d.allowed
    assert d.status == 401


def test_forged_signature_rejected():
    token = sign_jwt({"sub": "user-1", "exp": time.time() + 3600}, "wrong-secret")
    d = Gatekeeper().inspect(
        Request("/api/orders", headers={"Authorization": f"Bearer {token}"})
    )
    assert not d.allowed


def test_valid_token_passes_and_exposes_user():
    d = Gatekeeper().inspect(authed())
    assert d.allowed
    assert d.user["sub"] == "user-1"


def test_public_route_skips_auth_but_not_other_layers():
    gk = Gatekeeper()
    assert gk.inspect(Request("/api/public/products")).allowed
    # ...but injection screening still applies on public routes.
    assert not gk.inspect(
        Request("/api/public/products", query="q=';drop table users--")
    ).allowed
