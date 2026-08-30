import * as amqp from 'amqplib';

const connection = await amqp.connect('amqp://localhost');
const channel = await connection.createChannel();

// Dead-letter exchange for failed messages
await channel.assertExchange('dlx', 'direct');
await channel.assertQueue('email.tasks.dlq', { durable: true });
await channel.bindQueue('email.tasks.dlq', 'dlx', 'email.tasks');

// Durable queue with a dead-letter policy
await channel.assertQueue('email.tasks', {
  durable: true,
  arguments: {
    'x-dead-letter-exchange': 'dlx',
    'x-dead-letter-routing-key': 'email.tasks',
  },
});

async function sendEmailTask(email: unknown): Promise<void> {
  channel.sendToQueue('email.tasks', Buffer.from(JSON.stringify(email)), {
    persistent: true,
    headers: { 'x-attempt': 1 },
  });
}

// Example usage
sendEmailTask({ to: 'user@example.com', subject: 'Hello' });
