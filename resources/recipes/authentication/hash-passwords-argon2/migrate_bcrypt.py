"""Hybrid bcrypt → Argon2id migration demo.

Verify with the matching algorithm by hash prefix and transparently
upgrade bcrypt hashes on a successful login.

Companion to https://stackpractices.com/recipes/hash-passwords-argon2/
Run: python migrate_bcrypt.py
"""

import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)


def verify_password(password: str, hash_str: str) -> bool:
    if hash_str.startswith("$2"):  # bcrypt
        return bcrypt.checkpw(password.encode(), hash_str.encode())
    if hash_str.startswith("$argon2"):
        try:
            ph.verify(hash_str, password)
            return True
        except VerifyMismatchError:
            return False
    return False  # unknown format — fail closed


def login(stored_hash: str, password: str) -> tuple[bool, str]:
    """Returns (success, hash_to_store). Rehashes bcrypt on success."""
    if not verify_password(password, stored_hash):
        return False, stored_hash
    if stored_hash.startswith("$2"):
        return True, ph.hash(password)
    return True, stored_hash


if __name__ == "__main__":
    password = "correct horse battery staple"
    legacy = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

    ok, new_hash = login(legacy, password)
    print(f"Login: {ok}")
    print(f"Old:   {legacy[:31]}...")
    print(f"New:   {new_hash[:31]}...")
    assert new_hash.startswith("$argon2id$"), "bcrypt hash was not upgraded"
    assert verify_password(password, new_hash)
    print("bcrypt hash transparently upgraded to Argon2id")
