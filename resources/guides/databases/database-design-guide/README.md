# Database Design Guide — Companion

Runnable PostgreSQL DDL from the guide:

- `normalization-examples.sql` — 1NF/2NF/3NF violation → fix pairs (multi-valued phones, partial dependency, transitive dependency).
- `ecommerce-schema.sql` — full e-commerce schema (customers, addresses, categories, products, orders, order_items) with generated columns, partial/GIN indexes, plus the atomic inventory decrement.

Source: https://stackpractices.com/guides/database-design-guide/
