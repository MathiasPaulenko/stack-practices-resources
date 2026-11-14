# Paginación con Scroll Infinito — Recursos Companion

Código companion de la receta [Paginación con Scroll Infinito en JavaScript](https://stackpractices.com/es/recipes/javascript-infinite-scroll-pagination/) en StackPractices.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `infinite_scroll.js` | Clase `InfiniteScroll` — IntersectionObserver, estados de carga/error, `AbortController` al desmontar, batching con `DocumentFragment`, roles de accesibilidad |
| `use_infinite_scroll.jsx` | Hook de React con guardia síncrona vía `useRef` contra dobles fetch |
| `demo.html` | Demo ejecutable conectada a la clase (módulo ES, sin bundler) |
| `mock_server.js` | Servidor `node:http` sin dependencias: sirve la demo + `/api/posts` falso (120 posts) |
| `mock_server.test.js` | Tests `node:test` del contrato de paginación |
| `package.json` | Config ESM + `npm start` / `npm test` |

## Requisitos

- Node.js 18+ (`fetch` incorporado para los tests)

## Ejecutar la demo

```bash
npm start
# abre http://127.0.0.1:8010/demo.html y baja con el scroll
```

El API falso devuelve 12 posts por página, 120 en total — `hasMore` pasa a `false` en la página 10 y la demo muestra el mensaje final.

## Ejecutar los tests

```bash
npm test
```

Cubre el contrato del que depende el observer: cálculo de slices, bordes de `hasMore`, parámetros `page`/`limit` sobre HTTP real.

## Notas

- La clase y el hook son drop-in — apunta `fetchUrl` a cualquier API que responda `{ items, hasMore }`.
- Si tu dataset se escribe mucho, pide a la API paginación por cursor (`?after=<último-id>`) en lugar de `?page=N`; los offsets derivan cuando se insertan items arriba.
- Para listas de ~1k+ items renderizados, prefiere una lista virtual (`react-window`) — mira la tabla de variantes de la receta.
