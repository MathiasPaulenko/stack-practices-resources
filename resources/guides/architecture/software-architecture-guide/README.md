# Software Architecture — Modular Monolith E-commerce Layout

Companion code for [Software Architecture Guide](https://stackpractices.com/guides/software-architecture-guide/).

The Phase-1 codebase from the guide's e-commerce scenario: `catalog`, `orders`, and `payments` are Django-style modules behind public `api/` interfaces. Modules may only import each other's `api/` package plus `shared/kernel`; `contracts/importlinter.ini` enforces the rule in CI. When a module needs to become a service, its API is already the extraction seam.

## Layout

```
shop/
  shared/kernel/        BaseEntity, Money — the only shared code
  modules/
    catalog/            domain · application · infrastructure · api · views
    orders/             same structure
    payments/           same structure
contracts/importlinter.ini
tests/test_place_order.py
```

## Run the boundary check

```bash
pip install import-linter
lint-imports --config contracts/importlinter.ini
```

Versión en español: [README.es.md](README.es.md)
