"""totp_service.py — TOTP enrollment + verification service (Python).

Covers the three server-side pieces from the recipe:
  - enroll()    → secret + provisioning URI + QR (data-url)
  - confirm()   → verify first code before marking 2FA enabled
  - verify()    → login-time check with attempt rate limiting
  - backup codes → generated at enrollment, stored hashed, single-use

Deps: pip install pyotp qrcode pillow

Secrets are encrypted at rest with Fernet (AES-128-CBC + HMAC; swap for
AES-256-GCM or your KMS in production). The encryption key comes from the
environment — never from the database.
"""

import base64
import hashlib
import io
import os
import secrets
import time
from collections import defaultdict
from dataclasses import dataclass, field

import pyotp
import qrcode
from cryptography.fernet import Fernet


@dataclass
class UserTOTP:
    encrypted_secret: bytes | None = None
    enabled: bool = False
    pending_secret: bytes | None = None  # set at enroll, moved to encrypted_secret at confirm
    backup_hashes: set = field(default_factory=set)
    attempts: list = field(default_factory=list)


class TOTPService:
    MAX_ATTEMPTS = 5
    ATTEMPT_WINDOW_SEC = 300  # 5 tries per 5 minutes

    def __init__(self, issuer: str = "MyApp"):
        self.issuer = issuer
        key = os.environ.get("TOTP_ENCRYPTION_KEY")
        if not key:
            # Demo only — in production this MUST come from KMS/vault/env
            key = Fernet.generate_key().decode()
        self.fernet = Fernet(key.encode())
        self.users: dict = defaultdict(UserTOTP)

    # ---------- enrollment ----------

    def enroll(self, user_id: str, email: str) -> dict:
        """Step 1: generate secret + QR. Does NOT enable 2FA yet."""
        secret = pyotp.random_base32()
        uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=self.issuer)
        img = qrcode.make(uri)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_b64 = base64.b64encode(buf.getvalue()).decode()

        u = self.users[user_id]
        u.pending_secret = self.fernet.encrypt(secret.encode())
        return {"provisioning_uri": uri, "qr_png_b64": qr_b64}

    def confirm(self, user_id: str, token: str) -> dict:
        """Step 2: verify the first code, then enable + issue backup codes."""
        u = self.users[user_id]
        if not u.pending_secret:
            raise ValueError("no pending enrollment")
        secret = self.fernet.decrypt(u.pending_secret).decode()
        if not pyotp.TOTP(secret).verify(token, valid_window=1):
            return {"enabled": False}

        u.encrypted_secret = u.pending_secret
        u.pending_secret = None
        u.enabled = True
        codes = [secrets.token_hex(4).upper() for _ in range(10)]
        u.backup_hashes = {self._hash_code(c) for c in codes}
        return {"enabled": True, "backup_codes": codes}  # show ONCE, then discard

    # ---------- verification ----------

    def verify(self, user_id: str, token: str) -> bool:
        """Login-time check. Rate-limited; backup codes are single-use."""
        u = self.users[user_id]
        if not u.enabled:
            raise ValueError("2FA not enabled")

        now = time.time()
        u.attempts = [t for t in u.attempts if now - t < self.ATTEMPT_WINDOW_SEC]
        if len(u.attempts) >= self.MAX_ATTEMPTS:
            return False  # 429 in the endpoint layer
        u.attempts.append(now)

        # Backup codes work like a token but burn on use
        if self._hash_code(token.strip().upper()) in u.backup_hashes:
            u.backup_hashes.discard(self._hash_code(token.strip().upper()))
            return True

        secret = self.fernet.decrypt(u.encrypted_secret).decode()
        return pyotp.TOTP(secret).verify(token, valid_window=1)

    def disable(self, user_id: str) -> None:
        """Requires re-auth upstream; here we just clear the state."""
        self.users[user_id] = UserTOTP()

    @staticmethod
    def _hash_code(code: str) -> str:
        return hashlib.sha256(code.encode()).hexdigest()
