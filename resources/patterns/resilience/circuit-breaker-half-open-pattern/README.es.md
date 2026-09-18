# Circuit Breaker Half-Open — Código complementario

Versión ejecutable del breaker de tres estados del patrón
[Circuit Breaker Half-Open](https://stackpractices.com/es/patterns/circuit-breaker-half-open-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `circuit_breaker.py` | `CircuitBreaker` con estados `closed` / `open` / `half_open`, thread-safe con `threading.Lock`, más una suite `unittest` que cubre cada camino de transición |

## Requisitos

- Python 3.10+ — sin dependencias externas.

## Uso

```python
from circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

breaker = CircuitBreaker(
    failure_threshold=5,      # abre tras 5 fallos consecutivos
    recovery_timeout=30,      # segundos antes de los trials half-open
    half_open_max_calls=3,    # presupuesto de requests de prueba
    success_threshold=2,      # éxitos consecutivos para cerrar
)

try:
    result = breaker.call(downstream_api.get, "/status")
except CircuitBreakerOpenError:
    result = fallback_response()
```

## Notas

- La transición open → half-open es perezosa: ocurre dentro de `call()`
  cuando llega un request después del `recovery_timeout`, no en un timer.
- En half-open, un solo fallo reabre el circuito; cerrar exige
  `success_threshold` éxitos consecutivos — la asimetría es deliberada.
- El estado se chequea bajo el lock, pero la llamada envuelta corre fuera de
  él, así que un downstream lento nunca serializa a todos los callers.
