import hashlib
import hmac
import secrets
import time


def hash_password(password: bytes, iterations: int = 600_000) -> str:
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password, salt, iterations, dklen=32)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${key.hex()}"


def verify_password(stored: str, password: bytes) -> bool:
    _, iters, salt_hex, hash_hex = stored.split("$")
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password, salt, int(iters), dklen=len(expected)
    )
    return hmac.compare_digest(derived, expected)


if __name__ == "__main__":
    password = b"supersecret"
    start = time.perf_counter()
    stored = hash_password(password)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"PBKDF2 stored: {stored}")
    print(f"hash time: {elapsed_ms:.2f} ms")
    print(f"verify: {verify_password(stored, password)}")
