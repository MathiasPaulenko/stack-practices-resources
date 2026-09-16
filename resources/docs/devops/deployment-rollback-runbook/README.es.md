# Rollback de Despliegues — Recursos complementarios

Archivos complementarios del [Runbook de Rollback de Despliegues](https://stackpractices.com/es/docs/deployment-rollback-runbook/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `rollback-runbook.md` | Markdown | Runbook listo para adaptar: triggers, checklist de verificación y plantilla de comunicación |
| `rollback-commands.sh` | Bash | Biblioteca de funciones de rollback para kubectl/Helm/ArgoCD con variables `APP`/`NS` |

## Inicio rápido

### 1. Copia el runbook

```bash
cp rollback-runbook.md oncall/rollback-runbook.md
```

Rellena el nombre de tu app, namespace, umbrales y canales de stakeholders.

### 2. Usa la biblioteca de comandos

```bash
source rollback-commands.sh
export APP=my-app NS=production

rollback_kubectl          # revertir a la revisión anterior
rollback_kubectl_to 3     # revertir a una revisión concreta
rollback_helm             # helm rollback a la revisión anterior
verify_rollback           # imagen + pods + logs + eventos
argocd_git_revert <sha>   # revert GitOps — persiste en Git (a diferencia de `argocd app rollback`)
```

## Umbrales de trigger (por defecto del runbook)

| Trigger | Severidad | Acción | Plazo |
|---------|-----------|--------|-------|
| Tasa de errores > 5% | Crítica | Rollback inmediato | < 5 min |
| Latencia P99 > 5x baseline | Crítica | Rollback inmediato | < 5 min |
| Health checks fallando | Crítica | Rollback inmediato | < 5 min |
| Tasa de errores > 1% | Alta | Investigar, preparar | < 15 min |
| OOM kills en aumento | Alta | Rollback si sube | < 10 min |

## Referencias

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Helm rollback](https://helm.sh/docs/helm/helm_rollback/)
- [Documentación de Argo CD](https://argo-cd.readthedocs.io/)
