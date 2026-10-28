# Patrón Business Delegate

Código companion del patrón [Patrón Business Delegate](https://stackpractices.com/es/patterns/business-delegate-pattern/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `order_delegate.py` | Cadena completa del delegate en Python: `ServiceLocator`, referencia en caché, `OrderBusinessDelegate`, `ResilientOrderDelegate` con reintentos y backoff, y demo de controller |
| `OrderBusinessDelegate.java` | Delegate clásico estilo J2EE con búsqueda anidada y traducción de excepciones, `main` ejecutable |
| `order-delegate.js` | Delegate en JavaScript con service locator basado en `Map` y referencia en caché |

## Cómo usarlo

- Python: `python order_delegate.py` — solo stdlib.
- JavaScript: `node order-delegate.js`.
- Java: `javac OrderBusinessDelegate.java && java OrderBusinessDelegate`.

Cada archivo refleja una sección de la página del patrón: búsqueda de servicio vía `ServiceLocator`, referencias en caché, traducción de excepciones y la variante resiliente con reintentos y backoff.
