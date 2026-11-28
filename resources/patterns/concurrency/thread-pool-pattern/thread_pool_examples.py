"""Thread pool examples: submit/as_completed, bounded queue, fake I/O workload.

Everything runs locally — tasks sleep instead of hitting the network.
Run: python thread_pool_examples.py  (or: python -m doctest -v thread_pool_examples.py)
"""
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def fake_fetch(url: str) -> dict:
    """Simulates an I/O-bound task without touching the network."""
    time.sleep(random.uniform(0.05, 0.2))
    if "fail" in url:
        raise RuntimeError(f"simulated failure for {url}")
    return {"url": url, "status": 200, "length": random.randint(100, 9999)}


def run_fixed_pool() -> list:
    """Fixed pool: N workers, tasks queue up when all are busy."""
    urls = [f"https://example.local/item/{i}" for i in range(6)] + [
        "https://example.local/fail/1"
    ]
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fake_fetch, u): u for u in urls}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"url": futures[future], "error": str(e)})
    return results


def run_map() -> list:
    """map() preserves submission order and returns results, not futures."""
    urls = [f"https://example.local/page/{i}" for i in range(5)]
    with ThreadPoolExecutor(max_workers=2) as executor:
        return list(executor.map(fake_fetch, urls))


def sizing_example() -> int:
    """Goetz's formula: N * U * (1 + W/C). I/O task, 4 cores, 50% util, W/C=9."""
    import os
    cores = os.cpu_count() or 4
    utilization = 0.5
    wait_over_compute = 9
    return int(cores * utilization * (1 + wait_over_compute))


if __name__ == "__main__":
    t0 = time.time()
    results = run_fixed_pool()
    elapsed = time.time() - t0
    ok = sum(1 for r in results if r.get("status") == 200)
    print(f"fixed pool: {ok} ok, {len(results) - ok} failed in {elapsed:.2f}s")
    for r in results:
        print(" ", r)
    print("map:", [r["status"] for r in run_map()])
    print("suggested pool size (I/O):", sizing_example())
