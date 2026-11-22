# Patrón Multiton

Implementaciones ejecutables del
[patrón de StackPractices](https://stackpractices.com/es/patterns/multiton-pattern/):

| Archivo | Lenguaje | Notas |
|---|---|---|
| `src/multiton_pool.py` | Python | Double-checked locking sobre un registro a nivel de clase |
| `src/ThemeManager.java` | Java | `ConcurrentHashMap.computeIfAbsent` — creación atómica |
| `src/multiton_logger.js` | JavaScript | Registro en un campo privado estático (`#instances`) |
| `src/tenant-database.ts` | TypeScript | Un `pg.Pool` por tenant; `closeAll()` + `getActiveTenants()` para el ciclo de vida |

## Requisitos

- Python 3.10+ (solo stdlib)
- Node.js 18+ (`tenant-database.ts` necesita además `pg` y TypeScript)
- Java 17+

## Notas

- Mantén el registro privado y expón solo métodos tipo `getInstance`/`evict` — un mapa público invita a saltarse el control de creación.
- La carrera check-then-act es el bug clásico: protege la creación con un lock o una operación atómica del mapa.
- Solo para espacios de claves acotados. Para claves ilimitadas (IDs de usuario, de sesión), usa un caché con expulsión.
