import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class PaymentGatewayHealthIndicator implements HealthIndicator {

    private final PaymentGatewayClient client;

    public PaymentGatewayHealthIndicator(PaymentGatewayClient client) {
        this.client = client;
    }

    @Override
    public Health health() {
        try {
            PaymentGatewayStatus status = client.ping();
            if (status.isAvailable()) {
                return Health.up()
                    .withDetail("provider", "stripe")
                    .withDetail("latency_ms", status.getLatencyMs())
                    .withDetail("version", status.getVersion())
                    .build();
            }
            return Health.down()
                .withDetail("reason", "Gateway returned unavailable")
                .withDetail("status_code", status.getStatusCode())
                .build();
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
