# RabbitMQ Task Queue y RPC

Archivos complementarios ejecutables para la receta de StackPractices [Task Queues y RPC con RabbitMQ y AMQP](https://stackpractices.com/es/recipes/rabbitmq-task-queue/).

## Requisitos

- Node.js 18+ o un runner de TypeScript como `tsx`
- RabbitMQ 3.x con plugin de management (usá el Docker Compose incluido)
- `amqplib` 0.10.x

## Inicio rápido

```bash
# Levantar RabbitMQ
docker compose -f docker-compose.rabbitmq.yml up -d

# Instalar dependencias
npm install amqplib@0.10.x

# Ejecutar con tsx o similar
npx tsx producer.ts
npx tsx worker.ts
npx tsx rpc-server.ts
npx tsx rpc-client.ts
```

## Archivos

- `producer.ts` — publica tareas en una durable queue con política de dead-letter.
- `worker.ts` — consume con prefetch, ack manual y reintentos acotados.
- `rpc-client.ts` — cliente request-reply con reply queue temporal.
- `rpc-server.ts` — servidor RPC que responde con `correlationId`.
- `docker-compose.rabbitmq.yml` — RabbitMQ con UI de management en el puerto 15672.
