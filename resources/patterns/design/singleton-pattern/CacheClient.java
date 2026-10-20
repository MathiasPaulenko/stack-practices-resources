/**
 * Double-checked locking Singleton — lazy, thread-safe, fast path lock-free.
 *
 * `volatile` is mandatory: without it a thread can observe a non-null
 * reference to a partially constructed object (the JVM may publish the
 * reference before the constructor finishes writing fields).
 */
public class CacheClient {
    private static volatile CacheClient instance;

    private final java.util.Map<String, String> cache = new java.util.concurrent.ConcurrentHashMap<>();

    private CacheClient() {
    }

    public static CacheClient getInstance() {
        if (instance == null) {                       // fast path, no lock
            synchronized (CacheClient.class) {
                if (instance == null) {               // second check inside the lock
                    instance = new CacheClient();
                }
            }
        }
        return instance;
    }

    public void put(String key, String value) {
        cache.put(key, value);
    }

    public String get(String key) {
        return cache.get(key);
    }

    public static void main(String[] args) {
        CacheClient a = CacheClient.getInstance();
        CacheClient b = CacheClient.getInstance();
        a.put("session:42", "user-7");
        System.out.println("same instance: " + (a == b));
        System.out.println("shared state: " + b.get("session:42"));
    }
}
