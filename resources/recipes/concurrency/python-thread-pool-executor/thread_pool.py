"""ThreadPoolExecutor patterns — runnable examples.

Covers submit/map/as_completed, per-future error handling, thread-safe
result collection, and thread-local sessions. __main__ runs a smoke test
with sleep-based tasks so no network access is needed.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_url(url: str, delay: float = 0.1) -> dict:
    """Simulated I/O-bound fetch — replace sleep with requests.get in prod."""
    time.sleep(delay)
    return {"url": url, "status": 200, "size": 1024}


def collect_ordered(urls: list, workers: int = 4) -> list:
    """map() — results in input order."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(fetch_url, urls))


def collect_as_completed(urls: list, workers: int = 4) -> list:
    """submit + as_completed — results in finish order, errors per future."""
    results, errors = [], []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(futures):
            try:
                results.append(future.result(timeout=5))
            except Exception as e:  # noqa: BLE001 — one bad task shouldn't kill the batch
                errors.append({"url": futures[future], "error": str(e)})
    return results, errors


class ThreadSafeResults:
    """Shared collector guarded by a lock — threads append safely."""

    def __init__(self):
        self._results, self._errors = [], []
        self._lock = threading.Lock()

    def add_result(self, item):
        with self._lock:
            self._results.append(item)

    def add_error(self, item):
        with self._lock:
            self._errors.append(item)

    @property
    def results(self):
        with self._lock:
            return list(self._results)


_thread_local = threading.local()


def session():
    """One requests.Session per worker thread — never shared across threads."""
    if not hasattr(_thread_local, "session"):
        import requests
        _thread_local.session = requests.Session()
    return _thread_local.session


if __name__ == "__main__":
    urls = [f"https://api.example.com/data/{i}" for i in range(8)]

    start = time.time()
    ordered = collect_ordered(urls)
    t_map = time.time() - start
    print(f"map: {len(ordered)} results in {t_map:.2f}s "
          f"(~{0.1 * len(urls):.1f}s sequential)")

    results, errors = collect_as_completed(urls)
    print(f"as_completed: {len(results)} results, {len(errors)} errors")

    storage = ThreadSafeResults()
    with ThreadPoolExecutor(max_workers=4) as ex:
        ex.map(lambda u: storage.add_result(fetch_url(u)), urls)
    print(f"thread-safe store: {len(storage.results)} items")

    # per-future error handling
    def boom(url):
        raise ValueError("simulated API failure")

    with ThreadPoolExecutor(max_workers=2) as ex:
        f = ex.submit(boom, urls[0])
        try:
            f.result()
        except ValueError as e:
            print(f"caught per-future: {e}")
