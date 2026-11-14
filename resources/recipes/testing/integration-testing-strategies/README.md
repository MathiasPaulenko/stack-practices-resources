# Integration Testing Strategies — Companion Project

Runnable examples from the [Integration Testing Strategies recipe](https://stackpractices.com/recipes/integration-testing-strategies/) on StackPractices.

## What's inside

| File | Stack | What it shows |
|------|-------|---------------|
| `OrderServiceIntegrationTest.java` | Spring Boot + Testcontainers | Real PostgreSQL in Docker, dynamic properties, full HTTP-layer test |
| `PaymentGatewayIntegrationTest.java` | JUnit 5 + WireMock | Stubbing a third-party HTTP API and verifying the outgoing request |
| `order-api.pact.spec.ts` | TypeScript + Pact V3 | Consumer-driven contract test producing a pact file |
| `test_orders.py` | pytest + testcontainers | Postgres container fixture + API + DB assertion in one test |
| `integration-tests.yml` | GitHub Actions | CI split: fast unit tests vs. slower integration tests |
| `requirements.txt` | Python | Dependencies for the pytest example |

## Requirements

- Docker (Testcontainers and WireMock need it)
- Java 21 + Maven (or Gradle) for the Spring Boot tests
- Node.js 20+ for the Pact example (`npm i @pact-foundation/pact`)
- Python 3.11+ (`pip install -r requirements.txt`)

## Running

Each file drops into an existing project — they are recipe examples, not a standalone app. Copy the test you need, adjust the subject under test (your `Order`, `PaymentClient`, base URL), and run it with your usual test runner:

```bash
./mvnw verify -Dgroups=integration   # Java
npx jest order-api.pact.spec.ts      # TypeScript
pytest test_orders.py                # Python
```
