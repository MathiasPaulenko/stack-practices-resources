// RabbitMQ examples with amqplib (Node.js).
// Run: node javascript_rabbitmq.js
const amqp = require("amqplib");

async function demoDirectExchange() {
  const conn = await amqp.connect("amqp://localhost");
  const ch = await conn.createChannel();
  await ch.assertExchange("orders_direct", "direct");
  await ch.assertQueue("orders_created");
  await ch.assertQueue("orders_cancelled");
  await ch.bindQueue("orders_created", "orders_direct", "created");
  await ch.bindQueue("orders_cancelled", "orders_direct", "cancelled");

  ch.publish("orders_direct", "created", Buffer.from(JSON.stringify({ order_id: 123, total: 49.99 })));
  ch.publish("orders_direct", "cancelled", Buffer.from(JSON.stringify({ order_id: 124, reason: "customer_request" })));
  console.log("Direct exchange: 2 messages published");
  await conn.close();
}

async function demoTopicExchange() {
  const conn = await amqp.connect("amqp://localhost");
  const ch = await conn.createChannel();
  await ch.assertExchange("logs_topic", "topic");
  const q1 = await ch.assertQueue("all_errors");
  const q2 = await ch.assertQueue("app_errors");
  const q3 = await ch.assertQueue("all_logs");
  await ch.bindQueue(q1.queue, "logs_topic", "*.error");
  await ch.bindQueue(q2.queue, "logs_topic", "app.*");
  await ch.bindQueue(q3.queue, "logs_topic", "#");

  ch.publish("logs_topic", "app.error", Buffer.from("App error"));
  ch.publish("logs_topic", "db.warning", Buffer.from("DB warning"));
  ch.publish("logs_topic", "api.error.critical", Buffer.from("API critical"));
  console.log("Topic exchange: 3 messages published");
  await conn.close();
}

async function demoFanoutExchange() {
  const conn = await amqp.connect("amqp://localhost");
  const ch = await conn.createChannel();
  await ch.assertExchange("notifications_fanout", "fanout");
  const q1 = await ch.assertQueue("email_queue");
  const q2 = await ch.assertQueue("sms_queue");
  const q3 = await ch.assertQueue("push_queue");
  await ch.bindQueue(q1.queue, "notifications_fanout");
  await ch.bindQueue(q2.queue, "notifications_fanout");
  await ch.bindQueue(q3.queue, "notifications_fanout");

  ch.publish("notifications_fanout", "", Buffer.from(JSON.stringify({ user_id: 123, message: "Order shipped" })));
  console.log("Fanout exchange: 1 message broadcast to 3 queues");
  await conn.close();
}

async function workQueueConsumer() {
  const conn = await amqp.connect("amqp://localhost");
  const ch = await conn.createChannel();
  await ch.assertQueue("tasks", { durable: true });
  ch.prefetch(1);

  ch.consume("tasks", (msg) => {
    try {
      const task = JSON.parse(msg.content.toString());
      console.log("Processing task:", task);
      ch.ack(msg);
    } catch (err) {
      console.error("Error:", err);
      ch.nack(msg, false, true);
    }
  });
  console.log("Work queue consumer started. Press Ctrl+C to stop.");
}

async function main() {
  await demoDirectExchange();
  await demoTopicExchange();
  await demoFanoutExchange();
  console.log("\nAll demos complete. Run workQueueConsumer() to start consuming.");
}

main().catch(console.error);
