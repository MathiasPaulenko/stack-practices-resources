# Spring Cache Annotations with Redis — Companion Code

Runnable Java files from the recipe
[Use Spring Cache Annotations with Redis Backend](https://stackpractices.com/recipes/java-spring-cache-annotations/).

## Files

| File | What it shows |
| --- | --- |
| `CacheConfig.java` | `RedisCacheManager` with default + per-cache TTLs, JSON serialization, a custom `KeyGenerator`, and a `CacheErrorHandler` that degrades to uncached reads when Redis is down. |
| `UserService.java` | `@Cacheable` / `@CachePut` / `@CacheEvict` / `@Caching` / `@CacheConfig` with correct SpEL usage: `condition` sees arguments only, `unless` and post-invocation evict see `#result`. |
| `MultiLevelCache.java` | `CompositeCacheManager` wiring L1 Caffeine + L2 Redis. |
| `User.java`, `UserDto.java`, `UserRepository.java` | Minimal domain, DTO, and repository stubs so the service compiles. |
| `application.properties` | Redis connection, cache type, and an H2 datasource so the app boots without a real database. |
| `docker-compose.yml` | A throwaway Redis 7 for local runs. |
| `pom.xml` | Spring Boot 3.5 with `spring-boot-starter-cache` + `data-redis` + Caffeine for the multi-level variant. |

## SpEL timing cheat sheet

| Attribute | Evaluated | Sees `#result` | Sees args |
| --- | --- | --- | --- |
| `key` | Before the call | No | Yes |
| `condition` | Before the call | No | Yes |
| `unless` | After the call | Yes | Yes |
| `@CacheEvict` `condition` (default `beforeInvocation = false`) | After the call | Yes | Yes |

## Run

```bash
docker compose up -d        # Redis on :6379
./mvnw spring-boot:run      # or mvn spring-boot:run
```

Inspect what lands in Redis — keys are shaped `cacheName::key`:

```bash
docker exec -it $(docker ps -qf name=redis) redis-cli KEYS 'users::*'
docker exec -it $(docker ps -qf name=redis) redis-cli TTL 'users::42'
```
