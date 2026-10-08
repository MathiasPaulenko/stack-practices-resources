/**
 * Sequential Convoy pattern — runnable simulation (no broker required).
 *
 * Events are routed to a partition by entity ID. Each partition is owned by a
 * single consumer that applies events in sequence-number order and buffers
 * out-of-order arrivals until the gap closes.
 *
 * Run: node convoy_processor.js
 */

class PartitionedBroker {
  constructor(numPartitions = 4) {
    this.partitions = Array.from({ length: numPartitions }, () => []);
  }

  publish(entityId, event) {
    let hash = 0;
    for (const ch of entityId) {
      hash = (hash * 31 + ch.charCodeAt(0)) >>> 0;
    }
    this.partitions[hash % this.partitions.length].push(event);
  }
}

class ConvoyProducer {
  constructor(broker) {
    this.broker = broker;
    this.sequences = new Map();
  }

  send(entityId, eventType, payload) {
    const seq = (this.sequences.get(entityId) || 0) + 1;
    this.sequences.set(entityId, seq);
    this.broker.publish(entityId, {
      entityId,
      sequence: seq,
      eventType,
      payload,
    });
  }
}

class ConvoyConsumer {
  constructor() {
    this.lastProcessed = new Map();
    this.pending = new Map(); // entityId -> Map<seq, event>
    this.processedLog = [];
  }

  consume(event) {
    const entity = event.entityId;
    const expected = (this.lastProcessed.get(entity) || 0) + 1;

    if (event.sequence === expected) {
      this.#apply(event);
      this.#drainPending(entity);
    } else if (event.sequence > expected) {
      // Out of order — buffer until the missing messages arrive.
      if (!this.pending.has(entity)) this.pending.set(entity, new Map());
      this.pending.get(entity).set(event.sequence, event);
    }
    // sequence < expected is a duplicate; skip it.
  }

  #apply(event) {
    this.processedLog.push(`${event.entityId}#${event.sequence}`);
    this.lastProcessed.set(event.entityId, event.sequence);
  }

  #drainPending(entity) {
    const buffer = this.pending.get(entity);
    if (!buffer) return;
    let expected = (this.lastProcessed.get(entity) || 0) + 1;
    while (buffer.has(expected)) {
      this.#apply(buffer.get(expected));
      buffer.delete(expected);
      expected++;
    }
  }
}

const broker = new PartitionedBroker(4);
const producer = new ConvoyProducer(broker);
const consumer = new ConvoyConsumer();

producer.send('user-123', 'created', { name: 'Alice' });
producer.send('user-123', 'updated', { name: 'Alice Smith' });
producer.send('user-456', 'created', { name: 'Bob' });
producer.send('user-123', 'deleted', {});

const events = broker.partitions.flat();
const u123 = events.filter((e) => e.entityId === 'user-123');
const reordered = [u123[0], u123[2], u123[1]].concat(
  events.filter((e) => e.entityId !== 'user-123')
);

reordered.forEach((e) => consumer.consume(e));

console.log('Processed order:', consumer.processedLog);
const first3 = consumer.processedLog.slice(0, 3).join(',');
if (first3 !== 'user-123#1,user-123#2,user-123#3') {
  throw new Error('convoy ordering broken');
}
console.log('user-123 processed strictly in order despite out-of-order delivery.');
