import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.cache.support.CompositeCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.data.redis.cache.RedisCacheManager;

/**
 * Two-level cache: L1 Caffeine (in-JVM, microseconds) checked first, L2 Redis
 * (shared across instances) checked second. Keep the Caffeine TTL short —
 * seconds to a minute — so local copies don't go stale for long.
 */
@Configuration
public class MultiLevelCache {

  @Bean
  @Primary
  public CompositeCacheManager cacheManager(
      RedisCacheManager redisManager,
      CaffeineCacheManager caffeineManager) {
    CompositeCacheManager manager = new CompositeCacheManager(
        caffeineManager, // L1 — checked first
        redisManager     // L2 — checked second
    );
    manager.setFallbackToNoOpCache(false);
    return manager;
  }
}
