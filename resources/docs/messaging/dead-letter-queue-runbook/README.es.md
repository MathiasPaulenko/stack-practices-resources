# Runbook de Dead Letter Queue — Simulación ejecutable

Complemento del doc de StackPractices [Runbook de Dead Letter Queue](https://stackpractices.com/es/docs/dead-letter-queue-runbook/).

Una demo completa de operaciones con DLQ en tres implementaciones equivalentes: un broker en memoria donde un mensaje tóxico reintenta tres veces, aterriza en la DLQ con los metadatos del fallo, se inspecciona y categoriza, y luego se reprocesa a la cola de origen tras desplegar el "fix" — el ciclo completo del runbook en una sola ejecución. Solo stdlib, sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/dlq_runbook_simulation.py` | Python 3.9+ (solo stdlib) | `python src/dlq_runbook_simulation.py` |
| `src/dlq-runbook-simulation.js` | Node.js 14+ (solo stdlib) | `node src/dlq-runbook-simulation.js` |
| `src/DlqRunbookSimulation.java` | Java 11+ | `javac src/DlqRunbookSimulation.java -d out && java -cp out DlqRunbookSimulation` |

Cada ejecución imprime las cuatro fases: consumo (el tóxico reintenta y pasa a la DLQ), inspección con categorización de errores, replay tras el fix y verificación post-replay con las colas vacías.

El broker es un stub en memoria para que la demo corra en cualquier lado; en producción lo cambiarías por RabbitMQ (dead letter exchange), Kafka (error topic) o SQS (redrive policy) — la lógica de reintento, inspección y replay se mantiene idéntica.
