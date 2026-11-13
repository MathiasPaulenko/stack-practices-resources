# Workflows reutilizables de GitHub Actions — Ejemplos

Código complementario de la receta de StackPractices:
https://stackpractices.com/es/recipes/github-actions-reusable-workflows/

## Qué contiene

Workflows reutilizables (llamables vía `workflow_call`):

| Archivo | Propósito |
|---|---|
| `.github/workflows/reusable-build.yml` | Build reutilizable básico con inputs tipados `node-version` y `run-tests` |
| `.github/workflows/reusable-deploy.yml` | Deploy controlado por el input `environment` + secrets obligatorios/opcionales |
| `.github/workflows/reusable-test-matrix.yml` | Matrix pasada como input JSON y expandida con `fromJSON` |
| `.github/workflows/reusable-ci.yml` | Jobs condicionales dirigidos por inputs booleanos (`skip-lint`, `deploy`) |
| `.github/workflows/reusable-build-with-output.yml` | Expone `artifact-url` a través de `workflow_call.outputs` |
| `.github/workflows/reusable-docker-build.yml` | Build/push de Docker a GHCR con `permissions` explícitos |
| `.github/workflows/reusable-quality.yml` | Ejemplo anidado: orquesta los workflows de build y test-matrix |

Workflows que llaman:

| Archivo | Propósito |
|---|---|
| `.github/workflows/ci.yml` | Llama a los workflows de build y matrix en push/PR |
| `.github/workflows/deploy.yml` | Cadena staging → production con `needs` y secrets mapeados |
| `.github/workflows/release.yml` | Release por tags que consume el output `artifact-url` |

## Cómo usarlo

1. Copia los archivos que necesites a tu repositorio, manteniendo la estructura `.github/`.
2. Crea los secrets `STAGING_DEPLOY_TOKEN`, `PROD_DEPLOY_TOKEN` y `REGISTRY_PASSWORD` en **Settings > Secrets and variables > Actions**.
3. Crea los environments `staging` y `production` en **Settings > Environments** si quieres aprobaciones manuales.
4. `./deploy.sh` es un placeholder — apunta los pasos de deploy a tu propio script o action.
5. Para llamar a un workflow desde otro repo, referéncialo por ruta y ref:

```yaml
jobs:
  call-build:
    uses: my-org/shared-workflows/.github/workflows/reusable-build.yml@v1
    with:
      node-version: '20'
```

Los repositorios privados o internos deben habilitar el acceso de Actions para otros repos de la organización (**Settings > Actions > General > Access**).

## Notas

- Fija los callers a un tag o SHA (`@v1`) en lugar de `@main` para que un workflow modificado no rompa a los consumidores.
- Mantén `workflow_call` como único trigger en los workflows reutilizables — mezclarlo con `push` o `pull_request` también los dispara con los eventos de su propio repo.
