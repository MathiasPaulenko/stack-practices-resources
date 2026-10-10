#!/usr/bin/env node
// Message Queue Load Leveling with BullMQ + Redis.
// Producer enqueues at any rate; the worker drains at a limited rate.
// Needs a local Redis (`docker run -p 6379:6379 redis`), then `node bullmq_worker.mjs`.
import { Queue, Worker } from "bullmq";

const orderQueue = new Queue("orders", {
  connection: { host: "localhost", port: 6379 },
});

// Producer: enqueue at any rate
async function submitOrders(orderIds) {
  const jobs = orderIds.map((id) => ({
    name: "process-order",
    data: { orderId: id },
  }));
  await orderQueue.addBulk(jobs);
  console.log(`Enqueued ${orderIds.length} orders`);
}

// Consumer: process at controlled rate
const worker = new Worker(
  "orders",
  async (job) => {
    // Simulate slow processing
    await new Promise((resolve) => setTimeout(resolve, 2000));
    console.log(`Processed order ${job.data.orderId}`);
    return { status: "done", orderId: job.data.orderId };
  },
  {
    connection: { host: "localhost", port: 6379 },
    concurrency: 1, // Process one at a time
    limiter: { max: 1, duration: 2000 }, // Max 1 job per 2 seconds
  }
);

worker.on("failed", (job, err) => {
  console.error(`Job ${job.id} failed: ${err.message}`);
});

// Burst: 1000 orders submitted instantly
await submitOrders(Array.from({ length: 1000 }, (_, i) => i));
