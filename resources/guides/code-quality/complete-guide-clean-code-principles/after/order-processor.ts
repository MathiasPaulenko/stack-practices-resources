// AFTER — the same logic, refactored with the guide's principles:
// small functions, single responsibility, named constants,
// exceptions instead of codes, no argument mutation.

type Item = { price: number; category: 'food' | 'electronics' | string };
type Customer = { email: string; isVip: boolean };
type Order = { id: string; items: Item[]; total: number; customer: Customer };

const TAX_RATES: Record<string, number> = {
  food: 0.05,
  electronics: 0.18,
  default: 0.1,
};
const VIP_DISCOUNT = 0.9;

export class EmptyOrderError extends Error {}
export class InvalidOrderError extends Error {}

export class TaxCalculator {
  calculate(items: Item[]): number {
    return items.reduce(
      (sum, item) => sum + item.price * (TAX_RATES[item.category] ?? TAX_RATES.default),
      0,
    );
  }
}

export class OrderValidator {
  validate(order: Order): void {
    if (!order.items || order.items.length === 0) {
      throw new EmptyOrderError('Order has no items');
    }
    if (order.total <= 0) {
      throw new InvalidOrderError('Order total must be positive');
    }
  }
}

export class OrderProcessor {
  constructor(
    private readonly validator: OrderValidator,
    private readonly taxCalculator: TaxCalculator,
    private readonly orderRepository: { save(order: Order): void },
    private readonly mailer: { send(to: string, subject: string): void },
  ) {}

  process(order: Order): void {
    this.validator.validate(order);
    const tax = this.taxCalculator.calculate(order.items);
    const finalOrder = { ...order, total: order.total * VIP_DISCOUNT + tax };
    this.orderRepository.save(finalOrder);
    this.mailer.send(order.customer.email, 'Order confirmed');
  }
}
