# Fusionar Archivos JSON en JavaScript — Ejemplos Node.js ejecutables

Código de apoyo de [Fusionar Archivos JSON en JavaScript](https://stackpractices.com/es/recipes/merge-json-files-javascript/) en StackPractices.

## Contenido

- `src/mergeJson.js` — `deepMerge` blindado: seguro con `null`, filtra `__proto__`/`constructor`/`prototype`, no muta las entradas. `node src/mergeJson.js`
- `src/mergeJsonDir.js` — fusión de directorio ordenada con recolección de errores de parseo por archivo. `node src/mergeJsonDir.js ./config`
- `src/mergeRecords.js` — concat de arrays + deduplicación por clave estable con `Map`. `node src/mergeRecords.js`

## Notas

- Ordena la lista de archivos antes de fusionar: el orden de `readdirSync` depende de la plataforma y "gana el último" debe ser determinista.
- Para archivos que no caben en memoria, concatena arrays con `JSONStream` (ver la receta); el deep merge de objetos no puede hacer streaming.
- Valida la salida fusionada con AJV antes de usarla en un paso de build.
