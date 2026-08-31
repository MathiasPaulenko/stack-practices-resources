import time
from argon2 import PasswordHasher


def hash_password(password: str) -> str:
    ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=1)
    return ph.hash(password)


def verify_password(hashed: str, password: str) -> bool:
    ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=1)
    try:
        ph.verify(hashed, password)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    password = "supersecret"
    start = time.perf_counter()
    hashed = hash_password(password)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"Argon2id hash: {hashed}")
    print(f"hash time: {elapsed_ms:.2f} ms")
    print(f"verify: {verify_password(hashed, password)}")
