import * as amqp from 'amqplib';

async function rpcCall(queue: string, payload: unknown): Promise<unknown> {
  const connection = await amqp.connect('amqp://localhost');
  const channel = await connection.createChannel();

  const correlationId = generateId();
  const { queue: replyQueue } = await channel.assertQueue('', { exclusive: true });

  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('RPC timeout')), 5000);

    channel.consume(replyQueue, (msg) => {
      if (msg?.properties.correlationId === correlationId) {
        clearTimeout(timeout);
        resolve(JSON.parse(msg.content.toString()));
        channel.ack(msg);
      }
    });

    channel.sendToQueue(queue, Buffer.from(JSON.stringify(payload)), {
      replyTo: replyQueue,
      correlationId,
      expiration: '5000',
    });
  });
}

function generateId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

// Example usage
rpcCall('calc.multiply', { a: 7, b: 8 })
  .then((result) => {
    console.log('RPC result:', result);
    process.exit(0);
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
