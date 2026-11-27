interface PricingStrategy {
  calculate(order: Order): Money;
}

class BasePricingStrategy implements PricingStrategy {
  calculate(order: Order): Money {
    return order.items.reduce(
      (total, item) => total.add(item.price),
      Money.zero('USD')
    );
  }
}

class DiscountDecorator implements PricingStrategy {
  constructor(
    private wrapped: PricingStrategy,
    private discountPercentage: number
  ) {}

  calculate(order: Order): Money {
    const base = this.wrapped.calculate(order);
    const discount = base.multiply(this.discountPercentage / 100);
    return base.subtract(discount);
  }
}

class TaxDecorator implements PricingStrategy {
  constructor(
    private wrapped: PricingStrategy,
    private taxRate: number
  ) {}

  calculate(order: Order): Money {
    const base = this.wrapped.calculate(order);
    const tax = base.multiply(this.taxRate / 100);
    return base.add(tax);
  }
}

class FreeShippingDecorator implements PricingStrategy {
  constructor(
    private wrapped: PricingStrategy,
    private threshold: number
  ) {}

  calculate(order: Order): Money {
    const base = this.wrapped.calculate(order);
    if (base.amount > this.threshold) {
      return base;
    }
    return base.add(new Money(10, 'USD'));
  }
}

// Compose — stack decorators to build the final strategy
const pricing = new FreeShippingDecorator(
  new TaxDecorator(
    new DiscountDecorator(
      new BasePricingStrategy(),
      10
    ),
    8
  ),
  100
);

const total = pricing.calculate(order);
