import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
public class QueueDepthHealthIndicator implements HealthIndicator {

    private static final int THRESHOLD = 1000;

    private final MessageQueueService queueService;

    public QueueDepthHealthIndicator(MessageQueueService queueService) {
        this.queueService = queueService;
    }

    @Override
    public Health health() {
        int depth = queueService.getQueueDepth("order-processing");

        Map<String, Object> details = new HashMap<>();
        details.put("queue", "order-processing");
        details.put("depth", depth);
        details.put("threshold", THRESHOLD);

        if (depth < THRESHOLD * 0.8) {
            return Health.up().withDetails(details).build();
        }
        if (depth < THRESHOLD) {
            return Health.up().withDetails(details)
                .withDetail("warning", "Queue depth approaching threshold").build();
        }
        return Health.down().withDetails(details)
            .withDetail("error", "Queue depth exceeded threshold").build();
    }
}
