# Checklist de Auditoría de Accesibilidad — Recursos complementarios

Archivos complementarios de la [Checklist de Auditoría de Accesibilidad](https://stackpractices.com/es/docs/accessibility-audit-checklist/) en StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `accessibility-audit-checklist-template.md` | Auditoría WCAG 2.2 en blanco: información de auditoría, herramientas, las 86 tablas de criterios, resumen de criterios fallidos y plan de remediación — lista para rellenar |
| `axe-playwright.spec.ts` | Spec de Playwright + axe-core que ejecuta los chequeos automatizados WCAG 2.1/2.2 AA sobre cada página del alcance en CI |
| `.pa11yci.json` | Config de pa11y-ci para un segundo pase automatizado (WCAG2AA) — atrapa un corte de problemas distinto al de axe |

## Uso

```bash
# Pase automatizado con Playwright + axe
npm i -D @playwright/test @axe-core/playwright
npx playwright test axe-playwright.spec.ts

# O con pa11y-ci contra un preview en marcha
npm i -D pa11y-ci
npx pa11y-ci --config .pa11yci.json
```

Rellena primero la tabla de información de auditoría, registra cada resultado del escaneo automatizado como fila y después haz el pase manual de teclado y el pase con lector de pantalla — la columna de método de prueba de la lista existe para mantener eso honesto.
