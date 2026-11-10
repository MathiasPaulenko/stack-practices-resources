// Event-Carried State Transfer — runnable simulation.
// A source service emits events carrying the full updated entity state;
// a consumer applies them to a local replica (Map) and serves reads locally.
// Stdlib only — run with: node src/ecst.js

const { EventEmitter } = require('events');

class CustomerStateTransferEvent {
  constructor(eventType, customerId, payload, version) {
    this.eventId = `evt-${version}`;
    this.eventType = eventType;
    this.customerId = customerId;
    this.payload = payload;
    this.timestamp = new Date().toISOString();
    this.version = version;
  }
}

// Source service: owns customer data and publishes state transfer events
class CustomerService {
  constructor(eventBus) {
    this.customers = new Map();
    this.eventBus = eventBus;
    this.versionCounter = 0;
  }

  createCustomer(customerId, name, email, tier = 'basic') {
    const customer = {
      customerId, name, email, tier,
      loyaltyPoints: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    this.customers.set(customerId, customer);
    this.publish('CUSTOMER_CREATED', customer);
    return customer;
  }

  updateTier(customerId, newTier) {
    const customer = this.customers.get(customerId);
    if (!customer) return null;

    customer.tier = newTier;
    customer.updatedAt = new Date().toISOString();
    this.publish('CUSTOMER_UPDATED', customer);
    return customer;
  }

  publish(eventType, customer) {
    const event = new CustomerStateTransferEvent(
      eventType, customer.customerId, { ...customer }, this.versionCounter++
    );
    this.eventBus.emit('customer.state-transfer', event);
  }
}

// Consumer: Order Service maintains a local read-only replica
class OrderServiceProjection {
  constructor() {
    this.localReplica = new Map();
  }

  onCustomerEvent(event) {
    this.localReplica.set(event.customerId, event.payload);
    console.log(`[OrderService] Replicated customer ${event.customerId} (v${event.version})`);
  }

  getCustomerForOrder(customerId) {
    return this.localReplica.get(customerId);
  }
}

const eventBus = new EventEmitter();
const customerService = new CustomerService(eventBus);
const orderService = new OrderServiceProjection();

eventBus.on('customer.state-transfer', (event) => {
  orderService.onCustomerEvent(event);
});

customerService.createCustomer('C-001', 'Alice', 'alice@example.com', 'premium');
console.log('Order service local copy:', orderService.getCustomerForOrder('C-001'));

customerService.updateTier('C-001', 'gold');
console.log('After update:', orderService.getCustomerForOrder('C-001'));
