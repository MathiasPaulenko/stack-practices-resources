import * as amqp from 'amqplib';

const connection = await amqp.connect('amqp://localhost');
const channel = await connection.createChannel();

await channel.prefetch(5); // Process up to 5 messages concurrently per worker

await channel.consume('email.tasks', async (msg) => {
  if (!msg) return;

  const email = JSON.parse(msg.content.toString());
  const attempt = msg.properties.headers?.['x-attempt'] || 1;

  try {
    await sendEmail(email);
    channel.ack(msg);
  } catch (error) {
    if (attempt >= 3) {
      // Drop the message after three attempts; the DLX routes it to the DLQ
      channel.nack(msg, false, false);
    } else {
      // Reject the original message and republish with an incremented attempt
      channel.nack(msg, false, false);
      channel.sendToQueue('email.tasks', msg.content, {
        persistent: true,
        headers: { 'x-attempt': attempt + 1 },
      });
    }
  }
});

async function sendEmail(email: unknown): Promise<void> {
  // Your email-sending logic here
  console.log('Sending email:', email);
}
