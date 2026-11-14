import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.stereotype.Service;

// Counter — count events. Registered once in the constructor;
// increment() in the request path is the only work per call.
@Service
public class OrderService {

    private final Counter ordersCreated;
    private final Counter ordersFailed;

    public OrderService(MeterRegistry registry) {
        this.ordersCreated = Counter.builder("orders.created")
            .description("Total orders created")
            .tag("type", "standard")
            .register(registry);

        this.ordersFailed = Counter.builder("orders.failed")
            .description("Total orders that failed processing")
            .tag("type", "standard")
            .register(registry);
    }

    public void createOrder(Models.OrderRequest request) {
        try {
            // ... create order ...
            ordersCreated.increment();
        } catch (Exception e) {
            ordersFailed.increment();
            throw e;
        }
    }
}
