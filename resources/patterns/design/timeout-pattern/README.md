# Timeout Pattern — Companion Files

Runnable implementations for the [Timeout Pattern](https://stackpractices.com/patterns/timeout-pattern/) guide.

## Files

| File | What it shows |
| --- | --- |
| `with_timeout.py` | Decorator enforcing a hard deadline on synchronous functions. |
| `deadline_budget.py` | Deadline propagation: each layer receives the *remaining* budget, with headroom left for the caller to react. |
| `test_timeouts.py` | pytest suite: fast calls pass, slow calls raise, budgets shrink down the chain, expired budgets fail fast. |

## Run

```bash
pip install pytest
pytest test_timeouts.py
```

## Notes

- `with_timeout` abandons the wait but can't kill the worker thread — pair it with socket-level timeouts (`requests.get(url, timeout=...)`, `statement_timeout`) so abandoned work dies on its own.
- The budget demo shows why outer timeouts must exceed the sum of inner ones: the difference is reaction time for retries and fallbacks.
