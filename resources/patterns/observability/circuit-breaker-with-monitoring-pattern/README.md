# Circuit Breaker with Monitoring

Companion resources for the [Circuit Breaker with Monitoring Pattern](https://stackpractices.com/patterns/circuit-breaker-with-monitoring-pattern/).

## Files

| File | Description |
|------|-------------|
| `python_circuit_breaker.py` | Python implementation with Prometheus metrics |
| `javascript_circuit_breaker.js` | Node.js implementation with opossum and prom-client |
| `java_circuit_breaker.java` | Java implementation with Resilience4j and Micrometer |
| `test_circuit_breaker.py` | pytest tests for state transitions and metric emission |
| `requirements.txt` | Python dependencies |

## Running the tests

```bash
pip install -r requirements.txt
pytest -q
```

## Python usage

```python
from python_circuit_breaker import MonitoredCircuitBreaker

breaker = MonitoredCircuitBreaker("payment-service", "/api/charge", failure_threshold=5)
try:
    result = breaker.call(lambda: payment_gateway.charge(order))
except CircuitBreakerOpenError:
    print("Circuit is open, call rejected")
```

## Node.js usage

```javascript
const { createMonitoredBreaker } = require("./javascript_circuit_breaker");

const { breaker, registry } = createMonitoredBreaker(
  "payment-service",
  "/api/charge",
  async (order) => fetch("/api/charge", { method: "POST", body: JSON.stringify(order) }),
  { timeout: 5000, resetTimeout: 30000 }
);

breaker.fallback(() => ({ error: "circuit open" }));
```
