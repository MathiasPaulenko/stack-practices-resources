# Kubernetes Ingress — Companion

Kubernetes manifests for the StackPractices guide
[Complete Guide to Kubernetes Ingress](https://stackpractices.com/guides/complete-guide-kubernetes-ingress/).

## Files

| File | Description |
|------|-------------|
| `ingress/single-service.yaml` | Minimal Ingress: one host, all paths to one Service |
| `ingress/path-based-routing.yaml` | One host fanning out to api/web/default Services with `pathType: Prefix` |
| `ingress/name-based-vhost.yaml` | Two hostnames sharing the controller IP (Host-header routing) |
| `ingress/default-backend.yaml` | `defaultBackend` for a custom 404 on unmatched requests |
| `tls/clusterissuer-letsencrypt.yaml` | cert-manager ClusterIssuer for Let's Encrypt (HTTP-01) |
| `tls/ingress-tls.yaml` | Ingress terminating TLS with a cert-manager-issued secret |
| `tls/ingress-passthrough.yaml` | TLS passthrough to the backend (needs `--enable-ssl-passthrough`) |
| `annotations/common-annotations.yaml` | ingress-nginx rewrite, CORS, rate limit, timeouts, body size, allowlist, cookie affinity |
| `annotations/basic-auth.yaml` | htpasswd basic auth via secret + annotation block |
| `advanced/canary-ingress.yaml` | Canary Ingress with `canary-weight` traffic split |
| `production/controller-pdb.yaml` | PodDisruptionBudget keeping one controller replica alive during drains |
| `production/controller-networkpolicy.yaml` | NetworkPolicy admitting only 80/443 + metrics scraping to the controller |

## Quick start

```bash
# Install a maintained controller (Traefik example)
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik --namespace traefik --create-namespace

# cert-manager for automatic TLS
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --set crds.enabled=true

kubectl apply -f tls/clusterissuer-letsencrypt.yaml
kubectl apply -f ingress/
```

Note: the `ingress-nginx` community controller was retired in March 2026 — the
annotation examples follow its dialect because it remains the most widely
deployed, but new clusters should use a maintained controller or Gateway API.
Adapt hosts, service names, namespaces and CIDRs to your environment before
applying.
