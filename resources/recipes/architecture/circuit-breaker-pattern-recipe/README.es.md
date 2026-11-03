# Recursos de la Receta del Patrón Circuit Breaker

Complementarios de [Construir Sistemas Resilientes con el Patrón Circuit Breaker](https://stackpractices.com/es/recipes/circuit-breaker-pattern-recipe/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `impl/` | Implementaciones del circuit breaker extraídas de la receta (varios lenguajes) |

## Uso

Copia la implementación de tu stack al proyecto; envuelve las llamadas salientes con `.call(fn)` / `await breaker.execute(fn)` según el lenguaje. Ajusta `failureThreshold`, `resetTimeout` y el fallback a tu servicio.
