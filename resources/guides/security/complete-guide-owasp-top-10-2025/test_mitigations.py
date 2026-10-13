"""Tests for the OWASP Top 10 2025 companion mitigations. Run: pytest test_mitigations.py"""

import pytest

from access_control import AccessDenied, require_ownership, require_role
from fail_closed import InsufficientFunds, TransferError, transfer_funds
from security_logging import SecurityLogger
from ssrf_protection import SSRFProtector


class TestSSRF:
    protector = SSRFProtector()

    @pytest.mark.parametrize("url", [
        "file:///etc/passwd",
        "gopher://internal",
        "http://169.254.169.254/latest/meta-data/",
        "http://127.0.0.1:8080/admin",
        "http://10.0.0.1/internal",
        "http://192.168.1.1/",
        "http://example.com:22/",
        "notaurl",
        "http://nonexistent.invalid/",
    ])
    def test_blocked(self, url):
        assert self.protector.validate_url(url) is False

    def test_public_url_allowed(self):
        assert self.protector.validate_url("https://stackpractices.com/") is True


class TestAccessControl:
    get_user = staticmethod(lambda user_id: user_id)

    def test_owner_allowed(self):
        fn = require_ownership(self.get_user)(lambda u, user_id: "ok")
        assert fn({"id": 7, "role": "user"}, user_id=7) == "ok"

    def test_non_owner_denied(self):
        fn = require_ownership(self.get_user)(lambda u, user_id: "ok")
        with pytest.raises(AccessDenied):
            fn({"id": 7, "role": "user"}, user_id=9)

    def test_admin_bypasses_ownership(self):
        fn = require_ownership(self.get_user)(lambda u, user_id: "ok")
        assert fn({"id": 7, "role": "admin"}, user_id=9) == "ok"

    def test_role_required(self):
        fn = require_role("admin")(lambda u: "ok")
        with pytest.raises(AccessDenied):
            fn({"id": 1, "role": "user"})
        assert fn({"id": 1, "role": "admin"}) == "ok"


class TestFailClosed:
    def accounts(self):
        return {"a": {"balance": 100.0}, "b": {"balance": 50.0}}

    def test_successful_transfer(self):
        accs = self.accounts()
        assert transfer_funds(accs, "a", "b", 30.0) == {"status": "ok"}
        assert accs["a"]["balance"] == 70.0
        assert accs["b"]["balance"] == 80.0

    def test_insufficient_funds_rolls_back(self):
        accs = self.accounts()
        with pytest.raises(InsufficientFunds):
            transfer_funds(accs, "a", "b", 150.0)
        assert accs == self.accounts()

    def test_missing_receiver_rolls_back_debit(self):
        accs = self.accounts()
        with pytest.raises(TransferError):
            transfer_funds(accs, "a", "ghost", 10.0)
        assert accs["a"]["balance"] == 100.0


class TestSecurityLogging:
    def test_failed_login_threshold_alerts(self, tmp_path):
        alerts = []
        log = SecurityLogger(log_path=str(tmp_path / "s.log"), alert_fn=alerts.append)
        for _ in range(5):
            log.log_auth_event("login_failed", "x", "1.2.3.4", False)
        assert alerts and "1.2.3.4" in alerts[0]

    def test_admin_denial_alerts(self, tmp_path):
        alerts = []
        log = SecurityLogger(log_path=str(tmp_path / "s.log"), alert_fn=alerts.append)
        log.log_access_denied("u1", "/admin/panel", "5.6.7.8")
        log.log_access_denied("u1", "/api/data", "5.6.7.8")
        assert len(alerts) == 1
