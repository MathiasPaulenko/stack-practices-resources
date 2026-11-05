# Ejemplos de Property-Based Testing

Recursos complementarios de la [Guía de Property-Based Testing](https://stackpractices.com/es/guides/complete-guide-property-based-testing/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `test_string_properties.py` | Propiedades básicas de Hypothesis (roundtrip, invariantes) |
| `test_user_properties.py` | Estrategias compuestas, `@example`, roundtrip JSON |
| `test_stack_stateful.py` | Tests con estado vía `RuleBasedStateMachine` |
| `conftest.py` | Perfiles dev/ci de Hypothesis (`HYPOTHESIS_PROFILE`) |
| `properties.test.ts` | Suite fast-check: strings, usuarios, pila con estado |
| `package.json` | Dependencias para la suite TypeScript |
| `property-tests.yml` | Workflow de GitHub Actions que corre ambas suites |

## Uso

```bash
# Python — necesita hypothesis + pytest
pip install hypothesis pytest
pytest test_*.py -v

# TypeScript — necesita node 20+
npm install
npm test
```

Consulta la guía para el razonamiento detrás de cada patrón y la tabla de resolución de problemas.
