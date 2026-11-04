# Kubernetes Networking — Companion

Deployable manifests for the StackPractices guide
[Complete Guide to Kubernetes Networking](https://stackpractices.com/guides/complete-guide-kubernetes-networking/).

## Files

| File | Description |
|------|-------------|
| `services/clusterip.yaml` | Internal ClusterIP with named `http`/`metrics` ports |
| `services/nodeport.yaml` | NodePort on 30080 for external-LB targets or dev access |
| `services/loadbalancer-local.yaml` | AWS NLB annotations + `externalTrafficPolicy: Local` (client IP preserved) |
| `services/headless.yaml` | `clusterIP: None` for StatefulSet pod DNS identity |
| `ingress/ingress-nginx.yaml` | ingress-nginx path routing, TLS, rate limit, security headers |
| `ingress/ingress-cert-manager.yaml` | ClusterIssuer (Let's Encrypt HTTP-01) + annotated Ingress |
| `network-policies/default-deny.yaml` | Baseline ingress + egress isolation for the namespace |
| `network-policies/allow-ingress-controller.yaml` | Narrow allow: controller -> api, api -> postgres + DNS (UDP/TCP 53) |
| `network-policies/micro-segmentation.yaml` | Full frontend -> api -> postgres/redis layered policy set |
| `dns/custom-dns-pod.yaml` | Pod-level `dnsConfig`/`dnsPolicy` with nameservers, searches, ndots |
| `istio/peer-authentication-mtls.yaml` | STRICT mTLS + PERMISSIVE metrics port for scraping |
| `istio/virtualservice-canary.yaml` | Header-match + 90/10 weighted canary VirtualService/DestinationRule |
| `troubleshooting/debug-commands.sh` | Ordered debug workflow: endpoints -> DNS -> connectivity -> policy -> CNI |

## Quick start

```bash
# Deploy the service layer first
kubectl apply -f services/clusterip.yaml

# Then the ingress entry point (needs an ingress controller installed)
kubectl apply -f ingress/ingress-nginx.yaml

# Lock down traffic (requires a CNI that enforces NetworkPolicy)
kubectl apply -f network-policies/default-deny.yaml
kubectl apply -f network-policies/micro-segmentation.yaml

# Debug when something breaks
NAMESPACE=production POD=<pod-name> SVC=api-service ./troubleshooting/debug-commands.sh
```

Replace the `stackpractices.com` hosts, namespaces, and the ACM certificate
ARN with your own values before applying.
