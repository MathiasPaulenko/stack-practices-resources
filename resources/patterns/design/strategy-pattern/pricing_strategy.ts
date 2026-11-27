// Strategy pattern: swap algorithms at runtime
interface PricingStrategy {
  calculate(basePrice: number, context: PricingContext): number;
}

interface PricingContext {
  userAge?: number;
  isMember?: boolean;
  orderCount?: number;
  isHoliday?: boolean;
}

class RegularPricing implements PricingStrategy {
  calculate(basePrice: number): number { return basePrice; }
}

class MemberDiscountPricing implements PricingStrategy {
  calculate(basePrice: number, ctx: PricingContext): number {
    const discount = ctx.orderCount > 10 ? 0.20 : 0.10;
    return basePrice * (1 - discount);
  }
}

class SeniorDiscountPricing implements PricingStrategy {
  calculate(basePrice: number, ctx: PricingContext): number {
    if (ctx.userAge >= 65) return basePrice * 0.85;
    return basePrice;
  }
}

class HolidayPricing implements PricingStrategy {
  calculate(basePrice: number, ctx: PricingContext): number {
    if (ctx.isHoliday) return basePrice * 0.90;
    return basePrice;
  }
}

// Context: uses the active strategy
class PricingService {
  private strategy: PricingStrategy;

  constructor(strategy: PricingStrategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy: PricingStrategy) {
    this.strategy = strategy;
  }

  calculatePrice(basePrice: number, ctx: PricingContext): number {
    return this.strategy.calculate(basePrice, ctx);
  }
}

// Usage: switch strategy at runtime
const pricing = new PricingService(new RegularPricing());

// Regular customer
console.log(pricing.calculatePrice(100, {})); // 100

// Switch to member discount
pricing.setStrategy(new MemberDiscountPricing());
console.log(pricing.calculatePrice(100, { orderCount: 15 })); // 80

// Switch to senior
pricing.setStrategy(new SeniorDiscountPricing());
console.log(pricing.calculatePrice(100, { userAge: 70 })); // 85

// Combine strategies (composite)
class CompositePricing implements PricingStrategy {
  constructor(private strategies: PricingStrategy[]) {}
  calculate(basePrice: number, ctx: PricingContext): number {
    return this.strategies.reduce(
      (price, s) => s.calculate(price, ctx),
      basePrice
    );
  }
}

// Apply member + holiday
const composite = new CompositePricing([
  new MemberDiscountPricing(),
  new HolidayPricing(),
]);
console.log(composite.calculate(100, { orderCount: 15, isHoliday: true })); // 72
