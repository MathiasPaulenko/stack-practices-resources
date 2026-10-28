// Business Delegate: lookup, cached reference, error translation.

class RemoteOrderService {
  createOrder(customerId, items) {
    return { order_id: 'ORD-123', status: 'created', items };
  }

  getOrder(orderId) {
    return { order_id: orderId, status: 'shipped' };
  }
}

class ServiceLocator {
  static services = new Map();
  static register(name, service) { this.services.set(name, service); }
  static lookup(name) { return this.services.get(name); }
}

class OrderBusinessDelegate {
  constructor() {
    this.service = null;
  }

  getService() {
    if (!this.service) {
      this.service = ServiceLocator.lookup('OrderService') || new RemoteOrderService();
    }
    return this.service;
  }

  createOrder(customerId, items) {
    try {
      return this.getService().createOrder(customerId, items);
    } catch (e) {
      throw new Error(`Failed to create order: ${e.message}`);
    }
  }

  getOrder(orderId) {
    return this.getService().getOrder(orderId);
  }
}

class OrderController {
  constructor() {
    this.delegate = new OrderBusinessDelegate();
  }

  handleCreateOrder(customerId, items) {
    const result = this.delegate.createOrder(customerId, items);
    return `Order created: ${result.order_id}`;
  }
}

// Usage
ServiceLocator.register('OrderService', new RemoteOrderService());
const controller = new OrderController();
console.log(controller.handleCreateOrder('CUST-001', ['item1', 'item2']));
