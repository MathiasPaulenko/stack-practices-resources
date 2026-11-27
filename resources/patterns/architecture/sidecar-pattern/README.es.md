# Patrón Sidecar — Ejemplos de código

Ejemplos complementarios del recurso [Patrón Sidecar](https://stackpractices.com/es/patterns/sidecar-pattern/) en StackPractices.

## Archivos

- `kubernetes-pod.yaml` — Pod con un contenedor de app y dos sidecars (Fluent Bit para logs y un recargador de config) compartiendo volúmenes `emptyDir`.
- `fluentbit-sidecar.yaml` — ConfigMap + Deployment de Fluent Bit: la app escribe logs a un volumen compartido y el sidecar los envía a Elasticsearch.
- `envoy-tls-sidecar.yaml` — Config completa del listener de Envoy: termina TLS en :8443 y reenvía HTTP plano a la app en `127.0.0.1:8080`.
- `metrics_sidecar.py` — Sidecar en Python que lee el endpoint `/metrics` de la app y lo sube a un pushgateway de Prometheus.
- `docker-compose.yaml` — Versión Compose del patrón: servicios hermanos que comparten un volumen nombrado, para desarrollo local.
- `ConfigReloaderSidecar.java` — Sidecar en Java que vigila un directorio de configuración y llama al endpoint de recarga de la app por localhost.
- `istio-injection.yaml` — Label de namespace + Deployment para la inyección automática del sidecar de Envoy (variante service mesh).
- `init-container.yaml` — Init container que prepara un volumen compartido antes de que arranquen la app y el sidecar.

## Notas

- `metrics_sidecar.py` requiere `requests` y `prometheus-client` (`pip install requests prometheus-client`).
- Los ejemplos de Kubernetes asumen que un ConfigMap o un sistema externo llena los volúmenes compartidos.

## Licencia

Los ejemplos de código se proporcionan con fines educativos como parte de StackPractices.
