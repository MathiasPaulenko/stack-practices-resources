interface ShippingStrategy {
  calculate(order: Order): number;
}

class FlatRateStrategy implements ShippingStrategy {
  constructor(private rate: number) {}

  calculate(order: Order): number {
    return this.rate;
  }
}

class WeightBasedStrategy implements ShippingStrategy {
  constructor(private ratePerKg: number) {}

  calculate(order: Order): number {
    return order.totalWeight * this.ratePerKg;
  }
}

class DistanceBasedStrategy implements ShippingStrategy {
  constructor(private baseRate: number, private perKm: number) {}

  calculate(order: Order): number {
    return this.baseRate + (order.distanceKm * this.perKm);
  }
}

class CheckoutService {
  private shippingStrategy: ShippingStrategy;

  constructor(strategy: ShippingStrategy) {
    this.shippingStrategy = strategy;
  }

  setStrategy(strategy: ShippingStrategy): void {
    this.shippingStrategy = strategy;
  }

  getTotal(order: Order): number {
    const subtotal = order.items.reduce((sum, item) => sum + item.price, 0);
    const shipping = this.shippingStrategy.calculate(order);
    return subtotal + shipping;
  }
}

// Runtime selection
const strategy = order.destination === 'domestic'
  ? new FlatRateStrategy(10)
  : new WeightBasedStrategy(2.5);

const checkout = new CheckoutService(strategy);
const total = checkout.getTotal(order);
