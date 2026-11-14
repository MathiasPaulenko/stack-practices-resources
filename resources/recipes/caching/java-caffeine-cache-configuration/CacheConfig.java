import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

/**
 * Spring Boot cache configuration backed by Caffeine.
 * Global spec for the default manager, per-cache specs via registerCustomCache.
 */
@Configuration
@EnableCaching
public class CacheConfig {

  @Bean
  public CaffeineCacheManager cacheManager() {
    CaffeineCacheManager manager = new CaffeineCacheManager();
    manager.setCaffeine(Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(30, TimeUnit.MINUTES)
        .recordStats());
    return manager;
  }

  @Bean
  public CacheManager multiCacheManager() {
    CaffeineCacheManager manager = new CaffeineCacheManager("users", "products", "config");
    manager.registerCustomCache("users", Caffeine.newBuilder()
        .maximumSize(5_000)
        .expireAfterWrite(10, TimeUnit.MINUTES)
        .build());
    manager.registerCustomCache("products", Caffeine.newBuilder()
        .maximumSize(20_000)
        .expireAfterWrite(30, TimeUnit.MINUTES)
        .build());
    return manager;
  }
}
