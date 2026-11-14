# Configuración de Caffeine Cache — Código complementario

Ejemplos Java ejecutables de la receta
[Configurar Caffeine Cache en Java con Políticas de Expulsión](https://stackpractices.com/es/recipes/java-caffeine-cache-configuration/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `EvictionPolicies.java` | Ejemplos standalone del builder: tamaño, TTL por escritura/acceso, peso, carga+refresco, referencias débiles, scheduler. Incluye un `main` que ejercita el caché e imprime `CacheStats`. |
| `CacheConfig.java` | `@Configuration` de Spring con `CaffeineCacheManager` global y configuraciones por caché vía `registerCustomCache`. |
| `UserService.java` | Anotaciones `@Cacheable` / `@CachePut` / `@CacheEvict` respaldadas por Caffeine. |
| `User.java`, `UserRepository.java` | Stubs mínimos de dominio y repositorio para que el servicio compile. |
| `MultiLevelCache.java` | Consulta de dos niveles L1 Caffeine + L2 Redis con relleno en lectura. |
| `application.properties` | Alternativa declarativa: `spring.cache.caffeine.spec`. |

## Dependencias

```xml
<dependency>
  <groupId>com.github.ben-manes.caffeine</groupId>
  <artifactId>caffeine</artifactId>
  <version>3.1.8</version>
</dependency>
<!-- Solo integración Spring -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
<!-- Solo MultiLevelCache -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

## Ejecutar

`EvictionPolicies` es autocontenido: compílalo con el jar de Caffeine en el
classpath y ejecuta `main`. Los archivos de Spring necesitan un contexto de
Spring Boot 3+; `MultiLevelCache` además necesita un bean `RedisTemplate` y un
Redis en ejecución.
