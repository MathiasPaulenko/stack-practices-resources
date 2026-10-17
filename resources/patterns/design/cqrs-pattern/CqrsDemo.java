// CQRS Pattern — Java demo
// Write model enforces invariants; query model serves flat DTOs.
// Compile: javac CqrsDemo.java && java CqrsDemo

import java.util.*;

// Write Model — domain entity enforces invariants
class Order {
    String orderId;
    String customerId;
    List<Item> items = new ArrayList<>();
    String status = "pending";
    String createdAt = new Date().toString();

    record Item(String product, int qty, double price) {}

    void confirm() {
        if (items.isEmpty()) throw new IllegalStateException("Cannot confirm empty order");
        this.status = "confirmed";
    }
}

class OrderCommandHandler {
    private final Map<String, Order> orders = new HashMap<>();

    public void createOrder(String orderId, String customerId) {
        Order o = new Order();
        o.orderId = orderId;
        o.customerId = customerId;
        orders.put(orderId, o);
    }

    public void addItem(String orderId, String product, int qty, double price) {
        orders.get(orderId).items.add(new Order.Item(product, qty, price));
    }

    public void confirm(String orderId) {
        orders.get(orderId).confirm();
    }

    public Map<String, Order> getStore() { return orders; }
}

// Read Model — flat DTO, no behavior
class OrderSummary {
    public String orderId;
    public String customerId;
    public double total;
    public int itemCount;
    public String status;
}

class OrderQueryHandler {
    private final Map<String, Order> store;

    public OrderQueryHandler(Map<String, Order> store) {
        this.store = store;
    }

    public OrderSummary getSummary(String orderId) {
        Order o = store.get(orderId);
        OrderSummary s = new OrderSummary();
        s.orderId = o.orderId;
        s.customerId = o.customerId;
        s.total = o.items.stream().mapToDouble(i -> i.qty() * i.price()).sum();
        s.itemCount = o.items.size();
        s.status = o.status;
        return s;
    }
}

public class CqrsDemo {
    public static void main(String[] args) {
        OrderCommandHandler commands = new OrderCommandHandler();
        commands.createOrder("ORD-1", "CUST-1");
        commands.addItem("ORD-1", "Laptop", 1, 999.99);
        commands.confirm("ORD-1");

        OrderQueryHandler queries = new OrderQueryHandler(commands.getStore());
        System.out.println("Total: " + queries.getSummary("ORD-1").total);
    }
}
