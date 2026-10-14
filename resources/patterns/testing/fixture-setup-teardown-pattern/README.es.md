# Patrón Fixture Setup/Teardown — Código complementario

Ejemplos ejecutables que acompañan al recurso de StackPractices:
<https://stackpractices.com/es/patterns/fixture-setup-teardown-pattern/>

## Contenido

| Archivo | Qué muestra |
|---------|-------------|
| `conftest.py` | Fixtures de pytest: scopes function/module/session, teardown con `yield`, restauración de variables de entorno, objeto fixture, postgres en Docker con espera activa |
| `test_users.py` | Tests que consumen esos fixtures (estado limpio, mock de notificaciones, SQLite temporal) |
| `jest_fixtures.test.js` | `beforeEach`/`afterEach` en Jest, setup en `describe` anidados, fábricas `createTestUser`/`createTestOrder` |
| `UserServiceTest.java` | Ciclo de vida JUnit 5: `@BeforeEach`/`@AfterEach`/`@BeforeAll`/`@AfterAll` |

## Ejecutar

```bash
# Python (pytest >= 7)
cd fixture-setup-teardown-pattern
pip install pytest
pytest -v

# JavaScript (Jest >= 29)
npm i -D jest
npx jest jest_fixtures.test.js

# Java (JUnit 5)
mvn test   # con junit-jupiter en el classpath
```

El fixture `postgres_container` necesita Docker en el `PATH`; es de scope
session y espera con `pg_isready` en vez de dormir a ciegas.
