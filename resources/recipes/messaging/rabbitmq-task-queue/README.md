# RabbitMQ Task Queue and RPC

Runnable companion files for the StackPractices recipe [Task Queues and RPC with RabbitMQ and AMQP](https://stackpractices.com/recipes/rabbitmq-task-queue/).

## Requirements

- Node.js 18+ or a TypeScript runner such as `tsx`
- RabbitMQ 3.x with management plugin (use the included Docker Compose file)
- `amqplib` 0.10.x

## Quick start

```bash
# Start RabbitMQ
docker compose -f docker-compose.rabbitmq.yml up -d

# Install dependencies
npm install amqplib@0.10.x

# Run with tsx or a similar runner
npx tsx producer.ts
npx tsx worker.ts
npx tsx rpc-server.ts
npx tsx rpc-client.ts
```

## Files

- `producer.ts` — publishes tasks to a durable queue with a dead-letter policy.
- `worker.ts` — consumes with prefetch, manual ack and bounded retries.
- `rpc-client.ts` — request-reply client with a temporary reply queue.
- `rpc-server.ts` — RPC server that replies with a `correlationId`.
- `docker-compose.rabbitmq.yml` — RabbitMQ with the management UI on port 15672.
