/**
 * Dead Letter Channel pattern — in-memory simulation.
 *
 * A minimal broker with a main queue, a retry queue, and a dead letter
 * queue. The consumer processes orders; a poison message (missing
 * orderId) keeps failing, exhausts its retry budget, and lands in the
 * DLQ with failure metadata. Run: node src/dead-letter-channel.js
 */

class Broker {
  constructor() {
    this.queues = new Map();
  }

  declare(name) {
    if (!this.queues.has(name)) this.queues.set(name, []);
  }

  send(name, body) {
    this.queues.get(name).push({ body, attempts: 0 });
  }

  sendEnvelope(name, envelope) {
    this.queues.get(name).push(envelope);
  }

  receive(name) {
    return this.queues.get(name).shift() ?? null;
  }

  depth(name) {
    return this.queues.get(name).length;
  }
}

const MAX_RETRIES = 3;

function handleOrder(body) {
  if (body.orderId == null) throw new Error("Missing orderId");
  return { status: "done", orderId: body.orderId };
}

function main() {
  const broker = new Broker();
  for (const queue of ["main", "retry", "dlq"]) broker.declare(queue);

  broker.send("main", { orderId: "A-1", amount: 25 });
  broker.send("main", { orderId: null, amount: 99 }); // poison message
  broker.send("main", { orderId: "A-3", amount: 40 });

  let processed = 0;
  let retries = 0;

  for (;;) {
    const msg = broker.receive("main") ?? broker.receive("retry");
    if (msg === null) break;

    try {
      const result = handleOrder(msg.body);
      processed += 1;
      console.log(`[main] processed order ${result.orderId}`);
    } catch (err) {
      msg.attempts += 1;
      if (msg.attempts >= MAX_RETRIES) {
        msg.failure = { error: err.message, attempts: msg.attempts };
        broker.sendEnvelope("dlq", msg);
        console.log(`[dlq ] moved message after ${msg.attempts} attempts: ${err.message}`);
      } else {
        retries += 1;
        console.log(`[main] attempt ${msg.attempts} failed (${err.message}); retrying`);
        broker.sendEnvelope("retry", msg);
      }
    }
  }

  console.log(`\nmain=${broker.depth("main")} retry=${broker.depth("retry")} dlq=${broker.depth("dlq")}`);
  console.log(`processed=${processed} retried=${retries}`);

  // Replay: fix the poisoned payload, then move it back to the main queue
  const msg = broker.receive("dlq");
  if (msg) {
    console.log(`\n[replay] fixing message and re-queuing (was: ${JSON.stringify(msg.failure)})`);
    msg.body.orderId = "A-2-repaired";
    msg.attempts = 0;
    broker.sendEnvelope("main", msg);
    const fixed = broker.receive("main");
    console.log(`[main] processed order ${handleOrder(fixed.body).orderId}`);
  }
}

main();
