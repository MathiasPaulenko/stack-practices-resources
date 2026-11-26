# Lambda Event-Driven con Triggers SQS — Archivos de apoyo

Proyecto ejecutable complementario de la [receta de Lambda con triggers SQS](https://stackpractices.com/es/recipes/serverless-event-driven-sqs-lambda/) en StackPractices.

- `lambda_function.py` — consumidor por lotes con partial batch responses (`batchItemFailures`) para que solo los mensajes fallidos vuelvan a la cola.
- `producer.py` — envíos individuales, `send_message_batch` (lotes de 10) y envíos FIFO ordenados con message groups y deduplication IDs.
- `template.yaml` — template SAM: cola principal + DLQ con politica de redrive, trigger SQS con `BatchSize`/`MaxBatchingWindow`/`ReportBatchItemFailures`, topico SNS de alertas y alarma de CloudWatch sobre la profundidad del DLQ.
- `queue-attributes.json` — archivo de atributos para `aws sqs create-queue` (reemplaza `<DLQ_ARN>` con el ARN de tu dead-letter queue).
- `drain_queue.py` — handler programado que hace polling y drena la cola cuando lo invoca una regla de EventBridge.

Requiere `boto3`, credenciales de AWS, y `sam` para el template.
