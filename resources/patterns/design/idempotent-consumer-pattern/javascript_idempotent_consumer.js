// Idempotent Consumer Pattern — Node.js implementation with Redis dedup.

const Redis = require("ioredis");

class DedupStore {
  constructor(redis) {
    this.redis = redis;
  }

  async isNew(messageId, ttlSeconds = 604800) {
    const key = `processed:${messageId}`;
    const result = await this.redis.set(key, "1", "EX", ttlSeconds, "NX");
    return result === "OK";
  }
}

class IdempotentConsumer {
  constructor(redisUrl = "redis://localhost:6379") {
    this.redis = new Redis(redisUrl);
    this.dedup = new DedupStore(this.redis);
  }

  async processMessage(event) {
    const messageId = event.id;

    if (!(await this.dedup.isNew(messageId))) {
      return `Skipping duplicate: ${messageId}`;
    }

    return await this.upsertOrder(event);
  }

  async upsertOrder(event) {
    return `Upserted order ${event.order_id}: $${event.amount} (${event.status})`;
  }
}

// --- Run example ---
async function main() {
  const consumer = new IdempotentConsumer();

  const events = [
    { id: "msg-1", order_id: "ord-100", amount: 49.99, status: "confirmed" },
    { id: "msg-2", order_id: "ord-101", amount: 12.50, status: "pending" },
    { id: "msg-1", order_id: "ord-100", amount: 49.99, status: "confirmed" },
  ];

  for (const event of events) {
    const result = await consumer.processMessage(event);
    console.log(result);
  }

  await consumer.redis.quit();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { IdempotentConsumer, DedupStore };
