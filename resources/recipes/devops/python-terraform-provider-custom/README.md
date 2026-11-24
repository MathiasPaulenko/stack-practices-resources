# Custom Terraform Provider in Python — Companion Code

Runnable skeleton of the resource lifecycle a Terraform provider implements.

## Files

| File | What it shows |
|---|---|
| `provider.py` | `ApiClient` (requests wrapper), `ItemResource` with the four CRUD operations Terraform calls (create, read, update, delete), 404 → empty-state semantics, and a smoke test in `__main__` that runs the whole cycle against an in-memory mock API. |

## Quick start

```bash
pip install -r requirements.txt
python provider.py
# create: {'id': 'a1b2c3d4', 'name': 'prod-config', ...}
# read after delete: {}
```

Note: real providers serve this contract over gRPC via `terraform-plugin-go`/`terraform-plugin-framework` (or `terraform-plugin-python`). This module isolates the CRUD logic so it's testable without a Terraform binary.

## Source

- https://stackpractices.com/recipes/python-terraform-provider-custom/
- https://stackpractices.com/es/recipes/python-terraform-provider-custom/
