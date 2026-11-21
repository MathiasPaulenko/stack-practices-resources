# Merge JSON Files — Runnable Examples

Companion code for [Merge JSON Files](https://stackpractices.com/recipes/merge-json-files/) on StackPractices.

## Contents

- `src/merge_json.py` — Python: safe `deep_merge` (no input mutation), array concat, glob multi-merge, dedupe by key. Runs with stdlib only: `python src/merge_json.py`
- `src/mergeJson.js` — Node.js: `deepMerge` hardened against `null` and `__proto__`, array concat via `flatMap`, glob merge. `node src/mergeJson.js` (glob variant needs `npm i glob`)
- `src/JsonMerge.java` — Java + Jackson: recursive `JsonNode` merge for objects and arrays. Compile with `jackson-databind` on the classpath.

## Notes

- Deep merge is not symmetric: always merge files in a fixed, sorted order.
- The JS merge filters `__proto__`, `constructor`, and `prototype` keys to prevent prototype pollution.
