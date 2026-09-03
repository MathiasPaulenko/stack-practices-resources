import java.time.Instant;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Idempotent Consumer Pattern — Java implementation with in-memory + DB dedup.
 * Uses ConcurrentHashMap as a hot cache and a repository for persistence.
 */
public class IdempotentConsumer {

    private final Set<String> processedIds = ConcurrentHashMap.newKeySet();
    private final ProcessedMessageRepository repository;
    private final OrderService orderService;

    public IdempotentConsumer(ProcessedMessageRepository repository,
                               OrderService orderService) {
        this.repository = repository;
        this.orderService = orderService;
        processedIds.addAll(repository.findRecentIds());
    }

    public String consumeOrderEvent(OrderEvent event) {
        String eventId = event.getEventId();

        if (processedIds.contains(eventId) || repository.existsByEventId(eventId)) {
            processedIds.add(eventId);
            return "Skipping duplicate: " + eventId;
        }

        String result = orderService.upsertOrder(
            event.getOrderId(),
            event.getAmount(),
            event.getStatus()
        );

        repository.save(new ProcessedMessage(eventId));
        processedIds.add(eventId);
        return result;
    }

    // --- Supporting classes ---

    public static class OrderEvent {
        private final String eventId;
        private final String orderId;
        private final double amount;
        private final String status;

        public OrderEvent(String eventId, String orderId, double amount, String status) {
            this.eventId = eventId;
            this.orderId = orderId;
            this.amount = amount;
            this.status = status;
        }

        public String getEventId() { return eventId; }
        public String getOrderId() { return orderId; }
        public double getAmount() { return amount; }
        public String getStatus() { return status; }
    }

    public static class ProcessedMessage {
        private final String eventId;
        private final Instant processedAt;

        public ProcessedMessage(String eventId) {
            this.eventId = eventId;
            this.processedAt = Instant.now();
        }

        public String getEventId() { return eventId; }
        public Instant getProcessedAt() { return processedAt; }
    }

    public interface ProcessedMessageRepository {
        boolean existsByEventId(String eventId);
        void save(ProcessedMessage message);
        Set<String> findRecentIds();
    }

    public interface OrderService {
        String upsertOrder(String orderId, double amount, String status);
    }

    // --- Simple in-memory implementations for testing ---

    public static class InMemoryRepository implements ProcessedMessageRepository {
        private final Set<String> ids = ConcurrentHashMap.newKeySet();

        @Override
        public boolean existsByEventId(String eventId) {
            return ids.contains(eventId);
        }

        @Override
        public void save(ProcessedMessage message) {
            ids.add(message.getEventId());
        }

        @Override
        public Set<String> findRecentIds() {
            return Set.copyOf(ids);
        }
    }

    public static class SimpleOrderService implements OrderService {
        @Override
        public String upsertOrder(String orderId, double amount, String status) {
            return String.format("Upserted order %s: $%.2f (%s)", orderId, amount, status);
        }
    }

    public static void main(String[] args) {
        InMemoryRepository repo = new InMemoryRepository();
        SimpleOrderService service = new SimpleOrderService();
        IdempotentConsumer consumer = new IdempotentConsumer(repo, service);

        OrderEvent[] events = {
            new OrderEvent("msg-1", "ord-100", 49.99, "confirmed"),
            new OrderEvent("msg-2", "ord-101", 12.50, "pending"),
            new OrderEvent("msg-1", "ord-100", 49.99, "confirmed"),
        };

        for (OrderEvent event : events) {
            System.out.println(consumer.consumeOrderEvent(event));
        }
    }
}
