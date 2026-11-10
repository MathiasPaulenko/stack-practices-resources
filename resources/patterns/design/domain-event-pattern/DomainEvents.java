import java.time.Instant;
import java.util.*;

/**
 * Domain Event pattern: immutable event record + aggregate + in-memory publisher.
 * Run: javac DomainEvents.java && java DomainEvents
 */
public class DomainEvents {

    public record DomainEvent(
        UUID eventId,
        Instant occurredAt,
        String aggregateId,
        String eventType,
        Map<String, Object> payload
    ) {
        public DomainEvent(String aggregateId, String eventType, Map<String, Object> payload) {
            this(UUID.randomUUID(), Instant.now(), aggregateId, eventType, payload);
        }
    }

    static class EventPublisher {
        private static final List<java.util.function.Consumer<DomainEvent>> handlers = new ArrayList<>();

        public static void subscribe(java.util.function.Consumer<DomainEvent> handler) {
            handlers.add(handler);
        }

        public static void publish(DomainEvent event) {
            handlers.forEach(h -> h.accept(event));
        }
    }

    static class Order {
        private final UUID id = UUID.randomUUID();
        private final String customerId;
        private final List<Map<String, Object>> lines = new ArrayList<>();
        private String status = "pending";
        private final List<DomainEvent> events = new ArrayList<>();

        public Order(String customerId) {
            this.customerId = customerId;
        }

        public void addLine(String productId, int quantity, double price) {
            lines.add(Map.of("product_id", productId, "quantity", quantity, "price", price));
        }

        public void submit() {
            if (lines.isEmpty()) throw new IllegalStateException("Cannot submit empty order");
            status = "submitted";
            events.add(new DomainEvent(
                id.toString(), "OrderSubmitted",
                Map.of("customer_id", customerId, "line_count", lines.size())
            ));
        }

        public List<DomainEvent> clearEvents() {
            List<DomainEvent> result = new ArrayList<>(events);
            events.clear();
            return result;
        }
    }

    public static void main(String[] args) {
        EventPublisher.subscribe(e ->
            System.out.println("  [email] order " + e.aggregateId().substring(0, 8) + " confirmed"));
        EventPublisher.subscribe(e ->
            System.out.println("  [analytics] tracked " + e.eventType() + " " + e.payload()));

        Order order = new Order("cust-123");
        order.addLine("prod-1", 2, 9.99);
        order.submit();
        order.clearEvents().forEach(EventPublisher::publish);
    }
}
