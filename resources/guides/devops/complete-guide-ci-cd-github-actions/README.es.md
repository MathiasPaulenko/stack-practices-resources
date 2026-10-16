# CI/CD con GitHub Actions — Workflows de acompañamiento

Workflows listos para usar de la guía
[Guía completa de CI/CD con GitHub Actions](https://stackpractices.com/es/guides/complete-guide-ci-cd-github-actions/).

## Archivos

- `.github/workflows/ci.yml` — pipeline completo: lint, matriz de tests (Node 18/20/22), artefacto de build, despliegue a staging, despliegue a producción con aprobación, grupo de concurrencia y `permissions` de mínimo privilegio.
- `.github/workflows/test-suite.yml` — workflow de tests reutilizable (`workflow_call`) con input `node-version` opcional y secreto `API_KEY`.
- `deploy.sh` — script de despliegue de ejemplo que invocan los jobs de deploy; sustituye el cuerpo por tu plataforma (SSH, `kubectl`, una CLI de nube o un commit GitOps).
- `package.json` — proyecto Node mínimo para que los pasos `npm ci`/`lint`/`test`/`build` del workflow tengan algo que ejecutar.

## Uso

1. Copia `.github/workflows/` a tu repositorio.
2. Crea los entornos `staging` y `production` en Settings → Environments y añade revisores obligatorios a `production`.
3. Sustituye `deploy.sh` por tu despliegue real y actualiza las URLs de los entornos.
4. Adapta el filtro `paths` y la matriz de `node-version` a tu proyecto.

Los jobs de despliegue solo corren en `main`; los pull requests reciben lint y la matriz de tests.
