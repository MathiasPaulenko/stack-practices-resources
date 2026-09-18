# Recursos de la Plantilla de Performance Budget para Frontend

Recursos complementarios de [Plantilla de Performance Budget para Frontend](https://stackpractices.com/es/docs/frontend-performance-budget-template/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `budget/performance-budget-template.md` | Documento de budget completo: budgets de recursos por ruta, objetivos de Core Web Vitals, budgets de tiempo, budgets de terceros y umbrales de monitoreo RUM/sintético |
| `ci/budget-check.yml` | Workflow de GitHub Actions que corre el chequeo de bundle y Lighthouse CI en cada pull request |
| `ci/check-bundle-size.js` | Script de Node que compara tamaños gzip de assets contra los budgets; sale con error ante cualquier desborde (requiere `gzip-size`) |
| `ci/lighthouserc.json` | Configuración de Lighthouse CI que recolecta 3 corridas en rutas clave y verifica umbrales de Core Web Vitals |

## Uso

1. Copia `budget/performance-budget-template.md` a tu repo y completa tus propios números (mide primero — ver la sección "Cómo Elegir Tus Números" del artículo).
2. Copia `ci/check-bundle-size.js` a `scripts/` y ajusta las rutas de archivos y budgets a tu output de build.
3. Copia `ci/budget-check.yml` a `.github/workflows/` y `ci/lighthouserc.json` a la raíz del repo.
4. Añade `gzip-size` y `@lhci/cli` como dev dependencies si no están ya.
