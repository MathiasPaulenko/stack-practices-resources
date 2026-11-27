# Descubrimiento de servicios — Código complementario

Ejemplos ejecutables para la receta [Descubrimiento de servicios](https://stackpractices.com/es/recipes/service-discovery/) de StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `consul_register.go` | Registro en Consul con health check HTTP, `DeregisterCriticalServiceAfter` y desregistro elegante al recibir SIGTERM — un proceso que se cae se limpia solo. |
| `consul_discovery.py` | Descubrimiento client-side con caché local de 30 segundos más un fallback de «último estado conocido» sin expiración, para que una caída del registro no tumbe a tus clientes. Requiere `python-consul` y `requests`. |
| `health_check.go` | Handlers separados de liveness/readiness: liveness reinicia el proceso, readiness lo saca del pool durante el arranque o fallos de dependencias. |
| `istio-traffic.yaml` | VirtualService (canary 90/10 + reintentos) y DestinationRule (LEAST_REQUEST + detección de outliers) — política de tráfico sobre el descubrimiento de Kubernetes. |
| `pooled_client.py` | Pooling de conexiones por instancia: una `requests.Session` por URL descubierta en lugar de un handshake TCP nuevo por petición. |

## Inicio rápido

```bash
# Requiere un agente Consul en localhost:8500
go run consul_register.go

pip install python-consul requests
python consul_discovery.py

go run health_check.go
curl localhost:8080/ready

kubectl apply -f istio-traffic.yaml
```

## Qué adaptar para producción

- La caché de cliente de 30 segundos más un health check de 10 segundos
  significa que una instancia muerta sigue recibiendo tráfico hasta ~40
  segundos — por eso los reintentos ante errores de conexión no son
  opcionales.
- `DeregisterCriticalServiceAfter` es tu red de seguridad para procesos
  que mueren sin desregistrarse; no lo dejes sin configurar.
- En Kubernetes normalmente no necesitas un registro aparte: CoreDNS +
  Endpoints es la capa de descubrimiento, e Istio solo añade política.
