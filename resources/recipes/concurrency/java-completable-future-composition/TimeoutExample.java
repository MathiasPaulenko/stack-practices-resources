import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

/**
 * Java 9+ timeouts: orTimeout completes the future exceptionally with
 * TimeoutException; completeOnTimeout completes it normally with a fallback.
 * Neither cancels the underlying request — the work keeps running.
 */
public class TimeoutExample {

    public static CompletableFuture<String> fetchWithTimeout(String url) {
        return AsyncApiClient.fetchAsync(url)
            .orTimeout(5, TimeUnit.SECONDS)  // Complete exceptionally with TimeoutException
            .exceptionally(ex -> {
                if (ex instanceof java.util.concurrent.TimeoutException) {
                    return "{\"error\": \"request timed out\"}";
                }
                return "{\"error\": \"" + ex.getMessage() + "\"}";
            });
    }

    // completeOnTimeout — provide a default value instead of an exception
    public static CompletableFuture<String> fetchWithDefault(String url, String defaultValue) {
        return AsyncApiClient.fetchAsync(url)
            .completeOnTimeout(defaultValue, 3, TimeUnit.SECONDS);
    }

    public static void main(String[] args) {
        String result = fetchWithTimeout("https://slow-api.example.com/data").join();
        System.out.println(result);
    }
}
