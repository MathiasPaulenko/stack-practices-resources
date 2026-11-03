"""TOTP MFA with hashed backup codes and pending-challenge login flow.

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
import hashlib
import secrets
import pyotp
from jwt_service import JWTService, AuthError


class MFAService:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis

    def generate_totp_secret(self) -> str:
        return pyotp.random_base32()

    def get_totp_uri(self, secret: str, email: str,
                     issuer: str = "ExampleApp") -> str:
        return pyotp.TOTP(secret).provisioning_uri(
            name=email, issuer_name=issuer
        )

    def verify_totp(self, secret: str, code: str) -> bool:
        return pyotp.TOTP(secret).verify(code, valid_window=1)

    def generate_backup_codes(self, user_id: str, count: int = 10) -> list:
        codes = [secrets.token_hex(4).upper() for _ in range(count)]
        hashes = [hashlib.sha256(c.encode()).hexdigest() for c in codes]
        self.redis.sadd(f"backup_hashes:{user_id}", *hashes)
        return codes

    def verify_backup_code(self, user_id: str, code: str) -> bool:
        digest = hashlib.sha256(code.encode()).hexdigest()
        return self.redis.srem(f"backup_hashes:{user_id}", digest) == 1

    def send_sms_code(self, phone: str):
        code = f"{secrets.randbelow(1000000):06d}"
        self.redis.setex(f"sms_code:{phone}", 300, code)

    def verify_sms_code(self, phone: str, code: str) -> bool:
        stored = self.redis.get(f"sms_code:{phone}")
        if stored and stored.decode() == code:
            self.redis.delete(f"sms_code:{phone}")
            return True
        return False


class MFAAuthFlow:
    def __init__(self, mfa_service: MFAService, jwt_service: JWTService, redis):
        self.mfa = mfa_service
        self.jwt = jwt_service
        self.redis = redis

    def step1_verify_password(self, user) -> dict:
        """`user` is your ORM object after a successful password check."""
        if user.mfa_enabled:
            challenge = secrets.token_urlsafe(32)
            self.redis.setex(f"mfa_challenge:{challenge}", 300, user.id)
            return {
                "requires_mfa": True,
                "challenge": challenge,
                "methods": ["totp", "sms", "backup_code"],
            }
        return self._generate_tokens(user.id)

    def step2_verify_mfa(self, user, challenge: str,
                         method: str, code: str) -> dict:
        user_id = self.redis.get(f"mfa_challenge:{challenge}")
        if not user_id or user_id.decode() != str(user.id):
            raise AuthError("Invalid or expired challenge")

        ok = {
            "totp": lambda: self.mfa.verify_totp(user.totp_secret, code),
            "sms": lambda: self.mfa.verify_sms_code(user.phone, code),
            "backup_code": lambda: self.mfa.verify_backup_code(user.id, code),
        }.get(method, lambda: False)()
        if not ok:
            raise AuthError(f"Invalid {method} code")

        self.redis.delete(f"mfa_challenge:{challenge}")
        return self._generate_tokens(user.id)

    def _generate_tokens(self, user_id: str) -> dict:
        return {
            "requires_mfa": False,
            "access_token": self.jwt.generate_access_token(user_id, {}),
            "refresh_token": self.jwt.generate_refresh_token(user_id),
            "expires_in": self.jwt.config.access_token_ttl,
        }
