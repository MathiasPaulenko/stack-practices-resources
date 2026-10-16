# Tests de integración con Testcontainers — Companion Multi-Lenguaje

Companion ejecutable de la [guía de Testcontainers](https://stackpractices.com/es/guides/complete-guide-testcontainers-integration/) en StackPractices. Tres proyectos paralelos cubriendo los mismos servicios (PostgreSQL, Kafka, Redis, personalizado) en Java, Python y Node.js.

## Contenido

| Directorio | Qué es |
|------------|--------|
| `java/` | Proyecto Maven: `pom.xml` con los módulos del BOM de Testcontainers más `PostgresIntegrationTest`, `KafkaIntegrationTest`, `RedisIntegrationTest`, `CustomContainerTest` bajo `src/test/java`. |
| `python/` | `requirements.txt` + `tests/integration/` con `test_postgres.py`, `test_redis.py`, `test_kafka.py` (fixtures de pytest). |
| `node/` | `package.json` + `tests/integration/` con `postgres.test.ts` y `redis.test.ts` (vitest). |
| `.github/workflows/` | `integration-tests.yml` — el job de CI de la sección "Ejecutar en CI" de la guía. |

## Ejecútalo

Docker debe estar corriendo en tu máquina (o en el runner de CI).

```bash
# Java
cd java && mvn verify

# Python
cd python && pip install -r requirements.txt && pytest tests/integration

# Node.js
cd node && npm install && npm test
```

Guía fuente: https://stackpractices.com/es/guides/complete-guide-testcontainers-integration/
