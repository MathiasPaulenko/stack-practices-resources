import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.data.redis.core.RedisTemplate;

import java.util.concurrent.TimeUnit;

/**
 * Two-level cache: Caffeine as L1 (in-process, sub-microsecond),
 * Redis as L2 (shared source of truth across instances).
 * Keep the L1 TTL short — every L1 entry can be stale relative to L2.
 */
public class MultiLevelCache {

  private final Cache<String, String> l1 = Caffeine.newBuilder()
      .maximumSize(1_000)
      .expireAfterWrite(5, TimeUnit.MINUTES)
      .build();

  private final RedisTemplate<String, String> l2;

  public MultiLevelCache(RedisTemplate<String, String> l2) {
    this.l2 = l2;
  }

  public String get(String key) {
    String l1Value = l1.getIfPresent(key);
    if (l1Value != null) return l1Value;

    String l2Value = l2.opsForValue().get(key);
    if (l2Value != null) {
      l1.put(key, l2Value); // Populate L1 for the next read
      return l2Value;
    }

    String dbValue = fetchFromDb(key);
    l1.put(key, dbValue);
    l2.opsForValue().set(key, dbValue, 30, TimeUnit.MINUTES);
    return dbValue;
  }

  private String fetchFromDb(String key) {
    return "db:" + key;
  }
}
