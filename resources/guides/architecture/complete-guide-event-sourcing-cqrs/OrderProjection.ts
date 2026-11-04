// OrderProjection.ts — Build the read model from domain events
class OrderProjection {
  constructor(private readonly readDb: ReadDatabase) {}

  async handle(event: DomainEvent): Promise<void> {
    switch (event.eventType) {
      case 'OrderPlaced':
        await this.readDb.execute(
          `INSERT INTO read_orders (id, customer_id, status, total_amount, item_count, created_at)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [event.aggregateId, event.data.customerId, 'pending',
           event.data.totalAmount, event.data.items.length, event.timestamp],
        );
        break;
      case 'OrderCancelled':
        await this.readDb.execute(
          `UPDATE read_orders SET status = $1, cancelled_at = $2 WHERE id = $3`,
          ['cancelled', event.timestamp, event.aggregateId],
        );
        break;
      case 'OrderShipped':
        await this.readDb.execute(
          `UPDATE read_orders SET status = $1, shipped_at = $2, tracking_number = $3 WHERE id = $4`,
          ['shipped', event.timestamp, event.data.trackingNumber, event.aggregateId],
        );
        break;
    }
  }
}
