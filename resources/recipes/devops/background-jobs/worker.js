// BullMQ worker + producer for the background-jobs recipe.
// Requires Redis on localhost:6379. Run: node worker.js
const { Queue, Worker } = require("bullmq");
const IORedis = require("ioredis");

// BullMQ workers require maxRetriesPerRequest: null
const connection = new IORedis({ host: "localhost", port: 6379, maxRetriesPerRequest: null });

const emailQueue = new Queue("emails", { connection });
const dlqQueue = new Queue("dlq", { connection });

const worker = new Worker(
  "emails",
  async (job) => {
    const { to, subject, body } = job.data;
    if (to.includes("fail")) throw new Error("Simulated failure");
    console.log(`Sending email to ${to}: ${subject}`);
    return { sent: true };
  },
  {
    connection,
    attempts: 3,
    backoff: { type: "exponential", delay: 2000 },
  }
);

// "failed" fires on every attempt — only move to the DLQ on the last one
worker.on("failed", async (job, err) => {
  if (job.attemptsMade >= job.opts.attempts) {
    console.error(`Job ${job.id} exhausted retries: ${err.message}`);
    await dlqQueue.add("failed-email", job.data, { removeOnComplete: true });
  }
});

async function main() {
  await emailQueue.add(
    "send-email",
    { to: "alice@example.com", subject: "Welcome", body: "Hello!" },
    { attempts: 3, backoff: { type: "exponential", delay: 1000 } }
  );

  // Recurring job: cleanup every day at 02:00
  const cronQueue = new Queue("cron", { connection });
  await cronQueue.add("cleanup", {}, { repeat: { pattern: "0 2 * * *" } });
  console.log("Enqueued email job + recurring cleanup job");
}

main().catch(console.error);
