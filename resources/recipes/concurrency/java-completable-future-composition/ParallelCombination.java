import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * Parallel combination: three independent fetches started at once, merged
 * pairwise with thenCombine. Total time ≈ the slowest call, not the sum.
 */
public class ParallelCombination {

    public static CompletableFuture<Dashboard> buildDashboard(String userId) {
        // All three fetches run in parallel
        CompletableFuture<User> userFuture = UserService.fetchUser(userId);
        CompletableFuture<List<Order>> ordersFuture = UserService.fetchOrders(userId);
        CompletableFuture<List<Notification>> notifsFuture = UserService.fetchNotifications(userId);

        // thenCombine merges two futures — runs after both complete
        return userFuture
            .thenCombine(ordersFuture, (user, orders) ->
                new PartialDashboard(user, orders))
            .thenCombine(notifsFuture, (partial, notifs) ->
                new Dashboard(partial.user(), partial.orders(), notifs));
    }

    // Total time = max(fetchUser, fetchOrders, fetchNotifications), not sum
    public static void main(String[] args) {
        Dashboard dashboard = buildDashboard("123").join();
        System.out.println(dashboard);
    }
}
