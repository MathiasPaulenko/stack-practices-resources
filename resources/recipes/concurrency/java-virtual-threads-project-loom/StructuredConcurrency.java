import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Subtask;

// JDK 25+ with --enable-preview (JEP 505).
// On JDK 21–24 use new StructuredTaskScope.ShutdownOnFailure() instead.
public class StructuredConcurrency {
    record User(String name, String email) {}
    record Order(String id, double total) {}
    record UserOrder(User user, Order order) {}

    static User fetchUser(String userId) throws InterruptedException {
        Thread.sleep(100);
        return new User("Alice", "alice@example.com");
    }

    static Order fetchOrder(String orderId) throws InterruptedException {
        Thread.sleep(150);
        return new Order("ord-123", 99.99);
    }

    public static void main(String[] args) throws Exception {
        // open() gives the default policy: wait for all subtasks,
        // cancel everything and throw if any one fails.
        try (var scope = StructuredTaskScope.open()) {

            Subtask<User> userTask = scope.fork(() -> fetchUser("u1"));
            Subtask<Order> orderTask = scope.fork(() -> fetchOrder("o1"));

            scope.join(); // waits for all; throws FailedException on failure

            UserOrder result = new UserOrder(userTask.get(), orderTask.get());
            System.out.println("Result: " + result);

        } catch (StructuredTaskScope.FailedException e) {
            System.err.println("A subtask failed: " + e.getCause());
        }
    }
}
