// AmbassadorClient.java — Java ambassador for outbound calls.
// Requires Java 11+ (java.net.http). No external dependencies.
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class AmbassadorClient {

    private final HttpClient client;
    private final String targetUrl;
    private final ConcurrentHashMap<String, RequestStats> stats = new ConcurrentHashMap<>();
    private final AtomicInteger failureCount = new AtomicInteger(0);
    private final int failureThreshold = 5;
    private volatile boolean circuitOpen = false;
    private volatile long lastFailureTime = 0;
    private final long recoveryTimeoutMs = 30000;

    public AmbassadorClient(String targetUrl) {
        this.targetUrl = targetUrl;
        this.client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .build();
    }

    public HttpResponse<String> request(String method, String path,
                                        String body, int maxRetries) throws Exception {
        checkCircuit();

        Exception lastError = null;
        for (int attempt = 0; attempt < maxRetries; attempt++) {
            long start = System.currentTimeMillis();
            try {
                var builder = HttpRequest.newBuilder()
                    .uri(URI.create(targetUrl + path))
                    .timeout(Duration.ofSeconds(10));

                switch (method) {
                    case "GET" -> builder.GET();
                    case "POST" -> builder.POST(HttpRequest.BodyPublishers.ofString(body));
                    case "PUT" -> builder.PUT(HttpRequest.BodyPublishers.ofString(body));
                    case "DELETE" -> builder.DELETE();
                    default -> throw new IllegalArgumentException("Unsupported method: " + method);
                }

                var response = client.send(builder.build(),
                    HttpResponse.BodyHandlers.ofString());

                long latency = System.currentTimeMillis() - start;
                if (response.statusCode() < 500) {
                    recordSuccess(method + " " + path, latency);
                    return response;
                }
                recordFailure(method + " " + path, latency);
                lastError = new RuntimeException("HTTP " + response.statusCode());
            } catch (Exception e) {
                long latency = System.currentTimeMillis() - start;
                lastError = e;
                recordFailure(method + " " + path, latency);
            }

            if (attempt < maxRetries - 1) {
                Thread.sleep((long) Math.pow(2, attempt) * 1000);
            }
        }

        lastFailureTime = System.currentTimeMillis();
        if (failureCount.get() >= failureThreshold) {
            circuitOpen = true;
        }

        throw new RuntimeException("All retries exhausted", lastError);
    }

    private void checkCircuit() throws Exception {
        if (circuitOpen) {
            if (System.currentTimeMillis() - lastFailureTime > recoveryTimeoutMs) {
                circuitOpen = false;
                failureCount.set(0);
            } else {
                throw new RuntimeException("Circuit breaker is open");
            }
        }
    }

    private void recordSuccess(String endpoint, long latencyMs) {
        failureCount.set(0);
        circuitOpen = false;
        stats.computeIfAbsent(endpoint, k -> new RequestStats())
             .record(latencyMs, true);
    }

    private void recordFailure(String endpoint, long latencyMs) {
        failureCount.incrementAndGet();
        stats.computeIfAbsent(endpoint, k -> new RequestStats())
             .record(latencyMs, false);
    }

    static class RequestStats {
        final AtomicLong count = new AtomicLong(0);
        final AtomicLong errors = new AtomicLong(0);
        final AtomicLong totalLatency = new AtomicLong(0);

        void record(long latencyMs, boolean success) {
            count.incrementAndGet();
            totalLatency.addAndGet(latencyMs);
            if (!success) errors.incrementAndGet();
        }
    }
}
