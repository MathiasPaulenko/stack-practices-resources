import java.util.Random;
import java.util.concurrent.Callable;

/**
 * Retry helper with exponential backoff and jitter.
 * Companion code for https://stackpractices.com/recipes/retry-logic-exponential-backoff/
 */
public class Retry {

    private static final Random RANDOM = new Random();

    @FunctionalInterface
    public interface Sleeper {
        void sleep(long millis) throws InterruptedException;
    }

    public static <T> T execute(Callable<T> callable, int maxRetries,
                                long baseDelayMs, long maxDelayMs) throws Exception {
        return execute(callable, maxRetries, baseDelayMs, maxDelayMs, Thread::sleep);
    }

    /** Sleeper is injectable so tests can record delays instead of waiting. */
    public static <T> T execute(Callable<T> callable, int maxRetries,
                                long baseDelayMs, long maxDelayMs,
                                Sleeper sleeper) throws Exception {
        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return callable.call();
            } catch (Exception e) {
                if (attempt == maxRetries || !isRetryable(e)) {
                    throw e;
                }
                long delay = Math.min(baseDelayMs * (1L << attempt), maxDelayMs);
                delay = (long) (RANDOM.nextDouble() * delay);
                sleeper.sleep(delay);
            }
        }
        throw new IllegalStateException("unreachable");
    }

    private static boolean isRetryable(Exception e) {
        return e instanceof java.net.SocketTimeoutException
            || e instanceof java.net.ConnectException
            || e instanceof java.io.IOException;
    }

    public static void main(String[] args) throws Exception {
        // Demo: fails twice, then succeeds.
        final int[] attempts = {0};
        String result = Retry.execute(() -> {
            attempts[0]++;
            if (attempts[0] < 3) {
                throw new java.io.IOException("transient failure #" + attempts[0]);
            }
            return "ok";
        }, 5, 100, 5000);
        System.out.println(result + " after " + attempts[0] + " attempts");
    }
}
