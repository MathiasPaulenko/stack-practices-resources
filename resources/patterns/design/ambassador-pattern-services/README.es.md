# Patrón Ambassador — Ejemplos Companion

Ejemplos ejecutables del [patrón Ambassador](https://stackpractices.com/es/patterns/ambassador-pattern-services/): un proxy local que posee las políticas de resiliencia — reintentos, timeouts, circuit breaker, métricas — para que los clientes se mantengan delgados.

Sin servicios externos. El "remoto" es un callable falso; el ambassador lo envuelve con la misma semántica que usarías sobre un cliente HTTP o gRPC real.

## Qué contiene

| Fichero | Propósito |
| --- | --- |
| `ambassador.py` / `ambassador.js` | `ServiceAmbassador` (retry + timeout + circuit breaker half-open) y `MonitoringAmbassador` (capa de métricas componible) |
| `test_ambassador.py` | Suite pytest (8 tests) |
| `ambassador.test.js` | Suite `node:test` (8 tests) |

## Conceptos cubiertos

- **Wrapper transparente** — el cliente llama a `call()`; la resiliencia es invisible.
- **Backoff exponencial real + jitter** — `base * 2^attempt`, no lineal, más jitter para evitar reintentos sincronizados.
- **Circuit breaker half-open** — tras el enfriamiento, una llamada de prueba; si falla, se reabre inmediatamente.
- **Fail-fast con circuit abierto** — una llamada rechazada nunca toca el remoto.
- **Monitorización componible** — `MonitoringAmbassador(ServiceAmbassador(remote))` cuenta resultados finales, no ruido por intento.
- **Tests deterministas** — fakes inyectables de `sleep`/`clock` para que backoff y enfriamientos no ralenticen la suite.

## Ejecutar

```bash
node ambassador.js       # demo JS
python ambassador.py     # demo Python

node --test ambassador.test.js         # tests JS
python -m pytest test_ambassador.py -v # tests Python
```

Cero dependencias más allá de pytest para la suite de tests.
