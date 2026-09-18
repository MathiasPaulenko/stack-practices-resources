# Patrón Islands Architecture — Código complementario

Ejemplos ejecutables del
[patrón Islands Architecture](https://stackpractices.com/es/patterns/islands-architecture-pattern/)
en StackPractices: páginas renderizadas en el servidor que solo hidratan
sus islas interactivas.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `islands/page.astro` | Página de Astro que mantiene el grid de productos estático e hidrata solo `SearchBox` (client:load) y `NewsletterForm` (client:idle) |
| `islands/SearchBox.jsx` | Isla de React con fetch con debounce — el único componente que envía React al navegador |
| `islands/CartCounter.jsx` | Segunda isla que lee el store compartido con `useSyncExternalStore` |
| `islands/NewsletterForm.jsx` | Isla no crítica que funciona como formulario HTML normal antes de hidratar |
| `islands/nanostores-cart.js` | Store de carrito compartido con la API `map()` real de `nanostores` — el enfoque canónico multi-framework |
| `islands/store.js` | Store compartido sin dependencias con API al estilo de nanostores |
| `islands/vanilla-island.html` | Demo sin frameworks: un IntersectionObserver "hidrata" un contador al hacerse visible — la idea de `client:visible` en ~30 líneas |
| `islands/hydration-cost.js` | Script de Node que estima la diferencia de JS entre hidratación completa e islas |

## Uso

Los archivos `.astro` / `.jsx` se integran en un proyecto Astro con la
integración de React (`npx astro add react`). La demo vanilla no
necesita build:

```bash
open islands/vanilla-island.html   # o ábrelo con doble clic
node islands/hydration-cost.js
```

## Cómo funciona

1. El servidor renderiza toda la página — incluidas las islas — a HTML estático.
2. Las props de cada isla se serializan en el marcado como JSON.
3. Un runtime diminuto hidrata cada isla cuando lo indica su directiva
   (`client:load`, `client:visible`, `client:idle`, `client:media`).

Patrones relacionados:
[Mejora Progresiva](https://stackpractices.com/es/patterns/progressive-enhancement-pattern/) ·
[Suspense Boundary](https://stackpractices.com/es/patterns/suspense-boundary-pattern/)
