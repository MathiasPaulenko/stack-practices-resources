import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

/**
 * Async retry with exponential backoff: the retry is scheduled on
 * CompletableFuture.delayedExecutor(delay, unit) — a plain Executor that
 * runs tasks after the delay. It has no supplyAsync method of its own;
 * it goes as the executor argument of supplyAsync/runAsync/*Async.
 * On the final attempt failedFuture(ex) propagates the error instead of
 * completing with null.
 */
public class RetryWithBackoff {

    private static final Logger log = Logger.getLogger(RetryWithBackoff.class.getName());

    public static CompletableFuture<String> fetchWithBackoff(
            String url, int maxAttempts, long initialDelayMs) {
        return AsyncApiClient.fetchAsync(url)
            .handle((result, ex) -> {
                if (ex == null) {
                    return CompletableFuture.completedFuture(result);
                }
                if (maxAttempts <= 1) {
                    // Final attempt failed — propagate the error
                    return CompletableFuture.<String>failedFuture(ex);
                }
                long delay = initialDelayMs * (1L << (maxAttempts - 1));
                log.info(() -> "Retrying " + url + " in " + delay + "ms ("
                        + (maxAttempts - 1) + " attempts left)");
                return CompletableFuture
                    .supplyAsync(() -> fetchWithBackoff(url, maxAttempts - 1, initialDelayMs),
                        CompletableFuture.delayedExecutor(delay, TimeUnit.MILLISECONDS))
                    .thenCompose(f -> f);
            })
            .thenCompose(f -> f);
    }

    public static void main(String[] args) {
        String result = fetchWithBackoff("https://api.example.com/flaky", 3, 200)
            .join();
        System.out.println(result);
    }
}
