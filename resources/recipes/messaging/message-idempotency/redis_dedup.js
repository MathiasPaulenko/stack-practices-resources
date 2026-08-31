const redis = require('redis');

async function main() {
  const client = await redis.createClient({ url: process.env.REDIS_URL || 'redis://localhost:6379' }).connect();

  const message = { orderId: 'order-123', amount: 100 };
  const idempotencyKey = message.orderId;
  const key = `idempotency:${idempotencyKey}`;

  const locked = await client.set(key, 'processing', { NX: true, EX: 86400 });

  if (!locked) {
    console.log('Duplicate or in-flight message ignored:', idempotencyKey);
    return;
  }

  try {
    const result = await chargeCustomer(message);
    await client.set(key, JSON.stringify(result), { EX: 86400 });
    console.log('Processed:', result);
  } catch (err) {
    await client.del(key);
    throw err;
  } finally {
    await client.disconnect();
  }
}

async function chargeCustomer(message) {
  // Replace with your real payment call.
  return { status: 'charged', orderId: message.orderId, amount: message.amount };
}

main().catch(console.error);
