class Order {
  constructor(customerId) {
    this.id = crypto.randomUUID();
    this.customerId = customerId;
    this.lines = [];
    this.status = 'pending';
    this.createdAt = new Date();
    this.version = 0;
  }

  addLine(productId, quantity, unitPrice) {
    if (quantity <= 0) throw new Error('Quantity must be positive');
    if (this.status !== 'pending') throw new Error("Can't modify a non-pending order");

    this.lines.push({ productId, quantity, unitPrice });
    this.version++;
  }

  removeLine(productId) {
    if (this.status !== 'pending') throw new Error("Can't modify a non-pending order");

    this.lines = this.lines.filter(line => line.productId !== productId);
    this.version++;
  }

  total() {
    return this.lines.reduce((sum, line) => sum + line.quantity * line.unitPrice, 0);
  }

  submit() {
    if (this.lines.length === 0) throw new Error("Can't submit an empty order");
    this.status = 'submitted';
    this.version++;
  }
}

const order = new Order('cust-123');
order.addLine('prod-1', 2, 9.99);
order.addLine('prod-2', 1, 19.99);
console.log(`Total: ${order.total().toFixed(2)}`); // 39.97
order.submit();
console.log(`Order ${order.id} status: ${order.status}`);
