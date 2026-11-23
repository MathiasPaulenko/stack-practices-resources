# Patrón Object Pool

Archivos ejecutables que acompañan a [Patrón Object Pool](https://stackpractices.com/es/patterns/object-pool-pattern/).

Pool de tamaño fijo de conexiones costosas en tres lenguajes: objetos pre-calentados, `acquire()`/`release()` con fallo rápido al agotarse, y un wrapper seguro (`with`, try/finally, `withConnection`) para que los objetos siempre vuelvan al pool.

## Archivos

| Archivo | Lenguaje | Notas |
| --- | --- | --- |
| `connection_pool.py` | Python 3.8+ | Pool con `queue.Queue`, `PoolExhaustedError`, context manager `pool.pooled()` |
| `ConnectionPool.java` | Java 11+ | Pool con `BlockingQueue`, `poll()` acotado en lugar de `take()` bloqueante |
| `connection-pool.js` | Node 14+ | Pool con array, `PoolExhaustedError`, helper async `withConnection(fn)` |

## Ejecutar

```bash
python connection_pool.py
javac ConnectionPool.java && java ConnectionPool
node connection-pool.js
```

Cada demo extrae un objeto, consulta, devuelve y vuelve a extraer — el segundo checkout reutiliza el mismo objeto (no aparece otra línea "(expensive)").

## Notas

- Los tres pools fallan rápido en lugar de bloquearse para siempre al agotarse — un `acquire` sin límite convierte un pool lleno en una app colgada.
- La `DatabaseConnection` del pool es un stub. Sustitúyela por un cliente real (psycopg, JDBC, pg/mysql2) y añade una validación al extraer para uso en producción.
