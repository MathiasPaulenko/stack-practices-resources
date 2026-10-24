# Guía de Estrategia de Testing de Software — Compañero

Piezas ejecutables que implementan la estrategia de testing en capas descrita en la guía:

- `ci-test-workflow.yml` — workflow de GitHub Actions con las etapas de la pirámide (unit → integration → E2E) y un gate de regresión de coverage en pull requests.
- `unit_tests_pytest.py` — ejemplo de unit test parametrizado (pytest). Ejecuta con `pytest unit_tests_pytest.py -v`.

## Uso

1. Copia `ci-test-workflow.yml` a `.github/workflows/test.yml` en tu repo.
2. Adapta los comandos `npm run test:*` a los scripts de tu proyecto.
3. Mantén el orden de capas: unit tests rápidos primero, E2E costosos al final — ese orden es lo que mantiene el feedback por debajo de ~10 minutos.

Artículo fuente: <https://stackpractices.com/es/guides/testing-strategy-guide/>
