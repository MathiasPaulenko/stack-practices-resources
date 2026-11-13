# Implementar RBAC — Companion

Código companion de la receta de StackPractices [Implementar RBAC](https://stackpractices.com/es/recipes/implement-rbac/).

## Archivos

- `check_rbac.py` — evaluador RBAC mínimo (solo stdlib). Jerarquía de roles vía `parent`, resolución recursiva de permisos con guarda de ciclos, deny por defecto.

## Uso

```bash
python check_rbac.py --demo                  # roles y escenarios incluidos
python check_rbac.py roles.json checks.json  # tus propios roles y checks
```

## Salida de ejemplo

```
ana@example.com -> users:delete: ALLOW
beto@example.com -> orders:write: ALLOW
beto@example.com -> orders:read: ALLOW
carol@example.com -> orders:write: DENY
carol@example.com -> reports:read: ALLOW
```

`beto` puede leer pedidos aunque `orders:read` no esté en el rol
`editor` — lo hereda a través de `editor -> viewer`. A `carol` se le
deniega porque `orders:write` no está en ningún punto de la cadena de
`viewer`.
