# Role Pattern — Companion Resources

Runnable implementations of the Role Pattern in Python, Java, and JavaScript.
Each one models a `Person` entity that gains capabilities by attaching role
objects at runtime — no class-hierarchy explosion required.

## Files

| File | Language | Description |
|------|----------|-------------|
| `role_pattern.py` | Python | `Role` protocol + `CustomerRole`/`EmployeeRole`/`VendorRole` dataclasses, `Person` with assign/revoke/history |
| `RolePattern.java` | Java | `Role` interface + nested role classes, `Person` with capability check via `canPerform` |
| `role_pattern.js` | JavaScript | Same model with `Map`-based role registry and ISO-timestamped history |

## Running the examples

```bash
python role_pattern.py
javac RolePattern.java && java RolePattern
node role_pattern.js
```

Each script assigns `customer` + `employee` roles to Alice, checks a few
permissions (`browse`, `refund`, `list_products`), processes a refund through
the employee role, then revokes `customer` — all without touching the entity's
identity.

## Key concepts

- **Entity vs role**: `Person` holds identity only; behavior lives in role objects.
- **Runtime attach/detach**: `assignRole`/`revokeRole` mutate capabilities, not the type.
- **Capability union**: `canPerform` returns true if any attached role allows the action.
- **Auditability**: every assign/revoke lands in a history log.

## Source

Companion to the StackPractices article:
<https://stackpractices.com/patterns/role-pattern/>
