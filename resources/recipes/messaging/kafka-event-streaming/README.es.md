# Kafka Event Streaming — Código Companion

Demo ejecutable con KafkaJS para la receta de StackPractices [Event Streaming con Apache Kafka y Node.js](https://stackpractices.com/es/recipes/kafka-event-streaming/).

## Archivos

| Archivo | Propósito |
|---|---|
| `docker-compose.yml` | Kafka de un nodo en modo KRaft (sin Zookeeper) |
| `producer.js` | Publica 10 eventos `OrderCreated` con key `userId` |
| `consumer.js` | Grupo `notification-service` — envía mensajes venenosos a `orders.created.dlq` |
| `dlq-consumer.js` | Inspector que drena el DLQ e imprime los headers de error adjuntos |
| `package.json` | Dependencia `kafkajs` + scripts `produce`/`consume`/`consume-dlq` |

## Ejecución

```bash
docker compose up -d        # levantar Kafka (KRaft, localhost:9092)
npm install
npm run consume             # terminal 1
npm run consume-dlq         # terminal 2
npm run produce             # terminal 3 — envía 10 órdenes
```

Las órdenes con `totalCents` terminado en `500` están "envenenadas" a propósito: `consumer.js` lanza error dentro del handler, republica el mensaje a `orders.created.dlq` con el error en un header `x-error`, y deja avanzar el offset. Míralos llegar en la terminal del inspector DLQ.

## Notas

- `KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092` solo funciona desde el host. Para conectar desde otro contenedor, añade un segundo listener (ej. `PLAINTEXT://kafka:29092`).
- Los topics se auto-crean en el primer produce. En producción, créalos explícitamente con el número de particiones y el factor de replicación que necesites.
- El DLQ conserva la key original, así que los mensajes fallidos mantienen el orden con el resto de eventos del usuario.
