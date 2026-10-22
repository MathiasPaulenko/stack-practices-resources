# Plantilla de Reporte de Cobertura — Companion

Archivos complementarios de la [Plantilla de Reporte de Cobertura de Pruebas](https://stackpractices.com/es/docs/test-coverage-report-template/).

## Archivos

| Archivo | Qué es |
|---------|--------|
| `aggregate-coverage.mjs` | Script de Node que convierte un `coverage-summary.json` de c8/istanbul en la tabla markdown por módulo que usa la plantilla |
| `coverage-summary-sample.json` | Salida de ejemplo de c8 para probar el script |
| `example-report.md` | Un reporte rellenado mostrando el resultado final |

## Uso

```bash
# 1. genera cobertura con tu runner
npx vitest run --coverage --reporter=json-summary

# 2. agrega por módulo (raíz por defecto: src/modules/, personalizable por argumento)
node aggregate-coverage.mjs coverage/coverage-summary.json src/modules/
```

Pruébalo con los datos de ejemplo:

```bash
node aggregate-coverage.mjs coverage-summary-sample.json src/modules/
```

Pega la salida en la sección 2 del reporte. El script promedia la cobertura por archivo por directorio de módulo — adapta `moduleRoot` a tu estructura (`packages/`, `services/` para monorepos).
