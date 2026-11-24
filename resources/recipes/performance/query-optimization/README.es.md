# Optimización de consultas — Código complementario

Companion ejecutable en PostgreSQL para la [receta de optimización de consultas](https://stackpractices.com/es/recipes/query-optimization/). Te da una base de datos lo bastante grande para que las diferencias de plan importen, más los ejercicios exactos de `EXPLAIN (ANALYZE, BUFFERS)` del artículo.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `schema.sql` | Esquema de demo (customers, products, orders, order_items) con ~200k pedidos y 500k items vía `generate_series`. |
| `analyze.sql` | Comparaciones de planes lado a lado: Seq Sca
