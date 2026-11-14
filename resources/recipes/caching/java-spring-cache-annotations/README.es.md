# Anotaciones de caché de Spring con Redis — Código complementario

Archivos Java ejecutables de la receta
[Usar Anotaciones de Caché de Spring con Redis](https://stackpractices.com/es/recipes/java-spring-cache-annotations/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `CacheConfig.java` | `RedisCacheManager` con TTL por defecto y por caché, serialización JSON, un `KeyGenerator` personalizado y un `CacheErrorHandler` que degrada a lecturas sin caché cuando Redis cae. |
| `UserService.java` | `@Cacheable` / `@CachePut` / `@CacheEvict` / `@Caching` / `@CacheConfig` con SpEL correcto: `condition` solo ve argumentos, `unless` y la expulsión post-invocación ven `#result`. |
| `MultiLevelCache.java` | `CompositeCacheManager` con L1 Caffeine + L2 Redis. |
| `User.java`, `UserDto.java`, `UserRepository.java` | Dominio, DTO y repositorio mínimos para que el servicio compile. |
| `application.properties` | Conexión Redis, tipo de caché y un datasource H2 para arrancar sin base de datos real. |
| `docker-compose.yml` | Un Redis 7 desechable para pruebas locales. |
| `pom.xml` | Spring Boot 3.5 con `spring-boot-starter-cache` + `data-redis` + Caffeine para la variante multinivel. |

## Chuleta de evaluación SpEL

| Atributo | Se evalúa | Ve `#result` | Ve argumentos |
| --- | --- | --- | --- |
| `key` | Antes de la llamada | No | Sí |
| `condition` | Antes de la llamada | No | Sí |
| `unless` | Después de la llamada | Sí | Sí |
| `condition` de `@CacheEvict` (`beforeInvocation = false` por defecto) | Después de la llamada | Sí | Sí |

## Ejecutar

```bash
docker compose up -d        # Redis en :6379
./mvnw spring-boot:run      # o mvn spring-boot:run
```

Inspecciona lo que cae en Redis — las claves tienen forma `nombreCache::clave`:

```bash
docker exec -it $(docker ps -qf name=redis) redis-cli KEYS 'users::*'
docker exec -it $(docker ps -qf name=redis) redis-cli TTL 'users::42'
```
