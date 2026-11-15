# Lazy Loading — Recursos Complementarios

Ejemplos ejecutables para la receta [Lazy Loading](https://stackpractices.com/es/recipes/lazy-loading/) de StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `index.html` | Demo offline: un hero eager + 11 imágenes manejadas por IntersectionObserver |
| `intersection-observer.js` | Observer compartido con `rootMargin`, `unobserve` y fallback `onerror` |
| `make-placeholders.py` | Genera placeholders SVG locales para que la demo no necesite red |
| `LazyComponents.jsx` | `React.lazy` + `Suspense` con fallbacks skeleton y un error boundary |
| `use-infinite-list.jsx` | `useInfiniteQuery` + observer centinela = infinite scroll |

## Inicio rápido

```bash
# 1. Genera las imágenes placeholder (12 SVG + un fallback)
python make-placeholders.py

# 2. Abre la demo
#    Doble clic en index.html, o sírvela así:
python -m http.server 8080
# y visita http://localhost:8080
```

Abre DevTools → Network, limita a Slow 3G y haz scroll despacio. El contador de la esquina muestra cuántas imágenes se han descargado de verdad — las que nunca alcanzas nunca se bajan.

## Qué probar

- Cambia `rootMargin` en `intersection-observer.js` de `200px` a `0px` y haz scroll rápido — verás las imágenes aparecer tarde.
- Comenta los atributos `width`/`height` en `index.html` y observa el salto de layout (CLS) al aterrizar las imágenes.
- Rompe una ruta `data-src` para ver el fallback `onerror` en acción.

## Snippets de React

`LazyComponents.jsx` muestra por qué todo `React.lazy` necesita un error boundary: un chunk que da 404 (deploy nuevo, HTML viejo) lanza el error al renderizar y tumba el árbol sin él.

`use-infinite-list.jsx` usa paginación por cursor (`after=…`) en lugar de `page=n` — los cursores no derivan cuando se insertan filas entre peticiones, que es como evitas items duplicados en los feeds.
