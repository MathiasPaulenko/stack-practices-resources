class CreditCardPayment {
  pay(amount) {
    return `Paid $${amount} with Credit Card`;
  }
}

class PayPalPayment {
  pay(amount) {
    return `Paid $${amount} via PayPal`;
  }
}

class Checkout {
  constructor(strategy) {
    this.strategy = strategy;
  }

  process(amount) {
    return this.strategy.pay(amount);
  }
}

// Usage
const checkout = new Checkout(new CreditCardPayment());
console.log(checkout.process(100));
checkout.strategy = new PayPalPayment();
console.log(checkout.process(50));
