// Context Object Pattern — runnable demo (Node.js 18+).
// Boundary builds one immutable context; layers read it without extra params.

class RequestContext {
  constructor({ userId = null, correlationId = null, metadata = new Map() } = {}) {
    this.requestId = crypto.randomUUID();
    this.timestamp = new Date();
    this.userId = userId;
    this.correlationId = correlationId;
    this.metadata = metadata;
    Object.freeze(this);
  }

  withUser(userId) {
    return new RequestContext({
      userId,
      correlationId: this.correlationId,
      metadata: new Map(this.metadata),
    });
  }
}

class OrderService {
  processOrder(ctx, orderData) {
    console.log(`[${ctx.requestId}] Order for ${ctx.userId}`);
    return { ...orderData, orderId: 'ORD-123' };
  }
}

class RequestHandler {
  constructor(service) { this.service = service; }
  handleRequest(raw) {
    const ctx = new RequestContext({
      userId: raw.user_id,
      correlationId: raw.correlation_id,
    });
    return this.service.processOrder(ctx, raw.order_data || {});
  }
}

const handler = new RequestHandler(new OrderService());
const result = handler.handleRequest({
  user_id: 'user-42',
  correlation_id: 'corr-abc',
  order_data: { items: ['book', 'pen'] },
});
console.log(result.orderId === 'ORD-123' ? 'context-object-pattern OK' : 'FAIL');
