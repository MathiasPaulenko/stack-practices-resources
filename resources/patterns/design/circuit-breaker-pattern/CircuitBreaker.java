import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Supplier;

/**
 * Count-based circuit breaker with fallback support.
 *
 * Thread-safe: the failure counter is atomic, the state reference volatile.
 * Usage: javac CircuitBreaker.java && java CircuitBreaker
 */
public class CircuitBreaker {

    public static class Open extends RuntimeException {
        public Open(String message) { super(message); }
    }

    private enum State { CLOSED, OPEN, HALF_OPEN }

    private final int failureThreshold;
    private final long recoveryTimeoutMs;
    private volatile State state = State.CLOSED;
    private final AtomicInteger failures = new AtomicInteger(0);
    private volatile long lastFailureTime = 0;

    public CircuitBreaker(int failureThreshold, long recoveryTimeoutMs) {
        this.failureThreshold = failureThreshold;
        this.recoveryTimeoutMs = recoveryTimeoutMs;
    }

    public <T> T call(Supplier<T> supplier) {
        return call(supplier, null);
    }

    public <T> T call(Supplier<T> supplier, Supplier<T> fallback) {
        if (state == State.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime >= recoveryTimeoutMs) {
                state = State.HALF_OPEN;
            } else {
                if (fallback != null) return fallback.get();
                throw new Open("Circuit breaker is OPEN");
            }
        }

        try {
            T result = supplier.get();
            onSuccess();
            return result;
        } catch (RuntimeException e) {
            onFailure();
            if (fallback != null) return fallback.get();
            throw e;
        }
    }

    private void onSuccess() {
        failures.set(0);
        state = State.CLOSED;
    }

    private void onFailure() {
        int count = failures.incrementAndGet();
        lastFailureTime = System.currentTimeMillis();
        if (count >= failureThreshold) {
            state = State.OPEN;
        }
    }

    public State getState() {
        return state;
    }

    public static void main(String[] args) {
        CircuitBreaker breaker = new CircuitBreaker(2, 1000);

        for (int i = 0; i < 8; i++) {
            try {
                String result = breaker.call(() -> {
                    if (Math.random() < 0.7) throw new RuntimeException("Service error");
                    return "Data";
                }, () -> "cached value");
                System.out.println("Call " + (i + 1) + ": " + result);
            } catch (Exception e) {
                System.out.println("Call " + (i + 1) + ": " + e.getMessage()
                    + " (state=" + breaker.getState() + ")");
            }
            try { Thread.sleep(300); } catch (InterruptedException ignored) {}
        }
    }
}
