/**
 * In-memory simulation of the DLQ runbook workflow.
 *
 * Mirrors the procedures in the runbook: a poison message exhausts its
 * retries, lands in the DLQ with failure metadata, gets inspected and
 * categorized, then replays back to the source queue once the fix deploys.
 *
 * Run: node src/dlq-runbook-simulation.js
 */

const MAX_RETRIES = 3;
let fixDeployed = false;

/** Minimal message broker with a main queue and a DLQ. */
class Broker {
  constructor() {
    this.main = [];
    this.dlq = [];
  }

  publish(msg) {
    this.main.push(msg);
  }
}

/** Business handler — fails on poison payloads until the fix deploys. */
function processMessage(msg) {
  if (msg.value.poison && !fixDeployed) {
    throw new Error('ValidationError: poison payload');
  }
  return true;
}

/** Consumer with retry-count headers and DLQ routing (runbook §1.3). */
function consume(broker) {
  while (broker.main.length) {
    const msg = broker.main.shift();
    try {
      processMessage(msg);
    } catch (e) {
      const retryCount = parseInt(msg.headers['retry-count'] || '0', 10) + 1;
      msg.headers['retry-count'] = String(retryCount);
      if (retryCount <= MAX_RETRIES) {
        broker.publish(msg); // requeue on the source queue
      } else {
        msg.headers.error = e.message;
        msg.headers['failed-at'] = new Date().toISOString();
        broker.dlq.push(msg);
      }
    }
  }
}

/** Aggregate inspection — runbook §2.3. */
function inspectDlq(broker) {
  const categories = {};
  for (const msg of broker.dlq) {
    const error = msg.headers.error || 'unknown';
    const category = error.includes('ValidationError')
      ? 'schema_validation_error'
      : 'business_logic_error';
    categories[category] = (categories[category] || 0) + 1;
  }
  return categories;
}

/** Replay after the fix deploys — runbook §4. */
function replayDlq(broker) {
  let replayed = 0;
  while (broker.dlq.length) {
    const msg = broker.dlq.shift();
    for (const h of ['retry-count', 'error', 'failed-at']) {
      delete msg.headers[h]; // strip DLQ metadata
    }
    broker.publish(msg);
    replayed++;
  }
  return replayed;
}

function main() {
  const broker = new Broker();
  broker.publish({ headers: {}, value: { order_id: 1, poison: true } });
  broker.publish({ headers: {}, value: { order_id: 2, poison: false } });

  console.log('== Phase 1: consume (poison message retries then dead-letters) ==');
  consume(broker);
  console.log(`  main queue: ${broker.main.length} | dlq: ${broker.dlq.length}`);

  console.log('== Phase 2: inspect DLQ (error categorization) ==');
  for (const [category, count] of Object.entries(inspectDlq(broker))) {
    console.log(`  ${category}: ${count}`);
  }

  console.log('== Phase 3: fix deploys, replay DLQ ==');
  fixDeployed = true; // the consumer now handles the poison payload
  console.log(`  replayed: ${replayDlq(broker)}`);
  consume(broker);

  console.log(
    `== Phase 4: verified — dlq: ${broker.dlq.length}, ` +
      `unprocessed: ${broker.main.length} ==`
  );
}

main();
