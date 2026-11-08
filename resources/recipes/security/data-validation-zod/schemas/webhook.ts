// Discriminated union for polymorphic webhook payloads — Zod 4 API.
import { z } from 'zod';

export const OrderCreatedEvent = z.object({
  type: z.literal('order.created'),
  data: z.object({
    orderId: z.uuid(),
    customerId: z.uuid(),
    amount: z.number().positive(),
    currency: z.string().length(3),
  }),
});

export const OrderRefundedEvent = z.object({
  type: z.literal('order.refunded'),
  data: z.object({
    orderId: z.uuid(),
    refundAmount: z.number().positive(),
    reason: z.string().min(1).max(500),
  }),
});

export const OrderShippedEvent = z.object({
  type: z.literal('order.shipped'),
  data: z.object({
    orderId: z.uuid(),
    carrier: z.string(),
    trackingNumber: z.string(),
    shippedAt: z.coerce.date(),
  }),
});

export const WebhookEvent = z.discriminatedUnion('type', [
  OrderCreatedEvent,
  OrderRefundedEvent,
  OrderShippedEvent,
]);

export type WebhookEvent = z.infer<typeof WebhookEvent>;

export function handleWebhook(event: WebhookEvent) {
  switch (event.type) {
    case 'order.created':
      console.log(`Order ${event.data.orderId} created`);
      break;
    case 'order.refunded':
      console.log(`Refund ${event.data.refundAmount} issued`);
      break;
    case 'order.shipped':
      console.log(`Shipped: ${event.data.trackingNumber}`);
      break;
  }
}
