"""Timeout decorator for synchronous functions.

Raises TimeoutError when the wrapped call exceeds the deadline. Note the
limitation documented in the guide: the underlying worker thread keeps
running after the timeout fires — pair this with socket-level timeouts on
the I/O itself for real cleanup.
"""

import functools
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout


def with_timeout(seconds: float):
    """Wrap a callable with a hard execution deadline."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except FutureTimeout:
                    raise TimeoutError(f"Operation timed out after {seconds}s")

        return wrapper

    return decorator


@with_timeout(seconds=2.0)
def fetch_slow_data():
    import time

    time.sleep(5)
    return "data"


if __name__ == "__main__":
    try:
        print(fetch_slow_data())
    except TimeoutError as e:
        print(f"Failed: {e}")
