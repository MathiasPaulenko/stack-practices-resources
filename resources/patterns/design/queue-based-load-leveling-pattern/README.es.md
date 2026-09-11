# Patrón de Nivelación de Carga con Colas — Recursos Companion

Este companion contiene implementaciones ejecutables del patrón Queue-Based Load
Leveling en Python, Java y JavaScript.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `queue_producer.py` | Python | Cola en memoria con límite de profundidad, TTL, dead-letter queue, productor |
| `queue_consumer.py` | Python | Handlers para tipos de tarea email, report y payment |
| `queue_config.java` | Java | Configuración Spring + RabbitMQ con DLQ, TTL y overflow |
| `queue_producer.js` | JavaScript | Productor BullMQ con prioridad, backoff y rate limiting |
| `queue_consumer.js` | JavaScript | Consumidor BullMQ con concurrencia y rate limiting |
| `test_queue.py` | Python | 15 tests cubriendo enqueue, dequeue, depth limits, TTL, DLQ, consumer |
| `test_queue.js` | JavaScript | 15 tests cubriendo estructura del productor/consumidor y configuración |

## Ejecutar los tests de Python

```bash
python test_queue.py
```

Salida esperada:

```
=== All 15 tests passed ===
```

## Ejecutar los tests de JavaScript

```bash
node test_queue.js
```

Salida esperada:

```
=== All 15 tests passed ===
```

## Conceptos clave

- **Límite de profundidad**: La cola rechaza mensajes nuevos cuando llega a `max_length`.
- **TTL de mensajes**: Los mensajes viejos expiran y van a la dead-letter queue.
- **Dead-letter queue (DLQ)**: Los mensajes que fallan después de `max_retries` van acá.
- **Rate limiting**: El consumidor procesa a un ritmo controlado para evitar sobrecarga.
- **Auto-escalado**: Monitoreá `queue.depth()` — si sube, agregá más consumidores.

## Fuente

- [Patrón de Nivelación de Carga con Colas](https://stackpractices.com/es/patterns/queue-based-load-leveling-pattern/)
