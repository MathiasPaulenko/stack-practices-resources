# Checklist de Revisión de Helm Charts — Archivos Companion

Archivos independientes para la doc [Checklist de Revisión de Helm Charts](https://stackpractices.com/es/docs/helm-chart-review-checklist/) en StackPractices.

## Contenido

| Archivo | Qué es |
|------|-----------|
| `src/helm-chart-review-checklist.md` | La checklist completa lista para rellenar — cópiala en tu repo (p. ej. `.github/helm-review.md`) y completa la columna Status por chart |
| `src/chart-review-ci.yml` | Workflow de GitHub Actions que automatiza la checklist: `helm lint`, `helm template`, `kube-score`, detección de tags `:latest` y secretos en texto plano, upgrade en dry-run |

## Uso

```bash
# Suelta la checklist en un PR para revisar un chart a mano
cp src/helm-chart-review-checklist.md .github/helm-review.md

# O automatiza la barrera de revisión en CI
cp src/chart-review-ci.yml .github/workflows/helm-chart-review.yml
```

Ajusta `./charts/my-app` a la ruta de tu chart. El workflow falla el PR ante tags `:latest`, secretos en texto plano en `values.yaml` o warnings de kube-score — los mismos checks que cubre la checklist manual.
