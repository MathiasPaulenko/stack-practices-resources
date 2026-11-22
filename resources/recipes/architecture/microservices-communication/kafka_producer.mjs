// Asynchronous message producer for Kafka (kafkajs).
// Companion to https://stackpractices.com/recipes/microservices-communication/
// Usage: npm run kafka   (needs a broker at KAFKA_BROKERS, default kafka:9092)

import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  brokers: (process.env.KAFKA_BROKERS || 'kafka:9092').split(','),
});
const producer = kafka.producer();

export async function publishOrderCreated(order) {
  await producer.connect();
  await producer.send({
    topic: 'orders.created',
    messages: [{ key: order.id, value: JSON.stringify(order) }],
  });
  await producer.disconnect();
}

if (process.argv[1].endsWith('kafka_producer.mjs')) {
  publishOrderCreated({ id: 'ord_123', items: [{ sku: 'book', qty: 1 }] })
    .then(() => console.log('Published orders.created'))
    .catch((err) => {
      console.error(`Kafka unreachable: ${err.message}`);
      process.exit(1);
    });
}
