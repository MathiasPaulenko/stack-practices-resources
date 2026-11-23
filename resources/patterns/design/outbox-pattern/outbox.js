class OutboxPublisher {
  constructor(db) {
    this.db = db;
  }

  async publish(aggregateType, aggregateId, eventType, payload) {
    await this.db.query(
      `INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
       VALUES ($1, $2, $3, $4)`,
      [aggregateType, aggregateId, eventType, JSON.stringify(payload)]
    );
  }
}

class OrderService {
  constructor(db, outbox) {
    this.db = db;
    this.outbox = outbox;
  }

  async placeOrder(userId, productId, amount) {
    const client = await this.db.connect();
    try {
      await client.query('BEGIN');

      const result = await client.query(
        'INSERT INTO orders (user_id, product_id, amount) VALUES ($1, $2, $3) RETURNING id',
        [userId, productId, amount]
      );
      const orderId = result.rows[0].id;

      await this.outbox.publish('Order', String(orderId), 'OrderPlaced', {
        user_id: userId, product_id: productId, amount
      });

      await client.query('COMMIT');
    } catch (err) {
      await client.query('ROLLBACK');
      throw err;
    } finally {
      client.release();
    }
  }
}

class OutboxRelay {
  constructor(db, broker) {
    this.db = db;
    this.broker = broker;
  }

  async run() {
    const result = await this.db.query(
      `SELECT id, event_type, payload FROM outbox
       WHERE published_at IS NULL ORDER BY id LIMIT 100`
    );

    for (const row of result.rows) {
      try {
        await this.broker.publish(row.event_type, row.payload);
        await this.db.query(
          'UPDATE outbox SET published_at = NOW() WHERE id = $1',
          [row.id]
        );
      } catch (err) {
        await this.db.query(
          'UPDATE outbox SET retry_count = retry_count + 1 WHERE id = $1',
          [row.id]
        );
      }
    }
  }
}
