// Separate read database with Redis (TypeScript)
// Source: https://stackpractices.com/recipes/cqrs-pattern-recipe/

import type { Event } from './command-handler';

export interface OrderSummary {
  orderId: string;
  customerName: string;
  totalAmount: number;
  itemCount: number;
  status: string;
}

interface OrderCreatedPayload {
  customerName: string;
  total: number;
  items: Array<{ productId: string; quantity: number; price: number }>;
}

export interface RedisClient {
  hgetall(key: string): Promise<Record<string, string>>;
  hset(key: string, fields: Record<string, string>): Promise<number>;
}

export class OrderReadModelRedis {
  constructor(private redis: RedisClient) {}

  async getOrderSummary(orderId: string): Promise<OrderSummary | null> {
    const data = await this.redis.hgetall(`order:${orderId}:summary`);
    if (!data || Object.keys(data).length === 0) return null;

    return {
      orderId,
      customerName: data.customerName,
      totalAmount: parseFloat(data.totalAmount),
      itemCount: parseInt(data.itemCount, 10),
      status: data.status,
    };
  }

  async handleOrderCreated(event: Event): Promise<void> {
    const payload = event.payload as OrderCreatedPayload;
    await this.redis.hset(`order:${event.aggregateId}:summary`, {
      customerName: payload.customerName,
      totalAmount: payload.total.toString(),
      itemCount: payload.items.length.toString(),
      status: 'pending',
    });
  }

  async handleOrderPaid(event: Event): Promise<void> {
    await this.redis.hset(`order:${event.aggregateId}:summary`, {
      status: 'paid',
    });
  }
}
