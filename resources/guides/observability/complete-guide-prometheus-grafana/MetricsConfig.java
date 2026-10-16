// MetricsConfig.java — Micrometer with Prometheus
import io.micrometer.core.instrument.*;
import io.micrometer.prometheus.PrometheusMeterRegistry;
import io.micrometer.core.instrument.binder.jvm.JvmMemoryMetrics;
import io.micrometer.core.instrument.binder.system.ProcessorMetrics;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MetricsConfig {

    @Bean
    public PrometheusMeterRegistry prometheusRegistry() {
        PrometheusMeterRegistry registry = new PrometheusMeterRegistry(key -> null);

        // Bind JVM and system metrics
        new JvmMemoryMetrics().bindTo(registry);
        new ProcessorMetrics().bindTo(registry);

        return registry;
    }
}

// Service code using Micrometer
@Service
public class OrderService {

    private final Counter ordersCounter;
    private final Timer orderDurationTimer;
    private final Gauge activeUsersGauge;

    public OrderService(MeterRegistry registry) {
        this.ordersCounter = Counter.builder("orders_total")
            .description("Total number of orders created")
            .tags("status", "success")
            .register(registry);

        this.orderDurationTimer = Timer.builder("order_creation_duration")
            .description("Time spent creating orders")
            .publishPercentileHistogram()  // exposes _bucket series, aggregable in PromQL
            .register(registry);

        this.activeUsersGauge = Gauge.builder("active_users", this, OrderService::getActiveUserCount)
            .description("Number of currently active users")
            .register(registry);
    }

    public Order createOrder(Long userId, List<OrderItem> items) {
        return orderDurationTimer.record(() -> {
            Order order = processOrder(userId, items);
            ordersCounter.increment();
            return order;
        });
    }

    private int getActiveUserCount() {
        return userSessionManager.getActiveCount();
    }
}

// Metrics endpoint
@RestController
public class MetricsController {

    private final PrometheusMeterRegistry registry;

    public MetricsController(PrometheusMeterRegistry registry) {
        this.registry = registry;
    }

    @GetMapping("/metrics")
    public String metrics() {
        return registry.scrape();
    }
}
