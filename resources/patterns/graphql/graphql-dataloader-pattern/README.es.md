# Patrón DataLoader en GraphQL

Demo ejecutable del contrato de la librería DataLoader usado en el artículo [Patrón DataLoader en GraphQL](https://stackpractices.com/es/patterns/graphql-dataloader-pattern/).

## Qué demuestra

`contract.mjs` ejercita las cinco garantías que hacen funcionar el patrón:

1. **Deduplicación por tick**: 4 llamadas `load()` con 2 claves únicas producen 1 consulta a la base de datos.
2. **Errores por clave**: un `Error` en un índice rechaza solo a quien lo pidió (`Promise.allSettled` muestra `u404` fallando mientras `u2` resuelve).
3. **Invalidación de caché**: tras una mutación, `clear(key)` expulsa la entrada vieja; el siguiente `load()` vuelve a consultar.
4. **Orden de `loadMany`**: los resultados quedan alineados con las claves de entrada, incluidos los huecos de claves no encontradas.
5. **`cacheKeyFn`**: las claves objeto deduplican por valor, no por referencia.

`mock-db.mjs` es una base de datos falsa que cuenta consultas y devuelve copias, como haría un driver real.

## Ejecutar

```bash
npm install
npm run demo
```

La salida esperada muestra el conteo de deduplicación, el error por clave, `Ada` → `Ada Lovelace` tras `clear()`, los resultados alineados de `loadMany` y una sola llamada de lote para dos claves objeto iguales.

## Requisitos

Node.js 18+.
