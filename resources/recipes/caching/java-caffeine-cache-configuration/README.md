# Caffeine Cache Configuration — Companion Code

Runnable Java examples from the recipe
[Configure Caffeine Cache in Java with Eviction Policies](https://stackpractices.com/recipes/java-caffeine-cache-configuration/).

## Files

| File | What it shows |
| --- | --- |
| `EvictionPolicies.java` | Standalone builder examples: size, write/access TTL, weighted, loading+refresh, weak refs, scheduler. Includes a `main` that exercises the cache and prints `CacheStats`. |
| `CacheConfig.java` | Spring `@Configuration` with a global `CaffeineCacheManager` and per-cache specs via `registerCustomCache`. |
| `UserService.java` | `@Cacheable` / `@CachePut` / `@CacheEvict` annotations backed by Caffeine. |
| `User.java`, `UserRepository.java` | Minimal domain + repository stubs so the service compiles. |
| `MultiLevelCache.java` | L1 Caffeine + L2 Redis two-level lookup with populate-on-read. |
| `application.properties` | Declarative alternative: `spring.cache.caffeine.spec`. |

## Dependencies

```xml
<dependency>
  <groupId>com.github.ben-manes.caffeine</groupId>
  <artifactId>caffeine</artifactId>
  <version>3.1.8</version>
</dependency>
<!-- Spring integration only -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
<!-- MultiLevelCache only -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

## Run

`EvictionPolicies` is self-contained — compile it with the Caffeine jar on the
classpath and run `main`. The Spring files need a Spring Boot 3+ context;
`MultiLevelCache` additionally needs a `RedisTemplate` bean and a running Redis.
