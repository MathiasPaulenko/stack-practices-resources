# Patrones Tácticos de Domain-Driven Design — Archivos complementarios

Ejemplos ejecutables para la receta en
[stackpractices.com](https://stackpractices.com/es/recipes/domain-driven-design/).

## Archivos

- `money.ts` — value object `Money`: inmutable, se autovalida, aritmética segura por moneda
- `order_aggregate.py` — aggregate root `Order` con domain events `OrderPlaced`
- `order_repository.py` — repository + Unit of Work + application service (en memoria, corre sin DB)
- `pricing_service.ts` — domain service para pricing cross-aggregate
- `specifications.ts` — `Specification<T>` componible con and/or/not
- `OrderToShipmentAdapter.java` — anti-corruption layer traduciendo Order → Shipping (ilustrativo)

## Inicio rápido

```bash
# Pipeline Python del aggregate + repository (solo stdlib)
python order_aggregate.py
python order_repository.py
```

```bash
# Los TypeScript necesitan un runtime TS (ts-node, bun o tsc)
npx ts-node money.ts
```
