# Plantilla de Mapa de Dependencias de Servicios

Companion descargable del documento
[Plantilla de Mapa de Dependencias de Servicios](https://stackpractices.com/es/docs/service-dependency-map-template/).

Un mapa de dependencias rellenable para un servicio, más las piezas
operativas que lo mantienen vivo: configuración de servicegraph de OTel
para descubrimiento automático, presets de circuit breaker, un payload de
health check estructurado y un script de descubrimiento estático de
imports.

## Archivos

| Archivo | Propósito |
|---|---|
| `dependency-map-template.md` | La plantilla en blanco de 7 secciones, lista para copiar al repo del servicio |
| `dependency-map-filled-example.md` | La misma plantilla rellenada para un `checkout-service` real, incluida una dependencia transitiva (`fraud-service` vía `payment-service`) |
| `otel-servicegraph.yaml` | Config del OpenTelemetry Collector que exporta métricas llamador-llamado para descubrimiento automático |
| `circuit-breakers.yaml` | Presets de circuit breaker por dependencia, alineados con las banderas de criticidad del mapa |
| `health-check.json` | Payload estructurado de salud de dependencias (ejemplo degradado) |
| `discover_imports.py` | Script de análisis estático que lista las dependencias de imports de un proyecto Python |

## Cómo usarlo

1. Copia `dependency-map-template.md` al repo del servicio (README o
   carpeta `docs/`) y rellena cada sección con honestidad — la columna
   fallback describe lo que el servicio hace *hoy*, no el plan.
2. Reconcilia cada mes contra las métricas de `otel-servicegraph.yaml`:
   cualquier par `(client, server)` en traces pero ausente del mapa es
   desviación.
3. Conecta los valores de `circuit-breakers.yaml` a tu capa de
   resiliencia (Resilience4j, Polly, DestinationRules de Istio).
4. Sirve un payload con la forma de `health-check.json` desde tu endpoint
   de salud; `200` cuando está sano, `503` solo para fallos de ruta
   crítica.
