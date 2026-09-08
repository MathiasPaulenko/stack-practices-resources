# Patrón de Cola de Prioridad — Ejemplos Companion

Código companion para la guía del [Patrón de Cola de Prioridad](https://stackpractices.com/es/patterns/priority-queue-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `priority_queue_heap.py` | Python | Cola de prioridad basada en heap con worker threads |
| `PriorityQueueScheduler.java` | Java | `PriorityBlockingQueue` con thread pool |
| `redis_priority_queue.js` | JavaScript | Cola de prioridad con Redis sorted set y worker |
| `priority_queue_ts.ts` | TypeScript | Cola de prioridad genérica basada en heap |
| `test_priority_queue.py` | Python | Tests unitarios para la implementación de Python |

## Ejecutar

### Python

```bash
python priority_queue_heap.py
python -m pytest test_priority_queue.py -v
```

### Java

```bash
javac PriorityQueueScheduler.java
java PriorityQueueScheduler
```

### JavaScript (requiere Redis)

```bash
npm install ioredis
node redis_priority_queue.js
```

### TypeScript

```bash
npm install -g typescript
tsc priority_queue_ts.ts
node priority_queue_ts.js
```

## Licencia

MIT — ver el repositorio principal para más detalles.
