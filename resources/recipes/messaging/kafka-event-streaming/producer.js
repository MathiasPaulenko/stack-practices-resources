// producer.js — publishes OrderCreated events to the orders.created topic.
// The message key (userId) pins each user's events to one partition,
// preserving order. `idempotent: true` deduplicates retries on the broker.
import { Kafka, Partitioners } from 'kafkajs';
import { randomUUID } from 'node:crypto';

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['localhost:9092'],
});

const producer = kafka.producer({
  createPartitioner: Partitioners.DefaultPartitioner,
  idempotent: true,
  retry: { retries: 5, initialRetryTime: 300 },
});

function makeOrder(i) {
  const userIds = ['user-1', 'user-2', 'user-3'];
  return {
    id: `order-${Date.now()}-${i}`,
    userId: userIds[i % userIds.length],
    totalCents: 1000 + i * 250,
    createdAt: new Date().toISOString(),
  };
}

async function main() {
  await producer.connect();
  console.log('Producer connected — sending 10 orders to orders.created');

  await producer.send({
    topic: 'orders.created',
    messages: Array.from({ length: 10 }, (_, i) => {
      const order = makeOrder(i);
      return {
        key: order.userId,
        value: JSON.stringify(order),
        headers: {
          'content-type': 'application/json',
          'trace-id': randomUUID(),
        },
      };
    }),
  });

  console.log('Sent. Disconnecting.');
  await producer.disconnect();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
