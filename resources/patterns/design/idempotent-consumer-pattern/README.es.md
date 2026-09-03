# Patrón de Consumidor Idempotente — Código Companion

Código companion para la guía del [Patrón de Consumidor Idempotente](https://stackpractices.com/es/patterns/idempotent-consumer-pattern/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `python_idempotent_consumer.py` | Implementación Python con tienda de dedup SQLite |
| `java_idempotent_consumer.java` | Implementación Java con dedup en memoria + repositorio |
| `javascript_idempotent_consumer.js` | Implementación Node.js con dedup Redis |
| `test_dedup.py` | Tests de lógica de deduplicación (5 tests) |
| `test_idempotent_operations.py` | Tests de operaciones idempotentes y recuperación de crash (4 tests) |

## Ejecución

### Python

```bash
python python_idempotent_consumer.py
pytest test_dedup.py test_idempotent_operations.py -v
```

### Java

```bash
javac java_idempotent_consumer.java
java IdempotentConsumer
```

### JavaScript

```bash
node javascript_idempotent_consumer.js
```

## Licencia

MIT
