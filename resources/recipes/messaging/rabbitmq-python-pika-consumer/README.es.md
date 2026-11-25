# Consumer de RabbitMQ con Python y Pika

Código ejecutable complementario de la receta de StackPractices
[Construir un Consumer de RabbitMQ con Python y Pika](https://stackpractices.com/es/recipes/rabbitmq-python-pika-consumer/).

## Contenido

- `producer.py` — publica mensajes JSON persistentes en una cola durable.
- `consumer.py` — consumer con acks manuales, `prefetch_count=1` para fair dispatch y reintentos con header antes del dead-lettering.
- `dlq_setup.py` — declara el dead-letter exchange (`dlx`), la DLQ y la cola principal con argumentos de dead-letter.
- `resilient_consumer.py` — clase de consumer que se reconecta automáticamente si se pierde la conexión.

## Requisitos

- Python 3.10+
- `pika` (`pip install pika`)
- RabbitMQ en local (`docker run -p 5672:5672 rabbitmq:3`) o un host remoto.

## Uso

```bash
# 1. Declarar la cola con su DLX/DLQ
python dlq_setup.py

# 2. Iniciar el consumer (o el consumer con reconexión) en una terminal
python consumer.py task_queue
# python resilient_consumer.py

# 3. Publicar un mensaje en otra terminal
python producer.py
```
