import hashlib
import re

def mask_pii(data: dict) -> dict:
    """Enmascara campos sensibles para el logging."""
    sensitive_fields = ["email", "phone", "ssn", "creditCard"]
    masked = {}
    for key, value in data.items():
        if key in sensitive_fields:
            masked[key] = hash_value(str(value))
        else:
            masked[key] = value
    return masked

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]
