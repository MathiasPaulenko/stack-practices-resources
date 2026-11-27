# Guía de Procesamiento de Streams — Ejemplos de Código

Código complementario de [Procesamiento de Streams: Pipelines con Kafka y Flink](https://stackpractices.com/es/guides/stream-processing-guide/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---|---|
| `cloudevents_order_schema.json` | Ejemplo de evento `order.placed` compatible con CloudEvents |
| `schema_validator.py` | Validación de eventos con JSON Schema (Python) |
| `OrderAnalyticsApp.java` | App Kafka Streams: filtro, join de enriquecimiento con KTable, agregación por ventana |
| `FraudDetectionJob.java` | Job Flink con estado por clave (`ValueState`/`ListState`) para reglas de pico y velocidad |
| `ExactlyOnceConfig.java` | Configuración exactly-once Kafka + Flink: productor idempotente, checkpoints, sink transaccional |
