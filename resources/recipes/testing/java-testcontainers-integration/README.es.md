# Tests de integración con Testcontainers en Java

Proyecto ejecutable complementario de la receta de StackPractices
[Testcontainers para tests de integración en Java](https://stackpractices.com/es/recipes/java-testcontainers-integration/).

Levanta contenedores reales de Postgres, Redis y Kafka dentro de tests JUnit5
con Testcontainers 1.21.x — sin mocks, sin H2, sin fixtures mantenidos a mano.

## Requisitos

- JDK 17+
- Maven 3.8+
- Un daemon de Docker corriendo (`docker info` debe funcionar — vale Docker
  Desktop, Colima o Rancher Desktop)

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `src/test/java/PostgresIntegrationTest.java` | `@Testcontainers` + `@Container` con `PostgreSQLContainer`, query JDBC real |
| `src/test/java/RedisIntegrationTest.java` | `GenericContainer` con puerto mapeado y `getMappedPort(6379)` |
| `src/test/java/KafkaIntegrationTest.java` | `KafkaContainer` con `DockerImageName`, ida y vuelta produce/consume |
| `src/test/java/BaseIntegrationTest.java` | Patrón de contenedor estático compartido con `withReuse(true)` |
| `github-actions/testcontainers.yml` | Job de CI: descarga previa de imágenes + `mvn verify` |
| `pom.xml` | `testcontainers-bom` 1.21.3 gestionando todas las versiones |

## Ejecutar

```bash
mvn verify
```

La primera ejecución descarga las imágenes (Postgres ~80 MB, Redis ~30 MB,
Kafka ~700 MB). Las siguientes las reutilizan. Para mantener los contenedores
vivos entre ejecuciones locales, crea `~/.testcontainers.properties` con
`testcontainers.reuse.enable=true`.

## Estructura

```text
├── pom.xml                          # dependencias gestionadas por BOM
├── src/test/java/
│   ├── PostgresIntegrationTest.java
│   ├── RedisIntegrationTest.java
│   ├── KafkaIntegrationTest.java
│   └── BaseIntegrationTest.java     # contenedor estático compartido
└── github-actions/
    └── testcontainers.yml           # job de CI listo para copiar
```
