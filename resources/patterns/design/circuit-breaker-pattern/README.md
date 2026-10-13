# Circuit Breaker Pattern — Companion Files

Runnable circuit breaker implementations in three languages. Each one extends
the teaching version from the article with two production essentials: **failure
classification** (business errors don't trip the breaker) and a **fallback**
hook (serve a cached/default value while the circuit is open).

Source article: <https://stackpractices.com/patterns/circuit-breaker-pattern/>

## Files

| File | Language | Notes |
|------|----------|-------|
| `circuit_breaker.py` | Python 3.8+ | `expected_exceptions` tuple classifies failures; `CircuitBreakerOpen` is raised (or the fallback runs) when open |
| `circuitBreaker.mjs` | Node.js 18+ | `isFailure` predicate decides which errors count; `call(fn, fallback)` |
| `CircuitBreaker.java` | Java 11+ | `AtomicInteger` counter + `volatile` state for concurrent callers; `Open` runtime exception |

## Run

```bash
python circuit_breaker.py      # no dependencies
node circuitBreaker.mjs        # no dependencies
javac CircuitBreaker.java && java CircuitBreaker
```

Each demo calls a simulated flaky service (70% failure rate) 8 times so you can
watch the breaker trip open, reject calls with the fallback, and probe recovery
in half-open state.

## For production

Use a library instead — you get sliding-window metrics and half-open permits:

- Java: [Resilience4j](https://resilience4j.readme.io/) (`@CircuitBreaker`)
- Python: [pybreaker](https://github.com/danielfrg/pybreaker)
- JavaScript: [opossum](https://github.com/nodeshift/opossum)
- .NET: Polly `CircuitBreakerPolicy`
