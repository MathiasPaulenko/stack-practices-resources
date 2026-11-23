"""Password hashing with Argon2id (with pepper) and transparent bcrypt migration."""
import hashlib
import os
import re

import argon2
import bcrypt

PEPPER = os.environ.get("PASSWORD_PEPPER", "local-dev-pepper")

ph = argon2.PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)


def hash_argon2id(password: str) -> str:
    """Hash a password with Argon2id plus a server-side pepper."""
    return ph.hash(password + PEPPER)


def verify_argon2id(password: str, stored_hash: str) -> bool:
    try:
        ph.verify(stored_hash, password + PEPPER)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False


def is_legacy_hash(stored_hash: str) -> bool:
    """MD5 = 32 hex chars, SHA-256 = 64 hex chars."""
    return bool(re.match(r"^[a-f0-9]{32}$", stored_hash) or
                re.match(r"^[a-f0-9]{64}$", stored_hash))


def verify_and_migrate(password: str, stored_hash: str):
    """Return (is_valid, new_hash_or_none). Migrates legacy hashes to bcrypt."""
    if stored_hash.startswith(("$2b$", "$2a$")):
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            if int(stored_hash.split("$")[2]) < 12:
                return True, bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
            return True, None
        return False, None

    if is_legacy_hash(stored_hash):
        md5 = hashlib.md5(password.encode()).hexdigest()
        sha256 = hashlib.sha256(password.encode()).hexdigest()
        if md5 == stored_hash or sha256 == stored_hash:
            return True, bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
        return False, None

    return False, None


if __name__ == "__main__":
    h = hash_argon2id("correct horse battery staple")
    print("argon2id verify:", verify_argon2id("correct horse battery staple", h))
    print("argon2id wrong :", verify_argon2id("wrong password", h))

    legacy = hashlib.md5(b"hunter2").hexdigest()
    valid, new_hash = verify_and_migrate("hunter2", legacy)
    print("md5 migrate    :", valid, "->", new_hash[:12] + "...")
    valid2, _ = verify_and_migrate("hunter2", new_hash)
    print("bcrypt verify  :", valid2)
