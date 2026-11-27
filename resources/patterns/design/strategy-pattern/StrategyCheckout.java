interface PaymentStrategy {
    String pay(double amount);
}

class CreditCardPayment implements PaymentStrategy {
    public String pay(double amount) {
        return "Paid $" + amount + " with Credit Card";
    }
}

class PayPalPayment implements PaymentStrategy {
    public String pay(double amount) {
        return "Paid $" + amount + " via PayPal";
    }
}

class Checkout {
    private PaymentStrategy strategy;

    Checkout(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    String process(double amount) {
        return strategy.pay(amount);
    }

    void setStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
}

// Usage
Checkout checkout = new Checkout(new CreditCardPayment());
System.out.println(checkout.process(100));
checkout.setStrategy(new PayPalPayment());
System.out.println(checkout.process(50));
