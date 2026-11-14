import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.stereotype.Service;

// Gauge — track the current value. Micrometer keeps a WEAK reference
// to the state object, so bind it to a field, never a temporary.
@Service
public class ConnectionPoolMonitor {

    private final AtomicInteger activeConnections = new AtomicInteger(0);

    public ConnectionPoolMonitor(MeterRegistry registry) {
        Gauge.builder("connection.pool.active", activeConnections, AtomicInteger::doubleValue)
            .description("Current active database connections")
            .tag("pool", "primary")
            .register(registry);
    }

    public void acquireConnection() {
        activeConnections.incrementAndGet();
    }

    public void releaseConnection() {
        activeConnections.decrementAndGet();
    }
}
