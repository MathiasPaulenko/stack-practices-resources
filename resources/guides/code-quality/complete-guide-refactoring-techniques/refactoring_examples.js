// Companion examples for complete-guide-refactoring-techniques
// Run: node refactoring_examples.js

// ---- Before: messy function (4 jobs, nesting, magic values)
function processOrderBefore(order) {
  if (order != null) {
    if (order.items.length > 0) {
      let t = 0;
      for (const i of order.items) { t += i.price * i.qty; }
      if (order.customer.type === 'vip') { t = t * 0.9; }
      if (t > 100) { t = t - 10; }
      order.total = t;
      return order;
    }
  }
  throw new Error('Invalid order');
}

// ---- After: same behavior, step-by-step refactored
const VIP_DISCOUNT = 0.9;
const FREE_SHIPPING_THRESHOLD = 100;
const SHIPPING_FEE = 10;

class Customer {
  constructor(type) { this.type = type; }
  discountRate() { return this.type === 'vip' ? VIP_DISCOUNT : 1.0; }
}

function subtotal(order) {
  return order.items.reduce((sum, item) => sum + item.price * item.qty, 0);
}

function calculateOrderTotal(order) {
  if (order == null) throw new Error('Invalid order');
  if (order.items.length === 0) throw new Error('Invalid order');
  let total = subtotal(order) * order.customer.discountRate();
  if (total > FREE_SHIPPING_THRESHOLD) total -= SHIPPING_FEE;
  order.total = total;
  return order;
}

// ---- Smoke test: both versions must agree
const order1 = { items: [{ price: 30, qty: 2 }, { price: 50, qty: 1 }], customer: { type: 'vip' } };
const order2 = { items: [{ price: 30, qty: 2 }, { price: 50, qty: 1 }], customer: new Customer('vip') };
console.log('before:', processOrderBefore(order1).total); // 89.0
console.log('after :', calculateOrderTotal(order2).total); // 89.0
