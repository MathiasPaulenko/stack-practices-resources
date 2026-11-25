"""Context-aware retry with a hard deadline.

The retry loop stops early when the caller's budget of wall-clock
time runs out — and it never sleeps past the deadline.
"""

import random
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Type

import requests


@dataclass
class RetryConfig:
    max_attempts: int = 5
    base_delay: float = 1.0
    max_delay: float = 60.0
    deadline: Optional[float] = None  # seconds from start
    retryable_exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError)


def retry_with_deadline(config: RetryConfig):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            last_error = None

            for attempt in range(1, config.max_attempts + 1):
                if config.deadline:
                    elapsed = time.monotonic() - start_time
                    if elapsed >= config.deadline:
                        raise TimeoutError(
                            f"Retry deadline exceeded after {elapsed:.1f}s "
                            f"(attempt {attempt}/{config.max_attempts})"
                        )

                try:
                    return func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_error = e
                    if attempt == config.max_attempts:
                        raise

                    delay = min(
                        config.base_delay * (2 ** (attempt - 1)),
                        config.max_delay,
                    )
                    if config.deadline:
                        remaining = config.deadline - (time.monotonic() - start_time)
                        delay = min(delay, remaining * 0.5)

                    time.sleep(random.uniform(0, delay))

            raise last_error

        return wrapper

    return decorator


if __name__ == "__main__":

    @retry_with_deadline(
        RetryConfig(
            max_attempts=5,
            base_delay=0.5,
            max_delay=30,
            deadline=10.0,
            retryable_exceptions=(ConnectionError, TimeoutError, requests.HTTPError),
        )
    )
    def fetch_with_deadline(url: str):
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    print(fetch_with_deadline("https://httpbin.org/status/200"))
