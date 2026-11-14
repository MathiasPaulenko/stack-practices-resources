import io.micrometer.core.instrument.Counter;
import io.micrometer.prometheusmetrics.PrometheusConfig;
import io.micrometer.prometheusmetrics.PrometheusMeterRegistry;
import io.prometheus.metrics.exporter.httpserver.HTTPServer;

// Micrometer without Spring Boot, on micrometer-registry-prometheus
// (Prometheus client 1.x, Micrometer 1.12+ / Spring Boot 3.2+).
// For the legacy simpleclient 0.x, use the module
// micrometer-registry-prometheus-simpleclient instead — there the registry
// is io.micrometer.prometheus.PrometheusMeterRegistry and the endpoint is
// io.prometheus.client.exporter.HTTPServer (new HTTPServer(port)).
public class StandaloneApp {

    public static void main(String[] args) throws Exception {
        PrometheusMeterRegistry registry = new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);

        Counter counter = Counter.builder("app.requests")
            .tag("endpoint", "/api")
            .register(registry);

        // Builder API replaces the legacy new HTTPServer(port)
        HTTPServer server = HTTPServer.builder().port(9090).buildAndStart();

        counter.increment();
        server.stop();
    }
}
