import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

@Component
public class ExternalApiHealthIndicator implements HealthIndicator {

    private static final String HEALTH_URL = "https://api.example.com/health";

    private final HttpClient httpClient;

    public ExternalApiHealthIndicator() {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(2))
            .build();
    }

    @Override
    public Health health() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(HEALTH_URL))
                .timeout(Duration.ofSeconds(3))
                .GET()
                .build();

            HttpResponse<String> response = httpClient.send(
                request, HttpResponse.BodyHandlers.ofString()
            );

            if (response.statusCode() == 200) {
                return Health.up()
                    .withDetail("url", HEALTH_URL)
                    .withDetail("status_code", response.statusCode())
                    .build();
            }
            return Health.down()
                .withDetail("url", HEALTH_URL)
                .withDetail("status_code", response.statusCode())
                .withDetail("reason", "Non-200 response")
                .build();
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("url", HEALTH_URL)
                .withDetail("error", "Connection timeout or failure")
                .build();
        }
    }
}
