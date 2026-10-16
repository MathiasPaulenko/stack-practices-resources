// Kafka dead-letter topic with KafkaJS.
// Kafka has no broker-level DLQ; the consumer publishes to a separate topic
// after retries are exhausted, carrying enough headers to debug and replay.
//
// Requires: npm install kafkajs

const { Kafka } = require('kafkajs');

async function processOrder(order) {
  // Placeholder business logic — replace with the real handler.
  throw new Error('not implemented');
}

async function main() {
  const kafka = new Kafka({ brokers: ['localhost:9092'] });
  const consumer = kafka.consumer({ groupId: 'order-processors' });
  const producer = kafka.producer();

  await consumer.connect();
  await producer.connect();
  await consumer.subscribe({ topic: 'orders', fromBeginning: false });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        await processOrder(JSON.parse(message.value.toString()));
      } catch (err) {
        // Publish to the DLQ with enough context to debug and replay
        await producer.send({
          topic: 'orders-dlq',
          messages: [{
            key: message.key,
            value: message.value,
            headers: {
              'error.type': err.name,
              'error.message': err.message,
              'original.topic': topic,
              'original.partition': String(partition),
              'original.offset': String(message.offset),
              'retry.count': '3'
            }
          }]
        });
      }
    }
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
