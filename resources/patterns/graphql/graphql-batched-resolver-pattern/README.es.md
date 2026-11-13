# Patrón de Resolvers Agrupados en GraphQL

Ejemplos ejecutables del patrón de StackPractices
[Patrón de Resolvers Agrupados en GraphQL](https://stackpractices.com/es/patterns/graphql-batched-resolver-pattern/).

Tres programas pequeños que ejecutan los mismos resolvers contra una base de
datos en memoria que cuenta consultas:

| Archivo | Qué muestra | Consultas para 50 publicaciones + autores |
| --- | --- | --- |
| `n-plus-one.mjs` | El problema N+1: una llamada de resolver por publicación | **51** |
| `batched-resolver.mjs` | Agrupación con DataLoader y loaders por petición | **2** |
| `manual-batch.mjs` | El mismo patrón con un agrupador manual mínimo (sin dependencias) | **2** |

## Requisitos

- Node.js 18+
- `npm install` solo es necesario para `batched-resolver.mjs` (descarga
  `dataloader`). Las otras dos demos funcionan sin dependencias.

## Ejecutar

```bash
npm install            # una vez, para la demo de DataLoader

node n-plus-one.mjs    # base: 51 consultas
node batched-resolver.mjs  # DataLoader: 2 consultas
node manual-batch.mjs      # agrupador manual: 2 consultas
```

## En qué fijarse

- `mock-db.mjs` cuenta las consultas, así que la diferencia entre N+1 y la
  agrupación es un número, no una afirmación. Las 50 publicaciones comparten
  solo 30 autores distintos, lo que además muestra la deduplicación por
  petición de DataLoader.
- `batched-resolver.mjs` crea los loaders en una factoría
  `createLoaders(context)`, la misma forma que usarías dentro de la función
  `context` de Apollo Server. La función de lote devuelve resultados **en el
  orden de las claves**: ese contrato posicional es lo que hace obligatorio el
  `userMap.get(id)`.
- `manual-batch.mjs` muestra la mecánica del patrón sin la biblioteca: encolar
  claves durante una ventana de un microtask, deduplicar con un `Set`, disparar
  el lote una vez y repartir resultados por clave.

## Extensiones habituales

- Configura `maxBatchSize` cuando las listas pueden llegar a miles de padres.
- Devuelve `new Error()` por clave fallida en lugar de lanzar excepciones.
- Llama a `loader.clear(id)` tras una mutación que escriba la entidad cacheada.
