import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.ReactiveHealthIndicator;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class ReactiveApiHealthIndicator implements ReactiveHealthIndicator {

    private final WebClient webClient = WebClient.create("https://api.example.com");

    @Override
    public Mono<Health> health() {
        return checkExternalApi()
            .map(status -> Health.up().withDetail("status", status).build())
            .onErrorResume(e -> Mono.just(
                Health.down(e).withDetail("error", e.getMessage()).build()
            ));
    }

    private Mono<String> checkExternalApi() {
        return webClient.get()
            .uri("/health")
            .retrieve()
            .bodyToMono(String.class);
    }
}
