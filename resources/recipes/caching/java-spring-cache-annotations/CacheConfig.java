import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import org.springframework.cache.Cache;
import org.springframework.cache.annotation.CachingConfigurer;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.interceptor.CacheErrorHandler;
import org.springframework.cache.interceptor.KeyGenerator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Redis-backed cache configuration: default 10-minute TTL, per-cache TTL
 * overrides, JSON serialization, a custom key generator, and an error handler
 * that degrades to uncached calls when Redis is unreachable.
 */
@Configuration
@EnableCaching
public class CacheConfig implements CachingConfigurer {

  private static final Logger log = LoggerFactory.getLogger(CacheConfig.class);

  @Bean
  public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
    RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
        .entryTtl(Duration.ofMinutes(10))
        .disableCachingNullValues()
        .serializeValuesWith(
            RedisSerializationContext.SerializationPair.fromSerializer(
                new GenericJackson2JsonRedisSerializer()));

    // Per-cache TTL overrides
    Map<String, RedisCacheConfiguration> cacheConfigs = new HashMap<>();
    cacheConfigs.put("users", config.entryTtl(Duration.ofMinutes(5)));
    cacheConfigs.put("products", config.entryTtl(Duration.ofMinutes(30)));
    cacheConfigs.put("config", config.entryTtl(Duration.ofHours(24)));

    return RedisCacheManager.builder(factory)
        .cacheDefaults(config)
        .withInitialCacheConfigurations(cacheConfigs)
        .transactionAware()
        .build();
  }

  /**
   * Custom key generator: ClassName:method:paramHash:... — referenced from
   * annotations with keyGenerator = "customKeyGenerator".
   */
  @Bean
  public KeyGenerator customKeyGenerator() {
    return (target, method, params) -> {
      StringBuilder sb = new StringBuilder();
      sb.append(target.getClass().getSimpleName()).append(":");
      sb.append(method.getName()).append(":");
      for (Object param : params) {
        sb.append(param == null ? "null" : param.hashCode()).append(":");
      }
      return sb.toString();
    };
  }

  /**
   * When Redis is down every cache operation throws by default. This handler
   * logs the failure and lets the call fall through to the real method,
   * trading cache errors for uncached reads.
   */
  @Bean
  @Override
  public CacheErrorHandler errorHandler() {
    return new CacheErrorHandler() {
      @Override
      public void handleCacheGetError(RuntimeException e, Cache cache, Object key) {
        log.warn("Cache get failed for {}::{}", cache.getName(), key, e);
      }

      @Override
      public void handleCachePutError(RuntimeException e, Cache cache, Object key, Object value) {
        log.warn("Cache put failed for {}::{}", cache.getName(), key, e);
      }

      @Override
      public void handleCacheEvictError(RuntimeException e, Cache cache, Object key) {
        log.warn("Cache evict failed for {}::{}", cache.getName(), key, e);
      }

      @Override
      public void handleCacheClearError(RuntimeException e, Cache cache) {
        log.warn("Cache clear failed for {}", cache.getName(), e);
      }
    };
  }
}
