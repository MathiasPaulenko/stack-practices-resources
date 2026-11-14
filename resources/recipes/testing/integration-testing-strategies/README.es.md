# Estrategias de Testing de Integración — Proyecto Companion

Ejemplos ejecutables de la [receta de Estrategias de Testing de Integración](https://stackpractices.com/es/recipes/integration-testing-strategies/) en StackPractices.

## Contenido

| Archivo | Stack | Qué muestra |
|---------|-------|-------------|
| `OrderServiceIntegrationTest.java` | Spring Boot + Testcontainers | PostgreSQL real en Docker, propiedades dinámicas, test de capa HTTP completo |
| `PaymentGatewayIntegrationTest.java` | JUnit 5 + WireMock | Stub de una API HTTP de terceros y verificación de la petición saliente |
| `order-api.pact.spec.ts` | TypeScript + Pact V3 | Test de contrato consumer-driven que genera un archivo pact |
| `test_orders.py` | pytest + testcontainers | Fixture de contenedor Postgres + aserción de API y DB en un test |
| `integration-tests.yml` | GitHub Actions | Separación en CI: tests unitarios rápidos vs. integración lentos |
| `requirements.txt` | Python | Dependencias del ejemplo pytest |

## Requisitos

- Docker (Testcontainers y WireMock lo necesitan)
- Java 21 + Maven (o Gradle) para los tests de Spring Boot
- Node.js 20+ para el ejemplo de Pact (`npm i @pact-foundation/pact`)
- Python 3.11+ (`pip install -r requirements.txt`)

## Ejecución

Cada archivo se integra en un proyecto existente — son ejemplos de receta, no una aplicación standalone. Copia el test que necesites, ajusta el sujeto bajo prueba (tu `Order`, `PaymentClient`, URL base) y ejecútalo con tu runner habitual:

```bash
./mvnw verify -Dgroups=integration   # Java
npx jest order-api.pact.spec.ts      # TypeScript
pytest test_orders.py                # Python
```
