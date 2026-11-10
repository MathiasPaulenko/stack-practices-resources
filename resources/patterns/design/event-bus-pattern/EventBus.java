import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

/**
 * Event Bus pattern: lock-free dispatch with CopyOnWriteArrayList so
 * (un)subscription during publish() can never throw
 * ConcurrentModificationException.
 *
 * Compile/run: javac EventBus.java && java EventBus
 */
public class EventBus {
    public record Event(String type, Map<String, Object> payload) {}

    private final Map<String, List<Consumer<Event>>> subscribers = new ConcurrentHashMap<>();

    public void subscribe(String eventType, Consumer<Event> handler) {
        subscribers.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>()).add(handler);
    }

    public void unsubscribe(String eventType, Consumer<Event> handler) {
        List<Consumer<Event>> list = subscribers.get(eventType);
        if (list != null) list.remove(handler);
    }

    public void publish(Event event) {
        for (Consumer<Event> handler : subscribers.getOrDefault(event.type(), List.of())) {
            try {
                handler.accept(event);
            } catch (Exception e) {
                System.err.println("[BUS] handler error for " + event.type() + ": " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        EventBus bus = new EventBus();
        Consumer<Event> email = e -> System.out.println("email -> " + e.payload().get("user_id"));
        Consumer<Event> analytics = e -> System.out.println("analytics -> " + e.payload().get("user_id"));

        bus.subscribe("UserRegistered", email);
        bus.subscribe("UserRegistered", analytics);
        bus.publish(new Event("UserRegistered", Map.of("user_id", 42, "email", "alice@example.com")));

        bus.unsubscribe("UserRegistered", analytics);
        bus.publish(new Event("UserRegistered", Map.of("user_id", 43, "email", "bob@example.com")));
    }
}
