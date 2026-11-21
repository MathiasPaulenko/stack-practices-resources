# Fusionar Archivos JSON — Ejemplos ejecutables

Código de apoyo de [Fusionar Archivos JSON](https://stackpractices.com/es/recipes/merge-json-files/) en StackPractices.

## Contenido

- `src/merge_json.py` — Python: `deep_merge` seguro (sin mutar entradas), concatenación de arrays, fusión multi-archivo con glob, deduplicación por clave. Solo stdlib: `python src/merge_json.py`
- `src/mergeJson.js` — Node.js: `deepMerge` protegido contra `null` y `__proto__`, concatenación con `flatMap`, fusión con glob. `node src/mergeJson.js` (la variante glob requiere `npm i glob`)
- `src/JsonMerge.java` — Java + Jackson: merge recursivo de `JsonNode` para objetos y arrays. Compilar con `jackson-databind` en el classpath.

## Notas

- El deep merge no es simétrico: fusiona siempre los archivos en 
