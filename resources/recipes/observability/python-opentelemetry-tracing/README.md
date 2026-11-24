# Distributed Tracing with OpenTelemetry

Runnable companion code for the StackPractices recipe
[Distributed Tracing with OpenTelemetry](https://stackpractices.com/recipes/python-opentelemetry-tracing/).

## Contents

- `tracing_setup.py` — `setup_tracer()` with console/Jaeger/OTLP exporters,
  `ParentBased(TraceIdRatioBased)` sampling, `instrument_requests()`, and
  `inject_context`/`extract_context` propagation helpers.
- `main.py` — demo that creates nested spans with attributes, an event, and a
  recorded exception; exports to the console so no Jaeger instance is needed.
- `requirements.txt` — OpenTelemetry SDK, Jaeger and OTLP exporters, requests
  instrumentation.

## Usage

```bash
pip install -r requirements.txt
python main.py   # prints spans to stdout
```

For Jaeger export, run `setup_tracer(exporter="jaeger")` with Jaeger all-in-one
on `localhost:6831` (see the recipe for the Docker command).
