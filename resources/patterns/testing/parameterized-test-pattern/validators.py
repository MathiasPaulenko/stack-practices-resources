"""Minimal validators used by the parameterized tests."""


def validate_email(email) -> bool:
    if not isinstance(email, str) or not email:
        return False
    local, at, domain = email.partition("@")
    if not at or not local or not domain:
        return False
    return "." in domain and not domain.startswith(".")
