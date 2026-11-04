# Guía Completa de Sistemas Event-Driven — Assets del ejemplo

Artefactos ejecutables de la
[Guía Completa de Sistemas Event-Driven](https://stackpractices.com/es/guides/complete-guide-event-driven-systems/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `outbox.sql` | Tabla outbox en Postgres + índice del relay + nota de limpieza |
| `saga_orchestrator.py` | Saga por orquestación con flujo de compensación |
| `idempotent_consumer.py` | Patrón de consumer con dedup vía Redis `SETNX` |
| `dlq_worker.py` | Contador de reintentos + enrutado a dead letter queue |
| `docker-compose.yml` | Playground Redis + Postgres con la tabla outbox |

## Uso

```bash
docker compose up -d   # arranca Redis + Postgres (tabla outbox autocreada)
```
