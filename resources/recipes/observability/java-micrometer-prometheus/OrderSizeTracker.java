import io.micrometer.core.instrument.DistributionSummary;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.stereotype.Service;

// DistributionSummary — track the distribution of values
// (items per order, payload sizes) rather than durations.
@Service
public class OrderSizeTracker {

    private final DistributionSummary orderItemCounts;

    public OrderSizeTracker(MeterRegistry registry) {
        this.orderItemCounts = DistributionSummary.builder("order.item.count")
            .description("Number of items per order")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);
    }

    public void recordOrder(int itemCount) {
        orderItemCounts.record(itemCount);
    }
}
