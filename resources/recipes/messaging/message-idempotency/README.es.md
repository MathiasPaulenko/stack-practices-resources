# Idempotencia en Procesamiento de Mensajes — Companion

Ejemplos ejecutables para la receta de StackPractices [Idempotencia en Procesamiento de Mensajes](https://stackpractices.com/es/recipes/message-idempotency/).

## Qué hay aquí

- `redis_dedup.js` — webhook de pago idempotente con Node.js y Redis `SET NX EX`.
- `postgres_dedup.sql` — tabla PostgreSQL y una transacción de ejemplo que inserta el ID del mensaje y actualiza el side effect.
- `kafka_consumer.py` — consumer Kafka en Python con deduplicación en Redis.
- `kafka_consumer.java` — consumer Kafka en Java con deduplicación en Redis.
- `kafka_idempotent_producer.java` — configuración de producer idempotente de Kafka en Java.
- `sqs_handler.py` — consumer AWS SQS FIFO con escritura condicional en DynamoDB.
- `docker-compose.yml` — levanta Redis, PostgreSQL y un Kafka de un nodo localmente.
- `package.json`, `requirements.txt`, `pom.xml` — dependencias mínimas.

## Inicio rápido

1. Levantá la infraestructura:

```bash
docker compose up -d
```

1. Ejecutá el ejemplo de Redis en Node.js:

```bash
cp .env.example .env
npm install
node redis_dedup.js
```

1. Ejecutá el consumer Kafka en Python:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python kafka_consumer.py
```

1. Ejecutá el consumer Kafka en Java:

```bash
mvn compile
mvn exec:java -Dexec.mainClass="KafkaConsumerDedup"
```

## Notas

- Los ejemplos usan `localhost` y puertos por defecto. Actualizalos para tu entorno.
- Los ejemplos de Redis setean un estado `processing` y lo borran en caso de error. Borrá la clave solo si el side effect no se completó.
- El producer idempotente de Kafka cubre reintentos por partición, no rebalances o restarts del producer. El consumer todavía necesita su propio store de dedup.
