# Guía de OpenTelemetry — Recursos complementarios

Ejemplos ejecutables de la [guía de OpenTelemetry](https://stackpractices.com/es/guides/opentelemetry-guide/) de StackPractices.

## Contenido

- `otel-collector-config.yaml` — pipeline del Collector con forma de producción: receivers OTLP (4317/4318), `batch`, `resourcedetection`, políticas de `tail_sampling` (errores, trazas lentas, 10 % de base) y exporters para Jaeger, Prometheus remote write y Loki vía OTLP/HTTP nativo.
- `python-instrumented-app.py` — instrumentación manual mínima y funcional: `TracerProvider` + `BatchSpanProcessor`, `MeterProvider` + `PeriodicExportingMetricReader`, atributos de recurso y flush correcto al cerrar.
- `docker-compose.yml` — stack local: OpenTelemetry Collector + Jaeger all-in-one (UI en `http://localhost:16686`).

## Inicio rápido

```bash
docker compose up -d          # levanta collector + jaeger
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
python python-instrumented-app.py
```

Abre `http://localhost:16686`, elige `demo-service` y verás los tres spans (`/api/users`, `/api/orders`, `/fail`) con el error simulado marcado.

## Notas

- `tls.insecure: true` en la configuración del Collector es solo para local. Usa TLS real o un service mesh en producción.
- Los exporters de Loki y Mimir en `otel-collector-config.yaml` asumen que esos servicios existen; elimínalos o cámbialos según tu stack.
- El muestreo en cabeza se ajusta con `OTEL_TRACES_SAMPLER` / `OTEL_TRACES_SAMPLER_ARG` antes de ejecutar la app.
