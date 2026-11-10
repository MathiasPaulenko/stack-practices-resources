/**
 * Event Bus pattern: in-memory pub/sub where subscribe() returns an
 * unsubscribe closure.
 *
 * Run: node event_bus.js
 * Test: node --test event_bus.test.js
 */

class EventBus {
  constructor() {
    this.handlers = new Map();
  }

  subscribe(eventType, handler) {
    if (!this.handlers.has(eventType)) this.handlers.set(eventType, []);
    this.handlers.get(eventType).push(handler);
    return () => {
      const list = this.handlers.get(eventType) || [];
      this.handlers.set(eventType, list.filter((h) => h !== handler));
    };
  }

  publish(eventType, payload) {
    // Snapshot the list so handlers may unsubscribe during dispatch
    const list = [...(this.handlers.get(eventType) || [])];
    for (const handler of list) {
      try {
        handler(payload);
      } catch (err) {
        console.error(`[BUS] handler error for ${eventType}:`, err.message);
      }
    }
  }
}

export default EventBus;

if (import.meta.url === `file://${process.argv[1].replace(/\\/g, '/')}`) {
  const bus = new EventBus();
  const received = [];

  bus.subscribe('UserRegistered', (p) => received.push(`email:${p.userId}`));
  bus.subscribe('UserRegistered', (p) => received.push(`analytics:${p.userId}`));
  const unsubCrm = bus.subscribe('UserRegistered', (p) => received.push(`crm:${p.userId}`));

  bus.publish('UserRegistered', { userId: 42, email: 'alice@example.com' });
  console.log('after first publish:', received);

  unsubCrm();
  bus.publish('UserRegistered', { userId: 43, email: 'bob@example.com' });
  console.log('after unsubscribe:', received.slice(3));
}
