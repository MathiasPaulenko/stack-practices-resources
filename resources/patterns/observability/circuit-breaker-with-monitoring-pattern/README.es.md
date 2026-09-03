# Circuit Breaker con Monitoring

Recursos companion para el [Patrón Circuit Breaker con Monitoring](https://stackpractices.com/es/patterns/circuit-breaker-with-monitoring-pattern/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `python_circuit_breaker.py` | Implementación Python con métricas de Prometheus |
| `javascript_circuit_breaker.js` | Implementación Node.js con opossum y prom-client |
| `java_circuit_breaker.java` | Implementación Java con Resilience4j y Micrometer |
| `test_circuit_breaker.py` | Tests pytest para transiciones de estado y emisión de métricas |
| `requirements.txt` | Dependencias Python |

## Ejecutar los tests

```bash
pip install -r requirements.txt
pytest -q
```

## Uso Python

```python
from python_circuit_breaker import MonitoredCircuitBreaker

breaker = MonitoredCircuitBreaker("payment-service", "/api/charge", failure_threshold=5)
try:
    result = breaker.call(lambda: payment_gateway.charge(order))
except CircuitBreakerOpenError:
    print("Circuit abierto, llamada rechazada")
```

## Uso Node.js

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
