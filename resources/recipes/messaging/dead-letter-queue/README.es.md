# Colas de mensajes fallidos (DLQ) — Recursos complementarios

Código ejecutable de la receta
[Colas de mensajes fallidos (DLQ) en SQS, RabbitMQ y Kafka](https://stackpractices.com/es/recipes/dead-letter-queue/).

| Archivo | Propósito |
| --- | --- |
| `sqs-dlq-setup.sh` | AWS CLI: crea la cola + DLQ y adjunta la política de reenvío (`maxReceiveCount=3`) |
| `rabbitmq_dlq_consumer.py` | Consumidor pika con declaración de DLX y enrutado `basic_reject(requeue=False)` |
| `kafka_dlq_consumer.js` | Consumidor KafkaJS que publica los mensajes fallidos en `orders-dlq` con headers de error |

Cada broker trata el dead-lettering de forma distinta: SQS a nivel de broker
(política de reenvío), RabbitMQ a través de un dead-letter exchange y Kafka
íntegramente en el código cliente. Sella cada mensaje de la DLQ con el tipo
de error, el origen y el número de reintentos; sin ese contexto, el replay
es adivinanza.
