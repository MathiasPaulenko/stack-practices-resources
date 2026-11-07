"""Password hashing with Argon2id and bcrypt.

Argon2id is the current OWASP recommendation (RFC 9106); bcrypt with cost >= 12
remains a solid, widely supported fallback.

Run: pip install argon2-cffi bcrypt && python password-hashing.py
"""
from argon2 import PasswordHasher
import bcrypt


def hash_argon2id(password: str) -> str:
    # OWASP parameters: m=19 MiB, t=2 iterations, p=1
    return PasswordHasher(memory_cost=19456, time_cost=2, parallelism=1).hash(password)


def verify_argon2id(password: str, hashed: str) -> bool:
    try:
        return PasswordHasher().verify(hashed, password)
    except Exception:
        return False


def hash_bcrypt(password: str, rounds: int = 12) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=rounds)).decode()


def verify_bcrypt(password: str, hashed: str) -> bool:
    # checkpw is constant-time — do not use == on hashes
    return bcrypt.checkpw(password.encode(), hashed.encode())


if __name__ == "__main__":
    pw = "correct horse battery staple"
    a = hash_argon2id(pw)
    print("argon2id ok:", verify_argon2id(pw, a), "| wrong pw:", verify_argon2id("nope", a))
    b = hash_bcrypt(pw)
    print("bcrypt   ok:", verify_bcrypt(pw, b), "| wrong pw:", verify_bcrypt("nope", b))
