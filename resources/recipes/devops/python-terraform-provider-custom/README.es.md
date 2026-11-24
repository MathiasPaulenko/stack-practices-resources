# Provider personalizado de Terraform en Python — Codigo complementario

Skeleton ejecutable del ciclo de vida de recursos que implementa un provider de Terraform.

## Archivos

| Archivo | Que muestra |
|---|---|
| `provider.py` | `ApiClient` (wrapper con requests), `ItemResource` con las cuatro operaciones CRUD que llama Terraform (create, read, update, delete), semantica 404 → estado vacio, y un smoke test en `__main__` que corre el ciclo completo contra una API mock en memoria. |

## Inicio rapido

```bash
pip install -r requirements.txt
python provider.py
# create: {'id': 'a1b2c3d4', 'name': 'prod-config', ...}
# read after delete: {}
```

Nota: los providers reales sirven este contrato por gRPC via `terraform-plugin-go`/`terraform-plugin-framework` (o `terraform-plugin-python`). Este modulo aisla la logica CRUD para que sea testeable sin un binario de Terraform.

## Fuente

- https://stackpractices.com/recipes/python-terraform-provider-custom/
- https://stackprac
- https://stackpractices.com/es/recipes/python-terraform-provider-custom/
