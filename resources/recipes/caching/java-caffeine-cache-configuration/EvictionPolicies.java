import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import com.github.benmanes.caffeine.cache.LoadingCache;
import com.github.benmanes.caffeine.cache.Scheduler;

import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/**
 * Standalone examples of every Caffeine eviction policy.
 * Requires com.github.ben-manes.caffeine:caffeine:3.1.8 on the classpath.
 */
public class EvictionPolicies {

  record User(String id, String name) {}
  record Product(String id, String name, double price) {}

  /** Size-bounded cache with write TTL and stats. */
  static Cache<String, User> basicCache() {
    return Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(30, TimeUnit.MINUTES)
        .recordStats()
        .build();
  }

  /** Fixed TTL from insertion; good when staleness tolerance is known. */
  static Cache<String, String> writeExpireCache() {
    return Caffeine.newBuilder()
        .expireAfterWrite(10, TimeUnit.MINUTES)
        .maximumSize(5_000)
        .build();
  }

  /** TTL resets on each read; pair with expireAfterWrite for freshness. */
  static Cache<String, String> accessExpireCache() {
    return Caffeine.newBuilder()
        .expireAfterAccess(5, TimeUnit.MINUTES)
        .expireAfterWrite(30, TimeUnit.MINUTES)
        .build();
  }

  /** Weight-bounded cache for variable-size entries. */
  static Cache<String, String> weightedCache() {
    return Caffeine.newBuilder()
        .maximumWeight(10_000_000)
        .weigher((String key, String value) -> value.length())
        .build();
  }

  /** Auto-populating cache with refresh-ahead. */
  static LoadingCache<String, Product> loadingCache() {
    return Caffeine.newBuilder()
        .maximumSize(5_000)
        .expireAfterWrite(15, TimeUnit.MINUTES)
        .refreshAfterWrite(10, TimeUnit.MINUTES)
        .build(EvictionPolicies::fetchProductFromDb);
  }

  /** GC-reclaimable entries. weakKeys switches to identity (==) comparison. */
  static Cache<String, User> weakReferenceCache() {
    return Caffeine.newBuilder()
        .weakValues()
        .build();
  }

  /** Proactive cleanup instead of purely lazy expiry. */
  static Cache<String, String> scheduledCache() {
    return Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(10, TimeUnit.MINUTES)
        .scheduler(Scheduler.systemScheduler())
        .build();
  }

  private static Product fetchProductFromDb(String key) {
    return new Product(key, "Product " + key, 9.99);
  }

  public static void main(String[] args) {
    Cache<String, User> users = basicCache();
    users.put("user:123", new User("123", "Alice"));
    User u = users.getIfPresent("user:123");
    User loaded = users.get("user:456", k -> new User("456", "Bob"));

    LoadingCache<String, Product> products = loadingCache();
    Product p = products.get("product:1");
    Map<String, Product> batch = products.getAll(List.of("product:1", "product:2"));

    var stats = users.stats();
    System.out.printf("hitRate=%.2f hits=%d misses=%d evictions=%d%n",
        stats.hitRate(), stats.hitCount(), stats.missCount(), stats.evictionCount());
  }
}
