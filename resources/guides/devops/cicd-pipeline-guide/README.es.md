# Recursos de la Guía de Pipelines CI/CD

Recursos complementarios de [Guía de Pipelines CI/CD: Del Commit a Producción](https://stackpractices.com/es/guides/cicd-pipeline-guide/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `ci/cicd-pipeline.yml` | Pipeline de GitHub Actions listo para producción: gates de test/seguridad en paralelo, despliegue a staging, tests de integración, producción con aprobación |
| `scripts/rollback.sh` | Procedimientos de rollback en Kubernetes de la guía como script ejecutable: undo, rollback a revisión y verificación post-rollback |

## Uso

1. Copia `ci/cicd-pipeline.yml` a `.github/workflows/` y ajusta scripts, entornos y comandos de test.
2. Mantén `scripts/rollback.sh` junto a tus herramientas de despliegue; corre `./rollback.sh verify` tras cualquier rollback.
