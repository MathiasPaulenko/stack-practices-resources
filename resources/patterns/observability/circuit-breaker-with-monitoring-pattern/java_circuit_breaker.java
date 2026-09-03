import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.github.resilience4j.micrometer.tagged.TaggedCircuitBreakerMetrics;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.prometheus.PrometheusConfig;
import io.micrometer.prometheus.PrometheusMeterRegistry;
import java.time.Duration;

public class MonitoredCircuitBreaker {

    private final CircuitBreaker breaker;
    private final MeterRegistry meterRegistry;

    public MonitoredCircuitBreaker(String name, int failureRateThreshold,
                                   int waitDurationSeconds, int slidingWindowSize,
                                   int minimumNumberOfCalls) {
        this.meterRegistry = new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);
        CircuitBreakerRegistry registry = CircuitBreakerRegistry.ofDefaults();

        TaggedCircuitBreakerMetrics.ofCircuitBreakerRegistry(registry)
            .bindTo(meterRegistry);

        this.breaker = CircuitBreaker.of(
            name,
            CircuitBreakerConfig.custom()
                .failureRateThreshold(failureRateThreshold)
                .waitDurationInOpenState(Duration.ofSeconds(waitDurationSeconds))
                .slidingWindowSize(slidingWindowSize)
                .minimumNumberOfCalls(minimumNumberOfCalls)
                .build()
        );

        registry.addCircuitBreaker(breaker);
    }

    public <T> T execute(java.util.function.Supplier<T> supplier) {
        return CircuitBreaker.decorateSupplier(breaker, supplier).get();
    }

    public String getMetrics() {
        return meterRegistry
            .find("resilience4j_circuitbreaker_state")
            .meter()
            .getId()
            .toString();
    }

    public static void main(String[] args) {
        MonitoredCircuitBreaker mcb = new MonitoredCircuitBreaker(
            "payment-service", 50, 30, 10, 5
        );

        String result = mcb.execute(() -> "Payment processed");
        System.out.println(result);
    }
}
