import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Event-Carried State Transfer — runnable simulation.
 *
 * A source service publishes events carrying the full updated entity state;
 * a consumer applies them to a local replica and serves reads locally.
 * No dependencies — run with:
 *   javac src/EventCarriedStateTransfer.java && java -cp src EventCarriedStateTransfer
 */
public class EventCarriedStateTransfer {

    record CustomerStateTransferEvent(
        String eventId,
        String eventType,
        String customerId,
        CustomerPayload payload,
        String timestamp,
        int version
    ) {}

    record CustomerPayload(
        String customerId, String name, String email,
        String tier, int loyaltyPoints, String updatedAt
    ) {}

    /** In-memory stand-in for a Kafka topic subscription. */
    static class EventBus {
        private final Map<String, List<Consumer<CustomerStateTransferEvent>>> topics = new HashMap<>();

        void subscribe(String topic, Consumer<CustomerStateTransferEvent> handler) {
            topics.computeIfAbsent(topic, t -> new ArrayList<>()).add(handler);
        }

        void publish(CustomerStateTransferEvent event) {
            String topic = "customer." + event.eventType().toLowerCase();
            topics.getOrDefault(topic, List.of()).forEach(h -> h.accept(event));
        }
    }

    /** Source service: owns customer data and publishes state transfer events. */
    static class CustomerService {
        private final EventBus bus;
        private final Map<String, CustomerPayload> customers = new HashMap<>();
        private int versionCounter = 0;

        CustomerService(EventBus bus) {
            this.bus = bus;
        }

        CustomerPayload createCustomer(String id, String name, String email, String tier) {
            var customer = new CustomerPayload(id, name, email, tier, 0, Instant.now().toString());
            customers.put(id, customer);
            publish("CUSTOMER_CREATED", customer);
            return customer;
        }

        CustomerPayload updateTier(String id, String tier) {
            var existing = customers.get(id);
            if (existing == null) return null;

            var updated = new CustomerPayload(
                existing.customerId(), existing.name(), existing.email(),
                tier, existing.loyaltyPoints(), Instant.now().toString());
            customers.put(id, updated);
            publish("CUSTOMER_UPDATED", updated);
            return updated;
        }

        private void publish(String type, CustomerPayload payload) {
            var event = new CustomerStateTransferEvent(
                "evt-" + versionCounter, type, payload.customerId(),
                payload, Instant.now().toString(), versionCounter++);
            bus.publish(event);
        }
    }

    /** Consumer: maintains a local read-only replica for order processing. */
    static class OrderServiceProjection {
        private final Map<String, CustomerPayload> localReplica = new HashMap<>();

        void onCustomerEvent(CustomerStateTransferEvent event) {
            localReplica.put(event.customerId(), event.payload());
            System.out.println("[OrderService] Replicated customer "
                + event.customerId() + " (v" + event.version() + ")");
        }

        CustomerPayload getCustomerForOrder(String customerId) {
            return localReplica.get(customerId);
        }
    }

    public static void main(String[] args) {
        var bus = new EventBus();
        var customerService = new CustomerService(bus);
        var orderService = new OrderServiceProjection();

        bus.subscribe("customer.customer_created", orderService::onCustomerEvent);
        bus.subscribe("customer.customer_updated", orderService::onCustomerEvent);

        customerService.createCustomer("C-001", "Alice Johnson", "alice@example.com", "premium");
        System.out.println("Order service sees: " + orderService.getCustomerForOrder("C-001"));

        customerService.updateTier("C-001", "gold");
        System.out.println("After update: " + orderService.getCustomerForOrder("C-001"));
    }
}
