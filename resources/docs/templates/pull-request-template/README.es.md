# Plantilla de Pull Request

Plantilla de pull request lista para copiar en GitHub (y adaptable a GitLab, Bitbucket y Azure DevOps), más un workflow de GitHub Actions que valida las secciones obligatorias y títulos de tipo conventional commit.

## Archivos

- `pull_request_template.md` — la plantilla en inglés. Guárdala en `.github/pull_request_template.md` y GitHub la insertará en cada PR nueva.
- `pull_request_template.es.md` — la misma plantilla en español.
- `pr-validation.yml` — workflow de GitHub Actions que comprueba que el título de la PR sigue conventional commits y que la descripción conserva las secciones requeridas. Guárdalo en `.github/workflows/pr-validation.yml`.

## Uso

```bash
mkdir -p .github
cp pull_request_template.md .github/pull_request_template.md
cp pr-validation.yml .github/workflows/pr-validation.yml
```

Para varias plantillas, colócalas en `.github/PULL_REQUEST_TEMPLATE/` (p. ej. `feature.md`, `hotfix.md`) y elige una mediante el parámetro `?template=` de la URL.

## Fuente

- [Pull Request Template — StackPractices](https://stackpractices.com/docs/pull-request-template/)
- [Plantilla de Pull Request — StackPractices](https://stackpractices.com/es/docs/pull-request-template/)
