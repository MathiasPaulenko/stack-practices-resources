# Guía Básica de Kubernetes — Manifiestos Companion

Manifiestos listos para aplicar de la [guía básica de Kubernetes](https://stackpractices.com/es/guides/kubernetes-basics-guide/) en StackPractices.

## Contenido

| Archivo | Qué hace |
|---|---|
| `pod.yaml` | Pod mínimo de un contenedor con label y variable de entorno |
| `deployment.yaml` | Deployment de 3 réplicas con requests/limits de recursos |
| `service.yaml` | Service ClusterIP que selecciona los pods `app: myapp` |
| `configmap.yaml` | ConfigMap con dos claves estilo env |
| `production-deployment.yaml` | Deployment de producción: probes, env desde secret, anti-affinity, `maxUnavailable: 0` |
| `hpa.yaml` | HorizontalPodAutoscaler escalando el deployment 4–20 por CPU/memoria |
| `pdb.yaml` | PodDisruptionBudget manteniendo `minAvailable: 3` durante drains |

## Inicio rápido (kind / minikube / Docker Desktop)

```bash
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods -w
kubectl port-forward svc/myapp-service 8080:80   # abre http://localhost:8080
```

Los manifiestos `production-*` apuntan a un namespace `production` y esperan un Secret `db-secret` — son material de referencia más que una demo ejecutable.

## Notas

- Las imágenes usan `nginx:1.27-alpine` para que los manifiestos básicos realmente corran; la guía usa `myapp:1.0` como placeholder.
- El ejemplo de producción mantiene `registry.example.com/payment:v2.1.0` — cámbialo por tu imagen antes de aplicarlo.
