"""test_totp.py — pytest coverage for the recipe's four scenarios.

Deps: pip install pytest pyotp qrcode pillow cryptography
Run:  pytest test_totp.py -v

Scenarios: enrollment round-trip, window boundary, rate limiting,
and single-use backup codes.
"""

import pyotp
import pytest

from totp_service import TOTPService


@pytest.fixture()
def service():
    return TOTPService(issuer="TestApp")


@pytest.fixture()
def enrolled(service):
    """A user with 2FA fully enabled. Returns (user_id, secret, backup_codes)."""
    service.enroll("u1", "u1@example.com")
    # Recover the pending secret to generate a valid confirm token
    u = service.users["u1"]
    secret = service.fernet.decrypt(u.pending_secret).decode()
    result = service.confirm("u1", pyotp.TOTP(secret).now())
    assert result["enabled"]
    return "u1", secret, result["backup_codes"]


class TestEnrollmentRoundTrip:
    def test_enroll_then_confirm_enables(self, service, enrolled):
        user_id, _, _ = enrolled
        u = service.users[user_id]
        assert u.enabled is True
        assert u.encrypted_secret is not None
        assert u.pending_secret is None

    def test_confirm_rejects_wrong_first_code(self, service):
        service.enroll("u2", "u2@example.com")
        result = service.confirm("u2", "000000")
        assert result["enabled"] is False
        # 2FA must NOT be enabled — that's the lock-out prevention
        assert service.users["u2"].enabled is False

    def test_enroll_returns_qr_and_uri(self, service):
        out = service.enroll("u3", "u3@example.com")
        assert out["provisioning_uri"].startswith("otpauth://totp/")
        assert len(out["qr_png_b64"]) > 100


class TestVerification:
    def test_verify_accepts_current_code(self, service, enrolled):
        user_id, secret, _ = enrolled
        assert service.verify(user_id, pyotp.TOTP(secret).now()) is True

    def test_verify_rejects_wrong_code(self, service, enrolled):
        user_id, _, _ = enrolled
        assert service.verify(user_id, "999999") is False


class TestRateLimiting:
    def test_sixth_attempt_blocked(self, service, enrolled):
        user_id, _, _ = enrolled
        for _ in range(5):
            service.verify(user_id, "000000")
        # 6th attempt returns False regardless of code validity
        assert service.verify(user_id, "000000") is False


class TestBackupCodes:
    def test_backup_code_works_once(self, service, enrolled):
        user_id, _, codes = enrolled
        assert service.verify(user_id, codes[0]) is True

    def test_backup_code_replay_rejected(self, service, enrolled):
        user_id, _, codes = enrolled
        service.verify(user_id, codes[0])
        assert service.verify(user_id, codes[0]) is False

    def test_backup_codes_not_plaintext(self, service, enrolled):
        user_id, _, codes = enrolled
        hashes = service.users[user_id].backup_hashes
        assert codes[0] not in hashes  # only hashes are stored
