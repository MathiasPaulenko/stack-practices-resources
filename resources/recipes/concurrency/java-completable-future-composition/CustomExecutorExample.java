import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Dedicated executor: supplyAsync without an executor lands on
 * ForkJoinPool.commonPool(), shared JVM-wide. A blocking call there can
 * stall unrelated tasks — pin blocking work to your own pool.
 */
public class CustomExecutorExample {

    private static final HttpClient client = HttpClient.newHttpClient();

    // A dedicated pool — don't rely on the common ForkJoinPool
    private static final ExecutorService executor = Executors.newFixedThreadPool(
        Runtime.getRuntime().availableProcessors(),
        r -> {
            Thread t = new Thread(r);
            t.setName("async-worker-" + t.getId());
            t.setDaemon(true);
            return t;
        }
    );

    // Any pre-existing synchronous call — client.send, a JDBC query, a file read
    private static String blockingFetch(String url) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
            return client.send(request, HttpResponse.BodyHandlers.ofString()).body();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static CompletableFuture<String> fetchWithCustomPool(String url) {
        // supplyAsync runs the blocking call on the dedicated pool
        return CompletableFuture.supplyAsync(() -> blockingFetch(url), executor);
    }

    public static CompletableFuture<UserProfile> buildProfileWithPool(String userId) {
        // Reuses UserService fetchUser/fetchOrders; the *Async suffix pins
        // each stage to our executor. The nested thenApplyAsync closes over
        // `user` so new UserProfile(user, orders) sees both values.
        return UserService.fetchUser(userId)
            .thenComposeAsync(user -> UserService.fetchOrders(user.id())
                .thenApplyAsync(orders -> new UserProfile(user, orders), executor),
                executor);
    }

    public static void main(String[] args) {
        try {
            UserProfile profile = buildProfileWithPool("123").join();
            System.out.println(profile);
        } finally {
            executor.shutdown();
        }
    }
}
