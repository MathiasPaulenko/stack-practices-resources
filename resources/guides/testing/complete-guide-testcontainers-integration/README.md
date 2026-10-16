# Testcontainers Integration Tests — Multi-Language Companion

Runnable companion for the [Testcontainers guide](https://stackpractices.com/guides/complete-guide-testcontainers-integration/) on StackPractices. Three parallel projects covering the same services (PostgreSQL, Kafka, Redis, custom) in Java, Python, and Node.js.

## Contents

| Directory | What it is |
|-----------|------------|
| `java/` | Maven project: `pom.xml` with the Testcontainers BOM modules plus `PostgresIntegrationTest`, `KafkaIntegrationTest`, `RedisIntegrationTest`, `CustomContainerTest` under `src/test/java`. |
| `python/` | `requirements.txt` + `tests/integration/` with `test_postgres.py`, `test_redis.py`, `test_kafka.py` (pytest fixtures). |
| `node/` | `package.json` + `tests/integration/` with `postgres.test.ts` and `redis.test.ts` (vitest). |
| `.github/workflows/` | `integration-tests.yml` — the CI job from the guide's "Running in CI" section. |

## Run it

Docker must be running on your machine (or CI runner).

```bash
# Java
cd java && mvn verify

# Python
cd python && pip install -r requirements.txt && pytest tests/integration

# Node.js
cd node && npm install && npm test
```

Source guide: https://stackpractices.com/guides/complete-guide-testcontainers-integration/
