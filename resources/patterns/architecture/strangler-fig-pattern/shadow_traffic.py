// StranglerGateway.java — Spring Cloud Gateway for strangler fig routing
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class StranglerGateway {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            // Migrated routes -> new service
            .route("customers-new", r -> r
                .path("/api/customers/**")
                .uri("http://new-service:8080"))
            .route("orders-new", r -> r
                .path("/api/orders/**")
                .uri("http://new-service:8080"))
            .route("products-new", r -> r
                .path("/api/products/**")
                .uri("http://new-service:8080"))
            // Everything else -> legacy
            .route("legacy-fallback", r -> r
                .path("/**")
                .uri("http://legacy-app:3000"))
            .build();
    }
}
