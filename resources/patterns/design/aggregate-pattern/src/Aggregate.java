import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

class Order {
    private final UUID id;
    private final String customerId;
    private final List<OrderLine> lines = new ArrayList<>();
    private String status = "pending";
    private final Instant createdAt;
    private int version = 0;

    public Order(String customerId) {
        this.id = UUID.randomUUID();
        this.customerId = customerId;
        this.createdAt = Instant.now();
    }

    public void addLine(String productId, int quantity, double unitPrice) {
        if (quantity <= 0) throw new IllegalArgumentException("Quantity must be positive");
        if (!"pending".equals(status)) throw new IllegalStateException("Can't modify a non-pending order");
        lines.add(new OrderLine(productId, quantity, unitPrice));
        version++;
    }

    public void removeLine(String productId) {
        if (!"pending".equals(status)) throw new IllegalStateException("Can't modify a non-pending order");
        lines.removeIf(line -> line.productId().equals(productId));
        version++;
    }

    public double total() {
        return lines.stream().mapToDouble(OrderLine::total).sum();
    }

    public void submit() {
        if (lines.isEmpty()) throw new IllegalStateException("Can't submit an empty order");
        status = "submitted";
        version++;
    }

    public UUID getId() { return id; }
    public String getStatus() { return status; }
    public int getVersion() { return version; }

    public static void main(String[] args) {
        Order order = new Order("cust-123");
        order.addLine("prod-1", 2, 9.99);
        order.addLine("prod-2", 1, 19.99);
        System.out.printf("Total: %.2f%n", order.total()); // 39.97
        order.submit();
        System.out.println("Order " + order.getId() + " status: " + order.getStatus());
    }
}

record OrderLine(String productId, int quantity, double unitPrice) {
    public double total() { return quantity * unitPrice; }
}
