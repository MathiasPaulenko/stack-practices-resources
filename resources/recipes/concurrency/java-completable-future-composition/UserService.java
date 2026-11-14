import java.util.List;
import java.util.concurrent.CompletableFuture;

import static java.util.Collections.emptyList;

/**
 * Service layer used by the composition examples: the fetch* methods wrap
 * AsyncApiClient.fetchAsync with JSON parsing into domain records.
 */
public class UserService {

    public static CompletableFuture<User> fetchUser(String userId) {
        return AsyncApiClient.fetchAsync("https://api.example.com/users/" + userId)
            .thenApply(UserService::parseUser);
    }

    public static CompletableFuture<List<Order>> fetchOrders(String userId) {
        return AsyncApiClient.fetchAsync("https://api.example.com/users/" + userId + "/orders")
            .thenApply(UserService::parseOrders);
    }

    public static CompletableFuture<List<Notification>> fetchNotifications(String userId) {
        return AsyncApiClient.fetchAsync("https://api.example.com/users/" + userId + "/notifications")
            .thenApply(UserService::parseNotifications);
    }

    // Minimal parsing stubs — replace with Jackson/Gson in a real service.
    static User parseUser(String json) {
        String id = extract(json, "id");
        String name = extract(json, "name");
        return new User(id, name);
    }

    static List<Order> parseOrders(String json) {
        if (json == null || json.isBlank()) {
            return emptyList();
        }
        return List.of(new Order("o1", extract(json, "userId"), 42.0));
    }

    static List<Notification> parseNotifications(String json) {
        if (json == null || json.isBlank()) {
            return emptyList();
        }
        return List.of(new Notification("n1", json));
    }

    private static String extract(String json, String field) {
        int i = json.indexOf("\"" + field + "\"");
        if (i < 0) return "";
        int colon = json.indexOf(':', i);
        int start = json.indexOf('"', colon + 1) + 1;
        int end = json.indexOf('"', start);
        return json.substring(start, end);
    }
}
