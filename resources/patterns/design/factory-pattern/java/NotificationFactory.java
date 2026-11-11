import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

// Factory Pattern: canonical notification example with a registry.
public class NotificationFactory {

    public interface Notification {
        String send(String message);
    }

    public static class EmailNotification implements Notification {
        public String send(String message) {
            return "Sending email: " + message;
        }
    }

    public static class SmsNotification implements Notification {
        public String send(String message) {
            return "Sending SMS: " + message;
        }
    }

    private static final Map<String, Supplier<Notification>> REGISTRY = new HashMap<>();

    static {
        REGISTRY.put("email", EmailNotification::new);
        REGISTRY.put("sms", SmsNotification::new);
    }

    public static void register(String channel, Supplier<Notification> creator) {
        REGISTRY.put(channel, creator);
    }

    public static Notification create(String channel) {
        Supplier<Notification> creator = REGISTRY.get(channel);
        if (creator == null) {
            throw new IllegalArgumentException("Unknown channel: " + channel);
        }
        return creator.get();
    }

    public static void main(String[] args) {
        Notification notifier = NotificationFactory.create("email");
        System.out.println(notifier.send("Hello!"));

        NotificationFactory.register("push", () -> new Notification() {
            public String send(String message) {
                return "Sending push: " + message;
            }
        });
        System.out.println(NotificationFactory.create("push").send("Hello!"));
    }
}
