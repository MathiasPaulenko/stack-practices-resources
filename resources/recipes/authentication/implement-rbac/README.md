# Implement RBAC — Companion

Companion code for the StackPractices recipe [Implement RBAC](https://stackpractices.com/recipes/implement-rbac/).

## Files

- `check_rbac.py` — minimal RBAC evaluator (stdlib only). Role hierarchy via `parent`, recursive permission resolution with cycle guard, deny-by-default.

## Usage

```bash
python check_rbac.py --demo                  # built-in roles + scenarios
python check_rbac.py roles.json checks.json  # your own roles + checks
```

## Sample output

```
ana@example.com -> users:delete: ALLOW
beto@example.com -> orders:write: ALLOW
beto@example.com -> orders:read: ALLOW
carol@example.com -> orders:write: DENY
carol@example.com -> reports:read: ALLOW
```

`beto` can read orders even though `orders:read` is not on the `editor`
role — it is inherited through `editor -> viewer`. `carol` gets denied
because `orders:write` is nowhere in `viewer`'s chain.
