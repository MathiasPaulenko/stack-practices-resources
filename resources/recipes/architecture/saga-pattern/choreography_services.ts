// Choreography saga: Order, Inventory and Payment services reacting to events
// From https://stackpractices.com/recipes/saga-pattern-recipe/

// Order Service
class OrderService {
  async createOrder(orderData: OrderData): Promise<void> {
    const order = await this.orderRepo.create(orderData);
    await this.eventBus.publish('OrderCreated', {
      orderId: order.id,
      items: order.items,
      total: order.total,
    });
  }

  async cancelOrder(orderId: string): Promise<void> {
    await this.orderRepo.updateStatus(orderId, 'cancelled');
  }
}

// Inventory Service
class InventoryService {
  constructor(private eventBus: EventBus) {
    this.eventBus.subscribe('OrderCreated', this.onOrderCreated.bind(this));
    this.eventBus.subscribe('PaymentFailed', this.onPaymentFailed.bind(this));
  }

  async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
    await this.inventoryRepo.reserve(event.items);
    await this.eventBus.publish('InventoryReserved', {
      orderId: event.orderId,
      items: event.items,
    });
  }

  async onPaymentFailed(event: PaymentFailedEvent): Promise<void> {
    await this.inventoryRepo.release(event.orderId);
  }
}

// Payment Service
class PaymentService {
  constructor(private eventBus: EventBus) {
    this.eventBus.subscribe('InventoryReserved', this.onInventoryReserved.bind(this));
  }

  async onInventoryReserved(event: InventoryReservedEvent): Promise<void> {
    try {
      await this.paymentGateway.charge(event.orderId, event.total);
      await this.eventBus.publish('PaymentProcessed', { orderId: event.orderId });
    } catch (error) {
      await this.eventBus.publish('PaymentFailed', { orderId: event.orderId, reason: error.message });
    }
  }

  async refund(orderId: string): Promise<void> {
    await this.paymentGateway.refund(orderId);
  }
}
