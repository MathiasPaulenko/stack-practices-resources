import type { Order } from '../domain/order';

export interface DiscountStrategy {
  apply(order: Order): number;
}

export class NoDiscount implements DiscountStrategy {
  apply(order: Order): number {
    return order.total;
  }
}

export class PercentageDiscount implements DiscountStrategy {
  constructor(private percent: number) {}
  apply(order: Order): number {
    return order.total * (1 - this.percent / 100);
  }
}
