import java.util.concurrent.CompletableFuture;

/**
 * Sequential composition: fetchUser → fetchOrders → UserProfile.
 * thenCompose is the async flatMap — it keeps the chain flat when the next
 * call depends on the previous result.
 */
public class SequentialPipeline {

    public static CompletableFuture<UserProfile> buildProfile(String userId) {
        // thenCompose chains futures — each step waits for the previous
        return UserService.fetchUser(userId)
            .thenCompose(user -> UserService.fetchOrders(user.id())
                .thenApply(orders -> new UserProfile(user, orders)));
    }

    public static void main(String[] args) {
        UserProfile profile = buildProfile("123").join();
        System.out.println(profile);
    }
}
