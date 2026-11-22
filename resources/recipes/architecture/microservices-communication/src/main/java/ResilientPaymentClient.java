import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.vavr.control.Try;

import java.time.Duration;

/**
 * Circuit breaker + retry around a downstream payment gateway (Resilience4j).
 * Companion to https://stackpractices.com/recipes/microservices-communication/
 */
public class ResilientPaymentClient {
    private final CircuitBreaker circuitBreaker;
    private final Retry retry;
    private final PaymentGateway gateway;

    public ResilientPaymentClient(PaymentGateway gateway) {
        this.gateway = gateway;
        this.circuitBreaker = CircuitBreaker.of("payment",
            CircuitBreakerConfig.custom()
                .failureRateThreshold(50)
                .waitDurationInOpenState(Duration.ofSeconds(30))
                .slidingWindowSize(10)
                .minimumNumberOfCalls(5)
                .build()
        );
        this.retry = Retry.of("payment",
            RetryConfig.custom()
                .maxAttempts(3)
                .waitDuration(Duration.ofMillis(500))
                .build()
        );
    }

    public PaymentResult charge(PaymentRequest request) {
        return Try.of(() ->
            Retry.decorateSupplier(retry,
                CircuitBreaker.decorateSupplier(circuitBreaker,
                    () -> gateway.charge(request)
                )
            ).get()
        ).getOrElseThrow(throwable ->
            new PaymentFailedException("Payment service unavailable", throwable)
        );
    }
}

interface PaymentGateway {
    PaymentResult charge(PaymentRequest request);
}

record PaymentRequest(String orderId, long amountCents, String idempotencyKey) {}
record PaymentResult(String transactionId, String status) {}

class PaymentFailedException extends RuntimeException {
    PaymentFailedException(String message, Throwable cause) { super(message, cause); }
}
