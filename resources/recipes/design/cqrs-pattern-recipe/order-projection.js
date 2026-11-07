// Event handler updating the read model (Node.js)
// Source: https://stackpractices.com/recipes/cqrs-pattern-recipe/

class OrderProjection {
  constructor(readDb, elasticsearch) {
    this.readDb = readDb;
    this.elasticsearch = elasticsearch;
  }

  async handleOrderPaid(event) {
    // Update relational read model
    await this.readDb.query(
      'UPDATE order_summaries SET status = $1, last_updated = $2 WHERE order_id = $3',
      ['paid', event.occurredAt, event.aggregateId]
    );

    // Update search index
    await this.elasticsearch.update({
      index: 'orders',
      id: event.aggregateId,
      doc: { status: 'paid', paidAt: event.occurredAt }
    });
  }

  async handleOrderCreated(event) {
    await this.readDb.query(
      `INSERT INTO order_summaries (order_id, customer_name, total_amount, item_count, status, last_updated)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [event.aggregateId, event.payload.customerName, event.payload.total,
       event.payload.items.length, 'pending', event.occurredAt]
    );
  }
}

module.exports = { OrderProjection };
