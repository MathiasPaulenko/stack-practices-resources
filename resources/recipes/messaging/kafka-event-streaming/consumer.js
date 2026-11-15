// consumer.js — notification-service consumer group.
// Orders with totalCents ending in 500 simulate a poison message: the handler
// always throws, the message is republished to orders.created.dlq, and the
// offset advances because the DLQ publish is awaited inside eachMessage.
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'notification-service',
  brokers: ['localhost:9092'],
});

const consumer = kafka.consumer({
  groupId: 'notification-service',
  sessionTimeout: 30000,
  heartbeatInterval: 3000,
});

const dlqProducer = kafka.producer({ idempotent: true });

async function publishToDeadLetter(topic, partition, message, error) {
  await dlqProducer.send({
    topic: `${topic}.dlq`,
    messages: [
      {
        key: message.key,
        value: message.value,
        headers: {
          ...message.headers,
          'x-original-partition': String(partition),
          'x-error': String(error?.message ?? error).slice(0, 200),
        },
      },
    ],
  });
}

async function sendEmailNotification(order) {
  if (order.totalCents % 1000 === 500) {
    throw new Error(`poison payload: ${order.id}`);
  }
  console.log(`  -> notified ${order.userId} about ${order.id} ($${order.totalCents / 100})`);
}

async function main() {
  await dlqProducer.connect();
  await consumer.connect();
  await consumer.subscribe({ topic: 'orders.created', fromBeginning: false });
  console.log('Consumer running — Ctrl+C to stop. Failed orders go to orders.created.dlq');

  await consumer.run({
    autoCommit: true,
    autoCommitInterval: 5000,
    eachMessage: async ({ topic, partition, message }) => {
      const order = JSON.parse(message.value.toString());
      try {
        await sendEmailNotification(order);
      } catch (error) {
        console.log(`  !! ${order.id} failed (${error.message}) -> DLQ`);
        await publishToDeadLetter(topic, partition, message, error);
      }
    },
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
