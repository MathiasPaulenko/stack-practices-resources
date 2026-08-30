import * as amqp from 'amqplib';

const connection = await amqp.connect('amqp://localhost');
const channel = await connection.createChannel();

await channel.assertQueue('calc.multiply');
await channel.consume('calc.multiply', (msg) => {
  if (!msg) return;

  const { a, b } = JSON.parse(msg.content.toString());
  const result = a * b;

  channel.sendToQueue(
    msg.properties.replyTo,
    Buffer.from(JSON.stringify({ result })),
    { correlationId: msg.properties.correlationId },
  );

  channel.ack(msg);
});
