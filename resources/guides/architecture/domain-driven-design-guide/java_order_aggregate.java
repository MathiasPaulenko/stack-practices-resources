// Java aggregate root example: Order with invariant enforcement.
// Compile: javac java_order_aggregate.java
// Run: java OrderDemo

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

enum OrderStatus {
    PENDING, CONFIRMED, SHIPPED, CANCELLED
}

final class Money {
    private final BigDecimal amount;
    private final String currency;

    public Money(BigDecimal amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    public Money add(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalArgumentException("Currency mismatch");
        return new Money(amount.add(other.amount), currency);
    }

    public Money multiply(int factor) {
        return new Money(amount.multiply(BigDecimal.valueOf(factor)), currency);
    }

    public BigDecimal getAmount() { return amount; }
    public String getCurrency() { return currency; }

    public static Money ZERO(String currency) {
        return new Money(BigDecimal.ZERO, currency);
    }
}

class OrderLine {
    private final String productId;
    private final int quantity;
    private final Money unitPrice;

    public OrderLine(String productId, int quantity, Money unitPrice) {
        if (quantity <= 0) throw new IllegalArgumentException("Quantity must be positive");
        this.productId = productId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    public Money total() { return unitPrice.multiply(quantity); }
}

class DomainException extends RuntimeException {
    public DomainException(String message) { super(message); }
}

class Order {
    private final String orderId;
    private final String customerId;
    private final List<OrderLine> lines = new ArrayList<>();
    private OrderStatus status = OrderStatus.PENDING;

    public Order(String orderId, String customerId) {
        this.orderId = orderId;
        this.customerId = customerId;
    }

    public OrderStatus getStatus() { return status; }

    public void addLine(String productId, int quantity, Money unitPrice) {
        if (status != OrderStatus.PENDING)
            throw new DomainException("Cannot modify confirmed order");
        if (lines.size() >= 50)
            throw new DomainException("Max 50 items per order");
        lines.add(new OrderLine(productId, quantity, unitPrice));
    }

    public Money total() {
        Money result = Money.ZERO("USD");
        for (OrderLine line : lines) {
            result = result.add(line.total());
        }
        return result;
    }

    public void confirm() {
        if (lines.isEmpty())
            throw new DomainException("Cannot confirm empty order");
        if (total().getAmount().compareTo(BigDecimal.ZERO) <= 0)
            throw new DomainException("Total must be positive");
        status = OrderStatus.CONFIRMED;
    }
}

public class java_order_aggregate {
    public static void main(String[] args) {
        Order order = new Order("order-001", "customer-123");
        order.addLine("prod-1", 2, new Money(new BigDecimal("15"), "USD"));
        order.addLine("prod-2", 1, new Money(new BigDecimal("30"), "USD"));
        System.out.println("Total: " + order.total().getAmount() + " " + order.total().getCurrency());
        order.confirm();
        System.out.println("Status: " + order.getStatus());
    }
}
