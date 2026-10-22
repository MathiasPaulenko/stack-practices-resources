# Eager Loading Pattern — Companion Code

Runnable Eager Loading demos. Source:
<https://stackpractices.com/patterns/eager-loading-pattern/>

## Files

| File | Language | What it shows |
| --- | --- | --- |
| `eager_loading.py` | Python | Naive N+1 loop vs JOIN vs batch over `sqlite3`, with a `CountingConnection` that prints the query count for each strategy |
| `eager-loading.js` | JavaScript | Same three strategies on `node:sqlite` (Node ≥ 22.13), counting queries per strategy |
| `EagerLoadingDemo.java` | Java | Same structure; swaps JDBC for an in-memory table that counts "queries" so it runs with plain `javac`, no driver needed |

## Run

```bash
python eager_loading.py
node eager-loading.js
javac EagerLoadingDemo.java && java EagerLoadingDemo
```

Each one seeds 100 books and 2 authors, then runs the same repository
method three ways. Expected output looks like:

```text
     naive: 101 queries for 100 books
eager JOIN: 1 queries for 100 books
     batch: 2 queries for 100 books
Book 1 by Alice
```

## Notes

- The naive version is the point: watch the query count, not the latency.
  N+1 shows up as hundreds of small lookups, not one slow statement.
- JOIN is the right default for to-one relations; batch (`WHERE id IN`)
  avoids the cartesian product you get when joining to-many collections.
- The JDBC version in the article needs `sqlite-jdbc` on the classpath; the
  Java file here uses a fake table to stay dependency-free.
