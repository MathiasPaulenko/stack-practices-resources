# Fixtures y Parametrize de Pytest — Recursos complementarios

Archivos complementarios de [Fixtures y Parametrize de Pytest](https://stackpractices.com/es/recipes/python-pytest-fixtures-parametrize/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `conftest.py` | Fixtures compartidos: env con scope session, fixture indirecto vía `request.param`, fixture parametrizado con `params`, cleanup autouse |
| `test_parametrize.py` | Tests con fixtures yield, parametrize multi-input, IDs con `pytest.param`, parametrize indirecto, fixtures parametrizados y un caso salteado |
| `requirements.txt` | Dependencias de Python |

## Cómo usar

1. Instalá: `pip install -r requirements.txt`
2. Corré: `pytest -v` — todos los tests y casos parametrizados deberían pasar (un caso se saltea a propósito para mostrar `marks=pytest.mark.skip`).

Flags útiles: `pytest -v -k palindrome`, `pytest -v test_parametrize.py::test_is_palindrome[simple_palindrome]` para correr un solo caso parametrizado por su `id=`.
