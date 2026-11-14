# Java Testcontainers Integration Tests

Runnable companion project for the StackPractices recipe
[Java Testcontainers Integration Tests](https://stackpractices.com/recipes/java-testcontainers-integration/).

Spin up real Postgres, Redis, and Kafka containers inside JUnit5 tests with
Testcontainers 1.21.x — no mocks, no H2, no hand-maintained fixtures.

## Requirements

- JDK 17+
- Maven 3.8+
- A running Docker daemon (`docker info` must succeed — Docker Desktop,
  Colima, or Rancher Desktop all work)

## Contents

| File | What it shows |
| --- | --- |
| `src/test/java/PostgresIntegrationTest.java` | `@Testcontainers` + `@Container` with `PostgreSQLContainer`, real JDBC query |
| `src/test/java/RedisIntegrationTest.java` | `GenericContainer` with a mapped port and `getMappedPort(6379)` |
| `src/test/java/KafkaIntegrationTest.java` | `KafkaContainer` with `DockerImageName`, produce/consume round-trip |
| `src/test/java/BaseIntegrationTest.java` | Shared static container pattern with `withReuse(true)` |
| `github-actions/testcontainers.yml` | CI job: image pre-pull + `mvn verify` |
| `pom.xml` | `testcontainers-bom` 1.21.3 managing all module versions |

## Run

```bash
mvn verify
```

The first run downloads the images (Postgres ~80 MB, Redis ~30 MB, Kafka ~700 MB).
Later runs reuse them. To keep containers alive between local runs, create
`~/.testcontainers.properties` with `testcontainers.reuse.enable=true`.

## Layout

```text
├── pom.xml                          # BOM-managed dependencies
├── src/test/java/
│   ├── PostgresIntegrationTest.java
│   ├── RedisIntegrationTest.java
│   ├── KafkaIntegrationTest.java
│   └── BaseIntegrationTest.java     # shared static container
└── github-actions/
    └── testcontainers.yml           # drop-in CI job
```

Related recipe in Spanish: [versión en español](https://stackpractices.com/es/recipes/java-testcontainers-integration/).
