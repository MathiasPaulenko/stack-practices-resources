# Patrón Circuit Breaker — Archivos complementarios

Implementaciones ejecutables de circuit breaker en tres lenguajes. Cada una
extiende la versión didáctica del artículo con dos esenciales de producción:
**clasificación de fallos** (los errores de negocio no disparan el breaker) y un
hook de **fallback** (servir un valor cacheado/por defecto mientras el circuito
está abierto).

Artículo origen: <https://stackpractices.com/es/patterns/circuit-breaker-pattern/>

## Archivos

| Archivo | Lenguaje | Notas |
|---------|----------|-------|
| `circuit_breaker.py` | Python 3.8+ | la tupla `expected_exceptions` clasifica los fallos; `CircuitBreakerOpen` se lanza (o corre el fallback) cuando está abierto |
| `circuitBreaker.mjs` | Node.js 18+ | el predicado `isFailure` decide qué errores cuentan; `call(fn, fallback)` |
| `CircuitBreaker.java` | Java 11+ | contador `AtomicInteger` + estado `volatile` para llamantes concurrentes; excepción runtime `Open` |

## Ejecutar

```bash
python circuit_breaker.py      # sin dependencias
node circuitBreaker.mjs        # sin dependencias
javac CircuitBreaker.java && java CircuitBreaker
```

Cada demo llama a un servicio simulado inestable (70% de fallos) 8 veces para
que puedas ver el breaker saltar a abierto, rechazar llamadas con el fallback y
probar la recuperación en estado semi-abierto.

## Para producción

Usa una librería — obtienes métricas de ventana deslizante y permisos half-open:

- Java: [Resilience4j](https://resilience4j.readme.io/) (`@CircuitBreaker`)
- Python: [pybreaker](https://github.com/danielfrg/pybreaker)
- JavaScript: [opossum](https://github.com/nodeshift/opossum)
- .NET: Polly `CircuitBreakerPolicy`
