# Sort an Array — Companion Examples

Companion code for [Sort an Array](https://stackpractices.com/recipes/sort-array/).

Runnable versions of the recipe's tricky parts in three languages:

- **Multi-key sorting** — primary key plus deterministic tie-breaking (tuples, `||` chaining, `thenComparing`)
- **Numeric sorting** — the JavaScript `[10, 2].sort()` pitfall done right
- **Null handling** — `nullsLast` strategies that don't crash the comparator
- **Locale-aware ordering** — `localeCompare` / `locale.strxfrm` for user-facing strings

## Run

```bash
python -m pytest python/          # Python tests
npx vitest run javascript/        # JavaScript tests (vitest)
javac java/SortExamples.java && java -cp java SortExamples   # Java demo
```

Versión en español: [README.es.md](README.es.md)
