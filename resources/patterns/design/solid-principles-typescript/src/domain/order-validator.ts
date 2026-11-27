import type { Order } from './order';

export class OrderValidator {
  validate(order: Order): string[] {
    const errors: string[] = [];
    if (order.items.length === 0) errors.push('Order must have items');
    if (order.total <= 0) errors.push('Total must be positive');
    return errors;
  }
}
