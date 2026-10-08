import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * CompletableFuture pipeline demo: sequential composition with thenCompose,
 * parallel combination with thenCombine, and a single exceptionally() catch-all.
 *
 * Self-contained so it compiles and runs: javac AsyncOrderService.java && java AsyncOrderService
 */
public class AsyncOrderService {

    record Order(String id, String status) {}
    record ValidatedOrder(String id) {}
    record Profile(String userId, String name) {}
    record Dashboard(Profile profile, List<Order> orders) {}

    public CompletableFuture<Order> processOrder(String orderId) {
        return validateOrder(orderId)
            .thenCompose(this::checkInventory)
            .thenCompose(this::processPayment)
            .thenCompose(this::createShipment)
            .exceptionally(ex -> {
                System.err.println("Order processing failed: " + ex.getMessage());
                return new Order(orderId, "FAILED");
            });
    }

    private CompletableFuture<ValidatedOrder> validateOrder(String orderId) {
        return CompletableFuture.supplyAsync(() -> new ValidatedOrder(orderId));
    }

    private CompletableFuture<ValidatedOrder> checkInventory(ValidatedOrder order) {
        return CompletableFuture.supplyAsync(() -> order);
    }

    private CompletableFuture<ValidatedOrder> processPayment(ValidatedOrder order) {
        return CompletableFuture.supplyAsync(() -> order);
    }

    private CompletableFuture<Order> createShipment(ValidatedOrder order) {
        return CompletableFuture.supplyAsync(() -> new Order(order.id(), "SHIPPED"));
    }

    public CompletableFuture<Dashboard> loadDashboard(String userId) {
        CompletableFuture<Profile> profileFuture = fetchProfile(userId);
        CompletableFuture<List<Order>> ordersFuture = fetchOrders(userId);
        return profileFuture.thenCombine(ordersFuture, Dashboard::new);
    }

    private CompletableFuture<Profile> fetchProfile(String userId) {
        return CompletableFuture.supplyAsync(() -> new Profile(userId, "user-" + userId));
    }

    private CompletableFuture<List<Order>> fetchOrders(String userId) {
        return CompletableFuture.supplyAsync(() -> List.of(new Order("o-1", "DONE")));
    }

    public static void main(String[] args) {
        AsyncOrderService service = new AsyncOrderService();
        System.out.println(service.processOrder("order-7").join());
        System.out.println(service.loadDashboard("42").join());
    }
}
