# GitHub Actions — Workflows ejecutables de ejemplo

Código companion de la receta de StackPractices:
https://stackpractices.com/es/recipes/github-actions/

## Qué incluye

| Archivo | Propósito |
|---|---|
| `.github/workflows/ci.yml` | Pipeline CI de Node.js en push y PR a `main` |
| `.github/workflows/test-matrix.yml` | Workflow reutilizable con matriz (3 SO × 3 versiones de Node, `workflow_call`) |
| `.github/workflows/reusable-lint.yml` | Workflow reutilizable de lint con input `node-version` requerido |
| `.github/workflows/deploy.yml` | Deploy disparado por tags, controlado por el environment `production` y un grupo de concurrencia |
| `.github/workflows/nightly-audit.yml` | `npm audit` programado con cron a las 03:00 UTC más `workflow_dispatch` |
| `.github/actions/setup-project/action.yml` | Action compuesta: setup de Node + caché + `npm ci` + build |

## Cómo usarlo

1. Copia los archivos que necesites a tu repositorio, manteniendo la estructura `.github/`.
2. Crea el secret `DEPLOY_TOKEN` en **Settings > Secrets and variables > Actions**.
3. Crea el environment `production` en **Settings > Environments** si quieres la aprobación manual de `deploy.yml`.
4. Invoca un workflow reutilizable desde otro repositorio:

```yaml
jobs:
  call-lint:
    uses: org/shared-workflows/.github/workflows/reusable-lint.yml@main
    with:
      node-version: '20'
```

5. Referencia la action compuesta de forma local:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-project
    with:
      node-version: '22'
```

Para la explicación completa — modelo de ejecución, contextos, `GITHUB_TOKEN`, concurrencia, multiplicadores de facturación — lee la receta.
