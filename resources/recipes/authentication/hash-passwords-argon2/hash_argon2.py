"""Argon2id password hashing demo — hash, verify, and rehash-on-upgrade.

Companion to https://stackpractices.com/recipes/hash-passwords-argon2/
Run: python hash_argon2.py
"""

import time

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# RFC 9106 recommended profile: 64 MiB, 3 iterations, 4 lanes.
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4,
                    hash_len=32, salt_len=16)


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hash_str: str) -> bool:
    try:
        ph.verify(hash_str, password)
        return True
    except VerifyMismatchError:
        return False


def verify_and_rehash(password: str, hash_str: str) -> tuple[bool, str | None]:
    """Verify, then return a fresh hash when the stored parameters are stale."""
    try:
        ph.verify(hash_str, password)
        if ph.check_needs_rehash(hash_str):
            return True, ph.hash(password)
        return True, None
    except VerifyMismatchError:
        return False, None


if __name__ == "__main__":
    password = "correct horse battery staple"

    start = time.perf_counter()
    hashed = hash_password(password)
    elapsed_ms = (time.perf_counter() - start) * 1000

    print(f"Hash:    {hashed}")
    print(f"Time:    {elapsed_ms:.0f} ms (target: 250–500 ms on your hardware)")
    print(f"Valid:   {verify_password(password, hashed)}")
    print(f"Invalid: {verify_password('wrong', hashed)}")

    _, new_hash = verify_and_rehash(password, hashed)
    print(f"Rehash needed: {new_hash is not None}")
