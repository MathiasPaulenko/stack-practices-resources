import java.util.concurrent.CompletableFuture;
import java.util.logging.Logger;

/**
 * The three error handlers: exceptionally recovers with a value, handle sees
 * both branches and can branch (retry/propagate), whenComplete observes
 * without changing the outcome.
 */
public class ErrorHandling {

    private static final Logger log = Logger.getLogger(ErrorHandling.class.getName());

    public static CompletableFuture<String> fetchWithFallback(String url, String fallback) {
        return AsyncApiClient.fetchAsync(url)
            // exceptionally — recover from failure with a fallback value
            .exceptionally(ex -> {
                log.warning(() -> "Fetch failed: " + ex.getMessage());
                return fallback;
            });
    }

    public static CompletableFuture<String> fetchWithRetry(String url, int maxRetries) {
        return AsyncApiClient.fetchAsync(url)
            .handle((result, ex) -> {
                if (ex != null) {
                    if (maxRetries > 0) {
                        log.info(() -> "Retrying (" + maxRetries + " left): " + ex.getMessage());
                        return fetchWithRetry(url, maxRetries - 1);
                    }
                    // Out of retries — propagate the failure
                    return CompletableFuture.<String>failedFuture(ex);
                }
                return CompletableFuture.completedFuture(result);
            })
            .thenCompose(f -> f);  // Flatten nested CompletableFuture
    }

    // whenComplete — observe both branches without changing the result
    public static CompletableFuture<String> fetchWithLogging(String url) {
        return AsyncApiClient.fetchAsync(url)
            .whenComplete((result, ex) -> {
                if (ex != null) {
                    log.severe(() -> "Request to " + url + " failed: " + ex.getMessage());
                } else {
                    log.info(() -> "Request to " + url + " succeeded (" + result.length() + " bytes)");
                }
            });
    }

    public static void main(String[] args) {
        String result = fetchWithFallback(
            "https://api.example.com/maybe-down",
            "{\"status\": \"fallback\"}"
        ).join();
        System.out.println(result);
    }
}
