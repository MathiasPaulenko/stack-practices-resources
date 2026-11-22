# Multiton Pattern

Runnable implementations for the
[StackPractices pattern](https://stackpractices.com/patterns/multiton-pattern/):

| File | Language | Notes |
|---|---|---|
| `src/multiton_pool.py` | Python | Double-checked locking around a class-level registry |
| `src/ThemeManager.java` | Java | `ConcurrentHashMap.computeIfAbsent` — atomic creation |
| `src/multiton_logger.js` | JavaScript | Registry in a static private field (`#instances`) |
| `src/tenant-database.ts` | TypeScript | One `pg.Pool` per tenant; `closeAll()` + `getActiveTenants()` for lifecycle |

## Requirements

- Python 3.10+ (stdlib only)
- Node.js 18+ (`tenant-database.ts` also needs `pg` and TypeScript)
- Java 17+

## Notes

- Keep the registry private and expose only `getInstance`/`evict`-style methods — a public map invites callers to bypass creation control.
- The check-then-act race is the classic bug: guard creation with a lock or an atomic map operation.
- Bounded key spaces only. For unbounded keys (user IDs, session IDs), use a cache with eviction instead.
