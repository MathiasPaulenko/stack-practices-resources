# Recursos de Configuración de Pipelines CI/CD

Recursos complementarios de [Configuración de Pipelines CI/CD](https://stackpractices.com/es/recipes/cicd-pipeline-setup/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `ci/deploy.yml` | Pipeline de GitHub Actions: tests, escaneo de seguridad, despliegue a staging y a producción con gate |
| `ci/gitlab-ci.yml` | El mismo pipeline en GitLab CI: stages, regex de cobertura, entorno de producción protegido |
| `ci/blue-green.yml` | Job de despliegue blue-green: detecta el color activo, despliega al inactivo, conmuta tráfico y revierte si el smoke test falla |
| `ci/rollout-canary.yaml` | Canary con Argo Rollouts: 10% → 25% → 50% → 100% con pausas |

## Uso

Copia a `.github/workflows/` (o `.gitlab-ci.yml`) y ajusta nombres de imagen, entornos y comandos de despliegue.
