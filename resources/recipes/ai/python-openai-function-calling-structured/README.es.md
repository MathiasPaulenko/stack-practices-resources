# Salida JSON estructurada con OpenAI Function Calling

Código ejecutable complementario de la receta de StackPractices
[Salida JSON estructurada con OpenAI Function Calling](https://stackpractices.com/es/recipes/python-openai-function-calling-structured/).

## Contenido

- `structured_extract.py` — esquemas Pydantic (`ProductReview`, `SearchQuery`,
  `CalculationRequest`), extracción con function calling, `response_format`
  con `json_schema` + `strict`, reintentos con backoff exponencial ante
  `RateLimitError`, manejo de rechazos y extracción en batch.
- `main.py` — demo que extrae un `ProductReview` tipado desde texto libre.
- `requirements.txt` — dependencias fijadas (`openai`, `pydantic`).

## Uso

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```

Requiere una API key de OpenAI. Consulta la receta para la explicación
completa de strict mode, rechazos y semántica de reintentos.
