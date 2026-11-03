# Recursos de la Plantilla de Diseño de Pipeline CI/CD

Recursos complementarios de la [Plantilla de Diseño de Pipeline CI/CD](https://stackpractices.com/es/docs/ci-cd-pipeline-design-template/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `pipeline/ci-cd-pipeline-design-template.md` | Documento de diseño rellenable: resumen del pipeline, tablas de etapas y gates, matriz de entornos, estrategias de despliegue y procedimientos de rollback |
| `ci/github-actions-pipeline.yml` | Workflow completo de GitHub Actions que implementa el diseño: build, gate de tests + cobertura, lint, escaneo de seguridad, despliegue a staging, tests de integración, aprobación manual y despliegue blue-green a producción |
| `ci/gitlab-ci.yml` | El mismo pipeline expresado en GitLab CI: orden por `stages`, gate de aprobación con `when: manual` y traza de auditoría con `environment` |
| `scripts/rollback.sh` | Los procedimientos de rollback de la plantilla como script ejecutable: retorno a blue, undo de despliegue rolling, rollback a revisión concreta y verificación post-rollback |

## Uso

1. Copia `pipeline/ci-cd-pipeline-design-template.md` a la carpeta de documentación de tu repo y rellena proyecto, responsables, umbrales y duraciones.
2. Copia `ci/github-actions-pipeline.yml` a `.github/workflows/` (o `ci/gitlab-ci.yml` a `.gitlab-ci.yml`) y ajusta registro, nombre de imagen, namespaces y comandos de smoke tests.
3. Mantén `scripts/rollback.sh` como ejecutable junto a tus herramientas de despliegue; corre `./rollback.sh verify` tras cualquier rollback para confirmar versión, pods, tráfico y logs.
