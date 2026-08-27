# Proyecto de ejemplo de pytest-cov

Proyecto companion para la receta de StackPractices [Medir y Exigir Cobertura de Tests con pytest-cov](https://stackpractices.com/es/recipes/python-coverage-pytest-cov/).

## Archivos

- `pyproject.toml` — configuración de cobertura con `[tool.coverage.*]`.
- `.coveragerc` — archivo de configuración legacy de `coverage.py`.
- `tox.ini` — ejecuta tests en varias versiones de Python con `pytest-cov`.
- `github_actions_coverage.yml` — workflow de GitHub Actions con Codecov y `diff-cover`.
- `sample_app/` — paquete mínimo con `User` y `UserService`.
- `tests/` — suite de tests con pytest.

## Inicio rápido

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -e ".[test]"
pytest
```

Esto ejecuta los tests y exige `fail_under = 80` con branch coverage.

## Comandos útiles

```bash
pytest --cov=sample_app --cov-report=html
pytest -n auto --cov=sample_app --cov-report=term-missing
coverage combine
coverage report
diff-cover coverage.xml --compare-branch=origin/main --fail-under=100
```
