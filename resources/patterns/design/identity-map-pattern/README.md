# Identity Map Pattern — Companion Code

Runnable Identity Map implementations. Source:
<https://stackpractices.com/patterns/identity-map-pattern/>

## Files

| File | Language | What it shows |
| --- | --- | --- |
| `identity_map.py` | Python | Identity map over `sqlite3` — note the `row_factory` line, without it rows arrive as tuples and `row["id"]` crashes |
| `identity-map.js` | JavaScript | Same structure against a minimal async db stand-in (shape matches `node:sqlite` / `sqlite`) |
| `IdentityMapDemo.java` | Java | Same structure; swaps JDBC for an in-memory table so it runs with plain `javac`, no driver needed |

## Run

```bash
python identity_map.py
node identity-map.js
javac IdentityMapDemo.java && java IdentityMapDemo
```

Each one loads `User(id=1)` twice and prints `true`: the second call comes
from the map, not the database. `find_all`/`findAll` also reuses the map,
which is the part people usually forget.

## Notes

- The map lives for one unit of work. Longer and it starts serving stale data.
- On rollback, drop the map — uncommitted objects don't belong in it.
- The JDBC version in the article needs `sqlite-jdbc` on the classpath; the
  Java file here uses a fake table to stay dependency-free.
