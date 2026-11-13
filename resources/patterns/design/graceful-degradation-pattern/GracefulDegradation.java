import java.util.*;

public class GracefulDegradation {

    enum Status { HEALTHY, DEGRADED, DOWN }

    record ServiceResult(Object data, Status status, String source, boolean degraded, String error) {
        static ServiceResult healthy(Object data, String source) {
            return new ServiceResult(data, Status.HEALTHY, source, false, null);
        }
        static ServiceResult degraded(Object data, String source, String error) {
            return new ServiceResult(data, Status.DEGRADED, source, true, error);
        }
        static ServiceResult down(Object data, String source, String error) {
            return new ServiceResult(data, Status.DOWN, source, true, error);
        }
    }

    private final Map<String, long[]> cacheTimestamps = new HashMap<>();
    private final Map<String, Object> cacheData = new HashMap<>();

    Object cacheGet(String key) {
        if (cacheData.containsKey(key)) {
            if (System.currentTimeMillis() / 1000 - cacheTimestamps.get(key)[0] < 300) {
                return cacheData.get(key);
            }
        }
        return null;
    }

    void cacheSet(String key, Object data) {
        cacheData.put(key, data);
        cacheTimestamps.put(key, new long[]{System.currentTimeMillis() / 1000});
    }

    ServiceResult callWithFallback(String serviceName, java.util.function.Supplier<Object> primaryFn,
                                    Object defaultVal, String cacheKey) {
        try {
            Object result = primaryFn.get();
            if (cacheKey != null) cacheSet(cacheKey, result);
            return ServiceResult.healthy(result, serviceName);
        } catch (Exception e) {
            if (cacheKey != null) {
                Object cached = cacheGet(cacheKey);
                if (cached != null) {
                    return ServiceResult.degraded(cached, serviceName + ":cache", e.getMessage());
                }
            }
            return ServiceResult.down(defaultVal, serviceName + ":default", e.getMessage());
        }
    }

    public static void main(String[] args) {
        var deg = new GracefulDegradation();

        var results = new LinkedHashMap<String, ServiceResult>();
        results.put("product_details", deg.callWithFallback("product_details",
            () -> Map.of("id", "P100", "name", "Headphones", "price", 99.99), null, "product_details"));
        results.put("recommendations", deg.callWithFallback("recommendations",
            () -> { throw new RuntimeException("Recommendation service down"); }, List.of(), "recommendations"));
        results.put("reviews", deg.callWithFallback("reviews",
            () -> List.of(Map.of("user", "alice", "rating", 5)), null, "reviews"));
        results.put("inventory", deg.callWithFallback("inventory",
            () -> { throw new RuntimeException("Inventory API timed out"); },
            Map.of("inStock", "unknown", "message", "Check back later"), "inventory"));

        System.out.println("=== Page Assembly ===");
        results.forEach((name, result) -> {
            String icon = result.degraded() ? "DEGRADED" : "OK";
            System.out.printf("  [%s] %s: source=%s, data=%s%n", icon, name, result.source(), result.data());
        });
    }
}
