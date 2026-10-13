"""Structured security logging with alerting thresholds (A09 — Logging & Alerting)."""

import json
import logging
import time
from collections import defaultdict


class SecurityLogger:
    """Writes structured security events and trips alerts on suspicious rates."""

    def __init__(self, log_path: str = "security.log", alert_fn=None):
        self.logger = logging.getLogger("security")
        if not self.logger.handlers:
            handler = logging.FileHandler(log_path)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self._failed_logins: dict[str, list[float]] = defaultdict(list)
        self._alert_fn = alert_fn or (lambda msg: self.logger.critical(msg))

    def _emit(self, event: dict):
        self.logger.warning(json.dumps(event))

    def log_auth_event(self, event_type: str, user_id: str, ip: str, success: bool):
        """Log an auth event; alert if an IP piles up failed logins."""
        self._emit({
            "event": event_type,
            "user_id": user_id,
            "ip": ip,
            "success": success,
            "type": "authentication",
        })
        if not success:
            now = time.time()
            attempts = [t for t in self._failed_logins[ip] if now - t < 300]
            attempts.append(now)
            self._failed_logins[ip] = attempts
            if len(attempts) >= 5:
                self._alert_fn(f"Credential stuffing suspected from {ip}")

    def log_access_denied(self, user_id: str, resource: str, ip: str):
        """Log an authorization failure — page on admin-route denials."""
        self._emit({
            "event": "access_denied",
            "user_id": user_id,
            "resource": resource,
            "ip": ip,
            "type": "authorization",
        })
        if resource.startswith("/admin"):
            self._alert_fn(f"Admin route denied for {user_id} from {ip}")

    def log_security_event(self, event: str, details: dict):
        """Log a generic security event (injection attempt, WAF block, etc.)."""
        self._emit({"event": event, "details": details, "type": "security"})
