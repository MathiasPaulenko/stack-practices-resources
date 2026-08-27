import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Supplier;

public class InMemoryCache {
    private final ConcurrentHashMap<String, CachedValue> cache = new ConcurrentHashMap<>();

    public String get(String key, Supplier<String> loader) {
        return cache.computeIfAbsent(key, k -> {
            String value = loader.get();
            return new CachedValue(value, System.currentTimeMillis());
        }).value;
    }

    public void invalidate(String key) {
        cache.remove(key);
    }

    public static void main(String[] args) {
        InMemoryCache cache = new InMemoryCache();
        String value1 = cache.get("greeting", () -> {
            System.out.println("Loading value...");
            return "Hello, World!";
        });
        String value2 = cache.get("greeting", () -> "Should not load");
        System.out.println(value1);
        System.out.println(value2);
        cache.invalidate("greeting");
    }

    private record CachedValue(String value, long timestamp) {}
}
