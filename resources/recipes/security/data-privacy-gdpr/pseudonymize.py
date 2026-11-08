"""HMAC-based pseudonymization for analytics data.

Pseudonymized data is still personal data under GDPR because the key can
reverse it — rotate PII_HMAC_KEY periodically so old analytics rows become
unlinkable to new ones.
"""

import hashlib
import hmac
import os
from datetime import datetime


def _key() -> bytes:
    # Load from env / secrets manager (KMS, Vault) — never hardcode. Rotate yearly.
    return os.environ["PII_HMAC_KEY"].encode()


def pseudonymize(user_id: str) -> str:
    """Replace PII with irreversible hash for analytics."""
    return hmac.new(_key(), user_id.encode(), hashlib.sha256).hexdigest()[:16]


def anonymize_age(birth_date: datetime) -> str:
    """Bucket age into ranges for statistical use."""
    age = (datetime.now() - birth_date).days // 365
    if age < 18:
        return "<18"
    if age < 25:
        return "18-24"
    if age < 35:
        return "25-34"
    return "35+"


if __name__ == "__main__":
    os.environ.setdefault("PII_HMAC_KEY", "dev-only-key-not-for-production")
    print(pseudonymize("user-123"))
    print(anonymize_age(datetime(1995, 6, 15)))
