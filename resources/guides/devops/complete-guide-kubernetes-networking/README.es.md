# Networking en Kubernetes — Companion

Manifiestos desplegables de la guía de StackPractices
[Guía Completa de Networking en Kubernetes](https://stackpractices.com/es/guides/complete-guide-kubernetes-networking/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `services/clusterip.yaml` | ClusterIP interno con puertos `http`/`metrics` nombrados |
| `services/nodeport.yaml` | NodePort en 30080 para balanceadores externos o acceso en dev |
| `services/loadbalancer-local.yaml` | Anotaciones AWS NLB + `externalTrafficPolicy: Local` (conserva la IP del cliente) |
| `services/headless.yaml` | `clusterIP: None` para identidad DNS de pods en StatefulSet |
| `ingress/ingress-nginx.yaml` | Enrutado por path con ingress-nginx, TLS, rate limit y cabeceras de seguridad |
| `ingress/ingress-cert-manager.yaml` | ClusterIssuer (Let's Encrypt HTTP-01) + Ingress anotado |
| `network-policies/default-deny.yaml` | Aislamiento base de ingress + egress para el namespace |
| `network-policies/allow-ingress-controller.yaml` | Permiso estrecho: controlador -> api, api -> postgres + DNS (UDP/TCP 53) |
| `network-policies/micro-segmentation.yaml` | Conjunto por capas completo frontend -> api -> postgres/redis |
| `dns/custom-dns-pod.yaml` | `dnsConfig`/`dnsPolicy` a nivel de pod con nameservers, searches y ndots |
| `istio/peer-authentication-mtls.yaml` | mTLS STRICT + puerto de métricas PERMISSIVE para scraping |
| `istio/virtualservice-canary.yaml` | VirtualService/DestinationRule canary con cabecera + reparto 90/10 |
| `troubleshooting/debug-commands.sh` | Flujo de depuración ordenado: endpoints -> DNS -> conectividad -> políticas -> CNI |

## Inicio rápido

```bash
# Despliega primero la capa de servicios
kubectl apply -f services/clusterip.yaml

# Después el punto de entrada ingress (requiere un controlador instalado)
kubectl apply -f ingress/ingress-nginx.yaml

# Bloquea el tráfico (requiere un CNI que aplique NetworkPolicy)
kubectl apply -f network-policies/default-deny.yaml
kubectl apply -f network-policies/micro-segmentation.yaml

# Depura cuando algo se rompa
NAMESPACE=production POD=<pod-name> SVC=api-service ./troubleshooting/debug-commands.sh
```

Sustituye los hosts `stackpractices.com`, los namespaces y el ARN del
certificado ACM por tus propios valores antes de aplicar.
