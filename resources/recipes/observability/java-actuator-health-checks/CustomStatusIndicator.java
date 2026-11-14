import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.boot.actuate.health.Status;
import org.springframework.stereotype.Component;

@Component
public class CustomStatusIndicator implements HealthIndicator {

    private static final Status DEGRADED = new Status("DEGRADED", "Performance is degraded");

    @Override
    public Health health() {
        if (isDegraded()) {
            return Health.status(DEGRADED).build();
        }
        return Health.up().build();
    }

    private boolean isDegraded() {
        // your own signal here: latency p99, error rate, queue lag...
        return false;
    }
}
