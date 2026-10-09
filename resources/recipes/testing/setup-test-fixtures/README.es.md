# Configurar Fixtures de Test — Recursos complementarios

Archivos complementarios de [Configurar Fixtures de Test (pytest, Jest, JUnit)](https://stackpractices.com/es/recipes/setup-test-fixtures/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `conftest.py` | Fixtures compartidos de pytest: simple, yield/teardown, parametrizado, factory, scope session |
| `test_fixtures.py` | Tests que consumen fixtures de conftest + `@pytest.mark.parametrize` |
| `factories.js` | Helpers factory de Jest con IDs deterministas por contador |
| `fixtures.test.js` | Ciclo de vida Jest: `beforeAll`/`afterAll`, resets en `beforeEach`, uso de factories |
| `TestFixtures.java` | Ciclo de vida JUnit 5: `@BeforeAll`/`@BeforeEach`, método factory, `@ParameterizedTest` |
| `requirements.txt` | Dependencias Python |

## Cómo usarlo

1. Python: `pip install -r requirements.txt` y luego `pytest -v`.
2. JavaScript: `npm install --save-dev jest` y luego `npx jest fixtures.test.js` (ESM: añade `"type": "module"`).
3. Java: añade `junit-jupiter` al scope test y ejecuta `TestFixtures`.

Mantén el estado mutable en scope function/por test y resetea en `beforeEach` — los fallos dependientes del orden vienen de resets omitidos.