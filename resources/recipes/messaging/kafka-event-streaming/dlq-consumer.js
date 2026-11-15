// dlq-consumer.js — drains orders.created.dlq so you can inspect failed
// messages and the error headers attached by consumer.js.
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'dlq-inspector',
  brokers: ['localhost:9092'],
});

const consumer = kafka.consumer({ groupId: 'dlq-inspector' });

async function main() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'orders.created.dlq', fromBeginning: true });
  console.log('DLQ inspector running — Ctrl+C to stop');

  await consumer.run({
    eachMessage: async ({ message }) => {
      const order = JSON.parse(message.value.toString());
      const err = message.headers?.['x-error']?.toString() ?? 'unknown';
      console.log(`DLQ <- ${order.id} (${order.userId}) reason: ${err}`);
    },
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
