#!/usr/bin/env node
// Consume OrderPlaced events from RabbitMQ with manual acks and dead-lettering.
import amqp from "amqplib";

async function startInventoryConsumer() {
  const connection = await amqp.connect("amqp://rabbitmq");
  const channel = await connection.createChannel();

  const queue = "inventory_updates";
  await channel.assertQueue(queue, { durable: true });
  await channel.bindQueue(queue, "orders", "OrderPlaced");

  channel.consume(queue, async (msg) => {
    if (msg !== null) {
      const event = JSON.parse(msg.content.toString());
      console.log(`Processing ${event.type} for order ${event.aggregate_id}`);

      try {
        await reserveInventory(event.payload.items);
        channel.ack(msg); // Confirm processing
      } catch (error) {
        channel.nack(msg, false, false); // Dead-letter, don't requeue
      }
    }
  });
}

async function reserveInventory(items) {
  throw new Error("Provide your own inventory service");
}

startInventoryConsumer().catch((err) => {
  console.error("Consumer failed to start:", err);
  process.exit(1);
});
