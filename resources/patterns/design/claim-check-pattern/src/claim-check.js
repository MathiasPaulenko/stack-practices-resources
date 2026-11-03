// Claim Check Pattern demo — stdlib only.
// Simulates: large payload -> object storage -> claim token -> broker -> consumer.
// Run: node claim-check.js

const crypto = require('crypto');

class InMemoryBlobStorage {
  constructor() {
    this.store = new Map();
  }

  upload(data, contentType) {
    const token = crypto.randomUUID();
    this.store.set(token, { data, contentType, createdAt: new Date() });
    return token;
  }

  download(token) {
    const entry = this.store.get(token);
    return entry ? entry.data : null;
  }

  delete(token) {
    this.store.delete(token);
  }
}

class MessageBroker {
  constructor() {
    this.queues = new Map();
  }

  publish(queue, message) {
    if (!this.queues.has(queue)) this.queues.set(queue, []);
    this.queues.get(queue).push(message);
  }

  consume(queue) {
    const messages = this.queues.get(queue);
    return messages && messages.length > 0 ? messages.shift() : null;
  }
}

class ClaimCheckProducer {
  constructor(broker, storage) {
    this.broker = broker;
    this.storage = storage;
  }

  publishLargeMessage(queue, payload, metadata = {}) {
    const payloadBytes = Buffer.from(JSON.stringify(payload));
    const token = this.storage.upload(payloadBytes, 'application/json');

    const message = {
      claimCheck: token,
      metadata,
      payloadSize: payloadBytes.length,
      timestamp: new Date().toISOString(),
    };

    this.broker.publish(queue, message);
    console.log(`Published claim check: ${token}`);
    console.log(`  payload size in storage: ${payloadBytes.length.toLocaleString()} bytes`);
    console.log(`  message size on broker:  ~${JSON.stringify(message).length} bytes`);
    return token;
  }
}

class ClaimCheckConsumer {
  constructor(broker, storage) {
    this.broker = broker;
    this.storage = storage;
  }

  processNext(queue) {
    const message = this.broker.consume(queue);
    if (!message) return null;

    const payloadBytes = this.storage.download(message.claimCheck);
    if (!payloadBytes) {
      console.error(`ERROR: claim check ${message.claimCheck} not found in storage`);
      return null;
    }

    const payload = JSON.parse(payloadBytes.toString());
    console.log(`Retrieved payload (${message.payloadSize.toLocaleString()} bytes): ${payload.reportId}`);

    this.storage.delete(message.claimCheck);
    console.log(`Deleted claim check: ${message.claimCheck}`);
    return payload;
  }
}

const storage = new InMemoryBlobStorage();
const broker = new MessageBroker();
const producer = new ClaimCheckProducer(broker, storage);
const consumer = new ClaimCheckConsumer(broker, storage);

const largePayload = {
  reportId: 'RPT-2024-Q1',
  generatedAt: new Date().toISOString(),
  records: Array.from({ length: 1000 }, (_, i) => ({ id: i, data: 'x'.repeat(1000) })),
  summary: { total: 1000, revenue: 500000.0 },
};

producer.publishLargeMessage('reports.queue', largePayload, { priority: 'high' });
consumer.processNext('reports.queue');
