import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Registry Pattern: central map of named instances and lazy factories.
 *
 * Run: javac Registry.java && java Registry
 */
public class Registry {
    private static final Map<String, Object> instances = new HashMap<>();
    private static final Map<String, Supplier<?>> factories = new HashMap<>();

    public static void register(String name, Object instance) {
        instances.put(name, instance);
    }

    public static void registerFactory(String name, Supplier<?> factory) {
        factories.put(name, factory);
    }

    @SuppressWarnings("unchecked")
    public static <T> T get(String name) {
        if (instances.containsKey(name)) {
            return (T) instances.get(name);
        }
        if (factories.containsKey(name)) {
            T instance = (T) factories.get(name).get();
            instances.put(name, instance);
            return instance;
        }
        throw new IllegalArgumentException("No registration for: " + name);
    }

    public static boolean has(String name) {
        return instances.containsKey(name) || factories.containsKey(name);
    }

    /** Clear everything — call this between tests to avoid state leakage. */
    public static void reset() {
        instances.clear();
        factories.clear();
    }

    static class DatabaseConnection {
        String query(String sql) {
            return "Result: " + sql;
        }
    }

    static class CacheClient {
        String get(String key) {
            return "cached-" + key;
        }
    }

    public static void main(String[] args) {
        Registry.register("db", new DatabaseConnection());
        Registry.registerFactory("cache", CacheClient::new);

        DatabaseConnection db = Registry.get("db");
        CacheClient cache = Registry.get("cache"); // factory runs here, then the instance is cached

        System.out.println(db.query("SELECT 1"));
        System.out.println(cache.get("users"));
        System.out.println("has db: " + Registry.has("db"));
        System.out.println("same cache instance: " + (Registry.get("cache") == cache));

        try {
            Registry.get("missing");
        } catch (IllegalArgumentException e) {
            System.out.println("IllegalArgumentException: " + e.getMessage());
        }
    }
}
