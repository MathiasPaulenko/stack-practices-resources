# Guía de Accesibilidad WCAG 2.2 — Recursos complementarios

Archivos complementarios de la [Guía de Accesibilidad WCAG 2.2](https://stackpractices.com/es/guides/accessibility-wcag-guide/) en StackPractices. Cada snippet corresponde a una sección de la guía y está listo para adaptar.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `skip-link.css` | Enlace "saltar al contenido" — oculto visualmente hasta recibir foco |
| `sr-only.css` | Clase utility solo-lector-de-pantalla (oculta visualmente, aún anunciada) |
| `accessible-form.html` | Formulario con labels, hints `aria-describedby` y errores `aria-invalid` |
| `form-validation.ts` | Validación accesible que mueve el foco y anuncia errores |
| `accessible-modal.html` | Modal `<dialog>` nativo con título/descripción etiquetados y retorno de foco |
| `accessible-modal.ts` | Clase `AccessibleModal`: trampa de foco, cierre con Escape, restauración de foco |
| `roving-tabindex-tabs.ts` | Interfaz de pestañas con roving tabindex + navegación por flechas |
| `a11y-playwright.spec.ts` | Spec de Playwright + axe-core para el pase automatizado WCAG en CI |

## Uso

Copia los snippets en tu proyecto y adapta los selectores. Para el pase automatizado:

```bash
npm i -D @playwright/test @axe-core/playwright
npx playwright test a11y-playwright.spec.ts
```
