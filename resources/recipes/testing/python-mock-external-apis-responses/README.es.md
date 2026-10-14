# Mockear APIs Externas con responses — Ejemplos ejecutables

Código complementario de la receta de StackPractices
[Mockear APIs Externas con responses](https://stackpractices.com/es/recipes/python-mock-external-apis-responses/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `test_external_api.py` | 10 tests ejecutables: mock básico, `matchers` (query params), simulación de errores/timeout, secuencia de retry ordenada, `add_callback` dinámico, aserción sobre el request body, match de URL con regex, generador streaming, fixture compartido |
| `conftest.py` | Fixture `mock_api` que envuelve `responses.RequestsMock()` para reutilizar entre tests |
| `requirements.txt` | `pytest`, `requests`, `responses>=0.25` |

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Detalle clave

`match_querystring` se deprecó en responses 0.17.0 — usa
`matchers.query_param_matcher` en la lista `match` en su lugar. Las respuestas
registradas para la misma URL se consumen en orden, que es como el test de
retry devuelve 503 y luego 200.
