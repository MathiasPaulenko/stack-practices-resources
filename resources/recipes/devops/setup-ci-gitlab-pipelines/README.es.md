# Configurar CI con GitLab Pipelines — Proyecto Complementario

Proyecto ejecutable de la [receta Configurar CI con GitLab Pipelines](https://stackpractices.com/es/recipes/setup-ci-gitlab-pipelines/) en StackPractices.

## Contenido

- `.gitlab-ci.yml` — configuración raíz del pipeline usando includes de nivel superior.
- `.gitlab/ci/test.yml` — job de pruebas de Node.
- `.gitlab/ci/build.yml` — job de build que publica `dist/` como artefacto.
- `.gitlab/ci/deploy.yml` — job manual de staging que empaqueta `dist/` y lo sube al Generic Package Registry de GitLab con el CI job token.
- `package.json` y `package-lock.json` — configuración reproducible de Node usando `npm ci`.
- `.gitignore` — mantiene `node_modules/` y el `dist/` generado fuera del control de versiones, pero permite commitear el lockfile necesario para `npm ci`.
- `src/index.js`, `test/index.test.js`, `scripts/build.js` — aplicación mínima, prueba y script de build.

## Probarlo localmente

```bash
npm ci
npm test
npm run build
```

El job de despliegue es manual y corre solo en la rama por defecto. Usa variables predefinidas de GitLab (`CI_JOB_TOKEN`, `CI_API_V4_URL`, `CI_PROJECT_ID`, `CI_PIPELINE_IID` y `CI_COMMIT_SHORT_SHA`), así que no hace falta un servidor externo. Si tu organización deshabilita el package registry, reemplaza el paso `curl` por tu comando de despliegue.
