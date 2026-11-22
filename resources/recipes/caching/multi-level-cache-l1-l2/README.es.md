# Caché multi-nivel L1+L2 — Archivos complementarios

Código ejecutable de la receta [Cache multi-nivel con L1 en memoria y L2 en Redis](https://stackpractices.com/es/recipes/multi-level-cache-l1-l2/).

## Archivos

- `multi-level-cache.ts` — implementación TypeScript: L1 en memoria (`lru-cache`), L2 en Redis, invalidación por pub/sub entre instancias.
- `usage.ts` — ejemplo de uso: `getOrLoad` más invalidación tras una escritura.
- `instrumented-cache.ts` — subclase que registra hit rates de L1/L2/miss.
- `multi_level_cache.py` — variante Python (3.10+) con hilo daemon de escucha pub/sub.

## Requisitos

- Node.js 18+, `npm install redis lru-cache`
- Python 3.10+, `pip install redis`
- Un Redis en ejecución (`redis://localhost:6379` por defecto)
