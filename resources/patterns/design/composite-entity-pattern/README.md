# Composite Entity Pattern — Companion Examples

Runnable examples for the [Composite Entity pattern](https://stackpractices.com/patterns/composite-entity-pattern/): one aggregate root (`Order`) owning dependent objects (`LineItem`, `ShippingAddress`) persisted across three tables as a single unit.

## What's inside

| File | Language | Purpose |
| --- | --- | --- |
| `order_mapper.py` | Python | Complete `OrderMapper` over `sqlite3` — `save()` writes all three tables in one transaction; `find_by_id()` rehydrates the whole aggregate. Runnable: `python order_mapper.py` prints `Order total: $109.97`. |
| `OrderMapper.java` | Java | Same mapper with JDBC, including `save()` with `setAutoCommit(false)` + rollback handling and a `main()` demo. |
| `order-mapper.js` | JavaScript | Async mapper for an `sqlite`-style db handle, with `BEGIN`/`COMMIT`/`ROLLBACK` transaction in `save()`. |
| `schema.sql` | SQL | Schema encoding ownership: `ON DELETE CASCADE`, composite key `(order_id, line_no)`, check constraints. |
| `order_projection.py` | Python | List-view projection — one aggregate query instead of loading full composites for a table view. |
| `order_mapper_json.py` | Python | JSON-column variant — same aggregate stored as one row with JSON dependents. Runnable: prints `Order total: $109.97`. |

## Concepts covered

- **Dependent objects have local identity** — `line_items` is keyed by `(order_id, line_no)`, no global UUID per line.
- **One transaction per save** — partial writes would leave the aggregate inconsistent.
- **Delete-then-insert** for child collections — handles orphan rows for free.
- **Orphan cleanup at the database level** — `ON DELETE CASCADE` makes "delete the aggregate" one statement.

## Try it

```bash
python order_mapper.py    # -> Order total: $109.97
sqlite3 orders.db < schema.sql
```
