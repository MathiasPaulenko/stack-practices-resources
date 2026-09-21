// Composite Entity Pattern — Order + LineItem + ShippingAddress persisted
// as one unit across three tables.
//
// Works with an async sqlite wrapper exposing get/all/run/exec
// (e.g. `sqlite` + `sqlite3`, or a thin better-sqlite3 adapter).

class LineItem {
  constructor(productId, quantity, unitPrice) {
    this.productId = productId;
    this.quantity = quantity;
    this.unitPrice = unitPrice;
  }

  get total() {
    return this.quantity * this.unitPrice;
  }
}

class ShippingAddress {
  constructor(street, city, country, postalCode) {
    this.street = street;
    this.city = city;
    this.country = country;
    this.postalCode = postalCode;
  }
}

class Order {
  constructor(orderId, customerId) {
    this.orderId = orderId;
    this.customerId = customerId;
    this.lineItems = [];
    this.shippingAddress = null;
  }

  get total() {
    return this.lineItems.reduce((sum, item) => sum + item.total, 0);
  }
}

class OrderMapper {
  constructor(db) {
    this.db = db;
  }

  async findById(orderId) {
    const row = await this.db.get(
      'SELECT customer_id FROM orders WHERE order_id = ?',
      orderId
    );
    if (!row) return null;

    const order = new Order(orderId, row.customer_id);

    const items = await this.db.all(
      'SELECT product_id, quantity, unit_price FROM line_items WHERE order_id = ?',
      orderId
    );
    for (const item of items) {
      order.lineItems.push(
        new LineItem(item.product_id, item.quantity, item.unit_price)
      );
    }

    const addr = await this.db.get(
      'SELECT street, city, country, postal_code FROM shipping_addresses WHERE order_id = ?',
      orderId
    );
    if (addr) {
      order.shippingAddress = new ShippingAddress(
        addr.street, addr.city, addr.country, addr.postal_code
      );
    }

    return order;
  }

  async save(order) {
    // One transaction keeps the three tables consistent.
    await this.db.exec('BEGIN');
    try {
      await this.db.run(
        'INSERT OR REPLACE INTO orders (order_id, customer_id) VALUES (?, ?)',
        order.orderId, order.customerId
      );
      // Delete-then-insert: simplest correct way to handle orphans.
      await this.db.run('DELETE FROM line_items WHERE order_id = ?', order.orderId);
      for (const item of order.lineItems) {
        await this.db.run(
          'INSERT INTO line_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
          order.orderId, item.productId, item.quantity, item.unitPrice
        );
      }
      if (order.shippingAddress) {
        await this.db.run(
          'INSERT OR REPLACE INTO shipping_addresses (order_id, street, city, country, postal_code) VALUES (?, ?, ?, ?, ?)',
          order.orderId, order.shippingAddress.street, order.shippingAddress.city,
          order.shippingAddress.country, order.shippingAddress.postalCode
        );
      }
      await this.db.exec('COMMIT');
    } catch (err) {
      await this.db.exec('ROLLBACK');
      throw err;
    }
  }
}

// --- Usage example (uncomment and point at a real db handle) ---
// const mapper = new OrderMapper(db);
// const order = new Order('ORD-001', 'CUST-001');
// order.lineItems.push(new LineItem('PROD-1', 2, 29.99));
// order.lineItems.push(new LineItem('PROD-2', 1, 49.99));
// order.shippingAddress = new ShippingAddress('123 Main St', 'Springfield', 'USA', '62701');
// await mapper.save(order);
// const loaded = await mapper.findById('ORD-001');
// console.log('Order total: $' + loaded.total.toFixed(2));

module.exports = { LineItem, ShippingAddress, Order, OrderMapper };
