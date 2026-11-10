/**
 * Transactional outbox demo: order + outbox row commit together,
 * a relay publishes pending entries to the broker.
 *
 * Companion runnable for https://stackpractices.com/recipes/event-driven-microservices/
 * No dependencies — run `node outbox.js`. The "database" and "broker"
 * are in-memory stubs that model the transactional boundary.
 */

// --- In-memory stand-ins (replace with knex/Prisma + kafkajs in production) ---

const tables = { orders: [], outbox: [] };
const kafka = { published: [] };

const db = {
  transaction: (fn) => fn(tables), // everything inside succeeds or nothing persists
};

// --- Producer side ---

async function placeOrder(orderId, items) {
  await db.transaction(async (trx) => {
    // 1. Business write and outbox write commit atomically.
    trx.orders.push({ id: orderId, status: 'placed' });
    trx.outbox.push({
      id: trx.outbox.length + 1,
      topic: 'orders.events',
      key: orderId,
      payload: JSON.stringify({ event: 'order_placed', orderId, items }),
      sent: false,
    });
  });
}

// --- Relay side: poll the outbox, publish, mark sent ---

async function relayPending() {
  const pending = tables.outbox.filter((m) => !m.sent);
  for (const msg of pending) {
    kafka.published.push({ topic: msg.topic, key: msg.key, value: msg.payload });
    msg.sent = true;
  }
  return pending.length;
}

// --- Demo ---

const orderId = 'order-42';
await placeOrder(orderId, [{ sku: 'KB-87', qty: 1 }]);

console.log(`outbox rows before relay: ${tables.outbox.filter((m) => !m.sent).length}`);
const published = await relayPending();
console.log(`relay published: ${published}`);
console.log(`broker received: ${kafka.published.map((m) => m.value).join(', ')}`);
console.log(`outbox rows after relay: ${tables.outbox.filter((m) => !m.sent).length}`);
