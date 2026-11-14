import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.binder.MeterBinder;
import java.util.Map;
import java.util.concurrent.BlockingQueue;
import org.springframework.context.annotation.Configuration;

// MeterBinder — bind gauges to real state objects. Both fields are
// injected so nothing is implied; the registry weak-references them,
// so they must be app-owned objects (never short-lived temporaries).
@Configuration
public class CustomMetrics implements MeterBinder {

    private final BlockingQueue<Runnable> orderQueue;
    private final Map<String, ?> userCache;

    public CustomMetrics(BlockingQueue<Runnable> orderQueue, Map<String, ?> userCache) {
        this.orderQueue = orderQueue;
        this.userCache = userCache;
    }

    @Override
    public void bindTo(MeterRegistry registry) {
        Gauge.builder("queue.depth", orderQueue, BlockingQueue::size)
            .description("Current queue depth")
            .tag("queue", "order-processing")
            .register(registry);

        Gauge.builder("cache.size", userCache, Map::size)
            .description("Current cache entry count")
            .tag("cache", "user-cache")
            .register(registry);
    }
}
