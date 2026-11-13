# Patrón Graceful Degradation — Archivos complementarios

Implementaciones ejecutables de degradación elegante en tres lenguajes. Cada una
envuelve una llamada poco fiable con una escalera de tres alternativas:
**llamada principal → caché acotado por TTL → valor por defecto**, y devuelve un
`ServiceResult` que indica al llamador cuánto se ha degradado la respuesta
(`healthy`, `degraded` o `down`).

Artículo fuente: <https://stackpractices.com/es/patterns/graceful-degradation-pattern/>

## Archivos

| Archivo | Lenguaje | Notas |
|---------|----------|-------|
| `graceful_degradation.py` | Python 3.8+ | `call_with_fallback` acepta un `fallback_fn` opcional; `aggregate` degrada cada servicio de forma independiente |
| `gracefulDegradation.mjs` | Node.js 18+ | La misma escalera con un caché basado en `Map`; `callWithFallback(service, primary, fallback, default, cacheKey)` |
| `GracefulDegradation.java` | Java 11+ | `ServiceResult` basado en `record` con factorías `healthy`/`degraded`/`down` |

## Ejecutar

```bash
python graceful_degradation.py
node gracefulDegradation.mjs
javac GracefulDegradation.java && java GracefulDegradation
```

Cada programa simula una página de producto donde `recommendations` e
`inventory` fallan mientras `product_details` y `reviews` funcionan. Salida
esperada: la página se monta igualmente, con los servicios fallidos marcados
como `DEGRADED` y servidos desde valores por defecto o caché.

## Notas

- El caché en memoria y el TTL de 300 segundos son solo para la demo. En
  producción usa un caché compartido (Redis/Memcached) y un TTL por tipo de
  dato: las recomendaciones aguantan horas, los precios minutos.
- Los ejemplos capturan excepciones genéricas por brevedad. El código real solo
  debería tratar fallos de dependencia (timeouts, errores de conexión, 5xx,
  circuit breaker abierto) como detonantes de degradación; un 404 o un error de
  validación merece un fallo real.
