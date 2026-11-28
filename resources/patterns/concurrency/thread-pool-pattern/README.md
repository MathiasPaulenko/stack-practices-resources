# Thread Pool Pattern — Companion

Runnable Python examples for the Thread Pool pattern article: fixed pool with `submit`/`as_completed`, `executor.map`, per-future error handling, and Goetz's pool-sizing formula. All tasks are simulated I/O (sleep-based) — nothing touches the network.

## Files

- `thread_pool_examples.py` — the examples from the article, runnable standalone.
- `test_thread_pool.py` — pytest tests for the examples.
- `requirements.txt` — test dependency.

## Run

```bash
pip install -r requirements.txt
python thread_pool_examples.py   # prints results per task
pytest test_thread_pool.py       # 3 tests
```

Source article: https://stackpractices.com/patterns/thread-pool-pattern/
