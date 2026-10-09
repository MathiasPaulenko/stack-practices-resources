import java.time.Instant;
import java.util.*;

public class ContextObjectDemo {

    static final class RequestContext {
        private final String requestId;
        private final Instant timestamp;
        private final String userId;
        private final String correlationId;
        private final Map<String, Object> metadata;

        private RequestContext(Builder b) {
            this.requestId = b.requestId;
            this.timestamp = b.timestamp;
            this.userId = b.userId;
            this.correlationId = b.correlationId;
            this.metadata = Collections.unmodifiableMap(new HashMap<>(b.metadata));
        }

        String getRequestId() { return requestId; }
        String getUserId() { return userId; }

        static class Builder {
            private String requestId = UUID.randomUUID().toString();
            private Instant timestamp = Instant.now();
            private String userId;
            private String correlationId;
            private Map<String, Object> metadata = new HashMap<>();

            Builder userId(String v) { this.userId = v; return this; }
            Builder correlationId(String v) { this.correlationId = v; return this; }
            Builder metadata(String k, Object v) { this.metadata.put(k, v); return this; }
            RequestContext build() { return new RequestContext(this); }
        }
    }

    static class OrderService {
        Map<String, Object> processOrder(RequestContext ctx, Map<String, Object> orderData) {
            System.out.println("[" + ctx.getRequestId() + "] Order for " + ctx.getUserId());
            Map<String, Object> result = new HashMap<>(orderData);
            result.put("order_id", "ORD-123");
            return result;
        }
    }

    // Boundary: build the context once, pass it down
    static class RequestHandler {
        private final OrderService service;
        RequestHandler(OrderService service) { this.service = service; }

        Map<String, Object> handleRequest(Map<String, Object> raw) {
            RequestContext ctx = new RequestContext.Builder()
                .userId((String) raw.get("user_id"))
                .correlationId((String) raw.get("correlation_id"))
                .build();
            return service.processOrder(ctx, (Map<String, Object>) raw.get("order_data"));
        }
    }

    public static void main(String[] args) {
        RequestHandler handler = new RequestHandler(new OrderService());
        Map<String, Object> request = Map.of(
            "user_id", "user-42",
            "order_data", Map.of("items", List.of("book", "pen"))
        );
        Object orderId = handler.handleRequest(request).get("order_id");
        System.out.println("ORD-123".equals(orderId) ? "context-object-pattern OK" : "FAIL");
    }
}
