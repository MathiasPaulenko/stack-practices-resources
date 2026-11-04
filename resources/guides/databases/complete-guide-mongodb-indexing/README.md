# Complete Guide to MongoDB Indexing - Code Examples

Index workflows from the guide:
<https://stackpractices.com/guides/complete-guide-mongodb-indexing/>

## Files

| File | What it shows |
| --- | --- |
| `indexes.js` | createIndex per type: ESR compound, covered, partial, TTL, text, 2dsphere, wildcard, hashed |
| `explain_plan.js` | reading executionStats: stages, keys/docs/returned ratios |
| `index_audit.js` | $indexStats + getIndexes + indexSizes + hide/unhide safety |
| `decide_index.py` | offline harness mapping query shapes to index types |
| `queries.json` | query-shape cases with expected index type |

## Offline check

```bash
python decide_index.py --verbose
```

The .js files run against a live MongoDB with `mongosh --file <name>.js`.
