import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.bulkhead.Bulkhead;
import io.github.resilience4j.bulkhead.BulkheadConfig;
import io.github.resilience4j.timelimiter.TimeLimiter;
import io.github.resilience4j.decorators.Decorators;
import io.vavr.control.Try;

import java.net.ConnectException;
import java.time.Duration;
import java.util.concurrent.*;
import java.util.function.Supplier;

/**
 * Circuit breaker + retry + bulkhead + time limiter around a payment call.
 * Companion to https://stackpractices.com/recipes/microservices-patterns/
 */
public class ResilientPaymentClient {

    private final CircuitBreaker circuitBreaker;
    private final Retry retry;
    private final Bulkhead bulkhead;
    private final TimeLimiter timeLimiter;
    private final ExecutorService executor;

    public ResilientPaymentClient() {
        // Circuit breaker: open after 50% failure rate with min 10 calls
        CircuitBreakerConfig cbConfig = CircuitBreakerConfig.custom()
            .failureRateThreshold(50)
            .slowCallRateThreshold(50)
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            .minimumNumberOfCalls(10)
            .waitDurationInOpenState(Duration.ofSeconds(30))
            .permittedNumberOfCallsInHalfOpenState(3)
            .build();
        this.circuitBreaker = CircuitBreaker.of("payment", cbConfig);

        // Retry: 3 attempts with exponential backoff
        RetryConfig retryConfig = RetryConfig.custom()
            .maxAttempts(3)
            .waitDuration(Duration.ofMillis(500))
            .intervalFunction(attempt -> Math.pow(2, attempt) * 500)
            .retryOnException(e -> e instanceof TimeoutException || e instanceof ConnectException)
            .build();
        this.retry = Retry.of("payment", retryConfig);

        // Bulkhead: max 10 concurrent calls
        BulkheadConfig bulkheadConfig = BulkheadConfig.custom()
            .maxConcurrentCalls(10)
            .maxWaitDuration(Duration.ofMillis(500))
            .build();
        this.bulkhead = Bulkhead.of("payment", bulkheadConfig);

        // Time limiter: 3 seconds max
        this.timeLimiter = TimeLimiter.of(Duration.ofSeconds(3));
        this.executor = Executors.newCachedThreadPool();
    }

    public PaymentResult charge(String orderId, double amount) {
        Supplier<PaymentResult> supplier = () -> callPaymentService(orderId, amount);

        Supplier<PaymentResult> decorated = Decorators.ofSupplier(supplier)
            .withCircuitBreaker(circuitBreaker)
            .withRetry(retry)
            .withBulkhead(bulkhead)
            .decorate();

        return Try.ofSupplier(decorated)
            .recover(throwable -> {
                // Fallback: return cached or default result
                return PaymentResult.degraded(orderId, "Payment unavailable, using fallback");
            })
            .get();
    }

    private PaymentResult callPaymentService(String orderId, double amount) {
        // Actual HTTP call to payment service
        // Throws on failure
        return new PaymentResult(orderId, "SUCCESS");
    }
}

record PaymentResult(String orderId, String status) {
    static PaymentResult degraded(String orderId, String message) {
        return new PaymentResult(orderId, "DEGRADED: " + message);
    }
}
