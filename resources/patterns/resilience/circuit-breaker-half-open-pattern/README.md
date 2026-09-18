# Circuit Breaker Half-Open — Companion Code

Runnable version of the three-state breaker from the
[Circuit Breaker Half-Open Pattern](https://stackpractices.com/patterns/circuit-breaker-half-open-pattern/)
on StackPractices.

## Files

| File | Description |
|------|-------------|
| `circuit_breaker.py` | `CircuitBreaker` with `closed` / `open` / `half_open` states, thread-safe via `threading.Lock`, plus a `unittest` suite covering every transition path |

## Requirements

- Python 3.10+ — no external dependencies.

## Usage

```python
from circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

breaker = CircuitBreaker(
    failure_threshold=5,      # open after 5 consecutive failures
    recovery_timeout=30,      # seconds before half-open trials
    half_open_max_calls=3,    # trial request budget
    success_threshold=2,      # consecutive successes to close
)

try:
    result = breaker.call(downstream_api.get, "/status")
except CircuitBreakerOpenError:
    result = fallback_response()
```

## Notes

- The open → half-open transition is lazy: it happens inside `call()` when a
  request arrives after `recovery_timeout`, not on a timer.
- In half-open, one failure reopens the circuit; closing requires
  `success_threshold` consecutive successes — the asymmetry is deliberate.
- State is checked under the lock, but the wrapped call runs outside it, so a
  slow downstream service never serializes all callers.
