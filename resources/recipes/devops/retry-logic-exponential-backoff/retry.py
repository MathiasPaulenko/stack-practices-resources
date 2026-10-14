"""Configurable retry decorator with exponential backoff and jitter.

Companion code for https://stackpractices.com/recipes/retry-logic-exponential-backoff/

The `sleep` parameter is injectable so tests can record the computed delays
instead of actually sleeping.
"""

import random
import time
import uuid
from functools import wraps
from typing import Callable, Optional, Tuple, TypeVar

T = TypeVar("T")


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[type, ...] = (Exception,),
    jitter: bool = True,
    on_retry: Optional[Callable[[Exception, int, float], None]] = None,
    sleep: Callable[[float], None] = time.sleep,
):
    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    if jitter:
                        delay = random.uniform(0, delay)
                    if on_retry:
                        on_retry(e, attempt + 1, delay)
                    sleep(delay)
        return wrapper
    return decorator


# With idempotency key — generate it once, send it on every attempt
idempotency_key = str(uuid.uuid4())


@retry(max_retries=3, exceptions=(ConnectionError, TimeoutError))
def create_order(payload: dict) -> dict:
    import requests
    response = requests.post(
        "https://api.example.com/orders",
        json=payload,
        headers={"Idempotency-Key": idempotency_key},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Demo without network access: a function that fails twice, then succeeds.
    attempts = {"n": 0}

    @retry(max_retries=5, base_delay=0.1, jitter=True)
    def flaky() -> str:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ConnectionError(f"transient failure #{attempts['n']}")
        return "ok"

    print(flaky())          # -> ok
    print(attempts["n"])    # -> 3
