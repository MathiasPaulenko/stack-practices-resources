# Caché LRU en memoria en Node.js — Código complementario

Código ejecutable de la [receta de StackPractices](https://stackpractices.com/es/recipes/nodejs-in-memory-cache-lru/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `lru-dll.ts` | LRU de manual: `Map` para búsqueda O(1) + lista doblemente enlazada para mover/expulsar O(1) |
| `lru-map.ts` | LRU solo con `Map` (`delete` + `set`) para cachés pequeñas |
| `ttl-cache.ts` | LRU con TTL por entrada y barrido periódico (`cleanup` de recorrido completo) |
| `async-lru.ts` | LRU asíncrona que guarda promesas; los rechazos se borran solos en vez de envenenar la entrada |
| `benchmark.js` | Comparación del coste de expulsión entre ambas implementaciones a capacidades crecientes |

## Ejecutar

```bash
npx tsc lru-dll.ts lru-map.ts ttl-cache.ts async-lru.ts --target es2020 --module commonjs
node benchmark.js
```

La versión solo-Map se frena al expulsar a medida que la capacidad llega a las
decenas de miles, mientras la de lista enlazada se mantiene plana.

## ¿Cuál usar?

- Unos cientos de claves y legibilidad primero → `lru-map.ts`
- Expulsiones frecuentes o miles de claves → `lru-dll.ts`
- Producción con TTL, `dispose` y límites por bytes → el paquete [`lru-cache`](https://github.com/isaacs/node-lru-cache)
