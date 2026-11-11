class InventoryService {
  async checkStock(itemId) { return true; }
  async reserve(itemId, qty) { console.log(`  reserved ${qty}x ${itemId}`); }
}

class PricingService {
  calculateTotal(items) {
    return items.reduce((sum, i) => sum + i.price * i.qty, 0);
  }
  applyCoupon(total, coupon) { return coupon ? total * 0.9 : total; }
}

class PaymentService {
  async charge(amount, token) {
    console.log(`  charged ${amount.toFixed(2)} with ${token}`);
    return { success: true, txId: 'tx_123' };
  }
}

class ShippingService {
  async createLabel(address) { return 'TRK_456'; }
  calculateCost(address) { return 9.99; }
}

class NotificationService {
  async sendConfirmation(email, orderId) {
    console.log(`  confirmation sent to ${email} for ${orderId}`);
  }
}

class CheckoutFacade {
  // Facade: one entry point for the whole checkout flow.
  // Services are injected, so each one stays mockable in tests.
  constructor(inventory, pricing, payment, shipping, notification) {
    this.inventory = inventory;
    this.pricing = pricing;
    this.payment = payment;
    this.shipping = shipping;
    this.notification = notification;
  }

  async checkout(cart, coupon, paymentToken, address) {
    // 1. Check stock and reserve
    for (const item of cart) {
      const inStock = await this.inventory.checkStock(item.id);
      if (!inStock) throw new Error(`Item ${item.id} out of stock`);
      await this.inventory.reserve(item.id, item.qty);
    }

    // 2. Calculate price
    let total = this.pricing.calculateTotal(cart);
    if (coupon) total = this.pricing.applyCoupon(total, coupon);
    total += this.shipping.calculateCost(address);

    // 3. Charge
    const paymentResult = await this.payment.charge(total, paymentToken);
    if (!paymentResult.success) throw new Error('Payment failed');

    // 4. Create shipment
    const trackingNumber = await this.shipping.createLabel(address);

    // 5. Notify
    await this.notification.sendConfirmation(address.email, paymentResult.txId);

    return { orderId: paymentResult.txId, total, trackingNumber };
  }
}

const facade = new CheckoutFacade(
  new InventoryService(),
  new PricingService(),
  new PaymentService(),
  new ShippingService(),
  new NotificationService()
);

const cart = [
  { id: 'sku-1', price: 25.0, qty: 2 },
  { id: 'sku-2', price: 10.0, qty: 1 },
];
const address = { email: 'ana@example.com', country: 'ES' };

facade.checkout(cart, 'SAVE10', 'tok_abc', address).then(console.log);
