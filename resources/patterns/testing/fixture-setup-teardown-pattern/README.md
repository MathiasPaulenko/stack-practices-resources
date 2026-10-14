# Fixture Setup/Teardown Pattern — Companion Code

Runnable examples accompanying the StackPractices resource:
<https://stackpractices.com/patterns/fixture-setup-teardown-pattern/>

## Contents

| File | What it shows |
|------|---------------|
| `conftest.py` | pytest fixtures: function/module/session scopes, `yield` teardown, env-var restore, fixture object, Docker postgres with readiness polling |
| `test_users.py` | Tests consuming those fixtures (fresh state, notification mock, temp SQLite) |
| `jest_fixtures.test.js` | Jest `beforeEach`/`afterEach`, nested `describe` setup, `createTestUser`/`createTestOrder` factories |
| `UserServiceTest.java` | JUnit 5 `@BeforeEach`/`@AfterEach`/`@BeforeAll`/`@AfterAll` lifecycle |

## Run

```bash
# Python (pytest >= 7)
cd fixture-setup-teardown-pattern
pip install pytest
pytest -v

# JavaScript (Jest >= 29)
npm i -D jest
npx jest jest_fixtures.test.js

# Java (JUnit 5)
mvn test   # with junit-jupiter on the classpath
```

The `postgres_container` fixture needs Docker on `PATH`; it is session-scoped
and polls `pg_isready` instead of sleeping blindly.
