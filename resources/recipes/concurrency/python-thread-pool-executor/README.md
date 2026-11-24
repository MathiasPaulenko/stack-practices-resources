# ThreadPoolExecutor Patterns — Companion Code

Runnable patterns for parallel I/O work with `concurrent.futures`.

## Files

| File | What it shows |
|---|---|
| `thread_pool.py` | `collect_ordered` (map), `collect_as_completed` (submit + per-future errors), `ThreadSafeResults` (lock-guarded shared collector), `session()` (thread-local requests.Session), and a smoke test in `__main__` — sleep-based, no network. |

## Quick start

```bash
pip install -r requirements.txt
python thread_pool.py
# map: 8 results in 0.21s (~0.8s sequential)
# caught per-future: simulated API failure
```

## Source

- https://stackpractices.com/recipes/python-thread-pool-executor/
- https://stackpractices.com/es/recipes/python-thread-pool-executor/
