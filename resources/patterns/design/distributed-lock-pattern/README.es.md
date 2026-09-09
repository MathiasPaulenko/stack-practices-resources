# Patrón Distributed Lock

Código companion del [Patrón Distributed Lock](https://stackpractices.com/es/patterns/distributed-lock-pattern/) de StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `redis_lock.py` | Python | Lock con Redis SET NX, TTL y fencing token |
| `redlock.js` | JavaScript | Lock con Redis SET NX usando ioredis |
| `ZooKeeperLock.java` | Java | Lock con ZooKeeper vía Apache Curator InterProcessMutex |
| `test_redis_lock.py` | Python | Tests unitarios del lock en Python con un fake de Redis |

## Ejecutar los Tests

```bash
cd resources/patterns/design/distributed-lock-pattern
pip install pytest
pytest -v
```

## Conceptos Clave

- **TTL**: Cada lock tiene un time-to-live para que un holder caído no deadlockee el sistema.
- **Fencing token**: Un UUID asociado a cada adquisición, enviado con cada escritura para rechazar escrituras rezagadas.
- **Release atómico**: Un script Lua verifica el token antes de borrar la key, evitando liberar el lock de otro.
- **Redlock**: Adquiere el mismo lock en múltiples nodos Redis y lo considera mantenido solo con quorum.

## Relacionado

- [Distributed Lock Pattern (EN)](https://stackpractices.com/patterns/distributed-lock-pattern/)
- [Patrón Distributed Lock (ES)](https://stackpractices.com/es/patterns/distributed-lock-pattern/)
- [Redis distributed locks docs](https://redis.io/docs/manual/patterns/distributed-locks/)
- [Apache Curator](https://curator.apache.org/)
- [Martin Kleppmann sobre Redlock](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
