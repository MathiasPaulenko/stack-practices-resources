# Ambassador Pattern — Companion Examples

Runnable examples for the [Ambassador pattern](https://stackpractices.com/patterns/ambassador-pattern-services/): a local proxy that owns the resilience policies — retries, timeouts, circuit breaking, metrics — so clients stay thin.

No external services needed. The "remote" is a fake callable; the ambassador wraps it with the same semantics you'd put around a real HTTP or gRPC client.

## What's inside

| File | Purpose |
| --- | --- |
| `ambassador.py` / `ambassador.js` | `ServiceAmbassador` (retry + timeout + half-open circuit breaker) and `MonitoringAmbassador` (composable metrics layer) |
| `test_ambassador.py` | pytest suite (8 tests) |
| `ambassador.test.js` | `node:test` suite (8 tests) |

## Concepts covered

- **Transparent wrapper** — the client calls `call()`; resilience is invisible.
- **Real exponential backoff + jitter** — `base * 2^attempt`, not linear, plus jitter to avoid lockstep retries.
- **Half-open circuit breaker** — after the cool-down, one trial call; failure re-opens immediately.
- **Fail-fast on open** — a refused call never touches the remote.
- **Composable monitoring** — `MonitoringAmbassador(ServiceAmbassador(remote))` counts final outcomes, not per-attempt noise.
- **Deterministic tests** — injectable `sleep`/`clock` fakes so backoff and cool-downs don't slow the suite.

## Run

```bash
node ambassador.js       # JS demo
python ambassador.py     # Python demo

node --test ambassador.test.js         # JS tests
python -m pytest test_ambassador.py -v # Python tests
```

Zero dependencies beyond pytest for the test suite.
