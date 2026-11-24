# Trazado distribuido con OpenTelemetry

Código ejecutable complementario de la receta de StackPractices
[Trazado distribuido con OpenTelemetry](https://stackpractices.com/es/recipes/python-opentelemetry-tracing/).

## Contenido

- `tracing_setup.py` — `setup_tracer()` con exportadores consola/Jaeger/OTLP,
  sampling `ParentBased(TraceIdRatioBased)`, `instrument_requests()` y los
  helpers de propagación `inject_context`/`extract_context`.
- `main.py` — demo que crea spans anidados con atributos, un evento y una
  excepción registrada; exporta a consola, sin necesitar Jaeger.
- `requirements.txt` — SDK de OpenTelemetry, exportadores Jaeger y OTLP e
  instrumentación de requests.

## Uso

```bash
pip install -r requirements.txt
python main.py   # imprime los spans en stdout
```

Para exportar a Jaeger, usa `setup_tracer(exporter="jaeger")` con Jaeger
all-in-one en `localhost:6831` (la receta incluye el comando Docker).
