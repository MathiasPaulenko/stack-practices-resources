# Kubernetes Ingress — Companion

Manifiestos de Kubernetes para la guía de StackPractices
[Guía Completa de Kubernetes Ingress](https://stackpractices.com/es/guides/complete-guide-kubernetes-ingress/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `ingress/single-service.yaml` | Ingress mínimo: un host, todos los paths a un Service |
| `ingress/path-based-routing.yaml` | Un host repartiendo a Services api/web/default con `pathType: Prefix` |
| `ingress/name-based-vhost.yaml` | Dos hostnames compartiendo la IP del controlador (enrutamiento por Host) |
| `ingress/default-backend.yaml` | `defaultBackend` para un 404 personalizado en rutas sin coincidencia |
| `tls/clusterissuer-letsencrypt.yaml` | ClusterIssuer de cert-manager para Let's Encrypt (HTTP-01) |
| `tls/ingress-tls.yaml` | Ingress terminando TLS con un secret emitido por cert-manager |
| `tls/ingress-passthrough.yaml` | Passthrough TLS al backend (requiere `--enable-ssl-passthrough`) |
| `annotations/common-annotations.yaml` | Rewrite, CORS, rate limit, timeouts, body size, allowlist y afinidad por cookie de ingress-nginx |
| `annotations/basic-auth.yaml` | Autenticación básica htpasswd con secret + bloque de anotaciones |
| `advanced/canary-ingress.yaml` | Ingress canary con reparto de tráfico por `canary-weight` |
| `production/controller-pdb.yaml` | PodDisruptionBudget que mantiene una réplica del controlador durante drains |
| `production/controller-networkpolicy.yaml` | NetworkPolicy que solo admite 80/443 + scraping de métricas al controlador |

## Inicio rápido

```bash
# Instala un controlador mantenido (ejemplo con Traefik)
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik --namespace traefik --create-namespace

# cert-manager para TLS automático
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --set crds.enabled=true

kubectl apply -f tls/clusterissuer-letsencrypt.yaml
kubectl apply -f ingress/
```

Nota: el controlador comunitario `ingress-nginx` fue retirado en marzo de 2026 —
los ejemplos de anotaciones siguen su dialecto porque sigue siendo lo más
desplegado, pero los clusters nuevos deberían usar un controlador mantenido o
Gateway API. Adapta hosts, nombres de servicio, namespaces y CIDRs a tu entorno
antes de aplicar.
