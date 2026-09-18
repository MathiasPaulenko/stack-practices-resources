# Kubernetes Diagnostic One-Liners

Copy-paste commands for on-call engineers in containerized environments.
Replace `production` with your namespace and `<pod-name>` / `<service-name>` / `<dependency>` with your values.

```bash
# Quick pod status check
kubectl get pods -n production -o wide | grep -v Running

# Get logs from a crashing pod
kubectl logs -n production <pod-name> --previous --tail=50

# Describe a pod for events and conditions
kubectl describe pod -n production <pod-name>

# Check resource usage across nodes
kubectl top nodes
kubectl top pods -n production --sort-by=memory

# Execute into a pod for network debugging
kubectl exec -it -n production <pod-name> -- /bin/sh -c "nslookup <dependency>"

# Check recent events in namespace
kubectl get events -n production --sort-by='.lastTimestamp' | tail -20

# Port-forward for local debugging
kubectl port-forward -n production svc/<service-name> 8080:80
```
