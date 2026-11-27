# Sidecar Pattern — Code Examples

Companion examples for the [Sidecar Pattern](https://stackpractices.com/patterns/sidecar-pattern/) resource on StackPractices.

## Files

- `kubernetes-pod.yaml` — Pod with an app container plus two sidecars (Fluent Bit log forwarder and a config reloader) sharing `emptyDir` volumes.
- `fluentbit-sidecar.yaml` — Fluent Bit ConfigMap + Deployment: app writes logs to a shared volume, the sidecar ships them to Elasticsearch.
- `envoy-tls-sidecar.yaml` — Full Envoy listener config: terminates TLS on :8443 and forwards plain HTTP to the app on `127.0.0.1:8080`.
- `metrics_sidecar.py` — Python sidecar that scrapes the app's `/metrics` endpoint and pushes to a Prometheus pushgateway.
- `docker-compose.yaml` — Compose version of the pattern: sibling services sharing a named volume, for local development.
- `ConfigReloaderSidecar.java` — Java sidecar that watches a config directory and calls the app's reload endpoint over localhost.
- `istio-injection.yaml` — Namespace label + Deployment for automatic Envoy sidecar injection (service mesh variant).
- `init-container.yaml` — Init container that prepares a shared volume before the app and sidecar start.

## Notes

- `metrics_sidecar.py` requires `requests` and `prometheus-client` (`pip install requests prometheus-client`).
- The Kubernetes examples assume a ConfigMap or external system fills the shared volumes.

## License

Code examples are provided for educational purposes as part of StackPractices.
