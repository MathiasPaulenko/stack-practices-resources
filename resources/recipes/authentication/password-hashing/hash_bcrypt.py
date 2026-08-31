import bcrypt
import time


def hash_password(password: bytes) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt)


def verify_password(password: bytes, hashed: bytes) -> bool:
    return bcrypt.checkpw(password, hashed)


if __name__ == "__main__":
    password = b"supersecret"
    start = time.perf_counter()
    hashed = hash_password(password)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"bcrypt hash: {hashed.decode()}")
    print(f"hash time: {elapsed_ms:.2f} ms")
    print(f"verify: {verify_password(password, hashed)}")
