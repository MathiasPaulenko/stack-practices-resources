"""Smoke tests for the authentication building blocks.

Run with plain pytest. Redis is faked in-memory; cryptography generates a
throwaway RSA key pair per run.
"""
import fakeredis
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from jwt_service import JWTConfig, JWTService, AuthError
from token_rotation import TokenRotationManager
from abac_evaluator import ABACEvaluator, Permission, check_rbac
from mfa_service import MFAService


@pytest.fixture(scope="module")
def jwt_service():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    pub = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return JWTService(JWTConfig(private_key=priv, public_key=pub))


@pytest.fixture
def redis():
    return fakeredis.FakeStrictRedis(decode_responses=False)


def test_access_token_roundtrip(jwt_service):
    token = jwt_service.generate_access_token("u1", {"role": "admin"})
    payload = jwt_service.verify_token(token)
    assert payload["sub"] == "u1" and payload["role"] == "admin"


def test_refresh_rejected_as_access(jwt_service):
    token = jwt_service.generate_refresh_token("u1")
    with pytest.raises(AuthError):
        jwt_service.verify_token(token, expected_type="access")


def test_rotation_revokes_old_token(jwt_service, redis):
    mgr = TokenRotationManager(jwt_service, redis)
    old = jwt_service.generate_refresh_token("u1")
    new = mgr.refresh_tokens(old)
    assert new["access_token"] and new["refresh_token"] != old
    with pytest.raises(AuthError):
        mgr.refresh_tokens(old)


def test_revoke_all_kills_refresh(jwt_service, redis):
    mgr = TokenRotationManager(jwt_service, redis)
    token = jwt_service.generate_refresh_token("u1")
    mgr.revoke_all_tokens("u1")
    with pytest.raises(AuthError):
        mgr.refresh_tokens(token)


def test_rbac():
    assert check_rbac("editor", Permission.WRITE)
    assert not check_rbac("viewer", Permission.DELETE)


def test_abac_ownership():
    abac = ABACEvaluator()
    abac.add_policy({
        "effect": "allow", "actions": ["write"],
        "subject": {"role": "editor"},
        "resource": {"type": "article", "owner": "$subject.id"},
    })
    user = {"id": "u1", "role": "editor"}
    mine = {"type": "article", "owner": "u1"}
    theirs = {"type": "article", "owner": "u2"}
    assert abac.evaluate(user, mine, "write")
    assert not abac.evaluate(user, theirs, "write")


def test_backup_codes_single_use(redis):
    mfa = MFAService(db=None, redis=redis)
    (code,) = mfa.generate_backup_codes("u1", count=1)
    assert mfa.verify_backup_code("u1", code)
    assert not mfa.verify_backup_code("u1", code)
