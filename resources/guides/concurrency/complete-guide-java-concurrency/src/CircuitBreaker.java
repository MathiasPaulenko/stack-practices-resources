import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Supplier;

/** Minimal circuit breaker built on CompletableFuture. */
public class CircuitBreaker {
    private final AtomicReference<State> state = new AtomicReference<>(State.CLOSED);
    private final AtomicInteger failureCount = new AtomicInteger(0);
    private final int threshold;
    private final long timeoutMs;
    private volatile long lastFailureTime;

    enum State { CLOSED, OPEN, HALF_OPEN }

    public CircuitBreaker(int threshold, long timeoutMs) {
        this.threshold = threshold;
        this.timeoutMs = timeoutMs;
    }

    public <T> CompletableFuture<T> execute(Supplier<T> supplier) {
        if (state.get() == State.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > timeoutMs) {
                state.set(State.HALF_OPEN);
            } else {
                return CompletableFuture.failedFuture(new RuntimeException("Circuit open"));
            }
        }
        return CompletableFuture.supplyAsync(supplier)
            .handle((result, ex) -> {
                if (ex != null) {
                    if (failureCount.incrementAndGet() >= threshold) {
                        state.set(State.OPEN);
                        lastFailureTime = System.currentTimeMillis();
                    }
                    throw new CompletionException(ex);
                }
                failureCount.set(0);
                return CompletableFuture.completedFuture(result);
            }).thenCompose(f -> f);
    }
}
